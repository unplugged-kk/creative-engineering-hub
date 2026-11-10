"""`ceh add` and `ceh inspect`: register a resource, then read it statically in the lab."""
from __future__ import annotations

from pathlib import Path

from . import analyze
from .sources import Tree, find_local_copies, git, git_copy_state, github_meta, open_tree, remote_head
from .store import CehError, Registry, github_slug, normalize_url, now, set_status

ACTIVE = ("PRODUCTION", "APPROVED", "CANDIDATE")


def add(url: str, *, type_hint: str | None = None, note: str = "", inspect_now: bool = True,
        reg: Registry | None = None, by: str = "ceh add") -> tuple[dict, bool]:
    """Register a URL. Returns (record, created). An existing record is returned untouched."""
    reg = reg or Registry()
    url = normalize_url(url)
    dup = reg.find_duplicate(url)
    if dup:
        return dup, False
    meta = github_meta(url) if github_slug(url) else {}
    aliases = []
    if meta.get("full_name") and meta["full_name"].lower() != github_slug(url).lower():
        aliases.append(url)  # renamed or transferred upstream; keep the old URL as an alias
        url = f"https://github.com/{meta['full_name']}"
        dup = reg.find_duplicate(url)
        if dup:
            return dup, False
    elif meta.get("full_name"):
        url = f"https://github.com/{meta['full_name']}"
    rec = {
        "id": reg.next_id(),
        "name": github_slug(url) or url.split("://", 1)[-1],
        "url": url,
        "aliases": aliases,
        "type": type_hint,
        "type_manual": type_hint,  # an explicit --type survives re-inspection
        "status": None,
        "created": now(),
        "description": meta.get("description", ""),
        "capabilities": [],
        "local": {"paths": find_local_copies(url) if url.startswith(("https://github.com/", "file://")) else []},
        "upstream": {"strategy": "PINNED", "remote": url, "default_branch": meta.get("default_branch"),
                     "forks": [], "pins": []} if github_slug(url) or url.startswith("file://") else {},
        "meta": meta,
        "notes": [note] if note else [],
    }
    set_status(rec, "DISCOVERED", by=by, note=note)
    reg.save(rec)
    if inspect_now:
        rec = inspect(rec["id"], reg=reg, type_hint=type_hint)
    return rec, True


def inspect(ref: str, *, reg: Registry | None = None, type_hint: str | None = None, vulns: bool = True) -> dict:
    """Read the resource (local copy first, else an isolated lab clone) and fill in every static field."""
    reg = reg or Registry()
    rec = reg.get(ref)
    readable = bool(rec.get("upstream")) or bool(rec.get("local", {}).get("paths"))
    first = rec["status"] == "DISCOVERED" and readable  # websites and asset libraries stay DISCOVERED: metadata only
    if first:
        set_status(rec, "INSPECTING", by="ceh inspect")
    if rec["url"].startswith("https://github.com/") and not rec["meta"]:
        rec["meta"] = github_meta(rec["url"])
    tree = open_tree(rec, clone=True)
    files = [f for f, _ in tree.files()] if tree else []
    text = analyze.corpus(tree, rec["meta"], rec["name"])
    cls = analyze.classify(text, rec["url"], files, type_hint or rec.get("type_manual"))
    rec["type"] = cls["type"]
    # Manually curated capabilities (ceh tag) always survive re-inspection.
    rec["capabilities"] = list(dict.fromkeys(cls["capabilities"][:8] + rec.get("capabilities_manual", [])))
    rec["licence"] = analyze.licence(tree, rec["meta"])
    rec["dependencies"] = analyze.dependencies(tree)
    rec["security"] = analyze.security(tree, rec["dependencies"], check_vulns=vulns)
    rec["compatibility"] = analyze.compatibility(text, files)
    rec["files"] = {"count": len(files), "skills": sorted(f for f in files if f.endswith("SKILL.md"))[:40]}
    _record_copies(rec, tree)
    rec["alternatives"] = alternatives(rec, reg)
    rec["recommendation"] = recommend_action(rec)
    rec["inspected"] = now()
    if first:
        set_status(rec, "SANDBOXED" if tree else "INSPECTING", by="ceh inspect",
                   note="read statically in the lab; nothing executed" if tree else "no readable copy")
    reg.save(rec)
    return rec


def _record_copies(rec: dict, tree: Tree | None) -> None:
    """Pinned commit, local modifications and the latest upstream commit. Never touches a working tree."""
    up = rec.get("upstream")
    local = rec.setdefault("local", {"paths": []})
    local["state"] = {p: git_copy_state(Path(p).expanduser()) for p in local.get("paths", []) if Path(p).expanduser().is_dir()}
    local["modified"] = any(s.get("uncommitted_count") for s in local["state"].values())
    head = git("rev-parse", tree.ref, cwd=tree.path, check=False) if tree and tree.ref else None
    rec["analysed_commit"] = head
    if not up:
        return
    if head and not up.get("pinned_commit"):
        up["pinned_commit"] = head
        up["pins"].append({"commit": head, "at": now(), "by": "ceh inspect", "note": "commit read at inspection"})
    up["latest_commit"] = remote_head(up["remote"], up.get("default_branch"))
    up["latest_release"] = rec["meta"].get("latest_release")
    up["last_checked"] = now()


def alternatives(rec: dict, reg: Registry) -> list[dict]:
    mine = set(rec.get("capabilities", []))
    out = []
    for other in reg.all():
        if other["id"] == rec["id"] or not mine:
            continue
        shared = mine & set(other.get("capabilities", []))
        if shared:
            out.append({"id": other["id"], "name": other["name"], "status": other["status"],
                        "shared": sorted(shared), "overlap": round(len(shared) / len(mine), 2)})
    out.sort(key=lambda a: (a["status"] not in ACTIVE, -a["overlap"]))
    return out[:8]


def recommend_action(rec: dict) -> str:
    lic, sec = rec["licence"], rec["security"]
    if lic["gate"] == "block":
        return f"RESTRICT: {lic['spdx']} forbids commercial use. Reference the method only; never copy code or assets."
    if sec["gate"] == "block":
        return "DO NOT RUN: high-severity security findings. Review reports/<id>/security.md before anything else."
    active = [a for a in rec.get("alternatives", []) if a["status"] in ACTIVE and a["overlap"] >= 0.5]
    if active:
        return (f"COMPARE before adopting: overlaps {active[0]['name']} ({active[0]['status']}) on "
                f"{', '.join(active[0]['shared'])}. Run `ceh compare {rec['id']} {active[0]['id']}`.")
    gates = [g for g, v in (("licence", lic["gate"]), ("security", sec["gate"])) if v == "review"]
    tail = f" Gates needing review: {', '.join(gates)}." if gates else ""
    return f"EVALUATE: no active capability covers this. Run `ceh evaluate {rec['id']}`.{tail}"


def require(rec: dict, *states: str) -> None:
    if rec["status"] not in states:
        raise CehError(f"{rec['id']} is {rec['status']}; this needs one of {', '.join(states)}")
