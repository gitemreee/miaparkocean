#!/usr/bin/env python3
"""
180 m dev pano — 16. tur: müşterinin maket kurgusu (15.jpg) ile baştan.

Kurgu (soldan sağa, beyaz zemin):
  Tilda logosu · [boşluk: slogan] · dikey fotoğraf paneli (avlu) · [boşluk: finans] · ana görsel (gündüz
  render, ortada, panodan taşar) · [boşluk: aile + rozetler] · fotoğraf paneli (avlu/teras) · [boşluk: MİA
  logosu + yuvarlak detaylar] · Tilda logosu

Fotoğraf panelleri maketteki gibi tam yükseklik, keskin kenarlı. Alt şerit korunur (iletişim).

    python3.13 scripts/build-mega-bilbord-v16.py [--pdf]
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


v15 = _yukle("mb_v15", "build-mega-bilbord-v15.py")
v14, v11, v7, v6, v4, v2, mb = v15.v14, v15.v11, v15.v7, v15.v6, v15.v4, v15.v2, v15.mb
OUT = os.path.join(ROOT, "tabela", "mega-bilbord-180m-tur16")
TW, EXT = mb.TW, mb.EXT
y, kutu, damga, pill, pano = v4.y, v4.kutu, v4.damga, v11.pill, v11.pano
aile, AILE1, onay_liste, F = v14.aile, v14.AILE1, v11.onay_liste, v14.F
serit_buyut, KIR = v15.serit_buyut, v15.KIR

YESIL, ACIK = "#123d2a", "#2f8a4e"


def bina_olcekli(cx, s):
    """v4.bina ile aynı kahraman, s ölçeğinde (taşma üst kenara sığacak şekilde)."""
    HW, HH = round(v4.HW * s), round(v4.HH * s)
    hx, hy = round(cx - HW / 2), EXT - round(mb.UST_FR * HH)
    src = f"file://{mb.HERO}"
    dur = []
    for a, b in mb.SUTUNLAR:
        dur += [f"transparent {a * 100:.2f}%", f"#000 {a * 100:.2f}%", f"#000 {b * 100:.2f}%", f"transparent {b * 100:.2f}%"]
    maske = "linear-gradient(90deg," + ",".join(dur) + ")"
    tas = f'<img class="a" src="{src}" style="left:{hx}px;top:{hy}px;width:{HW}px;height:{HH}px;-webkit-mask-image:{maske}">'
    ic = f'<img class="a" src="{src}" style="left:{hx}px;top:{hy - EXT}px;width:{HW}px;height:{HH}px">'
    return tas, ic


def panel_foto(x, w, ad, pos="50% 50%"):
    """Maketteki gibi tam yükseklik, keskin kenarlı fotoğraf paneli."""
    return (f'<div class="a" style="left:{x}px;top:0;width:{w}px;height:718px;background:url({F[ad]}) {pos}/cover no-repeat;'
            f'box-shadow:0 0 60px rgba(0,0,0,.18)"></div>')


def M():
    r = dict(v4.SERIT_ACIK, serit=YESIL, serit_su="#8fd1a6")
    zemin = "linear-gradient(90deg,#f1f6f2 0%,#ffffff 20%,#ffffff 80%,#f1f6f2 100%)"
    tas, ic = bina_olcekli(8450, 0.78)
    rozet = lambda yy, t, bg, ek="": pill(11650, yy, t, bg, "#fff", 44, 108, "transform:translateX(-50%);letter-spacing:.06em" + ek)
    icerik = f"""
  {mb.tilda(250, 214, 290, False)}
  {y(1750, 150, "KİRAYA DEĞİL,", 125, 800, ACIK, maxw=1900)}
  {y(1750, 290, "KENDİ EVİNİZE", 125, 800, YESIL, maxw=1900)}
  {y(1750, 430, "ÖDEYİN.", 125, 800, YESIL, maxw=1900)}
  {panel_foto(3730, 880, "avlu2", "38% 60%")}
  {pill(5950, 60, "60 AY SABİT TAKSİT", ACIK, "#fff", 56, 110, "letter-spacing:.08em;transform:translateX(-50%)")}
  {kutu(4700, 200, 2500, 240, v6.fiyat_satiri(YESIL, 136, ACIK, "rgba(18,61,42,.25)"), "display:flex;justify-content:center")}
  {onay_liste(4760, 470, YESIL, ACIK, "#fff", 42, 108, 1220)}
  {aile(9900, 950, AILE1, -15)}
  {rozet(100, "VADE FARKI YOK", "#111")}
  {pill(11640, 232, "BANKA YOK", KIR, "#fff", 44, 108, "transform:translateX(-100%);letter-spacing:.06em")}
  {pill(11660, 232, "KREDİ YOK", KIR, "#fff", 44, 108, "letter-spacing:.06em")}
  {rozet(364, "ARA ÖDEME YOK", "#111")}
  {rozet(496, "60 AY SABİT TAKSİT", KIR)}
  {panel_foto(12460, 1530, "teras", "50% 55%")}
  {mb.mia(14250, 159, 400, False)}
  {v11.daire_foto(15330, 200, 380, "salon")}
  {v11.daire_foto(15740, 380, 380, "yatak")}
  {v11.daire_foto(15360, 525, 380, "mutfak")}
  {mb.tilda(16480, 219, 280, False)}
  {damga(17720, 610, 180, "SON", "DAİRELER", "KAÇIRMAYIN!", zemin=ACIK, yazi="#fff")}"""
    return serit_buyut(pano(r, zemin, "", icerik, tas, ic))


TASARIMLAR = [(M, "maket-kurgusu")]


def main():
    gecici = tempfile.mkdtemp(prefix="mega16-")
    isler = []
    for i, (fn, ad) in enumerate(TASARIMLAR, 1):
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
