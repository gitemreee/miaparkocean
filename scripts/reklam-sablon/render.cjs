// İşler listesini (JSON) Chromium'da 2x ölçekle ekran görüntüsüne çevirir.
//   NODE_PATH=$(npm root -g) node scripts/reklam-sablon/render.cjs isler.json
const fs = require("fs");
const { chromium } = require("playwright");

(async () => {
  const isler = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
  const tarayici = await chromium.launch();
  for (const is of isler) {
    const ctx = await tarayici.newContext({
      viewport: { width: is.w, height: is.h }, deviceScaleFactor: 2,
    });
    const sayfa = await ctx.newPage();
    await sayfa.goto("file://" + is.html);
    await sayfa.evaluate(() => document.fonts.ready);
    await sayfa.waitForFunction(() =>
      [...document.images].every((i) => i.complete && i.naturalWidth > 0));
    await sayfa.screenshot({ path: is.png, type: "png" });
    await ctx.close();
    console.log("  render:", is.png);
  }
  await tarayici.close();
})();
