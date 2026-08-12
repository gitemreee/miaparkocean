import { Users, Info } from "lucide-react";
import { Reveal } from "@/components/ui/Reveal";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { demographics } from "@/data/valuation";

export function Demographics() {
  return (
    <section id="demografi" className="surface-paper py-12 md:py-24">
      <div className="container-luxe">
        <SectionHeading eyebrow={demographics.eyebrow} title={demographics.title} lead={demographics.lead} />

        <div className="mt-10 grid grid-cols-2 gap-3 md:mt-12 md:gap-4 lg:grid-cols-4">
          {demographics.tiles.map((t, i) => (
            <Reveal key={t.label} delay={i * 0.07}>
              <div className="card-luxe h-full p-4 md:p-6">
                <span className="icon-tile h-9 w-9 items-center justify-center rounded-lg md:h-11 md:w-11 md:rounded-xl">
                  <Users className="h-4 w-4 md:h-5 md:w-5" />
                </span>
                <div className="mt-3 font-display text-[1.6rem] leading-none text-ink md:mt-4 md:text-4xl">{t.value}</div>
                <div className="mt-1.5 text-[0.82rem] font-semibold leading-snug text-ink/80 md:text-sm">{t.label}</div>
                <div className="text-[0.7rem] text-ink/45 md:text-xs">{t.note}</div>
              </div>
            </Reveal>
          ))}
        </div>

        {/* Yaş dağılımı çubuğu */}
        <Reveal delay={0.1}>
          <div className="card-luxe mt-6 p-5 md:p-6">
            <div className="flex items-center justify-between">
              <span className="text-sm font-semibold text-ink">Yaş Dağılımı</span>
              <span className="text-xs text-ink/45">İzmit</span>
            </div>
            <div className="mt-4 flex h-4 overflow-hidden rounded-full">
              <div className="bg-accent" style={{ width: `${demographics.ageBands[0].percent}%` }} title="Genç" />
              <div className="bg-accent-300" style={{ width: `${demographics.ageBands[1].percent}%` }} title="Orta" />
              <div className="bg-ink/25" style={{ width: `${demographics.ageBands[2].percent}%` }} title="Yaşlı" />
            </div>
            <div className="mt-3 flex flex-wrap gap-x-6 gap-y-1 text-sm">
              {demographics.ageBands.map((b, i) => (
                <span key={b.band} className="flex items-center gap-2 text-ink/70">
                  <span className={`h-2.5 w-2.5 rounded-full ${i === 0 ? "bg-accent" : i === 1 ? "bg-accent-300" : "bg-ink/25"}`} />
                  {b.band} <span className="font-semibold text-ink">%{b.percent.toString().replace(".", ",")}</span>
                </span>
              ))}
            </div>
          </div>
        </Reveal>

        <Reveal>
          <div className="mt-6 flex items-center gap-2 text-xs text-ink/40">
            <Info className="h-3.5 w-3.5" /> {demographics.source}
          </div>
        </Reveal>
      </div>
    </section>
  );
}
