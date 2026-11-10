# CEH-0040 · remsky/Kokoro-FastAPI

https://github.com/remsky/Kokoro-FastAPI

| Criterion | Weight | Score | Basis |
|---|---|---|---|
| workflow_completeness | 0.1 | 4 | skills, scripts, examples, tests present: [True, True, True, False] |
| reusability | 0.1 | 3 | resource type repository |
| agent_compatibility | 0.1 | 5 | agents detected: agent-skills-format, claude-code, codex |
| maintainability | 0.1 | 5 | last push 2 days ago |
| documentation | 0.1 | 5 | top-level README 41564 chars |
| licence_suitability | 0.1 | 5 | Apache-2.0 (permissive) |
| security | 0.05 | 3 | 5 findings, worst medium |
| integration_complexity | 0.05 | 2 | 36 runtime dependencies; install hooks: [] |
| visual_quality | 0.2 | — | needs a benchmark: render a sample and record it with --score |
| performance | 0.1 | — | needs a benchmark: render a sample and record it with --score |

Visual quality and performance need a rendered sample. Put outputs under lab/benchmarks/<id>/ and record them with
`ceh evaluate CEH-0040 --score visual_quality=N --evidence lab/benchmarks/CEH-0040/...`.
