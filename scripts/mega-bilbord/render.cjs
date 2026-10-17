// Dev pano parçalarını Chromium'da dilim dilim (tile) çizer.
// İş: {html, w, h, dsf, dilim, cikti} → cikti-0.png, cikti-1.png ... (soldan sağa)
//   NODE_PATH=$(npm root -g) node render.cjs isler.json
const fs = require("fs");
const { chromium } = require("playwright");

(async () => {
  const isler = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
  const tarayici = await chromium.launch();
  for (const is of isler) {
    const ctx = await tarayici.newContext({
      viewport: { width: is.w, height: is.h }, deviceScaleFactor: is.dsf,
    });
    const s = await ctx.newPage();
    await s.goto("file://" + is.html);
    await s.evaluate(() => document.fonts.ready);
    await s.waitForFunction(() =>
      [...document.images].every((i) => i.complete && i.naturalWidth > 0));
    await s.evaluate(() => new Promise((r) => requestAnimationFrame(() => r())));
    const dilimler = [];
    for (let x = 0, i = 0; x < is.w; x += is.dilim, i++) {
      const w = Math.min(is.dilim, is.w - x);
      const yol = `${is.cikti}-${i}.png`;
      await s.screenshot({ path: yol, omitBackground: true, clip: { x, y: 0, width: w, height: is.h } });
      dilimler.push(yol);
    }
    fs.writeFileSync(is.cikti + ".json", JSON.stringify(dilimler));
    await ctx.close();
    console.log("  çizildi:", is.cikti, dilimler.length, "dilim");
  }
  await tarayici.close();
})();
