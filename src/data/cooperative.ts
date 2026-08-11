// Kooperatif güven içeriği — sitenin kalbi.
// Ton: savunmacı değil; şeffaf, özgüvenli, kanıta dayalı.
// Genel bilgilendirme amaçlıdır; güncel mevzuat ve kooperatif ana sözleşmesi esastır.

export const whyCooperative = {
  title: "Neden Kooperatif?",
  lead: "Kooperatif, kâr amacı gütmeyen bir yapıdır. Devletin kayıt ve denetim sistemine tabidir ve kararlarda ortağın söz hakkı vardır.",
  points: [
    {
      icon: "PiggyBank",
      title: "Maliyetine Konut",
      text: "Kooperatif kâr amacı gütmez. Ortaklar, araya müteahhit kârı girmeden konutu maliyetine alır. Aradaki fark da ortağın cebinde kalır.",
    },
    {
      icon: "Vote",
      title: "Söz Hakkı ve Şeffaflık",
      text: "Her ortağın genel kurulda bir oyu var. Yönetimi ortaklar seçer, kararlar herkesin gözü önünde alınır.",
    },
    {
      icon: "Landmark",
      title: "Devlet Gözetimi",
      text: "Kooperatif kayıt dışı bir oluşum değildir. Kuruluşundan tasfiyesine kadar devletin kayıt ve denetim sistemine tabidir.",
    },
    {
      icon: "ScrollText",
      title: "Anayasal Meşruiyet",
      text: "Kooperatifçilik, Anayasa'yla desteklenen bir modeldir. Anayasa'nın 171. maddesi, devletin kooperatifçiliğin gelişmesi için gereken tedbirleri almasını öngörür.",
    },
  ],
};

export const legalAssurance = {
  title: "Yasal Güvence ve Denetim",
  lead: "MİA PARK OCEAN'ı yapan kooperatif, kanunla tanımlı bir yapıdır. e-Devlet üzerinden izlenebilir ve birden çok katmanda denetlenir.",
  cards: [
    {
      icon: "BookMarked",
      title: "1163 Sayılı Kooperatifler Kanunu",
      text: "Kooperatifin kuruluşundan tasfiyesine, yönetiminden ortak haklarına kadar her şey, 1969'dan bu yana yürürlükte olan 1163 sayılı Kooperatifler Kanunu ile güvence altında.",
    },
    {
      icon: "MonitorSmartphone",
      title: "e-Devlet / KOOPBİS Şeffaflığı",
      text: "7339 sayılı Kanun ile kurulan Kooperatif Bilgi Sistemi (KOOPBİS) sayesinde ortaklar; ana sözleşmeye, organlara, genel kurul kararlarına ve kendi ortaklık kayıtlarına e-Devlet üzerinden ulaşabilir. Yani her şey kayıt altında, her şey görünür.",
    },
    {
      icon: "UserCheck",
      title: "Genel Kurulda Bakanlık Temsilcisi",
      text: "Kooperatifin genel kurul toplantıları, Bakanlık tarafından görevlendirilen bir temsilci (komiser) gözetiminde yapılır. Toplantının kanuna ve ana sözleşmeye uygunluğunu devlet denetler.",
    },
    {
      icon: "Layers",
      title: "Çok Katmanlı Denetim",
      text: "İçeride ortakların seçtiği bir denetim organı var. Dışarıda ise 7339 sayılı Kanun ile getirilen dış denetim ve ilgili Bakanlığın (Çevre, Şehircilik ve İklim Değişikliği Bakanlığı) denetim yetkisi devrede.",
    },
    {
      icon: "FileSearch",
      title: "Ortağın Bilgi Alma Hakkı",
      text: "Her ortağın, kanundan doğan bilgi edinme ve belge inceleme hakkı vardır. Yönetim de ortaklara hesap vermek zorundadır.",
    },
    {
      icon: "KeyRound",
      title: "Ferdileşme = Tapu",
      text: "İnşaat tamamlandığında daireler, tahsis sürecinin ardından ortaklar adına tapuya bağlanır. Amaç, her ortağın kendi bağımsız tapusuna kavuşması.",
    },
  ],
  disclaimer:
    "Bu bölüm genel bilgilendirme amaçlıdır; güncel mevzuat ve kooperatif ana sözleşmesi esastır.",
};

