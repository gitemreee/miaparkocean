/**
 * MİA PARK OCEAN — emlakçı / broker lansman sunumu.
 *
 * B2B satış sunumu formatı: "bu projeyi neden portföyünüze almalısınız,
 * müşteriye nasıl anlatırsınız". Konut kataloğu değil.
 *
 * Tasarım dili: koyu lacivert · sıcak krem · champagne gold. İnce altın
 * çizgiler, düz lacivert ve krem bloklar, büyük Playfair Display başlık,
 * Montserrat alt metin. Dekoratif grafik, 3B ikon, gölgeli kart yok.
 *
 * Ritim bilinçli: tam kanama render → %60 görsel + %40 metin → büyük
 * rakam → infografik → dergi ızgarası. Aynı düzen arka arkaya gelmiyor.
 *
 *   python3 scripts/build-sunum-gorsel.py    # fotoğraf/perde/infografik
 *   node    scripts/build-sunum.js           # sunum
 *
 * Fotoğraflar yerleşecekleri kutunun tam pikseline kırpılmış olarak
 * geliyor; burada hiçbir görsel gerdirilmiyor.
 */
const pptxgen = require("pptxgenjs");
const path = require("path");
const fs = require("fs");

const KOK = path.join(__dirname, "..");
const KAYNAK = path.join(KOK, "sunum", "kaynak");
const fo = (n) => path.join(KAYNAK, "foto", n + ".jpg");
const ka = (n) => path.join(KAYNAK, n + ".png");
const mk = (n) => path.join(KOK, "public", n);
const INFO = JSON.parse(fs.readFileSync(path.join(KAYNAK, "info.json"), "utf-8"));

/* ---------------------------------------------------------------- palet */
const GECE   = "06192B",   // gece mavisi — tam kanama zeminler
      LACI   = "0E2E46",   // lacivert blok
      KREM   = "F3EDE3",   // sıcak kırık beyaz
      KREM_K = "E6DCCB",   // krem ayraç
      ALTIN  = "C9A961",   // champagne gold
      ALTIN_A= "E0CB9C",
      SU     = "6FA8BE",   // çok sınırlı açık mavi
      BEYAZ  = "FFFFFF",
      KURSUN = "6E6357",   // krem üstünde ikincil metin
      SIS    = "AFC0CC";   // lacivert üstünde ikincil metin

/* Başlık: premium editorial serif. Alt metin: modern sans. */
const SERIF = "Playfair Display";
const SANS  = "Montserrat";

const W = 13.333, HT = 7.5;
const M = 0.95;                    // tek kenar boşluğu — bütün slaytlarda aynı ızgara

const p = new pptxgen();
p.layout = "LAYOUT_WIDE";
p.author = "Ocean Gayrimenkul";
p.company = "MİA PARK OCEAN";
p.title = "MİA PARK OCEAN — Emlakçı Sunumu";
p.subject = "İzmit MİA Bölgesi · Broker Presentation";

/* --------------------------------------------------------------- parçalar */
function blok(s, x, y, w, h, renk) {
  /* line verilmezse pptxgenjs kenarlık çizmiyor; verince ince koyu çizgi
     kalıyordu ve krem bloklarda görünüyordu. */
  s.addShape(p.ShapeType.rect, { x, y, w, h, fill: { color: renk } });
}
function zeminFoto(s, ad, perdeAd) {
  s.addImage({ path: fo(ad), x: 0, y: 0, w: W, h: HT });
  if (perdeAd) s.addImage({ path: ka(perdeAd), x: 0, y: 0, w: W, h: HT });
}
/* ince altın çizgi — bu sunumun tek dekoratif öğesi */
function cizgi(s, x, y, w, renk, kalinlik) {
  s.addShape(p.ShapeType.line, { x, y, w, h: 0,
    line: { color: renk || ALTIN, width: kalinlik || 1 } });
}
function dikeyCizgi(s, x, y, h, renk, kalinlik) {
  s.addShape(p.ShapeType.line, { x, y, w: 0, h,
    line: { color: renk || KREM_K, width: kalinlik || 0.75 } });
}
/* harf aralıklı küçük etiket */
function etiket(s, t, x, y, renk, w, boy) {
  s.addText(t, { x, y, w: w || 5.0, h: 0.24, fontFace: SANS, fontSize: boy || 9,
    bold: true, color: renk || ALTIN, charSpacing: 3.4, margin: 0 });
}
function baslik(s, t, x, y, o) {
  o = o || {};
  s.addText(t, { x, y, w: o.w || 6.4, h: o.h || 1.0, fontFace: SERIF,
    fontSize: o.boy || 34, color: o.renk || GECE, bold: o.kalin !== false,
    italic: !!o.italik, align: o.hiza || "left", valign: o.dikey || "top",
    lineSpacingMultiple: o.satir || 1.02, charSpacing: o.aralik || 0, margin: 0 });
}
function metin(s, t, x, y, o) {
  o = o || {};
  s.addText(t, { x, y, w: o.w || 5.0, h: o.h || 0.6, fontFace: SANS,
    fontSize: o.boy || 10.5, color: o.renk || KURSUN, bold: !!o.kalin,
    italic: !!o.italik, align: o.hiza || "left", valign: o.dikey || "top",
    lineSpacingMultiple: o.satir || 1.30, charSpacing: o.aralik || 0, margin: 0 });
}
/* Playfair rakam — büyük sayılar bu sunumun omurgası */
function rakam(s, t, x, y, o) {
  o = o || {};
  s.addText(t, { x, y, w: o.w || 3.0, h: o.h || 1.15, fontFace: SERIF,
    fontSize: o.boy || 54, bold: true, color: o.renk || GECE,
    align: o.hiza || "left", valign: "bottom", margin: 0 });
}
/* sayfa altı imza — logo her slaytta değil, künye her slaytta */
function kunye(s, koyu, sagSinir) {
  /* sagSinir: içerik alanının bittiği x. Sağda tam boy fotoğraf varsa
     künyenin sağ yarısı fotoğrafın altında kaybolduğu için hiç basılmıyor. */
  const renk = koyu ? "5C6B78" : "A79C8C";
  metin(s, "MİA PARK OCEAN  ·  İZMİT MİA BÖLGESİ", M, 7.02,
    { w: 6.0, boy: 7.5, aralik: 2.2, renk });
  const sag = sagSinir || (W - M);
  if (sag > 9.6) {
    metin(s, "OCEAN GAYRİMENKUL — TEK YETKİLİ SATICI", sag - 5.2, 7.02,
      { w: 5.2, boy: 7.5, aralik: 2.2, hiza: "right", renk });
  }
}

