/**
 * MİA PARK OCEAN — lansman sunumu (emlakçılara).
 *
 * Görsel dil: organik mavi dalga blokları, fotoğrafın dikdörtgen değil o
 * eğrinin içine maskelenmesi, katmanlı şeritler, kemer/hap kartlar.
 * pptxgenjs bezier çizemediği ve fotoğrafı maskeleyemediği için bütün
 * organik parçalar scripts/build-sunum-sekil.py ile PIL'de üretilip
 * sunum/kaynak/sekil/ altına yazılıyor; burası sadece yerleştiriyor.
 *
 *   python3 scripts/build-sunum-sekil.py     # şekiller (önce bu)
 *   node    scripts/build-sunum.js           # sunum
 *
 * Yerleşim gözle değil ölçüyle: her zeminde yazının oturabileceği açık ve
 * koyu alanlar scripts/sunum-alan.py ile ölçüldü, kutular ona göre.
 * Aşağıdaki GUVENLI tablosu o ölçümün özeti.
 */
const pptxgen = require("pptxgenjs");
const path = require("path");

const KAYNAK = process.env.MIA_SUNUM_IMG || path.join(__dirname, "..", "sunum", "kaynak");
const im = (n) => path.join(KAYNAK, n);
const sk = (n) => path.join(KAYNAK, "sekil", n + ".png");

/* ------------------------------------------------------------- palet */
const INK   = "04283A",   // en koyu lacivert
      DEEP  = "075878",
      AZURE = "1789C7",   // parlak mavi — referansın canlı tonu
      CYAN  = "48ABC5",
      ICE   = "DDF7FA",
      GREY  = "5A6B75",
      WHITE = "FFFFFF",
      CORAL = "F2704B";

/* Tek aile: referans da tek aile. Calibri her Office kurulumunda var. */
const F = "Calibri";

const W = 13.333, HT = 7.5, M = 0.72;

/* sunum-alan.py ölçümünün özeti — kutular bu sınırların içinde kalır */
const GUVENLI = {
  1:  { acik: [0.00, 6.45] },
  2:  { acik: [6.96, 13.33] },
  4:  { acik: [0.00, 7.95] },
  6:  { acik: [5.21, 13.33] },
  7:  { koyu: [0.00, 7.26] },
  9:  { acik: [4.05, 13.33] },
  10: { koyu: [0.00, 9.13] },
  13: { acik: [0.00, 8.25] },
  14: { koyu: [0.00, 8.87] },
  15: { acik: [0.00, 7.01] },
};

const p = new pptxgen();
p.layout = "LAYOUT_WIDE";
p.author = "Ocean Gayrimenkul";
p.company = "MİA PARK OCEAN";
p.title = "MİA PARK OCEAN — Lansman Sunumu";

/* ------------------------------------------------------------ yardım */
const golge = (b) => ({ type: "outer", color: INK, blur: b || 14, offset: 3, angle: 90, opacity: 0.14 });

function zemin(s, ad) {
  s.addImage({ path: sk(ad), x: 0, y: 0, w: W, h: HT });
}
function ustyazi(s, t, x, y, renk, w) {
  s.addText(t, { x, y, w: w || 6.0, h: 0.28, fontFace: F, fontSize: 11.5, bold: true,
    color: renk || AZURE, charSpacing: 2.6, margin: 0 });
}
function baslik(s, t, x, y, renk, boy, w, h) {
  s.addText(t, { x, y, w: w || 6.6, h: h || 0.82, fontFace: F, fontSize: boy || 32,
    bold: true, color: renk || INK, margin: 0, lineSpacingMultiple: 0.94 });
}
function kart(s, x, y, w, h, dolgu, yari) {
  const o = { x, y, w, h, rectRadius: 0.14, fill: { color: dolgu || WHITE }, shadow: golge() };
  if (yari) { o.fill = { color: dolgu || WHITE, transparency: yari }; o.shadow = undefined;
              o.line = { color: CYAN, width: 0.75, transparency: 40 }; }
  s.addShape(p.ShapeType.roundRect, o);
}
/* numara rozeti — referanstaki mavi daireler */
function rozet(s, x, y, d, n, dolgu, yazi, boy) {
  s.addShape(p.ShapeType.ellipse, { x, y, w: d, h: d, fill: { color: dolgu || AZURE } });
  s.addText(String(n), { x, y, w: d, h: d, align: "center", valign: "middle",
    fontFace: F, fontSize: boy || 13, bold: true, color: yazi || WHITE, margin: 0 });
}
/* hap etiket */
function hap(s, x, y, w, h, t, dolgu, yazi, boy) {
  s.addShape(p.ShapeType.roundRect, { x, y, w, h, rectRadius: h / 2, fill: { color: dolgu || AZURE } });
  s.addText(t, { x, y, w, h, align: "center", valign: "middle", fontFace: F,
    fontSize: boy || 11.5, bold: true, color: yazi || WHITE, margin: 0 });
}

