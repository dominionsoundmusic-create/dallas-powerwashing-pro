# Prompt 2: Architecture (approved static equivalent of the SSR master)

There is no GoHighLevel AI Studio SSR master for this site. The approved architecture (CLAUDE.md, copied from the
Houston Power Washing Pro build system) is:

- **Static pre-rendered HTML** built by `build.py` (Python, Jinja2, YAML front matter) into `dist/`, committed.
  Every title, description, canonical, Open Graph tag, heading, body copy and JSON-LD block is in the initial HTML
  response, which satisfies every "raw server HTML" requirement. There is no hydration step and no client router:
  internal links are plain links, so "route changes start at the top" holds by default.
- **Centralized configuration:** `src/data/site.json` holds business data, phone, CTAs, social, analytics, nav,
  services, guides, cities and the sources registry. Templates and pages read from it; the phone number appears
  nowhere else.
- **Pages:** `src/pages/**.html` (front matter + Jinja body). URL = path, or `url:` override (used for
  /privacy-policy.html and /terms.html).
- **Shared components:** `src/templates/layouts/base.html`, `partials/{header,hero,faq,cta,footer}.html`,
  `macros.html` (img, service/guide/city cards, related, call box, how-it-works strip, disclosure, video, sources).
- **Static assets:** `src/static/` (inlined CSS source, JS, self-hosted Inter woff2, images, favicons, _redirects).
  WebP 480/800/1200/1600/1920 copies are generated into `images/w/` and served through `<picture>` srcsets.
- **Deploy config:** `netlify.toml` with `publish = "dist"` and no build command.
- **Forms:** none (phone only), enforced by check.py.
- **Commands:** `python3 build.py`, `python3 scripts/check.py`, `python3 scripts/check_old_urls.py`,
  `python3 scripts/similarity.py`, `python3 scripts/keyword_plan.py`, `node scripts/qa.js`.

Hard blockers: none.
