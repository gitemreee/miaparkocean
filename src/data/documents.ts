// Belge Merkezi — üye portalında yayımlanması öngörülen belgeler.
// Gerçek belgeler kesinleştikçe status "yayimlandi" yapılır ve href eklenir.
// [DOĞRULANACAK: belgelerin nihai sürüm, tarih ve erişim seviyeleri]

export type DocStatus = "yayimlandi" | "hazirlaniyor" | "planlanan";
export type DocAccess = "acik" | "uye";

export type DocItem = {
  title: string;
  desc: string;
  access: DocAccess;
  status: DocStatus;
  version?: string;
  date?: string;
  href?: string;
};

export const docStatusLabels: Record<DocStatus, string> = {
  yayimlandi: "Yayımlandı",
  hazirlaniyor: "Hazırlanıyor",
  planlanan: "Planlanan",
};

export const docAccessLabels: Record<DocAccess, string> = {
  acik: "Herkese Açık",
  uye: "Üyeye Özel",
};

export const documentGroups: { title: string; items: DocItem[] }[] = [
  {
    title: "Kurumsal ve Hukuki",
    items: [
      { title: "Kooperatif Anasözleşmesi", desc: "Kooperatifin kuruluş, yönetim ve ortaklık esasları.", access: "uye", status: "hazirlaniyor" },
      { title: "Ticaret Sicili / MERSİS Kaydı", desc: "Kooperatifin resmi tescil bilgileri.", access: "acik", status: "hazirlaniyor" },
      { title: "Yetki Belgeleri", desc: "Temsil ve imza yetkilerine ilişkin belgeler.", access: "uye", status: "hazirlaniyor" },
    ],
  },
  {
    title: "İnşaat ve İlerleme",
    items: [
      { title: "Hakediş Raporları", desc: "Bağımsız teknik onaya bağlı ödeme raporları.", access: "uye", status: "planlanan" },
      { title: "Aylık İlerleme Raporu", desc: "Planlanan-gerçekleşen ilerleme ve teslim tahmini.", access: "uye", status: "planlanan" },
      { title: "Teknik Şartname", desc: "Malzeme marka/performans kriterleri.", access: "uye", status: "hazirlaniyor" },
    ],
  },
  {
    title: "Genel Kurul",
    items: [
      { title: "Genel Kurul Gündemi ve Çağrı", desc: "Toplantı gündemi ve davet belgeleri.", access: "uye", status: "planlanan" },
      { title: "Genel Kurul Kararları / Tutanaklar", desc: "Alınan kararlar ve hazirun listesi.", access: "uye", status: "planlanan" },
      { title: "Faaliyet Raporu", desc: "Dönemsel yönetim faaliyet raporu.", access: "uye", status: "planlanan" },
    ],
  },
];

export const documentsNote =
  "Belge merkezi, üye portalı üzerinden hizmet vermek üzere hazırlanmaktadır. Belgeler; tür, sürüm, tarih ve erişim seviyesiyle yayımlanacak, güncellik doğrulama notu taşıyacaktır. Erişim seviyeleri ve yayım takvimi proje politikası olarak öngörülmektedir.";
