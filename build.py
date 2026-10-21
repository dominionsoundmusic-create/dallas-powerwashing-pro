#!/usr/bin/env python3
"""Build the static Dallas Power Washing Pro site (dallaspowerwashingpro.com).

Pages live in src/pages as Jinja templates with a YAML front matter block.
Shared business data lives in src/data/site.json. Output goes to dist/.

Usage:
  python3 build.py                 # full build to dist/, also writes docs/image-list.md
  python3 build.py --out DIR       # build somewhere else (no docs written)
"""
import argparse
import html
import json
import re
import shutil
import struct
import sys
from datetime import date
from pathlib import Path

import yaml
from jinja2 import ChainableUndefined, Environment, FileSystemLoader, pass_context
from markupsafe import Markup

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
PAGES = SRC / "pages"
STATIC = SRC / "static"
IMAGES = STATIC / "images"
FM_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)
BUILD_DATE = "2026-10-21"


def image_size(path):
    """Return (width, height) for a JPEG/PNG/WebP file, or None."""
    data = path.read_bytes()
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", data[16:24])
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        if data[12:16] == b"VP8X":
            w = int.from_bytes(data[24:27], "little") + 1
            h = int.from_bytes(data[27:30], "little") + 1
            return w, h
        return None
    if data[:2] == b"\xff\xd8":
        i = 2
        while i < len(data):
            marker = data[i + 1]
            length = struct.unpack(">H", data[i + 2:i + 4])[0]
            if marker in (0xC0, 0xC1, 0xC2):
                h, w = struct.unpack(">HH", data[i + 5:i + 9])
                return w, h
            i += 2 + length
    return None


def url_for_source(rel):
    """src/pages relative path -> public URL path."""
    rel = rel.with_suffix("")
    parts = list(rel.parts)
    if parts == ["index"]:
        return "/"
    if parts == ["404"]:
        return "/404.html"
    if parts[-1] == "index":
        parts = parts[:-1]
    return "/" + "/".join(parts) + "/"


def out_path_for(url, out):
    if url.endswith(".html"):
        return out / url.lstrip("/")
    return out / url.strip("/") / "index.html" if url != "/" else out / "index.html"


def inline_css(text):
    """Light minify for the inline <style> block: drop comments, collapse whitespace."""
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s*([{};:,>])\s*", r"\1", text)
    return text.replace(";}", "}").strip()


def strip_tags(text):
    return html.unescape(re.sub(r"<[^>]+>", "", str(text))).strip()


