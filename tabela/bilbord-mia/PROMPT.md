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

## Sekiz tasarım

| # | Bant rengi | MIDDLE | Türkçe metin |
|---|---|---|---|
| 1 | petrol #075878 | koyu gradyan, ÜÇ YUVARLAK fotoğraf yan yana, halkalı | KAPINIZIN ÖNÜNDE · SOSYAL YAŞAM · YÜZME HAVUZU / GENİŞ PEYZAJ / YÜRÜYÜŞ YOLLARI |
| 2 | antrasit #1B2228 | dev `%0 FAİZ` solda, dikey çizgi, `60 AY VADE` sağda mercan | KREDİ YOK · FAİZ YOK · KEFİL YOK |
| 3 | bronz #8A6534 | solda kırık beyaz alan, sağda loft iç mekân | TASARRUFA DAYALI FAİZSİZ FİNANSMAN · DÜŞÜK PEŞİNATLA EV SAHİBİ OLUN · 60 AY VADE FARKSIZ TAKSİT |
| 4 | gece #04222F | tam sayfa altın saat manzarası, solda perde, serif | BURADA EVİNİZ OLSUN İSTEMEZ MİYDİNİZ? · DENİZE VE ŞEHRE BİR ARADA BAKAN EVLER |
| 5 | gece #04222F | gece render'ı perdeli, üç şampanya hap, sağ altta BOŞ BEYAZ KARE | SATIŞ OFİSİMİZ AÇIK · KAHVENİZİ İÇMEYE BEKLERİZ · DAİRE PLANLARI / ÖDEME SEÇENEKLERİ / UZMAN DANIŞMANLIK |
| 6 | petrol #075878 | tam sayfa salon, altta perde, sağda üç hap | EVİNİZİ ŞİMDİDEN GÖRÜN · 1+0 / 1+1 / 2+1 |
| 7 | orman #12463F | tam sayfa avlu, altta perde | DIŞARISI DA EVİNİZİN BİR PARÇASI · YÜZME HAVUZU · YÜRÜYÜŞ YOLLARI · PEYZAJ ALANLARI · ÇOCUK OYUN ALANI |
| 8 | petrol #075878 | perdeli render üstünde üç buzlu cam kart | DAİRE TİPLERİ · 1+0 28 m² · 1+1 50 m² · 2+1 100 m² · TÜM TİPLERDE 60 AY VADE |

## Karekod yuvası

Beşinci istemde sağ alta "içi tamamen boş beyaz yuvarlak köşeli kare"
bırakılıyor; gerçek karekodu betik oraya basıyor. Yuvayı bulmak "beyaz
piksellerin sınır kutusu" ile denendi, olmadı: panodaki BEYAZ YAZI da
eşiği geçip kutuyu manşete kadar büyütüyor, karekod tasarımın yarısını
kaplıyordu. Çalışan ölçüt TAMAMEN DOLU KARE — maske sekizde bire
indirilip en büyük dolu kare DP ile bulunuyor. Yazı ince olduğu için asla
dolu kare oluşturmuyor.
