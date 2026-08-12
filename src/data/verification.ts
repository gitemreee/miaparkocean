/**
 * Arama motoru doğrulama kodları.
 *
 * Kodları aldıktan sonra YALNIZCA bu dosyayı düzenleyin; kod tabanında başka
 * yere dokunmanıza gerek yok. Boş bırakılan alanlar sayfaya hiç yazılmaz.
 *
 * NEREDEN ALINIR
 * ──────────────
 * Google Search Console
 *   1. https://search.google.com/search-console → "Mülk ekle" → "URL öneki"
 *   2. https://miaparkocean.com adresini girin
 *   3. Doğrulama yöntemi: "HTML etiketi" → content="..." içindeki değeri kopyalayın
 *   4. Aşağıdaki `google` alanına yapıştırın, siteyi yayına alın, "Doğrula"ya basın
 *
 * Bing Webmaster Tools
 *   1. https://www.bing.com/webmasters → "Site ekle"
 *      (Google Search Console'dan içe aktarma da yapılabilir — en hızlısı budur)
 *   2. "HTML Meta Etiketi" yöntemi → content="..." değerini `bing` alanına yazın
 *
 * Yandex Webmaster (Türkiye'de anlamlı trafik payı vardır)
 *   1. https://webmaster.yandex.com.tr → "Site ekle"
 *   2. "Meta etiketi" → content değerini `yandex` alanına yazın
 */

export const verification = {
  google: "", // örn: "abcDEF123..."
  bing: "",
  yandex: "",
} as const;

/**
 * IndexNow anahtarı — Bing, Yandex ve Seznam'a yeni/güncellenen sayfaları
 * anında bildirir. Anahtar dosyası `public/<key>.txt` olarak yayınlanır.
 * Değiştirirseniz public/ altındaki dosya adını da birlikte değiştirin.
 */
export const INDEXNOW_KEY = "8f3c1d7a49b24e6f9a0c5e2b7d18f4a6";
