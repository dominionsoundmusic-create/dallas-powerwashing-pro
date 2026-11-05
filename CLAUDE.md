# Dallas Power Washing Pro (dallaspowerwashingpro.com): instructions for Claude Code

This repo is a Playbook 2.0 rebuild of a live, indexed lead site owned by Maurice Johnson. The method, hard
rules and design rules came from the finished Yuma rebuild, translated to power washing and Dallas-Fort Worth.

## Source files
- INTAKE.md: the facts. It wins over anything else. UNKNOWN means leave it off the site.
- PLAYBOOK.md: the playbook. SERVICES.md and docs/keyword-plan.md: pages and keywords.
- docs/research/facts.md: facts read from sources, with URLs and a list of what could not be opened.
- docs/decisions.md, docs/qa.md, docs/fact-check.md: what was decided and tested.

## Git
Work on `build`. Do NOT push, merge or deploy unless Maurice says so. He pushes once at the end of a session:
each push starts a Netlify deploy and costs money.

## Hard rules for every page
1. Never contractor voice ("we wash", "our crews"). The line does no work.
2. Never invent licenses, insurance, reviews, ratings, prices, job counts, response times or awards. No aggregateRating.
3. Never name a washing company.
4. Dallas-Fort Worth places only.
5. No em or en dashes in visible copy except the Duplantis credit (drawn by CSS). No eyebrow labels. American spelling.
6. No prices as the line's prices. Cost figures only from published sources, named, with a note that real quotes vary.
7. Every page except privacy, terms, 404 and thanks has 3 to 6 FAQs, shown and in FAQPage JSON-LD, and a sources list.
8. Every content page has a hero plus at least two in-body images. One photo may repeat across pages, never twice on a page.
9. Research first. If a fact can not be verified, leave it out. Do not state a current drought stage.
10. Jaccard on 5-word shingles between same-type pages and against the Yuma site stays under 15%.
11. The phone number lives only in src/data/site.json.
12. Keep every old URL working: same path or 301.
13. Every page carries `dwdp:handwritten 2026-11-05` in the first 4KB.

## Design
Real color header, EN/ES toggle, phone visible, 3px gold strip under the menu. Full-width hero with a dark fade,
headline on the left rail. Text, photos and cards run full width on the rail. White sections broken by occasional
bold blue and gold bands. No white on white, no pale section tints. Card rows 3/2/1 with a short last row centered,
homepage row of four service cards with photos. Footer lists are rows of buttons.

## Speed (automatic)
WebP srcset 480 to 1920, preloaded hero with fetchpriority high, self-hosted woff2, CSS inlined in a style block,
GA4 loaded on first interaction or after 3.5 seconds, click-to-play video macro.

## Before you finish
`python3 build.py`, then check.py, grep_check.py, check_old_urls.py, similarity.py and, with dist served on port
8765, responsive_check.js and functional_check.js. Look at screenshots. Fact-check against sources and record it in
docs/fact-check.md. Never call anything fact-checked unless it was.
