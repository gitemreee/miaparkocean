"use client";

import { useEffect, useRef, useState } from "react";

// Gerçek logo dosyası varsa onu gösterir; yoksa (404) SVG fallback görünür.
// Görsel arka planda (gizli) yüklenir; başarıyla yüklenince SVG yerine geçer.
// Not: SSR'de img, React hidrasyonundan önce yüklenmiş olabilir (onLoad kaçar);
// bu yüzden mount'ta img.complete + naturalWidth kontrolü yapılır.
type Props = {
  src: string;
  alt: string;
  className?: string;
  children: React.ReactNode; // SVG fallback
};

export function LogoImage({ src, alt, className = "", children }: Props) {
  const [loaded, setLoaded] = useState(false);
  const ref = useRef<HTMLImageElement>(null);

  useEffect(() => {
    const img = ref.current;
    if (img && img.complete && img.naturalWidth > 0) {
      setLoaded(true);
    }
  }, []);

  return (
    <>
      {!loaded && children}
      <img
        ref={ref}
        src={src}
        alt={alt}
        aria-hidden={!loaded}
        className={loaded ? className : "hidden"}
        onLoad={() => setLoaded(true)}
      />
    </>
  );
}
