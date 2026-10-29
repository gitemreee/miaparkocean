import type { Metadata } from "next";
import { FileText, Lock, Globe, Download } from "lucide-react";
import { PageHero } from "@/components/layout/PageHero";
import { Reveal } from "@/components/ui/Reveal";
import { BelgeForm } from "@/components/sections/BelgeForm";
import { documentGroups, docAccessLabels, docStatusLabels } from "@/data/documents";

export const metadata: Metadata = {
  alternates: { canonical: "/belgeler/" },
  title: "Belgeler",
  description:
    "MİA PARK OCEAN belge merkezi: proje kataloğu, kooperatif kayıt bilgileri, anasözleşme, inşaat ilerleme ve genel kurul belgeleri. Yayımlanan belgeleri indirin, hazırlananlar için talep bırakın.",
};

export default function BelgelerPage() {
  return (
    <>
      <PageHero
        eyebrow="Belgeler"
        title={<>Şeffaflık, <span className="gilded">belgeyle</span> başlar</>}
        lead="Yayımlanan belgeleri hemen indirebilirsiniz. Hazırlanan belgeler için talep bırakın; yayımlandıkça size iletelim."
        image="/images/facade-warm.webp"
      />

      <section className="surface-paper py-11 md:py-20">
        <div className="container-luxe grid gap-12 lg:grid-cols-[1fr_1fr] lg:items-start">
          {/* Belge listesi */}
          <div>
            <h2 className="text-2xl text-ink md:text-3xl">Belge merkezi</h2>
            <p className="mt-2 text-ink/55">Her belgenin yayın durumu ve erişim seviyesi yanında belirtilmiştir.</p>
            <div className="mt-8 space-y-8">
              {documentGroups.map((group) => (
                <Reveal key={group.title}>
                  <div>
                    <h3 className="flex items-center gap-2 text-lg font-bold text-ink">
                      <FileText className="h-4 w-4 text-accent" /> {group.title}
                    </h3>
                    <ul className="mt-3 space-y-2">
                      {group.items.map((doc) => (
                        <li key={doc.title} className="flex items-start justify-between gap-3 border-b border-ink/8 py-3 text-sm">
                          <span className="min-w-0">
                            {doc.href ? (
                              <a href={doc.href} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 font-semibold text-accent hover:underline">
                                <Download className="h-3.5 w-3.5" /> {doc.title}
                              </a>
                            ) : (
                              <span className="text-ink/80">{doc.title}</span>
                            )}
                            <span className="mt-0.5 block text-xs leading-snug text-ink/50">{doc.desc}</span>
                          </span>
                          <span className="flex shrink-0 flex-col items-end gap-1 text-xs">
                            <span
                              className={`rounded-full px-2 py-0.5 font-semibold ${
                                doc.status === "yayimlandi" ? "bg-[#12885f]/12 text-[#0b6e4f]" : "bg-ink/6 text-ink/55"
                              }`}
                            >
                              {docStatusLabels[doc.status]}
                            </span>
                            <span className="inline-flex items-center gap-1 text-ink/45">
                              {doc.access === "uye" ? <Lock className="h-3 w-3" /> : <Globe className="h-3 w-3" />}
                              {docAccessLabels[doc.access]}
                            </span>
                          </span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </Reveal>
              ))}
            </div>
          </div>

          {/* Talep formu */}
          <div className="lg:sticky lg:top-28">
            <Reveal>
              <BelgeForm />
            </Reveal>
          </div>
        </div>
      </section>
    </>
  );
}
