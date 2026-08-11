// "Değerlenen Bölge: İzmit MİA" içeriği ve "Basında MİA" haber kartları.
// Yeni haber eklemek için press dizisine tek bir nesne ekleyin.

export const regionIntro = {
  title: "Değerlenen Bölge: İzmit MİA",
  lead: "Doğru yerden, doğru zamanda.",
  paragraphs: [
    "İzmit MİA Bölgesi, şehrin yeni gelişim aksı. D100 karayoluna 1 dakika, TEM Otoyolu ve şehir merkezine 5 dakika uzaklıkta. Üniversite, şehir hastanesi ve alışveriş merkezleri de yakında; bu yüzden bölge hem yaşamak hem de yatırım yapmak isteyenlerin ilgisini çekiyor.",
    "Kocaeli'nin güçlü sanayisi ve istihdamı, bölgedeki nitelikli konut talebini sürekli canlı tutuyor. Yeni konut projeleriyle büyüyen MİA aksı, altyapı ve ulaşım yatırımları arttıkça değer kazanmaya devam ediyor.",
    "MİA PARK OCEAN da tam bu gelişen aksın merkezinde yükseliyor. Modern mimarisi ve geniş sosyal alanlarıyla bölgenin en dikkat çeken projelerinden biri.",
  ],
  advantages: [
    { title: "Gelişen Aks", text: "İzmit'in yeni yaşam ve yatırım merkezi." },
    { title: "Güçlü Ulaşım", text: "D100'e 1 dk, TEM'e 5 dk. Ana yollara birkaç dakikada çıkarsınız." },
    { title: "Yakın Donatılar", text: "Üniversite, şehir hastanesi ve AVM'ler hep yakınınızda." },
    { title: "Yatırım Potansiyeli", text: "Talebin canlı olduğu, değeri artan bir bölge." },
  ],
};

export type PressItem = {
  title: string;
  source: string;
  date: string;
  href: string;
  verified: boolean; // false ise link/başlık doğrulanacak
};

// NOT: Aşağıdaki kartlar bölgenin gündemine örnek başlıklardır.
// Gerçek haber bağlantıları eklendikçe href ve verified alanları güncellenecek.
// [DOĞRULANACAK: gerçek haber başlıkları ve linkleri]
export const press: PressItem[] = [
  {
    title: "İzmit MİA Bölgesi yeni yaşam aksı olarak öne çıkıyor",
    source: "Bölge Haber",
    date: "2026",
    href: "#",
    verified: false,
  },
  {
    title: "Kocaeli'de konut talebi gelişen bölgelere yöneliyor",
    source: "Emlak Gündem",
    date: "2026",
    href: "#",
    verified: false,
  },
  {
    title: "Ulaşım yatırımları İzmit'in yeni gelişim bölgelerini büyütüyor",
    source: "Kent Bülteni",
    date: "2026",
    href: "#",
    verified: false,
  },
];
