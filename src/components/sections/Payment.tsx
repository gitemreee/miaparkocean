import { Reveal } from "@/components/ui/Reveal";
import { Icon } from "@/components/ui/Icon";
import { payment } from "@/data/payment";
import { contact } from "@/data/site";
import { ArrowRight } from "lucide-react";

/**
 * Ödeme modeli.
 *
 * Sol sütun iddiayı ve rakamları taşır, sağ sütun avantajları. Mobilde
 * avantajlar iki sütunlu, kompakt kartlara düşer — sayfa kaydırma yükü düşük.
 */
export function Payment() {
  return (
    <section id="odeme" className="surface-tint py-12 md:py-24">
      <div className="container-luxe">
        <div className="grid gap-8 md:gap-12 lg:grid-cols-[1fr_1.1fr] lg:items-center">
          {/* Sol: başlık + iddia */}
          <div>
            <Reveal>
              <div className="flex items-center gap-3">
                <span className="gold-rule-solid w-8" />
                <span className="eyebrow text-accent">{payment.eyebrow}</span>
              </div>
            </Reveal>
            <Reveal delay={0.05}>
              <h2 className="mt-3 font-display text-[1.9rem] leading-[1.08] text-ink md:mt-5 md:text-5xl">
                {payment.title}
                <br />
                <span className="gradient-text">{payment.accent}</span>
              </h2>
            </Reveal>
            <Reveal delay={0.1}>
              <p className="mt-3 max-w-md text-[0.9rem] leading-relaxed text-ink/70 md:mt-6 md:text-lg">
                {payment.lead}
              </p>
            </Reveal>

            <Reveal delay={0.12}>
              <div className="mt-4 flex flex-wrap gap-2 md:mt-6 md:gap-2.5">
                {payment.trio.map((t) => (
                  <span
                    key={t}
                    className="inline-flex items-center gap-1.5 rounded-full bg-gradient-surf px-3.5 py-1.5 text-[0.78rem] font-medium text-white md:px-5 md:py-2 md:text-sm"
                  >
                    <span className="h-1.5 w-1.5 rounded-full bg-logo-light" />
                    {t}
                  </span>
                ))}
              </div>
            </Reveal>

            {/* Rakam bloğu */}
            <Reveal delay={0.15}>
              <div className="card-gradient-border mt-6 grid grid-cols-3 overflow-hidden md:mt-9">
                <div className="px-2 py-4 text-center md:px-4 md:py-6">
                  <div className="font-display text-2xl text-ink md:text-4xl">%0</div>
                  <div className="eyebrow mt-1.5 text-[0.52rem] text-ink/55 md:mt-2 md:text-[0.58rem]">Faiz</div>
                </div>
                <div className="border-x border-sapphire/12 px-2 py-4 text-center md:px-4 md:py-6">
                  <div className="font-display text-2xl text-accent md:text-4xl">{payment.headline.installments}</div>
                  <div className="eyebrow mt-1.5 text-[0.52rem] text-ink/55 md:mt-2 md:text-[0.58rem]">Ay Sabit Taksit</div>
                </div>
                <div className="px-2 py-4 text-center md:px-4 md:py-6">
                  <div className="font-display text-lg leading-tight text-ink md:text-3xl">Avantajlı</div>
                  <div className="eyebrow mt-1.5 text-[0.52rem] text-ink/55 md:mt-2 md:text-[0.58rem]">Peşinat</div>
                </div>
              </div>
            </Reveal>

            <Reveal delay={0.2}>
              <a
                href={contact.whatsapp.href}
                target="_blank"
                rel="noopener noreferrer"
                className="btn-base btn-ocean btn-shine mt-6 px-6 py-3 text-sm md:mt-8 md:px-8 md:py-4"
              >
                {payment.cta} <ArrowRight className="h-4 w-4" />
              </a>
            </Reveal>
          </div>

          {/* Sağ: avantaj kartları — mobilde iki sütun, kompakt */}
          <div className="grid grid-cols-2 gap-2.5 md:gap-4">
            {payment.cards.map((c, i) => (
              <Reveal key={c.title} delay={i * 0.06}>
                <div className="card-luxe flex h-full flex-col p-3.5 md:p-5">
                  <span className="icon-tile h-9 w-9 items-center justify-center rounded-lg md:h-11 md:w-11 md:rounded-xl">
                    <Icon name={c.icon} className="h-4 w-4 md:h-5 md:w-5" />
                  </span>
                  <h3 className="mt-2.5 font-display text-[0.95rem] leading-snug text-ink md:mt-4 md:text-lg">
                    {c.title}
                  </h3>
                  <p className="mt-1 text-[0.78rem] leading-snug text-ink/60 md:mt-2 md:text-sm md:leading-relaxed">
                    {c.text}
                  </p>
                </div>
              </Reveal>
            ))}
          </div>
        </div>

        {payment.note && (
          <Reveal delay={0.1}>
            <p className="mx-auto mt-8 max-w-3xl text-center text-xs leading-relaxed text-ink/45 md:mt-12">
              {payment.note}
            </p>
          </Reveal>
        )}
      </div>
    </section>
  );
}
