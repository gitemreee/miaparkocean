"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { AnimatePresence, motion } from "framer-motion";
import { ArrowRight, Ban, Percent, UserRoundX, CalendarClock, ShieldCheck } from "lucide-react";
import { SmartImage } from "@/components/ui/SmartImage";

type Slide = {
  video?: string;
  image: string;
  poster?: string;
  duration: number;
  kicker: string;
  line1: string;
  accent: string;
};

// Önce video, sonra render'lar sırayla
const slides: Slide[] = [
  { video: "/videos/hero-tanitim.mp4", image: "/images/night-gate.webp", poster: "/images/entrance-gate.webp", duration: 9000, kicker: "İzmit MİA Bölgesi", line1: "Lüks artık", accent: "ulaşılabilir." },
  { image: "/images/hero-courtyard-dusk.webp", duration: 6000, kicker: "Yaşamınızın Yeni Merkezi", line1: "Hayatın yeni", accent: "merkezi." },
  { image: "/images/entrance-gate.webp", duration: 6000, kicker: "600 Daire · 3 Yaşam Tipi", line1: "Her detayıyla", accent: "ayrıcalıklı." },
  { image: "/images/courtyard-pools.webp", duration: 6000, kicker: "Merkezi Avlu · Süs Havuzları", line1: "Sosyal yaşam", accent: "kapınızda." },
  { image: "/images/night-gate.webp", duration: 6000, kicker: "Gece Aydınlatması", line1: "Gece bile", accent: "büyüleyici." },
];

const perks = [
  { icon: Ban, title: "Bankasız", text: "Krediye gerek yok" },
  { icon: Percent, title: "Faizsiz", text: "%0 faiz, vade farkı yok" },
  { icon: UserRoundX, title: "Kefilsiz", text: "Kefil aranmaz" },
  { icon: CalendarClock, title: "60 Ay Vade", text: "Sabit taksit imkânı" },
];

export function Hero() {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    const t = setTimeout(() => setIndex((i) => (i + 1) % slides.length), slides[index].duration);
    return () => clearTimeout(t);
  }, [index]);

  const active = slides[index];

  return (
    <section className="bg-paper pt-24 md:pt-28">
      <h1 className="sr-only">
        MİA PARK OCEAN — İzmit MİA Bölgesi konut projesi. Tasarrufa dayalı faizsiz finansman sistemiyle bankasız, faizsiz, kefilsiz; 60 ay vade.
      </h1>

      <div className="container-luxe">
        {/* Büyük görsel/video kart — slider */}
        <div className="relative min-h-[74vh] overflow-hidden rounded-[2rem] md:min-h-[70vh]">
          {slides.map((s, i) => (
            <div key={s.image + i} className={`absolute inset-0 transition-opacity duration-1000 ${i === index ? "opacity-100" : "opacity-0"}`}>
              {s.video ? (
                <video src={s.video} poster={s.poster ?? s.image} autoPlay muted loop playsInline preload="auto" className="h-full w-full object-cover" />
              ) : (
                <SmartImage src={s.image} alt={s.kicker} sizes="100vw" className="h-full w-full object-cover" />
              )}
            </div>
          ))}
          <div className="absolute inset-0 bg-gradient-to-t from-ink/85 via-ink/35 to-ink/10" />

          {/* İçerik */}
          <div className="relative flex min-h-[74vh] flex-col justify-end p-6 sm:p-10 md:min-h-[70vh] md:p-14">
            <span className="pill mb-5 w-fit bg-white/12 text-white backdrop-blur">
              <ShieldCheck className="h-4 w-4 text-white" /> Yahya Kaptan Birlik Güvencesiyle
            </span>

            <div className="relative min-h-[8rem] sm:min-h-[10.5rem] md:min-h-[13rem]">
              <AnimatePresence mode="wait">
                <motion.div
                  key={index}
                  className="absolute inset-x-0 bottom-0"
                  initial={{ opacity: 0, y: 14 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
                >
                  <p className="eyebrow text-white/70">{active.kicker}</p>
                  <h2 className="mt-3 max-w-2xl font-display text-[2.9rem] font-bold leading-[0.98] tracking-tight text-white sm:text-6xl md:text-7xl">
                    {active.line1} <span className="text-accent-300">{active.accent}</span>
                  </h2>
                </motion.div>
              </AnimatePresence>
            </div>

            <p className="mt-5 max-w-lg text-lg text-white/85">
              Bankaya, faize ya da kefile gerek kalmadan; tasarruf esaslı faizsiz finansmanla ev sahibi olun.
            </p>

            <div className="mt-7 flex flex-wrap items-center gap-3">
              <Link href="/iletisim" className="group inline-flex items-center gap-2 rounded-full bg-accent px-8 py-4 text-sm font-semibold text-white transition-colors hover:bg-accent-600">
                Dairenizi Seçin <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
              </Link>
              <Link href="/kooperatif" className="inline-flex items-center rounded-full border border-white/40 px-8 py-4 text-sm font-semibold text-white transition-colors hover:bg-white hover:text-ink">
                Neden Kooperatif?
              </Link>
            </div>

            {/* Slide göstergeleri */}
            <div className="mt-8 flex gap-2">
              {slides.map((s, i) => (
                <button key={s.image + i} type="button" onClick={() => setIndex(i)} aria-label={`${i + 1}. görsel`} className={`h-1.5 rounded-full transition-all duration-500 ${i === index ? "w-8 bg-white" : "w-1.5 bg-white/50 hover:bg-white/80"}`} />
              ))}
            </div>
          </div>
        </div>

        {/* Görselin üstüne binen avantaj kartları */}
        <div className="relative z-10 -mt-10 grid grid-cols-2 gap-3 px-2 md:-mt-12 md:grid-cols-4 md:gap-4 md:px-8">
          {perks.map((p) => (
            <div key={p.title} className="rounded-2xl border border-ink/8 bg-white p-5 shadow-[var(--shadow-card)]">
              <span className="flex h-11 w-11 items-center justify-center rounded-xl bg-accent-tint text-accent">
                <p.icon className="h-5 w-5" strokeWidth={2} />
              </span>
              <div className="mt-3 text-lg font-bold text-ink">{p.title}</div>
              <div className="text-sm text-ink/55">{p.text}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
