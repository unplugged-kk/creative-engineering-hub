# AGENTS.md: operating the Creative Engineering Hub

You are working in CEH, the user's permanent registry, R&D lab, skills library and upstream monitor for creative engineering.
Video Factory (`~/git/video-factory`) is a separate production system that consumes only what CEH approves.
Run everything as `uv run ceh <command>` from this directory. Add `--json` for machine-readable output.

## Hard rules

1. **Adding is not integrating.** `ceh add` registers and inspects. Only `ceh approve` then `ceh integrate` reach Video Factory, and both need the user's explicit go-ahead in chat.
2. **Never execute resource code.** Inspection is static. Installing, running scripts, or using credentials needs the user's approval, and happens under `lab/`.
3. **Never edit Video Factory from here.** CEH publishes `integrations/video-factory/catalog.json`; Video Factory reads it.
4. **Never overwrite local work.** Existing clones are reused, never re-cloned. Upstream is fetched into `refs/ceh/upstream/*` only. `ceh upstream sync` moves CEH's pin and nothing else.
5. **Licence and security gates are independent of scores.** Non-commercial licences are never approvable. A `review` gate needs a written note (`--licence-reviewed`, `--security-reviewed`) that reflects what the user actually checked.
6. Unknown facts stay unknown (`null`, "not verified"). Never guess a licence, pin or benchmark.

## What the user says → what you run

| The user says | Do this |
|---|---|
| "Add this repo / skill / tutorial" | `ceh add <url>` (`--type skill` if needed). Report id, type, capabilities, licence, gates, recommendation, alternatives. |
| "Inspect it" / "look again" | `ceh inspect <id>` |
| "Evaluate these" | `ceh evaluate <id>` each; summarise `reports/<id>/recommendation.md`. If they ask for real quality evidence, render a sample in `lab/benchmarks/<id>/` (ask before installing anything), then `ceh evaluate <id> --score visual_quality=N --evidence <path>`. |
| "Compare with our existing motion stack" | `ceh compare --capability motion-graphics <id>` or `ceh compare <id1> <id2>` |
| "Find the best festive video workflow" | `ceh recommend --brief "<their brief>"` (add `--renderer`, `--agent`). Explain gaps honestly. |
| "What do we have for X?" | `ceh search <capability or words>` |
| "Update our Remotion integration" | `ceh upstream check <id>` → `ceh upstream report <id>` → show the report → only after a yes: `ceh upstream sync <id> --approve` |
| "Check everything for updates" | `ceh upstream check --all --report`; summarise `reports/upstream/<date>.md` |
| "Integrate this into Video Factory" | Check overlap (`ceh compare`), gates and tests; ask for approval; then `ceh approve <id>` and `ceh integrate <id> --test` |
| "Find unused or duplicate skills" | `ceh skills list`, `ceh search` per capability, and `reports/historical-migration/REPORT.md` duplicates section; propose consolidation into one canonical skill. |
| "Install that skill for my agents" | `ceh install <skill>` (or `--agent codex`). It never replaces a skill it did not create. |
| "Is everything consistent?" | `ceh validate` and `ceh status` |

## Where things live

- `registry/resources/CEH-NNNN.yaml`: one record per resource (source of truth). Taxonomy: `registry/capabilities.yaml`, renderers, agent compatibility.
- `reports/<id>/`: overview, technical-analysis, capabilities, dependency-analysis, licensing, security, compatibility, benchmark, upstream-analysis, recommendation, evaluation.json.
- `library/skills/<name>/`: canonical skills (SKILL.md + skill.yaml + references/ scripts/ examples/ evals/). One skill per capability, many upstream sources.
- `lab/clones/<id>`: isolated, no-checkout clones (git-ignored). `lab/benchmarks/`, `lab/prototypes/` for experiments.
- `policies/policy.yaml`: lifecycle, licence classes, gates, scoring weights, schedules. Prose in `policies/*.md`, decisions in `docs/adr/`.
- `intake/historical/leads.yaml`: historical evidence; `ceh migrate` re-imports it idempotently.

To add a capability or category, edit `registry/capabilities.yaml`; no code change is needed. Run `uv run pytest -q` after code changes.
