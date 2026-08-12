import type { ReactNode } from "react";
import { Reveal } from "./Reveal";

type SectionHeadingProps = {
  eyebrow?: string;
  title: ReactNode;
  lead?: ReactNode;
  index?: string;
  tone?: "dark" | "light";
  align?: "center" | "left";
  className?: string;
};

/**
 * Bölüm başlığı — gradyanlı mini dalga çizgisi + Marcellus başlık.
 * `tone="dark"` koyu okyanus zeminlerde kullanılır.
 */
export function SectionHeading({
  eyebrow,
  title,
  lead,
  tone = "light",
  align = "center",
  className = "",
}: SectionHeadingProps) {
  const isDark = tone === "dark";
  const isCenter = align === "center";
  const text = isDark ? "text-cream" : "text-ink";
  const soft = isDark ? "text-cream/65" : "text-ink/60";
  const label = isDark ? "text-accent-300" : "text-accent";

  return (
    <div className={`${isCenter ? "mx-auto max-w-2xl text-center" : "max-w-2xl"} ${className}`}>
      {eyebrow && (
        <Reveal>
          <div className={`flex items-center gap-3 ${isCenter ? "justify-center" : ""}`}>
            <span
              className={`h-[3px] w-7 rounded-full ${isDark ? "bg-accent-300" : "bg-gradient-surf"}`}
              aria-hidden="true"
            />
            <span className={`eyebrow ${label}`}>{eyebrow}</span>
          </div>
        </Reveal>
      )}
      <Reveal delay={0.05}>
        <h2 className={`mt-5 text-balance text-[2rem] leading-[1.08] sm:text-[2.6rem] md:text-[3.1rem] ${text}`}>
          {title}
        </h2>
      </Reveal>
      {lead && (
        <Reveal delay={0.1}>
          <p className={`mt-5 text-pretty text-base leading-relaxed md:text-lg ${soft}`}>{lead}</p>
        </Reveal>
      )}
    </div>
  );
}
