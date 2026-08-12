# MİA PARK OCEAN — SEO ve GEO Denetimi

**Tarih:** Ağustos 2026 · **Alan adı:** miaparkocean.com
**Kapsam:** Teknik SEO, yerel SEO (İzmit mahalleleri + Kocaeli ilçeleri + Sakarya/İstanbul), üretici motor optimizasyonu (GEO), dizine gönderim.

---

## 1. Yönetici Özeti

| Alan | Önce | Sonra |
|---|---|---|
| Dizinlenebilir sayfa | 7 statik + 12 makale | 11 statik + 20 bölge + 12 makale = **43** |
| Yerel hedefleme | Yalnızca "İzmit MİA Bölgesi" | 8 İzmit mahallesi, 10 Kocaeli ilçesi, 2 komşu il |
| Yapısal veri | Tek `Organization` | `RealEstateAgent`, `Organization`, `ApartmentComplex`, `Place`, `FAQPage`, `BreadcrumbList`, `ItemList`, `Event` |
| Sitemap | 7 URL + makaleler, öncelik yok | Tüm sayfalar, tip bazlı öncelik, sondaki eğik çizgi tutarlı |
| robots.txt | Tek kural | Yapay zekâ tarayıcılarına açık izin + gizli sayfa koruması |
| GEO | Yok | `llms.txt`, sayfa başına SSS bloğu, net soru-cevap yapısı |
| Dizine gönderim | Manuel | GSC/Bing/Yandex doğrulama alanları + IndexNow otomasyonu |

---

## 2. Teknik SEO

### 2.1 Yapılanlar

- **Canonical:** Her sayfa kendi mutlak adresini `alternates.canonical` ile bildiriyor. `trailingSlash: true` olduğu için sitemap URL'leri de sondaki eğik çizgiyle üretiliyor — çift içerik riski kapandı.
- **robots meta:** `googleBot` için `max-image-preview: large` ve `max-snippet: -1` verildi; görsel açısından zengin bir konut projesinde büyük görsel önizleme tıklama oranını yükseltir.
- **Sitemap:** `src/app/sitemap.ts` veri dosyalarından üretiliyor. Yeni bir mahalle/ilçe eklendiğinde sitemap otomatik büyür.
- **robots.txt:** Yapay zekâ tarayıcıları (GPTBot, PerplexityBot, ClaudeBot, Google-Extended, Applebot-Extended …) açıkça izinli. Gizli sayfalar (`/davetiye/`, `/basin-aciklamasi/`) hem `robots.txt` hem sayfa içi `noindex` ile korunuyor.
- **Görseller:** WebP + `srcset`, hero ≤ 350 KB, galeri ≤ 200 KB. `next.config.mjs` statik export olduğu için `images.unoptimized: true`; boyut optimizasyonu derleme öncesi `npm run images` ile yapılıyor.
- **Font:** `next/font/google` ile self-host — üçüncü taraf istek yok, CLS riski `display: swap` ile sınırlı.
- **Yapısal veri:** `src/lib/seo.ts` tek kaynak. `@graph` içinde birbirine `@id` ile bağlı düğümler yayınlanıyor (satıcı → proje → yer).

### 2.2 Yayına almadan önce yapılacaklar

1. `src/data/verification.ts` içine GSC / Bing / Yandex doğrulama kodlarını yapıştırın.
2. `src/data/region.ts` içindeki basın haberleri hâlâ örnek başlık. Gerçek haber linkleri eklenene kadar `verified: false`; **bu kartlar yayında gösterilmemeli veya gerçek linklerle değiştirilmeli.**
3. `src/data/site.ts` içindeki sosyal medya adresleri (`instagram.com/miaparkocean` vb.) doğrulanmalı — hesap yoksa `sameAs` yapısal verisi yanlış sinyal verir.
4. Satış ofisi harita pinini kesinleştirin (`src/data/site.ts` → `address.googleMaps`).

---

## 3. Yerel SEO — Sayfa Ağacı

Her sayfa `/bolgeler/[slug]/` altında; **şablon metin yoktur**, her lokasyon kendi karakteri, ulaşımı ve alıcı profiliyle yazılmıştır. Bu, Google'ın "doorway page" (kapı sayfası) tanımına girmemesi için kritiktir.

### 3.1 İzmit mahalleleri (8 sayfa)

