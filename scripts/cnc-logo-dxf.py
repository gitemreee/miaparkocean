#!/usr/bin/env python3
"""
MİA PARK OCEAN logosu → CNC kesim vektörleri.

Kaynak: potrace'in GeoJSON çıktısı (düz parçalı halkalar) → mm ölçek, Douglas-Peucker sadeleştirme →
  - DXF 2000 (LWPOLYLINE, kapalı, mm, $INSUNITS=4)         *-2000.dxf
  - DXF R12  (POLYLINE/VERTEX, kapalı, yaysız)              *-r12.dxf
  - PLT (HPGL, 40 plu/mm)                                    *.plt
  - SVG (mm, evenodd)                                        *.svg
  - önizleme PNG
Potrace PDF/EPS ayrıca üretilir.

    potrace -b geojson -t 10 -a 1.0 -O 0.2 -o mia-cnc.geojson mia-cnc.pbm
    python3.13 scripts/cnc-logo-dxf.py mia-cnc.geojson public/brand/cnc 1000
"""

import json
import math
import os
import sys

import ezdxf
from ezdxf import units
from PIL import Image, ImageDraw


def rdp(pts, tol):
    """Douglas-Peucker (kapalı halka için ilk/son nokta sabit)."""
    if len(pts) < 3:
        return pts
    (x1, y1), (x2, y2) = pts[0], pts[-1]
    dx, dy = x2 - x1, y2 - y1
    n = math.hypot(dx, dy)
    best, idx = -1.0, 0
    for i in range(1, len(pts) - 1):
        x, y = pts[i]
        d = abs(dy * x - dx * y + x2 * y1 - y2 * x1) / n if n else math.hypot(x - x1, y - y1)
        if d > best:
            best, idx = d, i
    if best > tol:
        return rdp(pts[:idx + 1], tol)[:-1] + rdp(pts[idx:], tol)
    return [pts[0], pts[-1]]


def sadelestir(ring, tol):
    pts = ring[:-1] if ring[0] == ring[-1] else ring[:]
    # en uzak iki noktadan böl: kapalı halka için RDP
    far = max(range(len(pts)), key=lambda i: (pts[i][0] - pts[0][0]) ** 2 + (pts[i][1] - pts[0][1]) ** 2)
    a = rdp(pts[:far + 1], tol)
    b = rdp(pts[far:] + [pts[0]], tol)
    out = a[:-1] + b[:-1]
    return out


def main():
    src, outdir, genislik_mm = sys.argv[1], sys.argv[2], float(sys.argv[3])
    tol_mm = 0.03
    g = json.load(open(src))
    halkalar = []  # (feature_no, ring_no, [(x,y)...]) ham
    for fi, ft in enumerate(g["features"]):
        for ri, ring in enumerate(ft["geometry"]["coordinates"]):
            halkalar.append((fi, ri, [(float(x), float(y)) for x, y in ring]))
    xs = [x for _, _, r in halkalar for x, _ in r]
    ys = [y for _, _, r in halkalar for _, y in r]
    x0, y0, x1, y1 = min(xs), min(ys), max(xs), max(ys)
    k = genislik_mm / (x1 - x0)
    W, H = genislik_mm, (y1 - y0) * k
    temiz = []
    for fi, ri, r in halkalar:
        mm = [((x - x0) * k, (y - y0) * k) for x, y in r]
        s = sadelestir(mm, tol_mm)
        temiz.append((fi, ri, [(round(x, 3), round(y, 3)) for x, y in s]))
    n_pts = sum(len(r) for _, _, r in temiz)
    print(f"logo {W:.1f} x {H:.1f} mm, {len(temiz)} kontür, {n_pts} nokta (ham {len(xs)})")

    ad = os.path.join(outdir, "mia-park-ocean-logo")
    os.makedirs(outdir, exist_ok=True)

    # DXF 2000
    doc = ezdxf.new("R2000", setup=True)
    doc.units = units.MM
    doc.header["$INSUNITS"] = 4
    doc.header["$EXTMIN"] = (0, 0, 0)
    doc.header["$EXTMAX"] = (W, H, 0)
    doc.layers.add("KESIM", color=7)
    msp = doc.modelspace()
    for fi, ri, r in temiz:
        msp.add_lwpolyline(r, close=True, dxfattribs={"layer": "KESIM"})
    doc.saveas(ad + "-2000.dxf")

    # DXF R12 (en geniş uyumluluk)
    d12 = ezdxf.new("R12")
    d12.header["$EXTMIN"] = (0, 0, 0)
    d12.header["$EXTMAX"] = (W, H, 0)
    d12.layers.add("KESIM", color=7)
    m12 = d12.modelspace()
    for fi, ri, r in temiz:
        m12.add_polyline2d(r, close=True, dxfattribs={"layer": "KESIM"})
    d12.saveas(ad + "-r12.dxf")

    # PLT (HPGL): 40 plu = 1 mm
    plt = ["IN;SP1;"]
    for fi, ri, r in temiz:
        p = [(round(x * 40), round(y * 40)) for x, y in r]
        plt.append(f"PU{p[0][0]},{p[0][1]};")
        plt.append("PD" + ",".join(f"{x},{y}" for x, y in p[1:] + [p[0]]) + ";")
    plt.append("PU;SP0;IN;")
    open(ad + ".plt", "w").write("\n".join(plt))

    # SVG (mm, y aşağı)
    yol = []
    for fi, ri, r in temiz:
        yol.append("M" + " L".join(f"{x:.3f},{H - y:.3f}" for x, y in r) + " Z")
    svg = (f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="{W:.3f}mm" '
           f'height="{H:.3f}mm" viewBox="0 0 {W:.3f} {H:.3f}">\n<path fill="#000" fill-rule="evenodd" d="{" ".join(yol)}"/>\n</svg>\n')
    open(ad + ".svg", "w").write(svg)

    # önizleme PNG (evenodd: her feature'ın dış halkası siyah, delikleri beyaz)
    sc = 2.0
    im = Image.new("L", (int(W * sc) + 40, int(H * sc) + 40), 255)
    dr = ImageDraw.Draw(im)
    for fi, ri, r in temiz:
        pts = [(20 + x * sc, 20 + (H - y) * sc) for x, y in r]
        dr.polygon(pts, fill=0 if ri == 0 else 255, outline=0)
    im.save(ad + "-onizleme.png")

    # denetim
    for p in (ad + "-2000.dxf", ad + "-r12.dxf"):
        a = ezdxf.readfile(p).audit()
        print(os.path.basename(p), "hata:", len(a.errors), "düzeltme:", len(a.fixes))


if __name__ == "__main__":
    main()
