import type { Metadata } from "next";
import Link from "next/link";
import { PageHero } from "@/components/layout/PageHero";
import { UnitDetail } from "@/components/sections/UnitDetail";
import { Payment } from "@/components/sections/Payment";
import { Faq } from "@/components/sections/Faq";
import { Reveal } from "@/components/ui/Reveal";
import { units } from "@/data/units";
import { faq } from "@/data/faq";

export const metadata: Metadata = {
  title: "Daire Tipleri — 1+0, 1+1, 1+1 Bahçe Loft, 2+1 Bahçe Dubleks",
  description:
    "MİA PARK OCEAN daire tipleri: 1+0 (28 m²), 1+1 (50 m²) ve 2+1 Bahçe Dubleks (100 m²). Kat planları, özellikler ve fiyat avantajları.",
};

export default function DairelerPage() {
  return (
    <>
      <PageHero
        eyebrow="Daire Tipleri"
        title={<>Yaşam tarzınıza <span className="gilded">uygun daire</span></>}
        lead="1+0 stüdyodan 2+1 bahçe dublekse üç farklı daire tipi var. Her biri, günlük hayatınızı rahatça sürdürebileceğiniz akıllı planlarla hazırlandı."
        image="/images/interior-living.webp"
      />

      {/* Karşılaştırma şeridi */}
      <section className="surface-tint border-b border-ink/8 py-6 md:py-10">
        <div className="container-luxe grid grid-cols-2 gap-2.5 md:gap-4 lg:grid-cols-4">
          {units.map((u, i) => (
            <Reveal key={u.slug} delay={i * 0.08}>
              <Link
                href={`#${u.slug}`}
                className="card-luxe flex h-full items-center justify-between gap-2 px-3.5 py-3 transition-colors md:px-5 md:py-4"
              >
                <div>
                  <div className="font-display text-lg leading-none text-ink md:text-2xl">{u.type}</div>
                  <div className="mt-1 text-[0.72rem] leading-tight text-ink/55 md:text-sm">{u.name}</div>
                </div>
                <div className="text-right">
                  <div className="font-display text-[0.95rem] leading-none text-accent md:text-xl">{u.areaValue} m²</div>
                  <div className="mt-1 text-[0.7rem] text-ink/50 md:text-xs">{u.count} adet</div>
                </div>
              </Link>
            </Reveal>
          ))}
        </div>
      </section>

      {units.map((u, i) => (
        <UnitDetail key={u.slug} unit={u} index={i} />
      ))}

      <Payment />
      <Faq items={faq.filter((f) => f.category === "proje")} eyebrow="Daireler Hakkında" title={<>Merak <span className="gilded">edilenler</span></>} />
    </>
  );
}
