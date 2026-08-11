"use client";

import { useCallback, useEffect, useState } from "react";
import { X, ChevronLeft, ChevronRight } from "lucide-react";
import { SmartImage } from "@/components/ui/SmartImage";
import { gallery } from "@/data/gallery";

// Kayar galeri — sürekli akan film şeridi (marquee), üzerine gelince durur.
export function GallerySlider() {
  const [box, setBox] = useState<number | null>(null);
  const items = gallery;
  const loop = [...items, ...items]; // kesintisiz döngü için ikiye katla

  const close = useCallback(() => setBox(null), []);
  const move = useCallback(
    (d: number) => setBox((i) => (i === null ? i : (i + d + items.length) % items.length)),
    [items.length],
  );

  useEffect(() => {
    if (box === null) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") close();
      if (e.key === "ArrowRight") move(1);
      if (e.key === "ArrowLeft") move(-1);
    };
    document.addEventListener("keydown", onKey);
    document.body.style.overflow = "hidden";
    return () => { document.removeEventListener("keydown", onKey); document.body.style.overflow = ""; };
  }, [box, close, move]);

  return (
    <>
      <div className="marquee-wrap relative overflow-hidden">
        {/* kenar geçişleri */}
        <div className="pointer-events-none absolute inset-y-0 left-0 z-10 w-16 bg-gradient-to-r from-paper to-transparent md:w-28" />
        <div className="pointer-events-none absolute inset-y-0 right-0 z-10 w-16 bg-gradient-to-l from-paper to-transparent md:w-28" />

        <div className="marquee-track gap-4 pr-4">
          {loop.map((img, i) => (
            <button
              key={`${img.src}-${i}`}
              type="button"
              onClick={() => setBox(i % items.length)}
              className="group relative h-56 w-[300px] shrink-0 overflow-hidden rounded-2xl sm:h-72 sm:w-[400px]"
              aria-label={img.alt}
            >
              <SmartImage src={img.src} alt={img.alt} sizes="400px" className="h-full w-full object-cover transition-transform duration-700 group-hover:scale-105" />
              <span className="absolute inset-0 bg-ink/0 transition-colors group-hover:bg-ink/15" />
            </button>
          ))}
        </div>
      </div>

      {box !== null && (
        <div className="fixed inset-0 z-[60] flex items-center justify-center bg-ink/95 p-4" onClick={close} role="dialog" aria-modal="true">
          <button type="button" onClick={close} aria-label="Kapat" className="absolute right-5 top-5 text-white/80 hover:text-accent-300"><X className="h-8 w-8" /></button>
          <button type="button" onClick={(e) => { e.stopPropagation(); move(-1); }} aria-label="Önceki" className="absolute left-3 text-white/70 hover:text-accent-300 md:left-8"><ChevronLeft className="h-10 w-10" /></button>
          <figure className="max-h-[85vh] max-w-5xl" onClick={(e) => e.stopPropagation()}>
            <img src={items[box].src} alt={items[box].alt} className="max-h-[80vh] w-auto rounded-xl object-contain" />
            <figcaption className="mt-3 text-center text-sm text-white/70">{items[box].alt}</figcaption>
          </figure>
          <button type="button" onClick={(e) => { e.stopPropagation(); move(1); }} aria-label="Sonraki" className="absolute right-3 text-white/70 hover:text-accent-300 md:right-8"><ChevronRight className="h-10 w-10" /></button>
        </div>
      )}
    </>
  );
}
