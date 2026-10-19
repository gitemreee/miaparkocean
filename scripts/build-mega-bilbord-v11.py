#!/usr/bin/env python3
"""
180 m dev pano — 11. tur: 5. tasarım (eğik panel + mutlu aile) üzerinden beş varyasyon.

Ortak: gündüz render'ı ana görsel (gök maskeli, panonun üstünden taşar), mutlu aile,
Tilda + MİA PARK OCEAN logoları, alt şerit. Detay fotoğrafı yok; finans bloğu her
tasarımda büyük ve belirgin.

  1  Turuncu panel     — HAYALİNİZDEKİ EVE BUGÜN ADIM ATIN      · fiyat kartları
  2  Lacivert panel sağda — AİLENİZ İÇİN EN DOĞRU ADIM          · dev "60 AY"
  3  Turkuaz panel     — KİRAYA DEĞİL, KENDİ EVİNİZE ÖDEYİN     · fiyat satırları, aile sağ uçta
  4  Kırmızı panel     — SON DAİRELER! FIRSATI KAÇIRMAYIN       · beyaz kartlar, sarı vurgular
  5  Yeşil panel       — 60 AY SABİT TAKSİTLE EV SAHİBİ OLUN    · onay işaretli liste

Ödeme: 60 ay sabit taksit (vade) · 1+1 aylık 39.900 ₺ · 2+1 aylık 49.900 ₺ ·
faiz/banka/kredi/ara ödeme yok · son daireler.

    python3.13 scripts/build-mega-bilbord-v11.py [--sadece 1,3] [--pdf]
"""

import importlib.util as _il
import json
import os
import subprocess
import sys
import tempfile

from PIL import Image

Image.MAX_IMAGE_PIXELS = None
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _yukle(ad, dosya):
    spec = _il.spec_from_file_location(ad, os.path.join(ROOT, "scripts", dosya))
    m = _il.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


v10 = _yukle("mb_v10", "build-mega-bilbord-v10.py")
v7, v6, v4, v2, mb = v10.v7, v10.v6, v10.v4, v10.v2, v10.mb
OUT = os.path.join(ROOT, "tabela", "mega-bilbord-180m-tur11")
TW = mb.TW
y, kutu, satir, damga, pill, pano = v4.y, v4.kutu, v4.satir, v4.damga, v10.pill, v10.pano
YOKLAR = v4.YOKLAR
AILE, AILE_ORAN = v10.AILE, v10.AILE_ORAN
YOK4 = ("FAİZ YOK", "BANKA YOK", "KREDİ YOK", "ARA ÖDEME YOK")


def panel(x, w, bg, sol=True, nokta="rgba(255,255,255,.22)"):
    """Eğik kenarlı renkli panel; sol=True ise sağ kenarı eğik."""
    kes = "polygon(0 0,100% 0,86% 100%,0 100%)" if sol else "polygon(14% 0,100% 0,100% 100%,0 100%)"
    mask = ("linear-gradient(90deg,transparent 55%,#000 100%)" if sol
            else "linear-gradient(270deg,transparent 55%,#000 100%)")
    return (f'<div class="a" style="left:{x}px;top:0;width:{w}px;height:850px;clip-path:{kes};background:{bg}"></div>'
            f'<div class="a" style="left:{x}px;top:0;width:{w}px;height:850px;clip-path:{kes};'
            f'background-image:radial-gradient({nokta} 7px,transparent 8px);background-size:60px 60px;opacity:.5;'
            f'mask-image:{mask};-webkit-mask-image:{mask}"></div>')


def detay(x, top, w, h, yol, pos="50% 50%", r=44):
    """Köşeleri yuvarlatılmış detay fotoğrafı (proje render'ı)."""
    return (f'<div class="a" style="left:{x}px;top:{top}px;width:{w}px;height:{h}px;border-radius:{r}px;'
            f'background:url(file://{os.path.join(ROOT, yol)}) {pos}/cover no-repeat;'
            f'box-shadow:0 24px 50px rgba(0,0,0,.25)"></div>')


