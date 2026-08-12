import { WAVE_TILE } from "@/components/ui/Wave";

/**
 * Site arka planı — logodaki dalga.
 *
 * Sabit (fixed) bir katman olarak tüm sayfanın arkasında durur; içerik
 * kaydıkça dalgalar yerinde kalır ve sayfaya sakin bir "okyanus zemini"
 * hissi verir. Bölüm zeminleri yarı saydam olduğu için doku hafifçe görünür.
 *
 * Tamamen dekoratiftir: tıklama almaz, ekran okuyucuya görünmez.
 */
export function WaveBackdrop() {
  return (
    <div className="pointer-events-none fixed inset-0 -z-10 overflow-hidden bg-gradient-sky" aria-hidden="true">
      {/* Üst yumuşak ışık */}
      <div className="absolute -top-1/4 left-1/2 h-[70vh] w-[120vw] -translate-x-1/2 rounded-full bg-[radial-gradient(closest-side,rgba(255,255,255,0.9),transparent)]" />

      {/* Katman 1 — en açık, yavaş */}
      <div className="absolute inset-x-0 top-[18%] h-[26vh] opacity-45">
        <div className="wave-drift-slow absolute inset-0 w-[200%]">
          <svg viewBox="0 0 2880 140" preserveAspectRatio="none" className="h-full w-full">
            <path d={WAVE_TILE} fill="#d6e6f3" />
            <g transform="translate(1440 0)">
              <path d={WAVE_TILE} fill="#d6e6f3" />
            </g>
          </svg>
        </div>
      </div>

      {/* Katman 2 — orta ton */}
      <div className="absolute inset-x-0 top-[46%] h-[30vh] opacity-40">
        <div className="wave-drift absolute inset-0 w-[200%]">
          <svg viewBox="0 0 2880 140" preserveAspectRatio="none" className="h-full w-full">
            <path d={WAVE_TILE} fill="#c2e8f0" />
            <g transform="translate(1440 0)">
              <path d={WAVE_TILE} fill="#c2e8f0" />
            </g>
          </svg>
        </div>
      </div>

      {/* Katman 3 — en koyu turkuaz, altta */}
      <div className="absolute inset-x-0 bottom-0 h-[32vh] opacity-35">
        <div className="wave-drift-slow absolute inset-0 w-[200%]">
          <svg viewBox="0 0 2880 140" preserveAspectRatio="none" className="h-full w-full">
            <path d={WAVE_TILE} fill="#9cd8e4" />
            <g transform="translate(1440 0)">
              <path d={WAVE_TILE} fill="#9cd8e4" />
            </g>
          </svg>
        </div>
      </div>
    </div>
  );
}
