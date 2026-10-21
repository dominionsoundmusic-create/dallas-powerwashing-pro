# QA record: Dallas Power Washing Pro rebuild (Oct 21 2026)

All results below were produced by actually running the scripts on the built dist/ folder.

## Build and rule checks
- `python3 build.py`: 34 pages built, 31 planned images listed in docs/image-list.md.
- `python3 scripts/check.py`: **0 errors**, 1 warning (Carrollton page is 992 words including template; it is one of the
  four "shorter honest" town pages CLAUDE.md asks for, so it was left short rather than padded).
  check.py enforces: banned phrases and WORDS TO AVOID, no em/en dashes except "— Jesse Duplantis", no places or phone
  numbers outside DFW, the dwdp:handwritten 2026-10-21 comment in the first 4KB, the John 3:16 + Duplantis bar, the
  referral disclosure, inlined CSS (no stylesheet link), delayed GA4, no iframes, no forms, no photo used twice on a
  page, a hero plus at least 2 in-body images, one H1, unique titles/descriptions, canonicals, sitemap, a single valid
  JSON-LD graph, visible FAQ count = FAQPage count (3 to 6), internal links, image files and _redirects targets.

## Grep list from CLAUDE.md (run on dist/*.html)
we clean 0 · our crew 0 · our team 0 · our technicians 0 · licensed and insured 0 · free estimate 0 · same-day 0 ·
500+ 0 · Dallas Metro 0 · Houston 0 · Katy 0 · Harris County 0 · Pflugerville 0 · Georgia 0 · Virginia 0 · (832) 0 ·
(903) 0 · 903-636 0. Dashes: the only dash in any page is "— Jesse Duplantis" (34 pages, 34 hits).

## Old URLs (`python3 scripts/check_old_urls.py`)
```
OK    /  (page)
OK    /about  (page)
OK    /about/  (page)
OK    /addison-pressure-washing  (page)
OK    /addison-pressure-washing/  (page)
OK    /allen-pressure-washing  (page)
OK    /allen-pressure-washing/  (page)
OK    /arlington-pressure-washing  (page)
OK    /arlington-pressure-washing/  (page)
OK    /blog  -> 301 /
OK    /blog/best-time-of-year-to-pressure-wash-in-dallas-1786192225249  -> 301 /pressure-washing/
OK    /blog/best-time-of-year-to-pressure-wash-in-dallas-1786192225249.html  -> 301 /pressure-washing/
OK    /blog/how-clean-exterior-surfaces-prevent-costly-repairs-1786278748566  -> 301 /pressure-washing/
OK    /blog/how-clean-exterior-surfaces-prevent-costly-repairs-1786278748566.html  -> 301 /pressure-washing/
OK    /blog/how-much-does-pressure-washing-cost-in-dallas-1785937612576  -> 301 /pressure-washing/
OK    /blog/how-much-does-pressure-washing-cost-in-dallas-1785937612576.html  -> 301 /pressure-washing/
OK    /blog/how-much-does-pressure-washing-cost-in-dallas-1786023941108  -> 301 /pressure-washing/
OK    /blog/how-much-does-pressure-washing-cost-in-dallas-1786023941108.html  -> 301 /pressure-washing/
OK    /blog/how-much-does-pressure-washing-cost-in-dallas-1786106675424  -> 301 /pressure-washing/
OK    /blog/how-much-does-pressure-washing-cost-in-dallas-1786106675424.html  -> 301 /pressure-washing/
OK    /blog/how-often-should-you-pressure-wash-your-house-1786970483743  -> 301 /power-washing/
OK    /blog/how-often-should-you-pressure-wash-your-house-1786970483743.html  -> 301 /power-washing/
OK    /blog/how-power-washing-protects-your-home-value-1785707535398  -> 301 /power-washing/
OK    /blog/how-power-washing-protects-your-home-value-1785707535398.html  -> 301 /power-washing/
OK    /blog/pressure-washing-vs-soft-washing-what-is-the-difference-1786366105614  -> 301 /roof-soft-wash/
OK    /blog/pressure-washing-vs-soft-washing-what-is-the-difference-1786366105614.html  -> 301 /roof-soft-wash/
OK    /blog/signs-your-driveway-needs-professional-cleaning-1785851484387  -> 301 /driveway-cleaning/
OK    /blog/signs-your-driveway-needs-professional-cleaning-1785851484387.html  -> 301 /driveway-cleaning/
OK    /blog/why-diy-pressure-washing-damages-siding-1786452434928  -> 301 /power-washing/
OK    /blog/why-diy-pressure-washing-damages-siding-1786452434928.html  -> 301 /power-washing/
OK    /carrollton-pressure-washing  (page)
OK    /carrollton-pressure-washing/  (page)
OK    /contact  (page)
OK    /contact/  (page)
OK    /contact/thanks  -> 301 /contact/
OK    /contact/thanks/  -> 301 /contact/
OK    /deck-cleaning  (page)
OK    /deck-cleaning/  (page)
OK    /denton-pressure-washing  (page)
OK    /denton-pressure-washing/  (page)
OK    /driveway-cleaning  (page)
OK    /driveway-cleaning/  (page)
OK    /faq  (page)
OK    /faq/  (page)
OK    /fence-cleaning  (page)
OK    /fence-cleaning/  (page)
OK    /flower-mound-pressure-washing  (page)
OK    /flower-mound-pressure-washing/  (page)
OK    /fort-worth-pressure-washing  (page)
OK    /fort-worth-pressure-washing/  (page)
OK    /frisco-pressure-washing  (page)
OK    /frisco-pressure-washing/  (page)
OK    /irving-pressure-washing  (page)
OK    /irving-pressure-washing/  (page)
OK    /mckinney-pressure-washing  (page)
OK    /mckinney-pressure-washing/  (page)
OK    /plano-pressure-washing  (page)
OK    /plano-pressure-washing/  (page)
OK    /power-washing  (page)
OK    /power-washing/  (page)
OK    /pressure-washing  (page)
OK    /pressure-washing/  (page)
OK    /privacy-policy  (page)
OK    /privacy-policy.html  (page)
OK    /roof-soft-wash  (page)
OK    /roof-soft-wash/  (page)
OK    /services  (page)
OK    /services/  (page)
OK    /terms  (page)
OK    /terms.html  (page)

70 old URLs checked, 0 failing
```

