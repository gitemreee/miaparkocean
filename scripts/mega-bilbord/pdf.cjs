// Pano HTML'ini düzenlenebilir (metinleri gerçek metin, şekilleri vektör) tek sayfa PDF'e çevirir.
// Canva / Illustrator'a içe aktarmak için.  İş: {html, w, h, pdf}
//   NODE_PATH=$(npm root -g) node pdf.cjs isler.json
const fs = require("fs");
const { chromium } = require("playwright");

(async () => {
  const isler = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
  const tarayici = await chromium.launch();
  for (const is of isler) {
    const s = await tarayici.newPage({ viewport: { width: is.w, height: is.h } });
    await s.goto("file://" + is.html);
    await s.evaluate(() => document.fonts.ready);
    await s.waitForFunction(() =>
      [...document.images].every((i) => i.complete && i.naturalWidth > 0));
    await s.pdf({ path: is.pdf, width: `${is.w}px`, height: `${is.h}px`,
                  printBackground: true, pageRanges: "1" });
    await s.close();
    console.log("  pdf:", is.pdf);
  }
  await tarayici.close();
})();