let s;

/* ============================================================ 1 KAPAK */
s = p.addSlide();
zemin(s, "bg-01-kapak");
s.addImage({ path: path.join(__dirname, "..", "public", "brand", "logo-ocean-trim.png"),
  x: M, y: 0.52, w: 2.62, h: 1.81 });
ustyazi(s, "LANSMAN · İŞ ORTAKLARI SUNUMU", M, 2.86, AZURE, 5.4);
baslik(s, "Lüks artık\nulaşılabilir.", M, 3.24, INK, 46, 5.3, 2.0);
s.addText("İzmit MİA Bölgesi'nde 600 daire\nTasarrufa dayalı faizsiz finansman",
  { x: M, y: 5.18, w: 5.3, h: 0.76, fontFace: F, fontSize: 15, color: DEEP, margin: 0,
    lineSpacingMultiple: 1.22 });
hap(s, M, 6.12, 4.42, 0.56, "21 Ağustos 2026   ·   Emex Otel, Kocaeli", AZURE, WHITE, 12.5);
s.addText("S.S. Yahya Kaptan Birlik Yapı Kooperatifi  ·  Ocean Gayrimenkul, Tek Yetkili Satıcı",
  { x: M, y: 6.90, w: 5.6, h: 0.44, fontFace: F, fontSize: 9.5, color: GREY, margin: 0 });
s.addNotes("Açılış. Kendinizi ve kooperatifi tanıtın. Sunum 20 dakika, sonrasında soru-cevap. Bugünün amacı: MİA PARK OCEAN'ı satabilecek kadar iyi anlatmak.");

/* =========================================================== 2 GÜNDEM */
s = p.addSlide();
zemin(s, "bg-02-gundem");
ustyazi(s, "BUGÜN", 7.35, 0.72);
baslik(s, "Yirmi dakikada\naltı başlık", 7.35, 1.08, INK, 31, 5.5, 1.6);
[["Proje", "600 daire, dört yaşam tipi"],
 ["Konum", "D100'e 1 dk, merkeze 5 dk"],
 ["Ödeme", "Banka yok, faiz yok, kefil yok"],
 ["Yatırım", "m² fiyatı, beş yıllık projeksiyon"],
 ["Güvence", "Kooperatif neden devlet denetiminde"],
 ["İş birliği", "Size ne veriyoruz"]].forEach((g, i) => {
  const y = 2.74 + i * 0.74;
  kart(s, 7.35, y, 5.42, 0.62);
  rozet(s, 7.52, y + 0.11, 0.40, "0" + (i + 1), i < 3 ? AZURE : DEEP, WHITE, 11);
  s.addText(g[0], { x: 8.08, y, w: 1.55, h: 0.62, valign: "middle", fontFace: F,
    fontSize: 13.5, bold: true, color: INK, margin: 0 });
  s.addText(g[1], { x: 9.60, y, w: 3.0, h: 0.62, valign: "middle", fontFace: F,
    fontSize: 10.5, color: GREY, margin: 0 });
});
s.addNotes("Gündemi hızlı geçin. Vurgu 3. ve 6. başlıkta: ödeme modeli ve iş birliği. Emlakçı bu ikisini anlarsa gerisi kolay.");

/* ============================================================ 3 KÜNYE */
s = p.addSlide();
zemin(s, "bg-03-kunye");
ustyazi(s, "PROJE KÜNYESİ", M, 0.62, CYAN, 6.0);
baslik(s, "600 daire, dört yaşam tipi", M, 0.98, WHITE, 36, 9.5);
s.addText("İzmit MİA Bölgesi · S.S. Yahya Kaptan Birlik Yapı Kooperatifi",
  { x: M, y: 1.86, w: 8.4, h: 0.34, fontFace: F, fontSize: 13, color: ICE, margin: 0 });
