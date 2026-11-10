# Architecture

```
  URL / reference ──► ceh add ──► registry/resources/CEH-NNNN.yaml ◄── ceh migrate ◄── intake/historical/leads.yaml
                         │                 ▲          ▲
             reuse local clone             │          │
             or lab/clones/<id> ──► analyze (static) ─┘          upstream: ls-remote · gh api · fetch into refs/ceh/upstream/*
                         │                                       └─► check · diff · report · sync(--approve, pins, rollback)
                         ▼
                 ceh evaluate ──► reports/<id>/*.md + evaluation.json
                         │
       gates (licence, security) ──► ceh approve ──► ceh integrate ──► integrations/video-factory/catalog.json ──► Video Factory reads
                         │
   library/skills/<name> ──► ceh install ──► symlinks in ~/.claude/skills, ~/.codex/skills, ~/.config/opencode/skills,
                                             ~/.gemini/antigravity/skills, ~/.agents/skills
```

## Modules (`ceh/`)

| Module | Responsibility |
|---|---|
| `store.py` | CEH root, YAML I/O, taxonomy/policy loading, URL normalisation, `Registry` (ids, lookup, dedupe), lifecycle transitions |
| `sources.py` | git and `gh` access, local-clone discovery, lab clones, `Tree` (reads commits without checkout) |
| `analyze.py` | type and capability classification, licence (code vs assets), dependencies, security scan, OSV lookup, compatibility |
| `intake.py` | `add`, `inspect`, alternatives, rule-based recommendation |
| `evaluate.py` | weighted scoring with evidence coverage, gate-driven status, report rendering |
| `upstream.py` | upstream check/diff/report/sync/history/status, weekly digest |
| `integrate.py` | approve, integrate, withdraw, Video Factory catalog and test runner, artifact contract |
| `skills.py` | canonical skills library, validation, per-agent install/uninstall/disable |
| `search.py` | capability search, comparison, brief-driven recommendation |
| `migrate.py` | historical import and migration report |
| `cli.py` | `ceh` command |

## Data, not code

Taxonomy (`registry/capabilities.yaml`), renderers (`registry/renderers.yaml`), agents (`registry/compatibility.yaml`) and
governance (`policies/policy.yaml`: lifecycle, licence classes, gates, weights, schedule, paths) are data. New capabilities,
categories, renderers or agents need a YAML edit only.

## Record shape (abridged)

```yaml
id: CEH-0014
name: heygen-com/hyperframes
url: https://github.com/heygen-com/hyperframes
type: renderer
status: PRODUCTION
capabilities: [rendering, motion-graphics, ...]
local: {paths: [...], state: {<path>: {head, branch, uncommitted_count}}, modified: false}
upstream: {strategy: PINNED, remote, default_branch, pinned_commit, latest_commit, latest_release, forks: [...],
           pins: [{commit, at, by, note}], checks: [...], flags: [...], last_report: {...}}
licence: {spdx, class, gate, source, assets: {...}}
security: {gate, worst, findings: [...]}
compatibility: {agents: [...], renderers: [...]}
evaluation: {criteria: {...}, weighted_score, evidence_coverage, gates, manual: {...}}
historical: {group, previous_decision, evidence: [...]}
video_factory_usage: [...]
history: [{at, from, to, by, note}]
```

## Decisions

See `docs/adr/`. Trade-offs in brief: per-file records over one big YAML (merge-friendly, scales); static-only inspection over
running code (safety first, benchmarks are a separate explicit step); catalog file over editing Video Factory (keeps production
independent); symlink installs over copies (one canonical skill, instant updates, safe uninstall).

## Current consumer implementation status

The v2 contract is documented in integrations/video-factory/catalog-v2.md. `ceh catalog export` creates a separately versioned,
strictly governed consumer view; the current real catalog is empty. The prior diagram expresses the target VF flow, not an
already enabled production integration. The metadata-only consumer exists on isolated VF branch codex/ceh-catalog-consumer,
commit b1befad, and is disabled by default. It requires an independently reviewed catalog digest and explicit compatibility
observations. It never loads skill bodies or executes catalog data. Production pipeline, approvals and renderer defaults are unchanged.
