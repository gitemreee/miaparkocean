#!/usr/bin/env python3
"""
MİA PARK OCEAN × TİLDA İNŞAAT — 180 m'lik TEK PARÇA dev pano, 7 tasarım.

Pano 180 m x 8,5 m; baskı için 80 m (A) + 20 m (B) + 80 m (C) olarak
bölünür ama tasarım kesintisizdir: proje görseli ortadadır ve iki ek
yerini (80. ve 100. metre) içinde taşır. Binalar panonun üst kenarından
4,75 m'ye kadar taşar (kesme "extension" parçası).

Görsel: signage-source/entrance-gate.jpg (gerçek 4K render). Gökyüzü
maskesi scripts/gok-maskesi.py ile çıkarıldı → entrance-gate-kesik.png.

Ölçek: 1 CSS px = 1 cm. Tuval 18000 x 1350 (üst 500 = taşma, alt 850 = pano).
Baskı dsf=4 → metre başına 400 px (1:1'de ~10 dpi).

Çıktılar (tabela/mega-bilbord-180m/<no>-<ad>/):
  baski/A-80m.jpg, B-20m.jpg, C-80m.jpg   pano parçaları
  baski/tasma-kesim.png                    üst taşma, şeffaf zeminli
  onizleme.jpg                             gökyüzü üstünde tam görünüm

    python3.13 scripts/build-mega-bilbord.py --onizle [--sadece 1,3]
    python3.13 scripts/build-mega-bilbord.py [--sadece 1,3]
"""

import json
import os
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image, ImageDraw, ImageFont

Image.MAX_IMAGE_PIXELS = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "tabela", "mega-bilbord-180m")
FONT = os.path.join(ROOT, "brand-source", "fonts", "Montserrat-var.ttf")
VEK = os.path.join(ROOT, "public", "brand", "vektor")
HERO = os.path.join(ROOT, "signage-source", "entrance-gate-genis-kesik.png")

TW, EXT, PH = 18000, 500, 850          # tuval genişliği, taşma, pano yüksekliği
TH = EXT + PH
PARCA = [("A-80m", 0, 8000), ("B-20m", 8000, 10000), ("C-80m", 10000, 18000)]

# kahraman yerleşimi — genişletilmiş görsel (entrance-gate-genis, 21:9);
# görsel yüksekliğinin %40,4'ü pano üst kenarı, %94,3'ü pano alt kenarı
UST_FR, ALT_FR = 0.404, 0.943
HERO_ORAN = 3168 / 1344
HH = round(PH / (ALT_FR - UST_FR))
HW = round(HH * HERO_ORAN)
HX = 9000 - HW // 2                    # 90. metreye ortalı
HY = EXT - round(UST_FR * HH)
# taşmaya izin verilen bina sütunları (kahraman genişliğine oran)
SUTUNLAR = [(0.104, 0.444), (0.527, 0.954)]

TILDA_ORAN = 13684 / 2980
MIA_ORAN = 4764 / 3288

