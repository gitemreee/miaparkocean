import type { MetadataRoute } from "next";
import { site } from "@/data/site";
import { allArticles } from "@/lib/kb";
import { locations } from "@/data/locations";

export const dynamic = "force-static";

// next.config.mjs'te trailingSlash: true — sitemap URL'leri de sondaki eğik
// çizgiyle üretilir ki yayınlanan adreslerle birebir eşleşsin.
const url = (path: string) => `${site.url}${path}${path.endsWith("/") ? "" : "/"}`.replace(/\/+$/, "/");

export default function sitemap(): MetadataRoute.Sitemap {
  const now = new Date();

  const core: { path: string; priority: number; freq: MetadataRoute.Sitemap[number]["changeFrequency"] }[] = [
    { path: "/", priority: 1, freq: "weekly" },
    { path: "/daireler", priority: 0.9, freq: "weekly" },
    { path: "/bolgeler", priority: 0.9, freq: "weekly" },
    { path: "/kooperatif", priority: 0.85, freq: "weekly" },
    { path: "/bolge", priority: 0.8, freq: "weekly" },
    { path: "/bilgi-merkezi", priority: 0.8, freq: "weekly" },
    { path: "/belgeler", priority: 0.7, freq: "monthly" },
    { path: "/galeri", priority: 0.7, freq: "monthly" },
    { path: "/iletisim", priority: 0.8, freq: "monthly" },
    { path: "/kvkk", priority: 0.2, freq: "yearly" },
    { path: "/cerez-politikasi", priority: 0.2, freq: "yearly" },
  ];

  return [
    ...core.map((r) => ({
      url: url(r.path),
      lastModified: now,
      changeFrequency: r.freq,
      priority: r.priority,
    })),
    // Yerel SEO sayfaları — mahalle / ilçe / il
    ...locations.map((l) => ({
      url: url(`/bolgeler/${l.slug}`),
      lastModified: now,
      changeFrequency: "monthly" as const,
      priority: l.type === "mahalle" ? 0.75 : l.type === "ilce" ? 0.7 : 0.65,
    })),
    // Bilgi merkezi makaleleri
    ...allArticles.map((a) => ({
      url: url(`/bilgi-merkezi/${a.slug}`),
      lastModified: now,
      changeFrequency: "monthly" as const,
      priority: 0.6,
    })),
  ];
}
