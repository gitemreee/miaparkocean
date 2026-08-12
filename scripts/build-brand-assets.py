#!/usr/bin/env python3
"""MİA PARK OCEAN marka varlığı üreticisi.

Kaynak logo `brand-source/logo-ocean-source.jpg` dosyasındadır. Logo hiçbir
şekilde yeniden renklendirilmez: orijinal turkuaz hâliyle, **beyaz zemin**
üzerinde kullanılır. Script yalnızca kırpma, temizleme ve ölçekleme yapar.

Üretilenler:
    public/brand/logo-ocean.(png|webp)      tam kilit (işaret + kelime markası), beyaz zemin
    public/brand/logo-ocean-trim.(png|webp) aynı logo, şeffaf zemin (beyaz yüzeylere yerleşim için)
    public/brand/mark-ocean.(png|webp)      yalnız işaret, beyaz zemin
    public/brand/mark-ocean-trim.(png|webp) yalnız işaret, şeffaf zemin
    public/icon-512 / icon-192 / apple-touch-icon   beyaz zeminli favicon
    src/app/icon.png + favicon.ico
    public/og-image.jpg                     beyaz kart + okyanus gradyan çerçeve

Kullanım:
    pip install pillow numpy
    python scripts/build-brand-assets.py
"""

from __future__ import annotations

import os
from collections import deque

import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "brand-source")
OUT = os.path.join(ROOT, "public", "brand")
APP = os.path.join(ROOT, "src", "app")

# Site gradyanı (globals.css --gradient-ocean ile aynı) — yalnız çerçeve/zemin için
NAVY = (0, 9, 38)          # #000926 Deep Navy
MIDNIGHT = (6, 26, 74)     # #061A4A
SAPPHIRE = (15, 82, 186)   # #0F52BA
LOGO_BLUE = (12, 108, 144)  # #0C6C90  logonun kendi mavisi
LOGO_MID = (24, 120, 156)   # #18789C
BRAND_STOPS = [
    (0.0, NAVY),
    (0.24, MIDNIGHT),
    (0.52, SAPPHIRE),
    (0.78, LOGO_BLUE),
    (1.0, LOGO_MID),
]


# --------------------------------------------------------------------------
# Kaynak logoyu temizle: gri zemini beyaza çevir, şeffaf sürümü de üret
# --------------------------------------------------------------------------
def load_logo() -> tuple[Image.Image, Image.Image]:
    """(beyaz zeminli, şeffaf zeminli) logo çiftini döndürür."""
    im = Image.open(os.path.join(SRC, "logo-ocean-source.jpg")).convert("RGB")
    a = np.asarray(im).astype(np.int16)
    h, w, _ = a.shape
    dist = np.abs(a - np.array([240, 240, 240])).max(axis=2)
    seed = dist < 16

    # Köşelerden flood fill — logonun içindeki beyazlar korunur
    visited = np.zeros((h, w), bool)
    dq: deque = deque()
    for y, x in [(0, 0), (0, w - 1), (h - 1, 0), (h - 1, w - 1)]:
        visited[y, x] = True
        dq.append((y, x))
    while dq:
        y, x = dq.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx] and seed[ny, nx]:
                visited[ny, nx] = True
                dq.append((ny, nx))

    soft = np.clip((dist - 11) / 13.0, 0, 1)
    alpha = np.where(visited, (soft * 255).astype(np.uint8), np.uint8(255))

    # Kenar yumuşatma pikselleri kaynaktaki gri zeminin rengini taşıyor
    # (~#DEE7EB). Beyaz plakete bindirildiğinde bu, logonun etrafında gri bir
    # hale bırakıyordu. Kısmi saydam pikselleri saydamlıkları oranında beyaza
    # çekiyoruz: hale beyazlaşır, logonun kendi rengi bozulmaz.
    rgb = np.asarray(im).astype(np.float32)
    a01 = (alpha.astype(np.float32) / 255.0)[:, :, None]
    rgb = rgb * a01 + 255.0 * (1 - a01)

    transparent = Image.fromarray(
        np.dstack([rgb.astype(np.uint8), alpha.astype(np.uint8)]), "RGBA"
    )
    transparent = transparent.crop(transparent.getbbox())

    white = Image.new("RGBA", transparent.size, (255, 255, 255, 255))
    white.alpha_composite(transparent)
    return white, transparent


