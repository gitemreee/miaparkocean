import type { ReactNode } from "react";
import { SmartImage } from "@/components/ui/SmartImage";
import { WAVE_PATHS } from "@/components/ui/Wave";

type PageHeroProps = {
  eyebrow: string;
  title: ReactNode;
  lead?: string;
  image: string;
};

/**
 * İç sayfa başlığı — sabit beyaz header'ın altına yerleşir, alt kenarı
 * logodaki dalgayla beyaz sayfaya bağlanır.
 */
export function PageHero({ eyebrow, title, lead, image }: PageHeroProps) {
  return (
    <section className="relative flex min-h-[58vh] items-end overflow-hidden pt-28">
      <div className="absolute inset-0">
        <SmartImage src={image} alt="" priority sizes="100vw" className="h-full w-full scale-105 object-cover" />
        <div className="absolute inset-0 bg-[linear-gradient(to_top,rgba(0,9,38,0.94)_0%,rgba(4,17,58,0.68)_42%,rgba(15,82,186,0.26)_74%,rgba(1,50,32,0.24)_100%)]" />
      </div>

      <div className="container-luxe relative z-10 pb-24 md:pb-28">
        <div className="flex items-center gap-3">
          <span className="h-[3px] w-9 rounded-full bg-gradient-surf" aria-hidden="true" />
          <span className="eyebrow text-ice">{eyebrow}</span>
        </div>
        <h1 className="mt-5 max-w-3xl text-balance text-[2.3rem] leading-[1.06] text-cream sm:text-5xl md:text-[3.6rem]">
          {title}
        </h1>
        {lead && <p className="mt-6 max-w-2xl text-pretty text-lg leading-relaxed text-ice/80">{lead}</p>}
      </div>

      {/* İmza dalga */}
      <svg
        viewBox="0 0 1440 120"
        preserveAspectRatio="none"
        className="pointer-events-none absolute inset-x-0 bottom-0 block h-[42px] w-full md:h-[68px]"
        aria-hidden="true"
      >
        <path d={WAVE_PATHS.back} fill="#dff0f7" opacity="0.6" />
        <path d={WAVE_PATHS.mid} fill="#f2fafd" opacity="0.9" />
        <path d={WAVE_PATHS.front} fill="#ffffff" />
      </svg>
    </section>
  );
}
