// Browser QA for the built site (Prompts 18 and 19).
// Serve dist first:  python3 -m http.server 8090 -d dist
// Run:  NODE_PATH=/opt/node22/lib/node_modules PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers node scripts/qa.js [baseUrl]
// For every sitemap route plus /404.html, at 1440, 1024, 768 and 390 px wide: horizontal overflow,
// console/page errors, exactly one visible H1, hero image loaded, every in-page image loaded after
// scrolling, no <form>, a visible tap-to-call link in the header, small touch targets on mobile.
// At 1440, 1920 and 2560: the hero H1 starts near the left rail (not a narrow centered box) and the
// hero is no taller than about 700px with the call button above the fold.
// Then interaction checks: mobile menu, submenus, Escape, FAQ accordions, the EN/ES toggle cookie,
// GA4 not requested before interaction, and the delayed GA4 loader firing after a scroll.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const BASE = process.argv[2] || 'http://localhost:8090';
const dist = process.env.DIST || path.join(__dirname, '..', 'dist');
const sitemap = fs.readFileSync(path.join(dist, 'sitemap.xml'), 'utf8');
const routes = [...sitemap.matchAll(/<loc>https:\/\/dallaspowerwashingpro\.com([^<]*)<\/loc>/g)].map(m => m[1]);
routes.push('/404.html');
const WIDTHS = [1440, 1024, 768, 390];
// Fonts, analytics and Google Translate may be blocked by this sandbox's proxy; not a site error.
const IGNORE = /googletagmanager|google-analytics|translate\.google|ERR_CERT|ERR_TUNNEL|net::ERR_|Failed to load resource/;

