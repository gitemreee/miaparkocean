/**
 * Yerel SEO / GEO veri kaynağı.
 *
 * Her lokasyon için benzersiz içerik tutulur: şablon metin YOKTUR, her
 * mahalle/ilçe kendi karakteri, ulaşımı ve alıcı profiliyle anlatılır.
 * `/bolgeler/[slug]` sayfaları bu veriden üretilir.
 *
 * ÖNEMLİ: Proje yalnızca İzmit MİA Bölgesi'ndedir. Diğer lokasyon sayfaları
 * "oradan MİA PARK OCEAN'a ulaşım ve yatırım" perspektifiyle yazılır; hiçbir
 * sayfada o bölgede proje varmış izlenimi verilmez.
 *
 * Süreler yaklaşık, normal trafik koşullarına göredir.
 */

export type LocationType = "mahalle" | "ilce" | "il";

export type Location = {
  slug: string;
  /** Sayfa başlığındaki yer adı */
  name: string;
  /** Uzun ad (başlıklarda) */
  fullName: string;
  type: LocationType;
  parent: string;
  /** SEO başlığı */
  title: string;
  description: string;
  /** Projeye yaklaşık araç mesafesi */
  drive: string;
  /** Giriş paragrafları — her lokasyon için özgün */
  intro: string[];
  /** Bölgeye özel öne çıkanlar */
  highlights: { title: string; text: string }[];
  /** GEO uyumlu soru-cevap — yapay zekâ motorlarının alıntılayacağı net cevaplar */
  faq: { q: string; a: string }[];
  /** Yakın lokasyon slug'ları — iç bağlantı ağı */
  nearby: string[];
  /** Arama amacına yönelik anahtar ifadeler */
  keywords: string[];
};

const PROJECT = "MİA PARK OCEAN";

