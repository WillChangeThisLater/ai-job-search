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

## Agent tooling

The daemons (and the interactive application agents) are built on agent
skills — reusable, documented interaction patterns the agent loads before
touching a given tool:

- **browser skill** — agent-optimized automation of a real Chrome via the
  Chrome DevTools Protocol: navigate, click, type, screenshot-verify, with
  CDP port-selection rules so agents never attach to each other's browsers.
  Part of the [`pi` coding-agent](https://github.com/badlogic/pi-mono) skill
  library ([skills docs](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/skills.md)).
- **x11-gui-automation skill** — agent-authored (lives in the agent's local
  skills directory, not this repo): isolated Xvfb displays per app with VNC
  observation, an allocation registry (`x11_env.sh`) so concurrent agents
  never fight over displays or ports, and an escalation ladder
  (CDP/DOM → xdotool → ask the human).
- **tmux skill** — how agents communicate with tmux panes; the mechanism
  behind launching and monitoring subagents in separate panes
  ([docs](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/tmux.md)).

## Operations

- Cron entries call each `run.sh` directly (see the daemon's README for its
  schedule); logs go to a per-daemon cache directory.
- Status changes made by the Gmail sweeper are committed to git, so the repo
  history doubles as the status audit trail.
