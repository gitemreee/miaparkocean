# MİA PARK OCEAN — Saha Tabelaları · Ölçü ve Baskı Föyü

Bu klasördeki dosyalar **baskıya hazırdır**. Tabelacıya bu föyle birlikte
verin. Tasarımın tamamı `scripts/build-signage.py` içinde milimetre olarak
yazılıdır; ölçü değişirse dosyalar yeniden üretilir (`npm run tabela`).

## Dosyalar

| Dosya | Gerçek ölçü | Ölçek / çözünürlük | Piksel |
|---|---|---|---|
| `totem-on-yuz.jpg` | 1200 × 4000 mm | 1:1 @ 75 dpi | 3543 × 11811 |
| `totem-arka-yuz.jpg` | 1200 × 4000 mm | 1:1 @ 75 dpi | 3543 × 11811 |
| `afis-1-kimlik.jpg` | 3000 × 2400 mm | 1:1 @ 50 dpi | 5906 × 4724 |
| `afis-2-finansman.jpg` | 3000 × 2400 mm | 1:1 @ 50 dpi | 5906 × 4724 |
| `afis-3-daireler.jpg` | 3000 × 2400 mm | 1:1 @ 50 dpi | 5906 × 4724 |
| `afis-4-konum.jpg` | 3000 × 2400 mm | 1:1 @ 50 dpi | 5906 × 4724 |
| `afis-5-sosyal-yasam.jpg` | 3000 × 2400 mm | 1:1 @ 50 dpi | 5906 × 4724 |
| `rollup-1…6-*.jpg` | 800 × 2000 mm | 1:1 @ 100 dpi | 3150 × 7874 |
| `bilbord-*-SOL/SAG.jpg` | 5000 × 3000 mm | 1:1 @ 40 dpi | 7874 × 4724 |
| `yaka-1…10-*.jpg` | 90 × 130 mm | 1:1 @ 300 dpi | 1063 × 1535 |

`MIA-PARK-OCEAN-TABELA-SUNUMU.pdf` — A4 yatay, 8 sayfa. Baskı için değil,
müşteriye/ekibe göstermek için. `onizleme/` klasöründe küçültülmüş kontrol
kopyaları ve `cit-dizilimi.jpg` (beş afiş yan yana) vardır.

Dosyalara DPI bilgisi gömülüdür; tabelacı açtığında doğru fiziksel ölçüde
gelir. Büyük formatta 1:1 ölçekte 50–75 dpi standarttır — afiş 3–30 m,
totem 5–50 m mesafeden okunur.

## Totem — 1200 × 4000 mm, çift yüzlü

Projenin **ön ve yan cephesine** birer adet. Her totem çift yüzlü: gelen ve
giden trafik iki farklı yüzü görür.

- **Ön yüz** — kimlik: logo, "Lüks artık ulaşılabilir.", 600 daire /
  4 yaşam tipi, 60 ay vade · %0 faiz bandı, künye.
- **Arka yüz** — bilgi: dört daire tipi (m² ve adet), mesafeler, künye.

Bant düzeni (üstten, mm):

```
    0 –  940   beyaz baş bandı      logo kilidi (amblem + isim + bölge)
  940 – 3280   mavi gövde           mesaj alanı
 3280 – 4000   beyaz ayak           QR · web · telefon · satıcı
```

**Üretim notları**

- Işıklı kutu tabela olarak öneriliyor: beyaz bantlar arkadan aydınlatılınca
  gece logo ve künye kendiliğinden okunur.
- Dosyada **taşma payı yok** — görünen yüz ölçüsüdür. Gerginlik/katlama için
  her kenardan 20 mm pay ekleyin, tasarımın kritik öğeleri kenardan en az
  95 mm içeridedir, kesim payı yazıya girmez.
- Zeminden yükseklik: baş bandının alt kenarı en az 2200 mm yukarıda kalsın
  ki logo araç trafiğinden görünsün.
- QR yerden yaklaşık 500–900 mm arasında kalır; yaya mesafesinden (30–80 cm)
  rahat okunur.

## Çevre afişleri — 3000 × 2400 mm, 5 modül

Şantiyeyi çeviren çite modüler olarak asılır. **Sıra serbesttir** ve
tekrarlanabilir: 15 m'lik bir cephe beş modülle bir kez, 30 m'lik cephe
iki tur döner.

| # | Konu | Ne diyor |
|---|---|---|
| 1 | Kimlik | Akşam görüntüsü + "Lüks artık ulaşılabilir." + 600 daire |
| 2 | Finansman | %0 faiz · 60 ay sabit taksit · bankasız/faizsiz/kefilsiz |
| 3 | Daire tipleri | Dört tipin iç mekânı, m² ve adetleri |
| 4 | Konum | Sekiz mesafe kartı (D100 1 dk … üniversite 10 dk) |
| 5 | Sosyal yaşam | Avlu, havuzlar, yürüyüş yolları + ortak alan rozetleri |