CSS = """
@font-face { font-family: Mont; src: url("file://__FONT__"); font-weight: 100 900; }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 18000px; height: 1350px; overflow: hidden; background: transparent; }
body { font-family: Mont, sans-serif; -webkit-font-smoothing: antialiased;
       font-kerning: normal; font-variant-numeric: lining-nums; }
.a { position: absolute; }
.pano { position: absolute; left: 0; top: 500px; width: 18000px; height: 850px; overflow: hidden; }
.tasma { position: absolute; left: 0; top: 0; width: 18000px; height: 500px; overflow: hidden; }
.tek { white-space: nowrap; line-height: 1; }
.kas { font-weight: 600; letter-spacing: .3em; }
.altin { background: linear-gradient(180deg, #ffe7a8 0%, #e2b45c 45%, #b07a2c 100%);
         -webkit-background-clip: text; background-clip: text; color: transparent; }
.turuncu { background: linear-gradient(90deg, #ff4f33 0%, #ff8a2c 50%, #ffc23a 100%);
           -webkit-background-clip: text; background-clip: text; color: transparent; }

/* mühür — CMG örneğindeki altın rozet */
.muhur { position: absolute; border-radius: 50%; display: flex; flex-direction: column;
  align-items: center; justify-content: center; text-align: center; line-height: .92;
  font-weight: 800; transform: rotate(-9deg);
  box-shadow: 0 26px 60px rgba(0,0,0,.35); }
.muhur.altin-r { color: #2b1905;
  background: radial-gradient(circle at 34% 28%, #fff6cf 0%, #f4d27c 24%, #d6a34b 56%, #a9752d 84%, #7a5220 100%); }
.muhur.kirmizi-r { color: #fff;
  background: radial-gradient(circle at 34% 28%, #ff7a6b 0%, #e5323a 40%, #b5161f 85%, #8c0e16 100%); }
.muhur::before { content: ""; position: absolute; inset: 4.5%; border-radius: 50%;
  border: .55vmin solid rgba(255,255,255,.55); }
.muhur .m1 { font-size: .30em; font-weight: 700; letter-spacing: .12em; }
.muhur .m2 { font-size: 1em; letter-spacing: -.03em; }
.muhur .m3 { font-size: .46em; letter-spacing: .02em; }

/* fiyat paneli */
.fiyat { position: absolute; border-radius: 44px; overflow: hidden; }
.fiyat .bas { text-align: center; font-weight: 800; letter-spacing: .06em; padding: 34px 0 30px; }
.fiyat .satir { display: grid; grid-template-columns: 1fr 1fr; }
.fiyat .hucre { text-align: center; padding: 28px 10px 34px; }
.fiyat .hucre + .hucre { border-left: 3px solid var(--cizgi); }
.fiyat .tip { font-weight: 700; font-size: 70px; letter-spacing: .04em; }
.fiyat .tutar { font-weight: 800; font-size: 150px; letter-spacing: -.03em; line-height: 1; margin-top: 8px; }
.fiyat .tutar small { font-size: .5em; vertical-align: .62em; margin-left: .04em; }
.fiyat .ay { font-weight: 600; font-size: 44px; letter-spacing: .2em; margin-top: 10px; opacity: .85; }
.fiyat .alt { text-align: center; font-weight: 600; font-size: 50px; letter-spacing: .1em;
              padding: 22px 0 26px; border-top: 3px solid var(--cizgi); }

/* Ocean köşe plakası — panonun sağ alt köşesi */
.kose { position: absolute; right: 0; bottom: 0; width: 2350px; height: 640px;
  border-radius: 70px 0 0 0; display: flex; flex-direction: column; align-items: center;
  justify-content: center; gap: 14px; }

/* Ocean Gayrimenkul — Montserrat ile yeniden kurulmuş kilit */
.ocean { display: inline-flex; flex-direction: column; align-items: flex-start;
         line-height: 1; color: var(--oc); }
.ocean .o1 { font-weight: 800; letter-spacing: -.035em; position: relative;
             isolation: isolate; white-space: nowrap; }
.ocean .o1 .o { position: relative; display: inline-block; }
.ocean .o1 .o::before { content: ""; position: absolute; z-index: -1;
   left: .075em; right: .075em; top: .165em; bottom: .145em; border-radius: 50%;
   background: radial-gradient(ellipse 120% 46% at 50% 104%, var(--su) 98%, transparent 100%); }
.ocean .o2 { font-weight: 600; font-size: .465em; white-space: nowrap; margin-top: .06em; }
"""

JS = """
<script>
document.querySelectorAll("[data-maxw]").forEach(e => {
  const m = +e.dataset.maxw; let f = parseFloat(getComputedStyle(e).fontSize);
  while (e.scrollWidth > m && f > 10) { f -= 1; e.style.fontSize = f + "px"; }
});
document.querySelectorAll(".ocean").forEach(k => {
  const a = k.querySelector(".o1"), b = k.querySelector(".o2");
  b.style.letterSpacing = ((a.offsetWidth - b.offsetWidth) / (b.textContent.length - 1)) + "px";
});
</script>
"""


# ---------------------------------------------------------------- yardımcılar
def svg(ad, x, y, h, oran):
    return (f'<img class="a" src="file://{os.path.join(VEK, ad)}.svg" '
            f'style="left:{x}px;top:{y}px;height:{h}px;width:{round(h * oran)}px">')


def tilda(x, y, h, beyaz=True):
    return svg("tilda-beyaz" if beyaz else "tilda", x, y, h, TILDA_ORAN)


def mia(x, y, h, beyaz=True):
    return svg("mia-beyaz" if beyaz else "mia-lacivert", x, y, h, MIA_ORAN)


def ocean(fs, renk, su):
    return (f'<div class="ocean" style="font-size:{fs}px;--oc:{renk};--su:{su}">'
            f'<div class="o1"><span class="o">O</span>CEAN</div>'
            f'<div class="o2">GAYRİMENKUL</div></div>')


