// Usage: node scripts/shot.js <url> <out-prefix> [widths...]
const { chromium } = require('playwright');
(async () => {
  const [url, out, ...ws] = process.argv.slice(2);
  const widths = ws.length ? ws.map(Number) : [1440, 390];
  const browser = await chromium.launch();
  for (const w of widths) {
    const page = await browser.newPage({ viewport: { width: w, height: w > 800 ? 900 : 844 } });
    const errors = [];
    page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
    page.on('pageerror', e => errors.push(String(e)));
    await page.goto(url, { waitUntil: 'networkidle' }).catch(e => errors.push(String(e)));
    await page.screenshot({ path: `${out}-${w}.png`, fullPage: true });
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
    console.log(w, 'overflow:', overflow, 'errors:', JSON.stringify(errors));
    await page.close();
  }
  await browser.close();
})();