**Ortak künye şeridi.** Beş afişin de altında, aynı yükseklikte (üstten
2020 mm), 380 mm yüksekliğinde beyaz bir şerit vardır: web adresi, iki
telefon, karekod ve satıcı imzası. Afişler yan yana asıldığında çit boyunca
**kesintisiz beyaz bir çizgi** oluşur; set tek bir tasarım gibi okunur.
Bu yüzden afişler aynı hizada ve aynı yükseklikte asılmalıdır.

**Üretim notları**

- Malzeme: 440 gr branda (tam kapalı çit) ya da delikli mesh (rüzgâr yükü
  yüksekse). Mesh'te renkler ~%15 açılır; matbaaya "mesh için doygunluk
  artırılsın" notu düşün.
- Her kenardan 50 mm taşma payı ekleyin; kritik öğeler 130 mm içeridedir.
- Çıtaya/kuşgözüne denk gelen bölge en dıştaki 130 mm'dir — bu alanda yazı
  yoktur, delme güvenli.
- Alt künye şeridinin çamur/çamurluk hattının üstünde kalması için çitin
  alt kenarından en az 300 mm yukarıda asın.

## Roll-up — 800 × 2000 mm, 6 model

1 kimlik · 2 finansman · 3 daire tipleri · 4 ortak yaşam · 5 balkondan
körfez · 6 iç mekân.

**Görselden markaya gradyanlı geçiş.** Fotoğrafı sert bir çizgiyle kesip
altına renk koymak ucuz duruyordu; perde yumuşak inince görsel markaya
karışıyor ve yazı boşlukta değil kendi zemininde oturuyor. Daire tipleri
roll-up'ında dört kare de birbirine eriyerek geçiyor — sert çizgilerle
bölününce katalog sayfası gibi duruyordu.

Alt künye şeridi düz beyaz değil; beyazdan buz mavisine çok hafif bir
geçiş, yazı kontrastını bozmadan ölü alanı kaldırıyor.

**Alt kaset payı.** Roll-up'ın alt ~130 mm'si kasetin içinde kalır ve
görünmez. Kritik hiçbir şey oraya konmadı; künye şeridi beyaz olduğu için
kasete giren kısım da beyaz devam ediyor, kesildiği belli olmuyor.

Üst kenardan 40 mm, yanlardan 62 mm boş bırakıldı. Kaset genişliği 800 mm
olan standart mekanizmaya birebir oturur.

## Bilbord — 5000 × 3000 mm, 10 İKİLİ SET (20 adet)

Panolar **yan yana** kiralandığı için tasarımlar ikişerli. Her set bir
cümleyi ikiye bölüyor; `-SOL` ve `-SAG` dosyaları yan yana asılır.

| Set | Sol | Sağ |
|---|---|---|
| 01 gündüz-gece | Gündüz başka, | gece başka. |
| 02 dışarısı-içerisi | Dışarısı ne kadar iyiyse, | içerisi de o kadar. |
| 03 havuz-deniz | İster havuzu izleyin, | ister denizi. |
| 04 banka-faiz | Banka yok, kefil yok. | Kredi yok, faiz yok. |
| 05 balkon-bahçe | Kimine balkon, | kimine bahçe. |
| 06 rakamlar | 600 daire, | dört yaşam tipi. |
| 07 yürümek-oynamak | Yürüyüş yolu kapınızın önünde, | oyun parkı gözünüzün önünde. |
| 08 şehir-deniz | Şehrin içinde, | denizin yanında. |
| 09 ilk ev-aile | İlk eviniz de burada, | büyüyen aileniz de. |
| 10 kimlik | Lüks artık | ulaşılabilir. |

**Her panoda MİA logosu ve iletişim var** — biri diğerine bakmadan da tam.
Logo sol panoda sola, sağ panoda sağa yaslı; ikisi simetrik bir çift olur.

Bazı setlerde iki farklı kare (gündüz/gece gibi karşıtlıklar), bazılarında
**tek geniş karenin sol ve sağ yarısı** kullanıldı (04, 06, 10): o setlerde
iki pano tek bir görüntünün devamı gibi okunur.

**Tam boy baskı.** Beyaz künye şeridi yok: web adresi, telefonlar,
Instagram ve satıcı imzası BEYAZ olarak doğrudan görselin üstünde.
Karekod küçük bir beyaz plakette — görselin üstüne doğrudan basılan
karekodu telefon kamerası zeminden ayıramıyor.

Mesafe/konum bilgisi konmadı: bu boyda okunan tek şey başlık.

