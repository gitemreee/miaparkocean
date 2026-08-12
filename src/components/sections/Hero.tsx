"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { AnimatePresence, motion } from "framer-motion";
import { ArrowRight, Ban, Percent, UserRoundX, CalendarClock } from "lucide-react";
import { SmartImage } from "@/components/ui/SmartImage";
import { WaveEdge } from "@/components/ui/Wave";

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
  // Video ilk boyamayı bekletmesin: sayfa yerleşene kadar <video> hiç
  // basılmaz, yerine poster görseli durur. Bu sırada asıl içerik iner.
  const [videoReady, setVideoReady] = useState(false);

  useEffect(() => {
    const t = setTimeout(() => setIndex((i) => (i + 1) % slides.length), slides[index].duration);
    return () => clearTimeout(t);
  }, [index]);

  useEffect(() => {
    const idle =
      typeof window !== "undefined" && "requestIdleCallback" in window
        ? window.requestIdleCallback
        : (cb: () => void) => window.setTimeout(cb, 600);
    const id = idle(() => setVideoReady(true));
    return () => {
      if ("cancelIdleCallback" in window) window.cancelIdleCallback(id as number);
      else clearTimeout(id as number);
    };
  }, []);

  const active = slides[index];

  return (
    <section className="relative">
      <h1 className="sr-only">
        MİA PARK OCEAN — İzmit MİA Bölgesi konut projesi. Tasarrufa dayalı faizsiz finansman sistemiyle bankasız,
        faizsiz, kefilsiz; 60 ay vade.
      </h1>

      {/* Tam genişlik sahne */}
      <div className="wave-clip-end wave-h-hero relative min-h-[68vh] overflow-hidden md:min-h-[92vh]">
        {slides.map((s, i) => {
          // Yalnızca görünen ve bir sonraki kare basılır; kalanlar sıra
          // gelince yüklenir. Beş görselin tamamı baştan inmez.
          const near = i === index || i === (index + 1) % slides.length;
          return (
            <div
              key={s.image + i}
              className={`absolute inset-0 transition-opacity duration-[1200ms] ${i === index ? "opacity-100" : "opacity-0"}`}
            >
              {s.video ? (
                videoReady ? (
                  <video
                    src={s.video}
                    /* poster küçük varyant: video inerken tam boy görsel iki kez inmesin */
                    poster={(s.poster ?? s.image).replace(".webp", "-sm.webp")}
                    autoPlay
                    muted
                    loop
                    playsInline
                    preload="none"
                    className="h-full w-full scale-105 object-cover"
                  />
                ) : (
                  <SmartImage
                    src={s.poster ?? s.image}
                    alt={s.kicker}
                    priority
                    sizes="100vw"
                    className="h-full w-full scale-105 object-cover"
                  />
                )
              ) : (
                near && (
                  <SmartImage src={s.image} alt={s.kicker} sizes="100vw" className="h-full w-full scale-105 object-cover" />
                )
              )}
            </div>
          );
        })}

        {/* Okyanus perdesi — render'ı boğmayacak kadar hafif.
            En altta perde geri açılır: dalga koyu bir bandın değil, görselin
            kendisinin üstüne oturur; şeffaf PNG gibi durur. */}
        <div className="absolute inset-0 bg-[linear-gradient(to_top,rgba(4,40,58,0.22)_0%,rgba(4,40,58,0.5)_6%,rgba(4,40,58,0.86)_13%,rgba(9,86,120,0.56)_32%,rgba(26,116,150,0.2)_56%,transparent_80%)]" />
        <div className="absolute inset-0 bg-[linear-gradient(to_right,rgba(4,40,58,0.5)_0%,rgba(4,40,58,0.14)_44%,transparent_70%)]" />

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

        {/* İmza: logodaki dalganın kendisi sahneyi sayfaya bağlar.
            Sahne `.wave-clip-end` ile dalga şeklinde kesildiği için taban
            dolgusuna gerek yok — altındaki sayfa olduğu gibi görünür. */}
        <div className="pointer-events-none absolute inset-x-0 bottom-0">
          <WaveEdge fill={false} className="h-[58px] md:h-[104px]" />
        </div>
      </div>

      {/* Avantaj kartları — dalganın üstüne biner */}
      <div className="container-luxe">
        <div className="relative z-10 -mt-6 grid grid-cols-2 gap-2.5 md:-mt-14 md:grid-cols-4 md:gap-4">
          {perks.map((p, i) => (
            <motion.div
              key={p.title}
              initial={{ opacity: 0, y: 22 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-60px" }}
              transition={{ duration: 0.6, delay: i * 0.07, ease: [0.22, 1, 0.36, 1] }}
              className="card-luxe p-3.5 md:p-5"
            >
              <span className="icon-tile h-9 w-9 items-center justify-center rounded-lg md:h-11 md:w-11 md:rounded-xl">
                <p.icon className="h-4 w-4 md:h-5 md:w-5" strokeWidth={2} />
              </span>
              <div className="mt-2.5 text-[0.95rem] font-bold leading-tight tracking-tight text-ink md:mt-3.5 md:text-lg">
                {p.title}
              </div>
              <div className="mt-0.5 text-[0.78rem] leading-snug text-ink/55 md:text-sm md:leading-relaxed">
                {p.text}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
