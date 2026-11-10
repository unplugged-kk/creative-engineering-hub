# ADR 0004: Upstream is fetched into refs/ceh/upstream; sync moves a pin only

Status: accepted (2026-11-10)

Existing clones often carry local work. CEH fetches upstream into `refs/ceh/upstream/<branch>`, which never touches
branches, working trees or `origin/*`, so nothing local can be overwritten and no second clone is needed. `ceh upstream sync`
requires `--approve` and a report for that exact commit, appends to the pin history, and supports rollback (`--to`).
Forks and vendored copies are never merged automatically; the report tells the user what to merge.
