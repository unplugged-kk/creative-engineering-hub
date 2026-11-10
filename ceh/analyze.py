"""Static analysis of a resource: type, capabilities, licence, dependencies, security, compatibility.

Pure reading. Untrusted code is never imported, installed or run.
"""
from __future__ import annotations

import json
import re
import tomllib
import urllib.request
from pathlib import PurePosixPath

from .sources import Tree
from .store import data, policy

TEXT_EXT = {".md", ".txt", ".py", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".json", ".yaml", ".yml", ".toml",
            ".sh", ".bash", ".zsh", ".html", ".css", ".env", ".cfg", ".ini", ".rb", ".go", ".rs", ".ps1", ""}
MEDIA_EXT = {".mp4", ".mov", ".webm", ".mp3", ".wav", ".m4a", ".ogg", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".lottie"}
FONT_EXT = {".ttf", ".otf", ".woff", ".woff2"}
MODEL_EXT = {".onnx", ".pt", ".pth", ".safetensors", ".bin", ".gguf", ".ckpt"}
BINARY_EXT = {".exe", ".dll", ".so", ".dylib", ".app", ".jar", ".wasm"}


def _kw_match(keyword: str, text: str) -> bool:
    return re.search(r"(?<![\w-])" + re.escape(keyword) + r"(?![\w-])", text) is not None


def corpus(tree: Tree | None, meta: dict, name: str) -> str:
    """The text classification reads: name, description, topics, README head, SKILL.md heads, package.json."""
    parts = [name.replace("/", " ").replace("-", " "), name, meta.get("description", ""), " ".join(meta.get("topics", []))]
    if tree:
        files = [f for f, _ in tree.files()]
        readmes = [f for f in files if PurePosixPath(f).name.lower() in ("readme.md", "readme") and f.count("/") <= 1]
        skills = [f for f in files if PurePosixPath(f).name == "SKILL.md"][:12]
        for f in sorted(readmes, key=len)[:2] + skills + (["package.json"] if "package.json" in files else []):
            parts.append((tree.read(f) or "")[:20000])
    return "\n".join(parts).lower()


HEAD_CHARS = 2500


def classify(text: str, url: str, files: list[str], hint: str | None = None) -> dict:
    tax = data("registry/capabilities.yaml")
    head = text[:HEAD_CHARS]
    caps = []
    for cid, c in tax["capabilities"].items():
        # A keyword in the name, description, topics or README opening counts 3; elsewhere 1. Keep at >= 3,
        # so one passing mention deep in a SKILL.md cannot assign a capability.
        score = sum(3 if _kw_match(k, head) else len(re.findall(r"(?<![\w-])" + re.escape(k) + r"(?![\w-])", text[HEAD_CHARS:]))
                    for k in c["keywords"])
        if score >= 3:
            caps.append((score, cid))
    caps = [cid for hits, cid in sorted(caps, key=lambda x: (-x[0], x[1]))]
    if hint:
        rtype = hint
    elif "youtube.com/watch" in url:
        rtype = "tutorial"
    elif not url.startswith(("https://github.com/", "file://", "/")):
        rtype = next((t for t, v in tax["resource_types"].items() if any(_kw_match(k, text) for k in v.get("keywords", []))), "website")
    elif any(_kw_match(k, head) for k in tax["resource_types"]["renderer"]["keywords"]) and "rendering" in caps:
        rtype = "renderer"
    elif any(PurePosixPath(f).name == "SKILL.md" and f.count("/") <= 2 for f in files):  # not a monorepo's nested docs
        rtype = "agent-skill"
    elif any(_kw_match(k, head) for k in tax["resource_types"]["mcp-server"]["keywords"]):
        rtype = "mcp-server"
    elif any(_kw_match(k, text[:3000]) for k in tax["resource_types"]["template"]["keywords"]):
        rtype = "template"
    else:
        rtype = "repository"
    return {"type": rtype, "capabilities": caps}


