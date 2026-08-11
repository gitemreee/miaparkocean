import { Reveal } from "@/components/ui/Reveal";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { SmartImage } from "@/components/ui/SmartImage";
import { Icon } from "@/components/ui/Icon";
import { amenities } from "@/data/amenities";

export function SocialLife() {
  return (
    <section className="bg-paper-2 py-20 md:py-28">
      <div className="container-luxe">
        <SectionHeading
          eyebrow="Sosyal Yaşam"
          title={<>Her gün <span className="gilded">tatil konforu</span></>}
          lead="Yürüyüş yolları, süs havuzları, avlular ve akşam olunca devreye giren aydınlatma; MİA PARK OCEAN'da sosyal yaşam evinizin hemen dışında başlıyor."
        />

        <Reveal className="mt-12">
          <div className="overflow-hidden rounded-3xl">
            <div className="aspect-[16/7]">
              <SmartImage src="/images/hero-courtyard-dusk.webp" alt="Akşam aydınlatmalı merkezi avlu ve yürüyüş yolları" sizes="100vw" className="h-full w-full object-cover" />
            </div>
          </div>
        </Reveal>

        <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {amenities.map((a, i) => (
            <Reveal key={a.title} delay={(i % 3) * 0.07}>
              <div className="group flex h-full items-start gap-4 rounded-2xl border border-ink/8 bg-white p-6 transition-all duration-300 hover:-translate-y-0.5 hover:border-accent/40 hover:shadow-[var(--shadow-card)]">
                <span className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-accent-tint text-accent transition-colors group-hover:bg-accent group-hover:text-white">
                  <Icon name={a.icon} className="h-6 w-6" />
                </span>
                <div>
                  <h3 className="text-lg font-bold text-ink">{a.title}</h3>
                  <p className="mt-1.5 text-sm leading-relaxed text-ink/60">{a.text}</p>
                </div>
              </div>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}
