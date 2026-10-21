# Dallas Power Washing Pro (dallaspowerwashingpro.com): PLAYBOOK 2.0 REBUILD. INSTRUCTIONS FOR CLAUDE CODE

You are rebuilding a LIVE static lead-generation website for Maurice Johnson by running
Dominic & Dalton's Website Builder Prompt Playbook 2.0 (PLAYBOOK.md), Prompts 1 to 20, in full.
The site is live and indexed, so the rebuild must keep every URL Google knows.

## RUN STRAIGHT THROUGH. DO NOT STOP.
Maurice is not watching this session and cannot approve anything. Do NOT pause at the end of each
playbook phase, do NOT ask "continue?", do NOT wait for input. Make reasonable decisions yourself,
write them down in docs/decisions.md, and keep going until Prompt 20 is finished and every check
below passes. Commit and push the `build` branch after each phase so work is never lost. The only
reason to stop early is if something would require paying money, deploying, merging to main, or
changing a repository other than this one.

## Source files (read all of them first)
- INTAKE.md: the facts. It wins over anything else. UNKNOWN means leave it off the site.
- PLAYBOOK.md: the playbook (Operating Rules, then Prompts 1 to 20). It was written for GHL AI
  Studio; apply its rules and its 20 steps to this static build system.
- keywords/Dallas-Power-Washing-Keywords.xlsx: Ubersuggest, United States, pulled Oct 21 2026. 220
  unique keywords, 14 seed tabs (each row typed Suggestion or Question) plus an ALL tab. Every
  DFW keyword with 10 or more searches a month must be assigned to a page as a target or supporting
  keyword, or listed in docs/keyword-plan.md as deliberately unused with a one-line reason.
  "Near me" and national terms ("power washing services near me" 8,100, "how much does pressure
  washing cost" 1,300, "how often pressure wash house" 390) are national volume: supporting
  keywords or guide targets only. Unused list: other cities and states (Houston, Katy, Friendswood,
  Deer Park, League City, Fulshear, Pflugerville, El Paso, Dallas GA, Arlington VA, Flowery Branch
  GA, York PA, Mount Vernon), car washes, maid and house cleaning, washing machines, jobs and
  salary, "how to charge" and other business-owner searches, DIY equipment, chemical, PSI and
  instruction searches, and rows naming a company ("pressure washing plus").
- The current live site (this repo's main branch): read every page before writing. Keep useful
  verified facts, re-verify them on the web, but do NOT copy its paragraphs: every page is written
  fresh. Reuse its photos in images/ first.

## Copy the build system from Houston Power Washing Pro (NOT its words)
The repository dominionsoundmusic-create/houston-powerwashing-pro, branch `build`, holds a finished
Playbook 2.0 rebuild of the sister Houston site, with its latest layout and speed fixes. Clone it
and copy its BUILD SYSTEM: build.py, scripts/ (check, similarity, old-URL check), src/templates/,
src/static/css and JS, the macros (img, faqs, sources, disclosure), the site.json structure,
netlify.toml (publish = "dist") and the docs/ document set as a pattern. Keep its full-width layout,
centered card rows, left-to-right footer rows, the social link slots and the Google Translate EN/ES
toggle. Adapt every Houston value to Dallas.
NEVER copy page text, paragraphs, FAQs or sentence runs from Houston or any other site. No Houston
places, no Harris County, Fort Bend or City of Houston facts. Research DFW equivalents instead:
North Texas weather (heat, humidity, spring storms and hail, winter freezes), the North Texas
clay soil and what it does to concrete, mildew and algae on north-facing siding, pollen season,
the cities' storm water and wash-water runoff rules (City of Dallas, Fort Worth, Plano and others:
check what each says about pressure washing wastewater going into storm drains), HOA patterns in
the suburbs, water restrictions, and what Texas requires (if anything) to run a pressure washing
business.
Keep the speed fix exactly: WebP 480/800/1200/1600/1920 srcset, preloaded hero with fetchpriority
high, self-hosted woff2 font, the site CSS inlined in a <style> block instead of a render-blocking
stylesheet link, GA4 (G-37W4N8XFL8) loaded only on first scroll/click/keypress/touch or 3.5 seconds
after load with phone-tap tracking kept, and any YouTube video click-to-play (thumbnail plus play
button, iframe only on click).

## URLs: keep every live URL (this is a rebuild of an indexed site)
Every URL in main's sitemap.xml and every page file on main must still resolve on the new site,
either as a rebuilt page at the SAME path or a 301 to the closest new page (record each in
docs/decisions.md). Keep the existing paths, for example /pressure-washing/, /power-washing/,
/driveway-cleaning/, /fence-cleaning/, /deck-cleaning/, /roof-soft-wash/, /services/, /about/,
/contact/, /faq/, /privacy-policy.html, /terms.html and every /<town>-pressure-washing/ page. Keep
every existing _redirects rule that still makes sense (including the retired blog posts) and copy
_redirects into dist/. If you build a real page at a path an old rule or wildcard redirects, remove
that rule so it never shadows a real page. Run the old-URL check script and record the result in
docs/qa.md.

## Pages to build (decide the exact list from the keywords, then follow it)
- Core: home (target "power washing dallas" 720, "pressure washing in dallas" 720, "pressure
  washing dallas" 590 and "pressure washing dallas texas" 590; the brand says POWER washing, so
  the title and H1 lead with power washing and also cover pressure washing), services overview,
  service areas overview, how it works, about, FAQ, contact (a phone page), privacy, terms, 404.
- Service pages at their existing paths where one exists: residential pressure washing, house
  washing and soft washing ("what is soft wash pressure washing" 140, "soft pressure washing near
  me" 170), roof cleaning ("roof cleaning dallas" 30), driveway and concrete cleaning, commercial
  pressure washing ("commercial pressure washing rates" 260, "commercial pressure washing companies
  near me" 170), fence cleaning and deck cleaning. Decide which existing path each lives on and
  record it.
- Guide pages for the strongest question keywords, each researched and sourced: what pressure
  washing costs in DFW ("how much does pressure washing cost" 1,300, per square foot 40; cite
  published, sourced ranges and say real quotes vary), how often to pressure wash a house in North
  Texas (390), power washing vs pressure washing (90), what commercial pressure washing costs (30),
  and whether you need a license to pressure wash in Texas (10, answer it accurately with sources).
- Town pages: Maurice's rule is ANY town with 10 or more searches a month gets its own page. From
  the data that is Fort Worth ("pressure washing fort worth" 260), Frisco (170), Denton (170 plus
  "denton pressure washing" 10), Plano (110 plus "power washing plano" 50), Arlington (110 plus
  "pressure washing arlington" 90), McKinney ("mckinney pressure washing" 70 plus 30) and Allen (40
  plus "allen pressure washing" 30). Check each in the data yourself and record the exact keywords
  and volumes in SERVICES.md. These live at their existing paths (/fort-worth-pressure-washing/
  and so on).
- Addison, Carrollton, Flower Mound and Irving already have live pages but no 10+ keyword in this
  pull. Keep them at their URLs as shorter, honest town pages researched for that town. Do not pad.
- Write SERVICES.md (every page, URL, target keyword with volume and SEO difficulty) and
  docs/keyword-plan.md before writing pages.

## Hard rules for every page
1. Never "we clean", "our crew", "our team", "our equipment", "our technicians", "we are
   licensed/insured" or anything implying the line does the work.
2. Never invent licenses, certifications, insurance, reviews, ratings, prices, years in business,
   team members, job counts, guarantees, awards or statistics.
3. Never name the partner pressure washing company, or any specific company.
4. Only Dallas-Fort Worth places. No Houston-area or Austin-area towns, no other states.
5. No em dashes or en dashes in visible copy (except the Duplantis credit). No eyebrow labels.
   American spelling.
6. No DIY machine instructions (PSI settings, nozzle tips, chemical mixing). Explain what a good
   company should do and why, and point people to the phone line. Safety basics only.
7. No prices presented as the line's prices. Cost guides cite published, sourced ranges and say
   real quotes vary.
8. Every page except privacy, terms and 404 has 3 to 6 FAQs written the way people ask (use the
   Question rows), rendered visibly AND as FAQPage JSON-LD in the page's single JSON-LD graph.
9. Every page has a full-width hero image plus at least two in-body images, each with filename,
   alt, width, height and loading="lazy" (hero eager). Reuse this repo's images first. One photo
   may fill several spots across the site, but never twice on the same page.
10. Facts must be real and current. Research each page on the web and cite every source in the
    page's sources list (sources run across the page in rows, like the footer). If you cannot
    verify a fact, leave it out.
11. Each page is written for its own keyword. Never reuse paragraphs between pages with names
    swapped. Measure: Jaccard similarity on 5-word shingles between every pair of pages of the
    same type, and every Dallas page against every Houston page; any pair above 15% gets
    rewritten. Record the numbers in docs/qa.md. Town pages must be researched for THAT town: its
    neighborhoods, housing age and materials, HOA patterns, water and runoff rules, weather.
12. The referral disclosure appears on every page (wording in INTAKE.md).
13. Banned phrases: "your trusted partner", "one-stop solution", "look no further", "unmatched
    excellence", "we've got you covered", plus the WORDS TO AVOID in INTAKE.md.
14. Mark every page with the HTML comment `dwdp:handwritten 2026-10-21` in the first 4KB.

## Design (Maurice's standing rules, check each one)
- Header/menu bar in a real brand color (deep blue), never dull gray. Phone visible with
  tap-to-call. EN/ES Google Translate toggle in the header on every page, in brand colors.
- Hero stretches edge to edge on every page: full-strength photo, dark left-to-right fade behind
  the headline, logo/headline/buttons aligned to the left rail at 1440, 1920 and 2560 wide. Hero
  stays above the fold (max-height about 700px) with the call button visible.
- Body text, photos and cards run FULL WIDTH on the rail. Never box text into a narrow center strip.
- Mostly WHITE sections broken by occasional bold color bands (hero, white, sky blue band, white,
  an amber or deep blue band). Never pale off-white tints. Never every section tinted.
- No white text or white boxes on white. Every card, box and button has clear contrast.
- Card rows: 3 / 2 / 1 columns, any short last row CENTERED. Footer links and towns run left to
  right in rows.
- Logo: keep the mark; update the wordmark to "Dallas Power Washing Pro"; keep the favicons.

## Before you finish (all must pass)
- `python3 build.py` then `python3 scripts/check.py`: 0 errors.
- Every old URL resolves on the built site or has a 301 in dist/_redirects (script, result in
  docs/qa.md).
- Grep the built site for: em/en dashes in visible text (except the Duplantis credit), "we clean",
  "our crew", "our team", "our technicians", "licensed and insured", "free estimate", "same-day",
  "500+", "Dallas Metro", "Houston", "Katy", "Harris County", "Pflugerville", "Georgia",
  "Virginia", "(832)", "(903)", "903-636". Fix every hit.
- No horizontal overflow at 1440, 1024, 768 and 390 px wide.
- Independent fact-check: start separate sub-agents that did not write the pages, have them check
  every factual claim and source on every page, and fix what they find. Record it in
  docs/fact-check.md. Never say "fact-checked" unless this was actually run.
- docs/image-list.md lists every image still needed: File name, Size, then an Artistly prompt
  (bright, clearly visible, Dallas-Fort Worth homes, driveways and storefronts, no text, no logos,
  no recognizable faces, "wide cinematic landscape shot, subject positioned on right third of
  frame, well lit"). Missing images must never show as broken: pages use an existing photo until
  the new one arrives.

## Git
- Work on the branch `build`. Commit as you go with clear messages and push `build` after each
  phase.
- When finished, open a pull request from `build` to `main` so Netlify makes a deploy preview, but
  do NOT merge it.
- Do NOT merge to main, do NOT push to main, do NOT deploy, do NOT touch Netlify settings, do NOT
  pay for anything. Maurice decides when it goes live.

## Final report (Maurice reads on his phone, 5 lines max)
Pages built (count by type), checks passed, duplication range, fact-check result, how many images
need Artistly, and the one thing Maurice must do next.
