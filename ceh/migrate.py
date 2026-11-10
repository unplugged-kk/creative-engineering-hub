"""`ceh migrate`: turn intake/historical/leads.yaml into registry records and a migration report.

Idempotent: an existing record is refreshed, never duplicated. Historical facts (pins, decisions, statuses) are kept
as recorded; live facts (licence, latest commit, security) come from a fresh static inspection.
"""
from __future__ import annotations

import json
from pathlib import Path

from .evaluate import evaluate
from .intake import add, inspect
from .sources import find_local_copies, scan_local_clones
from .store import Registry, now, policy, read_yaml, root, set_status, url_key


def migrate(leads_file: Path | None = None, *, reg: Registry | None = None, inspect_now: bool = True, log=print) -> Path:
    reg = reg or Registry()
    leads_file = leads_file or root() / "intake" / "historical" / "leads.yaml"
    doc = read_yaml(leads_file)
    sources = doc.get("evidence_sources", {})
    rows, failures = [], []
    for lead in doc["leads"]:
        try:
            rec, created = add(lead["url"], type_hint=lead.get("type"), inspect_now=False, reg=reg, by="ceh migrate",
                               note=lead.get("note", ""))
            _apply_history(rec, lead, sources, created)
            reg.save(rec)
            if inspect_now:
                rec = inspect(rec["id"], reg=reg, type_hint=lead.get("type"))
                rec = evaluate(rec["id"], reg=reg, promote=False)
            rows.append(rec)
            log(f"{rec['id']} {rec['name']:55} {rec['status']:11} {(rec.get('licence') or {}).get('spdx')}")
        except Exception as e:  # one bad lead must not stop the batch; it is reported under "Failed leads"
            failures.append({"url": lead["url"], "error": str(e)[:300]})
            log(f"FAILED {lead['url']}: {e}")
    return write_report(rows, failures, doc, reg)


def _apply_history(rec: dict, lead: dict, sources: dict, created: bool) -> None:
    rec["historical"] = {
        "group": lead.get("group"), "previous_decision": lead.get("previous"),
        "evidence": [sources.get(e, e) for e in lead.get("evidence", [])], "note": lead.get("note"),
    }
    if lead.get("vf_usage"):
        rec["video_factory_usage"] = lead["vf_usage"]
    paths = [str(Path(p).expanduser()) for p in lead.get("local", [])] + find_local_copies(rec["url"])
    rec["local"]["paths"] = list(dict.fromkeys(rec["local"].get("paths", []) + paths))
    up = rec.get("upstream")
    if up:
        up["strategy"] = lead.get("strategy", up.get("strategy", "PINNED"))
        up["forks"] = sorted(set(up.get("forks", [])) | set(lead.get("forks", [])))
        if lead.get("pinned") and not any(p["commit"] == lead["pinned"] for p in up["pins"]):
            up["pinned_commit"] = lead["pinned"]
            up["pins"].append({"commit": lead["pinned"], "at": now(), "by": "ceh migrate",
                               "note": "pin recorded by earlier research: " + ", ".join(lead.get("evidence", []))})
    if created and lead.get("status") and lead["status"] != rec["status"]:
        gate = policy()["lifecycle"]["gated"].get(lead["status"])
        set_status(rec, lead["status"], by="ceh migrate", gate_ok=gate,
                   note="recorded from historical evidence" + (f" ({lead['previous']})" if lead.get("previous") else ""))


def _vf_inventory() -> dict:
    vf = Path(policy()["video_factory"]["path"]).expanduser()
    inv: dict = {"path": str(vf)}
    cs = vf / "config" / "creative-skills.json"
    if cs.exists():
        d = json.loads(cs.read_text())
        inv["creative_skills"] = {"bundle": d.get("bundle"), "count": len(d.get("skills", []))}
    caps = vf / "config" / "capabilities.json"
    if caps.exists():
        c = json.loads(caps.read_text())["capabilities"]
        inv["capabilities"] = {"count": len(c), "kinds": sorted({x["id"].split(":")[0] for x in c})}
    inv["project_skills"] = sorted(p.name for p in (vf / ".claude" / "skills").glob("*") if p.is_dir())
    inv["renderer_adapters"] = sorted(p.stem for p in (vf / "contentos" / "renderers").glob("*.py")
                                      if p.stem not in ("__init__", "base", "registry"))
    inv["vendor"] = sorted(p.name for p in (vf / "vendor").glob("*") if p.is_dir())
    lock = vf / "config" / "upstream-skills.lock.json"
    if lock.exists():
        inv["upstream_lock"] = [{k: s.get(k) for k in ("id", "tag", "commit", "skills")} for s in json.loads(lock.read_text())["sources"]]
    pkg = vf / "package.json"
    if pkg.exists():
        inv["npm_pins"] = json.loads(pkg.read_text()).get("dependencies", {})
    return inv


