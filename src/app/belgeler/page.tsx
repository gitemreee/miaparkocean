import type { Metadata } from "next";
import { FileText, Lock, Globe } from "lucide-react";
import { PageHero } from "@/components/layout/PageHero";
import { Reveal } from "@/components/ui/Reveal";
import { BelgeForm } from "@/components/sections/BelgeForm";
import { documentGroups, docAccessLabels } from "@/data/documents";

export const metadata: Metadata = {
  title: "Belgeler",
  description:
    "MİA PARK OCEAN kooperatif belgeleri: anasözleşme, tapu-ruhsat, bütçe, denetim ve genel kurul belgeleri. Bilgilerinizi bırakın, belgeleri size gönderelim.",
};

export default function BelgelerPage() {
  return (
    <>
      <PageHero
        eyebrow="Belgeler"
        title={<>Şeffaflık, <span className="gilded">belgeyle</span> başlar</>}
        lead="Kooperatife dair belgeleri talep edebilirsiniz. Bilgilerinizi bırakın, belgeleri en kısa sürede size gönderelim."
        image="/images/facade-warm.webp"
      />

      <section className="bg-paper py-16 md:py-24">
        <div className="container-luxe grid gap-12 lg:grid-cols-[1fr_1fr] lg:items-start">
          {/* Belge listesi */}
          <div>
            <h2 className="text-2xl text-ink md:text-3xl">Talep edebileceğiniz belgeler</h2>
            <p className="mt-2 text-ink/55">Aşağıdaki belgeler; tür ve erişim seviyesiyle hazırlanmaktadır.</p>
            <div className="mt-8 space-y-8">
              {documentGroups.map((group) => (
                <Reveal key={group.title}>
                  <div>
                    <h3 className="flex items-center gap-2 text-lg font-bold text-ink">
                      <FileText className="h-4 w-4 text-accent" /> {group.title}
                    </h3>
                    <ul className="mt-3 space-y-2">
                      {group.items.map((doc) => (
                        <li key={doc.title} className="flex items-center justify-between gap-3 border-b border-ink/8 py-2.5 text-sm">
                          <span className="text-ink/75">{doc.title}</span>
                          <span className="inline-flex shrink-0 items-center gap-1.5 text-xs text-ink/45">
                            {doc.access === "uye" ? <Lock className="h-3.5 w-3.5" /> : <Globe className="h-3.5 w-3.5" />}
                            {docAccessLabels[doc.access]}
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
