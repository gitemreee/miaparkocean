#!/usr/bin/env python3
"""
MİA PARK OCEAN — dalga varlıkları.

Dalga YENİDEN ÇİZİLMEZ. Kaynak, marka paketinden gelen hazır grafiktir:

  brand-source/wave-source.png   (mia-park-ocean-wave-transparent.png)

Bu betik onu olduğu gibi siteye taşır ve yalnızca CSS maskeleri türetir:

  public/brand/wave.png / .webp    → şeridin kendisi, orijinal pikseller
  public/brand/wave-mask.png       → kurdeleler + altı dolu (mask-image)
  public/brand/wave-mask-solid.png → üst kenardan aşağısı tamamen dolu
  src/components/ui/wave-path.ts   → varlık yolları

Maskeler yalnızca alfa kanalından türetilir; şekle dokunulmaz.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "brand-source" / "wave-source.png"
OUT = ROOT / "public" / "brand"
TS_OUT = ROOT / "src" / "components" / "ui" / "wave-path.ts"

ALPHA_MIN = 24
HOLE_MAX = 6  # bu kadar ince saydam boşluklar kapatılır (boya dokusu)


def median_smooth(y: np.ndarray, k: int) -> np.ndarray:
    pad = k // 2
    padded = np.pad(y, pad, mode="edge")
    return np.array([np.median(padded[i : i + k]) for i in range(len(y))])


def mean_smooth(y: np.ndarray, k: int) -> np.ndarray:
    pad = k // 2
    padded = np.pad(y, pad, mode="edge")
    return np.convolve(padded, np.ones(k) / k, mode="valid")


def edge(mask: np.ndarray, which: str) -> np.ndarray:
    """Her sütun için üst ya da alt kenar; boş sütunlar komşudan doldurulur."""
    h, w = mask.shape
    out = np.full(w, np.nan)
    for x in range(w):
        ys = np.where(mask[:, x])[0]
        if len(ys):
            out[x] = ys.min() if which == "top" else ys.max()
    idx = np.where(~np.isnan(out))[0]
    if len(idx):
        out[: idx[0]] = out[idx[0]]
        out[idx[-1] + 1 :] = out[idx[-1]]
    for x in np.where(np.isnan(out))[0]:
        left, right = x - 1, x + 1
        while right < w and np.isnan(out[right]):
            right += 1
        if 0 <= left and right < w:
            t = (x - left) / (right - left)
            out[x] = out[left] * (1 - t) + out[right] * t
    return out


def to_mask_png(alpha: np.ndarray, blur: float = 1.6) -> Image.Image:
    img = Image.fromarray(alpha.astype(np.uint8), "L").filter(
        ImageFilter.GaussianBlur(blur)
    )
    a = np.asarray(img)
    return Image.fromarray(np.dstack([np.full_like(a, 255)] * 3 + [a]), "RGBA")


def main() -> None:
    src = Image.open(SRC).convert("RGBA")
    src = src.crop(src.getbbox())
    w, h = src.size
    print(f"kaynak {w}x{h}")

    # ---------- 1) Şeridi olduğu gibi yayınla ----------
    src.save(OUT / "wave.png", optimize=True)
    src.save(OUT / "wave.webp", quality=95, method=6)
    print(f"wave.png / wave.webp → {w}x{h}")

    alpha = np.asarray(src)[:, :, 3]
    solid = alpha > ALPHA_MIN

    # Boya dokusundaki iğne deliklerini kapat; kurdele arasındaki geniş
    # boşluklar (dalganın karakteri) olduğu gibi kalır.
    for x in range(w):
        col = solid[:, x]
        ys = np.where(col)[0]
        if len(ys) == 0:
            continue
        y = ys.min()
        while y <= ys.max():
            if not col[y]:
                e = y
                while e <= ys.max() and not col[e]:
                    e += 1
                if e - y <= HOLE_MAX:
                    col[y:e] = True
                y = e
            else:
                y += 1

    # ---------- 2) Kurdeleli maske (altı dolu) ----------
    bottom = mean_smooth(median_smooth(edge(solid, "bottom"), 31), 25)
    below = np.arange(h)[:, None] >= bottom[None, :]
    to_mask_png(np.maximum(solid, below) * 255).save(
        OUT / "wave-mask.png", optimize=True
    )
    print("wave-mask.png")

    # ---------- 3) Boşluksuz siluet ----------
    # Üst kenar birebir aynı; kurdele araları dolu. Koyu fotoğraf üstünde
    # alt katman olarak kullanılır ki aralardan fotoğraf sızmasın.
    # Kurdelelerin ayrıldığı yerdeki çentik ayırıcı olarak kusur gibi
    # görünüyor; geniş pencereyle yuvarlanır, eğrinin gidişi değişmez.
    top = mean_smooth(median_smooth(edge(solid, "top"), 81), 61)
    to_mask_png((np.arange(h)[:, None] >= top[None, :]) * 255).save(
        OUT / "wave-mask-solid.png", optimize=True
    )
    print("wave-mask-solid.png")

    # ---------- 4) TypeScript sabitleri ----------
    TS_OUT.write_text(
        f'''/**
 * MİA PARK OCEAN dalgası — `scripts/build-wave.py` tarafından
 * `brand-source/wave-source.png` üzerinden üretilir.
 *
 * ELLE DÜZENLEMEYİN. Dalga yeniden çizilmez; kaynak grafik olduğu gibi
 * kullanılır. Sitedeki her dalga bu varlıklardan birini gösterir.
 */

/** Dalga şeridi — kaynak grafiğin orijinal pikselleri, şeffaf zemin. */
export const WAVE_IMAGE = "/brand/wave.webp";

/**
 * Aynı dalganın dolgulu maskesi: kurdeleler + altındaki her şey opak.
 * `mask-image` olarak kullanıldığında üst kenarı birebir dalga olan dolu
 * bir panel verir.
 */
export const WAVE_MASK = "/brand/wave-mask.png";

/**
 * Aynı dalganın boşluksuz silueti — üst kenar birebir aynı, kurdele araları
 * dolu. Koyu fotoğraf üstünde alt katman olarak kullanılır.
 */
export const WAVE_MASK_SOLID = "/brand/wave-mask-solid.png";

/** Şeridin en/boy oranı. */
export const WAVE_RATIO = {w / h:.4f};
''',
        encoding="utf-8",
    )
    print("wave-path.ts")


if __name__ == "__main__":
    main()
