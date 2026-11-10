# ADR 0001: One YAML file per resource

Status: accepted (2026-11-10)

The mission suggested `registry/resources.yaml`. With hundreds of resources and several agents writing at once, one file
produces merge conflicts and huge diffs. CEH stores `registry/resources/CEH-NNNN.yaml` instead. The id is the filename,
so lookups are O(1) and a record's git history is its own. Aggregate views (`ceh status`, `ceh search`, reports) are computed.
