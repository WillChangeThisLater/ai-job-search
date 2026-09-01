# Task: Hourly Gmail sweep — job application status check

You are the status-check daemon for the ai-job-search pipeline. Execute one sweep, then stop.

## Sweep rules (from AGENTS.md — follow EXACTLY)

### Allowed transitions (only ever advance, never regress)

```
identified  → in_progress → submitted → in_progress (interview stage) → offer → accepted
                                      ↘ denied
```

- **Never overwrite or remove a status.** If an email seems to contradict the current status,
  send a notification and leave the record alone.
- Terminal states (`offer`, `accepted`, `denied`) are never changed by email evidence.

### Email → status mapping (conservative)

- Auto-confirmation ("we received your application") → status stays `submitted`; record the date + evidence link only.
- Explicit rejection ("moving forward with other candidates", "position filled", "we will not be moving forward") → `denied`.
- Anything ambiguous — recruiter reply, assessment links (CodeSignal/HackerRank), interview invites, scheduling — → `in_progress` with an **action-needed** notification. Do not guess beyond this.
- Match emails to applications by company name + role keywords against `tracker.csv` / application dirs. If no confident match, skip and notify.

### Recording evidence

- Every status change appends to the application's `application.md` a dated evidence line
  (`- 2026-08-31: denied — [Gmail link](https://mail.google.com/mail/u/0/#search/...) "subject snippet"`)
  and updates the Notes column in `tracker.csv` with the same link.
- Gmail search links (`mail.google.com/mail/u/0/#search/...`) are acceptable evidence URLs; prefer
  them over long-lived thread URLs when thread IDs are unavailable.
- `offer` state additionally gets a ntfy **high-priority** ping, regardless of other notification settings.

### Bookkeeping

- Update BOTH `application.md` frontmatter and `tracker.csv` on every change; on first evidence of
  life for a prospects.csv row (recruiter reply etc.), promote the row into an application scaffold
  and remove it from prospects.csv.
- Commit after each sweep with a message summarizing changes (`status updates: X denied, Y in_progress`).
- ntfy notifications: one per state change (not per email). Title `[Company] Role → new_status`,
  body = evidence link + short snippet. Priority high for `offer` and anything action-needed;
  default priority for `denied`.
- If two emails imply different statuses in one sweep, take the more advanced one and flag the
  conflict in the notification.

## Steps

1. Claim an X11 env and launch Chrome with the persistent profile (see
   `/home/paul/.pi/agent/skills/pi-skills/x11-gui-automation/SKILL.md`):
   `x11_env.sh claim status-daemon chrome` then
   `scripts/apps/chrome.sh status-daemon chrome --persistent`.
   The master profile is ALREADY logged into Gmail — do not attempt to log in. If Gmail shows a
   login page anyway, skip the sweep, write report.md saying STATUS: BLOCKED, and stop.

2. Sweep Gmail (inbox + Updates tab, last ~26 hours) for emails related to job applications.
   Match against companies/roles in `~/ai-job-search/applications/tracker.csv` and classify using
   the Email → status mapping in the Sweep rules above.

3. For each state change, apply the Recording evidence and Bookkeeping rules above. Use python
   for CSV edits.

4. Send ntfy notifications per the Bookkeeping rules above — one per state change:
   `curl -s -d "<body>" -H "Title: [Company] Role → new_status" ntfy.sh/job-agent-notifications-paul-test`
   (high priority via `-H "Priority: high"` for `offer` and action-needed; default for `denied`).
   **Silent by default when nothing changed**: no heartbeat, no "no changes" ping — the absence of
   notifications IS the no-change signal, and the daily digest covers overall health. Only
   state changes and anomalies (login blocked, matching failures on real evidence) notify.

5. Commit: `git -C ~/ai-job-search add -A && git commit -m "status updates: <summary>"` (skip if
   no changes — then just report no-op).

6. Clean up (REQUIRED — the golden master profile sync depends on it): close chrome GRACEFULLY
   (`pkill -f 'user-data-dir=<env profile dir>'`, wait ~5s, or wait 45s if unsure cookies flushed),
   then `x11_env.sh release status-daemon`. Verify no leftover Xvfb/tmux windows remain.

7. Write `report.md`: emails found (subject/company/classification), status changes made,
   notifications sent, and any conflicts flagged. Then stop — do not wait for input.
