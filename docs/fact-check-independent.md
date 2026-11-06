# Independent fact-check (Nov 5 2026)

The agent that ran this check did not write the site. No page, commit or push was changed. This file is the only thing added.

## Bottom line
- **Pages read in full:** 29 of 31 (28 top-level pages plus contact/thanks, body and FAQs), plus the shared macros, footer and site.json. privacy-policy and terms were skipped as instructed. 404 and thanks hold no checkable facts.
- **Claims checked:** about 250 distinct checkable claims. This is an estimate; no exact tally was kept.
- **Result:** 3 ERROR, 28 WEAK entries plus 4 smaller wording items, 6 UNVERIFIED. All other checked claims matched their sources, including every Angi, HomeGuide, Fixr and Forbes price, every Fort Worth permit number and every Frisco section number.
- **Must fix before pushing:** E1, E2 and E3 (all three are on Keller and fence pages).

## How it was checked, and the limits
- Direct downloads were blocked by the network proxy (403), so sources were read with WebFetch. WebFetch returns text processed by a small model, not the raw page, and limits long quotes. Risky items were fetched a second time with narrow, word-for-word prompts. Where this file quotes a source, the wording comes from those fetches.
- **URLs:** 69 in site.json (68 sources plus the Comptroller search link). 66 opened. 1 was not tried (nws-normals, which no page cites).
- **Could not open (2):**
  - Denton's pressure wash manual (den-bmp), site error. Still unread by anyone. See U1.
  - EPA's live RRP page (epa-lead), site error. The search engine lists it, and EPA's own January 2021 archive copy opened. See the EPA note below.
- **Also could not open:** Flower Mound Ordinance 40-25 on Municode, site error. See U2.
- **Writer's "could not open" list, retried:**
  - Grapevine Main Street guidelines: **opens now**, section 2.1 was read.
  - Carrollton stormwater page: **opens now**.
  - Plano stormwater page: opens, but says nothing useful.
  - EPA pressure washing page: read through the archive copy.
  - Denton manual: still fails.
  - Arlington code chapter and the Texas AG home improvement page: not retried, because no page relies on them.
- PDFs were read to the 100,000 character mark, and past it for sec-std. fw-fair's last 18,000 characters were not read.

## Standing rules (hard flags)
| Check | Result |
|---|---|
| Names a washing company | None. Trex and James Hardie are product makers, Angi and Thumbtack are cited publishers. |
| Contractor voice, "we wash", "our crews" | None. A grep for we/our/us outside privacy and terms found none. "Crew" appears only for the independent company. |
| Invented license, insurance, rating, price as the line's own | None. No aggregateRating claims in page sources. |
| States a current drought stage | None. The pages say to call. FYI: Denton entered Stage 1 on Aug 19 2026, and a news sidebar says it lifted Aug 23 2026. Carrollton's page says it is "not under mandatory drought restrictions." Neither is stated on the site, which is correct. |
| Disclosure on every page, as the home page and about page claim | True. It is in the footer template. |
| TCEQ | No page mentions TCEQ, so there is nothing to check. No TCEQ pressure washing guidance turned up in a tceq.texas.gov search. |

---

## ERROR

### E1. Keller: wrong phone number for checking the stage (4 places)
- **File:** src/pages/keller-pressure-washing.html (lines 22, 30, 32, 40)
- **Sentence:** "Call 817-743-4080 to check the current stage."
- **Also:** "A quick call to 817-743-4080 settles it." and "For washing rules at the current stage, call 817-743-4080." and "Call 817-743-4080 and describe the job before you book."
- **Wrong:** The city page says "To report violations to any of the city's water conservation measures, please call 817-743-4080." That is the violations line, and the page gives no number for checking a stage. Its information line is "For more information, call Environmental Services at 817-743-4092 or 817-743-4094."
- **Fix:** Replace 817-743-4080 with "Environmental Services at 817-743-4092 or 817-743-4094" in all four places. Update docs/research/facts.md line 28 too.
- **Source:** https://www.cityofkeller.com/services/utility-billing/water-wastewater-drainage-billing/water-restrictions

