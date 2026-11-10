# Creative Engineering Hub (CEH)

The user's permanent system for discovering, evaluating, governing and tracking creative technology: repositories,
agent skills, renderers, MCP servers, packages, tutorials, models and techniques. CEH is the source of truth;
Video Factory is one consumer and only ever sees approved capabilities.

```bash
uv sync
uv run ceh add https://github.com/owner/repo        # register, inspect statically, score, report
uv run ceh search kinetic-typography
uv run ceh recommend --brief "Create a cinematic Diwali greeting video"
uv run ceh upstream check --all --report             # weekly upstream digest
uv run ceh status
```

## Lifecycle

`DISCOVERED → INSPECTING → SANDBOXED → TESTING → CANDIDATE → APPROVED → PRODUCTION`, plus `PARKED`, `REJECTED`,
`RESTRICTED`, `DEPRECATED`. `APPROVED` is set only by `ceh approve` (licence + security gates) and `PRODUCTION` only by
`ceh integrate` (publishes to `integrations/video-factory/catalog.json`).

## Commands

| Command | Purpose |
|---|---|
| `ceh add <url> [--type T] [--no-inspect]` | Normalise, dedupe, assign `CEH-NNNN`, reuse a local clone or make a no-checkout lab clone, classify, licence, deps, security, compatibility, alternatives, recommendation, reports |
| `ceh inspect <id>` / `ceh evaluate <id> [--score k=v --evidence p]` | Re-read; score with gates; write `reports/<id>/` |
| `ceh search <q>` / `ceh compare <a> <b> \| --capability c` / `ceh recommend --brief "…"` | Capability discovery and selection |
| `ceh approve <id>` / `ceh integrate <id> [--test]` / `ceh withdraw <id>` | Governance and the Video Factory catalog |
| `ceh set-status <id> PARKED --note …` / `ceh tag <id> caps…` | Curation |
| `ceh install <skill> [--agent a]` / `ceh skills list\|validate\|enable\|disable\|uninstall` | Universal skills library |
| `ceh upstream check [id\|--all] [--report]` / `diff` / `report [--run-tests]` / `sync --approve [--to pin]` / `history` / `status` | Upstream intelligence |
| `ceh migrate` / `ceh validate` / `ceh status` / `ceh artifact <dir>` | Migration, integrity, overview, artifact contract |

See [AGENTS.md](AGENTS.md) for natural-language operation, [ARCHITECTURE.md](ARCHITECTURE.md) for design,
[ROADMAP.md](ROADMAP.md) for what is next, and `reports/historical-migration/REPORT.md` for the recovered inventory.
