import Link from "next/link";

type LogoProps = {
  /** dark: açık zeminde kullanım (varsayılan) · light: koyu zeminde beyaz plaket içinde */
  tone?: "light" | "dark";
  className?: string;
  compact?: boolean;
};

/**
 * MİA PARK OCEAN yatay kilit.
 *
 * Logo işareti orijinal dosyadan hiç değiştirilmeden kullanılır ve her zaman
 * BEYAZ zemin üzerinde durur. Koyu bölümlerde işaret beyaz bir plaketin içine
 * alınır; asla renk değiştirilmez.
 */
export function Logo({ tone = "dark", className = "", compact = false }: LogoProps) {
  const onDark = tone === "light";
  const textColor = onDark ? "text-cream" : "text-ink";
  const subColor = onDark ? "text-cream/60" : "text-ink/50";

  return (
    <Link
      href="/"
      className={`group inline-flex items-center gap-3 ${className}`}
      aria-label="MİA PARK OCEAN ana sayfa"
    >
      <span
        className={`grid shrink-0 place-items-center overflow-hidden rounded-xl bg-white transition-transform duration-500 group-hover:scale-[1.04] ${
          onDark ? "p-1.5 shadow-[0_8px_24px_-10px_rgba(4,39,62,0.6)]" : ""
        }`}
      >
        <img
          src="/brand/mark-ocean-trim.webp"
          alt=""
          aria-hidden="true"
          width={44}
          height={41}
          className="h-9 w-auto"
        />
      </span>
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
 * Tam dikey kilit (işaret + kelime markası + alt başlık) — orijinal logo dosyası.
 * Footer, davetiye, basın sayfası ve baskı çıktıları için.
 */
export function LogoLockup({
  className = "",
  plate = false,
  width = 260,
}: {
  className?: string;
  /** Koyu zeminde beyaz plaket içine alır */
  plate?: boolean;
  width?: number;
}) {
  const img = (
    <img
      src="/brand/logo-ocean-trim.webp"
      alt="MİA PARK OCEAN — İzmit MİA Bölgesi"
      width={width}
      height={Math.round((width * 822) / 1200)}
      className={plate ? "w-full" : className}
    />
  );

  if (!plate) return img;

  return (
    <span
      className={`inline-block rounded-2xl bg-white px-7 py-6 shadow-[0_20px_50px_-24px_rgba(4,39,62,0.55)] ${className}`}
      style={{ width }}
    >
      {img}
    </span>
  );
}
