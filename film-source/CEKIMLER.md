# Film çekimleri

`clips/` altındaki mp4'ler Higgsfield'de **projenin kendi render'larından**
üretildi. Her çekim bir render'la başlatıldı (`start_image`), böylece ekranda
görünen bina uydurma değil — mimarisi, giriş kapısı, avlusu projenin kendisi.

Model: `seedance_2_0` · 8 sn · 1080p · `mode: std` · sessiz · 16:9
Maliyet: çekim başına 72 kredi.

| Dosya | Kaynak render | Ne yapıyor |
|---|---|---|
| `01-gunduz-gece` | entrance-gate → night-gate | Gündüzden geceye time-lapse (iki uç kare) |
| `02-sokak-drone` | street-corner | Cepheye drone yaklaşımı, araçlar geçiyor |
| `03-havadan-yorunge` | aerial-pools | Avlunun üstünde kuşbakışı yörünge |
| `04-avlu-suzulme` | courtyard-pools | Avluda alçak süzülme, insanlar yürüyor |
| `05-balkon-cift` | balcony-dusk | Balkonda bir çift, akşam |
| `06-teras-sosyal` | terrace-pergola | Terasta oturan insanlar |
| `07-aksam-avlu` | hero-courtyard-dusk | Akşam avlusu, ışıklar yanıyor |
| `08-cephe-yukselis` | facade-warm | Cephe boyunca yukarı vinç hareketi |
| `09-daire-1plus0` | unit-1plus0-a | 1+0 iç mekân kaydırma |
| `10-daire-1plus1` | unit-1plus1-a | 1+1 iç mekân kaydırma |
| `11-bahce-loft` | loft-living | Loft, yukarı doğru vinç |
| `12-bahce-dubleks` | duplex-cutaway | Dubleks kesitin çevresinde yörünge |
| `13-giris-drone` | entrance-gate | Yüksekten kapıya inen drone (açılış) |
| `14-gece-yaklasim` | night-gate | Gece yaklaşma, farlar ve pencere ışıkları |

## Yeniden üretmek

Görseller `https://miaparkocean.com/images/*.webp` adresinden Higgsfield'e
`media_import_url` ile alınır (site canlı olduğu için yüklemeye gerek yok),
sonra `generate_video_batch` ile `start_image` rolüyle üretilir.

Yeni çekim eklerken `scripts/build-film.py` içindeki `TIMELINE`'a satır ekleyin;
kare önbelleği (`.kare-onbellek/`) ilk çalıştırmada kendiliğinden dolar.
