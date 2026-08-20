/**
 * MİA PARK OCEAN — emlakçı / broker sunumu (25 slayt, elmas dili).
 *
 * Referans şablonun görsel dili birebir: elmas (45° kare) içine kırpılmış
 * fotoğraflar, ince elmas çerçeveler, numaralı listeler, kesik çizgiyle
 * bağlanan adım diyagramları, köşe elmas süsleri. Renkler bizim:
 * gece lacivert · sıcak krem · champagne gold.
 *
 * Elmas ve çizgiler PowerPoint'in KENDİ vektör şekilleri (45° döndürülmüş
 * kare) — keskin ve düzenlenebilir. Yalnızca fotoğraf maskeleri, perdeler
 * ve ikonlar PIL'den geliyor (scripts/build-sunum-gorsel.py).
 *
 *   python3 scripts/build-sunum-gorsel.py    # görseller (önce bu)
 *   node    scripts/build-sunum.js           # sunum
 *
 * Fotoğraflar yerleşecekleri kutunun tam pikseline kırpılmış geliyor;
 * burada hiçbir görsel gerdirilmiyor.
 */
const pptxgen = require("pptxgenjs");
const path = require("path");

const KOK = path.join(__dirname, "..");
const KAYNAK = path.join(KOK, "sunum", "kaynak");
const fo = (n) => path.join(KAYNAK, "foto", n + ".jpg");
const sk = (n) => path.join(KAYNAK, "sekil", n + ".png");
const ka = (n) => path.join(KAYNAK, n + ".png");
const mk = (n) => path.join(KOK, "public", n);

/* ------------------------------------------------- palet (marka: okyanus) */
const GECE   = "04283A",   // marka laciverti — koyu zemin (siteyle aynı)
      LACI   = "0A3A55",   // lacivert blok
      KAGIT  = "F5FAFC",   // kâğıt beyazı — açık zemin
      KAGIT_K= "D9E7EE",   // açık ayırıcı
      VURGU  = "1A7496",   // okyanus — elmaslar, çizgiler, açık zeminde aksan (5.0:1)
      VURGU_A= "48ABC5",   // camgöbeği — koyu zeminde aksan (5.8:1)
      VURGU_K= "136178",   // ayırıcı bloklar üstünde koyu aksan (6.6:1)
      BEYAZ  = "FFFFFF",
      KURSUN = "47606E",   // açık zeminde ikincil metin (6.3:1)
      SIS    = "A9C9D8";   // koyu zeminde ikincil metin (8.8:1)

const F = "Montserrat";            // referans gibi tek sans aile
const W = 13.333, HT = 7.5;
const M = 0.90;                    // ortak kenar boşluğu

const p = new pptxgen();
p.layout = "LAYOUT_WIDE";
p.author = "Ocean Gayrimenkul";
p.company = "MİA PARK OCEAN";
p.title = "MİA PARK OCEAN — Emlakçı Sunumu";
p.subject = "İzmit MİA Bölgesi · Broker Presentation";

/* --------------------------------------------------------------- parçalar */
function blok(s, x, y, w, h, renk) {
  s.addShape(p.ShapeType.rect, { x, y, w, h, fill: { color: renk } });
}
function cizgi(s, x, y, w, renk, kalin, kesik) {
  s.addShape(p.ShapeType.line, { x, y, w, h: 0,
    line: { color: renk || VURGU, width: kalin || 1, dashType: kesik ? "dash" : "solid" } });
}
function dikey(s, x, y, h, renk, kalin) {
  s.addShape(p.ShapeType.line, { x, y, w: 0, h,
    line: { color: renk || KAGIT_K, width: kalin || 0.75 } });
}
/* elmas: 45° döndürülmüş kare. boy = köşeden köşeye genişlik (bbox). */
function elmasDolu(s, cx, cy, boy, renk) {
  const a = boy / Math.SQRT2;
  s.addShape(p.ShapeType.rect, { x: cx - a / 2, y: cy - a / 2, w: a, h: a,
    rotate: 45, fill: { color: renk } });
}
function elmasCizgi(s, cx, cy, boy, renk, kalin) {
  const a = boy / Math.SQRT2;
  s.addShape(p.ShapeType.rect, { x: cx - a / 2, y: cy - a / 2, w: a, h: a,
    rotate: 45, fill: { type: "none" }, line: { color: renk || VURGU, width: kalin || 1 } });
}
/* elmas fotoğraf + dış çerçeve elması */
function elmasFoto(s, ad, cx, cy, boy, cerceveRenk) {
  elmasCizgi(s, cx, cy, boy * 1.13, cerceveRenk || VURGU, 1);
  s.addImage({ path: sk(ad), x: cx - boy / 2, y: cy - boy / 2, w: boy, h: boy });
}
/* köşe süsü: bir dolu + bir çizgi elmas */
function kose(s, cx, cy, renkDolu, renkCizgi, k) {
  k = k || 1;
  elmasDolu(s, cx, cy, 0.30 * k, renkDolu || VURGU);
  elmasCizgi(s, cx + 0.42 * k, cy + 0.30 * k, 0.52 * k, renkCizgi || VURGU, 0.9);
}
function etiket(s, t, x, y, renk, w, boy) {
  s.addText(t, { x, y, w: w || 5.4, h: 0.26, fontFace: F, fontSize: boy || 10,
    bold: true, color: renk || VURGU, charSpacing: 3.2, margin: 0 });
}
function baslik(s, t, x, y, o) {
  o = o || {};
  s.addText(t, { x, y, w: o.w || 7.0, h: o.h || 0.9, fontFace: F,
    fontSize: o.boy || 30, color: o.renk || GECE, bold: true,
    align: o.hiza || "left", valign: o.dikeyH || "top",
    lineSpacingMultiple: o.satir || 1.04, charSpacing: o.aralik || 0.6, margin: 0 });
}
function metin(s, t, x, y, o) {
  o = o || {};
  s.addText(t, { x, y, w: o.w || 5.0, h: o.h || 0.6, fontFace: F,
    fontSize: o.boy || 10.5, color: o.renk || KURSUN, bold: !!o.kalin,
    italic: !!o.italik, align: o.hiza || "left", valign: o.dikeyH || "top",
    lineSpacingMultiple: o.satir || 1.30, charSpacing: o.aralik || 0, margin: 0 });
}
function rakam(s, t, x, y, o) {
  o = o || {};
  s.addText(t, { x, y, w: o.w || 3.0, h: o.h || 1.0, fontFace: F,
    fontSize: o.boy || 44, bold: true, color: o.renk || GECE,
    align: o.hiza || "left", valign: "bottom", margin: 0 });
}
/* numara rozeti: dolu elmas + beyaz numara */
function noElmas(s, cx, cy, n, renk, boy) {
  elmasDolu(s, cx, cy, boy || 0.52, renk || VURGU);
  s.addText(String(n), { x: cx - 0.35, y: cy - 0.22, w: 0.7, h: 0.44, align: "center",
    valign: "middle", fontFace: F, fontSize: 11, bold: true, color: BEYAZ, margin: 0 });
}
/* ikon karesi: ince çerçeve + ikon */
function ikonKare(s, ad, x, y, boy, renk) {
  s.addShape(p.ShapeType.rect, { x, y, w: boy, h: boy, fill: { type: "none" },
    line: { color: renk || VURGU, width: 1 } });
  s.addImage({ path: sk(ad), x: x + boy * 0.16, y: y + boy * 0.16,
    w: boy * 0.68, h: boy * 0.68 });
}
/* adım elması: çerçeve + dolu lacivert elmas + beyaz ikon */
function adimElmas(s, cx, cy, boy, ikonAd, koyuZemin) {
  elmasCizgi(s, cx, cy, boy, VURGU, 1);
  elmasDolu(s, cx, cy, boy * 0.80, koyuZemin ? LACI : GECE);
  const ib = boy * 0.34;
  s.addImage({ path: sk(ikonAd), x: cx - ib / 2, y: cy - ib / 2, w: ib, h: ib });
}
function kunye(s, koyu, sagSinir) {
  const renk = koyu ? "7E9AAB" : KURSUN;
  metin(s, "MİA PARK OCEAN  ·  İZMİT MİA BÖLGESİ", M, 7.04,
    { w: 6.0, boy: 7.5, aralik: 2.2, renk });
  const sag = sagSinir || (W - M);
  if (sag > 9.6) {
    metin(s, "OCEAN GAYRİMENKUL — TEK YETKİLİ SATICI", sag - 5.2, 7.04,
      { w: 5.2, boy: 7.5, aralik: 2.2, hiza: "right", renk });
  }
}

