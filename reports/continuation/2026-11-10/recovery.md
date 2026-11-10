# Recovery and rollback

Original VF checkout: /Users/kishore/git/video-factory. Its user-owned tracked diff and untracked filenames were captured
before work and compared afterward. Do not reset, clean, stash, cherry-pick onto main, or remove user files.
Consumer worktree: /tmp/ceh-vf-consumer, branch codex/ceh-catalog-consumer. It starts at VF commit
36bb5581527fab6e2b39f52b88032e78ad64355e. No branch merge or activation is authorized.

The new reader is never called by the production pipeline. Omit --enable to leave it disabled. Rollback of a future enabled
standalone call is to remove that opt-in and return to existing routing. To recover a previous reviewed catalog, restore its
versioned file and independently reviewed fingerprint together. Do not calculate trust from an untrusted catalog at runtime.

CEH v2 export is separate from legacy publication. `uv run ceh catalog export --json` does not approve resources or ratify
historical records. The real v2 catalog is empty. Approval binds skill version, bundle digest and exact release entry digest;
changing content or compatibility metadata requires a fresh review. Production pins remain unchanged.

Fixture outputs live in /tmp/ceh-benchmark and /tmp/ceh-benchmark-repro and can be lost on reboot. Reproduce with
 tools/benchmarks/kinetic_type/README.md into a new external directory. Never put media in either repository or delete
existing outputs to make a command succeed. The harness has no unsandboxed fallback and preserves failing logs.
Source code and commands are committed; ephemeral media availability is not guaranteed. Copy evidence to an approved durable
external workspace before relying on it for a production release. There is no installed production dependency to uninstall.

The isolated full regression run temporarily reused the original pre-existing node_modules through a task-created symlink.
No packages were installed or changed. That task-owned link was removed after verification, leaving the consumer branch clean.
To reproduce the same dependency environment, create that local symlink again before full VF tests, or provide a separately
reviewed identical dependency tree. Never remove actual source dependencies. The metadata-only reader itself needs no node_modules.
