# Playbook 2.0, Prompts 1 to 3: fact brief, architecture, baseline and route plan (Oct 21 2026)

## Prompt 1: client fact brief (from INTAKE.md; INTAKE wins)

| Item | Value | Status |
|---|---|---|
| Official name | Yuma Pool Cleaning Pro, a d/b/a of Dominion Digital Group | Confirmed |
| What it is | A free phone line and website, not a pool company. An automated assistant answers, then transfers the caller to an independent, locally owned Yuma-area pool service company (or passes name, number, area and problem on for a call back). The company inspects, quotes, does the work and is paid by the customer. Companies may pay a referral fee | Confirmed |
| Primary category | Pool service referral line for Yuma and Yuma County | Confirmed |
| Services | Chosen from the keyword data (SERVICES.md). Not offered: building pools, fencing, landscaping, pest control, public or city pool information | Confirmed |
| Service area | Yuma, Fortuna Foothills, Somerton, San Luis, Wellton, Gadsden (Yuma County). Never outside Yuma County: no California towns, no Mexico, no other Arizona metros | Confirmed |
| Address | DO NOT DISPLAY | Confirmed (omitted) |
| Phone | (928) 615-5224, tel:+19286155224, only in src/data/site.json. Never 903-636-7511 | Confirmed |
| Email | UNKNOWN, not displayed | Missing, deferrable |
| Hours | Line answered 24/7 by an automated assistant | Confirmed |
| Year established, owner name | Not displayed | Confirmed (omitted) |
| Primary CTA | Call the number. Phone only: the old `yuma-pool-inquiry` Netlify form on /contact/ is retired | Confirmed |
| Secondary CTA | A real page (/how-it-works/ or a guide), never a form | Confirmed |
| Brand | Logo teal #14897a family and desert gold #f5c451; header in teal; one teal band and one gold band; mostly white sections; existing logo.svg and favicons kept | Confirmed |
| Top bar / footer | "John 3:16" left and the exact Duplantis quote; footer copyright "© 2026 Dominion Digital Group. All rights reserved." and the Dominion Web Design Pro credit | Confirmed |
| Language | EN / ES Google Translate toggle in the header, prominent | Confirmed |
| Social | Facebook https://www.facebook.com/yumapoolcleaningpro (live on main, kept); other slots empty and hidden | Confirmed |
| Analytics | GA4 G-STXQ0LYCST with the phone-tap event (live on main), now loaded with the delayed loader | Confirmed |
| Reviews, licenses, team, guarantees | None. Do not invent | Confirmed (none shown) |
| Domain | https://yumapoolcleaningpro.com on Netlify, production branch main (repo named arizona-pool-cleaning-pro) | Confirmed |
| Photos | img-01.jpg and 15 photos in images/pool/; new photos listed in docs/image-list.md | Confirmed |

Contradictions found on the live site (not resolved by guessing; dropped or re-verified):
- "175 days above 100 degrees" and "hottest city in Arizona": NWS Phoenix normals give about 118 days a year at
  or above 100 F at Yuma (1991 to 2020), and Visit Yuma itself does not call Yuma the hottest city. Dropped;
  pages use the NWS figures (docs/research/climate-seasons.md).
- "Chemicals are included in the monthly price", "one flat number", "same technician every week", "diagnoses
  and fixes it on site", "30 to 50 percent more chlorine than Phoenix", "population nearly doubles": unsourced
  or banned by INTAKE.md. Dropped. The winter visitor figure now comes from the 2017 to 2018 Visit Yuma /
  Arizona Office of Tourism study.
- The old about page called the line "a residential pool service company" with "the same technician": false.
  Rewritten from INTAKE.md.
- The old footer said "© 2026 Yuma Pool Cleaning Pro"; INTAKE.md says Dominion Digital Group. INTAKE wins.

Launch blockers needing Maurice: none. Deferred: an email address, more social profiles, new Artistly photos
(docs/image-list.md).

## Prompt 2: architecture

The playbook targets a GHL AI Studio SSR project. This repo is a static site on Netlify, so the SSR rules map
to: every page is a complete HTML file rendered at build time (title, meta, canonical, Open Graph, one JSON-LD
graph, headings and body copy are all in the raw HTML; no client rendering). The build system is copied from
dominionsoundmusic-create/tucson-pool-cleaning-pro (main, Oct 20 2026), words not copied:

