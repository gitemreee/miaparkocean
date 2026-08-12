// Lansman & Basın Toplantısı — davetiye sayfası, QR etiketi ve baskı
// çıktılarının tek kaynağı. Etkinlik bilgisi değişirse yalnızca burayı düzenleyin.

export const launchEvent = {
  kicker: "Davetlisiniz",
  name: "Lansman & Basın Toplantısı",
  project: "MİA PARK OCEAN",
  region: "İzmit MİA Bölgesi",

  // Tarih/saat
  dateLabel: "21 Ağustos 2026",
  dayLabel: "Cuma",
  timeLabel: "10:00",
  /** ISO 8601 — JSON-LD ve takvim bağlantıları için (TRT, UTC+3) */
  startsAt: "2026-08-21T10:00:00+03:00",
  endsAt: "2026-08-21T13:00:00+03:00",

  // Yer
  venue: "Emex Otel",
  city: "Kocaeli",
  venueAddress: "Emex Otel, Kocaeli",
  venueMaps: "https://www.google.com/maps/search/?api=1&query=Emex+Otel+Kocaeli",

  // Etkinlik iletişimi (davetiye ve RSVP bu numaraya gider)
  host: { name: "Gül Hanım", phoneLabel: "0534 859 26 72", phone: "+905348592672", wa: "905348592672" },

  invitationText:
    "İzmit'in yeni incisi MİA PARK OCEAN'ın lansmanına davetlisiniz. Ocean Gayrimenkul güvencesiyle, İzmit MİA Bölgesi'nde hayata geçecek projemizi; modern mimarisi, depreme dayanıklı yapısı ve tasarrufa dayalı faizsiz finansman modeliyle sizlere tanıtmaktan mutluluk duyacağız.",

  programme: [
    { time: "10:00", title: "Karşılama ve ikram" },
    { time: "10:30", title: "Proje sunumu ve tanıtım filmi" },
    { time: "11:15", title: "Kooperatif modeli ve finansman" },
    { time: "11:45", title: "Soru-cevap" },
    { time: "12:15", title: "Kokteyl ve birebir görüşmeler" },
  ],
} as const;

/** QR kodlarının işaret ettiği adresler. */
export const qrTargets = {
  davetiye: "https://miaparkocean.com/davetiye/",
  basin: "https://miaparkocean.com/basin-aciklamasi/",
} as const;
