// Usage: node scripts/shot-view.js <url> <out.png> <width> [scrollY] [height]
const { chromium } = require('playwright');
(async () => {
  const [url, out, w, y, h] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: +w, height: +(h || 900) } });
  await page.goto(url, { waitUntil: 'networkidle' });
  if (y) await page.evaluate(v => window.scrollTo(0, v), +y);
  await page.waitForTimeout(300);
  await page.screenshot({ path: out });
  await browser.close();
})();
