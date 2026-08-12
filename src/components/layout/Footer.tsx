import Link from "next/link";
import { Phone, Mail, MapPin, Globe, Instagram, Facebook, Youtube } from "lucide-react";
import { site, contact, socials, nav, secondaryNav } from "@/data/site";
import { YkbLogo } from "./YkbLogo";
import { WaveEdge } from "@/components/ui/Wave";

const socialIcons = { instagram: Instagram, facebook: Facebook, youtube: Youtube } as const;

export function Footer() {
  return (
    <footer className="section-dark">
      {/* Üstteki bölümden footer'a geçiş — logodaki dalganın kendisi */}
      <WaveEdge flip ribbon={false} className="-mt-px h-[42px] md:h-[58px]" />

      <div className="container-luxe relative z-10 py-16">
        <div className="grid gap-12 lg:grid-cols-[1.4fr_1fr_1fr]">
          {/* Marka + yapımcı */}
          <div>
            {/* Koyu mavi zeminde logo beyaz durur — şekli değişmez, boyası beyaz */}
            <Link href="/" aria-label="MİA PARK OCEAN ana sayfa" className="inline-block transition-transform duration-500 hover:scale-[1.02]">
              <img
                src="/brand/logo-ocean-white.webp"
                alt="MİA PARK OCEAN — İzmit MİA Bölgesi"
                width={210}
                height={144}
                className="h-auto w-[176px] md:w-[210px]"
              />
            </Link>
            <p className="mt-6 max-w-sm text-sm leading-relaxed text-cream/70">
              İzmit MİA Bölgesi'nde 600 daireden oluşan modern yaşam projesi. Tasarrufa dayalı faizsiz finansman, 60 ay vade ve %0 faiz ile.
            </p>

            <div className="mt-8 flex flex-wrap items-end gap-x-10 gap-y-6">
              <div>
                <div className="eyebrow text-logo-light">Yapımcı</div>
                <a href="https://ykbkoop.com" target="_blank" rel="noopener noreferrer" aria-label="S.S. Yahya Kaptan Birlik Yapı Kooperatifi" className="mt-3 inline-block transition-opacity hover:opacity-80">
                  <YkbLogo className="h-16 w-auto text-cream" />
                </a>
              </div>
              <div>
                <div className="eyebrow text-logo-light">{site.sellerRole}</div>
                <a href="https://oceangayrimenkul41.com" target="_blank" rel="noopener noreferrer" aria-label="Ocean Gayrimenkul" className="mt-3 inline-flex h-16 items-center transition-opacity hover:opacity-80">
                  <img src="/ocean-logo-white.webp" alt="Ocean Gayrimenkul" className="h-12 w-auto" width={180} height={75} />
                </a>
              </div>
            </div>
          </div>

          {/* Menü */}
          <div>
            <div className="eyebrow text-logo-light">Menü</div>
            <ul className="mt-5 space-y-3">
              {nav.map((item) => (
                <li key={item.href}>
                  <Link href={item.href} className="font-display text-[0.98rem] text-cream/80 transition-colors hover:text-white">
                    {item.label}
                  </Link>
                </li>
              ))}
              {secondaryNav.map((item) => (
                <li key={item.href}>
                  <Link href={item.href} className="font-display text-[0.98rem] text-cream/80 transition-colors hover:text-white">
                    {item.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* İletişim */}
          <div>
            <div className="eyebrow text-logo-light">İletişim</div>
            <ul className="mt-5 space-y-4 text-sm text-cream/80">
              {contact.phones.map((p) => (
                <li key={p.href}>
                  <a href={p.href} className="inline-flex items-center gap-3 hover:text-white">
                    <Phone className="h-4 w-4 text-logo-light" /> {p.label}
                  </a>
                </li>
              ))}
              <li>
                <a href={`mailto:${contact.email}`} className="inline-flex items-center gap-3 hover:text-white">
                  <Mail className="h-4 w-4 text-logo-light" /> {contact.email}
                </a>
              </li>
              <li>
                <a href={contact.websiteHref} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-3 hover:text-white">
                  <Globe className="h-4 w-4 text-logo-light" /> {contact.website}
                </a>
              </li>
              <li className="flex items-start gap-3">
                <MapPin className="mt-0.5 h-4 w-4 shrink-0 text-logo-light" />
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
                    className="flex h-9 w-9 items-center justify-center rounded-full border border-cream/20 text-cream/80 transition-colors hover:border-logo-light hover:text-logo-light"
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
