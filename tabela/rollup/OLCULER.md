# Roll-up — beş tasarım

Hepsi **800 × 2000 mm**, 1:1 ölçekte **100 dpi** (3150 × 7874 px).

| Dosya | Yazı tipi | Zemin |
|---|---|---|
| `rollup-1-gece` | Playfair Display | gece · night-gate |
| `rollup-2-oswald` | Oswald (sıkışık grotesk) | gündüz · entrance-gate |
| `rollup-3-beyaz` | Cormorant Garamond | sıcak beyaz · facade-warm |
| `rollup-4-klasik` | Marcellus (roman kapital) | gece · aerial-pools |
| `rollup-5-modern` | Montserrat (geometrik) | akşam · courtyard-pools |

Beşinin de ortak parçaları: iki logo üstte, daire kutuları, dikey
çizgiyle ayrılmış üç olgu, mesafe yayı, şok mührü, künye şeridi.

## Tipografi kütüphanesi

Önceki sürümlerde elde yalnızca **iki** yazı tipi vardı (Fraunces,
Manrope) ve yapılan her tasarım birbirinin aynısı çıkıyordu. Kütüphane
genişletildi — hepsi açık lisanslı, Türkçe karakterleri tam:

| Yazı tipi | Rol |
|---|---|
| Oswald 200-700 | sıkışık grotesk — vurucu manşet |
| Playfair Display 400-900 | display serif — proje adı |
| Cormorant Garamond 300-700 | ince zarif serif |
| Montserrat 100-900 | geometrik sans — veri |
| Barlow Condensed 500/700 | sıkışık sans — etiket |
| Marcellus | rafine roman kapital |
| Dancing Script 400-700 | el yazısı vurgu |

Değişken eksenli fontlar ağırlık parametresiyle örnekleniyor. PIL font
nesnesini yerinde değiştirdiği için her (dosya, punto, ağırlık) üçlüsü
ayrı önbellekleniyor — aksi halde son ayarlanan ağırlık hepsine sızıyor.

**₺ simgesi Playfair, Jost ve Marcellus'ta YOK.** Rakam bu yazı
tipleriyle, simge Montserrat'la basılıyor; yoksa kutu çıkıyor.

## Derinlik

Referanslardaki "tasarlanmış" his düz dikdörtgenden gelmiyor:

- **Işık halesi** binanın arkasında — düz zeminle render arasındaki
  geçişi yumuşatıyor.
- **Yumuşak bant kenarı** — sert dikdörtgen kenar "yapıştırılmış"
  duruyordu; alfası yumuşatılınca bina zeminden çıkıyormuş gibi oturuyor.
- **Vinyet** kenarlarda, göz merkeze toplanıyor.
- **Gölge** şok mührünün altında.

## Daireler

**1+0** · **1+1** · **1+1 Bahçe Loft**. 2+1 Bahçe Dubleks gösterilmiyor.

## Baskı

- **Malzeme:** 510 gr blockout branda.
- **Kaset:** 80 cm standart; alt 40 mm kasete girer, kritik yazı 1950 mm'yi
  geçmez.
- **Güvenli alan:** yanlardan 58 mm.

## Fiyat doğrulanmalı

Depoda fiyat kaydı yok. **699.000 ₺** gönderdiğiniz referans afişten
alındı. Bastırmadan önce doğrulatın; tek değiştirme noktası betikteki
`PESIN`.

## Değiştirmek

    npm run rollup

| Ne | Nereden |
|---|---|
| Peşinat | betikte `PESIN` |
| Daire tipleri | betikte `UNITS` |
| Telefon, web, satıcı | `src/data/site.ts` |
| Ölçü, çözünürlük | betikte `W_MM`, `H_MM`, `DPI` |
