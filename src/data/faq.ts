// Sıkça Sorulan Sorular — proje + kooperatif içerik dosyasından.
// Yeni soru eklemek için diziye ekleyin. Yasak ifade kullanılmaz.

export type FaqItem = {
  category: "kooperatif" | "proje";
  question: string;
  answer: string;
};

export const faq: FaqItem[] = [
  // ————— Proje —————
  {
    category: "proje",
    question: "MİA PARK OCEAN'da hangi daire tipleri var?",
    answer:
      "Projede üç yaşam tipi sunulur: 1+0 (brüt 28 m², 472 adet), 1+1 (brüt 50 m², 112 adet) ve 2+1 Bahçe Dubleks (brüt 100 m², 16 adet). Toplamda 600 daire yer alır.",
  },
  {
    category: "proje",
    question: "Ödeme planı nasıl işliyor?",
    answer:
      "Proje, tasarrufa dayalı faizsiz finansman yaklaşımıyla; avantajlı peşinat ve 60 aya varan sabit taksit imkânıyla sunulur. Size özel güncel plan için satış ekibimizle görüşebilirsiniz.",
  },
  {
    category: "proje",
    question: "Proje gecikirse ne olur?",
    answer:
      "Gecikme; yüklenici sözleşmesi, iş programı, mücbir sebep ve genel kurul kararları kapsamında değerlendirilir. Güncel teslim tahmini ve düzeltici plan üyelerle paylaşılır.",
  },
  {
    category: "proje",
    question: "Teslim tarihi garanti midir?",
    answer:
      "Teslim tarihi iş programına dayanır; ruhsat, finansman, tedarik ve mücbir sebep gibi riskler bulunabilir. Bu nedenle hukuki dayanağı olmadan “kesin garanti” ifadesi kullanılmaz; güncel tahmin ve ilerleme düzenli raporlanır.",
  },
  {
    category: "proje",
    question: "İnşaat ödemeleri nasıl yapılır?",
    answer: "İnşaat ödemeleri; sözleşme ve bağımsız teknik kontrolle doğrulanan hakedişlere dayanır.",
  },
  {
    category: "proje",
    question: "Malzeme değişebilir mi?",
    answer:
      "Gerekli hallerde eşdeğerlik analizi ve yetkili onayla malzeme değişikliği yapılabilir. Kalite ve maliyet etkisi kayıt altına alınır.",
  },
  {
    category: "proje",
    question: "Ruhsat olmadan üyelik alınabilir mi?",
    answer:
      "Kuruluş ve arsa geliştirme aşamasında üyelik mümkün olabilir; ancak ruhsat durumu açıkça belirtilir ve ruhsat varmış gibi bir pazarlama yapılmaz.",
  },
  {
    category: "proje",
    question: "Kısa dönem kiralama mümkün mü?",
    answer:
      "İmar, kullanım amacı, yönetim planı, yerel düzenlemeler ve turizm mevzuatı birlikte değerlendirilir. Bu konuda otomatik bir kira/Airbnb garantisi verilmez.",
  },
  {
    category: "proje",
    question: "Site işletmesi kim tarafından yürütülecek?",
    answer:
      "Teslim sonrası yönetim; kat mülkiyeti mevzuatı, yönetim planı ve varsa işletme kooperatifi modeline göre belirlenir.",
  },

  // ————— Kooperatif —————
  {
    category: "kooperatif",
    question: "Kooperatifin sahibi kimdir?",
    answer:
      "Kooperatif bağımsız tüzel kişiliğe sahiptir. Ortaklar üyelik haklarına sahiptir; yönetim kurulu kooperatifin sahibi değil, genel kurul tarafından seçilen yönetim organıdır.",
  },
  {
    category: "kooperatif",
    question: "Her üyenin oy hakkı eşit midir?",
    answer:
      "Kooperatifçilikte temel ilke demokratik kontroldür. Oy hakkı ve temsil şartları 1163 sayılı Kanun, anasözleşme ve güncel mevzuata göre uygulanır.",
  },
  {
    category: "kooperatif",
    question: "Yönetim kurulunu kim seçer?",
    answer:
      "Yönetim kurulu genel kurul tarafından seçilir. Görev süresi, adaylık şartları ve seçim usulü anasözleşmede düzenlenir.",
  },
  {
    category: "kooperatif",
    question: "Yönetim üyelerden istediği zaman para isteyebilir mi?",
    answer:
      "Konut yapı kooperatiflerinde ödeme ve taksitlerin genel kurul kararları çerçevesinde belirlenmesi esastır. Yönetimin tek taraflı ve dayanağı olmayan ek ödeme talebi hukuki risk doğurur.",
  },
  {
    category: "kooperatif",
    question: "Üyeler hesapları görebilir mi?",
    answer:
      "Üyeler kanun ve anasözleşme kapsamında temel mali tabloları ve raporları inceleyebilir. Mia Park Ocean ayrıca proje bazlı üye portalı üzerinden daha geniş şeffaflık sağlamayı hedefler.",
  },
  {
    category: "kooperatif",
    question: "Üyelik devredilebilir mi?",
    answer:
      "Anasözleşme şartlarını taşıyan kişiye, gerekli prosedür tamamlanarak üyelik devredilebilir. Borç ve tahsis durumu devirden önce yazılı olarak doğrulanmalıdır.",
  },
  {
    category: "kooperatif",
    question: "Üyelik tapu anlamına gelir mi?",
    answer:
      "Hayır. Üyelik kooperatif ortaklığıdır; bağımsız bölüm tapusu ise tescil işlemi tamamlandığında doğar.",
  },
  {
    category: "kooperatif",
    question: "Daireler nasıl tahsis edilir?",
    answer:
      "Tahsis yöntemi anasözleşme ve genel kurul kararlarıyla belirlenir. Kura veya kategori bazlı seçim uygulanacaksa kriterler önceden açıklanır.",
  },
  {
    category: "kooperatif",
    question: "Yönetim kendisine ayrıcalıklı daire seçebilir mi?",
    answer:
      "Yöneticiler de eşitlik ilkesine tabidir. Objektif ve genel kurula dayalı bir kural olmadan ayrıcalık sağlanması hukuki ve kurumsal risk oluşturur.",
  },
  {
    category: "kooperatif",
    question: "Ödemeyi kime yapmalıyım?",
    answer:
      "Yalnızca kooperatif adına açılmış ve resmen bildirilmiş banka hesabına ödeme yapılmalıdır. Kişisel hesaba veya elden ödeme yapılmamalıdır.",
  },
  {
    category: "kooperatif",
    question: "Arsa kooperatifin adına mı olmalı?",
    answer:
      "En güçlü model arsanın kooperatif mülkiyetinde olmasıdır. Farklı bir model varsa tapuya şerhli haklar ve sözleşmesel güvence hukuk müşavirince incelenmelidir.",
  },
  {
    category: "kooperatif",
    question: "Kooperatif devlet garantili midir?",
    answer:
      "Hayır. Kooperatifin mevzuata tabi ve kamu gözetiminde olması, yatırımın veya teslimin devlet garantisinde olduğu anlamına gelmez. Devlet denetler; ancak ödemeyi ya da teslimi garanti etmez.",
  },
  {
    category: "kooperatif",
    question: "KOOPBİS ne işe yarar?",
    answer:
      "Kooperatif verilerinin merkezi sistemde tutulmasına ve belirli süreçlerin elektronik yürütülmesine destek olur. Üyeler mevzuat kapsamındaki kayıtlara e-Devlet üzerinden erişebilir. Proje portalının yerine geçmez.",
  },
  {
    category: "kooperatif",
    question: "Bağımsız denetim zorunlu mu?",
    answer:
      "Zorunluluk kooperatifin türü ve güncel mevzuattaki kriterlere bağlıdır. Yasal zorunluluk olmasa dahi gönüllü bağımsız denetim uygulanabilir.",
  },
  {
    category: "kooperatif",
    question: "Müteahhit kim tarafından seçilir?",
    answer:
      "Yetki dağılımı anasözleşme ve genel kurul kararlarına göre belirlenir. Seçim; rekabetçi teklif ve teknik-mali yeterlilik değerlendirmesiyle yapılmalıdır.",
  },
  {
    category: "kooperatif",
    question: "Genel kurula katılmazsam ne olur?",
    answer:
      "Alınan kararlar şartları oluştuğunda tüm ortakları etkileyebilir. Bu nedenle çağrı, gündem ve vekâlet koşullarının takip edilmesi önemlidir.",
  },
  {
    category: "kooperatif",
    question: "Karara itiraz edebilir miyim?",
    answer:
      "Kanuna, anasözleşmeye veya dürüstlük kuralına aykırı kararlar için yasal itiraz ve dava yolları bulunabilir. Süreler açısından bir hukuk danışmanına başvurmanız önerilir.",
  },
  {
    category: "kooperatif",
    question: "Kooperatif tamamlanınca kapanır mı?",
    answer:
      "Amacın gerçekleşmesi sonrasında ferdi mülkiyet, tasfiye veya uygun modelde işletme yapısına geçiş seçenekleri proje özelinde kararlaştırılır.",
  },
  {
    category: "kooperatif",
    question: "Üyeliğimi teminat gösterebilir miyim?",
    answer:
      "Üyelik hakkının temlik veya rehni; anasözleşme, sözleşmeler ve finans kuruluşunun şartlarına göre değerlendirilir. Tapulu taşınmazla aynı güvence niteliğinde değildir.",
  },
  {
    category: "kooperatif",
    question: "Kooperatif iflas edebilir mi?",
    answer:
      "Kooperatif bir tüzel kişidir ve mali yükümlülüklerini yönetmek zorundadır. Finansman, tahsilat ve sözleşme riskleri iyi yönetilmezse mali sorunlar oluşabilir; bu nedenle şeffaf bütçe ve denetim kritik önemdedir.",
  },
  {
    category: "kooperatif",
    question: "Üyelerin kişisel verileri nasıl korunur?",
    answer:
      "Kimlik, iletişim, ödeme ve üyelik verileri KVKK ilkelerine göre; sınırlı erişim, güvenli sistem ve belirlenmiş saklama süreleriyle korunur.",
  },
];
