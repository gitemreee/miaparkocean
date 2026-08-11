import type { Metadata } from "next";
import { PageHero } from "@/components/layout/PageHero";
import Link from "next/link";
import { ArrowRight, BookOpen } from "lucide-react";
import { WhyCooperative } from "@/components/sections/WhyCooperative";
import { LegalAssurance } from "@/components/sections/LegalAssurance";
import { TrustSystem } from "@/components/sections/TrustSystem";
import { CooperativeOrg } from "@/components/sections/CooperativeOrg";
import { Faq } from "@/components/sections/Faq";
import { ContactForm } from "@/components/sections/ContactForm";
import { Reveal } from "@/components/ui/Reveal";
import { faq } from "@/data/faq";

export const metadata: Metadata = {
  title: "Neden Kooperatif? — Güvence ve Denetim",
  description:
    "Kooperatif modeli devlet gözetiminde, 1163 ve 7339 sayılı kanunlarla güvence altında. KOOPBİS / e-Devlet şeffaflığı, Bakanlık temsilcisi ve çok katmanlı denetim.",
};

export default function KooperatifPage() {
  return (
    <>
      <PageHero
        eyebrow="Güvence ve Denetim"
        title={<>Neden <span className="gilded">kooperatif?</span></>}
        lead="Kooperatif, kâr amacı gütmeyen güvenli bir yapıdır. Devletin kayıt ve denetim sistemine tabidir, e-Devlet üzerinden izlenebilir ve kararlarda ortağın söz hakkı vardır."
        image="/images/facade-warm.webp"
      />
      <WhyCooperative />
      <LegalAssurance />
      <TrustSystem />
      <CooperativeOrg />

      {/* Bilgi Merkezi yönlendirmesi */}
      <section className="bg-ocean py-20">
        <div className="container-luxe">
          <Reveal>
            <div className="flex flex-col items-center justify-between gap-6 rounded-3xl border border-bronze/20 bg-ocean-800 px-8 py-10 text-center sm:flex-row sm:text-left">
              <div className="flex items-start gap-4">
                <BookOpen className="mt-1 h-8 w-8 shrink-0 text-bronze-300" strokeWidth={1.4} />
                <div>
                  <h2 className="text-2xl text-cream">Bilgi Merkezi</h2>
                  <p className="mt-2 max-w-xl text-sm leading-relaxed text-cream/70">
                    Kooperatif modeli, üyelik, denetim, finansman ve inşaat süreçlerine dair kapsamlı rehber ve makaleler.
                  </p>
                </div>
              </div>
              <Link href="/bilgi-merkezi" className="inline-flex shrink-0 items-center gap-2 rounded-full bg-bronze px-7 py-3.5 text-sm font-medium text-cream transition-colors hover:bg-bronze-300">
                Bilgi Merkezi'ne Git <ArrowRight className="h-4 w-4" />
              </Link>
            </div>
          </Reveal>
        </div>
      </section>

      <Faq
        items={faq.filter((f) => f.category === "kooperatif")}
        eyebrow="Aklınızdaki Sorular"
        title={<>Kooperatif hakkında <span className="gilded">merak edilenler</span></>}
      />
      <ContactForm />
    </>
  );
}
