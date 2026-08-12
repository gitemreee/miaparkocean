# Google Search Console, Bing ve Yandex Kurulumu

Bu adımları **siteyi yayına aldıktan sonra** uygulayın. Doğrulama, canlı sitedeki
etiketleri okuduğu için önce yayın, sonra doğrulama sırası önemlidir.

---

## 1. Doğrulama kodlarını yerleştirme

Tek dosya düzenlenir: **`src/data/verification.ts`**

```ts
export const verification = {
  google: "BURAYA_GOOGLE_KODU",
  bing: "BURAYA_BING_KODU",
  yandex: "BURAYA_YANDEX_KODU",
} as const;
```

Boş bırakılan alan sayfaya hiç yazılmaz — hepsini doldurmak zorunda değilsiniz.

Sonra:

```bash
npm run build     # out/ klasörü yeniden üretilir
```

ve `out/` klasörünü Netlify'a yükleyin (veya Git bağlıysa push edin).

---

## 2. Google Search Console

1. https://search.google.com/search-console adresine girin.
2. **Mülk ekle** → **URL öneki** sekmesi → `https://miaparkocean.com` yazın.
   > "Alan adı" (Domain) seçeneği DNS kaydı ister; DNS'e erişiminiz varsa o daha
   > kapsamlıdır (tüm alt alan adlarını kapsar). Erişim yoksa URL öneki yeterlidir.
3. Doğrulama yöntemi: **HTML etiketi**.
4. Görünen `<meta name="google-site-verification" content="XXXX" />` satırındaki
   **yalnızca `content` değerini** kopyalayın.
5. `src/data/verification.ts` → `google` alanına yapıştırın → build → yayına alın.
6. Search Console'a dönüp **Doğrula**'ya basın.

### Sitemap gönderimi

Doğrulandıktan sonra sol menü → **Sitemap'ler** → şu adresi ekleyin:

```
sitemap.xml
```

(Search Console alan adını kendisi ekler; tam adres `https://miaparkocean.com/sitemap.xml`.)

### İlk hafta kontrol listesi

- **Sayfalar** raporu → "Dizine eklenmedi" sekmesinde beklenmeyen sayfa var mı?
  `/davetiye/` ve `/basin-aciklamasi/` burada **görünmeli** (bilinçli olarak `noindex`).
- **URL Denetimi** ile ana sayfayı ve bir bölge sayfasını test edin → "Canlı URL'yi test et"
  → yapısal veri hataları var mı?
- **Deneyim → Core Web Vitals** verisi 28 gün sonra dolmaya başlar.

---

## 3. Bing Webmaster Tools

**En hızlı yol — Google'dan içe aktarma:**

1. https://www.bing.com/webmasters adresine girin, Microsoft hesabıyla oturum açın.
2. **Import from Google Search Console** düğmesine basın.
3. Google hesabınızla izin verin — site, sitemap ve doğrulama otomatik aktarılır.

**Manuel yol:**

1. **Add a site** → `https://miaparkocean.com`
2. **HTML Meta Tag** yöntemi → `content` değerini kopyalayın.
3. `src/data/verification.ts` → `bing` alanına yapıştırın → build → yayın → **Verify**.
4. **Sitemaps** → `https://miaparkocean.com/sitemap.xml` gönderin.

---

## 4. Yandex Webmaster

Türkiye'de Yandex'in kayda değer bir arama payı vardır; atlanmamalıdır.

1. https://webmaster.yandex.com.tr → **Site ekle** → `https://miaparkocean.com`
2. **Meta etiketi** yöntemi → `content` değerini `verification.yandex` alanına yazın.
3. Build → yayın → **Kontrol et**.
4. **Dizine ekleme → Site haritası dosyaları** → `https://miaparkocean.com/sitemap.xml`

---

## 5. IndexNow — anında bildirim

IndexNow, yeni veya güncellenen sayfaları Bing, Yandex ve Seznam'a **saniyeler
içinde** bildirir. (Google IndexNow'ı desteklemez.)

Anahtar dosyası zaten yayında: `https://miaparkocean.com/8f3c1d7a49b24e6f9a0c5e2b7d18f4a6.txt`

Kullanım:

```bash
npm run build            # sitemap güncellenir
npm run indexnow         # sitemap'teki tüm URL'leri bildirir

# yalnızca belirli sayfalar:
node scripts/indexnow.mjs /bolgeler/izmit-yahya-kaptan/ /daireler/
```

`HTTP 200` veya `202` yanıtı başarılıdır. `202`, anahtarın doğrulanmayı beklediğini
gösterir; ilk gönderimde normaldir.

> **Not:** Günde birkaç kez göndermek yeterlidir. Aynı URL'leri sürekli yeniden
> bildirmek fayda sağlamaz, aşırı kullanımda hız sınırı uygulanabilir.

---

## 6. Google Business Profile (yerel paket)

Bölge sayfalarının etkisini çarpan tek adım budur. Harita sonuçlarında görünmek için:

1. https://business.google.com → **İşletme ekle**
2. İşletme adı: **Ocean Gayrimenkul — MİA PARK OCEAN Satış Ofisi**
3. Kategori: *Emlak Ofisi* (birincil), *Konut Geliştiricisi* (ikincil)
4. Adres: Ömerağa Mah. Abdurrahman Yüksel Cad. Bana Bak Ap. No:15/4, İzmit/Kocaeli
5. Telefon: 0540 028 00 41 · Web: https://miaparkocean.com
6. Doğrulama: kartpostal veya telefon (Google yönlendirir)
7. Kayıt açıldıktan sonra: proje görselleri yükleyin, hizmet bölgesi olarak
   İzmit / Körfez / Derince / Başiskele / Kartepe / Gölcük ekleyin.

---

## 7. Yayın sonrası rutini

| Sıklık | İş |
|---|---|
| Her yayında | `npm run build && npm run indexnow` |
| Haftalık | GSC → Performans raporu; yeni sorgu var mı? |
| Aylık | GSC → Sayfalar raporu; dizinlenmeyen sayfa var mı? |
| Aylık | GEO kontrolü — ChatGPT/Perplexity'ye proje sorusu sorun (bkz. SEO-AUDIT.md §4) |
| Üç aylık | Bölge sayfalarındaki mesafe/donatı bilgilerini gözden geçirin |
