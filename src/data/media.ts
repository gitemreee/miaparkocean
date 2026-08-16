// Online katalog sayfaları ve tanıtım filmi yapılandırması.

// Katalog görselleri sürümü — broşür sayfaları değişince artır.
// /images/* immutable (1 yıl) cache'lendiği için, aynı dosya adıyla içerik değişince
// eski sürüm tarayıcıda kalır; ?v= ile yeni URL üretip cache-bust ederiz.
const CATALOG_V = "5";
export const catalogPages = [
  { src: `/images/catalog-1.webp?v=${CATALOG_V}`, label: "Kapak" },
  { src: `/images/catalog-2.webp?v=${CATALOG_V}`, label: "Proje" },
  { src: `/images/catalog-3.webp?v=${CATALOG_V}`, label: "Finansman" },
  { src: `/images/catalog-4.webp?v=${CATALOG_V}`, label: "Daire Tipleri" },
  { src: `/images/catalog-5.webp?v=${CATALOG_V}`, label: "1+0 Daire" },
  { src: `/images/catalog-6.webp?v=${CATALOG_V}`, label: "1+1 Daire" },
  { src: `/images/catalog-7.webp?v=${CATALOG_V}`, label: "1+1 Bahçe Loft" },
  { src: `/images/catalog-8.webp?v=${CATALOG_V}`, label: "2+1 Bahçe Dubleks" },
  { src: `/images/catalog-9.webp?v=${CATALOG_V}`, label: "Sosyal Yaşam" },
  { src: `/images/catalog-10.webp?v=${CATALOG_V}`, label: "Lokasyon & İletişim" },
];

// Katalog PDF'i public/ altına konur. Yoksa buton gizlenir.
export const catalogPdf = "/mia-park-ocean-katalog.pdf";

// Tanıtım filmi.
//
// `file` sitede barındırılan mp4'tür ve varsayılan budur; ziyaretçi oynat
// tuşuna basmadan tek bayt inmez (preload="none"). Sürüm 25 MB'lık paylaşım
// kopyası — 1080p ama 1.7 Mbit/sn, mobilde de akıyor. 70 MB'lık master
// public/videos/mia-park-ocean-tanitim.mp4 olarak duruyor, siteye konmuyor.
//
// İleride YouTube'a yüklenirse `url`'i doldurmak yeterli; embed öne geçer
// ve izlenme sayısı YouTube tarafında toplanır.
export const promoVideo = {
  file: "/videos/mia-park-ocean-tanitim-web.mp4",
  url: "",
  poster: "/images/film-poster.webp",
  title: "MİA PARK OCEAN Tanıtım Filmi",
  caption: "İki dakikada proje: mimari, daire tipleri, konum ve ödeme modeli",
  duration: "2:00",
};
