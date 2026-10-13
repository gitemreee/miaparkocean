#!/usr/bin/env python3
"""
MİA PARK OCEAN × TİLDA İNŞAAT — Emlak Konut tarzı reklam görselleri.

Tipografi HTML/CSS ile kurulur ve Chromium'da 2x çözünürlükte çizilir
(gerçek kerning, eşit genişlikli rakamlar, cam panel). Zeminler GERÇEK
proje render'ları:
  · gece  — signage-source/night-gate-temiz.jpg (ufuktaki evler temizlendi)
  · avlu  — signage-source/courtyard-pools.jpg (proje içi, havuzlu avlu)

Şablon: scripts/reklam-sablon/sablon.html
Çıktı : sosyal-medya/turkuaz-kampanya/tilda/tilda-<zemin>-<tip>-<format>.jpg

    python3.13 scripts/build-tilda-reklam.py
"""

import importlib.util as _il
import json
import os
import subprocess
import sys
import tempfile

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SABLON = os.path.join(ROOT, "scripts", "reklam-sablon")
OUT = os.path.join(ROOT, "sosyal-medya", "turkuaz-kampanya", "tilda")
FONT = os.path.join(ROOT, "brand-source", "fonts", "Montserrat-var.ttf")

_spec = _il.spec_from_file_location(
    "build_film", os.path.join(ROOT, "scripts", "build-film.py"))
bf = _il.module_from_spec(_spec)
sys.modules["build_film"] = bf
_spec.loader.exec_module(bf)

DAIRELER = [("1+0", "699.000", "29.900", "1plus0"),
            ("1+1", "999.000", "39.900", "1plus1")]

# her format: kanvas, ölçek, üst blok y, alt bant alt boşluğu
FORMATLAR = {
    "story": dict(w=1080, h=1920, s=1.0, ust=210, alt=120),
    "kare": dict(w=1080, h=1080, s=0.74, ust=48, alt=34),
}

# zemin görsel yerleşimi (CSS) — format başına
ZEMINLER = {
    "gece": dict(
        img=os.path.join(ROOT, "signage-source", "night-gate-temiz.jpg"),
        stil={"story": "width:176%;left:-38%;top:640px;",
              "kare": "width:136%;left:-18%;top:300px;"}),
    "avlu": dict(
        img=os.path.join(ROOT, "signage-source", "courtyard-pools.jpg"),
        stil={"story": "height:100%;left:50%;transform:translateX(-50%);top:0;",
              "kare": "height:112%;left:50%;transform:translateX(-50%);top:-6%;"}),
}


def logolar(dizin):
    """Beyaz logoları şablonun okuyacağı PNG'lere yazar."""
    bf.logo_white(900).save(os.path.join(dizin, "mia.png"))
    bf.partner_white(900).save(os.path.join(dizin, "ocean.png"))
    return {"mia": os.path.join(dizin, "mia.png"),
            "ocean": os.path.join(dizin, "ocean.png"),
            "tilda": os.path.join(ROOT, "public", "brand", "logo-tilda-beyaz.png")}


def main():
    os.makedirs(OUT, exist_ok=True)
    gecici = tempfile.mkdtemp(prefix="reklam-")
    lg = logolar(gecici)
    sablon = open(os.path.join(SABLON, "sablon.html"), encoding="utf-8").read()

    isler = []
    for zad, z in ZEMINLER.items():
        for tip, pesinat, taksit, ek in DAIRELER:
            for fad, f in FORMATLAR.items():
                html = (sablon
                        .replace("__FONT__", "file://" + FONT)
                        .replace("__TUR__", zad)
                        .replace("__VARS__", f"--w:{f['w']}px;--h:{f['h']}px;"
                                 f"--s:{f['s']};--ust:{f['ust']}px;--alt:{f['alt']}px;")
                        .replace("__IMG__", "file://" + z["img"])
                        .replace("__IMGSTYLE__", z["stil"][fad])
                        .replace("__TIP__", tip)
                        .replace("__PESINAT__", pesinat)
                        .replace("__TAKSIT__", taksit)
                        .replace("__L_TILDA__", "file://" + lg["tilda"])
                        .replace("__L_MIA__", "file://" + lg["mia"])
                        .replace("__L_OCEAN__", "file://" + lg["ocean"]))
                ad = f"tilda-{zad}-{ek}-{fad}"
                hp = os.path.join(gecici, ad + ".html")
                open(hp, "w", encoding="utf-8").write(html)
                isler.append(dict(html=hp, png=os.path.join(gecici, ad + ".png"),
                                  w=f["w"], h=f["h"], ad=ad))

    jp = os.path.join(gecici, "isler.json")
    json.dump(isler, open(jp, "w"))
    npm_kok = subprocess.run(["npm", "root", "-g"], capture_output=True,
                             text=True).stdout.strip()
    subprocess.run(["node", os.path.join(SABLON, "render.cjs"), jp], check=True,
                   env={**os.environ, "NODE_PATH": npm_kok})

    for is_ in isler:
        im = Image.open(is_["png"]).convert("RGB")
        im = im.resize((is_["w"], is_["h"]), Image.LANCZOS)
        yol = os.path.join(OUT, is_["ad"] + ".jpg")
        im.save(yol, quality=94, optimize=True)
        print("  →", os.path.relpath(yol, ROOT))


if __name__ == "__main__":
    main()
