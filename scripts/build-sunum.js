const pptxgen = require("pptxgenjs");
const path = require("path");
const IMG = process.env.MIA_SUNUM_IMG || path.join(__dirname, "..", "sunum", "kaynak");
const im = (n) => path.join(IMG, n);

const INK="04283A", DEEP="075878", OCEAN="1A7496", CYAN="48ABC5",
      ICE="DDF7FA", PAPER="F5FAFC", WHITE="FFFFFF", CORAL="F2704B", GREY="5A6B75";
const H1="Cambria", BODY="Calibri";
const W=13.33, HT=7.5, M=0.62;
const TOP=0.55, BOT=6.95;               // içerik bu iki çizgi arasını DOLDURUR

const p = new pptxgen();
p.layout = "LAYOUT_WIDE";
p.author = "Ocean Gayrimenkul";
p.company = "MİA PARK OCEAN";
p.title = "MİA PARK OCEAN — Lansman Sunumu";

const sh = () => ({type:"outer",color:"04283A",blur:16,offset:4,angle:90,opacity:0.16});

/* tam kanama fotoğraf + perde */
function bleed(s, pic, perde="perde-alt"){
  s.addImage({path:im(pic),x:0,y:0,w:W,h:HT,sizing:{type:"cover",w:W,h:HT}});
  s.addImage({path:im(perde+".png"),x:0,y:0,w:W,h:HT});
}
/* yarım kanama: fotoğraf bir yanda, tepeden dibe */
function half(s, pic, side="left", w=5.55){
  const x = side==="left" ? 0 : W-w;
  s.addImage({path:im(pic),x,y:0,w,h:HT,sizing:{type:"cover",w,h:HT}});
}
function kicker(s,t,x,y,color,w){
  s.addText(t,{x,y,w:Math.min(w||6.4, 13.33-x-0.4),h:0.28,fontFace:BODY,fontSize:11.5,bold:true,
    color:color||OCEAN,charSpacing:2.8,margin:0});
}
function title(s,t,x,y,color,size,w){
  s.addText(t,{x,y,w:w||7.2,h:0.9,fontFace:H1,fontSize:size||33,bold:true,
    color:color||INK,margin:0});
}
function card(s,x,y,w,h,fill,line){
  const o={x,y,w,h,rectRadius:0.1,fill:{color:fill||WHITE},shadow:sh()};
  if(line) o.line=line;
  s.addShape(p.ShapeType.roundRect,o);
}
function dot(s,x,y,d,fill,txt,color,size){
  s.addShape(p.ShapeType.ellipse,{x,y,w:d,h:d,fill:{color:fill}});
  s.addText(txt,{x,y,w:d,h:d,align:"center",valign:"middle",fontFace:BODY,
    fontSize:size||13,bold:true,color:color||WHITE,margin:0});
}

/* =============================================================== 1 KAPAK */
let s = p.addSlide();
bleed(s,"gece.jpg","perde-alt");
s.addImage({path:im("logo-beyaz.png"),x:M,y:0.45,w:2.5,h:1.72});
kicker(s,"LANSMAN · İŞ ORTAKLARI SUNUMU",M,3.62,CYAN);
s.addText("Lüks artık ulaşılabilir.",{x:M,y:3.98,w:10,h:1.05,fontFace:H1,fontSize:48,
  bold:true,color:WHITE,margin:0});
s.addText("İzmit MİA Bölgesi'nde 600 daire  ·  Tasarrufa dayalı faizsiz finansman",
  {x:M,y:5.08,w:10,h:0.42,fontFace:BODY,fontSize:17,color:ICE,margin:0});
s.addShape(p.ShapeType.roundRect,{x:M,y:5.85,w:4.55,h:0.62,rectRadius:0.31,
  fill:{color:WHITE,transparency:82},line:{color:CYAN,width:0.75,transparency:40}});
s.addText("21 Ağustos 2026  ·  Emex Otel, Kocaeli",{x:M,y:5.85,w:4.55,h:0.62,
  align:"center",valign:"middle",fontFace:BODY,fontSize:13,bold:true,color:WHITE,margin:0});
