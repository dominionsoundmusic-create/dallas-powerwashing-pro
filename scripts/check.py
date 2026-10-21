#!/usr/bin/env python3
"""Rule and SEO checks over the built site in dist/.

Checks every built page for the hard rules in CLAUDE.md (banned phrases, em dashes,
places outside Dallas-Fort Worth, DIY machine advice), SEO basics (one H1, unique title and
description, canonical, JSON-LD validity, FAQ count) and link/image integrity.

Usage: python3 scripts/check.py [--dist DIR] [--only /services/]
Exit code 1 if any error is found.
"""
import argparse
import json
import re
import sys
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ORIGIN = "https://dallaspowerwashingpro.com"
PHONE_TEL = "tel:+14696497066"
DUPLANTIS = "— Jesse Duplantis"

BANNED = [
    r"\bwe clean", r"\bwe wash", r"\bwe use\b", r"\bwe offer", r"\bwe provide", r"\bwe remove",
    r"\bwe will clean", r"\bwe're\b", r"\bour crew", r"\bour team", r"\bour equipment",
    r"\bour technician", r"\bour pros?\b", r"\bour (?:soft|pressure) wash", r"\bour services?\b",
    r"\bour company", r"\bour work\b", r"\beco-friendly", r"\bsame[- ]day\b", r"\btop[- ]rated",
    r"#1\b", r"\blicensed and insured\b", r"\bfully insured\b", r"\bsatisfaction guarantee",
    r"\bguaranteed\b", r"\byears of experience", r"\baward", r"\b5[- ]star", r"\bfive[- ]star",
    r"\bnozzle tip", r"\b(?:red|yellow|green|white|black) tip\b", r"\b\d{2,3}[- ]degree (?:tip|nozzle)",
    r"\bmix(?:ing)? ratio", r"\bparts? (?:bleach|water) to\b", r"\bset (?:your|the) (?:machine|pressure washer)",
    r"\bfree estimates?\b", r"\bbest price", r"\bcheapest\b", r"\bguarantee", r"\b500\+", r"\bour technicians?\b",
    r"\bDallas Metro\b", r"\byour trusted partner", r"\bone-stop solution", r"\blook no further", r"\bunmatched excellence",
    r"\bwe've got you covered", r"\bwe are (?:licensed|insured)", r"\bwe repair", r"\bour staff",
]
OUTSIDE = ["Houston", "Katy", "Harris County", "Fort Bend", "Pflugerville", "Georgia", "Virginia", "Friendswood",
           "Deer Park", "League City", "Fulshear", "El Paso", "Austin", "San Antonio", "Florida", "Pennsylvania",
           "(832)", "(903)", "903-636", "(713)", "(281)"]


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text = []
        self.skip = 0
        self.h1 = 0
        self.title = ""
        self._in_title = False
        self.meta = {}
        self.links = []
        self.imgs = []
        self.ids = []
        self.canonical = None
        self.jsonld = []
        self._in_ld = False
        self._ld = ""
        self.headings = []
        self._h = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])
        if tag in ("script", "style"):
            self.skip += 1
            if tag == "script" and a.get("type") == "application/ld+json":
                self._in_ld = True
                self._ld = ""
        if tag == "title":
            self._in_title = True
        if tag == "h1":
            self.h1 += 1
        if tag in ("h1", "h2", "h3", "h4"):
            self._h = [tag, ""]
        if tag == "meta":
            k = a.get("name") or a.get("property")
            if k:
                self.meta[k] = a.get("content", "")
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href")
        if tag == "a":
            self.links.append(a.get("href"))
        if tag == "img":
            self.imgs.append(a)

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip -= 1
            if self._in_ld:
                self.jsonld.append(self._ld)
                self._in_ld = False
        if tag == "title":
            self._in_title = False
        if self._h and tag == self._h[0]:
            self.headings.append((self._h[0], self._h[1].strip()))
            self._h = None

    def handle_data(self, data):
        if self._in_ld:
            self._ld += data
        if self._in_title:
            self.title += data
        if self._h:
            self._h[1] += data
        if not self.skip:
            self.text.append(data)


def url_of(path, dist):
    rel = path.relative_to(dist).as_posix()
    if rel == "index.html":
        return "/"
    if rel == "404.html" or (rel.endswith(".html") and not rel.endswith("index.html")):
        return "/" + rel
    return "/" + rel[: -len("index.html")]


