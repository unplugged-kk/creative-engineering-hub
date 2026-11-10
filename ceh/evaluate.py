"""`ceh evaluate`: weighted scores plus independent licence and security gates, written as reports."""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path, PurePosixPath

from .sources import open_tree
from .store import Registry, now, policy, root, set_status

PRE_EVAL = ("DISCOVERED", "INSPECTING", "SANDBOXED", "TESTING")


def _days_since(iso: str | None) -> int | None:
    if not iso:
        return None
    return (dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(iso.replace("Z", "+00:00"))).days


def auto_scores(rec: dict) -> dict[str, dict]:
    """Each criterion: {score 0-5 or None, basis}. None means no evidence; it is reported, never guessed."""
    s: dict[str, dict] = {}
    files = []
    tree = open_tree(rec, clone=False)
    if tree:
        files = [f for f, _ in tree.files()]
    top = {PurePosixPath(f).parts[0].lower() for f in files if "/" in f}
    readme = next((f for f in files if PurePosixPath(f).name.lower() == "readme.md" and "/" not in f), None)
    readme_len = len(tree.read(readme) or "") if tree and readme else 0

    parts = [bool(rec["files"]["skills"]), bool(top & {"scripts", "bin", "src", "lib"}),
             bool(top & {"examples", "example", "demo", "samples", "templates"}), bool(top & {"tests", "test", "evals", "__tests__"})]
    s["workflow_completeness"] = {"score": 1 + sum(parts), "basis": "skills, scripts, examples, tests present: " + str(parts)} if tree else \
        {"score": None, "basis": "no readable copy"}
    reuse = {"agent-skill": 4, "renderer": 4, "npm-package": 4, "python-package": 4, "template": 3, "workflow": 3,
             "mcp-server": 4, "repository": 3, "tutorial": 2, "website": 1, "technique": 2, "asset-library": 3}
    s["reusability"] = {"score": reuse.get(rec["type"]), "basis": f"resource type {rec['type']}"}
    agents = rec["compatibility"]["agents"]
    s["agent_compatibility"] = {"score": min(5, len(agents) + (2 if "agent-skills-format" in agents else 0)),
                                "basis": f"agents detected: {', '.join(agents) or 'none'}"}
    days = _days_since(rec.get("meta", {}).get("pushed_at"))
    if rec.get("meta", {}).get("archived"):
        s["maintainability"] = {"score": 0, "basis": "upstream archived"}
    elif days is None:
        s["maintainability"] = {"score": None, "basis": "no push date"}
    else:
        s["maintainability"] = {"score": 5 if days < 30 else 4 if days < 90 else 3 if days < 180 else 2 if days < 365 else 1,
                                "basis": f"last push {days} days ago"}
    s["documentation"] = {"score": 5 if readme_len > 8000 else 4 if readme_len > 3000 else 3 if readme_len > 1000 else 2 if readme_len else 0,
                          "basis": f"top-level README {readme_len} chars"} if tree else {"score": None, "basis": "no readable copy"}
    s["licence_suitability"] = {"score": {"permissive": 5, "copyleft": 2, "custom": 1, "unknown": 1, "non-commercial": 0}[rec["licence"]["class"]],
                                "basis": f"{rec['licence']['spdx']} ({rec['licence']['class']})"}
    s["security"] = {"score": {"low": 5, "medium": 3, "high": 0}.get(rec["security"].get("worst"), None),
                     "basis": f"{rec['security'].get('finding_count', 0)} findings, worst {rec['security'].get('worst')}"}
    deps = rec.get("dependencies", {})
    n = len(deps.get("npm", {})) + len(deps.get("python", []))
    score = 5 if n == 0 else 4 if n < 10 else 3 if n < 30 else 2 if n < 100 else 1
    s["integration_complexity"] = {"score": max(0, score - (1 if deps.get("install_hooks") else 0)),
                                   "basis": f"{n} runtime dependencies; install hooks: {list(deps.get('install_hooks', {}))}"}
    for k in ("visual_quality", "performance"):
        s[k] = {"score": None, "basis": "needs a benchmark: render a sample and record it with --score"}
    return s


def evaluate(ref: str, *, scores: dict[str, float] | None = None, evidence: str = "", reg: Registry | None = None,
             promote: bool = True) -> dict:
    reg = reg or Registry()
    rec = reg.get(ref)
    ev = rec.setdefault("evaluation", {})
    manual = ev.setdefault("manual", {})
    for k, v in (scores or {}).items():
        if k not in policy()["evaluation"]["weights"]:
            raise ValueError(f"unknown criterion {k}")
        manual[k] = {"score": float(v), "basis": evidence or "manual score", "at": now()}
    crit = {**auto_scores(rec), **manual}
    weights = policy()["evaluation"]["weights"]
    scored = {k: c["score"] for k, c in crit.items() if c["score"] is not None}
    wsum = sum(weights[k] for k in scored)
    ev.update({
        "at": now(),
        "criteria": crit,
        "weighted_score": round(sum(weights[k] * v for k, v in scored.items()) / wsum, 2) if wsum else None,
        "evidence_coverage": round(wsum, 2),
        "gates": {"licence": rec["licence"]["gate"], "security": rec["security"]["gate"]},
    })
    if rec["status"] in PRE_EVAL + ("PARKED", "CANDIDATE") and rec["licence"]["gate"] == "block":
        # A fact, not a promotion: applies on every evaluation, including during migration.
        set_status(rec, "RESTRICTED", by="ceh evaluate", note=f"licence {rec['licence']['spdx']} blocks commercial use")
    elif promote and rec["status"] in PRE_EVAL:
        if rec["security"]["gate"] != "block":
            set_status(rec, "CANDIDATE", by="ceh evaluate", note=f"score {ev['weighted_score']} at coverage {ev['evidence_coverage']}")
    reg.save(rec)
    write_reports(rec)
    return rec


