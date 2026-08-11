import type { ReactNode } from "react";
import { SmartImage } from "@/components/ui/SmartImage";

type PageHeroProps = {
  eyebrow: string;
  title: ReactNode;
  lead?: string;
  image: string;
};

// İç sayfalar için kompakt başlık bloğu (sabit header'ın altına yerleşir).
export function PageHero({ eyebrow, title, lead, image }: PageHeroProps) {
  return (
    <section className="relative flex min-h-[52vh] items-end overflow-hidden pt-28">
      <div className="absolute inset-0">
        <SmartImage src={image} alt="" priority sizes="100vw" className="h-full w-full object-cover" />
        <div className="absolute inset-0 bg-gradient-to-t from-ocean via-ocean/60 to-ocean/40" />
      </div>
      <div className="container-luxe relative z-10 pb-14">
        <div className="flex items-center gap-3">
          <span className="gold-rule-solid w-10" />
          <span className="eyebrow text-bronze-100">{eyebrow}</span>
        </div>
        <h1 className="mt-5 max-w-3xl text-4xl leading-tight text-cream md:text-6xl">{title}</h1>
        {lead && <p className="mt-5 max-w-2xl text-lg leading-relaxed text-cream/80">{lead}</p>}
      </div>
    </section>
  );
}