[["600", "Toplam daire"], ["4", "Yaşam tipi"], ["28–100", "m² brüt"], ["60", "Ay sabit taksit"]]
.forEach((t, i) => {
  const x = M + i * 3.03;
  kart(s, x, 3.62, 2.78, 1.72);
  s.addText(t[0], { x: x + 0.26, y: 3.80, w: 2.30, h: 0.82, fontFace: F,
    fontSize: t[0].length > 3 ? 32 : 42, bold: true, color: AZURE, margin: 0 });
  s.addText(t[1], { x: x + 0.26, y: 4.72, w: 2.34, h: 0.34, fontFace: F,
    fontSize: 11.5, color: GREY, margin: 0 });
});
kart(s, M, 5.72, 11.89, 1.10, ICE);
s.addText("Dört tipin tamamı aynı sitede: 1+0 stüdyodan bahçeli 2+1 dublekse kadar her müşteri profiline bir cevap var.",
  { x: M + 0.42, y: 5.72, w: 11.1, h: 1.10, valign: "middle", fontFace: F,
    fontSize: 13, color: INK, margin: 0 });
s.addNotes("600 rakamını vurgulayın: emlakçı için sürekli stok demek. Dört tip, her müşteri profiline bir cevap.");

/* ============================================================ 4 KONUM */
s = p.addSlide();
zemin(s, "bg-04-konum");
ustyazi(s, "KONUM", M, 0.72);
baslik(s, "Her yere yakın", M, 1.08, INK, 34, 6.4);
s.addImage({ path: sk("i-konum"), x: M, y: 1.98, w: 0.46, h: 0.46 });
s.addText("İzmit'in gelişim aksı MİA Bölgesi", { x: M + 0.60, y: 1.98, w: 5.6, h: 0.46,
  valign: "middle", fontFace: F, fontSize: 13, bold: true, color: DEEP, margin: 0 });
[["D100 Karayolu", "1 dk"], ["İzmit Sahili", "2 dk"], ["41 Burada AVM", "3 dk"],
 ["Şehir Merkezi", "5 dk"], ["Şehir Hastanesi", "5 dk"], ["TEM Otoyolu", "5 dk"],
 ["Symbol AVM", "7 dk"], ["Kocaeli Üniversitesi", "10 dk"]].forEach((d, i) => {
  const x = M + (i % 2) * 3.70, y = 2.76 + Math.floor(i / 2) * 0.92;
  kart(s, x, y, 3.44, 0.72);
  s.addText(d[0], { x: x + 0.30, y, w: 2.18, h: 0.72, valign: "middle", fontFace: F,
    fontSize: 11.5, color: INK, margin: 0 });
  hap(s, x + 2.52, y + 0.14, 0.80, 0.44, d[1], ICE, DEEP, 12);
});
s.addText("Üniversite, hastane, AVM ve ana yollar dakikalar içinde.",
  { x: M, y: 6.56, w: 6.9, h: 0.34, fontFace: F, fontSize: 11, italic: true, color: GREY, margin: 0 });
s.addNotes("Mesafeleri ezberleyin; en çok D100 ve şehir hastanesi sorulur. İzmit Sahili süresi teyide açık, kesin konuşmayın.");

/* ============================================================= 5 STOK */
s = p.addSlide();
zemin(s, "bg-05-stok");
ustyazi(s, "STOK", M, 0.62);
baslik(s, "Dört tip, 600 daire", M, 0.98, INK, 34, 7.0);
[["k-1plus0", "1+0", "472", "Brüt 28 m²", "İlk ev ve yatırım"],
 ["k-1plus1", "1+1", "96", "Brüt 50 m²", "Çift ve küçük aile"],
 ["k-loft", "1+1 Bahçe Loft", "16", "Brüt 50 m²", "Zeminde kendi bahçesi"],
 ["k-dubleks", "2+1 Bahçe Dubleks", "16", "Brüt 100 m²", "Bahçeli dubleks"]]
.forEach((t, i) => {
  const x = M + i * 3.03;
  kart(s, x, 2.30, 2.78, 3.62);
  s.addImage({ path: sk(t[0]), x: x + 0.34, y: 1.86, w: 2.10, h: 2.63 });
  s.addText(t[1], { x: x + 0.20, y: 4.62, w: 2.38, h: 0.36, align: "center", fontFace: F,
    fontSize: t[1].length > 6 ? 12 : 15, bold: true, color: DEEP, margin: 0 });
  s.addText(t[2] + " adet", { x: x + 0.20, y: 5.00, w: 2.38, h: 0.42, align: "center",
    fontFace: F, fontSize: 22, bold: true, color: INK, margin: 0 });
  s.addText(t[3] + "  ·  " + t[4], { x: x + 0.16, y: 5.46, w: 2.46, h: 0.36, align: "center",
    fontFace: F, fontSize: 9.5, color: GREY, margin: 0 });
});
s.addText("Stokun %79'u 1+0 — hacim orada, kampanyayı oraya kurun.  Bahçeli tipler toplam 32 adet; aciliyet argümanınız bu.",
  { x: M, y: 6.48, w: 11.9, h: 0.52, align: "center", fontFace: F, fontSize: 14,
    bold: true, color: WHITE, margin: 0 });
