// Proje künyesi ve rakamlar.

export const projectStats = [
  { value: 472, suffix: "", label: "1+0 Daire", note: "brüt 28 m²" },
  { value: 112, suffix: "", label: "1+1 Daire", note: "brüt 50 m²" },
  { value: 16, suffix: "", label: "2+1 Dubleks", note: "brüt 100 m²" },
  { value: 600, suffix: "", label: "Toplam Daire", note: "3 yaşam tipi" },
] as const;

// Öne çıkanlar — ikonlu (Intro bölümü)
export const highlights = [
  { icon: "Building2", text: "600 daire · 3 farklı yaşam tipi" },
  { icon: "Waves", text: "Merkezi avlu, süs havuzları ve geniş peyzaj" },
  { icon: "Flower2", text: "Zeminde bahçeli daire keyfi" },
  { icon: "ShieldCheck", text: "Kapalı otopark ve 7/24 güvenlik" },
  { icon: "Car", text: "D100 karayoluna 1 dakika, şehir merkezine 5 dakika" },
] as const;

export const projectMeta = {
  totalUnits: 600,
  units: { "1+0": 472, "1+1": 112, "2+1": 16 },
  payment: "Tasarrufa dayalı faizsiz finansman · 60 ay vade · %0 faiz",
} as const;
