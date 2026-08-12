"use client";

import { useMemo, useState } from "react";
import { Check, Send, Users } from "lucide-react";
import { launchEvent } from "@/data/event";

/**
 * Katılım bildirimi (RSVP).
 *
 * Site statik export olduğu için sunucu tarafı yoktur: form doldurulduğunda
 * ön-doldurulmuş bir WhatsApp mesajı hazırlanıp etkinlik sorumlusuna yönlendirilir.
 */
export function RsvpForm() {
  const [form, setForm] = useState({ name: "", org: "", phone: "", guests: "1", note: "" });
  const [touched, setTouched] = useState(false);

  const valid = form.name.trim().length > 2 && form.phone.trim().length >= 10;

  const waHref = useMemo(() => {
    const lines = [
      `${launchEvent.project} — ${launchEvent.name}`,
      "Katılım bildirimi",
      "",
      `Ad Soyad: ${form.name.trim()}`,
      form.org.trim() ? `Kurum: ${form.org.trim()}` : null,
      `Telefon: ${form.phone.trim()}`,
      `Kişi sayısı: ${form.guests}`,
      form.note.trim() ? `Not: ${form.note.trim()}` : null,
      "",
      `${launchEvent.dateLabel} ${launchEvent.dayLabel} · ${launchEvent.timeLabel} · ${launchEvent.venue}, ${launchEvent.city}`,
    ].filter(Boolean);
    return `https://wa.me/${launchEvent.host.wa}?text=${encodeURIComponent(lines.join("\n"))}`;
  }, [form]);

  const set = (k: keyof typeof form) => (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) =>
    setForm((f) => ({ ...f, [k]: e.target.value }));

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        setTouched(true);
        if (valid) window.open(waHref, "_blank", "noopener,noreferrer");
      }}
      className="card-gradient-border p-6 shadow-[var(--shadow-card)] sm:p-8"
      noValidate
    >
      <div className="flex items-center gap-3">
        <span className="icon-tile h-11 w-11 items-center justify-center rounded-xl">
          <Users className="h-5 w-5" />
        </span>
        <div>
          <h2 className="font-display text-2xl leading-tight text-ink">Katılım Bildirimi</h2>
          <p className="text-sm text-ink/55">Formu doldurun, WhatsApp üzerinden bize ulaşsın.</p>
        </div>
      </div>

      <div className="mt-7 grid gap-4 sm:grid-cols-2">
        <div className="sm:col-span-2">
          <label className="form-label" htmlFor="rsvp-name">
            Ad Soyad <span className="text-accent">*</span>
          </label>
          <input
            id="rsvp-name"
            className="form-input"
            value={form.name}
            onChange={set("name")}
            placeholder="Adınız ve soyadınız"
            autoComplete="name"
            required
          />
          {touched && form.name.trim().length <= 2 && (
            <p className="mt-1.5 text-xs font-medium text-accent-600">Lütfen adınızı yazın.</p>
          )}
        </div>

        <div>
          <label className="form-label" htmlFor="rsvp-org">
            Kurum / Yayın
          </label>
          <input
            id="rsvp-org"
            className="form-input"
            value={form.org}
            onChange={set("org")}
            placeholder="Gazete, ajans, kurum"
            autoComplete="organization"
          />
        </div>

        <div>
          <label className="form-label" htmlFor="rsvp-phone">
            Telefon <span className="text-accent">*</span>
          </label>
          <input
            id="rsvp-phone"
            className="form-input"
            value={form.phone}
            onChange={set("phone")}
            placeholder="05XX XXX XX XX"
            inputMode="tel"
            autoComplete="tel"
            required
          />
          {touched && form.phone.trim().length < 10 && (
            <p className="mt-1.5 text-xs font-medium text-accent-600">Geçerli bir telefon numarası girin.</p>
          )}
        </div>

        <div>
          <label className="form-label" htmlFor="rsvp-guests">
            Kişi Sayısı
          </label>
          <select id="rsvp-guests" className="form-input" value={form.guests} onChange={set("guests")}>
            {["1", "2", "3", "4", "5+"].map((n) => (
              <option key={n} value={n}>
                {n} kişi
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="form-label" htmlFor="rsvp-note">
            Not
          </label>
          <input
            id="rsvp-note"
            className="form-input"
            value={form.note}
            onChange={set("note")}
            placeholder="İsteğe bağlı"
          />
        </div>
      </div>

      <button type="submit" className="btn-base btn-jade btn-shine mt-7 w-full px-8 py-4 text-sm">
        <Send className="h-4 w-4" /> Katılımımı Bildir
      </button>

      <p className="mt-4 flex items-start gap-2 text-xs leading-relaxed text-ink/50">
        <Check className="mt-0.5 h-3.5 w-3.5 shrink-0 text-accent" />
        Bilgileriniz yalnızca etkinlik katılım kaydı için kullanılır, üçüncü kişilerle paylaşılmaz.
      </p>
    </form>
  );
}
