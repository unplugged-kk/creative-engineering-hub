"""Upstream assessment never substitutes stale registry state for local evidence."""
import subprocess

from ceh.store import Registry
from ceh.upstream import analysis_markdown
from conftest import SKILL_REPO, commit, make_repo, sh


def test_check_refreshes_stale_object_only_modification_signal(ceh, run_ceh):
    upstream = make_repo(ceh["tmp"] / "upstream", SKILL_REPO)
    local = ceh["tmp"] / "local" / "object-copy"
    subprocess.run(["git", "clone", "--quiet", "--no-checkout", f"file://{upstream}", str(local)], check=True)
    _, rec, _ = run_ceh("add", f"file://{upstream}")
    registry = Registry()
    record = registry.get(rec["id"])
    record["local"]["modified"] = True
    record["local"]["state"][str(local)]["uncommitted_count"] = 999
    registry.save(record)
    original_head = sh("rev-parse", "HEAD", cwd=local)
    commit(upstream, {"new.md": "upstream change"}, "new upstream work")
    code, results, err = run_ceh("upstream", "check", rec["id"])
    assert code == 0, err
    assert results[0]["flags"] == ["new-commits"]
    refreshed = registry.get(rec["id"])
    assert refreshed["local"]["modified"] is False
    assert refreshed["local"]["state"][str(local)]["uncommitted_count"] == 0
    assert refreshed["upstream"]["pinned_commit"] == original_head
    assert sh("rev-parse", "HEAD", cwd=local) == original_head


def test_check_detects_new_untracked_work_and_preserves_it(ceh, run_ceh):
    upstream = make_repo(ceh["tmp"] / "upstream", SKILL_REPO)
    local = ceh["tmp"] / "local" / "working-copy"
    subprocess.run(["git", "clone", "--quiet", f"file://{upstream}", str(local)], check=True)
    _, rec, _ = run_ceh("add", f"file://{upstream}")
    original_head = sh("rev-parse", "HEAD", cwd=local)
    (local / "my-work.txt").write_text("user-owned\n")
    commit(upstream, {"new.md": "upstream change"}, "new upstream work")
    code, results, err = run_ceh("upstream", "check", rec["id"])
    assert code == 0, err
    assert "local-conflict" in results[0]["flags"]
    refreshed = Registry().get(rec["id"])
    assert refreshed["local"]["modified"] is True
    assert refreshed["local"]["state"][str(local)]["uncommitted_count"] == 1
    assert (local / "my-work.txt").read_text() == "user-owned\n"
    assert sh("rev-parse", "HEAD", cwd=local) == original_head
    assert refreshed["upstream"]["pinned_commit"] == original_head


def test_assessment_documents_unknowns_exact_commits_tests_and_rollback():
    pin, latest = "a" * 40, "b" * 40
    rec = {"id": "CEH-0001", "upstream": {"remote": "https://github.com/example/tool", "pinned_commit": pin,
           "latest_commit": latest, "flags": ["new-commits", "local-conflict"]}}
    diff = {"pinned": pin, "latest": latest, "commit_count": 1, "files_changed": 1, "breaking": [],
            "licence_files_changed": [], "manifests": {}, "deleted": [], "impacted_skills": ["kinetic-type-planning"],
            "impacted_video_factory": ["contentos/renderers/hyperframes.py"], "local_modifications": {"working-copy": 1},
            "commits": [{"date": "2026-11-10", "sha": latest, "subject": "update docs"}]}
    md = analysis_markdown(rec, diff)
    assert f"https://github.com/example/tool/compare/{pin}...{latest}" in md
    assert f"`{pin}`" in md and f"`{latest}`" in md
    assert "not proof of a merge conflict" in md
    assert "Compatibility: UNKNOWN" in md and "Security: UNKNOWN" in md and "Licence suitability: UNKNOWN" in md
    assert "semantic API" in md and "Required verification" in md
    assert f"ceh upstream sync CEH-0001 --approve --to {pin}" in md
    assert "Keep the current pin" in md


def test_missing_local_copy_is_unknown_instead_of_clean(ceh, run_ceh):
    upstream = make_repo(ceh["tmp"] / "upstream", SKILL_REPO)
    _, rec, _ = run_ceh("add", f"file://{upstream}")
    registry = Registry()
    record = registry.get(rec["id"])
    missing = str(ceh["tmp"] / "missing-copy")
    record["local"]["paths"] = [missing]
    record["local"]["modified"] = True
    registry.save(record)
    code, results, err = run_ceh("upstream", "check", rec["id"])
    assert code == 0, err
    assert "local-unverified" in results[0]["flags"]
    refreshed = registry.get(rec["id"])
    assert refreshed["local"]["modified"] is None
    assert refreshed["local"]["state"][missing]["unverified"] is True
