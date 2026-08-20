/**
 * MİA PARK OCEAN — lansman sunumu (emlakçılara).
 *
 * 15 slayt, 16:9. İçerik src/data altındaki proje verisinden alınmıştır;
 * rakam uydurulmamıştır. Konuşmacı notları her slaytta var.
 *
 * Yazı tipleri Cambria (başlık) ve Calibri (gövde): ikisi de Office ile
 * geliyor, sunumu açan makinede kesin var.
 *
 * Görseller sunum/kaynak/ altında. Yeniden üretmek için:
 *     node scripts/build-sunum.js
 *
 * DİKKAT — 13. slaytta üç alan bilerek BOŞ: komisyon oranı, hakediş
 * zamanı, müşteri koruma süresi. Bunlar depoda yok; sunumdan önce
 * elle doldurulmalı.
 */
const pptxgen = require("pptxgenjs");
const path = require("path");
const IMG = process.env.MIA_SUNUM_IMG ||
  path.join(__dirname, "..", "sunum", "kaynak");
const im = (n) => path.join(IMG, n);

const INK="04283A", DEEP="075878", OCEAN="1A7496", CYAN="48ABC5",
      ICE="DDF7FA", PAPER="F4FAFC", WHITE="FFFFFF", CORAL="F2704B",
      SAND="B9884E", GREY="5B6C75";
const H1="Cambria", BODY="Calibri";
const W=13.3, HT=7.5, M=0.62;

const p = new pptxgen();
p.layout = "LAYOUT_WIDE";
p.author = "Ocean Gayrimenkul";
p.company = "MİA PARK OCEAN";
p.title = "MİA PARK OCEAN — Lansman Sunumu";

const shadow = () => ({ type:"outer", color:"04283A", blur:14, offset:3, angle:90, opacity:0.14 });

/* koyu zeminli slayt */
function dark(s){ s.background={path:im("bg-koyu.jpg")}; }

/* açık zeminli slayt + başlık */
function head(s, kicker, title, opts={}){
  s.background={color: opts.bg||PAPER};
  if(kicker) s.addText(kicker,{x:M,y:0.44,w:9,h:0.3,fontFace:BODY,fontSize:12,bold:true,
    color:opts.kickerColor||OCEAN,charSpacing:2.6,margin:0});
  s.addText(title,{x:M,y:0.76,w:11.6,h:0.72,fontFace:H1,fontSize:34,bold:true,
    color:opts.titleColor||INK,margin:0});
}

/* numaralı daire */
function circle(s,x,y,d,fill,txt,color,size){
  s.addShape(p.ShapeType.ellipse,{x,y,w:d,h:d,fill:{color:fill}});
  s.addText(txt,{x,y,w:d,h:d,align:"center",valign:"middle",fontFace:BODY,
    fontSize:size||13,bold:true,color:color||WHITE,margin:0});
}

/* kart */
function card(s,x,y,w,h,fill){
  s.addShape(p.ShapeType.roundRect,{x,y,w,h,rectRadius:0.09,
    fill:{color:fill||WHITE},shadow:shadow()});
}

/* ---------------------------------------------------------------- 1 kapak */
let s = p.addSlide();
s.addImage({path:im("gece.jpg"),x:0,y:0,w:W,h:HT,sizing:{type:"cover",w:W,h:HT}});
s.addShape(p.ShapeType.rect,{x:0,y:0,w:W,h:HT,fill:{color:INK,transparency:38}});
s.addShape(p.ShapeType.rect,{x:0,y:3.5,w:W,h:4.0,fill:{color:INK,transparency:22}});
s.addImage({path:im("logo-beyaz.png"),x:M,y:0.5,w:2.35,h:1.61});
s.addText("LANSMAN · İŞ ORTAKLARI SUNUMU",{x:M,y:3.55,w:9,h:0.3,fontFace:BODY,
  fontSize:12.5,bold:true,color:CYAN,charSpacing:3,margin:0});
s.addText("Lüks artık ulaşılabilir.",{x:M,y:3.95,w:9.4,h:1.0,fontFace:H1,fontSize:46,
  bold:true,color:WHITE,margin:0});
