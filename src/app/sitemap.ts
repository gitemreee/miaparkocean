import type { MetadataRoute } from "next";
import { site } from "@/data/site";
import { allArticles } from "@/lib/kb";

export const dynamic = "force-static";

export default function sitemap(): MetadataRoute.Sitemap {
  const now = new Date();
  const routes = ["", "/daireler", "/kooperatif", "/bilgi-merkezi", "/bolge", "/galeri", "/iletisim"];

  const staticEntries: MetadataRoute.Sitemap = routes.map((r) => ({
    url: `${site.url}${r}`,
    lastModified: now,
    changeFrequency: "weekly",
    priority: r === "" ? 1 : 0.8,
  }));

  const articleEntries: MetadataRoute.Sitemap = allArticles.map((a) => ({
    url: `${site.url}/bilgi-merkezi/${a.slug}`,
    lastModified: now,
    changeFrequency: "monthly",
    priority: 0.6,
  }));

  return [...staticEntries, ...articleEntries];
}
