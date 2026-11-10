"""Upstream intelligence: detect, compare, report and (only with approval) adopt upstream changes.

Safety rules, enforced here:
- Upstream is fetched into refs/ceh/upstream/<branch>. Branches, working trees and origin refs are never touched,
  so local modifications cannot be overwritten.
- `sync` only moves CEH's pin, and only with explicit approval after a report exists for that exact commit.
  Every pin is kept, so any earlier one can be restored (`sync --to <commit>`).
"""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

from .sources import GIT_ENV, gh_api, git, git_copy_state, lab_dir, open_tree, remote_head
from .store import CehError, Registry, github_slug, now, policy, root, write_yaml

MANIFESTS = ("package.json", "package-lock.json", "requirements.txt", "pyproject.toml", "Cargo.toml", "go.mod")
FLAG_TEXT = {
    "up-to-date": "Upstream matches the pin",
    "unpinned": "No pinned commit recorded; run ceh inspect to pin",
    "new-commits": "Upstream has new commits",
    "new-release": "New release available",
    "security-update": "Security update available",
    "breaking": "Breaking update",
    "licence-changed": "Licence changed",
    "unmaintained": "No longer maintained",
    "archived": "Upstream archived",
    "unreachable": "Upstream unreachable or deleted",
    "local-conflict": "Local modifications plus upstream changes (heuristic signal)",
    "local-unverified": "Local copy state could not be verified",
    "rejected": "Update evaluated and rejected",
    "approved-not-integrated": "Update approved but not integrated",
    "integrated": "Update successfully integrated",
}


def default_branch(url: str) -> str | None:
    out = git("ls-remote", "--symref", url, "HEAD", check=False)
    m = re.search(r"ref: refs/heads/(\S+)\s+HEAD", out)
    return m.group(1) if m else None


def _up(rec: dict) -> dict:
    up = rec.get("upstream")
    if not up or not up.get("remote"):
        raise CehError(f"{rec['id']} has no git upstream (type {rec['type']})")
    return up


def _refresh_local_state(rec: dict) -> None:
    local = rec.setdefault("local", {"paths": []})
    states = {}
    for p in local.get("paths", []):
        path = Path(p).expanduser()
        state = git_copy_state(path) if path.is_dir() else {"git": False}
        if not state.get("git"):
            state["unverified"] = True
        states[p] = state
    local["state"] = states
    dirty = any(s.get("uncommitted_count", 0) for s in states.values())
    unknown = any(s.get("unverified") for s in states.values())
    local["modified"] = True if dirty else None if unknown else False


def check(rec: dict) -> dict:
    """Cheap remote check: ls-remote plus GitHub metadata. No objects are downloaded."""
    up = _up(rec)
    _refresh_local_state(rec)
    up["default_branch"] = up.get("default_branch") or default_branch(up["remote"])
    latest = remote_head(up["remote"], up.get("default_branch"))
    flags = []
    if not latest:
        flags.append("unreachable")
    elif up.get("pinned_commit") and latest != up["pinned_commit"]:
        flags.append("new-commits")
    elif latest == up.get("pinned_commit"):
        flags.append("up-to-date")
    else:
        flags.append("unpinned")
    slug = github_slug(up["remote"])
    if slug:
        repo = gh_api(f"repos/{slug}") or {}
        rel = gh_api(f"repos/{slug}/releases/latest")
        spdx = (repo.get("license") or {}).get("spdx_id")
        if spdx and rec.get("licence", {}).get("spdx") and spdx != rec["licence"]["spdx"] and rec["licence"]["source"] == "github-api":
            flags.append("licence-changed")
        if repo.get("archived"):
            flags.append("archived")
        if repo.get("pushed_at"):
            from .evaluate import _days_since
            if _days_since(repo["pushed_at"]) > policy()["evaluation"]["stale_days"]:
                flags.append("unmaintained")
        if rel and rel.get("tag_name") != (up.get("latest_release") or {}).get("tag"):
            if up.get("latest_release"):
                flags.append("new-release")
            up["latest_release"] = {"tag": rel.get("tag_name"), "published_at": rel.get("published_at")}
        adv = gh_api(f"repos/{slug}/security-advisories?state=published&per_page=5")
        if isinstance(adv, list) and adv:
            newest = max(a.get("published_at", "") for a in adv)
            if newest > (up.get("last_checked") or ""):
                flags.append("security-update")
    if rec.get("local", {}).get("modified") is None:
        flags.append("local-unverified")
    if rec.get("local", {}).get("modified") and "new-commits" in flags:
        flags.append("local-conflict")
    up["latest_commit"] = latest
    up["last_checked"] = now()
    up.setdefault("checks", []).append({"at": up["last_checked"], "latest": latest, "flags": flags})
    up["checks"] = up["checks"][-50:]
    up["flags"] = flags
    return {"id": rec["id"], "name": rec["name"], "pinned": up.get("pinned_commit"), "latest": latest, "flags": flags}