class Builder:
    def __init__(self, out, write_docs):
        self.out = out
        self.write_docs = write_docs
        self.site = json.loads((SRC / "data" / "site.json").read_text())
        self.missing_images = {}  # filename -> dict
        self.env = Environment(
            loader=FileSystemLoader([str(SRC / "templates"), str(PAGES)]),
            undefined=ChainableUndefined,
            autoescape=False,
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self.env.globals.update(webp_srcset=lambda f: webp_srcset(f),
            site_css=Markup(inline_css((STATIC / "css" / "site.css").read_text())),
            site=self.site,
            img=self.img,
            image_exists=lambda f: bool(f) and (IMAGES / f).exists(),
            img_size=lambda f: image_size(IMAGES / f) or (1200, 750),
            svc=self.find("services"),
            guide=self.find("guides"),
            city=self.find("cities"),
        )
        self.env.filters["striptags_plain"] = strip_tags
        self.env.filters["tojson_ld"] = lambda v: Markup(
            json.dumps(v, ensure_ascii=False, indent=1).replace("</", "<\\/")
        )

    def find(self, key):
        items = {i["slug"]: i for i in self.site[key]}

        def get(slug):
            if slug not in items:
                raise KeyError(f"unknown {key} slug: {slug}")
            return items[slug]
        return get

    # ---- images -------------------------------------------------------
    @pass_context
    def img(self, ctx, file, alt, width, height, desc="", cls="", caption="", lazy=True, fallback="", fallback_alt=""):
        """Render an in-body figure. A planned photo that does not exist yet is listed in
        docs/image-list.md and an existing photo (fallback) is shown in its place, so the
        page never shows a broken image."""
        page = ctx.get("page", {})
        if not (IMAGES / file).exists() and fallback:
            self.note_missing(file, width, height, alt, desc, page.get("url", "?"))
            fw, fh = image_size(IMAGES / fallback) or (width, height)
            planned = f"<!-- planned photo (see docs/image-list.md): /images/{file} -->"
            return Markup(planned + self.img(ctx, fallback, fallback_alt or alt, fw, fh, cls=cls, caption=caption, lazy=lazy))
        tag = (
            f'<img src="/images/{file}" alt="{html.escape(alt, quote=True)}" '
            f'width="{width}" height="{height}"'
            + (' loading="lazy" decoding="async"' if lazy else "")
            + ">"
        )
        cap = f"<figcaption>{caption}</figcaption>" if caption else ""
        cls_attr = f' class="fig {cls}"' if cls else ' class="fig"'
        if (IMAGES / file).exists():
            return Markup(f"<figure{cls_attr}>{tag}{cap}</figure>")
        self.note_missing(file, width, height, alt, desc, page.get("url", "?"))
        return Markup(f"<!-- image pending (see docs/image-list.md): {tag} -->")

    def note_missing(self, file, width, height, alt, desc, url):
        entry = self.missing_images.setdefault(
            file, {"file": file, "size": f"{width}x{height}", "alt": alt, "desc": desc, "pages": []}
        )
        if url not in entry["pages"]:
            entry["pages"].append(url)
        if desc and not entry["desc"]:
            entry["desc"] = desc

    # ---- pages --------------------------------------------------------
    def load_pages(self):
        pages = []
        for path in sorted(PAGES.rglob("*.html")):
            rel = path.relative_to(PAGES)
            if rel.parts[0].startswith("_"):
                continue
            text = path.read_text()
            m = FM_RE.match(text)
            if not m:
                raise SystemExit(f"{rel}: missing front matter")
            meta = yaml.safe_load(m.group(1)) or {}
            meta["url"] = meta.get("url") or url_for_source(rel)
            meta["source"] = str(rel)
            meta["body"] = text[m.end():]
            pages.append(meta)
        return pages

    def render(self, page, pages):
        layout = page.get("layout", "page")
        hero = page.get("hero")
        if hero:
            want = hero.get("image")
            if want and not (IMAGES / want).exists():
                self.note_missing(want, 1920, 1080, hero.get("alt", ""), hero.get("desc", ""), page["url"])
                hero["render_image"] = hero.get("fallback", "pw-hero.jpg")
                hero["render_alt"] = hero.get("fallback_alt", hero.get("alt", ""))
            else:
                hero["render_image"] = want or hero.get("fallback", "pw-hero.jpg")
                hero["render_alt"] = hero.get("alt", "")
            size = image_size(IMAGES / hero["render_image"])
            hero["w"], hero["h"] = size if size else (1920, 1080)
        if page.get("sources"):
            page["sources"] = [self.site["sources"][k] if isinstance(k, str) else k for k in page["sources"]]
        page.setdefault("breadcrumbs", self.breadcrumbs(page))
        page["jsonld"] = self.jsonld(page)
        source = (
            '{% extends "layouts/' + layout + '.html" %}\n'
            '{% import "macros.html" as m with context %}\n' + page["body"]
        )
        tpl = self.env.from_string(source)
        return tpl.render(page=page, pages=pages)

    # ---- breadcrumbs + structured data --------------------------------
    def breadcrumbs(self, page):
        url = page["url"]
        if url in ("/", "/404.html") or page.get("noindex"):
            return []
        crumbs = [{"label": "Home", "href": "/"}]
        parents = {"service": ("Services", "/services/"), "city": ("Service Areas", "/service-areas/"),
                   "guide": ("Guides", "/guides/")}
        if page.get("type") in parents:
            label, href = parents[page["type"]]
            crumbs.append({"label": label, "href": href})
        crumbs.append({"label": page.get("crumb", page.get("h1", page["title"])), "href": url})
        return crumbs

    def jsonld(self, page):
        b = self.site["business"]
        origin = b["origin"]
        url = origin + page["url"]
        org_id = origin + "/#organization"
        areas = [{"@type": "City", "name": "Dallas", "containedInPlace": {"@type": "State", "name": "Texas"}}] + [
            {"@type": "City", "name": c["name"], "containedInPlace": {"@type": "State", "name": "Texas"}}
            for c in self.site["cities"]
        ]
        org = {
            "@type": "Organization",
            "@id": org_id,
            "name": b["name"],
            "legalName": b["legal_name"],
            "url": origin + "/",
            "logo": origin + b["logo"],
            "telephone": b["phone_tel"],
            "description": b["description"],
            "areaServed": areas,
            "contactPoint": {
                "@type": "ContactPoint",
                "telephone": b["phone_tel"],
                "contactType": "customer service",
                "availableLanguage": ["English"],
                "hoursAvailable": {
                    "@type": "OpeningHoursSpecification",
                    "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                    "opens": "00:00",
                    "closes": "23:59",
                },
            },
        }
        same_as = [v for v in self.site["social"].values() if v]
        if same_as:
            org["sameAs"] = same_as
        graph = [org]
        if page["url"] == "/":
            graph.append({"@type": "WebSite", "@id": origin + "/#website", "url": origin + "/",
                          "name": b["name"], "publisher": {"@id": org_id}, "inLanguage": "en-US"})
        if page["url"] == "/404.html":
            return {"@context": "https://schema.org", "@graph": graph}
        image = origin + "/images/" + (page.get("hero") or {}).get("render_image", "pw-hero.jpg")
        webpage = {
            "@type": "WebPage",
            "@id": url + "#webpage",
            "url": url,
            "name": page["title"],
            "description": page["description"],
            "isPartOf": {"@type": "WebSite", "@id": origin + "/#website", "url": origin + "/", "name": b["name"]},
            "about": {"@id": org_id},
            "primaryImageOfPage": {"@type": "ImageObject", "url": image},
            "inLanguage": "en-US",
        }
        if page.get("type") == "contact":
            webpage["@type"] = "ContactPage"
        if page.get("type") == "about":
            webpage["@type"] = "AboutPage"
        graph.append(webpage)
        crumbs = page.get("breadcrumbs") or []
        if crumbs:
            graph.append({
                "@type": "BreadcrumbList",
                "@id": url + "#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": i + 1, "name": c["label"], "item": origin + c["href"]}
                    for i, c in enumerate(crumbs)
                ],
            })
            webpage["breadcrumb"] = {"@id": url + "#breadcrumb"}
        svc = page.get("schema_service")
        if svc:
            area = areas
            if page.get("type") == "city":
                area = {"@type": "City", "name": page["city_name"],
                        "containedInPlace": {"@type": "State", "name": "Texas"}}
            graph.append({
                "@type": "Service",
                "@id": url + "#service",
                "name": svc["name"],
                "serviceType": svc["type"],
                "description": svc.get("description", page["description"]),
                "provider": {"@id": org_id},
                "areaServed": area,
                "url": url,
                "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD",
                           "description": "Calling the line and being connected is free. The local company quotes its own price for the work."},
            })
        if page.get("type") == "guide":
            graph.append({
                "@type": "Article",
                "@id": url + "#article",
                "headline": page["h1"],
                "description": page["description"],
                "image": image,
                "datePublished": page.get("published", BUILD_DATE),
                "dateModified": page.get("modified", BUILD_DATE),
                "author": {"@id": org_id},
                "publisher": {"@id": org_id},
                "mainEntityOfPage": {"@id": url + "#webpage"},
                "inLanguage": "en-US",
            })
        faqs = page.get("faqs") or []
        if faqs:
            graph.append({
                "@type": "FAQPage",
                "@id": url + "#faq",
                "mainEntity": [
                    {"@type": "Question", "name": strip_tags(f["q"]),
                     "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"\s+", " ", strip_tags(f["a"]))}}
                    for f in faqs
                ],
            })
        return {"@context": "https://schema.org", "@graph": graph}

    def build(self):
        if self.out.exists():
            shutil.rmtree(self.out)
        shutil.copytree(STATIC, self.out)
        pages = self.load_pages()
        index = {p["url"]: p for p in pages}
        for page in pages:
            html_out = self.render(page, index)
            dest = out_path_for(page["url"], self.out)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(add_pictures(html_out))
        if WEBP_DIR.exists():
            shutil.copytree(WEBP_DIR, self.out / "images" / "w", dirs_exist_ok=True)
        self.write_sitemap(pages)
        self.write_robots()
        if self.write_docs:
            self.write_image_list()
        print(f"Built {len(pages)} pages into {self.out}")
        if self.missing_images:
            print(f"{len(self.missing_images)} images still to generate (docs/image-list.md)")

    def write_sitemap(self, pages):
        origin = self.site["business"]["origin"]
        urls = [p for p in pages if not p.get("noindex") and p["url"] != "/404.html"]
        lines = ['<?xml version="1.0" encoding="UTF-8"?>',
                 '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
        for p in sorted(urls, key=lambda p: (p["url"] != "/", p["url"])):
            lines.append(f"  <url><loc>{origin}{p['url']}</loc><lastmod>{BUILD_DATE}</lastmod></url>")
        lines.append("</urlset>")
        (self.out / "sitemap.xml").write_text("\n".join(lines) + "\n")

    def write_robots(self):
        origin = self.site["business"]["origin"]
        (self.out / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {origin}/sitemap.xml\n")

    def write_image_list(self):
        rows = sorted(self.missing_images.values(),
                      key=lambda e: (not e["size"].startswith("1920"), e["pages"][0], e["file"]))
        style = ("bright, clearly visible, Dallas-Fort Worth homes, driveways and storefronts, natural daylight, "
                 "no text, no logos, no watermarks, no recognizable faces, wide cinematic landscape shot, "
                 "subject positioned on right third of frame, well lit")
        out = [
            "# Images still needed (Artistly)",
            "",
            "Generated by build.py. Every image below already has its tag in the page source. Until the file",
            "exists in src/static/images/, the built page shows an existing photo in its place, so nothing",
            "ever looks broken. Save each new image under the exact File name and Size below in",
            "src/static/images/, run `python3 build.py`, and it replaces the stand-in automatically.",
            "",
            "Heroes (1920x1080) are listed first because they show on screen straight away.",
            "",
            f"Total: {len(rows)} images.",
            "",
        ]
        for n, e in enumerate(rows, 1):
            prompt = (e["desc"] or e["alt"]).rstrip(". ")
            out += [
                f"## {n}. {e['file']}",
                "",
                f"- **File name:** {e['file']}",
                f"- **Size:** {e['size']} px",
                f"- Page(s): {', '.join(e['pages'])}",
                f"- Alt text: {e['alt']}",
                "",
                f"Artistly prompt: {prompt}. Style: {style}.",
                "",
            ]
        (ROOT / "docs" / "image-list.md").write_text("\n".join(out))


# ---- speed fix (Oct 12 2026, same as the Orlando build): every photo also ships as small WebP
# copies, offered through <picture> + srcset so a phone downloads only the size it needs.
WEBP_WIDTHS = (480, 800, 1200, 1600, 1920)
WEBP_DIR = STATIC / "images" / "w"
_webp_cache = {}

def webp_srcset(file):
    from PIL import Image
    if not file or file in _webp_cache:
        return _webp_cache.get(file, "")
    src = STATIC / "images" / file
    if not src.exists() or src.suffix.lower() not in (".jpg", ".jpeg", ".png"):
        _webp_cache[file] = ""
        return ""
    WEBP_DIR.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as im:
        full_w, full_h = im.size
        widths = sorted({w for w in WEBP_WIDTHS if w < full_w} | {full_w})
        parts = []
        for w in widths:
            name = f"{src.stem}-{w}.webp"
            dest = WEBP_DIR / name
            if not dest.exists() or dest.stat().st_mtime < src.stat().st_mtime:
                h = round(full_h * w / full_w)
                im.convert("RGB").resize((w, h), Image.LANCZOS).save(dest, "WEBP", quality=66, method=6)
            parts.append(f"/images/w/{name} {w}w")
    _webp_cache[file] = ", ".join(parts)
    return _webp_cache[file]

_IMG_RE = re.compile(r'<img\b([^>]*?)\bsrc="/images/([^"/]+\.(?:jpe?g|png))"([^>]*)>', re.I)

def add_pictures(html):
    def swap(m):
        tag = m.group(0)
        srcset = webp_srcset(m.group(2))
        if not srcset:
            return tag
        if 'hero__img' in tag:
            sizes = "100vw"
        elif 'card' in m.group(1) + m.group(3) or 'loading="lazy"' in tag and 'width="1200" height="675"' in tag:
            sizes = "(max-width: 700px) 100vw, (max-width: 1100px) 50vw, 33vw"
        else:
            sizes = "(max-width: 860px) 100vw, 60vw"
        return f'<picture><source type="image/webp" srcset="{srcset}" sizes="{sizes}">{tag}</picture>'
    return _IMG_RE.sub(swap, html)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "dist"))
    args = ap.parse_args()
    out = Path(args.out).resolve()
    Builder(out, write_docs=(out == ROOT / "dist")).build()


if __name__ == "__main__":
    sys.exit(main())
