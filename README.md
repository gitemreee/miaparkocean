# MİA PARK OCEAN — Web Sitesi

İzmit MİA Bölgesi'nde S.S. Yahya Kaptan Birlik Yapı Kooperatifi tarafından geliştirilen 660 daireli **MİA PARK OCEAN** projesinin tanıtım + güven odaklı web sitesi. Tek yetkili satıcı: **Ocean Gayrimenkul**.

**Yığın:** Next.js 15 (App Router, statik export) · Tailwind CSS v4 · TypeScript · Framer Motion · lucide-react
**Tasarım dili:** "Deep Ocean" — beyaz zemin, mavi gradyan geçişler, logodaki dalga sitenin imzası.

---

## Kurulum ve Çalıştırma

```bash
npm install          # bağımlılıkları kur
npm run dev          # geliştirme sunucusu → http://localhost:3000
npm run build        # statik export → out/ klasörü
```

Yardımcı komutlar:

| Komut | Ne yapar |
|---|---|
| `npm run images` | Kaynak render'ları `public/images`'e WebP olarak üretir (sharp) |
| `npm run brand` | Logo varlıklarını, favicon'ları ve OG görselini yeniden üretir |
| `npm run etkinlik` | Davetiye kartlarını ve masa QR etiketlerini yeniden üretir |
| `npm run indexnow` | Yeni/güncel sayfaları Bing ve Yandex'e bildirir |

`brand` ve `etkinlik` komutları Python gerektirir: `pip install pillow numpy segno`

---

## Tasarım Sistemi

Tüm renk ve gradyan tanımları **tek yerde**: `src/app/globals.css`.

### Palet

| Rol | Ad | HEX |
|---|---|---|
| Zemin | Beyaz | `#FFFFFF` |
| Açık yüzey | Ice Blue | `#D6E6F3` |
| Orta ton | Powder Blue | `#A6C5D7` |
| Vurgu | Sapphire | `#0F52BA` |
| Derinlik | Deep Navy | `#000926` |
| **Logo mavisi** | logodan örneklendi | `#005478` · `#0C6C90` · `#18789C` · `#48B4CC` · `#9CD8E4` |
| İkincil aksan | Emerald / Forest | `#50C878` · `#0B6E4F` |

**Tüm gradyan geçişleri mavidir:** `Deep Navy → Sapphire → logo mavisi → turkuaz`.
Yeşil yalnızca güven/onay rozetlerinde kullanılır (`.pill-jade`), gradyanlarda yer almaz.

### Tipografi

- **Marcellus** (400) — başlıklar. Logodaki Trajan tarzı serifin devamı; tek ağırlıktır, kalınlaştırılmaz.
- **Manrope** (300–800) — gövde ve arayüz.

### Dalga — markanın imzası

Logonun altındaki dalga sitenin tekrar eden motifidir. SVG yolları
`src/components/ui/Wave.tsx` içinde tek kaynakta tutulur ve dört yerde kullanılır:

1. **Bölüm geçişleri** — `<WaveDivider />`
2. **Hero alt kenarı** — akan kurdele + sabit siluet
3. **Sayfa geçişi** — `PageTransition`: rota değişince dalga ekranı süpürerek geçer
4. **Arka plan** — `WaveBackdrop`: sabit, çok hafif dalga dokusu tüm sayfanın arkasında

Açık bölüm zeminleri (`.surface-paper`, `.surface-tint`) yarı saydamdır ki arkadaki
dalga hafifçe görünsün.

### Logo kuralı

**Logo hiçbir yerde renklendirilmez ve daima beyaz zeminde durur.** Koyu bölümlerde
beyaz bir plaketin içine alınır. Ayrıntı: `social-media/01-marka-kiti.md`.

---

## Proje Yapısı

