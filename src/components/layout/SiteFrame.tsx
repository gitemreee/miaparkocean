"use client";

import { usePathname } from "next/navigation";
import { PageTransition } from "./PageTransition";

// "Çıplak" rotalar: site header/footer/FAB gösterilmez
// (basın açıklaması ve davetiye — QR ile paylaşılan bağımsız sayfalar).
const BARE_PREFIXES = ["/basin-aciklamasi", "/davetiye"];

type Props = {
  header: React.ReactNode;
  footer: React.ReactNode;
  floating: React.ReactNode;
  children: React.ReactNode;
};

export function SiteFrame({ header, footer, floating, children }: Props) {
  const pathname = usePathname() || "/";
  const bare = BARE_PREFIXES.some((p) => pathname === p || pathname.startsWith(`${p}/`));

  if (bare) return <>{children}</>;

  return (
    <>
      {header}
      <main>
        <PageTransition>{children}</PageTransition>
      </main>
      {footer}
      {floating}
    </>
  );
}
