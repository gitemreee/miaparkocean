import type { Metadata } from "next";
import Link from "next/link";
import { Waves, Dumbbell, Flame, Baby, Car, Phone, Globe, Instagram, ShieldCheck } from "lucide-react";
import { contact, socials } from "@/data/site";

export const metadata: Metadata = {
  title: "Basın Açıklaması — MİA PARK OCEAN",
  description: "MİA PARK OCEAN lansman ve basın toplantısı açıklaması.",
  // Listelenmemiş / gizli sayfa: arama motorlarına kapalı, menüde/sitemap'te yok.
  robots: { index: false, follow: false },
};

const amenities = [
  { icon: Waves, label: "Kapalı yüzme havuzu" },
  { icon: Dumbbell, label: "Fitness salonu" },
  { icon: Flame, label: "Sauna ve Türk hamamı" },
  { icon: Baby, label: "Çocuk oyun parkı" },
  { icon: Car, label: "Kapalı otopark" },
];

const instagram = socials.find((s) => s.icon === "instagram");

// MİA monogram (footer ile aynı) — açık zemin için mürekkep rengi.
function MiaMonogram({ className = "" }: { className?: string }) {
  return (
    <svg viewBox="0 0 40 42" className={className} aria-hidden="true">
      <path d="M6 32V12l14 10 14-10v20" fill="none" stroke="#141414" strokeWidth="2.4" strokeLinejoin="round" strokeLinecap="round" />
      <path d="M20 22v10" fill="none" stroke="#141414" strokeWidth="2.4" strokeLinecap="round" />
      <circle cx="20" cy="7.5" r="1.7" fill="#D71D28" />
    </svg>
  );
}

