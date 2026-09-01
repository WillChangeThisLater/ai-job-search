#!/bin/bash
# Purpose: markdown -> PDF via headless Chrome (no LaTeX/weasyprint dependency)
# Usage: md2pdf.sh <input.md> <output.pdf>
# Dependencies: pandoc, google-chrome. Working dir: anywhere.
set -e
IN="$1"; OUT="$2"
TMP=$(mktemp --suffix=.html)
pandoc "$IN" -f gfm -t html5 -s --metadata title="Resume" -c /home/paul/job-search/scripts/resume.css -o "$TMP"
google-chrome --headless --disable-gpu --no-sandbox --print-to-pdf="$OUT" --no-pdf-header-footer "$TMP" 2>/dev/null
rm -f "$TMP"
echo "wrote $OUT"
