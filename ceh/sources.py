"""Read-only access to upstream sources: git, the GitHub API (via `gh`), and file trees.

Nothing here executes code from a resource. Lab clones are made with --no-checkout and read blob by blob,
so not even a git checkout hook or a large binary lands on disk.
"""
from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from .store import CehError, github_slug, policy, root

SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build", ".next", "target"}
GIT_ENV = {**os.environ, "GIT_NO_LAZY_FETCH": "1", "GIT_TERMINAL_PROMPT": "0"}


def git(*args, cwd: Path | None = None, check: bool = True) -> str:
    r = subprocess.run(["git", *args], cwd=cwd, env=GIT_ENV, capture_output=True, text=True, timeout=600)
    if check and r.returncode:
        raise CehError(f"git {' '.join(args)} failed: {r.stderr.strip()[:400]}")
    return r.stdout.strip()


def gh_api(path: str) -> dict | None:
    """GitHub REST via the user's `gh` login. None when offline, unauthenticated or 404."""
    if os.environ.get("CEH_OFFLINE"):
        return None
    try:
        r = subprocess.run(["gh", "api", path], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return json.loads(r.stdout) if r.returncode == 0 and r.stdout.strip() else None


def remote_head(url: str, branch: str | None = None) -> str | None:
    out = git("ls-remote", url, f"refs/heads/{branch}" if branch else "HEAD", check=False)
    return out.split()[0] if out else None


def github_meta(url: str) -> dict:
    """Live repository facts. Keys absent when unknown; never guessed."""
    slug = github_slug(url)
    repo = gh_api(f"repos/{slug}") if slug else None
    if not repo:
        return {}
    meta = {
        "full_name": repo["full_name"],
        "description": repo.get("description") or "",
        "topics": repo.get("topics", []),
        "licence_spdx": (repo.get("license") or {}).get("spdx_id"),
        "default_branch": repo.get("default_branch"),
        "pushed_at": repo.get("pushed_at"),
        "archived": repo.get("archived", False),
        "stars": repo.get("stargazers_count"),
        "is_fork": repo.get("fork", False),
        "parent": (repo.get("parent") or {}).get("html_url"),
        "language": repo.get("language"),
    }
    rel = gh_api(f"repos/{slug}/releases/latest")
    if rel:
        meta["latest_release"] = {"tag": rel.get("tag_name"), "published_at": rel.get("published_at")}
    return meta


# ---------- trees ----------

@dataclass
class Tree:
    """Uniform read access to a git commit (no checkout) or a plain directory."""
    path: Path
    ref: str | None = None  # git revision; None means read the working directory
    _batch: subprocess.Popen | None = field(default=None, repr=False, compare=False)

    def files(self) -> list[tuple[str, int]]:
        if self.ref:
            out = git("ls-tree", "-r", "-l", self.ref, cwd=self.path)
            rows = []
            for line in out.splitlines():
                meta, name = line.split("\t", 1)
                parts = meta.split()
                if parts[1] == "blob":
                    # "BAD" = blob left out by the partial clone because it is over the size filter
                    rows.append((name, int(parts[3]) if parts[3].isdigit() else 1 << 40))
            return rows
        rows = []
        for dirpath, dirs, names in os.walk(self.path):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for n in names:
                p = Path(dirpath) / n
                try:
                    rows.append((str(p.relative_to(self.path)), p.stat().st_size))
                except OSError:
                    pass
        return rows

    def _git_blob(self, name: str) -> bytes | None:
        """One long-lived `git cat-file --batch` per tree: thousands of reads without thousands of processes."""
        if self._batch is None:
            self._batch = subprocess.Popen(["git", "cat-file", "--batch"], cwd=self.path, env=GIT_ENV,
                                           stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        b = self._batch
        b.stdin.write(f"{self.ref}:{name}\n".encode())
        b.stdin.flush()
        header = b.stdout.readline().decode().split()
        if len(header) != 3:  # "<obj> missing" (or ambiguous): absent from the partial clone
            return None
        raw = b.stdout.read(int(header[2]))
        b.stdout.read(1)  # trailing newline
        return raw if header[1] == "blob" else None

    def read(self, name: str, limit: int | None = None) -> str | None:
        limit = limit or policy()["security"]["max_blob_bytes"]
        try:
            if self.ref:
                raw = self._git_blob(name)
            else:
                p = self.path / name
                raw = p.read_bytes() if p.stat().st_size <= limit else None
        except OSError:
            return None
        if raw is None or len(raw) > limit or b"\0" in raw[:8000]:
            return None
        return raw.decode("utf-8", "replace")

    def __del__(self):
        if getattr(self, "_batch", None):
            self._batch.kill()


def lab_dir(rid: str) -> Path:
    return root() / "lab" / "clones" / rid


_CLONES: dict[str, dict[str, list[str]]] = {}


def scan_local_clones() -> dict[str, list[str]]:
    """{canonical url key: [paths]} for every git clone under the configured roots (depth 5). Cached per process."""
    from .store import url_key
    env_roots = os.environ.get("CEH_LOCAL_ROOTS")
    roots = env_roots.split(os.pathsep) if env_roots is not None else policy()["local_copies"]["roots"]
    cache_key = os.pathsep.join(roots)
    if cache_key in _CLONES:
        return _CLONES[cache_key]
    found: dict[str, list[str]] = {}
    for r in filter(None, roots):
        base = Path(r).expanduser()
        if not base.is_dir():
            continue
        for dirpath, dirs, _ in os.walk(base):
            depth = len(Path(dirpath).relative_to(base).parts)
            if ".git" in dirs:
                origin = git("config", "--get", "remote.origin.url", cwd=Path(dirpath), check=False)
                if origin:
                    found.setdefault(url_key(origin), []).append(str(Path(dirpath)))
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".") and depth < 5]
    _CLONES[cache_key] = {k: sorted(set(v)) for k, v in found.items()}
    return _CLONES[cache_key]


def find_local_copies(url: str) -> list[str]:
    """Existing clones on this machine whose origin is exactly this URL (user forks are recorded separately)."""
    from .store import url_key
    return scan_local_clones().get(url_key(url), [])


def open_tree(rec: dict, *, clone: bool = True) -> Tree | None:
    """The best readable copy of a resource: an existing local copy first, else an isolated lab clone."""
    for p in rec.get("local", {}).get("paths", []):
        path = Path(p).expanduser()
        if path.is_dir():
            return Tree(path, "HEAD" if (path / ".git").exists() else None)
    lab = lab_dir(rec["id"])
    if (lab / ".git").exists() or (lab / "HEAD").exists():
        return Tree(lab, "HEAD")
    if not clone or not rec["url"].startswith(("https://github.com/", "file://", "/")):
        return None
    lab.parent.mkdir(parents=True, exist_ok=True)
    git("clone", "--quiet", "--no-checkout", "--depth", "1", "--filter=blob:limit=1m", rec["url"], str(lab))
    return Tree(lab, "HEAD")


def git_copy_state(path: Path) -> dict:
    """HEAD, branch and uncommitted changes of an existing local clone. Reads only."""
    if not (path / ".git").exists():
        return {"git": False}
    dirty = git("status", "--porcelain", cwd=path, check=False).splitlines()
    return {
        "git": True,
        "head": git("rev-parse", "HEAD", cwd=path, check=False),
        "branch": git("rev-parse", "--abbrev-ref", "HEAD", cwd=path, check=False),
        "origin": git("config", "--get", "remote.origin.url", cwd=path, check=False),
        "uncommitted": dirty[:50],
        "uncommitted_count": len(dirty),
    }
