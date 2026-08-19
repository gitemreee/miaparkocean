#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MİA PARK OCEAN — bilbord ve arsa panosu serisi (8 tasarım, 2 set).

Aynı sekiz tasarım iki ayrı sette çıkıyor. Görsel aynı; şehrin farklı
yerlerinde durdukları için üst ve alt bantları farklı:

    tabela/bilbord-mia/   5000 x 3000 mm, 40 dpi   — şehir içi bilbord
        üst bantta  İZMİT MİA BÖLGESİ   (nerede olduğunu bilmeyene)
        alt bantta  iri telefonlar      (araçtan okunur, karekod yok)

    tabela/arsa-mia/      3000 x 2000 mm, 50 dpi   — arsa çevresi
        üst bantta  PROJE ALANI         (arsanın kime ait olduğu)
        alt bantta  karekod + Instagram (yayadan okunur)

DALGA YOK. Bantlar iki ince çizgiyle ayrılıyor: kalın bir kural, ince bir
kural. Bant rengi her tasarımın KENDİ üretiminden ölçülüyor — set tek tip
mavi değil; lacivert, antrasit, bronz ve orman yeşili panolar var.

Kaynak: Higgsfield (nano_banana_pro, 3:2, 4K). İstemler PROMPT.md'de, ham
PNG'ler signage-source/hf-mia/ altında (git'e girmiyor). Üretime logo
çizdirilmiyor; iki bant boş bırakılıp gerçek MİA PARK OCEAN kilidi ve
OCEAN GAYRİMENKUL imzası buradan basılıyor.

    python scripts/build-mia-panolar.py
