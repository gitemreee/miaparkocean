# MİA PARK OCEAN — Arsa panosu serisi · Ölçü ve baskı föyü

Arsayı çeviren çite, dışarıdan okunacak şekilde asılan panolar. Aynı
sekiz tasarımın bilbord karşılığı `tabela/arsa-mia/` altında;
**görseller aynı, bantlar farklı.**

| Arsa (bu klasör) | Bilbord (`arsa-mia/`) |
|---|---|
| Üst bantta **PROJE ALANI** | Üst bantta **İZMİT MİA BÖLGESİ** |
| Alt bantta **karekod + Instagram** | Alt bantta **iri telefonlar** |
| Karekod var — yayadan okunur | Karekod yok — araçtan okunmaz |
| 3000 × 2000 mm, 50 dpi | 5000 × 3000 mm, 40 dpi |

Arsa panosunun önünden geçen zaten yerinde durur; orada gereken şey
arsanın kime ait olduğudur. Bilbord ise şehrin başka yerinde durur,
oradan geçen projenin nerede olduğunu bilmez — o yüzden konum yazar.

## Dosyalar

| # | Dosya | Konu |
|---|---|---|
| 1 | `arsa-1-sosyal-yuvarlak.jpg` | Üç yuvarlak fotoğraf — sosyal yaşam |
| 2 | `arsa-2-sifir-faiz.jpg` | %0 faiz · 60 ay vade · kredi/faiz/kefil yok |
| 3 | `arsa-3-dusuk-pesinat.jpg` | Düşük peşinatla ev sahibi olun |
| 4 | `arsa-4-burada-eviniz.jpg` | Burada eviniz olsun istemez miydiniz? |
| 5 | `arsa-5-satis-ofisi.jpg` | Kahvenizi içmeye bekleriz + karekod |
| 6 | `arsa-6-ic-mekan.jpg` | Evinizi şimdiden görün — iç mekân |
| 7 | `arsa-7-dis-mekan.jpg` | Dışarısı da evinizin bir parçası |
| 8 | `arsa-8-daire-tipleri.jpg` | 1+0 · 1+1 · 2+1, m² ile |

`onizleme/` altında 1/6 ölçekli kontrol kopyaları var.

## Baskı

- **Ölçü:** 3000 × 2000 mm
- **Dosya:** 5906 × 3937 px, 1:1 ölçekte 50 dpi, JPEG kalite 92,
  altörnekleme kapalı (4:4:4), dpi gömülü
- **Renk:** sRGB. CMYK dönüşümünü matbaa kendi profiliyle yapsın.
- **Taşma payı:** dosyada yok. Gergi/kıvırma için her kenardan 20 mm
  ekleyin; kritik öğeler kenardan en az 110 mm içeride.
- **Malzeme:** 440 gr tente branda ya da 3 mm dekota. Brandada kuşgözü
  aralığı en fazla 500 mm — arsa cephesi rüzgâr alır.
- Karekod alt bantta, yerden 200–450 mm arasına düşer; yayadan okunur.
- Zeminden yükseklik: kimlik bandının alt kenarı en az 1400 mm yukarıda
  kalsın ki logo araç trafiğinden de görünsün.

## Tasarım sistemi

- Üstte ve altta düz bir bant; **bandı panodan iki çizgi ayırıyor**
  (kalın bir kural, altında ince bir kural). Dalga yok.
- **Bant rengi her tasarımın kendi paletinden ölçülüyor**: lacivert,
  antrasit, bronz, orman yeşili ve petrol mavisi panolar var — set tek
  tip mavi değil.
- Logo yapay zekâya çizdirilmiyor: üretimde iki bant boş bırakılıp
  gerçek MİA PARK OCEAN kilidi ve OCEAN GAYRİMENKUL imzası betikle
  basılıyor.
- Alt bandın ortasında sabit: **GÖRSELLER TEMSİLİDİR**.

## İçerik

**Fiyat yok.** Ödeme mesajı vade ve finansman modeliyle sınırlı: %0 faiz,
60 ay vade farksız taksit, kredi/faiz/kefil yok, düşük peşinat. Rakam
soran arıyor ya da karekodu okutuyor. Daire m² değerleri depodaki proje
verisinden geliyor.

## Yeniden üretim

```
npm run panolar
```

Tasarımlar Higgsfield (nano_banana_pro, 3:2, 4K) ile üretiliyor; istemler
`PROMPT.md`'de, ham PNG'ler `signage-source/hf-mia/` altında (git'e
girmiyor). Bantları ve logoları `scripts/build-mia-panolar.py` basıyor.
