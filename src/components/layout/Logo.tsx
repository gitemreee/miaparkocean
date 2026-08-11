import Link from "next/link";

type LogoProps = {
  tone?: "light" | "dark"; // light: koyu zemin üzerinde açık yazı
  className?: string;
  compact?: boolean;
};

// MİA PARK OCEAN kelime markası — editoryal, mürekkep monogram.
export function Logo({ tone = "dark", className = "", compact = false }: LogoProps) {
  const stroke = tone === "light" ? "#F4F1EA" : "#1A1815";
  const textColor = tone === "light" ? "text-paper" : "text-ink";
  const subColor = tone === "light" ? "text-paper/50" : "text-ink/45";

  return (
    <Link href="/" className={`group inline-flex items-center gap-3 ${className}`} aria-label="MİA PARK OCEAN ana sayfa">
      <svg viewBox="0 0 40 42" className="h-8 w-8 shrink-0" aria-hidden="true">
        <path d="M6 32V12l14 10 14-10v20" fill="none" stroke={stroke} strokeWidth="2" strokeLinejoin="round" strokeLinecap="round" />
        <path d="M20 22v10" fill="none" stroke={stroke} strokeWidth="2" strokeLinecap="round" />
        <circle cx="20" cy="7.5" r="1.6" fill="#D71D28" />
      </svg>
      <span className="flex flex-col leading-none">
        <span className={`font-display text-lg font-medium tracking-[0.14em] ${textColor}`}>MİA PARK OCEAN</span>
        {!compact && <span className={`eyebrow mt-1 text-[0.54rem] ${subColor}`}>İzmit MİA Bölgesi</span>}
      </span>
    </Link>
  );
}
