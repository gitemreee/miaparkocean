# MİA PARK OCEAN — Bilbord serisi · Ölçü ve baskı föyü

Şehir içine, projeden uzağa asılan panolar. Aynı sekiz tasarımın arsa
karşılığı `tabela/arsa-mia/` altında; **görseller aynı, bantlar farklı.**

| Bilbord (bu klasör) | Arsa (`arsa-mia/`) |
|---|---|
| Üst bantta **İZMİT MİA BÖLGESİ** | Üst bantta **PROJE ALANI** |
| Alt bantta **iri telefon numaraları** | Alt bantta **karekod** |
| Karekod yok — araçtan okunmaz | Karekod var — yayadan okunur |
| 5000 × 3000 mm, 40 dpi | 3000 × 2000 mm, 50 dpi |

Bilbord şehrin başka yerinde durur; oradan geçen projenin nerede olduğunu
bilmez, o yüzden konum yazar. Arsa panosunun önünden geçen zaten yerinde
durur, orada gereken şey arsanın kime ait olduğudur.

## Dosyalar

| # | Dosya | Kurgu |
|---|---|---|
| 1 | `bilbord-1-mozaik.jpg` | Mozaik ızgara — altı farklı boy fotoğraf karosu, yazı yalnızca tek renkli blokta |
| 2 | `bilbord-2-kemer.jpg` | Üç kemer pencere — fotoğraf sadece kemerlerin içinde |
| 3 | `bilbord-3-tipografik.jpg` | Saf tipografi — %0 faiz · 60 ay vade, fotoğraf dipnot boyunda |
| 4 | `bilbord-4-diyagonal.jpg` | Eğik üst üste düşmüş katmanlar — düşük peşinatla ev sahibi olun |
| 5 | `bilbord-5-duotone.jpg` | İki renkli duotone zemin, içinde renkli kesit pencere |
| 6 | `bilbord-6-sutunlu.jpg` | Beş dikey sütun — evinizi şimdiden görün |
| 7 | `bilbord-7-veri.jpg` | Veri panosu — 600 konut · 60 ay · 4 daire tipi · %0 faiz |
| 8 | `bilbord-8-siluet.jpg` | Kesim siluet, dev daire içinde — kahvemizi içmeye bekleriz |

**Sekiz panonun sekizi ayrı kurgu.** Hiçbiri "fotoğrafın üstüne yazı"
değil: mozaik ızgara, kemer pencereler, saf tipografi, eğik katmanlar,
duotone üstünde renkli kesit, beş sütun, veri blokları, kesim siluet.
Üçünde fotoğraf ya dipnot boyunda ya da hiç yok.

**Havuz.** Panolarda "yüzme havuzu" ibaresi YOK. Render'lardaki su
**süs havuzu**; depodaki tabela sözlüğü de (`AMENITIES`) böyle diyor.
`src/data/amenities.ts` hâlâ "Kapalı Yüzme Havuzu" maddesi taşıyor —
proje gerçekten böyle bir havuz içermiyorsa sitedeki o madde de
düzeltilmeli, yoksa site panoyla çelişir.

`onizleme/` altında 1/6 ölçekli kontrol kopyaları var.

## Baskı

- **Ölçü:** 5000 × 3000 mm
- **Dosya:** 7874 × 4724 px, 1:1 ölçekte 40 dpi, JPEG kalite 92,
  altörnekleme kapalı (4:4:4), dpi gömülü
- **Renk:** sRGB. CMYK dönüşümünü matbaa kendi profiliyle yapsın.
- **Taşma payı:** dosyada yok. Gergi için her kenardan 30 mm ekleyin;
  kritik öğeler kenardan en az 125 mm içeride.
- Bilbord 30–100 m'den okunur. Telefonlar alt bantta bilerek iri; karekod
  yok, çünkü seyir hâlindeki araçtan okutulamaz.

## Tasarım sistemi

- Üstte ve altta düz bir bant; **bandı panodan iki çizgi ayırıyor**
  (kalın bir kural, altında ince bir kural). Dalga yok.
- **Bant rengi her tasarımın kendi paletinden ölçülüyor**: lacivert,
  antrasit, bronz, orman yeşili ve petrol mavisi panolar var — set tek
  tip mavi değil.
- Logo yapay zekâya çizdirilmiyor: üretimde iki bant boş bırakılıp
  gerçek MİA PARK OCEAN kilidi ve OCEAN GAYRİMENKUL imzası betikle
  basılıyor.
- Alt bandın ortasında sabit: **GÖRSELLER TEMSİLİDİR**.

## İçerik

**Fiyat yok.** Ödeme mesajı vade ve finansman modeliyle sınırlı: %0 faiz,
60 ay vade farksız taksit, kredi/faiz/kefil yok, düşük peşinat. Rakam
soran arıyor ya da karekodu okutuyor. Daire m² değerleri depodaki proje
verisinden geliyor.

## Yeniden üretim

```
npm run panolar
```

Tasarımlar Higgsfield (nano_banana_pro, 3:2, 4K) ile üretiliyor; istemler
`PROMPT.md`'de, ham PNG'ler `signage-source/hf-mia/` altında (git'e
girmiyor). Bantları ve logoları `scripts/build-mia-panolar.py` basıyor.