let s;

/* ════════════════════════════════════════════════════════ 1 · KAPAK */
s = p.addSlide();
s.background = { color: KAGIT };
/* sağda elmas kümesi (referans kapağı) */
elmasCizgi(s, 9.55, 2.62, 4.55, VURGU, 1);
elmasFoto(s, "e-kapak1", 9.75, 2.48, 3.80);
elmasFoto(s, "e-kapak2", 7.45, 5.05, 2.55);
elmasDolu(s, 11.85, 4.98, 1.15, GECE);
elmasDolu(s, 6.62, 3.28, 0.46, VURGU);
elmasCizgi(s, 12.25, 1.05, 0.85, VURGU, 0.9);
kose(s, 12.55, 6.85, VURGU, GECE, 1);
/* sol içerik */
s.addImage({ path: mk("brand/logo-ocean-trim.png"), x: M, y: 0.72, w: 1.95, h: 1.34 });
etiket(s, "OCEAN GAYRİMENKUL — TEK YETKİLİ SATICI", M, 2.55, KURSUN, 5.6, 8.5);
baslik(s, "MİA PARK\nOCEAN", M, 2.95, { w: 6.0, h: 2.0, boy: 54, satir: 0.98, aralik: 1 });
cizgi(s, M, 5.10, 1.30, VURGU, 1.5);
metin(s, "İZMİT MİA BÖLGESİ", M, 5.28, { w: 5.0, boy: 12, kalin: true, aralik: 3.0, renk: GECE });
metin(s, "Emlakçılar için yeni bir satış fırsatı", M, 5.66,
  { w: 5.4, boy: 12.5, renk: KURSUN });
blok(s, M, 6.28, 3.55, 0.52, GECE);
metin(s, "21 AĞUSTOS 2026  ·  EMEX OTEL, KOCAELİ", M + 0.22, 6.28,
  { w: 3.2, h: 0.52, boy: 8.5, kalin: true, aralik: 1.4, renk: VURGU_A, dikeyH: "middle" });
s.addNotes("Açılış. Kendinizi ve Ocean Gayrimenkul'ü tanıtın. Bu sunum bir konut kataloğu değil; bugün emlakçıya 'bu projeyi neden portföyüne almalı' sorusunun cevabını veriyoruz. Süre 25 dakika, sonrasında soru-cevap.");

/* ════════════════════════════════════════════════════════ 2 · GÜNDEM */
s = p.addSlide();
s.background = { color: GECE };
s.addImage({ path: fo("r-gundem"), x: 0, y: 0, w: 6.0, h: HT });
elmasCizgi(s, 3.0, 3.75, 4.6, VURGU, 1.2);
elmasDolu(s, 0.85, 6.6, 0.5, VURGU);
blok(s, 5.35, 0.72, 1.30, 0.52, VURGU);
metin(s, "2026", 5.35, 0.72, { w: 1.30, h: 0.52, boy: 13, kalin: true, hiza: "center",
  dikeyH: "middle", renk: BEYAZ, aralik: 1.5 });
etiket(s, "GÜNDEM", 6.85, 0.86, VURGU);
baslik(s, "BUGÜN NELER\nKONUŞACAĞIZ?", 6.85, 1.22, { w: 5.6, h: 1.5, boy: 30, renk: KAGIT });
[["Proje Özeti", "01"], ["Konum ve MİA Bölgesi", "02"], ["Mimari ve Yaşam", "03"],
 ["Ürün Dağılımı", "04"], ["Ödeme Modeli", "05"], ["Müşteri Profilleri", "06"],
 ["Satış Süreci ve İş Birliği", "07"], ["Güven ve İletişim", "08"]].forEach((g, i) => {
  const y = 3.06 + i * 0.50;
  noElmas(s, 7.12, y + 0.17, g[1], VURGU, 0.40);
  metin(s, g[0], 7.55, y, { w: 4.8, h: 0.36, boy: 12, kalin: true, renk: KAGIT, dikeyH: "middle" });
});
s.addNotes("Gündemi hızlı geçin. Vurgu 5. ve 7. başlıkta: ödeme modeli ve iş birliği. Emlakçı bu ikisini anlarsa gerisi kolay.");

/* ═══════════════════════════════════════════════════ 3 · PROJE ÖZETİ */
s = p.addSlide();
s.background = { color: KAGIT };
etiket(s, "PROJE ÖZETİ", M, 0.86);
baslik(s, "MİA PARK OCEAN NEDİR?", M, 1.22, { w: 7.4, boy: 30 });
cizgi(s, M, 2.18, 1.30, VURGU, 1.5);
[["600", "KONUT", "İzmit MİA Bölgesi'nde tek etapta"],
 ["584", "1+0 VE 1+1 STOK", "Satışın omurgası kompakt segment"],
 ["60 AY", "VADE FARKSIZ", "Banka yok, faiz yok, kefil yok"],
 ["%30", "PEŞİNAT", "Kalan tutar 60 aya kadar taksit"]].forEach((k, i) => {
  const x = M + (i % 2) * 3.45, y = 2.62 + Math.floor(i / 2) * 1.72;
  rakam(s, k[0], x, y, { w: 3.1, h: 0.78, boy: 36 });
  metin(s, k[1], x, y + 0.84, { w: 3.1, h: 0.26, boy: 8.5, kalin: true, aralik: 2.0, renk: VURGU });
  metin(s, k[2], x, y + 1.10, { w: 3.1, h: 0.28, boy: 9, renk: KURSUN });
  cizgi(s, x, y + 1.48, 3.0, KAGIT_K, 0.75);
});
metin(s, "MİA PARK OCEAN, İzmit'in gelişen merkezi iş alanında konumlanan; yatırım ve yaşam talebini aynı noktada buluşturan modern konut projesidir.",
  M, 6.28, { w: 6.9, h: 0.6, boy: 10.5, italik: true, renk: KURSUN });
elmasFoto(s, "e-ozet", 10.35, 3.55, 4.00);
elmasDolu(s, 12.55, 5.75, 0.52, VURGU);
elmasCizgi(s, 8.30, 1.35, 0.72, VURGU, 0.9);
kunye(s, true);
s.addNotes("Projeyi 30 saniyede anlatın: 600 konut, MİA Bölgesi, 60 aya kadar vade farksız, %30 peşinat. Emlakçı bu dört rakamı aklında tutsun.");

/* ══════════════════════════════ 4 · EMLAKÇI İÇİN NEDEN ÖNEMLİ */
s = p.addSlide();
s.background = { color: KAGIT };
etiket(s, "PORTFÖY DEĞERLENDİRMESİ", M, 0.86);
baslik(s, "SATILMASI KOLAY BİR ÜRÜN\nNEDEN OLUŞUR?", M, 1.22, { w: 7.2, h: 1.5, boy: 26 });
cizgi(s, M, 2.78, 1.30, VURGU, 1.5);
[["i-pin-vurgu", "Merkezi lokasyon", "Müşteriye konumu anlatmak kolay; dakika bazlı mesafeler tek cümlede aktarılır."],
 ["i-ev-vurgu", "Kompakt daire seçenekleri", "Daha geniş yatırımcı kitlesine hitap eder; giriş bütçesi düşer, talep genişler."],
 ["i-takvim-vurgu", "Uzun vadeli ödeme", "Alıcının giriş bariyerini azaltır; kredisi çıkmayan müşteri portföyde kalır."],
 ["i-grafik-vurgu", "Güçlü proje görselliği", "Sunum ve dijital satışta yüksek algı oluşturur; materyal hazır gelir."]]