def aile(x, ah=900, top=None):
    top = 910 - ah if top is None else top
    return (f'<img class="a" src="{AILE}" style="left:{x}px;top:{top}px;height:{ah}px;width:{round(ah * AILE_ORAN)}px;'
            f'filter:drop-shadow(0 30px 40px rgba(0,0,0,.3))">')


def kart(x, top, tip, tutar, bg, kenar, tip_renk, renk, alt_renk, w=1500, h=430):
    return f'''
<div class="a" style="left:{x}px;top:{top}px;width:{w}px;height:{h}px;border-radius:40px;background:{bg};border:7px solid {kenar};
     box-shadow:0 24px 50px rgba(0,0,0,.25);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center">
  <div class="tek" style="font-size:150px;font-weight:800;color:{tip_renk};letter-spacing:-.03em;line-height:.95">{tip}</div>
  <div class="tek kas" style="font-size:40px;color:{alt_renk};margin-top:10px">AYLIK</div>
  <div class="tek" style="font-size:140px;font-weight:800;color:{renk};letter-spacing:-.03em;margin-top:2px">{tutar}<span style="font-size:.45em">₺</span></div>
</div>'''


def yok_piller(x, top, bg, renk, kenar="transparent", fs=52, h=110, ara=30):
    s, cx = [], x
    for t in YOK4:
        s.append(pill(cx, top, t, bg, renk, fs, h, f"border:5px solid {kenar};padding:0 {round(h * .4)}px"))
        cx += round(len(t) * fs * .72 + h * .8 + ara)
    return "".join(s)