### E2. Keller: Stage 1 is a prohibition, not a restriction
- **File:** src/pages/keller-pressure-washing.html
- **Sentence:** "If you are planning pressure washing in Keller, start with the city's water restrictions page, because Stage 1 here already restricts hosing paved areas and buildings."
- **Also:** the table cell "Restricts hosing paved areas and buildings", and "Keller's page lists hosing of paved areas and buildings among the Stage 1 Water Watch restrictions"
- **Wrong:** The city's wording is "Prohibits hosing off of paved areas like driveways and sidewalks, or buildings and windows". The site understates a ban, and the understatement could lead a reader to book a job that is not allowed.
- **Fix:** "because Stage 1 here already prohibits hosing off paved areas, buildings and windows." In the table: "Prohibits hosing off paved areas, buildings and windows". The page gives no exception for professionals, so the existing FAQ can stay with the corrected number.
- **Source:** same Keller URL.

### E3. Fence page: lean limits are not in the current Dallas code text
- **File:** src/pages/fence-cleaning.html
- **Sentence:** "A fence more than 4 feet tall may not lean more than 1 foot from vertical."
- **Also:** "A fence under 4 feet may not lean more than 6 inches."
- **Wrong:** These come from a 2015 council briefing and an old checklist citing Section 27-11(b)(10). The current Dallas code, in the minimum property standards article at subsection (d)(17), says to keep fences "in operating condition" and in line with the Development Code. It also says to "repair or replace rotted, missing, fire-damaged, or broken wooden slots and support posts". The words "vertical", "alignment" and "lean" do not appear on that code page. The Dallas Development Code itself was not checked for a lean rule.
- **Fix:** Delete both lean bullets. Replace with "Fences must be kept in operating condition, and rotted, missing, fire-damaged or broken wooden slats and support posts must be repaired or replaced." Cite the code page, not the 2015 briefing. Also check docs/research/facts.md line 79.
- **Source:** https://codelibrary.amlegal.com/codes/dallas/latest/dallas_tx/0-0-0-111216 (old text: https://dallas.gov/government/Council%20Meeting%20Documents/qol_4_fences_combined_08242015.pdf)

---

## WEAK (stronger than the source supports)

### W1. "Mild detergent" (4 pages)
- **Files:** fort-worth-pressure-washing.html, grapevine-pressure-washing.html, mckinney-pressure-washing.html, pressure-washing.html
- **Sentence:** "It suggests low-pressure water, mild detergent and soft brushes, tested on a small area first."
- **Wrong:** The Standards say "low-pressure water and detergent and natural bristle or other soft-bristle brushes". "Mild detergent" does not appear anywhere in the document.
- **Fix:** Delete "mild" on all four pages.
- **Source:** https://www.fortworthtexas.gov/files/assets/public/v/2/development-services/documents/all-preservation-and-design/historic/secretary-interior-standards-treatment-historic-homes.pdf

### W2. Roofs: "soft wash" is not what ARMA describes
- **File:** roof-soft-wash.html, also services.html
- **Sentence:** "The route the trade points to, using approved cleaners"
- **Also (services.html):** "The roofing trade warns that high pressure is likely to damage asphalt shingles, so roofs get a low-pressure cleaning solution instead."
- **Wrong:** ARMA never uses "soft wash". It says "DO NOT use a power washer or any type of brush or broom", and describes a solution "gently dispersed" and then rinsed. Fixr's soft wash is a machine set under 500 PSI. So ARMA has not endorsed machine soft washing. It may not even permit it.
- **Fix:** Table cell: "Closest to what ARMA describes: a solution applied gently and rinsed gently. Ask whether the shingle maker approves the method". services.html: "...so roofs call for a gently applied cleaning solution instead."
- **Source:** https://www.asphaltroofing.org/algae-discoloration/

