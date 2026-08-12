import { Reveal } from "@/components/ui/Reveal";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { Icon } from "@/components/ui/Icon";
import { legalAssurance } from "@/data/cooperative";

export function LegalAssurance() {
  return (
    <section id="guvence" className="surface-paper py-12 md:py-24">
      <div className="container-luxe">
        <SectionHeading
          eyebrow="Yasal Güvence ve Denetim"
          title={<>Devlet <span className="gilded">gözetiminde</span>, kanunla güvence altında</>}
          lead={legalAssurance.lead}
        />

        <div className="mt-10 grid grid-cols-2 gap-3 md:mt-14 md:gap-5 lg:grid-cols-3">
          {legalAssurance.cards.map((c, i) => (
            <Reveal key={c.title} delay={(i % 3) * 0.08}>
              <div className="card-luxe group h-full p-4 md:p-7">
                <span className="icon-tile h-10 w-10 items-center justify-center rounded-xl md:h-12 md:w-12">
                  <Icon name={c.icon} className="h-5 w-5 md:h-6 md:w-6" />
                </span>
                <h3 className="mt-3 text-[0.98rem] font-bold leading-snug text-ink md:mt-5 md:text-xl">{c.title}</h3>
                <p className="mt-1.5 text-[0.8rem] leading-relaxed text-ink/60 md:mt-3 md:text-sm">{c.text}</p>
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
