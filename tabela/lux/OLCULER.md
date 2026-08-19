# Roll-up — ölçü ve baskı föyü

Dört tasarım, iki renk düzeni, sekiz dosya. Hepsi **800 × 2000 mm**,
1:1 ölçekte **100 dpi** (3150 × 7874 px).

| Dosya | Yapı | Konu |
|---|---|---|
| `rollup-1-cephe-*` | Üstte sert kenarlı mimari blok, altta yazı | Lüks artık ulaşılabilir |
| `rollup-2-altmis-*` | Dev rakam; fotoğraf yalnızca alt bant | 60 ay vade, %0 faiz |
| `rollup-3-odeme-*` | Editoryal fiyat tablosu, altta tam boy fotoğraf | Peşinat ve taksit |
| `rollup-4-daireler-*` | 2×2 fotoğraf ızgarası | Dört yaşam tipi |

Renk düzenleri — ikisi **ölçü ölçü aynıdır**, yalnızca renk sözlüğü değişir:

- **`-ALTIN`** — gece laciverti zemin, altın vurgu.
- **`-MIA`** — markanın kendi paleti: okyanus mavisi zemin, buz mavisi vurgu.

## Tasarım kuralları

Dördünün de **yapısı farklı**. Aynı iskeletin dört hali değil: biri
fotoğrafla, biri rakamla, biri tabloyla, biri ızgarayla kuruluyor.

- **Tek sol pay.** Her şey 62 mm'den başlar. Ortalanmış yığın şablon
  hissi veriyordu.
- **Ölçek farkı.** Manşet ~90 mm, ara başlık ~16 mm, künye ~9 mm. On kata
  varan fark; hepsi orta boy olunca hiyerarşi okunmuyor.
- **Altın az kullanılır.** Saç teli çizgi, küçük etiket ve tek bir rakam.
  Manşet sıcak beyaz. Her yere altın sürülünce lüks değil ucuz duruyor.

## Baskı

- **Malzeme:** 510 gr blockout branda. Roll-up kasetinde arkadan ışık
  geçmesin diye blockout tercih edilir.
- **Kaset:** 80 cm standart. Alt kasete giren **son 40 mm** gizlenir;
  kritik yazı 1950 mm'yi geçmez.
- **Güvenli alan:** yanlardan 62 mm. Kesim payı yok, dosya tam ölçüdür.
- **Fotoğraf çözünürlüğü:** `rollup-1` cephe karesi 2,9 kat, diğerleri
  1,9–2,0 kat büyütülüyor. Tam sayfa cephe denendi ama 4,9 kat büyütme
  gerekiyordu, baskıda dağılıyordu — blok o yüzden 1180 mm.

## Rakamlar

| Ne | Kaynak |
|---|---|
| Daire adetleri (472 · 96 · 16 · 16 = 600) | `src/data/units.ts` |
| m² değerleri | `src/data/units.ts` |
| 60 ay vade, %0 faiz | `src/data/payment.ts` |
| Telefon, web, satıcı | `src/data/site.ts` |
| **Fiyatlar** | **betikteki `PRICES` — doğrulatın** |

### Fiyatlar doğrulanmalı

Depoda fiyat kaydı yok. `rollup-3-odeme` üzerindeki rakamlar
**gönderdiğiniz referans afişten** alındı:

    1+0   28 m²   peşinat 699.000 ₺   aylık 29.900 ₺
    1+1   50 m²   peşinat 999.000 ₺   aylık 39.900 ₺

Bastırmadan önce satış ekibine doğrulatın. Değiştirmek için tek yer
`scripts/build-lux.py` içindeki `PRICES` listesi.

## Değiştirmek

    npm run lux                 # sekizi birden
    npm run lux -- cephe        # yalnız bir tasarım
    npm run lux -- --katman     # zemin + yazı katmanları

| Ne değişecek | Nereden |
|---|---|
| Fiyatlar | betikte `PRICES` |
| Renk düzeni | betikte `ALTIN` / `MIA` |
| Sol pay, künye yeri | betikte `M`, `FOOT` |
| Ölçü, çözünürlük | betikte `RU_W`, `RU_H`, `RU_DPI` |
| Telefon, web, satıcı | `src/data/site.ts` |
| Daire adedi, m² | `src/data/units.ts` |

## Karekod

Hepsinde aynı: `https://miaparkocean.com/?utm_source=rollup`
