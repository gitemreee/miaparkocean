import { Counter } from "@/components/ui/Counter";
import { Reveal } from "@/components/ui/Reveal";
import { projectStats as stats } from "@/data/project";

export function Stats() {
  return (
    <section className="surface-paper py-14 md:py-16">
      <div className="container-luxe">
        <div className="grid grid-cols-2 gap-y-10 rounded-3xl border border-ink/10 bg-white py-10 md:grid-cols-5">
          {stats.map((s, i) => (
            // Tek kalan "Toplam Daire" kutusu mobilde iki sütunu birden kaplar.
            <Reveal
              key={s.label}
              delay={i * 0.08}
              className={`px-4 text-center md:px-6 ${i > 0 ? "md:border-l md:border-ink/10" : ""} ${
                i === stats.length - 1 && stats.length % 2 === 1 ? "col-span-2 md:col-span-1" : ""
              }`}
            >
              <div className="font-display text-4xl text-ink md:text-5xl">
                <Counter value={s.value} />
                <span className="text-accent">{s.suffix}</span>
              </div>
              <div className="mt-2 text-sm font-semibold text-ink">{s.label}</div>
              <div className="text-xs text-ink/45">{s.note}</div>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}
