#!/bin/bash
# run.sh — daily credential-expiry check for the persistent agent profile.
# Purpose: cron-friendly wrapper; sends an ntfy ping to the job notifications
#          topic if the Google/LinkedIn sessions agents rely on have expired.
# Usage:   ./run.sh            (schedule daily; see README.md)
# Deps:    check_profile_sessions.sh (x11-gui-automation skill), browser CLI, curl
# CWD:     this directory
set -uo pipefail
cd "$(dirname "$0")"

NTFY_TOPIC="${CRED_CHECK_NTFY_TOPIC:-job-agent-notifications-paul-test}"
LOG="$HOME/.cache/cred-check-daemon/last-run.log"
mkdir -p "$(dirname "$LOG")"

if ~/.pi/agent/skills/pi-skills/x11-gui-automation/scripts/check_profile_sessions.sh --ntfy "$NTFY_TOPIC" \
    > "$LOG" 2>&1; then
    echo "$(date -Iseconds) all sessions alive" >> "$LOG"
else
    rc=$?
    # exit 1 = expired (ntfy already sent by the check script); 2 = setup error (also worth knowing)
    echo "$(date -Iseconds) check failed rc=$rc (notification path already handled)" >> "$LOG"
fi
