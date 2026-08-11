# MİA PARK OCEAN — Web Sitesi

İzmit MİA Bölgesi'nde S.S. Yahya Kaptan Birlik Yapı Kooperatifi tarafından geliştirilen 660 daireli **MİA PARK OCEAN** projesinin tanıtım + güven odaklı web sitesi. Tek yetkili satıcı: **Ocean Gayrimenkul**.

**Yığın:** Next.js 15 (App Router, statik export) · Tailwind CSS v4 · TypeScript · Framer Motion · lucide-react
**Tasarım dili:** "Gilded Horizon" — lacivert / altın / krem, ince hatlar, geniş boşluklar (bkz. kaynak `design-philosophy.md`).

---

## Kurulum ve Çalıştırma

```bash
npm install          # bağımlılıkları kur
npm run images       # kaynak render'ları public/images'e WebP olarak üretir (sharp)
npm run dev          # geliştirme sunucusu → http://localhost:3000
npm run build        # statik export → out/ klasörü
```

> `npm run images` yalnızca görselleri yeniden üretmek gerektiğinde çalıştırılır. Kaynak klasör: `C:\Users\emrey\Desktop\MIA PARK OCEAN`. Yeni görsel eklemek için `scripts/optimize-images.mjs` içindeki listeyi düzenleyin.

---

## Proje Yapısı

```
src/
  app/                 # sayfalar (App Router)
    page.tsx           # ana sayfa (14 bölüm)
    daireler/          # daire tipleri
    kooperatif/        # neden kooperatif + güvence + YKB + güven sistemi
    bilgi-merkezi/     # kooperatif bilgi merkezi (index + [slug] makale şablonu)
    bolge/             # İzmit MİA bölgesi + basında
    galeri/            # kategorili galeri
    iletisim/          # iletişim formu
    kvkk/              # KVKK aydınlatma metni
    sitemap.ts, robots.ts, icon.svg
  components/
    layout/            # Header, Footer, Logo, YkbLogo, PageHero, WhatsappFab
    sections/          # tüm sayfa bölümleri (Hero, Payment, Location, Catalog, PromoFilm, TrustSystem, ...)
    ui/                # Reveal, SmartImage, SectionHeading, Counter, Button, Icon
  data/                # TÜM METİN İÇERİĞİ BURADA (aşağıya bakın)
  lib/kb.ts            # bilgi merkezi yardımcıları
```

## İçerik Nasıl Güncellenir? (kod bilmeden)

Tüm metinler `src/data/` altındaki dosyalarda. Component'ler bu veriyi otomatik listeler.

| Ne değişecek | Dosya |
|---|---|
| İletişim, telefon, adres, menü | `data/site.ts` |
| Daire tipleri, m², adet, özellikler | `data/units.ts` |
| Ödeme modeli (faizsiz finansman metni) | `data/payment.ts` |
| Sosyal donatılar | `data/amenities.ts` |
| Lokasyon mesafeleri ve **harita koordinatı** | `data/location.ts` |
| Değerlenen bölge + **Basında MİA haberleri** | `data/region.ts` |
| Kooperatif güven kartları, güven sistemi, YKB künyesi | `data/cooperative.ts` |
| Sıkça Sorulan Sorular | `data/faq.ts` |
| Galeri görselleri | `data/gallery.ts` |
| **Katalog sayfaları + Tanıtım filmi linki** | `data/media.ts` |
| Bilgi Merkezi makaleleri | `data/articles.ts` |
| Bilgi Merkezi kısa rehberleri | `data/guides.ts` |

**Yeni haber eklemek:** `data/region.ts` → `press` dizisine `{ title, source, date, href, verified: true }` ekleyin.
**Yeni SSS eklemek:** `data/faq.ts` → diziye `{ category, question, answer }` ekleyin.
**Yeni makale eklemek:** `data/articles.ts` → diziye bir `Article` ekleyin; sayfa otomatik oluşur.
**Tanıtım filmi eklemek:** `data/media.ts` → `promoVideo.url` alanına YouTube/Vimeo **embed** linki yazın (örn. `https://www.youtube.com/embed/XXXX`). Boşken bölüm "Çok Yakında" gösterir.

---

## Deploy

Statik export (`out/`) her yerde barındırılabilir.

### Netlify — Sürükle & Bırak (önerilen, en kolay)

1. Bilgisayarınızda projeyi derleyin:
   ```bash
   npm run build
   ```
   Bu, proje kökünde bir **`out/`** klasörü oluşturur.
