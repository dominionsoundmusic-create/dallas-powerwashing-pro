# Fact-check record: dallaspowerwashingpro.com (Oct 21 2026)

## Status: NOT an independent fact-check

CLAUDE.md asks for the fact-check to be done by separate sub-agents that did not write the pages. **That was not
possible in this run.** The session had no tool for starting a sub-agent. So the check below was done by the same
agent that wrote the pages, as a separate verification pass. It should not be described as an independent
fact-check. **Before merging, have a fresh Claude Code session (one that did not write these pages) re-check every
claim against the sources listed on each page.**

## What the verification pass did
1. Every factual claim was written from a source fetched during this session, and every page lists its sources in
   its own Sources row (src/data/site.json "sources" registry, 54 entries).
2. Every number on the site (populations, enrollments, acreage, hail counts, temperatures, hours below freezing,
   rainfall, permit fees, fines, price ranges, dates of plans and guides) was listed with a grep and compared
   against the fetched source text. All matched after the fixes below.
3. Every quotation in quote marks was compared with the source wording.
4. Sentences that made claims no source supported were cut or softened.

## Errors found and fixed
| Page | Problem | Fix |
|---|---|---|
| /fort-worth-pressure-washing/ | Said "fourteen historic districts ... plus the Stockyards", double-counting (the city lists 13 plus the Stockyards) | "thirteen neighborhood historic districts ... plus the innermost Stockyards district" |
| /fort-worth-pressure-washing/ | Named "Ryan Place" as a neighbor of Mistletoe Heights and "early-1900s bungalows near the Near Southside" (not in the city source) | Removed |
| /index.html, FAQ | "Dallas and Fort Worth both treat dirty wash water in the storm drain as a violation" overstated Dallas, whose page addresses businesses and soapy water | Reworded to what each city actually says |
| /roof-soft-wash/ | Described how crews reach the roof (no source) | Removed |
| /fence-cleaning/ | Gave a picket thickness (no source) | Removed |
| /deck-cleaning/ | Cited a radio host's site not in the sources list | Replaced with the Family Handyman source already cited |
| /guides/pressure-washing-cost/ | Described Fixr's method of building estimates (not verified) | Replaced with the update dates each guide shows |
| /guides/power-washing-vs-pressure-washing/ | Claimed a history of how soft washing "grew" (no source) | Reworded |
| /guides/pressure-washing-license-texas/ | "Texas does not have a general contractor license" (not in the fetched sources) | Now says TDLR's list has no general contractor or pressure washing program |
| /plano-, /frisco-, /allen-, /denton-, /addison-, /flower-mound-, /arlington-, /carrollton- | Generalizations about housing (fences "on their third replacement", "full of brick homes", "many apartments", "larger lots", "one of the few three-county cities") | Softened or replaced with sourced facts |
| home, town pages | Headings and lines that implied call-volume data the line does not publish ("Most calls are...", "callers ask about") | Reworded |
| /driveway-cleaning/ | Technical detail about etching cement paste | Simplified to "can etch the surface" |

## Claims kept as general knowledge (no single cited source)
These are common, non-numeric building facts, stated plainly. A re-checker may want to source or cut them:
- Brick walls have weep holes near the bottom that let moisture out (/house-washing/).
- Shingle granules help shield the asphalt from the sun (/roof-soft-wash/).
- A rotary surface cleaner keeps the spray at a fixed height and avoids stripes (/driveway-cleaning/, /pressure-washing/).

## Older sources (dated on the page)
- Hail counts: Insurance Council of Texas figures as reported by CBS Texas in 2012.
- HomeAdvisor whole-house figures: January 2022 update. Fixr house page: January 2025.
- Addison's drought plan: the version in the town's May 2019 council packet (adopted 1999, amended 2011).
- Flower Mound watering limits: a 2018 Stage 1 example, presented as an example only.

## Sources that could not be fetched in this session
- Texas A&M AgriLife pesticide licensing page (redirect blocked). Because of that, the site makes **no** claim either
  way about whether soft washing chemicals require a Texas pesticide license. That question is worth a separate look.
- Medical sources on pressure washer injuries (redirects blocked). The site makes no injury statistics claims.
