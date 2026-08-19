# Arsa tabelaları — Higgsfield istemleri

Dört pano (finansman, sosyal yaşam, manzara, konum) **nano_banana_pro**
ile üretildi. Altısı `scripts/build-arsa-tabela.py` içinde çizilir.

## Ayarlar

| | |
|---|---|
| model | `nano_banana_pro` |
| aspect_ratio | `3:2` |
| resolution | `4k` → 5056 × 3392 px |
| medias | rol `image`, `signage-source/` altındaki render |

İndirilen PNG'ler `signage-source/hf-arsa/` altına `arsa-4-finansman`,
`arsa-6-sosyal`, `arsa-7-manzara`, `arsa-9-konum` adlarıyla konur.

## Ortak gövde

```
A horizontal CONSTRUCTION SITE HOARDING PANEL for a Turkish residential
project — the printed panel that clads the fence around a building plot.
Landscape. Print-quality, top-tier advertising-agency graphic design:
strict grid, big confident typography, generous space, no clutter, no
watermark, no invented extra text.

MANDATORY STRUCTURE:
• TOP BAND — the top 14% is a completely FLAT, EMPTY band of solid
  {renk}. No text, no graphics, no logo. Reserved space, leave it clean.
• BOTTOM BAND — the bottom 13% is a completely FLAT, EMPTY band of solid
  {renk}. No text, no graphics, no logo. Reserved space, leave it clean.
• MIDDLE — the remaining 73% carries the design below.
Do NOT draw any logo, brand mark, monogram, emblem or company symbol
anywhere in the image.

MIDDLE. {panoya özel tarif}

TEXT FIDELITY IS CRITICAL: reproduce every Turkish string EXACTLY as
written, preserving İ ı Ş ş Ğ ğ Ç ç Ö ö Ü ü. Do not translate,
abbreviate, re-spell, duplicate or invent any word.
```

Ayrılan iki bant tesadüf değil: kimlik bandı ve künye şeridi oraya
basılıyor, böylece marka yapay zekâya çizdirilmiyor ve on pano aynı
çizgide buluşuyor.

## Panoların mesajı

| Pano | MIDDLE özeti | Türkçe metin |
|---|---|---|
| **4 finansman** | kırık beyaz zemin, üç kare kart, üstü çizili banka/yüzde/tokalaşma ikonları, altta ince fotoğraf şeridi | TASARRUFA DAYALI FAİZSİZ FİNANSMAN · BANKA YOK · FAİZ YOK · KEFİL YOK · EV SAHİBİ OLMAK İÇİN BANKAYA GİTMENİZE GEREK YOK |
| **6 sosyal** | avlu/havuz render'ı tam sayfa, solda beyaz perde, dört madde | SOSYAL YAŞAM KAPINIZIN ÖNÜNDE · YÜZME HAVUZU · YÜRÜYÜŞ YOLLARI · PEYZAJ ALANLARI · ÇOCUK OYUN ALANI |
| **7 manzara** | balkondan deniz render'ı tam sayfa, sol altta koyu perde, yüksek kontrast serif | HER SABAH BAŞKA BİR MANZARA · GENİŞ BALKONLAR VE FERAH YAŞAM ALANLARI |
| **9 konum** | petrol gradyan, dev manşet, ince konum pini, altta ince gece şeridi | İZMİT MİA BÖLGESİ · KOCAELİ'NİN YENİ YAŞAM MERKEZİ |

## İki tuzak

**Maket üretiyor.** "Hoarding panel" denince üretim panoyu şantiye
çitine asılmış hâlde, perspektifli bir fotoğraf olarak çiziyor —
baskıya gidecek düz dosya değil. Kimlik panosu bu yüzden elendi ve
betikte çizildi. İsteme şunu eklemek gerekiyor: *"This is the FLAT
ARTWORK FILE, not a photograph of an installed sign. No fence, no
scaffolding, no perspective, no environment — the image IS the printed
panel, filling the frame edge to edge, viewed perfectly straight on."*

**Bant sınırına çizgi koyuyor.** Ayrılan bandın hemen altına kendi ince
şeridini çizebiliyor (konum panosunda beyaz bir şerit kalmıştı). Bandı
kalınlaştırmak çitin hizasını bozar; betikteki `clean_seam()` artığı
ölçüp siliyor — satır yatayda düz kaldığı sürece siliniyor, fotoğrafla
başlayan panolara dokunulmuyor.