s.addText("S.S. Yahya Kaptan Birlik Yapı Kooperatifi   ·   Ocean Gayrimenkul, Tek Yetkili Satıcı",
  {x:M,y:6.68,w:10,h:0.3,fontFace:BODY,fontSize:11,color:CYAN,margin:0});
s.addNotes("Açılış. Kendinizi ve kooperatifi tanıtın. Sunum 20 dakika, sonrasında soru-cevap. Bugünün amacı: MİA PARK OCEAN'ı satabilecek kadar iyi anlatmak.");

/* ============================================================== 2 GÜNDEM */
s = p.addSlide();
s.background={color:PAPER};
half(s,"hava.jpg","left",5.2);
kicker(s,"BUGÜN",5.85,TOP+0.12);
title(s,"Yirmi dakikada altı başlık",5.85,TOP+0.46,INK,30,7.0);
const gundem=[["Proje","600 daire, dört yaşam tipi"],["Konum","D100'e 1 dk, merkeze 5 dk"],
 ["Ödeme","Banka yok, faiz yok, kefil yok"],["Yatırım","m² fiyatı ve beş yıllık projeksiyon"],
 ["Güvence","Kooperatif neden devlet denetiminde"],["İş birliği","Size ne veriyoruz"]];
gundem.forEach((g,i)=>{
  const y=1.92+i*0.85;
  dot(s,5.85,y+0.06,0.44,i<3?DEEP:OCEAN,String(i+1),WHITE,12);
  s.addText(g[0],{x:6.48,y:y-0.02,w:2.5,h:0.34,fontFace:H1,fontSize:16,bold:true,color:INK,margin:0});
  s.addText(g[1],{x:9.0,y:y+0.02,w:3.7,h:0.34,fontFace:BODY,fontSize:12.5,color:GREY,margin:0});
});
s.addNotes("Gündemi hızlı geçin. Vurgu 3. ve 6. başlıkta: ödeme modeli ve iş birliği. Emlakçı bu ikisini anlarsa gerisi kolay.");

/* ============================================================== 3 KÜNYE */
s = p.addSlide();
bleed(s,"gunduz.jpg","perde-yari");
kicker(s,"PROJE KÜNYESİ",M,0.62,CYAN);
title(s,"600 daire, dört yaşam tipi",M,0.98,WHITE,36,9);
const st=[["600","Toplam daire"],["4","Yaşam tipi"],["28–100","m² brüt"],["60","Ay sabit taksit"]];
st.forEach((t,i)=>{
  const x=M+i*3.05;
  s.addText(t[0],{x,y:4.45,w:2.8,h:0.95,fontFace:H1,fontSize:t[0].length>3?38:48,
    bold:true,color:WHITE,margin:0});
  s.addText(t[1],{x,y:5.42,w:2.8,h:0.32,fontFace:BODY,fontSize:12.5,color:ICE,margin:0});
});
s.addText("S.S. Yahya Kaptan Birlik Yapı Kooperatifi   ·   Ocean Gayrimenkul, Tek Yetkili Satıcı   ·   İzmit MİA Bölgesi",
  {x:M,y:6.42,w:12.1,h:0.32,fontFace:BODY,fontSize:12,color:ICE,margin:0});
s.addNotes("600 rakamını vurgulayın: emlakçı için sürekli stok demek. Dört tip, her müşteri profiline bir cevap.");

/* ============================================================== 4 KONUM */
s = p.addSlide();
s.background={color:PAPER};
half(s,"sokak.jpg","right",5.2);
kicker(s,"KONUM",M,TOP+0.12);
title(s,"Her yere yakın",M,TOP+0.46,INK,30,6.4);
const mes=[["D100 Karayolu","1 dk"],["İzmit Sahili","2 dk"],["41 Burada AVM","3 dk"],
 ["Şehir Merkezi","5 dk"],["Şehir Hastanesi","5 dk"],["TEM Otoyolu","5 dk"],
 ["Symbol AVM","7 dk"],["Kocaeli Üniversitesi","10 dk"]];
