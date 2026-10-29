"use client";

import { useState, type FormEvent } from "react";
import Link from "next/link";
import { Check, FileText, Send } from "lucide-react";

type Errors = Partial<Record<"ad" | "telefon" | "email" | "kvkk", string>>;

const encode = (data: Record<string, string>) =>
  Object.keys(data).map((k) => encodeURIComponent(k) + "=" + encodeURIComponent(data[k])).join("&");

export function BelgeForm() {
  const [v, setV] = useState({ ad: "", telefon: "", email: "" });
  const [kvkk, setKvkk] = useState(false);
  const [errors, setErrors] = useState<Errors>({});
  const [sent, setSent] = useState(false);
  const [failed, setFailed] = useState(false);

  const set = (k: keyof typeof v) => (e: { target: { value: string } }) => setV((s) => ({ ...s, [k]: e.target.value }));

  const validate = () => {
    const n: Errors = {};
    if (v.ad.trim().length < 3) n.ad = "Lütfen ad ve soyadınızı girin.";
    if (v.telefon.replace(/\D/g, "").length < 10) n.telefon = "Geçerli bir telefon numarası girin.";
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.email)) n.email = "Geçerli bir e-posta girin.";
    if (!kvkk) n.kvkk = "Devam etmek için KVKK metnini onaylayın.";
    setErrors(n);
    return Object.keys(n).length === 0;
  };

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!validate()) return;
    let ok = false;
    try {
      const res = await fetch("/", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: encode({ "form-name": "belge-talep", ...v, kvkk: "onaylandı" }),
      });
      ok = res.ok;
    } catch {
      ok = false;
    }
    setFailed(!ok);
    setSent(true);
  };

  if (sent) {
    return (
      <div className="flex min-h-[380px] flex-col items-center justify-center rounded-3xl bg-paper-2 p-10 text-center">
        <span className="flex h-16 w-16 items-center justify-center rounded-full bg-accent-tint">
          <Check className="h-8 w-8 text-accent" strokeWidth={2} />
        </span>
        <h3 className="mt-6 text-2xl text-ink">{failed ? "Talebiniz iletilemedi" : "Talebiniz alındı"}</h3>
        <p className="mt-3 max-w-md text-ink/60">
          {failed ? (
            <>
              Bağlantı sorunu nedeniyle formu iletemedik. Lütfen{" "}
              <a href="tel:4441058" className="font-semibold text-ink underline">444 10 58</a> numarasını arayın.
            </>
          ) : (
            <>
              Teşekkürler {v.ad.split(" ")[0]}. Belge talebiniz bize ulaştı; hazır olan belgeleri ilettiğiniz iletişim bilgilerine
              <span className="font-semibold text-ink"> en kısa zamanda</span> göndereceğiz.
            </>
          )}
        </p>
      </div>
    );
  }

  return (
    <form name="belge-talep" method="POST" data-netlify="true" data-netlify-honeypot="bot-field" onSubmit={onSubmit} noValidate className="card-luxe p-5 md:p-9">
      <input type="hidden" name="form-name" value="belge-talep" />
      <p className="hidden"><label>Boş bırakın: <input name="bot-field" /></label></p>

      <div className="flex items-center gap-2 text-accent">
        <FileText className="h-5 w-5" />
        <span className="eyebrow">Belge Talep Formu</span>
      </div>
      <h3 className="mt-3 text-2xl text-ink">Belge talebi bırakın</h3>
      <p className="mt-2 text-sm text-ink/55">Hazırlanan belgeler yayımlandıkça ve üyeye özel belgeler için size dönüş yapalım.</p>

      <div className="mt-6 grid gap-4 sm:grid-cols-3">
        <Field label="Ad Soyad *" error={errors.ad}>
          <input name="ad" value={v.ad} onChange={set("ad")} className="form-input" placeholder="Adınız Soyadınız" autoComplete="name" />
        </Field>
        <Field label="Telefon *" error={errors.telefon}>
          <input name="telefon" value={v.telefon} onChange={set("telefon")} className="form-input" placeholder="05xx xxx xx xx" inputMode="tel" autoComplete="tel" />
        </Field>
        <Field label="E-posta *" error={errors.email}>
          <input name="email" value={v.email} onChange={set("email")} className="form-input" placeholder="ornek@eposta.com" inputMode="email" autoComplete="email" />
        </Field>
      </div>

      <label className="mt-5 flex items-start gap-3 text-sm text-ink/65">
        <input type="checkbox" checked={kvkk} onChange={(e) => setKvkk(e.target.checked)} className="mt-0.5 h-4 w-4 shrink-0 accent-[color:var(--color-accent)]" />
        <span><Link href="/kvkk" className="text-accent underline underline-offset-2">KVKK Aydınlatma Metni</Link>'ni okudum; kişisel verilerimin belge talebimin yanıtlanması amacıyla işlenmesine onay veriyorum. *</span>
      </label>
      {errors.kvkk && <p className="mt-1 text-xs text-[#c0392b]">{errors.kvkk}</p>}

      <button type="submit" className="mt-7 inline-flex w-full items-center justify-center gap-2 rounded-full bg-accent px-8 py-4 text-sm font-semibold text-white transition-colors hover:bg-accent-600 sm:w-auto sm:px-12">
        <Send className="h-4 w-4" /> Belge Talebi Gönder
      </button>
    </form>
  );
}

function Field({ label, error, children }: { label: string; error?: string; children: React.ReactNode }) {
  return (
    <label className="block">
      <span className="mb-1.5 block text-xs font-semibold uppercase tracking-wider text-ink/55">{label}</span>
      {children}
      {error && <span className="mt-1 block text-xs text-[#c0392b]">{error}</span>}
    </label>
  );
}
