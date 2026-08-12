import Link from "next/link";
import { ArrowRight, Check } from "lucide-react";
import { Reveal } from "@/components/ui/Reveal";
import { SmartImage } from "@/components/ui/SmartImage";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { units } from "@/data/units";

export function UnitTypes() {
  return (
    <section id="daireler" className="surface-paper py-12 md:py-24">
      <div className="container-luxe">
        <SectionHeading
          eyebrow="Daire Tipleri"
          title={<>Size <span className="gilded">uygun daireyi</span> seçin</>}
          lead="1+0 stüdyodan bahçeli 2+1 dublekse kadar dört farklı daire; ihtiyacınıza ve bütçenize göre seçebileceğiniz dört yaşam biçimi."
        />

        <div className="mt-10 grid grid-cols-2 items-stretch gap-3 md:mt-14 md:gap-6 lg:grid-cols-4">
          {units.map((u, i) => {
            return (
              <Reveal key={u.slug} delay={i * 0.1}>
                <div className="card-luxe flex h-full flex-col overflow-hidden">
                  <div className="relative aspect-[16/10] overflow-hidden">
                    <SmartImage src={u.image} alt={`${u.name} — MİA PARK OCEAN`} sizes="(max-width:1024px) 100vw, 33vw" className="h-full w-full object-cover" />
                  </div>

                  <div className="flex flex-1 flex-col p-4 md:p-6">
                    <div className="flex flex-wrap items-center gap-1.5">
                      <span className="rounded-lg bg-accent-tint px-2 py-0.5 text-xs font-bold text-accent md:px-2.5 md:py-1 md:text-sm">
                        {u.type}
                      </span>
                      <span className="text-xs text-ink/50 md:text-sm">{u.count} adet</span>
                    </div>
                    <div className="mt-2.5 flex items-end gap-1 md:mt-4 md:gap-1.5">
                      <span className="font-display text-3xl text-ink md:text-5xl">{u.areaValue}</span>
                      <span className="mb-0.5 text-sm font-semibold text-ink/50 md:mb-1.5 md:text-lg">m²</span>
                      <span className="mb-1 hidden text-xs font-medium text-ink/40 md:mb-2 md:inline">brüt</span>
                    </div>
                    <h3 className="mt-1 text-[0.98rem] font-bold leading-snug text-ink md:text-xl">{u.name}</h3>
                    <p className="mt-1 text-xs font-semibold text-accent md:text-sm">{u.tagline}</p>

                    {/* Özellik listesi mobilde gizli — kart yüksekliğini üçe katlıyordu */}
                    <ul className="mt-5 hidden space-y-2.5 md:block">
                      {u.features.slice(0, 4).map((f) => (
                        <li key={f} className="flex items-start gap-2.5 text-sm text-ink/70">
                          <Check className="mt-0.5 h-4 w-4 shrink-0 text-accent" strokeWidth={2.5} /> {f}
                        </li>
                      ))}
                    </ul>

                    <div className="mt-3 flex-1 md:mt-6" />
                    <Link
                      href={`/daireler#${u.slug}`}
                      className="btn-base btn-jade px-3 py-2.5 text-xs md:px-6 md:py-3.5 md:text-sm"
                    >
                      <span className="md:hidden">İncele</span>
                      <span className="hidden md:inline">Detayları İncele</span>
                      <ArrowRight className="h-3.5 w-3.5 md:h-4 md:w-4" />
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
