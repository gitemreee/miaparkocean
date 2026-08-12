#!/usr/bin/env node
/**
 * IndexNow gönderimi — Bing, Yandex ve Seznam'a yeni/güncellenen sayfaları
 * anında bildirir. (Google IndexNow'ı desteklemez; oraya sitemap + Search
 * Console üzerinden gidilir.)
 *
 * Kullanım:
 *   npm run build          # önce out/sitemap.xml üretilmeli
 *   node scripts/indexnow.mjs            # sitemap'teki tüm URL'ler
 *   node scripts/indexnow.mjs /bolgeler/ /bolgeler/izmit-yahya-kaptan/
 *
 * Anahtar dosyası public/<key>.txt olarak yayınlanır ve içeriği anahtarın
 * kendisidir; IndexNow doğrulaması bu dosyayı okur.
 */

import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import path from "node:path";

const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const HOST = "miaparkocean.com";
const KEY = "8f3c1d7a49b24e6f9a0c5e2b7d18f4a6";
const ENDPOINT = "https://api.indexnow.org/IndexNow";

async function urlsFromSitemap() {
  const xml = await readFile(path.join(ROOT, "out", "sitemap.xml"), "utf8");
  return [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);
}

const args = process.argv.slice(2);
const urlList = args.length
  ? args.map((a) => (a.startsWith("http") ? a : `https://${HOST}${a.startsWith("/") ? a : `/${a}`}`))
  : await urlsFromSitemap();

if (!urlList.length) {
  console.error("Gönderilecek URL bulunamadı. Önce `npm run build` çalıştırın.");
  process.exit(1);
}

console.log(`IndexNow: ${urlList.length} URL gönderiliyor…`);

const res = await fetch(ENDPOINT, {
  method: "POST",
  headers: { "Content-Type": "application/json; charset=utf-8" },
  body: JSON.stringify({
    host: HOST,
    key: KEY,
    keyLocation: `https://${HOST}/${KEY}.txt`,
    urlList,
  }),
});

// 200 = kabul edildi, 202 = kabul edildi (anahtar doğrulaması sürüyor)
if (res.ok || res.status === 202) {
  console.log(`✓ Gönderildi (HTTP ${res.status}). Bing/Yandex birkaç saat içinde tarar.`);
} else {
  console.error(`✗ Başarısız (HTTP ${res.status}): ${await res.text()}`);
  process.exit(1);
}
