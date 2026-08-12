/**
 * MİA PARK OCEAN dalgası — `scripts/build-wave.py` tarafından
 * `brand-source/wave-source.png` üzerinden üretilir.
 *
 * ELLE DÜZENLEMEYİN. Dalga yeniden çizilmez; kaynak grafik olduğu gibi
 * kullanılır. Sitedeki her dalga bu varlıklardan birini gösterir.
 */

/** Dalga şeridi — kaynak grafiğin orijinal pikselleri, şeffaf zemin. */
export const WAVE_IMAGE = "/brand/wave.webp";

/**
 * Aynı dalganın dolgulu maskesi: kurdeleler + altındaki her şey opak.
 * `mask-image` olarak kullanıldığında üst kenarı birebir dalga olan dolu
 * bir panel verir.
 */
export const WAVE_MASK = "/brand/wave-mask.png";

/**
 * Aynı dalganın boşluksuz silueti — üst kenar birebir aynı, kurdele araları
 * dolu. Koyu fotoğraf üstünde alt katman olarak kullanılır.
 */
export const WAVE_MASK_SOLID = "/brand/wave-mask-solid.png";

/** Şeridin en/boy oranı. */
export const WAVE_RATIO = 5.2287;