.forEach((k, i) => {
  const y = 3.12 + i * 0.94;
  ikonKare(s, k[0], M, y, 0.56);
  metin(s, k[1], M + 0.82, y - 0.02, { w: 5.6, h: 0.30, boy: 12.5, kalin: true, renk: GECE });
  metin(s, k[2], M + 0.82, y + 0.30, { w: 6.2, h: 0.50, boy: 9.5, renk: KURSUN });
});
elmasFoto(s, "e-neden", 10.55, 3.30, 3.90);
elmasDolu(s, 8.55, 5.42, 0.44, GECE);
elmasCizgi(s, 12.45, 1.25, 0.72, VURGU, 0.9);
metin(s, "İyi proje yalnızca güzel değildir; doğru müşteriye kolay anlatılabilir.",
  8.20, 6.20, { w: 4.6, h: 0.55, boy: 10, italik: true, hiza: "center", renk: KURSUN });
kunye(s, true);
s.addNotes("Bu slayt sunumun tezi. Emlakçı 'güzel proje' duymaktan sıkılmıştır; ona satılabilirlik argümanı verin.");

/* ═══════════════════════════════════════════════════════ 5 · KONUM */
s = p.addSlide();
s.background = { color: KAGIT };
s.addImage({ path: fo("r-konum"), x: 0, y: 0, w: 5.0, h: HT });
elmasCizgi(s, 2.5, 3.75, 3.8, VURGU, 1.2);
elmasDolu(s, 4.62, 0.80, 0.44, VURGU);
etiket(s, "KONUM", 5.75, 0.86);
baslik(s, "HER YERE\nDAKİKALAR İÇİNDE", 5.75, 1.22, { w: 6.7, h: 1.5, boy: 26 });
cizgi(s, 5.75, 2.78, 1.30, VURGU, 1.5);
[["D100 Karayolu", "1 DK"], ["İzmit Sahili", "2 DK"], ["41 Burada AVM", "3 DK"],
 ["Şehir Merkezi", "5 DK"], ["Şehir Hastanesi", "5 DK"], ["TEM Otoyolu", "5 DK"],
 ["Symbol AVM", "7 DK"], ["Kocaeli Üniversitesi", "10 DK"]].forEach((d, i) => {
  const y = 3.10 + i * 0.44;
  elmasDolu(s, 5.90, y + 0.15, 0.16, VURGU);
  metin(s, d[0], 6.18, y, { w: 4.2, h: 0.32, boy: 11, renk: GECE, dikeyH: "middle" });
  metin(s, d[1], 10.60, y, { w: 1.8, h: 0.32, boy: 12, kalin: true, hiza: "right",
    renk: VURGU, dikeyH: "middle", aralik: 1 });
  if (i < 7) cizgi(s, 5.90, y + 0.42, 6.50, KAGIT_K, 0.5);
});
metin(s, "Günlük yaşam, ulaşım, sağlık, eğitim ve alışveriş birkaç dakikalık erişim alanında.",
  5.75, 6.72, { w: 6.6, h: 0.30, boy: 9, italik: true, renk: KURSUN });
s.addNotes("Mesafeleri ezberleyin; en çok D100 ve şehir hastanesi sorulur. İzmit Sahili süresi teyide açık, kesin konuşmayın.");

/* ══════════════════════════════════════════════ 6 · MİA BÖLGESİ NEDİR */
s = p.addSlide();
s.background = { color: KAGIT };
blok(s, 0, 0, 5.30, HT, GECE);
etiket(s, "BÖLGE", M, 0.86, VURGU);
baslik(s, "MİA NEDEN\nÖNEMLİ?", M, 1.22, { w: 3.9, h: 1.6, boy: 30, renk: KAGIT });
cizgi(s, M, 2.92, 1.30, VURGU, 1.5);
metin(s, "MİA, Merkezi İş Alanı demektir: bir şehrin ofis, ticaret ve hizmet fonksiyonlarının yoğunlaşması için planlanan bölge.",
  M, 3.22, { w: 3.6, h: 1.0, boy: 10.5, renk: SIS, satir: 1.45 });
elmasFoto(s, "e-mia", 3.65, 5.95, 2.00);
elmasDolu(s, 1.35, 5.35, 0.4, VURGU);
[["01", "Yeni ticari merkez", "Ofis, ticaret ve hizmet fonksiyonlarının yoğunlaşacağı bölge."],
 ["02", "Yeni yaşam aksı", "Yeni konut ve karma kullanımlı projelerin geliştiği bölge."],
 ["03", "Değerlenme potansiyeli", "Altyapı ve ticari hareketlilik arttıkça bölgenin yatırım çekiciliği artar."]]
.forEach((k, i) => {
  const y = 1.30 + i * 1.66;
  rakam(s, k[0], 5.95, y, { w: 1.0, h: 0.62, boy: 26, renk: VURGU });
  metin(s, k[1], 7.10, y + 0.06, { w: 5.2, h: 0.34, boy: 14, kalin: true, renk: GECE });
  metin(s, k[2], 7.10, y + 0.46, { w: 5.2, h: 0.60, boy: 10, renk: KURSUN });
  if (i < 2) cizgi(s, 5.95, y + 1.30, 6.45, KAGIT_K, 0.75);
});
kose(s, 12.45, 6.55, VURGU, VURGU, 0.9);
metin(s, "Bölgesel gelişim bir potansiyeldir; değer artışı taahhüdü değildir.",
  5.95, 6.70, { w: 6.4, h: 0.28, boy: 8.5, italik: true, renk: KURSUN });
s.addNotes("MİA kısaltmasını mutlaka açın. DİKKAT: 'kesin değer artışı' demeyin; 'potansiyel', 'gelişim aksı', 'yatırım çekiciliği' deyin.");

/* ═══════════════════════════════ 7 · STRATEJİK AVANTAJ (AKS) */
s = p.addSlide();
s.background = { color: KAGIT };
etiket(s, "PAZAR", M, 0.86);
baslik(s, "İSTANBUL'A YAKIN, İZMİT'İN MERKEZİNDE", M, 1.22, { w: 11.5, boy: 26 });
cizgi(s, M, 2.10, 1.30, VURGU, 1.5);
blok(s, M, 2.48, 5.55, 1.85, GECE);
etiket(s, "İZMİT YATIRIMCISI İÇİN", M + 0.40, 2.82, VURGU_A, 4.6, 8.5);
metin(s, "Şehrin gelişen yeni merkezinde konum", M + 0.40, 3.16,
  { w: 4.8, h: 0.8, boy: 15, kalin: true, renk: KAGIT, satir: 1.2 });
blok(s, 6.88, 2.48, 5.55, 1.85, KAGIT_K);
etiket(s, "İSTANBUL YATIRIMCISI İÇİN", 7.28, 2.82, VURGU_K, 4.6, 8.5);
metin(s, "Anadolu Yakası'na kıyasla erişilebilir bütçeyle konut", 7.28, 3.16,
  { w: 4.8, h: 0.8, boy: 15, kalin: true, renk: GECE, satir: 1.2 });
/* ulaşım aksı: kesik çizgi + elmas duraklar */
const AY = 5.55;
cizgi(s, M + 0.3, AY, 11.25, VURGU, 1.25, true);
elmasDolu(s, M + 0.55, AY, 0.30, GECE);
elmasCizgi(s, 7.05, AY, 0.62, VURGU, 1.2);
elmasDolu(s, 7.05, AY, 0.36, VURGU);
elmasDolu(s, 12.10, AY, 0.30, GECE);
metin(s, "İSTANBUL ANADOLU YAKASI", M - 0.20, AY + 0.32, { w: 2.6, h: 0.3, boy: 8.5,
  kalin: true, renk: GECE, aralik: 1 });
metin(s, "MİA PARK OCEAN · İZMİT", 5.75, AY - 0.66, { w: 2.6, h: 0.3, boy: 9,
  kalin: true, hiza: "center", renk: GECE, aralik: 1 });
