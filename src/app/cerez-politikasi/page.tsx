import type { Metadata } from "next";
import Link from "next/link";
import { site, contact } from "@/data/site";

export const metadata: Metadata = {
  alternates: { canonical: "/cerez-politikasi/" },
  title: "Çerez Politikası",
  description:
    "MİA PARK OCEAN internet sitesinde kullanılan çerezler, türleri ve çerez tercihlerinizi nasıl yönetebileceğinize dair bilgilendirme.",
  robots: { index: false, follow: true },
};

const sections = [
  {
    h: "1. Çerez Nedir?",
    p: [
      "Çerezler, ziyaret ettiğiniz internet siteleri tarafından tarayıcınıza kaydedilen küçük metin dosyalarıdır. Sitenin doğru çalışmasını sağlar, tercihlerinizi hatırlar ve genel deneyiminizi iyileştirir.",
    ],
  },
  {
    h: "2. Hangi Çerezleri Kullanıyoruz?",
    p: [
      "Zorunlu kayıtlar: Sitenin temel işlevleri için gereklidir. Çerez tercihinizi hatırlamak için tarayıcınızın yerel depolamasına (localStorage) küçük bir kayıt yazılır; reklam veya takip amacı taşımaz.",
      "Üçüncü taraf çerezleri: Konum bölümlerindeki Google Haritalar yalnızca çerezleri kabul etmeniz ya da haritanın yanındaki \"Haritayı göster\" düğmesine basmanız halinde yüklenir; yüklendiğinde Google kendi çerezlerini kullanabilir. Çerezleri reddederseniz harita yüklenmez.",
    ],
  },
  {
    h: "3. Üçüncü Taraf Servisleri",
    p: [
      "Bölge ve konum bölümlerinde harita gösterimi için Google Haritalar (Google LLC) hizmetinden yararlanıyoruz. İletişim ve belge talep formları Netlify (Netlify Inc.) altyapısı üzerinden iletilir; WhatsApp bağlantıları Meta Platforms (WhatsApp) hizmetini açar. Bu servislerin veri işleme koşulları KVKK Aydınlatma Metni'nde açıklanmıştır.",
    ],
  },
  {
    h: "4. Çerezleri Yönetme",
    p: [
      "Çerez tercihinizi sitedeki onay kutusundan belirleyebilirsiniz. Ayrıca tarayıcınızın ayarlarından çerezleri dilediğiniz zaman silebilir veya engelleyebilirsiniz. Zorunlu çerezleri engellemeniz halinde sitenin bazı bölümleri beklendiği gibi çalışmayabilir.",
      "Tercihinizi sıfırlamak isterseniz tarayıcınızın site verilerini temizlemeniz yeterlidir; bir sonraki ziyaretinizde çerez bildirimi yeniden gösterilir.",
    ],
  },
  {
    h: "5. İletişim",
    p: [
      `Çerez kullanımı ve kişisel verilerinizle ilgili sorularınız için veri sorumlusu ${site.seller}'a ${contact.email} adresinden veya ${contact.phones[0].label} numarasından ulaşabilirsiniz.`,
    ],
  },
];

export default function CerezPolitikasiPage() {
  return (
    <div className="surface-paper pt-32 pb-24">
      <div className="container-luxe max-w-3xl">
        <div className="flex items-center gap-3">
          <span className="gold-rule-solid w-8" />
          <span className="eyebrow text-bronze">Yasal</span>
        </div>
        <h1 className="mt-5 text-4xl text-ocean md:text-5xl">Çerez Politikası</h1>
        <p className="mt-5 text-base leading-relaxed text-ocean/70">
          {site.name} internet sitesinde kullanılan çerezler ve çerez tercihlerinizi nasıl yönetebileceğinize ilişkin
          bilgilendirmedir.
        </p>
        <div className="gold-rule my-10" />

        <div className="space-y-10">
          {sections.map((s) => (
            <section key={s.h}>
              <h2 className="text-xl text-ocean">{s.h}</h2>
              {s.p.map((para) => (
                <p key={para.slice(0, 24)} className="mt-3 text-sm leading-relaxed text-ocean/75">
                  {para}
                </p>
              ))}
            </section>
          ))}
        </div>

        <p className="mt-12 text-xs leading-relaxed text-ocean/45">
          Son güncelleme: 29 Ekim 2026. Kişisel verilerinizin işlenmesine ilişkin ayrıntılar için{" "}
          <Link href="/kvkk" className="text-bronze underline underline-offset-2">
            KVKK Aydınlatma Metni
          </Link>{" "}
          sayfasını ziyaret edebilirsiniz.
        </p>
      </div>
    </div>
  );
}
