// Görsel galerisi. Kategori: "dis" (dış mekân), "sosyal", "ic" (iç mekân), "plan".
// Yeni görsel eklemek için diziye ekleyin (önce scripts/optimize-images.mjs ile üretin).

export type GalleryImage = {
  src: string;
  alt: string;
  category: "dis" | "sosyal" | "ic" | "plan";
  wide?: boolean;
};

export const galleryCategories = [
  { key: "all", label: "Tümü" },
  { key: "dis", label: "Dış Mekân" },
  { key: "sosyal", label: "Sosyal Alanlar" },
  { key: "ic", label: "İç Mekân" },
  { key: "plan", label: "Kat Planı" },
] as const;

export const gallery: GalleryImage[] = [
  { src: "/images/entrance-gate.webp", alt: "MİA PARK OCEAN karşılama kapısı ve havuzlu avlu", category: "dis", wide: true },
  { src: "/images/hero-courtyard-dusk.webp", alt: "Palmiyeli yürüyüş yolu ve akşam aydınlatmalı avlu", category: "sosyal", wide: true },
  { src: "/images/courtyard-pools.webp", alt: "Bloklar arasındaki süs havuzları ve palmiyeli peyzaj", category: "sosyal" },
  { src: "/images/aerial-pools.webp", alt: "Bloklar arasındaki süs havuzlarının kuş bakışı görünümü", category: "sosyal" },
  { src: "/images/terrace-pergola.webp", alt: "Pergolalı bahçe terası ve havuz manzarası", category: "sosyal" },
  { src: "/images/balcony-dusk.webp", alt: "Gün batımında aydınlatmalı balkonlar ve kavisli cephe", category: "dis" },
  { src: "/images/facade-warm.webp", alt: "Sıcak aydınlatmalı modern cephe detayı", category: "dis" },
  { src: "/images/street-corner.webp", alt: "Sokak cephesinden proje ve peyzaj görünümü", category: "dis" },
  { src: "/images/interior-living.webp", alt: "Şehir manzaralı modern salon iç mekânı", category: "ic" },
  { src: "/images/interior-bedroom.webp", alt: "Sıcak tonlu modern yatak odası tasarımı", category: "ic" },
  { src: "/images/loft-living.webp", alt: "Ferah salon ve açık mutfak", category: "ic" },
  { src: "/images/duplex-cutaway.webp", alt: "2+1 bahçe dubleks kesit görünümü ve özel bahçe", category: "ic" },
  { src: "/images/ic-mekan/09-loft-salon.webp", alt: "1+1 bahçe loft: çift yükseklikli salon (örnek iç mekân tasarımı)", category: "ic", wide: true },
  { src: "/images/ic-mekan/10-loft-mezanin.webp", alt: "1+1 bahçe loft: mezanin yatak katı (örnek iç mekân tasarımı)", category: "ic" },
  { src: "/images/ic-mekan/11-dubleks-salon.webp", alt: "2+1 bahçe dubleks: bahçeye açılan salon (örnek iç mekân tasarımı)", category: "ic" },
  { src: "/images/ic-mekan/05-1plus1-salon.webp", alt: "1+1 daire salonu (örnek iç mekân tasarımı)", category: "ic" },
  { src: "/images/ic-mekan/07-1plus1-mutfak.webp", alt: "1+1 daire açık mutfak (örnek iç mekân tasarımı)", category: "ic" },
  { src: "/images/ic-mekan/01-1plus0-salon.webp", alt: "1+0 daire açık plan yaşam alanı (örnek iç mekân tasarımı)", category: "ic" },
  { src: "/images/ic-mekan/13-bahceli-daire-terasi.webp", alt: "Bahçeli zemin kat dairenin terası", category: "dis", wide: true },
  { src: "/images/ic-mekan/17-sus-havuzu.webp", alt: "Bloklar arasında aydınlatmalı süs havuzu", category: "sosyal" },
  { src: "/images/ic-mekan/18-yuruyus-yolu.webp", alt: "Peyzajlı yürüyüş yolu ve dinlenme bankları", category: "sosyal" },
  { src: "/images/ic-mekan/19-cocuk-oyun-parki.webp", alt: "Site içi çocuk oyun parkı", category: "sosyal" },
  { src: "/images/plan-1plus0.webp", alt: "1+0 daire örnek kat planı", category: "plan" },
  { src: "/images/plan-1plus1.webp", alt: "1+1 daire örnek kat planı", category: "plan" },
];
