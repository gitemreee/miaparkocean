import { Counter } from "@/components/ui/Counter";
import { Reveal } from "@/components/ui/Reveal";
import { units } from "@/data/units";

/**
 * Daire dağılımı infografiği.
 *
 * Beş büyük rakam yerine tek okunur grafik: yığılmış oran çubuğu + lejant.
 * Hangi tipin projede ne kadar yer kapladığı bir bakışta görülür ve mobilde
 * çok daha az yer tutar.
 */
const SEGMENT_COLORS = ["#0f52ba", "#0c6c90", "#18789c", "#48b4cc"];

export function Stats() {
  const total = units.reduce((n, u) => n + u.count, 0);

  return (
    <section className="surface-paper py-10 md:py-14">
      <div className="container-luxe">
        <Reveal>
          <div className="card-gradient-border overflow-hidden p-5 shadow-[var(--shadow-card)] md:p-8">
            {/* Toplam */}
            <div className="flex flex-wrap items-end justify-between gap-x-6 gap-y-3">
              <div className="flex items-end gap-2.5">
                <span className="font-display text-[2.6rem] leading-none text-ink md:text-6xl">
                  <Counter value={total} />
                </span>
                <span className="mb-1 text-sm font-semibold text-ink/70 md:mb-2 md:text-base">Toplam Daire</span>
              </div>
              <span className="pill pill-ocean text-[0.72rem]">
                {units.length} yaşam tipi · 4 blok · 8 kat
              </span>
            </div>

            {/* Yığılmış oran çubuğu — tiplerin projedeki payı */}
            <div className="mt-5 flex h-3 w-full overflow-hidden rounded-full md:mt-6 md:h-3.5" aria-hidden="true">
              {units.map((u, i) => (
                <span
                  key={u.slug}
                  className="h-full"
                  style={{
                    width: `${(u.count / total) * 100}%`,
                    backgroundColor: SEGMENT_COLORS[i % SEGMENT_COLORS.length],
                  }}
                />
              ))}
            </div>

            {/* Lejant */}
            <ul className="mt-3 divide-y divide-ink/8 md:mt-5">
              {units.map((u, i) => (
                <li key={u.slug} className="flex items-center gap-3 py-2.5 md:py-3">
                  <span
                    className="h-2.5 w-2.5 shrink-0 rounded-full"
                    style={{ backgroundColor: SEGMENT_COLORS[i % SEGMENT_COLORS.length] }}
                    aria-hidden="true"
                  />
                  <span className="min-w-0 flex-1 truncate text-[0.88rem] font-semibold text-ink md:text-base">
                    {u.name}
                  </span>
                  <span className="shrink-0 text-[0.78rem] text-ink/45 md:text-sm">
                    {u.area.replace("Brüt ", "")}
                  </span>
                  <span className="w-11 shrink-0 text-right font-display text-lg leading-none text-ink md:w-16 md:text-2xl">
                    {u.count}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        </Reveal>
      </div>
    </section>
  );
}
