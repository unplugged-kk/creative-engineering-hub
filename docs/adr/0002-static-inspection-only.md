# ADR 0002: Inspection is static; execution is a separate, approved step

Status: accepted (2026-11-10)

`ceh add`/`inspect` never install or run resource code. Lab clones use `--no-checkout --depth 1 --filter=blob:limit=1m` and
files are read from git objects, so even checkout-time side effects and large binaries are avoided. Visual quality and
performance therefore start as "no evidence" and are filled by an explicit benchmark (`ceh evaluate --score ... --evidence ...`)
that the user approves. Trade-off: first scores are partial (coverage is always reported), in exchange for zero
execution risk on intake.
