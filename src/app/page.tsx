import { Hero } from "@/components/sections/Hero";
import { Stats } from "@/components/sections/Stats";
import { Intro } from "@/components/sections/Intro";
import { Process } from "@/components/sections/Process";
import { UnitTypes } from "@/components/sections/UnitTypes";
import { Payment } from "@/components/sections/Payment";
import { PromoFilm } from "@/components/sections/PromoFilm";
import { SocialLife } from "@/components/sections/SocialLife";
import { GalleryPreview } from "@/components/sections/GalleryPreview";
import { Catalog } from "@/components/sections/Catalog";
import { Location } from "@/components/sections/Location";
import { Valuation } from "@/components/sections/Valuation";
import { Demographics } from "@/components/sections/Demographics";
import { Region } from "@/components/sections/Region";
import { WhyCooperative } from "@/components/sections/WhyCooperative";
import { LegalAssurance } from "@/components/sections/LegalAssurance";
import { CooperativeOrg } from "@/components/sections/CooperativeOrg";
import { Faq } from "@/components/sections/Faq";
import { ContactForm } from "@/components/sections/ContactForm";
import { faq } from "@/data/faq";
import { units } from "@/data/units";
import { site } from "@/data/site";

const residenceJsonLd = {
  "@context": "https://schema.org",
  "@type": "ApartmentComplex",
  name: site.name,
  description: site.description,
  url: site.url,
  numberOfAccommodationUnits: 600,
  address: {
    "@type": "PostalAddress",
    addressLocality: "İzmit",
    addressRegion: "Kocaeli",
    addressCountry: "TR",
  },
  geo: { "@type": "GeoCoordinates", latitude: 40.736667, longitude: 29.944889 },
  containsPlace: units.map((u) => ({
    "@type": "Accommodation",
    name: u.name,
    floorSize: { "@type": "QuantitativeValue", value: u.areaValue, unitCode: "MTK" },
  })),
};

const faqJsonLd = {
  "@context": "https://schema.org",
  "@type": "FAQPage",
  mainEntity: faq.map((f) => ({
    "@type": "Question",
    name: f.question,
    acceptedAnswer: { "@type": "Answer", text: f.answer },
  })),
};

export default function HomePage() {
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(residenceJsonLd) }} />
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(faqJsonLd) }} />
      <Hero />
      <Stats />
      <Intro />
      <Process />
      <UnitTypes />
      <Payment />
      <PromoFilm />
      <SocialLife />
      <GalleryPreview />
      <Catalog />
      <Location />
      <Valuation />
      <Demographics />
      <Region />
      <WhyCooperative />
      <LegalAssurance />
      <CooperativeOrg />
      <Faq />
      <ContactForm />
    </>
  );
}
