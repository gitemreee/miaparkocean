import Link from "next/link";
import { Phone, Mail, MapPin, Globe, Instagram, Facebook, Youtube } from "lucide-react";
import { site, contact, socials, nav, secondaryNav } from "@/data/site";
import { YkbLogo } from "./YkbLogo";

const socialIcons = { instagram: Instagram, facebook: Facebook, youtube: Youtube } as const;

export function Footer() {
  return (
    <footer className="section-dark">
      {/* Üstteki bölümden footer'a dalga geçişi */}
      <div className="wave-divider -mt-px rotate-180" aria-hidden="true">
        <svg viewBox="0 0 1440 90" preserveAspectRatio="none" className="h-[52px] w-full">
          <path
            d="M0 60 C 240 10, 480 96, 720 56 C 960 16, 1200 84, 1440 42 L1440 90 L0 90 Z"
            fill="currentColor"
            className="text-paper"
          />
        </svg>
      </div>

      <div className="container-luxe relative z-10 py-16">
        <div className="grid gap-12 lg:grid-cols-[1.4fr_1fr_1fr]">
          {/* Marka + yapımcı */}
          <div>
            {/* Logo daima beyaz zeminde: koyu footer'da beyaz plaket içinde durur */}
            <Link href="/" aria-label="MİA PARK OCEAN ana sayfa" className="inline-block rounded-2xl bg-white p-5 shadow-[0_20px_50px_-26px_rgba(0,9,38,0.8)] transition-transform duration-500 hover:scale-[1.02]">
              <img
                src="/brand/logo-ocean-trim.webp"
                alt="MİA PARK OCEAN — İzmit MİA Bölgesi"
                width={196}
                height={134}
                className="h-auto w-[196px]"
              />
            </Link>
            <p className="mt-6 max-w-sm text-sm leading-relaxed text-cream/70">
              İzmit MİA Bölgesi'nde 600 daireden oluşan modern yaşam projesi. Tasarrufa dayalı faizsiz finansman, 60 ay vade ve %0 faiz ile.
            </p>

            <div className="mt-8 flex flex-wrap items-end gap-x-10 gap-y-6">
              <div>
                <div className="eyebrow text-accent-300">Yapımcı</div>
                <a href="https://ykbkoop.com" target="_blank" rel="noopener noreferrer" aria-label="S.S. Yahya Kaptan Birlik Yapı Kooperatifi" className="mt-3 inline-block transition-opacity hover:opacity-80">
                  <YkbLogo className="h-16 w-auto text-cream" />
                </a>
              </div>
              <div>
                <div className="eyebrow text-accent-300">{site.sellerRole}</div>
                <a href="https://oceangayrimenkul41.com" target="_blank" rel="noopener noreferrer" aria-label="Ocean Gayrimenkul" className="mt-3 inline-flex h-[4.2rem] items-center rounded-xl bg-white px-6 transition-opacity hover:opacity-90">
                  <img src="/ocean-logo.webp" alt="Ocean Gayrimenkul" className="h-9 w-auto" width={180} height={40} />
                </a>
              </div>
            </div>
          </div>

          {/* Menü */}
          <div>
            <div className="eyebrow text-bronze-300">Menü</div>
            <ul className="mt-5 space-y-3">
              {nav.map((item) => (
                <li key={item.href}>
                  <Link href={item.href} className="text-sm text-cream/75 transition-colors hover:text-bronze-100">
                    {item.label}
                  </Link>
                </li>
              ))}
              {secondaryNav.map((item) => (
                <li key={item.href}>
                  <Link href={item.href} className="text-sm text-cream/75 transition-colors hover:text-bronze-100">
                    {item.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* İletişim */}
          <div>
            <div className="eyebrow text-bronze-300">İletişim</div>
            <ul className="mt-5 space-y-4 text-sm text-cream/80">
              {contact.phones.map((p) => (
                <li key={p.href}>
                  <a href={p.href} className="inline-flex items-center gap-3 hover:text-bronze-100">
                    <Phone className="h-4 w-4 text-bronze" /> {p.label}
                  </a>
                </li>
              ))}
              <li>
                <a href={`mailto:${contact.email}`} className="inline-flex items-center gap-3 hover:text-bronze-100">
                  <Mail className="h-4 w-4 text-bronze" /> {contact.email}
                </a>
              </li>
              <li>
                <a href={contact.websiteHref} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-3 hover:text-bronze-100">
                  <Globe className="h-4 w-4 text-bronze" /> {contact.website}
                </a>
              </li>
              <li className="flex items-start gap-3">
                <MapPin className="mt-0.5 h-4 w-4 shrink-0 text-bronze" />
                <span className="leading-relaxed">{contact.address.lines.join(" ")}</span>
              </li>
            </ul>

            <div className="mt-6 flex items-center gap-3">
              {socials.map((s) => {
                const Icon = socialIcons[s.icon as keyof typeof socialIcons];
                return (
                  <a
                    key={s.name}
                    href={s.href}
                    target="_blank"
                    rel="noopener noreferrer"
                    aria-label={s.name}
                    className="flex h-9 w-9 items-center justify-center rounded-full border border-cream/20 text-cream/80 transition-colors hover:border-bronze hover:text-bronze"
                  >
                    <Icon className="h-4 w-4" />
                  </a>
                );
              })}
            </div>
          </div>
        </div>

        <div className="gold-rule mt-14" />
        <div className="mt-6 flex flex-col items-center justify-between gap-3 text-xs text-cream/50 sm:flex-row">
          <span>© {new Date().getFullYear()} MİA PARK OCEAN · {site.developer}</span>
          <span>Tek Yetkili Satıcı: {site.seller}</span>
        </div>
      </div>
    </footer>
  );
}