s.addNotes("472 adet 1+0 — hacim burada. 16'şar adetlik bahçeli tipler gerçekten kıt; 'sınırlı sayıda' derken bunu kastedin.");

/* ============================================================ 6 YAŞAM */
s = p.addSlide();
zemin(s, "bg-06-yasam");
ustyazi(s, "SOSYAL YAŞAM", 5.45, 0.72);
baslik(s, "Merkezi avlu\nçevresinde hayat", 5.45, 1.08, INK, 31, 7.3, 1.6);
["Merkezi avlu", "Dekoratif süs havuzları", "Geniş peyzaj alanları", "Yürüyüş ve dinlenme yolları",
 "Bahçeli zemin daireler", "Özel gece aydınlatması", "Kapalı otopark", "7/24 güvenlik"]
.forEach((o, i) => {
  const x = 5.45 + (i % 2) * 3.78, y = 2.94 + Math.floor(i / 2) * 0.66;
  s.addImage({ path: sk("i-onay"), x, y: y + 0.03, w: 0.30, h: 0.30 });
  s.addText(o, { x: x + 0.42, y, w: 3.30, h: 0.36, valign: "middle", fontFace: F,
    fontSize: 12, color: INK, margin: 0 });
});
kart(s, 5.45, 5.86, 7.16, 0.94, ICE);
s.addImage({ path: sk("i-kalkan"), x: 5.72, y: 6.09, w: 0.48, h: 0.48 });
s.addText("Avludaki su SÜS havuzudur — yüzme havuzu diye anlatmayın.",
  { x: 6.36, y: 5.86, w: 6.0, h: 0.94, valign: "middle", fontFace: F, fontSize: 12.5,
    bold: true, color: DEEP, margin: 0 });
s.addNotes("ÖNEMLİ: Süs havuzu ile yüzme havuzunu karıştırmayın. Yüzme havuzu sözü verilirse teslimde sorun çıkar.");

/* =========================================================== 7 ÖDEME */
s = p.addSlide();
zemin(s, "bg-07-odeme");
ustyazi(s, "ÖDEME MODELİ", M, 0.72, CYAN, 6.0);
baslik(s, "Banka yok.\nFaiz yok. Kefil yok.", M, 1.08, WHITE, 36, 6.2, 1.8);
[["%0", "Faiz / vade farkı"], ["60", "Ay sabit taksit"], ["0", "Ara ödeme"]].forEach((b, i) => {
  const x = M + i * 2.14;
  s.addText(b[0], { x, y: 3.06, w: 2.0, h: 0.90, fontFace: F, fontSize: 44, bold: true,
    color: CORAL, margin: 0 });
  s.addText(b[1], { x, y: 3.96, w: 2.0, h: 0.52, fontFace: F, fontSize: 10.5,
    color: ICE, margin: 0 });
});
[["Tasarrufa dayalı finansman", "Tasarruf esaslı, faizsiz model. Bankaya ve kefile gerek yok."],
 ["Sabit taksit", "Bugün belirlenen taksit 60 ay aynı kalır. Balon taksit yok."],
 ["Enflasyon avantajı", "Taksit sabit kaldığı için ödemenin gerçek yükü ay ay hafifler."],
 ["Üye maliyetine konut", "Kooperatif kâr amacı gütmez; araya müteahhit kârı girmez."]]
.forEach((o, i) => {
  const y = 4.68 + i * 0.62;
  s.addImage({ path: sk("i-onay"), x: M, y: y + 0.04, w: 0.28, h: 0.28 });
  s.addText([{ text: o[0] + " — ", options: { bold: true, color: WHITE } },
             { text: o[1], options: { color: ICE } }],
    { x: M + 0.40, y, w: 6.1, h: 0.40, valign: "middle", fontFace: F, fontSize: 10.5, margin: 0 });
});
s.addNotes("Sunumun kalbi. Emlakçı buradan tek cümle götürsün: bankaya gitmeden, faiz ödemeden, kefil bulmadan ev. Kredisi çıkmayan müşteri sizin müşteriniz.");

