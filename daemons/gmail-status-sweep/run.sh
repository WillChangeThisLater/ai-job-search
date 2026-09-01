#!/bin/bash
# run.sh — kick off one status-check daemon sweep as a headless pi agent.
# Purpose: run PROMPT.md through pi (-p mode) on glm-5.3-flash, isolated session dir.
# Usage: ./run.sh            (one sweep; safe to call from cron)
# Deps: pi, tmux (optional), z-ai/glm-5.3-flash access via OpenRouter.
# CWD: this directory (~/ai-job-search/daemons/gmail-status-sweep/).
set -euo pipefail

# cron has a minimal PATH — add nvm node bin so pi is findable
export PATH="$HOME/.nvm/versions/node/v25.2.1/bin:$PATH"
cd "$(dirname "$0")"

MODEL="z-ai/glm-5.3-flash"
TS=$(date +%Y%m%d-%H%M%S)
RUN_DIR="$HOME/.cache/gmail-status-sweep-daemon/$TS"
mkdir -p "$RUN_DIR"
cp PROMPT.md "$RUN_DIR/PROMPT.md"

# Isolated session dir + fresh cwd so the daemon never resumes a human session.
pi --session-dir "$RUN_DIR/sessions" --model "$MODEL" -p -- \
  "cd $RUN_DIR && Read PROMPT.md and execute the task it describes. Write your summary to report.md. Then stop." \
  > "$RUN_DIR/pi-stdout.log" 2>&1

# Keep the last N sweep dirs for auditing, prune older ones.
ls -1dt "$HOME"/.cache/gmail-status-sweep-daemon/*/ 2>/dev/null | tail -n +31 | xargs -r rm -rf
