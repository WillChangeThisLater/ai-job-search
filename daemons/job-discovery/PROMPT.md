# Task: Daily job discovery sweep

You are the job-discovery daemon for the ai-job-search pipeline. Execute one discovery run,
then stop. Budget yourself ~45 minutes of work; quality beats quantity.

## Goal

Append **at least 5 new quality prospects** to `/home/paul/ai-job-search/applications/prospects.csv`.

**Quality bar** (all required):
- AI/agentic engineering, ML ops/data platform, or tightly-fitting senior SWE (see
  `/home/paul/ai-job-search/AGENTS.md` "Role-fit vetting" and `RESUME.md` for Paul's actual experience)
- Company not already recorded anywhere (see dedupe gate below)
- Posting looks live (< ~3 weeks old, not obviously expired)
- Real URL or precise search instructions recorded in the URL column

## Procedure

1. **Read the playbook**: `/home/paul/ai-job-search/applications/JOB_SOURCES.md`. It documents every
   source that works, how to access it, and known failures. Also read `AGENTS.md` (writing-voice and
   vetting rules) and skim `prospects.csv` so you don't duplicate.

2. **Check rotation state**: `/home/paul/.cache/job-discovery-daemon/state.json` records recently
   used (source, query, city) combos. Prefer combos not used in the last ~7 runs. Create the file
   if missing.

3. **Sweep known sources** (Tier 1 first): HN Who's Hiring (check the current month's thread),
   LinkedIn guest API, Built In — with fresh keyword/city rotations. Aim to cover all four
   buckets over time: NYC, Boston, Philadelphia, Remote (see braindump preferences; remote-US only).

4. **If short of 5 after known sources**: explore ONE new source. Ideas ladder: other cities'
   Built In sites, company career pages of AI companies from prospects.csv competitors,
   r/hiring aggregators, Otta/Welcome to the Jungle, Wellfound with in-page search, EU-remote
   boards filtered to US-timezone,YC company directory, levels.fyi postings, staffing-firm
   feeds. Try to find a structured/API/RSS access path first (see JOB_SOURCES.md patterns).
   **Record the outcome in JOB_SOURCES.md** — works (with URL recipe + yield) or doesn't
   (with reason). A failed exploration is a valid run as long as the quota is met from
   known sources.

5. **Dedupe gate (hard requirement)**: before appending each row, run
   `python3 /home/paul/ai-job-search/scripts/check_dup.py --company "<Company>" --role "<Role>"`.
   Exit 0 → append. Exit 1 or 2 → skip the row entirely (do not add same-company rows that
   would make this decision harder later; a different role at a recorded company is only worth
   adding if clearly distinct AND high match — then note "role #N for this co" in Notes).

6. **Append rows** to prospects.csv with the standard 14 columns (match existing format exactly —
   use python csv, never raw string concat). Fill every column: Company, Source, Location,
   Role Title, Role Type (AI/Agent Engineering | Data/Platform | SWE), Salary, Equity, Status
   ("Not Applied"), Date Applied (empty), URL, Notes (1-2 sentences, concrete), Match (★ rating
   + tag), Key Skills Required, Key Gaps. Be honest with Match — a repo full of ★★★★★ is useless.

7. **Commit**: `git -C /home/paul/ai-job-search add -A && git commit -m "discovery <date>: +N prospects (<sources>)" && git push`.
   If JOB_SOURCES.md changed, mention it in the message.

8. **Notify**: one ntfy message summarizing the run:
   `curl -s -H "Title: discovery <date>: +N prospects" -d "<one line per job: Company — Role (city)>" ntfy.sh/<topic from run.sh env>`

9. **Write report.md** next to the run artifacts: sources tried, new-source explorations +
   outcomes, jobs added, dedupe rejects worth mentioning. Then stop.
