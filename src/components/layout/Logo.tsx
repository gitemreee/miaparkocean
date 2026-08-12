import Link from "next/link";

type LogoProps = {
  /** dark: açık zeminde orijinal logo · light: koyu mavi zeminde beyaz logo */
  tone?: "light" | "dark";
  className?: string;
  compact?: boolean;
};

/**
 * MİA PARK OCEAN yatay kilit.
 *
 * Logonun ŞEKLİ hiçbir zaman değişmez. Açık zeminde orijinal dosya, koyu mavi
 * zeminde ise aynı dosyanın beyaz (ters) sürümü kullanılır — plaket yok,
 * logo doğrudan mavinin üzerinde beyaz durur.
 */
export function Logo({ tone = "dark", className = "", compact = false }: LogoProps) {
  const onDark = tone === "light";
  const textColor = onDark ? "text-white" : "text-ink";
  const subColor = onDark ? "text-white/60" : "text-ink/50";

  return (
    <Link
      href="/"
      className={`group inline-flex items-center gap-3 ${className}`}
      aria-label="MİA PARK OCEAN ana sayfa"
    >
      <img
        src={onDark ? "/brand/mark-ocean-white.webp" : "/brand/mark-ocean-trim.webp"}
        alt=""
        aria-hidden="true"
        width={44}
        height={41}
        className="h-9 w-auto shrink-0 transition-transform duration-500 group-hover:scale-[1.04]"
      />
      <span className="flex flex-col leading-none">
        <span className={`font-display text-[1.02rem] font-semibold tracking-[0.2em] ${textColor}`}>
          MİA PARK OCEAN
        </span>
        {!compact && (
          <span className={`eyebrow mt-1.5 text-[0.53rem] tracking-[0.28em] ${subColor}`}>
            İzmit MİA Bölgesi
          </span>
        )}
      </span>
    </Link>
  );
}

/**
 * Tam dikey kilit (işaret + kelime markası + alt başlık).
 * Footer, davetiye, basın sayfası ve baskı çıktıları için.
 */
export function LogoLockup({
  className = "",
  onDark = false,
  width = 260,
}: {
  className?: string;
  /** Koyu mavi zeminde beyaz sürümü kullanır */
  onDark?: boolean;
  width?: number;
}) {
  return (
    <img
      src={onDark ? "/brand/logo-ocean-white.webp" : "/brand/logo-ocean-trim.webp"}
      alt="MİA PARK OCEAN — İzmit MİA Bölgesi"
      width={width}
      height={Math.round((width * 822) / 1200)}
      className={className}
      style={{ width }}
    />
  );
}
