# CEH-0044 · FFmpeg/FFmpeg

https://github.com/FFmpeg/FFmpeg

| Criterion | Weight | Score | Basis |
|---|---|---|---|
| workflow_completeness | 0.1 | 2 | skills, scripts, examples, tests present: [False, False, False, True] |
| reusability | 0.1 | 3 | resource type repository |
| agent_compatibility | 0.1 | 0 | agents detected: none |
| maintainability | 0.1 | 5 | last push 0 days ago |
| documentation | 0.1 | 3 | top-level README 2026 chars |
| licence_suitability | 0.1 | 2 | LGPL-3.0 (copyleft) |
| security | 0.05 | 5 | 0 findings, worst low |
| integration_complexity | 0.05 | 5 | 0 runtime dependencies; install hooks: [] |
| visual_quality | 0.2 | — | needs a benchmark: render a sample and record it with --score |
| performance | 0.1 | — | needs a benchmark: render a sample and record it with --score |

Visual quality and performance need a rendered sample. Put outputs under lab/benchmarks/<id>/ and record them with
`ceh evaluate CEH-0044 --score visual_quality=N --evidence lab/benchmarks/CEH-0044/...`.
