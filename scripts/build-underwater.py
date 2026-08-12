#!/usr/bin/env python3
"""
MİA PARK OCEAN — su altı dokusu.

Footer "suya iniş" olarak kurgulu; bu betik oraya derinlik veren dokuyu
üretir: yüzeyden süzülen ışık huzmeleri ve yükselen kabarcıklar.

Stok görsel kullanılmaz. Doku BEYAZ üstüne alfa olarak üretilir; rengini
CSS'teki zemin verir, böylece marka paletinden hiç çıkmaz ve her ölçekte
net kalır. Çıktı tek dosya:

  public/brand/underwater.webp   (1400x700, şeffaf)
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public" / "brand" / "underwater.webp"

W, H = 1400, 700
SS = 2  # süper örnekleme

# (x konumu 0-1, genişlik px, eğim, yoğunluk 0-1)
RAYS = [
    (0.08, 120, 0.16, 0.55),
    (0.17, 62, 0.13, 0.34),
    (0.29, 168, 0.19, 0.7),
    (0.38, 74, 0.15, 0.3),
    (0.5, 132, 0.1, 0.5),
    (0.61, 92, -0.09, 0.42),
    (0.72, 190, -0.14, 0.66),
    (0.83, 70, -0.11, 0.32),
    (0.92, 140, -0.17, 0.5),
]

# (x 0-1, y 0-1, yarıçap px, opaklık)
BUBBLES = [
    (0.21, 0.62, 3.9, 0.5), (0.235, 0.48, 2.2, 0.42), (0.19, 0.36, 2.8, 0.36),
    (0.26, 0.28, 1.7, 0.3), (0.225, 0.16, 2.2, 0.24),
    (0.47, 0.72, 5.0, 0.46), (0.5, 0.56, 2.8, 0.4), (0.455, 0.42, 3.3, 0.34),
    (0.515, 0.3, 1.9, 0.28), (0.48, 0.19, 2.5, 0.22), (0.53, 0.1, 1.7, 0.16),
    (0.68, 0.66, 3.3, 0.44), (0.71, 0.5, 2.2, 0.36), (0.665, 0.38, 2.8, 0.3),
    (0.72, 0.24, 1.7, 0.24),
    (0.87, 0.58, 2.8, 0.34), (0.9, 0.44, 1.9, 0.28), (0.855, 0.3, 2.2, 0.22),
    (0.12, 0.5, 2.2, 0.3), (0.145, 0.34, 1.7, 0.24),
    (0.35, 0.55, 2.2, 0.3), (0.37, 0.4, 1.7, 0.22),
]


def light_rays() -> np.ndarray:
    """Yüzeyden aşağı süzülen ışık huzmeleri (alfa haritası)."""
    w, h = W * SS, H * SS
    acc = np.zeros((h, w), np.float32)
    xx = np.arange(w, dtype=np.float32)[None, :]
    yy = np.arange(h, dtype=np.float32)[:, None]
    t = yy / h  # 0 = yüzey, 1 = derin

    for x0, width, slant, strength in RAYS:
        cx = x0 * w + slant * yy * SS * 0.9
        sigma = (width * SS) * (0.55 + 1.7 * t)  # aşağı indikçe yayılır
        prof = np.exp(-((xx - cx) ** 2) / (2 * sigma**2))
        # Yüzeyde parlak, derinde söner
        fade = np.clip(1.0 - t, 0, 1) ** 1.9
        acc += prof * fade * strength

    acc = acc / max(acc.max(), 1e-6)
    img = Image.fromarray((np.clip(acc, 0, 1) * 255).astype(np.uint8), "L")
    img = img.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(6))
    return np.asarray(img).astype(np.float32) / 255.0


def bubbles() -> np.ndarray:
    """Yükselen kabarcıklar — içi boş halkalar, üstte küçük parlama."""
    w, h = W * SS, H * SS
    img = Image.new("L", (w, h), 0)
    dr = ImageDraw.Draw(img)
    for x0, y0, r, op in BUBBLES:
        cx, cy, rr = x0 * w, y0 * h, r * SS
        a = int(255 * op)
        dr.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=a, width=max(2, int(rr * 0.42)))
        # üst sol parlama
        gr = rr * 0.34
        dr.ellipse(
            [cx - rr * 0.42 - gr, cy - rr * 0.42 - gr, cx - rr * 0.42 + gr, cy - rr * 0.42 + gr],
            fill=int(a * 0.9),
        )
    img = img.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.7))
    return np.asarray(img).astype(np.float32) / 255.0


def caustics() -> np.ndarray:
    """Yüzeye yakın hafif su titreşimi — huzmelere doku katar."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    v = (
        np.sin(xx / 46.0 + np.sin(yy / 90.0) * 2.2)
        + np.sin(xx / 23.0 - yy / 140.0)
        + np.sin((xx + yy) / 70.0)
    )
    v = (v - v.min()) / (v.max() - v.min())
    fade = np.clip(1.0 - yy / H, 0, 1) ** 2.6
    return v * fade


def main() -> None:
    a = 0.72 * light_rays() + 0.5 * bubbles() + 0.16 * caustics()
    a = np.clip(a, 0, 1)
    # Üst kenar dalganın altında başlasın: ilk %6 yumuşakça açılır
    ramp = np.clip(np.arange(H, dtype=np.float32) / (H * 0.06), 0, 1)[:, None]
    a *= ramp
    alpha = (a * 255).astype(np.uint8)
    rgb = np.full((H, W, 3), 255, np.uint8)
    img = Image.fromarray(np.dstack([rgb, alpha]), "RGBA")
    img.save(OUT, quality=72, method=6)
    print(f"{OUT.name} → {W}x{H} · {OUT.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
