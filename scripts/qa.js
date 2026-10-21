// Browser QA for the built site (Prompts 18 and 19).
// Serve dist first:  npx http-server dist -p 8080 -s
// Run:               NODE_PATH=$(npm root -g) node scripts/qa.js [baseUrl]
// Checks every sitemap route plus utility pages at five widths: horizontal overflow,
// console/page errors, exactly one visible H1, hero image loaded, the lead form present on
// first load, every in-page image loaded after scrolling, small touch targets on mobile.
// Then interaction checks: mobile menu, submenus, Escape, FAQ accordions, keyboard focus,
// the EN/ES toggle cookie, 404 for an invalid nested route, and scroll position on navigation.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const BASE = process.argv[2] || 'http://localhost:8080';
const dist = process.env.DIST || path.join(__dirname, '..', 'dist');
const sitemap = fs.readFileSync(path.join(dist, 'sitemap.xml'), 'utf8');
const routes = [...sitemap.matchAll(/<loc>https:\/\/houstonpowerwashingpro\.com([^<]*)<\/loc>/g)].map(m => m[1]);
routes.push('/thank-you/', '/404.html');
const WIDTHS = [1440, 1280, 768, 414, 360];
// Fonts and Google Translate are blocked by this sandbox's proxy; not a site error.
const IGNORE = /fonts\.(googleapis|gstatic)|translate\.google|ERR_CERT|ERR_TUNNEL|net::ERR_/;

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
      // form must exist in the first response, before any scrolling or interaction
      const hasForm = await page.$('form[name="houston-powerwashing-contact"][data-netlify="true"]');
      const formExpected = !['/privacy-policy/', '/terms-of-use/', '/thank-you/', '/404.html'].includes(route);
      if (formExpected && !hasForm) fail(route, w, 'lead form missing on first load');
      const h1 = await page.$$eval('h1', els => els.filter(e => e.offsetParent !== null).length);
      if (h1 !== 1) fail(route, w, `visible h1 count ${h1}`);
      const hero = await page.$('.hero__img');
      if (hero) {
        const ok = await hero.evaluate(i => i.complete && i.naturalWidth > 0 && i.loading !== 'lazy');
        if (!ok) fail(route, w, 'hero image not loaded or lazy');
        const heroH = await page.$eval('.hero', e => e.getBoundingClientRect().height);
        if (w >= 1280 && route !== '/' && (await page.$('.hero--full')) && heroH < 600) fail(route, w, `full hero only ${heroH}px tall`);
      }
      // scroll through to trigger lazy images
      await page.evaluate(async () => {
        for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); }
        await Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; setTimeout(r, 3000); })));
        window.scrollTo(0, 0);
      });
      await page.waitForTimeout(250);
      const broken = await page.$$eval('img', imgs => imgs.filter(i => !(i.complete && i.naturalWidth > 0)).map(i => i.getAttribute('src')));
      if (broken.length) fail(route, w, `images not loaded: ${broken.join(', ')}`);
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
      if (overflow > 1) fail(route, w, `horizontal overflow ${overflow}px`);
      const clipped = await page.$$eval('h1, h2, h3, .btn, table, form, img', els => els
        .filter(e => e.offsetParent !== null && !e.closest('.table-wrap') && !e.closest('.sub'))
        .filter(e => { const r = e.getBoundingClientRect(); return r.right > window.innerWidth + 1 || r.left < -1; })
        .map(e => e.tagName + ':' + (e.textContent || e.getAttribute('src') || '').trim().slice(0, 30)));
      if (clipped.length) fail(route, w, `elements outside viewport: ${clipped.slice(0, 4).join(' | ')}`);
      if (w <= 414) {
        const small = await page.$$eval('a.btn, button, .site-nav__link, input, select, textarea', els => els
          .filter(e => e.offsetParent !== null && !e.closest('.hp') && !e.closest('.sub'))
          .filter(e => { const r = e.getBoundingClientRect(); return r.height < 40 || r.width < 40; })
          .map(e => (e.textContent || e.name || '').trim().slice(0, 20)));
        if (small.length) fail(route, w, `small touch targets: ${small.slice(0, 5).join(', ')}`);
      }
      if (errors.length) fail(route, w, `console: ${errors.slice(0, 3).join(' | ')}`);
      await page.close();
    }
  }

  // ---- interaction checks ----
  const page = await browser.newPage({ viewport: { width: 390, height: 800 } });
  await page.goto(BASE + '/services/roof-cleaning/');
  const toggle = page.locator('.nav-toggle');
  await toggle.click();
  if (!(await page.locator('#site-nav').isVisible())) fail('mobile-menu', 390, 'menu did not open');
  if ((await toggle.getAttribute('aria-expanded')) !== 'true') fail('mobile-menu', 390, 'aria-expanded not true');
  const subBtn = page.locator('.has-sub .sub-toggle').first();
  await subBtn.click();
  if (!(await page.locator('#sub-services').isVisible())) fail('mobile-submenu', 390, 'services submenu did not open');
  await page.locator('#sub-services a', { hasText: 'Fence Cleaning' }).click();
  await page.waitForLoadState('load');
  if (!page.url().endsWith('/services/fence-cleaning/')) fail('mobile-submenu', 390, 'submenu link did not navigate');
  if ((await page.evaluate(() => window.scrollY)) !== 0) fail('navigation', 390, 'destination did not start at top');
  await page.locator('.nav-toggle').click();
  await page.keyboard.press('Escape');
  if (await page.locator('#site-nav').isVisible()) fail('mobile-menu', 390, 'Escape did not close menu');
  // back / forward
  await page.goBack(); await page.waitForLoadState('load');
  if (!page.url().endsWith('/services/roof-cleaning/')) fail('history', 390, 'back did not return');
  await page.goForward(); await page.waitForLoadState('load');
  if (!page.url().endsWith('/services/fence-cleaning/')) fail('history', 390, 'forward failed');
  // reload keeps form
  await page.reload();
  if (!(await page.$('form[name="houston-powerwashing-contact"]'))) fail('reload', 390, 'form missing after reload');
  // FAQ accordion
  const second = page.locator('.faq__item').nth(1);
  await second.locator('summary').click();
  if ((await second.getAttribute('open')) === null) fail('faq', 390, 'accordion did not open');
  await page.close();

  const desk = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await desk.goto(BASE + '/');
  // keyboard: first tab = skip link, visible focus
  await desk.keyboard.press('Tab');
  const skip = await desk.evaluate(() => document.activeElement.className);
  if (skip !== 'skip') fail('keyboard', 1440, 'first Tab is not the skip link');
  let sawOutline = true;
  for (let i = 0; i < 6; i++) {
    await desk.keyboard.press('Tab');
    const o = await desk.evaluate(() => { const s = getComputedStyle(document.activeElement); return s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) > 0; });
    if (!o) sawOutline = false;
  }
  if (!sawOutline) fail('keyboard', 1440, 'focused element without visible outline');
  // desktop submenu via keyboard
  await desk.focus('button[aria-controls="sub-guides"]');
  await desk.keyboard.press('Enter');
  if (!(await desk.locator('#sub-guides').isVisible())) fail('desktop-submenu', 1440, 'guides menu did not open with Enter');
  await desk.keyboard.press('Escape');
  if (await desk.locator('#sub-guides').isVisible()) fail('desktop-submenu', 1440, 'Escape did not close guides menu');
  // ES toggle sets cookie and reloads
  await desk.click('.lang__btn[data-lang="es"]');
  await desk.waitForLoadState('load');
  const cookies = await desk.context().cookies();
  if (!cookies.some(c => c.name === 'googtrans' && c.value === '/en/es')) fail('lang', 1440, 'googtrans cookie not set');
  if ((await desk.getAttribute('.lang__btn[data-lang="es"]', 'aria-pressed')) !== 'true') fail('lang', 1440, 'ES not marked pressed');
  await desk.click('.lang__btn[data-lang="en"]');
  await desk.waitForLoadState('load');
  const c2 = await desk.context().cookies();
  if (c2.some(c => c.name === 'googtrans' && c.value === '/en/es')) fail('lang', 1440, 'EN did not clear cookie');
  // invalid nested route -> 404 page
  const r404 = await desk.goto(BASE + '/services/not-a-real-service/');
  if (!r404 || r404.status() !== 404) fail('404', 1440, `invalid route status ${r404 && r404.status()}`);
  if (!(await desk.textContent('h1')).includes('Not Be Found')) fail('404', 1440, '404 page content not shown');
  // reduced motion honoured
  const rm = await browser.newPage({ reducedMotion: 'reduce' });
  await rm.goto(BASE + '/');
  const trans = await rm.$eval('.btn', b => getComputedStyle(b).transitionDuration);
  if (!/^0s/.test(trans)) fail('reduced-motion', 0, `transitions still ${trans}`);
  await browser.close();

  results.forEach(r => console.log(r));
  console.log(`\n${routes.length} routes x ${WIDTHS.length} widths + interaction checks: ${failures} failures`);
  process.exit(failures ? 1 : 0);
})();
