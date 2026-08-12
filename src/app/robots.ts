import type { MetadataRoute } from "next";
import { site } from "@/data/site";

export const dynamic = "force-static";

/**
 * Arama motorları + üretici yapay zekâ motorları (GEO).
 *
 * Yapay zekâ tarayıcılarına açıkça izin verilir: içerik alıntılandığında
 * projenin doğru ve güncel bilgisi kaynak gösterilerek aktarılsın.
 * Gizli sayfalar (davetiye, basın açıklaması) taramaya kapalıdır.
 */
const AI_CRAWLERS = [
  "GPTBot",
  "OAI-SearchBot",
  "ChatGPT-User",
  "PerplexityBot",
  "Perplexity-User",
  "ClaudeBot",
  "Claude-User",
  "Claude-SearchBot",
  "Google-Extended",
  "Applebot-Extended",
  "meta-externalagent",
  "Bingbot",
  "YandexBot",
];

const HIDDEN = ["/davetiye/", "/basin-aciklamasi/"];

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      { userAgent: "*", allow: "/", disallow: HIDDEN },
      ...AI_CRAWLERS.map((ua) => ({ userAgent: ua, allow: "/", disallow: HIDDEN })),
    ],
    sitemap: `${site.url}/sitemap.xml`,
    host: site.url,
  };
}
