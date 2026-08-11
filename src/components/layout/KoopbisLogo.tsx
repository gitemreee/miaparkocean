// KOOPBİS (Kooperatif Bilgi Sistemi) logosu — resmî görsele sadık SVG uyarlaması.
// Beyaz "koop|bis" wordmark, lacivert gradyan zeminde.
// [DOĞRULANACAK: birebir orijinal dosya gelirse public/koopbis-logo.* ile <img> olarak değiştirilebilir.]

type Props = { className?: string };

export function KoopbisLogo({ className = "" }: Props) {
  return (
    <svg
      viewBox="0 0 224 84"
      className={className}
      role="img"
      aria-label="KOOPBİS — Kooperatif Bilgi Sistemi"
    >
      <defs>
        <linearGradient id="koopbis-bg" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stopColor="#0d2769" />
          <stop offset="0.55" stopColor="#1a3a8c" />
          <stop offset="1" stopColor="#244a97" />
        </linearGradient>
      </defs>
      <rect x="0" y="0" width="224" height="84" rx="12" fill="url(#koopbis-bg)" />
      {/* ince diyagonal parlama */}
      <path d="M56 0 L96 0 L52 84 L14 84 Z" fill="#ffffff" opacity="0.06" />

      {/* koop | bis */}
      <text
        x="106"
        y="49"
        textAnchor="end"
        fontFamily="var(--font-manrope), sans-serif"
        fontWeight={800}
        fontSize="42"
        letterSpacing="-1.5"
        fill="#ffffff"
      >
        koop
      </text>
      <rect x="108.5" y="17" width="2.6" height="33" rx="1.3" fill="#c8d4f0" />
      <text
        x="117"
        y="49"
        textAnchor="start"
        fontFamily="var(--font-manrope), sans-serif"
        fontWeight={800}
        fontSize="42"
        letterSpacing="-1.5"
        fill="#ffffff"
      >
        bis
      </text>

      {/* ince alt çizgi */}
      <rect x="42" y="57" width="140" height="1.6" rx="0.8" fill="#ffffff" opacity="0.85" />

      {/* alt başlık */}
      <text
        x="112"
        y="71"
        textAnchor="middle"
        fontFamily="var(--font-manrope), sans-serif"
        fontWeight={500}
        fontSize="9.5"
        letterSpacing="2.6"
        fill="#e6ecfa"
      >
        KOOPERATİF BİLGİ SİSTEMİ
      </text>
    </svg>
  );
}
