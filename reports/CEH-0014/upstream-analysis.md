# CEH-0014 · heygen-com/hyperframes

https://github.com/heygen-com/hyperframes

| Field | Value |
|---|---|
| Strategy | PINNED |
| Remote | https://github.com/heygen-com/hyperframes |
| Default branch | main |
| Pinned commit | 01c6f6004a00ecfa6e77ab4025b47a46a5e925fc |
| Latest observed | cda84222aa12716f2ceb92b45629487be81a0601 |
| Latest release | v0.9.30 |
| Forks | https://github.com/kishorehq/hyperframes |
| Last checked | 2026-11-10T16:03:15+00:00 |
| Flags | Upstream has new commits |

## Change summary 01c6f6004a → cda84222aa

1858 commits, 5654 files changed.

### Breaking signals
- 7f48a689 feat!: remove Plan v1 distributed transport (#6970)
- 68822931 feat(skills)!: publish seven knowledge skills aligned with Studio and retire the workflow skills (#5651)
- abe97f6e refactor(inspector)!: drop the predefined agent tools; harnesses define their own (#5570)

### Licence files changed
- none

### Dependency manifests
```json
{
  "packages/parsers/package.json": {
    "version": [
      "0.8.114",
      "0.9.30"
    ],
    "added": [
      "entities"
    ],
    "removed": [],
    "changed": {}
  },
  "packages/producer/package.json": {
    "version": [
      "0.8.114",
      "0.9.30"
    ],
    "added": [],
    "removed": [
      "@fontsource/archivo-black",
      "@fontsource/eb-garamond",
      "@fontsource/ibm-plex-mono",
      "@fontsource/inter",
      "@fontsource/jetbrains-mono",
      "@fontsource/league-gothic",
      "@fontsource/montserrat",
      "@fontsource/nunito",
      "@fontsource/oswald",
      "@fontsource/outfit",
      "@fontsource/space-mono",
      "wawoff2"
    ],
    "changed": {
      "@hyperframes/core": [
        "workspace:^",
        "workspace:*"
      ],
      "@hyperframes/studio-server": [
        "workspace:^",
        "workspace:*"
      ],
      "puppeteer": [
        "^25.2.1",
        "~25.11.0"
      ],
      "@hyperframes/engine": [
        "workspace:^",
        "workspace:*"
      ],
      "puppeteer-core": [
        "^25.2.1",
        "^25.11.0"
      ],
      "@hyperframes/parsers": [
        "workspace:^",
        "workspace:*"
      ],
      "@hyperframes/lint": [
        "workspace:^",
        "workspace:*"
      ]
    }
  },
  "packages/gcp-cloud-run/package.json": {
    "version": [
      "0.8.114",
      "0.9.30"
    ],
    "added": [],
    "removed": [],
    "changed": {}
  },
  "packages/cli/package.json": {
    "version": [
      "0.8.114",
      "0.9.30"
    ],
    "added": [
      "acorn",
      "undici",
      "yauzl"
    ],
    "removed": [
      "prettier",
      "sharp"
    ],
    "changed": {
      "esbuild": [
        "^0.25.12",
        "^0.28.2"
      ]
    }
  },
  "packages/share/package.json": {
    "version": [
      null,
      "0.9.30"
    ],
    "added": [],
    "removed": [],
    "changed": {}
  },
  "registry/blocks/godrays/source/package-lock.json": {
    "changed": true
  },
  "packages/sdk/package.json": {
    "version": [
      "0.8.114",
      "0.9.30"
    ],
    "added": [],
    "removed": [],
    "changed": {}
  },
  "packages/core/package.json": {
    "version": [
      "0.8.114",
      "0.9.30"
    ],
    "added": [
      "acorn",
      "wawoff2"
    ],
    "removed": [
      "bpm-detective"
    ],
    "changed": {}
  },
  "packages/inspector/package.json": {
    "version": [
      null,
      "0.9.30"
    ],
    "added": [
      "@hyperframes/core",
      "@hyperframes/parsers",
      "@jridgewell/trace-mapping",
      "acorn",
      "esbuild",
      "eslint-scope",
      "htmlparser2",
      "postcss",
      "puppeteer-core"
    ],
    "removed": [],
    "changed": {}
  },
  "packages/shader-transitions/package.json": {
    "version": [
      "0.8.114",
      "0.9.30"
    ],
    "added": [],
    "removed": [],
    "changed": {}
  },
  "registry/blocks/frost-sequence-camera-orbit/source/package.json": {
    "version": [
      null,
      null
    ],
    "added": [],
    "removed": [],
    "changed": {}
  },
  "packages/aws-lambda/scripts/runtime-lock/sparticuz/package.json": {
    "version": [
      null,
      "0.0.0"
    ],
    "added": [
      "@sparticuz/chromium",
      "puppeteer-core"
    ],
    "removed": [],
    "changed": {}
  },
  "packages/engine/package.json": {
    "version": [
      "0.8.114",
      "0.9.30"
    ],
    "added": [
      "undici"
    ],
    "removed": [],
    "changed": {
      "puppeteer": [
        "^25.8.0",
        "~25.11.0"
      ],
      "puppeteer-core": [
        "^25.8.0",
        "^25.11.0"
      ]
    }
  },
  "packages/aws-lambda/scripts/runtime-lock/chrome-headless-shell/package.json": {
    "version": [
      null,
      "0.0.0"
    ],
    "added": [
      "puppeteer-core"
    ],
    "removed": [],
    "changed": {}
  },
  "package.json": {
    "version": [
      null,
      null
    ],
    "added": [
      "yaml"
    ],
    "removed": [],
    "changed": {}
  },
  "packages/player/package.json": {
    "version": [
      "0.8.114",
      "0.9.30"
    ],
    "added": [],
    "removed": [],
    "changed": {}
  },
  "packages/aws-lambda/package.json": {
    "version": [
      "0.8.114",
      "0.9.30"
    ],
    "added": [
      "@aws-sdk/client-ecr",
      "@aws-sdk/client-lambda",
      "@aws-sdk/s3-request-presigner"
    ],
    "removed": [],
    "changed": {
      "@aws-sdk/client-s3": [
        "^3.700.0",
        "^3.1146.0"
      ],
      "@aws-sdk/client-sfn": [
        "^3.700.0",
        "^3.1146.0"
      ]
    }
  },
  "registry/examples/path-traced-3d/source/package.json": {
    "version": [
      null,
      null
    ],
    "added": [],
    "removed": [],
    "changed": {}
  },
  "packages/lint/package.json": {
    "version": [
      "0.8.114",
      "0.9.30"
    ],
    "added": [
      "ignore"
    ],
    "removed": [],
    "changed": {}
  },
  "registry/examples/path-traced-3d/source/package-lock.json": {
    "changed": true
  },
  "packages/aws-lambda/scripts/runtime-lock/chrome-headless-shell/package-lock.json": {
    "changed": true
  },
  "packages/studio-server/package.json": {
    "version": [
      "0.8.114",
      "0.9.30"
    ],
    "added": [],
    "removed": [
      "sharp"
    ],
    "changed": {}
  },
  "packages/aws-lambda/scripts/runtime-lock/sparticuz/package-lock.json": {
    "changed": true
  },
  "packages/studio/package.json": {
    "version": [
      "0.8.114",
      "0.9.30"
    ],
    "added": [
      "acorn"
    ],
    "removed": [
      "bpm-detective"
    ],
    "changed": {
      "mediabunny": [
        "^1.45.3",
        "^1.65.2"
      ]
    }
  },
  "registry/blocks/godrays/source/package.json": {
    "version": [
      null,
      null
    ],
    "added": [],
    "removed": [],
    "changed": {}
  }
}
```

### Deleted files
- docs/catalog/components/simulated-cursor.mdx
- docs/contracts/2026-10-01-timeline-filmstrip.html
- docs/contracts/2026-10-02-ghost-lane-membership.html
- docs/contracts/2026-10-02-thumbnail-document-lifetime.html
- docs/go-further.mdx
- docs/guides/choose-creation-path.mdx
- docs/guides/color-grading.mdx
- docs/guides/feedback.mdx
- docs/guides/troubleshooting.mdx
- docs/plans/2026-09-26-image-thumbnails.md
- docs/prompting/anatomy.mdx
- docs/prompting/audio-effects.mdx
- docs/prompting/captions-and-talking-heads.mdx
- docs/prompting/code-and-prs.mdx
- docs/prompting/code-blocks.mdx
- docs/prompting/explainers.mdx
- docs/prompting/generated-artwork.mdx
- docs/prompting/iterating.mdx
- docs/prompting/motion-graphics.mdx
- docs/prompting/music-and-slideshows.mdx
- docs/prompting/overlays-and-lower-thirds.mdx
- docs/prompting/product-launch.mdx
- docs/prompting/rendering-and-output.mdx
- docs/prompting/rules-and-anti-patterns.mdx
- docs/prompting/runtimes-and-3d.mdx
- docs/prompting/specification-dial.mdx
- docs/prompting/storyboards.mdx
- docs/prompting/transitions.mdx
- docs/prompting/variables-and-templating.mdx
- docs/prompting/vfx-and-liquid-glass.mdx

### Impact
- CEH skills: none
- Video Factory: video-factory/config/upstream-skills.lock.json, video-factory/contentos/renderers/hyperframes.py, video-factory/package.json: hyperframes 0.8.114, video-factory/research/tool-catalog.yaml
- Local modifications (left untouched): {'/Users/kishore/audit-scratch/t1/hf-src': 0}

### Recent commits
- 2026-11-10 cda84222 fix(core): Safari keeps a small file's preload and leaves a playing clip's source alone (#7498)
- 2026-11-10 b0835262 fix(studio): check Host on the dev server's API routes and honor preview allowed hosts (#7493)
- 2026-11-10 265ec660 ci(publish): build the Lambda handler zip in a read-only job and verify its hash before release (#7495)
- 2026-11-10 983e865a fix(studio-server): thumbnail origin from the server, sandbox previews from other sites (#7492)
- 2026-11-10 5c579997 fix(producer): a render uses the CLI's own GSAP, so the default CDN's file needs no network (#7388)
- 2026-11-10 b28bd2b3 fix(cli): only name a shadowing install whose manager can move it (#7499)
- 2026-11-10 fecde999 perf(core): Safari stops a long video's clips from loading the whole file at once (#7436)
- 2026-11-10 ec30de06 fix(studio): messages that count clips or keyframes say 1 clip, not 1 clips (#7496)
- 2026-11-10 248f56fb fix(studio-server): a claim waits for a changing file's first copy, so its edit stays undoable (#7497)
- 2026-11-10 ad1a5eab chore: release v0.9.30 (#7494)
- 2026-11-10 007664e2 fix(reverse): give agents the sign-in reason to say, and catch stale CLIs that know reverse (#7488)
- 2026-11-10 f9255e39 fix(aws-lambda): the handler ZIP installs its runtime from a committed lockfile with scripts off (#7485)
- 2026-11-10 61e720b0 fix(studio-server): history sweeps stop holding the host's event loop on large projects (#7491)
- 2026-11-10 c6d243a2 fix(gcp-cloud-run): pin the base image and verify chrome-headless-shell and bun by sha256 (#7487)
- 2026-11-10 f318d3d0 fix(studio-server): refuse cross-origin writes and unknown hosts on the preview server (#7490)
- 2026-11-10 b4c7f9cf chore: release v0.9.29 (#7483)
- 2026-11-10 724ab39b fix(studio-server): buildSubCompositionHtml reads only compositions inside the project (#7482)
- 2026-11-10 0ba89412 feat(cli): label GPT image prices as estimates and show the charged credits (#7351)
- 2026-11-10 e8416b2a fix(studio-server): history waits out a file a save has emptied, and rereads one written mid-copy (#7480)
- 2026-11-10 88db8309 fix(producer): refuse a too-slow render only when its typical frame says it cannot finish (#7479)
- 2026-11-10 1a758fd6 test(engine): split the frame extractor tests so each file stays under the flake gate budget (#7476)
- 2026-11-10 b12365d6 docs(studio-app): the Reference read is paid by Pro or a saved HeyGen API key (#7440)
- 2026-11-10 235c80ba fix(engine): a video clip shows a new source frame on every frame it is on screen (#7471)
- 2026-11-09 58686a74 chore: release v0.9.28 (#7475)
- 2026-11-10 756bd6b1 docs(studio-app): cloud exports come with the plan, not only an API key (#7441)
- 2026-11-10 4d0fa2ba fix(engine): short clips from Apple-encoded videos keep their last frame (#7469)
- 2026-11-10 58e9cae7 fix(share): preserve re-invites and validate workspace responses (#7470)
- 2026-11-09 651de1d9 feat(cli): carry the motion blur summary on the @hf-result line (#7468)
- 2026-11-09 e5e79e59 fix(player): unload the video when its src is cleared (#7466)
- 2026-11-09 9e346f9b chore(release): cut v0.9.27 (#7464)
- 2026-11-09 6f909803 perf(parsers): speed up deleting animated groups (#7463)
- 2026-11-09 7bf19ab5 test(engine): nightly motion blur run over generated compositions (#7437)
- 2026-11-09 4b3f70fb fix(cli): Studio renders take the same one-render-slot lock as the CLI (#7459)
- 2026-11-09 48a2b4e0 docs(mcp): current ChatGPT and Claude setup steps, the hosted render's real output, and a first prompt that works (#7439)
- 2026-11-09 4d29a64b test(engine): real-Chrome tests get 30 s per test on slow runners, not 5 s (#7456)
- 2026-11-09 b95ab794 chore(codegen): resync cloud client from EF bc598db7 (#7455)
- 2026-11-09 a4e16d87 fix(cli): templates pull unpacks under .hyperframes, not beside templates/ (#7269)
- 2026-11-09 3ff0b3d8 docs(changelog): weekly digest 2026-11-02-2026-11-09 (#7453)
- 2026-11-09 fc13420d fix(skills): await the player seek in seam-gate (#7454)
- 2026-11-09 0ca2b1ae fix(cli): label SVG contact sheet thumbnails by file name on Windows (#6732)

Adopt only after review: `ceh upstream sync CEH-0014 --approve`. Nothing is merged automatically.
