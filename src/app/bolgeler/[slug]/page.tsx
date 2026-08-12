import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { MapPin, Car, ArrowRight, Phone, MessageCircle, ChevronRight, Check } from "lucide-react";
import { PageHero } from "@/components/layout/PageHero";
import { Reveal } from "@/components/ui/Reveal";
import { WaveDivider } from "@/components/ui/Wave";
import { Faq } from "@/components/sections/Faq";
import { locations, locationBySlug } from "@/data/locations";
import { site, contact } from "@/data/site";
import { distances } from "@/data/location";
import { graph, abs, breadcrumbJsonLd, faqJsonLd, developerJsonLd } from "@/lib/seo";

export function generateStaticParams() {
  return locations.map((l) => ({ slug: l.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const loc = locationBySlug(slug);
  if (!loc) return {};
  const url = abs(`/bolgeler/${loc.slug}`);
  return {
    title: loc.title,
    description: loc.description,
    keywords: loc.keywords,
    alternates: { canonical: url },
    openGraph: {
      title: `${loc.title} — ${site.name}`,
      description: loc.description,
      url,
      images: [{ url: "/og-image.jpg", width: 1200, height: 630, alt: site.name }],
    },
  };
}

export default async function LocationPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const loc = locationBySlug(slug);
  if (!loc) notFound();

  const nearby = loc.nearby.map(locationBySlug).filter(Boolean);
  const typeLabel = loc.type === "mahalle" ? "Mahalle" : loc.type === "ilce" ? "İlçe" : "İl";

  const jsonLd = graph(
    developerJsonLd,
    faqJsonLd(loc.faq),
    breadcrumbJsonLd([
      { name: "Ana Sayfa", path: "/" },
      { name: "Bölgeler", path: "/bolgeler" },
      { name: loc.fullName, path: `/bolgeler/${loc.slug}` },
    ]),
    {
      "@type": "Place",
      name: `${loc.fullName}, ${loc.parent}`,
      address: {
        "@type": "PostalAddress",
        addressLocality: loc.type === "il" ? loc.name : loc.parent,
        addressRegion: loc.type === "il" ? loc.name : "Kocaeli",
        addressCountry: "TR",
      },
      description: loc.intro[0],
    },
    {
      "@type": "WebPage",
      "@id": abs(`/bolgeler/${loc.slug}`),
      name: loc.title,
      description: loc.description,
      about: { "@id": `${site.url}#project` },
      inLanguage: "tr-TR",
    }
  );

  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />

      <PageHero
        eyebrow={`${loc.parent} · ${typeLabel}`}
        title={
          <>
            {loc.name}&apos;
            {loc.type === "il" ? "dan" : "den"} <span className="gradient-text-light">MİA PARK OCEAN</span>
          </>
        }
        lead={loc.description}
        image="/images/facade-warm.webp"
      />

      {/* Kırıntı navigasyonu — hem kullanıcı hem tarayıcı için */}
      <nav aria-label="Kırıntı navigasyonu" className="surface-paper border-b border-ink/8">
        <div className="container-luxe flex flex-wrap items-center gap-1.5 py-4 text-sm text-ink/55">
          <Link href="/" className="transition-colors hover:text-accent">
            Ana Sayfa
          </Link>
          <ChevronRight className="h-3.5 w-3.5 text-ink/30" />
          <Link href="/bolgeler" className="transition-colors hover:text-accent">
            Bölgeler
          </Link>
          <ChevronRight className="h-3.5 w-3.5 text-ink/30" />
          <span className="font-medium text-ink">{loc.fullName}</span>
        </div>
      </nav>

      {/* Özet + giriş */}
      <section className="surface-paper py-16 md:py-24">
        <div className="container-luxe grid gap-12 lg:grid-cols-[1.5fr_1fr] lg:items-start">
          <div>
            <div className="flex items-center gap-3">
              <span className="h-[3px] w-9 rounded-full bg-gradient-surf" aria-hidden="true" />
              <span className="eyebrow text-accent">{loc.fullName}</span>
            </div>
            <h2 className="mt-5 text-balance text-[1.9rem] leading-tight text-ink md:text-[2.5rem]">
              {loc.fullName}&apos;
              {loc.type === "il" ? "de" : "nde"} konut arayanlar için{" "}
              <span className="gilded">MİA Bölgesi</span>
            </h2>

            <div className="mt-7 space-y-5 text-pretty text-[1.02rem] leading-relaxed text-ink/70">
              {loc.intro.map((p) => (
                <p key={p.slice(0, 24)}>{p}</p>
              ))}
            </div>
          </div>

          {/* Hızlı künye kartı */}
          <Reveal>
            <aside className="card-gradient-border p-7 shadow-[var(--shadow-card)]">
              <div className="flex items-center gap-3">
                <span className="flex h-11 w-11 items-center justify-center rounded-xl bg-gradient-surf text-white">
                  <Car className="h-5 w-5" />
                </span>
                <div>
                  <div className="eyebrow text-[0.6rem] text-ink/45">Projeye Mesafe</div>
                  <div className="font-display text-2xl text-ink">{loc.drive}</div>
                </div>
              </div>

              <div className="rule my-6" />

              <div className="eyebrow text-[0.6rem] text-ink/45">Projeden Ulaşım</div>
              <ul className="mt-4 space-y-2.5">
                {distances.slice(0, 6).map((d) => (
                  <li key={d.place} className="flex items-center justify-between gap-4 text-sm">
                    <span className="text-ink/70">{d.place}</span>
                    <span className="font-semibold text-accent">{d.time}</span>
                  </li>
                ))}
              </ul>

              <div className="rule my-6" />

              <div className="flex flex-col gap-2.5">
                <a href={contact.phones[0].href} className="btn-base btn-jade btn-shine px-6 py-3.5 text-sm">
                  <Phone className="h-4 w-4" /> {contact.phones[0].label}
                </a>
                <a
                  href={contact.whatsapp.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn-base btn-outline px-6 py-3.5 text-sm"
                >
                  <MessageCircle className="h-4 w-4" /> WhatsApp&apos;tan Yazın
                </a>
              </div>
            </aside>
          </Reveal>
        </div>
      </section>

      {/* Öne çıkanlar */}
      <section className="surface-tint py-16 md:py-24">
        <div className="container-luxe">
          <div className="mx-auto max-w-2xl text-center">
            <span className="eyebrow text-accent">Öne Çıkanlar</span>
            <h2 className="mt-4 text-balance text-[1.8rem] leading-tight text-ink md:text-[2.3rem]">
              {loc.name} için neden {site.name}?
            </h2>
          </div>

          <div className="mt-12 grid gap-4 sm:grid-cols-2">
            {loc.highlights.map((h, i) => (
              <Reveal key={h.title} delay={i * 0.06}>
                <div className="card-luxe flex h-full items-start gap-4 p-6">
                  <span className="mt-0.5 flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-gradient-surf text-white">
                    <Check className="h-4.5 w-4.5" strokeWidth={2.5} />
                  </span>
                  <div>
                    <h3 className="font-display text-lg text-ink">{h.title}</h3>
                    <p className="mt-1.5 text-sm leading-relaxed text-ink/60">{h.text}</p>
                  </div>
                </div>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* Bölgeye özel SSS — GEO için net cevaplar */}
      <Faq
        items={loc.faq.map((f) => ({ question: f.q, answer: f.a, category: "proje" as const }))}
        eyebrow={`${loc.name} · Sık Sorulanlar`}
        title={
          <>
            {loc.name} için <span className="gilded">merak edilenler</span>
          </>
        }
        lead={`${loc.fullName} sakinlerinin MİA PARK OCEAN hakkında en çok sorduğu sorular ve net cevapları.`}
      />

      {/* Yakın bölgeler — iç bağlantı ağı */}
      {nearby.length > 0 && (
        <section className="surface-tint py-16 md:py-20">
          <div className="container-luxe">
            <div className="mx-auto max-w-2xl text-center">
              <span className="eyebrow text-accent">Yakın Bölgeler</span>
              <h2 className="mt-4 text-[1.7rem] leading-tight text-ink md:text-[2.1rem]">Çevredeki diğer bölgeler</h2>
            </div>

            <div className="mt-10 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
              {nearby.map((n) => (
                <Link
                  key={n!.slug}
                  href={`/bolgeler/${n!.slug}`}
                  className="card-luxe group flex items-center justify-between gap-3 p-5"
                >
                  <span>
                    <span className="flex items-center gap-2 font-display text-lg text-ink">
                      <MapPin className="h-4 w-4 text-accent" /> {n!.name}
                    </span>
                    <span className="mt-1 block text-xs text-ink/50">{n!.drive}</span>
                  </span>
                  <ArrowRight className="h-4 w-4 shrink-0 text-accent transition-transform duration-300 group-hover:translate-x-1" />
                </Link>
              ))}
            </div>

            <div className="mt-10 text-center">
              <Link href="/bolgeler" className="btn-base btn-outline px-7 py-3.5 text-sm">
                Tüm Bölgeler <ArrowRight className="h-4 w-4" />
              </Link>
            </div>
          </div>
        </section>
      )}

      {/* Kapanış CTA */}
      <section className="section-dark">
        <WaveDivider tone="paper" flip className="h-[44px] md:h-[68px]" />
        <div className="container-luxe relative z-10 py-16 text-center md:py-20">
          <span className="eyebrow text-ice/60">{loc.fullName}</span>
          <h2 className="mx-auto mt-5 max-w-2xl text-balance text-3xl leading-tight text-cream md:text-4xl">
            {loc.name}&apos;{loc.type === "il" ? "den" : "den"} gelin, daireleri yerinde görün
          </h2>
          <p className="mx-auto mt-5 max-w-xl text-pretty leading-relaxed text-ice/75">
            Satış ofisimiz İzmit merkezde, Ömerağa Mahallesi&apos;nde. Randevu oluşturun, daire tiplerini ve resmî
            belgeleri birlikte inceleyelim.
          </p>
          <div className="mt-9 flex flex-wrap justify-center gap-3">
            <Link href="/iletisim" className="btn-base btn-jade btn-shine px-8 py-4 text-sm">
              Randevu Alın <ArrowRight className="h-4 w-4" />
            </Link>
            <Link href="/daireler" className="btn-base btn-outline-light px-8 py-4 text-sm">
              Daire Tiplerini İnceleyin
            </Link>
          </div>
        </div>
        <WaveDivider tone="paper" className="h-[44px] md:h-[68px]" />
      </section>
    </>
  );
}
