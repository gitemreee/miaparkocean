# Bilbord + arsa panosu serisi — Higgsfield istemleri

Sekiz tasarım **nano_banana_pro** ile üretiliyor, ikisi de aynı kaynaktan
çıkıyor. Bantları ve logoları `scripts/build-mia-panolar.py` basıyor.

| | |
|---|---|
| model | `nano_banana_pro` |
| aspect_ratio | `3:2` (arsa oranı; bilbord 5:3'e yükseklikten kırpılıyor) |
| resolution | `4k` → 5056 × 3392 px |
| medias | rol `image`, `signage-source/` ve `public/images/ic-mekan/` render'ları |

Ham PNG'ler `signage-source/hf-mia/` altına `mia-1-sosyal-yuvarlak` …
`mia-8-daire-tipleri` adlarıyla konur.

## Her istemin başındaki iki blok

```
CRITICAL: this is the FLAT ARTWORK FILE for print — NOT a photograph of
an installed sign. No fence, no billboard frame, no poles, no
perspective, no environment, no mockup, no drop shadow around the panel.
The image IS the printed panel, filling the frame edge to edge, viewed
perfectly straight on.

MANDATORY STRUCTURE:
• TOP BAND — the top 16% is a completely FLAT, EMPTY band of solid
  {renk}. No text, no graphics, no logo. Reserved, leave it clean.
• BOTTOM BAND — the bottom 16% is the same completely FLAT, EMPTY solid
  {renk} band. Reserved, leave it clean.
• MIDDLE — the remaining 68% carries the design below.
Do NOT draw any logo, brand mark, monogram, emblem or company symbol
anywhere.
```

Birincisi olmazsa üretim panoyu şantiye çitine asılmış hâlde, perspektifli
bir FOTOĞRAF olarak çiziyor — baskıya gidecek düz dosya değil. Bir önceki
denemede kimlik panosu bu yüzden elenmişti.

İkincisi bantları ayırıyor: marka yapay zekâya çizdirilmiyor, gerçek logo
oraya betikle basılıyor. Bant rengi de oradan ölçülüyor, o yüzden istemde
verilen renk panonun paletini belirliyor.

Sonda her istemde:

```
TEXT FIDELITY IS CRITICAL: reproduce every Turkish string EXACTLY,
preserving İ ı Ş ş Ğ ğ Ç ç Ö ö Ü ü. No prices, no ₺. Do not translate,
abbreviate, re-spell or invent any word.
```

## Sekiz tasarım — sekiz ayrı KURGU

Önceki set reddedildi: hepsi "fotoğrafın üstüne yazı"ydı. Bu sette her
panonun kurgusu farklı; üçünde fotoğraf ya dipnot boyunda ya hiç yok.

| # | Bant rengi | Kurgu | Türkçe metin |
|---|---|---|---|
| 1 mozaik | petrol #075878 | altı farklı boy fotoğraf karosu, beyaz derzli ızgara; yazı yalnızca tek renkli blokta, hiçbir fotoğrafın üstünde değil | MERKEZİ AVLU ÇEVRESİNDE HAYAT · SÜS HAVUZLARI · GENİŞ PEYZAJ · YÜRÜYÜŞ YOLLARI · ÇOCUK OYUN PARKI |
| 2 kemer | kum #C8B18A | düz krem zemine açılmış üç kemer pencere; fotoğraf sadece kemerlerin içinde | MİA PARK OCEAN'DA · DIŞARISI DA EVİNİZİN BİR PARÇASI |
| 3 tipografik | antrasit #1B2228 | saf tipografi, arkada fotoğraf yok; altta mercan çubuk, sağ altta dipnot boyunda tek kare | %0 FAİZ · 60 AY VADE · KREDİ YOK · FAİZ YOK · KEFİL YOK |
| 4 diyagonal | petrol #075878 | 8 derece eğik, üst üste düşmüş üç düzlem; manşet yalnızca düz renkli düzlemde | DÜŞÜK PEŞİNATLA EV SAHİBİ OLUN · 60 AY VADE FARKSIZ TAKSİT |
| 5 duotone | gece #04222F | tüm zemin iki renkli duotone; sağ alta kesilmiş pencereden gerçek renk görünüyor | BURADA EVİNİZ OLSUN İSTEMEZ MİYDİNİZ? |
| 6 sutunlu | petrol #075878 | boydan boya beş dikey sütun; yazı yalnızca iki düz renkli sütunda, biri dikey dizilmiş | EVİNİZİ ŞİMDİDEN GÖRÜN · 1+0 / 1+1 / 2+1 · 28 – 100 m² |
| 7 veri | orman #12463F | altı düz renk bloğundan infografik duvar; tek blok fotoğraf | 600 KONUT · 60 AY VADE · 4 DAİRE TİPİ · 28–100 m² · %0 FAİZ |
| 8 siluet | gece #04222F | dev daire; bina arka planından kesilip daireden taşıyor, dikdörtgen fotoğraf çerçevesi yok | SATIŞ OFİSİMİZ AÇIK · KAHVEMİZİ İÇMEYE BEKLERİZ |

## Üç metin tuzağı

**Yüzme havuzu yok.** İsteme "There is NO swimming pool in this project —
never write or imply YÜZME HAVUZU" satırı eklendi. Render'lardaki su süs
havuzu; panolarda da öyle geçiyor.

**KAHVEMİZİ, KAHVENİZİ değil.** Modelin daha olası bulduğu çekim
KAHVENİZİ; isteme "Note it is KAHVEMİZİ (our coffee), not KAHVENİZİ"
diye ayrıca yazıldı.

**Artı işareti ve blok etiketi.** Veri panosunda "1+0" üç denemede de
bulanık/çift çıktı — model artı işaretinde takılıyor. Blok artı
içermeyen bir veriye çevrildi: 4 DAİRE TİPİ. Ayrıca istemde blokları
"block A, block B" diye adlandırmak panoya A/B/C harflerini bastırıyordu;
bloklar artık konumla tarif ediliyor ve "bu tarifler asla basılmayacak"
diye ayrıca yazılıyor.

## Karekod yuvası

Beşinci istemde sağ alta "içi tamamen boş beyaz yuvarlak köşeli kare"
bırakılıyor; gerçek karekodu betik oraya basıyor. Yuvayı bulmak "beyaz
piksellerin sınır kutusu" ile denendi, olmadı: panodaki BEYAZ YAZI da
eşiği geçip kutuyu manşete kadar büyütüyor, karekod tasarımın yarısını
kaplıyordu. Çalışan ölçüt TAMAMEN DOLU KARE — maske sekizde bire
indirilip en büyük dolu kare DP ile bulunuyor. Yazı ince olduğu için asla
dolu kare oluşturmuyor.
