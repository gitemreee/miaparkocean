import { Reveal } from "@/components/ui/Reveal";
import { SmartImage } from "@/components/ui/SmartImage";
import { ButtonLink } from "@/components/ui/Button";
import { Icon } from "@/components/ui/Icon";
import { highlights } from "@/data/project";

export function Intro() {
  return (
    <section className="bg-cream py-24 md:py-32">
      <div className="container-luxe grid items-center gap-14 lg:grid-cols-[1.3fr_1fr]">
        {/* Görsel — büyük */}
        <Reveal className="order-2 lg:order-1">
          <div className="relative">
            <div className="overflow-hidden rounded-[2rem] shadow-[var(--shadow-luxe)]">
              <div className="aspect-[3/2]">
                <SmartImage
                  src="/images/night-gate.webp"
                  alt="MİA PARK OCEAN gece görünümü ve aydınlatmalı giriş kapısı"
                  sizes="(max-width: 1024px) 100vw, 60vw"
                  className="h-full w-full object-cover"
                />
              </div>
            </div>
            <div className="absolute -bottom-6 -right-4 hidden w-64 rounded-2xl bg-ink p-6 text-white shadow-[var(--shadow-luxe)] sm:block">
              <div className="font-display text-2xl font-bold leading-tight">
                3 Farklı<br />Yaşam Konsepti
              </div>
              <div className="mt-2 text-sm text-white/70">Brüt 28 m²'den 100 m²'ye kadar</div>
            </div>
          </div>
        </Reveal>

        {/* Metin */}
        <div className="order-1 lg:order-2">
          <Reveal>
            <div className="flex items-center gap-2.5">
              <span className="h-0.5 w-6 rounded bg-accent" />
              <span className="eyebrow text-accent">Proje</span>
            </div>
          </Reveal>
          <Reveal delay={0.05}>
            <h2 className="mt-4 text-4xl leading-tight text-ink md:text-5xl">
              Yaşamınızın <span className="gilded">yeni merkezi</span>
            </h2>
          </Reveal>
          <Reveal delay={0.1}>
            <p className="mt-5 text-lg leading-relaxed text-ink/70">
              Burada yürüyüş yolları, süs havuzları ve bahçe alanları gündelik hayatın bir parçası;
              sosyal avlular ise komşularınızla vakit geçirebileceğiniz alanlar. MİA PARK OCEAN'ı,
              her gün rahatça yaşayabileceğiniz bir yer olsun diye planladık.
            </p>
          </Reveal>

          <ul className="mt-8 grid gap-4 sm:grid-cols-2">
            {highlights.map((h, i) => (
              <Reveal as="li" key={h.text} delay={0.12 + i * 0.05} className="flex items-start gap-3">
                <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-accent-tint text-accent">
                  <Icon name={h.icon} className="h-5 w-5" />
                </span>
                <span className="pt-1.5 text-sm leading-relaxed text-ink/75">{h.text}</span>
              </Reveal>
            ))}
          </ul>

          <Reveal delay={0.2}>
            <div className="mt-9 flex flex-wrap gap-4">
              <ButtonLink href="/daireler">Daire Tiplerini İncele</ButtonLink>
              <ButtonLink href="/galeri" variant="outline">Galeriyi Gör</ButtonLink>
            </div>
          </Reveal>
        </div>
      </div>
    </section>
  );
}