## Duplication (`python3 scripts/similarity.py`, Jaccard on 5-word shingles, limit 15%)
```
about pages (1): no pairs
city pages (11), 55 pairs: highest 6.2% (/carrollton-pressure-washing/ vs /irving-pressure-washing/), lowest 0.7%
contact pages (1): no pairs
guide pages (5), 10 pairs: highest 2.0% (/guides/commercial-pressure-washing-cost/ vs /guides/pressure-washing-license-texas/), lowest 0.2%
home pages (1): no pairs
hub pages (3), 3 pairs: highest 1.1% (/guides/ vs /services/), lowest 0.1%
legal pages (2), 1 pairs: highest 1.3% (/privacy-policy.html vs /terms.html), lowest 1.3%
page pages (2), 1 pairs: highest 5.5% (/faq/ vs /how-it-works/), lowest 5.5%
service pages (7), 21 pairs: highest 1.6% (/deck-cleaning/ vs /fence-cleaning/), lowest 0.3%
Dallas vs Houston (33 x 36 pages): highest 12.6% (/privacy-policy.html vs houston/privacy-policy/)

0 pairs above 15%
```

The terms page first scored 24.7% against Houston's terms (both descended from the same template). It was rewritten
from scratch and now scores under 12.6%, the highest cross-site pair being privacy policy vs privacy policy.

## Browser QA (`node scripts/qa.js`, Chromium via Playwright)
Every sitemap route plus /404.html at 1440, 1024, 768 and 390 px: HTTP 200, no horizontal overflow, no console
errors, exactly one visible H1, hero loaded, every image loaded after scrolling, no form, tap-to-call header link
present. Hero checks at 1440, 1920 and 2560 on / and /fort-worth-pressure-washing/: hero 700 px tall, H1 starts on
the same left rail as the logo, call button above the fold. Interaction: mobile menu, submenu, Escape, FAQ
accordion, ES toggle sets the googtrans cookie, GA4 not requested before interaction and loaded after the first
scroll.
```
INFO hero / @1440: height 700px, h1 left 79px, logo left 79px, call button bottom 615px
INFO hero / @1920: height 700px, h1 left 106px, logo left 106px, call button bottom 615px
INFO hero / @2560: height 700px, h1 left 140px, logo left 140px, call button bottom 615px
INFO hero /fort-worth-pressure-washing/ @1440: height 700px, h1 left 79px, logo left 79px, call button bottom 649px
INFO hero /fort-worth-pressure-washing/ @1920: height 700px, h1 left 106px, logo left 106px, call button bottom 649px
INFO hero /fort-worth-pressure-washing/ @2560: height 700px, h1 left 140px, logo left 140px, call button bottom 649px
INFO invalid nested route status: 404 (Netlify serves dist/404.html for this)

34 routes x 4 widths checked, 0 failures
```

Not verified here: live Netlify behavior (redirect execution, Pretty URLs), real phone routing, Google Translate output (blocked in this sandbox), and GA4 data arriving in the property.
