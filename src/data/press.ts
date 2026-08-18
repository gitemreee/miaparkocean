// Basında biz — projeyi haber yapan yayınlar.
//
// Yeni bir haber eklemek için diziye bir satır ekleyin; kart kendiliğinden
// çıkar. Sıralama dizideki sırayla aynıdır (en üstte en güncel).
//
// `excerpt` haberin kendi spot/özet cümlesinden alınır — kendi cümlemizi
// gazeteye söyletmeyiz. Kart tıklanınca haberin kendi sayfası açılır.

export type PressItem = {
  slug: string;        // varlık dosyalarının adı
  outlet: string;      // yayın adı
  title: string;       // haberin başlığı (gazetedeki haliyle)
  url: string;         // haberin kendi sayfası
  date: string;        // ISO — yayın tarihi
  dateLabel: string;   // ekranda görünen tarih
  excerpt: string;     // haberin spotundan alıntı
};

// Görseller ve logolar bir kez indirilip WebP/PNG olarak kendi sunucumuzda
// tutulur — scripts/build-press-assets.py üretir. Gazetenin sunucusuna
// bağlamıyoruz: adres değişince kart boşalırdı.
const asset = (slug: string) => ({
  image: `/images/basin/haber-${slug}.webp`,
  imageSmall: `/images/basin/haber-${slug}-sm.webp`,
  logo: `/images/basin/logo-${slug}.png`,
});

export const pressAsset = asset;

export const pressItems: PressItem[] = [
  {
    slug: "kocaeligazetesi",
    outlet: "Kocaeli Gazetesi",
    title: "Mia Park Ocean tanıtıldı: 600 konutluk projede faizsiz ödeme modeli",
    url: "https://www.kocaeligazetesi.com.tr/haber/28539382/mia-park-ocean-tanitildi-600-konutluk-projede-faizsiz-odeme-modeli",
    date: "2026-08-18",
    dateLabel: "18 Ağustos 2026",
    excerpt:
      "10 dönümlük arazi üzerinde inşa edilecek 600 konutluk projede faizsiz ve ara ödemesiz ödeme modeli uygulanacak.",
  },
  {
    slug: "ozgunkocaeli",
    outlet: "Özgün Kocaeli",
    title: "Kocaeli'ye 600 dairelik yeni proje: MİA Park Ocean'da fiyatlar belli oldu",
    url: "https://www.ozgunkocaeli.com.tr/kocaeliye-600-dairelik-yeni-proje-mia-park-oceanda-fiyatlar-belli-oldu",
    date: "2026-08-18",
    dateLabel: "18 Ağustos 2026",
    excerpt:
      "Kocaeli'nin MİA bölgesinde inşa edilecek 600 rezidans dairesinden oluşan MİA Park Ocean projesi kamuoyuna tanıtıldı.",
  },
  {
    slug: "ilkekocaeli",
    outlet: "İlke Kocaeli",
    title: "Mia Park Ocean Kocaeli'de tanıtıldı: 600 rezidans için fiyatlar belli oldu",
    url: "https://www.ilkekocaeli.com/gundem/249079-mia-park-ocean-kocaelide-tanitildi-600-rezidans-icin-fiyatlar-belli-oldu/",
    date: "2026-08-18",
    dateLabel: "18 Ağustos 2026",
    excerpt:
      "10 dönümlük arazi üzerinde yükselecek projede 600 rezidans yer alırken, daire fiyatları ve ödeme seçenekleri de açıklandı.",
  },
  {
    slug: "kocaeligundem",
    outlet: "Kocaeli Gündem",
    title: "Kocaeli MİA Bölgesine 600 dairelik dev proje: MİA Park Ocean'da fiyatlar belli oldu",
    url: "https://kocaeligundem.com/haber/28540878/kocaeli-mia-bolgesine-600-dairelik-dev-proje-mia-park-oceanda-fiyatlar-belli-oldu",
    date: "2026-08-18",
    dateLabel: "18 Ağustos 2026",
    excerpt:
      "Kocaeli'nin yatırım ve cazibe merkezi haline gelen MİA bölgesinde hayata geçirilecek proje lansman öncesinde kamuoyuna tanıtıldı.",
  },
  {
    slug: "kocaelifikir",
    outlet: "Kocaeli Fikir",
    title: "MİA Park Ocean'da fiyatlar açıklandı",
    url: "https://www.kocaelifikir.com/haber/28540941/mia-park-oceanda-fiyatlari-aciklandi",
    date: "2026-08-18",
    dateLabel: "18 Ağustos 2026",
    excerpt:
      "600 dairelik MİA Park Ocean projesinde lansmana özel fiyatlar ve ödeme seçenekleri açıklandı.",
  },
  {
    slug: "kocaelikoz",
    outlet: "Kocaeli Koz",
    title: "600 dairelik dev proje! MİA Park Ocean'da fiyatlar açıklandı",
    url: "https://www.kocaelikoz.com/haber/28541009/600-dairelik-dev-proje-mia-park-oceanda-fiyatlar-aciklandi",
    date: "2026-08-18",
    dateLabel: "18 Ağustos 2026",
    excerpt:
      "MİA Park Ocean projesi lansman öncesinde kent kamuoyuna tanıtıldı; nakit ve vadeli ödeme seçenekleriyle fiyatlar netleşti.",
  },
];

export const pressIntro =
  "MİA PARK OCEAN'ın tanıtım toplantısı Kocaeli basınında geniş yer buldu. Haberlerin tamamı yayınların kendi sayfalarında; başlığa dokunun, kaynağına gidin.";
