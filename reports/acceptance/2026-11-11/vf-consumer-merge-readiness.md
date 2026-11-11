# Video Factory consumer merge-readiness review

Date: 2026-11-10. Scope: existing metadata-only consumer and its exact release contract, reviewed read-only.
No branch, source, approval, catalog publication, merge, dependency or production activation change was performed by this review.
The reviewer did not author the VF provider, but did previously contribute to the shared contract; this is a fresh scoped review,
not an external security certification or a claim of complete reviewer independence from all implementation.

## Verdict

**The isolated commit is reviewable for a metadata-only merge. It is not ready to be described as activated production
skill consumption.** The default remains disabled, and no production pipeline calls the provider. A separate owner decision
must authorize any merge and opt-in invocation. Approval of the named canonical skill and its publication are different decisions.

The acceptance requirement that VF *uses an approved skill artifact* is not yet demonstrated. This provider validates and
returns reviewed metadata plus artifact digest references. It deliberately never reads, verifies against disk, installs or invokes
the actual canonical skill bundle. Do not represent metadata selection or the synthetic benchmark as approved-artifact consumption.

## Exact repository state reverified

| Checkout | Branch / state | Commit | Result |
|---|---|---|---|
| `/Users/kishore/git/video-factory` | `main`, existing user-owned tracked and untracked changes | `36bb5581527fab6e2b39f52b88032e78ad64355e` | Consumer commit is not an ancestor; no unmerged index entries |
| `/tmp/ceh-vf-consumer` (Git resolves `/private/tmp/...`) | `codex/ceh-catalog-consumer`, clean | `b1befad73b4285ce461eb48861e5559c069d2776` | Actual consumer implementation; no unmerged index entries |
| `/Users/kishore/.codex/worktrees/ceh-catalog-consumer/video-factory` | detached, clean | `36bb5581527fab6e2b39f52b88032e78ad64355e` | Managed worktree exists but contains only the baseline, not the consumer commit |
| CEH | committed checkpoint observed | `1ac01c3a2a92abe1b44e687806c43c86d0b7f711` | Contract compared directly with actual consumer copy |

The managed worktree name is not evidence of which code is present. Use the exact commit and actual consumer checkout for review.
No branch surgery or relocation was attempted. The original VF worktree's user changes remain present; this review did not modify
it and does not claim to reconstruct prior untracked-file contents from historical filename-only snapshots.

The consumer diff against its baseline is exactly five added files, 551 added lines:

- `contentos/ceh_catalog.py`
- `contentos/ceh_contract.py`
- `docs/integrations/CEH.md`
- `tests/test_ceh_catalog_provider.py`
- `tests/test_ceh_contract.py`

No pipeline, renderer, CLI routing, configuration, ContentForge, approval digest, QA, publishing or dependency file is modified.
The original `package.json` retains `hyperframes: 0.8.114`. No HyperFrames upgrade is proposed by this review.

## Fresh verification commands and results

Executed from `/tmp/ceh-vf-consumer` unless indicated:

```sh
git status --short
git rev-parse main HEAD
git diff --name-status 36bb558 b1befad
git diff --check 36bb558 b1befad
git ls-files -u
git merge-base --is-ancestor b1befad main
~/.contentos/venv/bin/python -m pytest tests/test_ceh_catalog_provider.py tests/test_ceh_contract.py -q
~/.contentos/venv/bin/python -m contentos.ceh_catalog --task 'kinetic typography'
rg -n 'ceh_catalog|ceh_contract|ceh-' contentos config docs/integrations/CEH.md
```

- Focused tests: **71 passed in 0.12 seconds**.
- Consumer worktree tracked/staged diffs are empty; unmerged indexes empty in the inspected checkouts.
- Ancestor check exits 1: consumer is not merged into `main`.
- Diff whitespace check passes. Added files only; no existing production path edited.
- Disabled CLI returns `available: false`, empty selections and an explicit existing-routing fallback.
- Search finds no call from production contentos or config paths; only the standalone module references its contract.
- This review did not repeat the full VF/Node suites: no new source change or focused failure justified that cost. Previous
  full-suite results remain historical evidence in `reports/continuation/2026-11-10/production-readiness.md`.

From CEH:

```sh
cmp ceh/catalog.py /tmp/ceh-vf-consumer/contentos/ceh_contract.py
shasum -a 256 ceh/catalog.py /tmp/ceh-vf-consumer/contentos/ceh_contract.py
```

Exact byte parity passes. Both hashes are:
`944eda73e49eb8b2aeb22b08878d8a223c973fd0fc042d333da43d51ba85c2cd`.
The standalone VF runtime validator is the identical implementation of CEH's strict v2 contract. Schema and runtime
have explicit additional semantic rules: fingerprint verification and unique capability IDs cannot be delegated solely to JSON Schema.

## Security and compatibility boundary

