import type { Metadata } from "next";
import Link from "next/link";
import { CalendarDays, Clock, MapPin, Phone, Globe, ArrowRight, Waves, Dumbbell, Flame, Baby, Car } from "lucide-react";
import { launchEvent } from "@/data/event";
import { contact, site } from "@/data/site";
import { RsvpForm } from "@/components/sections/RsvpForm";
import { WaveEdge } from "@/components/ui/Wave";

export const metadata: Metadata = {
  title: "Davetiye — MİA PARK OCEAN Lansman & Basın Toplantısı",
  description: `${launchEvent.dateLabel} ${launchEvent.timeLabel} · ${launchEvent.venue}, ${launchEvent.city}. MİA PARK OCEAN lansman ve basın toplantısı davetiyesi.`,
  // Listelenmemiş / gizli sayfa: QR ile paylaşılır, arama motorlarına kapalıdır.
  robots: { index: false, follow: false },
};

const amenities = [
  { icon: Waves, label: "Kapalı yüzme havuzu" },
  { icon: Dumbbell, label: "Fitness salonu" },
  { icon: Flame, label: "Sauna ve Türk hamamı" },
  { icon: Baby, label: "Çocuk oyun parkı" },
  { icon: Car, label: "Kapalı otopark" },
];

const eventJsonLd = {
  "@context": "https://schema.org",
  "@type": "Event",
  name: `${launchEvent.project} — ${launchEvent.name}`,
  startDate: launchEvent.startsAt,
  endDate: launchEvent.endsAt,
  eventStatus: "https://schema.org/EventScheduled",
  eventAttendanceMode: "https://schema.org/OfflineEventAttendanceMode",
  location: {
    "@type": "Place",
    name: launchEvent.venue,
    address: { "@type": "PostalAddress", addressLocality: launchEvent.city, addressCountry: "TR" },
  },
  image: `${site.url}/og-image.jpg`,
  description: launchEvent.invitationText,
  organizer: { "@type": "Organization", name: site.seller, url: site.url },
};

