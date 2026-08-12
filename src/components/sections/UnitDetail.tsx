import Link from "next/link";
import { ArrowRight, Check, Maximize2, Building2, Layers } from "lucide-react";
import { Reveal } from "@/components/ui/Reveal";
import { SmartImage } from "@/components/ui/SmartImage";
import type { Unit } from "@/data/units";

export function UnitDetail({ unit, index }: { unit: Unit; index: number }) {
  const flip = index % 2 === 1;

  return (
    <section
      id={unit.slug}
      className={`scroll-mt-24 py-12 md:py-24 ${index % 2 === 1 ? "bg-pearl" : "bg-cream"}`}
    >
      <div className="container-luxe grid items-center gap-12 lg:grid-cols-2">
        {/* Görsel */}
        <Reveal className={flip ? "lg:order-2" : ""}>
          <div className="relative">
            <div className="overflow-hidden rounded-[2rem] shadow-[var(--shadow-luxe)]">
              <div className="aspect-[4/3]">
                <SmartImage
                  src={unit.image}
                  alt={`${unit.name} — MİA PARK OCEAN`}
                  sizes="(max-width: 1024px) 100vw, 50vw"
                  className="h-full w-full object-cover"
                />
              </div>
            </div>
            {/* Plan küçük görseli */}
            <div className="absolute -bottom-6 right-4 w-40 overflow-hidden rounded-xl border-4 border-cream bg-cream shadow-[var(--shadow-card)] sm:w-52">
              <div className="aspect-[4/3]">
                <SmartImage
                  src={unit.planImage}
                  alt={`${unit.type} örnek kat planı`}
                  sizes="200px"
                  className="h-full w-full object-cover"
                />
              </div>
            </div>
          </div>
        </Reveal>

        {/* Metin */}
        <div className={flip ? "lg:order-1" : ""}>
          <Reveal>
            <div className="flex flex-wrap items-center gap-3">
              <span className="rounded-full bg-bronze px-4 py-1.5 font-display text-lg text-cream">{unit.type}</span>
              <span className="inline-flex items-center gap-1.5 text-sm font-medium text-ocean/70">
                <Maximize2 className="h-4 w-4 text-bronze" /> {unit.area}
              </span>
              <span className="inline-flex items-center gap-1.5 text-sm font-medium text-ocean/70">
                <Building2 className="h-4 w-4 text-bronze" /> {unit.count} adet
              </span>
            </div>
          </Reveal>
          <Reveal delay={0.05}>
            <h2 className="mt-5 text-3xl text-ocean md:text-4xl">{unit.name}</h2>
            <p className="mt-2 text-lg font-medium text-bronze">{unit.tagline}</p>
          </Reveal>
          <Reveal delay={0.1}>
            <p className="mt-5 text-base leading-relaxed text-ocean/75">{unit.summary}</p>
          </Reveal>

          <div className="mt-7 grid gap-4 sm:grid-cols-2">
            {unit.highlights.map((h, i) => (
              <Reveal key={h.title} delay={0.12 + i * 0.05}>
                <div className="rounded-xl border border-ocean/8 bg-cream/60 p-4">
                  <div className="flex items-center gap-2">
                    <Layers className="h-4 w-4 text-bronze" />
                    <h3 className="text-base text-ocean">{h.title}</h3>
                  </div>
                  <p className="mt-1.5 text-sm leading-relaxed text-ocean/65">{h.text}</p>
                </div>
              </Reveal>
            ))}
          </div>

          <Reveal delay={0.2}>
            <ul className="mt-6 grid gap-2 sm:grid-cols-2">
              {unit.features.map((f) => (
                <li key={f} className="flex items-center gap-2 text-sm text-ocean/75">
                  <Check className="h-4 w-4 shrink-0 text-bronze" strokeWidth={2.2} /> {f}
                </li>
              ))}
            </ul>
          </Reveal>

          <Reveal delay={0.25}>
            <Link
              href="/iletisim"
              className="mt-8 inline-flex items-center gap-2 rounded-full bg-bronze px-8 py-4 text-sm font-medium text-cream transition-colors hover:bg-bronze-300"
            >
              Bu Daireyi Seç <ArrowRight className="h-4 w-4" />
            </Link>
          </Reveal>
        </div>
      </div>
    </section>
  );
}
