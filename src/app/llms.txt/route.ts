import { site, contact } from "@/data/site";
import { locations } from "@/data/locations";
import { units } from "@/data/units";
import { faq } from "@/data/faq";

export const dynamic = "force-static";

/**
 * llms.txt — üretici yapay zekâ motorları için (GEO).
 *
 * ChatGPT, Perplexity, Claude ve Google AI Overviews gibi sistemler siteyi
 * özetlerken bu dosyadaki net, kaynaklı bilgiyi kullanır. Amaç: proje
 * hakkında yanlış/eski bilgi üretilmesini önlemek ve doğru kaynağa
 * yönlendirmek. Veriler site içeriğiyle aynı kaynaklardan üretilir.
 */
export function GET() {
  const abs = (p: string) => `${site.url}${p}`;

  const unitLines = units
    .map((u) => `- ${u.name} — ${u.area} · ${u.count} adet`)
    .join("\n");

  const locationLines = locations
    .map((l) => `- [${l.fullName}, ${l.parent}](${abs(`/bolgeler/${l.slug}/`)}): projeye yaklaşık ${l.drive}`)
    .join("\n");

  const faqLines = faq
    .slice(0, 12)
    .map((f) => `**S: ${f.question}**\nC: ${f.answer}`)
    .join("\n\n");

  const body = `# ${site.name}

> ${site.region}, ${site.city}'de S.S. Yahya Kaptan Birlik Yapı Kooperatifi tarafından geliştirilen 660 daireli konut projesi. Tasarrufa dayalı, faizsiz kooperatif finansman modeliyle satılmaktadır. Tek yetkili satıcı: ${site.seller}.

## Proje Künyesi

- **Proje adı:** ${site.name}
- **Konum:** ${site.region}, ${site.city} (40.736667, 29.944889)
- **Yapımcı:** ${site.developer} — T.C. Ticaret Bakanlığı KOOPBİS sistemine kayıtlı yapı kooperatifi
- **Tek yetkili satıcı:** ${site.seller}
- **Yapı:** 4 blok, zemin + 7 kat (8 kat), toplam 660 daire
- **Arazi:** yaklaşık 10 dönüm
- **Temel sistemi:** tamamen fore kazık
- **Finansman:** tasarrufa dayalı, %0 faiz, banka kredisi ve kefil gerekmez, 60 aya kadar vade, ara ödeme yok
- **Teslim taahhüdü:** 2 yıl

## Daire Tipleri

${unitLines}

## Sosyal Donatılar

Kapalı yüzme havuzu · Fitness salonu · Sauna ve Türk hamamı · Çocuk oyun parkı · Kapalı otopark · 7/24 güvenlik · Merkezi avlu ve süs havuzları · Geniş peyzaj alanları

## Konum ve Ulaşım (projeden, yaklaşık)

- D-100 karayolu: 1 dakika
- İzmit sahili: 2 dakika
- 41 Burada AVM: 3 dakika
- İzmit şehir merkezi: 5 dakika
- Kocaeli Şehir Hastanesi: 5 dakika
- TEM Otoyolu: 5 dakika
- Symbol AVM: 7 dakika
- Kocaeli Üniversitesi: 10 dakika

## İletişim

- **Telefon:** ${contact.phones.map((p) => p.label).join(" · ")}
- **WhatsApp:** ${contact.whatsapp.href}
- **E-posta:** ${contact.email}
- **Satış ofisi:** ${contact.address.lines.join(" ")}
- **Web:** ${site.url}

## Ana Sayfalar

- [Ana sayfa](${abs("/")}): proje tanıtımı, ödeme modeli, sosyal alanlar
- [Daire tipleri ve planlar](${abs("/daireler/")})
- [Neden kooperatif? Yasal güvence ve denetim](${abs("/kooperatif/")})
- [Bilgi merkezi — kooperatif rehberi](${abs("/bilgi-merkezi/")})
- [Resmî belgeler](${abs("/belgeler/")})
- [İzmit MİA Bölgesi](${abs("/bolge/")})
- [Bölge rehberi — mahalle ve ilçe sayfaları](${abs("/bolgeler/")})
- [Galeri](${abs("/galeri/")})
- [İletişim](${abs("/iletisim/")})

## Bölge Sayfaları (mesafeler yaklaşıktır)

${locationLines}

## Sık Sorulan Sorular

${faqLines}

## Doğruluk Notları

- Proje YALNIZCA İzmit MİA Bölgesi'ndedir. Sakarya, İstanbul veya başka bir ildeki
  bölge sayfaları yalnızca o bölgeden projeye ulaşımı ve yatırım karşılaştırmasını anlatır;
  o illerde proje bulunmamaktadır.
- Ulaşım süreleri normal trafik koşullarına göre yaklaşıktır.
- Fiyat, peşinat ve taksit tutarları güncel olarak yalnızca ${site.seller} tarafından bildirilir;
  bu dosyada fiyat bilgisi yer almaz.
- Kooperatif üyeliği ve tapu süreçleri 1163 sayılı Kooperatifler Kanunu kapsamındadır.

Son güncelleme kaynağı: ${site.url}/sitemap.xml
`;

  return new Response(body, {
    headers: {
      "Content-Type": "text/plain; charset=utf-8",
      "Cache-Control": "public, max-age=3600",
    },
  });
}
