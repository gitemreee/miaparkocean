import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { Reveal } from "@/components/ui/Reveal";
import { GallerySlider } from "./GallerySlider";

export function GalleryPreview() {
  return (
    <section id="galeri" className="surface-paper py-12 md:py-24">
      <div className="container-luxe">
        <SectionHeading
          eyebrow="Galeri"
          title={<>Projeyi <span className="gilded">yakından keşfedin</span></>}
          lead="Dış mekân, sosyal alanlar ve iç mekân tasarımlarından seçkiler."
        />
      </div>

      {/* Kayar galeri — tam genişlik */}
      <Reveal className="mt-12">
        <GallerySlider />
      </Reveal>

      <div className="container-luxe">
        <Reveal delay={0.1}>
          <div className="mt-10 text-center">
            <Link href="/galeri" className="inline-flex items-center gap-2 rounded-full bg-accent px-8 py-4 text-sm font-semibold text-white transition-colors hover:bg-accent-600">
              Tüm Galeriyi Gör <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
        </Reveal>
      </div>
    </section>
  );
}