export default function BasinAciklamasiPage() {
  return (
    <div className="min-h-screen bg-paper text-ink">
      {/* Üst marka bandı */}
      <div className="border-b border-ink/10">
        <div className="container-luxe flex items-center justify-between py-5">
          <div className="flex items-center gap-3">
            <MiaMonogram className="h-9 w-9" />
            <div className="leading-none">
              <div className="font-display text-lg font-semibold tracking-[0.16em]">MİA PARK OCEAN</div>
              <div className="eyebrow mt-1 text-[0.54rem] text-ink/45">İzmit MİA Bölgesi</div>
            </div>
          </div>
          <span className="pill hidden bg-accent-tint text-accent sm:inline-flex">
            <ShieldCheck className="h-4 w-4" /> Basın Bülteni
          </span>
        </div>
      </div>

      {/* Başlık — ortalanmış hoş geldin girişi */}
      <header className="container-luxe max-w-3xl pt-16 text-center md:pt-24">
        <span className="eyebrow text-accent">Lansman &amp; Basın Toplantısı</span>
        <h1 className="mx-auto mt-5 max-w-3xl font-display text-[2.2rem] font-bold leading-[1.08] tracking-tight text-ink sm:text-5xl md:text-[3.4rem]">
          İzmit&apos;in Yeni İncisi <span className="gilded">MİA PARK OCEAN</span> Lansmanına Hoş Geldiniz
        </h1>
        <p className="mx-auto mt-7 max-w-2xl text-lg leading-relaxed text-ink/70 sm:text-xl">
          Sizleri bu özel günde aramızda görmekten mutluluk duyuyor; Kocaeli&apos;ye değer katacak bu projeyi birlikte
          tanımaktan gurur duyuyoruz.
        </p>
      </header>

      {/* Konuşma metni */}
      <article className="container-luxe mt-12 max-w-3xl space-y-6 pb-20 text-[1.02rem] leading-relaxed text-ink/80">
        <p className="font-medium text-ink">Değerli Basın Mensupları ve Kıymetli Konuklar,</p>
        <p>
          Bugün burada, Kocaeli&apos;mize değer katacak, yaşam standartlarını yeniden belirleyecek vizyon projemiz Mia
          Park Ocean&apos;ı sizlere tanıtmaktan büyük bir gurur ve heyecan duyuyoruz. Yahya Kaptan Birlik Yapı Kooperatifi
          olarak, şehrimizin en prestijli noktalarından biri olan Mia bölgesinde, doğayla iç içe ama bir o kadar da
          şehrin tam merkezinde yepyeni bir yaşam alanı inşa ediyoruz.
        </p>

        <h2 className="pt-4 font-display text-2xl font-bold text-ink">Şehrin Merkezinde, Modern ve Güvenli Bir Yaşam</h2>
        <p>
          Toplam 10 dönüm arazi üzerine konumlandırılan projemiz, şehrin her yerine çok yakın olan eşsiz bir lokasyonda
          yer alıyor. Deprem gerçeğini asla unutmuyor, güvenliği her şeyin üstünde tutuyoruz. Bu doğrultuda, 8 katlı 4
          bloktan oluşan projemizin temellerini tamamen fore kazık sistemiyle, depreme ekstra dayanıklı olarak inşa
          ediyoruz.
        </p>
        <p>
          Modern mimarisiyle Kocaeli&apos;nin silüetine değer katacak Mia Park Ocean, eşsiz deniz ve şehir manzaralı
          daireleriyle ferah bir yaşam vaat ediyor. Toplamda 600 rezidanstan oluşan projemizde; her ihtiyaca ve bütçeye
          uygun 1+0, 1+1 ve 2+1 daire seçeneklerimiz bulunuyor. Özellikle giriş katlarımızda tasarladığımız, her birinin
          kendine ait özel bahçesi bulunan loft dairelerimiz, müstakil ev konforunu rezidans ayrıcalığıyla birleştiriyor.
        </p>

        <h2 className="pt-4 font-display text-2xl font-bold text-ink">
          Ayrıcalıklı Sosyal Alanlar ve Doğayla İç İçe Bir Konsept
        </h2>
        <p>
          Sizlere sadece bir ev değil; huzur ve mutluluğun bir arada olduğu, görselliğin ön planda tutulduğu eksiksiz bir
          yaşam merkezi sunuyoruz. Özel süs havuzlarımız ve geniş yeşil alanlarımızla, günün yorgunluğunu atabileceğiniz
          huzurlu bir peyzaj hazırladık.
        </p>
        <p>Bunun yanı sıra projemiz bünyesinde yer alan;</p>
        <ul className="grid gap-3 sm:grid-cols-2">
          {amenities.map((a) => (
            <li key={a.label} className="flex items-center gap-3 rounded-xl border border-ink/10 bg-paper-2 px-4 py-3">
              <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-accent-tint text-accent">
                <a.icon className="h-5 w-5" strokeWidth={2} />
              </span>
              <span className="font-medium text-ink">{a.label}</span>
            </li>
          ))}
        </ul>
        <p>
          gibi zengin sosyal donatılarımızla, sakinlerimizin yaşam kalitesini en üst düzeye çıkarıyoruz.
        </p>

        <h2 className="pt-4 font-display text-2xl font-bold text-ink">Faiz Yok, Ara Ödeme Yok: 2 Yılda Teslim!</h2>
        <p>
          Yahya Kaptan Birlik Yapı Kooperatifi olarak, herkesin bu prestijli projede yer alabilmesi için çok özel bir
          finansal model geliştirdik. Ev sahibi olmak veya yatırım yapmak isteyen vatandaşlarımızı ağır banka
          yüklerinden kurtarıyor; çok uygun ödeme koşullarıyla, faizsiz ve ara ödemesiz bir sistem sunuyoruz. Üstelik bu
          dev projeyi sadece 2 yıl içerisinde tamamlayarak sahiplerine teslim etmeyi taahhüt ediyoruz.
        </p>
        <p>
          Mia Park Ocean, yalnızca bir konut projesi değil; Kocaeli için yeni bir vizyon, kârlı bir yatırım ve mutlu
          yarınların teminatıdır. Projemizin şehrimize, kooperatif üyelerimize ve gelecekteki tüm sakinlerimize hayırlı
          olmasını diliyor, lansmanımıza katılımlarınızdan dolayı hepinize teşekkürlerimi sunuyorum.
        </p>
      </article>

      {/* Alt: iletişim + logolar */}
      <footer className="border-t border-ink/10 bg-paper-2">
        <div className="container-luxe py-12">
          <div className="mx-auto max-w-3xl">
            <div className="eyebrow text-accent">İletişim</div>
            <div className="mt-5 flex flex-wrap items-center gap-x-8 gap-y-4">
              <a href="https://miaparkocean.com" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 text-sm font-medium text-ink transition-colors hover:text-accent">
                <Globe className="h-4 w-4 text-accent" /> www.miaparkocean.com
              </a>
              {instagram && (
                <a href={instagram.href} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 text-sm font-medium text-ink transition-colors hover:text-accent">
                  <Instagram className="h-4 w-4 text-accent" /> @miaparkocean
                </a>
              )}
              {contact.phones.map((p) => (
                <a key={p.href} href={p.href} className="inline-flex items-center gap-2 text-sm font-medium text-ink transition-colors hover:text-accent">
                  <Phone className="h-4 w-4 text-accent" /> {p.label}
                </a>
              ))}
            </div>

            {/* Logolar */}
            <div className="mt-9 flex flex-wrap items-center gap-x-12 gap-y-8 border-t border-ink/10 pt-9">
              <div className="flex items-center gap-3">
                <MiaMonogram className="h-14 w-14" />
                <span className="font-display text-xl font-semibold tracking-[0.14em] text-ink">MİA PARK OCEAN</span>
              </div>
              <img src="/ykb-logo.png" alt="S.S. Yahya Kaptan Birlik Yapı Kooperatifi" className="h-[4.5rem] w-auto" />
              <img src="/ocean-logo.webp" alt="Ocean Gayrimenkul" className="h-11 w-auto" width={160} height={36} />
            </div>

            <p className="mt-8 text-xs leading-relaxed text-ink/45">
              Yapımcı: S.S. Yahya Kaptan Birlik Yapı Kooperatifi · Tek Yetkili Satıcı: Ocean Gayrimenkul ·
              {" "}
              <Link href="/" className="text-accent hover:underline">
                miaparkocean.com
              </Link>
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
