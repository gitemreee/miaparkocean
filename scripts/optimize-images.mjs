// MİA PARK OCEAN — görsel optimizasyon scripti
// Kaynak render'ları web için WebP'ye çevirir (büyük + küçük varyant) ve OG görseli üretir.
// Çalıştırma: npm run images

import sharp from "sharp";
import { mkdir } from "node:fs/promises";
import { existsSync, readdirSync } from "node:fs";
import path from "node:path";

const SRC = "C:/Users/emrey/Desktop/MIA PARK OCEAN";
const OUT = path.resolve("public/images");

const map = [
  { in: "WhatsApp Image 2026-07-13 at 00.14.31.jpeg", out: "hero-courtyard-dusk" },
  { in: "WhatsApp Image 2026-07-13 at 00.14.32 (5).jpeg", out: "entrance-gate" },
  { in: "WhatsApp Image 2026-07-13 at 00.14.58 (1).jpeg", out: "terrace-pergola" },
  { in: "WhatsApp Image 2026-07-13 at 00.15.31.jpeg", out: "facade-warm" },
  { in: "WhatsApp Image 2026-07-13 at 00.14.32.jpeg", out: "aerial-pools" },
  { in: "WhatsApp Image 2026-07-13 at 00.14.32 (3).jpeg", out: "street-corner" },
  { in: "WhatsApp Image 2026-07-13 at 00.14.58.jpeg", out: "interior-bedroom" },
  { in: "WhatsApp Image 2026-07-13 at 00.15.15.jpeg", out: "interior-living" },
  { in: "WhatsApp Image 2026-07-13 at 00.14.58 (3).jpeg", out: "duplex-cutaway" },
  { in: "WhatsApp Image 2026-07-13 at 00.14.58 (2).jpeg", out: "loft-living" },
  { in: "WhatsApp Image 2026-07-13 at 00.15.14.jpeg", out: "plan-1plus1" },
  { in: "WhatsApp Image 2026-07-08 at 12.20.48 (4).jpeg", out: "courtyard-pools" },
  { in: "WhatsApp Image 2026-07-13 at 00.15.14 (1).jpeg", out: "balcony-dusk" },
];

// Yeni Türkçe broşür sayfaları → online katalog görselleri.
// Dosya adına göre sıralanır (mia-park-ocean-01..10) ve catalog-1..N.webp olarak üretilir.
const BROSUR_SAYFALAR = "C:/Users/emrey/Desktop/mia-broşür/brosur-sayfalar";
const catalogFiles = existsSync(BROSUR_SAYFALAR)
  ? readdirSync(BROSUR_SAYFALAR).filter((f) => f.toLowerCase().endsWith(".png")).sort()
  : [];

// Daire tipi görselleri (1+0, 1+1, 2+1) — plan + iç mekanlar
const daire = [
  { in: "1+0/2f65bfd0-8a69-47d2-b781-708e68299043_00001.jpg", out: "unit-1plus0-plan" },
  { in: "1+0/sketch2img-result (10).jpg", out: "unit-1plus0-a" },
  { in: "1+0/sketch2img-result (11).jpg", out: "unit-1plus0-b" },
  { in: "1+1/6ae249e5-1e72-4183-af51-166be87c9c70_00001.jpg", out: "unit-1plus1-plan" },
  { in: "1+1/sketch2img-result (4).jpg", out: "unit-1plus1-a" },
  { in: "1+1/sketch2img-result (7).jpg", out: "unit-1plus1-b" },
  { in: "1+1/sketch2img-result (8).jpg", out: "unit-1plus1-c" },
  { in: "2+1/sketch2img-result (18).jpg", out: "unit-2plus1-cutaway" },
  { in: "2+1/sketch2img-result (20).jpg", out: "unit-2plus1-a" },
  { in: "2+1/sketch2img-result (16).jpg", out: "unit-2plus1-b" },
  { in: "2+1/sketch2img-result (15).jpg", out: "unit-2plus1-c" },
  { in: "2+1/sketch2img-result (19).jpg", out: "unit-2plus1-d" },
];

async function run() {
  await mkdir(OUT, { recursive: true });

  for (let i = 0; i < catalogFiles.length; i++) {
    const inPath = path.join(BROSUR_SAYFALAR, catalogFiles[i]);
    const out = `catalog-${i + 1}`;
    await sharp(inPath).resize({ width: 1600, withoutEnlargement: true }).webp({ quality: 82 }).toFile(path.join(OUT, `${out}.webp`));
    await sharp(inPath).resize({ width: 800, withoutEnlargement: true }).webp({ quality: 74 }).toFile(path.join(OUT, `${out}-sm.webp`));
    console.log("✓ katalog", out, "<-", catalogFiles[i]);
  }

  for (const item of daire) {
    const inPath = path.join(SRC, item.in);
    if (!existsSync(inPath)) {
      console.warn("!! Daire kaynağı bulunamadı:", item.in);
      continue;
    }
    await sharp(inPath).resize({ width: 1920, withoutEnlargement: true }).webp({ quality: 80 }).toFile(path.join(OUT, `${item.out}.webp`));
    await sharp(inPath).resize({ width: 960, withoutEnlargement: true }).webp({ quality: 72 }).toFile(path.join(OUT, `${item.out}-sm.webp`));
    console.log("✓ daire", item.out);
  }

  for (const item of map) {
    const inPath = path.join(SRC, item.in);
    if (!existsSync(inPath)) {
      console.warn("!! Kaynak bulunamadı:", item.in);
      continue;
    }
    // Büyük varyant (max 1920w)
    await sharp(inPath)
      .resize({ width: 1920, withoutEnlargement: true })
      .webp({ quality: 78 })
      .toFile(path.join(OUT, `${item.out}.webp`));
    // Küçük varyant (max 960w) — srcset için
    await sharp(inPath)
      .resize({ width: 960, withoutEnlargement: true })
      .webp({ quality: 72 })
      .toFile(path.join(OUT, `${item.out}-sm.webp`));
    console.log("✓", item.out);
  }

  // OG görseli (1200x630) — entrance-gate'ten
  const ogSrc = path.join(SRC, "WhatsApp Image 2026-07-13 at 00.14.32 (5).jpeg");
  if (existsSync(ogSrc)) {
    await sharp(ogSrc)
      .resize({ width: 1200, height: 630, fit: "cover", position: "centre" })
      .jpeg({ quality: 82 })
      .toFile(path.resolve("public/og-image.jpg"));
    console.log("✓ og-image.jpg");
  }

  // Ocean Gayrimenkul logosu → WebP (beyaz zeminli)
  const logoSrc = path.join(SRC, "hype/oceanlogo.jpeg");
  if (existsSync(logoSrc)) {
    await sharp(logoSrc)
      .resize({ width: 480, withoutEnlargement: true })
      .webp({ quality: 90 })
      .toFile(path.resolve("public/ocean-logo.webp"));
    console.log("✓ ocean-logo.webp");
  }

  console.log("\nTamamlandı → public/images");
}

run().catch((e) => {
  console.error(e);
  process.exit(1);
});
