/**
 * MİA PARK OCEAN — dalga sistemi.
 *
 * Logodaki dalga sitenin imzasıdır: bölüm geçişleri, hero alt kenarı ve sayfa
 * geçiş animasyonu hep aynı dalga jestini kullanır. Üç katman, logodaki
 * kurdele diziliminin aynısıdır (arka · orta · ön).
 */

/** Kapalı dalga siluetleri — viewBox 0 0 1440 120, alt kenara kadar dolu. */
export const WAVE_PATHS = {
  back: "M0,60 C130,60 200,46 380,54 C540,61 600,78 780,72 C960,66 1020,44 1200,52 C1310,57 1380,74 1440,86 L1440,120 L0,120 Z",
  mid: "M0,74 C140,74 210,34 390,42 C550,49 610,68 790,62 C970,56 1030,28 1210,36 C1320,41 1385,62 1440,76 L1440,120 L0,120 Z",
  front:
    "M0,88 C160,88 220,18 400,26 C560,33 620,54 800,48 C980,42 1040,12 1220,20 C1330,25 1390,48 1440,62 L1440,120 L0,120 Z",
} as const;

/** Yatayda kusursuz tekrar eden dalga (kayan kurdele animasyonu için). */
export const WAVE_TILE =
  "M0,60 C120,20 240,20 360,60 C480,100 600,100 720,60 C840,20 960,20 1080,60 C1200,100 1320,100 1440,60 L1440,140 L0,140 Z";

type Tone = "paper" | "sky" | "mint" | "ocean" | "sapphire" | "jade";

/** Katman renkleri — üstteki bölümden alttakine geçişi yumuşatır. */
const TONES: Record<Tone, { back: string; mid: string; front: string }> = {
  paper: { back: "#f3f8fc", mid: "#ffffff", front: "#ffffff" },
  sky: { back: "#e7f1f9", mid: "#f3f8fc", front: "#d6e6f3" },
  mint: { back: "#f1fbf8", mid: "#e9f7f2", front: "#d1f2eb" },
  ocean: { back: "#061a4a", mid: "#04113a", front: "#000926" },
  sapphire: { back: "#3e77ce", mid: "#0f52ba", front: "#061a4a" },
  jade: { back: "#12885f", mid: "#0b6e4f", front: "#013220" },
};

type WaveDividerProps = {
  /** Dalganın rengi — geçilen bölümün zeminiyle aynı olmalı */
  tone?: Tone;
  /** Dalga yukarı bakar (bir sonraki bölüm için) veya aşağı bakar */
  flip?: boolean;
  /** Yükseklik sınıfı */
  className?: string;
  /** Katmanlar hafifçe kaysın (dinamik his) */
  animated?: boolean;
};

/**
 * Bölümler arası dalga geçişi. Üç katman farklı opaklık ve gecikmeyle
 * yerleşir; `animated` ile yavaşça salınır.
 */
export function WaveDivider({
  tone = "paper",
  flip = false,
  className = "h-[64px] md:h-[92px]",
  animated = false,
}: WaveDividerProps) {
  const c = TONES[tone];
  return (
    <div
      className={`wave-divider pointer-events-none ${flip ? "rotate-180" : ""} ${className}`}
      aria-hidden="true"
    >
      <svg viewBox="0 0 1440 120" preserveAspectRatio="none" className="h-full w-full">
        <path d={WAVE_PATHS.back} fill={c.back} opacity="0.55" />
        <path d={WAVE_PATHS.mid} fill={c.mid} opacity="0.8" className={animated ? "animate-float" : undefined} />
        <path d={WAVE_PATHS.front} fill={c.front} />
      </svg>
    </div>
  );
}

/**
 * Sürekli akan dalga kurdelesi — hero altı ve CTA bantlarında kullanılır.
 * İki katman zıt yönde kayar, böylece gerçek su hissi oluşur.
 */
export function WaveRibbon({
  className = "h-[70px] md:h-[110px]",
  tone = "paper",
}: {
  className?: string;
  tone?: Tone;
}) {
  const c = TONES[tone];
  return (
    <div className={`pointer-events-none relative w-full overflow-hidden ${className}`} aria-hidden="true">
      <div className="wave-drift-slow absolute inset-0 w-[200%]">
        <svg viewBox="0 0 2880 140" preserveAspectRatio="none" className="h-full w-full">
          <path d={WAVE_TILE} fill={c.back} opacity="0.5" />
          <g transform="translate(1440 0)">
            <path d={WAVE_TILE} fill={c.back} opacity="0.5" />
          </g>
        </svg>
      </div>
      <div className="wave-drift absolute inset-0 w-[200%]">
        <svg viewBox="0 0 2880 140" preserveAspectRatio="none" className="h-full w-full">
          <path d={WAVE_TILE} fill={c.front} opacity="0.92" />
          <g transform="translate(1440 0)">
            <path d={WAVE_TILE} fill={c.front} opacity="0.92" />
          </g>
        </svg>
      </div>
    </div>
  );
}

/**
 * Gradyanlı dalga — koyu bölümlerin üst/alt kenarında marka gradyanını taşır.
 */
export function WaveGradient({
  className = "h-[70px] md:h-[110px]",
  flip = false,
  id = "wave-grad",
}: {
  className?: string;
  flip?: boolean;
  id?: string;
}) {
  return (
    <div className={`wave-divider pointer-events-none ${flip ? "rotate-180" : ""} ${className}`} aria-hidden="true">
      <svg viewBox="0 0 1440 120" preserveAspectRatio="none" className="h-full w-full">
        <defs>
          <linearGradient id={id} x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="#000926" />
            <stop offset="26%" stopColor="#061a4a" />
            <stop offset="62%" stopColor="#0f52ba" />
            <stop offset="88%" stopColor="#0b6e4f" />
            <stop offset="100%" stopColor="#013220" />
          </linearGradient>
        </defs>
        <path d={WAVE_PATHS.back} fill={`url(#${id})`} opacity="0.35" />
        <path d={WAVE_PATHS.mid} fill={`url(#${id})`} opacity="0.65" />
        <path d={WAVE_PATHS.front} fill={`url(#${id})`} />
      </svg>
    </div>
  );
}