def yazi(x, y, metin, fs, w=800, renk="#fff", sinif="", maxw=None, ls="0", ek=""):
    m = f' data-maxw="{maxw}"' if maxw else ""
    renk_css = "" if sinif in ("altin", "turuncu") else f"color:{renk};"
    return (f'<div class="a tek {sinif}"{m} style="left:{x}px;top:{y}px;font-size:{fs}px;'
            f'font-weight:{w};{renk_css}letter-spacing:{ls};{ek}">{metin}</div>')


def muhur(cx, cy, d, tur="altin-r", ust="SADECE", orta="60 AY", alt="SABİT TAKSİT!"):
    return (f'<div class="muhur {tur}" style="left:{cx - d // 2}px;top:{cy - d // 2}px;'
            f'width:{d}px;height:{d}px;font-size:{round(d * .30)}px">'
            f'<div class="m1">{ust}</div><div class="m2">{orta}</div>'
            f'<div class="m3">{alt}</div></div>')


def fiyat(x, y, w, p):
    return f"""
<div class="fiyat" style="left:{x}px;top:{y}px;width:{w}px;background:{p['panel']};
     color:{p['panel_yazi']};--cizgi:{p['panel_cizgi']};border:4px solid {p['panel_kenar']}">
  <div class="bas" style="font-size:78px;background:{p['panel_bas']};color:{p['panel_bas_yazi']}">
    60 AY SABİT TAKSİT</div>
  <div class="satir">
    <div class="hucre"><div class="tip">1+0</div>
      <div class="tutar">29.900<small>₺</small></div><div class="ay">AYLIK</div></div>
    <div class="hucre"><div class="tip">1+1</div>
      <div class="tutar">39.900<small>₺</small></div><div class="ay">AYLIK</div></div>
  </div>
  <div class="alt">BANKA YOK · FAİZ YOK · ARA ÖDEME YOK</div>
</div>"""


def kose(p):
    return f"""
<div class="kose" style="background:{p['kose']};color:{p['kose_yazi']}">
  <div class="tek kas" style="font-size:50px;color:{p['kose_etiket']}">TEK YETKİLİ SATIŞ</div>
  {ocean(230, p['kose_logo'], p['kose_su'])}
  <div class="tek" style="font-size:118px;font-weight:800;letter-spacing:-.01em;margin-top:6px">
    0540 028 00 41</div>
</div>"""


def kahraman(icinde_pano):
    """Proje görseli: pano içinde tamamı, taşmada yalnızca bina sütunları."""
    if icinde_pano:
        return (f'<img class="a" src="file://{HERO}" style="left:{HX}px;top:{HY - EXT}px;'
                f'width:{HW}px;height:{HH}px">')
    duraklar = []
    for a, b in SUTUNLAR:
        duraklar += [f"transparent {a * 100:.2f}%", f"#000 {a * 100:.2f}%",
                     f"#000 {b * 100:.2f}%", f"transparent {b * 100:.2f}%"]
    maske = "linear-gradient(90deg," + ",".join(duraklar) + ")"
    return (f'<img class="a" src="file://{HERO}" style="left:{HX}px;top:{HY}px;'
            f'width:{HW}px;height:{HH}px;-webkit-mask-image:{maske}">')


def merdiven(x0, x1, renk1, renk2, taban=850, hmin=40, hmax=470):
    n, adim = 60, (x1 - x0) / 60
    c1 = [int(renk1[i:i + 2], 16) for i in (1, 3, 5)]
    c2 = [int(renk2[i:i + 2], 16) for i in (1, 3, 5)]
    s = []
    for i in range(n):
        k = i / (n - 1)
        h = round(hmin + (hmax - hmin) * k)
        r = [round(a + (b - a) * k) for a, b in zip(c1, c2)]
        s.append(f'<div class="a" style="left:{x0 + i * adim:.1f}px;top:{taban - h}px;'
                 f'width:{adim * .8:.1f}px;height:{h}px;border-radius:8px 8px 0 0;'
                 f'background:rgb({r[0]},{r[1]},{r[2]})"></div>')
        if (i + 1) % 10 == 0:
            s.append(yazi(round(x0 + i * adim + adim * .4) - 40, taban - h - 74, str(i + 1),
                          54, 700, "rgba(255,255,255,.9)", ek="width:80px;text-align:center"))
    return "".join(s)


