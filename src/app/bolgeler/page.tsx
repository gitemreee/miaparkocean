import type { Metadata } from "next";
import Link from "next/link";
import { MapPin, Car, ArrowRight } from "lucide-react";
import { PageHero } from "@/components/layout/PageHero";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { Reveal } from "@/components/ui/Reveal";
import { WaveDivider } from "@/components/ui/Wave";
import { locations, locationGroups } from "@/data/locations";
import { site } from "@/data/site";
import { graph, breadcrumbJsonLd, abs } from "@/lib/seo";

export const metadata: Metadata = {
  title: "Bölgeler — İzmit, Kocaeli, Sakarya ve İstanbul'dan MİA PARK OCEAN",
  description:
    "İzmit mahalleleri, Kocaeli ilçeleri, Sakarya ve İstanbul'dan MİA PARK OCEAN'a mesafeler, bölge profilleri ve konut yatırımı rehberi.",
  alternates: { canonical: abs("/bolgeler") },
  openGraph: {
    title: "Bölgeler — MİA PARK OCEAN",
    description:
      "İzmit mahalleleri, Kocaeli ilçeleri, Sakarya ve İstanbul'dan projeye mesafeler ve bölge profilleri.",
    url: abs("/bolgeler"),
  },
};

// sellerJsonLd layout'ta site geneli yayınlanır.
const jsonLd = graph(
  breadcrumbJsonLd([
    { name: "Ana Sayfa", path: "/" },
    { name: "Bölgeler", path: "/bolgeler" },
  ]),
  {
    "@type": "ItemList",
    name: "MİA PARK OCEAN bölge rehberi",
    numberOfItems: locations.length,
    itemListElement: locations.map((l, i) => ({
      "@type": "ListItem",
      position: i + 1,
      name: `${l.fullName} — ${l.parent}`,
      url: abs(`/bolgeler/${l.slug}`),
    })),
  }
);

export default function BolgelerPage() {
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />

      <PageHero
        eyebrow="Bölge Rehberi"
        title={
          <>
            Nereden gelirseniz gelin, <span className="gradient-text-light">MİA Bölgesi</span> yakınınızda
          </>
        }
        lead="İzmit mahalleleri, Kocaeli ilçeleri ve komşu illerden MİA PARK OCEAN'a ulaşım süreleri, bölge profilleri ve o bölgeye özel sorular."
        image="/images/aerial-pools.webp"
      />

      {locationGroups.map((group, gi) => {
        const items = locations.filter((l) => l.type === group.type);
        return (
          <section
            key={group.type}
            id={group.type === "mahalle" ? "izmit-mahalleleri" : group.type === "ilce" ? "kocaeli-ilceleri" : "komsu-iller"}
            className={gi % 2 === 0 ? "surface-paper py-12 md:py-22" : "surface-tint py-12 md:py-22"}
          >
            <div className="container-luxe">
              <SectionHeading eyebrow={group.title} title={group.title} lead={group.lead} />

              <div className="mt-14 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                {items.map((l, i) => (
                  <Reveal key={l.slug} delay={i * 0.04}>
                    <Link
                      href={`/bolgeler/${l.slug}`}
                      className="card-luxe group flex h-full flex-col p-5 md:p-6"
                    >
                      <div className="flex items-start justify-between gap-4">
                        <span className="icon-tile h-11 w-11 items-center justify-center rounded-xl">
                          <MapPin className="h-5 w-5" />
                        </span>
                        <span className="pill pill-ocean text-[0.7rem]">
                          <Car className="h-3.5 w-3.5" /> {l.drive}
                        </span>
                      </div>

                      <h3 className="mt-5 font-display text-xl text-ink">{l.fullName}</h3>
                      <p className="mt-1 text-xs font-semibold uppercase tracking-[0.14em] text-ink/40">{l.parent}</p>
                      <p className="mt-3 flex-1 text-sm leading-relaxed text-ink/60">{l.intro[0].slice(0, 132)}…</p>

                      <span className="mt-5 inline-flex items-center gap-1.5 text-sm font-semibold text-accent">
                        Bölge sayfası
                        <ArrowRight className="h-4 w-4 transition-transform duration-300 group-hover:translate-x-1" />
                      </span>
                    </Link>
                  </Reveal>
                ))}
              </div>
            </div>
          </section>
        );
      })}

      <section className="section-dark">
        <WaveDivider tone="paper" flip className="h-[52px] md:h-[84px]" />
        <div className="container-luxe relative z-10 py-16 text-center md:py-20">
          <h2 className="mx-auto max-w-2xl text-balance text-3xl leading-tight text-cream md:text-4xl">
            Bölgenizi listede bulamadınız mı?
          </h2>
          <p className="mx-auto mt-5 max-w-xl text-pretty leading-relaxed text-ice/75">
            Nerede olursanız olun, {site.name} hakkında bilgi almak için bize ulaşın. Ulaşım, ödeme planı ve daire
            tipleri için satış ekibimiz yardımcı olur.
          </p>
          <Link href="/iletisim" className="btn-base btn-jade btn-shine mt-9 px-8 py-4 text-sm">
            İletişime Geçin <ArrowRight className="h-4 w-4" />
          </Link>
        </div>
        <WaveDivider tone="paper" className="h-[52px] md:h-[84px]" />
      </section>
    </>
  );
}
