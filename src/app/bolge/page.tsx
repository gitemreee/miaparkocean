import type { Metadata } from "next";
import { PageHero } from "@/components/layout/PageHero";
import { Region } from "@/components/sections/Region";
import { Location } from "@/components/sections/Location";
import { Valuation } from "@/components/sections/Valuation";
import { Demographics } from "@/components/sections/Demographics";
import { ContactForm } from "@/components/sections/ContactForm";

export const metadata: Metadata = {
  title: "İzmit MİA Bölgesi — Değer Kazanan Lokasyon",
  description:
    "İzmit MİA Bölgesi: D100'e 1 dk, TEM'e 5 dk, şehir merkezi ve hastaneye 5 dk. Gelişen ulaşım aksı ve güçlü konut talebiyle değer kazanan yatırım bölgesi.",
};

export default function BolgePage() {
  return (
    <>
      <PageHero
        eyebrow="İzmit MİA Bölgesi"
        title={<>Değer kazanan <span className="gilded">bir bölgede</span></>}
        lead="MİA PARK OCEAN, İzmit'in gelişen yaşam ve yatırım aksında yer alıyor. Ulaşım, üniversite ve hastane hep yakınınızda."
        image="/images/street-corner.webp"
      />
      <Region />
      <Location />
      <Valuation />
      <Demographics />
      <ContactForm />
    </>
  );
}
