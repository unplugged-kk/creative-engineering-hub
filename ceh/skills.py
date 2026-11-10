"""Universal skills library: one canonical skill per capability, exposed to every agent by symlink.

Agents differ only in where they look and which frontmatter keys they honour (registry/compatibility.yaml).
Installing never overwrites anything CEH did not create.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

import yaml

from .store import CehError, Registry, data, read_yaml, root, write_yaml

REQUIRED_DIRS = ("references", "scripts", "examples", "evals")


def lib() -> Path:
    return root() / "library" / "skills"


def agent_home() -> Path:
    return Path(os.environ.get("CEH_AGENT_HOME", "~")).expanduser()


def agents() -> dict:
    return data("registry/compatibility.yaml")["agents"]


def frontmatter(skill_md: Path) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", skill_md.read_text(), re.S)
    return (yaml.safe_load(m.group(1)) or {}) if m else {}


def all_skills() -> list[str]:
    return sorted(p.parent.name for p in lib().glob("*/skill.yaml"))


def validate(name: str, reg: Registry | None = None) -> list[str]:
    d = lib() / name
    problems = []
    if not (d / "SKILL.md").exists():
        return [f"{name}: SKILL.md missing"]
    fm, meta = frontmatter(d / "SKILL.md"), read_yaml(d / "skill.yaml") or {}
    if fm.get("name") != name:
        problems.append(f"{name}: SKILL.md name '{fm.get('name')}' must equal the directory name")
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", name):
        problems.append(f"{name}: name must be lowercase letters, digits and hyphens, at most 64 chars")
    desc = fm.get("description") or ""
    if not desc or len(desc) > 1024 or re.search(r"<[^>]+>", desc):
        problems.append(f"{name}: description must be 1-1024 chars with no XML tags")
    for k in ("name", "version", "description", "agents", "sources"):
        if k not in meta:
            problems.append(f"{name}: skill.yaml lacks '{k}'")
    if meta.get("name") != name:
        problems.append(f"{name}: skill.yaml name must equal the directory name")
    for a in meta.get("agents", []):
        if a not in agents():
            problems.append(f"{name}: unknown agent '{a}'")
        elif extra := set(fm) - set(agents()[a]["frontmatter"]):
            problems.append(f"{name}: frontmatter {sorted(extra)} not honoured by {a}")
    for sub in REQUIRED_DIRS:
        if not (d / sub).is_dir():
            problems.append(f"{name}: {sub}/ missing")
    if not any((d / "evals").glob("*")):
        problems.append(f"{name}: evals/ has no eval cases")
    reg = reg or Registry()
    for s in meta.get("sources", []):
        if s.get("ceh_id"):
            try:
                reg.get(s["ceh_id"])
            except CehError:
                problems.append(f"{name}: source {s['ceh_id']} is not in the registry")
    return problems


def _target(agent: str, name: str) -> Path:
    return agent_home() / agents()[agent]["home"] / name


def _ours(link: Path, name: str) -> bool:
    return link.is_symlink() and Path(os.path.realpath(link)) == (lib() / name).resolve()


def install(name: str, only: list[str] | None = None) -> list[dict]:
    meta = read_yaml(lib() / name / "skill.yaml")
    if not meta:
        raise CehError(f"no skill '{name}' in library/skills")
    if meta.get("status") == "disabled":
        raise CehError(f"{name} is disabled; `ceh skills enable {name}` first")
    if problems := validate(name):
        raise CehError("skill does not validate:\n  " + "\n  ".join(problems))
    results = []
    for a in only or meta["agents"]:
        if a not in meta["agents"]:
            raise CehError(f"{name} does not declare support for {a}")
        t = _target(a, name)
        if _ours(t, name):
            results.append({"agent": a, "path": str(t), "result": "already installed"})
        elif t.exists() or t.is_symlink():
            results.append({"agent": a, "path": str(t), "result": "skipped: something else is already there"})
        elif not t.parent.is_dir():
            results.append({"agent": a, "path": str(t), "result": f"skipped: {t.parent} does not exist (agent not set up)"})
        else:
            t.symlink_to(lib() / name, target_is_directory=True)
            results.append({"agent": a, "path": str(t), "result": "installed"})
    return results


def uninstall(name: str) -> list[str]:
    removed = []
    for a in agents():
        t = _target(a, name)
        if _ours(t, name):
            t.unlink()
            removed.append(str(t))
    return removed


def set_enabled(name: str, enabled: bool) -> dict:
    p = lib() / name / "skill.yaml"
    meta = read_yaml(p)
    if not meta:
        raise CehError(f"no skill '{name}'")
    meta["status"] = "active" if enabled else "disabled"
    write_yaml(p, meta)
    removed = [] if enabled else uninstall(name)
    return {"name": name, "status": meta["status"], "unlinked": removed}


def listing() -> list[dict]:
    rows = []
    for name in all_skills():
        meta = read_yaml(lib() / name / "skill.yaml")
        rows.append({"name": name, "version": meta.get("version"), "status": meta.get("status", "active"),
                     "installed": [a for a in agents() if _ours(_target(a, name), name)],
                     "sources": [s.get("ceh_id") for s in meta.get("sources", [])]})
    return rows
