# Decisions log (Dallas Playbook 2.0 rebuild, Nov 5 2026)

Maurice was not available during this run. Each decision can be reversed.

## Build system
1. Copied from /home/claude/az-model (Yuma): build.py, scripts, templates, CSS, JS, font, macros, site.json structure and netlify.toml with publish = dist. No page text was copied; similarity.py compares against Yuma.
2. Old live site moved to docs/old-site/. Photos moved to src/static/images/ at the same public paths, so old image URLs still work.
3. Main's git history here is one commit, so retired files could not be listed. All old wildcard rules are kept instead.

## Brand
4. Brand name is now **Dallas Power Washing Pro** everywhere, matching the domain. The old site said "Dallas Metro Power Washing Pro" and a footer logo said "DALLAS WASH PRO".
5. logo.svg spelled "DALLAS METRO" in outlined letters. The METRO letters were removed, and its title and aria-label changed. favicon.svg had no name in it.
6. netlify/functions/submission-created.mjs: brand label changed to Dallas Power Washing Pro.
7. Colors: water blue #12508a header and first band (a deeper version of the old site's blues, white text passes AA), navy #0d1f3c, logo gold #f0a500 for call buttons and the second band with dark text.

## URLs
8. All old URLs rebuilt at the same path except Allen and Irving, which 301 to /service-areas/ (per the brief).
9. Blog redirects re-pointed: cost posts to /pressure-washing-cost-dallas/; best-time and how-often posts to /how-often-to-pressure-wash-a-house/; siding and home value posts to /pressure-washing/. The soft washing post stays on /roof-soft-wash/.
10. _redirects keeps the /service-name/* wildcard rules. They are not forced, so real pages are served first.

## Pages
11. 30 pages plus the noindex thank-you page, which is above the "about 25 to 28" in the brief, because the brief's named list already reaches 30.
12. **Pressure vs soft washing guide left out.** It would overlap /roof-soft-wash/ and /pressure-washing/, and the page count was already over. "soft washing dallas" is a target of /roof-soft-wash/, with a comparison table there and a link to house washing.
13. Gutter cleaning (390 searches) has no page. FAQ answers say the line does not take gutter calls.
14. "how much to charge" keywords are unused: that is a contractor's question.
15. Home page row is four service cards, plus a fence and deck section, so no photo repeats on the page. /services/ uses split rows for the same reason.
16. Quote form kept with the field names from the old form, no email field (the Yuma form has one, this site never did). Dropdown choices kept from the old form so GoHighLevel texts look the same.
17. Old copy "usually the next business day" was dropped: a response-time promise.
18. Privacy policy keeps the old policy's text message consent wording and Texas Data Privacy and Security Act line, in case the A2P registration refers to them.
19. Terms keep the Texas governing law clause from the old terms.

## Writing
20. "Houston Black", the real name of the state soil, is not on the site because the brief wants zero Houston hits. The pages say Blackland Prairie clay and the Texas state soil.
21. No current drought stage is stated anywhere: it changes, and this run could not verify it.
22. Fact-check found "red clay", which was removed: Blackland soil is dark. See docs/fact-check.md.
23. No separate sub-agent was available in this run. See docs/fact-check.md.
