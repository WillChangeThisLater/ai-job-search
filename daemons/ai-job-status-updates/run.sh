#!/bin/bash
# run.sh — daily pipeline digest: daemon logs + git/CSV changes -> one ntfy message.
# Purpose: oversight daemon; read-only over pipeline data, alerts on anomalies.
# Usage: ./run.sh            (one digest; schedule once daily)
# Deps: pi, git, z-ai/glm-5.3-flash access via OpenRouter.
# CWD: this directory (~/ai-job-search/daemons/ai-job-status-updates/).
set -euo pipefail

# cron has a minimal PATH — add nvm node bin so pi is findable
export PATH="$HOME/.nvm/versions/node/v25.2.1/bin:$PATH"
cd "$(dirname "$0")"

MODEL="z-ai/glm-5.3-flash"
TS=$(date +%Y%m%d-%H%M%S)
RUN_DIR="$HOME/.cache/ai-job-status-updates/$TS"
mkdir -p "$RUN_DIR"
cp PROMPT.md "$RUN_DIR/PROMPT.md"

PIPELINE_DIGEST_NTFY_TOPIC="${PIPELINE_DIGEST_NTFY_TOPIC:-job-pipeline-digest-paul}" \
pi --session-dir "$RUN_DIR/sessions" --model "$MODEL" -p -- \
  "cd $RUN_DIR && Read PROMPT.md and execute the task it describes. Write your full findings to report.md and send the ntfy digest as instructed. Then stop." \
  > "$RUN_DIR/pi-stdout.log" 2>&1

# Keep the last 30 run dirs for auditing, prune older ones.
ls -1dt "$HOME"/.cache/ai-job-status-updates/*/ 2>/dev/null | tail -n +31 | xargs -r rm -rf
