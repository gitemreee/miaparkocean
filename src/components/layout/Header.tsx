"use client";

import Link from "next/link";
import { useEffect, useRef, useState } from "react";
import { Menu, X, Phone, ChevronDown, ArrowRight } from "lucide-react";
import { AnimatePresence, motion } from "framer-motion";
import { Logo } from "./Logo";
import { nav, contact } from "@/data/site";
import { units } from "@/data/units";

// Açılır alt menüler — parent href'e göre eşlenir. Alt menüsü olmayan öğe
// (Belgeler, İletişim) düz link kalır. Anchor'lar ilgili sayfadaki gerçek
// section id'lerine bağlıdır.
type SubItem = { label: string; href: string; hint?: string; footer?: boolean };

const daireSub: SubItem[] = [
  ...units.map((u) => ({ label: u.name, href: `/daireler#${u.slug}`, hint: u.area })),
  { label: "Tüm Daireler", href: "/daireler", footer: true },
];

const submenus: Record<string, SubItem[]> = {
  "/daireler": daireSub,
  "/kooperatif": [
    { label: "Neden Kooperatif", href: "/kooperatif#neden-kooperatif" },
    { label: "Yasal Güvence", href: "/kooperatif#guvence" },
    { label: "Güven ve Denetim Sistemi", href: "/kooperatif#guvence-sistemi" },
    { label: "Kooperatif Kurumu", href: "/kooperatif#kooperatif-hakkinda" },
  ],
  "/bilgi-merkezi": [
    { label: "Kooperatif Modeli", href: "/bilgi-merkezi#model" },
    { label: "Üyelik ve Üye Hakları", href: "/bilgi-merkezi#uyelik" },
    { label: "Güven ve Denetim", href: "/bilgi-merkezi#guven" },
    { label: "Finansman ve Maliyet", href: "/bilgi-merkezi#finansman" },
    { label: "Arsa, Ruhsat ve İnşaat", href: "/bilgi-merkezi#insaat" },
    { label: "Vergi ve Hukuki Bilgilendirme", href: "/bilgi-merkezi#vergi" },
    { label: "Tüm Bilgi Merkezi", href: "/bilgi-merkezi", footer: true },
  ],
  "/bolge": [
    { label: "Bölge", href: "/bolge#bolge" },
    { label: "Konum", href: "/bolge#lokasyon" },
    { label: "Değerleme", href: "/bolge#degerleme" },
    { label: "Demografi", href: "/bolge#demografi" },
  ],
};

