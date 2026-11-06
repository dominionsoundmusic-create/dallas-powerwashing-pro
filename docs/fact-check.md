# Fact-check (Nov 5 2026)

**What was run, plainly.** The rule calls for a separate agent that did not write the pages. **That did not happen in this run**: no sub-agent tool was available, so the same agent that wrote the pages also checked them. This is a self-check against sources, not an independent one. If Maurice wants the stricter standard, a separate agent should re-check it.

**Method.** Sources were opened with WebFetch, which returns a summary of the page made by a small model, not the raw page. Facts went into docs/research/facts.md with URLs, and pages were written from that file. Then: (a) the writer went back over the claims while the pages were being finished and compared them with facts.md, which was a review of the text as written, not a separate line-by-line read of every final page, and (b) a script listed every number in the page sources that does not appear in facts.md. The 8 items it flagged were confirmed against the fetch results (Denton and Flower Mound and Fort Worth phone numbers, $1.50 deck figure, Section 25-140, 911, age 13, dates).

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
- **EPA's page on pressure washing and the lead rule**, **Carrollton's stormwater page**, **Arlington's code chapter**, **Plano's stormwater pages** and the **Texas Attorney General's home improvement page** could not be read or returned no content. Pages use only what was read. The EPA link is cited by its title only, and the page gives no rule details from it.
- **Grapevine Main Street Historic District guidelines** would not open; only the document title and the city's Standards page were read.
- **Keller Stage 1**: the summary says it "restricts" hosing of paved areas and buildings. Exact wording not confirmed, and whether professionals are exempt is unknown; the page says to call.
- **Dallas watering hours**: the ordinance page says any day of the year, and a 2026 bill insert says April 1 to Oct 31. Pages do not state these hours for Dallas.
- **Cost figures**: Angi's main page came back as a 2022 cached copy and was not used; its Dallas page was used. HomeGuide shows no update date. Fixr's numbers conflict inside its own page, so the page uses only its whole-house and minimum figures and says guides differ.
- **Texas license**: "no state license" rests on TDLR's program list not including one. There is no official statement saying so. The FAQ says "this site found no state license".
- **Average 100-degree days at DFW**: a chart image, unreadable. Pages use only first and last dates.
- **Insurance, hail, general wall behavior**: no statistics used. Soft general statements (mud splash, mortar softer than brick) are common trade knowledge and are not cited.

## Totals
No exact claim count was kept. 13 items were corrected, softened or removed (table above). The aim was that everything left has a listed source, or is general knowledge, or is business fact from INTAKE.md, but this was a self-check, so a few soft general statements may have been missed.

## Corrections from the independent fact-check (Nov 5 2026)

A separate agent that did not write the site checked it. Its findings are in docs/fact-check-independent.md. This section supersedes anything above that conflicts with it, including the Keller, Dallas drought plan and Texas license notes. Each item below was changed in the page sources and rebuilt. The corrections were not independently re-read afterward, and no source was reopened for this pass: the wording comes from the quotes in the independent report.

### ERROR (3 of 3 fixed)
| # | Change |
|---|---|
| E1 | Keller: 817-743-4080 (the violations line) replaced in all four places with Environmental Services at 817-743-4092 or 817-743-4094. facts.md updated. |
| E2 | Keller: Stage 1 now reads "prohibits hosing off paved areas, buildings and windows" in the lead, body and table. The Stage 1 FAQ and the page title also dropped the softer wording. |
| E3 | Fence: both lean limits deleted. List now says fences must be kept in operating condition, and rotted, missing, fire-damaged or broken slats and posts must be repaired or replaced. Source is now the current Dallas code page, and the 2015 briefing was removed. facts.md updated. |