s.addText("İzmit MİA Bölgesi'nde 600 daire · Tasarrufa dayalı faizsiz finansman",
  {x:M,y:4.98,w:9.6,h:0.42,fontFace:BODY,fontSize:16,color:ICE,margin:0});
s.addText("21 Ağustos 2026   ·   Emex Otel, Kocaeli",{x:M,y:5.9,w:6,h:0.34,
  fontFace:BODY,fontSize:13.5,bold:true,color:WHITE,margin:0});
s.addText("S.S. Yahya Kaptan Birlik Yapı Kooperatifi   ·   Ocean Gayrimenkul, Tek Yetkili Satıcı",
  {x:M,y:6.3,w:9.6,h:0.34,fontFace:BODY,fontSize:11.5,color:CYAN,margin:0});
s.addNotes("Açılış. Kendinizi ve kooperatifi tanıtın. Bu sunum 20 dakika, sonrasında soru-cevap. Bugünün amacı: MİA PARK OCEAN'ı satabilecek kadar iyi anlatmak.");

/* -------------------------------------------------------------- 2 gündem */
s = p.addSlide();
head(s,"BUGÜN","Yirmi dakikada altı başlık");
const gundem=[
 ["Proje","600 daire, dört yaşam tipi, İzmit MİA Bölgesi"],
 ["Konum","D100'e 1 dakika, şehir merkezine 5 dakika"],
 ["Ödeme","Banka yok, faiz yok, kefil yok — 60 ay sabit taksit"],
 ["Yatırım","MİA Bölgesi m² fiyatı ve beş yıllık projeksiyon"],
 ["Güvence","Kooperatif neden devlet denetiminde"],
 ["İş birliği","Size ne veriyoruz, nasıl çalışıyoruz"]];
gundem.forEach((g,i)=>{
  const col=i%2, row=Math.floor(i/2);
  const x=M+col*6.05, y=2.0+row*1.42;
  circle(s,x,y+0.16,0.52,i<3?DEEP:OCEAN,String(i+1));
  s.addText(g[0],{x:x+0.74,y:y+0.06,w:5.1,h:0.36,fontFace:H1,fontSize:19,bold:true,color:INK,margin:0});
  s.addText(g[1],{x:x+0.74,y:y+0.46,w:5.1,h:0.6,fontFace:BODY,fontSize:13,color:GREY,margin:0});
});
s.addNotes("Gündemi hızlı geçin. Vurgu: 3. ve 6. başlık — ödeme modeli ve iş birliği. Emlakçının bu iki başlığı anlaması satışın tamamı.");

/* ------------------------------------------------------------ 3 künye */
s = p.addSlide();
s.background={color:PAPER};
s.addImage({path:im("gunduz.jpg"),x:0,y:0,w:5.6,h:HT,sizing:{type:"cover",w:5.6,h:HT}});
s.addText("PROJE KÜNYESİ",{x:6.1,y:0.7,w:6.5,h:0.3,fontFace:BODY,fontSize:12,bold:true,
  color:OCEAN,charSpacing:2.6,margin:0});
s.addText("600 daire, dört yaşam tipi",{x:6.1,y:1.04,w:6.6,h:0.75,fontFace:H1,
  fontSize:31,bold:true,color:INK,margin:0});
const stat=[["600","Toplam daire"],["4","Yaşam tipi"],["28–100","m² brüt aralık"],["60","Ay sabit taksit"]];
stat.forEach((t,i)=>{
  const x=6.1+(i%2)*3.3, y=2.15+Math.floor(i/2)*1.5;
  s.addText(t[0],{x,y,w:3.0,h:0.72,fontFace:H1,fontSize:40,bold:true,color:DEEP,margin:0});
  s.addText(t[1],{x,y:y+0.74,w:3.0,h:0.32,fontFace:BODY,fontSize:12.5,color:GREY,margin:0});
});
card(s,6.1,5.25,6.55,1.55);
s.addText("Yapımcı  ·  S.S. Yahya Kaptan Birlik Yapı Kooperatifi",
  {x:6.42,y:5.48,w:6.0,h:0.32,fontFace:BODY,fontSize:13,bold:true,color:INK,margin:0});
