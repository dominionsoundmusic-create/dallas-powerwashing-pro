#!/usr/bin/env python3
"""Old-URL check: every URL the live site (branch main) has must still work on the new build.

Collects from `main`: every <loc> in sitemap.xml, every .html file (as its public URL), and every
exact source path in main's _redirects. Each must either be a page in dist/ or be matched by a
rule in dist/_redirects whose target is a page in dist/.

Usage: python3 scripts/check_old_urls.py [--ref main] [--dist dist]
Exit code 1 if any old URL would 404.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ORIGIN = "https://dallaspowerwashingpro.com"


def git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True, check=True).stdout


def old_urls(ref):
    urls = set()
    for loc in re.findall(r"<loc>(.*?)</loc>", git("show", f"{ref}:sitemap.xml")):
        urls.add(loc.replace(ORIGIN, "") or "/")
    for f in git("ls-tree", "-r", "--name-only", ref).splitlines():
        if not f.endswith(".html"):
            continue
        if f == "index.html":
            urls.add("/")
        elif f.endswith("/index.html"):
            urls.add("/" + f[: -len("index.html")])
            urls.add("/" + f[: -len("/index.html")])  # extensionless form without slash
        else:
            urls.add("/" + f)
            urls.add("/" + f[: -len(".html")])  # Netlify pretty URL form
    for line in git("show", f"{ref}:_redirects").splitlines():
        parts = line.split()
        if parts and not parts[0].startswith("#") and "*" not in parts[0]:
            urls.add(parts[0])
    return sorted(urls)


def page_exists(dist, path):
    path = path.split("#")[0].split("?")[0]
    p = dist / path.lstrip("/")
    if path.endswith("/"):
        return (p / "index.html").exists()
    if p.is_file():
        return True
    if (p.with_suffix(".html")).is_file() or (p / "index.html").is_file():
        return True  # Netlify serves /x as /x.html or /x/ (pretty URLs)
    return False


def redirect_for(rules, path):
    for src, dst in rules:
        if src == path or src.rstrip("/") == path.rstrip("/") and src != "/":
            return dst
        if src.endswith("*") and path.startswith(src[:-1]):
            return dst
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", default="main")
    ap.add_argument("--dist", default=str(ROOT / "dist"))
    args = ap.parse_args()
    dist = Path(args.dist)
    rules = []
    for line in (dist / "_redirects").read_text().splitlines():
        parts = line.split()
        if len(parts) >= 2 and not parts[0].startswith("#"):
            rules.append((parts[0], parts[1]))
    failed = 0
    rows = []
    for u in old_urls(args.ref):
        if page_exists(dist, u):
            rows.append(f"OK    {u}  (page)")
            continue
        dst = redirect_for(rules, u)
        if dst and page_exists(dist, dst):
            rows.append(f"OK    {u}  -> 301 {dst}")
        else:
            failed += 1
            rows.append(f"FAIL  {u}  (no page, no working redirect)")
    print("\n".join(rows))
    print(f"\n{len(rows)} old URLs checked, {failed} failing")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