# ---------------------------------------------------------------- paletler
LACIVERT = dict(
    zemin="linear-gradient(180deg,#0a1f3d 0%,#123663 55%,#1d4c80 100%)",
    yazi="#ffffff", vurgu="altin", alt="rgba(255,255,255,.88)", kas="#e9c27a",
    tilda_beyaz=True, mia_beyaz=True, muhur="altin-r",
    panel="#123a68", panel_yazi="#fff", panel_cizgi="rgba(255,255,255,.35)",
    panel_kenar="rgba(255,255,255,.55)", panel_bas="linear-gradient(90deg,#e2b45c,#f4d27c,#e2b45c)",
    panel_bas_yazi="#2b1905",
    kose="#ffffff", kose_yazi="#0f2a4d", kose_etiket="#b07a2c", kose_logo="#0f4c9b", kose_su="#2f7fd6")

GOKYUZU = dict(
    zemin="linear-gradient(180deg,#6fb2e8 0%,#a9d3f3 45%,#e6f2fa 100%)",
    yazi="#0b2545", vurgu="turuncu", alt="#0b2545", kas="#0f4c9b",
    tilda_beyaz=False, mia_beyaz=False, muhur="kirmizi-r",
    panel="#ffffff", panel_yazi="#0b2545", panel_cizgi="rgba(11,37,69,.18)",
    panel_kenar="rgba(255,255,255,.9)", panel_bas="#0b2545", panel_bas_yazi="#fff",
    kose="#0b2545", kose_yazi="#fff", kose_etiket="#f4d27c", kose_logo="#ffffff", kose_su="#5fb3ff")

KREM = dict(
    zemin="linear-gradient(180deg,#f7f2ea 0%,#efe6d8 100%)",
    yazi="#13212c", vurgu=None, vurgu_renk="#9a6a3e", alt="#13212c", kas="#a87a55",
    tilda_beyaz=False, mia_beyaz=False, muhur="altin-r",
    panel="#13212c", panel_yazi="#fff", panel_cizgi="rgba(255,255,255,.25)",
    panel_kenar="#13212c", panel_bas="linear-gradient(90deg,#b88a5e,#d9b07c,#b88a5e)",
    panel_bas_yazi="#1a1106",
    kose="#13212c", kose_yazi="#fff", kose_etiket="#d9b07c", kose_logo="#ffffff", kose_su="#5fb3ff")

TURKUAZ = dict(
    zemin="linear-gradient(180deg,#0596a6 0%,#07b3c2 55%,#0a8a99 100%)",
    yazi="#ffffff", vurgu=None, alt="#ffffff", kas="#e6fbff",
    tilda_beyaz=True, mia_beyaz=True, muhur="kirmizi-r",
    panel="#ffffff", panel_yazi="#05505b", panel_cizgi="rgba(5,80,91,.2)",
    panel_kenar="#ffffff", panel_bas="#d7262f", panel_bas_yazi="#fff",
    kose="#ffffff", kose_yazi="#05505b", kose_etiket="#d7262f", kose_logo="#0f4c9b", kose_su="#2f7fd6")


# ---------------------------------------------------------------- yerleşimler
def sol_klasik(p, baslik, ikinci):
    """Sol bölge: dev Tilda + başlık bloğu + mühür."""
    vurgu_sinif = p["vurgu"] or ""
    return f"""
  {tilda(300, 250, 360, p['tilda_beyaz'])}
  <div class="a" style="left:2080px;top:200px;width:4px;height:460px;background:{p['kas']};opacity:.6"></div>
  {yazi(2260, 150, "İZMİT · MİA BÖLGESİ", 64, 600, p['kas'], "kas")}
  {yazi(2250, 240, baslik, 250, 800, p['yazi'], maxw=4100)}
  {yazi(2260, 520, ikinci, 150, 800, p.get('vurgu_renk', p['yazi']), vurgu_sinif, maxw=4100)}
  {yazi(2264, 720, "miaparkocean.com", 74, 700, p['alt'])}
  {muhur(6720, 430, 640, p['muhur'])}"""


def sag_klasik(p):
    return f"""
  {fiyat(10950, 70, 3350, p)}
  {mia(14620, 150, 400, p['mia_beyaz'])}
  {yazi(14560, 600, "miaparkocean.com", 64, 700, p['alt'])}
  {kose(p)}"""


def tasarim(p, sol, sag):
    return f"""
<div class="tasma">{kahraman(False)}</div>
<div class="pano" style="background:{p['zemin']}">
  {sol}
  {kahraman(True)}
  {sag}
</div>"""


def t1():
    p = LACIVERT
    return tasarim(p, sol_klasik(p, "MİA'DA YAŞAM BAŞLIYOR!", "EVİNİZE GİDEN 60 ADIM!"), sag_klasik(p))


