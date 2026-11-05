# QA record (Dallas Playbook 2.0 rebuild, Nov 5 2026)

| Check | Result |
|---|---|
| `python3 build.py` | 31 HTML pages (30 plus noindex thanks) |
| `python3 scripts/check.py` | 0 errors, 3 warnings: Addison, Arlington and Carrollton are just under the 1,500 word soft target (1,478 to 1,492) |
| `python3 scripts/grep_check.py` | 0 hits: dashes, contractor voice, banned phrases, Yuma, Tucson, Phoenix, pool, Houston, Austin, San Antonio, Georgia, Dallas Metro, placeholders, old phone numbers |
| `python3 scripts/check_old_urls.py` | 59 old URLs, 0 would 404 (docs/qa-old-urls.md) |
| `python3 scripts/similarity.py --other az-model/dist` | same-type max: city 2.0%, service 0.5%, guide 0.1%, core 1.8%, legal 0.0%; mixed 2.1%. Against 20 Yuma pages: max 1.8%, 0 shared 8-word runs. Limit 15% (docs/qa-similarity.md) |
| `python3 scripts/keyword_plan.py` | 69 keywords: 66 assigned, 3 unused with reasons |
| `node scripts/responsive_check.js` | 132 page loads at 1440, 1024, 768, 390 (all pages) and 1920, 2560 (four-page sample): 0 problems (no sideways scroll, no broken images, no JS errors, hero edge to edge, under 720px, call button above fold, headline on left rail) |
| `node scripts/functional_check.js` | 13 of 13 pass |
| Repeated photos | no photo scene twice on any page (hero and card versions of a scene count as one) |
| Speed fix | CSS inlined, no stylesheet link, hero preloaded with WebP srcset and fetchpriority high, woff2 preloaded, GA4 delayed |
| Eyes on screenshots | home, driveway, Fort Worth, cost guide, contact at 1440; Fort Worth at 390: readable, no white on white, rail aligned, card rows centered, photos load after scrolling |

## Not tested here
- Netlify behavior: redirects, the form and the function were checked by script and file layout, not on Netlify.
- Google Analytics and Google Translate requests, because the sandbox blocks them. The ES cookie logic passed.
- The phone flow.
- 1920 and 2560 were tested on a sample, not all pages.

## For Maurice to decide
1. Is he happy with 30 pages, and with no third guide?
2. Confirm the logo: gold "DALLAS" over "Power Washing Pro".
3. Should an independent agent re-check the facts? (docs/fact-check.md)
4. Does the A2P registration need any exact wording from the old privacy page? Text consent wording was kept.
5. Add "Black-owned" to /about/ if he wants it.