- `build.py` (Python 3, Jinja2, PyYAML, Pillow): pages in `src/pages/*.html` with YAML front matter,
  templates in `src/templates/` (layouts/base.html, partials for header, hero, FAQ, call band, footer, icons;
  macros.html with img, service/guide cards, area pills, related links, call box, how-it-works strip,
  disclosure, license check, sources and a click-to-play video macro), shared data in `src/data/site.json`,
  static files in `src/static/` (CSS, JS, woff2 font, images, favicons, _redirects). Output: `dist/`
  (committed; Netlify publishes it, no build command, netlify.toml `publish = "dist"`).
- Speed: CSS inlined in a `<style>` block, hero preloaded with fetchpriority high and WebP srcset
  480/800/1200/1600/1920, self-hosted Inter woff2, GA4 loaded on first scroll/click/keypress/touch or 3.5 s
  after load, YouTube click-to-play macro (no video on the site yet).
- Routing: folder URLs `/name/` from `src/pages/name.html`; flat live URLs keep their path with `url:` in front
  matter (/pool-service, /pool-cleaning, /privacy-policy.html, /terms.html). 404: dist/404.html (Netlify serves it).
- Checks: scripts/check.py (rules + SEO + links + images), similarity.py (Jaccard, Yuma vs Yuma, Tucson and
  Phoenix), check_old_urls.py, grep_check.py, keyword_plan.py, responsive_check.js, functional_check.js.

## Prompt 3: baseline and route matrix

Baseline: main is hand-written static HTML (8 page files), no build or tests; its one form (`yuma-pool-inquiry`)
is retired. The old site is preserved in docs/old-site/ (plus retired-urls.txt: 88 page files main deleted in
Sep 2026, each checked with and without .html).

| Route | Source | Type | Nav | Sitemap | Index | Status |
|---|---|---|---|---|---|---|
| / | src/pages/index.html | home | logo | yes | yes | live URL, rebuilt |
| /services/ | services.html | page | Services | yes | yes | new |
| /service-areas/ | service-areas.html | page | Service Areas | yes | yes | new |
| /how-it-works/ | how-it-works.html | page | How It Works | yes | yes | new |
| /about/ | about.html | about | About | yes | yes | live URL, rebuilt |
| /faq/ | faq.html | page | FAQ | yes | yes | live URL, rebuilt |
| /contact/ | contact.html | contact | Contact | yes | yes | live URL, rebuilt (phone page) |
| /pool-service (+ .html) | pool-service.html, url: | service | Services menu | yes | yes | live URL, rebuilt |
| /pool-cleaning (+ .html) | pool-cleaning.html, url: | service | Services menu | yes | yes | live URL, rebuilt |
| /pool-repair/ | pool-repair.html | service | Services menu | yes | yes | new |
| /pool-pump-repair/ | pool-pump-repair.html | service | Services menu | yes | yes | new |
| /pool-equipment-repair/ | pool-equipment-repair.html | service | Services menu | yes | yes | new (old 301 rule removed) |
| /green-pool-cleanup/ | green-pool-cleanup.html | service | Services menu | yes | yes | new |
| /pool-tile-cleaning/ | pool-tile-cleaning.html | service | Services menu | yes | yes | new |
| /pool-maintenance-cost/ | pool-maintenance-cost.html | guide | Guides menu | yes | yes | new |
| /yuma-pool-maintenance-schedule/ | yuma-pool-maintenance-schedule.html | guide | Guides menu | yes | yes | new |
| /my-pool-is-green/ | my-pool-is-green.html | guide | Guides menu | yes | yes | new |
| /is-a-pool-service-worth-it/ | is-a-pool-service-worth-it.html | guide | Guides menu | yes | yes | new |
| /privacy-policy.html | privacy-policy.html, url: | legal | footer | yes | yes | live URL, rebuilt |
| /terms.html | terms.html, url: | legal | footer | yes | yes | live URL, rebuilt |
| /404.html | 404.html | page | no | no | noindex | new |

Plan: Prompts 4 to 6 (site.json, brand CSS, nav/header/footer) are done with the build-system port; Prompts 7
to 12 are written page by page by separate writer agents from docs/WRITING-GUIDE.md and docs/research/; 13 to 15
(phone page, social, media) follow; 16 to 20 are the SEO, remnant, responsive, functional and final QA passes,
recorded in docs/playbook/04-20-build-qa-handoff.md and docs/qa.md.
