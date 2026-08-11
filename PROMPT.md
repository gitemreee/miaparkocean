# MİA PARK OCEAN — Web Sitesi Üretim Görevi (miaparkocean.com)

## 1. Görev Özeti

İzmit MİA Bölgesi'nde inşa edilen 660 daireli **MİA PARK OCEAN** projesi için, `C:\Users\emrey\Desktop\MIA - WEB` dizininde sıfırdan, üretime hazır, Türkçe bir tanıtım + güven inşası web sitesi geliştir.

Bu sıradan bir "müteahhit landing page"i DEĞİL. Projeyi **S.S. Yahya Kaptan Birlik Yapı Kooperatifi** yapıyor ve hedef kitlenin kooperatif modeline karşı ciddi tedirginlikleri var ("param güvende mi?", "tapu alabilecek miyim?", "kooperatifler batar"). Sitenin iki eşit önemli görevi var:

1. **Satış:** Projeyi lüks ama ulaşılabilir bir yaşam olarak sunmak ("Lüks Artık Ulaşılabilir").
2. **Güven:** Kooperatif modelinin devlet denetimindeki, yasayla korunan, şeffaf bir yapı olduğunu kanıtlarla anlatıp tedirginliği ikna edici şekilde dağıtmak.

Her tasarım ve içerik kararında bu iki hedefi birlikte gözet.

## 1.1 Referans Site (Kalite Çıtası)

Müşterinin beğendiği örnek: **https://www.ozakgyo.com/tr/proje/buyukyali** (Özak GYO — Büyükyalı). Site bu seviyede ve bu yapıda olacak. Büyükyalı'dan alınacak yapısal dersler:

- **Hero:** Full-bleed görsel/slider; her slayt tek şiirsel taglineli ("İstanbul'un Zamansız Deniz Semti" gibi). MİA PARK OCEAN karşılığı: "İzmit'in Yeni Yaşam Merkezi", "Lüks Artık Ulaşılabilir." gibi kısa, iddialı satırlar.
- **Tanıtım Filmi** bölümü (bizde şimdilik video yoksa görsel slideshow + `[İSTEĞE BAĞLI: tanıtım filmi gelince eklenecek]` placeholder).
- **Proje Lokasyon + Satış Ofisi** bloğu: adres, telefon, **Google Haritalar ve Yandex Haritalar** butonları.
- **Galeri:** Lightbox'lı, kategorili (Dış Mekân / İç Mekân / Sosyal Alanlar) görsel galerisi.
- **Kurumsal ortak tanıtımı:** Büyükyalı'da Özak/Yenigün/Ziylan ayrı ayrı tanıtılıyor; bizde aynı kalıpla **S.S. Yahya Kaptan Birlik Yapı Kooperatifi** (yapımcı) ve **Ocean Gayrimenkul** (tek yetkili satıcı) tanıtılacak.
- **Daire Planları:** Sekmeli/kartlı tip gezgini (onlarda 2+1/3+1/4+1; bizde 1+0 / 1+1 / 2+1 Bahçe Dubleks).
- **SSS:** Uzun, SEO hedefli, gerçek soru cümleleriyle yazılmış akordeon ("Büyükyalı satılık daire seçenekleri neler?" kalıbı → "MİA Park Ocean'da hangi daire tipleri var?").
- Genel his: kurumsal, sakin, geniş boşluklu, tipografi ağırlıklı prestij sitesi. Birebir kopyalama; yapıyı al, görsel dili bizim "Gilded Horizon" sistemimizle kur.

Görevi çalıştırırken bu URL'yi tarayıcıyla/WebFetch ile bizzat incele; bölüm ritmini ve ton kalitesini gör.

## 2. Kaynak Dosyalar