def resolve(href, dist):
    href = href.split("#")[0].split("?")[0]
    if not href:
        return True
    if href.startswith(ORIGIN):
        href = href[len(ORIGIN):] or "/"
    p = dist / href.lstrip("/")
    if href.endswith("/"):
        return (p / "index.html").exists()
    return p.exists()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dist", default=str(ROOT / "dist"))
    ap.add_argument("--only", default="")
    ap.add_argument("--skip-links", action="store_true", help="ignore links to pages not built yet")
    args = ap.parse_args()
    dist = Path(args.dist).resolve()
    errors, warnings = [], []
    titles, descs = defaultdict(list), defaultdict(list)
    files = sorted(dist.rglob("*.html"))
    sitemap = (dist / "sitemap.xml").read_text() if (dist / "sitemap.xml").exists() else ""
    for f in files:
        url = url_of(f, dist)
        if args.only and not url.startswith(args.only):
            continue
        raw = f.read_text()
        p = PageParser()
        p.feed(raw)
        text = re.sub(r"\s+", " ", " ".join(p.text))
        noindex = 'name="robots" content="noindex' in raw

        def err(msg):
            errors.append(f"{url}: {msg}")

        def warn(msg):
            warnings.append(f"{url}: {msg}")

        # hard copy rules (visible text + title + meta)
        visible = text + " " + p.title + " " + p.meta.get("description", "")
        for pat in BANNED:
            for mt in re.finditer(pat, visible, re.I):
                ctx = visible[max(0, mt.start() - 50): mt.end() + 50]
                err(f"banned phrase /{pat}/ in: ...{ctx}...")
        visible_nd = visible.replace(DUPLANTIS, "")
        if "—" in visible_nd or "–" in visible_nd:
            for mt in re.finditer("[—–]", visible_nd):
                err(f"em/en dash in: ...{visible_nd[max(0, mt.start()-40): mt.end()+40]}...")
        for c in OUTSIDE:
            if re.search(r"(?<![A-Za-z])" + re.escape(c) + r"(?![A-Za-z])", visible):
                err(f"place or number outside DFW mentioned: {c.strip()}")
        # required on every page
        head4k = raw[:4096]
        if "dwdp:handwritten 2026-10-21" not in head4k:
            err("missing dwdp:handwritten 2026-10-21 comment in first 4KB")
        if "John 3:16" not in raw or DUPLANTIS not in raw or "I believe the unbelievable, I receive the impossible, because it's doable." not in raw:
            err("quote bar (John 3:16 + Duplantis line) missing or altered")
        if "is a free phone line, not a pressure washing company" not in raw or "referral fee" not in raw:
            err("referral disclosure missing")
        if '<link rel="stylesheet"' in raw:
            err("render-blocking stylesheet link (CSS must be inlined)")
        if "googletagmanager.com/gtag/js" in raw and "setTimeout(load,3500)" not in raw:
            err("GA4 not using the delayed loader")
        if "<iframe" in raw:
            err("iframe in static HTML (videos must be click-to-play)")
        if "<form" in raw:
            err("form found: the site is phone only")
        body_imgs = [i.get("src") for i in p.imgs if i.get("src", "").startswith("/images/") and "logo" not in i.get("src", "")]
        dups = {x for x in body_imgs if body_imgs.count(x) > 1}
        if dups:
            err(f"same photo used twice on the page: {sorted(dups)}")
        figs = len(re.findall(r'<figure class="fig', raw))
        if url not in ("/404.html",) and not noindex and figs < 2:
            err(f"needs at least 2 in-body images, has {figs}")
        if url != "/404.html" and 'class="hero ' not in raw:
            err("missing full-width hero")
        if re.search(r"\b\d{3,4}\s?psi\b", visible, re.I):
            for mt in re.finditer(r"\b\d[\d,]{2,5}\s?psi\b", visible, re.I):
                warn(f"PSI number (make sure it is not DIY advice): ...{visible[max(0, mt.start()-60): mt.end()+40]}...")
        if "lorem" in visible.lower() or "TODO" in visible:
            err("placeholder text")

        # SEO basics
        if p.h1 != 1:
            err(f"expected exactly one h1, found {p.h1}")
        if not p.title.strip():
            err("missing title")
        if len(p.title) > 70:
            warn(f"title is {len(p.title)} chars: {p.title}")
        d = p.meta.get("description", "")
        if not d:
            err("missing meta description")
        elif not (110 <= len(d) <= 170):
            warn(f"meta description is {len(d)} chars")
        titles[p.title].append(url)
        descs[d].append(url)
        if url != "/404.html" and not noindex:
            if p.canonical != ORIGIN + url:
                err(f"canonical {p.canonical} != {ORIGIN + url}")
            if f"<loc>{ORIGIN}{url}</loc>" not in sitemap:
                err("indexable page missing from sitemap.xml")
        if noindex and f"<loc>{ORIGIN}{url}</loc>" in sitemap:
            err("noindex page listed in sitemap")
        for k in ("og:title", "og:description", "og:url", "og:image"):
            if not p.meta.get(k):
                err(f"missing {k}")
        if p.meta.get("og:image") and not p.meta["og:image"].startswith("https://"):
            err("og:image not absolute")
        # JSON-LD
        if len(p.jsonld) > 1:
            err("more than one JSON-LD block")
        faq_count = 0
        for block in p.jsonld:
            try:
                data = json.loads(block)
            except json.JSONDecodeError as e:
                err(f"invalid JSON-LD: {e}")
                continue
            types = [g.get("@type") for g in data.get("@graph", [])]
            if len(types) != len(set(types)):
                err(f"duplicate JSON-LD types: {types}")
            for g in data.get("@graph", []):
                if g.get("@type") == "FAQPage":
                    faq_count = len(g["mainEntity"])
        visible_faq = raw.count('class="faq__item"')
        if visible_faq != faq_count:
            err(f"visible FAQ items ({visible_faq}) != FAQPage entries ({faq_count})")
        max_faq = 6
        if url not in ("/404.html", "/privacy-policy.html", "/terms.html") and not (3 <= visible_faq <= max_faq):
            err(f"page needs 3 to 6 common questions, has {visible_faq}")
        # headings order
        last = 1
        for tag, label in p.headings:
            lvl = int(tag[1])
            if lvl > last + 1:
                warn(f"heading jumps from h{last} to {tag}: {label[:50]}")
            last = lvl
        # links and images
        for href in p.links:
            if href is None or href.strip() in ("", "#"):
                err("empty href")
                continue
            if href.startswith(("tel:", "mailto:", "http://", "https://")) and not href.startswith(ORIGIN):
                if href.startswith("tel:") and href != PHONE_TEL:
                    err(f"unexpected phone link {href}")
                continue
            if not resolve(href, dist):
                if not args.skip_links:
                    err(f"broken internal link {href}")
            elif href.startswith("/") and not href.split("#")[0].endswith(("/", ".html", ".xml", ".txt", ".svg", ".jpg", ".png")):
                warn(f"internal link without trailing slash {href}")
        for im in p.imgs:
            src = im.get("src", "")
            if not im.get("alt") and im.get("alt") != "":
                err(f"img missing alt: {src}")
            if not im.get("width") or not im.get("height"):
                err(f"img missing width/height: {src}")
            if src.startswith("/") and not (dist / src.lstrip("/")).exists():
                err(f"missing image file {src}")
        dup_ids = {i for i in p.ids if p.ids.count(i) > 1}
        if dup_ids:
            err(f"duplicate ids: {sorted(dup_ids)}")
        words = len(text.split())
        if any(f'data-content="{t}"' in raw for t in ("service", "guide", "city")) and words < 1000:
            warn(f"only {words} words on page (including template)")

    for t, urls in titles.items():
        if len(urls) > 1:
            errors.append(f"duplicate title '{t}' on {urls}")
    for d, urls in descs.items():
        if len(urls) > 1 and d:
            errors.append(f"duplicate description on {urls}")

    # _redirects: every target must exist, and no rule may shadow a real page
    red = dist / "_redirects"
    if red.exists():
        for line in red.read_text().splitlines():
            parts = line.split()
            if not parts or parts[0].startswith("#"):
                continue
            src, dst = parts[0], parts[1]
            if not resolve(dst, dist):
                errors.append(f"_redirects: target {dst} does not exist (from {src})")
            if "*" not in src and src != "/" and resolve(src, dist) and not src.endswith(".html"):
                errors.append(f"_redirects: rule {src} shadows a real page")
            if "*" in src:
                base = src.split("*")[0]
                if any(url_of(f, dist).startswith(base) and url_of(f, dist) != base for f in files):
                    errors.append(f"_redirects: wildcard {src} overlaps real pages")
    else:
        errors.append("dist/_redirects missing")
    errors = list(dict.fromkeys(errors))
    for w in warnings:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    print(f"\n{len(files)} pages checked, {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
