"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { AnimatePresence, motion } from "framer-motion";
import { ArrowRight, Ban, Percent, UserRoundX, CalendarClock, ShieldCheck } from "lucide-react";
import { SmartImage } from "@/components/ui/SmartImage";
import { WAVE_PATHS, WAVE_TILE } from "@/components/ui/Wave";

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
  { image: "/images/entrance-gate.webp", duration: 6000, kicker: "600 Daire · 4 Yaşam Tipi", line1: "Her detayıyla", accent: "ayrıcalıklı." },
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
    <section className="relative">
      <h1 className="sr-only">
        MİA PARK OCEAN — İzmit MİA Bölgesi konut projesi. Tasarrufa dayalı faizsiz finansman sistemiyle bankasız,
        faizsiz, kefilsiz; 60 ay vade.
      </h1>

      {/* Tam genişlik sahne */}
      <div className="relative min-h-[86vh] overflow-hidden md:min-h-[92vh]">
        {slides.map((s, i) => (
          <div
            key={s.image + i}
            className={`absolute inset-0 transition-opacity duration-[1200ms] ${i === index ? "opacity-100" : "opacity-0"}`}
          >
            {s.video ? (
              <video
                src={s.video}
                poster={s.poster ?? s.image}
                autoPlay
                muted
                loop
                playsInline
                preload="auto"
                className="h-full w-full scale-105 object-cover"
              />
            ) : (
              <SmartImage src={s.image} alt={s.kicker} sizes="100vw" className="h-full w-full scale-105 object-cover" />
            )}
          </div>
        ))}

        {/* Okyanus perdesi — lacivert/safirden zümrüde; metin okunurluğu için güçlü */}
        <div className="absolute inset-0 bg-[linear-gradient(to_top,rgba(0,9,38,0.95)_0%,rgba(2,14,46,0.82)_28%,rgba(6,26,74,0.55)_54%,rgba(15,82,186,0.3)_78%,rgba(1,50,32,0.38)_100%)]" />
        {/* Soldan sağa yumuşak koyulaşma — başlık bloğunu taşır */}
        <div className="absolute inset-0 bg-[linear-gradient(to_right,rgba(0,9,38,0.55)_0%,rgba(0,9,38,0.18)_46%,transparent_72%)]" />

        <div className="container-luxe relative flex min-h-[86vh] flex-col justify-end pb-32 pt-32 md:min-h-[92vh] md:pb-40 md:pt-36">
          <motion.span
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1] }}
            className="pill pill-light mb-6 w-fit"
          >
            <ShieldCheck className="h-4 w-4" /> Yahya Kaptan Birlik Güvencesiyle
          </motion.span>

          <div className="relative min-h-[8.5rem] sm:min-h-[11rem] md:min-h-[13.5rem]">
            <AnimatePresence mode="wait">
              <motion.div
                key={index}
                className="absolute inset-x-0 bottom-0"
                initial={{ opacity: 0, y: 18 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -12 }}
                transition={{ duration: 0.55, ease: [0.22, 1, 0.36, 1] }}
              >
                <p className="eyebrow text-ice/75">{active.kicker}</p>
                <h2 className="mt-4 max-w-3xl font-display text-[2.85rem] leading-[1] text-white sm:text-6xl md:text-[4.6rem]">
                  {active.line1}{" "}
                  <span className="gradient-text-light">{active.accent}</span>
                </h2>
              </motion.div>
            </AnimatePresence>
          </div>

          <p className="mt-6 max-w-lg text-lg leading-relaxed text-ice/85">
            Bankaya, faize ya da kefile gerek kalmadan; tasarruf esaslı faizsiz finansmanla ev sahibi olun.
          </p>

          <div className="mt-8 flex flex-wrap items-center gap-3">
            <Link href="/iletisim" className="btn-base btn-jade btn-shine group px-8 py-4 text-sm">
              Dairenizi Seçin
              <ArrowRight className="h-4 w-4 transition-transform duration-300 group-hover:translate-x-1" />
            </Link>
            <Link href="/kooperatif" className="btn-base btn-outline-light px-8 py-4 text-sm">
              Neden Kooperatif?
            </Link>
          </div>

          {/* Slide göstergeleri */}
          <div className="mt-10 flex gap-2">
            {slides.map((s, i) => (
              <button
                key={s.image + i}
                type="button"
                onClick={() => setIndex(i)}
                aria-label={`${i + 1}. görsel`}
                className={`h-1.5 rounded-full transition-all duration-500 ${
                  i === index ? "w-10 bg-gradient-surf" : "w-1.5 bg-white/45 hover:bg-white/80"
                }`}
              />
            ))}
          </div>
        </div>

        {/* İmza: logodaki dalga sahneyi beyaz sayfaya bağlar */}
        <div className="pointer-events-none absolute inset-x-0 bottom-0">
          {/* akan kurdele */}
          <div className="relative h-[46px] w-full overflow-hidden md:h-[70px]">
            <div className="wave-drift-slow absolute inset-0 w-[200%]">
              <svg viewBox="0 0 2880 140" preserveAspectRatio="none" className="h-full w-full">
                <path d={WAVE_TILE} fill="#d6e6f3" opacity="0.42" />
                <g transform="translate(1440 0)">
                  <path d={WAVE_TILE} fill="#d6e6f3" opacity="0.42" />
                </g>
              </svg>
            </div>
            <div className="wave-drift absolute inset-0 w-[200%]">
              <svg viewBox="0 0 2880 140" preserveAspectRatio="none" className="h-full w-full">
                <path d={WAVE_TILE} fill="#ffffff" opacity="0.6" />
                <g transform="translate(1440 0)">
                  <path d={WAVE_TILE} fill="#ffffff" opacity="0.6" />
                </g>
              </svg>
            </div>
          </div>
          {/* sabit dalga siluetı — logodaki kurdele dizilimi */}
          <svg viewBox="0 0 1440 120" preserveAspectRatio="none" className="-mt-px block h-[48px] w-full md:h-[76px]">
            <path d={WAVE_PATHS.back} fill="#d6e6f3" opacity="0.5" />
            <path d={WAVE_PATHS.mid} fill="#f3f8fc" opacity="0.85" />
            <path d={WAVE_PATHS.front} fill="#ffffff" />
          </svg>
        </div>
      </div>

      {/* Avantaj kartları — dalganın üstüne biner */}
      <div className="container-luxe">
        <div className="relative z-10 -mt-8 grid grid-cols-2 gap-3 md:-mt-14 md:grid-cols-4 md:gap-4">
          {perks.map((p, i) => (
            <motion.div
              key={p.title}
              initial={{ opacity: 0, y: 22 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-60px" }}
              transition={{ duration: 0.6, delay: i * 0.07, ease: [0.22, 1, 0.36, 1] }}
              className="card-luxe p-5"
            >
              <span className="flex h-11 w-11 items-center justify-center rounded-xl bg-gradient-surf text-white shadow-[0_10px_24px_-12px_rgba(15,82,186,0.8)]">
                <p.icon className="h-5 w-5" strokeWidth={2} />
              </span>
              <div className="mt-3.5 text-lg font-bold tracking-tight text-ink">{p.title}</div>
              <div className="text-sm leading-relaxed text-ink/55">{p.text}</div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
