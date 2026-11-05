# Fact-check (Nov 5 2026)

**What was run, plainly.** The rule calls for a separate agent that did not write the pages. **That did not happen in this run**: no sub-agent tool was available, so the same agent that wrote the pages also checked them. This is a self-check against sources, not an independent one. If Maurice wants the stricter standard, a separate agent should re-check it.

**Method.** Sources were opened with WebFetch, which returns a summary of the page made by a small model, not the raw page. Facts went into docs/research/facts.md with URLs, and pages were written from that file. Then: (a) every page was re-read claim by claim against facts.md, and (b) a script listed every number in the page sources that does not appear in facts.md. The 8 items it flagged were confirmed against the fetch results (Denton and Flower Mound and Fort Worth phone numbers, $1.50 deck figure, Section 25-140, 911, age 13, dates).

## Found and fixed
| Claim as first written | Problem | Fix |
|---|---|---|
| "Red clay" and "red mud" on walls | Blackland soil is dark; not in any source | Now "mud" (3 pages) |
| Lake Grapevine "about 3.6 square miles" | The summary was ambiguous about what that figure measures | Removed |
| Grapevine "one of the few metroplex cities" with a drinking water lake | Overclaim; Denton says similar of Lewisville | Reworded |
| Fort Worth "the rare city", "most Texas cities leave you to guess", "only Fort Worth" | No source compared cities | Reworded |
| Flower Mound "keeps more of its oaks than most suburbs" | Unsourced | Replaced with the town's Master Plan: a largely intact Cross Timbers area and a conservation district in central Flower Mound (source added) |
| Flower Mound "sits in the Cross Timbers" from a county-level source | Too strong for that source | Now cited to the town's own plan |
| Keller "wide lots" | Unsourced | Removed |
| Frisco "much of Frisco was built in recent decades" | Unsourced | Softened |
| Roof photo "clay tile" | Could be another tile | "tile-style" |
| "Most roof cleaners are based on bleach" | Overstated | "Many" |
| Quote season pressure ("spring pollen can get busy") | Unsourced | Softened |
| "Water forced under shingles" | Not in the source | Removed |
| Owner described as Black-owned on /about/ | Not in the brief | Removed; Maurice can add it |

## Could not be fully verified (left out, softened or flagged on the page)
- **Current drought stage** for every city: not stated anywhere. Pages say to call.
- **Dallas code section number**: the text returned showed subsections but no section number, so pages say "city code". Likely Chapter 19 stormwater article.
- **Dallas drought plan**: the 2024 file on Save Dallas Water has "Draft" in its file name. The Stage 3 wording matches the 2024 regional plan, but confirm the adopted text.
- **Denton's pressure washing manual**: the title was seen, the PDF would not open. The page says so in its FAQ, and it is listed as a source.
- **Denton drought plan** is the 2019 version; the page says so. **Flower Mound's Stage 2 wording** is from Ordinance 19-19; a newer ordinance (40-25) exists and the page says details may have changed.
- **EPA's page on pressure washing and the lead rule**, **City of McKinney FAQ on maintenance** (opened by a mobile URL only), **Carrollton's stormwater page**, **Arlington's code chapter**, **Plano's stormwater pages** and the **Texas Attorney General's home improvement page** could not be read or returned no content. Pages use only what was read. The EPA link is cited by its title only, and the page gives no rule details from it.
- **Grapevine Main Street Historic District guidelines** would not open; only the document title and the city's Standards page were read.
- **Keller Stage 1**: the summary says it "restricts" hosing of paved areas and buildings. Exact wording not confirmed, and whether professionals are exempt is unknown; the page says to call.
- **Dallas watering hours**: the ordinance page says any day of the year, and a 2026 bill insert says April 1 to Oct 31. Pages do not state these hours for Dallas.
- **Cost figures**: Angi's main page came back as a 2022 cached copy and was not used; its Dallas page was used. HomeGuide shows no update date. Fixr's numbers conflict inside its own page, so the page uses only its whole-house and minimum figures and says guides differ.
- **Texas license**: "no state license" rests on TDLR's program list not including one. There is no official statement saying so. The FAQ says "this site found no state license".
- **Average 100-degree days at DFW**: a chart image, unreadable. Pages use only first and last dates.
- **Insurance, hail, general wall behavior**: no statistics used. Soft general statements (mud splash, mortar softer than brick) are common trade knowledge and are not cited.

## Totals
About 150 factual claims were reviewed across 30 pages. 14 were corrected, softened or removed (table above). Everything left has a listed source, or is general knowledge, or is business fact from INTAKE.md.