def find_gaps(img: Image.Image, min_gap: int = 8) -> list[tuple[int, int]]:
    A = np.asarray(img)[:, :, 3]
    rows = (A > 30).sum(axis=1)
    gaps, start, inrun = [], 0, False
    for i, v in enumerate(rows):
        if v < 3 and not inrun:
            start, inrun = i, True
        elif v >= 3 and inrun:
            if i - start > min_gap:
                gaps.append((start, i))
            inrun = False
    return gaps


def fit(img: Image.Image, width: int) -> Image.Image:
    ratio = width / img.width
    return img.resize((width, max(1, round(img.height * ratio))), Image.LANCZOS)


def save(img: Image.Image, name: str) -> None:
    img.save(os.path.join(OUT, f"{name}.png"), optimize=True)
    img.save(os.path.join(OUT, f"{name}.webp"), quality=94, method=6)
    print(f"  {name}: {img.size[0]}x{img.size[1]}")


def pad_square(img: Image.Image, size: int, pad: float, bg=(255, 255, 255, 255)) -> Image.Image:
    inner = round(size * (1 - pad * 2))
    scale = min(inner / img.width, inner / img.height)
    r = img.resize((max(1, round(img.width * scale)), max(1, round(img.height * scale))), Image.LANCZOS)
    canvas = Image.new("RGBA", (size, size), bg)
    canvas.alpha_composite(r, ((size - r.width) // 2, (size - r.height) // 2))
    return canvas


def gradient(size: tuple[int, int], stops=BRAND_STOPS, angle: float = 0.62) -> Image.Image:
    w, h = size
    yy, xx = np.mgrid[0:h, 0:w]
    t = np.clip((xx / max(w - 1, 1)) * angle + (yy / max(h - 1, 1)) * (1 - angle), 0, 1)
    arr = np.zeros((h, w, 3), np.float32)
    for i in range(len(stops) - 1):
        t0, c0 = stops[i]
        t1, c1 = stops[i + 1]
        m = (t >= t0) & (t <= t1)
        k = np.clip((t - t0) / max(t1 - t0, 1e-6), 0, 1)
        for c in range(3):
            arr[:, :, c] = np.where(m, c0[c] + (c1[c] - c0[c]) * k, arr[:, :, c])
    return Image.fromarray(arr.astype(np.uint8), "RGB").convert("RGBA")


def rounded(img: Image.Image, radius: int) -> Image.Image:
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, img.width - 1, img.height - 1], radius=radius, fill=255)
    out = img.copy()
    out.putalpha(mask)
    return out


def whiteout(img: Image.Image) -> Image.Image:
    """
    Koyu mavi zemin için ters (beyaz) sürüm.

    Şekil hiç değişmez, boya DÜZ BEYAZ olur. Tonlamayı alfaya taşımak
    (metalik his vermek) koyu zeminde logoyu grileştiriyordu; ters logo
    tek renk olmalı. Silüetin kendi boşlukları zaten M'yi, kuleleri ve
    kelime markasını okunur tutuyor.
    """
    a = np.asarray(img.convert("RGBA")).astype(np.float32)
    alpha = a[:, :, 3]
    out = np.zeros_like(a)
    out[:, :, 0:3] = 255.0
    out[:, :, 3] = alpha
    return Image.fromarray(out.astype(np.uint8), "RGBA")


def open_counters(img: Image.Image, from_y: int) -> Image.Image:
    """
    Kelime markasındaki KAPALI harf gözlerini açar (O, A, P, R, B, Ö).

    Zemin, köşelerden flood fill ile siliniyor; harflerin içinde kalan kapalı
    boşluklara ulaşılamadığı için onlar opak kalıyordu. Beyaz zeminde fark
    edilmiyordu (göz de beyazdı) ama koyu zeminli ters sürümde harfler dolu
    görünüyor.

    Göz pikselleri kaynağın zemin rengini taşır: neredeyse beyaz VE nötr
    (kanallar arası fark yok). Harflerin turkuaz mürekkebi ve kenar
    yumuşatması nötr olmadığı için etkilenmez. Sert kesme yerine beyazlığa
    göre yumuşak azaltma yapılır; göz kenarları pürüzsüz kalır.
    """
    a = np.asarray(img.convert("RGBA")).astype(np.float32)
    rgb, alpha = a[:, :, :3], a[:, :, 3]
    lum = (0.2126 * rgb[:, :, 0] + 0.7152 * rgb[:, :, 1] + 0.0722 * rgb[:, :, 2]) / 255.0
    neutral = (rgb.max(axis=2) - rgb.min(axis=2)) < 14

    hole = np.clip((lum - 0.84) / 0.12, 0.0, 1.0) * neutral
    hole[:from_y, :] = 0.0  # işaret bölgesine dokunma

    out = a.copy()
    out[:, :, 3] = alpha * (1.0 - hole)
    return Image.fromarray(out.astype(np.uint8), "RGBA")