# ---------- reports ----------

def _bullets(items) -> str:
    return "\n".join(f"- {i}" for i in items) or "- none"


def write_reports(rec: dict) -> Path:
    from .upstream import analysis_markdown
    out = root() / "reports" / rec["id"]
    out.mkdir(parents=True, exist_ok=True)
    ev = rec.get("evaluation", {})
    lic, sec, deps, comp = rec["licence"], rec["security"], rec.get("dependencies", {}), rec["compatibility"]
    head = f"# {rec['id']} · {rec['name']}\n\n{rec['url']}\n\n"
    hist = "\n".join(f"- {h['at']} {h['from']} → {h['to']} ({h['by']}) {h.get('note', '')}" for h in rec.get("history", []))
    crit = ev.get("criteria", {})
    table = "\n".join(f"| {k} | {policy()['evaluation']['weights'][k]} | {'—' if c['score'] is None else c['score']} | {c['basis']} |"
                      for k, c in crit.items())
    reports = {
        "overview.md": head + f"**Type:** {rec['type']}  \n**Status:** {rec['status']}  \n**Description:** {rec.get('description') or '—'}\n\n"
                       f"**Capabilities:** {', '.join(rec['capabilities']) or 'none detected'}\n\n"
                       f"**Weighted score:** {ev.get('weighted_score')} (evidence covers {ev.get('evidence_coverage')} of the weight)\n\n"
                       f"## Notes\n{_bullets(rec.get('notes', []))}\n\n## Lifecycle\n{hist}\n",
        "technical-analysis.md": head + f"Files: {rec['files']['count']}  \nSkills found:\n{_bullets(rec['files']['skills'])}\n\n"
                                        f"Language: {rec.get('meta', {}).get('language')}  \nStars: {rec.get('meta', {}).get('stars')}\n\n"
                                        f"## Local copies\n" + _bullets(f"{p}: HEAD {s.get('head', '—')[:10]}, {s.get('uncommitted_count', 0)} uncommitted"
                                                                     for p, s in rec.get("local", {}).get("state", {}).items()),
        "capabilities.md": head + f"## Detected capabilities\n{_bullets(rec['capabilities'])}\n\n## Alternatives in CEH\n"
                                  + _bullets(f"{a['id']} {a['name']} ({a['status']}) shares {', '.join(a['shared'])}" for a in rec.get("alternatives", [])),
        "dependency-analysis.md": head + "```json\n" + json.dumps(deps, indent=2) + "\n```\n",
        "licensing.md": head + f"**Code licence:** {lic['spdx']} (class: {lic['class']}, source: {lic['source']})  \n**Gate:** {lic['gate']}\n\n"
                               f"## Bundled assets (separate from the code licence)\n```json\n{json.dumps(lic['assets'], indent=2)}\n```\n\n"
                               f"## Notes\n{_bullets(lic['notes'])}\n\nThis is a reading of licence files, not legal advice.\n",
        "security.md": head + f"**Gate:** {sec['gate']} (worst finding: {sec.get('worst')})  \nScanned files: {sec.get('scanned_files')}\n\n"
                              f"## Findings\n" + _bullets(f"[{f['severity']}] {f['kind']} — {f['path']}" for f in sec["findings"])
                              + f"\n\n## Notes\n{_bullets(sec.get('notes', []))}\n\nStatic scan only. No resource code was installed or executed.\n",
        "compatibility.md": head + f"## Agents\n{_bullets(comp['agents'])}\n\n## Renderers\n{_bullets(comp['renderers'])}\n",
        "benchmark.md": head + "| Criterion | Weight | Score | Basis |\n|---|---|---|---|\n" + table + "\n\n"
                               "Visual quality and performance need a rendered sample. Put outputs under lab/benchmarks/<id>/ and record them with\n"
                               f"`ceh evaluate {rec['id']} --score visual_quality=N --evidence lab/benchmarks/{rec['id']}/...`.\n",
        "upstream-analysis.md": head + analysis_markdown(rec),
        "recommendation.md": head + f"**{rec['recommendation']}**\n\nLicence gate: {lic['gate']} · Security gate: {sec['gate']} · "
                                    f"Score: {ev.get('weighted_score')}\n\nAdding to CEH never integrates into Video Factory. "
                                    f"That needs `ceh approve {rec['id']}` and then `ceh integrate {rec['id']}`.\n",
    }
    for name, body in reports.items():
        (out / name).write_text(body)
    (out / "evaluation.json").write_text(json.dumps({k: rec.get(k) for k in
        ("id", "name", "url", "type", "status", "capabilities", "licence", "security", "compatibility", "evaluation", "recommendation")},
        indent=2, default=str))
    return out
