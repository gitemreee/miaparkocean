// Lokasyon avantajları ve mesafeler. Broşür haritasından alınmıştır.

export type Distance = {
  icon: string;
  place: string;
  time: string;
};

export const distances: Distance[] = [
  { icon: "Car", place: "D100 Karayolu", time: "1 dk" },
  { icon: "Waves", place: "İzmit Sahili", time: "2 dk" }, // [DOĞRULANACAK: kesin süre]
  { icon: "ShoppingBag", place: "41 Burada AVM", time: "3 dk" },
  { icon: "Building2", place: "Şehir Merkezi", time: "5 dk" },
  { icon: "HeartPulse", place: "Şehir Hastanesi", time: "5 dk" },
  { icon: "Milestone", place: "TEM Otoyolu", time: "5 dk" },
  { icon: "ShoppingBag", place: "Symbol AVM", time: "7 dk" },
  { icon: "GraduationCap", place: "Kocaeli Üniversitesi", time: "10 dk" },
];

export const locationIntro =
  "MİA PARK OCEAN, İzmit'in en değerli gelişim aksı MİA Bölgesi'nde yer alıyor. Üniversitelere, hastanelere, alışveriş merkezlerine ve ana yollara buradan dakikalar içinde ulaşıyorsunuz.";

export const locationTags = [
  "Merkezi Konum",
  "Kolay Ulaşım",
  "Yatırım Bölgesi",
  "Değer Kazanan Lokasyon",
];

// Proje konumu — kullanıcı tarafından paylaşılan Google Maps koordinatı
// 40°44'12.0"N 29°56'41.6"E · Plus Code: PWPV+MX6 İzmit, Kocaeli
export const mapConfig = {
  lat: 40.736667,
  lng: 29.944889,
  plusCode: "PWPV+MX6 İzmit",
  label: "MİA PARK OCEAN · İzmit MİA Bölgesi",
  embed: "https://www.google.com/maps?q=40.736667,29.944889&z=15&hl=tr&output=embed",
  googleDirections: "https://www.google.com/maps/dir/?api=1&destination=40.736667,29.944889",
  googleView: "https://www.google.com/maps/search/?api=1&query=40.736667,29.944889",
  yandex: "https://yandex.com.tr/harita/?ll=29.944889%2C40.736667&z=15&pt=29.944889%2C40.736667%2Cpm2rdm",
};
