"use client";

import { useState } from "react";
import { Plus } from "lucide-react";
import { AnimatePresence, motion } from "framer-motion";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { faq, type FaqItem } from "@/data/faq";

type FaqProps = {
  items?: FaqItem[];
  eyebrow?: string;
  title?: React.ReactNode;
  lead?: string;
};

export function Faq({
  items = faq,
  eyebrow = "Aklınızdaki Sorular",
  title,
  lead = "Kooperatif modeli, güvence ve proje hakkında en çok merak edilenleri topladık.",
}: FaqProps) {
  const [open, setOpen] = useState<number | null>(0);

  return (
    <section id="sss" className="surface-tint py-24 md:py-32">
      <div className="container-luxe">
        <SectionHeading
          eyebrow={eyebrow}
          title={title ?? <>Sıkça sorulan <span className="gilded">sorular</span></>}
          lead={lead}
        />

        <div className="mx-auto mt-14 max-w-3xl divide-y divide-ocean/10 border-y border-ocean/10">
          {items.map((item, i) => {
            const isOpen = open === i;
            return (
              <div key={item.question}>
                <h3>
                  <button
                    type="button"
                    onClick={() => setOpen(isOpen ? null : i)}
                    className="flex w-full items-center justify-between gap-4 py-6 text-left"
                    aria-expanded={isOpen}
                  >
                    <span className={`text-lg transition-colors ${isOpen ? "text-bronze" : "text-ocean"}`}>
                      {item.question}
                    </span>
                    <span className={`grid h-8 w-8 shrink-0 place-items-center rounded-full border transition-all duration-300 ${isOpen ? "rotate-45 border-bronze bg-bronze text-cream" : "border-ocean/20 text-ocean"}`}>
                      <Plus className="h-4 w-4" />
                    </span>
                  </button>
                </h3>
                <AnimatePresence initial={false}>
                  {isOpen && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: "auto", opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: 0.35, ease: [0.22, 1, 0.36, 1] }}
                      className="overflow-hidden"
                    >
                      <p className="pb-6 pr-12 text-base leading-relaxed text-ocean/70">{item.answer}</p>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
