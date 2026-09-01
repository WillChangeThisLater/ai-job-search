#!/usr/bin/env python3
"""Duplicate-application guard.

Before scaffolding/applying to any job, run:
    python3 scripts/check_dup.py --company "Acme" --role "Senior AI Engineer"
    python3 scripts/check_dup.py --url "https://news.ycombinator.com/item?id=123"

Checks across applications/ (application dirs + tracker.csv) and
applications/prospects.csv. Exit code 0 = clear, 1 = duplicate found,
2 = fuzzy match worth human review.

This is a hard gate per AGENTS.md: do not start an application when this
returns 1. When it returns 2, show the match to the human and let them decide.
"""
import argparse, csv, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_DIR = os.path.join(ROOT, "applications")
TRACKER = os.path.join(APP_DIR, "tracker.csv")
PROSPECTS = os.path.join(APP_DIR, "prospects.csv")

def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()

def load_csv(path):
    if not os.path.exists(path):
        return []
    with open(path, newline="") as f:
        return [r for r in csv.DictReader(f)]

def records():
    recs = []
    # application dirs: <slug-company-role>/application.md frontmatter has company/role/posting_url
    for d in os.listdir(APP_DIR):
        md = os.path.join(APP_DIR, d, "application.md")
        if os.path.isdir(os.path.join(APP_DIR, d)) and os.path.exists(md):
            text = open(md).read()
            comp = re.search(r"^company:\s*(.+)$", text, re.M)
            role = re.search(r"^role:\s*(.+)$", text, re.M)
            url = re.search(r"^posting_url:\s*(.+)$", text, re.M)
            status = re.search(r"^status:\s*(.+)$", text, re.M)
            recs.append({
                "company": comp.group(1).strip() if comp else d,
                "role": role.group(1).strip() if role else "",
                "url": url.group(1).strip() if url else "",
                "status": status.group(1).strip() if status else "?",
                "where": f"applications/{d}/",
            })
    for path in (TRACKER, PROSPECTS):
        for r in load_csv(path):
            recs.append({
                "company": r.get("Company", ""),
                "role": r.get("Role Title", ""),
                "url": r.get("URL", ""),
                "status": r.get("Status", ""),
                "where": os.path.basename(path),
            })
    return recs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--company")
    ap.add_argument("--role")
    ap.add_argument("--url")
    args = ap.parse_args()
    if not (args.company or args.url):
        ap.error("need --company (and optionally --role) or --url")

    recs = records()
    # "Open" application = one that isn't terminal. Only one open app per company.
    OPEN = {"identified", "in_progress", "submitted"}
    open_recs = [r for r in recs if r["where"] != "prospects.csv" and r["status"].lower() in OPEN]
    hits, fuzzy = [], []
    for r in recs:
        if args.url and args.url in (r["url"] or ""):
            hits.append(r); continue
        if args.company:
            c_same = norm(args.company) == norm(r["company"])
            if not c_same:
                continue
            exact_role = args.role and (norm(args.role) == norm(r["role"])
                        or norm(args.role) in norm(r["role"])
                        or norm(r["role"]) in norm(args.role))
            if exact_role:
                hits.append(r)
            elif any(o["company"] == r["company"] for o in open_recs):
                hits.append(r)   # company already has an open application
            else:
                fuzzy.append(r)  # same company, different role, nothing open — human decides
    if hits:
        print("DUPLICATE — do not re-apply:")
        for r in hits:
            print(f"  [{r['status']}] {r['company']} | {r['role']} | {r['where']} | {r['url']}")
        sys.exit(1)
    if fuzzy:
        print("POSSIBLE MATCH — review before proceeding:")
        for r in fuzzy:
            print(f"  [{r['status']}] {r['company']} | {r['role']} | {r['where']}")
        sys.exit(2)
    print("CLEAR — no existing record for this company/role/url.")
    sys.exit(0)

if __name__ == "__main__":
    main()
