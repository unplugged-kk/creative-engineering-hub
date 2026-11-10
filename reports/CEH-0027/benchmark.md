# CEH-0027 · motiondivision/ai-kit

https://github.com/motiondivision/ai-kit

| Criterion | Weight | Score | Basis |
|---|---|---|---|
| workflow_completeness | 0.1 | 3 | skills, scripts, examples, tests present: [True, True, False, False] |
| reusability | 0.1 | 4 | resource type mcp-server |
| agent_compatibility | 0.1 | 5 | agents detected: agent-skills-format, antigravity, claude-code, codex, opencode |
| maintainability | 0.1 | 5 | last push 6 days ago |
| documentation | 0.1 | 3 | top-level README 2900 chars |
| licence_suitability | 0.1 | 1 | None (unknown) |
| security | 0.05 | 3 | 1 findings, worst medium |
| integration_complexity | 0.05 | 5 | 0 runtime dependencies; install hooks: [] |
| visual_quality | 0.2 | — | needs a benchmark: render a sample and record it with --score |
| performance | 0.1 | — | needs a benchmark: render a sample and record it with --score |

Visual quality and performance need a rendered sample. Put outputs under lab/benchmarks/<id>/ and record them with
`ceh evaluate CEH-0027 --score visual_quality=N --evidence lab/benchmarks/CEH-0027/...`.
