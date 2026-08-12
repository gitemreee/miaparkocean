"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { AnimatePresence, motion } from "framer-motion";
import { ArrowRight, Ban, Percent, UserRoundX, CalendarClock } from "lucide-react";
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
      <div className="relative min-h-[68vh] overflow-hidden md:min-h-[92vh]">
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

        {/* Okyanus perdesi — render'ı boğmayacak kadar hafif.
            Metin okunurluğu, alttaki yoğun bant ve sol taraftaki yumuşak
            koyulaşmayla sağlanır; görselin gökyüzü ve mimarisi açık kalır. */}
        <div className="absolute inset-0 bg-[linear-gradient(to_top,rgba(4,48,78,0.88)_0%,rgba(6,55,90,0.6)_26%,rgba(12,108,144,0.24)_52%,transparent_78%)]" />
        <div className="absolute inset-0 bg-[linear-gradient(to_right,rgba(4,48,78,0.5)_0%,rgba(4,48,78,0.14)_44%,transparent_70%)]" />

        <div className="container-luxe relative flex min-h-[68vh] flex-col justify-end pb-24 pt-28 md:min-h-[92vh] md:pb-40 md:pt-36">
          <div className="relative min-h-[6.5rem] sm:min-h-[10rem] md:min-h-[13.5rem]">
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
                <h2 className="mt-4 max-w-3xl font-display text-[2.15rem] leading-[1.04] text-white sm:text-5xl md:text-[4.6rem]">
                  {active.line1}{" "}
                  <span className="gradient-text-light">{active.accent}</span>
                </h2>
              </motion.div>
            </AnimatePresence>
          </div>

          <p className="mt-4 max-w-lg text-[0.95rem] leading-relaxed text-ice/85 md:mt-6 md:text-lg">
            Bankaya, faize ya da kefile gerek kalmadan; tasarruf esaslı faizsiz finansmanla ev sahibi olun.
          </p>

          <div className="mt-6 flex flex-wrap items-center gap-2.5 md:mt-8 md:gap-3">
            <Link href="/iletisim" className="btn-base btn-jade btn-shine group px-6 py-3 text-sm md:px-8 md:py-4">
              Dairenizi Seçin
              <ArrowRight className="h-4 w-4 transition-transform duration-300 group-hover:translate-x-1" />
            </Link>
            <Link href="/kooperatif" className="btn-base btn-outline-light px-6 py-3 text-sm md:px-8 md:py-4">
              Neden Kooperatif?
            </Link>
          </div>

          {/* Slide göstergeleri */}
          <div className="mt-7 flex gap-2 md:mt-10">
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
          <div className="relative h-[30px] w-full overflow-hidden md:h-[52px]">
            <div className="wave-drift-slow absolute inset-0 w-[200%]">
              <svg viewBox="0 0 2880 140" preserveAspectRatio="none" className="h-full w-full">
                <path d={WAVE_TILE} fill="#c6e9f2" opacity="0.32" />
                <g transform="translate(1440 0)">
                  <path d={WAVE_TILE} fill="#c6e9f2" opacity="0.32" />
                </g>
              </svg>
            </div>
            <div className="wave-drift absolute inset-0 w-[200%]">
              <svg viewBox="0 0 2880 140" preserveAspectRatio="none" className="h-full w-full">
                <path d={WAVE_TILE} fill="#ffffff" opacity="0.72" />
                <g transform="translate(1440 0)">
                  <path d={WAVE_TILE} fill="#ffffff" opacity="0.72" />
                </g>
              </svg>
            </div>
          </div>
          {/* sabit dalga siluetı — logodaki kurdele dizilimi */}
          <svg viewBox="0 0 1440 120" preserveAspectRatio="none" className="-mt-px block h-[48px] w-full md:h-[76px]">
            <path d={WAVE_PATHS.back} fill="#dff0f7" opacity="0.6" />
            <path d={WAVE_PATHS.mid} fill="#f2fafd" opacity="0.9" />
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
              <span className="icon-tile h-11 w-11 items-center justify-center rounded-xl">
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