/* ========================================================== 8 YATIRIM */
s = p.addSlide();
zemin(s, "bg-08-yatirim");
ustyazi(s, "YATIRIM", M, 0.72);
baslik(s, "MİA Bölgesi'nde m² değeri", M, 1.08, INK, 32, 7.8);
s.addChart(p.ChartType.bar, [{ name: "₺/m²", labels: ["2026", "2027", "2028", "2029", "2030", "2031"],
  values: [89000, 111250, 139063, 173828, 217285, 271606] }],
  { x: M - 0.16, y: 2.10, w: 8.30, h: 3.44, barDir: "col", chartColors: [AZURE],
    showValue: true, dataLabelPosition: "outEnd", dataLabelFontFace: F, dataLabelFontSize: 9,
    dataLabelColor: INK, dataLabelFormatCode: "#,##0",
    catAxisLabelFontFace: F, catAxisLabelFontSize: 11, catAxisLabelColor: GREY,
    valAxisHidden: true, catGridLine: { style: "none" }, valGridLine: { color: "E6F1F6", size: 1 },
    showLegend: false, barGapWidthPct: 46 });
[["89.000 ₺", "bugünkü m² fiyatı"], ["%25", "yıllık öngörü"], ["×3", "beş yılda"]]
.forEach((y, i) => {
  const x = M + i * 2.70;
  kart(s, x, 5.66, 2.48, 1.04);
  s.addText(y[0], { x: x + 0.22, y: 5.78, w: 2.06, h: 0.44, fontFace: F, fontSize: 19,
    bold: true, color: AZURE, margin: 0 });
  s.addText(y[1], { x: x + 0.22, y: 6.22, w: 2.10, h: 0.32, fontFace: F, fontSize: 10,
    color: GREY, margin: 0 });
});
s.addText("Beş yıllık projeksiyon %25 yıllık artış varsayımına dayalı bir ÖNGÖRÜDÜR; değer taahhüdü değildir.",
  { x: M, y: 6.86, w: 8.2, h: 0.32, fontFace: F, fontSize: 9, italic: true, color: GREY, margin: 0 });
s.addNotes("'Öngörü' kelimesini mutlaka kullanın. Taahhüt gibi anlatılırsa hem etik hem hukuki sorun olur.");

/* ========================================================== 9 GÜVENCE */
s = p.addSlide();
zemin(s, "bg-09-guvence");
ustyazi(s, "GÜVENCE", 4.42, 0.72);
baslik(s, "Kooperatif devlet\ndenetiminde", 4.42, 1.08, INK, 31, 8.2, 1.6);
[["1163 sayılı Kanun", "Kuruluştan tasfiyeye kadar her şey 1969'dan beri yürürlükteki kanunla tanımlı."],
 ["e-Devlet / KOOPBİS", "Ana sözleşme, genel kurul kararları ve ortaklık kaydı e-Devlet'ten görülebilir."],
 ["Bakanlık temsilcisi", "Genel kurul, Bakanlık tarafından görevlendirilen temsilci gözetiminde yapılır."],
 ["Çok katmanlı denetim", "İçeride ortakların denetim organı, dışarıda bağımsız dış denetim ve Bakanlık."]]
.forEach((g, i) => {
  const x = 4.42 + (i % 2) * 4.30, y = 2.96 + Math.floor(i / 2) * 1.90;
  kart(s, x, y, 4.02, 1.68);
  rozet(s, x + 0.26, y + 0.22, 0.50, "0" + (i + 1), i % 2 ? DEEP : AZURE, WHITE, 12);
  s.addText(g[0], { x: x + 0.88, y: y + 0.24, w: 2.94, h: 0.46, valign: "middle",
    fontFace: F, fontSize: 13.5, bold: true, color: INK, margin: 0 });
  s.addText(g[1], { x: x + 0.26, y: y + 0.82, w: 3.56, h: 0.72, fontFace: F,
    fontSize: 10.5, color: GREY, margin: 0 });
});
s.addText("Genel bilgilendirmedir; güncel mevzuat ve kooperatif ana sözleşmesi esastır.",
  { x: 5.05, y: 6.86, w: 7.6, h: 0.30, fontFace: F, fontSize: 9, italic: true, color: GREY, margin: 0 });
