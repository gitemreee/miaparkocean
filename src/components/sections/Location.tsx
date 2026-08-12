import { MapPin, Navigation, ExternalLink } from "lucide-react";
import { Reveal } from "@/components/ui/Reveal";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { Icon } from "@/components/ui/Icon";
import { LocationShowcase } from "./LocationShowcase";
import { distances, locationIntro, locationTags, mapConfig } from "@/data/location";

export function Location() {
  return (
    <section id="lokasyon" className="bg-cream py-24 md:py-32">
      <div className="container-luxe">
        <SectionHeading
          eyebrow="Lokasyon"
          title={<>İzmit'in <span className="gilded">mükemmel konumu</span></>}
          lead={locationIntro}
        />

        <Reveal className="mt-14">
          <LocationShowcase />
        </Reveal>

        <div className="mt-14 grid gap-10 lg:grid-cols-[1fr_1.15fr] lg:items-stretch">
          {/* Mesafeler */}
          <div>
            <div className="grid gap-3 sm:grid-cols-2">
              {distances.map((d, i) => (
                <Reveal key={d.place} delay={i * 0.05}>
                  <div className="group flex items-center gap-4 rounded-2xl border border-ink/10 bg-white px-5 py-4 transition-all duration-300 hover:-translate-y-0.5 hover:border-accent hover:shadow-[var(--shadow-card)]">
                    <span className="icon-tile h-12 w-12 items-center justify-center rounded-xl">
                      <Icon name={d.icon} className="h-5 w-5" />
                    </span>
                    <div>
                      <div className="font-display text-2xl font-bold leading-none text-ink">{d.time}</div>
                      <div className="mt-1 text-sm text-ink/60">{d.place}</div>
                    </div>
                  </div>
                </Reveal>
              ))}
            </div>

            <Reveal delay={0.2}>
              <div className="mt-6 flex flex-wrap gap-2">
                {locationTags.map((t) => (
                  <span key={t} className="rounded-full border border-bronze/30 px-4 py-1.5 text-xs font-medium text-ocean/70">
                    {t}
                  </span>
                ))}
              </div>
            </Reveal>
          </div>

          {/* Harita */}
          <Reveal delay={0.1}>
            <div className="overflow-hidden rounded-[2rem] border border-sapphire/20 bg-gradient-ocean shadow-[var(--shadow-luxe)]">
              <div className="flex items-center justify-between gap-3 border-b border-bronze/20 px-5 py-4">
                <div className="flex items-center gap-2 text-cream">
                  <MapPin className="h-4 w-4 text-bronze-300" />
                  <span className="text-sm font-medium">{mapConfig.label}</span>
                </div>
                <span className="hidden text-xs text-cream/50 sm:block">{mapConfig.plusCode}</span>
              </div>
              <iframe
                src={mapConfig.embed}
                title="MİA PARK OCEAN konum haritası"
                className="h-[360px] w-full md:h-[420px]"
                loading="lazy"
                referrerPolicy="no-referrer-when-downgrade"
                allowFullScreen
              />
              <div className="grid grid-cols-2 gap-px bg-bronze/20">
                <a
                  href={mapConfig.googleDirections}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center justify-center gap-2 bg-gradient-sapphire px-4 py-4 text-sm font-medium text-cream transition-colors hover:text-bronze-100"
                >
                  <Navigation className="h-4 w-4 text-bronze-300" /> Yol Tarifi (Google)
                </a>
                <a
                  href={mapConfig.yandex}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center justify-center gap-2 bg-gradient-sapphire px-4 py-4 text-sm font-medium text-cream transition-colors hover:text-bronze-100"
                >
                  <ExternalLink className="h-4 w-4 text-bronze-300" /> Yandex Haritalar
                </a>
              </div>
            </div>
          </Reveal>
        </div>
      </div>
    </section>
  );
}
