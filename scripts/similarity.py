#!/usr/bin/env python3
"""Duplication check (CLAUDE.md hard rule 11).

Compares only the page-specific content (the data-content block plus the FAQ answers),
not the shared header, call-to-action band, disclosure, card grids or footer.

Measure: Jaccard similarity on 5-word shingles.
  1. every pair of Dallas pages of the same type (service, guide, city, page)
  2. every Dallas page against every Houston Power Washing Pro page (any type)
Any pair above 15% fails. Also reports the longest run of identical words for flagged pairs.

Usage: python3 scripts/similarity.py [--dist DIR] [--houston DIR] [--limit 0.15]
Exit code 1 if any pair is above the limit.
"""
import argparse
import re
import sys
from html import unescape
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOUSTON_DIST = Path("/home/claude/houston-powerwashing-pro/dist")


def page_type(raw):
    m = re.search(r'data-content="([a-z]+)"', raw)
    return m.group(1) if m else "page"


def content_words(raw):
    m = (re.search(r'<div class="page-content"[^>]*>(.*?)<section class="band band--navy cta"', raw, re.S)
         or re.search(r'<div class="page-content"[^>]*>(.*?)</main>', raw, re.S))
    chunk = m.group(1) if m else raw
    chunk = re.sub(r"<!--.*?-->", " ", chunk, flags=re.S)
    chunk = re.sub(r"<script.*?</script>", " ", chunk, flags=re.S)
    chunk = re.sub(r'<aside class="sources".*?</aside>', " ", chunk, flags=re.S)
    chunk = re.sub(r'<ul class="pill-list">.*?</ul>', " ", chunk, flags=re.S)
    chunk = re.sub(r'<div class="cards">.*?</div>\s*</article>\s*</div>', " ", chunk, flags=re.S)
    chunk = re.sub(r'<div class="note">\s*<p><strong>(?:How this line works|About this line).*?</div>', " ", chunk, flags=re.S)
    chunk = re.sub(r'<ol class="how-strip">.*?</ol>', " ", chunk, flags=re.S)
    chunk = re.sub(r'<div class="note note--amber">.*?</div>', " ", chunk, flags=re.S)
    text = unescape(re.sub(r"<[^>]+>", " ", chunk))
    return re.findall(r"[a-z0-9']+", text.lower())


def shingles(words, n=5):
    return {" ".join(words[i:i + n]) for i in range(len(words) - n + 1)}


def jaccard(a, b):
    return len(a & b) / max(1, len(a | b))


def longest_common_run(a, b):
    best, best_end = 0, 0
    prev = [0] * (len(b) + 1)
    for i in range(1, len(a) + 1):
        cur = [0] * (len(b) + 1)
        ai = a[i - 1]
        for j in range(1, len(b) + 1):
            if ai == b[j - 1]:
                cur[j] = prev[j - 1] + 1
                if cur[j] > best:
                    best, best_end = cur[j], i
        prev = cur
    return best, " ".join(a[best_end - best:best_end])


def load(dist):
    pages = {}
    for f in sorted(dist.rglob("*.html")):
        raw = f.read_text()
        rel = "/" + f.relative_to(dist).as_posix()
        rel = rel[: -len("index.html")] if rel.endswith("index.html") else rel
        if rel in ("/404.html",):
            continue
        words = content_words(raw)
        pages[rel] = (page_type(raw), words, shingles(words))
    return pages


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dist", default=str(ROOT / "dist"))
    ap.add_argument("--houston", default=str(HOUSTON_DIST))
    ap.add_argument("--limit", type=float, default=0.15)
    args = ap.parse_args()
    dallas = load(Path(args.dist))
    bad = 0
    report = []
    by_type = {}
    for url, (t, w, sh) in dallas.items():
        by_type.setdefault(t, []).append(url)
    for t, urls in sorted(by_type.items()):
        scores = []
        for a, b in combinations(urls, 2):
            j = jaccard(dallas[a][2], dallas[b][2])
            scores.append((j, a, b))
            if j > args.limit:
                bad += 1
                run, phrase = longest_common_run(dallas[a][1], dallas[b][1])
                print(f"FLAG {t}: {a} vs {b}: Jaccard {j:.1%}, longest shared run {run} words: \"{phrase[:140]}\"")
        if scores:
            scores.sort(reverse=True)
            report.append(f"{t} pages ({len(urls)}), {len(scores)} pairs: highest {scores[0][0]:.1%} "
                          f"({scores[0][1]} vs {scores[0][2]}), lowest {scores[-1][0]:.1%}")
        else:
            report.append(f"{t} pages ({len(urls)}): no pairs")
    hdir = Path(args.houston)
    if hdir.exists():
        houston = load(hdir)
        top = (0, "", "")
        for a, (ta, wa, sa) in dallas.items():
            for b, (tb, wb, sb) in houston.items():
                j = jaccard(sa, sb)
                if j > top[0]:
                    top = (j, a, b)
                if j > args.limit:
                    bad += 1
                    print(f"FLAG vs Houston: {a} vs houston{b}: Jaccard {j:.1%}")
        report.append(f"Dallas vs Houston ({len(dallas)} x {len(houston)} pages): highest {top[0]:.1%} ({top[1]} vs houston{top[2]})")
    else:
        report.append("Houston dist not found: cross-site check NOT run")
    print("\n".join(report))
    print(f"\n{bad} pairs above {args.limit:.0%}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
