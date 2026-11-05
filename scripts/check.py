#!/usr/bin/env python3
"""Rule and SEO checks over the built site in dist/.

Checks every built page for the hard rules in CLAUDE.md (banned phrases that imply Dallas Power
Washing Pro does the work or holds a license, invented trust claims, em dashes, places outside
Dallas-Fort Worth, forms outside /contact/, eyebrow labels, the exact
top-bar quote, the referral disclosure in the footer), SEO basics (one H1, unique title and
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
MARK = "dwdp:handwritten 2026-11-05"
QUOTE = "I believe the unbelievable, I receive the impossible, because it's doable."

BANNED = [
    # implies the line does the work or holds a license
    r"\bour technicians?\b", r"\bour techs?\b", r"\bour trucks?\b", r"\bour vans?\b", r"\bour team\b", r"\bour crews?\b",
    r"\bour (?:experts?|pros?|cleaners?|staff|employees|guys?|washers?)\b", r"\bour (?:repair|cleaning|service|maintenance|washing|soft) ",
    r"\bwe (?:wash|clean|pressure|power|soft|repair|install|fix|service|replace|inspect|quote|schedule|send|dispatch|seal|stain|treat|rinse|scrub|remove)\b",
    r"\bwe(?:'re| are) (?:licensed|insured|certified|bonded)\b", r"\bwe hold (?:a|an) (?:license|licence|certification)\b",
    r"\bwe(?:'ll| will) (?:send|fix|wash|clean|be there|come out)\b", r"\bour licen[cs]e\b", r"\bour certifi",
    # invented trust claims and the INTAKE.md words to avoid
    r"\blicensed and insured\b", r"\binsured and licensed\b", r"\bfully insured\b", r"\bsatisfaction guarantee", r"(?<!not )(?<!never )(?<!no )(?<!or )\bguarantee[ds]?\b",
    r"\byears of experience", r"\baward[- ]winning\b", r"\b5[- ]star", r"\bfive[- ]star", r"\btop[- ]rated", r"\bbest in\b",
    r"#1\b", r"\bnumber one\b", r"\bsame[- ]day\b", r"\bwithin (?:an|one|1|two|2|four|4) hours?\b", r"\bA\+ rating\b",
    r"\bfree estimates?\b", r"\bbest (?:prices?|rates?)\b", r"\blowest price", r"\bcheapest\b",
    r"\bstarting at\b", r"\bbackground[- ]checked\b", r"\bowner-run\b", r"\baggregateRating\b",
    # filler phrases banned in CLAUDE.md
    r"\byour trusted partner\b", r"\bone-stop solution\b", r"\blook no further\b", r"\bunmatched excellence\b",
    r"\bwe've got you covered\b", r"\bwe have got you covered\b",
    # old brand and leftovers from the sites this build system came from
    r"Dallas Metro Power Washing", r"\bYuma\b", r"\bTucson\b", r"\bPhoenix\b", r"\bHouston\b", r"\bArizona\b", r"\bpools?\b", r"\bROC\b",
    r"\(928\)", r"\(903\)", r"903-636", r"903-505", r"\bHVAC\b",
    # gutter cleaning is not a service here
    r"\bgutter cleaning (?:service|company|companies|in)\b", r"\bgutter cleaning page\b",
]
# Places outside Dallas-Fort Worth must not appear.
OUTSIDE = ["Houston", "Austin", "San Antonio", "El Paso", "Oklahoma", "Louisiana", "Arkansas", "New Mexico", "Georgia", "Florida",
           "California", "Arizona", "Waco", "Tyler", "Gilmer", "Longview", "Dallas, GA", "Dallas, Georgia", "Dallas, Oregon",
           "Dallas, OR", "Dallas County, Iowa"]


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


FLAT = {"/privacy-policy.html", "/terms.html", "/404.html"}
# pages with no FAQ block or in-body images (the thank-you page is noindex, like 404)
EXEMPT = ("/404.html", "/privacy-policy.html", "/terms.html", "/contact/thanks/")


def url_of(path, dist):
    rel = path.relative_to(dist).as_posix()
    if rel == "index.html":
        return "/"
    if not rel.endswith("/index.html"):
        # flat pages
        return "/" + rel if "/" + rel in FLAT else "/" + rel[:-len(".html")]
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
    # flat URLs are served from name.html
    return p.exists() or (dist / (href.lstrip("/") + ".html")).exists()


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
        if "—" in visible or "–" in visible:
            for mt in re.finditer("[—–]", visible):
                err(f"em/en dash in: ...{visible[max(0, mt.start()-40): mt.end()+40]}...")
        for c in OUTSIDE:
            if re.search(r"\b" + re.escape(c) + r"\b", visible):
                err(f"place outside Dallas-Fort Worth mentioned: {c}")
        # The quote form lives on /contact/ only (Netlify form dallas-powerwashing-contact).
        if url == "/contact/":
            if 'name="dallas-powerwashing-contact"' not in raw or "data-netlify" not in raw:
                err("contact quote form dallas-powerwashing-contact missing")
            for fld in ("name", "phone", "city", "need", "message", "form-name", "bot-field"):
                if f'name="{fld}"' not in raw:
                    err(f"contact form field {fld} missing")
        elif "<form" in raw:
            err("form found outside /contact/")
        if re.search(r'class="[^"]*(?:eyebrow|kicker|overline|badge)', raw):
            err("eyebrow/badge label found")
        if QUOTE not in raw.replace("&#39;", "'").replace("&rsquo;", "'"):
            err("top-bar quote missing or not exact")
        if "Jesse Duplantis" not in raw:
            err("quote credit missing")
        if "Dominion Digital Group. All rights reserved." not in raw or "https://dominionwebdesignpro.com" not in raw:
            err("footer copyright or credit missing")
        if url != "/404.html" and "is a free phone line, not a power washing company" not in visible:
            err("referral disclosure missing from the footer")
        if url != "/404.html" and "Companies may pay a referral fee." not in visible:
            err("referral fee sentence missing")
        if 'aria-label="Language"' not in raw:
            err("EN/ES toggle missing")
        if "aggregateRating" in raw:
            err("aggregateRating found")
        if MARK not in raw[:4096]:
            err("dwdp:handwritten marker missing from the first 4KB")
        if "lorem" in visible.lower() or "TODO" in visible or "PHONE_" in raw:
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
        if url not in EXEMPT and 'class="sources"' not in raw:
            err("sources list missing")
        # images: hero plus at least two in-body figures on every content page
        pending = re.findall(r"<!-- image pending .*?-->(<figure)?", raw)
        figs = raw.count('<figure class="fig') + sum(1 for g in pending if not g)
        has_hero = '<section class="hero ' in raw
        if url not in EXEMPT and (not has_hero or figs < 2):
            err(f"needs a hero and at least two in-body images (hero={has_hero}, body images={figs})")
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
        if url not in EXEMPT:
            if not (3 <= visible_faq <= max_faq):
                err(f"page needs 3 to 6 common questions, has {visible_faq}")
            if 'id="faq-title">Common questions<' not in raw:
                err("visible 'Common questions' block missing")
            if faq_count == 0:
                err("FAQPage JSON-LD missing")
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
            elif href.startswith("/") and not href.split("#")[0].endswith(("/", ".html", ".xml", ".txt", ".svg", ".jpg", ".png", ".pdf")) \
                    and not (dist / (href.split("#")[0].lstrip("/") + ".html")).exists():
                warn(f"internal link without trailing slash {href}")
        if url not in ("/404.html",):
            for m_img in re.finditer(r'<figure class="fig[^"]*">(?:<picture>.*?</source>?)?.*?<img ([^>]*)>', raw, re.S):
                if 'loading="lazy"' not in m_img.group(1):
                    err("in-body figure image without loading=lazy")
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
        body_type = re.search(r'<body class="type-([a-z]+)', raw)
        if body_type and body_type.group(1) in ("service", "guide", "area") and words < 1500:
            warn(f"only {words} words on page (including template)")

    for t, urls in titles.items():
        if len(urls) > 1:
            errors.append(f"duplicate title '{t}' on {urls}")
    for d, urls in descs.items():
        if len(urls) > 1 and d:
            errors.append(f"duplicate description on {urls}")

    # _redirects: every target must exist, and no rule may shadow a real page
    red = dist / "_redirects"
    if args.skip_links:
        pass
    elif red.exists():
        for line in red.read_text().splitlines():
            parts = line.split()
            if not parts or parts[0].startswith("#"):
                continue
            src, dst = parts[0], parts[1]
            if not resolve(dst, dist):
                errors.append(f"_redirects: target {dst} does not exist (from {src})")
            if "*" not in src and src != "/" and resolve(src, dist) and not src.endswith(".html"):
                errors.append(f"_redirects: rule {src} shadows a real page")
            # Netlify serves an existing file before applying a rule that has no "!" (force), so a
            # wildcard never hides a real page; a forced rule would.
            if len(parts) > 2 and parts[2].endswith("!"):
                errors.append(f"_redirects: forced rule {src} would hide real pages")
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
