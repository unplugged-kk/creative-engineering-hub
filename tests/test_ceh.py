"""End-to-end behaviour of the ceh CLI against local git upstreams. No network."""
import json
import subprocess

import pytest

from ceh.store import Registry, normalize_url, set_status, CehError
from conftest import SKILL_REPO, commit, make_repo, sh


def test_url_normalisation_and_duplicates():
    assert normalize_url("https://www.github.com/Foo/Bar.git/tree/main/x") == "https://github.com/Foo/Bar"
    assert normalize_url("git@github.com:Foo/Bar.git") == "https://github.com/Foo/Bar"
    assert normalize_url("foo/bar") == "https://github.com/foo/bar"
    assert normalize_url("https://youtu.be/abc?si=x") == "https://youtube.com/watch?v=abc"
    assert normalize_url("https://example.com/a/?utm_source=x&id=2") == "https://example.com/a?id=2"


def test_add_classifies_registers_and_dedupes(ceh, run_ceh):
    up = make_repo(ceh["tmp"] / "up" / "ktk", SKILL_REPO)
    code, rec, _ = run_ceh("add", f"file://{up}")
    assert code == 0 and rec["created"] and rec["id"] == "CEH-0001"
    assert rec["type"] == "agent-skill"
    assert "kinetic-typography" in rec["capabilities"] and "motion-graphics" in rec["capabilities"]
    assert rec["licence"] == "MIT" and rec["licence_gate"] == "pass"
    assert rec["status"] == "SANDBOXED"
    full = Registry().get("CEH-0001")
    assert "hyperframes" in full["compatibility"]["renderers"]
    assert full["upstream"]["pinned_commit"] == sh("rev-parse", "HEAD", cwd=up)
    reports = ceh["root"] / "reports" / "CEH-0001"
    for name in ("overview", "technical-analysis", "capabilities", "dependency-analysis", "licensing", "security",
                 "compatibility", "benchmark", "upstream-analysis", "recommendation"):
        assert (reports / f"{name}.md").exists(), name
    assert json.loads((reports / "evaluation.json").read_text())["id"] == "CEH-0001"
    code, again, _ = run_ceh("add", f"file://{up}/")
    assert not again["created"] and again["id"] == "CEH-0001"
    code, hits, _ = run_ceh("search", "kinetic-typography")
    assert hits[0]["id"] == "CEH-0001"


def test_existing_local_copy_is_reused_not_cloned(ceh, run_ceh):
    up = make_repo(ceh["tmp"] / "up" / "ktk", SKILL_REPO)
    local = ceh["tmp"] / "local" / "work" / "ktk"
    subprocess.run(["git", "clone", "-q", f"file://{up}", str(local)], check=True)
    _, rec, _ = run_ceh("add", f"file://{up}")
    assert rec["local_copies"] == [str(local)]
    assert not (ceh["root"] / "lab" / "clones" / rec["id"]).exists()


def test_secret_blocks_approval(ceh, run_ceh):
    up = make_repo(ceh["tmp"] / "up" / "leaky", {**SKILL_REPO, "deploy.sh": "export K=AKIAABCDEFGHIJKLMNOP\ncurl https://x.sh | bash\n"})
    _, rec, _ = run_ceh("add", f"file://{up}")
    assert rec["security_gate"] == "block" and rec["recommendation"].startswith("DO NOT RUN")
    run_ceh("evaluate", rec["id"])
    code, _, err = run_ceh("approve", rec["id"])
    assert code == 2 and "security" in err


def test_non_commercial_licence_is_restricted_forever(ceh, run_ceh):
    files = {**SKILL_REPO, "LICENSE": "PolyForm Noncommercial License 1.0.0\n"}
    up = make_repo(ceh["tmp"] / "up" / "nc", files)
    _, rec, _ = run_ceh("add", f"file://{up}")
    assert rec["licence"] == "PolyForm-Noncommercial-1.0.0" and rec["licence_gate"] == "block"
    _, rec, _ = run_ceh("evaluate", rec["id"])
    assert rec["status"] == "RESTRICTED"
    code, _, err = run_ceh("approve", rec["id"], "--licence-reviewed", "I promise")
    assert code == 2