s.addNotes("Emlakçının en çok takıldığı yer. 'Kooperatif riskli mi?' sorusuna dört maddeyle cevap verin. KOOPBİS'i telefonda canlı gösterin — en ikna edici hamle.");

/* ======================================================= 10 İTİRAZLAR */
s = p.addSlide();
zemin(s, "bg-10-itiraz");
ustyazi(s, "SAHA", M, 0.72, CYAN, 6.0);
baslik(s, "Dört itiraz, dört cevap", M, 1.08, WHITE, 34, 8.0);
[["Kooperatif riskli.", "1163 sayılı Kanun kapsamında, KOOPBİS'ten izlenebilir, genel kurulu Bakanlık temsilcisi gözetiminde."],
 ["Kredim çıkmıyor.", "Zaten bankaya gitmiyoruz. Ne kredi, ne faiz, ne kefil."],
 ["Taksit sonradan artar mı?", "Hayır. Bugün belirlenen taksit 60 ay sabit; ara ödeme ve balon taksit yok."],
 ["Tapuyu ne zaman alırım?", "İnşaat tamamlandıktan sonra ferdileşme ile daire adınıza tapuya bağlanır."]]
.forEach((t, i) => {
  const y = 2.42 + i * 1.16;
  kart(s, M, y, 8.24, 1.00, WHITE, 90);
  rozet(s, M + 0.24, y + 0.26, 0.48, i + 1, i % 2 ? DEEP : AZURE, WHITE, 13);
  s.addText("“" + t[0] + "”", { x: M + 0.86, y: y + 0.08, w: 3.05, h: 0.42, valign: "middle",
    fontFace: F, fontSize: 12.5, bold: true, italic: true, color: CYAN, margin: 0 });
  s.addText(t[1], { x: M + 0.86, y: y + 0.46, w: 7.14, h: 0.46, valign: "middle",
    fontFace: F, fontSize: 10.5, color: WHITE, margin: 0 });
});
s.addNotes("Bu slaydı fotoğraflatın. Sahada en çok gelen dört itiraz. Cevapları ezberden değil kendi cümlelerinizle söyleyin.");

/* ===================================================== 11 HEDEF KİTLE */
s = p.addSlide();
zemin(s, "bg-11-kitle");
ustyazi(s, "HEDEF KİTLE", M, 0.60, CYAN, 6.0);
baslik(s, "Kimi getireceksiniz", M, 0.96, WHITE, 33, 9.0);
[["d-studyo", "İlk evini alan", "Peşinatı olan, kredisi çıkmayan genç alıcı", "1+0"],
 ["d-salon", "Yatırımcı", "Kiralamak ve değerlenme bekleyen", "1+0 · 1+1"],
 ["d-teras", "Küçük aile", "Çift ya da tek çocuklu aile", "1+1"],
 ["d-dubleks", "Bahçe isteyen", "Apartmanda müstakil ev hissi", "Bahçe Loft · Dubleks"]]
.forEach((k, i) => {
  const x = M + i * 3.03;
  kart(s, x, 2.72, 2.78, 3.16);
  s.addImage({ path: sk(k[0]), x: x + 0.64, y: 1.98, w: 1.50, h: 1.50 });
  s.addText(k[1], { x: x + 0.16, y: 3.68, w: 2.46, h: 0.40, align: "center", fontFace: F,
    fontSize: 15, bold: true, color: INK, margin: 0 });
  s.addText(k[2], { x: x + 0.20, y: 4.14, w: 2.38, h: 0.86, align: "center", fontFace: F,
    fontSize: 10.5, color: GREY, margin: 0 });
  hap(s, x + 0.24, 5.16, 2.30, 0.48, k[3], i % 2 ? AZURE : CORAL, WHITE, k[3].length > 12 ? 9 : 11);
});
s.addText("Portföyünüzdeki kredisi çıkmayan müşteriler bu projenin asıl hedefi. Reddedilen kredi başvurusu burada satışa dönüyor.",
  { x: M, y: 6.42, w: 11.9, h: 0.40, align: "center", fontFace: F, fontSize: 12,
    bold: true, color: DEEP, margin: 0 });
s.addNotes("Portföyünüzdeki kredisi çıkmayan müşterileri hatırlayın — bu projenin asıl hedefi onlar. Reddedilen kredi başvurusu burada satışa dönüyor.");

