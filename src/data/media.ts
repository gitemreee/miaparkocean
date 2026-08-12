// Online katalog sayfaları ve tanıtım filmi yapılandırması.

// Katalog görselleri sürümü — broşür sayfaları değişince artır.
// /images/* immutable (1 yıl) cache'lendiği için, aynı dosya adıyla içerik değişince
// eski sürüm tarayıcıda kalır; ?v= ile yeni URL üretip cache-bust ederiz.
const CATALOG_V = "4";
export const catalogPages = [
  { src: `/images/catalog-1.webp?v=${CATALOG_V}`, label: "Kapak" },
  { src: `/images/catalog-2.webp?v=${CATALOG_V}`, label: "Proje" },
  { src: `/images/catalog-3.webp?v=${CATALOG_V}`, label: "Finansman" },
  { src: `/images/catalog-4.webp?v=${CATALOG_V}`, label: "Daire Tipleri" },
  { src: `/images/catalog-5.webp?v=${CATALOG_V}`, label: "1+0 Daire" },
  { src: `/images/catalog-6.webp?v=${CATALOG_V}`, label: "1+1 Daire" },
  { src: `/images/catalog-7.webp?v=${CATALOG_V}`, label: "2+1 Bahçe Dubleks" },
  { src: `/images/catalog-8.webp?v=${CATALOG_V}`, label: "Sosyal Yaşam" },
  { src: `/images/catalog-9.webp?v=${CATALOG_V}`, label: "Lokasyon & Değerleme" },
  { src: `/images/catalog-10.webp?v=${CATALOG_V}`, label: "İletişim" },
];

// Katalog PDF'i public/ altına konur. Yoksa buton gizlenir.
export const catalogPdf = "/mia-park-ocean-katalog.pdf";

// Tanıtım filmi: YouTube/Vimeo embed URL'si gelince `url` doldurulur.
// Örn: "https://www.youtube.com/embed/VIDEO_ID"
// [DOĞRULANACAK: tanıtım filmi bağlantısı]
export const promoVideo = {
  url: "",
  poster: "/images/balcony-dusk.webp",
  title: "MİA PARK OCEAN Tanıtım Filmi",
  caption: "Projeyi hareketli görüntülerle keşfedin",
};
