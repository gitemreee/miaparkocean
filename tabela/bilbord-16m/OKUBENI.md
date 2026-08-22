# MİA PARK OCEAN — 16,00 × 2,70 m tek parça branda (10 tasarım)

Meta v5 kampanya dilinde ultra geniş (5,93:1) seri. Görsel olarak
YALNIZCA giriş kapısı dış cephesi kullanılır (tasarım başına farklı
kadraj); fotoğraf sağda tam boy durur, sol kenarı gradyan zemine
yumuşak karışır. MİA logosu solda, OCEAN GAYRİMENKUL sağ üstte.

## Basım dosyaları

| Dosya | İçerik | Çalışma ölçüsü |
|---|---|---|
| `bilbord-16m-*.jpg` | 10 görsel, baskıya hazır | 1:10 ölçek (1600 × 270 mm) @ **300 dpi** = 18898 × 3189 px, dpi gömülü |
| `psd/bilbord-16m-*.psd` | Aynı 10 tasarımın **kilitli PSD**'si | 1:10 ölçek @ **150 dpi** = 9449 × 1594 px, dpi gömülü |

- PSD'ler **düzleştirilmiş tek katmandır** — Photoshop'ta kilitli
  "Background" katmanı olarak açılır; içerik kaydırılamaz/bozulamaz.
- Gerçek ölçü **16000 × 2700 mm**. Çalışmalar matbaa standardı 1:10
  ölçektedir; RIP'te %1000 büyütülür (16 m'de efektif 30 / 15 dpi —
  5 m ve üzeri izleme mesafesi için standart).
- Kesim payı yoktur; branda kenar dönüşü gerekiyorsa matbaa zemin
  gradyanını uzatabilir (kenarlar düz renktir).

## Kurallar (işveren)

- "Görseller temsilidir", kooperatif adı ve dönemsellik dipnotu YOK.
- "Peşinatsız" ifadesi ve "%30" oranı geçmez; onaylı örnek fiyatlar
  (1+0: 699.000 / 29.900 · 1+1: 999.000 / 39.900).
- Bina üzerine yazı binmez; yıldız rozetler foto/gök bölgesinde.

## Yeniden üretme

```
python3 scripts/build-bilbord-16m.py
```

JPEG + PSD + önizleme + kontak tek komutla üretilir. PSD'ler depoya
alınmaz (`.gitignore`); betik her makinede aynı dosyayı yeniden yazar.
