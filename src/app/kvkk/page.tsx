import type { Metadata } from "next";
import { site, contact } from "@/data/site";

export const metadata: Metadata = {
  title: "KVKK Aydınlatma Metni",
  description: "6698 sayılı Kişisel Verilerin Korunması Kanunu kapsamında MİA PARK OCEAN aydınlatma metni.",
  robots: { index: false, follow: true },
};

const sections = [
  {
    h: "1. Veri Sorumlusu",
    p: [
      `İşbu aydınlatma metni, 6698 sayılı Kişisel Verilerin Korunması Kanunu ("KVKK") kapsamında; MİA PARK OCEAN projesinin tanıtım ve satış süreçlerini yürüten ${site.seller} (bundan sonra "Veri Sorumlusu") tarafından hazırlanmıştır. Proje, ${site.developer} tarafından geliştirilmektedir.`,
      `Veri Sorumlusu'na; ${contact.address.lines.join(" ")} adresinden, ${contact.email} e-posta adresinden veya ${contact.phones[0].label} numaralı telefondan ulaşabilirsiniz.`,
    ],
  },
  {
    h: "2. İşlenen Kişisel Veriler",
    p: [
      "İletişim formu ve satış görüşmeleri aracılığıyla; ad-soyad, telefon numarası, e-posta adresi, ilgilendiğiniz daire tipi ve tarafımıza ilettiğiniz mesaj içeriği gibi kimlik ve iletişim verileriniz işlenmektedir.",
    ],
  },
  {
    h: "3. Kişisel Verilerin İşlenme Amaçları",
    p: [
      "Kişisel verileriniz; talep ve sorularınızın yanıtlanması, proje ve daireler hakkında bilgilendirme yapılması, satış ve tanıtım süreçlerinin yürütülmesi, sizinle iletişim kurulması ve yasal yükümlülüklerin yerine getirilmesi amaçlarıyla işlenir.",
    ],
  },
  {
    h: "4. Hukuki Sebep",
    p: [
      "Verileriniz; KVKK m.5 uyarınca açık rızanıza dayanılarak ve/veya bir hakkın tesisi, ilgili kişinin temel hak ve özgürlüklerine zarar vermemek kaydıyla veri sorumlusunun meşru menfaati hukuki sebeplerine dayanılarak işlenir.",
    ],
  },
  {
    h: "5. Verilerin Aktarımı",
    p: [
      "Kişisel verileriniz; yalnızca yukarıdaki amaçlarla sınırlı olmak üzere, proje geliştiricisi kooperatif, yetkili satış ekibi ve yasal yükümlülükler kapsamında yetkili kamu kurum ve kuruluşları ile paylaşılabilir. Verileriniz, açık rızanız olmaksızın pazarlama amacıyla üçüncü taraflara satılmaz.",
    ],
  },
  {
    h: "6. Toplama Yöntemi",
    p: [
      "Kişisel verileriniz; internet sitesindeki iletişim formu, telefon, WhatsApp, e-posta ve yüz yüze görüşmeler gibi kanallar aracılığıyla elektronik ve fiziki ortamda toplanır.",
    ],
  },
  {
    h: "7. İlgili Kişi Olarak Haklarınız",
    p: [
      "KVKK m.11 kapsamında; kişisel verilerinizin işlenip işlenmediğini öğrenme, işlenmişse bilgi talep etme, işlenme amacını öğrenme, eksik veya yanlış işlenmişse düzeltilmesini, KVKK'da öngörülen şartlarda silinmesini/yok edilmesini isteme ve işlemenin hukuka aykırılığı halinde zararın giderilmesini talep etme haklarına sahipsiniz.",
      `Taleplerinizi ${contact.email} adresi üzerinden veya satış ofisimize yazılı başvuru ile iletebilirsiniz.`,
    ],
  },
];

export default function KvkkPage() {
  return (
    <div className="surface-paper pt-32 pb-24">
      <div className="container-luxe max-w-3xl">
        <div className="flex items-center gap-3">
          <span className="gold-rule-solid w-8" />
          <span className="eyebrow text-bronze">Yasal</span>
        </div>
        <h1 className="mt-5 text-4xl text-ocean md:text-5xl">KVKK Aydınlatma Metni</h1>
        <p className="mt-5 text-base leading-relaxed text-ocean/70">
          6698 sayılı Kişisel Verilerin Korunması Kanunu kapsamında kişisel verilerinizin işlenmesine ilişkin
          aydınlatma metnidir.
        </p>
        <div className="gold-rule my-10" />

        <div className="space-y-10">
          {sections.map((s) => (
            <section key={s.h}>
              <h2 className="text-xl text-ocean">{s.h}</h2>
              {s.p.map((para) => (
                <p key={para.slice(0, 24)} className="mt-3 text-sm leading-relaxed text-ocean/75">{para}</p>
              ))}
            </section>
          ))}
        </div>

        <p className="mt-12 text-xs leading-relaxed text-ocean/45">
          Bu metin genel bilgilendirme amaçlıdır ve proje belgeleri kesinleştikçe güncellenecektir. Nihai KVKK
          aydınlatma ve açık rıza süreçleri yetkili uzmanlarca onaylanmalıdır.
        </p>
      </div>
    </div>
  );
}