// Mia Park Ocean Güvence ve Denetim Sistemi — 14 kontrol (proje politikası çerçevesi).
// Yasal asgari yükümlülüklerin üzerine kurulması öngörülen kurumsal güven çerçevesidir.
export const trustSystem = {
  title: "Mia Park Ocean Güvence ve Denetim Sistemi",
  lead:
    "Aşağıdaki çerçeve, yasal asgari yükümlülüklerin üzerine kurulması öngörülen, projeye özel bir kurumsal güven modelidir. Hayata geçirilen unsurlar web sitesinde yayımlanır.",
  status: "Proje politikası olarak öngörülmektedir",
  controls: [
    { n: 1, title: "Kurumsal Banka Hesabı", text: "Bütün tahsilatların yalnızca kooperatif adına açılan banka hesabına yapılması; kişisel hesap ve elden ödeme yasağı." },
    { n: 2, title: "Yetki Matrisi", text: "Talep, teknik onay, mali kontrol ve banka ödeme yetkilerinin farklı kişiler arasında dağıtılması." },
    { n: 3, title: "Çift İmza ve Tutar Limitleri", text: "Belirli tutarların üzerindeki ödeme ve sözleşmelerde iki yetkilinin ortak onayı." },
    { n: 4, title: "Aylık Mali Rapor", text: "Tahsilat, ödeme, banka bakiyesi, borç, sözleşme yükümlülüğü, bütçe sapması ve nakit ihtiyacının açıklanması." },
    { n: 5, title: "Üç Aylık Bağımsız İnceleme", text: "Mali müşavir veya dış uzman tarafından kayıt, ödeme ve sözleşme örneklemesi yapılması." },
    { n: 6, title: "Teknik Hakediş Kontrolü", text: "Yüklenici ödemelerinin bağımsız mühendislik onayına bağlanması." },
    { n: 7, title: "Satın Alma Rekabeti", text: "Belirli eşik üzerindeki alımlarda en az üç teklif ve karşılaştırma tutanağı." },
    { n: 8, title: "İlişkili Taraf Bildirimi", text: "Yönetici, denetçi veya yakınlarının taraf olduğu işlemlerin beyanı ve karar sürecinden çekilme." },
    { n: 9, title: "Belge Merkezi", text: "Tapu, ruhsat, proje, genel kurul, rapor ve sözleşme özetlerinin üye portalında yayımlanması." },
    { n: 10, title: "İnşaat İlerleme Paneli", text: "Planlanan-gerçekleşen ilerleme, hakediş ve teslim tahmininin aylık güncellenmesi." },
    { n: 11, title: "Kura ve Tahsis Güvenliği", text: "Önceden ilan edilen yönerge, bağımsız gözlem, tutanak ve itiraz süreci." },
    { n: 12, title: "Etik ve İhbar Hattı", text: "Gizli bildirim, kayıt numarası, bağımsız inceleme ve misilleme yasağı." },
    { n: 13, title: "Risk Komitesi", text: "Maliyet, tahsilat, ruhsat, sözleşme ve teslim risklerinin üç aylık değerlendirilmesi." },
    { n: 14, title: "Yıllık Güven Raporu", text: "Yönetim, denetim, teknik ilerleme, bütçe ve risklerin tek raporda üyelere sunulması." },
  ],
};

export const cooperativeOrg = {
  name: "S.S. Yahya Kaptan Birlik Yapı Kooperatifi",
  short: "YKB",
  lead: "MİA PARK OCEAN'ın yapımcısı.",
  paragraphs: [
    "S.S. Yahya Kaptan Birlik Yapı Kooperatifi, 2021 yılında İzmit / Kocaeli'de kuruldu. Amacı basit: ortaklarını modern, nitelikli konuta maliyetine yakın bir fiyatla kavuşturmak.",
    "Kooperatif şeffaflıkla, düzenli genel kurullarla ve KOOPBİS kaydıyla yönetilir. Ortaklar kooperatifle ilgili bilgilere e-Devlet üzerinden ulaşabilir.",
    "MİA PARK OCEAN'ın satışı ise tek yetkili satıcı Ocean Gayrimenkul tarafından yürütülür.",
  ],
  facts: [
    { label: "Kuruluş Yılı", value: "2021" },
    { label: "Merkez", value: "İzmit / Kocaeli" },
    { label: "Telefon", value: "0546 640 2219" },
    { label: "MERSİS No", value: "0928116116500001" },
  ],
  address: "Ömerağa Mah. Abdurrahman Yüksel Cd. No:15/4 İzmit / Kocaeli",
};
