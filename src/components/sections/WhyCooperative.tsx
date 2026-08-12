import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { Reveal } from "@/components/ui/Reveal";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { Icon } from "@/components/ui/Icon";
import { whyCooperative } from "@/data/cooperative";

export function WhyCooperative() {
  return (
    <section id="neden-kooperatif" className="surface-tint py-12 md:py-24">
      <div className="container-luxe">
        <SectionHeading
          eyebrow="Neden Kooperatif?"
          title={<>Aklınızdaki soruların <span className="gradient-text">net cevabı</span></>}
          lead={whyCooperative.lead}
        />

        <div className="mt-8 grid gap-3 md:mt-14 md:grid-cols-2 md:gap-6">
          {whyCooperative.points.map((p, i) => (
            <Reveal key={p.title} delay={i * 0.08}>
              <div className="card-luxe flex h-full gap-3 p-3.5 md:gap-5 md:p-6">
                <span className="icon-tile h-9 w-9 shrink-0 items-center justify-center rounded-lg md:h-13 md:w-13 md:rounded-2xl">
                  <Icon name={p.icon} className="h-4 w-4 md:h-6 md:w-6" />
                </span>
                <div>
                  <h3 className="font-display text-[0.98rem] leading-snug text-ink md:text-xl">{p.title}</h3>
                  <p className="mt-1 text-[0.8rem] leading-snug text-ink/65 md:mt-2 md:text-sm md:leading-relaxed">{p.text}</p>
                </div>
              </div>
            </Reveal>
          ))}
        </div>

        <Reveal delay={0.15}>
          <div className="mt-8 text-center md:mt-12">
            <Link
              href="/bilgi-merkezi#guven"
              className="btn-base btn-outline px-6 py-3 text-sm md:px-8 md:py-4"
            >
              Güvence ve Denetim Detayları <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
        </Reveal>
      </div>
    </section>
  );
}
