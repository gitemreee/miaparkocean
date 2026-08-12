#!/usr/bin/env python3
"""
MİA PARK OCEAN — logodaki dalgayı birebir çıkarır.

Sitenin imzası logonun altındaki dalgadır. Bu betik o dalgayı
`public/brand/mark-ocean-trim.png` içinden HİÇ DEĞİŞTİRMEDEN keser:

  public/brand/wave.png / .webp   → dalga şeridi (şeffaf, orijinal pikseller)
  public/brand/wave-mask.png      → aynı şeklin dolgulu maskesi (CSS mask-image)
  public/brand/wave-mask-solid.png → aynı şeklin boşluksuz silueti
  src/components/ui/wave-path.ts  → varlık yolları

Silueti bulma kuralı: her sütunda y >= 460'tan sonra BAŞLAYAN ilk opak koşu
dalganın üst kenarıdır (daha yukarıda başlayan uzun koşular M harfinin ve
kulelerin gövdesidir). Bu ham siluet yalnızca piksel titremesini almak için
küçük bir medyan penceresinden geçirilir; eğrinin karakteri korunur.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "public" / "brand" / "mark-ocean-trim.png"
OUT = ROOT / "public" / "brand"
TS_OUT = ROOT / "src" / "components" / "ui" / "wave-path.ts"

ALPHA_MIN = 24
WAVE_FROM = 460  # bu satırın altında başlayan koşular dalgaya aittir


def column_runs(alpha: np.ndarray, x: int) -> list[tuple[int, int]]:
    col = alpha[:, x] > ALPHA_MIN
    runs: list[tuple[int, int]] = []
    start = None
    for y, on in enumerate(col):
        if on and start is None:
            start = y
        elif not on and start is not None:
            runs.append((start, y - 1))
            start = None
    if start is not None:
        runs.append((start, len(col) - 1))
    return runs


def trace_top_edge(alpha: np.ndarray) -> np.ndarray:
    """Her sütun için dalganın üst kenarı (yok ise NaN)."""
    h, w = alpha.shape
    top = np.full(w, np.nan)
    for x in range(w):
        for a, _b in column_runs(alpha, x):
            if a >= WAVE_FROM:
                top[x] = a
                break
    # Kenarlardaki boşlukları en yakın geçerli değerle doldur
    idx = np.where(~np.isnan(top))[0]
    if len(idx):
        top[: idx[0]] = top[idx[0]]
        top[idx[-1] + 1 :] = top[idx[-1]]
    # Aradaki tekil boşluklar
    for x in range(w):
        if np.isnan(top[x]):
            left = x - 1
            right = x + 1
            while right < w and np.isnan(top[right]):
                right += 1
            if right < w and left >= 0:
                t = (x - left) / (right - left)
                top[x] = top[left] * (1 - t) + top[right] * t
    return top


def median_smooth(y: np.ndarray, k: int) -> np.ndarray:
    pad = k // 2
    padded = np.pad(y, pad, mode="edge")
    return np.array([np.median(padded[i : i + k]) for i in range(len(y))])


def mean_smooth(y: np.ndarray, k: int) -> np.ndarray:
    pad = k // 2
    padded = np.pad(y, pad, mode="edge")
    kern = np.ones(k) / k
    return np.convolve(padded, kern, mode="valid")


def main() -> None:
    im = Image.open(SRC).convert("RGBA")
    arr = np.asarray(im)
    alpha = arr[:, :, 3]
    h, w = alpha.shape

    raw = trace_top_edge(alpha)
    # Kesim maskesi ham silueti kullanır (tek piksel bile kırpılmasın).
    cut_edge = median_smooth(raw, 3)
    y_top = float(cut_edge.min())
    print(f"kaynak {w}x{h} · dalga üst kenarı {y_top:.0f}–{cut_edge.max():.0f}")

    # ---------- 1) Dalga şeridini kes ----------
    yy = np.arange(h)[:, None]
    mask = yy >= cut_edge[None, :].round()
    cut = arr.copy()
    cut[:, :, 3] = np.where(mask, alpha, 0)

    band = cut[int(y_top) :, :, :]
    wave = Image.fromarray(band, "RGBA")
    # Sağ/sol uçlarda tamamen boş sütunları kırp
    bbox = wave.getbbox()
    wave = wave.crop(bbox)
    wave.save(OUT / "wave.png")
    wave.save(OUT / "wave.webp", quality=94, method=6)
    print(f"wave.png → {wave.size}")

    # ---------- 2) Dolgulu maske ----------
    # Dalganın kendi alfası + alt siluetinin altındaki her şey opak.
    # CSS `mask-image` ile kullanıldığında üst kenarı birebir logodaki dalga
    # olan dolu bir panel verir (bölüm geçişleri, koyu bantlar, sayfa geçişi).
    wa = np.asarray(wave)[:, :, 3].astype(np.uint8)
    bh, bw = wa.shape

    # Boya dokusundan gelen tırtıklı kenarı temizle: eşikle → bulanıklaştır →
    # tekrar eşikle. Silüet aynı kalır, kenar pürüzü gider.
    clean = ((wa > 30) * 255).astype(np.uint8)
    clean = np.asarray(
        Image.fromarray(clean, "L").filter(ImageFilter.GaussianBlur(1.0))
    )
    wa = ((clean > 96) * 255).astype(np.uint8)
    # Tek piksellik saçakları at (açma), sonra kenarı geri getir
    wa = np.asarray(
        Image.fromarray(wa, "L")
        .filter(ImageFilter.MinFilter(3))
        .filter(ImageFilter.MaxFilter(3))
    )

    # Şeridin içindeki KÜÇÜK saydam lekeleri kapat; iki kurdele arasındaki
    # geniş boşluk (dalganın karakteri) olduğu gibi kalsın.
    solid = wa.copy()
    for x in range(bw):
        col = solid[:, x] > 8
        ys = np.where(col)[0]
        if len(ys) == 0:
            continue
        y = ys.min()
        while y <= ys.max():
            if not col[y]:
                e = y
                while e <= ys.max() and not col[e]:
                    e += 1
                if e - y <= 2:
                    solid[y:e, x] = 255
                y = e
            else:
                y += 1

    bottom = np.full(bw, bh, dtype=float)
    for x in range(bw):
        ys = np.where(solid[:, x] > 8)[0]
        if len(ys):
            bottom[x] = ys.max()
    bottom = mean_smooth(median_smooth(bottom, 25), 21)
    below = (np.arange(bh)[:, None] >= bottom[None, :]).astype(np.uint8) * 255
    filled = np.maximum(solid, below)

    # Dalga yatay akar; kenardaki titreme dikey yöndedir. Yalnızca YATAYDA
    # yumuşatıp yeniden eşikleyerek tırtığı alıyoruz — eğrinin kendisi
    # (yükselişi, alçalışı, iki kurdele arası boşluk) aynen kalıyor.
    k = 17
    kern = np.ones(k) / k
    smoothed = np.stack(
        [np.convolve(np.pad(row, k // 2, mode="edge"), kern, mode="valid") for row in filled.astype(np.float32)]
    )
    filled = ((smoothed > 118) * 255).astype(np.uint8)

    # Maske sitede 1440px+ genişliğe esnetiliyor. 3× büyütüp yumuşatarak
    # kaydediyoruz; böylece kenar tırtıklı değil, temiz ve yumuşak görünür.
    mask_img = Image.fromarray(filled, "L").resize(
        (bw * 3, bh * 3), Image.LANCZOS
    )
    mask_img = mask_img.filter(ImageFilter.GaussianBlur(2.6))
    ma = np.asarray(mask_img)
    fill_img = Image.fromarray(
        np.dstack([np.full_like(ma, 255)] * 3 + [ma]), "RGBA"
    )
    fill_img.save(OUT / "wave-mask.png", optimize=True)
    print(f"wave-mask.png → {fill_img.size}")

    # ---------- 2b) Boşluksuz siluet ----------
    # Aynı dalganın üst kenarından aşağısı tamamen dolu hâli. Koyu fotoğraf
    # üstünde kurdele araları fotoğrafı göstermesin diye altta bu durur;
    # üst kenar birebir aynı eğridir.
    top_edge = np.full(bw, bh, dtype=float)
    for x in range(bw):
        ys = np.where(filled[:, x] > 8)[0]
        if len(ys):
            top_edge[x] = ys.min()
    top_edge = mean_smooth(median_smooth(top_edge, 9), 9)
    solid_alpha = (np.arange(bh)[:, None] >= top_edge[None, :]).astype(np.uint8) * 255
    solid_img = Image.fromarray(solid_alpha, "L").resize((bw * 3, bh * 3), Image.LANCZOS)
    solid_img = solid_img.filter(ImageFilter.GaussianBlur(2.6))
    sa3 = np.asarray(solid_img)
    Image.fromarray(np.dstack([np.full_like(sa3, 255)] * 3 + [sa3]), "RGBA").save(
        OUT / "wave-mask-solid.png", optimize=True
    )
    print("wave-mask-solid.png")

    # ---------- 3) TypeScript sabitleri ----------
    ts = f"""/**
 * Logodaki dalga — `scripts/build-wave.py` tarafından
 * `public/brand/mark-ocean-trim.png` içinden birebir kesildi.
 *
 * ELLE DÜZENLEMEYİN. Değişiklik gerekiyorsa betiği yeniden çalıştırın.
 * Sitedeki her dalga bu iki varlıktan birini kullanır; başka hiçbir yerde
 * elle çizilmiş dalga eğrisi yoktur.
 */

/** Dalga şeridi — logodaki orijinal pikseller, şeffaf zemin. */
export const WAVE_IMAGE = "/brand/wave.webp";

/**
 * Aynı dalganın dolgulu maskesi: şeridin kendisi + altındaki her şey opak.
 * `mask-image` olarak kullanıldığında üst kenarı birebir logodaki dalga olan
 * dolu bir panel verir.
 */
export const WAVE_MASK = "/brand/wave-mask.png";

/**
 * Aynı dalganın boşluksuz silueti — üst kenar birebir aynı, iç ayrımlar dolu.
 * Koyu fotoğraf üstünde alt katman olarak kullanılır.
 */
export const WAVE_MASK_SOLID = "/brand/wave-mask-solid.png";

/** Şeridin en/boy oranı. */
export const WAVE_RATIO = {wave.width / wave.height:.4f};
"""
    TS_OUT.write_text(ts, encoding="utf-8")
    print("wave-path.ts")


if __name__ == "__main__":
    main()