s.addText("Satış  ·  Ocean Gayrimenkul, Tek Yetkili Satıcı",
  {x:6.42,y:5.86,w:6.0,h:0.32,fontFace:BODY,fontSize:13,color:GREY,margin:0});
s.addText("Konum  ·  İzmit MİA Bölgesi, Kocaeli",
  {x:6.42,y:6.24,w:6.0,h:0.32,fontFace:BODY,fontSize:13,color:GREY,margin:0});
s.addNotes("600 rakamını vurgulayın: bu ölçek, emlakçı için sürekli stok demek. Dört tip olması her müşteri profiline bir cevabınız olduğu anlamına geliyor.");

/* ------------------------------------------------------------ 4 konum */
s = p.addSlide();
head(s,"KONUM","Her yere yakın");
const mesafe=[["D100 Karayolu","1 dk"],["İzmit Sahili","2 dk"],["41 Burada AVM","3 dk"],
  ["Şehir Merkezi","5 dk"],["Şehir Hastanesi","5 dk"],["TEM Otoyolu","5 dk"],
  ["Symbol AVM","7 dk"],["Kocaeli Üniversitesi","10 dk"]];
mesafe.forEach((d,i)=>{
  const x=M+(i%4)*3.05, y=1.95+Math.floor(i/4)*1.62;
  card(s,x,y,2.78,1.32);
  s.addText(d[0],{x:x+0.24,y:y+0.2,w:2.3,h:0.5,fontFace:BODY,fontSize:12.5,color:GREY,margin:0});
  s.addText(d[1],{x:x+0.24,y:y+0.68,w:2.3,h:0.5,fontFace:H1,fontSize:27,bold:true,color:DEEP,margin:0});
});
card(s,M,5.42,12.06,1.28,ICE);
s.addText("İzmit'in gelişim aksı MİA Bölgesi. Üniversite, hastane, AVM ve ana yollar dakikalar içinde — müşteriye anlatırken en kolay satan başlık bu.",
  {x:M+0.32,y:5.66,w:11.4,h:0.8,fontFace:BODY,fontSize:14,color:INK,margin:0});
s.addNotes("Mesafeleri ezberleyin. En çok sorulan: D100 ve şehir hastanesi. İzmit Sahili süresi teyide açık, kesin konuşmayın.");

/* --------------------------------------------------------- 5 daire tipleri */
s = p.addSlide();
head(s,"STOK","Dört tip, 600 daire");
const tip=[["1+0","472","Brüt 28 m²","İlk ev ve yatırım"],
  ["1+1","96","Brüt 50 m²","Çift ve küçük aile"],
  ["1+1 Bahçe Loft","16","Brüt 50 m²","Zeminde kendi bahçesi"],
  ["2+1 Bahçe Dubleks","16","Brüt 100 m²","Bahçeli dubleks"]];
tip.forEach((t,i)=>{
  const x=M+i*3.05;
  card(s,x,1.95,2.78,3.0);
  s.addShape(p.ShapeType.roundRect,{x:x,y:1.95,w:2.78,h:0.72,rectRadius:0.09,fill:{color:i<2?DEEP:OCEAN}});
  s.addText(t[0],{x:x+0.2,y:1.95,w:2.4,h:0.72,valign:"middle",fontFace:H1,fontSize:t[0].length>6?15:21,
    bold:true,color:WHITE,margin:0});
  s.addText(t[1],{x:x+0.24,y:2.92,w:2.3,h:0.68,fontFace:H1,fontSize:34,bold:true,color:INK,margin:0});
  s.addText("adet",{x:x+0.24,y:3.58,w:2.3,h:0.3,fontFace:BODY,fontSize:12,color:GREY,margin:0});
  s.addText(t[2],{x:x+0.24,y:3.98,w:2.3,h:0.3,fontFace:BODY,fontSize:13,bold:true,color:DEEP,margin:0});
  s.addText(t[3],{x:x+0.24,y:4.32,w:2.34,h:0.5,fontFace:BODY,fontSize:11.5,color:GREY,margin:0});
});
card(s,M,5.3,12.06,1.42,ICE);
s.addText("Stokun %79'u 1+0. Kampanyayı ve müşteri akışını buraya kurun; bahçeli tipler 32 adetle sınırlı, onları aciliyet argümanı olarak kullanın.",
  {x:M+0.32,y:5.56,w:11.4,h:0.9,fontFace:BODY,fontSize:14,color:INK,margin:0});
