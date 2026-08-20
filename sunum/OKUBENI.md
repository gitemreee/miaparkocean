# MİA PARK OCEAN — Emlakçı / broker sunumu

- `MIA-PARK-OCEAN-Emlakci-Sunumu.pptx` — 25 slayt, 16:9, konuşmacı notlu
- `MIA-PARK-OCEAN-Emlakci-Sunumu.pdf` — aynı sunumun PDF hâli
- `onizleme/slide-01…25.jpg` — slayt slayt önizleme
- `yazitipi/` — sunumun yazı tipi (**kurulması gerekiyor**, aşağıda)

## AÇMADAN ÖNCE: yazı tipini kurun

Sunumun tamamı **Montserrat** ile dizildi; Office ile gelmez.
`yazitipi/` klasöründeki `Montserrat-*.ttf` dosyalarını seçip sağ tık →
**Yükle** deyin (Mac'te çift tıklayıp "Yazı Tipini Yükle"). Kurmazsanız
PowerPoint başka bir yazı tipine düşer ve sunum farklı görünür.

**Kurulum yapamayacağınız makinede PDF'i kullanın** — yazı tipleri
gömülü, her yerde aynı görünür.

## Sunum ne yapıyor

Konut kataloğu değil, **B2B satış sunumu**: *bu projeyi neden portföyüme
almalıyım, müşteriye nasıl anlatırım?* Üç satış ekseni: **konum** (MİA
Bölgesi) · **ürün** (kompakt stok) · **ödeme** (faizsiz model).

## Akış (25 slayt)

| # | Slayt | Düzen |
|---|---|---|
| 1 | Kapak | Elmas fotoğraf kümesi |
| 2 | Gündem | Yarım fotoğraf + 8 elmas numaralı başlık |
| 3 | Proje özeti | Dört büyük rakam + elmas fotoğraf |
| 4 | Emlakçı için neden önemli | İkon satırları + elmas fotoğraf |
| 5 | Konum | Yarım fotoğraf + 8 mesafe listesi |
| 6 | MİA nedir | Lacivert panel + 01-03 numaralı |
| 7 | Stratejik avantaj | İki blok + kesik çizgili ulaşım aksı |
| 8 | Mimari | Tam kanama render |
| 9 | Site içinde yaşam | Madde listesi + iki fotoğraf + süs havuzu uyarısı |
| 10 | Ürün dağılımı | İki büyük blok: 472 · 112 |
| 11 | 1+0 detay | Yarım fotoğraf + 4 madde |
| 12 | 1+1 detay | Aynanın simetriği |
| 13 | Müşteri profilleri | 5 satır + elmas fotoğraf |
| 14 | Ödeme modeli | %30 · 60 AY · "banka yok" bandı |
| 15 | Fiyat örnekleri | İki lacivert kart + dönemsellik dipnotu |
| 16 | Müşteri süreci | 4 elmas adım + kesik çizgi |
| 17 | 60 saniyelik anlatım | 5 alıntı satırı (koyu) |
| 18 | İtiraz yönetimi | 4 soru / cevap |
| 19 | Güven | Lacivert panel + kurum listesi + logo bandı |
| 20 | İş birliği süreci | 5 elmas adım + **doldurulacak form** |
| 21 | Satış destek materyalleri | Liste + gerçek materyal önizlemeleri |
| 22 | Galeri | Dergi ızgarası, altı render |
| 23 | Rakamlarla proje | Altı büyük rakam (koyu) |
| 24 | Neden MİA PARK OCEAN | Altı madde + kapanış bandı |
| 25 | Kapanış / iletişim | Elmas küme + iletişim + CTA |

## Tasarım dili (elmas)

Referans şablonun dili birebir: **elmas (45° kare) içine kırpılmış
fotoğraflar**, ince elmas çerçeveler, elmas numara rozetleri, kesik
çizgiyle bağlanan adım diyagramları, köşe elmas süsleri. Renkler bizim:

| | |
|---|---|
| Gece lacivert | `#06192B` |
| Lacivert blok | `#0E2E46` |
| Sıcak krem | `#F3EDE3` |
| Champagne gold | `#C9A961` |

Elmaslar ve çizgiler PowerPoint'in KENDİ vektör şekilleri (45° döndürülmüş
kare) — keskin ve düzenlenebilir. Yalnızca fotoğraf maskeleri, perdeler,
ikonlar ve materyal önizlemeleri PIL'den geliyor
(`scripts/build-sunum-gorsel.py` → `kaynak/foto/`, `kaynak/sekil/`).

## Görsel kuralları

- Yalnızca projenin kendi render'ları (`public/images/`); stok yok, AI
  mimari yok.
- Her fotoğraf yerleşeceği kutunun tam pikseline kırpılıyor — PowerPoint'te
  **gerdirme yok**. Materyal önizlemeleri oran korunarak (contain) oturuyor.
- **Yüzme havuzu algısı yaratılmıyor.** Sudaki öğeler süs havuzu / su aksı;
  9. slaytta yazılı uyarı var, konuşmacı notlarında tekrarlanıyor.
  (`src/data/amenities.ts` hâlâ "Kapalı Yüzme Havuzu, Fitness, Sauna"
  taşıyor ve sitede görünüyor — gerçekten yoksa sitede de düzeltilmeli.)

## Denetim

```
npm run sunum:denetim
```

- `scripts/sunum-tasma.py` — her metin kendi kutusuna sığıyor mu
  (gerçek Montserrat metrikleriyle ölçer)
- `scripts/sunum-cakisma.py` — kutusuna sığan ama komşusunun/çizginin
  üstüne binen metinler ve slayt dışına taşanlar

Bu sunumda ikinci denetim 14 çakışma yakaladı (etiket kutuları yandaki
açıklamanın altına uzanıyordu); düzeltildi, ikisi de temiz.

## Sunum öncesi kontrol

- **20. slayttaki üç alan bilerek boş:** komisyon oranı, hakediş zamanı,
  müşteri koruma süresi. Bu rakamlar depoda yok; sunumdan önce doldurun.
- **Fiyatlar dönemseldir** — 15. slaytta dipnot var, sözlü de söyleyin.
- **Değer artışı taahhüdü vermeyin** — 6. slayt "potansiyel" der.
- **Yasal/finansal garanti vermeyin** — 18-19. slaytlar bilgilendirmedir.
- **2+1 anlatılmıyor** — ürün slaytları yalnızca 1+0 ve 1+1.

## Yeniden üretme

```
python3 scripts/build-sunum-gorsel.py     # görseller (ÖNCE)
node    scripts/build-sunum.js            # sunum
```

veya `npm run sunum`.
