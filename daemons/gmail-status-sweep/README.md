# gmail-status-sweep daemon

Hourly agent that sweeps Gmail for job-application status emails and advances
`applications/tracker.csv` (never regresses) per the rules in `AGENTS.md`
("Inbound status updates — Gmail sweep daemon"). Sends one ntfy notification
per state change; commits after every sweep.

## Run

```bash
./run.sh          # one sweep, foreground-ish (logs to sweep-<ts>.log)
```

Schedule hourly via cron:

```
0 * * * * /home/paul/ai-job-search/daemons/gmail-status-sweep/run.sh
```

Model: `z-ai/glm-5.3-flash` via OpenRouter (~$0.005/sweep, ~$0.80/week measured 2026-08-31).
