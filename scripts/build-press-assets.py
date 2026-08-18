#!/usr/bin/env python3
"""
MİA PARK OCEAN — basın varlıkları (haber görselleri + yayın logoları).

Girdi : press-source/   (haber sayfalarından indirilen ham dosyalar)
Çıktı : public/images/basin/
            haber-<yayin>.webp      1200x675  kart görseli
            haber-<yayin>-sm.webp    600x338  küçük ekran
            logo-<yayin>.png         600 px genişlik, şeffaf, kırpılmış

NEDEN AYRI BİR ADIM
───────────────────
Haber görselleri gazetelerin sunucusunda duruyor; doğrudan bağlamak
(hotlink) hem yavaş hem de dosya adresi değişince kart boşalır. Bir kez
indirip kendi sunucumuzda WebP olarak tutuyoruz.

LOGO KONTRASTI
──────────────
Altı yayının logosu altı farklı zemine göre çizilmiş:

    İlke Kocaeli     siyah yazı + kırmızı nokta   → açık zeminde okunur
    Kocaeli Fikir    siyah + kırmızı kutu         → açık zeminde okunur
    Kocaeli Gazetesi opak kırmızı kutu            → her zeminde okunur
    Kocaeli Koz      kırmızı                      → her zeminde okunur
    Özgün Kocaeli    opak, beyaz bantlı           → açık zeminde okunur
    Kocaeli Gündem   BEYAZ, şeffaf                → yalnızca koyu zeminde

Bu yüzden logolar hiçbir yerde çıplak koyu zemine konmuyor: hem sitede
hem Instagram panelinde BEYAZ PLAKET içinde duruyorlar. Böylece altısı da
kendi renkleriyle, olması gerektiği gibi görünüyor — başkasının logosunu
yeniden renklendirmiyoruz.

Tek istisna Kocaeli Gündem: logosu tek renk (beyaz) olduğu için açık
zeminde görünmüyor; tek renkli bir markanın rengini çevirmek meşru
kullanımdır, koyu lacivert sürümü üretiliyor.

Kullanım:
    python scripts/build-press-assets.py
"""

from __future__ import annotations

import os

import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "press-source")
OUT = os.path.join(ROOT, "public", "images", "basin")

INK = (10, 42, 61)

# slug, ham logo dosyası, ham haber görseli, tek renk beyaz mı (çevrilecek mi)
OUTLETS = [
    ("kocaeligazetesi", "logo-kocaeligazetesi.png", "haber-kocaeligazetesi.webp", False),
    ("ozgunkocaeli", "logo-ozgunkocaeli.png", "haber-ozgunkocaeli.jpg", False),
    ("ilkekocaeli", "logo-ilkekocaeli.webp", "haber-ilkekocaeli.jpg", False),
    ("kocaeligundem", "logo-kocaeligundem.png", "haber-kocaeligundem.webp", True),
    ("kocaelifikir", "logo-kocaelifikir.png", "haber-kocaelifikir.jpg", False),
    ("kocaelikoz", "logo-kocaelikoz.png", "haber-kocaelikoz.jpg", False),
]

CARD_W, CARD_H = 1200, 675          # 16:9
LOGO_W = 600


def trim(im: Image.Image) -> Image.Image:
    """Şeffaf ya da düz beyaz kenar boşluğunu kırpar.

    Logolar farklı boşluklarla geliyor; kırpmadan yan yana dizilince
    biri havada, biri yapışık duruyor.
    """
    if im.mode != "RGBA":
        im = im.convert("RGBA")
    box = im.split()[3].getbbox()
    if box:
        im = im.crop(box)
    # opak logolarda beyaz çerçeveyi de at
    a = np.array(im)
    if a[:, :, 3].min() > 250:
        lum = a[:, :, :3].mean(axis=2)
        mask = lum < 246
        if mask.any():
            ys, xs = np.where(mask)
            im = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    return im


def to_dark(im: Image.Image) -> Image.Image:
    """Tek renk beyaz logoyu koyu sürüme çevirir (alfa korunur)."""
    a = np.array(im.convert("RGBA"))
    a[:, :, 0], a[:, :, 1], a[:, :, 2] = INK
    return Image.fromarray(a, "RGBA")


def cover(im: Image.Image, w: int, h: int) -> Image.Image:
    im = im.convert("RGB")
    s = max(w / im.width, h / im.height)
    im = im.resize((max(w, round(im.width * s)), max(h, round(im.height * s))), Image.LANCZOS)
    x = (im.width - w) // 2
    y = (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    for slug, logo_file, shot_file, mono_white in OUTLETS:
        # -- logo --
        lg = trim(Image.open(os.path.join(SRC, logo_file)))
        if mono_white:
            lg = to_dark(lg)
        lg = lg.resize((LOGO_W, max(1, round(lg.height * LOGO_W / lg.width))), Image.LANCZOS)
        lp = os.path.join(OUT, f"logo-{slug}.png")
        lg.save(lp, optimize=True)

        # -- haber görseli --
        shot = Image.open(os.path.join(SRC, shot_file))
        big = cover(shot, CARD_W, CARD_H)
        big.save(os.path.join(OUT, f"haber-{slug}.webp"), "WEBP", quality=82, method=6)
        small = big.resize((CARD_W // 2, CARD_H // 2), Image.LANCZOS)
        small.save(os.path.join(OUT, f"haber-{slug}-sm.webp"), "WEBP", quality=78, method=6)

        kb = os.path.getsize(lp) / 1024
        print(f"  {slug:<18} logo {lg.size[0]}x{lg.size[1]} ({kb:.0f} KB)  ·  haber {CARD_W}x{CARD_H}")
    print(f"\n  → {OUT}")


if __name__ == "__main__":
    main()
