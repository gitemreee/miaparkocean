#!/usr/bin/env python3
"""
Raster logoları potrace ile vektöre (SVG) çevirir — dev ölçekli baskı için.

Her logo renk katmanlarına ayrılır (piksel en yakın palet rengine atanır),
her katman 4x büyütülüp yumuşatılarak potrace'e verilir, katmanlar tek
SVG'de üst üste dizilir. Sonuç sonsuz ölçeklenir; 180 m'lik panoda bile
kenarlar keskin kalır.

Kaynaklar:
  tilda : PDF'e gömülü özgün görüntü (3480x805), lacivert + bronz
  mia   : public/brand/logo-ocean-white.png (MİA PARK OCEAN kilidi, tek renk)
  ocean : public/ocean-logo.webp (OCEAN GAYRİMENKUL, tek renk)

Çıktı: public/brand/vektor/<ad>.svg  (+ beyaz varyantları)

    python3.13 scripts/vektorle-logolar.py <tilda-gomulu.png>
"""

import os
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "public", "brand", "vektor")
OLCEK = 4


def katman_svg(maske: np.ndarray, gecici: str, ad: str) -> tuple[str, int, int]:
    """Bool maske → potrace path'leri (svg <g> içeriği), genişlik, yükseklik."""
    im = Image.fromarray((maske * 255).astype(np.uint8), "L")
    im = im.resize((im.width * OLCEK, im.height * OLCEK), Image.LANCZOS)
    im = im.filter(ImageFilter.GaussianBlur(OLCEK * 0.6))
    im = im.point(lambda v: 0 if v >= 128 else 255).convert("1")  # siyah = dolu
    pbm = os.path.join(gecici, ad + ".pbm")
    svg = os.path.join(gecici, ad + ".svg")
    im.save(pbm)
    subprocess.run(["potrace", pbm, "-s", "-o", svg, "--turdsize", "8",
                    "--alphamax", "1.0", "--opttolerance", "0.2", "--flat"],
                   check=True)
    metin = open(svg).read()
    g0 = metin.index("<g")
    g1 = metin.rindex("</g>") + 4
    return metin[g0:g1], im.width, im.height


def yaz(ad, katmanlar, w, h):
    """katmanlar: [(renk_hex, g_icerigi)]"""
    os.makedirs(OUT, exist_ok=True)
    govde = "\n".join(g.replace('fill="#000000"', f'fill="{renk}"', 1)
                      for renk, g in katmanlar)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
           f'width="{w}" height="{h}">\n{govde}\n</svg>\n')
    yol = os.path.join(OUT, ad + ".svg")
    open(yol, "w").write(svg)
    print("  →", os.path.relpath(yol, ROOT))


def sinifla(rgb: np.ndarray, palet: dict) -> dict:
    """Her pikseli en yakın palet rengine atar; ad → bool maske."""
    adlar = list(palet)
    renkler = np.array([palet[a] for a in adlar], np.float32)
    d = ((rgb[:, :, None, :] - renkler[None, None]) ** 2).sum(-1)
    en = d.argmin(-1)
    return {a: en == i for i, a in enumerate(adlar)}


def kirp(*maskeler, pay=6):
    birlesik = np.zeros_like(maskeler[0])
    for m in maskeler:
        birlesik |= m
    ys, xs = np.where(birlesik)
    y0, y1 = max(ys.min() - pay, 0), ys.max() + pay
    x0, x1 = max(xs.min() - pay, 0), xs.max() + pay
    return [m[y0:y1, x0:x1] for m in maskeler]


def main():
    gecici = tempfile.mkdtemp(prefix="vektor-")

    # --- Tilda: lacivert + bronz
    rgb = np.asarray(Image.open(sys.argv[1]).convert("RGB")).astype(np.float32)
    m = sinifla(rgb, {"zemin": (242, 242, 242), "lacivert": (18, 33, 44),
                      "bronz": (168, 122, 85)})
    lac, brz = kirp(m["lacivert"], m["bronz"])
    g_lac, w, h = katman_svg(lac, gecici, "tilda-lac")
    g_brz, _, _ = katman_svg(brz, gecici, "tilda-brz")
    yaz("tilda", [("#13212c", g_lac), ("#a87a55", g_brz)], w, h)
    yaz("tilda-beyaz", [("#ffffff", g_lac), ("#b88a5e", g_brz)], w, h)

    # --- MİA: tek renk (beyaz kilit, alfa kanalından)
    a = np.asarray(Image.open(os.path.join(
        ROOT, "public", "brand", "logo-ocean-white.png")).convert("RGBA"))[:, :, 3]
    (mia,) = kirp(a > 110)
    g, w, h = katman_svg(mia, gecici, "mia")
    yaz("mia-beyaz", [("#ffffff", g)], w, h)
    yaz("mia-lacivert", [("#0b3a50", g)], w, h)

    # --- Ocean: beyaz zemin üzerinde koyu logo
    rgb = np.asarray(Image.open(os.path.join(
        ROOT, "public", "ocean-logo.webp")).convert("RGB")).astype(np.float32)
    koyu = rgb.min(axis=2) < 150
    (oc,) = kirp(koyu)
    # kaynak çok küçük (298 px): izlemeden önce ekstra büyüt
    big = Image.fromarray((oc * 255).astype(np.uint8), "L")
    big = big.resize((big.width * 4, big.height * 4), Image.LANCZOS)
    oc = np.asarray(big.filter(ImageFilter.GaussianBlur(2.2))) > 128
    g, w, h = katman_svg(oc, gecici, "ocean")
    yaz("ocean-beyaz", [("#ffffff", g)], w, h)
    yaz("ocean-lacivert", [("#0d3b66", g)], w, h)


if __name__ == "__main__":
    main()
