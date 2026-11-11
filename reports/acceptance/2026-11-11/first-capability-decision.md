# First capability decision - independent review

Review date: 2026-11-10. Reviewed CEH checkpoint: `1ac01c3a2a92abe1b44e687806c43c86d0b7f711`.
Scope: two instruction-only canonical bundles, their immutable research sources, current governance metadata and recorded
benchmark/agent evidence. No approval, publication, installation, metadata edit or production activation was performed.

## Decision

**Neither candidate is ready for unconditional publication today. Keep both as research candidates.**
`kinetic-type-planning` 0.1.0 is the recommended **first capability to take to a narrowly scoped owner approval**, after the
licence/usage decision, reviewed release metadata and remaining media acceptance below. It has a relevant sandboxed render and
bounded Codex planning evidence. `measured-sound-pass` 0.1.0 should remain a research candidate: there is no corresponding real
sound-pass benchmark or listening evidence. Neither is rejected; neither is represented as production-approved.

A successful fixture render or a permissive upstream licence does not approve the original CEH bundle. This review supplies a
recommendation, not the owner's approval.

## Exact reviewed artifacts

The fingerprints below were computed from the live bundles using `ceh.catalog_publish.skill_digest` without modifying them.
This algorithm binds all bundle paths and file bytes, normalizes top-level skill.yaml, and excludes its approval and catalog_release
envelopes to avoid self-reference. It is a content fingerprint, not a signature or proof of author identity. A published release
also requires the separately reviewed catalog-entry digest bound in its approval metadata.

| Candidate | Version | Current bundle SHA-256 | Current state |
|---|---|---|---|
| kinetic-type-planning | 0.1.0 | `942d06fc400fdf44beb9767d0300f6313cf8366372190325ad6c87799410c679` | candidate; approval unapproved; production_eligible false |
| measured-sound-pass | 0.1.0 | `b979f23298e823665e70cdd3bc5f1e6b6daaab9bf9de212e19f2eded66687a10` | candidate; approval unapproved; production_eligible false |

Each contains eight files: SKILL.md, skill.yaml, README.md, VERSION.md, one example, evaluation cases, provenance and a scripts
boundary note. There are no executable scripts, bundled fonts, sounds, images, models or third-party implementation files.
`uv run ceh skills validate --json` returns `all skills valid`; that establishes structure only. Metadata verification fields
still say pending/unverified and have not been silently updated to claim later evidence.

**No exact real release-entry digest exists yet.** No synthetic fixture entry fingerprint should be substituted for it.
Changes to licence/usage metadata, examples, guidance or verification fields change the bundle fingerprint. Recompute and present
the new version/fingerprint for approval after any such edit; do not approve a mutable name or version alone.

## Side-by-side assessment

| Review dimension | kinetic-type-planning 0.1.0 | measured-sound-pass 0.1.0 |
|---|---|---|
| Intended benefit | Exact-copy preservation, deterministic frame timing, readable holds and bounded frame-review plan | Rights-aware cue planning, final-export audio measurement, separate listening verdict |
| Existing VF fit | Complements existing HyperFrames direction/composition; does not replace renderer or job contracts | Complements existing audio QA; explicitly defers thresholds and mixing to consuming project |
| Dependencies of skill itself | None: instructions only, no install hook or executable | None: instructions only, no install hook or executable |
| Actual execution environment | Fixture used existing HyperFrames 0.8.114, Node 24.22.1, GSAP, Chromium through existing renderer and explicit ffmpeg/ffprobe 8.1.2 | No actual cue implementation/mix/render demonstrated; would require the existing approved mixing/measurement tools and rights-verified local audio |
| Transitive dependency finding | No new dependency introduced. Complete transitive vulnerability audit of the pre-existing renderer/browser stack is not established | No skill dependency tree to install. Runtime/mixer transitive audit remains unverified if subsequently executed |
| Agent evidence | Current Codex canonical-file planning invocation and Codex-authored sandbox fixture; no exact binary/model version exposed in that evidence | Portable metadata/frontmatter plus structural validation; no recorded real sound-pass invocation |
| Language limits | English-only benchmark. Hindi/other shaping, fonts, line breaking and normal-speed reading not verified | No language-specific narration/listening or localisation verification |
| Output limits | Plan JSON and checklist; one 1080x1920 MP4 fixture. Not a general renderer adapter, actual production request or all-platform export test | Cue JSON and review plan only. No measured mix or encoded sound-pass output |
| Benchmarks | Three currently present MP4s are byte-identical; recorded QA 8 PASS, 1 WARN | None demonstrating the skill's sound-pass purpose. Typography fixture's synthetic tone is not sound-design validation |
| Creative acceptance | Representative-frame inspection recorded; normal-speed/human review not recorded as accepted | Real cue alignment, intelligibility, stereo/mono behavior and human listening all unverified |
| Immediate recommendation | Keep research status; preferred first bounded instruction-only approval candidate after stated conditions | Keep research status pending a relevant rights-verified audio benchmark and listening review |

