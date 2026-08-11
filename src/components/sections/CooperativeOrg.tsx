import { Reveal } from "@/components/ui/Reveal";
import { YkbLogo } from "@/components/layout/YkbLogo";
import { cooperativeOrg } from "@/data/cooperative";

export function CooperativeOrg() {
  return (
    <section id="kooperatif-hakkinda" className="bg-pearl py-24 md:py-32">
      <div className="container-luxe grid gap-14 lg:grid-cols-[0.9fr_1.1fr] lg:items-center">
        {/* Logo + künye */}
        <Reveal>
          <div className="rounded-[2rem] bg-cream p-10 shadow-[var(--shadow-card)]">
            <YkbLogo className="mx-auto h-40 w-auto text-ocean" />
            <div className="gold-rule mt-8" />
            <dl className="mt-8 grid grid-cols-2 gap-6">
              {cooperativeOrg.facts.map((f) => (
                <div key={f.label}>
                  <dt className="eyebrow text-[0.58rem] text-ocean/45">{f.label}</dt>
                  <dd className="mt-1 font-display text-lg tabular-nums text-ocean">{f.value}</dd>
                </div>
              ))}
              <div className="col-span-2 border-t border-ocean/10 pt-5">
                <dt className="eyebrow text-[0.58rem] text-ocean/45">Adres</dt>
                <dd className="mt-1 text-sm leading-relaxed text-ocean/75">{cooperativeOrg.address}</dd>
              </div>
            </dl>
          </div>
        </Reveal>

        {/* Metin */}
        <div>
          <Reveal>
            <div className="flex items-center gap-3">
              <span className="gold-rule-solid w-8" />
              <span className="eyebrow text-bronze">Yapımcı</span>
            </div>
          </Reveal>
          <Reveal delay={0.05}>
            <h2 className="mt-5 text-3xl leading-tight text-ocean md:text-4xl">
              {cooperativeOrg.name}
            </h2>
          </Reveal>
          <Reveal delay={0.1}>
            <p className="mt-3 text-lg font-medium text-bronze">{cooperativeOrg.lead}</p>
          </Reveal>
          <div className="mt-6 space-y-4">
            {cooperativeOrg.paragraphs.map((p, i) => (
              <Reveal key={p.slice(0, 20)} delay={0.12 + i * 0.05}>
                <p className="text-base leading-relaxed text-ocean/75">{p}</p>
              </Reveal>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