s.addNotes("472 adet 1+0 — hacim burada. 16'şar adetlik bahçeli tipler kıt, gerçekten sınırlı; 'sınırlı sayıda' derken bunu kastedin.");

/* ------------------------------------------------------------ 6 yaşam */
s = p.addSlide();
s.background={color:PAPER};
s.addImage({path:im("avlu.jpg"),x:0,y:0,w:5.3,h:HT,sizing:{type:"cover",w:5.3,h:HT}});
s.addText("SOSYAL YAŞAM",{x:5.85,y:0.7,w:6.5,h:0.3,fontFace:BODY,fontSize:12,bold:true,
  color:OCEAN,charSpacing:2.6,margin:0});
s.addText("Merkezi avlu çevresinde hayat",{x:5.85,y:1.04,w:6.8,h:0.75,fontFace:H1,
  fontSize:29,bold:true,color:INK,margin:0});
const olanak=["Merkezi avlu","Dekoratif süs havuzları","Geniş peyzaj alanları",
  "Yürüyüş ve dinlenme yolları","Bahçeli zemin daireler","Özel gece aydınlatması",
  "Kapalı otopark","7/24 güvenlik"];
olanak.forEach((o,i)=>{
  const x=5.85+(i%2)*3.45, y=2.1+Math.floor(i/2)*0.86;
  circle(s,x,y,0.34,i%2?OCEAN:DEEP,"·",WHITE,20);
  s.addText(o,{x:x+0.5,y:y-0.02,w:2.95,h:0.42,fontFace:BODY,fontSize:13.5,color:INK,margin:0});
});
card(s,5.85,5.85,6.8,0.95,ICE);
s.addText("Avludaki su süs havuzudur; yüzme havuzu olarak anlatmayın.",
  {x:6.12,y:6.06,w:6.3,h:0.55,fontFace:BODY,fontSize:12.5,bold:true,color:DEEP,margin:0});
s.addNotes("ÖNEMLİ: Süs havuzu ile yüzme havuzunu karıştırmayın. Müşteriye yüzme havuzu sözü verilirse teslimde sorun çıkar.");

/* ------------------------------------------------------------ 7 ödeme */
s = p.addSlide();
dark(s);
s.addText("ÖDEME MODELİ",{x:M,y:0.62,w:9,h:0.3,fontFace:BODY,fontSize:12,bold:true,
  color:CYAN,charSpacing:2.6,margin:0});
s.addText("Banka yok. Faiz yok. Kefil yok.",{x:M,y:0.98,w:11.6,h:0.8,fontFace:H1,
  fontSize:36,bold:true,color:WHITE,margin:0});
const buyuk=[["%0","Faiz / vade farkı"],["60","Ay sabit taksit"],["0","Ara ödeme"]];
buyuk.forEach((b,i)=>{
  const x=M+i*4.05;
  s.addText(b[0],{x,y:2.05,w:3.7,h:1.15,fontFace:H1,fontSize:62,bold:true,color:CORAL,margin:0});
  s.addText(b[1],{x,y:3.2,w:3.7,h:0.34,fontFace:BODY,fontSize:14,color:ICE,margin:0});
});
const odeme=[["Tasarrufa dayalı finansman","Tasarruf esaslı, faizsiz bir model. Bankaya ve kefile gerek yok."],
  ["Sabit taksit","Bugün belirlenen taksit 60 ay boyunca aynı kalır. Balon taksit yok."],
  ["Enflasyon avantajı","Taksit sabit kaldığı için ödemenin gerçek yükü ay ay hafifler."],
  ["Üye maliyetine konut","Kooperatif kâr amacı gütmez; araya müteahhit kârı girmez."]];