let s;

/* ═══════════════════════════════════════════════════════ 1 · KAPAK */
s = p.addSlide();
zeminFoto(s, "tam-kapak", "perde-kapak");
s.addImage({ path: mk("brand/logo-ocean-white.png"), x: M, y: 3.10, w: 3.70, h: 2.53 });
cizgi(s, M, 5.92, 1.30, ALTIN, 1.5);
etiket(s, "İZMİT MİA BÖLGESİ", M, 6.14, ALTIN_A, 5.0, 9.5);
baslik(s, "Emlakçılar İçin Yeni Bir Satış Fırsatı", M, 6.48,
  { w: 6.2, h: 0.6, boy: 21, renk: BEYAZ, kalin: false });
metin(s, "OCEAN GAYRİMENKUL — TEK YETKİLİ SATICI", W - M - 5.0, 6.98,
  { w: 5.0, boy: 8.5, aralik: 2.4, hiza: "right", renk: SIS });
s.addNotes("Açılış. Kendinizi ve Ocean Gayrimenkul'ü tanıtın. Bu sunum bir konut kataloğu değil; bugün emlakçıya 'bu projeyi neden portföyüne almalı' sorusunun cevabını veriyoruz. Süre 20 dakika, sonrasında soru-cevap.");

/* ══════════════════════════════════════ 2 · PROJEYİ 30 SANİYEDE ANLAT */
s = p.addSlide();
s.background = { color: KREM };
s.addImage({ path: fo("yar-ozet"), x: W - 5.35, y: 0, w: 5.35, h: HT });
etiket(s, "PROJE ÖZETİ", M, 0.86);
baslik(s, "MİA PARK OCEAN\nNedir?", M, 1.24, { w: 6.0, h: 1.9, boy: 44, satir: 0.98 });
cizgi(s, M, 3.16, 1.30, ALTIN, 1.5);
[["600", "Konut"], ["60 AY", "Vade farksız ödeme"],
 ["584", "1+0 ve 1+1 stok"], ["MİA", "İzmit Merkezi İş Alanı"]].forEach((k, i) => {
  const x = M + (i % 2) * 3.35, y = 3.52 + Math.floor(i / 2) * 1.42;
  rakam(s, k[0], x, y, { w: 3.05, h: 0.82, boy: k[0].length > 3 ? 34 : 42 });
  metin(s, k[1], x, y + 0.88, { w: 3.05, h: 0.30, boy: 9.5, aralik: 1.4, renk: KURSUN });
  cizgi(s, x, y + 1.22, 2.90, KREM_K, 0.75);
});
metin(s, "MİA PARK OCEAN, İzmit'in gelişen merkezi iş alanında konumlanan; yatırım ve yaşam talebini aynı noktada buluşturan modern konut projesidir.",
  M, 6.36, { w: 6.55, h: 0.60, boy: 10.5, italik: true, renk: "8A7F70" });
kunye(s, true, W - 5.35);
s.addNotes("Projeyi 30 saniyede anlatın: 600 konut, İzmit MİA Bölgesi, 60 aya kadar vade farksız ödeme, ağırlıklı olarak 1+0 ve 1+1. Emlakçı bu dört rakamı aklında tutsun.");