### W3. Roofs: "breaks the same city rules" is too flat
- **File:** roof-soft-wash.html
- **Sentence:** "A solution that reaches a storm drain breaks the same city rules that apply to any soapy wash water."
- **Wrong:** Rules differ by city. Dallas turns on "a harmful quantity" for parts of the rule, and Addison turns on water quality standards.
- **Fix:** "A solution that reaches a storm drain can break the same city rules that apply to soapy wash water."
- **Source:** https://codelibrary.amlegal.com/codes/dallas/latest/dallas_tx/0-0-0-109726

### W4. Roofs: "spores"
- **File:** roof-soft-wash.html
- **Sentence:** "Algae spores travel in the air, so it can spread from roof to roof."
- **Wrong:** ARMA says "All species are transported through the air." It does not mention spores or spread from roof to roof.
- **Fix:** "ARMA says these algae are carried through the air."
- **Source:** https://www.asphaltroofing.org/algae-discoloration/

### W5. Deck: "most of its rain"
- **File:** deck-cleaning.html
- **Sentence:** "Dallas-Fort Worth gets most of its rain in spring and fall, according to the National Weather Service."
- **Wrong:** NWS says "The transition seasons of spring and fall are typically the wettest periods of the year." The fence page has this right.
- **Fix:** "Spring and fall are typically the wettest periods in Dallas-Fort Worth, according to the National Weather Service."
- **Source:** https://www.weather.gov/fwd/dfw_narrative

### W6. Deck: "low-visibility spot"
- **File:** deck-cleaning.html
- **Sentence:** "HGTV suggests a stair tread or another low-visibility spot before moving to the main boards."
- **Wrong:** HGTV says "Start in an area that would be easy to repair or replace, like a stair tread."
- **Fix:** "HGTV suggests starting somewhere easy to repair or replace, like a stair tread."
- **Source:** https://www.hgtv.com/remodel/outdoors/pressure-washing-a-deck

### W7. HGTV and Treated Wood deck figures applied to fences
- **Files:** fence-cleaning.html, services.html (table row "Softwood deck or fence"), index.html
- **Sentence:** "It can. HGTV puts softwood such as cedar and pine at roughly 500 to 600 PSI, and warns that resting the spray in one spot can gash wood permanently. Treated Wood says improper washing can etch, splinter or fuzz boards."
- **Wrong:** Both articles are about decks. HGTV's only mention of fences is about carpenter bees.
- **Fix:** Fence FAQ: "HGTV's deck guide puts softwood such as cedar and pine at roughly 500 to 600 PSI... The same soft wood is used in fences." services.html row: "Softwood deck". Keep index.html's sentence but add "for decks". Forbes also says wood fences "might require soft washing" and could be cited.
- **Source:** https://www.hgtv.com/remodel/outdoors/pressure-washing-a-deck

### W8. Fort Worth: the filter is recommended, not required
- **File:** fort-worth-pressure-washing.html
- **Sentence:** "A sanitary sewer discharge needs the owner's permission, a filter and no manholes."
- **Wrong:** The city says "Environmental Quality recommends filtering the wash water through a 400 micron filter". Owner permission and no manholes are firm, and the city also lists temperature, pH and grease limits.
- **Fix:** "A sanitary sewer discharge needs the owner's permission, can not go through a manhole, and must meet the city's limits. The city recommends a 400 micron filter."
- **Source:** https://www.fortworthtexas.gov/departments/environmental-services/environmental-quality/stormwater-quality/powerwash

### W9. Fort Worth: old materials "softer"
- **File:** fort-worth-pressure-washing.html
- **Sentence:** "Their paint may contain lead, and their masonry and wood are softer than anything built lately."
- **Wrong:** No source says this, and it is not true of all old materials. The guidance is about the damage abrasive cleaning can do to masonry and mortar joints.
- **Fix:** "Their paint may contain lead, and old masonry, mortar and wood trim can be easily damaged."
- **Source:** the sec-std URL in W1.

