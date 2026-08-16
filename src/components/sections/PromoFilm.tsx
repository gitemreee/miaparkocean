"use client";

import { useState, useEffect, useRef } from "react";
import { Volume2, X, Clapperboard, Maximize2 } from "lucide-react";
import { SmartImage } from "@/components/ui/SmartImage";
import { promoVideo } from "@/data/media";

export function PromoFilm() {
  const [open, setOpen] = useState(false);
  // Bölüm ekrana girene kadar filmden tek bayt inmez. Sayfayı hiç aşağı
  // kaydırmayan ziyaretçi 25 MB'ı boşuna indirmesin.
  const [inView, setInView] = useState(false);
  const [playing, setPlaying] = useState(false);

  const embed = Boolean(promoVideo.url);
  const hasVideo = embed || Boolean(promoVideo.file);
  const sectionRef = useRef<HTMLElement>(null);
  const inlineRef = useRef<HTMLVideoElement>(null);
  const modalRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    const el = sectionRef.current;
    if (!el || embed || !hasVideo) return;
    const io = new IntersectionObserver(
      ([e]) => setInView(e.isIntersecting),
      { threshold: 0.35 },
    );
    io.observe(el);
    return () => io.disconnect();
  }, [embed, hasVideo]);

  // Görünürken sessiz oynar, ekrandan çıkınca durur: arkada boşuna
  // çözülüp pil ve bant yemesin.
  useEffect(() => {
    const v = inlineRef.current;
    if (!v) return;
    if (inView && !open) v.play().catch(() => {});
    else v.pause();
  }, [inView, open]);

  // Sesli izlemeye geçerken film baştan başlamasın, kaldığı yerden sürsün.
  const openWithSound = () => {
    if (!hasVideo) return;
    setOpen(true);
    const at = inlineRef.current?.currentTime ?? 0;
    requestAnimationFrame(() => {
      const m = modalRef.current;
      if (!m) return;
      m.currentTime = at;
      m.play().catch(() => {});
    });
  };

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
    <section id="tanitim-filmi" ref={sectionRef} className="section-dark relative overflow-hidden">
      <div className="absolute inset-0">
        <SmartImage
          src={promoVideo.poster}
          alt="MİA PARK OCEAN tanıtım filmi"
          sizes="100vw"
          className={`h-full w-full object-cover transition-opacity duration-1000 ${playing ? "opacity-0" : "opacity-100"}`}
        />
        {inView && !embed && hasVideo && (
          <video
            ref={inlineRef}
            src={promoVideo.file}
            muted
            playsInline
            preload="metadata"
            onPlaying={() => setPlaying(true)}
            onEnded={() => setPlaying(false)}
            className={`absolute inset-0 h-full w-full object-cover transition-opacity duration-1000 ${playing ? "opacity-100" : "opacity-0"}`}
          />
        )}
        {/* Film oynarken perde hafifler: kendi görüntüsü görünsün */}
        <div
          className={`absolute inset-0 transition-opacity duration-1000 bg-[linear-gradient(to_top,rgba(0,9,38,0.94)_0%,rgba(4,17,58,0.72)_44%,rgba(15,82,186,0.34)_78%,rgba(1,50,32,0.4)_100%)] ${playing ? "opacity-55" : "opacity-100"}`}
        />
      </div>

      <div className="container-luxe relative z-10 flex min-h-[62vh] flex-col items-center justify-center py-24 text-center">
        {/* Film başlayınca başlık çekilir — filmin kendi yazılarıyla çakışmasın */}
        <div className={`transition-opacity duration-700 ${playing ? "pointer-events-none opacity-0" : "opacity-100"}`}>
          <div className="flex items-center justify-center gap-3">
            <Clapperboard className="h-5 w-5 text-bronze-300" />
            <span className="eyebrow text-bronze-100">Tanıtım Filmi</span>
          </div>
          <h2 className="mt-5 max-w-2xl text-4xl leading-tight text-cream md:text-5xl">
            MİA PARK OCEAN&apos;ı <span className="gradient-text-light">hareketle</span> keşfedin
          </h2>
          <p className="mt-4 max-w-lg text-lg text-cream/75">{promoVideo.caption}</p>
        </div>

        <button
          type="button"
          onClick={openWithSound}
          disabled={!hasVideo}
          className={`group flex items-center gap-3 rounded-full border border-cream/30 bg-ocean/45 px-6 py-3 text-cream backdrop-blur-sm transition hover:border-bronze hover:bg-ocean/70 disabled:opacity-60 ${playing ? "mt-0" : "mt-10"}`}
          aria-label={hasVideo ? "Filmi sesli ve tam ekran izle" : "Tanıtım filmi çok yakında"}
        >
          {hasVideo ? (
            <>
              <span className="relative flex h-10 w-10 items-center justify-center rounded-full bg-bronze text-cream">
                {!playing && <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-bronze/50" />}
                <Volume2 className="relative h-5 w-5" />
              </span>
              <span className="text-sm font-medium">
                {playing ? "Sesi aç · tam ekran" : "Sesli izle"}
              </span>
              <Maximize2 className="h-4 w-4 text-cream/60" />
            </>
          ) : (
            <span className="text-sm font-medium">Çok Yakında</span>
          )}
        </button>
        {promoVideo.duration && (
          <span className="mt-4 text-sm text-cream/55">
            {playing ? `${promoVideo.duration} · sessiz önizleme oynuyor` : `${promoVideo.duration} · sesli`}
          </span>
        )}
      </div>

      {open && hasVideo && (
        <div
          className="fixed inset-0 z-[60] flex items-center justify-center bg-ocean/95 p-4"
          onClick={() => setOpen(false)}
          role="dialog"
          aria-modal="true"
        >
          <button
            type="button"
            onClick={() => setOpen(false)}
            aria-label="Kapat"
            className="absolute right-5 top-5 text-cream/80 hover:text-bronze"
          >
            <X className="h-8 w-8" />
          </button>
          <div className="aspect-video w-full max-w-5xl overflow-hidden rounded-xl bg-black" onClick={(e) => e.stopPropagation()}>
            {embed ? (
              <iframe
                src={promoVideo.url}
                title={promoVideo.title}
                className="h-full w-full"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              />
            ) : (
              <video
                ref={modalRef}
                src={promoVideo.file}
                poster={promoVideo.poster}
                title={promoVideo.title}
                controls
                playsInline
                preload="auto"
                className="h-full w-full"
              />
            )}
          </div>
        </div>
      )}
    </section>
  );
}
