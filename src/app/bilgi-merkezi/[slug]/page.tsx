import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { ChevronRight, Check, ArrowRight, Info, ArrowUpRight } from "lucide-react";
import { Reveal } from "@/components/ui/Reveal";
import { mpoPolicyNote } from "@/data/articles";
import { site } from "@/data/site";
import { allArticles, getArticle, relatedArticles, categoryTitle } from "@/lib/kb";

export function generateStaticParams() {
  return allArticles.map((a) => ({ slug: a.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const a = getArticle(slug);
  if (!a) return {};
  return {
    title: a.title,
    description: a.metaDescription,
    alternates: { canonical: `${site.url}/bilgi-merkezi/${a.slug}` },
    openGraph: { title: a.title, description: a.metaDescription, type: "article" },
  };
}

export default async function ArticlePage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const a = getArticle(slug);
  if (!a) notFound();

  const related = relatedArticles(a);
  const hasToc = a.sections.length > 1;

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "Article",
    headline: a.title,
    description: a.metaDescription,
    articleSection: categoryTitle(a.category),
    publisher: { "@type": "Organization", name: site.seller },
    inLanguage: "tr-TR",
  };

  return (
    <article className="bg-cream pt-28 pb-24">
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
      <div className="container-luxe max-w-3xl">
        {/* Breadcrumb */}
        <nav aria-label="breadcrumb" className="flex flex-wrap items-center gap-1.5 text-xs text-ocean/50">
          <Link href="/" className="hover:text-bronze">Ana Sayfa</Link>
          <ChevronRight className="h-3 w-3" />
          <Link href="/bilgi-merkezi" className="hover:text-bronze">Bilgi Merkezi</Link>
          <ChevronRight className="h-3 w-3" />
          <Link href={`/bilgi-merkezi#${a.category}`} className="hover:text-bronze">{categoryTitle(a.category)}</Link>
        </nav>

        <div className="mt-6 flex items-center gap-2">
          <span className="gold-rule-solid w-8" />
          <span className="eyebrow text-bronze">{a.tier === "article" ? "Makale" : "Rehber"}</span>
        </div>
        <h1 className="mt-4 text-4xl leading-tight text-ocean md:text-5xl">{a.title}</h1>
        <p className="mt-5 text-lg leading-relaxed text-ocean/75">{a.intro}</p>

        <div className="gold-rule my-10" />

        {/* İçindekiler */}
        {hasToc && (
          <div className="mb-10 rounded-2xl border border-ocean/10 bg-pearl p-5 md:p-6">
            <div className="eyebrow text-ocean/50">İçindekiler</div>
            <ul className="mt-3 space-y-2">
              {a.sections.map((s, i) => (
                <li key={s.heading}>
                  <a href={`#s-${i}`} className="text-sm text-ocean/75 hover:text-bronze">
                    {i + 1}. {s.heading}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Bölümler */}
        <div className="space-y-10">
          {a.sections.map((s, i) => (
            <section key={s.heading} id={`s-${i}`} className="scroll-mt-28">
              <h2 className="text-2xl text-ocean">{s.heading}</h2>
              {s.body.map((p) => (
                <p key={p.slice(0, 24)} className="mt-3 text-base leading-relaxed text-ocean/75">{p}</p>
              ))}
            </section>
          ))}
        </div>

        {/* Kontrol listesi */}
        {a.checklist && a.checklist.length > 0 && (
          <div className="mt-12 rounded-2xl bg-gradient-ocean p-5 md:p-8">
            <h2 className="text-xl text-cream">Uygulama Kontrol Listesi</h2>
            <ul className="mt-5 space-y-3">
              {a.checklist.map((c) => (
                <li key={c} className="flex items-start gap-3 text-sm leading-relaxed text-cream/80">
                  <span className="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-bronze/20">
                    <Check className="h-3 w-3 text-bronze-300" strokeWidth={2.5} />
                  </span>
                  {c}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Mia Park Ocean politika notu */}
        {a.mpoNote && (
          <div className="mt-8 flex gap-3 rounded-2xl border border-bronze/25 bg-bronze/5 p-5 md:p-6">
            <Info className="mt-0.5 h-5 w-5 shrink-0 text-bronze" />
            <p className="text-sm leading-relaxed text-ocean/70">{mpoPolicyNote}</p>
          </div>
        )}

        {/* CTA */}
        <div className="mt-12 flex flex-col items-start gap-4 rounded-2xl bg-pearl p-8 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <div className="text-lg text-ocean">Sorularınız mı var?</div>
            <div className="mt-1 text-sm text-ocean/60">Proje danışmanımız süreçleri sizin için açıklasın.</div>
          </div>
          <Link href="/iletisim" className="inline-flex shrink-0 items-center gap-2 rounded-full bg-bronze px-7 py-3.5 text-sm font-medium text-cream transition-colors hover:bg-bronze-300">
            Danışmanla Görüşün <ArrowRight className="h-4 w-4" />
          </Link>
        </div>

        {/* İlgili içerikler */}
        {related.length > 0 && (
          <div className="mt-14">
            <h2 className="text-xl text-ocean">İlgili İçerikler</h2>
            <div className="mt-5 grid gap-4 sm:grid-cols-3">
              {related.map((r) => (
                <Reveal key={r.slug}>
                  <Link href={`/bilgi-merkezi/${r.slug}`} className="group flex h-full flex-col rounded-2xl border border-ocean/8 bg-pearl p-5 transition-colors hover:border-bronze/40">
                    <span className="eyebrow text-[0.54rem] text-ocean/40">{categoryTitle(r.category)}</span>
                    <h3 className="mt-2 flex-1 text-sm leading-snug text-ocean">{r.title}</h3>
                    <ArrowUpRight className="mt-3 h-4 w-4 text-bronze" />
                  </Link>
                </Reveal>
              ))}
            </div>
          </div>
        )}
      </div>
    </article>
  );
}