# ---------- licence ----------

_SPDX_TEXT = [
    ("AGPL-3.0", "gnu affero general public license"),
    ("LGPL-3.0", "gnu lesser general public license"),
    ("GPL-3.0", "gnu general public license\n                       version 3"),
    ("GPL-3.0", "gnu general public license version 3"),
    ("GPL-2.0", "gnu general public license version 2"),
    ("Apache-2.0", "apache license"),
    ("MPL-2.0", "mozilla public license version 2.0"),
    ("BSD-3-Clause", "neither the name of"),
    ("BSD-2-Clause", "redistributions in binary form must reproduce"),
    ("ISC", "permission to use, copy, modify, and/or distribute"),
    ("Unlicense", "this is free and unencumbered software"),
    ("MIT", "permission is hereby granted, free of charge"),
]


def licence_class(spdx: str | None) -> str:
    if not spdx or spdx in ("NOASSERTION", "NONE"):
        return "unknown"
    if spdx.startswith("Remotion"):
        return "custom"
    for cls, ids in policy()["licensing"]["classes"].items():
        if spdx in ids:
            return cls
    return "unknown"


def licence(tree: Tree | None, meta: dict) -> dict:
    files = [f for f, _ in tree.files()] if tree else []
    lic_files = [f for f in files if re.match(r"(licen[cs]e|copying)(\.md|\.txt)?$", PurePosixPath(f).name, re.I)]
    top = [f for f in lic_files if "/" not in f]
    spdx, source = meta.get("licence_spdx"), "github-api" if meta.get("licence_spdx") else None
    if spdx in (None, "NOASSERTION") and tree and top:
        text = (tree.read(top[0]) or "").lower()
        for fid, marks in policy()["licensing"]["fingerprints"].items():
            if any(m in text for m in marks):
                spdx, source = fid, f"fingerprint:{top[0]}"
                break
        else:
            for fid, mark in _SPDX_TEXT:
                if mark in text:
                    spdx, source = fid, f"text:{top[0]}"
                    break
    if spdx in (None, "NOASSERTION") and not top and tree:
        source = "no licence file"
    cls = licence_class(spdx)
    suffix = lambda exts: sum(PurePosixPath(f).suffix.lower() in exts for f in files)  # noqa: E731
    assets = {
        "media_files": suffix(MEDIA_EXT), "font_files": suffix(FONT_EXT), "model_files": suffix(MODEL_EXT),
        "nested_licence_files": [f for f in lic_files if "/" in f and "node_modules" not in f][:20],
    }
    notes = []
    if assets["media_files"] or assets["font_files"] or assets["model_files"]:
        notes.append("Bundled media, fonts or models may carry their own terms; the code licence does not cover them by default.")
    return {"spdx": spdx, "class": cls, "gate": policy()["licensing"]["gate"][cls], "source": source,
            "assets": assets, "notes": notes}


# ---------- dependencies ----------

def dependencies(tree: Tree | None) -> dict:
    if not tree:
        return {}
    files = {f for f, _ in tree.files()}
    out: dict = {"manifests": sorted(f for f in files if PurePosixPath(f).name in
                                     ("package.json", "requirements.txt", "pyproject.toml", "Cargo.toml", "go.mod")
                                     and f.count("/") <= 2 and "node_modules" not in f)}
    if "package.json" in files:
        try:
            pkg = json.loads(tree.read("package.json") or "{}")
            out["npm"] = {**pkg.get("dependencies", {}), **pkg.get("peerDependencies", {})}
            out["npm_dev"] = pkg.get("devDependencies", {})
            out["install_hooks"] = {k: v for k, v in pkg.get("scripts", {}).items()
                                    if k in ("preinstall", "install", "postinstall", "prepare")}
        except json.JSONDecodeError:
            out["npm_error"] = "package.json is not valid JSON"
    py = []
    if "requirements.txt" in files:
        py += [l.strip() for l in (tree.read("requirements.txt") or "").splitlines() if l.strip() and not l.startswith("#")]
    if "pyproject.toml" in files:
        try:
            py += tomllib.loads(tree.read("pyproject.toml") or "").get("project", {}).get("dependencies", [])
        except tomllib.TOMLDecodeError:
            out["python_error"] = "pyproject.toml does not parse"
    if py:
        out["python"] = py
    return out


