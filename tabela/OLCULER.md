# MİA PARK OCEAN — Saha Tabelaları · Ölçü ve Baskı Föyü

Bu klasördeki dosyalar **baskıya hazırdır**. Tabelacıya bu föyle birlikte
verin. Tasarımın tamamı `scripts/build-signage.py` içinde milimetre olarak
yazılıdır; ölçü değişirse dosyalar yeniden üretilir (`npm run tabela`).

## Dosyalar

| Dosya | Gerçek ölçü | Ölçek / çözünürlük | Piksel |
|---|---|---|---|
| `totem-on-yuz.jpg` | 1200 × 4000 mm | 1:1 @ 75 dpi | 3543 × 11811 |
| `totem-arka-yuz.jpg` | 1200 × 4000 mm | 1:1 @ 75 dpi | 3543 × 11811 |
| `afis-1-kimlik.jpg` | 3000 × 2400 mm | 1:1 @ 50 dpi | 5906 × 4724 |
| `afis-2-finansman.jpg` | 3000 × 2400 mm | 1:1 @ 50 dpi | 5906 × 4724 |
| `afis-3-daireler.jpg` | 3000 × 2400 mm | 1:1 @ 50 dpi | 5906 × 4724 |
| `afis-4-konum.jpg` | 3000 × 2400 mm | 1:1 @ 50 dpi | 5906 × 4724 |
| `afis-5-sosyal-yasam.jpg` | 3000 × 2400 mm | 1:1 @ 50 dpi | 5906 × 4724 |

`MIA-PARK-OCEAN-TABELA-SUNUMU.pdf` — A4 yatay, 8 sayfa. Baskı için değil,
müşteriye/ekibe göstermek için. `onizleme/` klasöründe küçültülmüş kontrol
kopyaları ve `cit-dizilimi.jpg` (beş afiş yan yana) vardır.

Dosyalara DPI bilgisi gömülüdür; tabelacı açtığında doğru fiziksel ölçüde
gelir. Büyük formatta 1:1 ölçekte 50–75 dpi standarttır — afiş 3–30 m,
totem 5–50 m mesafeden okunur.

## Totem — 1200 × 4000 mm, çift yüzlü

Projenin **ön ve yan cephesine** birer adet. Her totem çift yüzlü: gelen ve
giden trafik iki farklı yüzü görür.

- **Ön yüz** — kimlik: logo, "Lüks artık ulaşılabilir.", 600 daire /
  4 yaşam tipi, 60 ay vade · %0 faiz bandı, künye.
- **Arka yüz** — bilgi: dört daire tipi (m² ve adet), mesafeler, künye.

Bant düzeni (üstten, mm):

```
    0 –  940   beyaz baş bandı      logo kilidi (amblem + isim + bölge)
  940 – 3280   mavi gövde           mesaj alanı
 3280 – 4000   beyaz ayak           QR · web · telefon · satıcı
```

**Üretim notları**

- Işıklı kutu tabela olarak öneriliyor: beyaz bantlar arkadan aydınlatılınca
  gece logo ve künye kendiliğinden okunur.
- Dosyada **taşma payı yok** — görünen yüz ölçüsüdür. Gerginlik/katlama için
  her kenardan 20 mm pay ekleyin, tasarımın kritik öğeleri kenardan en az
  95 mm içeridedir, kesim payı yazıya girmez.
- Zeminden yükseklik: baş bandının alt kenarı en az 2200 mm yukarıda kalsın
  ki logo araç trafiğinden görünsün.
- QR yerden yaklaşık 500–900 mm arasında kalır; yaya mesafesinden (30–80 cm)
  rahat okunur.

## Çevre afişleri — 3000 × 2400 mm, 5 modül

Şantiyeyi çeviren çite modüler olarak asılır. **Sıra serbesttir** ve
tekrarlanabilir: 15 m'lik bir cephe beş modülle bir kez, 30 m'lik cephe
iki tur döner.

