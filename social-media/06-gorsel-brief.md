# Görsel Şablon Brief'i

Tasarımcıya verilecek teknik dosya. Renkler ve fontlar için
[`01-marka-kiti.md`](./01-marka-kiti.md).

---

## Ölçüler

| Format | Piksel | Oran | Güvenli alan |
|---|---|---|---|
| Instagram gönderi (dikey) | 1080 × 1350 | 4:5 | üst/alt 120 px |
| Instagram kare | 1080 × 1080 | 1:1 | kenar 90 px |
| Story / Reels kapağı | 1080 × 1920 | 9:16 | üst 250 px, alt 320 px |
| Facebook kapak | 1640 × 664 | — | orta 1200 × 500 |
| YouTube banner | 2560 × 1440 | — | orta 1546 × 423 |
| YouTube küçük resim | 1280 × 720 | 16:9 | kenar 60 px |
| WhatsApp paylaşımı | 1080 × 1350 | 4:5 | — |
| Baskı — A5 etiket | 1748 × 2480 | 300 dpi | kenar 120 px |

---

## Ortak düzen (tüm formatlarda aynı iskelet)

```
┌─────────────────────────────┐
│  GRADYAN BANT               │  ← Deep Navy → Sapphire → Logo Blue
│  (yükseklik %26–34)         │     üstte etiket, altında başlık
│                             │
│  ╭─ 3 katmanlı DALGA ─╮     │  ← logodaki dalga, beyaz
├─────────────────────────────┤
│                             │
│      [ LOGO ]               │  ← beyaz zeminde, ortalı
│                             │
│      İÇERİK                 │  ← beyaz zemin
│      (metin / görsel)       │
│                             │
│      [ CTA / site adresi ]  │
│                             │
│  ╭─ ters DALGA ─╮           │
│  GRADYAN TABAN              │  ← alt bilgi: telefon, site
└─────────────────────────────┘
```

Bu iskelet `public/etkinlik/davetiye-karti.png` ve `masa-qr-basin.png`
dosyalarında birebir uygulanmıştır — referans olarak açın.

---

## Dalga motifi

Üç katman, logodaki sırayla. SVG yolları `src/components/ui/Wave.tsx`
içindedir; tasarımcıya SVG olarak verin.

| Katman | Renk (açık zemin) | Opaklık |
|---|---|---|
| Arka | `#D6E6F3` | %50 |
| Orta | `#F3F8FC` | %85 |
| Ön | `#FFFFFF` | %100 |

Koyu bant üzerine oturan dalgada aynı sıra, marka gradyanıyla doldurulur.

---

## Şablon tipleri

### 1. Tek görsel — proje render'ı
- Render tam kare, üstüne alttan yukarı koyu perde
  (`rgba(0,9,38,0.92)` → şeffaf)
- Sol altta: etiket (Manrope 700, büyük harf, `#D6E6F3`) + başlık (Marcellus, beyaz)
- Sağ üstte: beyaz plaket içinde logo işareti (56 px)
- Alt kenarda ince dalga şeridi

### 2. Carousel — bilgilendirme
- **Kapak:** gradyan bant + dalga + beyaz alanda büyük soru cümlesi
- **İç kareler:** beyaz zemin, sol üstte küçük logo işareti, tek fikir/kare
- **Son kare:** CTA — "Detaylar: miaparkocean.com" + QR (isteğe bağlı)
- Kare başına en fazla **20 kelime**

### 3. Story — 4 kare kural
- Kare 1: soru / dikkat çekici cümle
- Kare 2–3: cevap, tek görsel + kısa metin
- Kare 4: CTA + bağlantı çıkartması
- Metin üst %250 px ve alt %320 px içine **yazılmaz** (arayüz kapatır)

### 4. SSS gönderisi
- Beyaz zemin, ortada Sapphire renkli büyük soru işareti veya ikon
- Soru: Marcellus, 2–3 satır
- Altında ince gradyan çizgi
- Sağ altta logo işareti

### 5. Rozet / güven şeridi
- Beyaz zemin, mint (`#D1F2EB`) zeminli pill rozetler
- Rozet metni Forest (`#0B6E4F`), yanında ✓ ikonu
- "Bankasız · Faizsiz · Kefilsiz · 60 Ay Vade"
- **Yeşilin tek göründüğü yer burasıdır.**

---

## İkonografi

- Kaynak: **Lucide** (sitede kullanılan set) — https://lucide.dev
- Çizgi kalınlığı: 2 px · Köşe: yuvarlak
- İkon kutusu: 44 × 44 px, 12 px yuvarlatma, marka gradyanı zemin, beyaz ikon
- Kullanılan ikonlar: `Waves`, `Dumbbell`, `Flame`, `Baby`, `Car`, `ShieldCheck`,
  `MapPin`, `Percent`, `CalendarClock`, `Ban`, `UserRoundX`

---

## Fotoğraf ve render kullanımı

- Render kaynağı: `public/images/` (WebP)
- Sosyal medyada JPG'ye çevirin, kalite 85, uzun kenar 1350–1920 px
- Render üzerine **her zaman** koyu perde uygulayın; metin doğrudan render
  üzerine yazılmaz
- Şantiye fotoğrafları rötuşlanmaz — güven içeriğinin gücü gerçekliğindedir

---

## Erişilebilirlik

- Metin/zemin kontrastı en az **4.5:1**
- Beyaz metin yalnızca Sapphire (`#0F52BA`) veya daha koyu zeminde
- Emerald (`#50C878`) üzerine **beyaz metin yazılmaz** (kontrast yetersiz) —
  bu renk yalnızca ikon ve ince vurgu içindir
- Her gönderiye alternatif metin (alt text) yazın

---

## Teslim formatı

- Kaynak dosya: Figma veya Canva (paylaşımlı bağlantı)
- Çıktı: PNG (baskı) + JPG kalite 85 (sosyal)
- Dosya adı: `mpo-<format>-<konu>-<tarih>.png`
  örn. `mpo-ig-post-forekazik-20260821.png`
- Baskı çıktılarında **3 mm taşma payı** ve 300 dpi
