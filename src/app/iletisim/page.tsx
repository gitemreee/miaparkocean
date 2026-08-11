import type { Metadata } from "next";
import { PageHero } from "@/components/layout/PageHero";
import { ContactForm } from "@/components/sections/ContactForm";

export const metadata: Metadata = {
  title: "İletişim",
  description:
    "MİA PARK OCEAN satış ofisi ile iletişime geçin. Telefon, WhatsApp, e-posta ve İzmit / Kocaeli adres bilgileri. Dairenizi birlikte seçelim.",
};

export default function IletisimPage() {
  return (
    <>
      <PageHero
        eyebrow="İletişim"
        title={<>Sizi <span className="gilded">arayalım</span></>}
        lead="Formu doldurun ya da doğrudan telefon veya WhatsApp'tan yazın. Satış ekibimiz size en uygun daireyi ve ödeme planını çıkarsın."
        image="/images/terrace-pergola.webp"
      />
      <ContactForm />
    </>
  );
}
