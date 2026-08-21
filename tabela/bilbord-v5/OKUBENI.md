# MİA PARK OCEAN — v5 kampanya bilbordları (10 ikili set = 20 pano)

Meta/Facebook v5 reklam setiyle **aynı tasarım dili**: dikey gradyan
zeminler, fosforlu sarı çipler, kırmızı yıldız rozetler, kartsız tam
genişlik dış cephe şeridi. Görseller gündüz: giriş kapısı ve pergola
terası kareleri, her çiftte farklı kadraj.

## İkili asım düzeni

Bilbordlar **yan yana iki pano** olarak kiralanır. Her set tek reklamın
ikiye bölünmüş hâlidir:

- `…-SOL.jpg` → soldaki panoya (manşet tarafı; MİA logosu solda)
- `…-SAG.jpg` → sağdaki panoya (fiyat/çip/telefon tarafı; OCEAN
  GAYRİMENKUL logosu sağda)

Fotoğraf şeridi ve gradyan iki panoda devam eder; **yazılar asla iki
panoya bölünmez** (çerçeve boşluğu hesaba katıldı). Panolar ters
asılırsa cümle kopar — SOL/SAĞ etiketine dikkat.

## Ölçü ve baskı

| | |
|---|---|
| Gerçek ölçü (pano başına) | **5000 × 3000 mm** |
| Dosya | 1:1 ölçekte 40 dpi · 7874 × 4724 px · JPEG (dpi gömülü) |
| Okunurluk | manşetler 320–570 mm, telefon 190 mm — 30–100 m |

## Setler

| # | Set | Mesaj | Şerit görseli |
|---|---|---|---|
| 01 | izmit | İZMİT EV SAHİBİ OLUYOR · 699.000/29.900 · ÜSTELİK FAİZSİZ! | Giriş kapısı (yakın) |
| 02 | yok-duvari | BANKA/FAİZ/KEFİL YOK · 60 AY SABİT TAKSİT · KOMİSYON YOK! | Giriş kapısı |
| 03 | sifir | %0 FAİZ·VADE FARKI·KOMİSYON · İZMİT MİA BÖLGESİ | Giriş kapısı (orta) |
| 04 | 60ay | 60 AY VADE FARKSIZ · yok listesi | Pergola terası |
| 05 | aylik | Aylık 29.900 TL'ye ev sahibi olun · FAİZ YOK! | Giriş kapısı (sağ) |
| 06 | kocaeli | KOCAELİ DENİZE YAKIN · 999.000/39.900 (1+1) · BANKA YOK! | Giriş kapısı (gökyüzü) |
| 07 | olma-zamani | EV SAHİBİ OLMA ZAMANI · 60 AY VADE FARKSIZ | Pergola (sağ detay) |
| 08 | studyo | 1+0 avantajlı yatırım · 699.000/29.900 kutuları | Pergola (sol) |
| 09 | tasarruf | Tasarrufa dayalı EV SAHİBİ OL! · ARA ÖDEME YOK! | Pergola (üst) |
| 10 | satis-ofisi | SATIŞ OFİSİMİZE BEKLERİZ · üçlü istatistik | Giriş kapısı (alçak) |

Fiyat geçen setler: 01, 05, 06, 08, 10 (onaylı örnek fiyatlar).

## Kurallar (işveren)

- "Görseller temsilidir", kooperatif adı ve dönemsellik dipnotu YOK.
- Logolar pedsiz şeffaf PNG; MİA solda, Ocean Gayrimenkul sağda.
- "Peşinatsız" ifadesi ve "%30" oranı geçmez.
- Bina üzerine yazı binmez (telefon çipi yol/peyzaj bandında,
  yıldızlar gök bölgesinde).

## Yeniden üretme

```
python3 scripts/build-bilbord-v5.py
```

`onizleme/` küçültülmüş kontrol kopyaları, `kontak-bilbord-v5.jpg`
tüm setlerin çift hâlinde tek bakışta görünümüdür.
