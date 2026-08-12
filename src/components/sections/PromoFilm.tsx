"use client";

import { useState, useEffect } from "react";
import { Play, X, Clapperboard } from "lucide-react";
import { SmartImage } from "@/components/ui/SmartImage";
import { promoVideo } from "@/data/media";

export function PromoFilm() {
  const [open, setOpen] = useState(false);
  const hasVideo = Boolean(promoVideo.url);

  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && setOpen(false);
    document.addEventListener("keydown", onKey);
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", onKey);
      document.body.style.overflow = "";
    };
  }, [open]);

  return (
    <section id="tanitim-filmi" className="section-dark relative overflow-hidden">
      <div className="absolute inset-0">
        <SmartImage src={promoVideo.poster} alt="MİA PARK OCEAN tanıtım filmi" sizes="100vw" className="h-full w-full object-cover" />
        <div className="absolute inset-0 bg-[linear-gradient(to_top,rgba(0,9,38,0.94)_0%,rgba(4,17,58,0.72)_44%,rgba(15,82,186,0.34)_78%,rgba(1,50,32,0.4)_100%)]" />
      </div>

      <div className="container-luxe relative z-10 flex min-h-[62vh] flex-col items-center justify-center py-24 text-center">
        <div className="flex items-center gap-3">
          <Clapperboard className="h-5 w-5 text-bronze-300" />
          <span className="eyebrow text-bronze-100">Tanıtım Filmi</span>
        </div>
        <h2 className="mt-5 max-w-2xl text-4xl leading-tight text-cream md:text-5xl">
          MİA PARK OCEAN'ı <span className="gradient-text-light">hareketle</span> keşfedin
        </h2>
        <p className="mt-4 max-w-lg text-lg text-cream/75">{promoVideo.caption}</p>

        <button
          type="button"
          onClick={() => hasVideo && setOpen(true)}
          disabled={!hasVideo}
          className="group mt-10 flex flex-col items-center"
          aria-label={hasVideo ? "Tanıtım filmini oynat" : "Tanıtım filmi çok yakında"}
        >
          <span className="relative flex h-20 w-20 items-center justify-center rounded-full bg-bronze text-cream shadow-[0_20px_44px_-16px_rgba(184,134,11,0.9)] transition-transform duration-300 group-hover:scale-105 group-disabled:opacity-70">
            {hasVideo && <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-bronze/50" />}
            <Play className="relative ml-1 h-8 w-8" fill="currentColor" />
          </span>
          <span className="mt-4 text-sm font-medium text-cream/80">
            {hasVideo ? "Filmi Oynat" : "Çok Yakında"}
          </span>
        </button>
      </div>

      {open && hasVideo && (
        <div className="fixed inset-0 z-[60] flex items-center justify-center bg-ocean/95 p-4" onClick={() => setOpen(false)} role="dialog" aria-modal="true">
          <button type="button" onClick={() => setOpen(false)} aria-label="Kapat" className="absolute right-5 top-5 text-cream/80 hover:text-bronze">
            <X className="h-8 w-8" />
          </button>
          <div className="aspect-video w-full max-w-4xl overflow-hidden rounded-xl bg-black" onClick={(e) => e.stopPropagation()}>
            <iframe
              src={promoVideo.url}
              title={promoVideo.title}
              className="h-full w-full"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            />
          </div>
        </div>
      )}
    </section>
  );
}