2. [app.netlify.com/drop](https://app.netlify.com/drop) adresini açın.
3. **`out` klasörünü** tarayıcıdaki alana sürükleyip bırakın. Site birkaç saniyede yayına girer.
4. Sonraki güncellemelerde: tekrar `npm run build` → yeni `out/` klasörünü aynı yere sürükleyin.

> Önemli: Netlify'a **`out` klasörünü** sürükleyin (projenin tamamını değil). Cache header'ları ve 404 sayfası `out/` içine hazır gelir (`_headers`, `404.html`).

**Alan adı:** Netlify'da site ayarlarından `miaparkocean.com` alan adını bağlayabilirsiniz (Domain settings → Add custom domain).

**Form:** İletişim formu Netlify Forms (`data-netlify="true"`) ile otomatik yakalanır; gönderimler Netlify panelinde **Forms → "iletisim"** altında görünür. (Netlify dışı hosting'de form **WhatsApp yedeği** ile çalışmaya devam eder.)

### Diğer seçenekler

- **Netlify (Git):** Repo'yu bağlayın; `netlify.toml` build ayarlarını (`npm run build`, publish `out`) otomatik okur.
- **Vercel:** Framework Next.js olarak algılanır; export ayarı hazırdır.
- **Klasik hosting (cPanel/FTP):** `out/` içeriğini `public_html`'e yükleyin.

> Not: `public/mia-park-ocean-katalog.pdf` ~22 MB'dır (indirilebilir katalog). Gerekmezse silinebilir; buton `data/media.ts` üzerinden yönetilir.

---

## ⚠️ [DOĞRULANACAK] — Yayın Öncesi Netleştirilecekler

Aşağıdaki bilgiler kaynak dosyalarda **elde olmadığı için işaretlenmiştir**. Yayına almadan önce doğru verilerle güncelleyin:

1. **Daire toplamı:** Broşür kapağında tipler 500+134+16 = **650** ediyor ancak başlıkta **660** yazıyor. Kesin dağılım netleştirilmeli. (`data/project.ts`, `data/units.ts`)
2. **S.S. Yahya Kaptan Birlik Yapı Kooperatifi künyesi:** ortak sayısı, kuruluş sicil no, MERSİS, yönetim kurulu. (`data/cooperative.ts` → `cooperativeOrg.facts`)
3. **YKB logosu:** İnline paylaşıldı, diskte dosya yoktu → **SVG olarak yeniden çizildi** (`components/layout/YkbLogo.tsx`). Birebir marka dosyası varsa `public/` altına konup değiştirilebilir. Not: resmi logoda unvan "YAHYAKAPTAN BİRLİK" (bitişik) yazıyor; sitede "Yahya Kaptan" kullanıldı — tercih edilen yazım teyit edilmeli.
4. **Basında MİA haberleri:** `data/region.ts` içindeki 3 kart örnek başlıktır (`verified: false`). Gerçek haber linkleriyle güncellenmeli.
5. **Tanıtım filmi:** `data/media.ts` → `promoVideo.url` boş. Film linki gelince eklenecek.
6. **Harita konumu:** Kullanıcının verdiği koordinat kullanıldı (40.736667, 29.944889 · PWPV+MX6). Satış ofisi pin'i teyit edilebilir. (`data/location.ts`, `data/site.ts`)
7. **İnşaat aşaması / teslim tarihi:** SSS'de iletişime yönlendiriliyor; net bilgi gelince eklenmeli. (`data/faq.ts`)
8. **KVKK:** Veri sorumlusunun tam ticaret unvanı, MERSİS ve tebligat adresi. (`app/kvkk/page.tsx`)
9. **Katalog PDF:** Şu an 8 sayfalık broşür PDF'i kullanılıyor; nihai katalog PDF'i ile değiştirilebilir (`public/mia-park-ocean-katalog.pdf`).

### Hukuki / Finansal Teyit (önemli)

- **"Tasarrufa Dayalı Faizsiz Finansman Sistemi"** ifadesi kullanıcı direktifiyle konumlandırılmıştır. Bu terim Türkiye'de BDDK denetimli (7292 sayılı Kanun) düzenli bir modeldir; kooperatif yapısıyla ilişkisi ve kullanım hakkı **avukat/mali müşavir onayı** gerektirir.
- Sitede resmi içerik dosyasındaki **yasak ifadeler** kullanılmamıştır ("devlet garantisi", "kesin teslim", "asla ek ödeme çıkmaz", "tam vergiden muaf", "garantili getiri" vb.).
- Kesinleşmemiş kooperatif uygulamaları makalelerde "**proje politikası olarak öngörülmektedir**" notuyla etiketlenmiştir.
- Nihai metinler; kooperatifler hukuku avukatı, SMMM/YMM ve teknik müşavir tarafından proje özelinde kontrol edilmelidir.

---

## Sonraki Adımlar (opsiyonel)

- Üye Portalı ve Belge Merkezi mockup ekranları (içerik dosyası bölüm 10) — ileride eklenebilir.
- Çok dilli yapı (EN / DE / AR) — veri katmanı buna uygun kurgulanmıştır.
- GA4 / Meta Pixel — id gelince `app/layout.tsx`'e eklenir.
