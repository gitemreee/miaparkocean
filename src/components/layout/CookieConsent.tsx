"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Cookie } from "lucide-react";

const STORAGE_KEY = "mpo-cookie-consent";

// Sol altta çerez onay kartı. Seçim localStorage'a yazılır, tekrar gösterilmez.
// WhatsApp butonu (sağ alt) ile çakışmaması için genişlik sınırlı ve sola yaslı.
export function CookieConsent() {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    try {
      if (!localStorage.getItem(STORAGE_KEY)) setVisible(true);
    } catch {
      // localStorage erişilemezse banner'ı göstermeyelim
    }
  }, []);

  function decide(choice: "accepted" | "rejected") {
    try {
      localStorage.setItem(STORAGE_KEY, choice);
    } catch {
      // sessizce geç
    }
    setVisible(false);
  }

  if (!visible) return null;

  return (
    <div
      role="dialog"
      aria-live="polite"
      aria-label="Çerez tercihi"
      className="fixed bottom-4 left-4 z-50 w-[min(22rem,calc(100vw-7rem))] rounded-2xl border border-ink/12 bg-white p-5 shadow-[0_24px_60px_-18px_rgba(0,0,0,0.35)]"
    >
      <div className="flex items-center gap-2.5">
        <span className="icon-tile h-9 w-9 items-center justify-center rounded-full">
          <Cookie className="h-5 w-5" />
        </span>
        <h2 className="text-[0.95rem] font-bold text-ink">Çerezleri kullanıyoruz</h2>
      </div>

      <p className="mt-3 text-[0.82rem] leading-relaxed text-ink/65">
        Siteyi düzgün çalıştırmak ve deneyiminizi iyileştirmek için çerezlerden yararlanıyoruz. Ayrıntılar için{" "}
        <Link href="/cerez-politikasi" className="font-medium text-accent underline underline-offset-2 hover:text-accent-600">
          Çerez Politikası
        </Link>
        {" "}ve{" "}
        <Link href="/kvkk" className="font-medium text-accent underline underline-offset-2 hover:text-accent-600">
          KVKK Aydınlatma Metni
        </Link>
        &apos;ni inceleyebilirsiniz.
      </p>

      <div className="mt-4 flex gap-2.5">
        <button
          type="button"
          onClick={() => decide("accepted")}
          className="flex-1 rounded-full bg-accent px-4 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-accent-600"
        >
          Kabul Et
        </button>
        <button
          type="button"
          onClick={() => decide("rejected")}
          className="rounded-full border border-ink/15 px-4 py-2.5 text-sm font-semibold text-ink/70 transition-colors hover:bg-paper-2"
        >
          Reddet
        </button>
      </div>
    </div>
  );
}
