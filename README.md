# ai-job-search

A **job application harness**: an AI coding agent that does all the tedious
parts of a job search and stops at the submit button.

Built on the [`pi` agent harness](https://github.com/badlogic/pi-mono) with
LLM subagents, it discovers relevant postings, distills an evidence bank into
tailored one-page resumes, fills out application forms on real job portals via
browser automation, and tracks status — while a human reviews everything and
makes the final call. The submit button is human-only; the harness exists to
make that last step take five minutes instead of an hour.

## The pipeline

```
discover → tailor → prepare → [ human reviews & submits ] → track
```

### 1. Posting discovery
- **HN Algolia** ("Who is Hiring?" threads) plus job boards (Indeed, Work at a
  Startup, Ashby/Greenhouse boards) are scraped and filtered against the
  candidate's field profiles (`job_field_profiles.md`) — recurring requirements,
  keyword mappings, and salary/location constraints.
- Candidate postings are checked for duplicates and close dates before any
  effort is spent, then staged locally with a match score, key skills
  required, and identified gaps.

### 2. Evidence-bank-driven resume tailoring
- `RESUME.md` is the master **evidence bank**: raw experience, impact metrics,
  projects, certifications, and context.
- For each role, the agent distills the evidence bank into a genuinely
  tailored resume under `resumes/<field>/resume.md` — reordering, reweighting,
  and rewording bullets to target the field (`insurtech`, `ml-platform`,
  `agentic-platform`, ...).
- `braindump.md` (a gitignored local knowledge bank) supplies personal
  narrative and preferences the agent can draw from.

### 3. Application preparation
- The agent drafts the tailored resume, renders it to a one-page PDF
  (pandoc + headless Chrome via [`scripts/cdp.py`](scripts/cdp.py)), and
  verifies it — page count, links attached to phrases, visual screenshot check.
- It then fills the application form through **browser automation over the
  Chrome DevTools Protocol (CDP)** — every step observed → acted on →
  screenshot-verified. File uploads, React-select dropdowns, Ashby/Greenhouse
  quirks: the harness has playbooks for the fiddly parts.
- **Then it stops** and hands the human a full field-by-field summary —
  written answers verbatim, exact resume PDF — for review and submit.

### 4. Tracking (human-approved events only)
- After the human submits, the harness records the application locally:
  status, date, the exact resume version used, and evidence links.
- A **companion daemon** (separate repo) sweeps Gmail hourly to pick up
  application status updates — confirmations, rejections, interview invites —
  and advances statuses automatically, with Gmail evidence links and ntfy
  notifications. The rules it must follow (status state machine, conservative
  evidence-based mapping) are codified in [AGENTS.md](AGENTS.md), section
  "Inbound status updates".
- A second daemon (`daemons/job-discovery/`) runs daily, appending new
  quality prospects from the sources documented in the local job-sources
  playbook — and when those run dry, it hunts down and documents new sources
  itself.

## Repo layout

| Path | Purpose |
|---|---|
| `AGENTS.md` | The agent's operating contract: hard rules, submit gate, fit vetting, form-filling discipline |
| `RESUME.md` | Master resume evidence bank |
| `job_field_profiles.md` | Requirements/keywords per field |
| `resumes/<field>/` | Tailored resume per field |
| `daemons/` | Job-discovery, Gmail status-sweep, and credential-check daemons |
| `scripts/cdp.py` | CDP browser automation |
| `scripts/md2pdf.sh` + `resume.css` | Resume markdown → PDF |

## Notes

- `applications/` (tracker, per-application dirs, discovery data) is
  **gitignored on purpose** — it contains live, private details about real
  companies the candidate is engaged with. The harness operates on it
  locally; the public repo shows the machinery, not the pipeline's private
  state.
- `braindump.md` is also intentionally not checked in — it is a local
  knowledge bank (personal context, preferences) that agents create and use
  as needed.
- This repo is the "public artifact of agentic workflow" referenced in the
  candidate's own applications: the resume tooling, agent operating contract,
  daemons, and browser-automation machinery described here were all built and
  operated by the agent pipeline itself.
