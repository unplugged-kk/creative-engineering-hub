# Creative media review package - 10 November 2026

**Human review and listening are pending.** This package contains a synthetic test-only kinetic typography demonstration,
not an approved production capability, published video or customer deliverable. No approval, merge, activation, export or
publishing action was performed. All three existing outputs were preserved; nothing was re-rendered for this review.

## Open these files

Authoritative review video: [video.mp4](/Users/kishore/Desktop/VideoFactory-Workspace/reports/ceh-acceptance/2026-11-10/kinetic-type-review-165236Z-1c37485d/ceh-benchmark-from-helper/video.mp4).

Representative frames from the encoded video (frames 6, 18, 90 and 168):

![Kinetic typography contact sheet](/Users/kishore/Desktop/VideoFactory-Workspace/reports/ceh-acceptance/2026-11-10/kinetic-type-review-165236Z-1c37485d/ceh-benchmark-from-helper/contact-sheet.png)

- [Full-size held frame at 2 seconds](/Users/kishore/Desktop/VideoFactory-Workspace/reports/ceh-acceptance/2026-11-10/kinetic-type-review-165236Z-1c37485d/ceh-benchmark/held-frame.png)
- [Technical QA](/Users/kishore/Desktop/VideoFactory-Workspace/reports/ceh-acceptance/2026-11-10/kinetic-type-review-165236Z-1c37485d/ceh-benchmark-from-helper/qa.json)
- [Benchmark configuration and selection trace](/Users/kishore/Desktop/VideoFactory-Workspace/reports/ceh-acceptance/2026-11-10/kinetic-type-review-165236Z-1c37485d/ceh-benchmark-from-helper/kinetic-type-plan.json)
- [Measured result](/Users/kishore/Desktop/VideoFactory-Workspace/reports/ceh-acceptance/2026-11-10/kinetic-type-review-165236Z-1c37485d/ceh-benchmark-from-helper/result.json)
- [Exact commands and clean environment](/Users/kishore/Desktop/VideoFactory-Workspace/reports/ceh-acceptance/2026-11-10/kinetic-type-review-165236Z-1c37485d/ceh-benchmark-from-helper/commands.json)
- [Sandbox policy](/Users/kishore/Desktop/VideoFactory-Workspace/reports/ceh-acceptance/2026-11-10/kinetic-type-review-165236Z-1c37485d/ceh-benchmark-from-helper/profile.sb) and [denial probes](/Users/kishore/Desktop/VideoFactory-Workspace/reports/ceh-acceptance/2026-11-10/kinetic-type-review-165236Z-1c37485d/ceh-benchmark-from-helper/probe.json)
- [Synthetic catalog and consumer input](/Users/kishore/Desktop/VideoFactory-Workspace/reports/ceh-acceptance/2026-11-10/kinetic-type-review-165236Z-1c37485d/ceh-fixture-repro-complete/fixture-catalog.json)
- [Consumer invocation](/Users/kishore/Desktop/VideoFactory-Workspace/reports/ceh-acceptance/2026-11-10/kinetic-type-review-165236Z-1c37485d/ceh-fixture-repro-complete/selection-command.json)

## Durable local evidence

The configured `VIDEO_FACTORY_WORKSPACE` environment override is absent and `config/storage.yaml` has workspace null.
The read-only `contentos.storage.workspace_root()` resolver returned `/Users/kishore/Desktop/VideoFactory-Workspace`, which
exists and is writable. A new unique review directory was created under its reports area:

`/Users/kishore/Desktop/VideoFactory-Workspace/reports/ceh-acceptance/2026-11-10/kinetic-type-review-165236Z-1c37485d`

Only 60 explicitly named task-owned files were copied from the four CEH fixture directories. Each source/copy SHA-256 was
compared after copying. No existing files, source artifacts, caches, user media or publishing sidecars were overwritten.
This is a review evidence folder, not the publishing directory. No package was installed and no credentials were accessed.

[Copy manifest](/Users/kishore/Desktop/VideoFactory-Workspace/reports/ceh-acceptance/2026-11-10/kinetic-type-review-165236Z-1c37485d/copy-manifest.json) records source and destination paths, sizes and hashes.
[Fresh verification](/Users/kishore/Desktop/VideoFactory-Workspace/reports/ceh-acceptance/2026-11-10/kinetic-type-review-165236Z-1c37485d/verification.json) records fresh ffprobe results and reread QA counts for all three preserved copies.
The files are outside both repositories and survive ordinary /tmp cleanup. They are still local evidence, not an off-machine backup.

## Fresh technical checks

All three original MP4 files existed, were readable by ffprobe, and were copied without modification:

| Original run | Bytes | Encoded video | Audio | Frames/duration |
|---|---:|---|---|---|
| `/tmp/ceh-benchmark/video.mp4` | 468363 | H.264 High, yuv420p, 1080x1920, 30 fps | AAC, 48000 Hz, stereo | 180 / 6.000 s |
| `/tmp/ceh-benchmark-repro/video.mp4` | 468363 | H.264 High, yuv420p, 1080x1920, 30 fps | AAC, 48000 Hz, stereo | 180 / 6.000 s |
| `/tmp/ceh-benchmark-from-helper/video.mp4` | 468363 | H.264 High, yuv420p, 1080x1920, 30 fps | AAC, 48000 Hz, stereo | 180 / 6.000 s |

