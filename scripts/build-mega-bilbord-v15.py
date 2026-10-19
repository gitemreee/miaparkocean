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
KIR = "#e3262e"


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
    tas, ic = v4.bina(10050)
    icerik = f"""
  {mb.tilda(300, 209, 300, False)}
  {y(1900, 150, "KİRAYA DEĞİL,", 112, 800, acik, maxw=1150)}
  {y(1900, 275, "KENDİ EVİNİZE", 112, 800, yesil, maxw=1150)}
  {y(1900, 400, "ÖDEYİN.", 112, 800, yesil, maxw=1150)}
  {pill(3200, 55, "60 AY SABİT TAKSİT", acik, "#fff", 52, 104, "letter-spacing:.08em")}
  {kutu(3150, 180, 2600, 240, v6.fiyat_satiri(yesil, 128, acik, "rgba(18,61,42,.25)"))}
  {onay_liste(3200, 455, yesil, acik, "#fff", 44, 112, 1250)}
  {yumusak(5650, 0, 2000, 718, "park", "50% 55%", (.22, .3), (0, .12))}
  {pill(7750, 95, "VADE FARKI YOK", "#111", "#fff", 46, 112, "transform:translateX(-50%);letter-spacing:.06em")}
  {pill(7740, 230, "BANKA YOK", KIR, "#fff", 46, 112, "transform:translateX(-100%);letter-spacing:.06em")}
  {pill(7760, 230, "KREDİ YOK", KIR, "#fff", 46, 112, "letter-spacing:.06em")}
  {pill(7750, 365, "ARA ÖDEME YOK", "#111", "#fff", 46, 112, "transform:translateX(-50%);letter-spacing:.06em")}
  {pill(7750, 500, "60 AY SABİT TAKSİT", KIR, "#fff", 46, 112, "transform:translateX(-50%);letter-spacing:.06em")}
  {aile(11900, 950, AILE1, -15)}
  {pill(13300, 60, "60 AY SABİT TAKSİT", acik, "#fff", 58, 116, "letter-spacing:.08em")}
  {kutu(13250, 215, 2700, 300, v6.fiyat_satiri(yesil, 140, acik, "rgba(18,61,42,.25)"))}
  {onay_liste(13300, 540, yesil, acik, "#fff", 42, 90, 1250)}
  {v11.daire_foto(15770, 200, 380, "salon")}
  {v11.daire_foto(16180, 380, 380, "yatak")}
  {v11.daire_foto(15800, 525, 380, "mutfak")}
  {mb.mia(16560, 219, 280, False)}
  {mb.tilda(16980, 259, 200, False)}
  {damga(17800, 605, 180, "SON", "DAİRELER", "KAÇIRMAYIN!", zemin=acik, yazi="#fff")}"""
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
