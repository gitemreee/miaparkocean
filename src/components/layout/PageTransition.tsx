"use client";

import { usePathname } from "next/navigation";
import { AnimatePresence, motion, useReducedMotion } from "framer-motion";
import { useEffect, useRef, useState } from "react";
import { WAVE_PATHS } from "@/components/ui/Wave";

/**
 * Sayfa geçişi — "dalga geliyor".
 *
 * Rota değiştiğinde logodaki dalga ekranın altından yükselir, sayfayı süpürerek
 * geçer ve üstten çıkar. Üç katman logodaki kurdele diziliminde, birbirini
 * kovalayan gecikmelerle akar; arkasından yeni sayfa yumuşakça belirir.
 *
 * İlk yüklemede oynatılmaz (LCP'yi geciktirmemek için).
 */
export function PageTransition({ children }: { children: React.ReactNode }) {
  const pathname = usePathname() || "/";
  const reduce = useReducedMotion();
  const first = useRef(true);
  const [sweep, setSweep] = useState<string | null>(null);

  useEffect(() => {
    if (first.current) {
      first.current = false;
      return;
    }
    setSweep(pathname);
    const t = setTimeout(() => setSweep(null), 1400);
    return () => clearTimeout(t);
  }, [pathname]);

  if (reduce) return <>{children}</>;

  return (
    <>
      <AnimatePresence>
        {sweep && (
          <div key={sweep} className="pointer-events-none fixed inset-0 z-[90] overflow-hidden" aria-hidden="true">
            {WAVE_LAYERS.map((layer, i) => (
              <motion.div
                key={layer.d}
                className="absolute inset-x-0 top-0 h-full will-change-transform"
                initial={{ y: "116%" }}
                animate={{ y: "-106%" }}
                transition={{ duration: 1.05, delay: i * 0.075, ease: [0.7, 0, 0.28, 1] }}
              >
                {/* Öne geçen dalga kenarı */}
                <svg
                  viewBox="0 0 1440 120"
                  preserveAspectRatio="none"
                  className="absolute bottom-full left-0 h-[10vh] w-full"
                  style={{ transform: "scaleY(-1)" }}
                >
                  <path d={layer.d} fill={layer.flat} opacity={layer.opacity} />
                </svg>
                {/* Dalganın gövdesi */}
                <div className="absolute inset-0" style={{ backgroundImage: layer.fill, opacity: layer.opacity }} />
              </motion.div>
            ))}
          </div>
        )}
      </AnimatePresence>

      <motion.div
        key={pathname}
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.28, ease: [0.22, 1, 0.36, 1] }}
      >
        {children}
      </motion.div>
    </>
  );
}

// Logodaki kurdele sırası: önde açık safir-zümrüt, arkada derin lacivert.
const WAVE_LAYERS = [
  { d: WAVE_PATHS.back, fill: "linear-gradient(135deg,#3e77ce,#12885f)", flat: "#3e77ce", opacity: 0.5 },
  { d: WAVE_PATHS.mid, fill: "linear-gradient(135deg,#0f52ba,#0b6e4f)", flat: "#0f52ba", opacity: 0.78 },
  { d: WAVE_PATHS.front, fill: "linear-gradient(135deg,#000926,#04113a 55%,#013220)", flat: "#04113a", opacity: 1 },
];
