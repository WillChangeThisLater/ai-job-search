# cred-check daemon

Alerts Paul via ntfy when the **persistent agent chrome profile's** logins
(Gmail, LinkedIn) have expired, BEFORE a job-search agent hits a login wall
mid-application.

## How it works

- `run.sh` calls the x11-gui-automation skill's `check_profile_sessions.sh`
  (no LLM — it drives a throwaway chrome via CDP against the golden master
  profile and checks for login redirects on mail.google.com and
  linkedin.com/feed).
- Any expired session → ntfy **high-priority** ping to
  `job-agent-notifications-paul-test` with refresh instructions.
- Fully self-cleaning: claims/releases its own x11 env via the standard
  lifecycle, so it never collides with running agents (the lock handles it).

## Schedule

Daily via cron (see `crontab -l`):

```
0 8 * * * ~/ai-job-search/daemons/cred-check/run.sh
```

## Manual run

```bash
~/ai-job-search/daemons/cred-check/run.sh
cat ~/.cache/cred-check-daemon/last-run.log
```

## Refreshing expired sessions

Fastest: `vncviewer localhost:<port>` inside any env running the persistent
chrome, log in, done (sync-back persists it). Or re-run the full bootstrap
(`chrome_bootstrap.sh`) per the x11-gui-automation skill.
