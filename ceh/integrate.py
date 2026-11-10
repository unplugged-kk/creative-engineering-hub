"""Approval gates and the Video Factory integration layer.

CEH never edits Video Factory. It publishes integrations/video-factory/catalog.json, which lists only resources that
passed `ceh approve` (licence and security gates) and then `ceh integrate`. Video Factory reads that file.
"""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

from .intake import require
from .store import CehError, Registry, now, policy, root, set_status

CATALOG_SCHEMA = "ceh-video-factory-catalog/1"


def _catalog_path() -> Path:
    return root() / "integrations" / "video-factory" / "catalog.json"


def catalog() -> dict:
    p = _catalog_path()
    return json.loads(p.read_text()) if p.exists() else {"schema": CATALOG_SCHEMA, "entries": []}


def approve(ref: str, *, reg: Registry, licence_note: str = "", security_note: str = "", by: str = "user") -> dict:
    """Gate check, then APPROVED. A blocking gate cannot be overridden; a review gate needs a written note."""
    rec = reg.get(ref)
    require(rec, "CANDIDATE", "TESTING", "SANDBOXED", "PARKED")
    if not rec.get("evaluation"):
        raise CehError(f"{rec['id']} has no evaluation; run `ceh evaluate {rec['id']}` first")
    lic, sec = rec["licence"], rec["security"]
    if lic["gate"] == "block":
        raise CehError(f"licence {lic['spdx']} is {lic['class']}: never approvable for commercial production")
    if sec["gate"] == "block":
        raise CehError("high-severity security findings block approval; see reports/" + rec["id"] + "/security.md")
    if lic["gate"] == "review" and not licence_note:
        raise CehError(f"licence {lic['spdx']} ({lic['class']}) needs review: pass --licence-reviewed \"<what you checked>\"")
    if sec["gate"] == "review" and not security_note:
        raise CehError(f"{sec.get('finding_count')} security findings need review: pass --security-reviewed \"<what you checked>\"")
    rec["approval"] = {"at": now(), "by": by, "licence_note": licence_note, "security_note": security_note,
                       "pinned_commit": (rec.get("upstream") or {}).get("pinned_commit")}
    set_status(rec, "APPROVED", by=by, note="gates passed", gate_ok="approve")
    reg.save(rec)
    return rec


def integrate(ref: str, *, reg: Registry, run_tests: bool = False, by: str = "user") -> dict:
    """APPROVED -> PRODUCTION: publish a catalog entry for Video Factory. Optional regression run first."""
    rec = reg.get(ref)
    require(rec, "APPROVED")
    if run_tests:
        res = run_vf_tests()
        rec.setdefault("integration_tests", []).append(res)
        if res["result"] != "pass":
            reg.save(rec)
            raise CehError(f"Video Factory tests failed; {rec['id']} stays APPROVED. Output: {res['tail'][-600:]}")
    entry = {
        "id": rec["id"], "name": rec["name"], "url": rec["url"], "type": rec["type"],
        "capabilities": rec["capabilities"], "renderers": rec["compatibility"]["renderers"],
        "pinned_commit": (rec.get("upstream") or {}).get("pinned_commit"),
        "licence": {"spdx": rec["licence"]["spdx"], "class": rec["licence"]["class"], "note": rec["approval"]["licence_note"]},
        "skills": rec.get("library_skills", []),
        "approved": rec["approval"], "integrated_at": now(),
    }
    cat = catalog()
    cat["entries"] = [e for e in cat["entries"] if e["id"] != rec["id"]] + [entry]
    cat["entries"].sort(key=lambda e: e["id"])
    cat["generated"] = now()
    _catalog_path().parent.mkdir(parents=True, exist_ok=True)
    _catalog_path().write_text(json.dumps(cat, indent=2) + "\n")
    set_status(rec, "PRODUCTION", by=by, note="published to integrations/video-factory/catalog.json", gate_ok="integrate")
    reg.save(rec)
    return entry


def withdraw(ref: str, *, reg: Registry, to: str = "DEPRECATED", note: str = "", by: str = "user") -> dict:
    rec = reg.get(ref)
    cat = catalog()
    cat["entries"] = [e for e in cat["entries"] if e["id"] != rec["id"]]
    _catalog_path().write_text(json.dumps(cat, indent=2) + "\n")
    set_status(rec, to, by=by, note=note or "withdrawn from Video Factory catalog")
    reg.save(rec)
    return rec


def run_vf_tests() -> dict:
    vf = policy()["video_factory"]
    cwd = Path(vf["path"]).expanduser()
    cmd = [str(Path(c).expanduser()) if c.startswith("~") else c for c in vf["test_command"]]
    try:
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=1800)
        out, code = r.stdout + r.stderr, r.returncode
    except (OSError, subprocess.TimeoutExpired) as e:
        out, code = str(e), -1
    return {"at": now(), "command": " ".join(cmd), "result": "pass" if code == 0 else "fail", "tail": out[-2000:]}


# ---------- production artifact contract ----------

ARTIFACT_REQUIRED = ("manifest.json",)
ARTIFACT_OPTIONAL = ("preview.mp4", "assets", "sources.json", "render-log.json", "quality-report.json")


def check_artifact(project: Path) -> dict:
    """Validate a renderer's output folder against integrations/video-factory/artifact-contract.md."""
    problems, info = [], {}
    for f in ARTIFACT_REQUIRED:
        if not (project / f).exists():
            problems.append(f"missing {f}")
    manifest = {}
    if (project / "manifest.json").exists():
        try:
            manifest = json.loads((project / "manifest.json").read_text())
        except json.JSONDecodeError as e:
            problems.append(f"manifest.json invalid: {e}")
    for key in ("schema", "renderer", "output"):
        if manifest and key not in manifest:
            problems.append(f"manifest.json lacks '{key}'")
    output = project / manifest.get("output", "output.mp4")
    if not output.exists():
        problems.append(f"output {output.name} missing")
    elif shutil.which("ffprobe"):
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,width,height",
                            "-of", "json", str(output)], capture_output=True, text=True)
        if r.returncode:
            problems.append(f"ffprobe cannot read {output.name}")
        else:
            info["probe"] = json.loads(r.stdout)
    for f in ("sources.json", "render-log.json", "quality-report.json"):
        if (project / f).exists():
            try:
                json.loads((project / f).read_text())
            except json.JSONDecodeError:
                problems.append(f"{f} is not valid JSON")
    info["optional_present"] = [f for f in ARTIFACT_OPTIONAL if (project / f).exists()]
    return {"ok": not problems, "problems": problems, **info}