odeme.forEach((o,i)=>{
  const x=M+(i%2)*6.1, y=4.05+Math.floor(i/2)*1.42;
  s.addShape(p.ShapeType.roundRect,{x,y,w:5.85,h:1.24,rectRadius:0.09,
    fill:{color:WHITE,transparency:88},line:{color:CYAN,width:0.75,transparency:55}});
  s.addText(o[0],{x:x+0.28,y:y+0.16,w:5.3,h:0.32,fontFace:BODY,fontSize:14,bold:true,color:WHITE,margin:0});
  s.addText(o[1],{x:x+0.28,y:y+0.5,w:5.35,h:0.62,fontFace:BODY,fontSize:11.5,color:ICE,margin:0});
});
s.addNotes("Sunumun kalbi bu slayt. Emlakçı buradan tek cümle götürsün: 'Bankaya gitmeden, faiz ödemeden, kefil bulmadan ev.' Kredi çıkmayan müşteri sizin müşteriniz.");

/* ------------------------------------------------------------ 8 yatırım */
s = p.addSlide();
head(s,"YATIRIM","MİA Bölgesi'nde m² değeri");
s.addChart(p.ChartType.bar,[{name:"₺/m²",labels:["2026","2027","2028","2029","2030","2031"],
  values:[89000,111250,139063,173828,217285,271606]}],
  {x:M,y:1.92,w:7.5,h:4.05,barDir:"col",chartColors:[DEEP],
   showTitle:true,title:"Yıllık %25 artış varsayımıyla beş yıllık projeksiyon (₺/m²)",
   titleFontFace:BODY,titleFontSize:11,titleColor:GREY,
   showValue:true,dataLabelPosition:"outEnd",dataLabelFontFace:BODY,dataLabelFontSize:9.5,
   dataLabelColor:INK,dataLabelFormatCode:"#,##0",
   catAxisLabelFontFace:BODY,catAxisLabelFontSize:11,catAxisLabelColor:GREY,
   valAxisHidden:true,catGridLine:{style:"none"},valGridLine:{color:"E3EEF2",size:1},
   showLegend:false,barGapWidthPct:55});
const yat=[["89.000 ₺","bugünkü m² birim fiyatı"],["%25","yıllık öngörülen artış"],["×3","beş yıl sonra değer"]];
yat.forEach((y,i)=>{
  const yy=1.98+i*1.4;
  card(s,8.5,yy,4.18,1.2);
  s.addText(y[0],{x:8.78,y:yy+0.14,w:3.7,h:0.52,fontFace:H1,fontSize:26,bold:true,color:DEEP,margin:0});
  s.addText(y[1],{x:8.78,y:yy+0.7,w:3.7,h:0.36,fontFace:BODY,fontSize:12,color:GREY,margin:0});
});
s.addText("Projeksiyon %25 yıllık artış varsayımına dayalı bir öngörüdür; kesin değer taahhüdü değildir.",
  {x:8.5,y:6.2,w:4.2,h:0.6,fontFace:BODY,fontSize:10,italic:true,color:GREY,margin:0});
s.addNotes("Rakamı verirken 'öngörü' kelimesini mutlaka kullanın. Taahhüt gibi anlatılırsa hem etik hem hukuki sorun olur.");

/* ------------------------------------------------------------ 9 güvence */
s = p.addSlide();
head(s,"GÜVENCE","Kooperatif devlet denetiminde");
const guv=[["1163 sayılı Kanun","Kuruluştan tasfiyeye kadar her şey 1969'dan beri yürürlükteki Kooperatifler Kanunu ile tanımlı."],
  ["e-Devlet / KOOPBİS","Ana sözleşme, organlar, genel kurul kararları ve ortaklık kaydı e-Devlet'ten görülebilir."],
  ["Bakanlık temsilcisi","Genel kurul, Bakanlık tarafından görevlendirilen temsilci gözetiminde yapılır."],
  ["Çok katmanlı denetim","İçeride ortakların seçtiği denetim organı, dışarıda bağımsız dış denetim ve Bakanlık yetkisi."]];
