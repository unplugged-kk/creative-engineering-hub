# Final acceptance decision package

Finalized 2026-11-11; source/media reviews and bounded CLI evidence were collected across the 2026-11-10 checkpoint.
Baseline CEH commit: 1ac01c3a2a92abe1b44e687806c43c86d0b7f711. No production capability approval or VF merge/activation occurred.

## Direct answers

1. **Technically ready?** The scoped metadata contract/publisher/reader engineering checkpoint is green and reviewable.
   It is not a claim that every master-mission feature or approved-artifact production flow is complete.
2. **Candidate safe/suitable?** Kinetic-type-planning is a promising non-executing, bounded first release. It is not unconditionally
   approved or accepted: owner usage permission and creative/media judgement remain pending. Both live candidates remain research status.
3. **Exact recommendation?** Kinetic-type-planning0.1.0, English instruction-only planning complementing HyperFrames0.8.114;
   keep measured-sound-pass0.1.0 research-only. See first-capability-decision.md for immutable sources and comparison.
4. **Evidence?** Fresh CEH104 tests/lint/validation, fresh VF71 contract/provider tests, strict publication mutation tests, exact
   contract parity, durable readable media, three identical output hashes, existing technical QA8PASS1WARN and bounded CLI attempts.
5. **Risks?** See remaining-risks.md: media/usage acceptance, agent runtime gaps, no approved-bundle consumption proof,
   parent-resource publication requirements and pending final trust fingerprint. Reproducibility does not prove creative quality.
6. **VF merge-ready?** b1befad is reviewable for a disabled metadata-only merge. Production activation remains on hold; the
   provider returns artifact fingerprint references and does not open/verify/use the canonical bundle on disk.
7. **What changes on authorization?** A can approve an exact original-guidance usage scope and bind/publish its reviewed release;
   it does not merge VF. B can separately authorize an exact consumer commit and explicit fingerprint-pinned metadata use;
   it grants no job approvals, executable plugins or publishing permission. Actual guidance handoff must be demonstrated honestly.
8. **Rollback?** Omit --enable, withdraw/re-export an authorized CEH entry if directed, and independently restore/accept the prior
   catalog fingerprint. Do not reset/clean original worktrees, alter production pins or delete user files. See runbook.

## Fresh revalidation

- CEH main remains the reviewed source checkpoint before acceptance documentation. No implementation or canonical skill files
  were changed in this mission. Original candidate fingerprints were recomputed and preserved.
- `uv run ceh validate --json`: 48 resources,3 skills,catalog consistent. `uv run ceh skills validate --json`: all skills valid.
- `uv run pytest -q`: **104 passed in10.54s**. `uvx ruff check ceh tests tools/benchmarks --select F,E9,B`: pass.
- `~/.contentos/venv/bin/python -m pytest tests/test_ceh_catalog_provider.py tests/test_ceh_contract.py -q` at actual consumer:
  **71 passed**. Consumer remains isolated/unmerged and has no production pipeline caller; tests cover hostile/failure behavior.
- Producer/VF contract files are byte-identical, SHA256944eda73e49eb8b2aeb22b08878d8a223c973fd0fc042d333da43d51ba85c2cd.
- Fresh `uv run ceh catalog export --output /tmp/ceh-acceptance-export.json --json`: zero entries/no exclusions. Strict schema
  validation passes; default load disabled, explicitly test-pinned empty load valid with no selectable capability. Real catalog untouched.
- VF main still36bb558, HyperFrames still0.8.114. Original tracked patch/untracked filename list captured before and compared after
  acceptance work. No prior untracked-content hashing is fabricated. No production source/config/dependency changes.
- Full regression historical checkpoint remains104 CEH/1080VF+17skip/66Node. Only relevant fast checks repeated because no
  production source change or new regression required repeating full render/regression phases.
- All three original media files were re-probed/rehashed; no render repeated. Durable copies verified and representative frames
  re-inspected. Full-speed/human listening and owner acceptance remain pending, not inferred from static image inspection.
- CodexCLI0.167.0, ClaudeCode2.1.316 and OpenCode2.2.7 were measured in a clean sandbox. Actual task attempts did not produce
  verified output: no auth/external model network allowed. Antigravity executable unavailable in PATH. See agent report/raw evidence.

## Exact artifacts for the pending owner decision

Current unchanged candidate bundle:
`942d06fc400fdf44beb9767d0300f6313cf8366372190325ad6c87799410c679`.

Proposed first-release bundle, changing only the staged skill.yaml described in proposed-skill-metadata.yaml:
`addfcc1b9a8f19cc3ba1c28b03abdfb25f954dc29208e96414515a7f9ee300b0`.
It includes the proposed internal-commercial-guidance scope and honest active/verification metadata. The canonical bundle has
not been changed. Draft status is not a rights grant or lifecycle promotion.

Non-consumable release-proposal.json fingerprint:
`d25916755faded6bd83e4c4be9e3dd540fddfd307fb1d63e606fa89e5637143c`.
Its approval is PENDING_OWNER_DECISION. It cannot be loaded as the production catalog and is not the final entry fingerprint.
Final approval actor/time/evidence and final catalog trust fingerprint must follow real owner authorization and be reviewed for B.

Authoritative review video and human checklist are linked in media-review-package.md. User review is not claimed.
The held-frame WARN is intentional in the fixture; tiny supporting/footer text and the synthetic tone need explicit human judgement.
The fixture does not exercise full production backdrop-diversity rules, narration or multilingual shaping.

## Separate decisions - neither executed

**Decision A, conditional capability release:** after watching the media, does the owner accept the proposed internal commercial
planning/no-redistribution scope and exact prospective kinetic-type-planning0.1.0 bundle above, and authorize its scoped
CEH-0018 parent bookkeeping plus canonical publication? If media/usage scope is not accepted, keep it a research candidate.
The runbook states all metadata steps and exact available CLI actions. No fictional standalone skill-approval command is proposed.

**Decision B, later consumer acceptance:** independently review exact commit b1befad73b4285ce461eb48861e5559c069d2776 and,
only after A/final fingerprint review, decide on a protected clean-target merge and explicit metadata-only opt-in. If the requested
scope is actual approved-skill consumption rather than metadata discovery, hold B until verified artifact handoff and normal VF
job approvals/QA are demonstrated. A does not authorize B, and pushing engineering code authorizes neither.

## Delivery and push status

User separately requested commit and push. The existing VF branch was pushed without source changes or merge:
`origin/codex/ceh-catalog-consumer` resolves to b1befad73b4285ce461eb48861e5559c069d2776 on
https://github.com/unplugged-kk/video-factory/tree/codex/ceh-catalog-consumer.
CEH has no configured Git remote. GitHub lookup of unplugged-kk/creative-engineering-hub found no accessible repository.
An asynchronous question requested the intended remote URL. No repository/destination was invented and no visibility was changed.
Acceptance work is to be committed locally; CEH push remains pending that destination.
