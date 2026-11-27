// CSS animasyonlu bir HTML sayfasını kare kare (saydam PNG) çizer.
// Tüm animasyonlar duraklatılır, her karede currentTime elle ayarlanır — sonuç kare kesinliğindedir.
//   NODE_PATH=$(npm root -g) node reel-kare.cjs sayfa.html cikti-klasoru KARE_SAYISI FPS [w] [h]
const path = require("path");
const { chromium } = require("playwright");

(async () => {
  const [html, cikti, nStr, fpsStr, wStr, hStr] = process.argv.slice(2);
  const n = +nStr, fps = +fpsStr, w = +(wStr || 1080), h = +(hStr || 1920);
  const ISCI = 3;
  const tarayici = await chromium.launch();
  await Promise.all([...Array(ISCI).keys()].map(async (k) => {
    const s = await tarayici.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
    await s.goto("file://" + html);
    await s.evaluate(() => document.fonts.ready);
    await s.waitForFunction(() => [...document.images].every((i) => i.complete && i.naturalWidth > 0));
    await s.evaluate(() => document.getAnimations().forEach((a) => a.pause()));
    for (let i = k; i < n; i += ISCI) {
      await s.evaluate((ms) => {
        document.getAnimations().forEach((a) => { a.currentTime = ms; });
        return new Promise((r) => requestAnimationFrame(() => r()));
      }, (i / fps) * 1000);
      await s.screenshot({ path: path.join(cikti, `k-${String(i).padStart(4, "0")}.png`), omitBackground: true });
    }
    await s.close();
  }));
  await tarayici.close();
})();
