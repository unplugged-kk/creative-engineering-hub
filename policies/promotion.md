# Promotion policy

1. `ceh add` → DISCOVERED → SANDBOXED (static read).  2. `ceh evaluate` → CANDIDATE, or RESTRICTED on a blocking licence.
3. `ceh approve` (gates + notes) → APPROVED. Requires the user's explicit approval in chat.
4. `ceh integrate [--test]` → PRODUCTION; publishes to `integrations/video-factory/catalog.json`. Separate explicit approval.
5. `ceh withdraw` removes it from the catalog (DEPRECATED by default).
Prefer one canonical capability over many overlapping resources: compare against PRODUCTION alternatives first.
