# AGENTS.md — Repo layout for agents

This repository is an agent-run job search pipeline. Humans and AI agents
collaborate here: agents discover postings, generate tailored resumes, submit
applications via browser automation, and track status. See `README.md` for the
full pipeline description.

## Directory layout

- `README.md` — what this repo is, how the pipeline works
- `RESUME.md` — master resume evidence bank / scratchpad (source of truth for experience, impact, metrics, skills). Agents distill this into tailored resumes.
- `braindump.md` — **local-only, gitignored.** Broader narrative + application defaults.
  - **If `braindump.md` does not exist, create it.** It is a general knowledge bank you can pull from for constructing tailored resumes — personal narrative, preferences, and context that are intentionally not checked in. Populate it as needed.
- `job_field_profiles.md` — recurring requirements by field and keyword mapping
- `resumes/<field>/resume.md` — the tailored resume for a given `<field>` (e.g. `insurtech`, `ml-platform`, `agentic-platform`). `<field>` is the canonical grouping key.
- `applications/tracker.csv` — master application tracker CSV (one row per company/role, with status, salary range, match assessment, key skills/gaps)
- `applications/<application>/application.md` — one directory per job application. Each `application.md` has YAML frontmatter (`company`, `role`, `field`, `status`, `posting_url`, `resume_used`, ...) plus the job description, links, and resume strategy.
- `scripts/` — tooling: `cdp.py` (Chrome DevTools Protocol browser automation), `md2pdf.sh` + `resume.css` (resume markdown → PDF rendering)

## Conventions