### W10. Fort Worth: Stage 3 line covers buildings
- **File:** fort-worth-pressure-washing.html
- **Sentence:** "Stage 1 discourages hosing paved areas and buildings, and at Stage 3 pressure washing is limited to painting preparation by a professional service with high efficiency equipment."
- **Wrong:** The Stage 3 clause is about "buildings or other structures", and it also allows fire protection. Paved areas stay at the carried-forward Stage 1 language.
- **Fix:** "...and at Stage 3, pressure washing of buildings is limited to surface preparation before painting, by a professional service with high efficiency equipment."
- **Source:** https://www.fortworthtexas.gov/files/assets/public/v/6/water/documents/save-water/fort-worth-2024-drought-contingency-plan.pdf

### W11. Denton: yard waste
- **File:** denton-pressure-washing.html
- **Sentence:** "Clear leaves and yard debris off the drive first, since Denton counts yard waste among the things that clog storm drains."
- **Wrong:** Denton's page does not mention yard waste, leaves or clippings. It says "fertilizing, mowing, taking out the trash, and walking the dog" can "clog or pollute a storm drain". McKinney is the source for yard waste.
- **Fix:** "Clear leaves and yard debris off the drive first, since Denton lists mowing among the everyday habits that can clog or pollute a storm drain."
- **Source:** https://www.cityofdenton.com/248/Residential-Watershed-Protection

### W12. Frisco: the defense does not itself mention cleaners
- **File:** frisco-pressure-washing.html
- **Sentence:** "Street wash water appears in the ordinance as an affirmative defense to enforcement, which is not the same as blanket permission. It does not cover water carrying a harmful cleaner, so ask how soapy water will be collected."
- **Wrong:** Section 34-331(b)(14) reads only "Street wash water", with no condition. The limit comes from a separate clause, 34-332(d)(7), on pavement wash-down holding a harmful quantity of soap. The defense can also be lost after a written notice (34-331(c)).
- **Fix:** "...A separate clause covers pavement wash-down water with a harmful quantity of soap, so ask how soapy water will be collected."
- **Source:** https://friscotexas.gov/DocumentCenter/View/22094/ARTICLE_IX__STORMWATER_DISCHARGEdoc

### W13. Frisco: dues and ponds
- **File:** frisco-pressure-washing.html
- **Sentence:** "So when wash water runs down the gutter on a Frisco street, it is often heading for water your own dues help maintain."
- **Wrong:** The city says only that "Many HOAs have maintenance responsibilities for common areas that include ponds, creeks and other stormwater features." Nothing says how often gutters lead to an HOA pond.
- **Fix:** "So on some Frisco streets, wash water in the gutter may be heading for water your own dues help maintain."
- **Source:** https://www.friscotexas.gov/1870/HOA-Stormwater-Management

### W14. Frisco: why people call
- **File:** frisco-pressure-washing.html
- **Sentence:** "Frisco homeowners often search for a washer because of a letter, a sale or a neighbor's clean driveway, and most of those trails lead back to an association."
- **Wrong:** No source for "most". It reads as a statistic.
- **Fix:** "Some Frisco homeowners go looking for a washer because of a letter, a sale or a neighbor's clean driveway, and an HOA is often part of that story."

### W15. NTMWD plan described as if it binds residents
- **Files:** frisco-pressure-washing.html, mckinney-pressure-washing.html, service-areas.html, how-often-to-pressure-wash-a-house.html, power-washing.html
- **Sentence:** "The district's plan bans hosing paved areas and buildings at Stage 3, except by variance and by a professional service using high efficiency equipment."
- **Wrong:** NTMWD says it does not have "the authority to create ordinances or enforce the measures". Member cities enforce through ordinances. Plano's page says this correctly. No member city's own ordinance was read.
- **Fix:** Add to the Frisco and McKinney FAQs: "Member cities adopt and enforce these rules themselves, so check with the city."
- **Source:** https://ntmwd.com/DocumentCenter/View/2162/2024-NTMWD-Water-Resource-and-Emergency-Management-Plan-PDF

