# Reels — MİA PARK OCEAN

Bu klasörü `scripts/build-reels.py` üretir; elle düzenlemeyin, betiği
çalıştırın:

    npm run reels

## Ne var burada

| Dosya | Ne |
|---|---|
| `reel-1-proje.mp4` | Mimari ve konum · 1080x1920 · ~26 sn |
| `reel-2-sosyal-yasam.mp4` | Avlu, havuz, yürüyüş yolları · ~27 sn |
| `reel-3-daireler.mp4` | Dört daire tipi · ~27 sn |
| `reel-*-kapak.jpg` | Her reels'in kapağı · 1080x1920 |
| `kapaklar-panel.jpg` | Üç kapağın birleşik hali · 3240x1920 |
| `kapaklar-izgara-onizleme.jpg` | Izgarada nasıl görüneceği |

Videolar filmin **kendi çekimlerinden** kurulur — `film-source/clips/`
altındaki aynı mp4'ler. Kaynak ikiye ayrılmaz: filmi değiştirirseniz
reels de aynı görüntüden üretilir.

## Kapaklar ızgarayı tamamlar

Üç kapak **tek bir geniş gece render'ının üç parçasıdır.** Profilde yan
yana geldiklerinde kesintisiz bir satır oluşturur — tıpkı gönderi
panelleri gibi.

Bunun çalışması için iki şey gerekir:

1. **Üçünü de arka arkaya paylaşın.** Araya gönderi girerse satır bozulur.
2. **Paylaşım sırası ters:** önce `reel-3`, sonra `reel-2`, sonra
   `reel-1`. Instagram en yeniyi sola koyar; bu sırayla satır soldan sağa
   *Proje · Sosyal yaşam · Daireler* diye dizilir.

### Kapağı yüklerken

Instagram reels kapağını **1080x1920** ister ama profil ızgarasında
hücreyi 3:4 gösterir; kapağın dikey ortasından 1080x1440'lık bir bant
kırpar. Tasarım o banda kuruldu.

Yükleme ekranında "Kapak" → "Galeriden seç" ile `reel-N-kapak.jpg`
dosyasını seçin. Ardından çıkan **ızgara kırpma** ekranında çerçeveyi
**tam ortada** bırakın — yukarı ya da aşağı kaydırırsanız satır kayar.
Kadrajın üstündeki ve altındaki 240'ar piksel zaten taşma payıdır,
yalnızca Reels sekmesinde görünür.

## Metinler nerede

Ekrandaki bütün yazılar `scripts/build-reels.py` içindeki `REELS`
listesindedir. Değiştirip `npm run reels` demek yeterli.

Güvenli alan: yazılar y 1200–1460 bandında ve solda durur. Reels arayüzü
altta ~340 px (kullanıcı adı, açıklama), sağda ~160 px (beğeni/yorum
tuşları) kaplar; bu bandın dışına çıkan yazı telefonda tuşların altında
kalır.

## Müzik

`scripts/film_score.py` ile sentezlenir — filmle aynı yatak, reels
uzunluğuna göre yeniden üretilir. Kendi müziğinizi kullanmak için
`public/videos/muzik.wav` koymanız yeterli; dosya varsa betik onu alır.
