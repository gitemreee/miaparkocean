import { Newspaper, TrendingUp, ArrowUpRight } from "lucide-react";
import { Reveal } from "@/components/ui/Reveal";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { regionIntro, press } from "@/data/region";

export function Region() {
  // Yalnızca gerçek link eklenmiş haberler gösterilir.
  const verifiedPress = press.filter((p) => p.verified && p.href !== "#");

  return (
    <section id="bolge" className="surface-tint py-14 md:py-28">
      <div className="container-luxe">
        <SectionHeading
          eyebrow="Değerlenen Bölge"
          title={<>İzmit MİA: <span className="gilded">doğru yerden, doğru zamanda</span></>}
          lead={regionIntro.paragraphs[0]}
        />

        {/* Avantajlar */}
        <div className="mt-10 grid grid-cols-2 gap-3 md:mt-14 md:gap-5 lg:grid-cols-4">
          {regionIntro.advantages.map((a, i) => (
            <Reveal key={a.title} delay={i * 0.08}>
              <div className="card-luxe h-full p-4 md:p-6">
                <span className="icon-tile h-9 w-9 items-center justify-center rounded-lg md:h-11 md:w-11 md:rounded-xl">
                  <TrendingUp className="h-4 w-4 md:h-5 md:w-5" strokeWidth={2} />
                </span>
                <h3 className="mt-3 text-[0.98rem] leading-snug text-ocean md:mt-4 md:text-lg">{a.title}</h3>
                <p className="mt-1.5 text-[0.8rem] leading-relaxed text-ocean/70 md:mt-2 md:text-sm">{a.text}</p>
              </div>
            </Reveal>
          ))}
        </div>

        <Reveal delay={0.1}>
          <div className="mx-auto mt-12 max-w-3xl space-y-4 text-center">
            {regionIntro.paragraphs.slice(1).map((p) => (
              <p key={p.slice(0, 20)} className="text-base leading-relaxed text-ocean/70">{p}</p>
            ))}
          </div>
        </Reveal>

        {/* Basında MİA */}
        {/* Basında MİA — YALNIZCA doğrulanmış haberler yayınlanır.
            Gerçek link eklenene kadar (verified: true) bölüm hiç görünmez;
            böylece örnek başlıklar gerçek haber gibi yayına çıkmaz. */}
        {verifiedPress.length > 0 && (
          <div className="mt-20">
            <Reveal>
              <div className="flex items-center justify-center gap-3">
                <Newspaper className="h-5 w-5 text-bronze" />
                <span className="eyebrow text-bronze">Basında MİA</span>
              </div>
            </Reveal>

            <div className="mt-8 grid gap-5 md:grid-cols-3">
              {verifiedPress.map((item, i) => (
                <Reveal key={item.title} delay={i * 0.08}>
                  <a href={item.href} target="_blank" rel="noopener noreferrer" className="block h-full">
                    <div className="card-luxe flex h-full flex-col p-5 md:p-6">
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-medium uppercase tracking-wider text-bronze">{item.source}</span>
                        <span className="text-xs text-ocean/40">{item.date}</span>
                      </div>
                      <h3 className="mt-3 flex-1 text-lg leading-snug text-ocean">{item.title}</h3>
                      <div className="mt-4 flex items-center gap-1.5 text-sm font-medium text-bronze">
                        Habere Git <ArrowUpRight className="h-4 w-4" />
                      </div>
                    </div>
                  </a>
                </Reveal>
              ))}
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
