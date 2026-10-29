"use client";

import { useEffect, useState } from "react";
import { MapPin } from "lucide-react";

export const CONSENT_KEY = "mpo-cookie-consent";
export const CONSENT_EVENT = "mpo-consent";

type Props = {
  src: string;
  title: string;
  className?: string;
  /** Harita yüklenmeden önce görünen görsel */
  fallbackImage?: string;
  /** Uydu vitrininde olduğu gibi etkileşimsiz gösterim */
  interactive?: boolean;
};

// Google Haritalar üçüncü taraf çerezi kullanır: yalnızca çerez onayı verildiyse ya da
// ziyaretçi "Haritayı göster" derse yüklenir. Öncesinde proje görseli yer tutar.
export function ConsentMap({ src, title, className = "", fallbackImage = "/images/aerial-pools.webp", interactive = true }: Props) {
  const [show, setShow] = useState(false);

  useEffect(() => {
    const check = () => {
      try {
        if (localStorage.getItem(CONSENT_KEY) === "accepted") setShow(true);
      } catch {
        /* erişilemezse yer tutucu kalır */
      }
    };
    check();
    window.addEventListener(CONSENT_EVENT, check);
    return () => window.removeEventListener(CONSENT_EVENT, check);
  }, []);

  return (
    <div className={`relative h-full w-full bg-cover bg-center ${className}`} style={{ backgroundImage: `url(${fallbackImage})` }}>
      {show ? (
        <iframe
          src={src}
          title={title}
          className={`absolute inset-0 h-full w-full ${interactive ? "" : "pointer-events-none"}`}
          loading="lazy"
          referrerPolicy="no-referrer-when-downgrade"
          allowFullScreen={interactive}
        />
      ) : (
        <div className={`absolute inset-0 flex justify-center bg-ink/25 ${interactive ? "items-center" : "items-end pb-3"}`}>
          <button
            type="button"
            onClick={() => setShow(true)}
            className="pointer-events-auto inline-flex items-center gap-2 rounded-full bg-white/95 px-5 py-2.5 text-sm font-semibold text-ink shadow-lg transition-colors hover:bg-white"
          >
            <MapPin className="h-4 w-4 text-accent" /> {interactive ? "Haritayı göster" : "Uydu haritasını göster"}
          </button>
        </div>
      )}
    </div>
  );
}
