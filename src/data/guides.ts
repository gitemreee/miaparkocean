// Bilgi Merkezi kısa rehberleri (Üyelik, Yönetim, Finansman, İnşaat, Güven).
// Her biri tek konulu açıklayıcıdır; kesinleşmemiş uygulamalar mpoNote ile etiketlenir.
import type { Article } from "./articles";

export const guides: Article[] = [
  // ————— B. Üyelik ve Ortaklık Rehberi —————
  {
    slug: "kooperatife-nasil-uye-olunur",
    category: "uyelik",
    tier: "guide",
    title: "Kooperatife Nasıl Üye Olunur?",
    metaDescription: "Kooperatif üyelik başvurusu, gerekli belgeler ve üyeliğin kesinleşme süreci.",
    intro:
      "Üyelik başvurusu; başvuru formu, kimlik ve gerekli belgelerin teslimi, anasözleşme şartlarının kontrolü, yönetim kurulu kararı ve ortaklık kaydının oluşturulması adımlarından oluşur. Üyeye ödeme yapmadan önce anasözleşme, proje bilgi formu, mali yükümlülük tablosu, tahsis yöntemi ve çıkış-devir hükümleri verilmelidir. Üyelik kabulü yazılı karar ve kayıtla kesinleşir.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "uyelik-ile-tapulu-satis-farki",
    category: "uyelik",
    tier: "guide",
    title: "Kooperatif Üyeliği ile Tapulu Satış Arasındaki Fark",
    metaDescription: "Kooperatif ortaklığı ile bağımsız bölüm tapusu arasındaki hukuki fark.",
    intro:
      "Kooperatif üyeliği bir ortaklık statüsüdür; doğrudan bağımsız bölüm tapusu anlamına gelmez. Üye, kooperatif içindeki hak ve yükümlülüklere sahip olur. Tapu devri ise bağımsız bölümün hukuken kişi adına tescilidir. Üyeliğin hangi aşamada tahsis ve tapuya dönüşeceği açıkça belirtilir.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "uyelik-sozlesmesi-icerigi",
    category: "uyelik",
    tier: "guide",
    title: "Üyelik Sözleşmesinde Neler Bulunmalıdır?",
    metaDescription: "Kooperatif üyelik sözleşmesinde yer alması gereken temel hükümler.",
    intro:
      "Sözleşmede taraflar, kooperatif türü, üyelik payı, başlangıç ve dönemsel ödemeler, tahsis yöntemi, proje takvimi, maliyet değişikliği prosedürü, devir ve çıkış, temerrüt, bilgi erişimi, kişisel veri, uyuşmazlık ve bildirim hükümleri bulunmalıdır. Sözleşme, anasözleşme ve genel kurul kararlarına aykırı hükümler içermemelidir.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "ortaklik-payi-nedir",
    category: "uyelik",
    tier: "guide",
    title: "Ortaklık Payı Nedir?",
    metaDescription: "Ortaklık payı ile toplam proje ödemesi arasındaki fark.",
    intro:
      "Ortaklık payı, kooperatif sermayesine katılımı ifade eder. Proje için yapılan toplam ödeme ile ortaklık sermaye payı aynı kavram olmayabilir. Aidat, inşaat finansmanı, hizmet bedeli ve sermaye taahhüdü ayrı muhasebe kalemleri olarak gösterilmelidir.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "kooperatiften-cikma",
    category: "uyelik",
    tier: "guide",
    title: "Kooperatiften Çıkma Süreci",
    metaDescription: "Kooperatif ortaklığından çıkma bildirimi, iade hesabı ve ödeme zamanı.",
    intro:
      "Ortak, kanun ve anasözleşmede belirlenen şartlarla çıkma bildiriminde bulunabilir. Çıkışın hangi hesap dönemi sonunda sonuç doğuracağı, iade hesabı, kesintiler ve ödeme zamanı açıkça anlatılmalıdır. İade tutarı “ödenen tüm paranın derhal geri verilmesi” şeklinde otomatik varsayılmamalıdır.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "uyelik-miras",
    category: "uyelik",
    tier: "guide",
    title: "Üyelik Mirasçılara Geçer mi?",
    metaDescription: "Ölüm halinde kooperatif ortaklığının mirasçılara geçişi.",
    intro:
      "Ölüm halinde ortaklığın devamı veya mirasçılara geçişi anasözleşme hükümleri ve miras hukukuyla birlikte değerlendirilir. Mirasçıların ortaklık şartlarını taşıması, temsilci belirlemesi veya ayrılma payı süreci gündeme gelebilir. Bu konu proje sözleşmesinde açıkça düzenlenmelidir.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "devirde-borc-sorumlulugu",
    category: "uyelik",
    tier: "guide",
    title: "Devirde Borçlardan Kim Sorumludur?",
    metaDescription: "Üyelik devrinde kooperatife karşı hak ve yükümlülüklerin geçişi.",
    intro:
      "Devir sonrasında kooperatife karşı üyelikten doğan hak ve yükümlülükler yeni ortağa geçebilir. Taraflar arasındaki özel devir bedeli kooperatif borcundan ayrıdır. Kooperatif, devir öncesinde borç ve tahakkuk dökümü vermelidir.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "sonradan-uye-odemeleri",
    category: "uyelik",
    tier: "guide",
    title: "Sonradan Üye Olanların Ödemeleri",
    metaDescription: "Sonradan katılan üyelerin geçmiş dönem maliyet ve finansman katkıları.",
    intro:
      "Sonradan katılan üyelerin önceki ortaklarla eşit konuma gelmesi için geçmiş dönem maliyetleri, finansman katkıları ve güncel maliyet farkları objektif şekilde hesaplanabilir. Uygulama genel kurul kararına, anasözleşmeye ve eşitlik ilkesine uygun olmalıdır.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "uyelikten-cikarilma",
    category: "uyelik",
    tier: "guide",
    title: "Üyelikten Çıkarılma Şartları",
    metaDescription: "Kooperatif ortaklığından çıkarılma sebepleri ve usulü.",
    intro:
      "Ortak, yalnızca anasözleşmede açıkça belirtilen sebeplere ve usule dayanılarak çıkarılabilir. Karar gerekçeli olmalı, tebliğ edilmeli ve itiraz yolları gösterilmelidir. Keyfî veya sonradan üretilmiş gerekçeler hukuki risk yaratır.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "cikarma-itiraz",
    category: "uyelik",
    tier: "guide",
    title: "Çıkarma Kararına İtiraz",
    metaDescription: "Çıkarma kararına karşı itiraz ve dava yolları.",
    intro:
      "Üye, kendisine tebliğ edilen çıkarma kararına karşı anasözleşme ve kanunda öngörülen itiraz veya dava yollarını kullanabilir. Süreler hak kaybına yol açabileceği için tebligat tarihi önemlidir. Bu içerik hukuki danışmanlık yerine genel prosedürü açıklar.",
    sections: [],
    mpoNote: true,
  },

  // ————— F. Yönetim ve Kurumsal Yönetişim —————
  {
    slug: "yonetim-kurulu-gorevleri",
    category: "yonetim",
    tier: "guide",
    title: "Yönetim Kurulunun Görevleri",
    metaDescription: "Kooperatif yönetim kurulunun temsil, uygulama ve bilgilendirme görevleri.",
    intro:
      "Yönetim kurulu kooperatifi temsil eder, genel kurul kararlarını uygular, muhasebe ve kayıt düzenini sağlar, sözleşmeleri yönetir, bütçeyi takip eder ve üyeleri bilgilendirir. Yetkilerini kanun, anasözleşme ve genel kurul kararları içinde kullanmalıdır.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "denetleme-organi-gorevleri",
    category: "yonetim",
    tier: "guide",
    title: "Denetleme Organının Görevleri",
    metaDescription: "Denetleme organının yönetimden bağımsız inceleme görevi.",
    intro:
      "Denetleme organı yönetimin işlem ve hesaplarını genel kurul adına inceler. Mali tabloların doğruluğu, kararların usule uygunluğu, kayıtların düzeni ve riskli işlemler raporlanır. Denetçinin yönetimden bağımsız hareket etmesi gerekir.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "bagimsiz-dis-denetim",
    category: "yonetim",
    tier: "guide",
    title: "Bağımsız Dış Denetim Neden Önemlidir?",
    metaDescription: "Gönüllü bağımsız dış denetimin kurumsal güvene katkısı.",
    intro:
      "Dış denetim, mali raporların ve belirli süreçlerin yetkili bağımsız kişi veya kuruluşça değerlendirilmesini sağlar. Yasal zorunluluk oluşmasa dahi gönüllü dış denetim, özellikle çok ortaklı ve yüksek bütçeli projelerde kurumsal güveni artırır.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "yonetim-degisikligi",
    category: "yonetim",
    tier: "guide",
    title: "Kooperatif Yönetimi Nasıl Değiştirilir?",
    metaDescription: "Yönetim kurulunun seçimi, azli ve devir teslim süreci.",
    intro:
      "Yönetim kurulu genel kurul tarafından seçilir. Görev süresi, seçim, azil ve boşalan üyeliklerin doldurulması anasözleşme ve mevzuata tabidir. Değişiklik halinde para, mal, belge, şifre ve kayıtlar tutanakla devredilmelidir.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "yonetici-sorumlulugu",
    category: "yonetim",
    tier: "guide",
    title: "Yönetim Kurulu Üyelerinin Sorumluluğu",
    metaDescription: "Yöneticilerin özen, sadakat ve mevzuata uygunluk sorumluluğu.",
    intro:
      "Yöneticiler görevlerini özen, sadakat ve mevzuata uygunluk içinde yürütmelidir. Yetki aşımı, belgesiz ödeme, çıkar çatışması, kayıtların gizlenmesi veya kooperatifi zarara uğratan işlemler hukuki ve cezai sorumluluk doğurabilir.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "cikar-catismasi",
    category: "yonetim",
    tier: "guide",
    title: "Çıkar Çatışması Nasıl Önlenir?",
    metaDescription: "İlişkili taraf işlemleri ve çıkar çatışması yönetimi.",
    intro:
      "Yönetici, denetçi veya yakınlarının taraf olduğu işlemler önceden beyan edilmeli; ilgili kişi karar ve onay sürecinden çekilmelidir. İlişkili taraf işlemleri piyasa koşullarıyla karşılaştırılmalı ve üyelere raporlanmalıdır.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "cift-imza-sistemi",
    category: "yonetim",
    tier: "guide",
    title: "Çift İmza Sistemi",
    metaDescription: "Belirli tutar üzerindeki ödemelerde iki yetkili onayı.",
    intro:
      "Belirlenen tutarın üzerindeki banka ödeme ve sözleşmelerde iki yetkilinin birlikte onayı, tek kişi riskini azaltır. Bunun yanında talep eden, kontrol eden ve ödeyen kişiler mümkün olduğunca ayrılmalıdır.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "yonetici-ucretleri",
    category: "yonetim",
    tier: "guide",
    title: "Yönetici Ücretleri Nasıl Belirlenir?",
    metaDescription: "Huzur hakkı ve harcırahın genel kurulca belirlenmesi.",
    intro:
      "Yönetim ve denetim organlarına yapılacak ücret, huzur hakkı ve harcırah ödemeleri genel kurul tarafından açıkça kararlaştırılmalıdır. Tutarlar bütçede ayrı gösterilmeli, gizli yan menfaat yaratılmamalıdır.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "etik-yonetim",
    category: "yonetim",
    tier: "guide",
    title: "Kooperatiflerde Etik Yönetim",
    metaDescription: "Dürüstlük, eşitlik ve hesap verebilirlik ilkeleri.",
    intro:
      "Etik yönetim; dürüstlük, eşitlik, gizlilik, çıkar çatışmasından kaçınma, belgelilik ve hesap verebilirlik ilkelerini içerir. Etik kod yalnızca metin değil, ihlal bildirim ve yaptırım sistemiyle desteklenmelidir.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "uyeler-bilgi-talebi",
    category: "yonetim",
    tier: "guide",
    title: "Üyeler Yönetimden Nasıl Bilgi İster?",
    metaDescription: "Bilgi taleplerinin kayıt altına alınması ve yanıtlanması.",
    intro:
      "Bilgi talepleri yazılı veya portal üzerinden alınmalı, kayıt numarası verilmeli ve makul süre içinde cevaplanmalıdır. Ticari sır, kişisel veri ve üçüncü kişi hakları korunurken üyelerin kanuni bilgi alma hakkı engellenmemelidir.",
    sections: [],
    mpoNote: true,
  },

  // ————— D. Finansman, Bütçe ve Ödeme —————
  {
    slug: "kooperatif-butcesi",
    category: "finansman",
    tier: "guide",
    title: "Kooperatif Bütçesi Nasıl Hazırlanır?",
    metaDescription: "Bütçe kalemleri, varsayımlar ve ödeme takvimi.",
    intro:
      "Bütçe; arsa, proje ve ruhsat, kaba ve ince inşaat, mekanik-elektrik, altyapı, peyzaj, müşavirlik, finansman, vergi, sigorta, yönetim ve risk rezervi kalemlerinden oluşmalıdır. Her kalemin dayanağı, varsayımı ve ödeme takvimi belirtilmelidir.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "insaat-maliyetleri-aciklama",
    category: "finansman",
    tier: "guide",
    title: "İnşaat Maliyetleri Nasıl Açıklanır?",
    metaDescription: "Gerçekleşen harcama, sözleşme tutarı ve kalan iş maliyetinin raporlanması.",
    intro:
      "Üyelere yalnızca toplam maliyet değil; gerçekleşen harcama, sözleşmeye bağlanan tutar, kalan iş maliyeti, tahsilat, nakit ihtiyacı ve risk rezervi birlikte sunulmalıdır. Raporlar karşılaştırılabilir dönem formatında yayımlanmalıdır.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "ek-odeme-sartlari",
    category: "finansman",
    tier: "guide",
    title: "Ek Ödeme Hangi Şartlarda Çıkar?",
    metaDescription: "Ek ödeme gerekçeleri, bağımsız doğrulama ve genel kurul kararı.",
    intro:
      "Ek ödeme; maliyet artışı, proje değişikliği, mevzuat gereği yeni imalat veya finansman açığı gibi nedenlerle gündeme gelebilir. Gerekçe, bağımsız doğrulama, alternatifler ve genel kurul kararı olmadan talep oluşturulmamalıdır.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "taksitler-nasil-belirlenir",
    category: "finansman",
    tier: "guide",
    title: "Taksitler Nasıl Belirlenir?",
    metaDescription: "Taksit planının nakit akışı ve ödeme kapasitesiyle ilişkisi.",
    intro:
      "Taksit planı proje nakit akışına, yüklenici ödeme takvimine, arsa borçlarına ve üyelerin ödeme kapasitesine göre hazırlanır. Aşırı önden tahsilat ile şantiye ilerlemesi arasında dengesizlik oluşmamalıdır.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "odemeler-bankadan",
    category: "finansman",
    tier: "guide",
    title: "Ödemeler Neden Bankadan Yapılmalıdır?",
    metaDescription: "Banka üzerinden ödemenin izlenebilirlik ve güven avantajı.",
    intro:
      "Banka üzerinden ödeme; kaynağı, tarihi, açıklaması ve alıcısı belli bir iz bırakır. Kişisel hesap, elden tahsilat ve belgesiz ödeme, hem güven hem vergi ve muhasebe açısından ciddi risk oluşturur.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "gecikme-faizi",
    category: "finansman",
    tier: "guide",
    title: "Gecikme Faizi Nasıl Belirlenir?",
    metaDescription: "Gecikme yaptırımının anasözleşme ve genel kurul kararına dayanması.",
    intro:
      "Gecikme yaptırımı anasözleşme ve genel kurul kararına dayanmalı, ölçülü ve bütün ortaklara eşit uygulanmalıdır. Faiz veya gecikme bedeli önceden açıklanmalı, keyfî olarak değiştirilmemelidir.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "insaat-fiyat-artislari",
    category: "finansman",
    tier: "guide",
    title: "İnşaat Fiyat Artışları Nasıl Yönetilir?",
    metaDescription: "Endeks, teklif yenileme ve tasarruf seçenekleriyle fiyat farkı yönetimi.",
    intro:
      "Fiyat artışları endeks, teklif yenileme, sözleşme fiyat farkı hükümleri ve kalan iş miktarı üzerinden analiz edilmelidir. Yönetim, yalnızca artışı değil; tasarruf seçeneklerini ve teslim etkisini de sunmalıdır.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "risk-rezervi",
    category: "finansman",
    tier: "guide",
    title: "Risk Rezervi Neden Gereklidir?",
    metaDescription: "Öngörülemeyen giderler için kontrollü bütçe payı.",
    intro:
      "Risk rezervi; öngörülemeyen zemin, mevzuat, altyapı veya fiyat farkı giderlerini karşılamak için bütçede ayrılan kontrollü paydır. Kullanım koşulları ve kalan rezerv düzenli raporlanmalıdır.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "proje-butce-kalemleri",
    category: "finansman",
    tier: "guide",
    title: "Proje Bütçesi Kalemleri",
    metaDescription: "Arsadan risk rezervine proje bütçesinin ana kalemleri.",
    intro:
      "Arsa, tapu ve harçlar, zemin ve proje, ruhsat, yapı denetim, yüklenici, malzeme, altyapı, sosyal alan, danışmanlık, sigorta, finansman, pazarlama, işletmeye geçiş ve risk rezervi ana bütçe kalemleridir.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "uye-basina-maliyet",
    category: "finansman",
    tier: "guide",
    title: "Üye Başına Gerçek Maliyet",
    metaDescription: "Toplam maliyetin objektif anahtarlarla üyelere dağıtımı.",
    intro:
      "Toplam proje maliyeti bağımsız bölüm türü, metrekare, arsa payı, cephe veya maliyet grubu gibi objektif dağıtım anahtarlarıyla üyelere dağıtılabilir. Hesap yöntemi önceden açıklanmalı ve genel kurulca onaylanmalıdır.",
    sections: [],
    mpoNote: true,
  },

  // ————— E. Arsa, Ruhsat ve İnşaat —————
  {
    slug: "hakedis-sistemi",
    category: "insaat",
    tier: "guide",
    title: "Hakediş Sistemi Nedir?",
    metaDescription: "Tamamlanan imalatın ölçülerek ödeme talebine dönüşmesi.",
    intro:
      "Hakediş, tamamlanan imalatın ölçülerek sözleşme fiyatları üzerinden ödeme talebine dönüştürülmesidir. Bağımsız kontrol, mükerrer ödeme ve yapılmamış işe ödeme riskini azaltır.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "bagimsiz-teknik-kontrol",
    category: "insaat",
    tier: "guide",
    title: "Bağımsız Teknik Kontrol",
    metaDescription: "Yükleniciden bağımsız teknik kontrolün rolü.",
    intro:
      "Teknik kontrol firması yükleniciden bağımsız olmalı; imalat miktarı, kalite, şartname, proje uyumu, iş programı ve kusurları raporlamalıdır. Mali müşavir teknik gerçekleşmeyi tek başına doğrulayamaz.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "yapi-ruhsati",
    category: "insaat",
    tier: "guide",
    title: "Yapı Ruhsatı Neden Önemlidir?",
    metaDescription: "Onaylı projeye göre yapılaşma izni ve kontrol edilecek bilgiler.",
    intro:
      "Yapı ruhsatı, onaylı projeye göre yapılaşma iznini gösterir. Ruhsat sahibi, yapı sınıfı, kullanım amacı, bağımsız bölüm sayısı ve geçerlilik tarihleri kontrol edilmelidir.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "arsa-tapu-kontrol",
    category: "insaat",
    tier: "guide",
    title: "Arsa Tapusunda Neler Kontrol Edilir?",
    metaDescription: "Malik, takyidat, ipotek ve şerh gibi tapu kayıtlarının incelenmesi.",
    intro:
      "Malik, yüzölçümü, nitelik, ada-parsel, ipotek, haciz, şerh, irtifak, satış vaadi ve dava kayıtları kontrol edilir. Tapu kaydı güncel tarihli alınmalı ve hukuk müşavirince incelenmelidir.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "imar-durumu",
    category: "insaat",
    tier: "guide",
    title: "İmar Durumu Belgesi",
    metaDescription: "Kullanım fonksiyonu, yapılaşma oranı ve plan notları.",
    intro:
      "İmar durumu; kullanım fonksiyonu, yapılaşma oranı, yükseklik, çekme mesafeleri ve plan notlarını gösterir. Tanıtım projesi; imar ve onaylı mimari proje ile uyumlu olmalıdır.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "yapi-denetim",
    category: "insaat",
    tier: "guide",
    title: "Yapı Denetim Firmasının Görevleri",
    metaDescription: "Yapı denetim kuruluşunun mevzuata uygunluk denetimi.",
    intro:
      "Yapı denetim kuruluşu, ilgili mevzuat kapsamında proje ve imalatların standartlara uygunluğunu denetler. Kooperatifin bağımsız proje yönetimi ve kalite kontrolü ise daha geniş operasyonel kapsam taşıyabilir.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "muteahhit-secim",
    category: "insaat",
    tier: "guide",
    title: "Müteahhit Seçim Kriterleri",
    metaDescription: "Mali kapasite, deneyim, teminat ve teklif bütünlüğü.",
    intro:
      "Mali kapasite, teknik kadro, benzer iş deneyimi, referanslar, iş programı, teminat gücü, dava ve yasaklılık durumu, iş güvenliği performansı ve teklifin kapsam bütünlüğü değerlendirilmelidir.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "insaat-teminat",
    category: "insaat",
    tier: "guide",
    title: "İnşaat Sözleşmesinde Teminat",
    metaDescription: "Avans, kesin ve performans teminatları ile garanti hükümleri.",
    intro:
      "Avans teminatı, kesin teminat, performans teminatı, sigorta, gecikme cezası, ayıp sorumluluğu ve garanti hükümleri kooperatifin riskini azaltır. Teminatların süresi ve paraya çevrilebilirliği kontrol edilmelidir.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "gecikme-cezasi",
    category: "insaat",
    tier: "guide",
    title: "Gecikme Cezası Nasıl Düzenlenir?",
    metaDescription: "İş programı, kilometre taşları ve ölçülebilir teslim tarihleri.",
    intro:
      "İş programı, ara kilometre taşları, teslim tarihi, mücbir sebep tanımı ve gecikme cezası açık olmalıdır. Belirsiz “uygun zamanda teslim” ifadeleri yerine ölçülebilir tarihler kullanılmalıdır.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "malzeme-kalitesi",
    category: "insaat",
    tier: "guide",
    title: "Malzeme Kalitesi Nasıl Denetlenir?",
    metaDescription: "Teknik şartname, numune onayı ve test sertifikaları.",
    intro:
      "Teknik şartname, marka/model veya performans kriterleri, numune onayı, test sertifikaları ve saha kontrol kayıtları kullanılır. Değişiklikler yazılı onaya bağlanmalıdır.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "insaat-ilerleme-raporu",
    category: "insaat",
    tier: "guide",
    title: "İnşaat İlerlemesi Nasıl Raporlanır?",
    metaDescription: "Planlanan-gerçekleşen oran, hakediş ve tahmini teslim.",
    intro:
      "Aylık rapor; planlanan-gerçekleşen oran, kritik yol, iş kalemleri, fotoğraf, hakediş, ödeme, risk ve tahmini teslim tarihini içermelidir.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "proje-degisikligi",
    category: "insaat",
    tier: "guide",
    title: "Proje Değişikliklerine Kim Karar Verir?",
    metaDescription: "Değişikliğin niteliğine göre yetkili organ ve onay süreci.",
    intro:
      "Değişikliğin niteliğine göre yönetim kurulu, genel kurul, proje müellifi, ruhsat mercii veya üyelerin onayı gerekebilir. Maliyet ve kullanım etkisi açıklanmadan değişiklik yapılmamalıdır.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "teslim-oncesi-kontrol",
    category: "insaat",
    tier: "guide",
    title: "Teslim Öncesi Bağımsız Bölüm Kontrolü",
    metaDescription: "Bağımsız bölüm ve ortak alanların kontrol listesiyle incelenmesi.",
    intro:
      "Teslim öncesinde bağımsız bölüm, ortak alan, tesisat, yüzey, kapı-pencere, ekipman ve güvenlik unsurları kontrol listesiyle incelenir. Kusurlar tutanak ve kapanış süresiyle kaydedilir.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "iskan-belgesi",
    category: "insaat",
    tier: "guide",
    title: "İskân Belgesi Nedir?",
    metaDescription: "Yapı kullanma izin belgesinin önemi.",
    intro:
      "Yapı kullanma izin belgesi (iskân), yapının ruhsat ve eklerine uygun tamamlandığını ve kullanım sürecine geçişi gösteren temel belgedir. Tapu ve abonelik süreçleri açısından önem taşır.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "ferdi-mulkiyet",
    category: "insaat",
    tier: "guide",
    title: "Ferdi Mülkiyete Geçiş",
    metaDescription: "Bağımsız bölümlerin üyeler adına tesciline geçiş.",
    intro:
      "Ferdi mülkiyete geçiş; kooperatif mülkiyetindeki bağımsız bölümlerin, şartlar tamamlandıktan sonra üyeler adına tescil edilmesidir. Borçlar, tahsis, kat mülkiyeti ve genel kurul kararları süreçte belirleyicidir.",
    sections: [],
    mpoNote: true,
  },

  // ————— C. Güven ve Şeffaflık Merkezi —————
  {
    slug: "guvenilir-kooperatif",
    category: "guven",
    tier: "guide",
    title: "Güvenilir Kooperatif Nasıl Anlaşılır?",
    metaDescription: "Güçlü güven göstergelerine sahip kooperatifin özellikleri.",
    intro:
      "Arsa ve ruhsat belgeleri açık, banka hesabı kurumsal, bütçesi gerçekçi, yönetim ve denetim kayıtları erişilebilir, tahsis kuralları yazılı ve yüklenici ödemeleri ilerlemeye bağlı bir kooperatif daha güçlü güven göstergelerine sahiptir.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "uye-olmadan-kontrol-belgeler",
    category: "guven",
    tier: "guide",
    title: "Üye Olmadan Önce Kontrol Edilecek Belgeler",
    metaDescription: "Anasözleşmeden ruhsata, üyelik öncesi incelenecek belgeler.",
    intro:
      "Anasözleşme, sicil kaydı, arsa tapusu, takyidat, imar, ruhsat, proje, yüklenici sözleşmesi, bütçe, ödeme planı, tahsis yönergesi, genel kurul kararları, denetim raporu, sigorta ve yetki belgeleri incelenmelidir.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "uye-portali-belgeler",
    category: "guven",
    tier: "guide",
    title: "Üye Portalında Hangi Belgeler Bulunmalı?",
    metaDescription: "Tapu, ruhsat, mali tablo ve ilerleme raporlarının portalda yayımı.",
    intro:
      "Tapu ve ruhsat, genel kurul kararları, bütçe, mali tablolar, denetim raporları, sözleşme özetleri, hakediş ve ilerleme raporları, tahsilat dökümü, teslim takvimi ve bildirimlerin üye portalında bulunması planlanmaktadır.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "aylik-seffaflik-raporu",
    category: "guven",
    tier: "guide",
    title: "Aylık Şeffaflık Raporu",
    metaDescription: "Tahsilat, ödeme, ilerleme ve riskin tek formatta sunumu.",
    intro:
      "Aylık şeffaflık raporu; tahsilat, ödeme, banka bakiyesi, sözleşmeye bağlı yükümlülük, ilerleme, risk, karar ve gelecek ay planını tek formatta sunar.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "belgesiz-odeme-riskleri",
    category: "guven",
    tier: "guide",
    title: "Belgesiz Ödemenin Riskleri",
    metaDescription: "Belgesiz ve kişisel hesaba ödemenin doğurduğu riskler.",
    intro:
      "Belgesiz ödeme; ispat, muhasebe, vergi, yetkisiz kullanım ve üyeler arası eşitlik sorunları doğurur. Kooperatif adına olmayan hesaba ödeme yapılmamalıdır.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "muteahhit-yonetim-iliskisi",
    category: "guven",
    tier: "guide",
    title: "Müteahhit ve Yönetim İlişkisi",
    metaDescription: "Sözleşme, hakediş ve ödeme onayının ayrı kontrol noktaları.",
    intro:
      "Sözleşme, hakediş, değişiklik emri ve ödeme onayı ayrı kontrol noktalarına bağlanmalıdır. Yönetici ile yüklenici arasındaki ilişkili taraf durumu açıklanmalıdır.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "satin-alma-komisyonu",
    category: "guven",
    tier: "guide",
    title: "Satın Alma Komisyonu",
    metaDescription: "Teklif toplama ve karşılaştırmadan sorumlu komisyon.",
    intro:
      "Teknik ve mali uzmanlardan oluşan komisyon; ihtiyaç tanımı, teklif toplama, karşılaştırma ve öneri raporu hazırlar. Nihai yetki anasözleşme ve iç yönergeye göre kullanılır.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "uc-teklif-sistemi",
    category: "guven",
    tier: "guide",
    title: "Üç Teklif Sistemi",
    metaDescription: "En az üç yazılı teklifle fiyat ve kalite karşılaştırması.",
    intro:
      "Benzer kapsamda en az üç yazılı teklif alınması, fiyat ve kalite karşılaştırmasını güçlendirir. Tek kaynak alımında gerekçeli istisna kararı oluşturulmalıdır.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "risk-bildirim-formu",
    category: "guven",
    tier: "guide",
    title: "Üyeler İçin Risk Bildirim Formu",
    metaDescription: "Arsa, ruhsat, maliyet ve teslim risklerinin sade dille açıklanması.",
    intro:
      "Arsa, ruhsat, finansman, maliyet, teslim, devir ve işletme riskleri sade dilde açıklanır; üyenin okuduğu kayıt altına alınır. Form, hukuka aykırı bir sorumsuzluk kaydı olarak kullanılmaz.",
    sections: [],
    mpoNote: true,
  },
  {
    slug: "sikayet-itiraz",
    category: "guven",
    tier: "guide",
    title: "Şikâyet ve İtiraz Mekanizması",
    metaDescription: "Kayıt numarası, cevap süresi ve üst itiraz basamağı.",
    intro:
      "Başvurular portal, e-posta veya yazılı kanaldan alınmalı; kayıt numarası, cevap süresi, inceleme sorumlusu ve üst itiraz basamağı belirlenmelidir.",
    sections: [],
    mpoNote: true,
  },
];
