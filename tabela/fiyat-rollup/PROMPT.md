# FİYAT AVANTAJI roll-up — üretim istemleri

Tasarım **Higgsfield / nano_banana_pro** ile üretiliyor. Bu dosya kaynak
kod yerine geçiyor: istemi değiştir, yeniden üret, `npm run fiyat:rollup`
ile bitir.

## Ayarlar

| | |
|---|---|
| model | `nano_banana_pro` |
| aspect_ratio | `9:16` (modelin en uzun dikey oranı; 1:2'ye betik tamamlıyor) |
| resolution | `4k` → 3072 × 5504 px |
| medias | gündüz: `signage-source/entrance-gate.jpg`, gece: `signage-source/night-gate.jpg`, rol `image` |

İndirilen PNG'ler `signage-source/hf/` altına şu adlarla konuyor:
`hf-0-gunduz-a`, `hf-1-gunduz-b`, `hf-2-gece-a`, `hf-3-gece-b` ve fiyatsız
karşılıkları `hf-10…hf-13` (`-fiyatsiz` ekiyle).

## Ortak gövde

İstem her tasarımda aynı iskeleti kuruyor, sadece `{...}` ile işaretli
yerler değişiyor:

```
A vertical ROLL-UP BANNER (pull-up banner) design for a Turkish
residential real-estate project. Portrait. Print-quality 300dpi look,
{ÜSLUP}: strict grid, crisp typography, generous breathing space,
absolutely no clutter, no watermark, no invented extra text.

{GÜNDÜZ|GECE} VERSION. Mood: {ATMOSFER}.

1) HEADER (top ~18%). {ZEMİN}. Headline in {BAŞLIK TİPOGRAFİSİ},
   two lines:  line 1: FİYAT — {RENK 1}   line 2: AVANTAJI — {RENK 2}
   Beneath, one flowing handwritten SCRIPT line: Kaçırılmayacak fırsat!
   Top-right: circular seal, two lines: SINIRLI / SAYIDA.

2) MIDDLE BLOCK (~37%), two columns.
   LEFT (58%): three rounded FROSTED-GLASS cards, semi-transparent
   ({SAYDAMLIK}), gradient {KART GRADYANI}, hairline inner border, soft
   shadow, real frosted blur. Left: unit-type badge. Right: two small
   uppercase labels each with a big value beneath.
     {KART İÇERİĞİ}
   RIGHT (42%): four solid WHITE rounded pills, flat line icon + two
   uppercase lines:
     check           — EN UYGUN / FİYATLAR
     rising chart    — YÜKSEK YATIRIM / POTANSİYELİ
     building        — MODERN MİMARİ / GENİŞ PEYZAJ
     calendar        — VADE FARKSIZ / 60 AY TAKSİT
   Full-width bar underneath: {ALT ÇUBUK}

3) PHOTOGRAPH (bottom ~45%). Use the ATTACHED PHOTOGRAPH, full banner
   width, TOP EDGE softly feathered into the gradient above with no hard
   seam and no visible cut line.

4) FOOTER BAR at the very bottom. Centered uppercase:
   TASARRUFA DAYALI FAİZSİZ FİNANSMAN
   Below, with bullets: BANKA YOK · FAİZ YOK · KEFİL YOK
   Below that: miaparkocean.com   0540 028 00 41   0541 128 40 41
   LEAVE THE BOTTOM-LEFT AND BOTTOM-RIGHT CORNERS OF THE FOOTER BAR
   EMPTY — flat reserved space for logos. Do NOT draw any logo, brand
   mark, monogram, emblem or company symbol anywhere in the image.

TEXT FIDELITY IS CRITICAL: render every Turkish string EXACTLY as
written, preserving İ ı Ş ş Ğ ğ Ç ç Ö ö Ü ü and the Turkish lira sign ₺
and the thousands separator dots. Do not translate, abbreviate, re-spell,
duplicate or invent any word or number.
```

Son paragraf pazarlık konusu değil: Türkçe noktalı/noktasız İ-ı ve ₺
ancak bu kadar açık söylenince tutuyor. Üretilen sekiz panonun tamamında
yazım tam çıktı, yine de baskıdan önce tek tek okunmalı.

Logo yasağı da bilinçli: markayı yapay zekâya çizdirmiyoruz, künyenin iki
alt köşesi boş bırakılıp gerçek logo dosyası betikte basılıyor.

## Tasarım farkları

| | ÜSLUP | ZEMİN / ATMOSFER | BAŞLIK TİPOGRAFİSİ | RENK 1 / RENK 2 | KART GRADYANI |
|---|---|---|---|---|---|
| **gunduz-1** | top-tier advertising-agency | #F1FCFD → #B8E4EC, aydınlık, güneşli | extra-bold geometric sans (Poppins/Gilroy), ortalı | #075878 / mercan #F2704B | #1A7496 → #2C94B4, %70 |
| **gunduz-2** | editorial, Swiss grid | sıcak kırık beyaz #FAF7F2, sağdan aqua parlama | tall condensed caps (Barlow Condensed/Oswald), sola dayalı | bronz #B9884E / #075878 | #2C94B4 → #48ABC5, %65 |
| **gece-1** | luxury agency | #04222F → #075878, şampanya parıltı | high-contrast serif (Playfair/Didot), ortalı | şampanya #E8C88A italik / beyaz | #095678 → #1A7496, %55 |
| **gece-2** | contemporary premium | #071B2B → #0B4E6C, sağ alttan camgöbeği bloom | heavy wide grotesque caps, sola dayalı | beyaz kontur / bakır #C97B5A | #1A7496 → #2C94B4, %55 |

Gündüz ve gece hem renk hem YAZI TİPİ olarak ayrışıyor — istenen buydu.

## Kart içeriği

**Rakamlı** (`ALT ÇUBUK` = `VADE FARKSIZ 60 AY TAKSİT`):

```
Card 1 — badge 1+0 — label PEŞİNAT, figure 699.000 ₺ — label AYLIK SADECE, figure 29.900 ₺
Card 2 — badge 1+1 — label PEŞİNAT, figure 999.000 ₺ — label AYLIK SADECE, figure 39.900 ₺
Card 3 — badge 2+1 — label PEŞİNAT, figure 2.000.000 ₺ — label AYLIK SADECE, figure 50.000 ₺
```

**Rakamsız** (`ALT ÇUBUK` = `PEŞİNAT VE TAKSİT SEÇENEKLERİ İÇİN BİZİ ARAYIN`),
ayrıca istemin sonuna şu satır ekleniyor:
*"IMPORTANT: this version carries NO prices. No money amounts, no ₺ lira
figures, no numbers beyond the unit types, the square metres and 60 AY."*

```
Card 1 — badge 1+0 — label DAİRE BÜYÜKLÜĞÜ, value 28 m² — label ÖDEME PLANI, value 60 AY VADE
Card 2 — badge 1+1 — label DAİRE BÜYÜKLÜĞÜ, value 50 m² — label ÖDEME PLANI, value 60 AY VADE
Card 3 — badge 2+1 — label DAİRE BÜYÜKLÜĞÜ, value 100 m² — label ÖDEME PLANI, value 60 AY VADE
```
