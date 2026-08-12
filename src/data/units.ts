// Daire tipleri. Yeni tip eklemek veya özellik güncellemek için bu diziyi düzenleyin.

export type Unit = {
  slug: string;
  type: string;
  name: string;
  count: number;
  area: string;
  areaValue: number;
  tagline: string;
  summary: string;
  features: string[];
  highlights: { title: string; text: string }[];
  image: string;
  planImage: string;
  interiorImages: string[];
};

export const units: Unit[] = [
  {
    slug: "1-plus-0",
    type: "1+0",
    name: "1+0 Daireler",
    count: 472,
    area: "Brüt 28 m²",
    areaValue: 28,
    tagline: "Akıllı Tasarım, Maksimum Konfor",
    summary:
      "Yaşam alanı, mutfak ve balkonun tek bir ferah düzende buluştuğu 1+0 daireler, ilk evini alanlar ve yatırım yapmak isteyenler için pratik bir seçenek. Küçük ama nefes alan, bakımı kolay bir ev.",
    features: [
      "Açık plan ferah yaşam alanı",
      "Geniş balkon",
      "Modern mutfak tasarımı",
      "Yüksek kaliteli iç mekân malzemeleri",
      "Yatırım için ideal seçenek",
    ],
    highlights: [
      { title: "Ferah Yaşam Alanı", text: "Açık plan tasarımı ile aydınlık ve konforlu bir yaşam." },
      { title: "Balkon Keyfi", text: "Geniş balkonu ile doğayla iç içe bir yaşam alanı." },
      { title: "Modern Mutfak", text: "Fonksiyonel mutfak alanı ile pratik ve estetik kullanım." },
      { title: "Yatırıma Uygun", text: "Kompakt planı ve merkezî konumuyla değerlenmeye ve kiralamaya uygun bir seçenek." },
    ],
    image: "/images/unit-1plus0-a.webp",
    planImage: "/images/unit-1plus0-plan.webp",
    interiorImages: ["/images/unit-1plus0-a.webp", "/images/unit-1plus0-b.webp"],
  },
  {
    slug: "1-plus-1",
    type: "1+1",
    name: "1+1 Daireler",
    count: 96,
    area: "Brüt 50 m²",
    areaValue: 50,
    tagline: "Ferah, Konforlu ve Fonksiyonel",
    summary:
      "Yatak odasının yaşam alanından ayrıldığı 1+1 daireler, hem yalnız hem de çift yaşayanlar için rahat bir düzen kuruyor. Geniş balkonu ve açık mutfağıyla gün boyu ferah kalıyor.",
    features: [
      "Açık plan ferah yaşam alanı",
      "Geniş balkon",
      "Modern mutfak tasarımı",
      "Yüksek kaliteli iç mekân",
      "Yatırım için ideal seçenek",
    ],
    highlights: [
      { title: "Geniş Yaşam Alanı", text: "Ferahlık hissettiren açık plan tasarım." },
      { title: "Büyük Balkon", text: "Geniş balkonlar ile keyifli bir yaşam alanı." },
      { title: "Modern Mutfak", text: "Fonksiyonel mutfak alanı ile pratik ve estetik kullanım." },
      { title: "Ayrı Yatak Odası", text: "Yatak odasının yaşam alanından ayrılması düzenli ve konforlu bir kullanım sağlar." },
    ],
    image: "/images/unit-1plus1-a.webp",
    planImage: "/images/unit-1plus1-plan.webp",
    interiorImages: ["/images/unit-1plus1-a.webp", "/images/unit-1plus1-b.webp", "/images/unit-1plus1-c.webp"],
  },
  {
    slug: "1-plus-1-bahce-loft",
    type: "1+1",
    name: "1+1 Bahçe Loft",
    count: 16,
    area: "Brüt 50 m²",
    areaValue: 50,
    tagline: "Zemin Katta Kendi Bahçeniz",
    summary:
      "1+1 dairenin aynı ferah planı, bu kez zemin katta ve kendine ait özel bahçesiyle. Loft kurgusu yaşam alanını yükselterek genişletiyor; bahçeye açılan camlar sabah kahvesini dışarı taşıyor.",
    features: [
      "Özel kullanım bahçesi",
      "Loft kurgulu yüksek tavan",
      "Zeminden bahçeye direkt erişim",
      "Ayrı yatak odası",
      "Modern mutfak tasarımı",
      "Bahçeye açılan geniş camlar",
    ],
    highlights: [
      { title: "Özel Kullanım Bahçesi", text: "Zemin kata ait, yalnızca size özel bahçe alanı." },
      { title: "Loft Ferahlığı", text: "Yükseltilmiş tavanıyla aynı m²'de belirgin şekilde daha ferah bir his." },
      { title: "Bahçeye Direkt Çıkış", text: "Yaşam alanından bir adımda bahçeye; iç ve dış mekân tek parça." },
      { title: "Ayrı Yatak Odası", text: "Yatak odasının ayrılması düzenli ve konforlu bir kullanım sağlar." },
    ],
    image: "/images/loft-living.webp",
    planImage: "/images/unit-1plus1-plan.webp",
    interiorImages: ["/images/loft-living.webp", "/images/unit-1plus1-a.webp", "/images/unit-1plus1-c.webp"],
  },
  {
    slug: "2-plus-1-bahce-dubleks",
    type: "2+1",
    name: "2+1 Bahçe Dubleks",
    count: 16,
    area: "Brüt 100 m²",
    areaValue: 100,
    tagline: "Bahçeniz, Evinizin Devamı",
    summary:
      "İki katlı kurgusu ve zemindeki özel bahçesiyle 2+1 dubleks, apartman içinde müstakil ev keyfi veriyor. Geniş sürme camlar ve bahçeye açılan yaşam alanı aileler düşünülerek planlandı.",
    features: [
      "Özel kullanım bahçesi",
      "İki katlı dubleks yaşam",
      "Geniş sürme camlar",
      "İç–dış mekân bütünlüğü",
      "Pergola ile gölgeli oturma alanı",
      "Zeminden bahçeye direkt erişim",
      "Aile yaşamına uygun ferah kurgu",
    ],
    highlights: [
      { title: "Özel Kullanım Bahçesi", text: "Size özel geniş bahçe alanı ile doğanın içinde kalın." },
      { title: "İki Katlı Dubleks", text: "Alt katta yaşam, üst katta yatak katı; ferah ve ayrışmış bir plan." },
      { title: "Geniş Sürme Camlar", text: "Doğal ışığı içeri davet eden modern tasarım." },
      { title: "İç–Dış Mekân Bütünlüğü", text: "Bahçeniz ve yaşam alanınız kusursuz biçimde bütünleşir." },
    ],
    image: "/images/unit-2plus1-a.webp",
    planImage: "/images/unit-2plus1-cutaway.webp",
    interiorImages: ["/images/unit-2plus1-a.webp", "/images/unit-2plus1-b.webp", "/images/unit-2plus1-c.webp", "/images/unit-2plus1-d.webp"],
  },
];
