import { TrendingUp, Info, ArrowUpRight } from "lucide-react";
import { Reveal } from "@/components/ui/Reveal";
import { WaveDivider, WaveSectionEnd } from "@/components/ui/Wave";
import { valuation } from "@/data/valuation";

export function Valuation() {
  return (
    <section id="degerleme" className="section-dark wave-clip-end">
      {/* Beyaz sayfadan okyanusa dalga geçişi */}
      <WaveDivider flip className="h-[52px] md:h-[84px]" />

      <div className="container-luxe relative z-10 py-16 text-white md:py-24">
        <Reveal>
          <div className="flex items-center gap-2.5">
            <span className="h-0.5 w-6 rounded bg-accent" />
            <span className="eyebrow text-accent-300">{valuation.eyebrow}</span>
          </div>
        </Reveal>

        <div className="mt-8 grid gap-12 lg:grid-cols-[1fr_1.05fr] lg:items-end">
          {/* Sol: dev güncel değer + öngörü */}
          <div>
            <Reveal>
              <h2 className="text-4xl leading-[1.05] text-white sm:text-5xl md:text-6xl">{valuation.title}</h2>
            </Reveal>
            <Reveal delay={0.05}>
              <p className="mt-5 max-w-lg text-lg text-white/65">{valuation.lead}</p>
            </Reveal>

            <Reveal delay={0.1}>
              <div className="mt-9 flex flex-wrap items-end gap-x-4 gap-y-2">
                <span className="font-display text-6xl leading-none text-white md:text-7xl">{valuation.headline.value}</span>
                <span className="mb-1 font-display text-2xl text-accent-300">{valuation.headline.unit}</span>
              </div>
              <p className="mt-2 text-sm uppercase tracking-wider text-white/50">{valuation.headline.label}</p>
            </Reveal>

            <Reveal delay={0.15}>
              <div className="mt-6 inline-flex items-center gap-2 rounded-full bg-accent px-5 py-2.5 text-sm font-semibold text-white">
                <TrendingUp className="h-4 w-4" /> {valuation.forecast.value} {valuation.forecast.label}
              </div>
            </Reveal>
          </div>

          {/* Sağ: 5 yıllık projeksiyon grafiği */}
          <Reveal delay={0.1}>
            <div className="rounded-3xl border border-white/12 bg-white/[0.06] p-6 md:p-7">
              <div className="flex items-center justify-between">
                <span className="text-sm font-semibold text-white/85">5 Yıllık Değer Projeksiyonu (₺/m²)</span>
                <span className="inline-flex items-center gap-1 rounded-full bg-accent/20 px-2.5 py-1 text-xs font-bold text-accent-300">
                  <ArrowUpRight className="h-3.5 w-3.5" /> +%205
                </span>
              </div>

              {/* Barlar */}
              <div className="mt-8 flex h-60 items-end gap-2 md:gap-3">
                {valuation.projection.map((p) => (
                  <div key={p.year} className="flex h-full flex-1 items-end">
                    <div
                      className="relative w-full rounded-t-lg bg-gradient-to-t from-accent to-accent-300"
                      style={{ height: `${p.h}%` }}
                    >
                      <span className="absolute inset-x-0 top-1.5 text-center text-[0.6rem] font-bold text-white md:text-xs">
                        {p.price}
                      </span>
                    </div>
                  </div>
                ))}
              </div>

              {/* Yıl etiketleri */}
              <div className="mt-2 flex gap-2 border-t border-white/10 pt-2 md:gap-3">
                {valuation.projection.map((p) => (
                  <div key={p.year} className="flex-1 text-center">
                    <div className="text-[0.62rem] text-white/55">{p.year}</div>
                    {p.label && <div className="text-[0.55rem] font-semibold text-accent-300">{p.label}</div>}
                  </div>
                ))}
              </div>

              <p className="mt-4 text-[0.65rem] leading-relaxed text-white/35">{valuation.projectionNote}</p>
            </div>
          </Reveal>
        </div>

        {/* Değer artışı metrikleri */}
        <div className="mt-12 grid gap-4 sm:grid-cols-3">
          {valuation.changes.map((m, i) => (
            <Reveal key={m.label} delay={i * 0.08}>
              <div className="rounded-2xl border border-white/12 bg-white/[0.06] p-5 md:p-6">
                <div className="flex items-center gap-2">
                  <ArrowUpRight className="h-6 w-6 text-accent-300" />
                  <div className="font-display text-4xl text-white md:text-5xl">{m.value}</div>
                </div>
                <div className="mt-2 text-sm font-semibold text-white/85">{m.label}</div>
                <div className="text-xs text-white/40">{m.note}</div>
              </div>
            </Reveal>
          ))}
        </div>

        <Reveal>
          <div className="mt-8 flex items-center gap-2 text-xs text-white/40">
            <Info className="h-3.5 w-3.5" /> {valuation.source}
          </div>
        </Reveal>
      </div>

      {/* Okyanustan beyaz sayfaya geri dönüş */}
      <WaveSectionEnd className="h-[52px] md:h-[84px]" />
    </section>
  );
}
