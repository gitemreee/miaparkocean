import Link from "next/link";
import { ArrowRight, Check } from "lucide-react";
import { Reveal } from "@/components/ui/Reveal";
import { SmartImage } from "@/components/ui/SmartImage";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { units } from "@/data/units";

export function UnitTypes() {
  return (
    <section id="daireler" className="bg-paper py-20 md:py-28">
      <div className="container-luxe">
        <SectionHeading
          eyebrow="Daire Tipleri"
          title={<>Size <span className="gilded">uygun daireyi</span> seçin</>}
          lead="1+0 stüdyodan bahçeli 2+1 dublekse kadar üç farklı daire; ihtiyacınıza ve bütçenize göre seçebileceğiniz üç yaşam biçimi."
        />

        <div className="mt-14 grid items-stretch gap-6 lg:grid-cols-3">
          {units.map((u, i) => {
            return (
              <Reveal key={u.slug} delay={i * 0.1}>
                <div className="relative flex h-full flex-col overflow-hidden rounded-3xl border border-ink/10 bg-white shadow-[var(--shadow-card)] transition-transform duration-300 hover:-translate-y-1">
                  <div className="relative aspect-[16/10] overflow-hidden">
                    <SmartImage src={u.image} alt={`${u.name} — MİA PARK OCEAN`} sizes="(max-width:1024px) 100vw, 33vw" className="h-full w-full object-cover" />
                  </div>

                  <div className="flex flex-1 flex-col p-7">
                    <div className="flex items-center gap-2">
                      <span className="rounded-lg bg-accent-tint px-2.5 py-1 text-sm font-bold text-accent">{u.type}</span>
                      <span className="text-sm text-ink/50">{u.count} adet</span>
                    </div>
                    <div className="mt-4 flex items-end gap-1.5">
                      <span className="font-display text-5xl font-bold text-ink">{u.areaValue}</span>
                      <span className="mb-1.5 text-lg font-semibold text-ink/50">m²</span>
                      <span className="mb-2 text-xs font-medium text-ink/40">brüt</span>
                    </div>
                    <h3 className="mt-1 text-xl font-bold text-ink">{u.name}</h3>
                    <p className="mt-1 text-sm font-semibold text-accent">{u.tagline}</p>

                    <ul className="mt-5 space-y-2.5">
                      {u.features.slice(0, 4).map((f) => (
                        <li key={f} className="flex items-start gap-2.5 text-sm text-ink/70">
                          <Check className="mt-0.5 h-4 w-4 shrink-0 text-accent" strokeWidth={2.5} /> {f}
                        </li>
                      ))}
                    </ul>

                    <div className="mt-6 flex-1" />
                    <Link
                      href={`/daireler#${u.slug}`}
                      className="inline-flex items-center justify-center gap-2 rounded-full bg-accent px-6 py-3.5 text-sm font-semibold text-white transition-colors hover:bg-accent-600"
                    >
                      Detayları İncele <ArrowRight className="h-4 w-4" />
                    </Link>
                  </div>
                </div>
              </Reveal>
            );
          })}
        </div>

        <Reveal delay={0.15}>
          <p className="mt-8 text-center text-sm text-ink/55">
            Tüm daireler <span className="font-semibold text-ink">60 aya varan · sıfır faiz</span> ödeme imkânıyla. Kefil yok, banka yok, faiz yok.
          </p>
        </Reveal>
      </div>
    </section>
  );
}