metin(s, "SAKARYA", 11.15, AY + 0.32, { w: 1.4, h: 0.3, boy: 8.5, kalin: true,
  hiza: "right", renk: GECE, aralik: 1 });
metin(s, "yaklaşık 1,5–2 saat", 2.90, AY - 0.40, { w: 2.6, h: 0.26, boy: 9, italik: true,
  hiza: "center", renk: KURSUN });
metin(s, "yaklaşık 45–60 dakika", 8.60, AY - 0.40, { w: 2.6, h: 0.26, boy: 9, italik: true,
  hiza: "center", renk: KURSUN });
metin(s, "Proje yalnız İzmit'e değil; İstanbul ve Sakarya'dan gelen Marmara yatırımcısına da hitap eder.",
  M, 6.60, { w: 11.5, h: 0.32, boy: 10.5, italik: true, hiza: "center", renk: KURSUN });
s.addNotes("İki yönlü anlatı: İzmit yatırımcısına merkeziyet, İstanbul yatırımcısına bütçe. Marmara yatırımcısı ikinci müşteri havuzu.");

/* ═══════════════════════════════════════════════════════ 8 · MİMARİ */
s = p.addSlide();
s.addImage({ path: fo("tam-mimari"), x: 0, y: 0, w: W, h: HT });
s.addImage({ path: ka("perde-mimari"), x: 0, y: 0, w: W, h: HT });
etiket(s, "MİMARİ", M, 4.30, VURGU_A);
baslik(s, "MODERN VE\nZAMANSIZ MİMARİ", M, 4.66, { w: 5.4, h: 1.5, boy: 28, renk: BEYAZ });
cizgi(s, M, 6.36, 1.30, VURGU, 1.5);
["Modern cephe dili", "Geniş peyzaj alanları", "Süs havuzu ve su aksları",
 "Düzenli site içi ulaşım", "Balkonlu daireler", "Güvenlikli site yaklaşımı"]
.forEach((o, i) => {
  const x = 7.05 + (i % 2) * 3.00, y = 4.72 + Math.floor(i / 2) * 0.52;
  elmasDolu(s, x + 0.08, y + 0.15, 0.15, VURGU);
  metin(s, o, x + 0.30, y, { w: 2.68, h: 0.30, boy: 10, renk: BEYAZ, dikeyH: "middle" });
});
metin(s, "Projedeki su öğeleri peyzaj amaçlı süs havuzu ve su akslarıdır.",
  7.05, 6.44, { w: 5.4, h: 0.26, boy: 8.5, italik: true, renk: SIS });
s.addNotes("DİKKAT: Projede yüzme havuzu YOK. Sudaki öğeler peyzaj amaçlı süs havuzu ve su aksı.");

/* ═══════════════════════════════════════════ 9 · SİTE İÇİNDE YAŞAM */
s = p.addSlide();
s.background = { color: KAGIT };
etiket(s, "SİTE KONSEPTİ", M, 0.86);
baslik(s, "MERKEZİ AVLU ÇEVRESİNDE YAŞAM", M, 1.22, { w: 10.4, boy: 26 });
cizgi(s, M, 2.10, 1.30, VURGU, 1.5);
["Merkezi avlu", "Süs havuzları ve su aksları", "Geniş peyzaj alanları",
 "Yürüyüş ve dinlenme yolları", "Çocuk oyun alanı", "Kapalı otopark",
 "7/24 güvenlik", "Gün ışığı odaklı cepheler"].forEach((o, i) => {
  const x = M + (i % 2) * 3.62, y = 2.56 + Math.floor(i / 2) * 0.56;
  elmasDolu(s, x + 0.08, y + 0.16, 0.16, VURGU);
  metin(s, o, x + 0.32, y, { w: 3.2, h: 0.34, boy: 11, renk: GECE, dikeyH: "middle" });
});
blok(s, M, 5.02, 7.15, 0.70, GECE);
s.addImage({ path: sk("i-kalkan-beyaz"), x: M + 0.22, y: 5.18, w: 0.38, h: 0.38 });
metin(s, "Avludaki su SÜS havuzudur — yüzme havuzu diye anlatmayın.",
  M + 0.75, 5.02, { w: 6.2, h: 0.70, boy: 11, kalin: true, renk: VURGU_A, dikeyH: "middle" });
s.addImage({ path: fo("ya-1"), x: 8.42, y: 2.42, w: 3.55, h: 2.25 });
s.addImage({ path: fo("ya-2"), x: 8.42, y: 4.82, w: 3.55, h: 2.25 });
elmasCizgi(s, 8.42, 2.42, 0.85, VURGU, 1);
kose(s, 12.35, 1.35, VURGU, VURGU, 0.8);
kunye(s, true, 8.3);
s.addNotes("ÖNEMLİ: Süs havuzu ile yüzme havuzunu karıştırmayın. Yüzme havuzu sözü verilirse teslimde sorun çıkar.");

/* ═══════════════════════════════════════════ 10 · ÜRÜN DAĞILIMI */
s = p.addSlide();
s.background = { color: KAGIT };
etiket(s, "ÜRÜN", M, 0.86);
baslik(s, "SATIŞIN OMURGASI: 1+0 VE 1+1", M, 1.22, { w: 10.0, boy: 26 });
cizgi(s, M, 2.10, 1.30, VURGU, 1.5);
[["urun-1plus0", "1+0", "472", "Yatırım, kiralama ve kompakt yaşam talebine yönelik güçlü stok."],
 ["urun-1plus1", "1+1", "112", "Tek kişi, çiftler ve yatırımcı müşteriler için dengeli ürün."]]
.forEach((u, i) => {
  const x = M + i * 5.80;
  s.addImage({ path: fo(u[0]), x, y: 2.52, w: 5.30, h: 2.40 });
  blok(s, x, 4.92, 5.30, 1.52, i ? LACI : GECE);
  elmasDolu(s, x + 0.62, 5.42, 0.72, VURGU);
  metin(s, u[1], x + 0.62 - 0.5, 5.42 - 0.22, { w: 1.0, h: 0.44, boy: 14, kalin: true,
    hiza: "center", renk: BEYAZ, dikeyH: "middle" });
  metin(s, "ADET", x + 2.45, 5.06, { w: 2.5, h: 0.24, boy: 8, aralik: 2.4, hiza: "right", renk: VURGU_A });
  rakam(s, u[2], x + 2.45, 5.20, { w: 2.5, h: 0.62, boy: 34, renk: KAGIT, hiza: "right" });
  metin(s, u[3], x + 0.30, 5.94, { w: 4.7, h: 0.44, boy: 9, renk: SIS });
});
metin(s, "Projenin ana satış gücü kompakt daire segmentidir.", M, 6.68,
  { w: 11.5, h: 0.30, boy: 10.5, italik: true, hiza: "center", renk: KURSUN });
s.addNotes("584 dairenin ikisi de kompakt: çok geniş bir müşteri havuzuna satarsınız. Bu sunumda 2+1'den söz etmiyoruz.");

/* ══════════════════════════════════════════════════ 11 · 1+0 DETAY */
s = p.addSlide();
s.background = { color: KAGIT };
s.addImage({ path: fo("r-1plus0"), x: 0, y: 0, w: 5.60, h: HT });
elmasCizgi(s, 2.8, 3.75, 4.0, VURGU, 1.2);
blok(s, 4.55, 0.72, 1.55, 0.55, GECE);
metin(s, "1+0", 4.55, 0.72, { w: 1.55, h: 0.55, boy: 15, kalin: true, hiza: "center",
  dikeyH: "middle", renk: VURGU, aralik: 2 });
etiket(s, "ÜRÜN DETAYI", 6.35, 0.86);
baslik(s, "1+0 — YATIRIMIN\nKOMPAKT YÜZÜ", 6.35, 1.22, { w: 6.1, h: 1.5, boy: 26 });
cizgi(s, 6.35, 2.78, 1.30, VURGU, 1.5);
[["Brüt 28 m²", "Verimli plan; her metrekare kullanımda."],
 ["472 adet", "Projenin en derin stoğu — sürekli satış imkânı."],
 ["Yatırım odaklı", "Kiralama talebi güçlü, likiditesi yüksek segment."],
 ["Hedef müşteri", "Genç profesyonel, öğrenci velisi, kira geliri arayan yatırımcı."]]