/* ═════════════════════════════════ 3 · EMLAKÇI İÇİN NEDEN ÖNEMLİ */
s = p.addSlide();
s.background = { color: KREM };
etiket(s, "PORTFÖY DEĞERLENDİRMESİ", M, 0.86);
baslik(s, "Satılması Kolay Bir Ürün Neden Oluşur?", M, 1.24, { w: 11.44, h: 0.9, boy: 34 });
cizgi(s, M, 2.44, 1.30, ALTIN, 1.5);
[["01", "Merkezi lokasyon", "Müşteriye konumu anlatmak kolay. Dakika bazlı mesafeler tek cümlede aktarılır."],
 ["02", "Kompakt daire seçenekleri", "Daha geniş yatırımcı kitlesine hitap eder. Giriş bütçesi düşer, talep genişler."],
 ["03", "Uzun vadeli ödeme", "Alıcının giriş bariyerini azaltır. Kredisi çıkmayan müşteri portföyde kalır."],
 ["04", "Güçlü proje görselliği", "Sunum ve dijital satışta yüksek algı oluşturur. Materyal hazır gelir."]]
.forEach((k, i) => {
  const x = M + i * 2.94;
  if (i) dikeyCizgi(s, x - 0.30, 3.00, 2.55, KREM_K, 0.75);
  rakam(s, k[0], x, 2.96, { w: 1.4, h: 0.72, boy: 30, renk: ALTIN });
  baslik(s, k[1], x, 3.88, { w: 2.50, h: 0.72, boy: 16, satir: 1.06 });
  metin(s, k[2], x, 4.66, { w: 2.50, h: 1.10, boy: 9.5 });
});
blok(s, 0, 6.06, W, 1.44, LACI);
baslik(s, "İyi proje yalnızca güzel değildir; doğru müşteriye kolay anlatılabilir.",
  0, 6.06, { w: W, h: 1.44, boy: 19, renk: KREM, kalin: false, italik: true,
             hiza: "center", dikey: "middle" });
s.addNotes("Bu slayt sunumun tezi. Emlakçı 'güzel proje' duymaktan sıkılmıştır; ona satılabilirlik argümanı verin. Dördüncü maddede materyal desteğini vurgulayın.");

/* ══════════════════════════════════════════════════════ 4 · KONUM */
s = p.addSlide();
s.background = { color: GECE };
etiket(s, "KONUM", M, 0.86, ALTIN);
baslik(s, "İzmit'in Yeni\nDeğer Aksı", M, 1.24, { w: 4.1, h: 1.9, boy: 38, renk: KREM, satir: 0.98 });
cizgi(s, M, 3.18, 1.30, ALTIN, 1.5);
metin(s, "Günlük yaşam, ulaşım, sağlık, eğitim ve alışveriş birkaç dakikalık erişim alanında.",
  M, 3.50, { w: 3.90, h: 0.90, boy: 11, renk: SIS, satir: 1.42 });
metin(s, "Işınların uzunluğu süreyle orantılıdır.", M, 6.20,
  { w: 3.90, h: 0.30, boy: 8.5, italik: true, renk: "6E7F8C" });
/* diyagram: geometri PIL'den, etiketler gerçek metin kutusu */
/* Kutu genişlikleri ölçüyle seçildi: en dıştaki etiket 5.75"–12.71"
   aralığında kalıyor; ne sol sütuna ne sağ kenara değiyor. */
const DX = 6.35, DY = 1.05, EW = 1.70;
s.addImage({ path: ka("info-konum"), x: DX, y: DY, w: 6.30, h: 5.30 });
baslik(s, "MİA PARK\nOCEAN", DX + INFO.konum.merkez.x - 1.00, DY + INFO.konum.merkez.y - 0.32,
  { w: 2.00, h: 0.64, boy: 11, renk: GECE, hiza: "center", satir: 1.02 });
INFO.konum.capalar.forEach((c) => {
  const x = c.hiza === "left" ? DX + c.x
          : c.hiza === "right" ? DX + c.x - EW
          : DX + c.x - EW / 2;
  metin(s, c.ad, x, DY + c.y - 0.32, { w: EW, h: 0.24, boy: 8.5, hiza: c.hiza, renk: SIS });
  baslik(s, c.dk + " dk", x, DY + c.y - 0.08, { w: EW, h: 0.32, boy: 15, renk: ALTIN, hiza: c.hiza });
});
kunye(s, false, 5.35);
s.addNotes("Mesafeleri ezberleyin; en çok D100 ve şehir hastanesi sorulur. Diyagramda ışın uzunluğu süreyle orantılı, yani göz otomatik olarak en yakınları görüyor. İzmit Sahili süresi teyide açık, kesin konuşmayın.");

/* ═══════════════════════════════════════════════ 5 · MİA BÖLGESİ NEDİR */
s = p.addSlide();
s.background = { color: KREM };
s.addImage({ path: fo("yar-mia"), x: W - 5.10, y: 0, w: 5.10, h: HT });
etiket(s, "BÖLGE", M, 0.86);
baslik(s, "MİA Neden Önemli?", M, 1.24, { w: 6.6, h: 0.9, boy: 40 });
metin(s, "MİA, Merkezi İş Alanı demektir: bir şehrin ofis, ticaret ve hizmet fonksiyonlarının yoğunlaşması için planlanan bölge.",
  M, 2.28, { w: 6.5, h: 0.70, boy: 11, renk: KURSUN });
cizgi(s, M, 3.16, 1.30, ALTIN, 1.5);
[["01", "Yeni ticari merkez", "Ofis, ticaret ve hizmet fonksiyonlarının yoğunlaşacağı bölge."],
 ["02", "Yeni yaşam aksı", "Yeni konut ve karma kullanımlı projelerin geliştiği bölge."],
 ["03", "Değerlenme potansiyeli", "Altyapı ve ticari hareketlilik arttıkça bölgenin yatırım çekiciliği artar."]]
