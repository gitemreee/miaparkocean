import Link from "next/link";
import { Phone, Mail, MapPin, Globe, Instagram, Facebook, Youtube } from "lucide-react";
import { site, contact, socials, nav, secondaryNav } from "@/data/site";
import { YkbLogo } from "./YkbLogo";
import { WaveEdge } from "@/components/ui/Wave";

const socialIcons = { instagram: Instagram, facebook: Facebook, youtube: Youtube } as const;

export function Footer() {
  return (
    <footer className="section-dark">
      {/* Üstteki bölümden footer'a geçiş — logodaki dalganın kendisi.
          z-10: section-dark'ın radyal ışık katmanı dalganın üstünü
          soldurmasın. Ters çevrildiği için hem taban dolgusu hem eriyen
          bant görsel olarak yer değiştirir: dolgu yukarıda sayfaya,
          eriyen bant aşağıda koyu zemine bağlanır. */}
      <WaveEdge
        flip
        ribbonOpacity={0.85}
        fill="linear-gradient(180deg,#e9f6f9,#f1fafb 60%,#f1fafb)"
        haze="linear-gradient(180deg,rgba(91,171,195,0) 0%,rgba(75,161,190,0.3) 34%,rgba(46,133,168,0.62) 68%,rgba(24,110,146,0.85) 100%)"
        hazeHeight="h-[260%]"
        className="relative z-10 -mt-px h-[52px] md:h-[84px]"
      />

      {/* Su altı derinliği: yüzeyden süzülen ışık ve kabarcıklar. Işık
          fiziksel olarak yüzeye yakındır, o yüzden katman yalnızca üst
          bölgeyi kaplar ve aşağı doğru eriyerek biter — mobilde uzayan
          footer'da doku gerilip düzleşmez. */}
      <div
        className="underwater pointer-events-none absolute inset-x-0 top-0 h-[300px] opacity-25 md:h-[480px]"
        aria-hidden="true"
      />

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
            <p className="mt-6 max-w-sm text-sm leading-relaxed text-cream/85">
              İzmit MİA Bölgesi'nde 600 daireden oluşan modern yaşam projesi. Tasarrufa dayalı faizsiz finansman, 60 ay vade ve %0 faiz ile.
            </p>

            {/* Yapımcı ve satıcı yan yana: etiketler aynı hizada başlar,
                logolar eşit yükseklikte bir bantta ortalanır. Optik ağırlıkları
                denk olsun diye YKB (dar ve dikey) biraz daha büyük durur. */}
            <div className="mt-8 grid max-w-md grid-cols-2 gap-x-6 sm:gap-x-10">
              <div className="border-r border-cream/15 pr-6 sm:pr-10">
                <div className="eyebrow text-logo-light">Yapımcı</div>
                <a
                  href="https://ykbkoop.com"
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label="S.S. Yahya Kaptan Birlik Yapı Kooperatifi"
                  className="mt-4 flex h-14 items-center transition-opacity hover:opacity-80"
                >
                  <YkbLogo className="h-14 w-auto text-cream" />
                </a>
              </div>
              <div>
                <div className="eyebrow text-logo-light">{site.sellerRole}</div>
                <a
                  href="https://oceangayrimenkul41.com"
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label="Ocean Gayrimenkul"
                  className="mt-4 flex h-14 items-center transition-opacity hover:opacity-80"
                >
                  <img src="/ocean-logo-white.webp" alt="Ocean Gayrimenkul" className="h-9 w-auto" width={180} height={75} />
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
                  <Link href={item.href} className="font-display text-[0.98rem] text-cream/90 transition-colors hover:text-white">
                    {item.label}
                  </Link>
                </li>
              ))}
              {secondaryNav.map((item) => (
                <li key={item.href}>
                  <Link href={item.href} className="font-display text-[0.98rem] text-cream/90 transition-colors hover:text-white">
                    {item.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* İletişim */}
          <div>
            <div className="eyebrow text-logo-light">İletişim</div>
            <ul className="mt-5 space-y-4 text-sm text-cream/90">
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
        <div className="mt-6 flex flex-col items-center justify-between gap-3 text-xs text-cream/65 sm:flex-row">
          <span>© {new Date().getFullYear()} MİA PARK OCEAN · {site.developer}</span>
          <span>Tek Yetkili Satıcı: {site.seller}</span>
        </div>
      </div>
    </footer>
  );
}
