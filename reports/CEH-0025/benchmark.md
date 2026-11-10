# CEH-0025 · Vincentwei1021/anything2explainer

https://github.com/Vincentwei1021/anything2explainer

| Criterion | Weight | Score | Basis |
|---|---|---|---|
| workflow_completeness | 0.1 | 3 | skills, scripts, examples, tests present: [True, False, True, False] |
| reusability | 0.1 | 4 | resource type agent-skill |
| agent_compatibility | 0.1 | 5 | agents detected: agent-skills-format, claude-code, codex |
| maintainability | 0.1 | 5 | last push 1 days ago |
| documentation | 0.1 | 5 | top-level README 17808 chars |
| licence_suitability | 0.1 | 0 | PolyForm-Noncommercial-1.0.0 (non-commercial) |
| security | 0.05 | 3 | 2 findings, worst medium |
| integration_complexity | 0.05 | 5 | 0 runtime dependencies; install hooks: [] |
| visual_quality | 0.2 | — | needs a benchmark: render a sample and record it with --score |
| performance | 0.1 | — | needs a benchmark: render a sample and record it with --score |

Visual quality and performance need a rendered sample. Put outputs under lab/benchmarks/<id>/ and record them with
`ceh evaluate CEH-0025 --score visual_quality=N --evidence lab/benchmarks/CEH-0025/...`.
