# SERVICES.md: every page on dallaspowerwashingpro.com (Playbook 2.0 rebuild, Oct 21 2026)

Keyword data: keywords/Dallas-Power-Washing-Keywords.xlsx (Ubersuggest, US, Oct 21 2026). Volume = searches a
month, SD = SEO difficulty. Full assignment of every 10+ keyword: docs/keyword-plan.md.
Every URL that is live on `main` keeps its path. New pages are marked NEW.

## Core pages

| Page | URL | Target keyword | Vol | SD |
|---|---|---|---:|---:|
| Home | / | power washing dallas / pressure washing in dallas | 720 / 720 | 20 / 19 |
| (home, also) | / | pressure washing dallas / pressure washing dallas texas | 590 / 590 | 21 / 23 |
| Services overview | /services/ | pressure washing services dallas (0, brand navigation) | 0 | 4 |
| Service areas overview NEW | /service-areas/ | pressure washing places (supporting) | 10 | 33 |
| Guides hub NEW | /guides/ | (navigation hub for the five guides) | - | - |
| How it works NEW | /how-it-works/ | who does pressure washing in my area (supporting) | 30 | 19 |
| About | /about/ | brand page | - | - |
| FAQ | /faq/ | brand page | - | - |
| Contact (phone page) | /contact/ | brand page | - | - |
| Privacy | /privacy-policy.html | - | - | - |
| Terms | /terms.html | - | - | - |
| 404 | /404.html | - | - | - |

## Service pages (Prompt 9 build order)

Which existing path each service lives on (decision recorded in docs/decisions.md):

| # | Service | URL | Target keyword | Vol | SD | Main supporting |
|---|---|---|---|---:|---:|---|
| 1 | Residential pressure washing | /pressure-washing/ | pressure washing needed near me (no local residential term in the pull) | 50 | 32 | pressure washing description 70, dangers of pressure washing 10 |
| 2 | House washing and soft washing NEW | /house-washing/ | house washing dallas | 10 | 19 | house washing services near me 1,300; soft pressure washing near me 170; what is soft wash pressure washing 140 |
| 3 | Roof cleaning and roof soft washing | /roof-soft-wash/ | roof cleaning dallas | 30 | 12 | roof cleaning how much 10, how often roof cleaning 10 |
| 4 | Driveway and concrete cleaning | /driveway-cleaning/ | driveway cleaning dallas | 10 | 13 | driveway dallas 30, how often pressure wash driveway 20 |
| 5 | Commercial power washing | /power-washing/ | commercial pressure washing dallas | 10 | 15 | commercial pressure washing companies near me 170 |
| 6 | Fence cleaning | /fence-cleaning/ | (no 10+ row; kept as a live indexed page) | 0 | - | how often pressure wash fence 0 |
| 7 | Deck and patio cleaning | /deck-cleaning/ | (no 10+ row; kept as a live indexed page) | 0 | - | how often to pressure wash a deck 0 |

## Guide pages (Prompt 9, after services)

| # | Guide | URL | Target keyword | Vol | SD |
|---|---|---|---|---:|---:|
| 1 | What pressure washing costs in DFW | /guides/pressure-washing-cost/ | how much does pressure washing cost | 1,300 | 30 |
| 2 | How often to pressure wash a house in North Texas | /guides/how-often-pressure-wash-house/ | how often pressure wash house | 390 | 31 |
| 3 | Power washing vs pressure washing (vs soft washing) | /guides/power-washing-vs-pressure-washing/ | what is the difference between power washing and pressure washing | 90 | 23 |
| 4 | What commercial pressure washing costs | /guides/commercial-pressure-washing-cost/ | commercial pressure washing rates | 260 | 31 |
| 5 | Do you need a license to pressure wash in Texas? | /guides/pressure-washing-license-texas/ | do you need a license to pressure wash in texas | 10 | 5 |

Cost guide supporting: per square foot (40 + 40), going rate 30, house washing cost 170, what is a good price 10,
how much is a pressure washing job 10, how much is house washing 10. Commercial guide supporting: how much does
commercial pressure washing cost 30, commercial pressure washing price list 20.

## Town pages (Prompt 11 build order)

Maurice's rule: any town with 10+ searches a month gets its own page. Checked in the data:

| # | Town | URL | Keywords in the data (vol / SD) | Page type |
|---|---|---|---|---|
| 1 | Fort Worth | /fort-worth-pressure-washing/ | pressure washing fort worth 260 / 20 | full town page |
| 2 | Frisco | /frisco-pressure-washing/ | pressure washing frisco 170 / 14 | full town page |
| 3 | Denton | /denton-pressure-washing/ | pressure washing denton 170 / 21; denton pressure washing 10 / 26 | full town page |
| 4 | Plano | /plano-pressure-washing/ | pressure washing plano 110 / 17; power washing plano 50 / 13 | full town page |
| 5 | Arlington | /arlington-pressure-washing/ | pressure washing arlington tx 110 / 14; pressure washing arlington 90 / 25 | full town page |
| 6 | McKinney | /mckinney-pressure-washing/ | mckinney pressure washing 70 / 21; pressure washing mckinney 30 / 16 | full town page |
| 7 | Allen | /allen-pressure-washing/ | pressure washing allen tx 40 / 12; allen pressure washing 30 / 18 | full town page |
| 8 | Irving | /irving-pressure-washing/ | none in this pull | shorter honest page (live URL kept) |
| 9 | Carrollton | /carrollton-pressure-washing/ | none in this pull | shorter honest page (live URL kept) |
| 10 | Addison | /addison-pressure-washing/ | none in this pull | shorter honest page (live URL kept) |
| 11 | Flower Mound | /flower-mound-pressure-washing/ | pressure washing flower mound 0 / 4 | shorter honest page (live URL kept) |

Rejected towns from the data (outside DFW): Friendswood, Deer Park, Fulshear, Katy, League City (Houston area),
Pflugerville (Austin area), El Paso, Dallas GA, Arlington VA, Flowery Branch GA, York PA, Mount Vernon.

## Old URL map

Every URL in main's sitemap.xml and every page file on main resolves on the new build (scripts/check_old_urls.py):

- Same path, rebuilt: /, /about/, /contact/, /faq/, /services/, /pressure-washing/, /power-washing/,
  /driveway-cleaning/, /fence-cleaning/, /deck-cleaning/, /roof-soft-wash/, /privacy-policy.html, /terms.html and
  all eleven /<town>-pressure-washing/ pages.
- 301: /contact/thanks/ to /contact/ (the contact form is retired; the site is phone only).
- Kept: every Sep 2026 rule for retired templated city pages (/<service>/* to the service hub) and the retired
  blog posts (/blog/... to the closest page).
