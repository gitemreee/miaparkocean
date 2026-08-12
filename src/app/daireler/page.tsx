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
      <section className="border-b border-ocean/8 bg-cream py-10">
        <div className="container-luxe grid gap-4 sm:grid-cols-3">
          {units.map((u, i) => (
            <Reveal key={u.slug} delay={i * 0.08}>
              <Link
                href={`#${u.slug}`}
                className="flex items-center justify-between rounded-2xl border border-ocean/10 bg-pearl px-6 py-5 transition-colors hover:border-bronze"
              >
                <div>
                  <div className="font-display text-2xl text-ocean">{u.type}</div>
                  <div className="text-sm text-ocean/60">{u.name}</div>
                </div>
                <div className="text-right">
                  <div className="font-display text-xl text-bronze">{u.area}</div>
                  <div className="text-xs text-ocean/50">{u.count} adet</div>
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
