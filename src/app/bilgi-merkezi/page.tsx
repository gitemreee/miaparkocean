import type { Metadata } from "next";
import Link from "next/link";
import { ArrowRight, FileText, BookText } from "lucide-react";
import { PageHero } from "@/components/layout/PageHero";
import { Reveal } from "@/components/ui/Reveal";
import { kbCategories } from "@/data/articles";
import { articlesByCategory } from "@/lib/kb";

export const metadata: Metadata = {
  title: "Bilgi Merkezi — Kooperatif Rehberi",
  description:
    "Kooperatif modeli, üyelik ve üye hakları, güven ve denetim, finansman, arsa-ruhsat-inşaat ve vergi konularında kapsamlı rehber ve makaleler.",
};

export default function BilgiMerkeziPage() {
  return (
    <>
      <PageHero
        eyebrow="Bilgi Merkezi"
        title={<>Kooperatif <span className="gilded">rehberi</span></>}
        lead="Ortaklık, şeffaflık, denetim, üye hakları ve daha fazlası. Kararınızı rahatça verebilmeniz için hazırladığımız içerikleri burada topladık."
        image="/images/facade-warm.webp"
      />

      <section className="surface-paper py-12 md:py-24">
        <div className="container-luxe space-y-16">
          {kbCategories.map((cat) => {
            const items = articlesByCategory(cat.key);
            if (items.length === 0) return null;
            return (
              <div key={cat.key} id={cat.key} className="scroll-mt-24">
                <Reveal>
                  <div className="flex items-end justify-between gap-4 border-b border-ocean/10 pb-4">
                    <div>
                      <div className="flex items-center gap-2">
                        <BookText className="h-5 w-5 text-bronze" />
                        <h2 className="text-2xl text-ocean md:text-3xl">{cat.title}</h2>
                      </div>
                      <p className="mt-2 max-w-xl text-sm text-ocean/60">{cat.desc}</p>
                    </div>
                    <span className="hidden shrink-0 text-sm text-ocean/40 sm:block">{items.length} içerik</span>
                  </div>
                </Reveal>

                <div className="mt-8 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                  {items.map((a, i) => (
                    <Reveal key={a.slug} delay={(i % 3) * 0.06}>
                      <Link
                        href={`/bilgi-merkezi/${a.slug}`}
                        className="group flex h-full flex-col rounded-2xl border border-ocean/8 bg-pearl p-6 transition-all duration-300 hover:-translate-y-1 hover:border-bronze/40 hover:shadow-[var(--shadow-card)]"
                      >
                        <div className="flex items-center gap-2">
                          <FileText className="h-4 w-4 text-bronze" />
                          <span className="eyebrow text-[0.56rem] text-ocean/45">
                            {a.tier === "article" ? "Makale" : "Rehber"}
                          </span>
                        </div>
                        <h3 className="mt-3 flex-1 text-lg leading-snug text-ocean">{a.title}</h3>
                        <span className="mt-4 inline-flex items-center gap-1.5 text-sm font-medium text-bronze transition-all group-hover:gap-2.5">
                          Oku <ArrowRight className="h-4 w-4" />
                        </span>
                      </Link>
                    </Reveal>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </section>
    </>
  );
}
