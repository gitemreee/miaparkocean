import { chromium } from "playwright";
const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });

async function capture(path, name, count = 6) {
  await page.goto("http://localhost:4173" + path, { waitUntil: "networkidle" });
  await page.waitForTimeout(1200);
  // çerez bandını kapat
  await page.getByRole("button", { name: /Kabul Et/i }).click().catch(() => {});
  await page.waitForTimeout(400);
  // yavaşça kaydırarak scroll-reveal'ları tetikle
  const h = await page.evaluate(() => document.body.scrollHeight);
  for (let y = 0; y < h; y += 700) {
    await page.evaluate((v) => window.scrollTo(0, v), y);
    await page.waitForTimeout(160);
  }
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(900);
  const step = Math.max(1, Math.floor((h - 900) / (count - 1)));
  for (let i = 0; i < count; i++) {
    await page.evaluate((v) => window.scrollTo(0, v), i * step);
    await page.waitForTimeout(700);
    await page.screenshot({ path: `/tmp/shots/${name}-${i}.png` });
  }
  console.log(name, "ok, yükseklik", h);
}

await capture(process.argv[2] || "/", process.argv[3] || "home", Number(process.argv[4] || 6));
await browser.close();
