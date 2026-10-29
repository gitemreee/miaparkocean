import type { Metadata } from "next";
import Link from "next/link";
import { Phone, ArrowRight } from "lucide-react";
import { contact } from "@/data/site";

export const metadata: Metadata = {
  title: "Sayfa bulunamadı",
  robots: { index: false, follow: true },
};

// Türkçe 404 — eski bağlantı ya da yanlış yazılmış adresle gelen ziyaretçiyi siteye geri kazandırır.
export default function NotFound() {
  const phone = contact.phones[0];
  return (
    <section className="surface-tint flex min-h-[70vh] items-center pb-20 pt-36 md:pt-44">
      <div className="container-luxe text-center">
        <span className="eyebrow text-accent">404</span>
        <h1 className="mx-auto mt-4 max-w-2xl text-balance font-display text-4xl leading-tight text-ink md:text-5xl">
          Aradığınız sayfa <span className="gilded">bulunamadı</span>
        </h1>
        <p className="mx-auto mt-5 max-w-xl text-pretty leading-relaxed text-ink/65">
          Bağlantı eskimiş ya da adres yanlış yazılmış olabilir. Aşağıdaki sayfalardan devam edebilir veya bizi arayabilirsiniz.
        </p>
        <div className="mt-9 flex flex-wrap justify-center gap-3">
          <Link href="/" className="btn-base btn-ocean btn-shine px-7 py-3.5 text-sm">
            Ana Sayfa <ArrowRight className="h-4 w-4" />
          </Link>
          <Link href="/daireler" className="btn-base btn-outline px-7 py-3.5 text-sm">
            Daireler
          </Link>
          <Link href="/iletisim" className="btn-base btn-outline px-7 py-3.5 text-sm">
            İletişim
          </Link>
        </div>
        <a href={phone.href} className="mt-8 inline-flex items-center gap-2 text-sm font-semibold text-ink/75 hover:text-accent">
          <Phone className="h-4 w-4 text-accent" /> {phone.label}
        </a>
      </div>
    </section>
  );
}