/* ========================================================== 12 DESTEK */
s = p.addSlide();
zemin(s, "bg-12-destek");
ustyazi(s, "SATIŞ DESTEĞİ", M, 0.72);
baslik(s, "Elinize ne veriyoruz", M, 1.08, INK, 33, 8.0);
/* materyaller: oranları korunmuş halde üretildi (build-sunum-sekil.py) */
s.addImage({ path: sk("m-bilbord"),  x: M,    y: 2.06, w: 3.30, h: 2.05 });
s.addImage({ path: sk("m-bilbord2"), x: M,    y: 4.32, w: 3.30, h: 2.05 });
s.addImage({ path: sk("m-arsa"),     x: 4.26, y: 4.98, w: 2.06, h: 1.42 });
s.addImage({ path: sk("m-rollup"),   x: 4.26, y: 2.06, w: 1.42, h: 2.79 });
s.addImage({ path: sk("m-katalog"),  x: 5.86, y: 2.06, w: 1.96, h: 2.79 });
s.addImage({ path: sk("m-yaka"),     x: 6.50, y: 4.98, w: 1.00, h: 1.42 });
["8 bilbord tasarımı", "8 arsa panosu", "Roll-up ve totem", "Yaka kartları",
 "Dijital katalog", "miaparkocean.com", "Sosyal medya seti", "Tanıtım filmi"]
.forEach((d, i) => {
  const x = 8.34 + (i % 2) * 2.42, y = 2.16 + Math.floor(i / 2) * 0.68;
  s.addImage({ path: sk("i-onay"), x, y: y + 0.03, w: 0.28, h: 0.28 });
  s.addText(d, { x: x + 0.38, y, w: 2.00, h: 0.34, valign: "middle", fontFace: F,
    fontSize: 11, color: INK, margin: 0 });
});
kart(s, 8.34, 5.06, 4.62, 1.34, ICE);
s.addText("Hepsi baskıya hazır dosya olarak paylaşılır. Bugün en az katalog ve site linki elinizde olsun.",
  { x: 8.62, y: 5.06, w: 4.10, h: 1.34, valign: "middle", fontFace: F, fontSize: 11.5,
    color: INK, margin: 0 });
s.addNotes("Somut olun: hangi dosyayı ne zaman göndereceğinizi söyleyin. Emlakçı eli boş dönmesin — bugün en az katalog ve site linkini verin.");

/* ====================================================== 13 İŞ BİRLİĞİ */
s = p.addSlide();
zemin(s, "bg-13-isbirligi");
ustyazi(s, "İŞ BİRLİĞİ", M, 0.72);
baslik(s, "Nasıl çalışıyoruz", M, 1.08, INK, 33, 7.0);
[["Kayıt", "Emlakçı kaydı ve yetki belgesi"],
 ["Müşteri bildirimi", "Müşteri ofise gelmeden bildirilir"],
 ["Görüşme", "Satış ofisinde birlikte"],
 ["Sözleşme", "Ortaklık işlemleri ve peşinat"],
 ["Hakediş", "Komisyon ödemesi"]].forEach((a, i) => {
  const y = 2.06 + i * 0.80;
  kart(s, M, y, 7.42, 0.66);
  rozet(s, M + 0.20, y + 0.11, 0.44, "0" + (i + 1), i < 3 ? AZURE : DEEP, WHITE, 11.5);
  s.addText(a[0], { x: M + 0.82, y, w: 2.42, h: 0.66, valign: "middle", fontFace: F,
    fontSize: 13.5, bold: true, color: INK, margin: 0 });
  s.addText(a[1], { x: M + 3.30, y, w: 3.90, h: 0.66, valign: "middle", fontFace: F,
    fontSize: 10.5, color: GREY, margin: 0 });
});
s.addShape(p.ShapeType.roundRect, { x: M, y: 6.10, w: 7.42, h: 1.06, rectRadius: 0.14,
  fill: { color: WHITE }, line: { color: CORAL, width: 1.5 }, shadow: golge() });
s.addText("SUNUMDAN ÖNCE DOLDURULACAK", { x: M + 0.30, y: 6.22, w: 5.4, h: 0.26,
  fontFace: F, fontSize: 9.5, bold: true, color: CORAL, charSpacing: 2.0, margin: 0 });
s.addText("Komisyon oranı  ______     Hakediş zamanı  ______     Müşteri koruma süresi  ______",
  { x: M + 0.30, y: 6.56, w: 6.9, h: 0.40, fontFace: F, fontSize: 11.5, color: INK, margin: 0 });
