#!/usr/bin/env python3
"""
MİA PARK OCEAN — dalga varlıkları.

Dalga YENİDEN ÇİZİLMEZ. Kaynak, marka paketinden gelen hazır grafiktir:

  brand-source/wave-source.png   (mia-park-ocean-wave-transparent.png)

Bu betik onu olduğu gibi siteye taşır ve yalnızca CSS maskeleri türetir:

  public/brand/wave.png / .webp    → şeridin kendisi, orijinal pikseller
  public/brand/wave-mask.png       → kurdeleler + altı dolu (mask-image)
  public/brand/wave-mask-base.png  → yalnızca alt siluetin altı
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


# Maskeler CSS'te `mask-size: 100% 100%` ile esnetiliyor; kaynak çözünürlük
# gerekmiyor. Bu genişlik 2x ekranda bile yeterli ve dosyayı küçük tutuyor.
MASK_WIDTH = 1200


def to_mask_png(alpha: np.ndarray, blur: float = 1.6) -> Image.Image:
    img = Image.fromarray(alpha.astype(np.uint8), "L").filter(
        ImageFilter.GaussianBlur(blur)
    )
    if img.width > MASK_WIDTH:
        img = img.resize(
            (MASK_WIDTH, round(img.height * MASK_WIDTH / img.width)), Image.LANCZOS
        )
    a = np.asarray(img)
    return Image.fromarray(np.dstack([np.full_like(a, 255)] * 3 + [a]), "RGBA")


def _gauss1d(sigma: float) -> np.ndarray:
    r = max(1, int(sigma * 3))
    x = np.arange(-r, r + 1, dtype=np.float32)
    k = np.exp(-(x**2) / (2 * sigma * sigma))
    return k / k.sum()


def _sep_blur(img: np.ndarray, sx: float, sy: float) -> np.ndarray:
    """Ayrık yönlü Gauss bulanıklığı (yatay ve dikey sigma ayrı)."""
    out = img
    for axis, sigma in ((1, sx), (0, sy)):
        if sigma <= 0:
            continue
        k = _gauss1d(sigma)
        p = len(k) // 2
        out = np.apply_along_axis(
            lambda line: np.convolve(np.pad(line, p, mode="edge"), k, mode="valid"),
            axis,
            out,
        )
    return out


def refine_alpha(alpha: np.ndarray) -> np.ndarray:
    """
    Kaba kesim maskesini temiz, pürüzsüz bir mata çevirir.

    Kaynak grafiğin alfası elle yapılmış bir seçim: kenarda ±3 piksellik
    tırtık ve basamaklar var, ekranda "pikselli" görünüyor. Dalga yatay
    aktığı için bu gürültü DİKEY yöndedir. Alfayı akış yönünde geniş
    (sigma 8), dikeyde dar (sigma 1.4) bir çekirdekle yumuşatıp ardından
    smoothstep ile kenar keskinliğini geri getiriyoruz: eğrinin gidişi
    korunur, tırtık kaybolur, geçiş düzgün yumuşatılmış olur.
    """
    a = alpha.astype(np.float32) / 255.0
    b = _sep_blur(a, sx=8.0, sy=1.4)
    t = np.clip((b - 0.5) / 0.30 + 0.5, 0.0, 1.0)
    return (t * t * (3 - 2 * t) * 255.0).astype(np.float32)


def unmatte_white(img: Image.Image, refined: np.ndarray) -> Image.Image:
    """
    Kenar yumuşatma piksellerindeki BEYAZ zemin kalıntısını temizler.

    Kaynak grafik beyaz zemin üzerinde kesilmiş: yarı saydam pikseller
    `gözlenen = gerçek·α + 255·(1−α)` biçiminde beyazla karışmış durumda
    (ölçüm: α<60 piksellerin ortalaması RGB 246,247,248). Koyu fotoğrafın
    üstüne konduğunda bu, dalganın çevresinde beyaz bir hale bırakıyor.
    Denklemi tersine çevirip gerçek rengi geri alıyoruz — şekil ve alfa
    hiç değişmez, yalnızca kenarın rengi düzelir.
    """
    a = np.asarray(img).astype(np.float32)
    rgb, alpha = a[:, :, :3], a[:, :, 3:4]
    k = np.clip(alpha / 255.0, 1e-3, 1.0)
    fixed = np.clip((rgb - 255.0 * (1.0 - k)) / k, 0, 255)

    # Düşük alfada bölme gürültüyü büyütüyor (koyu saçak). Rengi alfa
    # ağırlıklı bulanıklaştırıp güvenilir komşulardan dolduruyoruz:
    # premultiply → bulanıklaştır → böl. Alfa hiç değişmez.
    def blur(ch: np.ndarray, r: float) -> np.ndarray:
        return np.asarray(
            Image.fromarray(np.clip(ch, 0, 255).astype(np.uint8), "L").filter(
                ImageFilter.GaussianBlur(r)
            )
        ).astype(np.float32)

    aw = blur(alpha[:, :, 0], 2.0)
    pm = np.dstack([blur(fixed[:, :, c] * k[:, :, 0], 2.0) for c in range(3)])
    bled = np.clip(pm * 255.0 / np.maximum(aw, 1.0)[:, :, None], 0, 255)

    # Alfa yükseldikçe kendi rengine, düştükçe komşularınkine yaklaş
    t = np.clip((k - 0.18) / 0.42, 0.0, 1.0)
    out_rgb = fixed * t + bled * (1.0 - t)

    # Çıktı alfası, temizlenmiş mat
    ra = refined[:, :, None]
    out_rgb = np.where(ra > 0, out_rgb, 0)
    return Image.fromarray(np.dstack([out_rgb, ra]).astype(np.uint8), "RGBA")


def main() -> None:
    src = Image.open(SRC).convert("RGBA")
    src = src.crop(src.getbbox())
    w, h = src.size
    print(f"kaynak {w}x{h}")

    # ---------- 1) Matı temizle, şeridi yayınla ----------
    refined = refine_alpha(np.asarray(src)[:, :, 3])
    clean = unmatte_white(src, refined)
    clean.save(OUT / "wave.png", optimize=True)
    clean.save(OUT / "wave.webp", quality=95, method=6)
    print(f"wave.png / wave.webp → {w}x{h} (mat temizlendi, beyaz hale giderildi)")

    # Maskeler de temizlenmiş mattan türetilir
    solid = refined > (ALPHA_MIN * 2)

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

    # ---------- 2b) Taban maskesi ----------
    # Yalnızca dalganın ALT siluetinin altı. Bölüm geçişlerinde sayfa zemini
    # buradan başlar; dalga kurdeleleri fotoğrafın üstüne biner ve
    # aralarından gerçekten fotoğraf görünür — şeffaf PNG gibi.
    to_mask_png(below * 255).save(OUT / "wave-mask-base.png", optimize=True)
    print("wave-mask-base.png")

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
 * Yalnızca dalganın ALT siluetinin altı. Bölüm geçişlerinde sayfa zemini
 * buradan başlar; kurdeleler fotoğrafın üstüne biner ve araları gerçekten
 * saydam kalır.
 */
export const WAVE_MASK_BASE = "/brand/wave-mask-base.png";

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
