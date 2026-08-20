# MİA PARK OCEAN — Lansman sunumu (emlakçılara)

`MIA-PARK-OCEAN-Lansman-Sunumu.pptx` — 15 slayt, 16:9, konuşmacı notlu.

## Sunumdan önce YAPILACAK

**13. slaytta üç alan bilerek boş bırakıldı.** Bu rakamlar depoda yok,
uydurmadım; sunumdan önce siz doldurun:

- Komisyon oranı
- Hakediş zamanı
- Müşteri bildirim / koruma süresi

Emlakçının en çok merak ettiği slayt bu; boş kalırsa güven kaybı olur.

## Akış

| # | Slayt | Ne yapıyor |
|---|---|---|
| 1 | Kapak | Lansman, tarih, yer |
| 2 | Gündem | Yirmi dakikada altı başlık |
| 3 | Proje künyesi | 600 daire · 4 tip · 28–100 m² · 60 ay |
| 4 | Konum | Sekiz mesafe |
| 5 | Stok | Dört tip, adetleriyle |
| 6 | Sosyal yaşam | Sekiz olanak |
| 7 | Ödeme modeli | Sunumun kalbi — %0 faiz, 60 ay, ara ödeme yok |
| 8 | Yatırım | m² fiyatı ve beş yıllık projeksiyon (grafik) |
| 9 | Güvence | Kooperatif neden devlet denetiminde |
| 10 | Saha | Dört itiraz, dört cevap |
| 11 | Hedef kitle | Kimi getirecekler |
| 12 | Satış desteği | Verilen materyaller |
| 13 | İş birliği | **doldurulacak** |
| 14 | Müşteri süreci | Peşinattan tapuya |
| 15 | Kapanış | İletişim + karekod |

## İçerik kaynağı

Bütün rakamlar `src/data/` altındaki proje verisinden: daire adetleri
`units.ts`, mesafeler `location.ts`, ödeme modeli `payment.ts`, kooperatif
güvencesi `cooperative.ts`, m² projeksiyonu `valuation.ts`.

**Fiyat yok.** Roll-up'lardaki 699.000 / 999.000 / 2.000.000 ₺ rakamları
depoda bir veri dosyasından gelmiyordu; sunuma da koymadım. Fiyat
verecekseniz satış ekibine doğrulattıktan sonra 7. slayda ekleyin.

**Yüzme havuzu yok.** 6. slaytta avludaki suyun süs havuzu olduğu, yüzme
havuzu diye anlatılmaması gerektiği ayrıca yazıyor. `src/data/amenities.ts`
hâlâ "Kapalı Yüzme Havuzu", "Fitness Salonu", "Sauna ve Türk Hamamı"
maddelerini taşıyor ve sitede görünüyor — bunlar gerçekten yoksa sitede de
düzeltilmeli. Sunuma hiçbiri alınmadı.

**Yatırım projeksiyonu bir öngörüdür.** 8. slaytta dipnotu var; sözlü
anlatırken de "öngörü" deyin, taahhüt gibi kurmayın.

## Yeniden üretme

```
node scripts/build-sunum.js
```

Görseller `sunum/kaynak/` altında. Yazı tipleri Cambria (başlık) ve
Calibri (gövde) — ikisi de Office ile geliyor, sunumu açan makinede
kesin var.
