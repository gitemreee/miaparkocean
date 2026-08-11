// Kooperatif Bilgi Merkezi makaleleri — resmi içerik dosyasından (Sürüm 1.0).
// Yasak ifade kullanılmaz; kesinleşmemiş uygulamalar "planlanan" olarak etiketlenir.
// Yeni makale eklemek için diziye bir Article ekleyin.

export type ArticleSection = { heading: string; body: string[] };

export type Article = {
  slug: string;
  category: KbCategoryKey;
  tier: "article" | "guide";
  title: string;
  metaDescription: string;
  intro: string;
  sections: ArticleSection[];
  checklist?: string[];
  mpoNote?: boolean;
};

export type KbCategoryKey =
  | "model"
  | "uyelik"
  | "guven"
  | "finansman"
  | "insaat"
  | "yonetim"
  | "vergi";

export const kbCategories: { key: KbCategoryKey; title: string; desc: string }[] = [
  { key: "model", title: "Kooperatif Modeli", desc: "Kooperatifin yapısı, avantajları, demokratik yönetim ve ortak amaç." },
  { key: "uyelik", title: "Üyelik ve Üye Hakları", desc: "Üyeliğe kabul, devir, çıkış, oy, bilgi alma ve itiraz hakları." },
  { key: "guven", title: "Güven, Şeffaflık ve Denetim", desc: "İç ve dış denetim, genel kurul, KOOPBİS ve bağımsız kontroller." },
  { key: "finansman", title: "Finansman ve Maliyet", desc: "Bütçe, ödeme planı, ek maliyet, satın alma ve raporlama sistemi." },
  { key: "insaat", title: "Arsa, Ruhsat ve İnşaat", desc: "Tapu, imar, ruhsat, hakediş, teknik şartname, teslim ve ferdi mülkiyet." },
  { key: "yonetim", title: "Yönetim ve Kurumsal Yönetişim", desc: "Yönetim kurulu, etik, çıkar çatışması, çift imza ve hesap verebilirlik." },
  { key: "vergi", title: "Vergi ve Hukuki Bilgilendirme", desc: "Vergi muafiyetleri, ortak dışı işlemler ve proje özelinde uzman görüşü." },
];

// Kesinleşmemiş süreçler için standart proje politikası notu.
export const mpoPolicyNote =
  "Mia Park Ocean uygulaması (proje politikası olarak öngörülmektedir): Bu konuya ilişkin süreç, belge veya karar üye portalında erişilebilir olacak; sorumlu birim, işlem süresi ve itiraz yöntemi açıkça belirtilecektir. Nihai uygulama, anasözleşme ve genel kurul kararlarıyla kesinleşir.";

