# CEH-0038 · CopilotKit/CopilotKit

https://github.com/CopilotKit/CopilotKit

| Criterion | Weight | Score | Basis |
|---|---|---|---|
| workflow_completeness | 0.1 | 4 | skills, scripts, examples, tests present: [True, True, True, False] |
| reusability | 0.1 | 4 | resource type agent-skill |
| agent_compatibility | 0.1 | 5 | agents detected: agent-skills-format, antigravity, claude-code, claude-code-plugin, codex |
| maintainability | 0.1 | 5 | last push 0 days ago |
| documentation | 0.1 | 5 | top-level README 21968 chars |
| licence_suitability | 0.1 | 5 | MIT (permissive) |
| security | 0.05 | 3 | 79 findings, worst medium |
| integration_complexity | 0.05 | 4 | 0 runtime dependencies; install hooks: ['prepare'] |
| visual_quality | 0.2 | — | needs a benchmark: render a sample and record it with --score |
| performance | 0.1 | — | needs a benchmark: render a sample and record it with --score |

Visual quality and performance need a rendered sample. Put outputs under lab/benchmarks/<id>/ and record them with
`ceh evaluate CEH-0038 --score visual_quality=N --evidence lab/benchmarks/CEH-0038/...`.
