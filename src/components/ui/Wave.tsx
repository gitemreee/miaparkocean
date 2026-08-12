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
  /** Kurdele aralarını dolduran alt katman (fotoğraf sızmasın diye). */
  base?: string;
  /** Logodaki turkuaz şerit de üstte görünsün mü? */
  ribbon?: boolean;
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
  fill = "linear-gradient(180deg,#e4f4f9,#f2fafc 40%,#fbfeff 72%,#ffffff)",
  base = "linear-gradient(180deg,#8fcede,#b9e2ec 55%,#d8f0f5)",
  ribbon = false,
  flip = false,
  className = "h-[44px] md:h-[70px]",
}: WaveEdgeProps) {
  return (
    <div
      className={`pointer-events-none relative w-full ${flip ? "rotate-180" : ""} ${className}`}
      aria-hidden="true"
    >
      {/* Alt katman: boşluksuz siluet — kurdele aralarından fotoğraf sızmaz */}
      <span className="wave-solid absolute inset-0" style={{ backgroundImage: base }} />
      {/* Üst katman: dalganın kendi kurdeleleri */}
      <span className="wave-fill absolute inset-0" style={{ backgroundImage: fill }} />
      {ribbon && <span className="wave-ribbon absolute inset-0 opacity-40" />}
    </div>
  );
}

/** Geriye dönük ad — eski çağrı yerleri için. */
export function WaveDivider({
  flip = false,
  className = "h-[44px] md:h-[70px]",
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
      fill="linear-gradient(125deg,#0f52ba,#0c6c90 46%,#18789c 74%,#48b4cc)"
    />
  );
}

/** Kart köşesindeki dalga imzası. */
export function CardWave({ className = "" }: { className?: string }) {
  return <span className={`card-wave-mark ${className}`} aria-hidden="true" />;
}