def t2():
    p = GOKYUZU
    return tasarim(p, sol_klasik(p, "MİA'DA YAŞAM BAŞLIYOR!", "60 AY SABİT TAKSİT!"), sag_klasik(p))


def t3():
    p = KREM
    return tasarim(p, sol_klasik(p, "EVİNİZE GİDEN 60 ADIM!", "MİA'DA YAŞAM BAŞLIYOR!"), sag_klasik(p))


def t4():
    p = TURKUAZ
    return tasarim(p, sol_klasik(p, "MİA'DA YAŞAM BAŞLIYOR!", "EVİNİZE GİDEN 60 ADIM!"), sag_klasik(p))


def t5():
    """60 adım — basamaklar soldan binaya doğru yükselir."""
    p = dict(LACIVERT)
    sol = f"""
  {tilda(300, 90, 330, True)}
  {yazi(2050, 92, "EVİNİZE GİDEN 60 ADIM!", 230, 800, "#fff", maxw=4700)}
  {yazi(2060, 345, "60 ay sabit taksit · Banka yok · Faiz yok · Ara ödeme yok", 78, 600, "#e9c27a", maxw=4800)}
  {merdiven(300, 7000, "#6b4a2b", "#f0cd8f", hmin=40, hmax=330)}"""
    return tasarim(p, sol, sag_klasik(p))


def t6():
    """Dev 60 — uzaktan ilk okunan şey sayı."""
    p = GOKYUZU
    sol = f"""
  {tilda(300, 90, 300, False)}
  {yazi(300, 470, "miaparkocean.com", 80, 700, p['yazi'])}
  {yazi(2050, -190, "60", 1150, 800, "", "altin", ls="-.06em")}
  {yazi(3720, 150, "AY SABİT", 260, 800, p['yazi'], maxw=3300)}
  {yazi(3720, 420, "TAKSİT!", 260, 800, "", "turuncu", maxw=3300)}
  {yazi(3730, 700, "MİA'DA YAŞAM BAŞLIYOR!", 90, 800, p['yazi'], maxw=3300)}"""
    return tasarim(p, sol, sag_klasik(p))


def t7():
    """Gece mavisi + turuncu başlık — tek satırlık güçlü mesaj."""
    p = dict(LACIVERT, zemin="linear-gradient(180deg,#071225 0%,#0d2242 60%,#173a66 100%)",
             vurgu="turuncu", muhur="kirmizi-r")
    sol = f"""
  {tilda(300, 250, 360, True)}
  <div class="a" style="left:2080px;top:200px;width:4px;height:460px;background:#ff8a2c;opacity:.7"></div>
  {yazi(2260, 160, "60 AY SABİT TAKSİT!", 270, 800, "", "turuncu", maxw=4100)}
  {yazi(2262, 470, "MİA'DA YAŞAM BAŞLIYOR!", 140, 800, "#fff", maxw=4100)}
  {yazi(2264, 660, "Evinize giden 60 adım · miaparkocean.com", 74, 600, "rgba(255,255,255,.85)", maxw=4400)}
  {muhur(6720, 430, 640, "altin-r", "SADECE", "60 AY", "SABİT TAKSİT!")}"""
    return tasarim(p, sol, sag_klasik(p))


TASARIMLAR = [(t1, "lacivert-altin"), (t2, "gokyuzu"), (t3, "krem-tilda"),
              (t4, "turkuaz"), (t5, "60-adim"), (t6, "dev-60"), (t7, "gece-turuncu")]


def sayfa(govde):
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>'
            f'{CSS.replace("__FONT__", FONT)}</style></head><body>{govde}{JS}</body></html>')