| Requirement | Finding |
|---|---|
| Disabled by default | PASS: explicit `--enable` or programmatic `enabled=True` required |
| Read-only metadata | PASS: explicit local catalog/environment files only; no source fetch, skill body load, install or command execution |
| Trusted publisher snapshot | PASS: independently supplied expected catalog SHA256 required; embedded digest alone is insufficient |
| Approval / integrity | PASS: strict APPROVED metadata, actor/time/evidence, source pins, entry/catalog hashes and commercial licence restrictions |
| Asset licence isolation | PASS: listed NC/unknown assets rejected independently, even optional assets |
| Compatibility | PASS for declared evidence: explicit renderer/runtime/dependency/input/asset/agent/language/format checks; no environment probing |
| Invalid / missing input | PASS: bounded strict catalog load, malformed environment diagnostics, empty selections and safe fallback |
| Empty valid catalog | SAFE: valid metadata availability can be true while selection is empty; it authorizes no capability |
| Mutation / plugin risk | No evaluated code path, dynamic import, package manager or automatic skill loading |
| Existing approval/QA | Unchanged: no caller in production pipeline and no edits to its gates |
| Renderer/pins | Unchanged: caller explicitly selects a renderer; default standalone argument does not change VF's production default |
| Auditability | Selected metadata includes exact capability version, entry digest, skill digest and enclosing catalog digest |
| Actual artifact use | **NOT DEMONSTRATED:** hashes are references; no approved bundle is opened or consumed |

Digests provide integrity tied to the independently reviewed fingerprint, not a signature or automatic proof of human approval.
Evidence strings must be reviewed by the operator; the reader does not prove that referenced documents exist or that their claims
are true. Runtime/dependency observations come from the caller and must not be invented by an activation runbook.

## Publication runbook feasibility

Current CEH publication is intentionally stricter than merely assigning a skill name/version or running catalog export:

1. The resource must already be present in the legacy published catalog, have PRODUCTION status and a current explicit resource
   approval binding its exact upstream pin. Historical PRODUCTION status alone does not qualify.
2. That record must reference the canonical skill through `library_skills`; its licence/security gates must pass.
3. The skill's production approval must bind the exact version and `skill_digest`, plus the independently reviewed full entry digest.
   Skill and resource approval actor/time must match under the current implementation.
4. Every release source URL and pin must match the registry and have passing licence/security gates.
5. The v2 entry must satisfy the complete strict schema, reviewed commercial licence, benchmark/evaluation evidence and compatibility
   requirements. `catalog export` grants no missing approval and cannot fabricate this release envelope.
6. The operator independently accepts the resulting whole-catalog digest before VF opt-in. The consumer must never derive its trusted
   digest automatically from the file it is about to trust.

There is currently no standalone canonical-skill approval command. `ceh approve <resource-id>` approves a resource, not the independent
original CEH instruction bundle. The curated candidates remain unapproved and do not yet contain a production release envelope.
A runbook which says “approve kinetic-type-planning, then export” without addressing these preconditions is not executable as written.
Do not approve an upstream resource merely as an undocumented workaround for releasing an original instruction-only skill.
The exact resource approval scope, original-prose licence, release entry and actor/time binding must be part of Decision A.

## Smallest remaining actions, without another infrastructure phase

- Correct activation documentation to point at the actual branch/commit rather than the detached baseline worktree.
- Keep Decision A (named canonical instruction release and any necessary resource approval/publication scope) separate from Decision B
  (exact VF consumer commit, merge and opt-in metadata use). Neither is authorized by this review.
- Before Decision A, present the immutable skill bundle fingerprint and the complete reviewed entry fingerprint, assign the original
  skill's usage licence and prepare a release envelope matching current publisher preconditions. Do not rely on mutable names/versions.
- Describe first activation honestly as **metadata discovery only**. To claim artifact consumption, separately demonstrate a bounded
  read/verification of the already approved exact instruction artifact and its use in a normal VF job; do not introduce executable plugins
  or bypass existing skill precedence, human gates or QA to make that milestone appear complete.
- After owner-authorized merge, rerun the relevant tests on the actual target tree, whose user-owned uncommitted work must be preserved.

No material defect requiring code change was found in the scoped metadata-only reader. The actual-artifact requirement and standalone
skill publication procedure are acceptance/operating gaps, not permission to broaden the consumer into a plugin system.

## Rollback

Before merge: take no action; the branch is isolated and disabled.
After a separately approved metadata invocation: omit `--enable` / set `enabled=False`; existing routing remains authoritative.
For an earlier catalog: restore both the previously reviewed catalog snapshot and its independently accepted fingerprint. Removing a
catalog entry requires re-export and acceptance of the new whole-catalog digest. No renderer pin or dependency rollback is implicated.
A future revert of commit `b1befad73b4285ce461eb48861e5559c069d2776` requires separate authorization and a clean, protected target tree;
this report does not perform it. Do not reset or clean the original checkout.

## Delivery update - 2026-11-11

The user separately authorized commit/push of completed changes. The reviewed b1befad branch was pushed to
origin/codex/ceh-catalog-consumer and remote refs were verified. No merge, activation or production approval followed.
The managed checkout remains detached at its baseline; the reviewed branch implementation remains in the isolated consumer checkout.
The final acceptance runbook explicitly covers parent-resource/canonical approval bindings and stops before Decision B. Independent
review verified current/prospective bundle fingerprints and clarified proposal-envelope versus entry-preview hash scopes.
