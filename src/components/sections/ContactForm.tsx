"use client";

import { useState, type FormEvent } from "react";
import Link from "next/link";
import { Phone, Mail, MapPin, MessageCircle, Check, Navigation } from "lucide-react";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { Reveal } from "@/components/ui/Reveal";
import { contact } from "@/data/site";
import { units } from "@/data/units";
import { mapConfig } from "@/data/location";

type Errors = Partial<Record<"ad" | "telefon" | "email" | "kvkk", string>>;

const encode = (data: Record<string, string>) =>
  Object.keys(data)
    .map((k) => encodeURIComponent(k) + "=" + encodeURIComponent(data[k]))
    .join("&");

export function ContactForm() {
  const [values, setValues] = useState({ ad: "", telefon: "", email: "", tip: "", mesaj: "" });
  const [kvkk, setKvkk] = useState(false);
  const [errors, setErrors] = useState<Errors>({});
  const [sent, setSent] = useState(false);

  const set = (k: keyof typeof values) => (e: { target: { value: string } }) =>
    setValues((v) => ({ ...v, [k]: e.target.value }));

  const validate = (): boolean => {
    const next: Errors = {};
    if (values.ad.trim().length < 2) next.ad = "Lütfen adınızı girin.";
    if (values.telefon.replace(/\D/g, "").length < 10) next.telefon = "Geçerli bir telefon numarası girin.";
    if (values.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(values.email)) next.email = "Geçerli bir e-posta girin.";
    if (!kvkk) next.kvkk = "Devam etmek için KVKK metnini onaylayın.";
    setErrors(next);
    return Object.keys(next).length === 0;
  };

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!validate()) return;
    // Netlify Forms'a arka planda gönder (site Netlify'de ise yakalanır)
    try {
      await fetch("/", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: encode({ "form-name": "iletisim", ...values, kvkk: "onaylandı" }),
      });
    } catch {
      /* host Netlify değilse sessiz geç; WhatsApp yedeği devrede */
    }
    setSent(true);
  };

  const waMessage = `Merhaba, MİA PARK OCEAN ile ilgileniyorum.%0AAd: ${values.ad}%0ATelefon: ${values.telefon}${values.tip ? `%0ADaire Tipi: ${values.tip}` : ""}${values.mesaj ? `%0AMesaj: ${values.mesaj}` : ""}`;
  const waHref = `https://wa.me/905400280041?text=${waMessage}`;

  return (
    <section id="iletisim" className="surface-tint py-12 md:py-24">
      <div className="container-luxe">
        <SectionHeading
          tone="light"
          eyebrow="İletişim"
          title={<>Dairenizi <span className="gilded">birlikte seçelim</span></>}
          lead="Formu doldurun, satış ekibimiz en kısa sürede size ulaşsın. Dilerseniz hemen WhatsApp'tan da yazabilirsiniz."
        />

        <div className="mt-16 grid gap-10 lg:grid-cols-[1.1fr_0.9fr]">
          {/* Form */}
          <Reveal>
            <div className="rounded-[2rem] bg-cream p-8 md:p-10">
              {sent ? (
                <div className="flex min-h-[420px] flex-col items-center justify-center text-center">
                  <span className="flex h-16 w-16 items-center justify-center rounded-full bg-bronze/15">
                    <Check className="h-8 w-8 text-bronze" strokeWidth={2} />
                  </span>
                  <h3 className="mt-6 text-2xl text-ocean">Talebiniz alındı</h3>
                  <p className="mt-3 max-w-sm text-sm leading-relaxed text-ocean/70">
                    Teşekkürler {values.ad.split(" ")[0]}. Satış ekibimiz en kısa sürede sizinle iletişime geçecek.
                    Daha hızlı yanıt için WhatsApp'tan da yazabilirsiniz.
                  </p>
                  <a
                    href={waHref}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="mt-7 inline-flex items-center gap-2 rounded-full bg-[#25D366] px-7 py-3.5 text-sm font-medium text-white"
                  >
                    <MessageCircle className="h-4 w-4" /> WhatsApp'tan Gönder
                  </a>
                </div>
              ) : (
                <form
                  name="iletisim"
                  method="POST"
                  data-netlify="true"
                  data-netlify-honeypot="bot-field"
                  onSubmit={onSubmit}
                  noValidate
                >
                  <input type="hidden" name="form-name" value="iletisim" />
                  <p className="hidden">
                    <label>Boş bırakın: <input name="bot-field" /></label>
                  </p>

                  <div className="grid gap-5 sm:grid-cols-2">
                    <Field label="Ad Soyad *" error={errors.ad}>
                      <input
                        name="ad"
                        value={values.ad}
                        onChange={set("ad")}
                        className="form-input"
                        placeholder="Adınız Soyadınız"
                        autoComplete="name"
                      />
                    </Field>
                    <Field label="Telefon *" error={errors.telefon}>
                      <input
                        name="telefon"
                        value={values.telefon}
                        onChange={set("telefon")}
                        className="form-input"
                        placeholder="05xx xxx xx xx"
                        inputMode="tel"
                        autoComplete="tel"
                      />
                    </Field>
                    <Field label="E-posta" error={errors.email}>
                      <input
                        name="email"
                        value={values.email}
                        onChange={set("email")}
                        className="form-input"
                        placeholder="ornek@eposta.com"
                        inputMode="email"
                        autoComplete="email"
                      />
                    </Field>
                    <Field label="İlgilendiğiniz Daire Tipi">
                      <select name="tip" value={values.tip} onChange={set("tip")} className="form-input">
                        <option value="">Seçiniz</option>
                        {units.map((u) => (
                          <option key={u.slug} value={`${u.type} (${u.area})`}>
                            {u.type} — {u.name} ({u.area})
                          </option>
                        ))}
                      </select>
                    </Field>
                  </div>

                  <div className="mt-5">
                    <Field label="Mesajınız">
                      <textarea
                        name="mesaj"
                        value={values.mesaj}
                        onChange={set("mesaj")}
                        rows={4}
                        className="form-input resize-none"
                        placeholder="Sormak istedikleriniz…"
                      />
                    </Field>
                  </div>

                  <label className="mt-5 flex items-start gap-3 text-sm text-ocean/70">
                    <input
                      type="checkbox"
                      checked={kvkk}
                      onChange={(e) => setKvkk(e.target.checked)}
                      className="mt-0.5 h-4 w-4 shrink-0 accent-[color:var(--color-bronze)]"
                    />
                    <span>
                      <Link href="/kvkk" className="text-bronze underline underline-offset-2">KVKK Aydınlatma Metni</Link>'ni
                      okudum; kişisel verilerimin işlenmesine onay veriyorum. *
                    </span>
                  </label>
                  {errors.kvkk && <p className="mt-1 text-xs text-driftwood">{errors.kvkk}</p>}

                  <button
                    type="submit"
                    className="mt-7 w-full rounded-full bg-bronze px-8 py-4 text-sm font-medium tracking-wide text-cream transition-colors hover:bg-bronze-300 sm:w-auto sm:px-12"
                  >
                    Gönder
                  </button>
                </form>
              )}
            </div>
          </Reveal>

          {/* İletişim bilgileri */}
          <Reveal delay={0.1}>
            <div className="flex h-full flex-col gap-6">
              <a href={contact.whatsapp.href} target="_blank" rel="noopener noreferrer" className="flex items-center gap-4 rounded-2xl bg-[#25D366]/10 p-6 transition-colors hover:bg-[#25D366]/20">
                <span className="flex h-12 w-12 items-center justify-center rounded-xl bg-[#25D366]">
                  <MessageCircle className="h-6 w-6 text-white" />
                </span>
                <div>
                  <div className="text-base font-semibold text-ink">{contact.whatsapp.label}</div>
                  <div className="text-sm text-ink/55">Hızlı yanıt için</div>
                </div>
              </a>

              <div className="card-luxe p-5 md:p-6">
                <ul className="space-y-5 text-sm">
                  {contact.phones.map((p) => (
                    <li key={p.href}>
                      <a href={p.href} className="flex items-center gap-3 text-ink/80 hover:text-accent">
                        <Phone className="h-5 w-5 text-accent" /> {p.label}
                      </a>
                    </li>
                  ))}
                  <li>
                    <a href={`mailto:${contact.email}`} className="flex items-center gap-3 text-ink/80 hover:text-accent">
                      <Mail className="h-5 w-5 text-accent" /> {contact.email}
                    </a>
                  </li>
                  <li className="flex items-start gap-3 text-ink/80">
                    <MapPin className="mt-0.5 h-5 w-5 shrink-0 text-accent" />
                    <span className="leading-relaxed">{contact.address.lines.join(" ")}</span>
                  </li>
                </ul>
                <a
                  href={mapConfig.googleDirections}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="mt-6 inline-flex items-center gap-2 rounded-full border border-ink/20 px-5 py-2.5 text-sm font-semibold text-ink transition-colors hover:bg-accent hover:border-accent hover:text-white"
                >
                  <Navigation className="h-4 w-4" /> Satış Ofisine Yol Tarifi
                </a>
              </div>
            </div>
          </Reveal>
        </div>
      </div>
    </section>
  );
}

function Field({ label, error, children }: { label: string; error?: string; children: React.ReactNode }) {
  return (
    <label className="block">
      <span className="mb-1.5 block text-xs font-medium uppercase tracking-wider text-ocean/55">{label}</span>
      {children}
      {error && <span className="mt-1 block text-xs text-driftwood">{error}</span>}
    </label>
  );
}
