import { ShieldCheck, FileText } from "lucide-react";
import { YkbLogo } from "./YkbLogo";
import { KoopbisLogo } from "./KoopbisLogo";
import { TicaretBakanligiLogo } from "./TicaretBakanligiLogo";
import { LogoImage } from "./LogoImage";

// Footer üstü "Resmî Kayıt ve Denetim" güven şeridi.
// Gerçek logolar (KOOPBİS, T.C. Ticaret Bakanlığı, YKB, Ocean) + resmî belge linkleri.
const OFFICIAL_DOCS = [
  {
    label: "1163 Sayılı Kooperatifler Kanunu (PDF)",
    href: "https://www.mevzuat.gov.tr/mevzuatmetin/1.5.1163.pdf",
  },
  {
    label: "KOOPBİS Aydınlatma Metni (PDF)",
    href: "https://ticaret.gov.tr/data/5d41985f13b87639ac9e0095/Ayd%C4%B1nlatma%20Metni%20-%20KOOPB%C4%B0S.pdf",
  },
];

export function RegistryBadges() {
  return (
    <section aria-label="Resmî kayıt ve denetim" className="border-t border-ink/10 bg-paper-2">
      <div className="container-luxe py-12 md:py-14">
        <div className="mx-auto max-w-2xl text-center">
          <div className="eyebrow inline-flex items-center gap-2 text-accent">
            <ShieldCheck className="h-4 w-4" />
            Resmî Kayıt ve Denetim
          </div>
          <p className="mx-auto mt-4 max-w-xl text-sm leading-relaxed text-ink/70 sm:text-[0.95rem]">
            <strong className="font-semibold text-ink">S.S. Yahya Kaptan Birlik Yapı Kooperatifi</strong>, T.C.
            Ticaret Bakanlığı bünyesindeki{" "}
            <strong className="font-semibold text-ink">KOOPBİS (Kooperatif Bilgi Sistemi)</strong>&apos;ne kayıtlıdır.
            Süreçler 1163 sayılı Kooperatifler Kanunu kapsamında e-Devlet üzerinden izlenebilir ve resmî denetime tabidir.
          </p>
        </div>

        <div className="mx-auto mt-9 grid max-w-4xl grid-cols-2 gap-3 sm:flex sm:flex-wrap sm:justify-center sm:gap-4">
          {/* KOOPBİS */}
          <div className="flex h-[5.75rem] flex-1 flex-col items-center justify-center gap-1.5 rounded-2xl border border-ink/12 bg-white px-4 shadow-[0_1px_2px_rgba(0,0,0,0.04)] sm:min-w-[9.5rem]">
            <span className="flex h-10 items-center">
              <LogoImage src="/koopbis-logo.png" alt="KOOPBİS — Kooperatif Bilgi Sistemi" className="h-7 w-auto rounded-md">
                <KoopbisLogo className="h-7 w-auto rounded-md" />
              </LogoImage>
            </span>
            <span className="text-[0.6rem] font-semibold uppercase tracking-[0.1em] text-ink/45">Kayıt Sistemi</span>
          </div>

          {/* T.C. Ticaret Bakanlığı */}
          <div className="flex h-[5.75rem] flex-1 flex-col items-center justify-center gap-1.5 rounded-2xl border border-ink/12 bg-white px-4 shadow-[0_1px_2px_rgba(0,0,0,0.04)] sm:min-w-[9.5rem]">
            <span className="flex h-10 items-center">
              <LogoImage src="/ticaret-bakanligi-logo.webp" alt="T.C. Ticaret Bakanlığı" className="h-10 w-auto">
                <TicaretBakanligiLogo className="h-9 w-auto" />
              </LogoImage>
            </span>
            <span className="text-[0.6rem] font-semibold uppercase tracking-[0.1em] text-ink/45">Denetim Otoritesi</span>
          </div>

          {/* Yapımcı — YKB */}
          <div className="flex h-[5.75rem] flex-1 flex-col items-center justify-center gap-1.5 rounded-2xl border border-ink/12 bg-white px-4 shadow-[0_1px_2px_rgba(0,0,0,0.04)] sm:min-w-[9.5rem]">
            <span className="flex h-10 items-center">
              <LogoImage src="/ykb-logo.png" alt="S.S. Yahya Kaptan Birlik Yapı Kooperatifi" className="h-10 w-auto">
                <YkbLogo className="h-9 w-auto text-ink" />
              </LogoImage>
            </span>
            <span className="text-[0.6rem] font-semibold uppercase tracking-[0.1em] text-ink/45">Yapımcı Kooperatif</span>
          </div>

          {/* Tek Yetkili Satıcı — Ocean */}
          <div className="flex h-[5.75rem] flex-1 flex-col items-center justify-center gap-1.5 rounded-2xl border border-ink/12 bg-white px-4 shadow-[0_1px_2px_rgba(0,0,0,0.04)] sm:min-w-[9.5rem]">
            <span className="flex h-10 items-center">
              <img src="/ocean-logo.webp" alt="Ocean Gayrimenkul" width={160} height={36} className="h-6 w-auto" />
            </span>
            <span className="text-[0.6rem] font-semibold uppercase tracking-[0.1em] text-ink/45">Tek Yetkili Satıcı</span>
          </div>
        </div>

        {/* Resmî belgeler */}
        <div className="mt-7 flex flex-wrap items-center justify-center gap-x-6 gap-y-2.5">
          {OFFICIAL_DOCS.map((doc) => (
            <a
              key={doc.href}
              href={doc.href}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 text-xs font-medium text-ink/55 transition-colors hover:text-accent"
            >
              <FileText className="h-3.5 w-3.5" />
              {doc.label}
            </a>
          ))}
        </div>
      </div>
    </section>
  );
}
