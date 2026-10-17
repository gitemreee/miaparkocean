# MİA PARK OCEAN × TİLDA İNŞAAT — 180 m dev pano (7 tasarım)

## Ölçüler
- Pano: **180 m × 8,5 m**, tek parça kesintisiz tasarım.
- Baskı için 3 parça (soldan sağa): **A = 80 m**, **B = 20 m**, **C = 80 m**.
  Parçalar uç uca eklendiğinde görsel kesintisiz devam eder; ek yerleri
  80. ve 100. metrededir (proje görseli bu iki ek yerini içinde taşır).
- **Taşma (extension):** binanın üst kısmı panonun üst kenarından taşar.
  `tasma-kesim.png` şeffaf zeminlidir; kesim hattı görselin kendi
  kenarıdır (alfa kanalı). Panonun **75,28. metresinden** başlar,
  en yüksek noktası pano üst kenarından **3,55 m** yukarıdadır.
  Alt kenarı pano üst kenarına oturur.

## Çözünürlük
- Metre başına 400 piksel (1:1 ölçekte ~10 dpi). Bu boyuttaki ve bu
  izleme mesafesindeki (50 m+) panolar için standart değerdir.
- A ve C: 32.000 × 3.400 px · B: 8.000 × 3.400 px · RGB JPEG.
- Yazılar ve logolar vektörden çizildi; her ölçekte keskindir.
- Matbaa farklı bir ölçek isterse (ör. 1:10 @ 100 dpi) aynı dosya
  ölçeklenerek kullanılabilir; oranlar korunur.

## Dosyalar (her tasarım klasöründe)
- `onizleme.jpg` — gökyüzü önünde tam görünüm + ölçü çizgileri
- `baski/A-80m.jpg`, `baski/B-20m.jpg`, `baski/C-80m.jpg`
- `baski/tasma-kesim.png`

## Tasarımlar
1. Lacivert & altın — MİA'DA YAŞAM BAŞLIYOR! / EVİNİZE GİDEN 60 ADIM!
2. Gökyüzü — MİA'DA YAŞAM BAŞLIYOR! / 60 AY SABİT TAKSİT!
3. Krem & bronz (Tilda renkleri) — EVİNİZE GİDEN 60 ADIM!
4. Turkuaz — MİA'DA YAŞAM BAŞLIYOR!
5. 60 Adım — 60 basamak binaya doğru yükselir
6. Dev 60 — uzaktan ilk okunan sayı
7. Gece & turuncu — 60 AY SABİT TAKSİT!

Hepsinde: büyük Tilda İnşaat logosu (sol), altın/kırmızı "60 AY SABİT
TAKSİT" mührü, 1+0 / 1+1 aylık taksit paneli, MİA PARK OCEAN logosu,
miaparkocean.com, sağ alt köşede Ocean Gayrimenkul (tek yetkili satış)
+ 0540 028 00 41.

Üretim: `python3.13 scripts/build-mega-bilbord.py`
