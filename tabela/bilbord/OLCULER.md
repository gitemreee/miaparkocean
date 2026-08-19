# Bilbord — beş tasarım

Hepsi **5000 × 3000 mm**, 1:1 ölçekte **40 dpi** (7874 × 4724 px).
Roll-up serisinin yatay karşılığı; aynı tasarım sistemi.

| Dosya | Yazı tipi | Render |
|---|---|---|
| `bilbord-1-gece` | Playfair Display | night-gate |
| `bilbord-2-oswald` | Oswald (sıkışık grotesk) | entrance-gate |
| `bilbord-3-beyaz` | Cormorant Garamond | entrance-gate, açık |
| `bilbord-4-klasik` | Marcellus | aerial-pools |
| `bilbord-5-modern` | Montserrat | courtyard-pools |

## Kurgu

Yazı **hep sol yarıda**, render tam sayfa. Sol tarafta yatay perde var;
sağ yarı net kalıyor ki bina görünsün. Üç yuvarlak fotoğraf sağda
**dikey sütun** halinde — yatay panoda satır olarak dizilince manşetin
altını kaplayıp okunurluğu düşürüyordu.

Ortak parçalar: iki logo, dev manşet, daire kutuları, dikey çizgiyle
ayrılmış üç olgu, üç yuvarlak fotoğraf, şok mührü, künye şeridi.

## Okunurluk

Bilbord 30-100 m'den okunur. Manşet **300 mm**, olgu değerleri
**165 mm**, künye web **120 mm** punto. Roll-up'taki küçük satırlar
(uzun açıklama, satıcı alt künyesi) buraya **alınmadı** — o mesafeden
okunmaz, yalnızca kalabalık eder.

## Render kırpması

Render'lar 4096 × 2304. 5:3'lük panoya tam sayfa girerken yanlardan
yalnızca **%6** kırpılıyor. Roll-up'ta gereken gökyüzü uzatması burada
gerekmiyor.

## Daireler

**1+0** · **1+1** · **1+1 Bahçe Loft**. 2+1 Bahçe Dubleks yok.

## Baskı

- **Malzeme:** 440 gr çift taraflı bilbord brandası, mat.
- **Kesim payı:** her kenardan 50 mm; dosya tam ölçüdür, pay eklenecekse
  betikte `W_MM`/`H_MM` büyütülüp yeniden üretilir.
- **Güvenli alan:** kenarlardan 190 mm. Kritik yazı bu payın içinde.
- **Çözünürlük:** 40 dpi 1:1 — büyük format baskıda standart.

## Fiyat doğrulanmalı

**699.000 ₺** gönderdiğiniz referans afişten alındı; depoda fiyat kaydı
yok. Bastırmadan önce doğrulatın. Tek değiştirme noktası
`scripts/build-rollup.py` içindeki `PESIN` — bilbord betiği oradan
okuyor, ikisi birden değişiyor.

## Değiştirmek

    npm run bilbord                # beşi birden
    npm run bilbord -- gece        # tek tasarım

Karekod: `https://miaparkocean.com/?utm_source=bilbord`
(roll-up'ınki `?utm_source=rollup` — hangisinden geldiği analitikte ayrışır)

## 6 · Ödeme panosu

`bilbord-6-odeme` üç fiyat kartını yan yana verir (1+0 · 1+1 · 2+1).
Yatay panoda kart başına 1500 mm düşüyor, rakamlar rahat okunuyor.

| Tip | Peşinat | Aylık | Vade |
|---|---|---|---|
| 1+0 | 699.000 ₺ | 29.900 ₺ | 60 ay, vade farksız |
| 1+1 | 999.000 ₺ | 39.900 ₺ | 60 ay, vade farksız |
| 2+1 | 2.000.000 ₺ | 50.000 ₺ | 60 ay, vade farksız |

**2+1 yalnızca bu panoda var.**