guv.forEach((g,i)=>{
  const x=M+(i%2)*6.1, y=2.0+Math.floor(i/2)*2.1;
  card(s,x,y,5.85,1.85);
  circle(s,x+0.3,y+0.3,0.5,DEEP,String(i+1));
  s.addText(g[0],{x:x+0.98,y:y+0.28,w:4.6,h:0.36,fontFace:H1,fontSize:17,bold:true,color:INK,margin:0});
  s.addText(g[1],{x:x+0.98,y:y+0.72,w:4.6,h:0.95,fontFace:BODY,fontSize:12,color:GREY,margin:0});
});
s.addText("Genel bilgilendirmedir; güncel mevzuat ve kooperatif ana sözleşmesi esastır.",
  {x:M,y:6.42,w:9,h:0.32,fontFace:BODY,fontSize:10,italic:true,color:GREY,margin:0});
s.addNotes("Emlakçının en çok takıldığı yer burası. 'Kooperatif riskli mi?' sorusuna dört maddeyle cevap verin. KOOPBİS'i telefonda canlı gösterin, en ikna edici hamle bu.");

/* ---------------------------------------------------------- 10 itirazlar */
s = p.addSlide();
head(s,"SAHA","Dört itiraz, dört cevap");
const itr=[["\"Kooperatif riskli.\"","1163 sayılı Kanun kapsamında, KOOPBİS'ten izlenebilir, genel kurulu Bakanlık temsilcisi gözetiminde."],
  ["\"Kredim çıkmıyor.\"","Zaten bankaya gitmiyoruz. Ne kredi, ne faiz, ne kefil."],
  ["\"Taksit sonradan artar mı?\"","Hayır. Bugün belirlenen taksit 60 ay sabit; ara ödeme ve balon taksit yok."],
  ["\"Tapuyu ne zaman alırım?\"","İnşaat tamamlandıktan sonra ferdileşme ile daire adınıza tapuya bağlanır."]];
itr.forEach((t,i)=>{
  const y=1.95+i*1.24;
  card(s,M,y,12.06,1.08);
  s.addText(t[0],{x:M+0.3,y:y+0.16,w:3.9,h:0.76,valign:"middle",fontFace:H1,fontSize:15,
    bold:true,italic:true,color:DEEP,margin:0});
  s.addText(t[1],{x:M+4.35,y:y+0.16,w:7.4,h:0.76,valign:"middle",fontFace:BODY,fontSize:12.5,
    color:INK,margin:0});
});
s.addNotes("Bu slaydı fotoğraflatın. Sahada en çok gelen dört itiraz ve cevapları. Cevapları ezberden değil, kendi cümlelerinizle söyleyin.");

/* --------------------------------------------------------- 11 hedef kitle */
s = p.addSlide();
s.background={color:PAPER};
s.addImage({path:im("salon.jpg"),x:7.9,y:0,w:5.4,h:HT,sizing:{type:"cover",w:5.4,h:HT}});
s.addText("HEDEF KİTLE",{x:M,y:0.7,w:6.5,h:0.3,fontFace:BODY,fontSize:12,bold:true,
  color:OCEAN,charSpacing:2.6,margin:0});
s.addText("Kimi getireceksiniz?",{x:M,y:1.04,w:6.6,h:0.72,fontFace:H1,fontSize:31,
  bold:true,color:INK,margin:0});
const kitle=[["İlk evini alan","Peşinatı olan ama kredisi çıkmayan genç alıcı","1+0"],
  ["Yatırımcı","Kiralamak ve değerlenme bekleyen küçük yatırımcı","1+0 · 1+1"],
  ["Küçük aile","Çift ya da tek çocuklu aile","1+1"],
  ["Bahçe isteyen","Apartmanda müstakil ev hissi arayan","Bahçe Loft · Dubleks"]];
kitle.forEach((k,i)=>{
  const y=2.05+i*1.2;
  card(s,M,y,6.85,1.04);
  s.addText(k[0],{x:M+0.28,y:y+0.14,w:2.5,h:0.32,fontFace:H1,fontSize:15,bold:true,color:INK,margin:0});
  s.addText(k[1],{x:M+0.28,y:y+0.5,w:4.3,h:0.42,fontFace:BODY,fontSize:11.5,color:GREY,margin:0});
  s.addShape(p.ShapeType.roundRect,{x:M+4.85,y:y+0.3,w:1.82,h:0.44,rectRadius:0.22,fill:{color:ICE}});
  s.addText(k[2],{x:M+4.85,y:y+0.3,w:1.82,h:0.44,align:"center",valign:"middle",
    fontFace:BODY,fontSize:10.5,bold:true,color:DEEP,margin:0});
});
s.addNotes("Portföyünüzdeki kredisi çıkmayan müşterileri hatırlayın — bu projenin asıl hedefi onlar. Reddedilen kredi başvurusu burada satışa dönüyor.");

