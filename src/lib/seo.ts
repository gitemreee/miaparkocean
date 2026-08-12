/**
 * SEO / GEO yardımcıları.
 *
 * JSON-LD üreticileri tek yerde toplanır ki her sayfa aynı, tutarlı ve
 * doğrulanabilir yapısal veriyi yayınlasın. Üretici motorlar (Google AI
 * Overviews, ChatGPT, Perplexity vb.) net soru-cevap ve açık kimlik
 * bilgisi bulunca içeriği daha güvenilir şekilde alıntılar.
 */

import { site, contact } from "@/data/site";
import { units } from "@/data/units";

const ORG_ID = `${site.url}#seller`;
const DEV_ID = `${site.url}#developer`;
const PROJECT_ID = `${site.url}#project`;

export const abs = (path = "") => `${site.url}${path.startsWith("/") ? path : `/${path}`}`;

/** Tek yetkili satıcı — RealEstateAgent */
export const sellerJsonLd = {
  "@type": "RealEstateAgent",
  "@id": ORG_ID,
  name: site.seller,
  url: site.url,
  logo: abs("/brand/logo-ocean.png"),
  image: abs("/og-image.jpg"),
  telephone: contact.phones.map((p) => p.href.replace("tel:", "")),
  email: contact.email,
  areaServed: ["İzmit", "Kocaeli", "Sakarya", "İstanbul"],
  address: {
    "@type": "PostalAddress",
    streetAddress: "Ömerağa Mah. Abdurrahman Yüksel Cad. Bana Bak Ap. No:15/4",
    addressLocality: "İzmit",
    addressRegion: "Kocaeli",
    postalCode: "41300",
    addressCountry: "TR",
  },
};

/** Yapımcı kooperatif — Organization */
export const developerJsonLd = {
  "@type": "Organization",
  "@id": DEV_ID,
  name: site.developer,
  url: "https://ykbkoop.com",
  description:
    "T.C. Ticaret Bakanlığı KOOPBİS sistemine kayıtlı yapı kooperatifi. 1163 sayılı Kooperatifler Kanunu kapsamında faaliyet gösterir.",
};

/** Projenin kendisi — ApartmentComplex */
export const projectJsonLd = {
  "@type": "ApartmentComplex",
  "@id": PROJECT_ID,
  name: site.name,
  url: site.url,
  description: site.description,
  image: [abs("/images/hero-courtyard-dusk.webp"), abs("/images/aerial-pools.webp"), abs("/og-image.jpg")],
  // Toplam daire sayısı units.ts'ten hesaplanır — elle yazılmaz ki
  // daire dağılımı değiştiğinde toplam kaymasın.
  numberOfAccommodationUnits: units.reduce((n, u) => n + u.count, 0),
  numberOfBuildings: 4,
  numberOfFloors: 8,
  address: {
    "@type": "PostalAddress",
    addressLocality: "İzmit",
    addressRegion: "Kocaeli",
    addressCountry: "TR",
  },
  geo: { "@type": "GeoCoordinates", latitude: 40.736667, longitude: 29.944889 },
  amenityFeature: [
    "Kapalı yüzme havuzu",
    "Fitness salonu",
    "Sauna ve Türk hamamı",
    "Çocuk oyun parkı",
    "Kapalı otopark",
    "7/24 güvenlik",
    "Merkezi avlu ve süs havuzları",
  ].map((name) => ({ "@type": "LocationFeatureSpecification", name, value: true })),
  containsPlace: units.map((u) => ({
    "@type": "Accommodation",
    name: u.name,
    numberOfRooms: u.type,
    floorSize: { "@type": "QuantitativeValue", value: u.areaValue, unitCode: "MTK" },
  })),
  developer: { "@id": DEV_ID },
  provider: { "@id": ORG_ID },
};

/**
 * Sayfa bazlı SSS — GEO için en değerli blok.
 * Hem `{q, a}` (bölge verisi) hem `{question, answer}` (faq.ts) kabul eder.
 */
type QA = { q: string; a: string } | { question: string; answer: string };

export function faqJsonLd(items: readonly QA[]) {
  return {
    "@type": "FAQPage",
    mainEntity: items.map((f) => {
      const name = "q" in f ? f.q : f.question;
      const text = "a" in f ? f.a : f.answer;
      return { "@type": "Question", name, acceptedAnswer: { "@type": "Answer", text } };
    }),
  };
}

/** Kırıntı navigasyonu */
export function breadcrumbJsonLd(trail: { name: string; path: string }[]) {
  return {
    "@type": "BreadcrumbList",
    itemListElement: trail.map((t, i) => ({
      "@type": "ListItem",
      position: i + 1,
      name: t.name,
      item: abs(t.path),
    })),
  };
}

/** Birden fazla düğümü tek @graph içinde yayınlar */
export function graph(...nodes: object[]) {
  return { "@context": "https://schema.org", "@graph": nodes };
}
