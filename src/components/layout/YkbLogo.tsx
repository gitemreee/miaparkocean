// S.S. Yahya Kaptan Birlik Yapı Kooperatifi (YKB) logosunun ölçeklenebilir SVG uyarlaması.
// currentColor kullanır; koyu/açık zeminde text rengiyle yeniden renklendirilebilir.
// [DOĞRULANACAK: birebir marka dosyası gelirse public/ykb-logo.svg ile değiştirilebilir]

type YkbLogoProps = {
  className?: string;
  title?: string;
};

const spires = [
  { x: 150, top: 96 }, { x: 161, top: 68 }, { x: 172, top: 44 }, { x: 183, top: 28 },
  { x: 193, top: 20 }, { x: 203, top: 17 }, { x: 213, top: 24 }, { x: 223, top: 40 },
  { x: 233, top: 60 }, { x: 243, top: 88 }, { x: 253, top: 114 },
  { x: 139, top: 124 }, { x: 263, top: 134 },
];

export function YkbLogo({ className = "", title = "S.S. Yahya Kaptan Birlik Yapı Kooperatifi" }: YkbLogoProps) {
  return (
    <svg
      viewBox="0 0 402 360"
      className={className}
      role="img"
      aria-label={title}
      fill="currentColor"
    >
      <title>{title}</title>
      {/* Yükselen kule / spire motifi */}
      <g stroke="currentColor" strokeWidth="2.4" strokeLinecap="round">
        {spires.map((s) => (
          <line key={s.x} x1={s.x} y1={s.top} x2={s.x} y2={168} />
        ))}
      </g>
      {/* SS */}
      <text
        x="58"
        y="250"
        fontFamily="var(--font-manrope), sans-serif"
        fontSize="34"
        fontWeight={600}
        letterSpacing="1"
      >
        SS
      </text>
      {/* YKB */}
      <text
        x="212"
        y="272"
        textAnchor="middle"
        fontFamily="var(--font-manrope), sans-serif"
        fontSize="150"
        fontWeight={800}
        letterSpacing="-2"
      >
        YKB
      </text>
      {/* Alt başlık */}
      <text
        x="201"
        y="312"
        textAnchor="middle"
        fontFamily="var(--font-manrope), sans-serif"
        fontSize="29"
        fontWeight={600}
        letterSpacing="1.5"
      >
        YAHYAKAPTAN BİRLİK
      </text>
      <text
        x="201"
        y="346"
        textAnchor="middle"
        fontFamily="var(--font-manrope), sans-serif"
        fontSize="29"
        fontWeight={600}
        letterSpacing="1.5"
      >
        YAPI KOOPERATİFİ
      </text>
    </svg>
  );
}