| # | Konu | Ne diyor |
|---|---|---|
| 1 | Kimlik | Akşam görüntüsü + "Lüks artık ulaşılabilir." + 600 daire |
| 2 | Finansman | %0 faiz · 60 ay sabit taksit · bankasız/faizsiz/kefilsiz |
| 3 | Daire tipleri | Dört tipin iç mekânı, m² ve adetleri |
| 4 | Konum | Sekiz mesafe kartı (D100 1 dk … üniversite 10 dk) |
| 5 | Sosyal yaşam | Avlu, havuzlar, yürüyüş yolları + ortak alan rozetleri |

**Ortak künye şeridi.** Beş afişin de altında, aynı yükseklikte (üstten
2020 mm), 380 mm yüksekliğinde beyaz bir şerit vardır: web adresi, iki
telefon, karekod ve satıcı imzası. Afişler yan yana asıldığında çit boyunca
**kesintisiz beyaz bir çizgi** oluşur; set tek bir tasarım gibi okunur.
Bu yüzden afişler aynı hizada ve aynı yükseklikte asılmalıdır.

**Üretim notları**

- Malzeme: 440 gr branda (tam kapalı çit) ya da delikli mesh (rüzgâr yükü
  yüksekse). Mesh'te renkler ~%15 açılır; matbaaya "mesh için doygunluk
  artırılsın" notu düşün.
- Her kenardan 50 mm taşma payı ekleyin; kritik öğeler 130 mm içeridedir.
- Çıtaya/kuşgözüne denk gelen bölge en dıştaki 130 mm'dir — bu alanda yazı
  yoktur, delme güvenli.
- Alt künye şeridinin çamur/çamurluk hattının üstünde kalması için çitin
  alt kenarından en az 300 mm yukarıda asın.

## Karekodlar

| Yer | Adres |
|---|---|
| Totem | `https://miaparkocean.com/?utm_source=totem` |
| Afişler | `https://miaparkocean.com/?utm_source=saha-afis` |

`utm_source` sayesinde sahadaki tabeladan gelen ziyaretçi analitikte ayrı
görünür — hangi kanalın müşteri getirdiği ölçülebilir. Basılan dosyalardan
okunarak doğrulanmıştır.

## İçerik nereden geliyor

Tabelada yazan her rakam projenin veri dosyalarından üretiliyor; elle
yazılmıyor. Daire adedi ya da mesafe değişirse veriyi güncelleyip
`npm run tabela` demek yeterli.

| Bilgi | Kaynak |
|---|---|
| 600 daire, 4 tip, m² ve adetler | `src/data/units.ts` |
| Mesafeler | `src/data/location.ts` |
| Ortak alan rozetleri | `src/data/amenities.ts` |
| Telefon, web, satıcı | `src/data/site.ts` |
| 60 ay · %0 faiz metni | `src/data/payment.ts` |

## Dikkat

- **Bu afişler zorunlu şantiye tabelasının yerine geçmez.** Yapı sahibi,
  müteahhit, şantiye şefi, ruhsat tarih/no bilgilerini taşıyan resmî
  şantiye tabelası ayrıca asılmalıdır; bu set tanıtım amaçlıdır.
- Görsellerin tamamı mimari render'dır. Kullanılan üç dış cephe karesi
  baskı için 4096 px'e büyütülmüştür (`signage-source/`); mimari
  değişmemiştir, yalnızca çözünürlük artmıştır.
- **Logo renklendirilmez, üzerine yazı yazılmaz.** Koyu zeminde beyaz
  versiyonu, açık zeminde renkli versiyonu kullanılır; totemde beyaz bantla
  ayrılır.
- Ocean Gayrimenkul imzası şu an **tipografik** kuruludur: elimizdeki logo
  298 px ve bu ölçekte baskıda dağılıyor. Vektör logo (AI / EPS / SVG)
  gelirse `signage-source/ocean-logo-hi.png` olarak konulup betiğe
  bağlanabilir.

## Yeniden üretmek

```
npm run tabela
```

Gereksinimler: `pip install pillow numpy segno`.
