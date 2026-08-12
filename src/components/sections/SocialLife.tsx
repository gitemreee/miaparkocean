import { Reveal } from "@/components/ui/Reveal";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { SmartImage } from "@/components/ui/SmartImage";
import { Icon } from "@/components/ui/Icon";
import { amenities } from "@/data/amenities";

export function SocialLife() {
  return (
    <section className="surface-tint py-12 md:py-24">
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

        <div className="mt-8 grid grid-cols-2 gap-3 md:gap-4 lg:grid-cols-3">
          {amenities.map((a, i) => (
            <Reveal key={a.title} delay={(i % 3) * 0.07}>
              <div className="card-luxe group flex h-full flex-col gap-2.5 p-4 md:flex-row md:items-start md:gap-4 md:p-6">
                <span className="icon-tile h-10 w-10 items-center justify-center rounded-xl md:h-12 md:w-12">
                  <Icon name={a.icon} className="h-5 w-5 md:h-6 md:w-6" />
                </span>
                <div>
                  <h3 className="text-[0.95rem] font-bold leading-snug text-ink md:text-lg">{a.title}</h3>
                  <p className="mt-1 text-[0.8rem] leading-relaxed text-ink/60 md:mt-1.5 md:text-sm">{a.text}</p>
                </div>
              </div>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}