// Masaüstü nav öğesi — alt menü varsa hover-intent + focus ile açılan flyout.
function DesktopNavItem({ label, href, submenu }: { label: string; href: string; submenu?: SubItem[] }) {
  const [open, setOpen] = useState(false);
  const closeTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const suppressOpen = useRef(false);
  const triggerRef = useRef<HTMLAnchorElement>(null);

  const clearTimer = () => {
    if (closeTimer.current) {
      clearTimeout(closeTimer.current);
      closeTimer.current = null;
    }
  };
  const openNow = () => {
    if (suppressOpen.current) return;
    clearTimer();
    setOpen(true);
  };
  // Hover-intent: fare tetikleyiciden panele geçerken kapanmasın diye ~120ms gecikme.
  const closeSoon = () => {
    clearTimer();
    closeTimer.current = setTimeout(() => setOpen(false), 120);
  };

  useEffect(() => () => clearTimer(), []);

  if (!submenu) {
    return (
      <Link href={href} className="text-sm font-medium tracking-wide text-ink/70 transition-colors hover:text-ink">
        {label}
      </Link>
    );
  }

  return (
    <div
      className="relative"
      onMouseEnter={openNow}
      onMouseLeave={closeSoon}
      onFocus={openNow}
      onBlur={(e) => {
        if (!e.currentTarget.contains(e.relatedTarget as Node | null)) closeSoon();
      }}
      onKeyDown={(e) => {
        if (e.key === "Escape" && open) {
          e.stopPropagation();
          setOpen(false);
          suppressOpen.current = true;
          triggerRef.current?.focus();
          // Odak tetikleyiciye dönerken onFocus'un paneli yeniden açmasını engelle.
          setTimeout(() => {
            suppressOpen.current = false;
          }, 0);
        }
      }}
    >
      <Link
        ref={triggerRef}
        href={href}
        aria-haspopup="menu"
        aria-expanded={open}
        className={`inline-flex items-center gap-1 text-sm font-medium tracking-wide transition-colors ${open ? "text-ink" : "text-ink/70 hover:text-ink"}`}
      >
        {label}
        <ChevronDown className={`h-3.5 w-3.5 transition-transform duration-200 ${open ? "rotate-180" : ""}`} aria-hidden="true" />
      </Link>

      {/* pt-3: tetikleyici ile panel arasında kesintisiz hover köprüsü (ölü bölge yok). */}
      <div className="absolute left-1/2 top-full z-50 -translate-x-1/2 pt-3">
        <AnimatePresence>
          {open && (
            <motion.div
              role="menu"
              aria-label={label}
              initial={{ opacity: 0, y: -6, scale: 0.98 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -6, scale: 0.98 }}
              transition={{ duration: 0.16, ease: [0.22, 1, 0.36, 1] }}
              style={{ transformOrigin: "top center" }}
              className="min-w-[248px] rounded-2xl border border-ink/10 bg-paper p-2 shadow-[var(--shadow-luxe)]"
            >
              {submenu.map((sub) =>
                sub.footer ? (
                  <Link
                    key={sub.href}
                    href={sub.href}
                    role="menuitem"
                    onClick={() => setOpen(false)}
                    className="mt-1 flex items-center justify-between gap-6 whitespace-nowrap rounded-xl border-t border-ink/10 px-3.5 pb-2.5 pt-3 text-sm font-semibold text-accent transition-colors hover:bg-accent-tint"
                  >
                    <span>{sub.label}</span>
                    <ArrowRight className="h-4 w-4" aria-hidden="true" />
                  </Link>
                ) : (
                  <Link
                    key={sub.href}
                    href={sub.href}
                    role="menuitem"
                    onClick={() => setOpen(false)}
                    className="flex items-center justify-between gap-6 whitespace-nowrap rounded-xl px-3.5 py-2.5 text-sm font-medium text-ink/75 transition-colors hover:bg-accent-tint hover:text-accent"
                  >
                    <span>{sub.label}</span>
                    {sub.hint && <span className="text-xs font-normal text-ink/40">{sub.hint}</span>}
                  </Link>
                )
              )}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}

export function Header() {
  const [scrolled, setScrolled] = useState(false);
  const [open, setOpen] = useState(false);
  const [mobileSub, setMobileSub] = useState<string | null>(null);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 40);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => {
    document.body.style.overflow = open ? "hidden" : "";
    return () => { document.body.style.overflow = ""; };
  }, [open]);

  // Mobil menü kapanınca açık akordeonu sıfırla.
  useEffect(() => {
    if (!open) setMobileSub(null);
  }, [open]);

  const solid = scrolled || open;

  return (
    <header className={`fixed inset-x-0 top-0 z-50 transition-colors duration-300 ${solid ? "border-b border-ink/10 bg-paper/95 backdrop-blur" : "bg-transparent"}`}>
      <div className="container-luxe flex items-center justify-between py-4">
        <Logo tone="dark" />

        <nav className="hidden items-center gap-7 lg:flex">
          {nav.map((item) => (
            <DesktopNavItem key={item.href} label={item.label} href={item.href} submenu={submenus[item.href]} />
          ))}
        </nav>

        <div className="hidden items-center gap-5 lg:flex">
          <a href={contact.phones[0].href} className="inline-flex items-center gap-1.5 text-sm font-semibold text-ink/80 transition-colors hover:text-accent">
            <Phone className="h-4 w-4 text-accent" /> {contact.phones[0].label}
          </a>
          <Link href="/iletisim" className="inline-flex items-center rounded-full bg-accent px-6 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-accent-600">
            Dairenizi Seçin
          </Link>
        </div>

        <button type="button" onClick={() => setOpen((v) => !v)} className="text-ink lg:hidden" aria-label={open ? "Menüyü kapat" : "Menüyü aç"} aria-expanded={open}>
          {open ? <X className="h-7 w-7" /> : <Menu className="h-7 w-7" />}
        </button>
      </div>

      <div className={`lg:hidden ${open ? "pointer-events-auto" : "pointer-events-none"}`} aria-hidden={!open}>
        <div className={`border-t border-ink/10 bg-paper transition-[max-height,opacity] duration-500 ${open ? "max-h-[85vh] overflow-y-auto opacity-100" : "max-h-0 overflow-hidden opacity-0"}`}>
          <nav className="container-luxe flex flex-col py-4">
            {nav.map((item) => {
              const submenu = submenus[item.href];
              if (!submenu) {
                return (
                  <Link key={item.href} href={item.href} onClick={() => setOpen(false)} className="border-b border-ink/8 py-3.5 text-lg font-medium tracking-tight text-ink">
                    {item.label}
                  </Link>
                );
              }
              const isOpen = mobileSub === item.href;
              return (
                <div key={item.href} className="border-b border-ink/8">
                  <button
                    type="button"
                    onClick={() => setMobileSub(isOpen ? null : item.href)}
                    aria-expanded={isOpen}
                    className="flex w-full items-center justify-between py-3.5 text-lg font-medium tracking-tight text-ink"
                  >
                    {item.label}
                    <ChevronDown className={`h-5 w-5 text-ink/60 transition-transform duration-300 ${isOpen ? "rotate-180" : ""}`} aria-hidden="true" />
                  </button>
                  <AnimatePresence initial={false}>
                    {isOpen && (
                      <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: "auto", opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        transition={{ duration: 0.3, ease: [0.22, 1, 0.36, 1] }}
                        className="overflow-hidden"
                      >
                        <div className="flex flex-col pb-2">
                          {submenu.map((sub) => (
                            <Link
                              key={sub.href}
                              href={sub.href}
                              onClick={() => setOpen(false)}
                              className={`flex items-center justify-between gap-4 py-2.5 pl-4 text-base ${sub.footer ? "font-semibold text-accent" : "text-ink/70"}`}
                            >
                              <span>{sub.label}</span>
                              {sub.hint ? <span className="text-xs text-ink/40">{sub.hint}</span> : sub.footer ? <ArrowRight className="h-4 w-4" aria-hidden="true" /> : null}
                            </Link>
                          ))}
                        </div>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>
              );
            })}
            <div className="mt-4 flex flex-col gap-3">
              <a href={contact.whatsapp.href} target="_blank" rel="noopener noreferrer" className="inline-flex items-center justify-center gap-2 rounded-full border border-ink/25 px-5 py-3 text-sm font-medium text-ink">
                {contact.whatsapp.label}
              </a>
              <Link href="/iletisim" onClick={() => setOpen(false)} className="inline-flex items-center justify-center rounded-full bg-accent px-5 py-3 text-sm font-semibold text-white">
                Dairenizi Seçin
              </Link>
            </div>
          </nav>
        </div>
      </div>
    </header>
  );
}
