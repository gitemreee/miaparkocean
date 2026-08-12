import { Counter } from "@/components/ui/Counter";
import { Reveal } from "@/components/ui/Reveal";

const stats = [
  { value: 472, suffix: "", label: "1+0 Daire", note: "brüt 28 m²" },
  { value: 112, suffix: "", label: "1+1 Daire", note: "brüt 50 m²" },
  { value: 16, suffix: "", label: "2+1 Dubleks", note: "brüt 100 m²" },
  { value: 600, suffix: "", label: "Toplam Daire", note: "3 yaşam tipi" },
];

export function Stats() {
  return (
    <section className="surface-paper py-14 md:py-16">
      <div className="container-luxe">
        <div className="grid grid-cols-2 gap-y-10 rounded-3xl border border-ink/10 bg-white py-10 md:grid-cols-4">
          {stats.map((s, i) => (
            <Reveal key={s.label} delay={i * 0.08} className={`px-4 text-center md:px-6 ${i > 0 ? "md:border-l md:border-ink/10" : ""}`}>
              <div className="font-display text-5xl font-bold text-ink md:text-6xl">
                <Counter value={s.value} />
                <span className="text-accent">{s.suffix}</span>
              </div>
              <div className="mt-2 text-base font-semibold text-ink">{s.label}</div>
              <div className="text-xs text-ink/45">{s.note}</div>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}
