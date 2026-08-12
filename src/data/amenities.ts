// Sosyal yaşam ve donatılar. Yeni özellik eklemek için diziye ekleyin.

export type Amenity = {
  icon: string; // lucide-react ikon adı
  title: string;
  text: string;
};

export const amenities: Amenity[] = [
  { icon: "Trees", title: "Geniş Peyzaj Alanları", text: "Yıl boyu yeşil kalan, bakımı düşünülmüş geniş peyzaj alanları." },
  { icon: "Waves", title: "Dekoratif Süs Havuzları", text: "Avlunun ortasında, sesiyle bile insanı sakinleştiren süs havuzları." },
  { icon: "Footprints", title: "Yürüyüş ve Dinlenme Yolları", text: "Sabah koşusu ya da akşam yürüyüşü için ayrılmış geniş yollar." },
  { icon: "Sparkles", title: "Merkezi Avlu", text: "Komşularla karşılaştığınız, çocukların rahatça oynadığı bir avlu." },
  { icon: "Lamp", title: "Özel Gece Aydınlatması", text: "Akşam olunca devreye giren LED aydınlatmayla bambaşka bir görünüm." },
  { icon: "Flower2", title: "Bahçeli Zemin Daireler", text: "Zemin kattaki bahçeli dairelerle apartmanda müstakil ev hissi." },
  { icon: "Car", title: "Kapalı Otopark", text: "Aracınızı güvenle bırakabileceğiniz geniş kapalı otopark." },
  { icon: "ShieldCheck", title: "7/24 Güvenlik", text: "Gece gündüz kesintisiz güvenlik; aklınız arkada kalmıyor." },
  { icon: "Dumbbell", title: "Sosyal ve Spor Alanları", text: "Spor yapmak, dinlenmek ve vakit geçirmek için ayrılmış alanlar." },
  { icon: "Baby", title: "Çocuk Oyun Parkı", text: "Çocukların güvenle oynayabileceği, gözünüzün önünde bir oyun alanı." },
];
