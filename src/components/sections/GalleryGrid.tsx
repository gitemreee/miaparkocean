"use client";

import { useCallback, useEffect, useState } from "react";
import { X, ChevronLeft, ChevronRight } from "lucide-react";
import { SmartImage } from "@/components/ui/SmartImage";
import { gallery as allImages, galleryCategories, type GalleryImage } from "@/data/gallery";

type GalleryGridProps = {
  images?: GalleryImage[];
  showFilter?: boolean;
};

export function GalleryGrid({ images = allImages, showFilter = false }: GalleryGridProps) {
  const [cat, setCat] = useState<string>("all");
  const [lightbox, setLightbox] = useState<number | null>(null);

  const filtered = cat === "all" ? images : images.filter((i) => i.category === cat);

  const close = useCallback(() => setLightbox(null), []);
  const move = useCallback(
    (dir: number) => setLightbox((i) => (i === null ? i : (i + dir + filtered.length) % filtered.length)),
    [filtered.length],
  );

  useEffect(() => {
    if (lightbox === null) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") close();
      if (e.key === "ArrowRight") move(1);
      if (e.key === "ArrowLeft") move(-1);
    };
    document.addEventListener("keydown", onKey);
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", onKey);
      document.body.style.overflow = "";
    };
  }, [lightbox, close, move]);

  return (
    <div>
      {showFilter && (
        <div className="mb-10 flex flex-wrap justify-center gap-2">
          {galleryCategories.map((c) => (
            <button
              key={c.key}
              type="button"
              onClick={() => setCat(c.key)}
              className={`rounded-full px-5 py-2 text-sm font-medium transition-colors ${
                cat === c.key ? "bg-bronze text-cream" : "border border-ocean/15 text-ocean/70 hover:border-bronze"
              }`}
            >
              {c.label}
            </button>
          ))}
        </div>
      )}

      <div className="grid grid-cols-2 gap-3 md:grid-cols-3 md:gap-4">
        {filtered.map((img, i) => (
          <button
            key={img.src}
            type="button"
            onClick={() => setLightbox(i)}
            className={`group relative overflow-hidden rounded-2xl ${img.wide ? "col-span-2" : ""}`}
          >
            <div className={`${img.wide ? "aspect-[16/9]" : "aspect-[4/3]"}`}>
              <SmartImage
                src={img.src}
                alt={img.alt}
                sizes="(max-width: 768px) 50vw, 33vw"
                className="h-full w-full object-cover transition-transform duration-700 group-hover:scale-105"
              />
            </div>
            <div className="absolute inset-0 bg-ocean/0 transition-colors duration-300 group-hover:bg-ocean/20" />
          </button>
        ))}
      </div>

      {/* Lightbox */}
      {lightbox !== null && (
        <div
          className="fixed inset-0 z-[60] flex items-center justify-center bg-ocean/95 p-4"
          onClick={close}
          role="dialog"
          aria-modal="true"
        >
          <button type="button" onClick={close} aria-label="Kapat" className="absolute right-5 top-5 text-cream/80 hover:text-bronze">
            <X className="h-8 w-8" />
          </button>
          <button
            type="button"
            onClick={(e) => { e.stopPropagation(); move(-1); }}
            aria-label="Önceki"
            className="absolute left-3 text-cream/70 hover:text-bronze md:left-8"
          >
            <ChevronLeft className="h-10 w-10" />
          </button>
          <figure className="max-h-[85vh] max-w-5xl" onClick={(e) => e.stopPropagation()}>
            <img
              src={filtered[lightbox].src}
              alt={filtered[lightbox].alt}
              className="max-h-[80vh] w-auto rounded-xl object-contain"
            />
            <figcaption className="mt-3 text-center text-sm text-cream/70">{filtered[lightbox].alt}</figcaption>
          </figure>
          <button
            type="button"
            onClick={(e) => { e.stopPropagation(); move(1); }}
            aria-label="Sonraki"
            className="absolute right-3 text-cream/70 hover:text-bronze md:right-8"
          >
            <ChevronRight className="h-10 w-10" />
          </button>
        </div>
      )}
    </div>
  );
}