Tüm marka varlıkları şurada: `C:\Users\emrey\Desktop\MIA PARK OCEAN\`

| Dosya / Klasör | İçerik |
|---|---|
| `design-philosophy.md` | "Gilded Horizon" tasarım felsefesi — TAM METNİ OKU ve tasarımın anayasası olarak uygula |
| `MIA PARK OCEAN renk paleti (pano).png` | Resmi renk paleti (aşağıda hex kodları verildi) |
| `broşür-türkçe-png\` (8 JPEG) | Türkçe broşürün sayfa sayfa görselleri — içerik ve görsel kaynak |
| `hype\oceanlogo.jpeg` | Ocean Gayrimenkul logosu (beyaz zemin, mavi logo) |
| `hype\MIA PARK OCEAN post 1 (lansman).png`, `post 2 (odeme).png` | Sosyal medya lansman görselleri |
| `WhatsApp Image 2026-07-*.jpeg` (kök klasörde ~50 adet) | Proje render'ları — site görselleri için ana havuz; hepsine bak, en iyilerini seç |
| `MİA PARK OCEAN NEW BROSHURE.pdf`, `mia park ocean 8 sayfa broşür.pdf` | Basılı broşürler (gerekirse referans) |

Görselleri projeye kopyalarken **ASCII dosya adlarıyla yeniden adlandır** (ör. `hero-sunset.webp`, `courtyard-night.webp`) ve web için optimize et (WebP, hero ≤ 350 KB, galeri ≤ 200 KB, `srcset` ile responsive).

## 3. Proje Künyesi (Broşürden Doğrulanmış Bilgiler)

- **Proje adı:** MİA PARK OCEAN
- **Konum:** İzmit MİA Bölgesi, Kocaeli
- **Yapı:** 4 blok, zemin + 7 kat (toplam 8 kat)
- **Toplam daire:** 660 *(kapak sayfasında tipler 500+134+16=650 toplanıyor; başlıkta 660 kullan, kesin dağılımı `[DOĞRULANACAK]` işaretle)*
- **Daire tipleri:**
  - **1+0** — 500 adet, brüt 28,00 m² — açık plan, geniş balkon, modern mutfak, gizli/akıllı depolama, yatırım için ideal
  - **1+1** — 134 adet, brüt 50,00 m² — geniş yaşam alanı, büyük balkon, modern mutfak, akıllı depolama
  - **2+1 Bahçe Dubleks** — 16 adet, brüt 100,00 m² — özel kullanım bahçesi, yüksek tavanlı loft yaşam, geniş sürme camlar, iç-dış mekân bütünlüğü, ahşap pergola, zeminden bahçeye direkt erişim, aile yaşamına uygun
- **Ödeme kampanyası:** Avantajlı peşinat, **vade farksız 60 ay**
- **Sosyal donatılar:** Merkezi avlu, dekoratif süs havuzları, geniş peyzaj alanları, yürüyüş ve dinlenme yolları, loft bahçeler, özel LED gece aydınlatması, kapalı otopark, 7/24 güvenlik, spor ve sosyal yaşam alanları
- **Lokasyon avantajları (broşür haritasından):** Şehir merkezi 5 dk · Şehir Hastanesi 5 dk · Kocaeli Üniversitesi 10 dk · TEM Otoyolu 5 dk · D100 Karayolu 1 dk · 41 Burada AVM 3 dk · Symbol AVM 7 dk
- **Sloganlar (broşürden, aynen kullanılabilir):** "Lüks Artık Ulaşılabilir." · "Hayalinizdeki yaşam, şimdi çok daha yakın." · "Hayatın yeni merkezine hoş geldiniz." · "Yaşamınızın yeni merkezi"
- **Yapımcı:** S.S. Yahya Kaptan Birlik Yapı Kooperatifi (YKB)
- **Tek yetkili satıcı:** Ocean Gayrimenkul
- **İletişim:** 0540 028 00 41 · 0541 128 40 41 · info@oceangayrimenkul.com · www.oceangayrimenkul.com
- **Adres:** Ömerağa Mah. Abdurrahman Yüksel Cad. Bana Bak Ap. No:15/4 İzmit / Kocaeli
- **Sosyal medya:** Instagram, Facebook, YouTube, LinkedIn → `/oceangayrimenkul`
- **Alan adı:** miaparkocean.com

## 4. Marka ve Tasarım Sistemi

`design-philosophy.md` dosyasındaki **"Gilded Horizon" (Yaldızlı Ufuk)** felsefesini birebir uygula. Özet ilkeler:

- Lüks bağırılmaz, fısıldanır. Bilgi paragrafla değil; boşluk, ışık ve oranla iletilir.
- Yatay "ufuk çizgisi" disiplini: ince altın hatlar, kusursuz hizalanmış yatay bantlar, dalga yayları.
- Full-bleed fotoğraflar daima altın bir çizgiyle veya derin boşlukla "sahnelenir".
- Tipografi: ince, geometrik, harf arası açılmış BÜYÜK HARFLİ başlıklar; kısa ve ikincil gövde metni. (Öneri: başlıklar için Cormorant Garamond / Marcellus, gövde için Jost / Manrope — Google Fonts, `next/font` ile self-host.)
- Hiyerarşi puntoyla değil ışıkla kurulur: altın parlayan tek kelime, paragraftan yüksek sesle konuşur.
- İkonlar tek kalınlıkta, klinik incelikte çizgiler (lucide-react uygun).

**Resmi renk paleti (başka renk üretme):**

| Renk | Hex | Kullanım |
|---|---|---|
| Derin Okyanus (Deep Ocean) | `#001F3F` | Ana zemin, koyu bölümler, footer |
| İnci Beyazı (Pearl White) | `#F5F5F5` | Açık zeminler, kart yüzeyleri |
| Kum Beji (Sand Beige) | `#D2B48C` | Nötr yüzeyler, ikincil vurgu |
| Ahşap (Driftwood) | `#A0522D` | Sıcak detay vurguları (az kullan) |
| Canlı Akuamarin (Vibrant Aquamarine) | `#00E5FF` | Su öğeleri, tekil vurgu (çok az, tek nokta) |
| Fırçalanmış Bronz (Brushed Bronze) | `#B8860B` | Altın hatlar, başlık vurguları, CTA, lüks metinler |

