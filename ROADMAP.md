# Roadmap

Phases from the mission brief and where they stand.

| Phase | State |
|---|---|
| 1 Historical audit and inventory | Done: `intake/historical/leads.yaml`, `reports/historical-migration/REPORT.md` |
| 2 Architecture and repository | Done: this repo, ADRs 0001-0005 |
| 3 Registry and ingestion | Done: `ceh add`, `inspect`, `migrate` |
| 4 Evaluation and security | Done (static); benchmarks are recorded per resource on request |
| 5 Skills library and adapters | Done: library, validation, symlink adapters for 5 agent locations |
| 6 Upstream intelligence | Done: check/diff/report/sync/history/status, weekly digest |
| 7 Video Factory integration | CEH side done (catalog, gates, test run, artifact contract); VF-side reader pending approval |
| 8 Tests and docs | Done for current scope; extend with each feature |
| 9 Creative Workbench dashboard | Not started (optional) |

Next candidates: VF reader of `catalog.json`; scheduled weekly `ceh upstream check --all --report`; benchmark harness
(render the same brief with each candidate into `lab/benchmarks/` and record scores); curated skills that merge the ADAPT
decisions (motion thresholds from LottieFiles, SFX pass from Barty-Bart, style grammar from cth9191/animate).