**Asarken:** iki pano arasında çerçeve boşluğu olduğu için cümlenin her
yarısı kendi panosuna ortalandı, dikişe yaslanmadı. Panoların sırası
karışırsa cümle bozulur — dosya adındaki SOL/SAG'a dikkat.

## Yaka kartı — 90 × 130 mm, 10 model

1 beyaz · 2 mavi · 3 buz mavisi · 4 fotoğraflı başlık · 5 yürüyüş yolu ·
6 dış cephe · 7 balkondan körfez · 8 avlu · 9 önden gündüz · 10 önden gece.
Lansman: 21 Ağustos 2026, Emex Otel, Kocaeli.

**5-8'de kart boyu proje karesi var, gradyanla eriyerek.** Düz perde kartı
dümdüz beyaz bırakıyordu. Kare üstte neredeyse tam güçte kalıyor, aşağı
indikçe zemine karışıyor; **geçiş ismin üstünde bitiyor** — bandın içinde
kalan isim arkasındaki ağaç ya da denizle yarışıp okunmuyordu.

**9-10 projeyi ÖNDEN, kırpmadan gösterir.** Bant yüksekliği ölçüden değil
render'ın en-boyundan çıkıyor: 16:9 kare 90 mm genişlikte tam 50,6 mm
ediyor, daha uzun bant kareyi yanlardan kırpıp projeyi yarım bırakırdı.
Bandın alt kenarı sert kesilmiyor, fotoğrafın kendisi saydama eriyip
zemindeki gradyanı açığa çıkarıyor — altına düz renk sürülünce o rengin
bittiği yerde görünür bir dikiş kalıyordu. 9 gündüz, 10 gece.

- **Soyadı büyük harf** — isimle soyadı bir bakışta ayrılıyor, uzaktan da
  soyadı okunuyor. İsim `BADGE_FIRST` / `BADGE_LAST` ile değişir.
- Üstten 14 mm kordon deliğine ayrıldı; o banda logo ya da yazı girerse
  zımba deliği tam ortasından geçer. Kartlarda deliğin yeri ince bir
  kılavuzla işaretli.
- Karekod 18 mm, sağ altta. Mavi kartta beyaz plakete alındı; koyu zeminde
  karekod okunmuyor.
- Kart başına isim değiştirmek için betikteki `BADGE_*` değerlerini
  düzenleyip `npm run tabela` çalıştırın.

## Karekodlar

| Yer | Adres |
|---|---|
| Totem, roll-up | `https://miaparkocean.com/?utm_source=totem` / `?utm_source=rollup` |
| Afişler | `https://miaparkocean.com/?utm_source=saha-afis` |
| Bilbord | `https://miaparkocean.com/?utm_source=bilbord` |
| Yaka kartı | `https://miaparkocean.com/?utm_source=lansman` |

`utm_source` sayesinde sahadaki tabeladan gelen ziyaretçi analitikte ayrı
görünür — hangi kanalın müşteri getirdiği ölçülebilir. Basılan dosyalardan
okunarak doğrulanmıştır.

## İçerik nereden geliyor

Tabelada yazan her rakam projenin veri dosyalarından üretiliyor; elle
yazılmıyor. Daire adedi ya da mesafe değişirse veriyi güncelleyip
`npm run tabela` demek yeterli.

| Bilgi | Kaynak |
|---|---|
| 600 daire, 4 tip, m² ve adetler | `src/data/units.ts` |
| Mesafeler | `src/data/location.ts` |
| Ortak alan rozetleri | `src/data/amenities.ts` |
| Telefon, web, satıcı | `src/data/site.ts` |
| 60 ay · %0 faiz metni | `src/data/payment.ts` |

## Dikkat

- **Bu afişler zorunlu şantiye tabelasının yerine geçmez.** Yapı sahibi,
  müteahhit, şantiye şefi, ruhsat tarih/no bilgilerini taşıyan resmî
  şantiye tabelası ayrıca asılmalıdır; bu set tanıtım amaçlıdır.
- Görsellerin tamamı mimari render'dır. Kullanılan üç dış cephe karesi
  baskı için 4096 px'e büyütülmüştür (`signage-source/`); mimari
  değişmemiştir, yalnızca çözünürlük artmıştır.
- **Logo renklendirilmez, üzerine yazı yazılmaz.** Koyu zeminde beyaz
  versiyonu, açık zeminde renkli versiyonu kullanılır; totemde beyaz bantla
  ayrılır.
- Ocean Gayrimenkul imzası şu an **tipografik** kuruludur: elimizdeki logo
  298 px ve bu ölçekte baskıda dağılıyor. Vektör logo (AI / EPS / SVG)
  gelirse `signage-source/ocean-logo-hi.png` olarak konulup betiğe
  bağlanabilir.

## Yeniden üretmek

```
npm run tabela
```

Gereksinimler: `pip install pillow numpy segno`.