Koyu lacivert zemin + altın hat + krem boşluk = ana kompozisyon. Akuamarin her ekranda en fazla bir kez konuşur.

## 5. Site Mimarisi

**Yığın:** Next.js 15 (App Router, `output: 'export'` ile statik) + Tailwind CSS v4 + TypeScript. Framer Motion ile ölçülü, zarif animasyonlar (scroll-reveal, ince parallax; asla oyuncaklaştırma). Statik export Netlify/Vercel/klasik hosting hepsinde çalışır.

**Sayfalar:**

1. `/` — Ana Sayfa (aşağıdaki tüm bölümler)
2. `/kooperatif` — "Neden Kooperatif? Güvence ve Denetim" (ana sayfadaki güven bölümünün derinleştirilmiş hali + S.S. YKB kurumsal tanıtımı)
3. `/daireler` — Daire tipleri detay (3 tip ayrı ayrı, plan görselleri, karşılaştırma tablosu, "Dairenizi Seçin" formu)
4. `/bolge` — "İzmit MİA Bölgesi" (bölgenin yatırım değeri + "Basında MİA" haber kartları)
5. `/galeri` — Kategorili görsel galerisi (lightbox)
6. `/iletisim` — İletişim + form + harita + adres + Google/Yandex Haritalar butonları
7. `/kvkk` — KVKK Aydınlatma Metni (form için zorunlu)

**Genişleyebilirlik (önemli):** Müşteri siteye sürekli yeni içerik ekleyecek (yeni kampanyalar, şantiye/inşaat durumu güncellemeleri, basın haberleri, yeni sayfalar). Bu yüzden:

- Tüm metin ve listeler (daire tipleri, SSS, haberler, lokasyon mesafeleri) `src/data/*.ts` dosyalarında yaşasın; component'ler datayı map'lesin. Yeni haber/soru eklemek = tek satır data eklemek olsun.
- Bölüm component'leri bağımsız ve yeniden kullanılabilir olsun; ana sayfaya yeni bölüm eklemek mevcutları bozmasın.
- README'ye "yeni haber nasıl eklenir, yeni bölüm nasıl eklenir" kısa rehberi yaz.

**Ana sayfa bölüm sırası (kullanıcının açık talebi — hepsi ana sayfada olacak):**