### W16. Carrollton: Dallas Stage 3 implied to apply
- **File:** carrollton-pressure-washing.html
- **Sentence:** "Carrollton buys its water from Dallas, so a Dallas drought can reach your driveway here."
- **Wrong:** The Dallas plan says wholesale customers follow "similar procedures" under their contracts. It does not say Dallas's Stage 3 hosing clause binds Carrollton residents. Carrollton's own drought plan was not read, and its watering page does not mention hosing.
- **Fix:** Add after the Stage 3 sentence: "Carrollton sets its own rules, and this site has not read its drought plan." The lead can stay if softened to "so a Dallas drought may affect what Carrollton asks of you."
- **Source:** https://www.cityofcarrollton.com/departments/departments-a-f/environmental-quality/water-conservation/watering-rules-and-restrictions

### W17. Addison: one exemption left out
- **File:** addison-pressure-washing.html
- **Sentence:** "Its list of exempt discharges includes individual residential vehicle washing, but it does not mention pavement washing or mobile washing services."
- **Wrong:** True as written, but the list also ends with "any other water source not containing Pollutants". A reader who has the ordinance will see this.
- **Fix:** Add: "It also exempts any other water source not containing pollutants, which is why greasy water is the real question." Apply to the FAQ as well.
- **Source:** https://gis.addisontx.gov/GIS_Documents/Ordinances/2010/010-016%20Amend%20Chapter%2072,%20Illicit%20Discharges%20to%20Strmwtr%20Drainage%20System.pdf

### W18. McKinney: paint in the commercial area
- **File:** mckinney-pressure-washing.html
- **Sentence:** "Painting, repairs and like-for-like replacement typically need no permission."
- **Wrong:** Correct for residential areas. The same FAQ says "Paint colors in the commercial area of the Historic Overlay District do require approval when changing colors."
- **Fix:** "Repairs and like-for-like replacement typically need no permission, and residential paint colors are not regulated. Changing paint colors in the commercial area does need approval."
- **Source:** https://www.mckinneytexas.org/m/faq?cat=50

### W19. Southlake: report period
- **File:** southlake-pressure-washing.html
- **Sentence:** "Its report for fiscal 2025 counts 24 illicit discharges detected and eliminated."
- **Wrong:** The report's stated period is January 1 to August 20, 2025, not a full fiscal year.
- **Fix:** "Its report covering January to August 2025 counts 24 illicit discharges detected and eliminated."
- **Source:** https://cityofsouthlake.com/DocumentCenter/View/45170/Southlake-Year-6-2024-MS4-Annual-Report-FY25-Q2-Q4?bidId=

### W20. Southlake: VSI stretched
- **File:** southlake-pressure-washing.html
- **Sentence:** "The Vinyl Siding Institute's point about angled spray holds for most lapped materials."
- **Wrong:** VSI speaks only about vinyl siding.
- **Fix:** "The Vinyl Siding Institute makes this point about vinyl, and it is worth asking about on other lapped siding."
- **Source:** https://www.prnewswire.com/news-releases/when-thoughts-turn-to-spring-cleaning-6-simple-tips-can-keep-your-vinyl-siding-looking-new-300062053.html

### W21. Southlake: how many ponds
- **File:** southlake-pressure-washing.html
- **Sentence:** "Many neighborhoods here have ponds kept up by HOAs."
- **Wrong:** The city says who maintains HOA ponds, not how many there are.
- **Fix:** "Where a neighborhood has an HOA or private pond, the HOA or owner keeps it up."
- **Source:** https://cityofsouthlake.com/3833/Drainage-FAQs

### W22. "Does not license" stated as flat fact (3 places)
- **Files:** index.html, about.html, src/templates/macros.html
- **Sentence:** "Texas does not license power washing, so these questions do the job a license number would do in other trades."
- **Also:** "Pressure washing is not a state-licensed trade in Texas, so a homeowner has to know what to ask." and, in macros.html, "so there is no state license number to look up."
- **Wrong:** TDLR's list of 41 programs has no pressure washing program, but that shows only that one agency does not license it. No official statement was found. faq.html has the right wording: "this site found no state license for it". TDLR does license "Mold Assessors and Remediators", and whether that touches mildew washing was not checked.
- **Fix:** index.html: "This site found no Texas state license for power washing, so these questions do the job a license number would do in other trades." Use the same wording in about.html and the macro.
- **Source:** https://www.tdlr.texas.gov/licenses.htm