### WEAK (28 of 28 entries and 4 of 4 smaller items fixed)
| # | Change |
|---|---|
| W1 | "Mild" deleted on all four pages. |
| W2 | Roof table now says "Closest to what ARMA describes" and to ask whether the shingle maker approves the method. services.html says "a gently applied cleaning solution". |
| W3 | "Breaks" changed to "can break". |
| W4 | Now "ARMA says these algae are carried through the air." |
| W5 | Deck: "typically the wettest periods". |
| W6 | Deck: "somewhere easy to repair or replace, like a stair tread". The step title "Test a hidden spot" became "Test a spot first". |
| W7 | Fence FAQ names HGTV's deck guide and deck boards, and adds that the same soft wood is used in fences. The sanding note also names the deck guide. services.html row is "Softwood deck". index.html adds "for decks". |
| W8 | Fort Worth: permission, no manhole, city limits, and the filter as a recommendation. |
| W9 | Fort Worth: "old masonry, mortar and wood trim can be easily damaged". |
| W10 | Fort Worth: Stage 3 line limited to pressure washing of buildings, as surface preparation before painting. |
| W11 | Denton: cites mowing among everyday habits, not yard waste. |
| W12 | Frisco: the limit now points to the separate soap clause. |
| W13 | Frisco: "on some Frisco streets ... may be heading". |
| W14 | Frisco: "Some ... an HOA is often part of that story". |
| W15 | Frisco and McKinney FAQs now say member cities adopt and enforce the rules. Same point added on service-areas, how-often and power-washing, which the finding also listed. |
| W16 | Carrollton: lead softened, and "Carrollton sets its own rules, and this site has not read its drought plan" added. |
| W17 | Addison: the "any other water source not containing pollutants" exemption added to the body and the FAQ. |
| W18 | McKinney: repairs and like-for-like need no permission, residential colors are not regulated, commercial color changes need approval. |
| W19 | Southlake: report covers January to August 2025. |
| W20 | Southlake: VSI point stated as about vinyl. |
| W21 | Southlake: "Where a neighborhood has an HOA or private pond, the HOA or owner keeps it up." |
| W22 | "This site found no Texas state license for power washing" on index, about and how-it-works. The macro says TDLR's list does not include it, this site found no license, and "you may have no state license number". |
| W23 | Sole proprietor note added on how-it-works, the macro and faq. |
| W24 | Source relabeled "(unsigned copy)", and the adopted 2019 plan (Resolution 190680) added as a second source on the four pages that use it. The signed 2024 version is still not found. |
| W25 | How-often: "The versions this site read ... and those may have changed." |
| W26 | How-often: "The season Angi recommends." |
| W27 | Home: "Mold also peaks from July through late summer, and shaded walls that stay damp can turn green." |
| W28a | Contact page, its meta description, FAQ and how-it-works now say the request is passed along for a possible call back. The thanks page says the same, and "may call you back" replaces "should call you back" and "calls you back". |
| W28b | How-it-works: "You never pay the line, and the line sends you no bill." |
| W28c | "Is my information sold?" became "Who sees my information?". The FAQ, the form note and the privacy page dropped "sold" and "nobody sells", and they state that companies may pay a referral fee. The form wording leaves out "only", because the privacy page allows legally required disclosure. |
| Small | Plano "Some cost guides, such as HomeGuide". Driveway "a cleaning solvent can help before washing". Cost guide "HomeGuide's driveway guide lists". Plano lead "ranked ... in a 2022 list". |

### UNVERIFIED (4 softened, 2 left with their caveat)
| # | Change |
|---|---|
| U1 | Denton: "lists a manual titled", and "Ask a company that works here whether it knows it." |
| U2 | No copy change. The page caveat stays. Still unconfirmed: Ordinance 40-25 on Municode. |
| U3 | Flower Mound: both places now say only Stage 4 keeps the rule. |
| U4 | No copy change. The 2019 caveat stays. Still unconfirmed: whether Denton has a newer plan. |
| U5 | Plano: claim now attributed to Arlington, so arl-storm stays as its source. den-res removed. hg-drive stays, because the page now names HomeGuide. |
| U6 | Mortar line now "can be damaged by too much pressure", with Forbes added as a source. Tire mark cell now says to ask the company. Roof-from-ground FAQ now "That depends on height and pitch." McKinney "damage often shows up only then" removed. |

### Source and URL fixes
- Bob Vila link corrected to the normal page.
- PWNA FAQ added as a source on how-it-works.
- Flower Mound stormwater FAQ now gives 972-874-6354, with the town's stormwater page as a new source.

Optional additions in the report (EPA archive copy, Carrollton stormwater, Grapevine guidelines, the Frisco ecode360 clause) were not added, because no finding required them.

### Left for Maurice
- The privacy page still says mobile numbers and text consent "are not sold or shared with third parties for their marketing". It is SMS consent wording and speaks only to marketing, so it was left alone. The independent report did not review privacy or terms.
- W28 is a business decision as well as a wording one. The report notes it is not a legal finding.
