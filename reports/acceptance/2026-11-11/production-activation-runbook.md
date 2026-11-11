# First production release runbook

Date: 2026-11-11. **Preparation only. No approval, publication, merge or activation has been executed.**
Decision A and Decision B are separate. A documentation Git push is neither decision.

## Five separate lifecycle events

1. Intake: `uv run ceh add URL` registers a research resource and inspects it statically. It grants no usage approval.
2. Capability approval: the owner reviews exact original guidance, source pins, usage licence, evidence and fingerprint.
3. Catalog publication: the reviewed approved release is sealed and exported. Export cannot invent missing approval.
4. VF eligibility: an independently reviewed catalog fingerprint plus explicit opt-in allow metadata discovery/selection.
5. Production job: an explicitly authorised planner uses verified guidance in the existing VF workflow, with unchanged script,
   production and QA gates. Metadata selection grants no job gate or publishing permission.

## Candidate and non-consumable preview

Preferred first candidate: kinetic-type-planning 0.1.0. Current bundle SHA256:
`942d06fc400fdf44beb9767d0300f6313cf8366372190325ad6c87799410c679`.

The current bundle has no owner-assigned original-prose release licence. To make Decision A concrete without changing it,
proposed-skill-metadata.yaml describes a non-authoritative post-approval preview: active status, internal commercial planning
permission with no external redistribution, and honest verification limitations. The prospective bundle fingerprint is:
`addfcc1b9a8f19cc3ba1c28b03abdfb25f954dc29208e96414515a7f9ee300b0`.

Only that proposed skill.yaml changes; the other seven bundle files remain byte-identical. The canonical skill is untouched.
The skill digest algorithm canonicalizes this YAML and excludes approval/catalog_release envelopes, so adding the actual
owner approval later does not alter the prospective guidance fingerprint. A different licence or metadata choice needs a
newly calculated preview and fresh owner review. Never assign the upstream MIT licence to the original CEH prose by inference.

release-proposal.json is deliberately invalid as a consumable catalog: CANDIDATE/PENDING_OWNER_DECISION, not APPROVED.
Its current proposal fingerprint is `d25916755faded6bd83e4c4be9e3dd540fddfd307fb1d63e606fa89e5637143c`.
It is a review artifact, not the final entry fingerprint or production approval.

The real final entry fingerprint cannot truthfully exist before the owner decision and its actor/time/evidence are recorded.
After Decision A, the final exact entry/catalog fingerprints must be displayed for Decision B. Do not substitute synthetic
fixture hashes, a mutable name/version, or the current empty catalog's fingerprint.

## Decision A: capability approval and publication

HOLD until the owner explicitly accepts the media/usage scope and proposed fingerprint. Scope requested:

- Original instruction-only kinetic-type-planning 0.1.0, English title planning with the existing HyperFrames0.8.114 path.
- Internal commercial production planning only; no skill redistribution/sublicensing, renderer upgrade, dependency install,
  global agent installation, unattended-agent compatibility claim, production job gate or publication permission.
- Preserve pinned MIT source attribution: LottieFiles f9a8a041b85185ee4881b3471d3415e939aac772 and Charlie Hills
  229022ebca76972e119e36ada23a1648d51665ab. No upstream code/assets are installed or consumed.
- Explicitly authorize the current publisher's required CEH-0018 resource approval/publication bookkeeping solely as the parent
  record for this canonical guidance. Do not silently approve the whole upstream project for execution as a workaround.

If that expanded bookkeeping scope is not accepted, STOP publication and propose a minimal independent-capability approval
change. This mission does not implement more infrastructure to hide the distinction.

After A is explicitly granted, from CEH:

1. Verify clean/reviewed state, candidate and prospective bundle fingerprints, source URL/pins/gates, and durable evidence.
   Record the actual owner message, scope and time in an approval audit document. Never backdate or fabricate a review note.
2. Execute `uv run ceh approve CEH-0018 --json` only within the explicit resource-bookkeeping scope above. Read its real
   `approval.by`, `approval.at` and pin from Registry. These exact values must bind the canonical release under the current code.
3. Apply only proposed-skill-metadata.yaml to the canonical skill.yaml after owner permission; assert the approved prospective
   bundle digest. Populate approval and catalog_release envelopes via reviewed YAML/Registry APIs, not generated report edits:
   - Skill approval: APPROVED, production_eligible true, version0.1.0, approved bundle digest, the exact actor/time above.
   - Start from release-proposal.entry; replace only pending status/approval/permission-evidence fields with factual owner approval,
     retain reviewed compatibility/requirements/guidance, and reference the owner decision/media acceptance evidence.
   - Calculate the canonical complete entry digest and bind it as approval.catalog_entry_digest. Record the exact final payload.
   - Set CEH-0018.library_skills to only kinetic-type-planning. No other canonical skills are implicitly approved.
   There is no canonical-skill approval CLI. This is a separately reviewed controlled metadata update, not an available command
   named `ceh approve kinetic-type-planning`. Any unreviewed substantive change requires a new decision.
