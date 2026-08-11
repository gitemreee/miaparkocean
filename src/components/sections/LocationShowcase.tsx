import { mapConfig } from "@/data/location";

// Uydu haritası üzerine MİA logosu + mesafe etiketleri (hepsi bizim fontta).
// Harita sabit (etkileşimsiz) tutulur ki etiketler konumla hizalı kalsın.
type Callout = { place: string; time: string; pos: string; align: "l" | "r" };

const callouts: Callout[] = [
  { place: "TEM Otoyolu", time: "5 dk", pos: "top-[7%] left-[5%]", align: "l" },
  { place: "Kocaeli Üniversitesi", time: "10 dk", pos: "top-[3%] left-1/2 -translate-x-1/2", align: "l" },
  { place: "Şehir Hastanesi", time: "5 dk", pos: "top-[9%] right-[5%]", align: "r" },
  { place: "Symbol AVM", time: "7 dk", pos: "top-[45%] right-[3%]", align: "r" },
  { place: "41 Burada AVM", time: "3 dk", pos: "bottom-[16%] right-[8%]", align: "r" },
  { place: "Şehir Merkezi", time: "5 dk", pos: "bottom-[12%] left-1/2 -translate-x-1/2", align: "l" },
  { place: "D100 Karayolu", time: "1 dk", pos: "top-[44%] left-[3%]", align: "l" },
  { place: "İzmit Sahili", time: "2 dk", pos: "bottom-[16%] left-[6%]", align: "l" },
];

// Uydu embed (t=k), etkileşimsiz gösterilir
const satelliteEmbed = `https://maps.google.com/maps?q=${mapConfig.lat},${mapConfig.lng}&t=k&z=16&hl=tr&output=embed`;

function Pill({ place, time, align }: { place: string; time: string; align: "l" | "r" }) {
  return (
    <div className={`flex items-center gap-2 ${align === "r" ? "flex-row-reverse" : ""}`}>
      <span className="relative flex h-2.5 w-2.5">
        <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-accent/60" />
        <span className="relative inline-flex h-2.5 w-2.5 rounded-full bg-accent" />
      </span>
      <span className="whitespace-nowrap rounded-lg bg-white/95 px-3 py-1.5 shadow-[0_8px_20px_-10px_rgba(20,20,20,0.6)] backdrop-blur">
        <span className="block text-[0.72rem] font-semibold leading-tight text-ink">{place}</span>
        <span className="block text-[0.68rem] font-semibold leading-tight text-accent">{time}</span>
      </span>
    </div>
  );
}

export function LocationShowcase() {
  return (
    <div>
      <div className="relative overflow-hidden rounded-[2rem] shadow-[var(--shadow-luxe)]">
        <div className="aspect-[16/11] md:aspect-[16/8]">
          {/* Uydu haritası — sabit, etkileşimsiz */}
          <iframe
            src={satelliteEmbed}
            title="MİA PARK OCEAN uydu konumu"
            className="pointer-events-none h-full w-full"
            loading="lazy"
            referrerPolicy="no-referrer-when-downgrade"
          />
        </div>
        {/* Etiket okunabilirliği için ince tül */}
        <div className="pointer-events-none absolute inset-0 bg-gradient-to-b from-ink/15 via-transparent to-ink/20" />

        {/* Bölge etiketi — bizim fontta */}
        <div className="absolute left-4 top-4">
          <span className="rounded-full bg-ink/85 px-4 py-1.5 text-xs font-semibold tracking-wide text-white backdrop-blur">
            İzmit MİA Bölgesi · Sanayi Mah.
          </span>
        </div>

        {/* Merkez — MİA monogramı (tam konum) */}
        <div className="absolute left-1/2 top-1/2 z-10 flex -translate-x-1/2 -translate-y-1/2 flex-col items-center">
          <span className="relative flex h-14 w-14 items-center justify-center rounded-full bg-accent shadow-[0_10px_28px_-8px_rgba(215,29,40,0.8)]">
            <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-accent/40" />
            <svg viewBox="0 0 40 42" className="relative h-8 w-8" aria-hidden="true">
              <path d="M6 32V12l14 10 14-10v20" fill="none" stroke="#fff" strokeWidth="2.6" strokeLinejoin="round" strokeLinecap="round" />
              <path d="M20 22v10" fill="none" stroke="#fff" strokeWidth="2.6" strokeLinecap="round" />
            </svg>
          </span>
          <span className="mt-2 whitespace-nowrap rounded-full bg-ink px-4 py-1.5 font-display text-sm font-bold tracking-wide text-white">
            MİA PARK OCEAN
          </span>
        </div>

        {/* Mesafe etiketleri — yalnızca geniş ekran */}
        <div className="hidden lg:block">
          {callouts.map((c) => (
            <div key={c.place} className={`absolute z-10 ${c.pos}`}>
              <Pill place={c.place} time={c.time} align={c.align} />
            </div>
          ))}
        </div>
      </div>

      {/* Mobil / tablet için etiket listesi */}
      <div className="mt-4 flex flex-wrap gap-2 lg:hidden">
        {callouts.map((c) => (
          <span key={c.place} className="inline-flex items-center gap-1.5 rounded-full bg-paper-2 px-3 py-1.5 text-xs">
            <span className="h-1.5 w-1.5 rounded-full bg-accent" />
            <span className="font-semibold text-ink">{c.place}</span>
            <span className="font-semibold text-accent">{c.time}</span>
          </span>
        ))}
      </div>
      <p className="mt-3 text-center text-xs text-ink/40 lg:text-right">Uydu görünümü · etiket konumları temsilidir.</p>
    </div>
  );
}
