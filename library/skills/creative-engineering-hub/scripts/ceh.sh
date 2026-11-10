#!/bin/sh
# Run ceh from anywhere.
exec uv run --project "${CEH_HOME:-$HOME/git/creative-engineering-hub}" ceh "$@"
