/**
 * MİA PARK OCEAN — dalga sistemi.
 *
 * TEK BİR DALGA VAR: logonun altındaki dalga. `scripts/build-wave.py` onu
 * `mark-ocean-trim.png` içinden hiç değiştirmeden keser ve iki varlık üretir:
 *
 *   /brand/wave.webp      → şeridin kendisi, logodaki orijinal pikseller
 *   /brand/wave-mask.png  → aynı şeklin dolgulu maskesi (alt kısmı opak)
 *
 * Sitedeki her dalga — arka plan, bölüm geçişleri, hero alt kenarı, kart
 * köşeleri, sayfa geçiş animasyonu — bu iki varlıktan birini kullanır.
 * Elle çizilmiş, sentetik ya da "dalgamsı" hiçbir eğri yoktur.
 */

export { WAVE_IMAGE, WAVE_MASK, WAVE_MASK_SOLID, WAVE_RATIO } from "./wave-path";

type WaveEdgeProps = {
  /**
   * Dalganın altını dolduran renk/gradyan — geçilen bölümün zemini.
   * `false` verilirse taban çizilmez: bölüm `.wave-clip-end` ile zaten
   * dalga şeklinde kesiliyorsa dolguya gerek yoktur (ve sabit bir renk
   * sayfanın değişen tonunu hiçbir zaman tam tutturamaz).
   */
  fill?: string | false;
  /**
   * Dalganın KARŞI tarafındaki eriyen bant. Dalga, koyu fotoğraf ile açık
   * sayfa arasında sert bir kesim olarak durmasın diye o taraf yavaşça
   * dalganın tonuna doğru erir. `false` verilirse çizilmez.
   */
  haze?: string | false;
  /** Eriyen bandın yüksekliği (sarmalayıcının yüzdesi). */
  hazeHeight?: string;
  /** Dalganın kendi renkli şeridi üstte görünsün mü? */
  ribbon?: boolean;
  /** Şeridin opaklığı (0–1). */
  ribbonOpacity?: number;
  /** Dalga aşağı baksın (bir üstteki bölüme bağlanır). */
  flip?: boolean;
  className?: string;
};

/**
 * Bölüm zeminlerini birbirine bağlayan dalga kenarı.
 *
 * Akış içinde `position: relative` bir blok olarak durur. Bir bölümün alt
 * kenarına yapıştırmak için ÇAĞIRAN taraf mutlak konumlu bir sarmalayıcı
 * kullanır (`<div className="absolute inset-x-0 bottom-0"><WaveEdge …/></div>`);
 * böylece konum sınıfları burada çakışmaz.
 */
export function WaveEdge({
  fill = "linear-gradient(180deg,#eaf7fa,#f1fafb 55%,#f1fafb)",
  haze = "linear-gradient(180deg,rgba(233,246,249,0) 0%,rgba(233,246,249,0.1) 34%,rgba(235,247,250,0.34) 60%,rgba(238,249,251,0.72) 82%,rgba(241,250,251,0.95) 100%)",
  hazeHeight = "h-[260%]",
  ribbon = true,
  ribbonOpacity = 1,
  flip = false,
  className = "h-[54px] md:h-[88px]",
}: WaveEdgeProps) {
  return (
    <div
      className={`pointer-events-none relative w-full ${flip ? "rotate-180" : ""} ${className}`}
      aria-hidden="true"
    >
      {/* Karşı taraftaki eriyen bant — saydamdan başlar, dalgaya yaklaştıkça
          zeminin tonuna erir. Üst ucu saydam olduğu için hiçbir yerde çizgi
          bırakmaz; dalga yapıştırılmış gibi değil, zeminden çıkıyormuş gibi
          durur. Düz (flip yok) kullanımda bant dalga kutusunu da kaplar:
          kutunun kendi saydam üst bölgesi fotoğrafı olduğu gibi gösterip
          bandın bittiği yerde kesik yaratmasın. */}
      {haze && (
        <span
          className={`absolute inset-x-0 ${flip ? "bottom-full" : "bottom-0"} ${hazeHeight}`}
          style={{ backgroundImage: haze }}
        />
      )}
      {/* Taban: sayfa zemini dalganın ALT siluetinden başlar. Kurdeleler
          fotoğrafın üstüne biner, araları gerçekten saydam kalır — şeffaf
          PNG gibi görünür, arkasında beyaz bir gövde olmaz. */}
      {fill && <span className="wave-base absolute inset-0" style={{ backgroundImage: fill }} />}
      {/* Üstte dalganın kendisi — kaynak grafiğin orijinal renkleri */}
      {ribbon && (
        <span className="wave-ribbon absolute inset-0" style={{ opacity: ribbonOpacity }} />
      )}
    </div>
  );
}

