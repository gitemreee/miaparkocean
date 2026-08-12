"use client";

import { useState, useEffect } from "react";
import { ChevronLeft, ChevronRight, Download, Maximize2, X } from "lucide-react";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { SmartImage } from "@/components/ui/SmartImage";
import { catalogPages, catalogPdf } from "@/data/media";

export function Catalog() {
  const [i, setI] = useState(0);
  const [full, setFull] = useState(false);
  const total = catalogPages.length;
  const go = (d: number) => setI((p) => (p + d + total) % total);

  useEffect(() => {
    if (!full) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") setFull(false);
      if (e.key === "ArrowRight") go(1);
      if (e.key === "ArrowLeft") go(-1);
    };
    document.addEventListener("keydown", onKey);
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", onKey);
      document.body.style.overflow = "";
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [full]);

  return (
    <section id="katalog" className="bg-pearl py-24 md:py-32">
      <div className="container-luxe">
        <SectionHeading
          eyebrow="Online Katalog"
          title={<>Projeyi <span className="gilded">sayfa sayfa</span> inceleyin</>}
          lead="MİA PARK OCEAN tanıtım kataloğunu çevrimiçi inceleyebilir, dilerseniz PDF olarak indirebilirsiniz."
        />

        <div className="mt-14 grid gap-8 lg:grid-cols-[1.15fr_1fr] lg:items-center">
          {/* Aktif sayfa */}
          <div className="relative mx-auto w-full max-w-md">
            <button
              type="button"
              onClick={() => setFull(true)}
              className="group block w-full overflow-hidden rounded-2xl bg-cream shadow-[var(--shadow-luxe)]"
              aria-label="Kataloğu tam ekran görüntüle"
            >
              <div className="aspect-[1414/2000]">
                <SmartImage src={catalogPages[i].src} alt={`Katalog — ${catalogPages[i].label}`} sizes="(max-width:1024px) 90vw, 40vw" className="h-full w-full object-cover" />
              </div>
              <span className="absolute right-3 top-3 flex h-9 w-9 items-center justify-center rounded-full bg-gradient-sapphire text-cream opacity-0 transition-opacity group-hover:opacity-100">
                <Maximize2 className="h-4 w-4" />
              </span>
            </button>
            <div className="mt-4 flex items-center justify-between">
              <button type="button" onClick={() => go(-1)} aria-label="Önceki sayfa" className="flex h-10 w-10 items-center justify-center rounded-full border border-ocean/15 text-ocean transition-colors hover:border-bronze hover:text-bronze">
                <ChevronLeft className="h-5 w-5" />
              </button>
              <span className="text-sm font-medium text-ocean/70">
                {i + 1} / {total} · {catalogPages[i].label}
              </span>
              <button type="button" onClick={() => go(1)} aria-label="Sonraki sayfa" className="flex h-10 w-10 items-center justify-center rounded-full border border-ocean/15 text-ocean transition-colors hover:border-bronze hover:text-bronze">
                <ChevronRight className="h-5 w-5" />
              </button>
            </div>
          </div>

          {/* Küçük resimler + indir */}
          <div>
            <div className="grid grid-cols-4 gap-3">
              {catalogPages.map((p, idx) => (
                <button
                  key={p.src}
                  type="button"
                  onClick={() => setI(idx)}
                  aria-label={`${idx + 1}. sayfa: ${p.label}`}
                  className={`overflow-hidden rounded-lg border-2 transition-colors ${idx === i ? "border-bronze" : "border-transparent hover:border-bronze/40"}`}
                >
                  <div className="aspect-[1414/2000]">
                    <SmartImage src={p.src} alt={p.label} sizes="120px" className="h-full w-full object-cover" />
                  </div>
                </button>
              ))}
            </div>

            <a
              href={catalogPdf}
              className="mt-8 inline-flex items-center gap-2 rounded-full bg-bronze px-8 py-4 text-sm font-medium text-cream transition-colors hover:bg-bronze-300"
              download="MIA-PARK-OCEAN-Brosur.pdf"
            >
              <Download className="h-4 w-4" /> Kataloğu PDF İndir
            </a>
            <p className="mt-3 text-xs text-ocean/45">Katalog görselleri Türkçe tanıtım broşüründen alınmıştır.</p>
          </div>
        </div>
      </div>

      {/* Tam ekran */}
      {full && (
        <div className="fixed inset-0 z-[60] flex items-center justify-center bg-ocean/95 p-4" onClick={() => setFull(false)} role="dialog" aria-modal="true">
          <button type="button" onClick={() => setFull(false)} aria-label="Kapat" className="absolute right-5 top-5 text-cream/80 hover:text-bronze">
            <X className="h-8 w-8" />
          </button>
          <button type="button" onClick={(e) => { e.stopPropagation(); go(-1); }} aria-label="Önceki" className="absolute left-3 text-cream/70 hover:text-bronze md:left-8">
            <ChevronLeft className="h-10 w-10" />
          </button>
          <img src={catalogPages[i].src} alt={catalogPages[i].label} className="max-h-[88vh] w-auto rounded-lg object-contain" onClick={(e) => e.stopPropagation()} />
          <button type="button" onClick={(e) => { e.stopPropagation(); go(1); }} aria-label="Sonraki" className="absolute right-3 text-cream/70 hover:text-bronze md:right-8">
            <ChevronRight className="h-10 w-10" />
          </button>
        </div>
      )}
    </section>
  );
}