- Adding a new `<field>`: create `resumes/<new-field>/` and author a genuinely tailored resume (not a copy of another field's), then link it from the application's `application.md` via `../../resumes/<field>/resume.md`.
- Application status lives in each `application.md` frontmatter `status:`: `identified` | `in_progress` | `submitted` | `offer` | `accepted` | `denied`, mirrored in `applications/tracker.csv`. Terminal states: `offer`, `accepted`, `denied`.
- Do not commit `braindump.md` or its contents; it is deliberately excluded from version control.

## Writing voice — open-ended prose must sound like Paul
- Any open-ended writing that a recruiter/human will read as Paul (cover-letter-style notes, recruiter emails, LinkedIn messages, "anything you'd like us to know" answers, interview follow-ups) must be written **as if Paul wrote it himself** — with the knowledge that he's applying for a job and wants to put his best foot forward.
- Read the [`write-like-me` skill](file:///home/paul/.pi/agent/skills/pi-skills/write-like-me/SKILL.md) and skim the relevant samples in `samples/` before drafting. Canonical copy also symlinked at `writing-style/write-like-me.md`.
- Best-foot-forward caveat: this is polished-Paul. Fix his phonetic spellings and typos, drop the lowercase-first habit in recruiter-facing email — but keep the substance of his voice: direct and concrete, homely analogies, honest hedging, no corporate filler, no fake enthusiasm, numbered points for multi-part asks.
- Resume bullets and CSV fields are excluded (those follow their own formats); this rule is for prose.
- Anything longer than a sentence that will be *sent* gets shown to the human for approval first (consistent with the submit gate below).

## Application workflow (hard rules)

These rules were crystallized from real runs. Follow them exactly.

### 1. Resume review gate — BEFORE any form filling
- Draft the tailored resume (`resumes/<field>/resume.md`) and render the PDF.
- **Stop. Present the resume content to the human for review and approval BEFORE opening the application form or filling any fields.** No exceptions.
- If the human requests changes, apply them, re-render, and re-confirm before proceeding.

### 2. Resume cosmetics (non-negotiable)
- **One page.** Always. Verify by counting pages in the rendered PDF (`pdftotext`, count `\f`). If it overflows, cut content or trim bullets — never shrink below ~8.4pt or drop margins below 0.2in.
- **Links must be attached to phrases, never shown as literal URLs.** Write `[Extended the pi agent harness](https://github.com/...)`, not `Extended the pi agent harness (github.com/...)`. Header links use labels (`LinkedIn`, `GitHub`), not URLs.
- **Links must be verified visually** (screenshot the rendered resume) — text extraction alone has missed literal URLs before.
- **No internal jargon** in resumes. Codenames like "the Friday service" mean nothing to a hiring manager — describe it ("the video-ingestion service").
- First person where a sentence needs a pronoun ("I configured..."), never third person ("he/she").

### 3. PDF rendering pipeline
- Use: `pandoc resume.md -f gfm -t html5 -s --metadata title=" " -H scripts/resume-style.html -o out.html` then `Page.printToPDF` via `scripts/cdp.py` (WebSocket CDP, `preferCSSPageSize`, letter size).
- Gotchas learned the hard way:
  - pandoc's standalone template injects default CSS (50px body padding, base font) that overrides linked stylesheets — embed styles via `-H` (inline `<style>`), and make sure the style file **ends with `</style>`** (an unterminated tag swallows the whole document).
  - headless-chrome `--print-to-pdf` silently cached CSS in one session; the CDP print path is deterministic. Prefer it.
  - `#resume`-style file inputs: upload via `DOM.setFileInputFiles` (browser CLI `type` on file inputs fails silently).
  - After printing, verify: page count = 1, all sections present, no literal URLs, then screenshot visually.

### 4. Form filling discipline
- Observe → act → screenshot-verify every step. Never assume a field took a value.
- React-select dropdowns (Greenhouse, Ashby, Kula): synthetic JS events often fail — use real `Input.dispatchMouseEvent`/`dispatchKeyEvent`, or locate rendered option nodes (`[id*=-option]`) and click them.
- File upload fields: `DOM.setFileInputFiles`, then verify the chip/filename appears in the page text.
- NEVER click Submit/Apply. Fill everything, then present a full summary of every field + written answers to the human and wait for explicit approval. The human may submit personally.
- Site-specific form-fighting knowledge (LinkedIn React forms, ProseMirror fields, hidden checkboxes) lives in `applications/FORM_PLAYBOOK.md` — read it before filling forms on a site listed there. Prefer `browser click "text:..."` / `--verify` over `eval el.click()`; see the `browser` skill.

### 5. Tracker + records
- On submission (by agent or human): update `application.md` frontmatter `status: submitted`, tick progress checklist, and update `applications/tracker.csv` (Status, Date Applied).
- Commit and push after each meaningful state change.

### 6. Browser hygiene
- Keep open tabs minimal: close research/testing/application tabs when done. One tab per active application.
- When a dropdown menu, iframe, or captcha blocks automation, fall back to CDP → xdotool (X11) in that order — and tell the human if it needs eyes.

### 7. Duplicate guard — run BEFORE scaffolding any application
- `python3 scripts/check_dup.py --company "<Company>" --role "<Role Title>"` (optionally `--url`).
  Exit 1 (duplicate) = hard stop, never re-apply. **Only one OPEN application per company at a
  time** — if the company already has an application in `identified`/`in_progress`/`submitted`, a
  second role there is blocked until the first reaches a terminal state (`accepted`/`denied`). Exit 2 (same company, different role) =
  show the human the existing rows and let them decide. Only exit 0 proceeds.
- Status gates: only rows with `Status: Not Applied` in prospects.csv may be scaffolded; anything
  already in tracker.csv has been actioned.
- tracker.csv is for **applied/actioned** roles only; discovered roles live in prospects.csv until
  the human picks them up.

### 8. Role-fit vetting — before applying
- Before scaffolding an application, honestly assess the gap between the JD's core requirements and Paul's actual experience (see `RESUME.md` evidence bank).
- Rules of thumb:
  - Title stretch (e.g. Senior → Staff) is fine when the *work* matches the evidence.
  - Do NOT apply to roles whose day-1 skills Paul lacks — e.g. hands-on model training/fine-tuning, deep framework-specific ML (PyTorch/TF internals), or a primary language he doesn't know. "Ran the platform ML engineers used" ≠ "built the models."
  - Flag the fit assessment in the application's `application.md` (a "Fit / keywords" section) including known gaps, so the human can veto before any effort is spent.
- When in doubt, surface the gap and let the human decide — applications are cheap, brutal interviews are not.
- Check the posting's application close date BEFORE drafting anything (July-HN-thread postings frequently expire 07-31). If closed, stop and record in tracker as a missed lead rather than investing resume effort.
- Resume versioning: `resumes/<field>/resume.md` is the living draft. When the human approves it for a submission, snapshot it to `resume_v1.md` (then `_v2`, ...) and render the matching `resume_vN.pdf`. The application's `application.md` frontmatter (`resume_used:`) must point at the **versioned file**, not the living draft, so every application records exactly which resume was submitted.
- Interview prep: every `application.md` gets an "Interview prep notes" section listing the skills Paul should brush up on for that company's interview loop (based on the fit/gap assessment), plus the strong areas to lean on. Create it at scaffold time, not post-submit.

## Inbound status updates — Gmail sweep daemon

A companion daemon (see `daemons/gmail-status-sweep/` — its PROMPT.md holds the detailed sweep
rules) runs hourly: it reads job-application email in Gmail, classifies it, and updates
application statuses in this repo. Summary of what it does:

- **Advances statuses only**, per this state machine (never regress; terminal states immutable):

  ```
  identified  → in_progress → submitted → in_progress (interview stage) → offer → accepted
                                        ↘ denied
  ```

- Maps emails conservatively: auto-confirmations only record evidence; explicit rejections →
  `denied`; anything ambiguous (recruiter reply, assessment, interview invite) → `in_progress`
  with an action-needed notification. Ambiguity is escalated to the human, never guessed.
- Records evidence for every change: a dated Gmail-link line in the application's
  `application.md` and the same link in `tracker.csv` Notes.
- Keeps `application.md` frontmatter and `tracker.csv` in sync on every change, promotes
  prospects.csv rows that show first signs of life, and commits after each sweep
  (git history = status audit trail).
- Sends ntfy notifications per state change; `offer` and action-needed items ping high-priority.

## Job discovery daemon (daily)

A sibling daemon (`daemons/job-discovery/`) runs once a day: it sweeps known job sources
(see `applications/JOB_SOURCES.md`) and appends at least 5 new quality prospects to
`prospects.csv` (AI/agentic, ML-ops/data, or tight-fit senior SWE; honest match ratings;
no duplicates — enforced via `scripts/check_dup.py`). When known sources run dry, its job
is to *find and test new sources*, recording the results back into JOB_SOURCES.md so the
playbook keeps improving.