## Immutable source provenance and attribution

The bundles contain original CEH prose synthesizing general concepts. The original source attribution and source commit references
are retained in each `references/provenance.md` and `skill.yaml`. No claim is made that an upstream approval transfers to CEH.
Source pin, recorded registry pin and actual analysed commit were checked independently in the live registry.

| Used by | Source | Exact reviewed research commit | Licence evidence at that commit |
|---|---|---|---|
| kinetic-type-planning; measured-sound-pass | CEH-0018 LottieFiles/motion-design-skill | `f9a8a041b85185ee4881b3471d3415e939aac772` | Root LICENSE, MIT; Copyright 2025 LottieFiles |
| kinetic-type-planning | CEH-0002 charlie947/motion-graphics-skills | `229022ebca76972e119e36ada23a1648d51665ab` | Root LICENSE, MIT; Copyright 2026 Charlie Hills |
| measured-sound-pass | CEH-0004 Barty-Bart/motion-graphics | `d6e5d95e45167d95bb4260b9da4d674791143710` | Root LICENSE, MIT; Copyright 2026 Bart; fonts separately licensed |

Immutable links:

- https://github.com/LottieFiles/motion-design-skill/tree/f9a8a041b85185ee4881b3471d3415e939aac772
- https://github.com/charlie947/motion-graphics-skills/tree/229022ebca76972e119e36ada23a1648d51665ab
- https://github.com/Barty-Bart/motion-graphics/tree/d6e5d95e45167d95bb4260b9da4d674791143710

Root licence blobs were read from existing local git objects with `git show <commit>:LICENSE`, without checkout or execution.
Their text SHA-256 values were respectively:

- CEH-0018: `9fc2e8685daa09e28d54b6afa8a38f168417c5735a3cd676c80c159785e93a80`
- CEH-0002: `ed17713237d18555a34c208bf0cb1ce347faa937731d509e265ce91be660e218`
- CEH-0004: `40a5f89f85b8345b3af943b0e2d28dc7199ff83ddf9d905cded0abcc38431672`

Source file review from the curation report: LottieFiles timing/easing and quality-checklist references; Charlie Hills motion-effects
and motion-brief-writer skills; Barty-Bart sound-effects skill. The latter includes upstream installation/download instructions and
per-asset licensing distinctions; neither its scripts nor its media are included in CEH's candidate.

Current source review gates pass for all three registry records. CEH-0018 analysed commit equals the research pin; CEH-0002 likewise.
CEH-0004's recorded analysed commit is `3d83d987d658601d8a1269eb691622bdcd427335`, different from the curated research pin above.
Do not describe that static scan as an exact-pin scan of d6e5d95e. The pinned licence blob and instruction file were inspected, but a
complete source/security/transitive audit at that historical pin is not supplied by this dossier.

Source attribution remains useful even though no substantial third-party code/assets are copied. If subsequent work copies or
redistributes licensed material, preserve the applicable notices and evaluate asset-specific terms separately. This report does not
offer a legal conclusion about the distribution rights of original or derivative text.

## Licence and usage blocker

Both skill.yaml files currently state `original CEH instructions; no new redistribution licence granted`. Their upstream MIT references
do not assign a licence to the newly authored CEH prose. There is no approved release licence/usage declaration in either candidate.
This is a governance gap, not evidence that either candidate contains non-commercial material or must be rejected.

Before publication, the owner must explicitly choose the permitted use/distribution scope for the original CEH instructions, and
review how it is represented in the v2 entry's licence/restrictions/evidence fields. Internal owner-controlled use and unrestricted
external redistribution are different scopes; neither is silently assumed by this review. Do not relabel the bundle MIT merely
because its research references are MIT. Any metadata correction requires a newly computed bundle fingerprint.

## Security and supply-chain scope

The two skills are non-executing guidance. They cannot install dependencies by themselves and do not contain download/install hooks.
Their instructions keep existing VF renderer pins, approvals, QA thresholds and skill precedence authoritative. They require explicit
asset rights and prevent a repository licence from being treated as permission for bundled audio. No zero-vulnerability or formal
security-certification claim is made.

The consumer is metadata-only; it does not load SKILL.md or execute catalog steps. Any future agent reads guidance deliberately within
its own task/permission boundary. A catalog match must not turn text into execution authority. Independent producer/consumer review
is recorded in the continuation security report. It found and resolved post-approval metadata/byte mutation bypasses; production
publication requires both reviewed bundle and exact entry digests plus independently configured catalog trust.

## Benchmark evidence and its limit

The three paths below exist at this review and hash identically:

- `/tmp/ceh-benchmark/video.mp4`
- `/tmp/ceh-benchmark-repro/video.mp4`
- `/tmp/ceh-benchmark-from-helper/video.mp4`