1. **Hero** — Büyükyalı tarzı full-bleed slider (2-3 slayt, her biri tek taglineli), logo/proje adı, "Lüks Artık Ulaşılabilir." + "Avantajlı peşinat, vade farksız 60 ay" rozeti, 2 CTA: "Dairenizi Seçin" ve "Neden Kooperatif?"
2. **Rakamlarla proje** — 4 blok · 660 daire · zemin+7 kat · 3 daire tipi (sayaç animasyonlu ince bant)
3. **Proje tanıtımı** — "Yaşamınızın yeni merkezi" metni + öne çıkan görseller; tanıtım filmi alanı için placeholder bırak (`[İSTEĞE BAĞLI: video]`)
4. **Daire tipleri** — 3 kart (1+0 / 1+1 / 2+1 Bahçe Dubleks), m², adet, öne çıkan özellikler → `/daireler`e link, "Dairenizi Seçin" CTA
5. **Sosyal yaşam** — merkezi avlu, süs havuzları, yürüyüş yolları, gece aydınlatması, güvenlik, otopark (ikon grid)
6. **Galeri** — 6-8 seçilmiş kare, lightbox → `/galeri`ye link
7. **Lokasyon** — dakika mesafeleri şeridi + harita görseli/embed + satış ofisi bloğu (adres, telefonlar, Google Haritalar / Yandex Haritalar butonları — Büyükyalı kalıbı)
8. **Değerlenen Bölge: İzmit MİA + Basında MİA** — bölgenin yatırım hikâyesi (aşağıda 6.5)
9. **NEDEN KOOPERATİF?** — güven bölümü (aşağıda ayrıntılı içerik direktifi var)
10. **Yasal Güvence ve Denetim** — kooperatifin yasa ve sorumlulukları (aşağıda)
11. **S.S. Yahya Kaptan Birlik Yapı Kooperatifi** — kısa kurumsal tanıtım → `/kooperatif`e link
12. **Aklınızdaki Sorular (SSS)** — akordeon
13. **İletişim / Dairenizi Seçin formu** — form + telefonlar + WhatsApp linki (`https://wa.me/905400280041`)
14. **Footer** — Deep Ocean zemin; Ocean Gayrimenkul "Tek Yetkili Satıcı" + S.S. YKB logoları/adları, adres, sosyal medya, KVKK linki

## 6. Kooperatif Güven İçeriği (SİTENİN KALBİ — özenle yaz)

Ton: Savunmacı değil, özgüvenli ve şeffaf. "Korkmayın" deme; mekanizmayı göster, okuyucu kendisi rahatlasın. Kısa cümleler, somut kurum ve kanun adları, ikonlu kartlar.

### 6.1 "Neden Kooperatif?" bölümü

Şu mesajları işle:

- **Maliyetine ev:** Kooperatif kâr amacı gütmez; ortaklar müteahhit kârı ödemeden, maliyet esasıyla konut sahibi olur. Aradaki fark cebinizde kalır.
- **Söz hakkı:** Her ortağın genel kurulda **bir oyu** vardır. Yönetimi ortaklar seçer, kararlar şeffaf alınır.
- **Devlet gözetimi:** Kooperatif "kayıt dışı bir oluşum" değil; kuruluşundan tasfiyesine kadar devletin kayıt ve denetim sistemine tabidir.
- **Tarihi meşruiyet:** Kooperatifçilik Türkiye'de Anayasa ile desteklenen bir modeldir (Anayasa m.171: "Devlet, kooperatifçiliğin gelişmesini sağlayacak tedbirleri alır").

### 6.2 "Yasal Güvence ve Denetim" bölümü (ana sayfada)

Aşağıdaki olguları ikonlu güven kartları halinde sun (her kart: başlık + 1-2 cümle):

- **1163 sayılı Kooperatifler Kanunu:** Kooperatifin kuruluşu, yönetimi, ortak hakları ve tasfiyesi 1969'dan beri yürürlükte olan bu kanunla güvence altındadır.
- **e-Devlet / KOOPBİS şeffaflığı:** 7339 sayılı Kanun'la (2021) kurulan **Kooperatif Bilgi Sistemi (KOOPBİS)** sayesinde ortaklar; kooperatifin ana sözleşmesine, organlarına, genel kurul kararlarına ve kendi ortaklık kayıtlarına **e-Devlet üzerinden** erişebilir. Her şey kayıt altında, her şey görünür.
- **Genel kurulda Bakanlık temsilcisi (komiser):** Kooperatif genel kurul toplantıları, Bakanlık tarafından görevlendirilen bir **temsilci (komiser) gözetiminde** yapılır. Toplantının kanuna ve ana sözleşmeye uygunluğu devlet gözetimindedir.
- **Çok katmanlı denetim:** İçeride ortakların seçtiği denetim organı; dışarıda 7339 sayılı Kanun'la getirilen **dış denetim** ve ilgili Bakanlığın (yapı kooperatiflerinde Çevre, Şehircilik ve İklim Değişikliği Bakanlığı) denetim yetkisi.
- **Ortağın bilgi alma hakkı:** Her ortak, kanundan doğan bilgi edinme ve belge inceleme hakkına sahiptir; yönetim hesap vermekle yükümlüdür.
- **Ferdileşme = Tapu:** İnşaat tamamlandığında daireler kura/tahsis sonucu ortaklar adına **tapuya bağlanır**. Hedef, her ortağın kendi bağımsız tapusuna kavuşmasıdır.

