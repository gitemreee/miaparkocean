import type { Metadata, Viewport } from "next";
import { Marcellus, Manrope } from "next/font/google";
import "./globals.css";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";
import { RegistryBadges } from "@/components/layout/RegistryBadges";
import { WhatsappFab } from "@/components/layout/WhatsappFab";
import { CookieConsent } from "@/components/layout/CookieConsent";
import { SiteFrame } from "@/components/layout/SiteFrame";
import { site, contact } from "@/data/site";
import { verification } from "@/data/verification";
import { graph, sellerJsonLd, projectJsonLd } from "@/lib/seo";

// Marcellus: logodaki Trajan tarzı serif kelime markasının devamı.
const display = Marcellus({
  subsets: ["latin", "latin-ext"],
  weight: "400",
  variable: "--font-display-family",
  display: "swap",
});

// Manrope: uzun Türkçe metinlerde yüksek okunabilirlik.
const body = Manrope({
  subsets: ["latin", "latin-ext"],
  weight: ["300", "400", "500", "600", "700", "800"],
  variable: "--font-body-family",
  display: "swap",
});

export const metadata: Metadata = {
  metadataBase: new URL(site.url),
  title: {
    default: "MİA PARK OCEAN — İzmit MİA Bölgesi Konut Projesi | Lüks Artık Ulaşılabilir",
    template: "%s | MİA PARK OCEAN",
  },
  description: site.description,
  keywords: [
    "MİA PARK OCEAN",
    "İzmit MİA Bölgesi konut projesi",
    "Kocaeli kooperatif daire",
    "İzmit satılık daire",
    "Yahya Kaptan Birlik Yapı Kooperatifi",
    "İzmit 1+1 daire",
    "faizsiz konut projesi Kocaeli",
    "İzmit yeni konut projeleri",
  ],
  authors: [{ name: site.seller }],
  creator: site.seller,
  publisher: site.developer,
  openGraph: {
    type: "website",
    locale: "tr_TR",
    url: site.url,
    siteName: site.name,
    title: "MİA PARK OCEAN — İzmit MİA Bölgesi Konut Projesi",
    description: site.description,
    images: [{ url: "/og-image.jpg", width: 1200, height: 630, alt: "MİA PARK OCEAN — İzmit MİA Bölgesi" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "MİA PARK OCEAN — İzmit MİA Bölgesi",
    description: site.description,
    images: ["/og-image.jpg"],
  },
  icons: {
    icon: [
      { url: "/icon-192.png", sizes: "192x192", type: "image/png" },
      { url: "/icon-512.png", sizes: "512x512", type: "image/png" },
    ],
    apple: [{ url: "/apple-touch-icon.png", sizes: "180x180", type: "image/png" }],
  },
  alternates: { canonical: site.url },
  robots: {
    index: true,
    follow: true,
    googleBot: { index: true, follow: true, "max-image-preview": "large", "max-snippet": -1 },
  },
  // Doğrulama kodları src/data/verification.ts içinde tutulur.
  // Boş bırakılan alanlar sayfaya hiç yazılmaz.
  verification: {
    ...(verification.google ? { google: verification.google } : {}),
    ...(verification.yandex ? { yandex: verification.yandex } : {}),
    ...(verification.bing ? { other: { "msvalidate.01": verification.bing } } : {}),
  },
};

export const viewport: Viewport = {
  themeColor: "#0f52ba",
  colorScheme: "light",
};

// Site geneli kimlik — tüm sayfalarda yayınlanır, iç sayfalar @id ile referans verir.
const siteJsonLd = graph(sellerJsonLd, projectJsonLd, {
  "@type": "WebSite",
  "@id": `${site.url}#website`,
  url: site.url,
  name: site.name,
  inLanguage: "tr-TR",
  publisher: { "@id": `${site.url}#seller` },
});

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="tr" className={`${display.variable} ${body.variable}`}>
      <body>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(siteJsonLd) }}
        />
        <SiteFrame
          header={<Header />}
          footer={
            <>
              <RegistryBadges />
              <Footer />
            </>
          }
          floating={
            <>
              <WhatsappFab />
              <CookieConsent />
            </>
          }
        >
          {children}
        </SiteFrame>
      </body>
    </html>
  );
}
