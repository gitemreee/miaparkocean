#!/usr/bin/env python3
"""
180 m dev pano — 7. tur: üç yeni konsept, üç yeni renk.

  V  FAİZ YOK, BANKA YOK... SADECE EVİNİZ VAR.   — krem & kiremit, kalemle çizilmiş kelimeler
  P  AİLENİZİN YENİ ADRESİ                        — orman yeşili & altın, dev konum pini
  D  SON DAİRELER!                                — siyah & sarı, uyarı şeridi

Ödeme: 60 ay sabit taksit (vade) · 1+1 aylık 39.900 ₺ · 2+1 aylık 49.900 ₺ ·
faiz/banka/kredi/ara ödeme yok · son daireler.

    python3.13 scripts/build-mega-bilbord-v7.py [--sadece 1,3] [--pdf]

--pdf: önizleme yerine düzenlenebilir PDF üretir (Canva/Illustrator'a aktarmak için;
metinler gerçek metin, şekiller vektör). Baskı dosyası değildir.
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


v6 = _yukle("mb_v6", "build-mega-bilbord-v6.py")
v5, v4, v2, mb = v6.v5, v6.v4, v6.v2, v6.mb
OUT = os.path.join(ROOT, "tabela", "mega-bilbord-180m-tur7")
ICERIK = v2.ICERIK
satir, kutu, y, damga, pano = v4.satir, v4.kutu, v4.y, v4.damga, v4.pano
fiyat_satiri = v6.fiyat_satiri


def kalem_cizgi(x, y_, w, don=-4):
    """Kırmızı kalemle atılmış çizgi — hafif dalgalı, iki geçiş."""
    return (f'<svg class="a" style="left:{x - 40}px;top:{y_ - 60}px;transform:rotate({don}deg)" '
            f'width="{w + 80}" height="120"><path d="M20 70 C {w * .3:.0f} 40, {w * .6:.0f} 85, {w + 60} 50" '
            f'stroke="#e3262e" stroke-width="34" fill="none" stroke-linecap="round"/>'
            f'<path d="M40 62 C {w * .35:.0f} 75, {w * .7:.0f} 45, {w + 40} 66" stroke="#e3262e" '
            f'stroke-width="16" fill="none" stroke-linecap="round" opacity=".7"/></svg>')


# ================================================================ V — sadece eviniz var
def V():
    r = dict(v4.SERIT_ACIK, serit="#7a2e1c", zemin="linear-gradient(90deg,#fbf4ea 0%,#f7eadb 60%,#f3e2cf 100%)")
    gri, kir = "#3d4a55", "#c8482f"
    kelimeler = [("FAİZ", 1950, 60, 640), ("BANKA", 2850, 60, 860), ("KREDİ", 3980, 60, 780),
                 ("ARA ÖDEME", 1950, 330, 1520)]
    s = []
    for k, x, yy, w in kelimeler:
        s.append(y(x, yy, k, 220, 800, gri))
        s.append(kalem_cizgi(x, yy + 140, w))
    s.append(y(3620, 380, "YOK.", 170, 800, kir))
    kart = (f'<div style="padding:0 50px">{satir("60 AY SABİT TAKSİT", 66, 800, "#ffe2d6", "letter-spacing:.1em;margin-bottom:12px")}</div>'
            + fiyat_satiri("#fff", 150, "#ffd2c2", "rgba(255,255,255,.35)"))
    icerik = f"""
  {mb.tilda(300, 200, 290, False)}
  {"".join(s)}
  {y(5450, 70, "SADECE", 170, 800, gri)}
  {y(5440, 250, "EVİNİZ VAR.", 300, 800, kir, maxw=4300)}
  {y(5455, 590, "60 AY SABİT TAKSİTLE EV SAHİBİ OLUN", 70, 800, "#8a6a4a", sinif="kas", maxw=4300)}
  {kutu(10050, 90, 2550, 520, kart, "width:fit-content;border-radius:40px;background:linear-gradient(160deg,#d65a3d,#a8361f);"
        "padding:44px 0;box-shadow:0 24px 60px rgba(120,40,20,.35)")}
  {mb.mia(16450, 160, 400, False)}
  {damga(17500, 360, 380, "SON", "DAİRELER", "KAÇIRMAYIN!", zemin="#c8482f", yazi="#fff")}"""
    return pano(r, "", icerik, 14250)


# ================================================================ P — yeni adres
def P():
    r = dict(v4.SERIT_KOYU, zemin="radial-gradient(ellipse 70% 150% at 40% 40%,#2b6248 0%,#1b4635 55%,#0f2d22 100%)")
    salon = "file://" + os.path.join(ROOT, "public", "images", "unit-1plus1-a.webp")
    cx, cy, R = 6750, 280, 270
    pin = (f'<svg class="a" style="left:0;top:0;filter:drop-shadow(0 26px 40px rgba(0,0,0,.45))" width="18000" '
           f'height="{ICERIK}"><defs>'
           f'<linearGradient id="pg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff1c2"/>'
           f'<stop offset=".5" stop-color="#e2b45c"/><stop offset="1" stop-color="#a8712a"/></linearGradient>'
           f'<clipPath id="pc"><circle cx="{cx}" cy="{cy}" r="{R - 46}"/></clipPath></defs>'
           f'<path d="M{cx} {cy + R + 150} C {cx - 90} {cy + R + 40}, {cx - R} {cy + 140}, {cx - R} {cy} '
           f'A {R} {R} 0 1 1 {cx + R} {cy} C {cx + R} {cy + 140}, {cx + 90} {cy + R + 40}, {cx} {cy + R + 150} Z" '
           f'fill="url(#pg)"/>'
           f'<image href="{salon}" x="{cx - R}" y="{cy - R}" width="{2 * R}" height="{2 * R}" '
           f'preserveAspectRatio="xMidYMid slice" clip-path="url(#pc)"/></svg>')
    fiyat = (f'<div style="padding:0 50px">{satir("60 AY SABİT TAKSİT", 66, 800, "#f3d39c", "letter-spacing:.1em;margin-bottom:12px")}</div>'
             + fiyat_satiri("#fff", 160, "#cfe8da", "rgba(255,255,255,.3)"))
    icerik = f"""
  {mb.tilda(300, 200, 290, True)}
  {y(1950, 70, "AİLENİZİN", 170, 800, "#ffffff", maxw=4300)}
  {y(1940, 250, "YENİ ADRESİ", 280, 800, "", sinif="altin", maxw=4300)}
  {y(1955, 590, "İZMİT · MİA BÖLGESİ", 70, 700, "#cfe8da", sinif="kas", maxw=4300)}
  {pin}
  {kutu(7400, 70, 3500, 450, fiyat)}
  {y(7460, 560, v4.YOKLAR, 64, 700, "#cfe8da", sinif="kas", maxw=3400)}
  {mb.mia(15700, 120, 460, True)}
  {damga(17400, 380, 400, "SON", "DAİRELER", "KAÇIRMAYIN!", zemin="#e2b45c", yazi="#1b2a1f")}"""
    return pano(r, "", icerik, 13300)


# ================================================================ D — son daireler
def D():
    r = dict(v4.SERIT_KOYU, serit="#ffd21f", serit_yazi="#111", serit_logo="#111", serit_su="#ffffff",
             zemin="repeating-linear-gradient(135deg,#121212 0 60px,#171717 60px 120px)")
    sari = "#ffd21f"
    bant_metin = ("SON DAİRELER &nbsp;•&nbsp; KAÇIRMAYIN &nbsp;•&nbsp; " * 30)
    bant = (f'<div class="a" style="left:-200px;top:570px;width:18400px;height:116px;transform:rotate(-.15deg);'
            f'background:{sari};box-shadow:0 14px 30px rgba(0,0,0,.5);overflow:hidden;'
            f'border-top:10px solid #111;border-bottom:10px solid #111">'
            f'<div class="tek" style="font-size:66px;font-weight:800;color:#111;letter-spacing:.06em;'
            f'line-height:96px;padding-left:40px">{bant_metin}</div></div>')
    yok = "".join(
        f'<div class="tek" style="font-size:78px;font-weight:800;color:#fff;border:5px solid {sari};'
        f'border-radius:999px;padding:10px 40px;margin:0 0 16px">{t}</div>'
        for t in ("FAİZ YOK", "BANKA YOK", "KREDİ YOK", "ARA ÖDEME YOK"))
    fiyat = (f'<div style="padding:0 50px">{satir("60 AY SABİT TAKSİT", 70, 800, "#fff", "letter-spacing:.1em;margin-bottom:12px")}</div>'
             + fiyat_satiri(sari, 170, "#ffffff", "rgba(255,210,31,.4)"))
    icerik = f"""
  {mb.tilda(300, 170, 290, True)}
  {y(1940, -40, "SON", 560, 800, sari, ls="-.04em")}
  {y(3550, 70, "DAİRELER!", 240, 800, "#ffffff", maxw=3200)}
  {y(3560, 330, "FIRSATI KAÇIRMAYIN.", 120, 800, sari, maxw=3200)}
  {kutu(7500, 40, 1800, 520, yok, "display:flex;flex-direction:column;align-items:flex-start")}
  {kutu(12950, 40, 3200, 500, fiyat)}
  {mb.mia(16650, 90, 380, True)}"""
    return pano(r, bant, icerik, 11000)


TASARIMLAR = [(V, "sadece-eviniz-var"), (P, "ailenizin-yeni-adresi"), (D, "son-daireler")]


def sayfa(govde):
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>'
            f'{mb.CSS.replace("__FONT__", mb.FONT)}{v2.CSS_EK}{v4.CSS_EK}{v5.CSS_EK}</style></head>'
            f'<body>{govde}{mb.JS}</body></html>')


def main():
    sec = None
    if "--sadece" in sys.argv:
        sec = {int(v) for v in sys.argv[sys.argv.index("--sadece") + 1].split(",")}
    gecici = tempfile.mkdtemp(prefix="mega7-")
    isler = []
    for i, (fn, ad) in enumerate(TASARIMLAR, 1):
        if sec and i not in sec:
            continue
        hp = os.path.join(gecici, f"{i}.html")
        open(hp, "w", encoding="utf-8").write(sayfa(fn()))
        isler.append(dict(html=hp, w=mb.TW, h=mb.TH, dsf=0.5, dilim=mb.TW,
                          cikti=os.path.join(gecici, f"{i}"), no=i, ad=ad))
    if "--pdf" in sys.argv:
        hedef = os.path.join(OUT, "duzenlenebilir-pdf")
        os.makedirs(hedef, exist_ok=True)
        for is_ in isler:
            is_["pdf"] = os.path.join(hedef, f"{is_['no']:02d}-{is_['ad']}.pdf")
        jp = os.path.join(gecici, "pdf.json")
        json.dump(isler, open(jp, "w"))
        npm = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
        subprocess.run(["node", os.path.join(ROOT, "scripts", "mega-bilbord", "pdf.cjs"), jp],
                       check=True, env={**os.environ, "NODE_PATH": npm})
        return
    jp = os.path.join(gecici, "isler.json")
    json.dump(isler, open(jp, "w"))
    npm = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    subprocess.run(["node", os.path.join(ROOT, "scripts", "mega-bilbord", "render.cjs"), jp],
                   check=True, env={**os.environ, "NODE_PATH": npm})
    os.makedirs(OUT, exist_ok=True)
    for is_ in isler:
        tam = Image.open(json.load(open(is_["cikti"] + ".json"))[0]).convert("RGBA")
        yol = os.path.join(OUT, f"{is_['no']:02d}-{is_['ad']}.jpg")
        v2.sunum(tam, is_["no"], is_["ad"], yol)
        print("  →", os.path.relpath(yol, ROOT))


if __name__ == "__main__":
    main()