mes.forEach((d,i)=>{
  const x=M+(i%2)*3.55, y=1.95+Math.floor(i/2)*1.03;
  card(s,x,y,3.32,0.84);
  s.addText(d[0],{x:x+0.24,y:y,w:1.9,h:0.84,valign:"middle",fontFace:BODY,fontSize:11.5,color:INK,margin:0});
  s.addText(d[1],{x:x+2.02,y:y,w:1.1,h:0.84,valign:"middle",align:"right",fontFace:H1,
    fontSize:18,bold:true,color:DEEP,margin:0});
});
s.addText("İzmit'in gelişim aksı MİA Bölgesi. Üniversite, hastane, AVM ve ana yollar dakikalar içinde.",
  {x:M,y:6.18,w:6.9,h:0.62,fontFace:BODY,fontSize:12.5,italic:true,color:GREY,margin:0});
s.addNotes("Mesafeleri ezberleyin; en çok D100 ve şehir hastanesi sorulur. İzmit Sahili süresi teyide açık, kesin konuşmayın.");

/* =============================================================== 5 STOK */
s = p.addSlide();
s.background={color:PAPER};
["studyo.jpg","salon.jpg","teras.jpg","dubleks.jpg"].forEach((f,i)=>{
  s.addImage({path:im(f),x:i*3.3325,y:0,w:3.3325,h:2.5,sizing:{type:"cover",w:3.3325,h:2.5}});
});
s.addImage({path:im("perde-yatay.png"),x:0,y:0,w:W,h:2.5});
kicker(s,"STOK",M,0.55,CYAN);
title(s,"Dört tip, 600 daire",M,0.9,WHITE,32,8);
const tip=[["1+0","472","Brüt 28 m²","İlk ev ve yatırım"],["1+1","96","Brüt 50 m²","Çift ve küçük aile"],
 ["1+1 Bahçe Loft","16","Brüt 50 m²","Zeminde kendi bahçesi"],["2+1 Bahçe Dubleks","16","Brüt 100 m²","Bahçeli dubleks"]];
tip.forEach((t,i)=>{
  const x=M+i*3.05;
  card(s,x,2.85,2.8,2.55);
  s.addText(t[0],{x:x+0.24,y:3.02,w:2.35,h:0.42,fontFace:H1,fontSize:t[0].length>6?13.5:18,
    bold:true,color:DEEP,margin:0});
  s.addText(t[1],{x:x+0.24,y:3.52,w:2.35,h:0.78,fontFace:H1,fontSize:38,bold:true,color:INK,margin:0});
  s.addText("adet",{x:x+0.24,y:4.3,w:2.35,h:0.28,fontFace:BODY,fontSize:11,color:GREY,margin:0});
  s.addText(t[2],{x:x+0.24,y:4.63,w:2.35,h:0.3,fontFace:BODY,fontSize:12.5,bold:true,color:OCEAN,margin:0});
  s.addText(t[3],{x:x+0.24,y:4.96,w:2.4,h:0.32,fontFace:BODY,fontSize:11,color:GREY,margin:0});
});
card(s,M,5.62,12.09,1.28,ICE);
s.addText("Stokun %79'u 1+0 — hacim orada, kampanyayı oraya kurun. Bahçeli tipler toplam 32 adet; aciliyet argümanınız bu.",
  {x:M+0.34,y:5.62,w:11.4,h:1.28,valign:"middle",fontFace:BODY,fontSize:13.5,color:INK,margin:0});
s.addNotes("472 adet 1+0 — hacim burada. 16'şar adetlik bahçeli tipler gerçekten kıt; 'sınırlı sayıda' derken bunu kastedin.");