"""
from __future__ import annotations

import importlib.util
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_spec = importlib.util.spec_from_file_location(
    "bs", os.path.join(ROOT, "scripts", "build-signage.py"))
bs = importlib.util.module_from_spec(_spec)
sys.modules["bs"] = bs
_spec.loader.exec_module(bs)

Board, lockup, track, fit_track, qr_image = (bs.Board, bs.lockup, bs.track,
                                            bs.fit_track, bs.qr_image)
WHITE, INK, BRAND = bs.WHITE, bs.INK, bs.BRAND
SITE, PHONES = bs.SITE, bs.PHONES
SELLER, SELLER_ROLE = bs.SELLER, bs.SELLER_ROLE

IG = "@miaparkocean"
BOLGE = "İZMİT MİA BÖLGESİ"
ALAN = "PROJE ALANI"
DISCLAIM = "GÖRSELLER TEMSİLİDİR"

SRC = os.path.join(ROOT, "signage-source", "hf-mia")

DESIGNS = [
    ("mia-1-sosyal-yuvarlak", "Üç yuvarlak fotoğraf — sosyal yaşam"),
    ("mia-2-sifir-faiz",      "%0 faiz · 60 ay vade · kredi/faiz/kefil yok"),
    ("mia-3-dusuk-pesinat",   "Düşük peşinatla ev sahibi olun"),
    ("mia-4-burada-eviniz",   "Burada eviniz olsun istemez miydiniz?"),
    ("mia-5-satis-ofisi",     "Satış ofisi — kahvenizi içmeye bekleriz"),
    ("mia-6-ic-mekan",        "İç mekân — evinizi şimdiden görün"),
    ("mia-7-dis-mekan",       "Dış mekân — dışarısı da evinizin bir parçası"),
    ("mia-8-daire-tipleri",   "Daire tipleri — 1+0 / 1+1 / 2+1"),
]

# (klasör, mm genişlik, mm yükseklik, dpi, bant mm, üst sağ yazı, karekod)
SETS = {
    "bilbord": (os.path.join(ROOT, "tabela", "bilbord-mia"),
                5000, 3000, 40, 300, BOLGE, False),
    "arsa":    (os.path.join(ROOT, "tabela", "arsa-mia"),
                3000, 2000, 50, 260, ALAN, True),
}

QR_URL = "https://miaparkocean.com/?utm_source=arsa"


def cap_top(f, cy: float) -> float:
    t, b = f.getbbox("H")[1], f.getbbox("H")[3]
    return cy - (t + b) / 2


def logo_h(b: Board, h_mm: float) -> Image.Image:
    """Kilidi yüksekliğe göre ölçekle."""
    src = Image.open(os.path.join(BRAND, "logo-ocean-white.png"))
    box = src.getbbox()
    ar = (box[2] - box[0]) / (box[3] - box[1])
    return lockup(round(b.p(h_mm) * ar), white=True)


def band_color(im: Image.Image) -> tuple:
    """Üretimin ayırdığı bandın rengi.

    Bant rengini sabitlemiyoruz: her tasarım kendi paletini getiriyor
    (lacivert, antrasit, bronz, orman yeşili) ve bant o rengin devamı
    oluyor. Ortadaki sütunlardan, üstteki %6'lık şeritten medyan alınıyor —
    kenarlarda gradyan olabilir, ortada bant düz.
    """
    a = np.asarray(im.convert("RGB"), np.float32)
    h, w, _ = a.shape
    strip = a[round(h * 0.02):round(h * 0.07), round(w * 0.35):round(w * 0.65)]
    return tuple(int(v) for v in np.median(strip, axis=(0, 1)))


def fit_to(im: Image.Image, W: int, H: int) -> Image.Image:
    """Kaynak 3:2. Bilbord 5:3 istediğinde YÜKSEKLİKTEN kırpılıyor — kırpma
    payı üretimde boş bırakılan bantların içine düşüyor, tasarımdan bir şey
    gitmiyor."""
    s = max(W / im.width, H / im.height)
    im = im.resize((max(W, round(im.width * s)), max(H, round(im.height * s))),
                   Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))


def qr_slot(b: Board) -> tuple | None:
    """Üretimin bıraktığı beyaz karekod yuvasını bul.

    Satış ofisi panosunda isteme "boş beyaz kare bırak" dendi; gerçek
    karekodu oraya biz basıyoruz.

    Yuvayı "beyaz piksellerin sınır kutusu" diye aramak işe yaramadı:
    panodaki BEYAZ YAZI da eşiği geçiyor, kutu manşetten yuvaya kadar
    uzayıp karekod tasarımın yarısını kaplıyordu. Doğru ölçüt TAMAMEN DOLU
    KARE: maske sekizde bire indirilip integral görüntüden, içi baştan sona
    beyaz olan en büyük kare aranıyor. Yazı ince olduğu için hiçbir zaman
    dolu bir kare oluşturmuyor.
    """
    a = np.asarray(b.im.convert("RGB"), np.int16)
    H, W, _ = a.shape
    m = ((a.min(axis=2) > 238) & (np.ptp(a, axis=2) < 12)).astype(np.float32)
    k = 8
    sm = m[:H // k * k, :W // k * k].reshape(H // k, k, W // k, k).mean(axis=(1, 3))
    sm = (sm > 0.9).astype(np.int32)
    h, w = sm.shape
    ii = np.zeros((h + 1, w + 1), np.int32)
    ii[1:, 1:] = sm.cumsum(0).cumsum(1)
    y0, x0 = int(h * 0.40), int(w * 0.55)      # yuva sağ altta
    for size in range(min(h - y0, w - x0), max(6, b.p(70) // k), -2):
        tot = (ii[y0 + size:, x0 + size:] - ii[y0:h - size + 1, x0 + size:]
               - ii[y0 + size:, x0:w - size + 1] + ii[y0:h - size + 1, x0:w - size + 1])
        hit = np.argwhere(tot >= size * size)
        if len(hit):
            yy, xx = hit[0]
            return ((x0 + xx) * k, (y0 + yy) * k,
                    (x0 + xx + size) * k, (y0 + yy + size) * k)
    return None


def bands(b: Board, col: tuple, band_mm: float, right_text: str,
          with_qr: bool) -> None:
    """Üst kimlik bandı + alt künye bandı. Dalga yok: bantlar iki ince
    çizgiyle ayrılıyor, kalın bir kural ve altında ince bir kural."""
    dr = b.draw
    bh = b.p(band_mm)
    dark = sum(col) / 3 < 150
    fg = WHITE if dark else INK
    sub = (255, 255, 255, 190) if dark else (*INK, 190)

    dr.rectangle([0, 0, b.W, bh], fill=col)
    dr.rectangle([0, b.H - bh, b.W, b.H], fill=col)

    # İki çizgi — bandı panodan ayıran tek şey bu.
    t1, gap, t2 = b.p(band_mm * 0.030), b.p(band_mm * 0.028), b.p(band_mm * 0.011)
    c1 = (255, 255, 255, 230) if dark else (*INK, 210)
    c2 = (255, 255, 255, 120) if dark else (*INK, 110)
    for y, d in ((bh, 1), (b.H - bh, -1)):
        # Alt bantta çizgiler YUKARI doğru gidiyor; PIL y1 < y0 kabul
        # etmediği için köşeler sıralanıyor.
        for off, t, c in ((0, t1, c1), (t1 + gap, t2, c2)):
            ya, yb = sorted((y + off * d, y + (off + t) * d))
            dr.rectangle([0, ya, b.W, yb], fill=c)

    pad = b.p(band_mm * 0.42)
    lg = logo_h(b, band_mm * 0.68)
    b.im.alpha_composite(lg, (pad, (bh - lg.height) // 2))

    f, sp = fit_track(b, dr, [right_text], b.W - lg.width - pad * 3,
                      band_mm * 0.26, 0.22, lambda s: b.sans(s, "700"))
    track(b, dr, (b.W - pad, cap_top(f, bh / 2)), right_text, f, fg, sp, "ra")

    # ---- alt bant
    cy = b.H - bh / 2
    x = pad
    if with_qr:
        q = round(bh * 0.62)
        plate = q + b.p(band_mm * 0.07)
        py = b.H - bh + (bh - plate) // 2
        dr.rounded_rectangle([x, py, x + plate, py + plate],
                             radius=b.p(band_mm * 0.035), fill=WHITE)
        b.im.alpha_composite(qr_image(QR_URL, q, col if dark else INK),
                             (x + (plate - q) // 2, py + (plate - q) // 2))
        x += plate + b.p(band_mm * 0.22)
        f1 = b.sans(band_mm * 0.185, "700")
        f2 = b.sans(band_mm * 0.145, "600")
        dr.text((x, cap_top(f1, cy - bh * 0.16)), f"{SITE}   ·   {IG}", font=f1, fill=fg)
        dr.text((x, cap_top(f2, cy + bh * 0.18)), "   ·   ".join(PHONES), font=f2,
                fill=sub)
    else:
        # Bilbord araçtan okunur: karekod yok, telefon iri.
        f1 = b.sans(band_mm * 0.30, "700")
        f2 = b.sans(band_mm * 0.165, "600")
        dr.text((x, cap_top(f1, cy - bh * 0.13)), "   ·   ".join(PHONES),
                font=f1, fill=fg)
        dr.text((x, cap_top(f2, cy + bh * 0.24)), f"{SITE}   ·   {IG}", font=f2,
                fill=sub)

    # Ortada küçük ve sabit: render'lar temsilî, panoda yazması gerekiyor.
    # İç mekân panosunda bu satır üretimin içinde de vardı ama alt bandın
    # altında kalıyordu; buraya alınca on altı panoda da aynı yerde duruyor.
    f0, sp0 = fit_track(b, dr, [DISCLAIM], b.p(1400), band_mm * 0.105, 0.24,
                        lambda s: b.sans(s, "600"))
    track(b, dr, (b.W // 2, cap_top(f0, cy + bh * 0.30)), DISCLAIM, f0, sub,
          sp0, "ma")

    fx = b.W - pad
    f3, sp3 = fit_track(b, dr, [SELLER], b.p(1600), band_mm * 0.165, 0.14,
                        lambda s: b.sans(s, "700"))
    track(b, dr, (fx, cap_top(f3, cy - bh * 0.15)), SELLER, f3, fg, sp3, "ra")
    f4, sp4 = fit_track(b, dr, [SELLER_ROLE], b.p(1600), band_mm * 0.105, 0.22,
                        lambda s: b.sans(s, "600"))
    track(b, dr, (fx, cap_top(f4, cy + bh * 0.19)), SELLER_ROLE, f4, sub, sp4, "ra")


def build(src: str, kind: str) -> Image.Image:
    out, w_mm, h_mm, dpi, band_mm, right, with_qr = SETS[kind]
    im = Image.open(os.path.join(SRC, src + ".png")).convert("RGB")
    col = band_color(im)
    b = Board(w_mm, h_mm, dpi)
    b.im.paste(fit_to(im, b.W, b.H).convert("RGBA"), (0, 0))

    slot = qr_slot(b)
    if slot:
        q = min(slot[2] - slot[0], slot[3] - slot[1]) - b.p(14)
        b.im.alpha_composite(qr_image(QR_URL, q, col),
                             (slot[0] + ((slot[2] - slot[0]) - q) // 2,
                              slot[1] + ((slot[3] - slot[1]) - q) // 2))

    bands(b, col, band_mm, right, with_qr)
    return b.im.convert("RGB")


def main() -> None:
    for kind, (out, w_mm, h_mm, dpi, *_rest) in SETS.items():
        os.makedirs(os.path.join(out, "onizleme"), exist_ok=True)
        print(f"\n{kind}: {w_mm}x{h_mm} mm @ {dpi} dpi "
              f"({round(w_mm / 25.4 * dpi)}x{round(h_mm / 25.4 * dpi)} px)")
        for name, _desc in DESIGNS:
            if not os.path.exists(os.path.join(SRC, name + ".png")):
                print(f"  ! {name} — kaynak yok, atlandı")
                continue
            im = build(name, kind)
            base = name.replace("mia-", f"{kind}-", 1)
            im.save(os.path.join(out, base + ".jpg"), quality=92, subsampling=0,
                    optimize=True, dpi=(dpi, dpi))
            im.resize((im.width // 6, im.height // 6), Image.LANCZOS).save(
                os.path.join(out, "onizleme", base + ".jpg"), quality=88,
                optimize=True)
            print(f"  -> {base}.jpg")


if __name__ == "__main__":
    main()
