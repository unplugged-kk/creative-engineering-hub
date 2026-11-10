# Kinetic typography fixture benchmark - 2026-11-10

## Scope

An original six-second kinetic type composition supplements the existing HyperFrames workflow. The illustrative copy is
"Make the idea clear." It follows the new canonical kinetic-type-planning skill: a single semantic phrase, one emphasis,
18 entrance frames, held interval to frame 150, exit through frame 180, deterministic paused timeline at 30 fps.
The authored tone is a synthetic 440 Hz signal, not narration, licensed music or an audio-quality demonstration.

This is a fixture-only integration benchmark. The VF consumer selection was generated against a synthetic approved catalog;
it does not approve a real CEH candidate. The real production catalog stays empty. No HyperFrames version is changed.

## Isolation and verification

The installed HyperFrames package reports 0.8.114; Node is 24.22.1. Existing local GSAP is copied as a static input, not installed.
A native macOS sandbox confines writes to a disposable external directory, denies private user-file reads except explicit
runtime/QA paths, blocks external networking and permits loopback only for HyperFrames' local server. `env -i` equivalent
clean environment provides a disposable HOME/TMPDIR and no account credentials. Telemetry is disabled.

Isolation probe: arbitrary private HOME file read EPERM, outside-output write EPERM, 1.1.1.1:443 connection EPERM, loopback
connection succeeds. The configured ~/.contentos/secrets path is absent (ENOENT); no credential values were read or printed.
Profile/probe are preserved with the output. A strict deny-default system-file allowlist initially exited 134 without diagnostics;
the final policy uses allow-default with explicit private-data, write and network denial and verified runtime exceptions.
It is a bounded fixture execution environment, not a general hostile-code sandbox certification.

An initial render selected the unusable x86_64 /usr/local ffmpeg because /opt/homebrew/bin/ffmpeg is absent on this machine.
The successful run explicitly used the already installed Nix ffmpeg/ffprobe 8.1.2 paths. No installation or production config
change was needed. Sandbox QA used CEH's existing Python/PyYAML environment to keep the runtime allowlist explicit; the dedicated VF environment remains valid for the host baseline.

## First measured run

- HyperFrames lint: 0 errors, 0 warnings.
- Output: /tmp/ceh-benchmark/video.mp4, 468363 bytes, 1080x1920, 30 fps, 6.0 seconds.
- HyperFrames reported render duration: 9.3 seconds. `/usr/bin/time -l` wall time: 9.99 seconds.
- Reported maximum resident set size: 843399168 bytes. This is the tool's process-tree metric, not a per-frame memory guarantee.
- Existing VF technical QA: 8 PASS, 1 WARN, no FAIL.
- PASS: integrity, resolution, frame rate, duration, audio track, loudness (-15.6 LUFS), clipping (-14.5 dBFS), black frames.
- WARN: held typography generates one frozen_frames segment longer than 3 seconds. Existing QA treats this as WARN.

## Independent visual review and unknowns

The coordinating agent independently viewed encoded-frame contact sheet frames 6, 18, 90 and 168: held title is clear, no
visible clipping, entrance/exit have expected fade opacity. No subjective numeric visual score is assigned. Human listening,
normal-speed readability and temporal smoothness remain unverified. No superiority over another renderer or skill is claimed.
The six-second single-canvas study is not a full production job and does not exercise the two background-diversity rules.

## Reproduction

Original source and sandbox harness: tools/benchmarks/kinetic_type/README.md and run.py. The harness requires a new external
output directory and consumer-generated selection trace, then verifies isolation before lint, render and existing technical QA.
No code from catalog entries is executed. All binaries are explicit pre-existing paths. Selection must be produced through the
consumer's version/integrity/approval/compatibility validation before passing it to the fixture harness.

Initial evidence directory: /tmp/ceh-benchmark/ (profile.sb, probe.json, kinetic-type-plan.json, selection.json, lint.log,
render.log, qa.json, contact-sheet.png, video.mp4). These local disposable artifacts are not committed media.

## Reproduced consumer-to-render trace

The persisted harness was run successfully against /tmp/ceh-benchmark/selection.json, produced by the isolated VF consumer
against /tmp/ceh-benchmark/fixture-catalog.json and environment.json. Selection identifies kinetic-type-planning version 0.1.0,
renderer hyperframes and its fixture entry digest. It explicitly labels its approval synthetic and test-only.
The harness stores that exact structured selection in the kinetic type plan and benchmark result. The reader supplies guidance
metadata; it does not load or execute the skill. The authored composition is the deliberate manual planning step in that workflow.

Reproduced output: /tmp/ceh-benchmark-repro/video.mp4. Wall time 10.355 seconds; maximum resident set size 842596352 bytes.
QA repeated with the same 8 PASS, 1 WARN. Full evidence is in /tmp/ceh-benchmark-repro/result.json, commands.json, profile.sb,
probe.json, selection.json, kinetic-type-plan.json, render.log, qa.json and contact-sheet.png.

Both encoded outputs have identical SHA-256:
`dd5e82dd97a73e4fce1bc1f091ed5b37f17215bb3896d701ce80f868119e2c54`.
This establishes repeatability for two local runs of this exact fixture and installed runtime, not cross-platform reproducibility.
The fixture exercises discovery and compatible selection through a real VF consumer, deterministic authored composition,
the existing renderer and existing technical QA. Real owner-approved capability consumption remains pending; no fixture
approval or successful render is promoted into the production catalog.

## Fresh two-stage command reproduction

`select_fixture.py` now regenerates the test-only catalog/environment and invokes the isolated VF consumer, so reproduction
no longer depends on an ephemeral root command. The helper was verified into /tmp/ceh-fixture-repro-complete, then run.py
rendered /tmp/ceh-benchmark-from-helper/video.mp4. The third output matches the same SHA256 above, with the same sandbox
probe results and existing QA8PASS1WARN. README documents both commands with explicit existing paths and new output directories.