/* --------------------------------------------------------- 12 destek */
s = p.addSlide();
head(s,"SATIŞ DESTEĞİ","Elinize ne veriyoruz");
const destek=[["Bilbord ve saha panosu","Sekiz farklı tasarım, baskıya hazır"],
  ["Roll-up ve totem","Ofisiniz ve stant için"],
  ["Dijital katalog","Daire planları ve teknik bilgiler"],
  ["miaparkocean.com","Karekodla açılan tanıtım sitesi"],
  ["Sosyal medya seti","Hazır gönderi ve reels içerikleri"],
  ["Tanıtım filmi","Proje tanıtım videosu"]];
destek.forEach((d,i)=>{
  const x=M+(i%3)*4.06, y=2.0+Math.floor(i/3)*2.05;
  card(s,x,y,3.8,1.8);
  circle(s,x+0.3,y+0.3,0.5,i%2?OCEAN:DEEP,String(i+1));
  s.addText(d[0],{x:x+0.3,y:y+0.92,w:3.2,h:0.36,fontFace:H1,fontSize:15,bold:true,color:INK,margin:0});
  s.addText(d[1],{x:x+0.3,y:y+1.28,w:3.24,h:0.4,fontFace:BODY,fontSize:11.5,color:GREY,margin:0});
});
card(s,M,6.15,12.06,0.85,ICE);
s.addText("Tüm görseller baskıya hazır dosya olarak paylaşılır; kendi logonuzu ekleyeceğiniz alanlar bırakılmıştır.",
  {x:M+0.32,y:6.32,w:11.4,h:0.5,fontFace:BODY,fontSize:12.5,color:INK,margin:0});
s.addNotes("Somut olun: hangi dosyayı ne zaman göndereceğinizi söyleyin. Emlakçı eli boş dönmesin — bugün en az katalog ve site linkini verin.");

/* --------------------------------------------------------- 13 iş birliği */
s = p.addSlide();
head(s,"İŞ BİRLİĞİ","Nasıl çalışıyoruz");
const adim=[["Kayıt","Emlakçı kaydı ve yetki belgesi"],
  ["Müşteri bildirimi","Müşteri ofise gelmeden önce bildirilir"],
  ["Görüşme","Satış ofisinde birlikte ya da bizim tarafımızdan"],
  ["Sözleşme","Ortaklık işlemleri ve peşinat"],
  ["Hakediş","Komisyon ödemesi"]];
adim.forEach((a,i)=>{
  const x=M+i*2.44;
  circle(s,x+0.85,2.05,0.62,DEEP,String(i+1),WHITE,16);
  s.addText(a[0],{x:x,y:2.85,w:2.3,h:0.36,align:"center",fontFace:H1,fontSize:14.5,
    bold:true,color:INK,margin:0});
  s.addText(a[1],{x:x,y:3.24,w:2.32,h:0.75,align:"center",fontFace:BODY,fontSize:11,
    color:GREY,margin:0});
});
card(s,M,4.35,12.06,2.15,ICE);
s.addText("Doldurulacak",{x:M+0.34,y:4.55,w:5,h:0.3,fontFace:BODY,fontSize:11,bold:true,
  color:CORAL,charSpacing:2.2,margin:0});
s.addText([{text:"Komisyon oranı:  ______",options:{bullet:true,breakLine:true}},
  {text:"Hakediş zamanı:  ______",options:{bullet:true,breakLine:true}},
  {text:"Müşteri bildirim / koruma süresi:  ______",options:{bullet:true}}],
  {x:M+0.34,y:4.9,w:11.3,h:1.4,fontFace:BODY,fontSize:14,color:INK,
   paraSpaceAfter:6,margin:0});
s.addNotes("DİKKAT: Komisyon oranı, hakediş zamanı ve müşteri koruma süresi bu sunumda boş bırakıldı — bu üç rakamı sunumdan önce siz doldurun. Emlakçının en çok merak ettiği slayt bu; boş kalırsa güven kaybı olur.");

