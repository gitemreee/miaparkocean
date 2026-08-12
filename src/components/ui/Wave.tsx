/**
 * MİA PARK OCEAN — dalga sistemi.
 *
 * Buradaki eğriler logonun altındaki dalganın ÜST SİLUETİNDEN birebir
 * çıkarılmıştır (`mark-ocean-trim.png` alfa kanalı taranıp yumuşatıldı).
 * Jest: soldan yükselir, orta boyunca tepede kalıp hafifçe salınır, sağda
 * alçalır. Üç katman, logodaki kurdele dizilimini verecek şekilde aynı
 * eğrinin faz kaydırmalı kopyalarıdır.
 *
 * Dalga sitenin imzasıdır: bölüm geçişleri, hero alt kenarı, kart köşeleri,
 * arka plan dokusu ve sayfa geçiş animasyonu hep bu eğriyi kullanır.
 */

/** Kapalı dalga siluetleri — viewBox 0 0 1440 120, alt kenara kadar dolu. */
export const WAVE_PATHS = {
  back: "M0,24 C15,22 60,13 90,11 C120,9 150,14 180,14 C210,14 240,13 270,13 C300,12 330,13 360,11 C390,10 420,6 450,6 C480,6 510,8 540,9 C570,10 600,9 630,10 C660,11 690,13 720,14 C750,15 780,17 810,17 C840,18 870,16 900,15 C930,14 960,12 990,11 C1020,11 1050,10 1080,12 C1110,14 1140,18 1170,23 C1200,27 1230,36 1260,39 C1290,42 1320,43 1350,43 C1380,44 1425,43 1440,43 L1440,120 L0,120 Z",
  mid: "M0,53 C15,49 60,36 90,30 C120,24 150,19 180,17 C210,16 240,21 270,21 C300,21 330,20 360,20 C390,19 420,19 450,17 C480,16 510,12 540,12 C570,12 600,15 630,16 C660,17 690,15 720,16 C750,17 780,21 810,22 C840,23 870,24 900,24 C930,24 960,24 990,22 C1020,21 1050,17 1080,17 C1110,17 1140,17 1170,20 C1200,22 1230,28 1260,33 C1290,38 1320,47 1350,50 C1380,54 1425,53 1440,54 L1440,120 L0,120 Z",
  front:
    "M0,88 C15,83 60,67 90,58 C120,49 150,41 180,36 C210,30 240,27 270,26 C300,25 330,29 360,30 C390,30 420,30 450,29 C480,28 510,26 540,24 C570,23 600,20 630,20 C660,20 690,25 720,26 C750,27 780,24 810,25 C840,26 870,32 900,33 C930,34 960,31 990,31 C1020,31 1050,33 1080,31 C1110,30 1140,25 1170,25 C1200,24 1230,27 1260,31 C1290,35 1320,41 1350,47 C1380,53 1425,62 1440,66 L1440,120 L0,120 Z",
} as const;

/** Yatayda kusursuz tekrar eden dalga (kayan kurdele animasyonu için). */
export const WAVE_TILE =
  "M0,60 C120,20 240,20 360,60 C480,100 600,100 720,60 C840,20 960,20 1080,60 C1200,100 1320,100 1440,60 L1440,140 L0,140 Z";

/**
 * Kart köşesi için dalga — sağ üst köşeye oturan, logodaki eğrinin
 * kısa bir parçası. `.card-wave` sınıfıyla birlikte kullanılır.
 */
export const WAVE_CORNER =
  "M0,0 L120,0 L120,34 C102,34 92,20 74,20 C54,20 44,36 24,36 C14,36 6,32 0,26 Z";

type Tone = "paper" | "sky" | "mint" | "ocean" | "sapphire" | "lagoon";

/** Katman renkleri — üstteki bölümden alttakine geçişi yumuşatır. */
const TONES: Record<Tone, { back: string; mid: string; front: string }> = {
  paper: { back: "#dff0f7", mid: "#f2fafd", front: "#ffffff" },
  sky: { back: "#cfe8f4", mid: "#e8f5fb", front: "#f4fafd" },
  mint: { back: "#d8f0f0", mid: "#eaf8f8", front: "#f6fcfc" },
  ocean: { back: "#18789c", mid: "#0d5f80", front: "#06375a" },
  sapphire: { back: "#3e77ce", mid: "#1a5fb4", front: "#0f52ba" },
  lagoon: { back: "#9cd8e4", mid: "#6ac4d8", front: "#48b4cc" },
};

type WaveDividerProps = {
  /** Dalganın rengi — geçilen bölümün zeminiyle aynı olmalı */
  tone?: Tone;
  /** Dalga yukarı bakar (bir sonraki bölüm için) veya aşağı bakar */
  flip?: boolean;
  className?: string;
  /** Orta katman yavaşça salınsın */
  animated?: boolean;
};

/** Bölümler arası dalga geçişi — logodaki üç kurdele. */
export function WaveDivider({
  tone = "paper",
  flip = false,
  className = "h-[56px] md:h-[86px]",
  animated = false,
}: WaveDividerProps) {
  const c = TONES[tone];
  return (
    <div
      className={`wave-divider pointer-events-none ${flip ? "rotate-180" : ""} ${className}`}
      aria-hidden="true"
    >
      <svg viewBox="0 0 1440 120" preserveAspectRatio="none" className="h-full w-full">
        <path d={WAVE_PATHS.back} fill={c.back} opacity="0.6" />
        <path d={WAVE_PATHS.mid} fill={c.mid} opacity="0.85" className={animated ? "animate-float" : undefined} />
        <path d={WAVE_PATHS.front} fill={c.front} />
      </svg>
    </div>
  );
}

/**
 * Sürekli akan dalga kurdelesi — hero altı ve CTA bantlarında.
 * İki katman zıt yönde kayar, gerçek su hissi oluşur.
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
 * Kart köşesindeki dalga imzası. Kartın sağ üstüne mutlak konumlanır;
 * `.card-luxe` / `.card-gradient-border` içinde kullanılır.
 */
export function CardWave({ className = "" }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 120 40"
      className={`pointer-events-none absolute right-0 top-0 h-8 w-24 rounded-tr-[1.25rem] ${className}`}
      aria-hidden="true"
      preserveAspectRatio="none"
    >
      <defs>
        <linearGradient id="cw" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stopColor="#9cd8e4" stopOpacity="0.35" />
          <stop offset="55%" stopColor="#48b4cc" stopOpacity="0.55" />
          <stop offset="100%" stopColor="#18789c" stopOpacity="0.7" />
        </linearGradient>
      </defs>
      <path d={WAVE_CORNER} fill="url(#cw)" />
    </svg>
  );
}

/** Gradyanlı dalga — koyu bölümlerin kenarında marka gradyanını taşır. */
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
            <stop offset="0%" stopColor="#0f52ba" />
            <stop offset="55%" stopColor="#18789c" />
            <stop offset="100%" stopColor="#48b4cc" />
          </linearGradient>
        </defs>
        <path d={WAVE_PATHS.back} fill={`url(#${id})`} opacity="0.3" />
        <path d={WAVE_PATHS.mid} fill={`url(#${id})`} opacity="0.6" />
        <path d={WAVE_PATHS.front} fill={`url(#${id})`} />
      </svg>
    </div>
  );
}
