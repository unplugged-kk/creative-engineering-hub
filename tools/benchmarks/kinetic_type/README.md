# Isolated kinetic typography fixture

This is an original six-second test composition informed by the canonical `kinetic-type-planning` skill. It uses the existing
Video Factory HyperFrames installation, its local GSAP asset, and synthesized illustrative tone. No package is installed or
fetched. It never executes commands or imports code from catalog entries.

`run.py` requires an existing selection JSON produced by the opt-in VF consumer. The continuation demonstration uses a
synthetically approved fixture catalog. A fixture approval is not approval of a real CEH resource or production capability.
The selection trace is preserved in `selection.json`, `kinetic-type-plan.json` and `result.json` in the output directory.
The harness does not authenticate an arbitrary selection JSON by itself: the consumer must validate the catalog first.

First generate a fresh **synthetic test-only** catalog and selection using the isolated VF consumer checkout. Supply runtime
versions from measurements already taken; this helper does not probe Node or HyperFrames, approve a resource, or change a
production catalog. Its source URL and all-zero pin are deliberate fixture data, not upstream provenance. The skill bundle
reference uses CEH's current `skill_digest` API, so changes to the canonical skill are reflected in the fixture.

```sh
uv run python tools/benchmarks/kinetic_type/select_fixture.py \
  --vf /tmp/ceh-vf-consumer \
  --python /Users/kishore/.contentos/venv/bin/python \
  --node-version 24.22.1 \
  --hyperframes-version 0.8.114 \
  --output /tmp/ceh-fixture-repro-complete
```

The `--vf` path here must contain the proposed read-only `contentos.ceh_catalog` module. It is intentionally different from
the unchanged production checkout used as the render engine below. The helper invokes only that metadata consumer with a
clean HOME/environment and writes catalog, measured-environment declaration, exact consumer command and selection evidence.
No external scripts are imported and no binaries are installed. An output path that already exists is refused.

Then run on macOS from CEH with explicit paths to already installed binaries and another new directory outside both repositories:

```sh
uv run python tools/benchmarks/kinetic_type/run.py \
  --vf /Users/kishore/git/video-factory \
  --node /Users/kishore/.nvm/versions/node/v24.22.1/bin/node \
  --chrome /Users/kishore/.cache/hyperframes/chrome/chrome-headless-shell/mac_arm-152.0.7977.30/chrome-headless-shell-mac-arm64/chrome-headless-shell \
  --ffmpeg /nix/store/q3jvds9x1vvl55yj0fj2zqlx57cf7l19-ffmpeg-headless-8.1.2-bin/bin/ffmpeg \
  --ffprobe /nix/store/q3jvds9x1vvl55yj0fj2zqlx57cf7l19-ffmpeg-headless-8.1.2-bin/bin/ffprobe \
  --python /Users/kishore/git/creative-engineering-hub/.venv/bin/python3 \
  --selection /tmp/ceh-fixture-repro-complete/selection.json \
  --output /tmp/ceh-benchmark-repro
```

Existing output directories are refused. Change `--output` for another run; do not remove previous evidence.
The Python interpreter needs PyYAML for existing VF QA. The exact installed versions are recorded in each result/log.

The native sandbox has no inherited credentials or host HOME. It denies file reads under users, private temporary locations
and mounted volumes except the selected tool directories, the read-only VF QA code/config, the CEH Python environment and
the new output directory. Filesystem metadata is allowed for path traversal. Writes are confined to output plus `/dev/null`.
External networking is denied; loopback is allowed for the renderer's local server. Telemetry is disabled. The harness verifies
HOME read denial, outside-directory write denial, loopback access and external-network denial before lint/render. No
unsandboxed fallback exists. This boundary is for the known installed runtime and original fixture, not permission to run
arbitrary upstream install scripts. System services and public system files remain available to the installed renderer.

Artifacts: plan, selection trace, sandbox policy/probe evidence, exact commands and clean environment, lint/render logs,
video.mp4, qa.json, contact-sheet.png and result.json. No media is written into either repository.

Technical QA passes do not establish normal-speed readability, pleasant sound, language shaping, production approval or
comparative visual quality. View the output and obtain independent review before making those claims.