export default function DavetiyePage() {
  return (
    <div className="min-h-screen text-ink">
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(eventJsonLd) }} />

      {/* ---------- Üst: okyanus gradyanı + logodaki dalga ---------- */}
      <header className="section-dark relative">
        <div className="container-luxe relative z-10 pb-28 pt-16 text-center md:pb-36 md:pt-20">
          <span className="pill pill-light mx-auto w-fit tracking-[0.28em]">{launchEvent.kicker.toUpperCase()}</span>

          <h1 className="mx-auto mt-8 max-w-3xl text-balance font-display text-[2.1rem] leading-[1.08] text-white sm:text-5xl md:text-[3.5rem]">
            {launchEvent.project}
            <br />
            <span className="gradient-text-light">{launchEvent.name}</span>
          </h1>

          <p className="mx-auto mt-6 max-w-xl text-pretty text-base leading-relaxed text-ice/80 md:text-lg">
            Sizleri bu özel günde aramızda görmekten mutluluk duyarız.
          </p>
        </div>

        {/* logodaki dalga sahneyi sayfaya bağlar */}
        <div className="pointer-events-none absolute inset-x-0 bottom-0">
          <WaveEdge className="h-[42px] md:h-[64px]" />
        </div>
      </header>

      {/* ---------- Logo — dalganın üstüne biner ---------- */}
      <div className="container-luxe relative z-20 -mt-10 md:-mt-14">
        <img
          src="/brand/logo-ocean-trim.webp"
          alt={`${launchEvent.project} — ${launchEvent.region}`}
          width={230}
          height={158}
          className="mx-auto h-auto w-[170px] md:w-[230px]"
        />
      </div>

      {/* ---------- Etkinlik künyesi ---------- */}
      <section className="container-luxe mt-12 md:mt-16">
        <div className="mx-auto grid max-w-3xl gap-4 sm:grid-cols-3">
          {[
            { icon: CalendarDays, label: "Tarih", value: launchEvent.dateLabel, sub: launchEvent.dayLabel },
            { icon: Clock, label: "Saat", value: launchEvent.timeLabel, sub: "Karşılama ile başlar" },
            { icon: MapPin, label: "Yer", value: launchEvent.venue, sub: launchEvent.city },
          ].map((item) => (
            <div key={item.label} className="card-luxe p-6 text-center">
              <span className="icon-tile mx-auto h-11 w-11 items-center justify-center rounded-xl">
                <item.icon className="h-5 w-5" />
              </span>
              <div className="eyebrow mt-4 text-[0.6rem] text-ink/45">{item.label}</div>
              <div className="mt-1.5 font-display text-xl text-ink">{item.value}</div>
              <div className="mt-0.5 text-sm text-ink/55">{item.sub}</div>
            </div>
          ))}
        </div>

        <div className="mx-auto mt-6 flex max-w-3xl flex-wrap justify-center gap-3">
          <a href={launchEvent.venueMaps} target="_blank" rel="noopener noreferrer" className="btn-base btn-outline px-6 py-3 text-sm">
            <MapPin className="h-4 w-4" /> Yol Tarifi Al
          </a>
          <a href={`tel:${launchEvent.host.phone}`} className="btn-base btn-outline px-6 py-3 text-sm">
            <Phone className="h-4 w-4" /> {launchEvent.host.name} · {launchEvent.host.phoneLabel}
          </a>
        </div>
      </section>

      {/* ---------- Davet metni ---------- */}
      <section className="container-luxe mt-16 md:mt-24">
        <div className="mx-auto max-w-2xl text-center">
          <div className="mx-auto h-[3px] w-12 rounded-full bg-gradient-surf" aria-hidden="true" />
          <h2 className="mt-6 font-display text-3xl leading-tight text-ink md:text-4xl">Değerli Konuğumuz,</h2>
          <p className="mt-6 text-pretty text-[1.05rem] leading-relaxed text-ink/70">{launchEvent.invitationText}</p>
        </div>
      </section>

      {/* ---------- Program ---------- */}
      <section className="section-mint mt-16 py-16 md:mt-24 md:py-20">
        <div className="container-luxe">
          <div className="mx-auto max-w-2xl text-center">
            <span className="eyebrow text-accent">Program</span>
            <h2 className="mt-4 font-display text-3xl leading-tight text-ink md:text-4xl">Günün akışı</h2>
          </div>

          <ol className="mx-auto mt-10 max-w-2xl">
            {launchEvent.programme.map((p, i) => (
              <li key={p.time} className="flex gap-5">
                {/* Zaman çizgisi */}
                <div className="flex flex-col items-center">
                  <span className="mt-1.5 h-3 w-3 shrink-0 rounded-full bg-gradient-surf ring-4 ring-white" />
                  {i < launchEvent.programme.length - 1 && <span className="w-px flex-1 bg-sapphire/20" />}
                </div>
                <div className="pb-7">
                  <div className="font-display text-lg text-sapphire">{p.time}</div>
                  <div className="mt-0.5 text-[0.98rem] text-ink/75">{p.title}</div>
                </div>
              </li>
            ))}
          </ol>
        </div>
      </section>

      {/* ---------- Katılım formu ---------- */}
      <section className="container-luxe mt-16 md:mt-24">
        <div className="mx-auto max-w-2xl">
          <RsvpForm />
        </div>
      </section>

      {/* ---------- Proje kısa tanıtım ---------- */}
      <section className="container-luxe mt-16 md:mt-24">
        <div className="mx-auto max-w-3xl text-center">
          <span className="eyebrow text-accent">Tanıtılacak Proje</span>
          <h2 className="mt-4 font-display text-3xl leading-tight text-ink md:text-4xl">
            {launchEvent.project} · <span className="gilded">{launchEvent.region}</span>
          </h2>
          <p className="mt-5 text-pretty leading-relaxed text-ink/65">
            4 blok, 600 daire. 1+0, 1+1, 1+1 bahçe loft ve 2+1 bahçe dubleks tiplerinden oluşan, geniş sosyal donatılı modern yaşam projesi.
          </p>

          <ul className="mt-9 flex flex-wrap justify-center gap-2.5">
            {amenities.map((a) => (
              <li key={a.label} className="pill pill-ocean">
                <a.icon className="h-4 w-4" /> {a.label}
              </li>
            ))}
          </ul>

          <Link href="/" className="btn-base btn-ocean btn-shine mt-10 px-8 py-4 text-sm">
            Projeyi İnceleyin <ArrowRight className="h-4 w-4" />
          </Link>
        </div>
      </section>

      {/* ---------- Alt bant ---------- */}
      <footer className="section-dark mt-20 md:mt-28">
        <WaveEdge flip className="h-[42px] md:h-[64px]" />

        <div className="container-luxe relative z-10 py-12 text-center">
          <div className="eyebrow text-ice/60">Tek Yetkili Satıcı</div>
          <a
            href={contact.websiteHref}
            target="_blank"
            rel="noopener noreferrer"
            className="mt-4 inline-flex items-center rounded-xl bg-white px-6 py-4 transition-transform duration-300 hover:scale-[1.03]"
          >
            <img src="/ocean-logo.webp" alt="Ocean Gayrimenkul" width={168} height={38} className="h-9 w-auto" />
          </a>

          <div className="mt-8 flex flex-wrap items-center justify-center gap-x-7 gap-y-3 text-sm text-ice/75">
            <a href={`tel:${launchEvent.host.phone}`} className="inline-flex items-center gap-2 hover:text-white">
              <Phone className="h-4 w-4" /> {launchEvent.host.phoneLabel}
            </a>
            <a href={site.url} className="inline-flex items-center gap-2 hover:text-white">
              <Globe className="h-4 w-4" /> {site.domain}
            </a>
          </div>

          <p className="mt-8 text-xs text-ice/40">
            © {new Date().getFullYear()} {launchEvent.project} · {site.developer}
          </p>
        </div>
      </footer>
    </div>
  );
}
