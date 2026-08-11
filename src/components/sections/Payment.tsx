import { Reveal } from "@/components/ui/Reveal";
import { Icon } from "@/components/ui/Icon";
import { payment } from "@/data/payment";
import { contact } from "@/data/site";
import { ArrowRight } from "lucide-react";

export function Payment() {
  return (
    <section id="odeme" className="bg-cream-200 py-24 md:py-32">
      <div className="container-luxe">
        <div className="grid gap-14 lg:grid-cols-[1fr_1.1fr] lg:items-center">
          {/* Sol: başlık + iddia */}
          <div>
            <Reveal>
              <div className="flex items-center gap-3">
                <span className="gold-rule-solid w-8" />
                <span className="eyebrow text-bronze">{payment.eyebrow}</span>
              </div>
            </Reveal>
            <Reveal delay={0.05}>
              <h2 className="mt-5 text-4xl leading-[1.06] text-ocean md:text-5xl">
                {payment.title}
                <br />
                <span className="gilded">{payment.accent}</span>
              </h2>
            </Reveal>
            <Reveal delay={0.1}>
              <p className="mt-6 max-w-md text-lg leading-relaxed text-ocean/75">{payment.lead}</p>
            </Reveal>

            <Reveal delay={0.12}>
              <div className="mt-6 flex flex-wrap gap-2.5">
                {payment.trio.map((t) => (
                  <span key={t} className="inline-flex items-center gap-2 rounded-full bg-ocean px-5 py-2 text-sm font-medium text-cream">
                    <span className="h-1.5 w-1.5 rounded-full bg-bronze-300" />
                    {t}
                  </span>
                ))}
              </div>
            </Reveal>

            {/* Rakam bloğu */}
            <Reveal delay={0.15}>
              <div className="mt-9 grid grid-cols-3 overflow-hidden rounded-2xl border border-bronze/25 bg-cream">
                <div className="px-4 py-6 text-center">
                  <div className="font-display text-3xl text-ocean md:text-4xl">%0</div>
                  <div className="eyebrow mt-2 text-[0.58rem] text-ocean/55">Faiz</div>
                </div>
                <div className="border-x border-bronze/20 px-4 py-6 text-center">
                  <div className="font-display text-3xl text-bronze md:text-4xl">{payment.headline.installments}</div>
                  <div className="eyebrow mt-2 text-[0.58rem] text-ocean/55">Ay Sabit Taksit</div>
                </div>
                <div className="px-4 py-6 text-center">
                  <div className="font-display text-2xl leading-tight text-ocean md:text-3xl">Avantajlı</div>
                  <div className="eyebrow mt-2 text-[0.58rem] text-ocean/55">Peşinat</div>
                </div>
              </div>
            </Reveal>

            <Reveal delay={0.2}>
              <a
                href={contact.whatsapp.href}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-8 inline-flex items-center gap-2 rounded-full bg-bronze px-8 py-4 text-sm font-medium text-cream transition-colors hover:bg-bronze-300"
              >
                {payment.cta} <ArrowRight className="h-4 w-4" />
              </a>
            </Reveal>
          </div>

          {/* Sağ: avantaj kartları */}
          <div className="grid gap-5 sm:grid-cols-2">
            {payment.cards.map((c, i) => (
              <Reveal key={c.title} delay={i * 0.08}>
                <div className="flex h-full flex-col rounded-2xl bg-cream p-6 shadow-[var(--shadow-card)]">
                  <span className="flex h-11 w-11 items-center justify-center rounded-xl bg-bronze/12">
                    <Icon name={c.icon} className="h-5 w-5 text-bronze" />
                  </span>
                  <h3 className="mt-4 text-lg text-ocean">{c.title}</h3>
                  <p className="mt-2 text-sm leading-relaxed text-ocean/70">{c.text}</p>
                </div>
              </Reveal>
            ))}
          </div>
        </div>

        <Reveal delay={0.1}>
          <p className="mx-auto mt-12 max-w-3xl text-center text-xs leading-relaxed text-ocean/45">
            {payment.note}
          </p>
        </Reveal>
      </div>
    </section>
  );
}