.forEach((k, i) => {
  const y = 3.50 + i * 1.10;
  rakam(s, k[0], M, y, { w: 0.75, h: 0.44, boy: 19, renk: ALTIN });
  baslik(s, k[1], M + 0.90, y - 0.02, { w: 5.4, h: 0.40, boy: 17 });
  metin(s, k[2], M + 0.90, y + 0.40, { w: 5.5, h: 0.52, boy: 9.5 });
});
metin(s, "Bölgesel gelişim bir potansiyeldir; değer artışı taahhüdü değildir.",
  M, 6.94, { w: 6.5, h: 0.28, boy: 8, italik: true, renk: "9A9082" });
s.addNotes("MİA kısaltmasını mutlaka açın; emlakçıların çoğu bilmiyor. DİKKAT: 'kesin değer artışı' demeyin. 'Potansiyel', 'gelişim aksı', 'yatırım çekiciliği' deyin.");

/* ══════════════════════════════════ 6 · BÖLGENİN STRATEJİK AVANTAJI */
s = p.addSlide();
s.background = { color: KREM };
etiket(s, "PAZAR", M, 0.86);
baslik(s, "İstanbul'a Yakın, İzmit'in Merkezinde", M, 1.24, { w: 10.2, h: 0.9, boy: 38 });
cizgi(s, M, 2.44, 1.30, ALTIN, 1.5);
blok(s, M, 2.86, 5.42, 1.98, LACI);
etiket(s, "İZMİT YATIRIMCISI İÇİN", M + 0.46, 3.24, ALTIN_A, 4.6);
baslik(s, "Şehrin gelişen yeni merkezinde konum", M + 0.46, 3.58,
  { w: 4.6, h: 0.86, boy: 19, renk: KREM, kalin: false, satir: 1.06 });
blok(s, 6.96, 2.86, 5.42, 1.98, KREM_K);
etiket(s, "İSTANBUL YATIRIMCISI İÇİN", 7.42, 3.24, "8A6B2E", 4.6);
baslik(s, "Anadolu Yakası'na kıyasla erişilebilir bütçe", 7.42, 3.58,
  { w: 4.6, h: 0.86, boy: 19, renk: GECE, kalin: false, satir: 1.06 });
/* ulaşım aksı */
const AX = M - 0.09, AY = 5.32;
s.addImage({ path: ka("info-aks"), x: AX, y: AY, w: 11.60, h: 1.30 });
const AKS = INFO.aks.capalar;
AKS.forEach((c) => {
  const w = 3.30, x = AX + c.x - w / 2;
  if (c.ana) {
    baslik(s, c.ad, x, AY + c.y - 0.88, { w, h: 0.34, boy: 15, hiza: "center", renk: GECE });
  } else {
    metin(s, c.ad, x, AY + c.y + 0.26, { w, h: 0.28, boy: 10, hiza: "center", renk: GECE, kalin: true });
  }
});
/* süreler duraklar ARASINDA, çizginin üstünde — uçlara koyunca durak
   adlarının üstüne biniyordu (sunum-cakisma.py yakaladı) */
[["yaklaşık 1,5–2 saat", 0, 1], ["yaklaşık 45–60 dakika", 1, 2]].forEach((d) => {
  const orta = (AKS[d[1]].x + AKS[d[2]].x) / 2, w = 2.60;
  metin(s, d[0], AX + orta - w / 2, AY + AKS[0].y - 0.46,
    { w, h: 0.26, boy: 9, hiza: "center", italik: true, renk: "9A9082" });
});
s.addNotes("İki yönlü anlatı: İzmit yatırımcısına merkeziyet, İstanbul yatırımcısına bütçe. Marmara yatırımcısı bu projenin ikinci müşteri havuzu — emlakçıya bunu hatırlatın.");

/* ═══════════════════════════════════════════════════ 7 · PROJE MİMARİSİ */
s = p.addSlide();
zeminFoto(s, "tam-mimari", "perde-mimari");
etiket(s, "MİMARİ", M, 4.34, ALTIN_A);
baslik(s, "Modern ve\nZamansız Mimari", M, 4.70,
  { w: 5.4, h: 1.60, boy: 36, renk: BEYAZ, satir: 1.0 });
cizgi(s, M, 6.52, 1.30, ALTIN, 1.5);
["Modern cephe dili", "Geniş peyzaj alanları", "Süs havuzu ve su aksları",
 "Düzenli site içi ulaşım", "Balkonlu daireler", "Güvenlikli site yaklaşımı",
 "Gün ışığı odaklı cepheler"].forEach((o, i) => {
  const x = 7.00 + (i % 2) * 3.10, y = 4.72 + Math.floor(i / 2) * 0.52;
  cizgi(s, x, y + 0.14, 0.16, ALTIN, 1);
  metin(s, o, x + 0.30, y, { w: 2.76, h: 0.28, boy: 10.5, renk: BEYAZ });
});
metin(s, "Projedeki su öğeleri peyzaj amaçlı süs havuzu ve su akslarıdır.",
  7.00, 6.68, { w: 5.4, h: 0.26, boy: 8.5, italik: true, renk: SIS });
