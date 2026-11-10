User: "Add https://github.com/acme/kinetic-kit to CEH, inspect it, compare it with our motion-graphics stack and prepare a report."

1. `ceh add https://github.com/acme/kinetic-kit` → CEH-0052, agent-skill, MIT (pass), security pass, capabilities kinetic-typography, motion-graphics.
2. `ceh compare --capability motion-graphics CEH-0052` → shared and unique capabilities against PRODUCTION entries.
3. `ceh evaluate CEH-0052` → `reports/CEH-0052/`. Tell the user the score, its evidence coverage, and that visual quality needs a benchmark.
4. Stop. Do not approve or integrate without an explicit yes.