.forEach((k, i) => {
  const y = 3.14 + i * 0.86;
  noElmas(s, 6.55, y + 0.16, "0" + (i + 1), VURGU, 0.42);
  metin(s, k[0], 7.02, y - 0.02, { w: 1.95, h: 0.32, boy: 12.5, kalin: true, renk: GECE });
  metin(s, k[1], 9.10, y - 0.02, { w: 3.3, h: 0.64, boy: 9.5, renk: KURSUN });
  if (i < 3) cizgi(s, 6.35, y + 0.66, 6.05, KAGIT_K, 0.6);
});
metin(s, "Kompakt daire, geniş kiracı havuzu demektir: kiralama süresi kısalır, boş kalma riski düşer.",
  6.35, 6.62, { w: 6.05, h: 0.5, boy: 9.5, italik: true, renk: KURSUN });
s.addNotes("1+0 anlatırken metrekareyi savunmayın, kiracı havuzunu anlatın. 472 adet: emlakçı için bitmeyen stok.");

/* ══════════════════════════════════════════════════ 12 · 1+1 DETAY */
s = p.addSlide();
s.background = { color: KAGIT };
s.addImage({ path: fo("r-1plus1"), x: W - 5.60, y: 0, w: 5.60, h: HT });
elmasCizgi(s, W - 2.8, 3.75, 4.0, VURGU, 1.2);
blok(s, W - 6.10, 0.72, 1.55, 0.55, GECE);
metin(s, "1+1", W - 6.10, 0.72, { w: 1.55, h: 0.55, boy: 15, kalin: true, hiza: "center",
  dikeyH: "middle", renk: VURGU, aralik: 2 });
etiket(s, "ÜRÜN DETAYI", M, 0.86);
baslik(s, "1+1 — DENGELİ\nYAŞAM ÜRÜNÜ", M, 1.22, { w: 6.1, h: 1.5, boy: 26 });
cizgi(s, M, 2.78, 1.30, VURGU, 1.5);
[["Brüt 50 m²", "Yaşam alanı ile yatak odası ayrışır; konfor artar."],
 ["112 adet", "Talebi dengeleyen, kıtlığı hissedilen stok."],
 ["Çift ve küçük aile", "Oturum amaçlı alıcının ilk tercihi."],
 ["Kiracı profili", "Çalışan çiftler ve profesyoneller; istikrarlı kira."]]
.forEach((k, i) => {
  const y = 3.14 + i * 0.86;
  noElmas(s, M + 0.20, y + 0.16, "0" + (i + 1), VURGU, 0.42);
  metin(s, k[0], M + 0.67, y - 0.02, { w: 1.95, h: 0.32, boy: 12.5, kalin: true, renk: GECE });
  metin(s, k[1], M + 2.75, y - 0.02, { w: 3.3, h: 0.64, boy: 9.5, renk: KURSUN });
  if (i < 3) cizgi(s, M, y + 0.66, 6.05, KAGIT_K, 0.6);
});
metin(s, "1+0'dan taşınan kiracının doğal adresi: site içinde yükselme merdiveni kurar.",
  M, 6.62, { w: 6.05, h: 0.5, boy: 9.5, italik: true, renk: KURSUN });
s.addNotes("1+1'i 'bir üst adım' olarak konumlayın: hem oturum alıcısı hem yatırımcı için dengeli ürün.");

/* ══════════════════════════════════════════ 13 · MÜŞTERİ PROFİLLERİ */
s = p.addSlide();
s.background = { color: KAGIT };
etiket(s, "HEDEF KİTLE", M, 0.86);
baslik(s, "BU PROJEYİ KİME\nSATABİLİRSİNİZ?", M, 1.22, { w: 7.0, h: 1.5, boy: 26 });
cizgi(s, M, 2.78, 1.30, VURGU, 1.5);
[["İlk kez konut alanlar", "Düşük başlangıç bariyeri arayanlar"],
 ["Yatırımcılar", "Kiralama potansiyeli olan kompakt konut arayanlar"],
 ["İstanbul yatırımcıları", "İstanbul dışında alternatif arayanlar"],
 ["Çalışan profesyoneller", "Merkezi ve ulaşımı kolay daire isteyenler"],
 ["Üniversiteli aileleri", "Kocaeli Üniversitesi'ne yakınlık arayanlar"]]
.forEach((k, i) => {
  const y = 3.10 + i * 0.74;
  noElmas(s, M + 0.20, y + 0.16, "0" + (i + 1), VURGU, 0.42);
  metin(s, k[0], M + 0.68, y, { w: 3.05, h: 0.34, boy: 12.5, kalin: true, renk: GECE, dikeyH: "middle" });
  metin(s, k[1], M + 3.85, y, { w: 3.60, h: 0.34, boy: 9.5, renk: KURSUN, dikeyH: "middle" });
  if (i < 4) cizgi(s, M, y + 0.56, 7.0, KAGIT_K, 0.6);
});
elmasFoto(s, "e-profil", 10.60, 3.60, 3.70);
elmasDolu(s, 8.75, 5.55, 0.44, VURGU);
elmasCizgi(s, 12.50, 1.30, 0.72, VURGU, 0.9);
metin(s, "Reddedilen kredi başvurusu burada satışa dönüyor.", 8.55, 6.10,
  { w: 4.2, h: 0.55, boy: 10, italik: true, hiza: "center", renk: KURSUN });
kunye(s, true);
s.addNotes("Beş profili okurken emlakçıya sorun: portföyünüzde böyle kaç müşteri var? Salonda isim çıkarsa satış başlamıştır.");

/* ═══════════════════════════════════════════════ 14 · ÖDEME MODELİ */
s = p.addSlide();
s.background = { color: GECE };
s.addImage({ path: fo("r-odeme"), x: W - 4.60, y: 0, w: 4.60, h: HT });
elmasCizgi(s, W - 2.3, 3.75, 3.4, VURGU, 1.2);
etiket(s, "FİNANSMAN", M, 0.86, VURGU);
baslik(s, "ALICININ ÖNÜNDEKİ ENGELİ\nAZALTAN ÖDEME MODELİ", M, 1.22,
  { w: 7.4, h: 1.5, boy: 25, renk: KAGIT });
cizgi(s, M, 2.80, 1.30, VURGU, 1.5);
[["%30", "PEŞİNAT"], ["60 AY", "VADE FARKSIZ"]].forEach((k, i) => {
  const x = M + i * 3.80;
  rakam(s, k[0], x, 3.20, { w: 3.4, h: 1.05, boy: 54, renk: VURGU });
  metin(s, k[1], x, 4.34, { w: 3.4, h: 0.28, boy: 9.5, kalin: true, aralik: 2.6, renk: SIS });
});
blok(s, M, 4.98, 7.45, 0.74, LACI);
metin(s, "BANKA YOK   ·   FAİZ YOK   ·   KEFİL YOK", M, 4.98,
  { w: 7.45, h: 0.74, boy: 16, kalin: true, hiza: "center", dikeyH: "middle",
    renk: VURGU, aralik: 1.6 });
metin(s, "Tasarrufa dayalı finansman yaklaşımı sayesinde konut alımında banka kredisine alternatif bir ödeme modeli sunulur.",
  M, 6.02, { w: 7.3, h: 0.6, boy: 10.5, renk: SIS, satir: 1.4 });
kunye(s, false, 8.6);
s.addNotes("Sunumun en güçlü slaydı. Tek cümle: bankaya gitmeden, faiz ödemeden, kefil bulmadan ev. Kredisi çıkmayan müşteri artık kayıp değil.");

