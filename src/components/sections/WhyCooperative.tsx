import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { Reveal } from "@/components/ui/Reveal";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { Icon } from "@/components/ui/Icon";
import { whyCooperative } from "@/data/cooperative";

export function WhyCooperative() {
  return (
    <section id="neden-kooperatif" className="bg-cream py-14 md:py-28">
      <div className="container-luxe">
        <SectionHeading
          eyebrow="Neden Kooperatif?"
          title={<>Aklınızdaki soruların <span className="gilded">net cevabı</span></>}
          lead={whyCooperative.lead}
        />

        <div className="mt-16 grid gap-6 md:grid-cols-2">
          {whyCooperative.points.map((p, i) => (
            <Reveal key={p.title} delay={i * 0.08}>
              <div className="flex h-full gap-3.5 rounded-2xl md:gap-5 border border-ocean/8 bg-pearl p-4 md:p-7">
                <span className="icon-tile h-11 w-11 items-center justify-center rounded-xl md:h-14 md:w-14 md:rounded-2xl">
                  <Icon name={p.icon} className="h-5 w-5 md:h-7 md:w-7" />
                </span>
                <div>
                  <h3 className="text-[1.02rem] leading-snug text-ocean md:text-xl">{p.title}</h3>
                  <p className="mt-1.5 text-[0.82rem] leading-relaxed text-ocean/70 md:mt-2 md:text-sm">{p.text}</p>
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