Bölümün altına küçük puntoyla: *"Bu bölüm genel bilgilendirme amaçlıdır; güncel mevzuat ve kooperatif ana sözleşmesi esastır."*

### 6.3 "Aklınızdaki Sorular" (SSS — akordeon, en az 8 soru)

Şu soruları samimi, net, 2-4 cümlelik cevaplarla yaz:

1. Kooperatif ile müteahhitten ev almak arasındaki fark nedir?
2. Param güvende mi? Ödemelerim nereye gidiyor, nasıl takip edilir?
3. Kooperatifi kim denetliyor? (KOOPBİS, Bakanlık temsilcisi, dış denetim — yukarıdaki kartlara bağla)
4. Kooperatif bilgilerimi e-Devlet'ten görebilir miyim? (Evet — KOOPBİS)
5. Tapumu ne zaman alırım? (ferdileşme süreci)
6. Ortaklıktan çıkmak istersem ne olur? (1163 SK'daki çıkma hakkı; ayrıntı için ana sözleşmeye yönlendir)
7. Aidat/ödeme planı nasıl işliyor? (avantajlı peşinat + vade farksız 60 ay; kesin rakamlar için iletişime yönlendir)
8. Genel kurulda oy hakkım var mı? (her ortak 1 oy)
9. İnşaat hangi aşamada, teslim ne zaman? → `[DOĞRULANACAK]`, iletişime yönlendir
10. Yabancıya/ikinci el ortaklık devri mümkün mü? → kısa cevap + ana sözleşmeye yönlendir

### 6.4 S.S. Yahya Kaptan Birlik Yapı Kooperatifi tanıtımı

Bilinenler: **2021 yılında kuruldu**, İzmit/Kocaeli merkezli, MİA PARK OCEAN projesinin yapımcısı. Şu iskeletle yaz, bilinmeyen her yeri `[DOĞRULANACAK: ...]` ile işaretle:

- Kuruluş yılı ve amacı (ortaklarını modern, nitelikli konuta maliyet esasıyla kavuşturmak)
- Yönetim anlayışı: şeffaflık, düzenli genel kurul, KOOPBİS kaydı
- `[DOĞRULANACAK: ortak sayısı, tamamlanan önceki etaplar/projeler, yönetim kurulu adları, kuruluş sicil no]`
- Ocean Gayrimenkul'ün "tek yetkili satıcı" rolünün açıklaması

### 6.5 "Değerlenen Bölge: İzmit MİA" + "Basında MİA"

MİA Bölgesi, İzmit'in yeni gelişim aksı ve değer kazanan yatırım bölgesi. Bu bölüm alıcıya "doğru yerden, doğru zamanda alıyorsun" hissini vermeli:

- **Bölge hikâyesi:** İzmit MİA Bölgesi'nin konumu (D100'e 1 dk, TEM'e 5 dk, şehir merkezine 5 dk, üniversite ve şehir hastanesine yakınlık), yeni gelişen modern konut aksı olması, altyapı ve ulaşım yatırımları. Kocaeli'nin sanayi ve istihdam gücünün konut talebini beslemesi. Abartılı getiri vaadi YOK ("×2 olacak" gibi ifadeler yasak); "değer kazanan bölge", "yatırım potansiyeli" gibi ölçülü dil kullan.
- **"Basında MİA" haber kartları:** `src/data/press.ts` içinde başlık + kaynak + tarih + link + görsel alanlı haber kartı yapısı kur. Gerçek haber linkleri henüz elimizde yok: WebSearch ile "İzmit MİA bölgesi", "Kocaeli MİA konut" haberlerini ara; bulursan gerçek başlık/kaynak/linkle ekle, bulamazsan 3-4 kartı `[DOĞRULANACAK: haber linki]` placeholder'ıyla kur ve README'de belirt. Uydurma haber başlığı YAZMA.
- Bu bölümün genişleyeceğini varsay: müşteri sürekli yeni haber ekleyecek → kart eklemek tek data satırı olmalı.

## 7. Teknik Gereksinimler

- **Responsive:** 360px'den 1920px'e kusursuz. Mobil öncelikli; hero mobilde de etkileyici.
- **Performans:** Lighthouse ≥ 90 (Performance/SEO/Best Practices/A11y). Görseller WebP + lazy load (`next/image` yerine statik exportta `<img srcset>` veya `next/image` unoptimized + önceden boyutlandırılmış varyantlar). CLS yok.
- **SEO:** Türkçe metadata; her sayfada benzersiz title/description; Open Graph + Twitter kartları (hero görseliyle); `sitemap.xml` + `robots.txt`; JSON-LD: `Organization`, `ApartmentComplex`/`Residence`, `FAQPage`. Hedef sorgular: "izmit mia bölgesi konut", "kocaeli kooperatif daire", "mia park ocean", "izmit 1+1 satılık daire projesi", "yahya kaptan birlik yapı kooperatifi".
- **Form:** Ad, telefon, e-posta, ilgilenilen daire tipi (1+0/1+1/2+1), mesaj + KVKK onay checkbox'ı (zorunlu, `/kvkk` sayfasına link). Statik sitede backend yok: Netlify Forms attribute'ları (`data-netlify="true"`) ekle VE `mailto:`/WhatsApp fallback butonları koy. Zod ile client-side doğrulama, Türkçe hata mesajları.
- **Erişilebilirlik:** Semantik HTML, alt metinleri Türkçe, kontrast oranları (altın-üstü-lacivert kontrolü!), klavye navigasyonu, akordeon için ARIA.
- **Kod düzeni:** Bölüm başına ayrı component (`components/sections/`), 200-400 satır dosya hedefi, mutation yok, console.log yok, hardcoded secret yok.
- **Analytics:** Şimdilik ekleme; `[İSTEĞE BAĞLI: GA4/Meta Pixel id gelince eklenecek]` yorumu bırak.

## 8. Çalışma Sırası

1. Kaynak klasörünü tara, `design-philosophy.md`'yi ve broşür görsellerini incele.
2. Görselleri seç, optimize et, `public/images/` altına ASCII adlarla kopyala.
3. Projeyi iskeletle (Next.js + Tailwind + font kurulumu + renk token'ları).
4. Bölümleri yukarıdaki sırayla üret; her bölümden sonra diske yaz (bellekte biriktirme).
5. İçerikleri yaz (kooperatif bölümüne en fazla zamanı ayır).
6. SEO + form + KVKK sayfası.
7. Build al (`next build`), hataları çöz, responsive kontrolü yap (360/768/1440).
8. Kısa bir `README.md`: nasıl çalıştırılır, nasıl deploy edilir, `[DOĞRULANACAK]` listesinin özeti.

## 9. Yapma / Kaçın

- Paletteki 6 renk dışında renk üretme; degrade çorbası yapma.
- Stok fotoğraf, sahte insan görseli, sahte referans/testimonial **ekleme**.
- Kesin fiyat, kesin teslim tarihi, "devlet garantisi" gibi **verilmemiş taahhütler yazma**. Devlet *denetler*, ödemeyi *garanti etmez* — bu ayrımı asla bulanıklaştırma; güven bölümü doğru bilgiyle ikna eder, abartıyla değil.
- Broşürdeki yazım hatalarını (ör. "Esterik", "hızırlu", "Dubeks") siteye taşıma; hepsini düzgün Türkçeyle yeniden yaz.
- Lorem ipsum bırakma; her metin yayınlanabilir kalitede Türkçe olacak.
- `[DOĞRULANACAK]` işaretli hiçbir bilgiyi uydurma; işaretle ve README'de listele.

## 10. Kabul Kriterleri

- [ ] `npm run build` hatasız; statik export çalışıyor
- [ ] 7 sayfa tam içerikle hazır; ana sayfada 14 bölümün tamamı var
- [ ] Büyükyalı referansındaki kalıplar mevcut: hero slider, satış ofisi bloğu (Google/Yandex Haritalar), galeri, kurumsal tanıtım, sekmeli daire planları, uzun SSS
- [ ] "Değerlenen Bölge: İzmit MİA" + "Basında MİA" bölümü kuruldu; haber kartları data dosyasından besleniyor
- [ ] "Neden Kooperatif", "Yasal Güvence", SSS ve YKB bölümleri ana sayfada ve dolu
- [ ] KOOPBİS/e-Devlet, Bakanlık temsilcisi (komiser), 1163 ve 7339 sayılı kanun atıfları doğru şekilde yer alıyor
- [ ] Gilded Horizon estetiği: lacivert-altın-krem dengesi, ince hatlar, geniş boşluklar ekranda hissediliyor
- [ ] Mobilde hero, daire kartları ve SSS kusursuz
- [ ] Form KVKK onayıyla çalışıyor (Netlify Forms + WhatsApp fallback)
- [ ] README'de `[DOĞRULANACAK]` listesi eksiksiz
