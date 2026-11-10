import json
import shutil
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent


def sh(*args, cwd):
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def make_repo(path: Path, files: dict[str, str]) -> Path:
    path.mkdir(parents=True)
    sh("init", "-q", "-b", "main", cwd=path)
    sh("config", "user.email", "t@t", cwd=path)
    sh("config", "user.name", "t", cwd=path)
    commit(path, files, "initial")
    return path


def commit(path: Path, files: dict[str, str], msg: str) -> str:
    for name, text in files.items():
        f = path / name
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(text)
    sh("add", "-A", cwd=path)
    sh("commit", "-q", "-m", msg, cwd=path)
    return sh("rev-parse", "HEAD", cwd=path)


SKILL_REPO = {
    "README.md": "# Kinetic Type Kit\n\nA Claude Code skill for kinetic typography and motion graphics, rendered with HyperFrames.\n" + "x" * 1200,
    "SKILL.md": "---\nname: kinetic-type-kit\ndescription: Kinetic typography for reels.\n---\nUse npx hyperframes.\n",
    "LICENSE": "MIT License\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\n",
    "package.json": json.dumps({"name": "ktk", "version": "1.2.0", "dependencies": {"gsap": "3.12.0"}}),
    "examples/demo.html": "<html></html>",
}


@pytest.fixture
def ceh(tmp_path, monkeypatch):
    """An isolated CEH root with the real taxonomy and policy, no network, fake agent homes."""
    root = tmp_path / "ceh"
    for d in ("registry", "policies", "library"):
        shutil.copytree(REPO / d, root / d, ignore=shutil.ignore_patterns("resources", "skills"))
    (root / "registry" / "resources").mkdir()
    (root / "library" / "skills").mkdir(parents=True, exist_ok=True)
    home = tmp_path / "home"
    for d in (".claude/skills", ".codex/skills", ".config/opencode/skills", ".gemini/antigravity/skills", ".agents/skills"):
        (home / d).mkdir(parents=True)
    vf = tmp_path / "vf"
    vf.mkdir()
    pol = (root / "policies" / "policy.yaml").read_text().replace("~/git/video-factory", str(vf))
    (root / "policies" / "policy.yaml").write_text(pol)
    monkeypatch.setenv("CEH_ROOT", str(root))
    monkeypatch.setenv("CEH_OFFLINE", "1")
    monkeypatch.setenv("CEH_AGENT_HOME", str(home))
    monkeypatch.setenv("CEH_LOCAL_ROOTS", str(tmp_path / "local"))
    (tmp_path / "local").mkdir()
    return {"root": root, "home": home, "tmp": tmp_path, "vf": vf}


@pytest.fixture
def run_ceh(capsys):
    from ceh.cli import main

    def _run(*argv):
        code = main(["--json", *argv])
        captured = capsys.readouterr()
        try:
            return code, json.loads(captured.out), captured.err
        except json.JSONDecodeError:
            return code, captured.out, captured.err
    return _run
