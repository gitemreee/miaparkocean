import { ArrowUpRight } from "lucide-react";
import { Reveal } from "@/components/ui/Reveal";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { SmartImage } from "@/components/ui/SmartImage";
import { pressItems, pressIntro, pressAsset, type PressItem } from "@/data/press";

/** Haberin kendi alan adı — kartın altında kaynak künyesi olarak görünür. */
function domainOf(url: string) {
  try {
    return new URL(url).hostname.replace(/^www\./, "");
  } catch {
    return "";
  }
}

/**
 * Kartın tamamı bağlantıdır: görsele, başlığa, herhangi bir yerine dokunmak
 * haberin kendi sayfasını açar. Haber başka bir sitede olduğu için yeni
 * sekmede açılır ve alt künyede kaynağın alan adı yazar — okuyucu nereye
 * gittiğini tıklamadan önce görür.
 *
 * Yayın logosu beyaz bir plaketin içinde durur. Altı gazetenin logosu altı
 * farklı zemine göre çizilmiş (Gündem beyaz, İlke ve Fikir siyah); beyaz
 * plaket hepsini kendi renkleriyle okunur kılan tek ortak zemin.
 */
function PressCard({ item }: { item: PressItem }) {
  const a = pressAsset(item.slug);
  return (
    <a
      href={item.url}
      target="_blank"
      rel="noopener noreferrer"
      className="card-luxe group flex h-full flex-col overflow-hidden"
    >
      <div className="relative aspect-[16/9] overflow-hidden">
        <SmartImage
          src={a.image}
          alt={`${item.outlet} — ${item.title}`}
          sizes="(min-width: 1024px) 33vw, (min-width: 768px) 50vw, 100vw"
          className="h-full w-full object-cover transition duration-700 group-hover:scale-[1.04]"
        />
        {/* Logo plaketi görselin üstüne biner: kart tek bakışta hangi gazete belli olur */}
        <span className="absolute bottom-3 left-3 flex h-11 items-center rounded-xl bg-white/95 px-3 shadow-sm backdrop-blur-sm">
          <img
            src={a.logo}
            alt={item.outlet}
            loading="lazy"
            decoding="async"
            className="max-h-6 w-auto max-w-[120px] object-contain"
          />
        </span>
        <span className="absolute right-3 top-3 flex h-8 w-8 items-center justify-center rounded-full bg-white/90 text-ink/50 transition group-hover:bg-white group-hover:text-accent">
          <ArrowUpRight className="h-4 w-4" />
        </span>
      </div>

      <div className="flex flex-1 flex-col p-5 md:p-6">
        <h3 className="text-pretty text-[1.02rem] font-bold leading-snug text-ink md:text-[1.1rem]">
          {item.title}
        </h3>
        <p className="mt-2.5 text-pretty text-[0.85rem] leading-relaxed text-ink/60 md:text-sm">
          {item.excerpt}
        </p>

        <div className="mt-auto flex items-center gap-2 pt-5 text-[0.72rem] text-ink/45">
          <time dateTime={item.date}>{item.dateLabel}</time>
          <span aria-hidden="true">·</span>
          {/* Kaynak künyesi: haber bizim değil, gazetenin. */}
          <span className="truncate">{domainOf(item.url)}</span>
          <span className="ml-auto shrink-0 whitespace-nowrap font-semibold text-accent opacity-0 transition group-hover:opacity-100">
            Haberi oku
          </span>
        </div>
      </div>
    </a>
  );
}

export function PressCoverage() {
  if (!pressItems.length) return null;

  return (
    <section id="basinda-biz" className="surface-tint py-12 md:py-24">
      <div className="container-luxe">
        <SectionHeading
          eyebrow="Basında Biz"
          title={<>Kocaeli basını <span className="gilded whitespace-nowrap">MİA PARK OCEAN</span>&apos;ı yazdı</>}
          lead={pressIntro}
        />

        <div className="mt-12 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {pressItems.map((item, i) => (
            <Reveal key={item.url} delay={(i % 3) * 0.07}>
              <PressCard item={item} />
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}