/* ═══════════════════════════════════════════════ 15 · FİYAT ÖRNEĞİ */
s = p.addSlide();
s.background = { color: KAGIT };
etiket(s, "ÖRNEK ÖDEME", M, 0.86);
baslik(s, "BUGÜNKÜ ÖDEME ÖRNEKLERİ", M, 1.22, { w: 9.4, boy: 26 });
cizgi(s, M, 2.10, 1.30, VURGU, 1.5);
[["1+0", "699.000 TL", "29.900 TL"], ["1+1", "999.000 TL", "39.900 TL"]].forEach((f, i) => {
  const x = M + i * 5.80;
  blok(s, x, 2.50, 5.30, 3.30, i ? LACI : GECE);
  elmasDolu(s, x + 0.78, 3.16, 0.82, VURGU);
  metin(s, f[0], x + 0.28, 2.94, { w: 1.0, h: 0.44, boy: 15, kalin: true, hiza: "center",
    dikeyH: "middle", renk: BEYAZ });
  cizgi(s, x + 1.55, 3.16, 3.35, "2A5B77", 0.75);
  metin(s, "PEŞİNAT", x + 0.42, 3.78, { w: 2.4, h: 0.24, boy: 8.5, aralik: 2.4, renk: SIS });
  metin(s, f[1], x + 0.42, 4.04, { w: 4.4, h: 0.52, boy: 24, kalin: true, renk: KAGIT });
  metin(s, "AYLIK", x + 0.42, 4.72, { w: 2.4, h: 0.24, boy: 8.5, aralik: 2.4, renk: SIS });
  metin(s, f[2], x + 0.42, 4.98, { w: 4.4, h: 0.46, boy: 19, kalin: true, renk: VURGU_A });
});
blok(s, M, 6.06, 11.53, 0.60, KAGIT_K);
metin(s, "60 AY  ·  VADE FARKSIZ", M, 6.06, { w: 11.53, h: 0.60, boy: 14, kalin: true,
  hiza: "center", dikeyH: "middle", renk: VURGU_K, aralik: 2.2 });
metin(s, "Fiyatlar ve kampanya koşulları dönemsel olarak değişebilir. Güncel bilgi için satış ofisiyle iletişime geçiniz.",
  M, 6.86, { w: 11.53, h: 0.28, boy: 8, italik: true, hiza: "center", renk: KURSUN });
s.addNotes("Rakamları verirken mutlaka dipnotu söyleyin: fiyat ve kampanya koşulları dönemseldir. Yazılı teklif satış ofisinden çıkar.");

/* ══════════════════════════════ 16 · MÜŞTERİ SÜRECİ (4 ADIM) */
s = p.addSlide();
s.background = { color: KAGIT };
etiket(s, "MÜŞTERİ SÜRECİ", M, 0.86);
baslik(s, "PEŞİNATTAN TAPUYA DÖRT ADIM", M, 1.22, { w: 10.4, boy: 26 });
cizgi(s, M, 2.10, 1.30, VURGU, 1.5);
cizgi(s, 1.60, 3.82, 10.15, VURGU, 1.25, true);
[["i-banknot-beyaz", "Peşinat", "Avantajlı peşinatla başlar; kalan tutar 60 aya kadar taksitlenir."],
 ["i-takvim-beyaz", "Sabit taksit", "Faiz yok, kefil yok, banka yok; ara ödeme ve balon taksit yok."],
 ["i-bina-beyaz", "İnşaat ve takip", "Ödemeler ve inşaat aşamaları KOOPBİS üzerinden izlenir."],
 ["i-anahtar-beyaz", "Tapu", "İnşaat bitince ferdileşme ile daire adınıza tapuya bağlanır."]]
.forEach((a, i) => {
  const cx = 2.10 + i * 3.05;
  adimElmas(s, cx, 3.82, 1.85, a[0]);
  metin(s, "ADIM 0" + (i + 1), cx - 1.35, 5.02, { w: 2.7, h: 0.24, boy: 8, kalin: true,
    aralik: 2.2, hiza: "center", renk: VURGU });
  metin(s, a[1], cx - 1.35, 5.28, { w: 2.7, h: 0.32, boy: 13, kalin: true,
    hiza: "center", renk: GECE });
  metin(s, a[2], cx - 1.35, 5.64, { w: 2.7, h: 0.85, boy: 9, hiza: "center", renk: KURSUN });
});
metin(s, "Tapu sorusu mutlaka gelir: ferdileşme, inşaat bitiminde.", M, 6.72,
  { w: 11.5, h: 0.28, boy: 9.5, italik: true, hiza: "center", renk: KURSUN });
s.addNotes("Süreci dört adımda anlatın. 'Ferdileşme' kelimesini kullanın ve tapunun inşaat bitiminde olduğunu net söyleyin.");

/* ═══════════════════════════ 17 · SATIŞ ARGÜMANI (60 SANİYE) */
s = p.addSlide();
s.background = { color: GECE };
etiket(s, "SAHA", M, 0.86, VURGU);
baslik(s, "MÜŞTERİYE 60 SANİYEDE NASIL ANLATILIR?", M, 1.22, { w: 11.5, boy: 25, renk: KAGIT });
cizgi(s, M, 2.10, 1.30, VURGU, 1.5);
["Proje, İzmit'in gelişen MİA Bölgesi'nde.",
 "D100'e 1 dakika, sahile 2 dakika.",
 "Ağırlıklı olarak yatırımcıya uygun 1+0 ve 1+1 daireler var.",
 "Bankasız, faizsiz ve kefilsiz 60 aya kadar ödeme modeli bulunuyor.",
 "İstanbul'a yakınlığıyla yalnız İzmit'e değil, Marmara yatırımcısına da hitap ediyor."]
.forEach((c, i) => {
  const y = 2.52 + i * 0.86;
  noElmas(s, M + 0.22, y + 0.20, i + 1, VURGU, 0.46);
  metin(s, "“" + c + "”", M + 0.75, y, { w: 10.6, h: 0.44, boy: 14, italik: true,
    renk: KAGIT, dikeyH: "middle" });
  if (i < 4) cizgi(s, M, y + 0.66, 11.53, "1E4E6B", 0.6);
});
kose(s, 12.45, 0.95, VURGU, VURGU, 0.8);
kunye(s);
s.addNotes("Bu beş cümleyi emlakçıya ezberletin. Sırası önemli: konum, mesafe, ürün, ödeme, pazar.");

/* ════════════════════════════════════════════ 18 · İTİRAZ YÖNETİMİ */
s = p.addSlide();
s.background = { color: KAGIT };
etiket(s, "İTİRAZ YÖNETİMİ", M, 0.86);
baslik(s, "MÜŞTERİ SORARSA NE SÖYLEYECEĞİZ?", M, 1.22, { w: 11.0, boy: 26 });
cizgi(s, M, 2.10, 1.30, VURGU, 1.5);
[["“Kooperatif modeli güvenli mi?”", "Proje, 1163 sayılı Kooperatifler Kanunu çerçevesinde faaliyet gösterir; resmî kayıtlar T.C. Ticaret Bakanlığı'nın KOOPBİS sisteminde tutulur."],
 ["“Banka kredisi gerekiyor mu?”", "Hayır. Proje kendi tasarrufa dayalı ödeme modelini sunar; banka, faiz ve kefil devrede değildir."],
 ["“Konum gerçekten merkezi mi?”", "D100 1 dakika, İzmit Sahili 2 dakika, 41 Burada AVM 3 dakika, şehir merkezi 5 dakika."],
 ["“Yatırım için neden 1+0 / 1+1?”", "Kompakt daireler daha geniş kiracı ve yatırımcı segmentine hitap eder; kiralama hızlanır, likidite artar."]]
.forEach((q, i) => {
  const y = 2.52 + i * 1.02;
  elmasDolu(s, M + 0.10, y + 0.16, 0.18, VURGU);
  metin(s, q[0], M + 0.40, y - 0.04, { w: 3.95, h: 0.70, boy: 12, kalin: true,
    italik: true, renk: GECE, satir: 1.12 });
  metin(s, q[1], M + 4.70, y - 0.02, { w: 6.85, h: 0.80, boy: 9.5, renk: KURSUN });
  if (i < 3) cizgi(s, M, y + 0.84, 11.53, KAGIT_K, 0.6);
});
metin(s, "Bilgilendirme amaçlıdır; yasal veya finansal garanti niteliği taşımaz. Belgeler satış ofisinden talep edilebilir.",
  M, 6.72, { w: 11.53, h: 0.28, boy: 8, italik: true, renk: KURSUN });
