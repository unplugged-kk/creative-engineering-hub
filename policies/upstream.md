# Upstream policy

Strategies: PINNED (exact commit), TRACKED (follow a branch after review), FORKED (user fork carries changes; merge by hand),
VENDORED (copy inside another project; update deliberately). Checks are weekly by default (`ceh upstream check --all --report`),
security advisories daily where supported. A detected change goes check → report (diff, breaking signals, licence and
manifest changes, impacted skills and Video Factory files, optional regression run) → user approval → `sync --approve`.
Nothing is merged or updated automatically. Local work is never overwritten.
