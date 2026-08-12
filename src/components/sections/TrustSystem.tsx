import { ShieldCheck } from "lucide-react";
import { Reveal } from "@/components/ui/Reveal";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { trustSystem } from "@/data/cooperative";

export function TrustSystem() {
  return (
    <section id="guvence-sistemi" className="surface-tint py-14 md:py-28">
      <div className="container-luxe">
        <SectionHeading
          eyebrow="Güvence ve Denetim Sistemi"
          title={<>14 kontrolde <span className="gilded">kurumsal güven</span></>}
          lead={trustSystem.lead}
        />

        <Reveal>
          <div className="mx-auto mt-8 flex w-fit items-center gap-2 rounded-full border border-bronze/30 bg-cream px-5 py-2">
            <ShieldCheck className="h-4 w-4 text-bronze" />
            <span className="text-xs font-medium text-ocean/70">{trustSystem.status}</span>
          </div>
        </Reveal>

        <div className="mt-14 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {trustSystem.controls.map((c, i) => (
            <Reveal key={c.n} delay={(i % 3) * 0.06}>
              <div className="flex h-full gap-4 rounded-2xl border border-ocean/8 bg-cream p-6 transition-colors hover:border-bronze/40">
                <span className="font-display text-3xl leading-none text-bronze/40">
                  {String(c.n).padStart(2, "0")}
                </span>
                <div>
                  <h3 className="text-base font-semibold text-ocean">{c.title}</h3>
                  <p className="mt-1.5 text-sm leading-relaxed text-ocean/65">{c.text}</p>
                </div>
              </div>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}