s.addNotes("İlk soru en çok gelen soru. KOOPBİS'i telefonda canlı gösterin — en ikna edici hamle. Garanti cümlesi KURMAYIN.");

/* ═══════════════════════════════════════ 19 · GÜVEN VE ŞEFFAFLIK */
s = p.addSlide();
s.background = { color: KAGIT };
blok(s, 0, 0, 5.30, HT, GECE);
etiket(s, "KURUMSAL", M, 0.86, VURGU);
baslik(s, "SATIŞTA EN GÜÇLÜ\nUNSUR: GÜVEN", M, 1.22, { w: 3.9, h: 1.6, boy: 27, renk: KAGIT });
cizgi(s, M, 2.92, 1.30, VURGU, 1.5);
metin(s, "Emlakçının müşterisine karşı arkasında duracağı zemin: kayıtlı, denetlenen, belgeli bir yapı.",
  M, 3.22, { w: 3.6, h: 1.0, boy: 10.5, renk: SIS, satir: 1.45 });
elmasFoto(s, "e-guven", 3.65, 5.95, 2.00);
elmasDolu(s, 1.35, 5.35, 0.4, VURGU);
[["S.S. Yahya Kaptan Birlik Yapı Kooperatifi", "Projeyi geliştiren yapı kooperatifi"],
 ["T.C. Ticaret Bakanlığı — KOOPBİS", "Kooperatif Bilgi Sistemi'nde kayıtlı"],
 ["1163 Sayılı Kooperatifler Kanunu", "Kuruluş, genel kurul ve denetim bu kanuna tabi"],
 ["Ocean Gayrimenkul", "Tek yetkili satıcı"]].forEach((g, i) => {
  const y = 1.26 + i * 1.14;
  cizgi(s, 5.95, y + 0.16, 0.20, VURGU, 1.5);
  metin(s, g[0], 6.35, y - 0.02, { w: 6.1, h: 0.34, boy: 13, kalin: true, renk: GECE });
  metin(s, g[1], 6.35, y + 0.34, { w: 6.1, h: 0.28, boy: 9.5, renk: KURSUN });
  if (i < 3) cizgi(s, 5.95, y + 0.86, 6.45, KAGIT_K, 0.6);
});
blok(s, 5.95, 5.90, 6.45, 0.72, BEYAZ);
s.addImage({ path: mk("ykb-logo.png"), x: 6.55, y: 6.02, w: 0.48, h: 0.48 });
s.addImage({ path: mk("koopbis-logo.png"), x: 8.35, y: 6.08, w: 1.25, h: 0.38 });
s.addImage({ path: mk("ticaret-bakanligi-logo.webp"), x: 10.85, y: 6.02, w: 0.48, h: 0.48 });
metin(s, "Belgeler satış ofisinden talep edilebilir.", 5.95, 6.76,
  { w: 6.45, h: 0.26, boy: 8.5, italik: true, renk: KURSUN });
s.addNotes("Sade ve kurumsal anlatın. KOOPBİS kaydını göstermeyi teklif edin; belgeleri gösterme sözü verin ve tutun.");

/* ═══════════════════════════ 20 · İŞ BİRLİĞİ SÜRECİ (5 ADIM) */
s = p.addSlide();
s.background = { color: KAGIT };
etiket(s, "İŞ BİRLİĞİ", M, 0.86);
baslik(s, "EMLAKÇIYLA NASIL ÇALIŞIYORUZ?", M, 1.22, { w: 10.4, boy: 26 });
cizgi(s, M, 2.10, 1.30, VURGU, 1.5);
cizgi(s, 1.35, 3.72, 10.65, VURGU, 1.25, true);
[["i-belge-beyaz", "Kayıt", "Emlakçı kaydı ve yetki belgesi"],
 ["i-mail-beyaz", "Bildirim", "Müşteri ofise gelmeden bildirilir"],
 ["i-balon-beyaz", "Görüşme", "Satış ofisinde birlikte"],
 ["i-kalem-beyaz", "Sözleşme", "Ortaklık işlemleri ve peşinat"],
 ["i-banknot-beyaz", "Hakediş", "Komisyon ödemesi"]].forEach((a, i) => {
  const cx = 1.75 + i * 2.48;
  adimElmas(s, cx, 3.72, 1.55, a[0]);
  metin(s, "0" + (i + 1), cx - 1.1, 4.74, { w: 2.2, h: 0.24, boy: 8.5, kalin: true,
    aralik: 2.4, hiza: "center", renk: VURGU });
  metin(s, a[1], cx - 1.1, 5.00, { w: 2.2, h: 0.30, boy: 12.5, kalin: true,
    hiza: "center", renk: GECE });
  metin(s, a[2], cx - 1.1, 5.34, { w: 2.2, h: 0.62, boy: 8.5, hiza: "center", renk: KURSUN });
});
s.addShape(p.ShapeType.rect, { x: M, y: 6.14, w: 11.53, h: 0.92,
  fill: { color: BEYAZ }, line: { color: VURGU, width: 1.25 } });
metin(s, "SUNUMDAN ÖNCE NETLEŞTİRİN", M + 0.30, 6.26, { w: 4.0, h: 0.22, boy: 8,
  kalin: true, aralik: 2.0, renk: VURGU });
metin(s, "Komisyon oranı  ______        Hakediş zamanı  ______        Müşteri koruma süresi  ______",
  M + 0.30, 6.52, { w: 11.0, h: 0.40, boy: 11, renk: GECE });
s.addNotes("DİKKAT: Komisyon oranı, hakediş zamanı ve müşteri koruma süresi BOŞ bırakıldı — bu rakamlar sizde. Sunumdan önce doldurun; emlakçının en çok merak ettiği slayt bu.");

/* ═══════════════════════════════════ 21 · SATIŞ DESTEK MATERYALLERİ */
s = p.addSlide();
s.background = { color: KAGIT };
etiket(s, "SATIŞ DESTEĞİ", M, 0.86);
baslik(s, "ELİNİZE NE VERİYORUZ?", M, 1.22, { w: 7.2, boy: 26 });
cizgi(s, M, 2.10, 1.30, VURGU, 1.5);
["8 bilbord tasarımı", "8 arsa panosu", "Roll-up ve totem", "Yaka kartları",
 "Dijital katalog", "miaparkocean.com", "Sosyal medya seti", "Tanıtım filmi"]
.forEach((d, i) => {
  const x = M + (i % 2) * 3.55, y = 2.56 + Math.floor(i / 2) * 0.62;
  elmasDolu(s, x + 0.08, y + 0.16, 0.16, VURGU);
  metin(s, d, x + 0.32, y, { w: 3.1, h: 0.34, boy: 11, renk: GECE, dikeyH: "middle" });
});
blok(s, M, 5.20, 7.10, 0.86, GECE);
metin(s, "Hepsi baskıya hazır dosya olarak paylaşılır. Bugün en az katalog ve site linki elinizde olsun.",
  M + 0.32, 5.20, { w: 6.5, h: 0.86, boy: 10.5, renk: VURGU_A, dikeyH: "middle" });
s.addImage({ path: fo("m-bilbord"), x: 8.42, y: 1.10, w: 3.90, h: 2.34 });
s.addImage({ path: fo("m-rollup"), x: 8.42, y: 3.62, w: 1.30, h: 2.60 });
s.addImage({ path: fo("m-arsa"), x: 9.90, y: 3.62, w: 2.42, h: 1.62 });
elmasDolu(s, 10.35, 5.85, 0.4, VURGU);
kunye(s, true, 8.3);
s.addNotes("Somut olun: hangi dosyayı ne zaman göndereceğinizi söyleyin. Emlakçı eli boş dönmesin.");

