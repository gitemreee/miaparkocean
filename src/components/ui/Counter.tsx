"use client";

import { useEffect, useRef, useState } from "react";
import { useInView } from "framer-motion";

type CounterProps = {
  value: number;
  durationMs?: number;
  className?: string;
};

// Görünür olunca 0'dan hedefe sayan animasyonlu sayaç.
export function Counter({ value, durationMs = 1400, className }: CounterProps) {
  const ref = useRef<HTMLSpanElement>(null);
  const inView = useInView(ref, { once: true, margin: "-60px" });
  const [display, setDisplay] = useState(0);

  useEffect(() => {
    if (!inView) return;
    let raf = 0;
    const start = performance.now();
    const tick = (now: number) => {
      const p = Math.min((now - start) / durationMs, 1);
      if (p >= 1) {
        // Son kareyi yuvarlamaya bırakma: hedef değeri birebir yaz.
        setDisplay(value);
        return;
      }
      const eased = 1 - Math.pow(1 - p, 3);
      setDisplay(Math.round(eased * value));
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [inView, value, durationMs]);

  return (
    <span ref={ref} className={className}>
      {display}
    </span>
  );
}
