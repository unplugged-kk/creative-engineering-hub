# CEH-0026 · morluto/rea

https://github.com/morluto/rea

| Criterion | Weight | Score | Basis |
|---|---|---|---|
| workflow_completeness | 0.1 | 5 | skills, scripts, examples, tests present: [True, True, True, True] |
| reusability | 0.1 | 4 | resource type mcp-server |
| agent_compatibility | 0.1 | 5 | agents detected: agent-skills-format, antigravity, claude-code, claude-code-plugin, codex, generic |
| maintainability | 0.1 | 5 | last push 0 days ago |
| documentation | 0.1 | 5 | top-level README 32982 chars |
| licence_suitability | 0.1 | 5 | MIT (permissive) |
| security | 0.05 | 0 | 38 findings, worst high |
| integration_complexity | 0.05 | 1 | 42 runtime dependencies; install hooks: ['prepare'] |
| visual_quality | 0.2 | — | needs a benchmark: render a sample and record it with --score |
| performance | 0.1 | — | needs a benchmark: render a sample and record it with --score |

Visual quality and performance need a rendered sample. Put outputs under lab/benchmarks/<id>/ and record them with
`ceh evaluate CEH-0026 --score visual_quality=N --evidence lab/benchmarks/CEH-0026/...`.
