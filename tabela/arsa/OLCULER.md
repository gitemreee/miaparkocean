# MİA PARK OCEAN — Arsa çevre tabelaları · Ölçü ve baskı föyü

Arsayı çeviren çite, **dışarıdan okunacak** şekilde asılır. Yoldan geçen
tek bir panoya bakar; bu yüzden her pano tek mesaj taşır, kimlik ve
iletişim ise hepsinde tekrarlanır.

## Dosyalar — 10 modül

| # | Dosya | Konu | Kaynak |
|---|---|---|---|
| 1 | `arsa-01-proje-alani.jpg` | Kimlik: gece render, "Lüks artık ulaşılabilir." | betik |
| 2 | `arsa-02-ulasim.jpg` | Sekiz mesafe kartı (D100 1 dk … üniversite 10 dk) | betik |
| 3 | `arsa-03-odeme.jpg` | Vade farksız 60 ay taksit | betik |
| 4 | `arsa-04-finansman.jpg` | Banka yok · Faiz yok · Kefil yok | Higgsfield |
| 5 | `arsa-05-daireler.jpg` | Dört daire tipi, m² ve adet | betik |
| 6 | `arsa-06-sosyal.jpg` | Sosyal yaşam: havuz, yürüyüş yolu, peyzaj | Higgsfield |
| 7 | `arsa-07-manzara.jpg` | Balkondan manzara | Higgsfield |
| 8 | `arsa-08-yatirim.jpg` | Yüksek yatırım potansiyeli | betik |
| 9 | `arsa-09-konum.jpg` | İzmit MİA Bölgesi | Higgsfield |
| 10 | `arsa-10-karekod.jpg` | Karekod: planlar, ödeme, sanal tur | betik |

`onizleme/` altında 1/5 ölçekli kontrol kopyaları ve **`cit-dizilimi.jpg`**
— onunun yan yana hâli, çitin dışarıdan görünüşü.

## Baskı

- **Ölçü:** 3000 × 2000 mm (her modül aynı)
- **Dosya:** 5906 × 3937 px, 1:1 ölçekte 50 dpi, JPEG kalite 92,
  altörnekleme kapalı (4:4:4), dpi gömülü
- **Renk:** sRGB. CMYK dönüşümünü matbaa kendi profiliyle yapsın.
- **Taşma payı:** dosyada yok, görünen yüz ölçüsüdür. Gergi/kıvırma için
  her kenardan 20 mm pay ekleyin; kritik öğeler kenardan en az 110 mm
  içeride, kesim yazıya girmez.
- **Malzeme:** çit panosu için 440 gr tente branda ya da 3 mm dekota.
  Branda seçilirse kenar kuşgözü aralığı en fazla 500 mm olsun; arsa
  cephesi rüzgâr alıyor.

## Bant düzeni (mm, üstten)

```
    0 –  280   kimlik bandı   MİA PARK OCEAN kilidi + PROJE ALANI
  280 – 1740   mesaj alanı    panodan panoya değişen tek konu
 1740 – 2000   künye şeridi   karekod · web · Instagram · telefon · satıcı
```

**Bu iki bant onunda da birebir aynıdır.** Panolar aynı hizada ve aynı
yükseklikte asılırsa çit boyunca kesintisiz iki mavi çizgi oluşur, on
pano tek tasarım gibi okunur. Sıra serbesttir ve tekrarlanabilir: 30
metrelik bir cephe onunu bir kez, 60 metre iki tur döner.

**"PROJE ALANI" ibaresi her panonun sağ üstündedir** — hangi panonun
önünden geçilirse geçilsin arsanın kime ait olduğu yazar.

- Zeminden yükseklik: kimlik bandının alt kenarı en az 1400 mm yukarıda
  kalsın ki logo araç trafiğinden görünsün.
- Karekod künye şeridinde, yerden 200–450 mm arasına düşer; yaya
  mesafesinden okunur. Onuncu panodaki büyük karekod göz hizasındadır.

## İçerik notu

Panolarda **fiyat yok**. Ödeme mesajı vade ve finansman modeliyle
sınırlı; rakam soran karekodu okutur ya da telefonu arar. Daire adetleri
(472 / 96 / 16 / 16) ve mesafeler depodaki proje verisinden gelir.

## Yeniden üretim

```
npm run arsa
```

Altı pano `scripts/build-arsa-tabela.py` içinde milimetre olarak
yazılıdır. Dördü Higgsfield ile üretildi; istemler `PROMPT.md`'de, ham
PNG'ler `signage-source/hf-arsa/` altında (git'e girmiyor). Kaynağı ne
olursa olsun kimlik bandını ve künye şeridini hep betik basar — logo
yapay zekâya çizdirilmez.
