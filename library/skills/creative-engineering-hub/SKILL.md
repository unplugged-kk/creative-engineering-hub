---
name: creative-engineering-hub
description: Manage creative technology through the Creative Engineering Hub (CEH) at ~/git/creative-engineering-hub. Use when the user shares a repository, skill, renderer, tutorial or tool URL to add, inspect, evaluate or compare; asks what we have for a creative capability (motion graphics, kinetic typography, explainers, festive videos, voiceover); asks to check creative repos for upstream updates; or asks to integrate something into Video Factory.
---

# Creative Engineering Hub

CEH is the user's registry, lab, skills library and upstream monitor for creative engineering. Video Factory consumes only
what CEH approves. Work from `~/git/creative-engineering-hub` and run `uv run ceh <command>` (add `--json` to parse).

## Rules

- Adding is not integrating. `approve` and `integrate` need the user's explicit yes in chat, each time.
- Never run, install or build a resource's code during intake. Never edit Video Factory from CEH.
- Never overwrite local work; CEH reuses existing clones and fetches upstream into `refs/ceh/upstream/*` only.
- Non-commercial licences are never approvable. Review notes must describe what the user actually checked.

## Requests

| User asks | Run |
|---|---|
| add / register this URL | `ceh add <url>` then report id, type, capabilities, licence and security gates, recommendation, alternatives |
| evaluate / review it | `ceh evaluate <id>`; summarise `reports/<id>/recommendation.md` and gaps in evidence |
| compare with what we have | `ceh compare <id> <other>` or `ceh compare --capability <cap> <id>` |
| best tool for a brief | `ceh recommend --brief "<brief>"` |
| what do we have for X | `ceh search <x>` |
| check for updates | `ceh upstream check --all --report`, then `ceh upstream report <id>` for anything flagged |
| adopt an update | show the report; after a yes: `ceh upstream sync <id> --approve` |
| put it into Video Factory | `ceh compare`, then after a yes: `ceh approve <id>` and `ceh integrate <id> --test` |
| install a skill for my agents | `ceh install <skill>` |

Details: `references/commands.md`. Full playbook: `~/git/creative-engineering-hub/AGENTS.md`.