export const locations: Location[] = [
  // ==========================================================
  // İZMİT MAHALLELERİ
  // ==========================================================
  {
    slug: "izmit-yahya-kaptan",
    name: "Yahya Kaptan",
    fullName: "Yahya Kaptan Mahallesi",
    type: "mahalle",
    parent: "İzmit",
    title: "Yahya Kaptan Mahallesi Satılık Daire ve Yeni Konut Projeleri",
    description:
      "Yahya Kaptan Mahallesi'nde konut arayanlar için İzmit MİA Bölgesi'ndeki MİA PARK OCEAN: faizsiz kooperatif modeli, 1+0, 1+1 ve 2+1 bahçe dubleks seçenekleri.",
    drive: "2-4 dakika",
    intro: [
      "Yahya Kaptan, İzmit'in planlı toplu konut dokusuyla öne çıkan, geniş bulvarları ve olgunlaşmış yeşil alanlarıyla bilinen mahallelerinden biri. Uzun yıllardır aileler tarafından tercih edilmesi, mahalleyi İzmit'in en oturmuş yaşam alanlarından biri hâline getirdi.",
      "Mahalle, adını taşıyan S.S. Yahya Kaptan Birlik Yapı Kooperatifi'nin de merkezi. MİA PARK OCEAN, bu kooperatifin İzmit MİA Bölgesi'nde yükselen projesi; Yahya Kaptan'dan araçla birkaç dakika uzaklıkta.",
      "Yahya Kaptan'da oturup daha büyük bir daireye ya da sosyal donatısı geniş bir siteye geçmek isteyenler için MİA PARK OCEAN, mahalleyi ve alışkanlıkları değiştirmeden konfor yükseltmeye imkân veriyor.",
    ],
    highlights: [
      { title: "Kooperatifin merkezi", text: "S.S. Yahya Kaptan Birlik Yapı Kooperatifi'nin adını aldığı mahalle." },
      { title: "Oturmuş doku", text: "Planlı toplu konut yapısı, geniş bulvarlar ve olgun yeşil alanlar." },
      { title: "Projeye çok yakın", text: "MİA PARK OCEAN'a araçla yaklaşık 2-4 dakika." },
      { title: "Aile profili", text: "Uzun süredir aile yoğunluklu, komşuluk ilişkisi güçlü bir mahalle." },
    ],
    faq: [
      {
        q: "Yahya Kaptan'dan MİA PARK OCEAN'a nasıl ulaşılır?",
        a: "MİA PARK OCEAN, İzmit MİA Bölgesi'nde yer alır ve Yahya Kaptan Mahallesi'nden araçla yaklaşık 2-4 dakika uzaklıktadır. D-100 karayolu bağlantısı üzerinden birkaç dakikada ulaşılır.",
      },
      {
        q: "Yahya Kaptan'da oturuyorum, kooperatif üyeliği için ne yapmalıyım?",
        a: "S.S. Yahya Kaptan Birlik Yapı Kooperatifi'ne üyelik, tek yetkili satıcı Ocean Gayrimenkul üzerinden yapılır. Üyelik sözleşmesi, ödeme planı ve resmî belgeler görüşme sırasında paylaşılır; işlemler 1163 sayılı Kooperatifler Kanunu kapsamında yürütülür.",
      },
      {
        q: "Yahya Kaptan'daki dairemi satmadan MİA PARK OCEAN'dan daire alabilir miyim?",
        a: "Evet. Kooperatif modeli tasarrufa dayalı ve 60 aya varan vadeli olduğu için peşin büyük bir sermaye gerektirmez; mevcut konutunuzu elde tutarak taksitli ödeme yapabilirsiniz. Ödeme planı Ocean Gayrimenkul ile birlikte belirlenir.",
      },
    ],
    nearby: ["izmit-yenisehir", "izmit-omeraga", "izmit-alikahya", "kocaeli-basiskele"],
    keywords: [
      "Yahya Kaptan satılık daire",
      "Yahya Kaptan konut projesi",
      "Yahya Kaptan kooperatif daire",
      "İzmit Yahya Kaptan yeni proje",
    ],
  },
  {
    slug: "izmit-yenisehir",
    name: "Yenişehir",
    fullName: "Yenişehir Mahallesi",
    type: "mahalle",
    parent: "İzmit",
    title: "Yenişehir Mahallesi Satılık Daire ve Yeni Konut Projeleri",
    description:
      "İzmit Yenişehir'de yeni konut arayanlara MİA PARK OCEAN: MİA Bölgesi'nde 660 daire, faizsiz kooperatif finansmanı, 60 ay vade.",
    drive: "3-5 dakika",
    intro: [
      "Yenişehir, İzmit'in D-100 aksına yakın, son yıllarda yeni yapı stokunun hızla arttığı mahallelerinden. Şehir merkezine yakınlığı ve ana yollara kolay bağlantısı, mahalleyi hem oturum hem yatırım açısından hareketli tutuyor.",
      "MİA Bölgesi'nin gelişim aksı Yenişehir'in hemen yanında ilerliyor. Bu nedenle Yenişehir'de konut arayanların karşısına MİA PARK OCEAN, aynı ulaşım avantajlarını daha geniş sosyal donatılarla birleştiren bir alternatif olarak çıkıyor.",
      "Mahallede kiralık ve satılık konut hareketliliğinin yüksek olması, bölgeye yatırım yapmak isteyenler için de referans oluşturuyor.",
    ],
    highlights: [
      { title: "D-100'e komşu", text: "Ana karayoluna doğrudan bağlantı, şehir dışına hızlı çıkış." },
      { title: "Yeni yapı stoku", text: "Son yıllarda artan yeni bina yoğunluğu, genç aile profilini büyütüyor." },
      { title: "Merkeze yakın", text: "İzmit şehir merkezine araçla yaklaşık 5 dakika." },
      { title: "Hareketli piyasa", text: "Kiralık ve satılık konut dolaşımının canlı olduğu bir mahalle." },
    ],
    faq: [
      {
        q: "Yenişehir'den MİA PARK OCEAN kaç dakika?",
        a: "İzmit Yenişehir Mahallesi'nden MİA PARK OCEAN'a araçla yaklaşık 3-5 dakikada ulaşılır. Proje, MİA Bölgesi'nde D-100 karayoluna yaklaşık 1 dakika mesafededir.",
      },
      {
        q: "Yenişehir'deki yeni projelerle MİA PARK OCEAN arasındaki fark nedir?",
        a: "MİA PARK OCEAN bir yapı kooperatifi projesidir: banka kredisi, faiz ve kefil gerektirmez. Ödemeler tasarrufa dayalı sistemle 60 aya kadar vadelendirilir ve %0 faiz uygulanır. Kooperatif, T.C. Ticaret Bakanlığı'nın KOOPBİS sistemine kayıtlıdır.",
      },
      {
        q: "Yenişehir'de yatırım için mi oturmak için mi daire almalıyım?",
        a: "İkisi de mümkündür. Yenişehir ve komşusu MİA Bölgesi, ulaşım yatırımlarıyla gelişen bir aks üzerindedir; bu da hem kira getirisi hem değer artışı beklentisini destekler. MİA PARK OCEAN'da 1+0 ve 1+1 tipleri yatırım, 2+1 bahçe dubleks aile kullanımı için öne çıkar.",
      },
    ],
    nearby: ["izmit-yahya-kaptan", "izmit-alikahya", "izmit-omeraga", "kocaeli-kartepe"],
    keywords: [
      "Yenişehir İzmit satılık daire",
      "İzmit Yenişehir konut projesi",
      "Yenişehir yeni daire fiyatları",
    ],
  },
  {
    slug: "izmit-omeraga",
    name: "Ömerağa",
    fullName: "Ömerağa Mahallesi",
    type: "mahalle",
    parent: "İzmit",
    title: "Ömerağa Mahallesi Satılık Daire ve Yeni Konut Projeleri",
    description:
      "İzmit'in merkez mahallesi Ömerağa'dan MİA PARK OCEAN'a: satış ofisimiz Ömerağa'da, proje MİA Bölgesi'nde. Faizsiz kooperatif modeli.",
    drive: "5-7 dakika",
    intro: [
      "Ömerağa, İzmit'in tam kalbi. Belediye, kamu kurumları, Cumhuriyet Caddesi ve yürüme mesafesindeki ticaret dokusuyla şehrin idari ve sosyal merkezi konumunda.",
      "MİA PARK OCEAN'ın satış ofisi de Ömerağa Mahallesi'nde: Abdurrahman Yüksel Caddesi üzerinde. Projeyi yerinde görmeden önce belgeleri incelemek, ödeme planını konuşmak ve daire tiplerini karşılaştırmak için merkezden kolayca ulaşabilirsiniz.",
      "Merkezde oturup daha geniş sosyal alanlı, otoparklı ve site güvenlikli bir yaşam isteyenler için MİA PARK OCEAN, merkeze yakınlığı korurken konfor farkı sunuyor.",
    ],
    highlights: [
      { title: "Satış ofisi burada", text: "Ömerağa Mah. Abdurrahman Yüksel Cad. No:15/4 — İzmit merkez." },
      { title: "Şehrin merkezi", text: "Kamu kurumları, ticaret ve sosyal hayatın toplandığı mahalle." },
      { title: "Yürüme mesafesi", text: "Merkezde her şeye yaya erişim; projeye araçla yaklaşık 5-7 dakika." },
      { title: "Konfor farkı", text: "Merkezde bulunması zor olan kapalı otopark, havuz ve site güvenliği." },
    ],
    faq: [
      {
        q: "MİA PARK OCEAN satış ofisi nerede?",
        a: "Satış ofisi İzmit merkezde, Ömerağa Mahallesi Abdurrahman Yüksel Caddesi Bana Bak Apartmanı No:15/4 adresindedir. Randevu için 0540 028 00 41 numarasından ulaşabilirsiniz.",
      },
      {
        q: "Ömerağa'dan projeye nasıl gidilir?",
        a: "İzmit merkezden MİA Bölgesi'ne araçla yaklaşık 5-7 dakikada ulaşılır. Satış ofisinden proje alanına yönlendirme ve yerinde inceleme organizasyonu yapılmaktadır.",
      },
      {
        q: "Merkezde oturuyorum, siteye taşınmanın avantajı ne?",
        a: "MİA PARK OCEAN'da kapalı yüzme havuzu, fitness salonu, sauna ve Türk hamamı, çocuk oyun parkı ve kapalı otopark bulunur. Bunlar İzmit merkezdeki klasik apartman stokunda çoğunlukla yer almayan donatılardır.",
      },
    ],
    nearby: ["izmit-karabas", "izmit-cedit", "izmit-yahya-kaptan", "izmit-kozluk"],
    keywords: ["Ömerağa satılık daire", "İzmit merkez konut projesi", "İzmit satış ofisi"],
  },
  {
    slug: "izmit-alikahya",
    name: "Alikahya",
    fullName: "Alikahya (Fatih ve Atatürk Mahalleleri)",
    type: "mahalle",
    parent: "İzmit",
    title: "Alikahya Satılık Daire ve Yeni Konut Projeleri",
    description:
      "Alikahya'da konut arayanlara MİA PARK OCEAN alternatifi: İzmit MİA Bölgesi'nde faizsiz kooperatif projesi, 60 ay vade, 660 daire.",
    drive: "8-12 dakika",
    intro: [
      "Alikahya, İzmit'in doğusunda son on yılda en hızlı büyüyen bölgelerden biri. Yeni konut alanları, stadyum ve sanayi istihdamının etkisiyle nüfusu sürekli artıyor.",
      "Bölgede yeni yapı arzı yüksek olsa da, MİA Bölgesi'nin şehir merkezine ve D-100'e yakınlığı farklı bir konum avantajı sunuyor. Alikahya'da fiyat/konum dengesini araştıranlar için MİA PARK OCEAN karşılaştırmaya değer bir seçenek.",
      "Özellikle sanayide çalışan ve şehir merkezine düzenli ulaşım ihtiyacı olan aileler, merkeze daha yakın bir konumu tercih ediyor.",
    ],
    highlights: [
      { title: "Hızlı büyüyen bölge", text: "Yeni konut alanları ve artan nüfusla İzmit'in gelişen doğu aksı." },
      { title: "Sanayi istihdamı", text: "Çevredeki sanayi tesisleri nedeniyle güçlü kiralama talebi." },
      { title: "Merkeze mesafe", text: "MİA Bölgesi, Alikahya'ya göre şehir merkezine belirgin şekilde daha yakın." },
      { title: "Karşılaştırma", text: "Aynı bütçeyle konum ve donatı farkını değerlendirme imkânı." },
    ],
    faq: [
      {
        q: "Alikahya'dan MİA PARK OCEAN'a ulaşım ne kadar sürer?",
        a: "Alikahya'dan MİA PARK OCEAN'a araçla yaklaşık 8-12 dakikada ulaşılır. Proje, D-100 karayoluna yaklaşık 1 dakika, TEM Otoyolu'na yaklaşık 5 dakika mesafededir.",
      },
      {
        q: "Alikahya mı MİA Bölgesi mi daha iyi bir yatırım?",
        a: "Alikahya yeni konut arzının yoğun olduğu bir bölge; MİA Bölgesi ise şehir merkezine ve ana ulaşım akslarına daha yakın, arz sınırlı bir aks. Merkeze yakınlık ve donatı zenginliği önceliğiniz ise MİA Bölgesi öne çıkar. Kesin karar için her iki bölgede güncel m² fiyatlarını karşılaştırmanızı öneririz.",
      },
      {
        q: "Alikahya'da kooperatif projesi var mı?",
        a: "MİA PARK OCEAN, İzmit MİA Bölgesi'nde yer alan tek projemizdir; Alikahya'da projemiz bulunmamaktadır. Alikahya'da oturanlar için MİA Bölgesi araçla yaklaşık 8-12 dakika uzaklıktadır.",
      },
    ],
    nearby: ["izmit-yenisehir", "izmit-yahya-kaptan", "kocaeli-kartepe", "kocaeli-basiskele"],
    keywords: ["Alikahya satılık daire", "Alikahya konut projesi", "İzmit Alikahya yeni daire"],
  },
  {
    slug: "izmit-karabas",
    name: "Karabaş",
    fullName: "Karabaş Mahallesi",
    type: "mahalle",
    parent: "İzmit",
    title: "Karabaş Mahallesi Satılık Daire ve Yeni Konut Projeleri",
    description:
      "İzmit Karabaş'ta konut arayanlara MİA PARK OCEAN: sahil ve merkeze yakın MİA Bölgesi'nde faizsiz kooperatif projesi.",
    drive: "5-8 dakika",
    intro: [
      "Karabaş, İzmit sahil şeridine ve merkeze yakınlığıyla bilinen, şehrin köklü mahallelerinden. Sahil bandındaki yürüyüş ve rekreasyon alanları mahallenin en güçlü yanı.",
      "Mahalledeki yapı stoğunun önemli bölümü daha eski dönemlere ait. Deprem yönetmeliğine uygun, fore kazık temelli yeni yapı arayanlar için MİA PARK OCEAN, merkeze yakınlığı korurken güncel yapı standartları sunuyor.",
      "Sahil hattına ve şehir merkezine ulaşımın kolay kalması, MİA Bölgesi'ni Karabaş sakinleri için makul bir alternatif hâline getiriyor.",
    ],
    highlights: [
      { title: "Sahile yakın", text: "İzmit sahil bandı ve yürüyüş yollarına kısa mesafe." },
      { title: "Köklü mahalle", text: "Merkeze bitişik, oturmuş sosyal doku." },
      { title: "Yapı yenileme ihtiyacı", text: "Eski yapı stoğuna karşı güncel deprem standartlarında alternatif." },
      { title: "Fore kazık temel", text: "MİA PARK OCEAN'da temeller tamamen fore kazık sistemiyle inşa ediliyor." },
    ],
    faq: [
      {
        q: "MİA PARK OCEAN depreme dayanıklı mı?",
        a: "Proje, 8 katlı 4 bloktan oluşur ve temelleri tamamen fore kazık sistemiyle inşa edilmektedir. Yapı, yürürlükteki deprem yönetmeliğine uygun olarak projelendirilmiştir.",
      },
      {
        q: "Karabaş'tan denize ve projeye mesafe nedir?",
        a: "Karabaş, İzmit sahiline yürüme/kısa araç mesafesindedir. MİA PARK OCEAN'a Karabaş'tan araçla yaklaşık 5-8 dakikada ulaşılır; projeden İzmit sahiline yaklaşık 2 dakikadır.",
      },
      {
        q: "Karabaş'ta eski dairemi yenilemek yerine ne yapabilirim?",
        a: "Kentsel dönüşüm sürecine girmeden, tasarrufa dayalı kooperatif modeliyle yeni bir daireye geçmek mümkündür. Ödemeler 60 aya kadar vadelendirilir ve faiz uygulanmaz.",
      },
    ],
    nearby: ["izmit-omeraga", "izmit-cedit", "izmit-kozluk", "kocaeli-derince"],
    keywords: ["Karabaş satılık daire", "İzmit sahil konut projesi", "Karabaş yeni bina"],
  },
  {
    slug: "izmit-cedit",
    name: "Cedit",
    fullName: "Cedit Mahallesi",
    type: "mahalle",
    parent: "İzmit",
    title: "Cedit Mahallesi Satılık Daire ve Yeni Konut Projeleri",
    description:
      "İzmit Cedit'te yeni konut arayanlara MİA PARK OCEAN: MİA Bölgesi'nde bankasız, faizsiz, kefilsiz kooperatif modeli.",
    drive: "5-8 dakika",
    intro: [
      "Cedit, İzmit merkezine bitişik, yoğun yerleşimli mahallelerden biri. Çarşıya, pazara ve toplu taşımaya yakınlığı günlük yaşamı kolaylaştırıyor.",
      "Mahallede yapı yoğunluğu yüksek, otopark ve yeşil alan ise sınırlı. MİA PARK OCEAN, kapalı otopark, merkezi avlu ve süs havuzlarıyla bu ihtiyaçlara doğrudan cevap veriyor.",
      "Merkezle bağını koparmadan daha ferah bir yaşam alanına geçmek isteyen Cedit sakinleri için MİA Bölgesi birkaç dakika uzaklıkta.",
    ],
    highlights: [
      { title: "Merkeze bitişik", text: "Çarşı, pazar ve toplu taşımaya yakın konum." },
      { title: "Otopark çözümü", text: "Projede kapalı otopark; mahalledeki park sorununa alternatif." },
      { title: "Yeşil alan", text: "Merkezi avlu, süs havuzları ve geniş peyzaj alanları." },
      { title: "Kısa mesafe", text: "MİA Bölgesi'ne araçla yaklaşık 5-8 dakika." },
    ],
    faq: [
      {
        q: "Cedit'ten MİA PARK OCEAN'a nasıl ulaşırım?",
        a: "Cedit Mahallesi'nden MİA PARK OCEAN'a araçla yaklaşık 5-8 dakikada ulaşılır. Proje İzmit MİA Bölgesi'nde, D-100 karayoluna yaklaşık 1 dakika mesafededir.",
      },
      {
        q: "Projede otopark var mı?",
        a: "Evet, MİA PARK OCEAN'da kapalı otopark bulunmaktadır. Ayrıca kapalı yüzme havuzu, fitness salonu, sauna ve Türk hamamı ile çocuk oyun parkı yer alır.",
      },
      {
        q: "Kefil veya banka kredisi gerekiyor mu?",
        a: "Hayır. MİA PARK OCEAN tasarrufa dayalı kooperatif modeliyle satılır: banka kredisi, faiz ve kefil gerekmez. Ödemeler 60 aya kadar vade ile yapılır.",
      },
    ],
    nearby: ["izmit-omeraga", "izmit-karabas", "izmit-kozluk", "izmit-yahya-kaptan"],
    keywords: ["Cedit satılık daire", "İzmit Cedit konut", "İzmit merkez yeni proje"],
  },
  {
    slug: "izmit-kozluk",
    name: "Kozluk",
    fullName: "Kozluk Mahallesi",
    type: "mahalle",
    parent: "İzmit",
    title: "Kozluk Mahallesi Satılık Daire ve Yeni Konut Projeleri",
    description:
      "İzmit Kozluk'ta konut arayanlar için MİA PARK OCEAN: merkeze yakın MİA Bölgesi'nde 660 daireli faizsiz kooperatif projesi.",
    drive: "5-8 dakika",
    intro: [
      "Kozluk, İzmit merkezinin batısında, sahil bandına ve şehir içi ana arterlere yakın bir mahalle. Merkeze yürüme mesafesinde olması günlük hayatı kolaylaştırıyor.",
      "Mahallede yeni konut arzı sınırlı; bu nedenle geniş sosyal donatılı bir siteye geçmek isteyenler MİA Bölgesi gibi gelişim akslarına yöneliyor.",
      "MİA PARK OCEAN, Kozluk'tan birkaç dakika uzaklıkta; merkeze yakınlığı korurken 1+0, 1+1 ve 2+1 bahçe dubleks seçenekleri sunuyor.",
    ],
    highlights: [
      { title: "Merkeze yürüme mesafesi", text: "İzmit çarşısı ve sahil bandına yakın konum." },
      { title: "Sınırlı yeni arz", text: "Mahallede yeni proje stoğunun az olması, çevre akslara yöneltiyor." },
      { title: "Daire çeşitliliği", text: "Projede 1+0, 1+1 ve bahçeli 2+1 dubleks seçenekleri." },
      { title: "Kısa mesafe", text: "MİA Bölgesi'ne araçla yaklaşık 5-8 dakika." },
    ],
    faq: [
      {
        q: "MİA PARK OCEAN'da hangi daire tipleri var?",
        a: "Projede 1+0, 1+1 ve zemin katlarda kendine ait özel bahçesi bulunan 2+1 loft/dubleks daireler bulunmaktadır. Toplam 660 daire, 8 katlı 4 blokta yer alır.",
      },
      {
        q: "Kozluk'tan projeye mesafe nedir?",
        a: "Kozluk Mahallesi'nden MİA PARK OCEAN'a araçla yaklaşık 5-8 dakikada ulaşılır.",
      },
      {
        q: "Bahçeli daire seçeneği var mı?",
        a: "Evet. Zemin katlarda konumlanan 2+1 dubleks dairelerin her birinin kendine ait özel bahçesi vardır; müstakil ev konforunu site ayrıcalığıyla birleştirir.",
      },
    ],
    nearby: ["izmit-karabas", "izmit-omeraga", "izmit-cedit", "kocaeli-derince"],
    keywords: ["Kozluk satılık daire", "İzmit Kozluk konut projesi"],
  },
  {
    slug: "izmit-bekirpasa",
    name: "Bekirpaşa",
    fullName: "Bekirpaşa",
    type: "mahalle",
    parent: "İzmit",
    title: "Bekirpaşa Satılık Daire ve Yeni Konut Projeleri",
    description:
      "Bekirpaşa'da konut arayanlara MİA PARK OCEAN: İzmit MİA Bölgesi'nde faizsiz, kefilsiz kooperatif projesi, 60 ay vade.",
    drive: "6-10 dakika",
    intro: [
      "Bekirpaşa, İzmit'in yoğun nüfuslu yerleşim bölgelerinden biri; geniş bir alana yayılan mahalle grubuyla şehrin doğu-güney aksını oluşturuyor.",
      "Bölgede konut stoğu çeşitli, ancak site tipi yaşam ve kapalı sosyal donatı arayanların seçenekleri sınırlı. MİA PARK OCEAN bu ihtiyaca yönelik bir alternatif sunuyor.",
      "D-100'e ve şehir merkezine yakın bir konumda, ailelerin sosyal donatı beklentisini karşılayan bir proje arayanlar için MİA Bölgesi kısa mesafede.",
    ],
    highlights: [
      { title: "Yoğun yerleşim", text: "İzmit'in en kalabalık yerleşim aksları arasında." },
      { title: "Site tipi yaşam", text: "Kapalı havuz, fitness, sauna ve hamam gibi donatılar." },
      { title: "Aile odaklı", text: "Çocuk oyun parkı ve güvenlikli site yapısı." },
      { title: "Ulaşım", text: "MİA Bölgesi'ne araçla yaklaşık 6-10 dakika." },
    ],
    faq: [
      {
        q: "Bekirpaşa'dan MİA PARK OCEAN'a kaç dakika?",
        a: "Bekirpaşa'dan MİA PARK OCEAN'a araçla yaklaşık 6-10 dakikada ulaşılır.",
      },
      {
        q: "Projede hangi sosyal donatılar var?",
        a: "Kapalı yüzme havuzu, fitness salonu, sauna ve Türk hamamı, çocuk oyun parkı, kapalı otopark, merkezi avlu, süs havuzları ve geniş yeşil alanlar bulunmaktadır.",
      },
      {
        q: "Aidat ve işletme giderleri nasıl belirlenir?",
        a: "Site yönetimi ve aidat esasları, teslim sürecinde kat malikleri/kooperatif genel kurulu kararlarıyla belirlenir. Güncel bilgi için Ocean Gayrimenkul ile görüşebilirsiniz.",
      },
    ],
    nearby: ["izmit-alikahya", "izmit-yenisehir", "kocaeli-basiskele", "izmit-yahya-kaptan"],
    keywords: ["Bekirpaşa satılık daire", "İzmit Bekirpaşa konut projesi"],
  },

  // ==========================================================
  // KOCAELİ İLÇELERİ
  // ==========================================================
  {
    slug: "kocaeli-basiskele",
    name: "Başiskele",
    fullName: "Başiskele",
    type: "ilce",
    parent: "Kocaeli",
    title: "Başiskele Satılık Daire ve Yeni Konut Projeleri",
    description:
      "Başiskele'de konut arayanlara MİA PARK OCEAN: İzmit MİA Bölgesi'nde 660 daireli faizsiz kooperatif projesi, 60 ay vade.",
    drive: "12-18 dakika",
    intro: [
      "Başiskele, körfezin güney kıyısında yer alan, doğayla iç içe yapısı ve villa/bahçeli konut dokusuyla öne çıkan bir ilçe. Son yıllarda İzmit merkezden taşınan ailelerin tercih ettiği bölgelerden biri hâline geldi.",
      "İlçede müstakil ve bahçeli yaşam yaygın; buna karşılık kapalı havuz, fitness ve güvenlikli site donatısı arayanların seçenekleri daha sınırlı. MİA PARK OCEAN'ın zemin kat bahçeli 2+1 dubleksleri, bahçeli yaşam beklentisini site konforuyla birleştiriyor.",
      "Merkeze günlük ulaşım ihtiyacı olan aileler için MİA Bölgesi, Başiskele'ye göre şehir merkezine ve ana akslara belirgin şekilde daha yakın konumda.",
    ],
    highlights: [
      { title: "Bahçeli yaşam kültürü", text: "İlçede yaygın olan bahçeli yaşam beklentisi, projedeki dubleks tiplerle karşılanıyor." },
      { title: "Körfez manzarası", text: "Başiskele kıyı hattı; projede ise deniz ve şehir manzaralı daire seçenekleri." },
      { title: "Merkeze erişim", text: "MİA Bölgesi, İzmit merkezine yaklaşık 5 dakika." },
      { title: "Site donatısı", text: "Kapalı havuz, hamam, fitness ve 7/24 güvenlik." },
    ],
    faq: [
      {
        q: "Başiskele'den MİA PARK OCEAN'a ulaşım ne kadar sürer?",
        a: "Başiskele'den MİA PARK OCEAN'a araçla yaklaşık 12-18 dakikada ulaşılır. Süre, çıkış noktasına ve trafik yoğunluğuna göre değişebilir.",
      },
      {
        q: "Başiskele'de kooperatif projeniz var mı?",
        a: "Hayır. MİA PARK OCEAN yalnızca İzmit MİA Bölgesi'nde yer almaktadır. Başiskele'de oturanlar projeye araçla yaklaşık 12-18 dakikada ulaşabilir.",
      },
      {
        q: "Bahçeli daire arıyorum, projede seçenek var mı?",
        a: "Evet. Zemin katlardaki 2+1 loft/dubleks dairelerin her birinin kendine ait özel bahçesi bulunur. Bu tip, müstakil ev konforu arayan ancak site güvenliği ve donatısından vazgeçmek istemeyenler için tasarlanmıştır.",
      },
    ],
    nearby: ["izmit-yahya-kaptan", "kocaeli-kartepe", "kocaeli-golcuk", "izmit-alikahya"],
    keywords: ["Başiskele satılık daire", "Başiskele konut projesi", "Kocaeli Başiskele yeni proje"],
  },
  {
    slug: "kocaeli-kartepe",
    name: "Kartepe",
    fullName: "Kartepe",
    type: "ilce",
    parent: "Kocaeli",
    title: "Kartepe Satılık Daire ve Yeni Konut Projeleri",
    description:
      "Kartepe'de konut arayanlara MİA PARK OCEAN: İzmit MİA Bölgesi'nde faizsiz kooperatif modeli, 1+0, 1+1 ve 2+1 bahçe dubleks.",
    drive: "12-20 dakika",
    intro: [
      "Kartepe, Sapanca Gölü kıyısı ve Kartepe zirvesiyle Kocaeli'nin doğa turizmi merkezi. İlçe, hem yazlık hem daimi konut talebiyle hareketli bir piyasaya sahip.",
      "Doğaya yakınlık Kartepe'nin en güçlü yanı; buna karşılık şehir merkezine günlük ulaşım mesafesi daha uzun. Merkeze yakın, donatısı geniş bir konut arayanlar MİA Bölgesi'ni değerlendiriyor.",
      "MİA PARK OCEAN, Kartepe'den araçla yaklaşık 12-20 dakika uzaklıkta; TEM Otoyolu'na yaklaşık 5 dakika mesafesiyle bölge içi ulaşımı kolaylaştırıyor.",
    ],
    highlights: [
      { title: "Doğa ile şehir dengesi", text: "Kartepe'nin doğası, MİA Bölgesi'nin merkeze yakınlığı." },
      { title: "TEM'e 5 dakika", text: "Projeden TEM Otoyolu'na yaklaşık 5 dakika." },
      { title: "İki tip talep", text: "Kartepe'de yazlık, MİA Bölgesi'nde daimi konut talebi öne çıkar." },
      { title: "Yatırım profili", text: "1+0 ve 1+1 tipleri kiralama açısından hareketli." },
    ],
    faq: [
      {
        q: "Kartepe'den MİA PARK OCEAN'a kaç dakika sürer?",
        a: "Kartepe'den MİA PARK OCEAN'a araçla yaklaşık 12-20 dakikada ulaşılır. Proje, TEM Otoyolu'na yaklaşık 5 dakika mesafededir.",
      },
      {
        q: "Kartepe'de mi İzmit merkezde mi daire almalıyım?",
        a: "Kartepe doğa ve sakinlik önceliği olanlar için uygundur; İzmit MİA Bölgesi ise şehir merkezine, üniversiteye, şehir hastanesine ve AVM'lere yakınlık isteyenler için avantajlıdır. Günlük şehir içi ulaşım ihtiyacınız yüksekse MİA Bölgesi daha pratiktir.",
      },
      {
        q: "Teslim süresi ne kadar?",
        a: "Kooperatif, projeyi 2 yıl içinde tamamlayıp teslim etmeyi taahhüt etmektedir. Güncel inşaat durumu ve teslim takvimi için Ocean Gayrimenkul ile görüşebilirsiniz.",
      },
    ],
    nearby: ["kocaeli-basiskele", "izmit-alikahya", "sakarya", "izmit-yenisehir"],
    keywords: ["Kartepe satılık daire", "Kartepe konut projesi", "Kocaeli Kartepe yeni daire"],
  },
  {
    slug: "kocaeli-derince",
    name: "Derince",
    fullName: "Derince",
    type: "ilce",
    parent: "Kocaeli",
    title: "Derince Satılık Daire ve Yeni Konut Projeleri",
    description:
      "Derince'de konut arayanlara MİA PARK OCEAN: İzmit MİA Bölgesi'nde bankasız, faizsiz kooperatif projesi.",
    drive: "10-15 dakika",
    intro: [
      "Derince, liman ve sanayi faaliyetleriyle Kocaeli ekonomisinin önemli merkezlerinden. Kocaeli Üniversitesi kampüsüne yakınlığı ilçedeki kiralama talebini de canlı tutuyor.",
      "İlçede sanayi ve liman istihdamı yoğun; konut talebi de büyük ölçüde bu istihdamdan besleniyor. Daha merkezi, sosyal donatısı geniş bir konut arayanlar için MİA Bölgesi kısa mesafede.",
      "MİA PARK OCEAN'dan Kocaeli Üniversitesi'ne yaklaşık 10 dakika, şehir hastanesine yaklaşık 5 dakika mesafe bulunuyor.",
    ],
    highlights: [
      { title: "Üniversiteye yakınlık", text: "Projeden Kocaeli Üniversitesi'ne yaklaşık 10 dakika." },
      { title: "Liman ve sanayi", text: "Derince'nin güçlü istihdam yapısı kiralama talebini destekliyor." },
      { title: "Şehir hastanesi", text: "Projeden Kocaeli Şehir Hastanesi'ne yaklaşık 5 dakika." },
      { title: "Yatırım tipi", text: "Öğrenci ve çalışan kiralaması için 1+0 ve 1+1 seçenekleri." },
    ],
    faq: [
      {
        q: "Derince'den MİA PARK OCEAN'a mesafe nedir?",
        a: "Derince'den MİA PARK OCEAN'a araçla yaklaşık 10-15 dakikada ulaşılır.",
      },
      {
        q: "Öğrenciye kiralamak için hangi daire tipi uygun?",
        a: "Kocaeli Üniversitesi'ne yaklaşık 10 dakika mesafedeki proje için 1+0 ve 1+1 tipleri öğrenci ve genç çalışan kiralamasında öne çıkar.",
      },
      {
        q: "Kooperatif güvenilir mi, param güvende mi?",
        a: "S.S. Yahya Kaptan Birlik Yapı Kooperatifi, T.C. Ticaret Bakanlığı bünyesindeki KOOPBİS (Kooperatif Bilgi Sistemi)'ne kayıtlıdır. Süreçler 1163 sayılı Kooperatifler Kanunu kapsamında yürütülür, e-Devlet üzerinden izlenebilir ve resmî denetime tabidir.",
      },
    ],
    nearby: ["izmit-karabas", "kocaeli-korfez", "izmit-kozluk", "izmit-omeraga"],
    keywords: ["Derince satılık daire", "Derince konut projesi", "Kocaeli Derince yeni proje"],
  },
  {
    slug: "kocaeli-korfez",
    name: "Körfez",
    fullName: "Körfez",
    type: "ilce",
    parent: "Kocaeli",
    title: "Körfez Satılık Daire ve Yeni Konut Projeleri",
    description:
      "Körfez ilçesinde konut arayanlara MİA PARK OCEAN: İzmit MİA Bölgesi'nde 660 daireli faizsiz kooperatif projesi.",
    drive: "18-25 dakika",
    intro: [
      "Körfez, Kocaeli'nin sanayi ağırlıklı ilçelerinden; rafineri ve petrokimya tesisleriyle güçlü bir istihdam yapısına sahip.",
      "İlçede konut talebi büyük ölçüde sanayi çalışanlarından geliyor. Şehir merkezine, üniversiteye ve şehir hastanesine yakın bir konut arayanlar için MİA Bölgesi öne çıkan alternatiflerden.",
      "TEM Otoyolu ve D-100 bağlantıları sayesinde Körfez ile MİA Bölgesi arasındaki ulaşım pratik şekilde sağlanıyor.",
    ],
    highlights: [
      { title: "Sanayi istihdamı", text: "Rafineri ve petrokimya tesisleriyle güçlü çalışan nüfusu." },
      { title: "Otoyol bağlantısı", text: "TEM ve D-100 üzerinden MİA Bölgesi'ne pratik ulaşım." },
      { title: "Merkezî donatılar", text: "Projeden üniversite, şehir hastanesi ve AVM'lere kısa mesafe." },
      { title: "Faizsiz model", text: "Banka kredisi ve kefil gerektirmeyen ödeme sistemi." },
    ],
    faq: [
      {
        q: "Körfez'den MİA PARK OCEAN'a nasıl ulaşılır?",
        a: "Körfez'den MİA PARK OCEAN'a D-100 veya TEM Otoyolu üzerinden araçla yaklaşık 18-25 dakikada ulaşılır.",
      },
      {
        q: "Ara ödeme veya balon ödeme var mı?",
        a: "Kooperatif modeli faizsiz ve ara ödemesiz olarak sunulmaktadır; ödemeler 60 aya kadar vadelendirilir. Güncel ödeme planı için Ocean Gayrimenkul ile görüşebilirsiniz.",
      },
      {
        q: "Uzaktan üyelik işlemi yapabilir miyim?",
        a: "Ön görüşme ve belge paylaşımı telefon/WhatsApp üzerinden yapılabilir; üyelik sözleşmesi imzası için satış ofisinde randevu oluşturulur.",
      },
    ],
    nearby: ["kocaeli-derince", "kocaeli-golcuk", "izmit-karabas", "kocaeli-gebze"],
    keywords: ["Körfez satılık daire", "Körfez konut projesi", "Kocaeli Körfez yeni daire"],
  },
  {
    slug: "kocaeli-golcuk",
    name: "Gölcük",
    fullName: "Gölcük",
    type: "ilce",
    parent: "Kocaeli",
    title: "Gölcük Satılık Daire ve Yeni Konut Projeleri",
    description:
      "Gölcük'te konut arayanlara MİA PARK OCEAN: İzmit MİA Bölgesi'nde fore kazık temelli, faizsiz kooperatif projesi.",
    drive: "20-28 dakika",
    intro: [
      "Gölcük, körfezin güney kıyısında, denizle iç içe yapısı ve donanma tesisleriyle bilinen bir ilçe. Sahil bandı ve yeşil alanları yaşam kalitesini yükseltiyor.",
      "1999 depremi bölgede yapı güvenliği hassasiyetini kalıcı olarak yükseltti. MİA PARK OCEAN'ın temelleri tamamen fore kazık sistemiyle inşa ediliyor; bu, yapı güvenliğine öncelik veren alıcılar için belirleyici bir kriter.",
      "İzmit merkeze düzenli ulaşım ihtiyacı olan aileler için MİA Bölgesi, merkeze ve ana akslara yakınlığıyla değerlendiriliyor.",
    ],
    highlights: [
      { title: "Yapı güvenliği önceliği", text: "Projede temeller tamamen fore kazık sistemiyle inşa ediliyor." },
      { title: "Sahil kültürü", text: "Gölcük sahili; projeden İzmit sahiline yaklaşık 2 dakika." },
      { title: "Merkeze erişim", text: "MİA Bölgesi'nden İzmit merkeze yaklaşık 5 dakika." },
      { title: "Aile donatıları", text: "Çocuk oyun parkı, kapalı havuz ve güvenlikli site." },
    ],
    faq: [
      {
        q: "Gölcük'ten MİA PARK OCEAN'a mesafe ne kadar?",
        a: "Gölcük'ten MİA PARK OCEAN'a araçla yaklaşık 20-28 dakikada ulaşılır.",
      },
      {
        q: "Projenin temel sistemi nedir?",
        a: "MİA PARK OCEAN'ın temelleri tamamen fore kazık sistemiyle inşa edilmektedir. Proje 8 katlı (zemin + 7) 4 bloktan oluşur.",
      },
      {
        q: "Deniz manzaralı daire var mı?",
        a: "Projede deniz ve şehir manzaralı daire seçenekleri bulunmaktadır. Manzara yönü blok ve kata göre değişir; güncel durum için satış ofisinden bilgi alabilirsiniz.",
      },
    ],
    nearby: ["kocaeli-basiskele", "kocaeli-korfez", "kocaeli-karamursel", "izmit-yahya-kaptan"],
    keywords: ["Gölcük satılık daire", "Gölcük konut projesi", "Kocaeli Gölcük yeni proje"],
  },
  {
    slug: "kocaeli-gebze",
    name: "Gebze",
    fullName: "Gebze",
    type: "ilce",
    parent: "Kocaeli",
    title: "Gebze Satılık Daire ve Yeni Konut Projeleri",
    description:
      "Gebze'de konut ve yatırım arayanlara MİA PARK OCEAN: İzmit MİA Bölgesi'nde faizsiz kooperatif projesi, uygun giriş maliyeti.",
    drive: "45-55 dakika",
    intro: [
      "Gebze, Kocaeli'nin İstanbul'a en yakın ilçesi ve sanayi-lojistik merkezi. Marmaray, Gebze-Halkalı hattı ve otoyol bağlantılarıyla İstanbul ile bütünleşmiş durumda.",
      "İstanbul'a yakınlık Gebze'de m² fiyatlarını Kocaeli ortalamasının üzerine taşıyor. Aynı bütçeyle daha geniş bir daireye ve daha zengin sosyal donatıya ulaşmak isteyen yatırımcılar için İzmit MİA Bölgesi bir alternatif oluşturuyor.",
      "Gebze'de çalışıp Kocaeli'de yatırım yapmayı planlayanlar, faizsiz kooperatif modelinin giriş maliyetini düşürmesi nedeniyle MİA PARK OCEAN'ı değerlendiriyor.",
    ],
    highlights: [
      { title: "İstanbul bağlantısı", text: "Marmaray ve otoyollarla İstanbul'a entegre ilçe." },
      { title: "Fiyat karşılaştırması", text: "Aynı bütçeyle İzmit MİA'da daha geniş daire ve donatı imkânı." },
      { title: "Yatırım kurgusu", text: "Faizsiz, 60 ay vadeli model peşin sermaye ihtiyacını azaltır." },
      { title: "Otoyol erişimi", text: "Projeden TEM Otoyolu'na yaklaşık 5 dakika." },
    ],
    faq: [
      {
        q: "Gebze'den MİA PARK OCEAN'a ulaşım ne kadar sürer?",
        a: "Gebze'den MİA PARK OCEAN'a TEM Otoyolu üzerinden araçla yaklaşık 45-55 dakikada ulaşılır.",
      },
      {
        q: "Gebze yerine İzmit'te yatırım yapmanın avantajı nedir?",
        a: "Gebze'de m² fiyatları İstanbul yakınlığı nedeniyle daha yüksektir. Aynı bütçeyle İzmit MİA Bölgesi'nde daha geniş bir daireye ve daha kapsamlı sosyal donatıya ulaşmak mümkündür. Ayrıca kooperatif modeli faizsiz ve kefilsizdir.",
      },
      {
        q: "Gebze'de projeniz var mı?",
        a: "Hayır. MİA PARK OCEAN yalnızca İzmit MİA Bölgesi'nde bulunmaktadır.",
      },
    ],
    nearby: ["kocaeli-darica", "kocaeli-cayirova", "istanbul", "kocaeli-korfez"],
    keywords: ["Gebze satılık daire", "Gebze konut yatırımı", "Gebze yerine İzmit yatırım"],
  },
  {
    slug: "kocaeli-darica",
    name: "Darıca",
    fullName: "Darıca",
    type: "ilce",
    parent: "Kocaeli",
    title: "Darıca Satılık Daire ve Yeni Konut Projeleri",
    description:
      "Darıca'da konut arayanlara MİA PARK OCEAN alternatifi: İzmit MİA Bölgesi'nde faizsiz kooperatif projesi, 60 ay vade.",
    drive: "50-60 dakika",
    intro: [
      "Darıca, Marmara kıyısındaki konumu ve İstanbul'a yakınlığıyla Kocaeli'nin en hızlı kentleşen ilçelerinden biri. Metro bağlantısı ilçedeki konut talebini daha da artırdı.",
      "İlçede yeni konut arzı yüksek olsa da fiyatlar İstanbul etkisiyle yukarıda seyrediyor. Bütçesini koruyup daha geniş bir daireye geçmek isteyenler Kocaeli'nin merkez aksına yöneliyor.",
      "MİA PARK OCEAN, faizsiz ve kefilsiz kooperatif modeliyle giriş maliyetini düşürerek bu geçişi mümkün kılıyor.",
    ],
    highlights: [
      { title: "Kıyı ilçesi", text: "Marmara kıyısında hızlı kentleşen bir yerleşim." },
      { title: "İstanbul etkisi", text: "Fiyatlar İstanbul yakınlığı nedeniyle yüksek seyrediyor." },
      { title: "Bütçe avantajı", text: "İzmit MİA'da aynı bütçeyle daha geniş daire imkânı." },
      { title: "Faizsiz model", text: "Banka, faiz ve kefil gerektirmeyen ödeme sistemi." },
    ],
    faq: [
      {
        q: "Darıca'dan MİA PARK OCEAN'a nasıl gidilir?",
        a: "Darıca'dan MİA PARK OCEAN'a TEM Otoyolu veya D-100 üzerinden araçla yaklaşık 50-60 dakikada ulaşılır.",
      },
      {
        q: "Uzaktan daire seçebilir miyim?",
        a: "Daire tipleri, kat planları ve görseller web sitemizde yer alır; ön seçim uzaktan yapılabilir. Sözleşme aşaması için İzmit'teki satış ofisinde randevu oluşturulur.",
      },
      {
        q: "Kooperatiften alınan dairenin tapusu olur mu?",
        a: "Yapı kooperatiflerinde üyelik payı karşılığı konut edinilir; inşaat tamamlanıp iskân alındıktan sonra ferdileşme ile üyeler adına tapu devri yapılır. Süreç 1163 sayılı Kooperatifler Kanunu kapsamındadır.",
      },
    ],
    nearby: ["kocaeli-gebze", "kocaeli-cayirova", "istanbul", "kocaeli-korfez"],
    keywords: ["Darıca satılık daire", "Darıca konut projesi", "Kocaeli Darıca yeni daire"],
  },
  {
    slug: "kocaeli-cayirova",
    name: "Çayırova",
    fullName: "Çayırova",
    type: "ilce",
    parent: "Kocaeli",
    title: "Çayırova Satılık Daire ve Yeni Konut Projeleri",
    description:
      "Çayırova'da konut arayanlara MİA PARK OCEAN: İzmit MİA Bölgesi'nde bankasız, faizsiz, kefilsiz kooperatif projesi.",
    drive: "45-55 dakika",
    intro: [
      "Çayırova, Gebze ile Darıca arasında konumlanan, sanayi ve lojistik istihdamının yoğun olduğu bir ilçe. İstanbul'a yakınlığı nüfusu sürekli büyütüyor.",
      "İlçede konut talebi yüksek, ancak sosyal donatısı geniş site tipi projelerde fiyatlar hızla yükseliyor. Bütçe/donatı dengesi arayanlar Kocaeli merkezine yöneliyor.",
      "MİA PARK OCEAN, kapalı havuzdan Türk hamamına uzanan donatı setini faizsiz ödeme modeliyle birleştiriyor.",
    ],
    highlights: [
      { title: "Sanayi ve lojistik", text: "Yoğun istihdam, sürekli büyüyen nüfus." },
      { title: "Donatı/bütçe dengesi", text: "İzmit MİA'da geniş donatı daha erişilebilir bütçeyle." },
      { title: "Faizsiz finansman", text: "%0 faiz, vade farkı yok, 60 aya kadar taksit." },
      { title: "Ulaşım", text: "TEM üzerinden yaklaşık 45-55 dakika." },
    ],
    faq: [
      {
        q: "Çayırova'dan MİA PARK OCEAN'a mesafe nedir?",
        a: "Çayırova'dan MİA PARK OCEAN'a TEM Otoyolu üzerinden araçla yaklaşık 45-55 dakikada ulaşılır.",
      },
      {
        q: "Peşinat ne kadar?",
        a: "Peşinat ve taksit tutarları daire tipine ve seçilen ödeme planına göre değişir. Güncel rakamlar için Ocean Gayrimenkul ile görüşebilir veya WhatsApp üzerinden bilgi alabilirsiniz.",
      },
      {
        q: "Faizsiz sistem nasıl işliyor?",
        a: "Tasarrufa dayalı kooperatif modelinde üyeler ortak bir havuza düzenli ödeme yapar; inşaat bu kaynakla finanse edilir. Banka kredisi kullanılmadığı için faiz ve vade farkı oluşmaz.",
      },
    ],
    nearby: ["kocaeli-gebze", "kocaeli-darica", "istanbul", "kocaeli-korfez"],
    keywords: ["Çayırova satılık daire", "Çayırova konut projesi"],
  },
  {
    slug: "kocaeli-karamursel",
    name: "Karamürsel",
    fullName: "Karamürsel",
    type: "ilce",
    parent: "Kocaeli",
    title: "Karamürsel Satılık Daire ve Yeni Konut Projeleri",
    description:
      "Karamürsel'de konut arayanlara MİA PARK OCEAN: İzmit MİA Bölgesi'nde 660 daireli faizsiz kooperatif projesi.",
    drive: "35-45 dakika",
    intro: [
      "Karamürsel, körfezin güneybatı ucunda, sahil şeridi ve sakin yaşam temposuyla öne çıkan bir ilçe. Yazlık konut talebi ilçede belirgin.",
      "Daimi konut ve şehir merkezine yakınlık arayan aileler ise İzmit aksını değerlendiriyor. MİA Bölgesi, üniversite, şehir hastanesi ve AVM'lere kısa mesafede.",
      "MİA PARK OCEAN, sahil kültürüne alışkın alıcılar için deniz ve şehir manzaralı daire seçenekleri sunuyor.",
    ],
    highlights: [
      { title: "Sahil yaşamı", text: "Karamürsel kıyısı; projeden İzmit sahiline yaklaşık 2 dakika." },
      { title: "Merkezî donatılar", text: "Üniversite ~10 dk, şehir hastanesi ~5 dk, AVM'ler ~3-7 dk." },
      { title: "Manzara", text: "Deniz ve şehir manzaralı daire seçenekleri." },
      { title: "Daimi konut", text: "Yazlık yerine yıl boyu kullanıma uygun site yaşamı." },
    ],
    faq: [
      {
        q: "Karamürsel'den MİA PARK OCEAN'a kaç dakika?",
        a: "Karamürsel'den MİA PARK OCEAN'a araçla yaklaşık 35-45 dakikada ulaşılır.",
      },
      {
        q: "Projenin çevresinde neler var?",
        a: "Projeden D-100 karayoluna yaklaşık 1 dakika, İzmit sahiline yaklaşık 2 dakika, 41 Burada AVM'ye yaklaşık 3 dakika, şehir merkezine ve Kocaeli Şehir Hastanesi'ne yaklaşık 5 dakika, Kocaeli Üniversitesi'ne yaklaşık 10 dakika mesafe bulunur.",
      },
      {
        q: "Site içinde havuz var mı?",
        a: "Evet, kapalı yüzme havuzu bulunmaktadır. Ayrıca merkezi avluda süs havuzları yer alır.",
      },
    ],
    nearby: ["kocaeli-golcuk", "kocaeli-basiskele", "kocaeli-korfez", "izmit-yahya-kaptan"],
    keywords: ["Karamürsel satılık daire", "Karamürsel konut projesi"],
  },
  {
    slug: "kocaeli-kandira",
    name: "Kandıra",
    fullName: "Kandıra",
    type: "ilce",
    parent: "Kocaeli",
    title: "Kandıra Satılık Daire ve Yeni Konut Projeleri",
    description:
      "Kandıra'da konut arayanlara MİA PARK OCEAN: İzmit MİA Bölgesi'nde faizsiz, kefilsiz kooperatif projesi.",
    drive: "40-50 dakika",
    intro: [
      "Kandıra, Karadeniz kıyısındaki plajları ve tarım dokusuyla Kocaeli'nin en geniş yüzölçümlü ilçelerinden. Şehir merkezinden uzaklığı yaşam temposunu sakinleştiriyor.",
      "İlçede yeni konut projesi arzı sınırlı; kentsel donatı, sağlık ve eğitim erişimi için İzmit merkezine yöneliniyor.",
      "MİA PARK OCEAN, şehir merkezine ve donatılara yakın bir konumda site yaşamı arayan Kandıralılar için değerlendirilebilir bir seçenek.",
    ],
    highlights: [
      { title: "Kentsel donatı erişimi", text: "İzmit merkezde sağlık, eğitim ve alışveriş erişimi." },
      { title: "Sınırlı yerel arz", text: "Kandıra'da site tipi yeni proje seçeneği az." },
      { title: "Site yaşamı", text: "Güvenlikli site, kapalı otopark ve sosyal donatılar." },
      { title: "Faizsiz model", text: "Banka ve kefil gerektirmeyen ödeme sistemi." },
    ],
    faq: [
      {
        q: "Kandıra'dan MİA PARK OCEAN'a ulaşım süresi nedir?",
        a: "Kandıra'dan MİA PARK OCEAN'a araçla yaklaşık 40-50 dakikada ulaşılır.",
      },
      {
        q: "Projede kaç daire var?",
        a: "MİA PARK OCEAN 4 bloktan oluşur ve toplam 660 daire içerir. Bloklar zemin + 7 kat olmak üzere 8 katlıdır.",
      },
      {
        q: "Randevu almadan satış ofisine gidebilir miyim?",
        a: "Randevu alınması, size ayrılan sürede daire tiplerini ve belgeleri detaylı incelemeniz açısından önerilir. 0540 028 00 41 veya WhatsApp üzerinden randevu oluşturabilirsiniz.",
      },
    ],
    nearby: ["izmit-yahya-kaptan", "kocaeli-derince", "izmit-alikahya", "kocaeli-korfez"],
    keywords: ["Kandıra satılık daire", "Kandıra konut projesi"],
  },
  {
    slug: "kocaeli-dilovasi",
    name: "Dilovası",
    fullName: "Dilovası",
    type: "ilce",
    parent: "Kocaeli",
    title: "Dilovası Satılık Daire ve Yeni Konut Projeleri",
    description:
      "Dilovası'nda konut arayanlara MİA PARK OCEAN: İzmit MİA Bölgesi'nde faizsiz kooperatif projesi, geniş yeşil alanlar.",
    drive: "40-50 dakika",
    intro: [
      "Dilovası, Kocaeli'nin organize sanayi bölgeleriyle şekillenmiş ilçelerinden. Sanayi istihdamı yoğun, konut talebi büyük ölçüde çalışan nüfustan geliyor.",
      "Sanayiden uzak, yeşil alanı geniş bir yaşam alanı arayan aileler için İzmit'in merkez aksı öne çıkıyor.",
      "MİA PARK OCEAN'da geniş peyzaj alanları, merkezi avlu ve süs havuzları bulunuyor; proje sanayi dokusundan uzakta, şehir merkezine yakın konumda.",
    ],
    highlights: [
      { title: "Yeşil alan", text: "Geniş peyzaj alanları, merkezi avlu ve süs havuzları." },
      { title: "Sanayiden uzak konum", text: "Şehir merkezine yakın, yerleşim odaklı bir aks." },
      { title: "Aile donatıları", text: "Çocuk oyun parkı, kapalı havuz ve güvenlik." },
      { title: "Ulaşım", text: "TEM üzerinden yaklaşık 40-50 dakika." },
    ],
    faq: [
      {
        q: "Dilovası'ndan MİA PARK OCEAN'a mesafe nedir?",
        a: "Dilovası'ndan MİA PARK OCEAN'a TEM Otoyolu üzerinden araçla yaklaşık 40-50 dakikada ulaşılır.",
      },
      {
        q: "Projede yeşil alan oranı nasıl?",
        a: "Proje yaklaşık 10 dönümlük arazi üzerinde konumlanır; merkezi avlu, süs havuzları ve geniş peyzaj alanları bulunur.",
      },
      {
        q: "Çocuklar için alan var mı?",
        a: "Evet, çocuk oyun parkı bulunmaktadır. Ayrıca 7/24 güvenlik ve kapalı otopark yer alır.",
      },
    ],
    nearby: ["kocaeli-gebze", "kocaeli-cayirova", "kocaeli-korfez", "izmit-yahya-kaptan"],
    keywords: ["Dilovası satılık daire", "Dilovası konut projesi"],
  },

  // ==========================================================
  // KOMŞU İLLER
  // ==========================================================
  {
    slug: "sakarya",
    name: "Sakarya",
    fullName: "Sakarya (Adapazarı ve çevresi)",
    type: "il",
    parent: "Marmara",
    title: "Sakarya'dan İzmit'e Konut Yatırımı — MİA PARK OCEAN",
    description:
      "Sakarya'dan İzmit MİA Bölgesi'ne yatırım: MİA PARK OCEAN'da faizsiz kooperatif modeli, 60 ay vade, 1+0, 1+1 ve 2+1 bahçe dubleks.",
    drive: "45-60 dakika",
    intro: [
      "Sakarya, TEM Otoyolu üzerinden Kocaeli'ye komşu; Adapazarı merkezden İzmit'e günlük gidiş-geliş yapan çalışan ve öğrenci sayısı hayli yüksek.",
      "İki şehir arasındaki bu yoğun hareketlilik, Sakaryalı alıcıların Kocaeli'yi doğal bir yatırım alanı olarak görmesini sağlıyor. İzmit'in merkezî konumu ve kurumsal donatıları kira talebini canlı tutuyor.",
      "MİA PARK OCEAN, faizsiz ve kefilsiz kooperatif modeliyle Sakarya'dan yatırım yapmak isteyenlere düşük giriş maliyetli bir seçenek sunuyor. Proje TEM Otoyolu'na yaklaşık 5 dakika mesafede.",
    ],
    highlights: [
      { title: "TEM'e 5 dakika", text: "Projeden TEM Otoyolu'na yaklaşık 5 dakika; Sakarya bağlantısı doğrudan." },
      { title: "Günlük hareketlilik", text: "İzmit-Adapazarı arasında yoğun çalışan ve öğrenci sirkülasyonu." },
      { title: "Kira talebi", text: "Üniversite ve şehir hastanesi yakınlığı kiralama talebini destekliyor." },
      { title: "Düşük giriş maliyeti", text: "Faizsiz, kefilsiz, 60 ay vadeli ödeme planı." },
    ],
    faq: [
      {
        q: "Sakarya'dan İzmit'e MİA PARK OCEAN'a ulaşım ne kadar sürer?",
        a: "Adapazarı merkezden MİA PARK OCEAN'a TEM Otoyolu üzerinden araçla yaklaşık 45-60 dakikada ulaşılır. Proje TEM Otoyolu'na yaklaşık 5 dakika mesafededir.",
      },
      {
        q: "Sakarya'da projeniz var mı?",
        a: "Hayır. MİA PARK OCEAN yalnızca İzmit MİA Bölgesi'nde yer almaktadır. Sakarya'dan yatırım yapmak isteyenler için ulaşım TEM üzerinden yaklaşık 45-60 dakikadır.",
      },
      {
        q: "Sakarya'dan yatırım yaparsam kiralama sürecini kim yönetir?",
        a: "Kiralama ve yönetim süreçleri için tek yetkili satıcı Ocean Gayrimenkul ile görüşebilirsiniz. Teslim sonrası kiralama desteği hakkında güncel bilgi satış ofisinden alınır.",
      },
    ],
    nearby: ["kocaeli-kartepe", "izmit-alikahya", "izmit-yahya-kaptan", "kocaeli-basiskele"],
    keywords: [
      "Sakarya'dan İzmit konut yatırımı",
      "Adapazarı İzmit satılık daire",
      "Sakarya faizsiz konut projesi",
    ],
  },
  {
    slug: "istanbul",
    name: "İstanbul",
    fullName: "İstanbul (Anadolu Yakası ve çevresi)",
    type: "il",
    parent: "Marmara",
    title: "İstanbul'dan İzmit'e Konut Yatırımı — MİA PARK OCEAN",
    description:
      "İstanbul'dan Kocaeli'ye yatırım: MİA PARK OCEAN'da faizsiz kooperatif modeli, İstanbul'a göre erişilebilir m² maliyeti, 60 ay vade.",
    drive: "1.5-2 saat",
    intro: [
      "İstanbul'da konut m² maliyetleri, aynı bütçeyle ulaşılabilecek daire büyüklüğünü belirgin şekilde sınırlıyor. Bu nedenle Marmara'nın gelişen ikinci halkası — Kocaeli ve çevresi — yatırımcılar için giderek daha çok değerlendiriliyor.",
      "Kocaeli, güçlü sanayi istihdamı, üniversitesi ve şehir hastanesiyle nitelikli konut talebini yıl boyu canlı tutan bir şehir. İzmit MİA Bölgesi de bu talebin yoğunlaştığı yeni gelişim aksı.",
      "MİA PARK OCEAN, banka kredisi ve faiz gerektirmeyen kooperatif modeliyle İstanbul'dan yatırım yapmak isteyenler için giriş bariyerini düşürüyor. Proje TEM Otoyolu'na yaklaşık 5 dakika mesafede.",
    ],
    highlights: [
      { title: "m² maliyeti farkı", text: "Aynı bütçeyle İzmit MİA'da belirgin şekilde daha geniş daire." },
      { title: "Otoyol erişimi", text: "TEM Otoyolu'na yaklaşık 5 dakika; İstanbul'a doğrudan bağlantı." },
      { title: "Canlı kira talebi", text: "Sanayi istihdamı, üniversite ve şehir hastanesi." },
      { title: "Kredisiz giriş", text: "Faizsiz, kefilsiz, 60 aya kadar vadeli ödeme." },
    ],
    faq: [
      {
        q: "İstanbul'dan MİA PARK OCEAN'a ulaşım ne kadar sürer?",
        a: "İstanbul Anadolu Yakası'ndan MİA PARK OCEAN'a TEM Otoyolu üzerinden araçla yaklaşık 1,5-2 saatte ulaşılır. Süre çıkış noktasına ve trafiğe göre değişir.",
      },
      {
        q: "İstanbul'da projeniz var mı?",
        a: "Hayır. MİA PARK OCEAN yalnızca İzmit MİA Bölgesi'nde (Kocaeli) yer almaktadır.",
      },
      {
        q: "İstanbul yerine Kocaeli'ye yatırım yapmanın mantığı nedir?",
        a: "İstanbul'da aynı bütçe genellikle daha küçük ve donatısı sınırlı bir daireye karşılık gelir. Kocaeli'nin sanayi istihdamı ve kurumsal donatıları kira talebini canlı tutar; MİA Bölgesi ise ulaşım yatırımlarıyla gelişen bir aks üzerindedir. Ayrıca kooperatif modeli faiz ve kredi yükü olmadan taksitli giriş imkânı sağlar.",
      },
    ],
    nearby: ["kocaeli-gebze", "kocaeli-darica", "kocaeli-cayirova", "izmit-yahya-kaptan"],
    keywords: [
      "İstanbul'dan Kocaeli konut yatırımı",
      "İstanbul yerine İzmit daire",
      "Kocaeli faizsiz konut projesi",
    ],
  },
];

export const locationBySlug = (slug: string) => locations.find((l) => l.slug === slug);

export const locationsByType = (type: LocationType) => locations.filter((l) => l.type === type);

export const locationGroups = [
  { type: "mahalle" as const, title: "İzmit Mahalleleri", lead: "Projeye en yakın mahalleler ve ulaşım süreleri." },
  { type: "ilce" as const, title: "Kocaeli İlçeleri", lead: "Kocaeli genelinden MİA Bölgesi'ne mesafeler ve bölge profilleri." },
  { type: "il" as const, title: "Komşu İller", lead: "Sakarya ve İstanbul'dan İzmit'e konut yatırımı." },
];

export const PROJECT_NAME = PROJECT;
