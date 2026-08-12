// Proje künyesi ve rakamlar.
//
// Daire adetleri units.ts'ten türetilir — elle yazılmaz. Yeni bir daire tipi
// eklendiğinde ya da adet değiştiğinde buradaki rakamlar kendiliğinden güncellenir.

import { units } from "./units";

export const totalUnits = units.reduce((n, u) => n + u.count, 0);

// Sayaç şeridindeki kısa etiketler (tam ad yerine)
const SHORT_LABEL: Record<string, string> = {
  "1-plus-0": "1+0 Daire",
  "1-plus-1": "1+1 Daire",
  "1-plus-1-bahce-loft": "1+1 Bahçe Loft",
  "2-plus-1-bahce-dubleks": "2+1 Bahçe Dubleks",
};

export const projectStats = [
  ...units.map((u) => ({
    value: u.count,
    suffix: "",
    label: SHORT_LABEL[u.slug] ?? u.name,
    note: u.area.toLowerCase(),
  })),
  { value: totalUnits, suffix: "", label: "Toplam Daire", note: `${units.length} yaşam tipi` },
];

// Öne çıkanlar — ikonlu (Intro bölümü)
export const highlights = [
  { icon: "Building2", text: `${totalUnits} daire · ${units.length} farklı yaşam tipi` },
  { icon: "Waves", text: "Merkezi avlu, süs havuzları ve geniş peyzaj" },
  { icon: "Flower2", text: "Zeminde bahçeli daire keyfi" },
  { icon: "ShieldCheck", text: "Kapalı otopark ve 7/24 güvenlik" },
  { icon: "Car", text: "D100 karayoluna 1 dakika, şehir merkezine 5 dakika" },
];

export const projectMeta = {
  totalUnits,
  units: Object.fromEntries(units.map((u) => [u.name, u.count])),
  payment: "Tasarrufa dayalı faizsiz finansman · 60 ay vade · %0 faiz",
} as const;