def onay_liste(x, top, renk, daire, ic, fs=58, satir_h=130, sutun_w=1550):
    s = []
    for i, t in enumerate(YOK4):
        cx, cy = x + (i % 2) * sutun_w, top + (i // 2) * satir_h
        s.append(f'<div class="a" style="left:{cx}px;top:{cy}px;display:flex;align-items:center;gap:28px">'
                 f'<div style="width:90px;height:90px;border-radius:50%;background:{daire};display:flex;align-items:center;justify-content:center">'
                 f'<svg width="54" height="54" viewBox="0 0 24 24" fill="none" stroke="{ic}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12.5l5 5L20 7"/></svg></div>'
                 f'<div class="tek" style="font-size:{fs}px;font-weight:800;color:{renk};letter-spacing:.03em">{t}</div></div>')
    return "".join(s)


# ================================================================ 1 — turuncu, fiyat kartları
def A1():
    lac, tur = "#14225a", "#f5701d"
    r = dict(v4.SERIT_ACIK, serit=lac, serit_su="#ff9b4a")
    zemin = "linear-gradient(90deg,#e6ecf3 0%,#f3f6f9 50%,#e9eef4 100%)"
    tas, ic = v4.bina(10300)
    arka = panel(0, 7700, "linear-gradient(135deg,#ff9a3c 0%,#f5701d 60%,#e85d10 100%)")
    icerik = f"""
  {mb.tilda(300, 70, 230, True)}
  {y(1600, 60, "HAYALİNİZDEKİ EVE", 230, 800, "#fff", maxw=4700)}
  {y(1600, 300, "BUGÜN ADIM ATIN.", 230, 800, "#fff", maxw=4700)}
  {pill(1600, 575, "60 AY SABİT TAKSİT &nbsp;·&nbsp; FAİZ YOK &nbsp;·&nbsp; BANKA YOK", "#fff", tur, 52, 120)}
  {aile(6450)}
  {pill(12500, 60, "60 AY SABİT TAKSİT", lac, "#fff", 60, 130, "letter-spacing:.08em")}
  {kart(12500, 230, "1+1", "39.900", "#fff", tur, tur, lac, "#5a6a8a")}
  {kart(14150, 230, "2+1", "49.900", "#fff", tur, tur, lac, "#5a6a8a")}
  {y(12520, 690, YOKLAR, 44, 700, lac, sinif="kas", maxw=3100, ek="display:none")}
  {mb.mia(16150, 60, 300, False)}
  {damga(17450, 420, 360, "SON", "DAİRELER", "KAÇIRMAYIN!", zemin=tur, yazi="#fff")}"""
    return pano(r, zemin, arka, icerik, tas, ic)


# ================================================================ 2 — lacivert panel sağda, dev 60 AY
def A2():
    lac, altin = "#14225a", "#e2b45c"
    r = dict(v4.SERIT_ACIK, serit="#0c1640", serit_su=altin, serit_logo="#fff")
    zemin = "linear-gradient(90deg,#dfe7f0 0%,#f1f5f9 40%,#f1f5f9 60%,#e4eaf1 100%)"
    tas, ic = v4.bina(2600)
    arka = panel(10900, 7100, "linear-gradient(315deg,#1b2d6e 0%,#14225a 55%,#0c1640 100%)", sol=False, nokta="rgba(226,180,92,.25)")
    icerik = f"""
  {y(5000, -30, "60", 620, 800, lac, ls="-.05em")}
  {y(6500, 120, "AY", 300, 800, lac)}
  {y(6500, 410, "SABİT TAKSİT", 150, 800, "#c8482f", maxw=3400)}
  {kutu(5000, 590, 5200, 120, "".join(pill(0, 0, t, "transparent", lac, 46, 100, f"position:relative;border:5px solid {lac};margin-right:26px;display:inline-flex") for t in YOK4), "display:flex;align-items:center")}
  {aile(10200)}
  {mb.tilda(12500, 60, 220, True)}
  {mb.mia(14000, 40, 260, True)}
  {y(12500, 330, "AİLENİZ İÇİN", 170, 800, "#fff", maxw=5000)}
  {y(12500, 510, "EN DOĞRU ADIM.", 170, 800, "", sinif="altin", maxw=5000)}
  {kutu(15000, 350, 2800, 330, v6.fiyat_satiri("#fff", 130, altin, "rgba(226,180,92,.5)"))}"""
    return pano(r, zemin, arka, icerik, tas, ic)


# ================================================================ 3 — turkuaz → beyaz geçişli, şok finans kartı
def sok(cx, cy, d, ust, alt, bg="#e3262e", renk="#fff", don=-12):
    """Kırmızı yıldız patlaması rozeti."""
    import math
    n, pts = 16, []
    for i in range(2 * n):
        rr = d / 2 if i % 2 == 0 else d / 2 * .78
        a_ = math.pi * i / n
        pts.append(f"{d / 2 + rr * math.cos(a_):.1f},{d / 2 + rr * math.sin(a_):.1f}")
    return (f'<div class="a" style="left:{cx - d // 2}px;top:{cy - d // 2}px;width:{d}px;height:{d}px;transform:rotate({don}deg);'
            f'filter:drop-shadow(0 16px 30px rgba(0,0,0,.3))"><svg width="{d}" height="{d}"><polygon points="{" ".join(pts)}" fill="{bg}"/></svg>'
            f'<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;color:{renk};text-align:center;line-height:1">'
            f'<div class="tek" style="font-size:{round(d * (.21 if len(ust) <= 5 else .115))}px;font-weight:800;letter-spacing:-.01em">{ust}</div>'
            f'<div class="tek" style="font-size:{round(d * .15)}px;font-weight:800;letter-spacing:.06em;margin-top:.12em">{alt}</div></div></div>')


def daire_foto(cx, cy, d, ad, kenar="#fff"):
    return (f'<div class="a" style="left:{cx - d // 2}px;top:{cy - d // 2}px;width:{d}px;height:{d}px;border-radius:50%;'
            f'background:url({v10.F[ad]}) 50% 50%/cover no-repeat;border:12px solid {kenar};box-shadow:0 20px 40px rgba(0,0,0,.25)"></div>')


def A3():
    koyu, turk, kir = "#06343f", "#0e8a98", "#e3262e"
    r = dict(v4.SERIT_ACIK, serit=koyu, serit_su="#5fd3e0")
    zemin = "linear-gradient(90deg,#0b7f8d 0%,#15a0ae 20%,#6cc6d1 38%,#d9eff2 50%,#ffffff 60%,#ffffff 100%)"
    tas, ic = v4.bina(11200)
    kart = ('<div class="a" style="left:4350px;top:60px;width:4050px;height:640px;border-radius:56px;background:#fff;'
            'box-shadow:0 30px 70px rgba(6,52,63,.28)"></div>')
    yoklar = "".join(sok(cx, cy, 310, t.rsplit(" ", 1)[0], "YOK", don=d)
                     for (cx, cy, d), t in zip(((7700, 215, -10), (8090, 215, 7), (7700, 540, 5), (8090, 540, -8)), YOK4))
    icerik = f"""
  {mb.tilda(300, 100, 300, True)}
  {y(1950, 55, "KİRAYA DEĞİL,", 190, 800, "#fff", maxw=2250)}
  {y(1950, 262, "KENDİ EVİNİZE", 190, 800, "#fff", maxw=2250)}
  {y(1950, 470, "ÖDEYİN.", 190, 800, "#dff8fb", maxw=2250)}
  {kart}
  {pill(4650, 130, "60 AY SABİT TAKSİT", koyu, "#fff", 64, 130, "letter-spacing:.08em")}
  {kutu(4600, 300, 3000, 300, v6.fiyat_satiri(kir, 170, koyu, "rgba(6,52,63,.25)"))}
  {yoklar}
  {detay(13200, 60, 1550, 390, "signage-source/avlu-havuz-teras.jpg", "50% 62%", 40)}
  {daire_foto(13330, 600, 230, "salon")}
  {daire_foto(13975, 600, 230, "mutfak")}
  {daire_foto(14620, 600, 230, "park")}
  {aile(14850, 950, -15)}
  {mb.mia(16300, 60, 400, False)}
  {damga(17480, 530, 330, "SON", "DAİRELER", "KAÇIRMAYIN!", zemin=kir, yazi="#fff")}"""
    return pano(r, zemin, "", icerik, tas, ic)


# ================================================================ 4 — kırmızı, son daireler
def A4():
    kir, sari, koyu = "#c8282e", "#ffd21f", "#1a1a1a"
    r = dict(v4.SERIT_ACIK, serit=koyu, serit_su=sari)
    zemin = "linear-gradient(90deg,#efe8e8 0%,#f7f4f4 50%,#ece9e9 100%)"
    tas, ic = v4.bina(10300)
    arka = panel(0, 7700, "linear-gradient(135deg,#e8373d 0%,#c8282e 55%,#9e1c21 100%)")
    icerik = f"""
  {mb.tilda(300, 70, 230, True)}
  {y(1600, 40, "SON DAİRELER!", 290, 800, sari, maxw=4800, ls="-.02em")}
  {y(1600, 350, "FIRSATI KAÇIRMAYIN.", 170, 800, "#fff", maxw=4800)}
  {pill(1600, 575, "60 AY SABİT TAKSİT &nbsp;·&nbsp; ARA ÖDEME YOK", "#fff", kir, 52, 120)}
  {aile(6450)}
  {pill(12500, 60, "60 AY SABİT TAKSİT", koyu, sari, 60, 130, "letter-spacing:.08em")}
  {kart(12500, 230, "1+1", "39.900", "#fff", sari, kir, koyu, "#777")}
  {kart(14150, 230, "2+1", "49.900", "#fff", sari, kir, koyu, "#777")}
  {mb.mia(16150, 60, 300, False)}
  {yok_piller(16050, 520, kir, "#fff", kir, 36, 80, 16)}"""
    return pano(r, zemin, arka, icerik, tas, ic)


# ================================================================ 5 — yeşil, onay listesi
def A5():
    yesil, altin = "#123d2a", "#e2b45c"
    r = dict(v4.SERIT_ACIK, serit=yesil, serit_su="#8fd1a6")
    zemin = "linear-gradient(90deg,#e6efe8 0%,#f3f7f4 50%,#e7efe9 100%)"
    tas, ic = v4.bina(9800)
    arka = panel(0, 7200, "linear-gradient(135deg,#2b6248 0%,#1b4635 55%,#0f2d22 100%)", nokta="rgba(226,180,92,.22)")
    icerik = f"""
  {mb.tilda(300, 70, 230, True)}
  {y(1600, 60, "60 AY SABİT TAKSİTLE", 180, 800, "", sinif="altin", maxw=4400)}
  {y(1600, 260, "EV SAHİBİ OLUN.", 230, 800, "#fff", maxw=4400)}
  {y(1610, 530, "Faiz yok · banka yok · kredi yok · ara ödeme yok", 56, 600, "#cfe8da", maxw=4400)}
  {aile(5950)}
  {kutu(12200, 60, 3600, 320, v6.fiyat_satiri(yesil, 170, "#2f8a4e", "rgba(18,61,42,.25)"))}
  {onay_liste(12250, 430, yesil, "#2f8a4e", "#fff")}
  {mb.mia(16000, 70, 330, False)}
  {damga(17450, 450, 340, "SON", "DAİRELER", "KAÇIRMAYIN!", zemin="#2f8a4e", yazi="#fff")}"""
    return pano(r, zemin, arka, icerik, tas, ic)


TASARIMLAR = [(A1, "turuncu-fiyat-kartlari"), (A2, "lacivert-60-ay"), (A3, "turkuaz-kiraya-degil"),
              (A4, "kirmizi-son-daireler"), (A5, "yesil-onay-listesi")]


def main():
    sec = None
    if "--sadece" in sys.argv:
        sec = {int(v) for v in sys.argv[sys.argv.index("--sadece") + 1].split(",")}
    gecici = tempfile.mkdtemp(prefix="mega11-")
    isler = []
    for i, (fn, ad) in enumerate(TASARIMLAR, 1):
        if sec and i not in sec:
            continue
        hp = os.path.join(gecici, f"{i}.html")
        open(hp, "w", encoding="utf-8").write(v7.sayfa(fn()))
        isler.append(dict(html=hp, w=TW, h=mb.TH, dsf=0.5, dilim=TW, cikti=os.path.join(gecici, f"{i}"), no=i, ad=ad))
    npm = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    env = {**os.environ, "NODE_PATH": npm}
    if "--pdf" in sys.argv:
        hedef = os.path.join(OUT, "duzenlenebilir-pdf")
        os.makedirs(hedef, exist_ok=True)
        for is_ in isler:
            is_["pdf"] = os.path.join(hedef, f"{is_['no']:02d}-{is_['ad']}.pdf")
        jp = os.path.join(gecici, "pdf.json")
        json.dump(isler, open(jp, "w"))
        subprocess.run(["node", os.path.join(ROOT, "scripts", "mega-bilbord", "pdf.cjs"), jp], check=True, env=env)
        return
    jp = os.path.join(gecici, "isler.json")
    json.dump(isler, open(jp, "w"))
    subprocess.run(["node", os.path.join(ROOT, "scripts", "mega-bilbord", "render.cjs"), jp], check=True, env=env)
    os.makedirs(OUT, exist_ok=True)
    for is_ in isler:
        tam = Image.open(json.load(open(is_["cikti"] + ".json"))[0]).convert("RGBA")
        yol = os.path.join(OUT, f"{is_['no']:02d}-{is_['ad']}.jpg")
        v2.sunum(tam, is_["no"], is_["ad"], yol)
        print("  →", os.path.relpath(yol, ROOT))


if __name__ == "__main__":
    main()
