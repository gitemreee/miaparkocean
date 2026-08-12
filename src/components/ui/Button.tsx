import Link from "next/link";
import type { ReactNode } from "react";

type Variant = "solid" | "ocean" | "outline" | "ghost";

type ButtonLinkProps = {
  href: string;
  children: ReactNode;
  variant?: Variant;
  className?: string;
  external?: boolean;
};

const base = "btn-base px-7 py-3.5 text-sm tracking-wide";

const variants: Record<Variant, string> = {
  /** Yeşil ana eylem */
  solid: "btn-jade btn-shine",
  /** Safir ikincil eylem */
  ocean: "btn-ocean btn-shine",
  /** Açık zeminde dış hatlı */
  outline: "btn-outline",
  /** Koyu zeminde dış hatlı */
  ghost: "btn-outline-light",
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
