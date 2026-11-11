# Final agent interoperability assessment

Package date: 2026-11-11. The bounded command evidence was collected on 2026-11-10 UTC. This report does not upgrade
installation or planning-only evidence into successful runtime invocation.

## Fresh local checks

| Environment | Measured version | Exposed | Discovered by model | Invoked | Correct output | Independently verified |
|---|---|---|---|---|---|---|
| Codex CLI | 0.167.0 | Candidate copied only to disposable project .agents/skills | Unverified | CLI task attempt launched | No model result; network blocked; stopped after 20s | No |
| Claude Code CLI | 2.1.316 | Candidate copied only to disposable project .claude/skills | Unverified | CLI task attempt launched | Not logged in; zero API ms/tokens/cost reported | No |
| OpenCode CLI | 2.2.7 | Candidate copied only to disposable project .opencode/skills; explicit file path in task | Unverified | Private standalone-server task attempted | Transport blocked; stopped after 20s | No |
| Antigravity | Not found in PATH | Existing global CEH operating-skill link is historical exposure evidence only | Unverified | Not attempted | None | No |
| Current Codex app agents | Runtime/model version not exposed by tools | Canonical file directly read in prior controlled task | Direct read known, automatic discovery unverified | Prior bounded planning and fixture authoring | Plan/artifact evidence exists | Planning and sampled technical/visual evidence only; not proof of CLI interchangeability |

The standalone generic adapter is a location convention, not an executable agent. No global creative skill was installed,
no authentication performed, no account configuration changed and no paid provider call permitted by the sandbox.

## Exact task and controls

The task asked for a six-second 1080x1920/30fps HyperFrames plan preserving `Revenue target 20%`, one emphasis, a reading
hold, brand/font blockers and no production or quality claims. Prompt and exact argv are preserved in the evidence.

All CLI tests ran under sandbox-exec, clean HOME/XDG/CODEX_HOME/CLAUDE_CONFIG_DIR and no inherited credentials. User/private
filesystem reads and writes outside the test directory were denied; system Keychain service lookup was denied. External
network access was denied. Loopback only was added for OpenCode's private server, without enabling external model access.
No existing daemon session, user auth store or global candidate installation was used. Timeout cleanup terminated the task
process groups. Initial setup failures were retained and not confused with agent incompatibility.

The final Claude attempt set CLAUDE_CODE_TMPDIR inside the task directory; otherwise its hardcoded /tmp/claude-501 path
was correctly denied. The initial /tmp versus /private/tmp sandbox-path alias issue was corrected for task-owned writes.
No permission was granted to the real user's Claude temporary directory.

## Evidence

Durable raw logs, versions, prompt, environment and sandbox policies:
`/Users/kishore/Desktop/VideoFactory-Workspace/reports/ceh-acceptance/2026-11-11/agent-cli-review-68e7c83f`.

Exact invocations appear in codex-invocation.json, claude-invocation-final.json and opencode-invocation-final.json.
Version commands used `--version`; help was inspected before choosing bounded, noninteractive flags. Codex used exec,
--ignore-user-config, --ephemeral, --skip-git-repo-check, --sandbox read-only and JSON output. Claude used -p,
--no-session-persistence, project-only settings, plan permissions, Read-only tools and JSON output. OpenCode used
--standalone run --format json. These are recorded command attempts, not successful skill executions.

## Acceptance consequence

Actual CLI interoperability remains **BLOCKED/UNVERIFIED**, not PASS. This does not prove the skill incompatible: the safety
boundary deliberately withholds the model connection/authentication needed for execution. First publication must not claim
verified unattended agent support; the proposed entry lists no named agent allow-list. Any subsequent account-backed test
requires an explicitly approved, no-new-spend execution route. Do not request keys or weaken isolation to make the test pass.
