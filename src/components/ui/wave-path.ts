/**
 * Logodaki dalga — `scripts/build-wave.py` tarafından
 * `public/brand/mark-ocean-trim.png` içinden birebir kesildi.
 *
 * ELLE DÜZENLEMEYİN. Değişiklik gerekiyorsa betiği yeniden çalıştırın.
 * Sitedeki her dalga bu iki varlıktan birini kullanır; başka hiçbir yerde
 * elle çizilmiş dalga eğrisi yoktur.
 */

/** Dalga şeridi — logodaki orijinal pikseller, şeffaf zemin. */
export const WAVE_IMAGE = "/brand/wave.webp";

/**
 * Aynı dalganın dolgulu maskesi: şeridin kendisi + altındaki her şey opak.
 * `mask-image` olarak kullanıldığında üst kenarı birebir logodaki dalga olan
 * dolu bir panel verir.
 */
export const WAVE_MASK = "/brand/wave-mask.png";

/**
 * Aynı dalganın boşluksuz silueti — üst kenar birebir aynı, iç ayrımlar dolu.
 * Koyu fotoğraf üstünde alt katman olarak kullanılır.
 */
export const WAVE_MASK_SOLID = "/brand/wave-mask-solid.png";

/** Şeridin en/boy oranı. */
export const WAVE_RATIO = 4.9535;