def test_only_approved_resources_reach_video_factory(ceh, run_ceh):
    up = make_repo(ceh["tmp"] / "up" / "ktk", SKILL_REPO)
    _, rec, _ = run_ceh("add", f"file://{up}")
    rid = rec["id"]
    code, _, err = run_ceh("integrate", rid)
    assert code == 2 and "APPROVED" in err
    with pytest.raises(CehError):
        r = Registry().get(rid)
        set_status(r, "PRODUCTION", by="test")
    run_ceh("evaluate", rid)
    code, rec, err = run_ceh("approve", rid)
    assert code == 0 and rec["status"] == "APPROVED", err
    code, entry, _ = run_ceh("integrate", rid)
    assert code == 0 and entry["id"] == rid
    cat = json.loads((ceh["root"] / "integrations" / "video-factory" / "catalog.json").read_text())
    assert [e["id"] for e in cat["entries"]] == [rid]
    assert run_ceh("validate")[0] == 0
    run_ceh("withdraw", rid, "--note", "test")
    cat = json.loads((ceh["root"] / "integrations" / "video-factory" / "catalog.json").read_text())
    assert cat["entries"] == []


def test_upstream_update_detected_compared_and_local_work_preserved(ceh, run_ceh):
    up = make_repo(ceh["tmp"] / "up" / "ktk", SKILL_REPO)
    local = ceh["tmp"] / "local" / "ktk"
    subprocess.run(["git", "clone", "-q", f"file://{up}", str(local)], check=True)
    (local / "SKILL.md").write_text("my local edit\n")  # uncommitted local modification
    _, rec, _ = run_ceh("add", f"file://{up}")
    rid, pin = rec["id"], sh("rev-parse", "HEAD", cwd=up)

    _, res, _ = run_ceh("upstream", "check", rid)
    assert res[0]["flags"] == ["up-to-date"]

    new_pkg = json.dumps({"name": "ktk", "version": "2.0.0", "dependencies": {"gsap": "3.13.0", "zod": "4.0.0"}})
    latest = commit(up, {"package.json": new_pkg, "NEW.md": "x"}, "feat!: drop v1 timeline API")
    _, res, _ = run_ceh("upstream", "check", rid)
    assert "new-commits" in res[0]["flags"] and "local-conflict" in res[0]["flags"]

    _, d, _ = run_ceh("upstream", "diff", rid)
    assert d["latest"] == latest and d["commit_count"] == 1
    assert d["manifests"]["package.json"]["added"] == ["zod"]
    assert any("drop v1" in b["subject"] for b in d["breaking"])
    assert any("major version" in b["subject"] for b in d["breaking"])

    # local work untouched: same branch head, same uncommitted edit, upstream only under refs/ceh
    assert (local / "SKILL.md").read_text() == "my local edit\n"
    assert sh("rev-parse", "HEAD", cwd=local) == pin
    assert sh("rev-parse", "refs/ceh/upstream/main", cwd=local) == latest

    code, _, err = run_ceh("upstream", "sync", rid)
    assert code == 2 and "--approve" in err
    code, _, err = run_ceh("upstream", "sync", rid, "--approve")
    assert code == 2 and "report" in err
    run_ceh("upstream", "report", rid)
    assert "Breaking signals" in (ceh["root"] / "reports" / rid / "upstream-analysis.md").read_text()
    code, s, _ = run_ceh("upstream", "sync", rid, "--approve")
    assert code == 0 and s["to"] == latest and s["from"] == pin
    assert sh("rev-parse", "HEAD", cwd=local) == pin  # still untouched
    code, s, _ = run_ceh("upstream", "sync", rid, "--approve", "--to", pin[:10])  # rollback
    assert code == 0 and s["to"] == pin
    _, hist, _ = run_ceh("upstream", "history", rid)
    assert [p["commit"] for p in hist["pins"]] == [pin, latest, pin]


