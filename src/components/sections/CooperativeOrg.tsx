import { Reveal } from "@/components/ui/Reveal";
import { YkbLogo } from "@/components/layout/YkbLogo";
import { cooperativeOrg } from "@/data/cooperative";

export function CooperativeOrg() {
  return (
    <section id="kooperatif-hakkinda" className="surface-tint py-12 md:py-24">
      <div className="container-luxe grid gap-8 md:gap-12 lg:grid-cols-[0.9fr_1.1fr] lg:items-center">
        {/* Logo + künye */}
        <Reveal>
          <div className="card-luxe p-5 md:p-8">
            <YkbLogo className="mx-auto h-24 w-auto text-ink md:h-32" />
            <div className="gold-rule mt-5 md:mt-7" />
            <dl className="mt-5 grid grid-cols-2 gap-x-5 gap-y-4 md:mt-7 md:gap-6">
              {cooperativeOrg.facts.map((f) => (
                <div key={f.label}>
                  <dt className="eyebrow text-[0.54rem] text-ink/45">{f.label}</dt>
                  <dd className="mt-0.5 font-display text-[0.98rem] tabular-nums text-ink md:text-lg">{f.value}</dd>
                </div>
              ))}
              <div className="col-span-2 border-t border-ink/10 pt-4 md:pt-5">
                <dt className="eyebrow text-[0.54rem] text-ink/45">Adres</dt>
                <dd className="mt-1 text-[0.82rem] leading-relaxed text-ink/70 md:text-sm">{cooperativeOrg.address}</dd>
              </div>
            </dl>
          </div>
        </Reveal>

        {/* Metin */}
        <div>
          <Reveal>
            <div className="flex items-center gap-3">
              <span className="gold-rule-solid w-8" />
              <span className="eyebrow text-accent">Yapımcı</span>
            </div>
          </Reveal>
          <Reveal delay={0.05}>
            <h2 className="mt-3 font-display text-[1.6rem] leading-tight text-ink md:mt-5 md:text-4xl">
              {cooperativeOrg.name}
            </h2>
          </Reveal>
          <Reveal delay={0.1}>
            <p className="mt-2 text-[0.95rem] font-medium text-accent md:mt-3 md:text-lg">{cooperativeOrg.lead}</p>
          </Reveal>
          <div className="mt-4 space-y-3 md:mt-6 md:space-y-4">
            {cooperativeOrg.paragraphs.map((p, i) => (
              <Reveal key={p.slice(0, 20)} delay={0.12 + i * 0.05}>
                <p className="text-[0.88rem] leading-relaxed text-ink/70 md:text-base">{p}</p>
              </Reveal>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
