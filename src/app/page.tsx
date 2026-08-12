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
import { WhyCooperative } from "@/components/sections/WhyCooperative";
import { LegalAssurance } from "@/components/sections/LegalAssurance";
import { CooperativeOrg } from "@/components/sections/CooperativeOrg";
import { Faq } from "@/components/sections/Faq";
import { ContactForm } from "@/components/sections/ContactForm";
import { faq } from "@/data/faq";
import { graph, faqJsonLd, developerJsonLd } from "@/lib/seo";

// Proje ve satıcı düğümleri layout'ta site geneli yayınlanır; burada yalnızca
// ana sayfaya özel SSS ve yapımcı bilgisi eklenir.
const jsonLd = graph(developerJsonLd, faqJsonLd(faq));

export default function HomePage() {
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
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
      <WhyCooperative />
      <LegalAssurance />
      <CooperativeOrg />
      <Faq limit={6} moreHref="/bilgi-merkezi" />
      <ContactForm />
    </>
  );
}