/* ============================================================== 6 YAŞAM */
s = p.addSlide();
s.background={color:PAPER};
[["sus.jpg",0,0],["yuruyus.jpg",1,0],["oyun.jpg",0,1],["otopark.jpg",1,1]].forEach(([f,cx,cy])=>{
  s.addImage({path:im(f),x:cx*3.05,y:cy*3.75,w:3.05,h:3.75,sizing:{type:"cover",w:3.05,h:3.75}});
});
kicker(s,"SOSYAL YAŞAM",6.5,TOP+0.12);
title(s,"Merkezi avlu çevresinde hayat",6.5,TOP+0.46,INK,29,6.3);
const ol=["Merkezi avlu","Dekoratif süs havuzları","Geniş peyzaj alanları","Yürüyüş ve dinlenme yolları",
 "Bahçeli zemin daireler","Özel gece aydınlatması","Kapalı otopark","7/24 güvenlik"];
ol.forEach((o,i)=>{
  const y=2.0+i*0.53;
  dot(s,6.5,y+0.04,0.26,i%2?OCEAN:DEEP,"·",WHITE,15);
  s.addText(o,{x:6.92,y:y-0.03,w:5.8,h:0.38,fontFace:BODY,fontSize:14,color:INK,margin:0});
});
card(s,6.5,6.28,6.2,0.72,ICE);
s.addText("Avludaki su SÜS havuzudur — yüzme havuzu diye anlatmayın.",
  {x:6.5,y:6.28,w:6.2,h:0.72,align:"center",valign:"middle",fontFace:BODY,fontSize:12.5,
   bold:true,color:DEEP,margin:0});
s.addNotes("ÖNEMLİ: Süs havuzu ile yüzme havuzunu karıştırmayın. Yüzme havuzu sözü verilirse teslimde sorun çıkar.");

/* ============================================================= 7 ÖDEME */
s = p.addSlide();
bleed(s,"gece.jpg","perde-tam");
kicker(s,"ÖDEME MODELİ",M,0.58,CYAN);
title(s,"Banka yok. Faiz yok. Kefil yok.",M,0.92,WHITE,36,11.5);
const bk=[["%0","Faiz / vade farkı"],["60","Ay sabit taksit"],["0","Ara ödeme"]];
bk.forEach((b,i)=>{
  const x=M+i*4.08;
  s.addText(b[0],{x,y:2.0,w:3.8,h:1.2,fontFace:H1,fontSize:66,bold:true,color:CORAL,margin:0});
  s.addText(b[1],{x,y:3.2,w:3.8,h:0.34,fontFace:BODY,fontSize:14,color:ICE,margin:0});
});
const od=[["Tasarrufa dayalı finansman","Tasarruf esaslı, faizsiz model. Bankaya ve kefile gerek yok."],
 ["Sabit taksit","Bugün belirlenen taksit 60 ay aynı kalır. Balon taksit yok."],
 ["Enflasyon avantajı","Taksit sabit kaldığı için ödemenin gerçek yükü ay ay hafifler."],
 ["Üye maliyetine konut","Kooperatif kâr amacı gütmez; araya müteahhit kârı girmez."]];
od.forEach((o,i)=>{
  const x=M+(i%2)*6.15, y=4.05+Math.floor(i/2)*1.45;
  s.addShape(p.ShapeType.roundRect,{x,y,w:5.88,h:1.28,rectRadius:0.1,
    fill:{color:WHITE,transparency:86},line:{color:CYAN,width:0.75,transparency:50}});
  s.addText(o[0],{x:x+0.3,y:y+0.16,w:5.3,h:0.32,fontFace:BODY,fontSize:14,bold:true,color:WHITE,margin:0});
  s.addText(o[1],{x:x+0.3,y:y+0.52,w:5.35,h:0.62,fontFace:BODY,fontSize:11.5,color:ICE,margin:0});
});
s.addNotes("Sunumun kalbi. Emlakçı buradan tek cümle götürsün: bankaya gitmeden, faiz ödemeden, kefil bulmadan ev. Kredisi çıkmayan müşteri sizin müşteriniz.");