def keyed_white(img: Image.Image) -> Image.Image:
    """Beyaz zeminli düz renkli logoyu koyu zemin için beyaza çevirir."""
    a = np.asarray(img.convert("RGBA")).astype(np.float32)
    rgb, alpha = a[:, :, :3], a[:, :, 3]
    lum = (0.2126 * rgb[:, :, 0] + 0.7152 * rgb[:, :, 1] + 0.0722 * rgb[:, :, 2]) / 255.0
    ink = np.clip((0.92 - lum) / 0.72, 0.0, 1.0)
    out = np.zeros_like(a)
    out[:, :, 0:3] = 255.0
    out[:, :, 3] = np.minimum(alpha, ink * 255.0)
    return Image.fromarray(out.astype(np.uint8), "RGBA")


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    print("Logo hazırlanıyor (renk değiştirilmiyor)…")
    white, trans = load_logo()

    gaps = find_gaps(trans)
    mark_end = gaps[0][0] + 6 if gaps else int(trans.height * 0.7)

    # Kelime markasındaki kapalı harf gözlerini aç (beyaz zeminde görünüm
    # değişmez; koyu zeminli ters sürümde harfler dolu görünmez).
    trans = open_counters(trans, mark_end)
    white = Image.new("RGBA", trans.size, (255, 255, 255, 255))
    white.alpha_composite(trans)

    mark_trans = trans.crop((0, 0, trans.width, mark_end))
    mark_trans = mark_trans.crop(mark_trans.getbbox())
    mark_white = Image.new("RGBA", mark_trans.size, (255, 255, 255, 255))
    mark_white.alpha_composite(mark_trans)

    save(fit(white, 1200), "logo-ocean")
    save(fit(trans, 1200), "logo-ocean-trim")
    save(fit(mark_white, 640), "mark-ocean")
    save(fit(mark_trans, 640), "mark-ocean-trim")

    print("Ters (beyaz) sürüm — koyu mavi zemin için…")
    save(fit(whiteout(trans), 1200), "logo-ocean-white")
    save(fit(whiteout(mark_trans), 640), "mark-ocean-white")

    # Satıcı logosu da koyu zeminde beyaz durur (YKB ile aynı davranış)
    seller = Image.open(os.path.join(ROOT, "public", "ocean-logo.webp")).convert("RGBA")
    sw = keyed_white(seller)
    sw.save(os.path.join(ROOT, "public", "ocean-logo-white.png"), optimize=True)
    sw.save(os.path.join(ROOT, "public", "ocean-logo-white.webp"), quality=95, method=6)
    print(f"  ocean-logo-white: {sw.width}x{sw.height}")

    print("Favicon / uygulama ikonları (beyaz zemin)…")
    for size, name in [(512, "icon-512"), (192, "icon-192"), (180, "apple-touch-icon")]:
        plate = pad_square(mark_trans, size, pad=0.10)
        plate = rounded(plate, round(size * 0.2))
        plate.save(os.path.join(ROOT, "public", f"{name}.png"), optimize=True)
        print(f"  {name}.png: {size}x{size}")

    ico = Image.open(os.path.join(ROOT, "public", "icon-512.png"))
    ico.resize((256, 256), Image.LANCZOS).save(os.path.join(APP, "icon.png"), optimize=True)
    ico.resize((48, 48), Image.LANCZOS).save(
        os.path.join(APP, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)]
    )
    print("  src/app/icon.png + favicon.ico")

    print("OG görseli (beyaz kart + okyanus çerçeve)…")
    og = gradient((1200, 630))
    card = Image.new("RGBA", (1084, 514), (255, 255, 255, 255))
    card = rounded(card, 34)
    lock = fit(trans, 620)
    card.alpha_composite(lock, ((card.width - lock.width) // 2, (card.height - lock.height) // 2))
    og.alpha_composite(card, ((1200 - card.width) // 2, (630 - card.height) // 2))
    og.convert("RGB").save(os.path.join(ROOT, "public", "og-image.jpg"), quality=90, optimize=True)
    print("  public/og-image.jpg: 1200x630")


if __name__ == "__main__":
    main()
