"""Capability search, side-by-side comparison and brief-driven recommendation."""
from __future__ import annotations

from . import analyze
from .store import Registry, data

STATUS_RANK = {"PRODUCTION": 1.0, "APPROVED": 0.95, "CANDIDATE": 0.8, "TESTING": 0.7, "SANDBOXED": 0.6,
               "INSPECTING": 0.5, "DISCOVERED": 0.5, "PARKED": 0.4, "DEPRECATED": 0.2, "RESTRICTED": 0.1, "REJECTED": 0.05}
UNUSABLE = {"REJECTED", "RESTRICTED", "DEPRECATED"}


def capabilities_for(text: str) -> list[str]:
    """Capability ids named by, or keyword-matched in, free text ('festive-video', 'hand drawn Diwali reel')."""
    caps = data("registry/capabilities.yaml")["capabilities"]
    t = text.lower().strip()
    if t in caps:
        return [t]
    spaced = t.replace("-", " ")
    found = [c for c in caps if c.startswith(t) or spaced in c.replace("-", " ")]
    found += analyze.classify(spaced, "https://x", [], hint="technique")["capabilities"]
    return list(dict.fromkeys(found))


def search(query: str, reg: Registry, include_unusable: bool = False) -> list[dict]:
    wanted = set(capabilities_for(query))
    q = query.lower()
    rows = []
    for r in reg.all():
        if r["status"] in UNUSABLE and not include_unusable:
            continue
        shared = wanted & set(r.get("capabilities", []))
        text_hit = q in r["name"].lower() or q in (r.get("description") or "").lower()
        if not shared and not text_hit:
            continue
        score = (len(shared) * 10 + (3 if text_hit else 0)) * STATUS_RANK.get(r["status"], 0.3)
        rows.append({"id": r["id"], "name": r["name"], "status": r["status"], "type": r["type"],
                     "matched": sorted(shared), "licence": (r.get("licence") or {}).get("spdx"),
                     "score": round(score, 2)})
    return sorted(rows, key=lambda x: -x["score"])


def compare(ids: list[str], reg: Registry) -> dict:
    recs = [reg.get(i) for i in ids]
    caps = [set(r.get("capabilities", [])) for r in recs]
    common = set.intersection(*caps) if caps else set()
    rows = []
    for r, c in zip(recs, caps, strict=False):
        ev = r.get("evaluation", {})
        rows.append({
            "id": r["id"], "name": r["name"], "status": r["status"], "type": r["type"],
            "licence": f"{r['licence']['spdx']} ({r['licence']['class']})", "licence_gate": r["licence"]["gate"],
            "security_gate": r["security"]["gate"], "score": ev.get("weighted_score"),
            "coverage": ev.get("evidence_coverage"), "renderers": r["compatibility"]["renderers"],
            "agents": r["compatibility"]["agents"], "last_push": (r.get("meta") or {}).get("pushed_at"),
            "unique_capabilities": sorted(c - common),
        })
    return {"shared_capabilities": sorted(common), "resources": rows}


def recommend(brief: str, reg: Registry, *, renderer: str | None = None, agent: str | None = None,
              commercial: bool = True) -> dict:
    """Pick, per capability the brief needs, the best usable resource. Status and gates outrank popularity."""
    needed = capabilities_for(brief)
    plan, gaps = [], []
    for cap in needed:
        pool = []
        for r in reg.all():
            if cap not in r.get("capabilities", []) or r["status"] in UNUSABLE:
                continue
            if commercial and (r.get("licence") or {}).get("gate") == "block":
                continue
            if renderer and r["compatibility"]["renderers"] and renderer not in r["compatibility"]["renderers"]:
                continue
            if agent and r["type"] == "agent-skill" and agent not in r["compatibility"]["agents"] \
                    and "agent-skills-format" not in r["compatibility"]["agents"]:
                continue
            ev = (r.get("evaluation") or {}).get("weighted_score") or 0
            pool.append((STATUS_RANK.get(r["status"], 0.3) * 10 + ev, r))
        pool.sort(key=lambda x: -x[0])
        if not pool:
            gaps.append(cap)
            continue
        best = pool[0][1]
        plan.append({"capability": cap, "use": f"{best['id']} {best['name']}", "status": best["status"],
                     "why": f"{best['status']}, score {(best.get('evaluation') or {}).get('weighted_score')}, "
                            f"licence {best['licence']['spdx']}",
                     "alternatives": [f"{r['id']} {r['name']} ({r['status']})" for _, r in pool[1:4]],
                     "ready_for_production": best["status"] in ("PRODUCTION", "APPROVED")})
    return {"brief": brief, "capabilities": needed, "plan": plan, "gaps": gaps,
            "note": "Only PRODUCTION/APPROVED entries can be used by Video Factory; anything else needs evaluate + approve first."}
