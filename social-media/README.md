# MİA PARK OCEAN — Sosyal Medya Klasörü

Bu klasör, projenin sosyal medya iletişiminin tek kaynağıdır. Tasarımcı, içerik
üreticisi ve satış ekibi aynı dosyalardan çalışır.

| Dosya | İçerik |
|---|---|
| [`01-marka-kiti.md`](./01-marka-kiti.md) | Renkler, fontlar, logo kullanım kuralları, dalga motifi |
| [`02-profil-metinleri.md`](./02-profil-metinleri.md) | Instagram / Facebook / YouTube / TikTok bio ve profil ayarları |
| [`03-icerik-takvimi.md`](./03-icerik-takvimi.md) | 4 haftalık dönen içerik takvimi ve içerik sütunları |
| [`04-post-metinleri.md`](./04-post-metinleri.md) | Kullanıma hazır 24 gönderi metni |
| [`05-hashtag-setleri.md`](./05-hashtag-setleri.md) | Konuya göre hashtag setleri |
| [`06-gorsel-brief.md`](./06-gorsel-brief.md) | Şablon ölçüleri ve tasarım brief'leri |
| [`07-lansman-plani.md`](./07-lansman-plani.md) | 21 Ağustos lansmanı — gün gün paylaşım planı |

## Instagram ızgara seti

[`instagram/`](./instagram/) — 23 geniş panel, her biri 3 gönderiye bölünmüş:
**69 gönderi.** Profil ızgarasında her satır tek bir geniş görsel gibi görünür.
Paylaşım sırası ve sabitleme yönergesi için
[`instagram/README.md`](./instagram/README.md); profilin tamamının maketi
`instagram/IZGARA-ONIZLEME.jpg`. Yeniden üretmek için:

    npm run instagram

## Hazır görseller

Baskıya ve paylaşıma hazır varlıklar `public/etkinlik/` klasöründedir:

| Dosya | Ölçü | Kullanım |
|---|---|---|
| `davetiye-karti.png` | 1080×1350 | WhatsApp / Instagram gönderi davetiyesi |
| `davetiye-karti-story.png` | 1080×1920 | Instagram / WhatsApp story |
| `masa-qr-davetiye.png` | A5, 300 dpi | Masaya konulacak davetiye + RSVP QR etiketi |
| `masa-qr-basin.png` | A5, 300 dpi | Masaya konulacak basın açıklaması QR etiketi |
| `qr-davetiye.png` / `.svg` | — | Tekil QR (afiş, e-posta imzası) |
| `qr-basin.png` / `.svg` | — | Tekil QR |

Logo varlıkları `public/brand/` klasöründedir.

## Değişiklik yapmak

- Etkinlik bilgisi değişirse: `src/data/event.ts` → sonra `npm run etkinlik`
  (davetiye ve QR görselleri yeniden üretilir).
- Logo değişirse: `brand-source/logo-ocean-source.jpg` → sonra `npm run brand`.

## Altın kural

**Logo hiçbir zaman renklendirilmez, üzerine yazı yazılmaz ve daima beyaz zeminde
durur.** Koyu görsellerde logo beyaz bir plaketin (kartın) içine alınır.
