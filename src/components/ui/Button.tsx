import Link from "next/link";
import type { ReactNode } from "react";

type Variant = "solid" | "outline" | "ghost";

type ButtonLinkProps = {
  href: string;
  children: ReactNode;
  variant?: Variant;
  className?: string;
  external?: boolean;
};

const base =
  "inline-flex items-center justify-center gap-2 rounded-full px-7 py-3.5 text-sm font-semibold tracking-wide transition-colors duration-300";

const variants: Record<Variant, string> = {
  solid: "bg-accent text-white hover:bg-accent-600",
  outline: "border border-ink/20 text-ink hover:border-ink hover:bg-ink hover:text-white",
  ghost: "border border-white/40 text-white hover:bg-white hover:text-ink",
};

export function ButtonLink({ href, children, variant = "solid", className = "", external = false }: ButtonLinkProps) {
  const cls = `${base} ${variants[variant]} ${className}`;
  if (external) {
    return (
      <a href={href} target="_blank" rel="noopener noreferrer" className={cls}>
        {children}
      </a>
    );
  }
  return (
    <Link href={href} className={cls}>
      {children}
    </Link>
  );
}
