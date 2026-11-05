// Functional QA: mobile menu, submenus, FAQ accordion, tel links, skip link, EN/ES cookie, 404, footer links land at top.
// Usage: serve dist, then PORT=8765 NODE_PATH=$(npm root -g) node scripts/functional_check.js
const { chromium } = require("playwright");
(async () => {
  const b = await chromium.launch(); const out = [];
  const ok = (n, c) => out.push((c ? "PASS " : "FAIL ") + n);
  let p = await b.newPage({ viewport: { width: 390, height: 844 } });
  await p.goto("http://127.0.0.1:" + (process.env.PORT || "8765") + "/roof-soft-wash/");
  await p.click(".nav-toggle"); ok("mobile menu opens", await p.isVisible("#site-nav"));
  await p.click('.sub-toggle[aria-controls="sub-services"]'); ok("services submenu opens", await p.isVisible("#sub-services"));
  await p.keyboard.press("Escape"); ok("Escape closes menu", !(await p.isVisible("#site-nav")));
  p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  await p.goto("http://127.0.0.1:" + (process.env.PORT || "8765") + "/faq/");
  const items = await p.$$(".faq__item"); const second = items[1];
  ok("FAQ first open by default", await items[0].evaluate(e => e.open));
  await second.$eval("summary", s => s.click()); ok("FAQ item toggles open", await second.evaluate(e => e.open));
  const tels = await p.$$eval('a[href^="tel:"]', as => [...new Set(as.map(a => a.getAttribute("href")))]);
  ok("all tel links +14696497066 " + tels.join(","), tels.length === 1 && tels[0] === "tel:+14696497066");
  await p.hover('.has-sub:has(#sub-guides)'); ok("guides submenu on hover", await p.isVisible("#sub-guides"));
  await p.keyboard.press("Tab"); const f = await p.evaluate(() => document.activeElement.className); ok("first Tab focuses skip link (" + f + ")", f.includes("skip"));
  await p.click('.lang__btn[data-lang="es"]').catch(()=>{}); await p.waitForLoadState("load");
  const ck = (await p.context().cookies()).map(c => c.name + "=" + c.value).join(";"); ok("ES toggle sets googtrans cookie (" + ck + ")", /googtrans=\/en\/es/.test(ck));
  const r = await p.goto("http://127.0.0.1:" + (process.env.PORT || "8765") + "/404.html"); ok("404 page renders h1", (await p.textContent("h1")).length > 3);
  for (const u of ["/", "/fort-worth-pressure-washing/", "/privacy-policy.html"]) { await p.goto("http://127.0.0.1:" + (process.env.PORT || "8765") + "" + u); await p.evaluate(() => window.scrollTo(0, 3000)); await p.click('.site-footer a[href="/about/"]'); ok("footer link from " + u + " lands at top", (await p.evaluate(() => window.scrollY)) === 0); }
  console.log(out.join("\n")); await b.close();
})();