### W23. Comptroller search will miss sole proprietors
- **File:** src/templates/macros.html (repeated on most pages), how-it-works.html
- **Sentence:** "Look it up on the Texas Comptroller's account status search, which shows if an entity may transact business in Texas."
- **Wrong:** Accurate for entities. The search takes a taxpayer number, entity name or SOS file number, and the instructions refer only to "entities". A sole proprietor, which is common in this trade, may not appear, so a reader could wrongly take a miss as a warning sign.
- **Fix:** Add: "A sole proprietor may not appear, so a missing result does not by itself mean a problem."
- **Source:** https://comptroller.texas.gov/taxes/franchise/coas-instructions.php

### W24. Dallas drought plan source is an unsigned copy
- **File:** src/data/site.json (dal-dcp), used on index, power-washing, carrollton, how-often
- **Sentence:** source label "Dallas Water Utilities: 2024 Drought Contingency Plan"
- **Wrong:** The file name has "Draft83" and its resolution number and date are blank ("No. xxxxxx", "April xx, 2024"). **The wording itself holds up:** the adopted 2019 plan (Resolution 190680, April 24 2019) has the identical Stage 3 sentence.
- **Fix:** Label it "Dallas Water Utilities: 2024 Drought Contingency Plan (unsigned copy)", and add the adopted 2019 plan as a second source. Look for the signed 2024 version.
- **Source:** https://dallascityhall.com/departments/waterutilities/dch%20documents/pdf/drought-contingency-plan.pdf

### W25. How-often page drops the version caveats
- **File:** how-often-to-pressure-wash-a-house.html
- **Sentence:** "Flower Mound's Stage 2 and Denton's Stage 2 prohibit hosing off paved areas and buildings."
- **Wrong:** The Denton and Flower Mound pages rightly warn that these come from a 2019 plan and a 2019 ordinance. This page says it as current fact.
- **Fix:** "The versions this site read for Flower Mound and Denton prohibit hosing off paved areas and buildings at Stage 2, and those may have changed."

### W26. How-often: "The most popular time"
- **File:** how-often-to-pressure-wash-a-house.html
- **Sentence:** "The most popular time. Book a dry stretch, and expect pollen to return."
- **Wrong:** Angi calls spring the best season. No source says it is the most popular.
- **Fix:** "The season Angi recommends. Book a dry stretch, and expect pollen to return."
- **Source:** https://www.angi.com/articles/best-time-to-pressure-wash-house.htm

### W27. Home page: mold and green walls
- **File:** index.html
- **Sentence:** "Add mold, which peaks in humid late summer, and north walls stay green."
- **Wrong:** Children's Health is an allergy source. It says nothing about walls, and the link to green walls is the writer's own.
- **Fix:** "Mold also peaks from July through late summer, and shaded walls that stay damp can turn green."
- **Source:** https://www.childrens.com/health-wellness/dallas-named-one-worst-cities-allergies

### W28. Claims about the line itself
Facts about the business, not checkable on the web. Maurice should decide these.
- **a. contact.html.** "Say what needs washing, and an independent local company phones you." This is an unconditional promise, while the same page says the line "can not promise a time" and thanks says "should call you back". Fix: "and it is passed to an independent local company to call you back."
- **b. how-it-works.html.** "You never pay the line, and it does not add anything to your bill." The line cannot know whether a company builds a referral fee into its price. Fix: "You never pay the line, and the line sends you no bill."
- **c. contact.html.** "No. It goes to the company that will call you back, and to the service providers that run the line." with the question "Is my information sold?", and the form note "nobody sells them". A caller's details go to a company that "may pay a referral fee". A reader, or a regulator, could see that as selling a lead. This is not a legal finding, and it is not in INTAKE.md. Fix: drop "sold" and say plainly "Your details go only to the company and the providers running this line. Companies may pay a referral fee."