```
src/
  app/
    page.tsx              # ana sayfa
    daireler/             # daire tipleri
    kooperatif/           # neden kooperatif + güvence + YKB
    bilgi-merkezi/        # kooperatif bilgi merkezi (index + [slug])
    bolge/                # İzmit MİA bölgesi + basında
    bolgeler/             # YEREL SEO: index + [slug] (mahalle/ilçe/il)
    belgeler/ galeri/ iletisim/ kvkk/ cerez-politikasi/
    davetiye/             # gizli — lansman davetiyesi + RSVP (QR ile paylaşılır)
    basin-aciklamasi/     # gizli — basın bülteni (QR ile paylaşılır)
    llms.txt/             # GEO — yapay zekâ motorları için proje künyesi
    sitemap.ts, robots.ts, icon.png
  components/
    layout/               # Header, Footer, Logo, PageHero, PageTransition, WaveBackdrop
    sections/             # sayfa bölümleri (Hero, Payment, Location, RsvpForm, ...)
    ui/                   # Wave, Reveal, SmartImage, SectionHeading, Button, Counter
  data/                   # TÜM METİN İÇERİĞİ BURADA
  lib/
    seo.ts                # JSON-LD üreticileri (tek kaynak)
    kb.ts                 # bilgi merkezi yardımcıları
public/
  brand/                  # logo varlıkları
  etkinlik/               # davetiye kartları, masa QR etiketleri, tekil QR'lar
  images/ videos/
brand-source/             # kaynak logo + fontlar (üretim girdisi)
scripts/                  # varlık üreticileri + indexnow
docs/                     # SEO denetimi ve kurulum rehberleri
social-media/             # marka kiti, içerik takvimi, gönderi metinleri
```

---

## İçerik Nasıl Güncellenir? (kod bilmeden)

Tüm metinler `src/data/` altındadır.

| Ne değişecek | Dosya |
|---|---|
| İletişim, telefon, adres, menü, sosyal medya | `data/site.ts` |
| **Lansman etkinliği** (tarih, yer, program, sorumlu) | `data/event.ts` |
| **Bölge sayfaları** (mahalle/ilçe içerikleri) | `data/locations.ts` |
| **Arama motoru doğrulama kodları** | `data/verification.ts` |
| Daire tipleri, m², adet, özellikler | `data/units.ts` |
| Ödeme modeli | `data/payment.ts` |
| Sosyal donatılar | `data/amenities.ts` |
| Lokasyon mesafeleri ve harita koordinatı | `data/location.ts` |
| Değerlenen bölge + basında MİA haberleri | `data/region.ts` |
| Kooperatif güven kartları, YKB künyesi | `data/cooperative.ts` |
| Sıkça Sorulan Sorular | `data/faq.ts` |
| Galeri görselleri | `data/gallery.ts` |
| Katalog sayfaları + tanıtım filmi | `data/media.ts` |

`data/event.ts` değiştikten sonra `npm run etkinlik` çalıştırın — davetiye kartları
ve QR etiketleri aynı veriden yeniden üretilir, tutarsızlık olmaz.

---

## Yerel SEO ve GEO

- **20 bölge sayfası:** 8 İzmit mahallesi, 10 Kocaeli ilçesi, Sakarya ve İstanbul.
  Her sayfanın içeriği benzersizdir (şablon metin yoktur).
- **Yapısal veri:** `src/lib/seo.ts` üzerinden `@graph`; düğümler `@id` ile bağlıdır.
- **GEO:** `/llms.txt` üretici yapay zekâ motorlarına proje künyesini ve
  "doğruluk notları"nı sunar.
- **Dizine gönderim:** `docs/GSC-BING-KURULUM.md`
- **Denetim raporu:** `docs/SEO-AUDIT.md`

> **Önemli:** Proje yalnızca İzmit MİA Bölgesi'ndedir. Diğer il/ilçe sayfalarında
> orada proje varmış izlenimi verilmez; Sakarya ve İstanbul sayfalarında bu durum
> SSS içinde açıkça belirtilir.

---

## Gizli Sayfalar (QR ile paylaşılan)

| Sayfa | İçerik |
|---|---|
| `/davetiye/` | Lansman davetiyesi, program ve WhatsApp'a giden katılım formu |
| `/basin-aciklamasi/` | Basın bülteni tam metni |

Her ikisi de `noindex, nofollow` ve `robots.txt` ile taramaya kapalıdır; site
header/footer'ı gösterilmez (`SiteFrame` → `BARE_PREFIXES`).

Baskıya hazır QR etiketleri: `public/etkinlik/masa-qr-davetiye.png` ve
`masa-qr-basin.png` (A5, 300 dpi).

---

## Yayına Alma

Netlify (sürükle-bırak veya Git bağlantısı):

```bash
npm run build     # out/ klasörü üretilir
```

`netlify.toml` yapılandırması hazırdır. Yayından sonra:

```bash
npm run indexnow  # Bing ve Yandex'e bildir
```

---

## Formlar

Site statik export olduğu için sunucu tarafı yoktur. Tüm formlar
(iletişim, katılım bildirimi) doldurulan bilgiyi **ön-doldurulmuş bir WhatsApp
mesajına** çevirip ilgili numaraya yönlendirir.
