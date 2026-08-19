# MİA PARK OCEAN — Ekip yaka kartları · Ölçü ve baskı föyü

Lansman yaka kartının kişiye özel basılmış hâli. Altı kart, tek tasarım.

| Dosya | İsim | Unvan |
|---|---|---|
| `yaka-engin-kocak.jpg` | Engin KOÇAK | Broker |
| `yaka-gul-gunerhan.jpg` | Gül GÜNERHAN | Satış Temsilcisi |
| `yaka-nursena-acikgoz.jpg` | Nursena AÇIKGÖZ | Satış Temsilcisi |
| `yaka-emir-yavuz.jpg` | Emir YAVUZ | Satış Temsilcisi |
| `yaka-kenan-duman.jpg` | Kenan DUMAN | Satış Temsilcisi |
| `yaka-mert-guler.jpg` | Mert GÜLER | Satış Temsilcisi |

`onizleme/` altında 1/3 ölçekli kontrol kopyaları var.

## Baskı

- **Ölçü:** 90 × 130 mm (standart kordon kabı ölçüsü)
- **Dosya:** 1063 × 1535 px, 1:1 ölçekte **300 dpi**, JPEG kalite 95,
  kromalık altörnekleme kapalı (4:4:4), dpi gömülü
- **Renk:** sRGB. Matbaa CMYK isterse kendi profiliyle çevirsin.
- **Malzeme:** 350 gr mat kuşe + mat selofan, ya da doğrudan PVC kart.
- **Taşma payı:** dosyada yok, görünen yüz ölçüsüdür. Kesim için her
  kenardan 3 mm pay ekleyin; zemin gradyanı kenara kadar dolu olduğu için
  payı matbaa uzatarak alabilir. Çerçeve kenardan 2,6 mm içeride, kritik
  yazı 14 mm içeride — kesim hiçbir şeyi kesmez.

## Düzen (mm, üstten)

```
    0 –  14   kordon deliği payı — kılavuz kapsül burada, yazı yok
   19 –  62   logo kilidi, ortalanmış (60 mm genişlik)
   72 –  84   isim, sola dayalı
   85 –  92   unvan
   96 –  97   vurgu çizgisi
  103 – 123   solda künye bloğu, sağda karekod (20 mm)
```

- **Soyadı büyük harf.** İsimle soyadı bir bakışta ayrılıyor, kalabalıkta
  soyadı uzaktan okunuyor.
- **İsim puntosu altı kartta da aynı.** En uzun isme (Nursena AÇIKGÖZ)
  göre bir kez ölçülüp hepsine uygulanıyor; kart başına ayrı punto
  seçilseydi yan yana asıldıklarında set dağınık görünürdü.
- Kordon deliği bandında hiçbir öğe yok; zımba ortadan geçebilir.

## Karekod

`https://miaparkocean.com` — sade adres, izleme eki yok. Kısa içerik
karekodu seyrek yapıyor, 20 mm'de telefon bir seferde okuyor. Üretilen
dosyadan geri okunarak doğrulandı.

## Kadro değişirse

`scripts/build-yaka-ekip.py` içindeki `EKIP` listesine satır ekleyip:

```
npm run yaka
```

Tasarım tek yerde; isim, unvan ve dosya adı listeden geliyor. Türkçe
karakterler dosya adında sadeleşiyor (Açıkgöz → acikgoz).
