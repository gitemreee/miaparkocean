import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { Reveal } from "@/components/ui/Reveal";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { Icon } from "@/components/ui/Icon";
import { whyCooperative } from "@/data/cooperative";

export function WhyCooperative() {
  return (
    <section id="neden-kooperatif" className="bg-cream py-24 md:py-32">
      <div className="container-luxe">
        <SectionHeading
          eyebrow="Neden Kooperatif?"
          title={<>Aklınızdaki soruların <span className="gilded">net cevabı</span></>}
          lead={whyCooperative.lead}
        />

        <div className="mt-16 grid gap-6 md:grid-cols-2">
          {whyCooperative.points.map((p, i) => (
            <Reveal key={p.title} delay={i * 0.08}>
              <div className="flex h-full gap-5 rounded-2xl border border-ocean/8 bg-pearl p-7">
                <span className="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-gradient-surf">
                  <Icon name={p.icon} className="h-7 w-7 text-bronze-300" />
                </span>
                <div>
                  <h3 className="text-xl text-ocean">{p.title}</h3>
                  <p className="mt-2 text-sm leading-relaxed text-ocean/70">{p.text}</p>
                </div>
              </div>
            </Reveal>
          ))}
        </div>

        <Reveal delay={0.15}>
          <div className="mt-12 text-center">
            <Link
              href="/bilgi-merkezi#guven"
              className="inline-flex items-center gap-2 rounded-full border border-bronze/50 px-8 py-4 text-sm font-medium text-bronze transition-colors hover:bg-bronze hover:text-cream"
            >
              Güvence ve Denetim Detayları <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
        </Reveal>
      </div>
    </section>
  );
}
