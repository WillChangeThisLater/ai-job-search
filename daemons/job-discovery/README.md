# job-discovery daemon

Daily daemon that appends 5+ new quality job prospects to `applications/prospects.csv`.
See `PROMPT.md` for the full task spec and `../gmail-status-sweep/` for the sibling daemon.

## Run

```bash
./run.sh          # one discovery run (safe for cron; schedule once daily)
```

- Model: `z-ai/glm-5.3-flash` via pi `-p` mode, isolated session dir under
  `~/.cache/job-discovery-daemon/<ts>/` (reports + logs kept there, last 30 runs pruned).
- Rotation state (which source/query combos were used recently): `~/.cache/job-discovery-daemon/state.json`.
- The daemon is expected to edit `applications/JOB_SOURCES.md` when it discovers new sources —
  that file is the shared playbook and the daemon is its primary maintainer.
