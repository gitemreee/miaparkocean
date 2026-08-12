import type { ReactNode } from "react";
import { SmartImage } from "@/components/ui/SmartImage";
import { WaveEdge } from "@/components/ui/Wave";

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
    <section className="relative flex min-h-[46vh] items-end overflow-hidden pt-24 md:min-h-[58vh] md:pt-28">
      <div className="absolute inset-0">
        <SmartImage src={image} alt="" priority sizes="100vw" className="h-full w-full scale-105 object-cover" />
        <div className="absolute inset-0 bg-[linear-gradient(to_top,rgba(4,40,58,0.26)_0%,rgba(4,40,58,0.6)_8%,rgba(4,40,58,0.9)_17%,rgba(6,64,90,0.64)_46%,rgba(26,116,150,0.26)_76%,rgba(44,148,180,0.2)_100%)]" />
      </div>

      <div className="container-luxe relative z-10 pb-16 md:pb-28">
        <div className="flex items-center gap-3">
          <span className="h-[3px] w-9 rounded-full bg-gradient-surf" aria-hidden="true" />
          <span className="eyebrow text-ice">{eyebrow}</span>
        </div>
        <h1 className="mt-5 max-w-3xl text-balance text-[1.85rem] leading-[1.1] text-cream sm:text-4xl md:text-[3.6rem]">
          {title}
        </h1>
        {lead && <p className="mt-4 max-w-2xl text-pretty text-[0.95rem] leading-relaxed text-ice/80 md:mt-6 md:text-lg">{lead}</p>}
      </div>

      {/* İmza dalga — logodaki dalganın kendisi */}
      <div className="pointer-events-none absolute inset-x-0 bottom-0">
        <WaveEdge className="h-[52px] md:h-[92px]" />
      </div>
    </section>
  );
}