/* ============================================================ 8 YATIRIM */
s = p.addSlide();
s.background={color:PAPER};
half(s,"cephe.jpg","right",4.5);
s.addImage({path:im("perde-sol.png"),x:8.83,y:0,w:4.5,h:HT});
kicker(s,"YATIRIM",M,TOP+0.12);
title(s,"MİA Bölgesi'nde m² değeri",M,TOP+0.46,INK,30,7.4);
s.addChart(p.ChartType.bar,[{name:"₺/m²",labels:["2026","2027","2028","2029","2030","2031"],
  values:[89000,111250,139063,173828,217285,271606]}],
 {x:M-0.1,y:1.9,w:8.2,h:3.5,barDir:"col",chartColors:[DEEP],
  showValue:true,dataLabelPosition:"outEnd",dataLabelFontFace:BODY,dataLabelFontSize:9,
  dataLabelColor:INK,dataLabelFormatCode:"#,##0",
  catAxisLabelFontFace:BODY,catAxisLabelFontSize:11,catAxisLabelColor:GREY,
  valAxisHidden:true,catGridLine:{style:"none"},valGridLine:{color:"E3EEF2",size:1},
  showLegend:false,barGapWidthPct:52});
const ya=[["89.000 ₺","bugünkü m² fiyatı"],["%25","yıllık öngörü"],["×3","beş yılda"]];
ya.forEach((y,i)=>{
  const x=M+i*2.72;
  card(s,x,5.5,2.5,1.0);
  s.addText(y[0],{x:x+0.2,y:5.62,w:2.1,h:0.44,fontFace:H1,fontSize:20,bold:true,color:DEEP,margin:0});
  s.addText(y[1],{x:x+0.2,y:6.06,w:2.15,h:0.32,fontFace:BODY,fontSize:10.5,color:GREY,margin:0});
});
s.addText("Beş yıllık projeksiyon %25 yıllık artış varsayımına dayalı bir ÖNGÖRÜDÜR; değer taahhüdü değildir.",
  {x:M,y:6.62,w:8.0,h:0.32,fontFace:BODY,fontSize:9.5,italic:true,color:GREY,margin:0});
s.addNotes("'Öngörü' kelimesini mutlaka kullanın. Taahhüt gibi anlatılırsa hem etik hem hukuki sorun olur.");

/* =========================================================== 9 GÜVENCE */
s = p.addSlide();
s.background={color:PAPER};
half(s,"alacakaranlik.jpg","left",4.6);
kicker(s,"GÜVENCE",5.25,TOP+0.12);
title(s,"Kooperatif devlet denetiminde",5.25,TOP+0.46,INK,28,7.5);
const gv=[["1163 sayılı Kanun","Kuruluştan tasfiyeye kadar her şey 1969'dan beri yürürlükteki kanunla tanımlı."],
 ["e-Devlet / KOOPBİS","Ana sözleşme, genel kurul kararları ve ortaklık kaydı e-Devlet'ten görülebilir."],
 ["Bakanlık temsilcisi","Genel kurul, Bakanlık tarafından görevlendirilen temsilci gözetiminde yapılır."],
 ["Çok katmanlı denetim","İçeride ortakların denetim organı, dışarıda bağımsız dış denetim ve Bakanlık."]];
gv.forEach((g,i)=>{
  const y=1.95+i*1.22;
  card(s,5.25,y,7.45,1.05);
  dot(s,5.5,y+0.28,0.5,DEEP,String(i+1));
  s.addText(g[0],{x:6.2,y:y+0.14,w:6.2,h:0.32,fontFace:H1,fontSize:15,bold:true,color:INK,margin:0});
  s.addText(g[1],{x:6.2,y:y+0.5,w:6.25,h:0.44,fontFace:BODY,fontSize:11,color:GREY,margin:0});
});
s.addText("Genel bilgilendirmedir; güncel mevzuat ve kooperatif ana sözleşmesi esastır.",
  {x:5.25,y:6.76,w:7.45,h:0.28,fontFace:BODY,fontSize:9,italic:true,color:GREY,margin:0});
s.addNotes("Emlakçının en çok takıldığı yer. 'Kooperatif riskli mi?' sorusuna dört maddeyle cevap verin. KOOPBİS'i telefonda canlı gösterin — en ikna edici hamle.");

