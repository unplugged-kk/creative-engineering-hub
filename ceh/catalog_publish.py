"""Export the v2 consumer view without granting approvals or mutating lifecycle."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from . import catalog as contract
from .integrate import catalog as legacy_catalog
from .store import CehError, Registry, now, read_yaml, root


def skill_digest(directory: Path) -> str:
    """Bind guidance and metadata, excluding the release envelope to avoid self-reference."""
    if directory.is_symlink():
        raise CehError("skill bundle root is a symlink")
    chunks = []
    for path in sorted(directory.rglob("*")):
        if path.is_symlink():
            raise CehError("skill bundle contains symlinks")
        if path.is_file():
            payload = path.read_bytes()
            if path.name == "skill.yaml" and path.parent == directory:
                metadata = read_yaml(path)
                metadata.pop("catalog_release", None)
                metadata.pop("approval", None)
                payload = json.dumps(metadata, sort_keys=True, separators=(",", ":")).encode()
            chunks.append((path.relative_to(directory).as_posix(), hashlib.sha256(payload).hexdigest()))
    return hashlib.sha256(json.dumps(chunks, separators=(",", ":")).encode()).hexdigest()


def export_catalog(reg: Registry, path: Path) -> dict:
    """Only previously published resource approvals plus reviewed skill releases qualify."""
    entries, excluded = [], []
    for published in legacy_catalog()["entries"]:
        rec = reg.get(published["id"])
        try:
            approval = rec.get("approval", {})
            pin = rec.get("upstream", {}).get("pinned_commit")
            if rec["status"] != "PRODUCTION" or not approval or approval.get("pinned_commit") != pin:
                raise CehError("missing current explicit resource approval")
            if rec["licence"]["gate"] != "pass" or rec["security"]["gate"] != "pass":
                raise CehError("v2 release requires passing licence and security gates")
            if not rec.get("library_skills"):
                raise CehError("no reviewed canonical skill release")
            for name in rec["library_skills"]:
                if not isinstance(name, str) or not contract.ID.fullmatch(name) or "/" in name or name in (".", ".."):
                    raise CehError("invalid canonical skill name")
                directory = root() / "library" / "skills" / name
                meta = read_yaml(directory / "skill.yaml") or {}
                skill_approval = meta.get("approval", {})
                if skill_approval.get("status") != "APPROVED" or skill_approval.get("production_eligible") is not True:
                    raise CehError("canonical skill is not explicitly approved for production")
                bundle_digest = skill_digest(directory)
                if skill_approval.get("version") != meta.get("version") or skill_approval.get("digest") != bundle_digest:
                    raise CehError("skill version or bytes differ from approved release")
                if skill_approval.get("by") != approval.get("by") or skill_approval.get("at") != approval.get("at"):
                    raise CehError("skill approval actor/time do not match resource approval")
                release = meta.get("catalog_release", {})
                entry = release.get("entry")
                if not isinstance(entry, dict):
                    raise CehError("canonical skill has no independently reviewed catalog_release.entry")
                entry = dict(entry)
                if skill_approval.get("catalog_entry_digest") != contract.digest(entry):
                    raise CehError("catalog metadata differs from approved release")
                if entry.get("id") != name or entry.get("version") != meta.get("version"):
                    raise CehError("skill identity/version differs from reviewed release")
                refs = entry.get("skills", [])
                if refs != [{"name": name, "version": meta["version"], "digest": skill_digest(directory)}]:
                    raise CehError("skill bytes differ from reviewed release")
                sources = entry.get("resources", [])
                if not isinstance(sources, list) or not all(isinstance(s, dict) for s in sources):
                    raise CehError("invalid release provenance")
                for source in sources:
                    source_rec = reg.get(source.get("id", ""))
                    if source.get("url") != source_rec["url"] or source.get("pinned_commit") != source_rec.get("upstream", {}).get("pinned_commit"):
                        raise CehError("source URL/pin differs from registry")
                    if source_rec.get("licence", {}).get("gate") != "pass" or source_rec.get("security", {}).get("gate") != "pass":
                        raise CehError("source review gates do not pass")
                if not any(s.get("id") == rec["id"] and s.get("pinned_commit") == pin for s in sources):
                    raise CehError("release provenance does not bind resource pin")
                approved = entry.get("approval", {})
                if approved.get("by") != approval.get("by") or approved.get("at") != approval.get("at"):
                    raise CehError("release approval does not match resource approval")
                # Never manufacture approval or evidence; only seal the independently reviewed release.
                entries.append(contract.seal_entry(entry))
        except (CehError, KeyError, TypeError, AttributeError) as exc:
            excluded.append({"id": rec["id"], "reason": str(exc)})
    doc = contract.seal_catalog(entries, generated=now())
    if errors := contract.validate_catalog(doc):
        raise CehError("catalog release invalid: " + "; ".join(errors))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, indent=2, allow_nan=False) + "\n")
    return {"path": str(path), "entries": len(entries), "digest": doc["digest"], "excluded": excluded}
