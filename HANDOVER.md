# CEH handover

Written 2026-11-10 mid-build so another agent can continue. Mission text: the user's "MASTER MISSION: Build Creative
Engineering Hub (CEH)" prompt (phases 1-9, acceptance criteria 1-15). Read that first if you have it.

## Where things are

- Repo: `~/git/creative-engineering-hub` (git init done, **nothing committed yet**). Python 3.14 via `uv` (`uv sync`, `uv run ceh ...`, `uv run pytest`).
- Video Factory (VF): `~/git/video-factory`. **Do not modify it.** It has the user's own uncommitted WIP (16 files: lang/, docs, tests). Leave it.

## Done

Phase 1 audit (evidence gathered, encoded as data):
- `intake/historical/leads.yaml`: 49 leads (groups A-E) with canonical URL, earlier decision, recovered pins, local copies, user forks,
  VF usage, near-duplicate groups, and 2 unresolved (OpenSEO, CannerAI). Every fact cites a file in `evidence_sources`.
- Key sources found: `video-factory/docs/research/video-factory-evolution/repository-audit.md` (19-repo decisions),
  `.../motion-design-integration/01-repository-audit.md` (full pin SHAs), `~/Desktop/VideoFactory-Lanes/evidence/m3-repo-matrix.json`,
  `video-factory/research/tool-catalog.yaml`, `config/upstream-skills.lock.json` (hyperframes v0.8.114 = 01c6f600), `package.json`,
  `~/Desktop/Animate-Studio/STATUS.md` (cth9191/animate v0.4.0 @ 7e5eb56). LottieFiles pin f9a8a041 confirmed.
- Group D (bang-motion, vox-explainer, paint-mv, hand-drawn-nikola, anything2explainer) had no prior local research.
  video-shotcraft is installed as a Claude plugin.
- VF facts: renderer registry `contentos/renderers/{hyperframes,mpt,remotion}.py` (`registry.get_renderer`, default hyperframes);
  86 creative skills in `config/creative-skills.json`; 93 capabilities in `config/capabilities.json`; project skills
  `.claude/skills/explainer-motion-craft`, `explainer-visual-qa`; approvals bound to digests (`pipeline.gate_digest`); vendor/ has
  MoneyPrinterTurbo, OpenMontage, youtube-agent-skill (MPT and OpenMontage have untracked local Docker files).
- VF baseline tests: `~/.contentos/venv/bin/python -m pytest tests` = 1022 passed, 8 skipped, **1 failed**
  (`tests/test_lang.py::test_real_hindi_audio...`, `asr_binary_missing` although `/opt/homebrew/bin/whisper-cli` exists; the test file is
  the user's uncommitted WIP). Node tests pass. Report this to the user; not ours to fix.

Phases 2-7 code (written, **not yet run or tested**):
- `ceh/store.py` registry (one YAML per resource in `registry/resources/CEH-NNNN.yaml`), URL normalisation, dedupe (url, forks, aliases), lifecycle (`set_status`; APPROVED/PRODUCTION gated to approve/integrate).
- `ceh/sources.py` git/gh helpers, `Tree` (reads git objects without checkout), local-clone scan (`policy.local_copies.roots`), lab clones `lab/clones/<id>` (`--no-checkout --depth 1 --filter=blob:limit=1m`).
- `ceh/analyze.py` classify (taxonomy keywords), licence (SPDX + fingerprints, asset separation), deps, security (secrets, risky scripts, install hooks, binaries, osv.dev), agent/renderer compatibility.
- `ceh/intake.py` add/inspect/alternatives/recommendation. `ceh/evaluate.py` weighted scores + gates + 10 reports + evaluation.json.
- `ceh/upstream.py` check/diff/report/sync(--approve, --to rollback)/history/status/weekly_report; fetches only into `refs/ceh/upstream/<branch>`.
- `ceh/integrate.py` approve/integrate/withdraw, `integrations/video-factory/catalog.json`, VF test runner, artifact contract check.
- `ceh/skills.py` library skills, symlink install into agent dirs from `registry/compatibility.yaml`, never overwrite foreign dirs.
- `ceh/search.py` search/compare/recommend. `ceh/migrate.py` leads -> records + `reports/historical-migration/REPORT.md`.
- `ceh/cli.py` all commands (`ceh --help`). Data: `registry/{capabilities,renderers,compatibility}.yaml`, `policies/policy.yaml`.
- Tests: `tests/conftest.py`, `tests/test_ceh.py` (hermetic: file:// upstreams, CEH_OFFLINE, fake agent homes). Not yet run.

## Progress log (newest last)

- Tests: `uv run pytest -q` = **11 passed** (hermetic). Fixed: local-copy reuse for file:// URLs; partial-clone `ls-tree` "BAD" sizes.
- Written: README.md, AGENTS.md, ARCHITECTURE.md, ROADMAP.md, CHANGELOG.md, .gitignore, docs/adr/0001-0005,
  policies/{licensing,security,promotion,upstream}.md, integrations/video-factory/{README,artifact-contract}.md.
- Canonical skill `library/skills/creative-engineering-hub/` written and validates. NOT installed into real agent dirs yet (ask user).
- `ceh migrate` running against real network (first two runs crashed: "BAD" blob size, then zsh glob no-match in my shell chain;
  third run in progress). Output: `/private/tmp/claude-501/ceh-migrate.{out,log}`. If interrupted, re-run:
  `rm -rf registry/resources lab/clones && mkdir -p registry/resources lab/clones && uv run ceh migrate` (idempotent anyway).

## Next steps, in order

1. (done) tests green.
2. (done) docs. Remaining from original list below if any: ROADMAP.md, CHANGELOG.md, `policies/{licensing,security,promotion,upstream}.md`, `docs/adr/0001..` (one-file-per-record
   registry; CEH never edits VF, catalog.json is the contract; fetch into refs/ceh only; static-only inspection), `.gitignore` (lab/clones, .venv).
3. Canonical skill `library/skills/creative-engineering-hub/` (SKILL.md, skill.yaml, references/, scripts/, examples/, evals/, README.md)
   teaching agents the CEH workflows; `ceh install creative-engineering-hub` (ask user before touching real agent dirs).
4. `integrations/video-factory/README.md` + `artifact-contract.md` (manifest.json{schema,renderer,output}, output.mp4, optional preview.mp4, assets/, sources.json, render-log.json, quality-report.json).
5. `uv run ceh migrate` (real network, clones ~40 repos into lab/, minutes). Review `reports/historical-migration/REPORT.md`; `ceh validate`.
6. E2E demos: historical (e.g. cth9191/animate or heygen-com/hyperframes: `upstream check/diff/report`), new repo (`ceh add <unknown github url>`, evaluate, search, compare, recommend).
7. Commit in small conventional commits (no Claude co-author per user's CLAUDE.md; no em dashes). Confirm VF tests still at baseline.
8. Offer: weekly `ceh upstream check --all --report` schedule (scheduled task or launchd), and a VF-side reader of catalog.json (needs user approval; VF change).

## Rules from the user

Never overwrite existing projects or local work; no installs/execution of untrusted code; approval before production or destructive
actions; add != integrate; non-commercial never approved; prefer graft for code exploration (`graft ask/grep/skeleton/callers`).
