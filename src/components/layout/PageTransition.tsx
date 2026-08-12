"use client";

import { usePathname } from "next/navigation";
import { AnimatePresence, motion, useReducedMotion } from "framer-motion";
import { useEffect, useRef, useState } from "react";
import "@/components/ui/Wave";

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
                key={layer.flat}
                className="absolute inset-x-0 top-0 h-full will-change-transform"
                initial={{ y: "116%" }}
                animate={{ y: "-106%" }}
                transition={{ duration: 1.05, delay: i * 0.075, ease: [0.7, 0, 0.28, 1] }}
              >
                {/* Öne geçen dalga kenarı — logodaki dalganın maskesi */}
                <span
                  className="wave-solid absolute bottom-full left-0 h-[9vh] w-full"
                  style={{
                    backgroundImage: layer.fill,
                    opacity: layer.opacity,
                    transform: "scaleY(-1)",
                  }}
                />
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

// Üç katman da aynı dalga; renkleri logodaki maviden lacivere derinleşir.
const WAVE_LAYERS = [
  { fill: "linear-gradient(135deg,#48b4cc,#18789c)", flat: "#48b4cc", opacity: 0.5 },
  { fill: "linear-gradient(135deg,#0f52ba,#0c6c90)", flat: "#0f52ba", opacity: 0.78 },
  { fill: "linear-gradient(135deg,#000926,#04304e 55%,#0a5578)", flat: "#04113a", opacity: 1 },
];