/* --------------------------------------------------------- 14 süreç */
s = p.addSlide();
s.background={color:PAPER};
s.addImage({path:im("deniz.jpg"),x:0,y:0,w:W,h:2.75,sizing:{type:"cover",w:W,h:2.75}});
s.addShape(p.ShapeType.rect,{x:0,y:0,w:W,h:2.75,fill:{color:INK,transparency:45}});
s.addText("MÜŞTERİ SÜRECİ",{x:M,y:0.75,w:9,h:0.3,fontFace:BODY,fontSize:12,bold:true,
  color:CYAN,charSpacing:2.6,margin:0});
s.addText("Peşinattan tapuya",{x:M,y:1.1,w:9,h:0.8,fontFace:H1,fontSize:34,bold:true,
  color:WHITE,margin:0});
const sur=[["Peşinat","Avantajlı peşinatla başlar, kalan tutar 60 aya kadar taksitlenir."],
  ["60 ay taksit","Faiz yok, kefil yok, banka yok. Sabit taksit, ara ödeme yok."],
  ["İnşaat ve takip","Ödemeler ve inşaat aşamaları KOOPBİS ve ilerleme panelinden izlenir."],
  ["Tapu","İnşaat bitince ferdileşme ile daire adına tapuya bağlanır."]];
sur.forEach((t,i)=>{
  const x=M+i*3.05;
  card(s,x,3.35,2.78,2.6);
  circle(s,x+0.28,3.62,0.54,i<2?DEEP:OCEAN,String(i+1));
  s.addText(t[0],{x:x+0.28,y:4.32,w:2.3,h:0.36,fontFace:H1,fontSize:16,bold:true,color:INK,margin:0});
  s.addText(t[1],{x:x+0.28,y:4.72,w:2.32,h:1.1,fontFace:BODY,fontSize:11.5,color:GREY,margin:0});
});
s.addNotes("Süreci dört adımda anlatın. Tapu sorusu mutlaka gelir; ferdileşme kelimesini kullanın ve inşaat bitiminde olduğunu net söyleyin.");

/* --------------------------------------------------------- 15 kapanış */
s = p.addSlide();
dark(s);
s.addImage({path:im("logo-beyaz.png"),x:M,y:0.85,w:2.6,h:1.78});
s.addText("Yarın sabah ilk müşterinizi getirin.",{x:M,y:3.02,w:8.2,h:1.42,fontFace:H1,
  fontSize:38,bold:true,color:WHITE,margin:0});
s.addText("Satış ofisimiz her gün açık. Kahvemizi içmeye bekleriz.",
  {x:M,y:4.6,w:8.2,h:0.42,fontFace:BODY,fontSize:16,color:ICE,margin:0});
s.addText([{text:"0540 028 00 41   ·   0541 128 40 41",options:{breakLine:true}},
  {text:"miaparkocean.com   ·   @miaparkocean",options:{breakLine:true}},
  {text:"OCEAN GAYRİMENKUL  ·  Tek Yetkili Satıcı",options:{}}],
  {x:M,y:5.35,w:8.2,h:1.3,fontFace:BODY,fontSize:14,color:WHITE,lineSpacingMultiple:1.5,margin:0});
s.addShape(p.ShapeType.roundRect,{x:9.9,y:3.35,w:2.78,h:2.78,rectRadius:0.12,fill:{color:WHITE}});
s.addImage({path:im("qr.png"),x:10.14,y:3.59,w:2.3,h:2.3});
s.addText("Projeyi telefonunuzda açın",{x:9.9,y:6.24,w:2.78,h:0.32,align:"center",
  fontFace:BODY,fontSize:11,color:CYAN,margin:0});
s.addNotes("Kapanış: net bir çağrı yapın. Kayıt formunu masalara dağıtın, bugün kaydolan emlakçıya katalog ve görsel setini akşam gönderin.");

p.writeFile({ fileName: path.join(__dirname, "..", "sunum",
  "MIA-PARK-OCEAN-Lansman-Sunumu.pptx") })
 .then(f => console.log("yazildi:", f));
