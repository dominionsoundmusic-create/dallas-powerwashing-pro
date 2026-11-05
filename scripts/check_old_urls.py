#!/usr/bin/env python3
"""Every URL the live site had must still work on the rebuilt site.

The old site (main branch, saved in docs/old-site/) is read for its URLs: every <loc> in its
sitemap.xml, every file in its tree (pages and icons; its photos are listed below because they now
live in src/static/images/) and every URL its _redirects file already redirected. Main's git history
here is a single commit, so deleted files can not be listed; the old wildcard rules are kept instead.
Each URL must either be
served by a file in dist/ or be caught by a 301 rule in dist/_redirects whose target exists in dist/.

Usage: python3 scripts/check_old_urls.py [--dist dist] [--report docs/qa-old-urls.md]
Exit code 1 if any old URL would 404.
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OLD = ROOT / "docs" / "old-site"
SKIP = {"/_redirects", "/retired-urls.txt"}
OLD_IMAGES = ["/images/logo.svg"] + [f"/images/{n}.jpg" for n in (
    "pw-01-card", "pw-01-hero", "pw-02-card", "pw-03-card", "pw-03-hero", "pw-04-card", "pw-05-card", "pw-06-card", "pw-06-hero", "pw-hero")]


def old_urls():
    urls = set(re.findall(r"<loc>https://dallaspowerwashingpro\.com(/[^<]*)</loc>", (OLD / "sitemap.xml").read_text()))
    for f in OLD.rglob("*"):
        if f.is_file():
            rel = "/" + f.relative_to(OLD).as_posix()
            if rel.endswith("/index.html"):
                rel = rel[: -len("index.html")]
            if rel == "/index.html":
                rel = "/"
            urls.add(rel)
            if rel.endswith(".html") and rel not in ("/privacy-policy.html", "/terms.html"):
                urls.add(rel[: -len(".html")])  # Netlify pretty URL the live site linked to
    retired = OLD / "retired-urls.txt"
    if retired.exists():
        for line in retired.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                urls.add(line)
    for line in (OLD / "_redirects").read_text().splitlines():
        parts = line.split()
        if parts and not parts[0].startswith("#") and "*" not in parts[0]:
            urls.add(parts[0])
    return sorted(u for u in urls | set(OLD_IMAGES) if u not in SKIP)


def served(url, dist):
    p = dist / url.lstrip("/")
    if url.endswith("/"):
        return (p / "index.html").exists()
    return p.is_file() or (dist / (url.lstrip("/") + ".html")).exists()


def rules(dist):
    out = []
    for line in (dist / "_redirects").read_text().splitlines():
        parts = line.split()
        if parts and not parts[0].startswith("#"):
            out.append((parts[0], parts[1], parts[2] if len(parts) > 2 else "301"))
    return out


def redirected(url, rs):
    for src, dst, code in rs:
        if src == url or ("*" in src and url.startswith(src.split("*")[0]) and url != src.split("*")[0]):
            return src, dst, code
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dist", default=str(ROOT / "dist"))
    ap.add_argument("--report", default="")
    args = ap.parse_args()
    dist = Path(args.dist)
    rs = rules(dist)
    rows, bad = [], 0
    for u in old_urls():
        if served(u, dist):
            # a served file wins over any rule without "!" on Netlify
            rows.append((u, "200", "served by a rebuilt page or file at the same path"))
            continue
        r = redirected(u, rs)
        if r and served(r[1], dist):
            rows.append((u, r[2], f"redirect to {r[1]} (rule {r[0]})"))
        else:
            bad += 1
            rows.append((u, "404", "NOT FOUND"))
    for u, code, how in rows:
        print(f"{code}  {u}  {how}")
    print(f"\n{len(rows)} old URLs checked, {bad} would 404")
    if args.report:
        lines = ["| Old URL | Result | How |", "|---|---|---|"] + [f"| {u} | {c} | {h} |" for u, c, h in rows]
        lines.append(f"\n{len(rows)} old URLs checked, {bad} would 404.")
        Path(args.report).write_text("\n".join(lines) + "\n")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
