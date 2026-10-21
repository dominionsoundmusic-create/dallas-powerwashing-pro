# Prompt 3: Route matrix

| Route | Type | Source | Nav | Sitemap | Indexable | Status |
|---|---|---|---|---|---|---|
| / | home | src/pages/index.html | logo | yes | yes | rebuilt (existing URL) |
| /services/ | hub | services/index.html | yes | yes | yes | rebuilt |
| /pressure-washing/ /house-washing/ /roof-soft-wash/ /driveway-cleaning/ /power-washing/ /fence-cleaning/ /deck-cleaning/ | service | root pages, site.json services | Services menu | yes | yes | rebuilt; /house-washing/ NEW |
| /guides/ and 5 x /guides/<slug>/ | hub, guide | guides/ | Guides menu | yes | yes | NEW |
| /service-areas/ | hub | service-areas/index.html | yes | yes | yes | NEW |
| 11 x /<town>-pressure-washing/ | city | root pages, site.json cities | Service Areas menu | yes | yes | rebuilt (existing URLs) |
| /how-it-works/ | page | how-it-works.html | yes | yes | yes | NEW |
| /about/ /faq/ /contact/ | about, page, contact | root pages | yes | yes | yes | rebuilt |
| /privacy-policy.html /terms.html | legal | url override | footer | yes | yes | rebuilt (exact old URLs) |
| /404.html | page | 404.html | no | no | noindex | NEW |
| /contact/thanks/ | redirect | _redirects | no | no | 301 to /contact/ | retired (form removed) |
| /blog/* and old templated sub-pages | redirect | _redirects | no | no | 301 | kept from Sep 2026 |

Baseline: the old site had no build, typecheck or tests (hand-written HTML). Pre-existing issues: old brand name,
a contact form, 400 to 900 word pages, no FAQ schema on most pages, render-blocking CSS.