/* ========================================================= 10 İTİRAZLAR */
s = p.addSlide();
bleed(s,"avlu.jpg","perde-koyu");
kicker(s,"SAHA",M,0.58,CYAN);
title(s,"Dört itiraz, dört cevap",M,0.92,WHITE,34,9);
const it=[["\"Kooperatif riskli.\"","1163 sayılı Kanun kapsamında, KOOPBİS'ten izlenebilir, genel kurulu Bakanlık temsilcisi gözetiminde."],
 ["\"Kredim çıkmıyor.\"","Zaten bankaya gitmiyoruz. Ne kredi, ne faiz, ne kefil."],
 ["\"Taksit sonradan artar mı?\"","Hayır. Bugün belirlenen taksit 60 ay sabit; ara ödeme ve balon taksit yok."],
 ["\"Tapuyu ne zaman alırım?\"","İnşaat tamamlandıktan sonra ferdileşme ile daire adınıza tapuya bağlanır."]];
it.forEach((t,i)=>{
  const y=2.2+i*1.2;
  s.addShape(p.ShapeType.roundRect,{x:M,y,w:12.09,h:1.02,rectRadius:0.1,
    fill:{color:INK,transparency:40},line:{color:CYAN,width:0.75,transparency:55}});
  s.addText(t[0],{x:M+0.32,y,w:3.7,h:1.02,valign:"middle",fontFace:H1,fontSize:14.5,
    bold:true,italic:true,color:CYAN,margin:0});
  s.addText(t[1],{x:M+4.2,y,w:7.6,h:1.02,valign:"middle",fontFace:BODY,fontSize:12.5,
    color:WHITE,margin:0});
});
s.addNotes("Bu slaydı fotoğraflatın. Sahada en çok gelen dört itiraz. Cevapları ezberden değil kendi cümlelerinizle söyleyin.");

/* ======================================================== 11 HEDEF KİTLE */
s = p.addSlide();
s.background={color:INK};
const kit=[["kolon-studyo.jpg","İlk evini alan","Peşinatı olan, kredisi çıkmayan genç alıcı","1+0"],
 ["kolon-salon.jpg","Yatırımcı","Kiralamak ve değerlenme bekleyen","1+0 · 1+1"],
 ["kolon-teras.jpg","Küçük aile","Çift ya da tek çocuklu aile","1+1"],
 ["kolon-dubleks.jpg","Bahçe isteyen","Apartmanda müstakil ev hissi","Bahçe Loft · Dubleks"]];
kit.forEach((k,i)=>{
  const x=i*3.3325;
  s.addImage({path:im(k[0]),x,y:0,w:3.3325,h:HT});
  s.addImage({path:im("perde-dip.png"),x,y:0,w:3.3325,h:HT});
  s.addText(k[1],{x:x+0.3,y:4.62,w:2.75,h:0.42,fontFace:H1,fontSize:18,bold:true,color:WHITE,margin:0});
  s.addText(k[2],{x:x+0.3,y:5.1,w:2.78,h:0.72,fontFace:BODY,fontSize:11.5,color:ICE,margin:0});
  s.addShape(p.ShapeType.roundRect,{x:x+0.3,y:5.95,w:2.7,h:0.44,rectRadius:0.22,fill:{color:CORAL}});
  s.addText(k[3],{x:x+0.3,y:5.95,w:2.7,h:0.44,align:"center",valign:"middle",fontFace:BODY,
    fontSize:10.5,bold:true,color:WHITE,margin:0});
});
s.addShape(p.ShapeType.rect,{x:0,y:0,w:W,h:1.15,fill:{color:INK,transparency:22}});
s.addText("HEDEF KİTLE  ·  KİMİ GETİRECEKSİNİZ",{x:M,y:0.42,w:9,h:0.32,fontFace:BODY,
  fontSize:12,bold:true,color:WHITE,charSpacing:2.8,margin:0});
s.addNotes("Portföyünüzdeki kredisi çıkmayan müşterileri hatırlayın — bu projenin asıl hedefi onlar. Reddedilen kredi başvurusu burada satışa dönüyor.");