4. Execute `uv run ceh integrate CEH-0018 --test --json` only after that separate publication authorization within A. A failing
   regression leaves the resource APPROVED and stops publication. This writes CEH's legacy catalog, not VF source.
5. Execute `uv run ceh catalog export --json`. Verify exactly one expected v2 entry, no excluded release, the final approved
   skill/version/digest, current pins, explicit original-guidance permission and all mandatory evidence.
6. Run `uv run ceh validate --json`, `uv run ceh skills validate --json` and relevant publisher/contract tests. Record approval,
   legacy publication, v2 publication and exact final fingerprints as separate audit events. Commit authorised CEH metadata only.
7. Present the final exact entry and catalog fingerprints for Decision B. STOP here. Do not enable VF under A.

The proposed entry intentionally has no named agent support and no executable skill loading. No named agent CLI produced independently verified plan output.
The initial human-reviewed test is English/vertical; other language/brand/narration claims remain out of scope.

## Decision B: consumer merge and controlled opt-in

Reviewed consumer commit: `b1befad73b4285ce461eb48861e5559c069d2776`, codex/ceh-catalog-consumer.
Actual code is in /tmp/ceh-vf-consumer; the similarly named managed checkout is detached at the baseline and must not be
mistaken for the reviewed commit. Pushing this isolated branch is authorised documentation/engineering delivery, not B.

The current branch is merge-reviewable as a metadata-only provider. It does NOT yet prove approved bundle use. Owner scope
must state whether B authorizes only metadata discovery or a later verified guidance handoff. Do not label metadata-only opt-in
as automatic capability consumption. A production-consumption claim stays on hold until actual approved-artifact verification
and the normal VF job flow are demonstrated.

After a specific B is granted:

1. Reverify exact branch/target commits and original VF tracked/untracked state. Merge only on an owner-authorised clean target;
   do not stash/reset/clean or force a dirty user checkout into the merge. Reconfirm safe merge target if main has moved.
   The exact reviewed change is b1befad; no unrelated WIP or renderer changes are part of it.
2. Rerun relevant tests on the actual merged target. Preserve publishing disabled, renderer pin0.8.114, ContentForge and all gates.
3. Use an explicitly measured environment JSON. No package discovery/installation, guessed versions or user-global skill copies.
4. Invoke metadata discovery only with the separately accepted final catalog fingerprint:

```
~/.contentos/venv/bin/python -m contentos.ceh_catalog --enable \
  --catalog /Users/kishore/git/creative-engineering-hub/integrations/video-factory/catalog-v2.json \
  --trusted-digest FINAL_OPERATOR_REVIEWED_CATALOG_SHA256 \
  --task 'kinetic typography' --renderer hyperframes --environment /ABSOLUTE/MEASURED-ENVIRONMENT.json
```

5. Check selected entry and skill fingerprints against the actual approved local artifact before any deliberately authorised
   planner reads it. The current reader returns references and does not perform that disk verification. Do not bypass this
   gap with mutable names, automatic external skill loading or a downloaded plugin. Record any minimal handoff change separately.
6. Prepare a disposable project in the existing workspace. Show the script/title and composition for the existing approvals;
   normal rendering/QA/independent critic still apply. Neither A nor B grants job gates or publishing permission.

## Operating cycle, withdrawal and recovery

Discovery/intake -> evidence and source review -> exact capability approval -> separately audited catalog publication ->
operator-pinned consumer eligibility -> existing VF job approvals/QA -> upstream monitoring. No auto-adoption.

For monitoring use `uv run ceh upstream check --all --report` and `uv run ceh upstream report CEH-0018 --json`; inspect changed
source/asset terms and dependencies, preserve pins and request a new decision for updates. Weekly policy does not create a scheduler.

Rollback metadata discovery by omitting --enable; this never changes the existing pipeline. Withdraw an authorised publication
with `uv run ceh withdraw CEH-0018 --note 'OWNER-APPROVED-REASON' --json`, re-export v2, and review/accept its new whole-catalog
fingerprint. Restore an earlier reviewed catalog and its independently accepted fingerprint together if directed. Do not change
upstream pins, reset worktrees or delete user files. Any revert of a merged VF commit requires explicit authorization.

Proposal fingerprint algorithm: UTF-8 canonical JSON of the entire release-proposal.json envelope with proposal_digest omitted, sorted keys, Unicode preserved, compact comma/colon separators and no NaN. It is distinct from contract.digest(entry). The current non-consumable entry-preview digest is `c52670fb735a13ecc408f06c57404b92c571e226d0cd219d0a14a0fbd9ab9392`; neither value is the final owner-approved entry fingerprint.
