import { Wallet, CalendarClock, HardHat, KeyRound, type LucideIcon } from "lucide-react";
import { Reveal } from "@/components/ui/Reveal";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { processIntro, processSteps } from "@/data/process";

const icons: Record<string, LucideIcon> = { Wallet, CalendarClock, HardHat, KeyRound };

/**
 * Ev sahibi olma süreci — ilerleme infografiği.
 *
 * Mobilde soldan geçen gradyan bir ray üzerinde dikey zaman çizelgesi,
 * masaüstünde aynı rayın yatay hâli. Adımlar birbirine bağlı görünür;
 * peşinattan tapuya akış tek bakışta okunur.
 */
export function Process() {
  return (
    <section id="surec" className="surface-tint py-12 md:py-24">
      <div className="container-luxe">
        <SectionHeading eyebrow={processIntro.eyebrow} title={processIntro.title} lead={processIntro.lead} />

        {/* ---------- Mobil: dikey ilerleme rayı ---------- */}
        <ol className="relative mt-10 md:hidden">
          {/* Gradyan ray */}
          <span
            className="absolute bottom-6 left-[21px] top-3 w-[3px] rounded-full bg-[linear-gradient(180deg,#0f52ba,#0c6c90_45%,#18789c_75%,#48b4cc)]"
            aria-hidden="true"
          />
          {processSteps.map((s, i) => {
            const Icon = icons[s.icon] ?? Wallet;
            return (
              <Reveal key={s.title} delay={i * 0.08}>
                <li className="relative flex gap-4 pb-7 last:pb-0">
                  <span className="relative z-10 flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-gradient-surf text-white shadow-[0_10px_22px_-12px_rgba(15,82,186,0.8)] ring-4 ring-white">
                    <Icon className="h-5 w-5" strokeWidth={2} />
                  </span>
                  <div className="min-w-0 pt-0.5">
                    <div className="flex items-center gap-2">
                      <span className="text-[0.68rem] font-bold uppercase tracking-[0.14em] text-accent">
                        Adım {i + 1}
                      </span>
                      <span className="h-px flex-1 bg-sapphire/15" aria-hidden="true" />
                    </div>
                    <h3 className="mt-1 font-display text-[1.15rem] leading-snug text-ink">{s.title}</h3>
                    <p className="mt-1 text-[0.85rem] leading-relaxed text-ink/60">{s.text}</p>
                  </div>
                </li>
              </Reveal>
            );
          })}
        </ol>

        {/* ---------- Masaüstü: yatay ilerleme rayı ---------- */}
        <ol className="relative mt-16 hidden md:grid md:grid-cols-4 md:gap-6">
          <span
            className="absolute left-[12.5%] right-[12.5%] top-7 h-[3px] rounded-full bg-[linear-gradient(90deg,#0f52ba,#0c6c90_45%,#18789c_75%,#48b4cc)]"
            aria-hidden="true"
          />
          {processSteps.map((s, i) => {
            const Icon = icons[s.icon] ?? Wallet;
            return (
              <Reveal key={s.title} delay={i * 0.1}>
                <li className="relative flex flex-col items-center text-center">
                  <span className="relative z-10 flex h-14 w-14 items-center justify-center rounded-full bg-gradient-surf text-white shadow-[0_12px_28px_-12px_rgba(15,82,186,0.7)] ring-8 ring-[#eef7fb]">
                    <Icon className="h-6 w-6" strokeWidth={2} />
                  </span>
                  <span className="mt-4 text-[0.68rem] font-bold uppercase tracking-[0.14em] text-accent">
                    Adım {i + 1}
                  </span>
                  <h3 className="mt-1.5 font-display text-xl text-ink">{s.title}</h3>
                  <p className="mt-2 text-sm leading-relaxed text-ink/60">{s.text}</p>
                </li>
              </Reveal>
            );
          })}
        </ol>
      </div>
    </section>
  );
}
