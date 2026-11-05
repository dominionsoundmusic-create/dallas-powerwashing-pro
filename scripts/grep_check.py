#!/usr/bin/env python3
"""CLAUDE.md final grep: banned strings in the built site's visible text, titles, meta and alt text.

Usage: python3 scripts/grep_check.py [--dist dist]. Exit code 1 on any hit.
"""
import argparse
import html
import re
import sys
from pathlib import Path

# The CLAUDE.md "Before you finish" list. The one allowed dash, before "Jesse Duplantis" in the top bar, is
# drawn by CSS (::before), so it never appears in the HTML text.
PATS = ["—", "–", "we wash", "we clean", "we pressure", "we power", "our crew", "our team", "our technicians", "licensed and insured",
        "background checked", "free estimate", "same-day", "same day", "#1", "500+", "starting at", "owner-run", "Yuma", "Tucson", "Phoenix",
        "Scottsdale", "Mesa", "Pima", "Maricopa", "Houston", "Austin", "San Antonio", "Dallas, GA", "Georgia", "California", "Arizona",
        "Dallas Metro", "pool", "lorem", "TODO", "placeholder", "(928)", "(903)", "903-636", "penetrat"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dist", default=str(Path(__file__).resolve().parent.parent / "dist"))
    dist = Path(ap.parse_args().dist)
    total = 0
    for p in PATS:
        files = []
        for f in sorted(dist.rglob("*.html")):
            raw = f.read_text()
            vis = re.sub(r"(?s)<(script|style)[^>]*>.*?</\1>", " ", raw)
            vis = re.sub(r"(?s)<!--.*?-->", " ", vis)
            vis = html.unescape(re.sub(r"<[^>]+>", " ", vis)) + " " + " ".join(re.findall(r'(?:content|alt|title)="([^"]*)"', raw))
            if re.search(r"(?<![a-z])" + re.escape(p.lower()) if p.isalpha() else re.escape(p.lower()), vis.lower()):
                files.append("/" + f.relative_to(dist).as_posix())
        total += len(files)
        print(f"{p!r}: {len(files)} hits {files[:5]}")
    print(f"\n{total} hits in total")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