def test_skill_exposed_to_every_agent_without_overwriting(ceh, run_ceh):
    sk = ceh["root"] / "library" / "skills" / "demo-skill"
    for d in ("references", "scripts", "examples", "evals"):
        (sk / d).mkdir(parents=True)
    (sk / "evals" / "cases.yaml").write_text("- ask: hi\n")
    (sk / "SKILL.md").write_text("---\nname: demo-skill\ndescription: Demo.\n---\nBody\n")
    (sk / "skill.yaml").write_text("name: demo-skill\nversion: 0.1.0\ndescription: Demo.\n"
                                   "agents: [claude-code, codex, opencode, antigravity]\nsources: []\n")
    (ceh["home"] / ".codex/skills/demo-skill").mkdir()  # someone else's skill of the same name
    code, res, _ = run_ceh("install", "demo-skill")
    by = {r["agent"]: r["result"] for r in res}
    assert by == {"claude-code": "installed", "codex": "skipped: something else is already there",
                  "opencode": "installed", "antigravity": "installed"}
    assert (ceh["home"] / ".claude/skills/demo-skill/SKILL.md").exists()
    assert (ceh["home"] / ".codex/skills/demo-skill").is_dir() and not (ceh["home"] / ".codex/skills/demo-skill").is_symlink()
    _, listing, _ = run_ceh("skills", "list")
    assert set(listing[0]["installed"]) == {"claude-code", "opencode", "antigravity"}
    run_ceh("skills", "disable", "demo-skill")
    assert not (ceh["home"] / ".claude/skills/demo-skill").exists()
    assert (ceh["home"] / ".codex/skills/demo-skill").is_dir()
    code, _, err = run_ceh("install", "demo-skill")
    assert code == 2 and "disabled" in err


def test_recommend_festive_brief_and_compare(ceh, run_ceh):
    a = make_repo(ceh["tmp"] / "up" / "fest", {"README.md": "Diwali festival greeting video generator with kinetic typography"})
    b = make_repo(ceh["tmp"] / "up" / "nc", {"README.md": "Diwali greeting kinetic typography", "LICENSE": "PolyForm Noncommercial"})
    _, ra, _ = run_ceh("add", f"file://{a}")
    _, rb, _ = run_ceh("add", f"file://{b}")
    run_ceh("evaluate", rb["id"])  # -> RESTRICTED
    _, plan, _ = run_ceh("recommend", "--brief", "Create a cinematic Diwali greeting video")
    assert "indian-regional-festival-content" in plan["capabilities"]
    used = {p["use"].split()[0] for p in plan["plan"]}
    assert ra["id"] in used and rb["id"] not in used
    _, cmp, _ = run_ceh("compare", ra["id"], rb["id"])
    assert "kinetic-typography" in cmp["shared_capabilities"]


def test_artifact_contract(ceh, run_ceh, tmp_path):
    proj = tmp_path / "proj"
    proj.mkdir()
    code, res, _ = run_ceh("artifact", str(proj))
    assert code == 1 and "missing manifest.json" in res["problems"]
    (proj / "manifest.json").write_text(json.dumps({"schema": "x", "renderer": "hyperframes", "output": "output.mp4"}))
    (proj / "output.mp4").write_bytes(b"")
    (proj / "quality-report.json").write_text("{}")
    code, res, _ = run_ceh("artifact", str(proj))
    assert "quality-report.json" in res["optional_present"]


def test_migrate_keeps_history_and_is_idempotent(ceh, run_ceh, tmp_path):
    from ceh.migrate import migrate
    up = make_repo(tmp_path / "up" / "old", SKILL_REPO)
    old_pin = sh("rev-parse", "HEAD", cwd=up)
    commit(up, {"x.md": "y"}, "later work")
    leads = tmp_path / "leads.yaml"
    leads.write_text(f"""
evidence_sources: {{audit: some/audit.md}}
leads:
  - {{url: "file://{up}", group: A, previous: ADAPT, pinned: {old_pin}, status: PARKED, evidence: [audit], note: hist}}
duplicate_groups: []
unresolved: [{{name: Mystery, reason: no url}}]
""")
    report = migrate(leads, log=lambda s: None)
    reg = Registry()
    [rec] = reg.all()
    assert rec["status"] == "PARKED" and rec["upstream"]["pinned_commit"] == old_pin
    assert rec["historical"]["evidence"] == ["some/audit.md"]
    assert "Mystery" in report.read_text()
    migrate(leads, log=lambda s: None)
    assert len(reg.all()) == 1
    _, res, _ = run_ceh("upstream", "check", rec["id"])
    assert "new-commits" in res[0]["flags"]