def _readable_repo(rec: dict) -> Path:
    """A git dir that can hold upstream history: the existing local copy, else the lab clone."""
    for p in rec.get("local", {}).get("paths", []):
        path = Path(p).expanduser()
        if (path / ".git").exists():
            return path
    lab = lab_dir(rec["id"])
    if not lab.exists():
        open_tree(rec, clone=True)
    return lab


def fetch(rec: dict) -> tuple[Path, str]:
    up = _up(rec)
    branch = up.get("default_branch") or default_branch(up["remote"]) or "main"
    repo = _readable_repo(rec)
    args = ["fetch", "--quiet", "--filter=blob:limit=1m", up["remote"], f"+refs/heads/{branch}:refs/ceh/upstream/{branch}"]
    if git("rev-parse", "--is-shallow-repository", cwd=repo, check=False) == "true":
        args.insert(1, "--unshallow")
    git(*args, cwd=repo)
    return repo, git("rev-parse", f"refs/ceh/upstream/{branch}", cwd=repo)


def _blob(repo: Path, rev: str, path: str) -> str | None:
    r = subprocess.run(["git", "cat-file", "blob", f"{rev}:{path}"], cwd=repo, env=GIT_ENV, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def diff(rec: dict) -> dict:
    """What changed between the pin and the latest upstream commit, and what in CEH and Video Factory it touches."""
    up = _up(rec)
    _refresh_local_state(rec)
    repo, latest = fetch(rec)
    pin = up.get("pinned_commit")
    if not pin:
        raise CehError(f"{rec['id']} has no pinned commit; run `ceh inspect {rec['id']}` first")
    if subprocess.run(["git", "cat-file", "-e", f"{pin}^{{commit}}"], cwd=repo, env=GIT_ENV).returncode:
        raise CehError(f"pinned commit {pin[:10]} is not in upstream history (force-push or wrong pin)")
    log = git("log", "--format=%H%x09%ad%x09%s", "--date=short", f"{pin}..{latest}", cwd=repo).splitlines()
    commits = [dict(zip(("sha", "date", "subject"), l.split("\t", 2), strict=False)) for l in log]
    changes = [l.split("\t") for l in git("diff", "--name-status", "--no-renames", pin, latest, cwd=repo).splitlines()]
    files = [{"status": c[0], "path": c[-1]} for c in changes]
    paths = {f["path"] for f in files}
    breaking = [c for c in commits if re.search(r"BREAKING|^\w+(\(.+\))?!:", c["subject"])]
    lic_changed = [p for p in paths if re.match(r"(licen[cs]e|copying)", Path(p).name, re.I)]
    manifests = {}
    for m in (p for p in paths if Path(p).name in MANIFESTS and "node_modules" not in p):
        if Path(m).name == "package.json":
            old, new = (json.loads(_blob(repo, r, m) or "{}") for r in (pin, latest))
            od, nd = {**old.get("dependencies", {}), **old.get("peerDependencies", {})}, {**new.get("dependencies", {}), **new.get("peerDependencies", {})}
            manifests[m] = {"version": [old.get("version"), new.get("version")],
                            "added": sorted(set(nd) - set(od)), "removed": sorted(set(od) - set(nd)),
                            "changed": {k: [od[k], nd[k]] for k in set(od) & set(nd) if od[k] != nd[k]}}
            ov, nv = old.get("version"), new.get("version")
            if ov and nv and ov.split(".")[0] != nv.split(".")[0]:
                breaking.append({"sha": "", "date": "", "subject": f"{m}: major version {ov} -> {nv}"})
        else:
            manifests[m] = {"changed": True}
    result = {
        "id": rec["id"], "pinned": pin, "latest": latest, "at": now(),
        "commits": commits[:200], "commit_count": len(commits),
        "files_changed": len(files), "deleted": [f["path"] for f in files if f["status"] == "D"][:100],
        "breaking": breaking, "licence_files_changed": lic_changed, "manifests": manifests,
        "impacted_skills": impacted_skills(rec["id"]), "impacted_video_factory": impacted_video_factory(rec),
        "local_modifications": {p: None if s.get("unverified") else s.get("uncommitted_count", 0)
                                for p, s in rec.get("local", {}).get("state", {}).items()},
    }
    return result


def impacted_skills(rid: str) -> list[str]:
    from .store import read_yaml
    return sorted(p.parent.name for p in (root() / "library" / "skills").glob("*/skill.yaml")
                  if rid in [s.get("ceh_id") for s in (read_yaml(p) or {}).get("sources", [])])


def impacted_video_factory(rec: dict) -> list[str]:
    from .integrate import catalog
    hits = [f"CEH catalog entry {e['id']}" for e in catalog()["entries"] if e["id"] == rec["id"]]
    vf = Path(policy().get("video_factory", {}).get("path", "~/git/video-factory")).expanduser()
    for rel in ("package.json", "config/upstream-skills.lock.json", "research/tool-catalog.yaml"):
        p = vf / rel
        if p.exists() and (github_slug(rec["url"]) or rec["url"]).lower() in p.read_text().lower():
            hits.append(f"video-factory/{rel}")
    hits += [f"video-factory/{u}" for u in rec.get("video_factory_usage", [])]
    return sorted(set(hits))


def report(rec: dict, reg: Registry, run_tests: bool = False) -> dict:
    d = diff(rec)
    if run_tests and d["impacted_video_factory"]:
        from .integrate import run_vf_tests
        d["regression"] = run_vf_tests()
    up = rec["upstream"]
    up["last_report"] = {k: d[k] for k in ("at", "pinned", "latest", "commit_count", "files_changed", "licence_files_changed")}
    up["last_report"]["breaking"] = len(d["breaking"])
    up["last_report"]["regression"] = d.get("regression", {}).get("result") if d.get("regression") else None
    out = root() / "reports" / rec["id"]
    out.mkdir(parents=True, exist_ok=True)
    (out / f"upstream-diff-{d['latest'][:10]}.json").write_text(json.dumps(d, indent=2))
    reg.save(rec)
    (out / "upstream-analysis.md").write_text(f"# {rec['id']} · {rec['name']}\n\n{rec['url']}\n\n" + analysis_markdown(rec, d))
    return d


def analysis_markdown(rec: dict, d: dict | None = None) -> str:
    up = rec.get("upstream") or {}
    if not up.get("remote"):
        return "Not a git resource; no upstream tracking.\n"
    lines = ["| Field | Value |\n|---|---|",
             *(f"| {k} | {v} |" for k, v in (
                 ("Strategy", up.get("strategy")), ("Remote", up.get("remote")), ("Default branch", up.get("default_branch")),
                 ("Pinned commit", up.get("pinned_commit")), ("Latest observed", up.get("latest_commit")),
                 ("Latest release", (up.get("latest_release") or {}).get("tag")), ("Forks", ", ".join(up.get("forks", [])) or "—"),
                 ("Last checked", up.get("last_checked")), ("Flags", ", ".join(FLAG_TEXT.get(f, f) for f in up.get("flags", [])) or "—")))]
    md = "\n".join(lines) + "\n"
    md += ("\n## Assessment scope\n\n"
           "- Local modification flags are heuristic signals, not proof of a merge conflict. "
           "No merge or semantic overlap analysis was performed.\n"
           "- Compatibility: UNKNOWN for the proposed upstream revision until targeted regression and rendered QA evidence exists.\n"
           "- Security: UNKNOWN for the proposed revision; advisory flags and historical scans are not a new-revision audit.\n"
           "- Licence suitability: UNKNOWN for the proposed revision until code, bundled assets and transitive terms are reviewed.\n"
           "- Breaking signals use commit subjects and package major versions; deleted files are observations, "
           "not verified deleted features. No semantic API compatibility analysis is claimed.\n")
    if d:
        md += f"\n## Change summary {d['pinned'][:10]} → {d['latest'][:10]}\n\n{d['commit_count']} commits, {d['files_changed']} files changed.\n\n"
        md += f"- Exact old commit: `{d['pinned']}`\n- Exact proposed commit: `{d['latest']}`\n"
        slug = github_slug(up["remote"])
        if slug:
            compare_url = f"https://github.com/{slug}/compare/{d['pinned']}...{d['latest']}"
            md += f"- [Source comparison]({compare_url})\n\n"
        else:
            md += f"- Source remote: `{up['remote']}`; inspect the exact git comparison above.\n\n"
        md += "### Breaking signals\n" + ("\n".join(f"- {c['sha'][:8]} {c['subject']}" for c in d["breaking"]) or "- none detected") + "\n\n"
        md += "### Licence files changed\n" + ("\n".join(f"- {p}" for p in d["licence_files_changed"]) or "- none") + "\n\n"
        md += "### Dependency manifests\n```json\n" + json.dumps(d["manifests"], indent=2) + "\n```\n\n"
        md += "### Deleted files\n" + ("\n".join(f"- {p}" for p in d["deleted"][:30]) or "- none") + "\n\n"
        md += "### Impact\n" + f"- CEH skills: {', '.join(d['impacted_skills']) or 'none'}\n" \
              f"- Video Factory: {', '.join(d['impacted_video_factory']) or 'none'}\n" \
              f"- Local modifications (left untouched): {d['local_modifications'] or 'none'}\n"
        if d.get("regression"):
            md += f"- Video Factory regression: {d['regression']['result']} (`{d['regression']['command']}`)\n"
        md += "\n### Recent commits\n" + "\n".join(f"- {c['date']} {c['sha'][:8]} {c['subject']}" for c in d["commits"][:40]) + "\n"
        md += ("\n### Required verification\n"
               "- Inspect changed APIs, renamed/deleted features and each downstream skill or adapter named above.\n"
               "- Review new-revision dependency, security and licence evidence; inspect assets separately.\n"
               "- Run `uv run pytest -q` in CEH; run the configured VF regression suite for affected VF components.\n"
               "- Run an isolated representative render with the proposed revision, compare visual/audio QA and record exact versions.\n"
               "- A passing installed VF baseline does not verify the proposed upstream revision.\n")
        md += (f"\n### Recommendation and rollback\nKeep the current pin `{d['pinned']}`. "
               "Review and verify the proposed revision before requesting adoption. No adoption is performed by this report.\n"
               f"After explicit adoption, CEH pin rollback is `ceh upstream sync {rec['id']} --approve --to {d['pinned']}`. "
               "This restores CEH metadata only; restore the separately reviewed consumer catalog and configuration if those "
               "were changed, then rerun regressions. Working trees and production pins are never merged automatically.\n")
    return md


def sync(rec: dict, reg: Registry, *, approve: bool, to: str | None = None, note: str = "") -> dict:
    """Move CEH's pin. Requires --approve. Never merges, never touches a working tree or local commits."""
    up = _up(rec)
    if not approve:
        raise CehError("sync changes the pinned version; re-run with --approve after reading the report")
    known = [p["commit"] for p in up.get("pins", [])]
    if to:
        target = next((c for c in known if c.startswith(to)), None)
        if not target:
            target = to if (up.get("last_report") or {}).get("latest", "").startswith(to) else None
        if not target:
            raise CehError(f"{to} is neither an earlier pin nor the reported latest commit")
    else:
        rep = up.get("last_report")
        if not rep or rep.get("latest") != up.get("latest_commit"):
            raise CehError(f"no report for the latest upstream commit; run `ceh upstream report {rec['id']}` first")
        target = rep["latest"]
    prev = up.get("pinned_commit")
    up["pinned_commit"] = target
    up["pins"].append({"commit": target, "previous": prev, "at": now(), "by": "ceh upstream sync", "note": note,
                       "strategy": up["strategy"]})
    guidance = {
        "PINNED": "CEH pin moved. Consumers that read the pin pick it up on their next install.",
        "TRACKED": "CEH pin moved to the tracked branch head.",
        "FORKED": "Pin moved. Your fork was NOT changed: merge refs/ceh/upstream/<branch> into it yourself, then re-run tests.",
        "VENDORED": "Pin moved. The vendored copy was NOT changed: update it deliberately and review the diff.",
    }[up["strategy"]]
    reg.save(rec)
    return {"id": rec["id"], "from": prev, "to": target, "guidance": guidance}


def status(reg: Registry) -> list[dict]:
    return [{"id": r["id"], "name": r["name"], "strategy": r["upstream"].get("strategy"),
             "pinned": (r["upstream"].get("pinned_commit") or "")[:10], "latest": (r["upstream"].get("latest_commit") or "")[:10],
             "flags": r["upstream"].get("flags", []), "checked": r["upstream"].get("last_checked")}
            for r in reg.all() if (r.get("upstream") or {}).get("remote")]


def weekly_report(results: list[dict]) -> Path:
    """Concise digest of a --all check: only resources whose flags need attention."""
    out = root() / "reports" / "upstream"
    out.mkdir(parents=True, exist_ok=True)
    stamp = now()[:10]
    attention = [r for r in results if set(r["flags"]) - {"up-to-date"}]
    md = [f"# Upstream check {stamp}\n", f"{len(results)} tracked resources, {len(attention)} need attention.\n"]
    for r in attention:
        md.append(f"- **{r['id']} {r['name']}**: {', '.join(FLAG_TEXT.get(f, f) for f in r['flags'])}"
                  f" (pinned {str(r['pinned'])[:10]}, latest {str(r['latest'])[:10]})")
    md.append("\nNext: `ceh upstream report <id>` for any of these. Nothing has been updated.")
    path = out / f"{stamp}.md"
    path.write_text("\n".join(md) + "\n")
    write_yaml(out / "latest.yaml", {"at": now(), "results": results})
    return path