s.addNotes("DİKKAT: Projede yüzme havuzu YOK. Sudaki öğeler peyzaj amaçlı süs havuzu ve su aksı. Yüzme havuzu sözü verilirse teslimde sorun çıkar.");

/* ═════════════════════════════════════════════════ 8 · ÜRÜN DAĞILIMI */
s = p.addSlide();
s.background = { color: KREM };
etiket(s, "ÜRÜN", M, 0.86);
baslik(s, "Satışın Omurgası: 1+0 ve 1+1", M, 1.24, { w: 9.6, h: 0.9, boy: 38 });
cizgi(s, M, 2.42, 1.30, ALTIN, 1.5);
[["urun-1plus0", "1+0", "472", "Yatırım, kiralama ve kompakt yaşam talebine yönelik güçlü stok."],
 ["urun-1plus1", "1+1", "112", "Tek kişi, çiftler ve yatırımcı müşteriler için dengeli ürün."]]
.forEach((u, i) => {
  const x = M + i * 5.72;
  s.addImage({ path: fo(u[0]), x, y: 2.84, w: 5.30, h: 2.55 });
  blok(s, x, 5.39, 5.30, 1.44, i ? LACI : GECE);
  baslik(s, u[1], x + 0.40, 5.56, { w: 1.6, h: 0.52, boy: 26, renk: ALTIN });
  metin(s, "ADET", x + 2.10, 5.50, { w: 2.8, h: 0.22, boy: 8.5, aralik: 2.4,
    hiza: "right", renk: ALTIN_A });
  rakam(s, u[2], x + 2.10, 5.66, { w: 2.8, h: 0.60, boy: 34, renk: KREM, hiza: "right" });
  metin(s, u[3], x + 0.40, 6.34, { w: 4.5, h: 0.40, boy: 9.5, renk: SIS });
});
metin(s, "Projenin ana satış gücü kompakt daire segmentidir.", M, 6.96,
  { w: 11.4, h: 0.30, boy: 10.5, italik: true, hiza: "center", renk: "8A7F70" });
s.addNotes("584 dairenin ikisi de kompakt. Emlakçı için bu şu demek: tek bir müşteri profiline değil, çok geniş bir havuza satabilirsiniz. Bu slaytta 2+1'den söz etmiyoruz.");

/* ═══════════════════════════════════════════════ 9 · MÜŞTERİ PROFİLLERİ */
s = p.addSlide();
s.background = { color: KREM };
s.addImage({ path: fo("yar-profil"), x: W - 4.10, y: 0, w: 4.10, h: HT });
etiket(s, "HEDEF KİTLE", M, 0.86);
baslik(s, "Bu Projeyi Kime Satabilirsiniz?", M, 1.24, { w: 7.4, h: 1.5, boy: 38, satir: 0.98 });
cizgi(s, M, 2.86, 1.30, ALTIN, 1.5);
[["İlk kez konut alanlar", "Düşük başlangıç bariyeri arayanlar."],
 ["Yatırımcılar", "Kiralama potansiyeli olan kompakt konut arayanlar."],
 ["İstanbul yatırımcıları", "İstanbul dışında alternatif arayanlar."],
 ["Çalışan profesyoneller", "Merkezi ve ulaşımı kolay daire isteyenler."],
 ["Çocuğu üniversitede okuyan aileler", "Kocaeli Üniversitesi ve şehir merkezine yakınlık arayanlar."]]
.forEach((k, i) => {
  const y = 3.22 + i * 0.80;
  rakam(s, "0" + (i + 1), M, y, { w: 0.70, h: 0.38, boy: 17, renk: ALTIN });
  baslik(s, k[0], M + 0.86, y - 0.04, { w: 4.0, h: 0.36, boy: 15 });
  metin(s, k[1], M + 4.96, y + 0.02, { w: 3.4, h: 0.44, boy: 9, renk: KURSUN });
  if (i < 4) cizgi(s, M, y + 0.60, 7.44, KREM_K, 0.75);
});
s.addNotes("Beş profili sırayla okuyun ve her birinde emlakçıya sorun: portföyünüzde böyle kaç müşteri var? Salonda isim çıkarsa satış başlamış demektir.");

/* ══════════════════════════════════════════════════ 10 · ÖDEME MODELİ */
s = p.addSlide();
s.background = { color: GECE };
s.addImage({ path: fo("yar-odeme"), x: W - 4.35, y: 0, w: 4.35, h: HT });
etiket(s, "FİNANSMAN", M, 0.86, ALTIN);
baslik(s, "Alıcının Önündeki Finansman\nEngelini Azaltan Model", M, 1.24,
  { w: 7.4, h: 1.6, boy: 34, renk: KREM, satir: 1.0 });
