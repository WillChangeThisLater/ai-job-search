#!/bin/bash
# Purpose: markdown -> PDF via pandoc + CDP Page.printToPDF (deterministic)
# Usage: md2pdf.sh <input.md> <output.pdf>
# Dependencies: pandoc, google-chrome, scripts/cdp.py (same repo). Working dir: anywhere.
# Notes:
#   - styles are INLINED via -H resume-style.html (pandoc's standalone template CSS
#     would otherwise override linked stylesheets; its max-width/margin are the
#     cause of "narrow column" rendering bugs)
#   - hard_line_breaks so single newlines in the md render as <br>
#   - CDP print (not --print-to-pdf) with preferCSSPageSize: @page margins in the
#     style file control geometry; chrome CLI flag path has shown caching quirks
set -e
IN="$1"; OUT="$2"
DIR=$(cd "$(dirname "$0")" && pwd)
TMP=$(mktemp --suffix=.html)
pandoc "$IN" -f gfm+hard_line_breaks -t html5 -s --metadata title=" " \
  -H "$DIR/resume-style.html" -o "$TMP"

# ensure a headless chrome with CDP is up (reuse if port already open)
if ! curl -s --max-time 2 http://localhost:9222/json/version >/dev/null; then
  (google-chrome --headless --disable-gpu --no-sandbox \
     --remote-debugging-port=9222 about:blank >/dev/null 2>&1 &)
  for i in $(seq 1 20); do
    curl -s --max-time 1 http://localhost:9222/json/version >/dev/null && break
    sleep 0.5
  done
fi

python3 "$DIR/cdp.py" navigate "file://$TMP" >/dev/null
sleep 0.5
python3 "$DIR/cdp.py" print "$OUT"
rm -f "$TMP"
echo "wrote $OUT"
