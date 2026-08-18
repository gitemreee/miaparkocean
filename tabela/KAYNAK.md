# Baskı kaynak dosyaları — onay sonrası değişiklik

Tasarımlar onaylandıktan sonra üzerinde oynanabilsin diye her tasarım
**iki katmana ayrılmış** olarak veriliyor.

    kaynak/<ad>-zemin.jpg   fotoğraf, gradyan, logo, karekod — YAZI YOK
    kaynak/<ad>-yazi.png    yalnızca tipografi, saydam zeminde
    kaynak/yazi-tipleri/    Fraunces ve Manrope (kullanılan yazı tipleri)

İkisi üst üste konunca onaylanan tasarımın **birebir aynısı** çıkar.
Kontrol edildi: sapma 2/255, yani yalnızca yuvarlama.

## Photoshop / Illustrator ile değiştirmek

1. `<ad>-zemin.jpg` dosyasını açın — alt katman bu.
2. `<ad>-yazi.png` dosyasını üstüne sürükleyin, **Normal** karışım,
   %100 opaklık. Hizalama gerekmez; iki dosya aynı ölçüdedir.
3. Değiştirmek istediğiniz yazıyı yazı katmanında silin (silgi ya da
   seçim + delete), yerine yenisini yazın.
4. Yazı tipleri `yazi-tipleri/` klasöründe. İkisi de açık lisanslı,
   kurup kullanabilirsiniz:
   - **Fraunces** — başlıklar (600 ve 700 ağırlık)
   - **Manrope** — alt başlıklar, telefon, künye (400/600/700)
5. Renkler:

   | | |
   |---|---|
   | Koyu lacivert | `#04283A` |
   | MİA derin mavi | `#095678` |
   | MİA okyanus | `#2C94B4` |
   | MİA buz | `#DDF7FA` |
   | Beyaz | `#FFFFFF` |

Zemine dokunmanız gerekmez — logo, karekod ve fotoğraf orada durur.

## Daha temizi: veriyi düzeltip yeniden üretmek

Tasarımların **asıl kaynağı `scripts/build-signage.py`** dosyasıdır.
Ölçüler milimetre cinsinden yazılıdır; katmanlı dosyalar da bu betikten
çıkar. Şu değişiklikler için Photoshop'a hiç girmeye gerek yok:

| Ne değişecek | Nereden | Sonra |
|---|---|---|
| Telefon, web adresi, satıcı adı | `src/data/site.ts` | `npm run tabela` |
| Daire adedi, m², tip adları | `src/data/units.ts` | `npm run tabela` |
| Mesafeler | `src/data/location.ts` | `npm run tabela` |
| Ortak alanlar | `src/data/amenities.ts` | `npm run tabela` |
| Yaka kartındaki isim | betikte `BADGE_FIRST` / `BADGE_LAST` | `npm run tabela` |
| Bilbord cümleleri | betikte `PAIRS` listesi | `npm run tabela` |
| Ölçü ya da çözünürlük | betikte `RU_*`, `BB_*`, `YK_*` | `npm run tabela` |

Bu yol daha güvenli: rakam bir yerde değişince bütün tabelalarda birden
değişir, biri eski kalmaz.

Katmanlı dosyaları yeniden üretmek:

    npm run tabela -- --katman

## Kapsam

Katmanlı kaynak **bütün tasarımlar** için üretilir: totem (2), şantiye
çevre afişi (5), roll-up (6), bilbord (20), yaka kartı (10) — toplam 43
tasarım, 86 dosya.

## Sınırlar

- **Logo ve karekod zeminde kalır.** İkisi de yazı değil, görsel olarak
  yerleştiriliyor. Yerlerini değiştirmek isterseniz betikten yapmak
  gerekir; Photoshop'ta zeminin üstünü kapatmanız icap eder.
- **Yazı katmanı gerçek metin değil, piksel.** Harfleri yeniden
  yazabilirsiniz ama mevcut yazıyı "seçip düzenlemek" mümkün değil.
  Canlı metin isterseniz betikten üretmek tek yol.
- Fotoğrafların tamamı mimari render'dır; ticari kullanım hakları
  projeye aittir.
