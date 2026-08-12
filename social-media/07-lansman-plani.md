# Lansman İletişim Planı — 21 Ağustos 2026

**Etkinlik:** MİA PARK OCEAN Lansman & Basın Toplantısı
**Tarih:** 21 Ağustos 2026, Cuma · **Saat:** 10:00
**Yer:** Emex Otel, Kocaeli
**Etkinlik sorumlusu:** Gül Hanım · 0534 859 26 72

**Davetiye sayfası:** https://miaparkocean.com/davetiye/
**Basın açıklaması:** https://miaparkocean.com/basin-aciklamasi/

> Her iki sayfa da arama motorlarına kapalıdır (`noindex`); yalnızca QR ve
> doğrudan bağlantıyla paylaşılır.

---

## Hazır varlıklar

| Dosya | Kullanım |
|---|---|
| `public/etkinlik/davetiye-karti.png` | WhatsApp ve Instagram gönderi davetiyesi (1080×1350) |
| `public/etkinlik/davetiye-karti-story.png` | Story davetiyesi (1080×1920) |
| `public/etkinlik/masa-qr-davetiye.png` | Masaya konulacak davetiye/RSVP etiketi (A5, 300 dpi) |
| `public/etkinlik/masa-qr-basin.png` | Masaya konulacak basın açıklaması etiketi (A5, 300 dpi) |
| `public/etkinlik/qr-davetiye.svg` | Afiş, e-posta imzası, roll-up için tekil QR |
| `public/etkinlik/qr-basin.svg` | Aynı |

**Baskı notu:** A5 etiketleri 250–300 gr mat kuşe kartona bastırın, mat selofan
kaplama önerilir. Masa üstünde ayakta durması için akrilik menü standı kullanın.
QR yüksek hata düzeltme (H) seviyesindedir — %30'a kadar bozulmada bile okunur.

---

## Zaman çizelgesi

### T-9 gün (12 Ağustos) — bugün
- [ ] Davetli listesini kesinleştirin (basın, yerel yönetim, iş ortakları, üyeler)
- [ ] Davetiye kartını WhatsApp'tan göndermeye başlayın
- [ ] `/davetiye` sayfasını test edin: form → WhatsApp akışı çalışıyor mu?
- [ ] Masa etiketlerini baskıya verin

### T-7 gün (14 Ağustos)
- [ ] **Sosyal medya duyurusu #1** — tarih açıklaması
  > Metin: `04-post-metinleri.md` → D1
- [ ] Basın davetiyelerini e-postayla gönderin (QR + `/davetiye` bağlantısı)
- [ ] Yerel gazete ve haber sitelerine ön bilgilendirme

### T-5 gün (16 Ağustos)
- [ ] **Story serisi** — "Geri sayım başladı" (4 kare)
- [ ] Katılım bildirimlerini takip edin (WhatsApp)
- [ ] Otel ile masa düzeni, projeksiyon ve ikram teyidi

### T-3 gün (18 Ağustos)
- [ ] **Sosyal medya duyurusu #2** — programı paylaşın
- [ ] Basılan etiketleri teslim alın, QR'ları **telefonla test edin**
- [ ] Sunum dosyasını son hâline getirin
- [ ] Katılım teyidi vermeyenlere hatırlatma araması

### T-1 gün (20 Ağustos)
- [ ] **Story** — "Yarın görüşmek üzere" + mekân görseli
- [ ] Etiketleri ve roll-up'ları otele götürün
- [ ] Karşılama masası düzeni: QR etiketleri her masaya
- [ ] Fotoğrafçı/video ekibiyle çekim listesi netleştirin

### Etkinlik günü (21 Ağustos)
| Saat | İş |
|---|---|
| 08:30 | Ekip mekânda, masa etiketleri yerleştirilir |
| 09:00 | Teknik prova (projeksiyon, ses, tanıtım filmi) |
| 09:30 | Karşılama masası açılır, isim listesi hazır |
| 10:00 | **Karşılama ve ikram** — canlı story |
| 10:30 | Proje sunumu ve tanıtım filmi |
| 11:15 | Kooperatif modeli ve finansman |
| 11:45 | Soru-cevap |
| 12:15 | Kokteyl ve birebir görüşmeler |
| 13:00 | Kapanış |

**Gün içi sosyal medya:**
- 09:45 — Story: "Başlamak üzereyiz" (mekân)
- 10:15 — Story: karşılama, kalabalık
- 10:45 — Story: sunumdan kare
- 12:00 — Gönderi: sahne/sunum fotoğrafı + teşekkür metni
- 13:30 — Story: "Bugün bizimle olan herkese teşekkürler"

### T+1 gün (22 Ağustos)
- [ ] **Gönderi:** lansman özeti + fotoğraf carousel (6-8 kare)
- [ ] Basın bültenini haber sitelerine gönderin
- [ ] Katılımcılara teşekkür mesajı (WhatsApp) + katalog bağlantısı
- [ ] `/davetiye` sayfasındaki formdan gelen kayıtları satış ekibine aktarın

### T+3 gün (24 Ağustos)
- [ ] **Gönderi:** "Basında MİA PARK OCEAN" — çıkan haberler
- [ ] Çıkan haber linklerini `src/data/region.ts` → `press` dizisine ekleyin
      (`verified: true` yapın) — bu SEO için de değerlidir
- [ ] Lansman videosunu YouTube'a yükleyin, siteye gömün

### T+7 gün (28 Ağustos)
- [ ] Reels: lansman özeti (30-45 sn)
- [ ] Katılımcı geri dönüş oranını değerlendirin
- [ ] Randevu dönüşümlerini raporlayın

---

## Basın kiti (gazetecilere verilecek)

Fiziksel klasör veya QR ile dijital:

1. Basın bülteni (yazılı) — `/basin-aciklamasi` sayfasının çıktısı
2. Proje künyesi tek sayfa (600 daire, 4 blok, tipler, donatılar, finansman)
3. Yüksek çözünürlüklü render'lar (USB veya indirme bağlantısı)
4. Logo dosyaları — `public/brand/`
5. Yetkili iletişim: Ocean Gayrimenkul · 0540 028 00 41

---

## Ölçüm

| Metrik | Nasıl |
|---|---|
| Davetiye sayfası görüntülenmesi | GSC'de değil (noindex) — Netlify Analytics veya kısaltılmış bağlantı |
| QR okutma sayısı | Etiketlerdeki QR farklı sayfalara gidiyor; trafik ayrımı buradan |
| RSVP sayısı | WhatsApp'a düşen form mesajları |
| Katılım | Karşılama masası isim listesi |
| Basın yansıması | Çıkan haber sayısı ve erişimi |
| Satış dönüşümü | Lansman sonrası 30 gün içinde açılan randevu sayısı |

---

## Etkinlik bilgisi değişirse

`src/data/event.ts` dosyasını düzenleyin, sonra:

```bash
npm run etkinlik    # davetiye kartları ve QR etiketleri yeniden üretilir
npm run build       # /davetiye sayfası güncellenir
```

Tek kaynak burasıdır — sayfa, kart ve QR aynı veriden beslenir, tutarsızlık olmaz.
