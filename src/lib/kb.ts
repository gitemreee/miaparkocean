// Bilgi Merkezi yardımcıları: makale + rehberleri birleştirir.
import { articles, kbCategories, type Article, type KbCategoryKey } from "@/data/articles";
import { guides } from "@/data/guides";

export const allArticles: Article[] = [...articles, ...guides];

export function getArticle(slug: string): Article | undefined {
  return allArticles.find((a) => a.slug === slug);
}

export function articlesByCategory(key: KbCategoryKey): Article[] {
  return allArticles.filter((a) => a.category === key);
}

export function relatedArticles(current: Article, count = 3): Article[] {
  const sameCat = allArticles.filter((a) => a.category === current.category && a.slug !== current.slug);
  if (sameCat.length >= count) return sameCat.slice(0, count);
  const others = allArticles.filter((a) => a.category !== current.category && a.slug !== current.slug);
  return [...sameCat, ...others].slice(0, count);
}

export function categoryTitle(key: KbCategoryKey): string {
  return kbCategories.find((c) => c.key === key)?.title ?? "";
}