(async () => {
  const browser = await chromium.launch();
  const results = [];
  let failures = 0;
  const fail = (route, w, msg) => { failures++; results.push(`FAIL ${route} @${w}: ${msg}`); };

  for (const route of routes) {
    for (const w of WIDTHS) {
      const page = await browser.newPage({ viewport: { width: w, height: w >= 1024 ? 900 : 800 } });
      const errors = [];
      page.on('console', m => { if (m.type() === 'error' && !IGNORE.test(m.text())) errors.push(m.text()); });
      page.on('pageerror', e => errors.push(String(e)));
      const resp = await page.goto(BASE + route, { waitUntil: 'load' });
      if (!resp || resp.status() !== 200) fail(route, w, `HTTP ${resp && resp.status()}`);
      if (await page.$('form')) fail(route, w, 'form found (site is phone only)');
      const h1 = await page.$$eval('h1', els => els.filter(e => e.offsetParent !== null).length);
      if (h1 !== 1) fail(route, w, `visible h1 count ${h1}`);
      const heroOk = await page.$eval('.hero__img', i => i.complete && i.naturalWidth > 0).catch(() => route === '/404.html');
      if (!heroOk) fail(route, w, 'hero image not loaded');
      const call = await page.$eval('.header-call', a => a.offsetParent !== null && a.getAttribute('href')).catch(() => null);
      if (call !== 'tel:+14696497066') fail(route, w, `header call link missing or wrong: ${call}`);
      // scroll to the bottom so lazy images load, then check every image
      await page.evaluate(async () => {
        for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 40)); }
      });
      await page.waitForTimeout(300);
      const broken = await page.$$eval('img', imgs => imgs.filter(i => !(i.complete && i.naturalWidth > 0)).map(i => i.currentSrc || i.src));
      if (broken.length) fail(route, w, `images not loaded: ${broken.join(', ')}`);
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
      if (overflow > 1) fail(route, w, `horizontal overflow ${overflow}px`);
      if (w === 390) {
        const small = await page.$$eval('a, button', els => els.filter(e => {
          const r = e.getBoundingClientRect(); const cs = getComputedStyle(e);
          return r.width > 0 && r.height > 0 && r.height < 24 && cs.display !== 'inline' && !e.closest('.crumbs, .sources, .site-footer, p, li');
        }).map(e => (e.textContent || e.getAttribute('aria-label') || '').trim().slice(0, 30)));
        if (small.length) results.push(`WARN ${route} @390: small touch targets: ${small.join(' | ')}`);
      }
      if (errors.length) fail(route, w, `console errors: ${errors.join(' | ')}`);
      await page.close();
    }
  }

  // Hero alignment and height on wide screens (home and one city page)
  for (const route of ['/', '/fort-worth-pressure-washing/']) {
    for (const w of [1440, 1920, 2560]) {
      const page = await browser.newPage({ viewport: { width: w, height: 1000 } });
      await page.goto(BASE + route, { waitUntil: 'load' });
      const m = await page.evaluate(() => {
        const h = document.querySelector('.hero').getBoundingClientRect();
        const t = document.querySelector('.hero h1').getBoundingClientRect();
        const b = document.querySelector('.hero .btn').getBoundingClientRect();
        const logo = document.querySelector('.site-header .logo').getBoundingClientRect();
        return { heroH: Math.round(h.height), h1Left: Math.round(t.left), logoLeft: Math.round(logo.left), btnBottom: Math.round(b.bottom), vh: innerHeight };
      });
      results.push(`INFO hero ${route} @${w}: height ${m.heroH}px, h1 left ${m.h1Left}px, logo left ${m.logoLeft}px, call button bottom ${m.btnBottom}px`);
      if (Math.abs(m.h1Left - m.logoLeft) > 4) fail(route, w, `hero h1 not on the logo rail (${m.h1Left} vs ${m.logoLeft})`);
      if (m.h1Left > 0.12 * w) fail(route, w, `hero h1 starts too far right (${m.h1Left}px)`);
      if (m.heroH > 720) fail(route, w, `hero taller than about 700px (${m.heroH}px)`);
      if (m.btnBottom > m.vh) fail(route, w, 'call button below the fold');
      await page.screenshot({ path: path.join(process.env.SHOTS || '/tmp', `hero-${route.replace(/\//g, '_') || 'home'}-${w}.png`) });
      await page.close();
    }
  }

  // Interaction checks
  const page = await browser.newPage({ viewport: { width: 390, height: 800 } });
  const requests = [];
  page.on('request', r => requests.push(r.url()));
  await page.goto(BASE + '/', { waitUntil: 'load' });
  await page.waitForTimeout(500);
  if (requests.some(u => u.includes('googletagmanager.com/gtag/js'))) fail('/', 390, 'GA4 requested before any interaction');
  await page.click('.nav-toggle');
  if (!(await page.$eval('.site-header', h => h.classList.contains('nav-open')))) fail('/', 390, 'mobile menu did not open');
  await page.click('#site-nav .sub-toggle');
  if (!(await page.$eval('#site-nav .has-sub', li => li.classList.contains('sub-open')))) fail('/', 390, 'submenu did not open');
  await page.keyboard.press('Escape');
  if (await page.$eval('.site-header', h => h.classList.contains('nav-open'))) fail('/', 390, 'Escape did not close the menu');
  await page.mouse.wheel(0, 400);
  await page.waitForTimeout(800);
  if (!requests.some(u => u.includes('googletagmanager.com/gtag/js'))) fail('/', 390, 'GA4 loader did not fire after scroll');
  const faqBefore = await page.$eval('.faq__item:nth-child(2)', d => d.open);
  await page.click('.faq__item:nth-child(2) summary');
  const faqAfter = await page.$eval('.faq__item:nth-child(2)', d => d.open);
  if (faqBefore === faqAfter) fail('/', 390, 'FAQ accordion did not toggle');
  await page.click('.lang__btn[data-lang="es"]');
  await page.waitForTimeout(800);
  const cookie = (await page.context().cookies()).find(c => c.name === 'googtrans');
  if (!cookie || cookie.value !== '/en/es') fail('/', 390, 'ES toggle did not set the googtrans cookie');
  await page.close();

  // Invalid route returns the 404 page (python http.server returns its own 404; Netlify serves /404.html)
  const p404 = await browser.newPage();
  const r404 = await p404.goto(BASE + '/fort-worth-pressure-washing/not-a-page/');
  results.push(`INFO invalid nested route status: ${r404.status()} (Netlify serves dist/404.html for this)`);
  await p404.close();

  await browser.close();
  console.log(results.join('\n'));
  console.log(`\n${routes.length} routes x ${WIDTHS.length} widths checked, ${failures} failures`);
  process.exit(failures ? 1 : 0);
})();
