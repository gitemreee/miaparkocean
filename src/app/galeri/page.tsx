import type { Metadata } from "next";
import { PageHero } from "@/components/layout/PageHero";
import { GalleryGrid } from "@/components/sections/GalleryGrid";

export const metadata: Metadata = {
  title: "Galeri",
  description:
    "MİA PARK OCEAN görsel galerisi: dış mekân, sosyal alanlar, iç mekân tasarımları ve kat planları.",
};

export default function GaleriPage() {
  return (
    <>
      <PageHero
        eyebrow="Galeri"
        title={<>Projeyi <span className="gilded">keşfedin</span></>}
        lead="Dış mekân, sosyal alanlar, iç mekân ve kat planlarıyla projeyi yakından görün."
        image="/images/aerial-pools.webp"
      />
      <section className="bg-cream py-12 md:py-24">
        <div className="container-luxe">
          <GalleryGrid showFilter />
        </div>
      </section>
    </>
  );
}