Each original and each preserved copy has SHA-256:

`dd5e82dd97a73e4fce1bc1f091ed5b37f17215bb3896d701ce80f868119e2c54`

The ffprobe command was `/nix/store/q3jvds9x1vvl55yj0fj2zqlx57cf7l19-ffmpeg-headless-8.1.2-bin/bin/ffprobe -v error -show_streams -show_format -of json VIDEO_PATH`.
Python hashlib recomputed each hash. Each saved QA report was reread: 8 PASS, 1 WARN, 0 FAIL. Existing QA was not rerun in
this pass because all three encoded files remain byte-identical to the measured checkpoint; fresh ffprobe confirms readability.

| Existing QA check | Status | Recorded finding |
|---|---|---|
| Render integrity | PASS | Readable 6.0-second output |
| Resolution | PASS | 1080x1920 |
| Frame rate | PASS | 30.0 fps |
| Duration | PASS | 6.0 seconds, within 180-second limit |
| Audio track | PASS | AAC present |
| Loudness | PASS | -15.6 LUFS, configured target -14 |
| Clipping | PASS | -14.5 dBFS peak |
| Black frames | PASS | No segment longer than 0.5 seconds |
| Frozen frames | WARN | One held segment longer than 3 seconds |

The WARN reflects the deliberately quiet reading hold. It is retained, not suppressed or reclassified. A hold can be technically
acceptable while still feeling too slow; the human reviewer should make that creative judgement.

## What the frames show and what they cannot prove

The media workstream viewed both the encoded-frame contact sheet and a full-resolution held frame again. The four-word title
has clear hierarchy and one teal emphasis, consistent light background and no visible clipping in those samples. Entrance and
exit frames show the expected lower text opacity. Typography stays left aligned and the accent rule is consistent.

The support caption and footer are small relative to the delivery canvas. They are secondary test annotations, not the main
message. At phone size they may be difficult to read. The sparse composition and long held phrase may feel slow despite its
readability objective. These are review considerations, not measured failures or reasons to change production settings.

This reviewer authored the fixture in the earlier workstream, so these observations are **not an independent critic pass**.
The coordinating agent previously inspected the encoded-frame sheet independently; no user review is inferred from that.
Static samples do not establish normal-speed readability, temporal smoothness, audio pleasantness or synchronization.
No human listening was performed or claimed. No numerical visual-quality score or superiority claim is assigned.

## Capability demonstrated and limits

The fixture applies `kinetic-type-planning` 0.1.0 to one English phrase with a deterministic paused timeline, entrance to frame
18, reading hold to frame 150 and exit through frame 180. The workflow preserves synthetic catalog selection in its plan/result,
uses existing HyperFrames 0.8.114 and existing VF technical QA, and does not load or execute catalog skill content.
The recorded skill digest is `942d06fc400fdf44beb9767d0300f6313cf8366372190325ad6c87799410c679`;
it was recomputed against the current canonical bundle and matches the benchmark reference.

Byte identity supports two local reruns of this exact fixture and runtime. It does not establish creative quality, cross-platform
reproducibility, multilingual shaping, brand suitability, another renderer's behavior, or a real production approval path.
The 440 Hz synthetic tone is a technical audio signal, not narration or music. This is not evidence for `measured-sound-pass`.
The single-canvas study does not exercise VF's two background-diversity rules or its complete gated production job.

An early evidence discrepancy is preserved: the first `/tmp/ceh-benchmark/kinetic-type-plan.json` omits the trailing period,
while the rendered phrase includes it. Both later harness plans contain `Make the idea clear.` exactly. The from-helper trace
is the authoritative review package; no historical evidence was silently rewritten to hide the first-plan punctuation mismatch.

## Reproduction

Follow [the two-stage fixture instructions](/Users/kishore/git/creative-engineering-hub/tools/benchmarks/kinetic_type/README.md):
first `select_fixture.py` generates a synthetic test-only catalog/environment and invokes the isolated VF consumer; then
`run.py` consumes that selection and renders into a new external directory using explicit existing tool paths. Never reuse or
delete an existing output directory to make the harness run. The source instructions and scripts are versioned in CEH.

The saved commands use original task paths, so the durable review copies are for inspection and audit, not in-place rerunning.
Use the README's commands with new output paths. Native sandbox probes must pass before rendering; there is no unsandboxed
fallback. No real capability approval or production consumer activation is granted by reproduction.

## Specific human judgements requested

1. At normal speed and actual phone size, is the main phrase immediately readable, including during entrance and exit?
2. Does the long quiet hold feel intentional, or should timing be revised for the intended production use?
3. Is the single teal emphasis and sparse layout useful for your preferred visual style? Are the small test annotations acceptable?
4. While listening at comfortable volume, is the synthetic tone unpleasant or distracting? Treat it only as a technical test signal.
5. Is the scoped instruction-only planning capability useful enough to approve, knowing this fixture does not prove multilingual,
   brand-specific, narrated or complete production-job behavior?

These review questions do not grant either capability publication or consumer activation. Those remain separate owner decisions.
