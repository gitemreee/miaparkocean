import type { Metadata } from "next";
import { site, contact } from "@/data/site";

export const metadata: Metadata = {
  alternates: { canonical: "/kvkk/" },
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
      "İletişim formu, belge talep formu ve satış görüşmeleri aracılığıyla; ad-soyad, telefon numarası, e-posta adresi, ilgilendiğiniz daire tipi ve tarafımıza ilettiğiniz mesaj içeriği gibi kimlik ve iletişim verileriniz işlenmektedir.",
      "Etkinlik katılım formu aracılığıyla ayrıca kurum/yayın adı ve katılımcı sayısı bilgileri işlenir.",
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
      "Verileriniz KVKK m.5 kapsamında şu hukuki sebeplere dayanılarak işlenir: açık rızanız (m.5/1); bir sözleşmenin kurulması veya ifasıyla doğrudan ilgili olması (m.5/2-c); veri sorumlusunun hukuki yükümlülüğünü yerine getirmesi (m.5/2-ç); bir hakkın tesisi, kullanılması veya korunması (m.5/2-e); temel hak ve özgürlüklerinize zarar vermemek kaydıyla veri sorumlusunun meşru menfaati (m.5/2-f).",
    ],
  },
  {
    h: "5. Verilerin Aktarımı",
    p: [
      "Kişisel verileriniz; yalnızca yukarıdaki amaçlarla sınırlı olmak üzere, proje geliştiricisi kooperatif, yetkili satış ekibi ve yasal yükümlülükler kapsamında yetkili kamu kurum ve kuruluşları ile paylaşılabilir. Verileriniz, açık rızanız olmaksızın pazarlama amacıyla üçüncü taraflara satılmaz.",
      "Yurt dışına aktarım: İnternet sitesindeki formlar Netlify Inc. (ABD) altyapısı üzerinden iletilir; WhatsApp üzerinden yazdığınız mesajlar Meta Platforms (WhatsApp) altyapısında işlenir; konum haritaları, onay vermeniz halinde Google LLC tarafından sunulur. Bu aktarımlar KVKK m.9 kapsamında, ilgili hizmetin kullanılmasına ilişkin açık rızanıza dayanılarak gerçekleştirilir.",
    ],
  },
  {
    h: "6. Toplama Yöntemi",
    p: [
      "Kişisel verileriniz; internet sitesindeki iletişim formu, telefon, WhatsApp, e-posta ve yüz yüze görüşmeler gibi kanallar aracılığıyla elektronik ve fiziki ortamda toplanır.",
    ],
  },
  {
    h: "7. Saklama Süresi",
    p: [
      "Kişisel verileriniz, işlenme amacının gerektirdiği süre boyunca ve ilgili mevzuatta öngörülen zamanaşımı süreleri kadar saklanır; bu sürelerin sonunda silinir, yok edilir veya anonim hale getirilir.",
    ],
  },
  {
    h: "8. İlgili Kişi Olarak Haklarınız",
    p: [
      "KVKK m.11 kapsamında; (a) kişisel verilerinizin işlenip işlenmediğini öğrenme, (b) işlenmişse buna ilişkin bilgi talep etme, (c) işlenme amacını ve bunların amacına uygun kullanılıp kullanılmadığını öğrenme, (ç) yurt içinde veya yurt dışında aktarıldığı üçüncü kişileri bilme, (d) eksik veya yanlış işlenmişse düzeltilmesini isteme, (e) KVKK m.7'de öngörülen şartlar çerçevesinde silinmesini veya yok edilmesini isteme, (f) (d) ve (e) bentleri uyarınca yapılan işlemlerin verilerin aktarıldığı üçüncü kişilere bildirilmesini isteme, (g) işlenen verilerin münhasıran otomatik sistemler vasıtasıyla analiz edilmesi suretiyle aleyhinize bir sonucun ortaya çıkmasına itiraz etme ve (ğ) kanuna aykırı işlenmesi sebebiyle zarara uğramanız halinde zararın giderilmesini talep etme haklarına sahipsiniz.",
      `Başvurularınızı, Veri Sorumlusuna Başvuru Usul ve Esasları Hakkında Tebliğ'e uygun olarak yazılı şekilde satış ofisimize iletebilir veya ${contact.email} adresine gönderebilirsiniz. Başvurunuz en geç 30 gün içinde ücretsiz olarak sonuçlandırılır.`,
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

        <p className="mt-12 text-xs leading-relaxed text-ocean/45">Son güncelleme: 29 Ekim 2026</p>
      </div>
    </div>
  );
}
