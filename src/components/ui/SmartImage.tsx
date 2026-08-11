import type { CSSProperties } from "react";

type SmartImageProps = {
  src: string; // /images/foo.webp
  alt: string;
  className?: string;
  sizes?: string;
  priority?: boolean;
  style?: CSSProperties;
};

// Statik export uyumlu görsel: -sm varyantıyla srcset üretir, CLS için object-cover kullanır.
export function SmartImage({ src, alt, className, sizes = "100vw", priority = false, style }: SmartImageProps) {
  // -sm varyantını üret; olası ?v= sürüm sorgusunu koru (immutable cache-bust ile uyumlu).
  const smSrc = src.replace(/\.webp(\?.*)?$/, "-sm.webp$1");
  return (
    <img
      src={src}
      srcSet={`${smSrc} 960w, ${src} 1920w`}
      sizes={sizes}
      alt={alt}
      loading={priority ? "eager" : "lazy"}
      fetchPriority={priority ? "high" : "auto"}
      decoding="async"
      className={className}
      style={style}
    />
  );
}
