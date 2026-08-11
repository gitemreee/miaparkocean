import type { Metadata } from "next";
import { Jost, Manrope } from "next/font/google";
import "./globals.css";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";
import { RegistryBadges } from "@/components/layout/RegistryBadges";
import { WhatsappFab } from "@/components/layout/WhatsappFab";
import { CookieConsent } from "@/components/layout/CookieConsent";
import { site } from "@/data/site";

const display = Jost({
  subsets: ["latin", "latin-ext"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-cormorant",
  display: "swap",
});

const body = Manrope({
  subsets: ["latin", "latin-ext"],
  weight: ["300", "400", "500", "600", "700"],
  variable: "--font-manrope",
  display: "swap",
});

export const metadata: Metadata = {
  metadataBase: new URL(site.url),
  title: {
    default: "MİA PARK OCEAN — İzmit MİA Bölgesi | Lüks Artık Ulaşılabilir",
    template: "%s | MİA PARK OCEAN",
  },
  description: site.description,
  keywords: [
    "MİA PARK OCEAN",
    "İzmit MİA Bölgesi konut",
    "Kocaeli kooperatif daire",
    "İzmit satılık daire projesi",
    "Yahya Kaptan Birlik Yapı Kooperatifi",
    "İzmit 1+1 daire",
    "vade farksız konut projesi",
  ],
  authors: [{ name: site.seller }],
  openGraph: {
    type: "website",
    locale: "tr_TR",
    url: site.url,
    siteName: site.name,
    title: "MİA PARK OCEAN — İzmit MİA Bölgesi",
    description: site.description,
    images: [{ url: "/og-image.jpg", width: 1200, height: 630, alt: "MİA PARK OCEAN" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "MİA PARK OCEAN — İzmit MİA Bölgesi",
    description: site.description,
    images: ["/og-image.jpg"],
  },
  alternates: { canonical: site.url },
  robots: { index: true, follow: true },
};

const orgJsonLd = {
  "@context": "https://schema.org",
  "@type": "Organization",
  name: site.seller,
  url: site.url,
  logo: `${site.url}/ocean-logo.webp`,
  description: `${site.name} projesinin tek yetkili satıcısı.`,
  address: {
    "@type": "PostalAddress",
    streetAddress: "Ömerağa Mah. Abdurrahman Yüksel Cad. Bana Bak Ap. No:15/4",
    addressLocality: "İzmit",
    addressRegion: "Kocaeli",
    addressCountry: "TR",
  },
  telephone: "+90 540 028 00 41",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="tr" className={`${display.variable} ${body.variable}`}>
      <body>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(orgJsonLd) }}
        />
        <Header />
        <main>{children}</main>
        <RegistryBadges />
        <Footer />
        <WhatsappFab />
        <CookieConsent />
      </body>
    </html>
  );
}