s.addNotes("DİKKAT: Komisyon oranı, hakediş zamanı ve müşteri koruma süresi BOŞ. Bu üç rakamı sunumdan önce doldurun; emlakçının en çok merak ettiği slayt bu, boş kalırsa güven kaybı olur.");

/* ============================================================ 14 SÜREÇ */
s = p.addSlide();
zemin(s, "bg-14-surec");
ustyazi(s, "MÜŞTERİ SÜRECİ", M, 0.72, CYAN, 6.0);
baslik(s, "Peşinattan tapuya", M, 1.08, WHITE, 34, 7.6);
[["Peşinat", "Avantajlı peşinatla başlar, kalan tutar 60 aya kadar taksitlenir."],
 ["60 ay taksit", "Faiz yok, kefil yok, banka yok. Sabit taksit, ara ödeme yok."],
 ["İnşaat ve takip", "Ödemeler ve inşaat aşamaları KOOPBİS ve ilerleme panelinden izlenir."],
 ["Tapu", "İnşaat bitince ferdileşme ile daire adına tapuya bağlanır."]]
.forEach((t, i) => {
  const y = 2.42 + i * 1.14;
  kart(s, M, y, 7.98, 0.98, WHITE, 90);
  rozet(s, M + 0.24, y + 0.25, 0.48, i + 1, i < 2 ? CORAL : AZURE, WHITE, 13);
  s.addText(t[0], { x: M + 0.86, y, w: 2.20, h: 0.98, valign: "middle", fontFace: F,
    fontSize: 13.5, bold: true, color: WHITE, margin: 0 });
  s.addText(t[1], { x: M + 3.10, y, w: 4.72, h: 0.98, valign: "middle", fontFace: F,
    fontSize: 10.5, color: ICE, margin: 0 });
});
s.addText("Tapu sorusu mutlaka gelir: ferdileşme, inşaat bitiminde.",
  { x: M, y: 7.00, w: 7.9, h: 0.32, fontFace: F, fontSize: 10.5, italic: true, color: CYAN, margin: 0 });
s.addNotes("Süreci dört adımda anlatın. Tapu sorusu mutlaka gelir; ferdileşme kelimesini kullanın ve inşaat bitiminde olduğunu net söyleyin.");

/* ========================================================= 15 KAPANIŞ */
s = p.addSlide();
zemin(s, "bg-15-kapanis");
s.addImage({ path: path.join(__dirname, "..", "public", "brand", "logo-ocean-trim.png"),
  x: M, y: 0.52, w: 2.40, h: 1.66 });
baslik(s, "Yarın sabah ilk\nmüşterinizi getirin.", M, 2.60, INK, 38, 5.9, 1.7);
s.addText("Satış ofisimiz her gün açık. Kahvemizi içmeye bekleriz.",
  { x: M, y: 4.36, w: 5.9, h: 0.36, fontFace: F, fontSize: 13.5, color: DEEP, margin: 0 });
[["i-telefon", "0540 028 00 41  ·  0541 128 40 41"],
 ["i-web", "miaparkocean.com"],
 ["i-instagram", "@miaparkocean"]].forEach((c, i) => {
  const y = 4.94 + i * 0.62;
  s.addImage({ path: sk(c[0]), x: M, y, w: 0.44, h: 0.44 });
  s.addText(c[1], { x: M + 0.60, y, w: 5.2, h: 0.44, valign: "middle", fontFace: F,
    fontSize: 12.5, bold: true, color: INK, margin: 0 });
});
s.addText("OCEAN GAYRİMENKUL  ·  Tek Yetkili Satıcı",
  { x: M, y: 6.86, w: 5.9, h: 0.32, fontFace: F, fontSize: 10, color: GREY,
    charSpacing: 0.8, margin: 0 });
kart(s, 9.42, 2.62, 3.06, 3.06);
s.addImage({ path: im("qr.png"), x: 9.70, y: 2.90, w: 2.50, h: 2.50 });
hap(s, 9.42, 5.88, 3.06, 0.50, "Projeyi telefonunuzda açın", AZURE, WHITE, 10.5);
s.addNotes("Kapanış: net çağrı yapın. Kayıt formunu dağıtın, bugün kaydolan emlakçıya katalog ve görsel setini akşam gönderin.");

p.writeFile({ fileName: path.join(__dirname, "..", "sunum", "MIA-PARK-OCEAN-Lansman-Sunumu.pptx") })
  .then((f) => console.log("yazildi:", f));