### Smaller wording items (WEAK, one line each)
- **plano-pressure-washing.html**, "Cost guides often use power washing for hot water work, which helps on grease and oil." Only HomeGuide was found. Fix: "Some cost guides, such as HomeGuide, use..." services.html already says this correctly.
- **driveway-cleaning.html**, "Angi says large grease or oil stains need a cleaning solvent applied before washing". Angi says solvents "can help break up those stains". Fix: "Angi says a cleaning solvent can help before washing."
- **pressure-washing-cost-dallas.html**, "HomeGuide lists a day's machine rental at $40 to $100." True of its driveway page, but its main price page says $45 to $250. Fix: "HomeGuide's driveway guide lists..."
- **plano-pressure-washing.html**, lead "In Plano, peeling paint and bad fences rank among the most common property violations." The list is from 2022. Fix: "ranked among the most common property violations in a 2022 list."

---

## UNVERIFIED (could not check)

| # | File and claim | What was tried | Recommendation |
|---|---|---|---|
| U1 | denton-pressure-washing.html: "Denton backs this up with a city manual called BMPs for Pressure Washing and Surface Cleaning. A company that works here often should know it." | PDF fails at the city's site. No one has read it. Only the title is known. The FAQ admits this, which is good. | Change to "Denton lists a manual titled..." and drop "backs this up". |
| U2 | flower-mound-pressure-washing.html: Stage 2 hosing rule from Ordinance 19-19 | Ordinance 40-25, which the town now links to, would not open on Municode. | Keep the page's caveat. Confirm with the town. Have Chrome open the Municode page. |
| U3 | flower-mound-pressure-washing.html: "later stages keep that rule" and "Stages 3 and 4 keep that rule" | Stage 4 carries forward Stages 2 and 3. Stage 3 text as read has the stage number missing ("All requirements of Stage shall effect"). Almost certainly fine. | Have the PDF checked by eye, or change to "and Stage 4 keeps it". |
| U4 | denton-pressure-washing.html: 2019 plan | The city's /droughtplan page gives no version and the PDF link could not be seen. No newer plan was found. The page already says 2019. | Keep the caveat. Ask the city. |
| U5 | plano-pressure-washing.html: "since storm drains here do not lead to a treatment plant" | Plano's stormwater page does not say this. True by nature of separate systems, and Carrollton, Arlington and Southlake say it of themselves. The page's source list has arl-storm and den-res, which are other cities, plus hg-drive, which supports nothing on this page. | Remove the three unrelated sources, or say "storm drains in the metroplex". |
| U6 | Trade knowledge with no source: "The mortar joint is softer than the brick", tire marks "moderate pressure", "Often some of it can" (roof from the ground), "damage often shows up only then" (McKinney) | Not cited on the pages. Reasonable, but not from any source read. | Fine as advice. Forbes supports the mortar point ("to prevent damage to mortar joints"), so add it if wanted. |

---

## Source and URL fixes
- **Bob Vila:** the cited link ends in .md. https://www.bobvila.com/articles/black-roof-stains-check-for-algae/ loads as the normal page. Use that.
- **PWNA:** the cited post does not say "trade group" or that certification is optional. https://www.pwna.org/frequently-asked-questions says "non-profit trade association founded in 1992". Add it as a source for how-it-works.html.
- **EPA:** the claim "EPA has its own guidance on pressure washing under its lead renovation rule" is **confirmed** from EPA's archive copy: https://19january2021snapshot.epa.gov/lead/how-do-rrp-requirements-apply-pressure-washing-what-containment-and-other-preparation-are_.html. EPA says pressure washing is "not a prohibited practice" under the rule, and firms must keep dust and debris "(including in the waste water)" in the work area. This could be added to the page. The live page itself was not read.
- **Carrollton stormwater page** now opens and could be added: "anything that flows into the storm sewer system empties directly into waterways without any treatment." https://cityofcarrollton.com/departments/departments-a-f/environmental-quality/stormwater
- **Grapevine design guidelines** now open and could be added to the historic section: "Chemicals and physical treatments should always be as gentle as possible" and "harsh methods (like sandblasting) can irreversibly damage historic fabric". https://www.grapevinetexas.gov/DocumentCenter/View/103
- **Flower Mound stormwater phone:** the FAQ's 972-874-6340 is correct for Environmental Services, but the town's stormwater page says "please call 972.874.6354". Use 6354 for stormwater questions. https://www.flowermound.gov/310/Stormwater
- **Frisco ordinance** has the same content on the city's linked ecode360 page, https://ecode360.com/38353390. It also covers wastewater "from the washing or other cleaning of a building exterior" with soap, which could be added since it reaches house washing.
- **Southlake:** Fort Worth's plan says wholesale customers must apply the same measures, and Southlake is on its list. The page is softer than it needs to be, which is safe.

