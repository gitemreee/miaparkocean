#!/usr/bin/env python3
"""
180 m dev pano — 15. tur: 14/4 (yeşil & çocuklar) üzerinden devam.

İki uçta Tilda logosu · "KİRAYA DEĞİL, KENDİ EVİNİZE ÖDEYİN." eklendi · alt şeritte telefon büyütüldü.

    python3.13 scripts/build-mega-bilbord-v15.py [--pdf]
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


v14 = _yukle("mb_v14", "build-mega-bilbord-v14.py")
v11, v7, v6, v4, v2, mb = v14.v11, v14.v7, v14.v6, v14.v4, v14.v2, v14.mb
OUT = os.path.join(ROOT, "tabela", "mega-bilbord-180m-tur15")
TW = mb.TW
y, kutu, damga, pill, pano = v4.y, v4.kutu, v4.damga, v11.pill, v11.pano
yumusak, aile, AILE1, onay_liste = v14.yumusak, v14.aile, v14.AILE1, v11.onay_liste

TEL = "0540 028 00 41"


def serit_buyut(html):
    """Alt şeritte telefonu büyüt (yazı 62 → 96 px, simge 70 → 100 px)."""
    eski = f'<div class="oge">{v2.IK_TEL}{TEL}</div>'
    simge = v2.IK_TEL.replace("<svg", '<svg style="width:100px;height:100px"', 1)
    yeni = f'<div class="oge" style="font-size:96px;font-weight:800;letter-spacing:.02em">{simge}{TEL}</div>'
    assert eski in html, "şerit telefon öğesi bulunamadı"
    return html.replace(eski, yeni)


def Y():
    yesil, acik = "#123d2a", "#2f8a4e"
    r = dict(v4.SERIT_ACIK, serit=yesil, serit_su="#8fd1a6")
    zemin = "linear-gradient(90deg,#eef5ef 0%,#f8fbf8 45%,#e9f3eb 100%)"
    tas, ic = v4.bina(9700)
    icerik = f"""
  {mb.tilda(300, 80, 300, False)}
  {y(1900, 55, "ÇOCUKLARINIZ İÇİN", 165, 800, acik, maxw=2900)}
  {y(1900, 235, "GÜVENLİ BİR GELECEK.", 185, 800, yesil, maxw=2900)}
  {y(1905, 505, "KİRAYA DEĞİL,", 100, 800, acik, maxw=2900)}
  {y(1905, 615, "KENDİ EVİNİZE ÖDEYİN.", 80, 800, yesil, maxw=2900)}
  {yumusak(4750, 0, 2700, 718, "park", "50% 55%", (.2, .25), (0, .12))}
  {aile(11550, 950, AILE1, -15)}
  {pill(12950, 60, "60 AY SABİT TAKSİT", acik, "#fff", 60, 120, "letter-spacing:.08em")}
  {kutu(12900, 215, 3100, 300, v6.fiyat_satiri(yesil, 155, acik, "rgba(18,61,42,.25)"))}
  {onay_liste(12950, 540, yesil, acik, "#fff", 44, 90, 1450)}
  {mb.mia(16450, 50, 300, False)}
  {mb.tilda(16300, 420, 230, False)}
  {damga(17720, 600, 200, "SON", "DAİRELER", "KAÇIRMAYIN!", zemin=acik, yazi="#fff")}"""
    return serit_buyut(pano(r, zemin, "", icerik, tas, ic))


TASARIMLAR = [(Y, "yesil-cocuklar-iki-tilda")]


def main():
    gecici = tempfile.mkdtemp(prefix="mega15-")
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
