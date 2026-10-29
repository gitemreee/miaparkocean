// MİA Bölgesi (Sanayi Mah.) değerleme + demografi.
// Güncel m² 89.000 ₺; 5 yıllık projeksiyon yıllık %25 bileşik büyüme ile.
// Projeksiyon öngörüdür; kesin taahhüt içermez.

export const regionLabel = "MİA Bölgesi (Sanayi Mah.)";

export const valuation = {
  eyebrow: "Bölge Değerleme",
  title: "MİA Bölgesi'nde değer artış öngörüsü",
  lead: "MİA Bölgesi (Sanayi Mah.) güçlü bir değer artışı yaşıyor. Yıllık %25 artış varsayımıyla bugünkü m² değeri 5 yılda yaklaşık 3 katına çıkabilir (öngörü).",
  source: "m² verisi: Endeksa, 2026 · 5 yıllık projeksiyon: %25 yıllık artış varsayımı",
  asOf: "2026",

  // Dev başlık — güncel m² değeri
  headline: { value: "89.000", unit: "₺/m²", label: "MİA Bölgesi (Sanayi Mah.) güncel m² birim fiyatı" },

  // Öngörü rozeti
  forecast: { value: "%25", label: "yıllık öngörülen değer artışı" },

  // Değer artışı vurgu metrikleri
  changes: [
    { value: "%25", label: "Yıllık Değer Artışı", note: "öngörülen bileşik büyüme" },
    { value: "+%205", label: "5 Yılda Toplam Artış", note: "%25 yıllık bileşik" },
    { value: "≈×3", label: "5 Yıl Sonra (Öngörü)", note: "89.000 → 271.606 ₺/m²" },
  ],

  // 5 yıllık projeksiyon — 89.000 ₺, yıllık %25 büyüme (bar yükseklikleri değere orantılı)
  projection: [
    { year: "2026", price: "89.000", h: 33, label: "Bugün" },
    { year: "2027", price: "111.250", h: 41 },
    { year: "2028", price: "139.063", h: 51 },
    { year: "2029", price: "173.828", h: 64 },
    { year: "2030", price: "217.285", h: 80 },
    { year: "2031", price: "271.606", h: 100, label: "+5 Yıl" },
  ],
  projectionNote:
    "5 yıllık projeksiyon, yıllık %25 değer artışı varsayımına dayalı bir öngörüdür; kesin bir değer taahhüdü içermez.",
};

// MİA Bölgesi demografisi — Endeksa bölge (İzmit) verileri
export const demographics = {
  eyebrow: "Bölge Demografisi",
  title: "İzmit'in insan haritası",
  lead: "İzmit'in genç ve dinamik bir nüfusu var; bu da konut talebini sürekli canlı tutuyor.",
  source: "Kaynak: Endeksa · İzmit / Kocaeli (bölge verileri)",
  tiles: [
    { value: "380.831", label: "İzmit Nüfusu", note: "kişi" },
    { value: "≈784", label: "Nüfus Yoğunluğu", note: "kişi/km²" },
    { value: "%85", label: "Genç + Orta Yaş", note: "genç %34,6 · orta %50,5" },
    { value: "%50,8", label: "Kadın Nüfus", note: "erkek %49,2" },
  ],
  ageBands: [
    { band: "Genç", percent: 34.64 },
    { band: "Orta", percent: 50.49 },
    { band: "Yaşlı", percent: 14.87 },
  ],
};