---

## What passed, by topic
Each item below was matched against the cited source.

- **Dallas:** the offense, defense (b)(14), (f)(6)(E) and (G), burden of proof, no power washer permit in the code text, flyer steps, cones, barriers, 214-948-4022, two-day schedule and fines. Stage 3 wording.
- **Fort Worth:** $25 plus $25, one year, not transferable, insurance and licenses, 3 inch numbers on each side, 110 degree rule, parking lot warning, biodegradable warning, 1993 study and 560 sites, "most frequently encountered pollutant", $2,000 fines, floor drains, 817-392-6309, 817-392-1234, (817) 392-8000, 14 districts, Fairmount 375 acres, 1885 to 1940, two miles, wood frame bungalows, Stage 1 language, paint exception.
- **Frisco:** Sections 34-331, 34-332(d)(5), (d)(7), (g), 34-339 amounts, warning notice, notice of violation, cost recovery, 972-292-5800, fish kill note.
- **Addison:** 4.4 square miles, 180+ restaurants, 22 hotels, 12 million square feet, Chapter 72, 2010, $500, separate days, water entirely from Dallas.
- **Arlington:** spill line, separate systems, car wash tips, 817-459-6777, 10 a.m. to 6 p.m. daily.
- **Denton:** Lewisville Lake line, leading cause, car wash wastewater, 311 and 911, Stage 1 and 2 wording, three trigger types.
- **McKinney:** bacteria listing, 53,000 dogs, tenth of an inch, algal blooms, HHW, 972-547-2000, ordinary maintenance rule, masonry paint advice.
- **Keller:** all watering days, Monday rule, 10 to 6, runoff ban, TRWD trigger, Stage 2 and 3 items, vehicle rules, stormwater numbers and hours, lawn advice.
- **Grapevine:** 25 miles, 65.3 miles, northern drainage, five named waters, allowable discharges, 817-410-3330, 817-410-8127, Section 25-140, 70 and 30 percent, Standard 7 in full.
- **Southlake:** Fort Worth water, 748-8051, 748-8098 and hours, pond and creek rules, pH listing on the 2024 list.
- **Flower Mound:** two-day limit, HOA Monday and Thursday, hand-held hose rule, 972-874-6000, master plan wording, Cross Timbers.
- **Carrollton:** DWU supply, April to October hours, two days encouraged, Tuesday and Friday, 972-466-3035.
- **Plano:** the 2022 list order and items, 13 member cities, Stage 3 wording, enforcement through members.
- **Climate, soil, pollen:** July 1 and August 27, spring storms, hail, 90s and 100s, Houston Black clay, TPWD soils and trees, TSHA route, all five pollen ranges.
- **Costs:** all Angi Dallas figures (page dated Nov 16 2025), HomeGuide figures including $25 to $50, $20 to $75, sealing, staining, and deck, Fixr, Forbes including the $0.35 to $1 table row.
- **Makers:** ARMA checklist including 15 to 20 minutes, Hardie 1500 psi, 6 feet and warranty, VSI, Trex 3100 psi, 8 inches and warranty, Treated Wood 800 psi, HGTV 12 to 18 inches.
- **Other:** AG three-day rule, CPSC, SOS filing rules, Google Translate button (site.js), Allen and Irving redirects, footer disclosure.