def pinned_packages(tree: Tree | None) -> list[dict]:
    """Exact versions from lockfiles and == pins, for the OSV vulnerability lookup."""
    if not tree:
        return []
    files = {f for f, _ in tree.files()}
    pkgs = []
    if "package-lock.json" in files:
        try:
            lock = json.loads(tree.read("package-lock.json", limit=20_000_000) or "{}")
            for path, info in lock.get("packages", {}).items():
                if path.startswith("node_modules/") and info.get("version"):
                    pkgs.append({"ecosystem": "npm", "name": path.split("node_modules/")[-1], "version": info["version"]})
        except json.JSONDecodeError:
            pass
    for line in (tree.read("requirements.txt") or "").splitlines() if "requirements.txt" in files else []:
        m = re.match(r"^([A-Za-z0-9_.\-]+)==([\w.]+)", line.strip())
        if m:
            pkgs.append({"ecosystem": "PyPI", "name": m.group(1), "version": m.group(2)})
    return pkgs


def osv_lookup(pkgs: list[dict]) -> list[dict] | None:
    """Known vulnerabilities from osv.dev. None when the service could not be reached."""
    if not pkgs:
        return []
    import os
    if os.environ.get("CEH_OFFLINE"):
        return None
    found = []
    for i in range(0, min(len(pkgs), 3000), 1000):
        chunk = pkgs[i:i + 1000]
        body = json.dumps({"queries": [{"package": {"ecosystem": p["ecosystem"], "name": p["name"]}, "version": p["version"]}
                                       for p in chunk]}).encode()
        req = urllib.request.Request("https://api.osv.dev/v1/querybatch", body, {"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                results = json.load(r)["results"]
        except (OSError, ValueError, KeyError):
            return None
        for p, res in zip(chunk, results, strict=False):
            if res.get("vulns"):
                found.append({**p, "ids": [v["id"] for v in res["vulns"]][:10]})
    return found


# ---------- security ----------

SECRET_PATTERNS = [
    ("high", "private key", re.compile(r"-----BEGIN (RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----")),
    ("high", "AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("high", "GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b")),
    ("high", "Slack token", re.compile(r"\bxox[abpr]-[A-Za-z0-9-]{20,}")),
    ("high", "OpenAI/Anthropic key", re.compile(r"\bsk-(ant-)?[A-Za-z0-9_-]{32,}")),
    ("high", "Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("medium", "hardcoded credential", re.compile(
        r"(?i)\b(api[_-]?key|secret|token|password)\b\s*[:=]\s*['\"](?!your|xxx|<|\$\{|placeholder|changeme|example)[A-Za-z0-9_\-/+=]{24,}['\"]")),
]
SECRET_KINDS = {(sev, kind) for sev, kind, _ in SECRET_PATTERNS}
PLACEHOLDER = re.compile(r"(?i)example|dummy|fake|placeholder|redact|xxxx|this-is|test-?key|not-a-real")
TEST_PATH = re.compile(r"(?i)(^|/)(tests?|__tests__|fixtures?|spec|e2e)/|\.(test|spec)\.[a-z]+$")
DOC_PATH = re.compile(r"(?i)(^|/)(docs?|examples?|samples?)/|\.mdx?$")
RISKY_PATTERNS = [
    ("high", "obfuscated execution", re.compile(r"eval\s*\(\s*(atob|Buffer\.from)\(|base64\s+(-d|--decode)[^|\n]*\|\s*(ba)?sh")),
    ("medium", "pipe remote script to shell", re.compile(r"(curl|wget)\s[^|\n]*\|\s*(sudo\s+)?(ba|z)?sh\b")),
    ("medium", "privilege escalation", re.compile(r"(?m)^\s*sudo\s")),
]


def security(tree: Tree | None, deps: dict, check_vulns: bool = True) -> dict:
    if not tree:
        return {"gate": "review", "findings": [], "scanned_files": 0, "notes": ["no readable copy; nothing scanned"]}
    findings, scanned, skipped = [], 0, 0
    for name, size in tree.files():
        suffix = PurePosixPath(name).suffix.lower()
        if suffix in BINARY_EXT:
            findings.append({"severity": "medium", "kind": "committed binary", "path": name})
            continue
        if suffix not in TEXT_EXT or "node_modules/" in name or name.endswith((".min.js", "package-lock.json")):
            continue
        text = tree.read(name) if size <= policy()["security"]["max_blob_bytes"] else None
        if text is None:
            skipped += 1
            continue
        scanned += 1
        soft_path = TEST_PATH.search(name) or DOC_PATH.search(name)
        for sev, kind, rx in SECRET_PATTERNS + RISKY_PATTERNS:
            for m in rx.finditer(text):
                finding_sev, finding_kind = sev, kind
                if (sev, kind) in SECRET_KINDS and PLACEHOLDER.search(m.group(0)):
                    continue  # documented example keys, e.g. AKIAIOSFODNN7EXAMPLE
                line_text = text[text.rfind("\n", 0, m.start()) + 1:m.start()].lstrip()
                if (sev, kind) in SECRET_KINDS and (soft_path or line_text.startswith(("*", "//", "#", "<!--"))):
                    # tests, docs and comments: worth a human look, not proof of a leaked credential
                    finding_sev, finding_kind = "medium", f"secret-shaped string in test, docs or comment ({kind})"
                line = text.count("\n", 0, m.start()) + 1
                findings.append({"severity": finding_sev, "kind": finding_kind, "path": f"{name}:{line}"})
    for hook, cmd in deps.get("install_hooks", {}).items():
        findings.append({"severity": "medium", "kind": f"npm {hook} hook runs on install", "path": f"package.json: {cmd[:120]}"})
    notes = [f"{skipped} large or binary files not scanned"] if skipped else []
    if check_vulns:
        vulns = osv_lookup(pinned_packages(tree))
        if vulns is None:
            notes.append("dependency vulnerability lookup (osv.dev) unavailable")
        else:
            for v in vulns:
                findings.append({"severity": "medium", "kind": "known vulnerability",
                                 "path": f"{v['ecosystem']}:{v['name']}@{v['version']} {', '.join(v['ids'])}"})
            notes.append(f"osv.dev checked {len(pinned_packages(tree))} pinned packages")
    worst = "high" if any(f["severity"] == "high" for f in findings) else "medium" if findings else "low"
    return {"gate": policy()["security"]["gate"][worst], "worst": worst, "findings": findings[:200],
            "finding_count": len(findings), "scanned_files": scanned, "notes": notes}


# ---------- compatibility ----------

def compatibility(text: str, files: list[str]) -> dict:
    names = {PurePosixPath(f).name for f in files}
    agents = []
    for aid, a in data("registry/compatibility.yaml")["agents"].items():
        if any(_kw_match(k, text) for k in a["detect"]):
            agents.append(aid)
    if "SKILL.md" in names:
        agents.append("agent-skills-format")
    if any(f.startswith(".claude-plugin/") for f in files):
        agents.append("claude-code-plugin")
    renderers = [rid for rid, r in data("registry/renderers.yaml")["renderers"].items()
                 if any(k.strip() in text for k in r["detect"])]
    return {"agents": sorted(set(agents)), "renderers": renderers}
