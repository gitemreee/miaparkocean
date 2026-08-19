# FİYAT AVANTAJI roll-up — ölçü ve baskı föyü

## Dosyalar

| Dosya | Gündüz/Gece | Rakam |
|---|---|---|
| `fiyat-rollup-gunduz-1.jpg` | gündüz — geometrik sans, mercan | var |
| `fiyat-rollup-gunduz-2.jpg` | gündüz — sıkışık kondens, bronz | var |
| `fiyat-rollup-gece-1.jpg` | gece — yüksek kontrast serif, şampanya | var |
| `fiyat-rollup-gece-2.jpg` | gece — geniş grotesk, bakır | var |
| `fiyat-rollup-gunduz-1-fiyatsiz.jpg` | gündüz — geometrik sans, mercan | yok |
| `fiyat-rollup-gunduz-2-fiyatsiz.jpg` | gündüz — sıkışık kondens, bronz | yok |
| `fiyat-rollup-gece-1-fiyatsiz.jpg` | gece — yüksek kontrast serif, şampanya | yok |
| `fiyat-rollup-gece-2-fiyatsiz.jpg` | gece — geniş grotesk, bakır | yok |

`onizleme/` altındakiler 1/6 ölçekli, sadece ekranda bakmak için.

## Baskı

- **Görünen ölçü:** 100 × 200 cm (1000 × 2000 mm)
- **Dosya:** 3937 × 7874 px, 100 dpi, JPEG kalite 92, kromalık altörnekleme
  kapalı (4:4:4), gömülü dpi bilgisi var
- **Renk:** sRGB. Matbaa CMYK isterse dönüşümü kendi profiliyle yapsın;
  marka mavisi #075878 dönüşümde koyulaşırsa provada düzeltilir.
- **Kasete giren pay:** dosyada YOK. Roll-up kasetine giren 15–20 cm'lik
  payı matbaa alt kenardan uzatarak eklesin; tasarımın alt bandı düz renk
  olduğu için uzatma dikişsiz olur.
- **Taşma payı:** yanlarda gerek yok, tasarım kenara kadar dolu.

## Yerleşim

- Üst bant: MİA PARK OCEAN kilidi (üretimde değil, gerçek logo dosyasından
  basılıyor)
- Başlık: FİYAT AVANTAJI + "Kaçırılmayacak fırsat!" + SINIRLI SAYIDA mührü
- Orta blok: solda üç buzlu cam fiyat kartı (1+0 / 1+1 / 2+1), sağda dört
  beyaz özellik hapı
- Alt: proje fotoğrafı → künye (finansman + iletişim) → OCEAN GAYRİMENKUL
  imzası

## Fiyatlar

| Tip | Peşinat | Aylık | Vade |
|---|---|---|---|
| 1+0 | 699.000 ₺ | 29.900 ₺ | 60 ay, vade farksız |
| 1+1 | 999.000 ₺ | 39.900 ₺ | 60 ay, vade farksız |
| 2+1 | 2.000.000 ₺ | 50.000 ₺ | 60 ay, vade farksız |

Bu rakamlar depoda bir veri dosyasından gelmiyor; ilk ikisi verilen
görselden, 2+1 sözlü olarak alındı. **Baskıya gitmeden satış ekibine
doğrulatın.** Fiyatsız sürümler rakam yerine m² ve vade gösterip
"PEŞİNAT VE TAKSİT SEÇENEKLERİ İÇİN BİZİ ARAYIN" diyor.

## Yeniden üretim

Tasarım Higgsfield (nano_banana_pro) ile üretiliyor, istemler
`PROMPT.md` dosyasında. Ham PNG'ler `signage-source/hf/` altına indirilip:

```
npm run fiyat:rollup
```

Betik oranı 9:16'dan 1:2'ye tamamlıyor, logoları basıyor, 100 dpi'a
ölçekliyor. Ayrıntı: `scripts/finish-fiyat-rollup.py`.
