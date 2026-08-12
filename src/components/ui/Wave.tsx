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
  /** Dalganın altını dolduran renk/gradyan — geçilen bölümün zemini. */
  fill?: string;
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
  fill = "linear-gradient(180deg,#e9f7fa,#f6fcfd 46%,#ffffff)",
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
      {/* Taban: dalganın boşluksuz silueti, bir sonraki bölümün zemininde.
          Üst kenarı birebir dalga olduğu için fotoğrafla sayfa arasındaki
          sınır dalgayı izler. */}
      <span className="wave-solid absolute inset-0" style={{ backgroundImage: fill }} />
      {/* Üstte dalganın kendisi — kaynak grafiğin orijinal renkleri */}
      {ribbon && (
        <span className="wave-ribbon absolute inset-0" style={{ opacity: ribbonOpacity }} />
      )}
    </div>
  );
}

/** Geriye dönük ad — eski çağrı yerleri için. */
export function WaveDivider({
  flip = false,
  className = "h-[54px] md:h-[88px]",
}: {
  tone?: string;
  flip?: boolean;
  className?: string;
  animated?: boolean;
}) {
  return <WaveEdge flip={flip} className={className} />;
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