| Sayfa | Ana hedef sorgu | İkincil | Mesafe |
|---|---|---|---|
| `izmit-yahya-kaptan` | Yahya Kaptan satılık daire | Yahya Kaptan kooperatif daire | 2-4 dk |
| `izmit-yenisehir` | Yenişehir İzmit satılık daire | İzmit Yenişehir konut projesi | 3-5 dk |
| `izmit-omeraga` | İzmit merkez konut projesi | Ömerağa satılık daire | 5-7 dk |
| `izmit-alikahya` | Alikahya satılık daire | Alikahya konut projesi | 8-12 dk |
| `izmit-karabas` | Karabaş satılık daire | İzmit sahil konut projesi | 5-8 dk |
| `izmit-cedit` | Cedit satılık daire | İzmit merkez yeni proje | 5-8 dk |
| `izmit-kozluk` | Kozluk satılık daire | İzmit Kozluk konut projesi | 5-8 dk |
| `izmit-bekirpasa` | Bekirpaşa satılık daire | İzmit Bekirpaşa konut projesi | 6-10 dk |

**Neden bu mahalleler:** Yahya Kaptan kooperatifin adını taşıdığı ve projeye en yakın mahalle; Ömerağa satış ofisinin bulunduğu yer; diğerleri İzmit'in en yüksek konut arama hacmine sahip yerleşimleri.

### 3.2 Kocaeli ilçeleri (10 sayfa)

Başiskele, Kartepe, Derince, Körfez, Gölcük, Gebze, Darıca, Çayırova, Karamürsel, Kandıra, Dilovası.

Her ilçe sayfasında farklı bir **satın alma gerekçesi** işleniyor:
- **Başiskele / Kartepe** → bahçeli yaşam beklentisi ↔ zemin kat dubleksler
- **Derince** → üniversite yakınlığı ↔ öğrenci kiralaması (1+0 / 1+1)
- **Gölcük** → deprem hassasiyeti ↔ fore kazık temel
- **Gebze / Darıca / Çayırova** → İstanbul fiyat baskısı ↔ aynı bütçeye daha geniş daire
- **Körfez / Dilovası** → sanayi istihdamı ↔ merkeze yakın yerleşim
- **Karamürsel / Kandıra** → sınırlı yerel arz ↔ kentsel donatı erişimi

### 3.3 Komşu iller (2 sayfa)

`sakarya` ve `istanbul`. **Bu sayfalarda "orada projemiz var" izlenimi verilmez** — her ikisinde de "Sakarya'da/İstanbul'da projemiz yok" cümlesi SSS içinde açıkça yer alır. Bu hem yanıltıcı reklam riskini hem de arama motoru güven kaybını önler.

### 3.4 İç bağlantı ağı

Her bölge sayfası 4 komşu bölgeye bağlanıyor, hepsi `/bolgeler` merkezine dönüyor, `/bolgeler` ana menüde. Bu, link otoritesinin derin sayfalara akmasını sağlar ve tarama derinliğini 2 tıka indirir.

---

## 4. GEO — Üretici Motor Optimizasyonu

Yapay zekâ arama motorları (Google AI Overviews, ChatGPT Search, Perplexity, Claude) klasik SEO'dan farklı sinyaller kullanır: **net cevap cümleleri, doğrulanabilir kimlik bilgisi ve yapılandırılmış veri.**

### Yapılanlar

1. **`/llms.txt`** — proje künyesi, daire tipleri, mesafeler, iletişim ve doğruluk notlarını tek dosyada, makine tarafından okunabilir biçimde sunar. "Doğruluk Notları" bölümü, modellerin en sık ürettiği yanlışı (başka illerde proje olduğu varsayımı) doğrudan engeller.
2. **Sayfa başına `FAQPage`** — her bölge sayfasında o bölgeye özel 3 soru-cevap. Cevaplar **tek başına alıntılanabilecek** şekilde yazıldı: özne, rakam ve koşul aynı cümlede.
3. **`@graph` yapısal verisi** — satıcı, yapımcı, proje ve yer düğümleri `@id` ile birbirine bağlı. Modeller "kim satıyor, kim yapıyor, nerede" sorusunu tek geçişte çözebiliyor.
4. **Rakamların metin içinde tekrarı** — 600 daire, 4 blok, 8 kat, %0 faiz, 60 ay vade, 2 yıl teslim; hem yapısal veride hem düz metinde geçiyor.
5. **`Event` yapısal verisi** — `/davetiye` sayfasında lansman etkinliği (tarih, yer, organizatör) işaretli.