cizgi(s, M, 3.02, 1.30, ALTIN, 1.5);
[["%30", "Peşinat"], ["60 AY", "Vade farksız"]].forEach((k, i) => {
  const x = M + i * 3.70;
  rakam(s, k[0], x, 3.42, { w: 3.4, h: 1.10, boy: 60, renk: ALTIN });
  metin(s, k[1], x, 4.60, { w: 3.4, h: 0.30, boy: 10, aralik: 2.6, renk: SIS });
});
blok(s, M, 5.24, 7.44, 0.78, LACI);
baslik(s, "BANKA YOK   ·   FAİZ YOK   ·   KEFİL YOK", M, 5.24,
  { w: 7.44, h: 0.78, boy: 19, renk: ALTIN, hiza: "center", dikey: "middle", aralik: 1.4 });
metin(s, "Tasarrufa dayalı finansman yaklaşımı sayesinde konut alımında banka kredisine alternatif bir ödeme modeli sunulur.",
  M, 6.30, { w: 7.3, h: 0.60, boy: 10.5, renk: SIS, satir: 1.36 });
kunye(s);
s.addNotes("Sunumun en güçlü slaydı. Emlakçı buradan tek cümle götürsün: bankaya gitmeden, faiz ödemeden, kefil bulmadan ev. Kredisi çıkmayan müşteri artık kayıp müşteri değil.");

/* ══════════════════════════════════════════════════ 11 · FİYAT ÖRNEĞİ */
s = p.addSlide();
s.background = { color: KREM };
etiket(s, "ÖRNEK ÖDEME", M, 0.86);
baslik(s, "Bugünkü Ödeme Örnekleri", M, 1.24, { w: 9.0, h: 0.9, boy: 38 });
cizgi(s, M, 2.42, 1.30, ALTIN, 1.5);
[["1+0", "699.000 TL", "29.900 TL"], ["1+1", "999.000 TL", "39.900 TL"]].forEach((f, i) => {
  const x = M + i * 5.72;
  blok(s, x, 2.86, 5.30, 2.94, i ? LACI : GECE);
  baslik(s, f[0], x + 0.46, 3.14, { w: 2.0, h: 0.62, boy: 30, renk: ALTIN });
  cizgi(s, x + 0.46, 3.94, 4.38, "2C4459", 0.75);
  metin(s, "PEŞİNAT", x + 0.46, 4.14, { w: 2.2, h: 0.26, boy: 8.5, aralik: 2.4, renk: SIS });
  baslik(s, f[1], x + 0.46, 4.40, { w: 4.4, h: 0.52, boy: 24, renk: KREM });
  metin(s, "AYLIK", x + 0.46, 5.02, { w: 2.2, h: 0.26, boy: 8.5, aralik: 2.4, renk: SIS });
  baslik(s, f[2], x + 0.46, 5.24, { w: 4.4, h: 0.46, boy: 21, renk: ALTIN_A });
});
blok(s, M, 6.06, 11.44, 0.66, KREM_K);
baslik(s, "60 AY  ·  VADE FARKSIZ", M, 6.06,
  { w: 11.44, h: 0.66, boy: 17, renk: "8A6B2E", hiza: "center", dikey: "middle", aralik: 2.0 });
metin(s, "Fiyatlar ve kampanya koşulları dönemsel olarak değişebilir. Güncel bilgi için satış ofisiyle iletişime geçiniz.",
  M, 6.94, { w: 11.44, h: 0.28, boy: 8, italik: true, hiza: "center", renk: "9A9082" });
s.addNotes("Rakamları verirken mutlaka dipnotu da söyleyin: fiyat ve kampanya koşulları dönemseldir. Yazılı teklif satış ofisinden çıkar.");

/* ═════════════════════════════════════════ 12 · EMLAKÇININ SATIŞ ARGÜMANI */
s = p.addSlide();
s.background = { color: KREM };
s.addImage({ path: fo("ser-arguman"), x: 0, y: 0, w: W, h: 2.10 });
s.addImage({ path: ka("perde-serit"), x: 0, y: 0, w: W, h: 2.10 });
etiket(s, "SAHA", M, 0.62, ALTIN_A);
baslik(s, "Müşteriye 60 Saniyede Nasıl Anlatılır?", M, 0.96,
  { w: 9.4, h: 0.9, boy: 34, renk: BEYAZ });
[["Proje İzmit'in gelişen MİA Bölgesi'nde."],
 ["D100'e 1 dakika, sahile 2 dakika."],
 ["Projede ağırlıklı olarak yatırımcıya uygun 1+0 ve 1+1 daireler var."],
 ["Bankasız, faizsiz ve kefilsiz 60 aya kadar ödeme modeli bulunuyor."],
 ["İstanbul'a yakınlığı nedeniyle yalnız İzmit'e değil, Marmara yatırımcısına da hitap ediyor."]]
.forEach((c, i) => {
  const y = 2.72 + i * 0.86;
  rakam(s, String(i + 1), M, y, { w: 0.64, h: 0.46, boy: 22, renk: ALTIN });
  baslik(s, "“" + c[0] + "”", M + 0.86, y - 0.02, { w: 10.5, h: 0.52, boy: 18,
    kalin: false, italik: true });
  if (i < 4) cizgi(s, M, y + 0.62, 11.44, KREM_K, 0.75);
});
kunye(s, true);
s.addNotes("Bu beş cümleyi emlakçıya ezberletin. Sırası önemli: konum, mesafe, ürün, ödeme, pazar. Beşinci cümle projeyi İzmit'in dışına açıyor.");

