# MİA PARK OCEAN — Lansman sunumu (emlakçılara)

- `MIA-PARK-OCEAN-Lansman-Sunumu.pptx` — 15 slayt, 16:9, konuşmacı notlu
- `MIA-PARK-OCEAN-Lansman-Sunumu.pdf` — aynı sunumun PDF hâli (salondaki
  makinede Office yoksa bununla açın)
- `onizleme/slide-01…15.jpg` — slayt slayt önizleme

## Sunumdan önce YAPILACAK

**13. slaytta üç alan bilerek boş bırakıldı.** Bu rakamlar depoda yok,
uydurmadım; sunumdan önce siz doldurun:

- Komisyon oranı
- Hakediş zamanı
- Müşteri bildirim / koruma süresi

Emlakçının en çok merak ettiği slayt bu; boş kalırsa güven kaybı olur.

## Görsel dil

Organik mavi dalga blokları, fotoğrafın **dikdörtgen değil o eğrinin
içine maskelenmesi**, katmanlı mavi şeritler, kemer / daire / hap
formunda kartlar. Tek yazı tipi ailesi (Calibri), tek renk ailesi.

PowerPoint bunların hiçbirini kendi başına yapamaz: pptxgenjs bezier eğri
çizemez ve bir fotoğrafı serbest bir şeklin içine maskeleyemez. Bu yüzden
bütün organik parçalar `scripts/build-sunum-sekil.py` ile PIL + numpy'da
üretilip `kaynak/sekil/` altına şeffaf PNG olarak yazılıyor;
`scripts/build-sunum.js` sadece yerleştiriyor.

Maskeler analitik: her piksel için eğriye olan işaretli uzaklık hesaplanıp
1 piksellik yumuşak geçişe çevriliyor, o yüzden kenarlar tırtıklı değil.

### `kaynak/sekil/` içindekiler

| Önek | Ne |
|---|---|
| `bg-01…15` | Slayt zeminleri — dalga blokları, şeritler, maskeli fotoğraf |
| `k-*` | Kemer formunda daire tipi fotoğrafları (5. slayt) |
| `d-*` | Halkalı yuvarlak fotoğraflar (11. slayt) |
| `m-*` | Materyal önizlemeleri — **oranı korunarak** kutuya oturtulmuş |
| `i-*` | İkon rozetleri (telefon, web, instagram, konum, onay, kalkan) |

`m-*` görselleri bilerek `contain` ile üretiliyor: önceki sürümde
materyaller kutuya gerdirilmişti (bilbord %10, roll-up %20 yatayda
eziliyordu). Artık kaynak oranı ne ise o.

## Yerleşim gözle değil ÖLÇÜYLE

Dalgalı zeminde "sol yarı beyazdır" varsayımı tutmuyor; sınır her yükseklikte
başka yerden geçiyor. `scripts/sunum-alan.py` her zeminde koyu yazının ve
beyaz yazının okunacağı alanları yarım inçlik bantlar hâlinde raporluyor;
metin kutuları o sınırların içine yerleştirildi. `build-sunum.js` içindeki
`GUVENLI` tablosu o ölçümün özeti.

```
python3 scripts/sunum-alan.py                 # bütün zeminler
python3 scripts/sunum-alan.py bg-04-konum     # tek zemin
```

`scripts/sunum-tasma.py` de her metin kutusunu metrik olarak ölçüp kutuya
sığıp sığmadığını söylüyor (Calibri ile metrik uyumlu Carlito ile; o yoksa
Calibri'den geniş olan Liberation Sans'a düşüyor, yani güvenli tarafta
hata yapıyor).

```
python3 scripts/sunum-tasma.py sunum/MIA-PARK-OCEAN-Lansman-Sunumu.pptx
```

## Akış

| # | Slayt | Düzen | Ne yapıyor |
|---|---|---|---|
| 1 | Kapak | Sağ dalga bloğu | Lansman, tarih, yer |
| 2 | Gündem | Sol dalga bloğu | Yirmi dakikada altı başlık |
| 3 | Proje künyesi | Üst dalga bandı | 600 daire · 4 tip · 28–100 m² · 60 ay |
| 4 | Konum | Sağ dalga bloğu | Sekiz mesafe |
| 5 | Stok | Alt dalga bandı | Dört tip, kemer kartlarla |
| 6 | Sosyal yaşam | Sol dalga bloğu | Sekiz olanak + süs havuzu uyarısı |
| 7 | Ödeme modeli | Lacivert panel | Sunumun kalbi — %0 faiz, 60 ay |
| 8 | Yatırım | Sağ dalga bloğu | m² projeksiyonu (grafik) |
| 9 | Güvence | Sol dalga bloğu | Kooperatif neden devlet denetiminde |
| 10 | Saha | Lacivert panel | Dört itiraz, dört cevap |
| 11 | Hedef kitle | Üst dalga bandı | Yuvarlak fotoğraflı dört profil |
| 12 | Satış desteği | Köşe halkaları | Verilen materyaller |
| 13 | İş birliği | Sağ dalga bloğu | **doldurulacak** |
| 14 | Müşteri süreci | Koyu + sağ blok | Peşinattan tapuya |
| 15 | Kapanış | Sağ dalga bloğu | İletişim + karekod |

## İçerik kaynağı

Bütün rakamlar `src/data/` altındaki proje verisinden: daire adetleri
`units.ts`, mesafeler `location.ts`, ödeme modeli `payment.ts`, kooperatif
güvencesi `cooperative.ts`, m² projeksiyonu `valuation.ts`. Fotoğraflar
`public/images/` altındaki tam çözünürlüklü render'lardan; sunum klasörü
artık kendi kopyalarını tutmuyor.

**Fiyat yok.** Roll-up'lardaki 699.000 / 999.000 / 2.000.000 ₺ rakamları
depoda bir veri dosyasından gelmiyordu; sunuma da koymadım. 12. slayttaki
roll-up önizlemesi de bilerek **fiyatsız** sürüm. Fiyat verecekseniz satış
ekibine doğrulattıktan sonra 7. slayda ekleyin.

**Yüzme havuzu yok.** 6. slaytta avludaki suyun süs havuzu olduğu, yüzme
havuzu diye anlatılmaması gerektiği ayrıca yazıyor. `src/data/amenities.ts`
hâlâ "Kapalı Yüzme Havuzu", "Fitness Salonu", "Sauna ve Türk Hamamı"
maddelerini taşıyor ve sitede görünüyor — bunlar gerçekten yoksa sitede de
düzeltilmeli. Sunuma hiçbiri alınmadı.

**Yatırım projeksiyonu bir öngörüdür.** 8. slaytta dipnotu var; sözlü
anlatırken de "öngörü" deyin, taahhüt gibi kurmayın.

## Yeniden üretme

```
python3 scripts/build-sunum-sekil.py     # şekiller (ÖNCE bu, ~1 dk)
node    scripts/build-sunum.js           # sunum
```

Yazı tipi Calibri — her Office kurulumunda var, sunumu açan makinede
kesin bulunur.
