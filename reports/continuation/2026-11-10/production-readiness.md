# Production readiness recommendation

**Do not activate new creative capabilities in production yet.** The read-only provider is reviewable and tested on an isolated
VF branch; candidate guidance and fixture evidence are useful but do not satisfy every production acceptance criterion.

## Implemented and verified

- Strict v2 schema, independent catalog fingerprint, approval/provenance/asset-licence enforcement, compatibility explanations,
  bounded malformed-input handling and deterministic phrase-based selection.
- Publisher binds current resource approval, canonical skill approval/version/bytes, reviewed release metadata digest and source
  registry URL/pin/gates. Modifying workflow/requirements/evidence after approval prevents publication.
- Original CEH operating skill plus two new candidate instruction-only skills. No copied upstream code/assets or install hooks.
- Isolated VF provider commit b1befad73b4285ce461eb48861e5559c069d2776 on codex/ceh-catalog-consumer at /tmp/ceh-vf-consumer.
  It adds only new modules/tests/docs; no pipeline/CLI/config/default-renderer/gate/ContentForge edits. Disabled by default.
- Synthetic consumer selection -> explicit plan -> authored HyperFrames0.8.114 sandbox render -> existing technical QA.
  Three runs produced byte-identical MP4s. Scope and quality limits are in benchmark.md.
- Upstream checks refreshed 45 resources; 14 need attention. False conflicts from no-checkout clones removed. Two genuine
  local-modification signals remain heuristic; p5.brush local Git state is unverified, not falsely clean.
- Exact registry pins compared against pre-mission commit: no changes. Original VF tracked patch and untracked filename
  list compare unchanged. No new production dependency, credential use, publishing or branch merge.

## Verification

CEH: `uv run pytest -q` and `uvx ruff check ceh tests tools/benchmarks --select F,E9,B`; latest counts recorded in handover.
Registry and skills validation pass. No dedicated type checker is installed, so no type-check pass is claimed.
Live VF baseline: 1023 passed, 8 skipped; Node adapter tests: 66 passed.
Final isolated VF regression result is appended below after completion. Isolated counts differ because the branch excludes
user-owned uncommitted/untracked tests; the live checkout remains untouched. Contract/provider focus: 71 passed independently.
Independent security reviewer confirmed exact CEH/VF contract parity and resolved the identified publication bypasses.

## Before production activation

1. Review/approve a specific canonical capability version and its redistribution/usage licence. Neither new skill is approved.
2. Complete normal-speed output/independent critic and listening review, required brand/language checks, and relevant agent runs.
3. Review exact source pins, transitive dependencies, approval scope and compatibility metadata; bind approved skill and entry digests.
4. Explicitly authorize publication of that release. The real v2 production catalog is empty; historical PRODUCTION does not qualify.
5. Review the separate VF consumer branch before any merge, then independently accept its catalog fingerprint and opt in.
6. Run an approved disposable project through existing VF approvals and QA; do not replace those gates with fixture evidence.

HyperFrames adoption is a separate decision. Scheduled automation, semantic API analysis and full agent coverage are not claimed.
Recovery instructions are in recovery.md. Acceptance details are in acceptance-matrix.md.

## Final measured regression results

- CEH: 104 passed in 11.76 seconds; focused Ruff passes; compileall syntax check passes; registry/skill validation passes.
- Final isolated VF: 1080 passed, 17 skipped in 137.06 seconds. Node adapter suite: 66 passed.
- Live original VF: 1023 passed, 8 skipped. Its original tracked patch and untracked file list still compare unchanged.
- Consumer contract/provider focus: 71 passed independently. CEH/VF contract implementations compare byte-identical.
- Third fresh helper-to-render reproduction: /tmp/ceh-benchmark-from-helper/video.mp4, same encoded SHA256 and QA8PASS1WARN.
  This closes documented command reproducibility for a synthetic fixture; it does not grant real capability approval.