def write_report(rows: list[dict], failures: list[dict], doc: dict, reg: Registry) -> Path:
    out = root() / "reports" / "historical-migration"
    out.mkdir(parents=True, exist_ok=True)
    recs = reg.all()
    by_key = {url_key(r["url"]): r for r in recs}
    inv = _vf_inventory()
    clones = scan_local_clones()
    dup_clones = {k: v for k, v in clones.items() if len(v) > 1}
    lines = ["# Historical migration report\n", f"Generated {now()} by `ceh migrate`.\n",
             f"{len(rows)} leads registered, {len(failures)} failed, {len(doc.get('unresolved', []))} unresolved.\n",
             "## Inventory\n",
             "| ID | Name | Type | Group | Previous decision | CEH status | Licence | Pinned | Latest | Local copies | Local mods | Upstream | Recommended action |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: r["id"]):
        up = r.get("upstream") or {}
        h = r.get("historical", {})
        pinned, latest = (up.get("pinned_commit") or "")[:8], (up.get("latest_commit") or "")[:8]
        drift = "—" if not up else "unreachable" if not latest else "same" if pinned == latest else "new commits"
        lines.append(f"| {r['id']} | [{r['name']}]({r['url']}) | {r['type']} | {h.get('group')} | {h.get('previous_decision') or '—'} "
                     f"| {r['status']} | {r['licence']['spdx']} ({r['licence']['gate']}) | {pinned or '—'} | {latest or '—'} "
                     f"| {len(r['local'].get('paths', []))} | {'yes' if r['local'].get('modified') else 'no'} | {drift} "
                     f"| {r['recommendation'].split(':')[0]} |")
    lines += ["\n## Recovered pins\n"]
    for r in rows:
        for p in (r.get("upstream") or {}).get("pins", []):
            if p["by"] == "ceh migrate":
                lines.append(f"- {r['id']} {r['name']}: `{p['commit']}` ({p['note']})")
    lines += ["\n## Forks and duplicates\n", "### User forks (recorded on the upstream record, not registered twice)"]
    lines += [f"- {r['id']} {r['name']}: {', '.join(r['upstream']['forks'])}" for r in rows if (r.get("upstream") or {}).get("forks")]
    lines += ["\n### Near-duplicate groups (same method)"]
    for g in doc.get("duplicate_groups", []):
        ids = [by_key.get(url_key("https://github.com/" + m), {}).get("id", "?") for m in g["members"]]
        lines.append(f"- **{g['name']}**: {', '.join(f'{i} {m}' for i, m in zip(ids, g['members'], strict=False))}. {g['note']}")
    lines += ["\n### Duplicate local clones (same origin cloned more than once)"]
    lines += [f"- {k}: " + "; ".join(v) for k, v in sorted(dup_clones.items())] or ["- none"]
    lines += ["\n## Video Factory first-party inventory (accounted for, not re-registered)\n",
              "```json", json.dumps(inv, indent=2), "```",
              "\nThese are Video Factory's own skills and adapters. CEH does not copy or replace them; upstream sources they "
              "depend on are registered above with `video_factory_usage`."]
    lines += ["\n## Failed leads\n"] + ([f"- {f['url']}: {f['error']}" for f in failures] or ["- none"])
    lines += ["\n## Unresolved (manual investigation)\n"] + [f"- **{u['name']}**: {u['reason']}" for u in doc.get("unresolved", [])]
    lines += ["\n## Method\n",
              "- Leads come from intake/historical/leads.yaml, each citing the file it was recovered from.",
              "- Live facts: GitHub API via `gh`, `git ls-remote`, and a static read of an existing local clone or a "
              "`--no-checkout` lab clone. No resource code was installed or executed.",
              "- Statuses reflect earlier decisions; nothing was promoted by this migration."]
    path = out / "REPORT.md"
    path.write_text("\n".join(lines) + "\n")
    (out / "inventory.json").write_text(json.dumps(
        [{k: r.get(k) for k in ("id", "name", "url", "type", "status", "historical", "capabilities", "recommendation")} |
         {"licence": r["licence"]["spdx"], "pinned": (r.get("upstream") or {}).get("pinned_commit"),
          "latest": (r.get("upstream") or {}).get("latest_commit"), "local": r["local"].get("paths")} for r in rows],
        indent=2, default=str))
    return path
