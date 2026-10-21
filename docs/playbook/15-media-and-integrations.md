# Prompts 13 to 15: Contact, trust, media

- **13 Contact:** phone page only. No form anywhere (check.py fails on `<form>`). Tap-to-call in header, hero,
  CTA band, footer.
- **14 Trust and social:** no reviews, badges or ratings exist, so none are shown. Facebook link in the top bar,
  footer and Organization `sameAs`; other icon slots stay hidden until site.json gets URLs. External links open
  in a new tab with an accessible "(opens in a new tab)" label.
- **15 Media:** 10 existing photos reused (7 distinct scenes), never the same photo twice on one page (check.py).
  Heroes are not lazy-loaded and are preloaded with fetchpriority=high; in-body images are lazy with width and
  height. 31 new images (heroes 1920x1080) are listed in docs/image-list.md with Artistly prompts; until they
  exist, each page shows an existing stand-in photo, so nothing is broken.
