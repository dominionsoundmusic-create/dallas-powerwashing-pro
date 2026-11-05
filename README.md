# dallas-powerwashing-pro (Dallas Power Washing Pro)

Static site for dallaspowerwashingpro.com, a free power washing phone line for Dallas-Fort Worth.

- Edit pages in `src/pages/`, shared data in `src/data/site.json`, templates in `src/templates/`.
- Build: `python3 build.py` (writes `dist/` and `docs/image-list.md`). Netlify publishes `dist/`.
- Checks: `python3 scripts/check.py`, `python3 scripts/grep_check.py`, `python3 scripts/check_old_urls.py`,
  `python3 scripts/similarity.py --other <yuma>/dist`, `python3 scripts/keyword_plan.py`, and with dist served on :8765
  `node scripts/responsive_check.js` and `node scripts/functional_check.js`.
- Records: `SERVICES.md`, `docs/keyword-plan.md`, `docs/decisions.md`, `docs/qa.md`, `docs/fact-check.md`,
  `docs/image-list.md`, `docs/research/facts.md`. The old live site is kept in `docs/old-site/`.
