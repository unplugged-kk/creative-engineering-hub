"""Registry storage: one YAML file per resource under registry/resources/, plus the data-driven taxonomy."""
from __future__ import annotations

import datetime as dt
import os
import re
from functools import lru_cache
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import yaml


class CehError(Exception):
    pass


def root() -> Path:
    if os.environ.get("CEH_ROOT"):
        return Path(os.environ["CEH_ROOT"]).expanduser().resolve()
    return Path(__file__).resolve().parent.parent


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def read_yaml(path: Path):
    return yaml.safe_load(path.read_text()) if path.exists() else None


def write_yaml(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=120))


@lru_cache(maxsize=None)
def _data(rel: str, ceh_root: str):
    return read_yaml(Path(ceh_root) / rel) or {}


def data(rel: str) -> dict:
    """Taxonomy and policy files, e.g. data('registry/capabilities.yaml')."""
    return _data(rel, str(root()))


def policy() -> dict:
    return data("policies/policy.yaml")


# ---------- URLs ----------

_TRACKING = re.compile(r"^(utm_.*|si|feature|ref|ref_src|fbclid|gclid)$")


def normalize_url(url: str) -> str:
    """Canonical form used for storage and duplicate detection."""
    url = url.strip()
    if m := re.match(r"^git@github\.com:(.+)$", url):
        url = "https://github.com/" + m.group(1)
    if url.startswith("/"):
        url = "file://" + url
    if url.startswith("file://"):
        return url.rstrip("/")
    if not re.match(r"^[a-z]+://", url):
        if re.fullmatch(r"[\w.-]+/[\w.-]+", url):  # owner/repo shorthand
            url = "https://github.com/" + url
        else:
            url = "https://" + url
    p = urlsplit(url)
    host = p.netloc.lower().removeprefix("www.")
    path = re.sub(r"/+$", "", p.path)
    if host == "github.com":
        parts = [x for x in path.split("/") if x]
        if len(parts) >= 2:
            return f"https://github.com/{parts[0]}/{parts[1].removesuffix('.git')}"
        return f"https://github.com/{'/'.join(parts)}"
    if host == "youtu.be":
        return f"https://youtube.com/watch?v={path.strip('/')}"
    if host in ("youtube.com", "m.youtube.com") and path == "/watch":
        v = dict(parse_qsl(p.query)).get("v", "")
        return f"https://youtube.com/watch?v={v}"
    query = urlencode([(k, v) for k, v in parse_qsl(p.query) if not _TRACKING.match(k)])
    return urlunsplit(("https", host, path or "/", query, ""))


def url_key(url: str) -> str:
    return normalize_url(url).lower()


def github_slug(url: str) -> str | None:
    m = re.match(r"https://github\.com/([^/]+/[^/]+)$", normalize_url(url))
    return m.group(1) if m else None


# ---------- registry ----------

class Registry:
    def __init__(self, base: Path | None = None):
        self.dir = (base or root()) / "registry" / "resources"

    def path(self, rid: str) -> Path:
        return self.dir / f"{rid}.yaml"

    def all(self) -> list[dict]:
        return [read_yaml(p) for p in sorted(self.dir.glob("CEH-*.yaml"))]

    def get(self, ref: str) -> dict:
        """Look up by CEH id, URL, owner/repo or name."""
        if re.fullmatch(r"CEH-\d+", ref, re.I):
            rec = read_yaml(self.path(ref.upper()))
            if rec:
                return rec
        else:
            hit = self.find_duplicate(ref) if ("/" in ref or "." in ref) else None
            if hit:
                return hit
            named = [r for r in self.all() if r["name"].lower() == ref.lower() or r["name"].split("/")[-1].lower() == ref.lower()]
            if len(named) == 1:
                return named[0]
            if len(named) > 1:
                raise CehError(f"'{ref}' is ambiguous: {', '.join(r['id'] for r in named)}")
        raise CehError(f"no resource '{ref}'")

    def save(self, rec: dict) -> None:
        rec["updated"] = now()
        write_yaml(self.path(rec["id"]), rec)

    def next_id(self) -> str:
        nums = [int(p.stem.split("-")[1]) for p in self.dir.glob("CEH-*.yaml")]
        return f"CEH-{max(nums, default=0) + 1:04d}"

    def find_duplicate(self, url: str) -> dict | None:
        """Same canonical URL, a known fork, or a recorded alias (e.g. a renamed repo)."""
        key = url_key(url)
        for rec in self.all():
            keys = [rec["url"], *rec.get("aliases", []), *rec.get("upstream", {}).get("forks", [])]
            if key in {url_key(k) for k in keys}:
                return rec
        return None


def set_status(rec: dict, to: str, *, by: str, note: str = "", gate_ok: str | None = None) -> None:
    """Move a record through the lifecycle. Gated states demand the command that owns them."""
    lc = policy()["lifecycle"]
    if to not in lc["states"]:
        raise CehError(f"unknown lifecycle state {to}; valid: {', '.join(lc['states'])}")
    owner = lc["gated"].get(to)
    if owner and gate_ok != owner:
        raise CehError(f"{to} can only be set by `ceh {owner}`, which checks the licence and security gates")
    frm = rec.get("status")
    rec["status"] = to
    rec.setdefault("history", []).append({"at": now(), "from": frm, "to": to, "by": by, "note": note})
