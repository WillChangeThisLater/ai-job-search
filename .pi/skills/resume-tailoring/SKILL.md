---
name: resume-tailoring
description: How to author and visually polish tailored resumes in this repo — content principles (simple, honest), the render→view→critique loop, and the PDF pipeline gotchas.
---

# Resume Tailoring

Workflow for creating `resumes/<field>/wendt_paul_resume.md` and its rendered PDF. This skill is
project-specific: it assumes the repo layout in the root `AGENTS.md` (evidence bank in
`RESUME.md`, one directory per field, `scripts/md2pdf.sh`).

## Content: write it before you style it

### Distill from the evidence bank, not from memory
- Read `RESUME.md` first. It is the source of truth for experience, metrics, and scope.
  Never invent or embellish numbers; the bank already has concrete ones (e.g. "cut
  ingestion 75%, 1.2M → ~300K videos/day").
- Skim an existing field's resume (e.g. `resumes/ml-platform/wendt_paul_resume.md`) for structure —
  but genuinely re-angle content for the new field. A `data-engineer` resume leads with
  pipelines/tables/partitioning; an `agentic-platform` resume leads with services/agents.
  Do not copy-paste with a new title.

### Paul's content rules (apply regardless of role)
1. **Keep bullets simple.** One idea per bullet. Lead with the verb + what was built;
   metric follows if one exists. If a bullet needs a semicolon AND a "which became" AND
   an em-dash aside, split or cut it. Bullets that survive multiple re-reads are the ones
   that stay short.
2. **Be honest.** No title inflation beyond what's real, no claiming other people's
   systems, no "PoC" dressed up as production (mark it "successful PoC" if used). If a
   number is approximate, write ~. Interviewers will probe every line.
3. **Jargon check.** No internal codenames ("Friday", "RTBF") — spell out what the thing
   is for a hiring manager who has never heard of it.
4. **Links attach to phrases**, never bare URLs (see AGENTS.md cosmetics rules).
5. **One page. Always.** Verified by page count, not by eyeball.
6. **Fit flagging.** Note known gaps in the application's `application.md` "Fit / keywords"
   section at scaffold time — do not bend the resume to hide a real gap.

### Ordering / emphasis
- Experience first, Education after (degrees before experience is for new grads).
- Certifications and Projects near the end; Projects are a place to show AI-flavored
  side work (agents, RAG, automation) — pick 2–3, not all of them.
- Paul reviews and approves every resume before it is used for any application
  (hard gate in AGENTS.md — present the drafted content, wait for approval).

## Visual: the render → view → think loop

Do not judge layout from the markdown. Render the PDF, convert to PNG, **look at it**,
and critique like a designer. Repeat until it passes.

```bash
cd /home/paul/ai-job-search
./scripts/md2pdf.sh resumes/<field>/wendt_paul_resume.md resumes/<field>/wendt_paul_resume.pdf
pdftotext resumes/<field>/wendt_paul_resume.pdf - | tr -cd '\f' | wc -c   # must print 1
pdftoppm -png -r 100 resumes/<field>/wendt_paul_resume.pdf /tmp/wendt_resume_vN
# then Read /tmp/wendt_resume_vN-1.png and actually look at it
```

Critique checklist (each iteration, with a critical eye):

- **Flow**: does the page read top-to-bottom in the right order of importance? Is the
  strongest content (most recent, most relevant role) doing the most visual work?
- **Margins**: text should fill the page edge-to-edge with even margins — a narrow
  column with wide whitespace means the style isn't being applied (see gotchas).
- **Hierarchy**: name > section headings > company names > job titles > dates/body.
  Every layer should be visually distinct (size, weight, italics — not all three at once
  for unrelated things).
  - Companies: bold, slightly larger. Titles: bold italic, body size.
    Dates: italic, regular weight. This trio is the current convention.
- **Density**: no big dead whitespace at the bottom; bullets not cramped (2px breathing
  room between list items); no orphaned single words wrapping to a second line.
- **Tables**: skills table spans full width, first column doesn't wrap mid-label.
- **No literal URLs**, no overflowing lines, exactly 1 page.

One change per iteration: adjust → re-render → re-view. Two pages after a change means
dial the last change back (font size, margins, list spacing) rather than deleting content
first.

## Pipeline gotchas (learned the hard way — 2026-09-09 session)

All live in `scripts/md2pdf.sh` + `scripts/resume-style.html`; read them before
"fixing" a render by hand:

- Styles must be **inlined via `-H`** — pandoc's standalone template CSS overrides
  linked stylesheets.
- Pandoc's template sets `body { max-width: 36em; margin: auto }` — if `resume-style.html`
  doesn't override with `max-width: none; margin: 0`, the resume renders as a narrow
  centered column. This is the classic "resume looks narrow" bug.
- Use `-f gfm+hard_line_breaks` so single newlines (dates under titles, address lines)
  render as line breaks instead of being collapsed into one run-on line.
- Print via **CDP `Page.printToPDF`** (`scripts/cdp.py print`), not chrome's
  `--print-to-pdf` CLI flag — the CDP path is deterministic; the CLI path has shown
  caching/geometry quirks. `md2pdf.sh` already wires this up (starts chrome on :9222
  if needed).
- Font sizing that currently works: body 9pt / 1.2 line-height, h1 1.7em, h2 1.15em,
  h3 1.1em, h4 1em italic, `@page` margin 0.3in × 0.4in. These fill one page with this
  much content — re-tune together, not one at a time.
- For true pixel-level GUI inspection (e.g. PDF in a viewer), use the x11-gui-automation
  skill — but `pdftoppm` + Read is usually sufficient and faster.

## After approval

On approval for a submission: copy the rendered PDF into the application directory as `applications/<application>/wendt_paul_resume.pdf` (no `_v1` snapshots in `resumes/` — one copy per field),
point the application's `resume_used:` frontmatter at the versioned file, and commit.
