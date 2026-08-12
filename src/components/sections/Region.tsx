import { Newspaper, TrendingUp, ArrowUpRight } from "lucide-react";
import { Reveal } from "@/components/ui/Reveal";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { regionIntro, press } from "@/data/region";

export function Region() {
  // Yalnızca gerçek link eklenmiş haberler gösterilir.
  const verifiedPress = press.filter((p) => p.verified && p.href !== "#");

  return (
    <section id="bolge" className="surface-tint py-24 md:py-32">
      <div className="container-luxe">
        <SectionHeading
          eyebrow="Değerlenen Bölge"
          title={<>İzmit MİA: <span className="gilded">doğru yerden, doğru zamanda</span></>}
          lead={regionIntro.paragraphs[0]}
        />

        {/* Avantajlar */}
        <div className="mt-14 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
          {regionIntro.advantages.map((a, i) => (
            <Reveal key={a.title} delay={i * 0.08}>
              <div className="h-full rounded-2xl border border-ocean/8 bg-cream p-6">
                <TrendingUp className="h-6 w-6 text-bronze" strokeWidth={1.4} />
                <h3 className="mt-4 text-lg text-ocean">{a.title}</h3>
                <p className="mt-2 text-sm leading-relaxed text-ocean/70">{a.text}</p>
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
                    <div className="card-luxe flex h-full flex-col p-6">
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