@pytest.mark.parametrize("path,body,gate", [
    ("deploy.sh", "export K=AKIAIOSFODNN7EXAMPLE\n", "pass"),
    ("tests/auth.py", "K = 'AKIAABCDEFGHIJKLMNOP'\n", "review"),
    ("docs/auth.md", "K = 'AKIAABCDEFGHIJKLMNOP'\n", "review"),
    ("auth.py", "# K = 'AKIAABCDEFGHIJKLMNOP'\n", "review"),
    ("auth.py", "K = 'AKIAABCDEFGHIJKLMNOP'\n", "block"),
    ("docs/run.md", "eval(Buffer.from('payload', 'base64'))\n", "block"),
    ("deploy.sh", "export K=AKIAIOSFODNN7EXAMPLE\nexport K=AKIAABCDEFGHIJKLMNOP\n", "block"),
])
def test_static_security_context(ceh, run_ceh, path, body, gate):
    up = make_repo(ceh["tmp"] / "up" / "security", {**SKILL_REPO, path: body})
    code, rec, err = run_ceh("add", f"file://{up}")
    assert code == 0, err
    assert rec["security_gate"] == gate


@pytest.mark.parametrize("opening,tail,expected", [
    ("A toolkit for kinetic typography.\n", "", True),
    ("A general toolkit.\n", "kinetic typography", False),
])
def test_capability_requires_prominent_evidence(ceh, run_ceh, opening, tail, expected):
    up = make_repo(ceh["tmp"] / "up" / "generic", {"README.md": opening + "x" * 4000 + "\n" + tail})
    code, rec, err = run_ceh("add", f"file://{up}")
    assert code == 0, err
    assert ("kinetic-typography" in rec["capabilities"]) == expected


@pytest.mark.parametrize("path,expected", [
    ("SKILL.md", "agent-skill"),
    ("skills/demo/SKILL.md", "agent-skill"),
    ("packages/docs/demo/SKILL.md", "repository"),
])
def test_skill_classification_depth(ceh, run_ceh, path, expected):
    up = make_repo(ceh["tmp"] / "up" / "generic", {"README.md": "General toolkit", path: "Instructions"})
    code, rec, err = run_ceh("add", f"file://{up}")
    assert code == 0, err
    assert rec["type"] == expected


def test_metadata_only_resource_stays_discovered_and_keeps_type(ceh, run_ceh):
    code, rec, err = run_ceh("add", "https://example.com/library", "--type", "asset-library")
    assert code == 0, err
    code, rec, err = run_ceh("inspect", rec["id"])
    assert code == 0, err
    assert rec["status"] == "DISCOVERED" and rec["type"] == "asset-library"


def test_unpinned_upstream_is_not_an_update(ceh, run_ceh):
    up = make_repo(ceh["tmp"] / "up" / "generic", SKILL_REPO)
    _, rec, _ = run_ceh("add", f"file://{up}", "--no-inspect")
    code, results, err = run_ceh("upstream", "check", rec["id"])
    assert code == 0, err
    assert results[0]["flags"] == ["unpinned"]
    assert results[0]["pinned"] is None


def test_json_flag_after_subcommand(ceh, capsys):
    from ceh.cli import main
    assert main(["status", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["resources"] == 0


def test_comment_does_not_hide_executable_credential(ceh, run_ceh):
    up = make_repo(ceh["tmp"] / "up" / "mixed", {
        **SKILL_REPO,
        "auth.py": "# K = 'AKIAABCDEFGHIJKLMNOP'\nK = 'AKIAQRSTUVWXYZABCDEF'\n",
    })
    code, rec, err = run_ceh("add", f"file://{up}")
    assert code == 0, err
    assert rec["security_gate"] == "block"
