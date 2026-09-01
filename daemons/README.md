# daemons/

Cron-scheduled agent daemons: small headless `pi` runs (one prompt, one job,
stop) that keep the job-search pipeline moving between interactive sessions.

Each daemon is a directory with:

- `PROMPT.md` — the full, self-contained task prompt the agent executes on
  each fire. Daemons are stateless: everything needed to do the job (rules,
  state machines, escalation ladders) is in the prompt, not in a session.
- `run.sh` — the cron entrypoint. Launches `pi` headless with the prompt,
  isolates logs, and handles environment quirks (e.g. cron's minimal `PATH`
  needs the nvm node bin exported explicitly).

| Daemon | Cadence | Job |
|---|---|---|
| `gmail-status-sweep/` | Hourly | Reads job-application email in Gmail, classifies it, and advances application statuses per a conservative state machine (advance-only, evidence-linked, ambiguity escalated to the human — never guessed). |
| `job-discovery/` | Daily | Sweeps known job sources for new quality postings and appends them to the local prospects data; when known sources run dry, it hunts for and documents new sources. |
| `ai-job-status-updates/` | Daily | Digest of daemon logs plus git/CSV changes, pushed via ntfy — anomaly-first, silent when nothing changed. |
| `cred-check/` | Daily | Checks that browser session credentials the pipeline depends on are still live; alerts via ntfy on expiry. |

## Operations

- Cron entries call each `run.sh` directly (see the daemon's README for its
  schedule); logs go to a per-daemon cache directory.
- Status changes made by the Gmail sweeper are committed to git, so the repo
  history doubles as the status audit trail.
