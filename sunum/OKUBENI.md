# MİA PARK OCEAN — Emlakçı / broker sunumu

- `MIA-PARK-OCEAN-Emlakci-Sunumu.pptx` — 17 slayt, 16:9, konuşmacı notlu
- `MIA-PARK-OCEAN-Emlakci-Sunumu.pdf` — aynı sunumun PDF hâli
- `onizleme/slide-01…17.jpg` — slayt slayt önizleme
- `yazitipi/` — sunumun yazı tipleri (aşağıya bakın, **kurulması gerekiyor**)

## AÇMADAN ÖNCE: yazı tiplerini kurun

Sunum **Playfair Display** (başlık) ve **Montserrat** (alt metin)
kullanıyor. İkisi de Office ile gelmez. `yazitipi/` klasöründeki 10 dosyayı
seçip sağ tık → **Yükle** deyin (Mac'te çift tıklayıp "Yazı Tipini Yükle").
Otuz saniyelik iş; kurmazsanız PowerPoint başka bir yazı tipine düşer ve
sunum bambaşka görünür.

**Kurulum yapamayacağınız bir makinede sunacaksanız PDF'i kullanın** —
PDF'te yazı tipleri gömülü, her yerde aynı görünür.

## Sunum ne yapıyor

Bu bir konut kataloğu değil, **B2B satış sunumu**. Emlakçının kafasındaki
soruya cevap veriyor: *bu projeyi neden portföyüme almalıyım, müşteriye
nasıl anlatırım?* Üç satış ekseni üzerine kurulu:

1. **Konum** — İzmit'in gelişen MİA bölgesi
2. **Ürün** — yatırımcıya uygun kompakt daire stoğu
3. **Ödeme** — tasarrufa dayalı faizsiz finansman

## Akış

| # | Slayt | Düzen | Ne yapıyor |
|---|---|---|---|
| 1 | Kapak | Tam kanama render | Marka, bölge, "yeni satış fırsatı" |
| 2 | 30 saniyede proje | %60 metin + %40 görsel | Dört büyük rakam |
| 3 | Emlakçı için neden önemli | Dört sütun | Satılabilirlik argümanı |
| 4 | Konum | İnfografik | Sekiz mesafe, ışın uzunluğu süreyle orantılı |
| 5 | MİA nedir | %60 metin + %40 görsel | Merkezi İş Alanı kavramı |
| 6 | Stratejik avantaj | İki blok + ulaşım aksı | İzmit ve İstanbul yatırımcısı |
| 7 | Mimari | Tam kanama render | Premium katalog sayfası |
| 8 | Ürün dağılımı | İki büyük blok | 472 adet 1+0 · 112 adet 1+1 |
| 9 | Müşteri profilleri | Beş satır | Kime satılır |
| 10 | Ödeme modeli | Büyük rakam | %30 peşinat · 60 ay vade farksız |
| 11 | Fiyat örneği | İki kart | Peşinat ve aylık |
| 12 | Satış argümanı | Şerit + beş cümle | 60 saniyelik anlatım |
| 13 | İtiraz yönetimi | Soru / cevap | Dört itiraz |
| 14 | Güven ve şeffaflık | %60 metin + %40 görsel | Kooperatif, KOOPBİS, kanun |
| 15 | Galeri | Dergi ızgarası | Altı render, başlıksız |
| 16 | Özet | Altı madde + bant | "Doğru konum, doğru ürün" |
| 17 | Kapanış | Tam kanama render | İletişim + çağrı |

Ritim bilinçli: aynı düzen arka arkaya gelmiyor. Tam kanama render → metin
ağırlıklı → büyük rakam → infografik → dergi ızgarası.

## Tasarım dili

| | |
|---|---|
| Gece mavisi | `#06192B` |
| Lacivert blok | `#0E2E46` |
| Sıcak krem | `#F3EDE3` |
| Krem ayraç | `#E6DCCB` |
| Champagne gold | `#C9A961` |
| Açık altın | `#E0CB9C` |

Tek dekoratif öğe **ince altın çizgi**. Gölgeli kart, 3B ikon, dekoratif
grafik yok. Kenar boşluğu bütün slaytlarda aynı (`M = 0.95"`), yani tek
ızgara.

## Görseller

Yalnızca MİA PARK OCEAN'ın kendi render'ları (`public/images/`). Stok
görsel, başka proje, AI mimari yok.

**Her fotoğraf yerleşeceği kutunun tam pikseline kırpılmış olarak
üretiliyor** (`scripts/build-sunum-gorsel.py` → `kaynak/foto/`), yani
PowerPoint'te hiçbir görsel gerdirilmiyor. Mimari okunabilir kalsın diye
yakınlaştırma bilerek düşük; 7. slayt (mimari) hiç kırpılmadan tam
kanama 16:9 kullanıyor.

**Yüzme havuzu yok.** Sudaki öğeler peyzaj amaçlı süs havuzu ve su aksı.
7. slaytta bu ayrıca yazıyor, konuşmacı notunda uyarı var, galeriye
projenin kendi süs havuzu render'ı kondu. `src/data/amenities.ts` hâlâ
"Kapalı Yüzme Havuzu", "Fitness Salonu", "Sauna ve Türk Hamamı"
maddelerini taşıyor ve sitede görünüyor — gerçekten yoksa sitede de
düzeltilmeli.

## İnfografikler

4. slayttaki konum diyagramının ve 6. slayttaki ulaşım aksının
**geometrisi** PIL'de üretiliyor, **yazıları** gerçek metin kutusu olarak
konuyor (`kaynak/info.json` etiket çapalarını taşıyor). Böylece yazılar
PowerPoint'te düzenlenebilir ve keskin kalıyor.

Konum diyagramında ışın uzunluğu süreyle orantılı: göz otomatik olarak en
yakın hedefleri görüyor, diyagram süs değil bilgi taşıyor.

## Denetim

Dalgalı/blok zeminlerde yerleşim gözle değil ölçüyle kuruldu:

```
python3 scripts/sunum-tasma.py   sunum/MIA-PARK-OCEAN-Emlakci-Sunumu.pptx
python3 scripts/sunum-cakisma.py sunum/MIA-PARK-OCEAN-Emlakci-Sunumu.pptx
```

- **tasma** — her metin kutusunun kendi kutusuna sığıp sığmadığı
- **cakisma** — kutusuna sığan ama komşusunun ya da altın çizginin üstüne
  binen metinler, ve slayt dışına taşanlar

İkinci denetim bu sunumda 10 gerçek hata yakaladı (konum etiketlerinin
noktaların üstüne binmesi, aks etiketlerinin çakışması, 14. slaytta
dipnotun slayt dışına çıkması). Yeniden düzenledikten sonra ikisi de temiz.

## Sunum öncesi kontrol

- **Fiyatlar dönemseldir.** 11. slaytta dipnot var; sözlü anlatırken de
  söyleyin. Yazılı teklif satış ofisinden çıkar.
- **Değer artışı taahhüdü vermeyin.** 5. slayt "potansiyel" diyor,
  "kesin artış" demiyor. Sözlü anlatımda da böyle kalsın.
- **Yasal / finansal garanti vermeyin.** 13. ve 14. slaytlar bilgilendirme
  amaçlı; belgeler satış ofisinden talep edilebilir.
- **2+1 anlatılmıyor.** 8. slayt yalnızca 1+0 ve 1+1 gösteriyor.

## Yeniden üretme

```
python3 scripts/build-sunum-gorsel.py     # fotoğraf/perde/infografik (ÖNCE)
node    scripts/build-sunum.js            # sunum
```

veya `npm run sunum`.