/* ════════════════════════════════════════════════ 13 · İTİRAZ YÖNETİMİ */
s = p.addSlide();
s.background = { color: KREM };
etiket(s, "İTİRAZ YÖNETİMİ", M, 0.86);
baslik(s, "Müşteri Sorarsa Ne Söyleyeceğiz?", M, 1.24, { w: 9.6, h: 0.9, boy: 38 });
cizgi(s, M, 2.42, 1.30, ALTIN, 1.5);
[["Kooperatif modeli güvenli mi?", "Proje, 1163 sayılı Kooperatifler Kanunu çerçevesinde faaliyet gösteren bir yapı kooperatifi bünyesinde; resmî kayıtlar T.C. Ticaret Bakanlığı'nın KOOPBİS sisteminde tutulur."],
 ["Banka kredisi gerekiyor mu?", "Hayır. Proje kendi tasarrufa dayalı ödeme modelini sunuyor; banka, faiz ve kefil devrede değil."],
 ["Konum gerçekten merkezi mi?", "D100 1 dakika, İzmit Sahili 2 dakika, 41 Burada AVM 3 dakika, şehir merkezi 5 dakika."],
 ["Yatırım için neden 1+0 / 1+1?", "Kompakt daireler daha geniş kiracı ve yatırımcı segmentine hitap eder; kiralama süresi kısalır, likidite artar."]]
.forEach((q, i) => {
  const y = 2.86 + i * 1.06;
  baslik(s, "“" + q[0] + "”", M, y, { w: 4.30, h: 0.72, boy: 16, satir: 1.06 });
  metin(s, q[1], M + 4.66, y + 0.02, { w: 6.78, h: 0.80, boy: 9.5 });
  if (i < 3) cizgi(s, M, y + 0.88, 11.44, KREM_K, 0.75);
});
metin(s, "Bilgilendirme amaçlıdır; yasal veya finansal garanti niteliği taşımaz. Belgeler satış ofisinden talep edilebilir.",
  M, 7.00, { w: 11.44, h: 0.28, boy: 8, italik: true, renk: "9A9082" });
s.addNotes("İlk soru en çok gelen soru. KOOPBİS'i telefonda canlı gösterin — en ikna edici hamle. Yasal ya da finansal garanti cümlesi KURMAYIN.");

/* ══════════════════════════════════════════════ 14 · GÜVEN VE ŞEFFAFLIK */
s = p.addSlide();
s.background = { color: GECE };
s.addImage({ path: fo("yar-guven"), x: W - 4.35, y: 0, w: 4.35, h: HT });
etiket(s, "KURUMSAL", M, 0.86, ALTIN);
baslik(s, "Satışta En Güçlü\nUnsur: Güven", M, 1.24,
  { w: 7.0, h: 1.6, boy: 36, renk: KREM, satir: 1.0 });
cizgi(s, M, 3.02, 1.30, ALTIN, 1.5);
[["S.S. Yahya Kaptan Birlik Yapı Kooperatifi", "Projeyi geliştiren yapı kooperatifi"],
 ["T.C. Ticaret Bakanlığı — KOOPBİS", "Kooperatif Bilgi Sistemi'nde kayıtlı"],
 ["1163 Sayılı Kooperatifler Kanunu", "Kuruluş, genel kurul ve denetim bu kanuna tabi"],
 ["Ocean Gayrimenkul", "Tek yetkili satıcı"]].forEach((g, i) => {
  const y = 3.36 + i * 0.82;
  cizgi(s, M, y + 0.17, 0.18, ALTIN, 1);
  baslik(s, g[0], M + 0.36, y - 0.04, { w: 7.0, h: 0.36, boy: 15, renk: KREM });
  metin(s, g[1], M + 0.36, y + 0.34, { w: 7.0, h: 0.28, boy: 9, renk: SIS });
});
blok(s, M, 6.50, 7.44, 0.62, KREM);
s.addImage({ path: mk("ykb-logo.png"), x: M + 0.80, y: 6.59, w: 0.44, h: 0.44 });
s.addImage({ path: mk("koopbis-logo.png"), x: M + 3.14, y: 6.65, w: 1.16, h: 0.36 });
s.addImage({ path: mk("ticaret-bakanligi-logo.webp"), x: M + 6.18, y: 6.59, w: 0.44, h: 0.44 });
metin(s, "Belgeler satış ofisinden talep edilebilir.", M, 7.22,
  { w: 7.44, h: 0.24, boy: 8, italik: true, renk: "6E7F8C" });
s.addNotes("Sade ve kurumsal anlatın. Emlakçının müşterisine karşı arkasında duracağı zemin bu slayt. Belgeleri gösterme sözü verin ve tutun.");

/* ═════════════════════════════════════════════════ 15 · PROJE GALERİSİ */
s = p.addSlide();
s.background = { color: GECE };
s.addImage({ path: fo("gal-1"), x: 0.00, y: 0.00, w: 7.07, h: 3.42 });
s.addImage({ path: fo("gal-2"), x: 7.15, y: 0.00, w: 3.05, h: 3.42 });
s.addImage({ path: fo("gal-3"), x: 10.28, y: 0.00, w: 3.05, h: 3.42 });
s.addImage({ path: fo("gal-4"), x: 0.00, y: 3.50, w: 3.05, h: 3.42 });
s.addImage({ path: fo("gal-5"), x: 3.13, y: 3.50, w: 3.05, h: 3.42 });
s.addImage({ path: fo("gal-6"), x: 6.26, y: 3.50, w: 7.07, h: 3.42 });
metin(s, "MİA PARK OCEAN  ·  PROJE GÖRSELLERİ", M, 7.06,
  { w: 6.0, boy: 8, aralik: 2.6, renk: ALTIN_A });