Encoded SHA-256: `dd5e82dd97a73e4fce1bc1f091ed5b37f17215bb3896d701ce80f868119e2c54`.
The recorded output is 1080x1920, 30 fps, 6.0 seconds. Existing technical QA records 8 PASS, 1 WARN; WARN is a held-text frozen-frame
segment longer than three seconds. Lint records 0 errors and 0 warnings. Commands, sandbox probe, tool paths, source and outputs are
in `reports/continuation/2026-11-10/benchmark.md` and `tools/benchmarks/kinetic_type/README.md`.

This is a synthetic-approved fixture, with authored composition and synthetic tone. It proves a useful repeatable technical path,
not owner-approved real catalog consumption, independent creative acceptance or multilingual support. It is not evidence that a
measured sound pass was completed. Normal-speed motion/readability and any claimed auditory quality require separate review.
The `/tmp` files are ephemeral; preserve accepted evidence in an approved durable external workspace before release reliance.

## Proposed bounded first approval scope

After resolving the blockers, the sensible first owner decision is for **kinetic-type-planning**, an exact reviewed version and
bundle fingerprint, as original instruction-only planning guidance for the existing HyperFrames 0.8.114 path. Scope should remain
English title planning with exact-copy preservation and a normal gate-preserving handoff. Do not promise new runtime, new renderer,
festival/cultural correctness, general multilingual typography, automatic skill loading, installed third-party software or publishing.

This would not approve measured-sound-pass, ratify historical PRODUCTION records, upgrade HyperFrames, merge/enable the consumer,
permit downloads, or grant any job-level script/production/publish approval. Owner approval and consumer activation are separate.

Publication prerequisites:

1. Owner-approved original-prose usage/licence scope, recorded without claiming unverified rights.
2. Accepted human media review, including the frozen-frame WARN and known scope limits; no claim the owner has already reviewed it.
3. Exact reviewed release entry containing approved input/output/language/runtime constraints, evidence and current source pins.
4. Final bundle fingerprint and entry fingerprint presented together after metadata is finalized.
5. Explicit owner approval and publication authorization. Until then, leave candidate status and the real catalog unchanged.

There is no pre-existing release envelope to publish as-is. `ceh catalog export` does not manufacture these approvals or licensing facts.
The operating runbook must provide the final concrete release and commands after its scoped human decision; this dossier grants none.

## Installation and rollback implications

Neither candidate is installed globally by this review. Installing a shared canonical symlink would expose future bundle edits at
that location, so installation must not stand in for an immutable release approval. The catalog pins bundle/version/entry fingerprints,
and its reader returns metadata only. Preserve that separation in any approved installation or agent-invocation procedure.

For a future published release, stop opting into the consumer and revert to existing routing; withdraw the affected catalog release
through the documented CEH path and restore the previously reviewed catalog file and trusted fingerprint together. Do not reset VF,
rewrite pins, delete user files or treat a changed catalog's self-reported digest as trust. No rollback is currently needed because no
capability publication or consumer activation occurred.

## Reverification commands executed

- `uv run ceh skills validate --json`: all skills valid.
- Read-only `skill_digest(Path('library/skills') / name)` for both candidates: fingerprints above.
- Read-only registry/pin/analysed-commit comparison for CEH-0018, CEH-0002 and CEH-0004: results above.
- Static `git show <commit>:LICENSE` for each existing source clone: licence evidence above.
- Read-only SHA-256 of all three MP4s: identical hash above.

The reviewer did not run upstream code, re-render, listen to audio, install candidates, change metadata, approve or publish anything.
This dossier is a scoped independent review and must be read alongside the final media, agent-interoperability and consumer reports.

## Finalized 2026-11-11 preview addendum

The canonical candidates remain unchanged. To make the owner decision concrete, the coordinator staged only proposed future
metadata outside the canonical library and committed a non-authoritative proposed-skill-metadata.yaml in this report package.
The proposed kinetic-type-planning0.1.0 release bundle has SHA256
`addfcc1b9a8f19cc3ba1c28b03abdfb25f954dc29208e96414515a7f9ee300b0`.
Both independent reviews confirmed that source pins, file set and every non-skill.yaml byte match the current candidate; the
report YAML parses identically to the staged metadata. It proposes internal commercial planning permission/no external redistribution,
active status and honest evidence limitations. None of that is applied or granted in the canonical library today.

The prospective bundle is a conditional approval target, not a current approved capability. Owner acceptance of media and usage
scope remains required. Choosing a different scope requires another preview fingerprint. The complete release proposal stays
CANDIDATE/PENDING_OWNER_DECISION and cannot pass the production validator even if mechanically sealed. The proposal envelope
fingerprint and non-consumable entry-preview fingerprint are separately defined in the runbook; neither substitutes for a final
entry fingerprint containing the real owner actor/time/evidence. Decision B must review the final published snapshot after A.
