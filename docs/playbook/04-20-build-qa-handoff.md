# Playbook 2.0, Prompts 4 to 20: build, QA and handoff (Oct 21 2026)

| Prompt | What was done | Result |
|---|---|---|
| 4 Business data | src/data/site.json: name, d/b/a, phone (one place), 24/7 hours, no email, no address, CTAs, origin, Facebook, GA4 G-STXQ0LYCST, disclosure text, services, guides, areas | Done. Old-business check: no Tucson, Phoenix or 903 values left (grep_check 0 hits) |
| 5 Brand | site.css tokens: teal header #0d6b60, deep teal-navy headings and call band, desert gold buttons, teal band then gold band, white sections; logo.svg and favicons kept; apple-touch-icon rendered | Done; contrast: white on #0d6b60 and dark text on #f5c451 both pass AA |
| 6 Navigation | Header menu from site.json (Services and Guides submenus, Service Areas, How It Works, About, FAQ, Contact), EN/ES toggle and call button in the header, quote bar, footer rows left to right | Done; functional_check 13/13 |
| 7 Home | / targets "pool service yuma az", "yuma pool service", "pool service yuma" | Done (photo hero; no approved video exists) |
| 8 Services overview | /services/ | Done |
| 9 Service pages | /pool-service, /pool-cleaning, /pool-repair/, /pool-pump-repair/, /pool-equipment-repair/, /green-pool-cleanup/, /pool-tile-cleaning/ | Done, one writer per pair, each with its own design treatment |
| 10 Service areas overview | /service-areas/ with a section per place (anchors used by menu and footer) | Done |
| 11 Area pages | None: no town reaches 10 searches a month for a pool service keyword (SERVICES.md) | Intentional skip, recorded |
| 12 About, FAQ, legal | /about/, /faq/, /privacy-policy.html, /terms.html, /404.html | Done |
| 13 Contact | /contact/ is a phone page; the yuma-pool-inquiry form is retired; check.py fails any form | Done; no form exists to test |
| 14 Reviews and social | No reviews exist (none invented). Facebook icon in top bar and footer; other slots hidden until URLs are added | Done |
| 15 Media | Every page: hero plus at least two in-body photos from the existing set, WebP srcset, lazy below the fold, eager hero; 18 planned Artistly heroes in docs/image-list.md, each shown with an existing fallback until it arrives | Done; 18 images pending from Maurice |
| 16 SEO | Titles, descriptions, canonicals, OG, single JSON-LD graph, sitemap, robots, 404 noindex | Pass on all 21 routes (docs/qa.md) |
| 17 Remnant sweep | grep_check and check.py (old phone numbers, other cities, banned phrases, lorem, TODO, empty hrefs, duplicate ids, duplicate titles and descriptions, missing images) | 0 hits |
| 18 Responsive and accessibility | responsive_check.js at 1440/1024/768/390 plus 1920/2560; skip link, focus styles, alt text, heading order, reduced motion | 0 problems |
| 19 Functional | functional_check.js | 13/13 pass |
| 20 Final | build, check, grep, old URLs, similarity, keyword plan, browser checks, independent fact-check | All pass; see docs/qa.md and docs/fact-check.md |

Readiness: ready for Maurice's review on the Netlify deploy preview. Not deployed, not merged.

Remaining before launch (Maurice): generate the 18 Artistly images (docs/image-list.md), save them under the
exact file names in src/static/images/, run `python3 build.py`, review the deploy preview, then merge.
Optional: an email address, more social profiles, a governing-law clause for the terms.
