# Decisions log: Dallas Power Washing Pro rebuild (Oct 21 2026)

Maurice was not watching this run, so every judgment call is written down here.

## Brand and identity
1. **Name:** "Dallas Power Washing Pro" everywhere, replacing "Dallas Metro Power Washing Pro", to match the
   domain (same approach as the Dallas HVAC and roofing renames). Per INTAKE.md.
2. **Logo:** kept the mark, colors and layout of images/logo.svg. Removed only the word "METRO" from the small
   amber top line, so the wordmark now reads DALLAS / PowerWashingPro. Title and aria-label updated. Favicons
   (favicon.svg, favicon.ico, apple-touch-icon.png) unchanged.
3. **Header color:** deep blue #163a5f built from the logo slate (#2a313e) and sky blue (#38bdf8). The quote bar
   above it uses the logo slate. Bands: sky blue (#38bdf8) and amber (#f0a500), each used occasionally.
4. **Top bar:** "John 3:16" at the left and the Jesse Duplantis line exactly as INTAKE.md gives it, credited
   "— Jesse Duplantis". That attribution dash is the only dash in visible copy, and scripts/check.py allows
   only that exact string.

## Architecture
5. **Build system copied from houston-powerwashing-pro (branch build):** build.py (Jinja2 + YAML front
   matter), src/data/site.json, src/templates, macros, CSS, JS, scripts/check.py, scripts/similarity.py and the
   docs set. No words were copied.
6. **URLs stay at the live paths.** The Houston build put services under /services/<slug>/; this build keeps
   Dallas's existing root paths (/pressure-washing/, /fort-worth-pressure-washing/ ...). build.py was given a
   `url:` front matter override so /privacy-policy.html and /terms.html keep their exact .html URLs.
7. **Speed fix added on top of the Houston system** (CLAUDE.md requires it; Houston did not yet have all of
   it): site CSS is inlined in a <style> block (no render-blocking stylesheet), GA4 G-37W4N8XFL8 loads only on
   first scroll/click/keypress/touch or 3.5 s after load with phone-tap tracking kept, YouTube embeds are
   click-to-play (macro `m.video`, none used yet because no video exists), WebP 480/800/1200/1600/1920
   srcsets, preloaded hero with fetchpriority high, self-hosted Inter woff2.
8. **netlify.toml** sets `publish = "dist"` with no build command. When `build` is merged, Netlify will serve
   the committed dist/ folder. The old root-level HTML moved to docs/old-site/ (research only, not published).

## Lead capture
9. **Phone only.** The old Netlify form `dallas-powerwashing-contact` is retired. /contact/ is a phone page.
   /contact/thanks/ (the old form thank-you page) is 301'd to /contact/. check.py fails the build if any
   <form> appears.

## Which service lives on which existing path
10. /pressure-washing/ = **Residential Pressure Washing** (hard surfaces and the whole outside of a home). It
    was a house washing page before; the path name now matches its topic.
11. /house-washing/ = **House Washing and Soft Washing**, a NEW page. "house washing services near me" (1,300)
    and the soft wash questions (170, 140) justify its own page, and the old house-washing content moved here.
12. /power-washing/ = **Commercial Power Washing**, as it is today (the live page was already commercial).
    The home page owns "power washing dallas", so /power-washing/ targets "commercial pressure washing dallas"
    and the commercial "near me" term, avoiding two pages chasing the same term.
13. /roof-soft-wash/ = roof cleaning, /driveway-cleaning/ = driveway and concrete, /fence-cleaning/ and
    /deck-cleaning/ unchanged in topic.

## Pages added
14. /service-areas/, /how-it-works/ and /guides/ (hub) are new. The five guides live under /guides/<slug>/.
15. No new town pages beyond the eleven live ones: the seven with 10+ searches get full pages, and Addison,
    Carrollton, Irving and Flower Mound stay as shorter honest pages (CLAUDE.md).

## Redirects
16. Kept every existing _redirects rule. The service wildcards (/deck-cleaning/* etc.) only catch the retired
    templated sub-pages; Netlify never applies a non-forced rule where a real file exists, so they do not
    shadow the hub pages. check.py was adjusted to flag a wildcard only if a real page sits *below* its base.
    `_redirects` is copied into dist/ by the build (it lives in src/static/).

## Content rules applied
17. **FAQ page:** CLAUDE.md caps FAQs at 3 to 6 per page, so /faq/ carries 6 FAQPage questions in the shared
    "Common questions" block, and the rest of its questions are written as ordinary headed sections (not
    schema), so the page stays useful without breaking the 3 to 6 rule.
18. **Water and runoff rules:** only rules found on a city's own site or its adopted plan are stated, with the
    plan's date. Where a city's page says nothing about pressure washing, the page says so and points to the
    city rather than guessing.
19. **Sales tax:** the Texas Comptroller's publication 94-111 says pressure washing buildings, sidewalks and
    parking lots is taxable as building or grounds cleaning, so the license guide mentions that a company may
    add sales tax. Stated as the Comptroller's guidance, not legal advice.
20. **No company named anywhere.** Brand names that appear are product makers whose care instructions are
    cited (Trex, the Asphalt Roofing Manufacturers Association, the Brick Industry Association,
    Sherwin-Williams) and price-guide publishers (Angi, HomeAdvisor, Fixr, Thumbtack, Housecall Pro).