metin(s, "Görseller projenin kendi render'larıdır.", W - M - 5.0, 7.06,
  { w: 5.0, boy: 8, aralik: 1.2, hiza: "right", renk: "5C6B78" });
s.addNotes("Bu slaytta konuşmayın, bıraktırın. Gerekirse tek cümle: 'Bunların hepsi projenin kendi görselleri.' Sudaki öğeler süs havuzu.");

/* ═══════════════════════════════════════════════ 16 · EMLAKÇI İÇİN ÖZET */
s = p.addSlide();
s.background = { color: KREM };
etiket(s, "ÖZET", M, 0.86);
baslik(s, "Neden MİA PARK OCEAN?", M, 1.24, { w: 9.0, h: 0.9, boy: 38 });
cizgi(s, M, 2.42, 1.30, ALTIN, 1.5);
[["Merkezi Lokasyon", "D100'e 1 dk"], ["Gelişen MİA Bölgesi", "Yeni ticari aks"],
 ["472 Adet 1+0", "Kompakt stok"], ["112 Adet 1+1", "Dengeli ürün"],
 ["60 Ay Vade Farksız", "Banka, faiz, kefil yok"], ["Geniş Müşteri Profili", "Beş ayrı persona"]]
.forEach((o, i) => {
  const x = M + (i % 3) * 3.82, y = 2.88 + Math.floor(i / 3) * 1.10;
  cizgi(s, x, y, 3.44, ALTIN, 1);
  baslik(s, o[0], x, y + 0.16, { w: 3.44, h: 0.40, boy: 17 });
  metin(s, o[1], x, y + 0.60, { w: 3.44, h: 0.28, boy: 9.5, renk: KURSUN });
});
blok(s, 0, 5.42, W, 1.36, GECE);
baslik(s, "Doğru Konum.  Doğru Ürün.  Güçlü Satış Hikâyesi.", 0, 5.42,
  { w: W, h: 1.36, boy: 30, renk: KREM, hiza: "center", dikey: "middle" });
metin(s, "MİA PARK OCEAN  ·  İZMİT MİA BÖLGESİ  ·  OCEAN GAYRİMENKUL, TEK YETKİLİ SATICI",
  0, 7.00, { w: W, h: 0.30, boy: 8.5, aralik: 2.2, hiza: "center", renk: "9A9082" });
s.addNotes("Kapanıştan önce özet. Altı maddeyi tek tek okumayın; emlakçının aklında kalması gereken üç kelimeyi söyleyin: konum, ürün, hikâye.");

/* ═══════════════════════════════════════════════════════ 17 · KAPANIŞ */
s = p.addSlide();
zeminFoto(s, "tam-kapanis", "perde-kapanis");
s.addImage({ path: mk("brand/logo-ocean-white.png"), x: M, y: 0.80, w: 3.30, h: 2.26 });
cizgi(s, M, 3.42, 1.30, ALTIN, 1.5);
baslik(s, "İzmit'in Yeni Satış Fırsatını\nPortföyünüze Ekleyin.", M, 3.72,
  { w: 7.6, h: 1.6, boy: 33, renk: BEYAZ, satir: 1.04 });
[["0540 028 00 41   ·   0541 128 40 41"],
 ["info@oceangayrimenkul41.com"],
 ["miaparkocean.com"]].forEach((c, i) => {
  metin(s, c[0], M, 5.48 + i * 0.42, { w: 6.4, h: 0.34, boy: 12, renk: BEYAZ, kalin: i === 0 });
});
blok(s, W - M - 4.10, 5.42, 4.10, 0.86, ALTIN);
baslik(s, "Satış Ekibimizle İletişime Geçin", W - M - 4.10, 5.42,
  { w: 4.10, h: 0.86, boy: 16, renk: GECE, hiza: "center", dikey: "middle" });
metin(s, "OCEAN GAYRİMENKUL — TEK YETKİLİ SATICI", W - M - 4.10, 6.40,
  { w: 4.10, h: 0.28, boy: 8, aralik: 2.2, hiza: "center", renk: SIS });
metin(s, "S.S. Yahya Kaptan Birlik Yapı Kooperatifi", M, 6.94,
  { w: 6.4, h: 0.28, boy: 8.5, aralik: 1.6, renk: SIS });
s.addNotes("Kapanış: net çağrı yapın. Kayıt formunu dağıtın; bugün kaydolan emlakçıya katalog, görsel seti ve fiyat listesini akşam gönderin. Randevu almadan salondan çıkarmayın.");

p.writeFile({ fileName: path.join(KOK, "sunum", "MIA-PARK-OCEAN-Emlakci-Sunumu.pptx") })
  .then((f) => console.log("yazildi:", f));
