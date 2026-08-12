# Instagram ızgara seti — MİA PARK OCEAN

Bu klasörü `scripts/build-instagram-grid.py` üretir; elle düzenlemeyin,
betiği çalıştırın:

    python3 scripts/build-instagram-grid.py

## Ne var burada

* `01-…` … `14-…` — her klasör TEK bir geniş görselin üç parçası.
  Profil ızgarasında bu üç parça yan yana gelip tek kare gibi görünür.
* `_izgara-gorunumu.jpg` — o panelin ızgarada nasıl görüneceği.
* `IZGARA-ONIZLEME.jpg` — profilin tamamının maketi (en yeni üstte).
* `profil-fotografi.jpg` — profil resmi (1080x1080).

## Nasıl paylaşılır

1. Parçaları **dosya adındaki sıraya göre** paylaşın: `paylasim-1`,
   sonra `paylasim-2`, sonra `paylasim-3`. Instagram en yeniyi sola
   koyduğu için satır bu sırayla soldan sağa dizilir.
2. Bir paneli bitirmeden diğerine geçmeyin; yarım kalan satır ızgarayı
   bozar.
3. Panel klasörlerini numara sırasıyla ilerletin (01 → 14).
4. `01-karsidan-sabit` klasörünün üç parçasını **sabitleyin**. Instagram
   üç gönderi sabitlemeye izin verir; böylece o panel her zaman en üst
   satırda tek bir geniş görsel olarak durur.
5. Kırpma ekranında görsel tam oturur: akışta 4:5 yüklenir, ızgarada 3:4
   kırpılır ve fazlalık zaten hesaba katılmıştır.

## Ölçüler

| | |
|---|---|
| Akış gönderisi | 1080 x 1350 (4:5) |
| Izgarada görünen | 1012 x 1350 (3:4) |
| Panel | 3104 x 1350 |
| Parça bindirmesi | 68 px |
