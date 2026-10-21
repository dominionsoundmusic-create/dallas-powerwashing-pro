CLIENT WEBSITE QUESTIONNAIRE: DALLAS POWER WASHING PRO (dallaspowerwashingpro.com)

Filled in Oct 21 2026 from what Maurice Johnson has stated. This is the factual source of truth for
Playbook 2.0. Anything marked UNKNOWN stays off the site. Never fill a gap by guessing.

1. BUSINESS BASICS
OFFICIAL BUSINESS NAME: Dallas Power Washing Pro (a d/b/a of Dominion Digital Group). The old site
  and logo say "Dallas Metro Power Washing Pro". Use "Dallas Power Washing Pro" to match the domain,
  the same way the Dallas HVAC and roofing sites were renamed to match theirs. Update the logo
  wordmark text to match (keep the mark, colors and layout). Record this in docs/decisions.md.
PRIMARY CITY: Dallas
STATE: Texas
FULL BUSINESS ADDRESS: DO NOT DISPLAY
PHONE: (469) 649-7066 / tel:+14696497066. Lives in ONE place only (src/data/site.json); never
  hard-coded in a page. Never show 903-636-7511 or any Houston number.
PUBLIC EMAIL: UNKNOWN (do not display an email)
YEAR ESTABLISHED: do not display
OWNER: Owned by Dominion Digital Group. Do not name an owner on the site.
HOURS: The phone line is answered 24 hours a day, 7 days a week by an automated assistant.

WHAT THE BUSINESS ACTUALLY IS (read this twice):
Dallas Power Washing Pro is a FREE PHONE LINE and website, NOT a pressure washing company. It does
not own a pressure washer and never cleans, quotes or schedules anything itself. When someone calls:
- An automated assistant answers, any hour. The same number also takes AC/heating, roofing, water
  damage and mold calls for the Dallas area, so it first asks what the caller needs.
- The caller says what needs cleaning and roughly how big it is.
- The call is transferred to an independent, locally owned DFW pressure washing company, which hears
  a short summary before it picks up.
- If that company cannot answer, the caller's name, callback number, city and need are passed along
  for a call back.
The company inspects, quotes, does the work and is paid directly by the customer. The line never
charges the customer. Companies may pay the line a referral fee (always disclose this).
Never name the partner company. Never say "we clean", "our crew", "our team", "our equipment",
"our technicians", "licensed and insured", or anything implying the line does the work.

REFERRAL DISCLOSURE (footer of every page, adapt lightly but keep the meaning):
"Dallas Power Washing Pro is a free phone line, not a pressure washing company. It answers your
call and connects you with an independent local pressure washing company, which inspects, quotes
and does the work, and which you pay directly. Companies may pay a referral fee."

2. SERVICES
PRIMARY CATEGORY: Pressure washing and soft washing referral line for Dallas-Fort Worth.
ALL SERVICES: choose from the keyword research (rules in CLAUDE.md).
SERVICES NOT OFFERED: painting, sealing or staining as a main service, window cleaning, gutter
  repair, mold remediation inside the home, car washing, equipment sales or rentals, house cleaning
  (maid service).

3. SERVICE AREA
PRIMARY AREA: Dallas and the Dallas-Fort Worth metroplex.
TOWN PAGES: the towns listed in CLAUDE.md. Keep every existing town URL.
LOCATIONS NOT TO CLAIM: anywhere outside DFW. No Houston-area towns (no Katy, Friendswood, Deer
  Park, League City, Fulshear), no Austin-area towns (no Pflugerville), no El Paso, no other states
  (no Dallas, Georgia; no Arlington, Virginia; no Flowery Branch, Georgia).

4. BRANDING
LOGO: images/logo.svg (slate #2a313e, sky blue #38bdf8, amber #f0a500). Keep the mark and colors;
  change only the wordmark text as described above. Keep favicon.svg, favicon.ico and
  apple-touch-icon.png.
COLORS: header in a real brand color (a deep blue built from the logo's slate and sky blue, never
  dull gray), sky blue for one color band, amber for buttons and a second band.
BACKGROUND: mostly WHITE sections with occasional bold color bands. Never pale off-white tints.
STYLE: bright, clearly visible photos. Full-width hero edge to edge with a dark fade behind the
  headline. Text, photos and cards share one full-width layout (see CLAUDE.md). No white on white.
  No eyebrow labels. No em dashes or en dashes in visible copy.
TOP OF EVERY PAGE: "John 3:16" at the left and the quote, EXACTLY: "I believe the unbelievable, I
  receive the impossible, because it's doable." credited "— Jesse Duplantis". (This attribution
  dash is the one dash allowed.)
FOOTER OF EVERY PAGE: "© 2026 Dominion Digital Group. All rights reserved." and the linked credit
  "Designed by Dominion Web Design Pro" to https://dominionwebdesignpro.com (opens in a new tab).
LANGUAGE: EN / ES toggle in the header, in brand colors.

5. CALLS TO ACTION
MAIN CTA: Call the phone number. THE SITE IS PHONE ONLY, like the Houston, Tucson and Yuma sites.
  Retire the old contact form (`dallas-powerwashing-contact`): /contact/ becomes a phone page. If an
  old form thank-you URL exists, 301 it to /contact/.
SECONDARY CTA: a real page (How it works, a guide). Never a form.

6. SOCIAL PROFILES
Facebook: https://www.facebook.com/dallaspowerwashingpro (already on the live site; keep it). Other
  icon slots are data-driven and stay hidden until URLs are added.

7. TRUST
LICENSES: verify on the web whether Texas requires a state license for residential pressure
  washing, and whether any DFW city requires a permit or registration, and state it correctly with
  a source. Do not claim any license, certification, insurance or bond for Dallas Power Washing Pro.
WHAT A HOMEOWNER SHOULD ASK ANY COMPANY: proof of liability insurance, a written price per surface,
  whether siding, roofs and wood will be soft washed rather than blasted, and how runoff is handled.
REVIEWS / GUARANTEES / YEARS / JOB COUNTS / TEAM: none. Do not invent any.

8. WORDS TO AVOID
"free estimate(s)", "same-day", "guarantee", "best price", "cheapest", "top-rated", "#1",
"licensed and insured", "years of experience", "500+", "5-star", "eco-friendly products".

9. WEBSITE
DOMAIN: https://dallaspowerwashingpro.com (live on Netlify, production branch main)
ANALYTICS: GA4 G-37W4N8XFL8 is on the live pages. Keep it, loaded with the delayed loader (see
  CLAUDE.md speed rules), with phone-tap tracking.
PHOTOS: the photos already in images/ (pw-*.jpg, pw-hero.jpg). Reuse first; list every other image
  in docs/image-list.md with File name, Size and an Artistly prompt.
NETLIFY: do not deploy, do not change settings. Work stays on the `build` branch.
