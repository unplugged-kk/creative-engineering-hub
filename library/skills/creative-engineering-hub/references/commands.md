# ceh commands

`add <url> [--type T] [--no-inspect]` · `inspect <id>` · `evaluate <id> [--score k=N --evidence path]` · `search <q> [--all]` ·
`compare <ids..> [--capability c]` · `recommend --brief "…" [--renderer r] [--agent a] [--non-commercial]` ·
`approve <id> [--licence-reviewed note] [--security-reviewed note]` · `integrate <id> [--test]` · `withdraw <id>` ·
`set-status <id> STATE --note …` · `tag <id> caps…` · `install <skill> [--agent a]` ·
`skills list|validate|enable|disable|uninstall [name]` · `validate` · `status` · `migrate` · `artifact <dir>` ·
`upstream check [id|--all] [--report]` · `upstream diff|report|history <id>` · `upstream sync <id> --approve [--to commit]` · `upstream status`

Ids accept `CEH-0001`, a URL, `owner/repo`, or a unique repo name.
