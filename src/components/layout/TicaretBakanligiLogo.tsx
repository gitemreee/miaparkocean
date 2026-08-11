// T.C. Ticaret Bakanlığı logosu — ay-yıldız amblemi + wordmark, SVG uyarlaması.
// [DOĞRULANACAK: birebir orijinal logo dosyası gelirse public/ticaret-bakanligi-logo.* ile <img> olarak değiştirilebilir.]

type Props = { className?: string };

export function TicaretBakanligiLogo({ className = "" }: Props) {
  return (
    <svg
      viewBox="0 0 224 84"
      className={className}
      role="img"
      aria-label="T.C. Ticaret Bakanlığı"
    >
      <defs>
        <mask id="tb-crescent">
          <circle cx="34" cy="42" r="24" fill="#ffffff" />
          <circle cx="42.5" cy="42" r="19.5" fill="#000000" />
        </mask>
      </defs>

      {/* Hilal */}
      <rect x="8" y="16" width="52" height="52" fill="#E30A17" mask="url(#tb-crescent)" />
      {/* Yıldız */}
      <path
        d="M50 34 L51.9 39.4 L57.6 39.5 L53 43 L54.7 48.5 L50 45.2 L45.3 48.5 L47 43 L42.4 39.5 L48.1 39.4 Z"
        fill="#E30A17"
      />

      {/* Wordmark */}
      <text
        x="76"
        y="33"
        fontFamily="var(--font-manrope), sans-serif"
        fontWeight={700}
        fontSize="12"
        letterSpacing="2.5"
        fill="#141414"
      >
        T.C.
      </text>
      <text
        x="75"
        y="53"
        fontFamily="var(--font-manrope), sans-serif"
        fontWeight={800}
        fontSize="18.5"
        letterSpacing="-0.3"
        fill="#141414"
      >
        TİCARET
      </text>
      <text
        x="75"
        y="72"
        fontFamily="var(--font-manrope), sans-serif"
        fontWeight={800}
        fontSize="18.5"
        letterSpacing="-0.3"
        fill="#141414"
      >
        BAKANLIĞI
      </text>
    </svg>
  );
}
