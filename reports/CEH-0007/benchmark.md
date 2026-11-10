# CEH-0007 · feitangyuan/onetake

https://github.com/feitangyuan/onetake

| Criterion | Weight | Score | Basis |
|---|---|---|---|
| workflow_completeness | 0.1 | 4 | skills, scripts, examples, tests present: [True, True, True, False] |
| reusability | 0.1 | 4 | resource type agent-skill |
| agent_compatibility | 0.1 | 5 | agents detected: agent-skills-format, claude-code, codex |
| maintainability | 0.1 | 5 | last push 5 days ago |
| documentation | 0.1 | 5 | top-level README 13418 chars |
| licence_suitability | 0.1 | 0 | PolyForm-Noncommercial-1.0.0 (non-commercial) |
| security | 0.05 | 5 | 0 findings, worst low |
| integration_complexity | 0.05 | 5 | 0 runtime dependencies; install hooks: [] |
| visual_quality | 0.2 | — | needs a benchmark: render a sample and record it with --score |
| performance | 0.1 | — | needs a benchmark: render a sample and record it with --score |

Visual quality and performance need a rendered sample. Put outputs under lab/benchmarks/<id>/ and record them with
`ceh evaluate CEH-0007 --score visual_quality=N --evidence lab/benchmarks/CEH-0007/...`.