export const articles: Article[] = [
  {
    slug: "kooperatif-modeli-nedir",
    category: "model",
    tier: "article",
    title: "Kooperatif Modeli Nedir?",
    metaDescription:
      "Mia Park Ocean kooperatif modelinin nasıl çalıştığını, ortakların projeye nasıl katıldığını ve karar süreçlerinin nasıl yönetildiğini öğrenin.",
    intro:
      "Kooperatif modeli; kişilerin ortak ekonomik ve sosyal ihtiyaçlarını karşılıklı yardım, dayanışma ve demokratik yönetim yoluyla karşılamak üzere oluşturdukları kurumsal bir yapıdır.",
    sections: [
      {
        heading: "Mia Park Ocean açısından modelin anlamı",
        body: [
          "Mia Park Ocean'da üyeler yalnızca ödeme yapan müşteriler değil, kooperatifin ortaklarıdır. Projenin bütçesi, yönetim organları, temel yatırım kararları ve denetim süreçleri anasözleşme, mevzuat ve genel kurul kararları çerçevesinde yürütülür.",
          "Kooperatif tüzel kişiliği; arsa edinimi, sözleşmeler, banka hesapları, ruhsat süreçleri ve proje harcamalarının tek bir kurumsal yapı altında yönetilmesini sağlar. Yönetim kurulu günlük işleri yürütür; en yetkili karar organı ise ortakların oluşturduğu genel kuruldur.",
        ],
      },
      {
        heading: "Kooperatif ile klasik satış modeli arasındaki fark",
        body: [
          "Klasik ön satış modelinde alıcı, geliştirici şirketin belirlediği fiyat ve sözleşme şartları üzerinden hareket eder. Kooperatif modelinde ortaklar, proje maliyetlerine ve yönetim kararlarına belirlenen kurallar çerçevesinde katılır. Bu yapı maliyet görünürlüğü ve demokratik katılım sağlayabilir; buna karşılık ortakların mali yükümlülükleri ve proje riskleri konusunda açık bilgilendirme yapılmasını gerektirir.",
        ],
      },
      {
        heading: "Modelin başarı koşulları",
        body: [
          "Başarılı bir kooperatif modeli; doğru anasözleşme, temiz ve doğrulanabilir arsa hukuku, gerçekçi bütçe, güçlü tahsilat disiplini, uzman yönetim, bağımsız teknik kontrol ve düzenli mali denetim gerektirir. Kooperatif unvanı tek başına güvence değildir; güven, süreçlerin izlenebilirliğiyle oluşur.",
        ],
      },
    ],
    checklist: [
      "Kooperatif türünü proje kullanımına göre kesinleştirin.",
      "Arsa edinim modelini ve tapu sahibini açıklayın.",
      "Ödeme ve tahsis kurallarını anasözleşme ve genel kurul kararlarıyla uyumlu kurun.",
      "Üye portalı ve raporlama takvimini üyelik başlamadan önce planlayın.",
    ],
  },
  {
    slug: "kooperatif-modelinin-avantajlari",
    category: "model",
    tier: "article",
    title: "Kooperatif Modelinin Avantajları",
    metaDescription:
      "Kooperatif modeliyle gayrimenkul geliştirmenin maliyet, satın alma gücü, demokratik yönetim ve şeffaflık açısından avantajlarını inceleyin.",
    intro:
      "Kooperatif modeli doğru kurulduğunda üyelerin toplu satın alma gücünü, ortak karar mekanizmasını ve mali görünürlüğü aynı çatı altında birleştirir.",
    sections: [
      {
        heading: "Toplu satın alma ve ölçek ekonomisi",
        body: [
          "Malzeme, mimarlık, mühendislik, şantiye ve yüklenici hizmetlerinin toplu alımı daha güçlü pazarlık kapasitesi yaratabilir. Avantajın üyeye yansıması için alımların rekabetçi teklifler, teknik şartnameler ve kayıtlı kararlarla yapılması gerekir.",
        ],
      },
      {
        heading: "Demokratik yönetim",
        body: [
          "Kooperatifçilikte temel yaklaşım, sermaye büyüklüğünden bağımsız demokratik kontroldür. Üyeler genel kurula katılarak yönetim ve denetim organlarını seçebilir, faaliyet raporlarını değerlendirebilir ve önemli kararlar üzerinde oy kullanabilir.",
        ],
      },
      {
        heading: "Maliyet görünürlüğü",
        body: [
          "Proje bütçesi ve gerçekleşen harcamalar düzenli raporlandığında üyeler yatırımlarının hangi aşamada olduğunu daha net izler. Bu görünürlük yalnızca toplam harcama rakamıyla sınırlı kalmamalı; sözleşme, hakediş, tahsilat ve kalan iş maliyeti birlikte açıklanmalıdır.",
        ],
      },
      {
        heading: "Ortak değer üretimi",
        body: [
          "Kooperatifin odağı, dış yatırımcıya azami kâr aktarmaktan ziyade ortakların ihtiyacını kurallı ve sürdürülebilir şekilde karşılamaktır. Bunun sonucu olarak proje yönetimi üye değeri, kalite ve uzun vadeli işletme performansı etrafında kurgulanabilir.",
        ],
      },
    ],
    checklist: [
      "Her büyük satın almada en az üç karşılaştırılabilir teklif alın.",
      "Üyelere maliyet tahmini ile satış fiyatı arasındaki farkı açık anlatın.",
      "Yönetim ve denetim raporlarını periyodik yayımlayın.",
      "Avantaj söylemini garanti veya kesin tasarruf vaadine dönüştürmeyin.",
    ],
  },
  {
    slug: "kooperatifte-guven",
    category: "guven",
    tier: "article",
    title: "Kooperatif Sisteminde Güven Nasıl Sağlanır?",
    metaDescription:
      "Bir kooperatif projesinde güvenin hangi belgeler, denetimler ve şeffaflık uygulamalarıyla oluşturulduğunu öğrenin.",
    intro:
      "Güven, tanıtım diliyle değil; doğrulanabilir belgeler, görev ayrılığı, düzenli raporlama ve bağımsız kontrol mekanizmalarıyla kurulur.",
    sections: [
      {
        heading: "Arsa ve ruhsat güvenliği",
        body: [
          "Tapu kaydı, malik bilgisi, takyidatlar, imar durumu, yapı ruhsatı ve onaylı projeler üyelerin inceleyebileceği biçimde açıklanmalıdır. Arsa kooperatif adına değilse, devir veya tapuya şerhli sözleşme mekanizması hukuk müşavirince değerlendirilmelidir.",
        ],
      },
      {
        heading: "Finansal güvenlik",
        body: [
          "Tahsilatlar yalnızca kooperatif adına açılmış banka hesaplarına yapılmalı, elden veya kişisel hesaba ödeme kabul edilmemelidir. Her ödeme fatura, sözleşme, hakediş veya yetkili kurul kararına dayanmalıdır.",
        ],
      },
      {
        heading: "Teknik güvenlik",
        body: [
          "Yüklenici ödemeleri takvim gününe değil, bağımsız teknik uzman tarafından doğrulanmış fiziki ilerlemeye bağlanmalıdır. Kullanılan malzemeler teknik şartnameye göre kontrol edilmeli; eksik ve kusurlu imalatlar ödeme öncesinde kayda alınmalıdır.",
        ],
      },
      {
        heading: "Kurumsal güvenlik",
        body: [
          "Yönetim kurulu, denetleme organı, mali müşavir, teknik müşavir ve satın alma süreçleri arasında görev ayrılığı kurulmalıdır. Aynı kişinin talep, onay, ödeme ve denetim zincirinin tamamını kontrol etmesine izin verilmemelidir.",
        ],
      },
    ],
    checklist: [
      "Tüm banka hesaplarını üyelik belgelerinde açıkça tanımlayın.",
      "Aylık mali özet ve üç aylık teknik rapor yayımlayın.",
      "Yönetici ve yakınlarıyla işlemler için çıkar çatışması prosedürü oluşturun.",
      "İhbar, şikâyet ve itiraz kanalı kurun.",
    ],
  },
  {
    slug: "kooperatif-uyelerinin-haklari",
    category: "uyelik",
    tier: "article",
    title: "Kooperatif Üyelerinin Hakları",
    metaDescription:
      "Kooperatif üyelerinin bilgi alma, genel kurula katılma, oy kullanma, devir, çıkış ve itiraz haklarını ayrıntılı olarak inceleyin.",
    intro:
      "Kooperatif ortaklığı, ödeme yükümlülüğünün yanında yönetime katılma ve denetim süreçlerinde söz sahibi olma hakkı verir.",
    sections: [
      {
        heading: "Bilgi alma ve inceleme hakkı",
        body: [
          "Üyeler mevzuat ve anasözleşme çerçevesinde faaliyet raporu, bilanço, gelir-gider tablosu ve denetim raporları gibi temel belgeleri inceleyebilir. Proje özelinde daha geniş bir dijital arşiv sunulması şeffaflığı güçlendirir.",
        ],
      },
      {
        heading: "Genel kurula katılma ve oy hakkı",
        body: [
          "Ortaklar genel kurula katılabilir, gündem maddeleri hakkında görüş açıklayabilir ve oy kullanabilir. Temel ilke, ortakların demokratik kontrolüdür. Temsil ve vekâlet şartları anasözleşme ve güncel mevzuata göre uygulanır.",
        ],
      },
      {
        heading: "Seçme, seçilme ve yönetimi değerlendirme hakkı",
        body: [
          "Şartları taşıyan üyeler yönetim ve denetim organlarına aday olabilir. Genel kurul, bu organların faaliyetlerini değerlendirir, seçim yapar ve hukuki şartlar oluştuğunda görev değişikliği kararı alabilir.",
        ],
      },
      {
        heading: "Devir, çıkış ve itiraz hakları",
        body: [
          "Ortaklık devri ve çıkış işlemleri anasözleşmede belirlenen prosedüre tabidir. Çıkarma kararları yalnızca anasözleşmede açıkça gösterilen sebeplere dayanmalı ve üyeye yasal itiraz yolları bildirilmelidir.",
        ],
      },
    ],
    checklist: [
      "Üye haklarını tek sayfalık “Üye Hakları Beyanı”nda yayımlayın.",
      "Belge talepleri için cevap süresi belirleyin.",
      "Genel kurul çağrı ve dokümanlarını zamanında paylaşın.",
      "İtirazların bağımsız kayıt numarasıyla izlenmesini sağlayın.",
    ],
  },
  {
    slug: "kooperatif-denetim-sistemi",
    category: "guven",
    tier: "article",
    title: "Kooperatif Nasıl Denetlenir?",
    metaDescription:
      "Kooperatiflerde genel kurul, denetleme organı, dış denetim, mali müşavirlik ve kamu gözetiminin nasıl çalıştığını öğrenin.",
    intro:
      "Etkili denetim tek bir rapordan ibaret değildir. Denetim; hukuki, mali, operasyonel ve teknik kontrol katmanlarının birlikte çalışmasıdır.",
    sections: [
      {
        heading: "Genel kurul denetimi",
        body: [
          "Genel kurul, kooperatifin en yetkili organıdır. Yönetim faaliyetleri, mali tablolar, bütçe, çalışma programı ve denetim raporları genel kurulda değerlendirilir. İbra kararı, yöneticilerin her türlü sorumluluğunu otomatik olarak ortadan kaldıran sınırsız bir koruma olarak yorumlanmamalıdır.",
        ],
      },
      {
        heading: "Denetleme organı",
        body: [
          "Kooperatifin denetleme organı, genel kurul adına işlem ve hesapları inceler. Denetçilerin bağımsız hareket edebilmesi, yeterli bilgi ve belgelere erişmesi ve bulgularını açık şekilde raporlaması gerekir.",
        ],
      },
      {
        heading: "Dış denetim",
        body: [
          "Mevzuatta belirlenen kriterleri taşıyan kooperatifler dış denetime tabidir. Mia Park Ocean yasal eşiğe girmese dahi güven politikasının parçası olarak gönüllü bağımsız denetim yaptırabilir. Dış denetçinin seçimi ve görevlendirilmesi güncel mevzuata uygun yürütülmelidir.",
        ],
      },
      {
        heading: "Teknik ve sözleşmesel denetim",
        body: [
          "Mali denetim yapılan ödemenin kayıtlarda bulunup bulunmadığını kontrol eder; fakat imalatın gerçekten yapılıp yapılmadığını tek başına doğrulamaz. Bu nedenle teknik müşavir, hakediş ve kalite kontrol raporları mali denetimin tamamlayıcısıdır.",
        ],
      },
    ],
    checklist: [
      "Yıllık denetim planı oluşturun.",
      "Mali, teknik ve hukuki denetimleri ayrı raporlayın.",
      "Denetçi bulgularına karşı yönetim aksiyon planı yayımlayın.",
      "Kritik bulgular için kapanış tarihi ve sorumlu kişi atayın.",
    ],
  },
  {
    slug: "koopbis-nedir",
    category: "guven",
    tier: "article",
    title: "KOOPBİS Nedir?",
    metaDescription:
      "KOOPBİS sisteminin kooperatif bilgileri, mali tablolar, genel kurul belgeleri ve ortakların bilgi erişimindeki rolünü inceleyin.",
    intro:
      "KOOPBİS, kooperatifçilik işlemlerinin merkezi elektronik sistem üzerinden yürütülmesine ve belirli verilerin kamu gözetiminde kayıt altına alınmasına hizmet eder.",
    sections: [
      {
        heading: "Sistemin işlevi",
        body: [
          "KOOPBİS; kooperatif bilgileri, ortak kayıtları, yönetim ve denetim verileri ile genel kurul süreçlerinin elektronik ortamda izlenmesini destekler. Yönetim kurulunun sisteme doğru ve zamanında veri girişi sorumluluğu bulunmaktadır.",
        ],
      },
      {
        heading: "Üyelere sağladığı fayda",
        body: [
          "Mevzuat kapsamında erişilebilen rapor ve kayıtlar üyelerin bilgi edinmesini kolaylaştırabilir. Ancak KOOPBİS, proje yönetiminde ihtiyaç duyulan günlük teknik ve finansal detayların tamamını tek başına karşılamaz.",
        ],
      },
      {
        heading: "Mia Park Ocean Üye Portalı ile tamamlayıcı yapı",
        body: [
          "Mia Park Ocean'a özel portalda bütçe, tahsilat özeti, gerçekleşen maliyet, teknik ilerleme, hakediş özeti, genel kurul kararları, tapu ve ruhsat belgeleri, teslim takvimi ve soru-cevap kayıtlarının bulunması planlanmaktadır. Portal, KOOPBİS'in yerine geçmez; proje bazlı şeffaflığı güçlendirir.",
        ],
      },
    ],
    checklist: [
      "KOOPBİS sorumlusu ve yedek sorumlu belirleyin.",
      "Veri giriş takvimi oluşturun.",
      "Üye portalındaki belgeleri sürüm numarasıyla yayımlayın.",
      "Kişisel verileri KVKK ilkelerine uygun koruyun.",
    ],
  },
  {
    slug: "kooperatif-genel-kurulu",
    category: "guven",
    tier: "article",
    title: "Genel Kurul Nedir ve Nasıl Çalışır?",
    metaDescription:
      "Kooperatif genel kurulunun yetkileri, oy sistemi, yönetim seçimi ve üyelerin karar süreçlerine katılımı hakkında bilgi alın.",
    intro:
      "Genel kurul, ortakların kooperatifin temel yönünü belirlediği en yetkili karar organıdır.",
    sections: [
      {
        heading: "Başlıca yetkiler",
        body: [
          "Mali tabloların görüşülmesi, yönetim ve denetim organlarının seçimi, bütçe ve çalışma programı, ortaklardan alınacak ödemeler, taşınmaz işlemleri ve önemli yatırım kararları genel kurul gündeminin temel konularıdır. Yetki dağılımı kanun ve anasözleşmeye göre belirlenir.",
        ],
      },
      {
        heading: "Toplantı hazırlığı",
        body: [
          "Toplantı çağrısı, gündem, faaliyet raporu, mali tablolar ve denetim raporları mevzuatta öngörülen süre ve usule göre hazırlanmalıdır. Bakanlık temsilcisi talebi gereken hallerde zamanında yapılmalıdır.",
        ],
      },
      {
        heading: "Kararların kayıt altına alınması",
        body: [
          "Hazirun listesi, tutanak, oy sonuçları ve ek belgeler eksiksiz saklanmalı; gerekli bildirim ve tescil işlemleri tamamlanmalıdır. Üyelere karar özeti ve uygulama takvimi gönderilmesi kurumsal güveni artırır.",
        ],
      },
    ],
    checklist: [
      "Yıllık genel kurul takvimini önceden duyurun.",
      "Gündem açıklamalarını sade dille hazırlayın.",
      "Kararların mali etkisini üye başına gösterin.",
      "Toplantı sonrası uygulama raporu yayımlayın.",
    ],
  },
  {
    slug: "ek-odeme-ve-maliyet",
    category: "finansman",
    tier: "article",
    title: "Ek Ödeme ve Maliyet Artışı Nasıl Yönetilir?",
    metaDescription:
      "Kooperatiflerde taksit, ek ödeme, maliyet artışı ve genel kurul kararlarının nasıl yönetilmesi gerektiğini öğrenin.",
    intro:
      "İnşaat maliyetleri değişebilir; güvenilir yönetim, bu gerçeği gizlemek yerine değişiklikleri önceden tanımlanmış ve denetlenebilir bir prosedürle yönetir.",
    sections: [
      {
        heading: "Ek ödeme kararı",
        body: [
          "Konut yapı kooperatifi modelinde ortaklardan alınacak taksit ve ilave ödemelerin genel kurul yetkisi çerçevesinde belirlenmesi esastır. Yönetim kurulunun yetkisi, anasözleşme ve genel kurul kararlarıyla sınırlandırılmalıdır.",
        ],
      },
      {
        heading: "Gerekçelendirme standardı",
        body: [
          "Her maliyet artışı için neden, tutar, alternatifler, üyeye etkisi, teslim takvimine etkisi ve bütçe sonrası kalan risk açıklanmalıdır. “Piyasa şartları” gibi genel ifadeler tek başına yeterli gerekçe sayılmamalıdır.",
        ],
      },
      {
        heading: "Risk rezervi",
        body: [
          "Başlangıç bütçesinde öngörülemeyen giderler için ölçülü bir risk rezervi ayrılması, ani ek ödeme ihtiyacını azaltabilir. Rezerv kullanımı ayrı raporlanmalı ve genel bütçe içinde görünür olmalıdır.",
        ],
      },
    ],
    checklist: [
      "Maliyet artışı prosedürünü anasözleşme ve iç yönergeyle uyumlu kurun.",
      "Bağımsız maliyet doğrulaması alın.",
      "En az iki alternatif senaryo sunun.",
      "Ödeme kararını yazılı bildirin ve üyeye makul planlama süresi tanıyın.",
    ],
  },
  {
    slug: "insaat-teknik-denetim",
    category: "insaat",
    tier: "article",
    title: "İnşaat Süreci Nasıl Denetlenir?",
    metaDescription:
      "Mia Park Ocean inşaatının hakediş, kalite kontrol, malzeme onayı ve ilerleme raporlarıyla nasıl denetlenebileceğini öğrenin.",
    intro: "Şantiyede gerçekleşen iş ile yapılan ödeme aynı doğrulama zincirine bağlanmalıdır.",
    sections: [
      {
        heading: "Hakediş sistemi",
        body: [
          "Yüklenici, tamamladığı imalatları miktar ve tutar bazında hakedişe dönüştürür. Bağımsız teknik müşavir yerinde ölçüm yapar, sözleşme ve birim fiyatlarla karşılaştırır, kusurlu veya eksik işleri düşer. Onaylanan tutar mali kontrol sonrasında ödenir.",
        ],
      },
      {
        heading: "Kalite güvence",
        body: [
          "Malzeme marka ve teknik özellikleri şartnamede açıkça tanımlanmalıdır. Numune ve ürün onayları kayıt altına alınmalı; değişiklikler eşdeğerlik analizi ve yetkili onay olmadan uygulanmamalıdır.",
        ],
      },
      {
        heading: "İlerleme raporu",
        body: [
          "Aylık raporda planlanan ve gerçekleşen ilerleme yüzdeleri, kritik işler, gecikme sebepleri, yapılan ödeme, kalan sözleşme bedeli ve güncel teslim tahmini birlikte gösterilmelidir. Drone görüntüleri destekleyici olabilir; teknik raporun yerine geçmez.",
        ],
      },
    ],
    checklist: [
      "Bağımsız teknik müşavir görevlendirin.",
      "Hakediş onay matrisini yazılı hale getirin.",
      "Malzeme değişikliklerini üyeye açıklayın.",
      "Gecikmeler için düzeltici faaliyet planı yayımlayın.",
    ],
  },
  {
    slug: "kooperatif-uyelik-devri",
    category: "uyelik",
    tier: "article",
    title: "Üyelik Devri Nasıl Yapılır?",
    metaDescription:
      "Kooperatif üyeliğinin devri, devralanın hak ve yükümlülükleri ve güvenli devir kontrol listesini inceleyin.",
    intro:
      "Üyelik devri, yalnızca iki kişi arasındaki satış işlemi değil; kooperatif nezdindeki bütün hak ve yükümlülüklerin kurallı biçimde yeni ortağa geçirilmesidir.",
    sections: [
      {
        heading: "Devir şartları",
        body: [
          "Devralacak kişinin anasözleşmedeki ortaklık şartlarını taşıması gerekir. Başvuru, yönetim kurulu incelemesi ve ortaklık kaydı usulüne uygun tamamlanmalıdır.",
        ],
      },
      {
        heading: "Mali durum tespiti",
        body: [
          "Devirden önce ödenen sermaye ve aidatlar, gecikmiş borçlar, gelecek taksitler, genel kurulca kararlaştırılmış ek yükümlülükler ve bağımsız bölüm tahsis durumu yazılı olarak doğrulanmalıdır.",
        ],
      },
      {
        heading: "Güvenli devir belgesi",
        body: [
          "Mia Park Ocean'ın “Üyelik Mali ve Hukuki Durum Belgesi” düzenlemesi planlanmaktadır. Belgede üyelik numarası, tahsis bilgisi, toplam tahakkuk, ödeme, borç, gecikme, temlik veya haciz kaydı ve devam eden uyuşmazlıklar yer alır.",
        ],
      },
    ],
    checklist: [
      "Standart devir başvuru formu hazırlayın.",
      "Mali durum belgesi olmadan devir onayı vermeyin.",
      "Yeni üyeye anasözleşme ve son genel kurul kararlarını teslim edin.",
      "Devir bedeli ile kooperatif alacağını birbirinden ayırın.",
    ],
  },
  {
    slug: "kooperatifte-esitlik",
    category: "uyelik",
    tier: "article",
    title: "Kooperatiflerde Eşitlik İlkesi",
    metaDescription:
      "Kooperatif üyelerinin oy, bilgi erişimi, ödeme, daire tahsisi ve yönetim süreçlerinde eşitlik ilkesini öğrenin.",
    intro:
      "Kooperatifin sürdürülebilirliği, benzer durumda bulunan ortaklara objektif ve önceden bilinen kuralların uygulanmasına bağlıdır.",
    sections: [
      {
        heading: "Eşit oy ve bilgi erişimi",
        body: [
          "Demokratik kontrol ilkesi gereği ortakların oy ve bilgi edinme hakları ayrımcı biçimde sınırlandırılmamalıdır. Yönetici olmak, üyeye kişisel ayrıcalık sağlamaz.",
        ],
      },
      {
        heading: "Maliyet farklılıkları eşitsizlik midir?",
        body: [
          "Bağımsız bölüm büyüklüğü, katı, cephesi veya maliyet grubuna göre farklı ödeme belirlenebilir. Ancak farklılık teknik hesap, genel kurul kararı ve önceden açıklanmış objektif kriterlere dayanmalıdır.",
        ],
      },
      {
        heading: "Tahsis ve kura güvenliği",
        body: [
          "Tahsis yöntemi, kategori, kura usulü, seçim sırası, maliyet farkı ve itiraz prosedürü üyelikten önce açıklanmalıdır. Yönetim kurulu üyelerine kura dışı veya belgesiz avantaj sağlanmamalıdır.",
        ],
      },
    ],
    checklist: [
      "Eşitlik ve tahsis yönergesi hazırlayın.",
      "Kura sürecini bağımsız gözlemciyle yürütün.",
      "Maliyet farklarını ekspertiz veya teknik hesapla destekleyin.",
      "Yönetici işlemlerini ayrıca raporlayın.",
    ],
  },
  {
    slug: "kooperatif-vergi",
    category: "vergi",
    tier: "article",
    title: "Kooperatiflerde Vergi ve Mali Yükümlülükler",
    metaDescription:
      "Kooperatiflerin vergi muafiyetleri, ortak dışı işlemleri ve proje özelinde değerlendirilmesi gereken mali yükümlülükleri hakkında bilgi alın.",
    intro:
      "Kooperatif unvanı otomatik vergi muafiyeti sağlamaz; muafiyetler kanuni şartlara ve fiili faaliyet modeline bağlıdır.",
    sections: [
      {
        heading: "Kurumlar vergisi yönü",
        body: [
          "Anasözleşmede gerekli sınırlamaların bulunması ve uygulamada bu şartlara uyulması önemlidir. Ortak dışı işlemler ayrı iktisadi işletme ve vergilendirme sonuçları doğurabilir.",
        ],
      },
      {
        heading: "KDV yönü",
        body: [
          "Konut teslimlerinde geçmişte uygulanan bazı istisnalar değişmiştir. Teslimin niteliği, yapı ruhsatı tarihi, alıcının durumu ve güncel KDV düzenlemeleri proje özelinde uzman tarafından değerlendirilmelidir.",
        ],
      },
      {
        heading: "Vergi iletişimi",
        body: [
          "Web sitesinde “tamamen vergiden muaf” gibi kesin ifadeler kullanılmaz. En doğru yaklaşım, vergisel uygulamaların güncel mevzuat ve proje işlemleri doğrultusunda yetkili mali müşavirlerce yönetildiğini belirtmektir.",
        ],
      },
    ],
    checklist: [
      "YMM/SMMM vergi görüşü alın.",
      "Ortak dışı işlemleri ayrı izleyin.",
      "Arsa, ruhsat ve teslim modelini vergi planıyla birlikte değerlendirin.",
      "Eski tarihli internet içeriklerine dayanarak vergi vaadi vermeyin.",
    ],
  },
  {
    slug: "koopbis-yonetmeligi-2022",
    category: "guven",
    tier: "article",
    title: "KOOPBİS Yönetmeliği (2022): Kooperatif Bilgi Sistemi",
    metaDescription:
      "2022'de yürürlüğe giren KOOPBİS Yönetmeliğiyle kooperatiflerin sisteme hangi bilgileri hangi sürelerde girmesi gerektiğini, yetkili atamasını ve aydınlatma metni yükümlülüğünü öğrenin.",
    intro:
      "14 Ocak 2022 tarihli Resmî Gazete'de yayımlanan Kooperatif Bilgi Sistemi (KOOPBİS) Yönetmeliği; kooperatiflerin, üst kuruluşların ve ortakların kooperatifçilik hizmetlerine elektronik ortamda erişimini düzenler. Sistem, kooperatife ilişkin temel bilgileri kamu gözetiminde kayıt altına alarak şeffaflığı ve ortakların bilgiye erişimini güçlendirir.",
    sections: [
      {
        heading: "KOOPBİS nedir ve neyi amaçlar?",
        body: [
          "KOOPBİS (Kooperatif Bilgi Sistemi); kooperatiflerin, üst kuruluşların ve bunların ortaklarının kooperatifçilik hizmetlerine elektronik ortamda eriştiği merkezi bir sistemdir. Amaç, kooperatife ilişkin temel bilgilerin düzenli, güncel ve erişilebilir biçimde tutulmasıdır.",
          "S.S. Yahya Kaptan Birlik Yapı Kooperatifi de faaliyetlerini KOOPBİS kaydıyla yürütür; böylece Mia Park Ocean ortakları, kooperatife ait bilgilere e-Devlet üzerinden ulaşabilir.",
        ],
      },
      {
        heading: "KOOPBİS yetkilisi kimdir, nasıl belirlenir?",
        body: [
          "KOOPBİS işlemlerini yürütmek üzere yönetim kurulunun yetki verdiği kişiler KOOPBİS yetkilisi olarak tanımlanır. Yönetim kurulu üyelerinin her biri sistemde işlem yapmaya yetkilidir; ayrıca ortak olmayan kişiler ve kooperatif personeli de yetkili olarak atanabilir.",
          "Yetkilendirme için, yetkilendirmenin yapıldığı yönetim kurulu kararının bir nüshası ile yetkilendirilen kişinin bilgileri İl Müdürlüğüne iletilir ve yetki tanımlaması bu şekilde yaptırılır.",
        ],
      },
      {
        heading: "Faaliyete geçtikten sonra 6 ay içinde girilecek bilgiler",
        body: [
          "Kooperatif faaliyete geçtikten sonra altı ay içinde şu bilgiler sisteme girilir: ticaret sicili kayıtları, finansal tablolar, yönetim kurulu ve denetim kurulu faaliyet raporları, genel kurul toplantı evrakları, ortakların kimlik bilgileri ile pay ve ödemeleri, gayrimenkul bilgileri ve gerekli görülen diğer bilgiler.",
        ],
      },
      {
        heading: "Sürekli güncellenen ve genel kurul sonrası yüklenen bilgiler",
        body: [
          "En geç on beş gün içinde yüklenmesi gereken bilgiler; yeni ortakların kimlik, iletişim, pay ve ödeme bilgileri ile ortaklık kabulüne dair yönetim kurulu kararı, ortak bilgilerindeki değişiklikler, yönetim ve denetim kurulu faaliyet raporları, mali tablolar ve dış denetçi raporlarıdır.",
          "Genel kurul toplantısından sonra ise on beş gün içinde toplantı tutanağı, gündem ve genel durum bildirim formu sisteme yüklenir.",
        ],
      },
      {
        heading: "KOOPBİS aydınlatma metni yükümlülüğü",
        body: [
          "Kişisel verilerin KOOPBİS aracılığıyla işlendiğini belirten aydınlatma metninin, ortaklığa kabul tarihinden sonra ortaklara imzalatılması zorunludur. Bu yükümlülük, KVKK ilkeleriyle uyumlu bir veri işleme sürecinin parçasıdır.",
          "Bakanlığın yayımladığı resmî aydınlatma metnine şu adresten ulaşılabilir: https://ticaret.gov.tr/data/5d41985f13b87639ac9e0095/Ayd%C4%B1nlatma%20Metni%20-%20KOOPB%C4%B0S.pdf",
        ],
      },
      {
        heading: "Resmî kaynak ve bilgilendirme",
        body: [
          "Yönetmeliğin tam metni 14 Ocak 2022 tarihli Resmî Gazete'de yayımlanmıştır: https://www.resmigazete.gov.tr/eskiler/2022/01/20220114-1.htm",
          "Bu içerik genel bilgilendirme amaçlıdır; güncel mevzuat ve kooperatif anasözleşmesi esastır.",
        ],
      },
    ],
    checklist: [
      "KOOPBİS yetkilisi ve yedeğini yönetim kurulu kararıyla belirleyin.",
      "Faaliyete geçişten itibaren altı aylık ilk veri girişini takvime bağlayın.",
      "Ortak ve mali bilgi değişikliklerini on beş gün içinde sisteme işleyin.",
      "Aydınlatma metnini yeni ortaklara ortaklık kabulünden sonra imzalatın.",
    ],
    mpoNote: true,
  },
  {
    slug: "kooperatifcilik-egitimi-yonetmeligi",
    category: "guven",
    tier: "article",
    title: "Kooperatifçilik Eğitimi Yönetmeliği (2022)",
    metaDescription:
      "2022 Kooperatifçilik Eğitimi Yönetmeliğine göre yönetim ve denetim kurulu üyelerinin hangi kooperatiflerde, hangi sürede ve kaç ders saati eğitim alması gerektiğini öğrenin.",
    intro:
      "14 Ocak 2022 tarihli Resmî Gazete'de yayımlanan Kooperatifçilik Eğitimi Yönetmeliği; belirli kooperatiflerde görev alan yönetim ve denetim kurulu üyelerine zorunlu eğitim getirerek kurumsal yönetim kalitesini yükseltmeyi amaçlar. Bilinçli ve eğitimli organlar, ortakların hak ve menfaatlerinin korunmasına doğrudan katkı sağlar.",
    sections: [
      {
        heading: "Kimler eğitim almak zorundadır?",
        body: [
          "Yönetmelik kapsamındaki kooperatif ve üst kuruluşların yönetim kurulu ile denetim kurulu asıl ve yedek üyeleri kooperatifçilik eğitimi almakla yükümlüdür. Eğitim, seçilen kişilerin görevlerini mevzuata uygun ve bilinçli biçimde yürütmesini hedefler.",
        ],
      },
      {
        heading: "Hangi kooperatifler kapsamdadır?",
        body: [
          "Esnaf ve sanatkârlar kredi ve kefalet, tarım satış, tarım kredi ve pancar ekicileri kooperatiflerinde herhangi bir kriter aranmaksızın eğitim zorunludur.",
          "Bunun yanında; inşaat ruhsatı alınmış ve ortak sayısı 50 veya daha fazla olan yapı, turizm geliştirme ve gayrimenkul işletme kooperatifleri; ortak sayısı 50 ve üzeri taşıma kooperatifleri; 20 milyon TL üzerinde satış hasılatı olan kooperatifler ile 1.000'den fazla ortağı bulunan kooperatifler de kapsamdadır.",
        ],
      },
      {
        heading: "Mia Park Ocean açısından anlamı",
        body: [
          "S.S. Yahya Kaptan Birlik Yapı Kooperatifi bir yapı kooperatifidir. Yönetmelik, inşaat ruhsatı alınmış ve ortak sayısı 50 ve üzeri olan yapı kooperatiflerini doğrudan kapsama aldığından, bu tür bir projede yönetim ve denetim organlarının eğitim yükümlülüğü öne çıkar.",
          "Eğitimli organlar; şeffaf raporlama, doğru genel kurul yönetimi ve mevzuata uygun karar alma açısından ortaklara güvence sağlar.",
        ],
      },
      {
        heading: "Eğitim süresi ve zamanı",
        body: [
          "Eğitim, seçimleri takip eden 9 ay içinde tamamlanır. Program; 30 ders saati temel eğitim ve 10 ders saati destekleyici eğitim olmak üzere en az 40 ders saatinden oluşur ve yüz yüze veya uzaktan eğitim yöntemiyle verilebilir.",
        ],
      },
      {
        heading: "Resmî kaynak ve bilgilendirme",
        body: [
          "Yönetmeliğin tam metni 14 Ocak 2022 tarihli Resmî Gazete'de yayımlanmıştır: https://www.resmigazete.gov.tr/eskiler/2022/01/20220114-3.htm",
          "Bu içerik genel bilgilendirme amaçlıdır; güncel mevzuat ve kooperatif anasözleşmesi esastır.",
        ],
      },
    ],
    checklist: [
      "Seçilen yönetim ve denetim üyelerinin eğitim yükümlülüğünü kayda alın.",
      "Eğitimi seçimden itibaren 9 ay içinde tamamlanacak şekilde planlayın.",
      "En az 40 ders saatlik (30 temel + 10 destekleyici) programı takip edin.",
      "Eğitim katılım ve tamamlama belgelerini üye bilgisine açık tutun.",
    ],
    mpoNote: true,
  },
  {
    slug: "elektronik-genel-kurul-egks-yonetmeligi",
    category: "guven",
    tier: "article",
    title: "Elektronik Ortamda Genel Kurul (EGKS) Yönetmeliği (2022)",
    metaDescription:
      "2022 EGKS Yönetmeliğiyle kooperatif ortaklarının genel kurula elektronik ortamda nasıl katılabileceğini ve toplantının hangi şartlarda elektronik yapılacağını öğrenin.",
    intro:
      "14 Ocak 2022 tarihli Resmî Gazete'de yayımlanan Elektronik Ortamda Genel Kurul (EGKS) Yönetmeliği; ortakların genel kurula fiziksel katılımın yanında elektronik ortamda da katılabilmesine imkân tanır. Bu düzenleme, ortakların karar süreçlerine erişimini kolaylaştırır.",
    sections: [
      {
        heading: "Elektronik katılımın dayanağı",
        body: [
          "Ortaklar, 1163 sayılı Kooperatifler Kanunu'nun 45'inci maddesinin yedinci fıkrası (45/7) uyarınca genel kurul toplantılarına elektronik ortamda da katılabilir. Böylece toplantıya fiziken katılamayan ortaklar da görüş bildirme ve oy kullanma hakkını elektronik ortamda kullanabilir.",
        ],
      },
      {
        heading: "Toplantı hangi şartlarda elektronik yapılır?",
        body: [
          "Genel kurul, yönetim kurulu kararıyla elektronik ortamda yapılabilir. Ayrıca genel kurul tarihinden 20 gün önce, 4'ten az olmamak üzere ortakların en az onda birinin (1/10) yazılı talebiyle toplantının elektronik ortamda yapılması sağlanır.",
          "Bu mekanizma, azınlıkta kalan ortakların dahi elektronik katılım imkânını talep edebilmesini kurumsal olarak mümkün kılar.",
        ],
      },
      {
        heading: "Sistemin kurulması ve hizmet alımı",
        body: [
          "Kooperatif, elektronik genel kurul sistemini kendisi kurabilir veya bu amaçla oluşturulmuş sistemlerden hizmet satın alabilir. Tercih edilen yöntem, güvenli kimlik doğrulama ve oy güvenliğini sağlamalıdır.",
        ],
      },
      {
        heading: "Mia Park Ocean açısından anlamı",
        body: [
          "Çok ortaklı bir projede elektronik katılım, farklı şehirlerde bulunan ortakların dahi genel kurul kararlarına erişimini kolaylaştırabilir. S.S. Yahya Kaptan Birlik Yapı Kooperatifi için elektronik katılım imkânı, ortakların söz ve oy hakkını güçlendiren bir şeffaflık aracı olarak değerlendirilir.",
        ],
      },
      {
        heading: "Resmî kaynak ve bilgilendirme",
        body: [
          "Yönetmeliğin tam metni 14 Ocak 2022 tarihli Resmî Gazete'de yayımlanmıştır: https://www.resmigazete.gov.tr/eskiler/2022/01/20220114-4.htm",
          "Bu içerik genel bilgilendirme amaçlıdır; güncel mevzuat ve kooperatif anasözleşmesi esastır.",
        ],
      },
    ],
    checklist: [
      "Elektronik katılım imkânını genel kurul çağrısında ortaklara duyurun.",
      "Yönetim kurulu kararı veya 1/10 talebi sürecini yazılı olarak izleyin.",
      "Kimlik doğrulama ve oy güvenliği sağlayan bir EGKS çözümü seçin.",
      "Elektronik ve fiziki katılımın eşit haklar sağladığını gözetin.",
    ],
    mpoNote: true,
  },
  {
    slug: "kooperatif-dis-denetim-yonetmeligi",
    category: "guven",
    tier: "article",
    title: "Kooperatiflerde Dış Denetim Yönetmeliği (2022)",
    metaDescription:
      "2022'de yürürlüğe giren dış denetim yönetmeliğine göre hangi kooperatiflerin dış denetime tabi olduğunu, denetimi kimlerin yapabileceğini ve raporlama sürelerini öğrenin.",
    intro:
      "1 Şubat 2022 tarihli Resmî Gazete'de yayımlanan Kooperatif ve Üst Kuruluşlarının Denetimine Dair Yönetmelik; belirli ölçekteki kooperatiflerin bağımsız dış denetime tabi tutulmasını düzenler. Dış denetim, ortakların mali güvenliğini güçlendiren önemli bir kurumsal denetim katmanıdır.",
    sections: [
      {
        heading: "Dış denetimin konusu",
        body: [
          "Dış denetimde; finansal tabloların 1163, 6102 ve 213 sayılı Kanunlar ile ilgili mevzuata uygun hazırlanıp hazırlanmadığı, gelir ve gider belgelerinin uygunluğu ile hesapların defter, kayıt ve belgelerle uyumu incelenir.",
          "Böylece denetim, yalnızca rakamsal doğruluğu değil; kayıt düzeninin ve belge dayanağının mevzuata uygunluğunu da kapsar.",
        ],
      },
      {
        heading: "Hangi kooperatifler dış denetime tabidir?",
        body: [
          "Tarım satış, tarım kredi, esnaf ve sanatkârlar kredi ve kefalet ile pancar ekicileri kooperatifleri herhangi bir kriter aranmaksızın dış denetime tabidir.",
          "Bunun yanında; yapı ruhsatı alınmış ve ortak sayısı 100'den fazla olan yapı, turizm geliştirme ve gayrimenkul işletme kooperatifleri; ardı ardına iki yıl 30 milyon TL satış hasılatını geçen kooperatifler ile 2.000'den fazla ortağı bulunan kooperatifler de dış denetim kapsamındadır.",
        ],
      },
      {
        heading: "Mia Park Ocean açısından anlamı",
        body: [
          "S.S. Yahya Kaptan Birlik Yapı Kooperatifi bir yapı kooperatifidir. Yönetmelik, yapı ruhsatı alınmış ve ortak sayısı 100'den fazla olan yapı kooperatiflerini dış denetim kapsamına aldığından, bu eşik çok ortaklı yapı projeleri için doğrudan önem taşır.",
          "Dış denetim, ortakların yatırımının bağımsız gözle incelenmesini sağlayarak proje güven çerçevesini güçlendirir.",
        ],
      },
      {
        heading: "Denetimi kimler yapabilir?",
        body: [
          "Dış denetim; 3568 sayılı Kanuna tabi meslek mensupları, bağımsız denetçiler ve ilgili Bakanlıkça yetkilendirilen Merkez Birlikleri tarafından yapılabilir.",
          "Bağımsız denetçiler hariç olmak üzere dış denetçilere, Bakanlık veya görevlendirdiği kuruluşlarca 5 yıl geçerli olacak bir eğitim verilir.",
        ],
      },
      {
        heading: "Denetçinin seçimi ve görev süresi",
        body: [
          "Dış denetçi, kuruluşta anasözleşmeyle; sonraki dönemlerde ise genel kurul kararıyla seçilir. Bir denetçi en fazla 4 hesap dönemi için görev yapabilir.",
        ],
      },
      {
        heading: "Raporlama süresi",
        body: [
          "Dış denetim raporu, hesap dönemi sonundan itibaren en geç 3 ay içinde hazırlanarak yönetim kuruluna teslim edilir. Yönetim kurulu, raporu genel kuruldan en az 15 gün önce ortakların incelemesine hazır bulundurur ve KOOPBİS'e yükler.",
          "Bu süreç, ortakların denetim sonuçlarını genel kurulda bilinçli biçimde değerlendirmesine imkân tanır.",
        ],
      },
      {
        heading: "Resmî kaynak ve bilgilendirme",
        body: [
          "Yönetmeliğin tam metni 1 Şubat 2022 tarihli Resmî Gazete'de yayımlanmıştır: https://www.resmigazete.gov.tr/eskiler/2022/02/20220201-1.htm",
          "Bu içerik genel bilgilendirme amaçlıdır; güncel mevzuat ve kooperatif anasözleşmesi esastır.",
        ],
      },
    ],
    checklist: [
      "Projenin dış denetim eşiklerine girip girmediğini her yıl değerlendirin.",
      "Dış denetçiyi genel kurul kararıyla ve en fazla 4 hesap dönemi için seçin.",
      "Denetim raporunu hesap dönemi sonundan itibaren 3 ay içinde alın.",
      "Raporu genel kuruldan 15 gün önce ortaklara açın ve KOOPBİS'e yükleyin.",
    ],
    mpoNote: true,
  },
  {
    slug: "genel-kurul-bakanlik-temsilcisi-yonetmeligi",
    category: "guven",
    tier: "article",
    title: "Genel Kurul ve Bakanlık Temsilcisi Yönetmeliği (2022)",
    metaDescription:
      "2022 yönetmeliğiyle kooperatif genel kurul toplantılarının usul ve esasları ile toplantıda bulunan Bakanlık temsilcisinin (komiser) görev ve niteliklerini öğrenin.",
    intro:
      "14 Ocak 2022 tarihli Resmî Gazete'de yayımlanan yönetmelik; kooperatif ve üst kuruluşlarının genel kurul toplantılarının usul ve esasları ile bu toplantılarda bulundurulacak Bakanlık temsilcisinin nitelik ve görevlerini düzenler. Bakanlık temsilcisinin gözetimi, genel kurulun kanuna ve anasözleşmeye uygunluğunu güçlendiren bir kamu denetimi unsurudur.",
    sections: [
      {
        heading: "Yönetmeliğin kapsamı",
        body: [
          "Yönetmelik, kooperatiflerin ve üst kuruluşların genel kurul toplantılarının nasıl yapılacağını düzenler; toplantı çağrısı, gündem, katılım, oylama ve tutanak gibi usul kurallarının çerçevesini çizer.",
          "Aynı zamanda bu toplantılarda görevlendirilen Bakanlık temsilcisinin nitelikleri ile görev ve yetkilerini belirler.",
        ],
      },
      {
        heading: "Bakanlık temsilcisinin (komiser) rolü",
        body: [
          "Genel kurul toplantıları, Bakanlıkça görevlendirilen bir temsilci (komiser) gözetiminde yapılır. Temsilci, toplantının kanuna, anasözleşmeye ve gündeme uygun yürütülüp yürütülmediğini gözlemler.",
          "Bu kamu gözetimi, kararların usulüne uygun alınması ve ortakların haklarının korunması bakımından ek bir güvence sağlar.",
        ],
      },
      {
        heading: "Mia Park Ocean açısından anlamı",
        body: [
          "S.S. Yahya Kaptan Birlik Yapı Kooperatifi'nin genel kurulları da bu usul kuralları ve Bakanlık temsilcisi gözetimi çerçevesinde yapılır. Böylece Mia Park Ocean ortakları, kararların şeffaf ve denetlenebilir bir zeminde alındığını bilerek karar süreçlerine katılır.",
        ],
      },
      {
        heading: "Resmî kaynak ve bilgilendirme",
        body: [
          "Yönetmeliğin tam metni 14 Ocak 2022 tarihli Resmî Gazete'de yayımlanmıştır: https://www.resmigazete.gov.tr/eskiler/2022/01/20220114-2.htm",
          "Bu içerik genel bilgilendirme amaçlıdır; güncel mevzuat ve kooperatif anasözleşmesi esastır.",
        ],
      },
    ],
    checklist: [
      "Genel kurul çağrısı, gündem ve belgeleri mevzuattaki usule göre hazırlayın.",
      "Bakanlık temsilcisi görevlendirme talebini zamanında yapın.",
      "Toplantı tutanağı ve hazirun listesini eksiksiz kayda alın.",
      "Alınan kararları ortaklara açık ve anlaşılır biçimde duyurun.",
    ],
    mpoNote: true,
  },
];
