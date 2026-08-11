import { Reveal } from "@/components/ui/Reveal";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { Icon } from "@/components/ui/Icon";
import { legalAssurance } from "@/data/cooperative";

export function LegalAssurance() {
  return (
    <section id="guvence" className="bg-paper py-20 md:py-28">
      <div className="container-luxe">
        <SectionHeading
          eyebrow="Yasal Güvence ve Denetim"
          title={<>Devlet <span className="gilded">gözetiminde</span>, kanunla güvence altında</>}
          lead={legalAssurance.lead}
        />

        <div className="mt-14 grid gap-5 md:grid-cols-2 lg:grid-cols-3">
          {legalAssurance.cards.map((c, i) => (
            <Reveal key={c.title} delay={(i % 3) * 0.08}>
              <div className="group h-full rounded-2xl border border-ink/10 bg-white p-7 transition-all duration-300 hover:-translate-y-1 hover:border-accent/40 hover:shadow-[var(--shadow-card)]">
                <span className="flex h-12 w-12 items-center justify-center rounded-xl bg-accent-tint text-accent transition-colors group-hover:bg-accent group-hover:text-white">
                  <Icon name={c.icon} className="h-6 w-6" />
                </span>
                <h3 className="mt-5 text-xl font-bold text-ink">{c.title}</h3>
                <p className="mt-3 text-sm leading-relaxed text-ink/60">{c.text}</p>
              </div>
            </Reveal>
          ))}
        </div>

        <Reveal delay={0.1}>
          <p className="mx-auto mt-10 max-w-2xl text-center text-xs leading-relaxed text-ink/45">{legalAssurance.disclaimer}</p>
        </Reveal>
      </div>
    </section>
  );
}
