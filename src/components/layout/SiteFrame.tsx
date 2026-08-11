"use client";

import { usePathname } from "next/navigation";

// "Çıplak" rotalar: site header/footer/FAB gösterilmez (ör. basın açıklaması — QR ile paylaşılan bağımsız sayfa).
const BARE_PREFIXES = ["/basin-aciklamasi"];

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
      <main>{children}</main>
      {footer}
      {floating}
    </>
  );
}
