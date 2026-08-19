# Roll-up — beş tasarım, ölçü ve baskı föyü

Hepsi **800 × 2000 mm**, 1:1 ölçekte **100 dpi** (3150 × 7874 px).

| Dosya | Ton | Kurgu |
|---|---|---|
| `rollup-1-cam-panel` | mavi | Gece render üstünde buzlu cam panel |
| `rollup-2-kunye` | mavi | Gökyüzü üstte, bina altta, bölmeli künye şeridi |
| `rollup-3-rozet` | mavi | Cam hap rozetler + mesafe şeridi |
| `rollup-4-beyaz-plan` | beyaz | Segment hap: peşinat / vade / faiz |
| `rollup-5-beyaz-baslik` | beyaz | İki tonlu manşet + yuvarlak ikon hapları |

## Tasarım dili

Verilen beş emlak referansının ortak dili alındı:

- **Bina tek başına kahraman.** Fotoğraf ızgarası, ikon listesi, kolaj yok.
- **Cam hap rozetler** taşıyor sayıları — peşinat, vade, faiz.
- **Bölmeli bilgi şeridi:** dikey çizgiyle ayrılmış üç olgu.
- İnce tipografi, geniş harf aralığı, az renk, çok boşluk.

**Şok rozeti** beşinde de var: 699.000 ₺ peşinatla ev sahibi olun ·
banka yok · kredi yok · faiz yok.

**İki logo da kendi renginde.** MİA kilidi ve Ocean Gayrimenkul hiçbir
panoda renklendirilmiyor; koyu panolarda ikisinin de kendi beyaz sürümü
kullanılıyor, açık panolarda asıl renkleriyle duruyorlar.

## Daireler

**1+0** (28 m², 472 daire) · **1+1** (50 m², 96 daire) ·
**1+1 Bahçe Loft** (50 m², 16 daire).

2+1 Bahçe Dubleks panolarda **gösterilmiyor**. Projenin toplam 600 daire
olduğu ayrı bir olgu; tip listesinin toplamı değil.

## Bina neden bant halinde

Render'lar 4096 × 2304 (16:9). Dikey panoya tam sayfa kırpınca simetrik
ikiz blok kompozisyonu ortadan kesiliyor. Kare doğal en-boyunda bant
olarak konup **gökyüzü yukarı, zemin aşağı uzatılıyor**.

İnce şeridi doğrudan esnetmek olmuyor: 200 pikseli 4000 piksele çekince
bulutun yatay dokusu dikey çizgiye dönüşüyordu. Uzatma artık örneklenen
renkten gradyan kurup kaynağı ağır bulanıklıkla üstüne bindiriyor.

## Baskı

- **Malzeme:** 510 gr blockout branda.
- **Kaset:** 80 cm standart. Alt **40 mm** kasete girer; kritik yazı
  1950 mm'yi geçmez.
- **Güvenli alan:** yanlardan 56 mm.

## Fiyat doğrulanmalı

Depoda fiyat kaydı yok. **699.000 ₺** peşinat rakamı gönderdiğiniz
referans afişten alındı. Bastırmadan önce satış ekibine doğrulatın;
değiştirmek için tek yer `scripts/build-rollup.py` içindeki `PESIN`.

## Değiştirmek

    npm run rollup                 # beşi birden
    npm run rollup -- cam-panel    # tek tasarım
    npm run rollup -- --katman     # zemin + yazı katmanları

| Ne değişecek | Nereden |
|---|---|
| Peşinat | betikte `PESIN` |
| Şok rozeti metni | betikte `SHOCK`, `SHOCK_SUB` |
| Daire tipleri | betikte `UNITS` |
| Telefon, web, satıcı | `src/data/site.ts` |
| Ölçü, çözünürlük | betikte `W_MM`, `H_MM`, `DPI` |

Karekod hepsinde: `https://miaparkocean.com/?utm_source=rollup`