/* ========================================================== 12 DESTEK */
s = p.addSlide();
s.background={color:PAPER};
kicker(s,"SATIŞ DESTEĞİ",M,TOP+0.12);
title(s,"Elinize ne veriyoruz",M,TOP+0.46,INK,30,7);
s.addImage({path:im("m-bilbord.jpg"),x:M,y:1.95,w:3.71,h:2.47});
s.addImage({path:im("m-arsa.jpg"),x:M,y:4.58,w:3.71,h:2.47});
s.addImage({path:im("m-rollup.jpg"),x:4.58,y:1.95,w:2.04,h:5.1});
s.addImage({path:im("m-yaka.jpg"),x:6.87,y:1.95,w:1.71,h:2.47});
s.addImage({path:im("m-katalog-01.jpg"),x:6.87,y:4.58,w:1.75,h:2.47});
const dst=["8 bilbord tasarımı","8 arsa panosu","Roll-up ve totem","Yaka kartları",
 "Dijital katalog","miaparkocean.com","Sosyal medya seti","Tanıtım filmi"];
dst.forEach((d,i)=>{
  const y=2.02+i*0.6;
  dot(s,9.05,y+0.05,0.26,i%2?OCEAN:DEEP,"·",WHITE,15);
  s.addText(d,{x:9.45,y:y-0.02,w:3.3,h:0.38,fontFace:BODY,fontSize:13,color:INK,margin:0});
});
s.addText("Hepsi baskıya hazır dosya olarak paylaşılır.",{x:9.05,y:6.9,w:3.7,h:0.3,
  fontFace:BODY,fontSize:10,italic:true,color:GREY,margin:0});
s.addNotes("Somut olun: hangi dosyayı ne zaman göndereceğinizi söyleyin. Emlakçı eli boş dönmesin — bugün en az katalog ve site linkini verin.");

/* ======================================================= 13 İŞ BİRLİĞİ */
s = p.addSlide();
s.background={color:PAPER};
half(s,"loft.jpg","right",4.35);
s.addImage({path:im("perde-sol.png"),x:8.98,y:0,w:4.35,h:HT});
kicker(s,"İŞ BİRLİĞİ",M,TOP+0.12);
title(s,"Nasıl çalışıyoruz",M,TOP+0.46,INK,30,7);
const ad=[["Kayıt","Emlakçı kaydı ve yetki belgesi"],["Müşteri bildirimi","Müşteri ofise gelmeden bildirilir"],
 ["Görüşme","Satış ofisinde birlikte"],["Sözleşme","Ortaklık işlemleri ve peşinat"],["Hakediş","Komisyon ödemesi"]];
ad.forEach((a,i)=>{
  const y=1.92+i*0.78;
  card(s,M,y,7.95,0.66);
  dot(s,M+0.18,y+0.11,0.44,i<3?DEEP:OCEAN,String(i+1),WHITE,12);
  s.addText(a[0],{x:M+0.78,y,w:2.6,h:0.66,valign:"middle",fontFace:H1,fontSize:15,bold:true,color:INK,margin:0});
  s.addText(a[1],{x:M+3.42,y,w:4.35,h:0.66,valign:"middle",fontFace:BODY,fontSize:11.5,color:GREY,margin:0});
});
s.addShape(p.ShapeType.roundRect,{x:M,y:5.88,w:7.95,h:1.12,rectRadius:0.1,
  fill:{color:WHITE},line:{color:CORAL,width:1.5},shadow:sh()});
s.addText("SUNUMDAN ÖNCE DOLDURULACAK",{x:M+0.3,y:6.0,w:6,h:0.28,fontFace:BODY,fontSize:10,
  bold:true,color:CORAL,charSpacing:2.2,margin:0});
s.addText("Komisyon oranı  ______     Hakediş zamanı  ______     Müşteri koruma süresi  ______",
  {x:M+0.3,y:6.36,w:7.4,h:0.42,fontFace:BODY,fontSize:12.5,color:INK,margin:0});
s.addNotes("DİKKAT: Komisyon oranı, hakediş zamanı ve müşteri koruma süresi BOŞ. Bu üç rakamı sunumdan önce doldurun; emlakçının en çok merak ettiği slayt bu, boş kalırsa güven kaybı olur.");

