# ADR 0005: One canonical skill, symlinked into each agent

Status: accepted (2026-11-10)

All four agents on this machine (Claude Code, Codex, OpenCode, Antigravity) read Agent Skills directories (SKILL.md with
name/description frontmatter); verified 2026-11-10, each directory already holds per-skill symlinks. CEH keeps one
canonical skill in `library/skills/<name>` and links it into each agent's directory. Agent differences (honoured frontmatter
keys, location) are data in `registry/compatibility.yaml` and checked by `ceh skills validate`. CEH never replaces a skill
it did not create. Several upstream repositories may feed one skill through `skill.yaml: sources`.
