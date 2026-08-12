// Site geneli sabit bilgiler. Yeni iletişim kanalı / menü öğesi eklemek için burayı düzenleyin.

export const site = {
  name: "MİA PARK OCEAN",
  shortName: "MİA PARK OCEAN",
  region: "İzmit MİA Bölgesi",
  city: "Kocaeli",
  domain: "miaparkocean.com",
  url: "https://miaparkocean.com",
  tagline: "Lüks Artık Ulaşılabilir.",
  description:
    "İzmit MİA Bölgesi'nde 600 daireden oluşan modern yaşam projesi. Tasarrufa dayalı faizsiz finansman, 60 ay vade ve %0 faiz ile MİA PARK OCEAN.",
  developer: "S.S. Yahya Kaptan Birlik Yapı Kooperatifi",
  seller: "Ocean Gayrimenkul",
  sellerRole: "Tek Yetkili Satıcı",
} as const;

export const contact = {
  phones: [
    { label: "0540 028 00 41", href: "tel:+905400280041" },
    { label: "0541 128 40 41", href: "tel:+905411284041" },
  ],
  whatsapp: {
    label: "WhatsApp'tan Yazın",
    href: "https://wa.me/905400280041",
  },
  email: "info@oceangayrimenkul41.com",
  website: "www.oceangayrimenkul41.com",
  websiteHref: "https://www.oceangayrimenkul41.com",
  address: {
    lines: [
      "Ömerağa Mah. Abdurrahman Yüksel Cad.",
      "Bana Bak Ap. No:15/4",
      "İzmit / Kocaeli",
    ],
    // Satış ofisi harita bağlantıları. [DOĞRULANACAK: kesin pin konumu]
    googleMaps:
      "https://www.google.com/maps/search/?api=1&query=Ömerağa+Mah.+Abdurrahman+Yüksel+Cad.+İzmit+Kocaeli",
    yandexMaps:
      "https://yandex.com.tr/harita/?text=Ömerağa%20Mah.%20Abdurrahman%20Yüksel%20Cad.%20İzmit%20Kocaeli",
  },
} as const;

export const socials = [
  { name: "Instagram", handle: "/miaparkocean", href: "https://instagram.com/miaparkocean", icon: "instagram" },
  { name: "Facebook", handle: "/miaparkocean", href: "https://facebook.com/miaparkocean", icon: "facebook" },
  { name: "YouTube", handle: "/miaparkocean", href: "https://youtube.com/@miaparkocean", icon: "youtube" },
] as const;

export const nav = [
  { label: "Daireler", href: "/daireler" },
  { label: "Neden Kooperatif?", href: "/kooperatif" },
  { label: "Bilgi Merkezi", href: "/bilgi-merkezi" },
  { label: "Belgeler", href: "/belgeler" },
  { label: "Bölgeler", href: "/bolgeler" },
  { label: "İletişim", href: "/iletisim" },
] as const;

// İkincil bağlantılar (footer)
export const secondaryNav = [
  { label: "Galeri", href: "/galeri" },
  { label: "İzmit MİA Bölgesi", href: "/bolge" },
  { label: "Online Katalog", href: "/#katalog" },
  { label: "Belgeler", href: "/belgeler" },
  { label: "Güven ve Denetim", href: "/kooperatif#guvence-sistemi" },
  { label: "KVKK", href: "/kvkk" },
  { label: "Çerez Politikası", href: "/cerez-politikasi" },
] as const;