### Ölçüm

GEO'nun tıklama raporu yoktur. Aylık kontrol için:
- ChatGPT / Perplexity'ye sorun: *"İzmit MİA Bölgesi'nde faizsiz konut projesi var mı?"*, *"Yahya Kaptan Birlik Yapı Kooperatifi güvenilir mi?"*
- Cevapta proje adı, doğru rakamlar ve miaparkocean.com kaynağı geçiyor mu?
- Yanlış bilgi varsa `llms.txt` içindeki "Doğruluk Notları" bölümünü genişletin.

---

## 5. Anahtar Kelime Haritası

| Niyet | Sorgu ailesi | Hedef sayfa |
|---|---|---|
| Marka | "mia park ocean", "mia park ocean izmit" | `/` |
| Ürün | "izmit 1+1 satılık daire", "izmit bahçe dubleks" | `/daireler/` |
| Güven | "kooperatif daire güvenli mi", "kooperatiften daire alınır mı" | `/kooperatif/`, `/bilgi-merkezi/` |
| Finansman | "faizsiz konut projesi kocaeli", "bankasız ev sahibi olma" | `/` + `/kooperatif/` |
| Yerel | "<mahalle/ilçe> satılık daire" | `/bolgeler/<slug>/` |
| Karşılaştırma | "istanbul yerine kocaeli yatırım" | `/bolgeler/istanbul/`, `/bolgeler/kocaeli-gebze/` |
| Bölge | "izmit mia bölgesi neresi", "izmit yeni konut projeleri" | `/bolge/` |

**Kaçınılan sorgular:** Fiyat içeren sorgular (m² fiyatı, daire fiyatı) bilinçli olarak hedeflenmedi. Fiyat yayınlamak hem güncelleme yükü hem de kooperatif mevzuatı açısından risk yaratır; fiyat bilgisi satış ofisine yönlendiriliyor.

---

## 6. Dizine Gönderim

Ayrıntılı adımlar: [`docs/GSC-BING-KURULUM.md`](./GSC-BING-KURULUM.md)

Özet:
1. `src/data/verification.ts` → kodları yapıştır → `npm run build` → yayına al → doğrula.
2. GSC'de `https://miaparkocean.com/sitemap.xml` gönder.
3. Bing Webmaster'a GSC'den içe aktar (en hızlı yol).
4. Her yayından sonra `npm run indexnow` — Bing/Yandex'e anında bildirim.
5. Google Business Profile: satış ofisi için işletme kaydı açın (Ömerağa Mah.). Yerel paket sonuçları için en yüksek etkili tek adım budur.

---

## 7. Öncelikli Yapılacaklar

| # | İş | Etki | Efor |
|---|---|---|---|
| 1 | GSC/Bing doğrulama kodlarını gir, sitemap gönder | Yüksek | 15 dk |
| 2 | Google Business Profile aç (satış ofisi) | Yüksek | 1 saat |
| 3 | Gerçek basın haberleri ekle veya kartları kaldır | Yüksek | 30 dk |
| 4 | Sosyal medya hesaplarını doğrula, `sameAs`'i güncelle | Orta | 20 dk |
| 5 | Her mahalle sayfasına 1 gerçek saha fotoğrafı ekle | Orta | 2 saat |
| 6 | Yerel gazete/haber sitelerinden 3-5 kaliteli geri bağlantı | Yüksek | Süregelen |
| 7 | Aylık GEO kontrolü (bkz. bölüm 4) | Orta | 30 dk/ay |

---

## 8. Kalıcı Kurallar

- **Yeni bölge sayfası** eklerken `src/data/locations.ts` içine benzersiz `intro`, `highlights` ve `faq` yazın. Kopyala-yapıştır sayfa açmayın — Google bunu kapı sayfası sayar ve tüm ağı cezalandırabilir.
- **Bir bölgede proje yoksa** bunu SSS içinde açıkça yazın.
- **Mesafe/süre** verirken "yaklaşık" ifadesini koruyun.
- **Fiyat** yayınlamayın; satış ofisine yönlendirin.
- Her içerik değişikliğinden sonra `npm run build && npm run indexnow`.