/**
 * Koyu bölümlerin kenarındaki dalga.
 *
 * `flip` = koyu bölüme GİRİŞ (üst kenar): eriyen bant koyu tarafta olmalı,
 * yoksa dalganın hemen altında parlak bir şerit ve keskin bir çizgi kalır.
 * `flip` yok = koyu bölümden ÇIKIŞ (alt kenar): eriyen bant açık tarafta,
 * yani varsayılan.
 */
export function WaveDivider({
  flip = false,
  className = "h-[54px] md:h-[88px]",
}: {
  flip?: boolean;
  className?: string;
}) {
  return (
    <WaveEdge
      flip={flip}
      className={className}
      haze={
        flip
          ? "linear-gradient(180deg,rgba(91,171,195,0) 0%,rgba(70,156,187,0.32) 36%,rgba(40,128,165,0.66) 70%,rgba(18,104,140,0.92) 100%)"
          : undefined
      }
      hazeHeight={flip ? "h-[300%]" : undefined}
    />
  );
}

/**
 * Koyu bölümün ALT kenarı: bölüm `.wave-clip-end` ile dalga şeklinde kesilir,
 * bu bileşen de kesim çizgisinin üzerine dalganın kendi renkli şeridini koyar.
 * Şerit ve kesim aynı varlıktan geldiği için birebir hizalıdır.
 *
 * Bölümün `position: relative` olması gerekir (`.section-dark` zaten öyle).
 */
export function WaveSectionEnd({
  className = "h-[52px] md:h-[84px]",
}: {
  className?: string;
}) {
  return (
    <div
      className={`pointer-events-none absolute inset-x-0 bottom-0 ${className}`}
      aria-hidden="true"
    >
      {/* Koyu zemin dalgaya doğru açılsın diye yumuşak bir sis */}
      <span
        className="absolute inset-x-0 bottom-0 h-[300%]"
        style={{
          backgroundImage:
            "linear-gradient(180deg,rgba(226,244,249,0) 0%,rgba(226,244,249,0.1) 40%,rgba(230,246,250,0.3) 70%,rgba(234,247,250,0.55) 100%)",
        }}
      />
      <span className="wave-ribbon absolute inset-0" />
    </div>
  );
}

/** Serbest akan dalga şeridi — bant süslemesi. */
export function WaveRibbon({
  className = "h-[54px] md:h-[86px]",
  opacity = 0.6,
}: {
  className?: string;
  opacity?: number;
}) {
  return (
    <div className={`pointer-events-none relative w-full overflow-hidden ${className}`} aria-hidden="true">
      <span className="wave-ribbon absolute inset-0" style={{ opacity }} />
    </div>
  );
}

/** Marka gradyanıyla boyanmış dalga — koyu bantların kenarında. */
export function WaveGradient({
  className = "h-[52px] md:h-[84px]",
  flip = false,
}: {
  className?: string;
  flip?: boolean;
  id?: string;
}) {
  return (
    <WaveEdge
      flip={flip}
      ribbon={false}
      className={className}
      fill="linear-gradient(115deg,#095678,#1a7496 22%,#2c94b4 46%,#48abc5 68%,#6ebdd0)"
    />
  );
}

/** Kart köşesindeki dalga imzası. */
export function CardWave({ className = "" }: { className?: string }) {
  return <span className={`card-wave-mark ${className}`} aria-hidden="true" />;
}
