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

// Birevim tarzı başlık: kırmızı etiket + kısa çizgi + kalın başlık + gri alt metin.
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
  const text = isDark ? "text-paper" : "text-ink";
  const soft = isDark ? "text-paper/60" : "text-ink/55";

  return (
    <div className={`${isCenter ? "mx-auto max-w-2xl text-center" : "max-w-2xl"} ${className}`}>
      {eyebrow && (
        <Reveal>
          <div className={`flex items-center gap-2.5 ${isCenter ? "justify-center" : ""}`}>
            <span className="h-0.5 w-6 rounded bg-accent" />
            <span className="eyebrow text-accent">{eyebrow}</span>
          </div>
        </Reveal>
      )}
      <Reveal delay={0.05}>
        <h2 className={`mt-4 text-3xl leading-[1.08] sm:text-4xl md:text-5xl ${text}`}>{title}</h2>
      </Reveal>
      {lead && (
        <Reveal delay={0.1}>
          <p className={`mt-4 text-base leading-relaxed md:text-lg ${soft}`}>{lead}</p>
        </Reveal>
      )}
    </div>
  );
}
