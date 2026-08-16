# İç mekân ve ortak alan görselleri

20 görsel · 1920 px genişlik · WebP (+ `-sm` yarı boy varyantları)

Higgsfield `nano_banana_pro` ile üretildi. Her biri projenin **kendi
render'ı referans alınarak** yapıldı, böylece malzeme paleti tutuyor:
travertan, sıcak meşe, beyaz mermer, fırçalanmış metal.

## Kapsam

Yalnızca `src/data/amenities.ts` ve `src/data/units.ts` içinde **belgelenmiş**
özellikler görselleştirildi. Kapalı havuz, spor salonu gibi projede
tanımlı olmayan donatılar bilerek üretilmedi.

| Dosya | Ne | Dayanağı |
|---|---|---|
| `01-1plus0-salon` | 1+0 açık plan salon | units.ts · 28 m², 472 daire |
| `02-1plus0-mutfak` | 1+0 mutfak detayı | units.ts · "modern mutfak tasarımı" |
| `03-1plus0-balkon` | Balkondan dışarı | units.ts · "geniş balkon" |
| `04-1plus0-banyo` | Kompakt banyo | — |
| `05-1plus1-salon` | 1+1 salon | units.ts · 50 m², 96 daire |
| `06-1plus1-yatak-odasi` | 1+1 yatak odası | units.ts · "yatak odası ayrı" |
| `07-1plus1-mutfak` | 1+1 açık mutfak | units.ts · "açık mutfak" |
| `08-1plus1-banyo` | Küvetli banyo | — |
| `09-loft-salon` | Çift yükseklik loft | units.ts · 1+1 Bahçe Loft |
| `10-loft-mezanin` | Loft mezanin katı | units.ts · 1+1 Bahçe Loft |
| `11-dubleks-salon` | 2+1 dubleks alt kat | units.ts · 100 m², 16 daire |
| `12-dubleks-yatak-odasi` | 2+1 üst kat | units.ts · 2+1 Bahçe Dubleks |
| `13-bahceli-daire-terasi` | Zemin kat bahçe terası | amenities · "bahçeli zemin daireler" |
| `14-dubleks-bahcesi` | Dubleksin özel bahçesi | amenities · "bahçeli zemin daireler" |
| `15-balkondan-avlu` | Balkondan avlu manzarası | amenities · "merkezi avlu" |
| `16-giris-holu` | Bina giriş holü | — |
| `17-sus-havuzu` | Süs havuzu detayı | amenities · "dekoratif süs havuzları" |
| `18-yuruyus-yolu` | Peyzaj ve yürüyüş yolu | amenities · "yürüyüş ve dinlenme yolları" |
| `19-cocuk-oyun-parki` | Çocuk oyun parkı | amenities · "çocuk oyun parkı" |
| `20-kapali-otopark` | Kapalı otopark | amenities · "kapalı otopark" |

`04`, `08` ve `16` için amenities.ts'te doğrudan bir madde yok; banyo ve
giriş holü her konut projesinde bulunan mimari verili alanlar olduğu için
eklendi, pazarlama iddiası taşımıyorlar.

## Not

Bunlar üretilmiş görsellerdir, fotoğraf değildir. Satış malzemesinde
kullanırken projenin resmî render'larıyla birlikte, temsilî olduğu
anlaşılacak şekilde kullanın.