/* ═══════════════════════════════════════════════════ 22 · GALERİ */
s = p.addSlide();
s.background = { color: GECE };
s.addImage({ path: fo("gal-1"), x: 0.00, y: 0.00, w: 7.07, h: 3.42 });
s.addImage({ path: fo("gal-2"), x: 7.15, y: 0.00, w: 3.05, h: 3.42 });
s.addImage({ path: fo("gal-3"), x: 10.28, y: 0.00, w: 3.05, h: 3.42 });
s.addImage({ path: fo("gal-4"), x: 0.00, y: 3.50, w: 3.05, h: 3.42 });
s.addImage({ path: fo("gal-5"), x: 3.13, y: 3.50, w: 3.05, h: 3.42 });
s.addImage({ path: fo("gal-6"), x: 6.26, y: 3.50, w: 7.07, h: 3.42 });
metin(s, "MİA PARK OCEAN  ·  PROJE GÖRSELLERİ", M, 7.06,
  { w: 6.0, boy: 8, aralik: 2.6, renk: VURGU_A });
metin(s, "Görseller projenin kendi render'larıdır.", W - M - 5.0, 7.06,
  { w: 5.0, boy: 8, aralik: 1.2, hiza: "right", renk: "7E9AAB" });
s.addNotes("Bu slaytta konuşmayın, bıraktırın. Gerekirse tek cümle: bunların hepsi projenin kendi görselleri.");

/* ═══════════════════════════════════ 23 · RAKAMLARLA MİA PARK OCEAN */
s = p.addSlide();
s.background = { color: GECE };
etiket(s, "ÖZET", M, 0.86, VURGU);
baslik(s, "RAKAMLARLA MİA PARK OCEAN", M, 1.22, { w: 10.4, boy: 26, renk: KAGIT });
cizgi(s, M, 2.10, 1.30, VURGU, 1.5);
[["600", "KONUT"], ["472", "ADET 1+0"], ["112", "ADET 1+1"],
 ["60 AY", "VADE FARKSIZ"], ["%30", "PEŞİNAT"], ["1 DK", "D100 KARAYOLU"]]
.forEach((k, i) => {
  const x = M + (i % 3) * 3.90, y = 2.66 + Math.floor(i / 3) * 1.95;
  elmasDolu(s, x + 0.16, y + 0.24, 0.22, VURGU);
  rakam(s, k[0], x + 0.48, y - 0.24, { w: 3.0, h: 0.92, boy: 40, renk: KAGIT });
  metin(s, k[1], x + 0.50, y + 0.76, { w: 3.0, h: 0.26, boy: 9, kalin: true,
    aralik: 2.2, renk: VURGU_A });
  cizgi(s, x + 0.50, y + 1.16, 2.9, "1E4E6B", 0.75);
});
kose(s, 12.45, 0.95, VURGU, VURGU, 0.8);
kunye(s);
s.addNotes("Kapanıştan önce rakam özeti. Altı rakamı tek tek okumayın; emlakçının aklında 600 / 60 ay / %30 kalsın.");

/* ═══════════════════════════════════════ 24 · NEDEN MİA PARK OCEAN */
s = p.addSlide();
s.background = { color: KAGIT };
etiket(s, "SONUÇ", M, 0.86);
baslik(s, "NEDEN MİA PARK OCEAN?", M, 1.22, { w: 9.4, boy: 26 });
cizgi(s, M, 2.10, 1.30, VURGU, 1.5);
[["Merkezi lokasyon", "D100'e 1 dk, merkeze 5 dk"],
 ["Gelişen MİA Bölgesi", "İzmit'in yeni değer aksı"],
 ["Derin kompakt stok", "472 adet 1+0, 112 adet 1+1"],
 ["Erişilebilir ödeme", "%30 peşinat, 60 ay vade farksız"],
 ["Geniş müşteri profili", "Beş ayrı alıcı segmenti"],
 ["Kurumsal güven", "KOOPBİS kayıtlı, kanuna tabi yapı"]]
.forEach((o, i) => {
  const x = M + (i % 3) * 3.90, y = 2.58 + Math.floor(i / 3) * 1.42;
  cizgi(s, x, y, 3.5, VURGU, 1);
  metin(s, o[0], x, y + 0.14, { w: 3.5, h: 0.32, boy: 13, kalin: true, renk: GECE });
  metin(s, o[1], x, y + 0.50, { w: 3.5, h: 0.30, boy: 9.5, renk: KURSUN });
});
blok(s, 0, 5.66, W, 1.30, GECE);
metin(s, "DOĞRU KONUM.  DOĞRU ÜRÜN.  GÜÇLÜ SATIŞ HİKÂYESİ.", 0, 5.66,
  { w: W, h: 1.30, boy: 22, kalin: true, hiza: "center", dikeyH: "middle",
    renk: KAGIT, aralik: 1.6 });
metin(s, "MİA PARK OCEAN  ·  İZMİT MİA BÖLGESİ  ·  OCEAN GAYRİMENKUL, TEK YETKİLİ SATICI",
  0, 7.08, { w: W, h: 0.28, boy: 8, aralik: 2.0, hiza: "center", renk: KURSUN });
s.addNotes("Kapanıştan önce özet. Üç kelime kalsın: konum, ürün, hikâye.");

/* ═══════════════════════════════════════════ 25 · KAPANIŞ / İLETİŞİM */
s = p.addSlide();
s.background = { color: GECE };
elmasCizgi(s, 10.35, 3.10, 4.15, VURGU, 1);
elmasFoto(s, "e-kapanis1", 10.50, 2.95, 3.40);
elmasFoto(s, "e-kapanis2", 8.35, 5.35, 2.30);
elmasDolu(s, 12.35, 5.30, 0.95, LACI);
elmasDolu(s, 7.50, 1.35, 0.42, VURGU);
s.addImage({ path: mk("brand/logo-ocean-white.png"), x: M, y: 0.70, w: 2.55, h: 1.75 });
cizgi(s, M, 2.78, 1.30, VURGU, 1.5);
baslik(s, "İZMİT'İN YENİ SATIŞ FIRSATINI\nPORTFÖYÜNÜZE EKLEYİN.", M, 3.02,
  { w: 6.4, h: 1.4, boy: 22, renk: KAGIT });
[["i-telefon-beyaz", "0540 028 00 41  ·  0541 128 40 41"],
 ["i-mail-beyaz", "info@oceangayrimenkul41.com"],
 ["i-globe-beyaz", "miaparkocean.com"],
 ["i-insta-beyaz", "@miaparkocean"]].forEach((c, i) => {
  const y = 4.58 + i * 0.50;
  s.addImage({ path: sk(c[0]), x: M, y: y + 0.03, w: 0.30, h: 0.30 });
  metin(s, c[1], M + 0.48, y, { w: 5.4, h: 0.36, boy: 11.5, kalin: i === 0,
    renk: KAGIT, dikeyH: "middle" });
});
blok(s, M, 6.62, 3.85, 0.58, VURGU_A);
metin(s, "SATIŞ EKİBİMİZLE İLETİŞİME GEÇİN", M, 6.62, { w: 3.85, h: 0.58, boy: 10,
  kalin: true, hiza: "center", dikeyH: "middle", renk: GECE, aralik: 1.2 });
metin(s, "OCEAN GAYRİMENKUL — TEK YETKİLİ SATICI  ·  S.S. YAHYA KAPTAN BİRLİK YAPI KOOPERATİFİ",
  5.05, 7.08, { w: 7.4, h: 0.26, boy: 7.5, aralik: 1.6, hiza: "right", renk: "7E9AAB" });
s.addNotes("Kapanış: net çağrı yapın. Kayıt formunu dağıtın; bugün kaydolan emlakçıya katalog ve görsel setini akşam gönderin. Randevu almadan salondan çıkarmayın.");

p.writeFile({ fileName: path.join(KOK, "sunum", "MIA-PARK-OCEAN-Emlakci-Sunumu.pptx") })
  .then((f) => console.log("yazildi:", f));
