# ai-job-status-updates daemon

Daily oversight digest for the ai-job-search pipeline. Reads the other daemons' run logs
(`~/.cache/check-status-daemon/`, `~/.cache/job-discovery-daemon/`), the repo's git history,
and tracker health, then sends one ntfy summary — with loud callouts for anything broken
(daemon BLOCKED, crashed runs, sources drying up, dup-guard failure).

See `PROMPT.md` for the full task spec. Read-only with respect to pipeline data.

## Run

```bash
./run.sh          # one digest (schedule daily, after the other daemons' likely windows)
```