# ---------------------------------------------------------------- önizleme mockup'ı
def mockup(tam, yol):
    """Panoyu açık bir gökyüzü önünde, taşmasıyla birlikte gösterir."""
    w, h = tam.size
    pay_ust, pay_alt = round(h * .25), round(h * .55)
    zem = Image.new("RGB", (w, h + pay_ust + pay_alt))
    d = ImageDraw.Draw(zem)
    for y in range(zem.height):
        k = y / zem.height
        d.line([(0, y), (w, y)], fill=(round(150 + 90 * k), round(190 + 55 * k), round(228 + 22 * k)))
    py = pay_ust + round(EXT / TH * h)
    ph = h - round(EXT / TH * h)
    # direkler ve alt kiriş
    for xm in range(10, 180, 20):
        x = round(xm / 180 * w)
        d.rectangle([x - 4, py + ph, x + 4, zem.height], fill=(70, 78, 88))
    d.rectangle([0, py + ph, w, py + ph + 6], fill=(60, 66, 74))
    zem.paste(tam, (0, pay_ust), tam)
    # ölçü çizgileri
    f = ImageFont.truetype(FONT, 22)
    yy = py + ph + 34
    for ad, x0, x1 in PARCA:
        a, b = round(x0 / TW * w), round(x1 / TW * w)
        d.line([(a + 3, yy), (b - 3, yy)], fill=(20, 30, 45), width=2)
        d.line([(a + 3, yy - 8), (a + 3, yy + 8)], fill=(20, 30, 45), width=2)
        d.line([(b - 3, yy - 8), (b - 3, yy + 8)], fill=(20, 30, 45), width=2)
        d.text(((a + b) / 2, yy + 22), ad.split("-")[1].upper(), font=f, fill=(20, 30, 45), anchor="mm")
    zem.save(yol, quality=90)


# ---------------------------------------------------------------- üretim
def uret(onizle, sec):
    gecici = tempfile.mkdtemp(prefix="mega-")
    dsf = 0.25 if onizle else 4
    dilim = 18000 if onizle else 2000
    isler = []
    for i, (fn, ad) in enumerate(TASARIMLAR, 1):
        if sec and i not in sec:
            continue
        hp = os.path.join(gecici, f"{i}.html")
        open(hp, "w", encoding="utf-8").write(sayfa(fn()))
        isler.append(dict(html=hp, w=TW, h=TH, dsf=dsf, dilim=dilim,
                          cikti=os.path.join(gecici, f"{i}"), no=i, ad=ad))
    jp = os.path.join(gecici, "isler.json")
    json.dump(isler, open(jp, "w"))
    npm = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    subprocess.run(["node", os.path.join(ROOT, "scripts", "mega-bilbord", "render.cjs"), jp],
                   check=True, env={**os.environ, "NODE_PATH": npm})

    for is_ in isler:
        hedef = os.path.join(OUT, f"{is_['no']:02d}-{is_['ad']}")
        os.makedirs(hedef, exist_ok=True)
        dilimler = [Image.open(d) for d in json.load(open(is_["cikti"] + ".json"))]
        olc = dsf
        if onizle:
            tam = dilimler[0].convert("RGBA")
            mockup(tam, os.path.join(hedef, "onizleme.jpg"))
            print("  önizleme:", os.path.relpath(hedef, ROOT))
            continue
        os.makedirs(os.path.join(hedef, "baski"), exist_ok=True)
        dw = round(dilim * olc)
        ey = round(EXT * olc)
        # pano parçaları
        for ad, x0, x1 in PARCA:
            i0, i1 = x0 // dilim, x1 // dilim
            parca = Image.new("RGB", (round((x1 - x0) * olc), round(PH * olc)))
            for k in range(i0, i1):
                parca.paste(dilimler[k].convert("RGB").crop((0, ey, dw, dilimler[k].height)),
                            ((k - i0) * dw, 0))
            yol = os.path.join(hedef, "baski", f"{ad}.jpg")
            parca.save(yol, quality=92, dpi=(10.16, 10.16))
            print("  →", os.path.relpath(yol, ROOT), parca.size,
                  f"{os.path.getsize(yol) / 1048576:.1f} MB")
        # taşma kesimi (şeffaf)
        tx0 = HX // dilim
        tx1 = (HX + HW) // dilim
        tas = Image.new("RGBA", (round((tx1 - tx0 + 1) * dw), ey), (0, 0, 0, 0))
        for k in range(tx0, tx1 + 1):
            tas.paste(dilimler[k].crop((0, 0, dw, ey)), ((k - tx0) * dw, 0))
        kutu = tas.getchannel("A").getbbox()
        tas = tas.crop(kutu)
        yol = os.path.join(hedef, "baski", "tasma-kesim.png")
        tas.save(yol, dpi=(10.16, 10.16))
        sol_m = (tx0 * dilim + kutu[0] / olc) / 100
        print("  →", os.path.relpath(yol, ROOT), tas.size,
              f"panonun {sol_m:.2f}. metresinden başlar, {tas.height / olc / 100:.2f} m yüksek")


if __name__ == "__main__":
    sec = None
    if "--sadece" in sys.argv:
        sec = {int(v) for v in sys.argv[sys.argv.index("--sadece") + 1].split(",")}
    uret("--onizle" in sys.argv, sec)
