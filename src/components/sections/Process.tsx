import { Wallet, CalendarClock, HardHat, KeyRound, type LucideIcon } from "lucide-react";
import { Reveal } from "@/components/ui/Reveal";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { processIntro, processSteps } from "@/data/process";

const icons: Record<string, LucideIcon> = { Wallet, CalendarClock, HardHat, KeyRound };

export function Process() {
  return (
    <section id="surec" className="surface-tint py-20 md:py-28">
      <div className="container-luxe">
        <SectionHeading eyebrow={processIntro.eyebrow} title={processIntro.title} lead={processIntro.lead} />

        <div className="relative mt-16 grid gap-6 md:grid-cols-4">
          {/* Bağlantı çizgisi (masaüstü) */}
          <div className="absolute left-0 right-0 top-8 hidden h-px bg-ink/10 md:block" />

          {processSteps.map((s, i) => {
            const Icon = icons[s.icon] ?? Wallet;
            return (
              <Reveal key={s.title} delay={i * 0.1}>
                <div className="relative flex flex-col items-center text-center">
                  <span className="relative z-10 flex h-16 w-16 items-center justify-center rounded-full bg-accent text-white shadow-[0_12px_28px_-12px_rgba(215,29,40,0.6)]">
                    <Icon className="h-7 w-7" strokeWidth={2} />
                    <span className="absolute -right-1 -top-1 flex h-6 w-6 items-center justify-center rounded-full bg-white text-xs font-bold text-accent shadow">
                      {i + 1}
                    </span>
                  </span>
                  <h3 className="mt-5 text-xl font-bold text-ink">{s.title}</h3>
                  <p className="mt-2 text-sm leading-relaxed text-ink/60">{s.text}</p>
                </div>
              </Reveal>
            );
          })}
        </div>
      </div>
    </section>
  );
}