/* =========================================================== 14 SÜREÇ */
s = p.addSlide();
bleed(s,"teras.jpg","perde-tam");
kicker(s,"MÜŞTERİ SÜRECİ",M,0.58,CYAN);
title(s,"Peşinattan tapuya",M,0.92,WHITE,34,9);
const sr=[["Peşinat","Avantajlı peşinatla başlar, kalan tutar 60 aya kadar taksitlenir."],
 ["60 ay taksit","Faiz yok, kefil yok, banka yok. Sabit taksit, ara ödeme yok."],
 ["İnşaat ve takip","Ödemeler ve inşaat aşamaları KOOPBİS ve ilerleme panelinden izlenir."],
 ["Tapu","İnşaat bitince ferdileşme ile daire adına tapuya bağlanır."]];
sr.forEach((t,i)=>{
  const x=M+i*3.05;
  s.addShape(p.ShapeType.roundRect,{x,y:2.5,w:2.8,h:3.5,rectRadius:0.1,
    fill:{color:WHITE,transparency:86},line:{color:CYAN,width:0.75,transparency:50}});
  dot(s,x+0.26,2.76,0.56,i<2?CORAL:OCEAN,String(i+1));
  s.addText(t[0],{x:x+0.26,y:3.52,w:2.3,h:0.4,fontFace:H1,fontSize:17,bold:true,color:WHITE,margin:0});
  s.addText(t[1],{x:x+0.26,y:3.98,w:2.32,h:1.6,fontFace:BODY,fontSize:11.5,color:ICE,margin:0});
});
s.addText("Tapu sorusu mutlaka gelir: ferdileşme, inşaat bitiminde.",{x:M,y:6.32,w:9,h:0.32,
  fontFace:BODY,fontSize:11.5,italic:true,color:CYAN,margin:0});
s.addNotes("Süreci dört adımda anlatın. Tapu sorusu mutlaka gelir; ferdileşme kelimesini kullanın ve inşaat bitiminde olduğunu net söyleyin.");

/* ========================================================= 15 KAPANIŞ */
s = p.addSlide();
bleed(s,"deniz.jpg","perde-tam");
s.addImage({path:im("logo-beyaz.png"),x:M,y:0.75,w:2.5,h:1.72});
s.addText("Yarın sabah ilk müşterinizi getirin.",{x:M,y:3.0,w:8.3,h:1.45,fontFace:H1,
  fontSize:40,bold:true,color:WHITE,margin:0});
s.addText("Satış ofisimiz her gün açık. Kahvemizi içmeye bekleriz.",{x:M,y:4.6,w:8.3,h:0.42,
  fontFace:BODY,fontSize:16,color:ICE,margin:0});
s.addText([{text:"0540 028 00 41   ·   0541 128 40 41",options:{breakLine:true}},
 {text:"miaparkocean.com   ·   @miaparkocean",options:{breakLine:true}},
 {text:"OCEAN GAYRİMENKUL  ·  Tek Yetkili Satıcı",options:{}}],
 {x:M,y:5.35,w:8.3,h:1.35,fontFace:BODY,fontSize:14,color:WHITE,lineSpacingMultiple:1.5,margin:0});
s.addShape(p.ShapeType.roundRect,{x:9.95,y:3.3,w:2.78,h:2.78,rectRadius:0.12,fill:{color:WHITE}});
s.addImage({path:im("qr.png"),x:10.19,y:3.54,w:2.3,h:2.3});
s.addText("Projeyi telefonunuzda açın",{x:9.95,y:6.2,w:2.78,h:0.3,align:"center",
  fontFace:BODY,fontSize:10.5,color:CYAN,margin:0});
s.addNotes("Kapanış: net çağrı yapın. Kayıt formunu dağıtın, bugün kaydolan emlakçıya katalog ve görsel setini akşam gönderin.");

p.writeFile({ fileName: path.join(__dirname, "..", "sunum",
  "MIA-PARK-OCEAN-Lansman-Sunumu.pptx") }).then(f => console.log("yazildi:", f));
