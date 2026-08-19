#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MİA PARK OCEAN — ekip yaka kartları (kişiye özel).

Lansman yaka kartının isim isim basılmış hâli. Tasarım tek yerde, isimler
EKIP listesinde; kadro değişince yalnızca o liste düzenlenir.

ÖLÇÜ: 90 x 130 mm, 1:1 ölçekte 300 dpi (1063 x 1535 px) — depodaki diğer
yaka kartlarıyla aynı, standart kordon kabına giriyor.

DÜZEN (mm, üstten)
──────────────────
     0 –  14   kordon deliği payı; kılavuz kapsül burada
    18 –  62   logo kilidi, ortalanmış
    72 –  92   isim + unvan + vurgu çizgisi, sola dayalı
   100 – 122   kurum / etkinlik / adres bloğu, sağ altta karekod

Soyadı BÜYÜK HARF: isimle soyadı bir bakışta ayrılıyor, kalabalıkta
soyadı uzaktan okunuyor.

İsim punto'su altı kartta da AYNI: en uzun isme göre bir kez ölçülüp
hepsine uygulanıyor. Kart başına ayrı punto seçilirse set dağınık
görünüyor, yan yana asıldıklarında isimler farklı boyda çıkıyor.

    python scripts/build-yaka-ekip.py
"""
from __future__ import annotations

import importlib.util
import os
import sys

from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_spec = importlib.util.spec_from_file_location(
    "bs", os.path.join(ROOT, "scripts", "build-signage.py"))
bs = importlib.util.module_from_spec(_spec)
sys.modules["bs"] = bs
_spec.loader.exec_module(bs)

Board, gradient, glow, crisp = bs.Board, bs.gradient, bs.glow, bs.crisp
track, fit_track, qr_image, overlay = bs.track, bs.fit_track, bs.qr_image, bs.overlay

WHITE, INK = bs.WHITE, bs.INK
DEEP, DARK, OCEAN = bs.MIA_DEEP, bs.MIA_DARK, bs.MIA_OCEAN
CYAN, AQUA, PALE, ICE = bs.MIA_CYAN, bs.MIA_AQUA, bs.MIA_PALE, bs.MIA_ICE

OUT = os.path.join(ROOT, "tabela", "yaka-ekip")
PREVIEW = os.path.join(OUT, "onizleme")

W_MM, H_MM, DPI = 90, 130, 300
PAD = 14                     # sol/sağ yazı marjı
SLOT = 14                    # üstten kordon deliğine ayrılan bant
QR_URL = "https://miaparkocean.com"

SELLER = bs.SELLER           # OCEAN GAYRİMENKUL
EVENT = ["21 AĞUSTOS 2026", "EMEX OTEL · KOCAELİ", "MIAPARKOCEAN.COM"]

# (ad, SOYAD, unvan) — kadro değişince yalnızca burası düzenlenir.
EKIP = [
    ("Engin",   "KOÇAK",    "BROKER"),
    ("Gül",     "GÜNERHAN", "SATIŞ TEMSİLCİSİ"),
    ("Nursena", "AÇIKGÖZ",  "SATIŞ TEMSİLCİSİ"),
    ("Emir",    "YAVUZ",    "SATIŞ TEMSİLCİSİ"),
    ("Kenan",   "DUMAN",    "SATIŞ TEMSİLCİSİ"),
    ("Mert",    "GÜLER",    "SATIŞ TEMSİLCİSİ"),
]


def slug(first: str, last: str) -> str:
    tr = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")
    return f"{first}-{last}".translate(tr).lower().replace(" ", "-")


def cap_top(f, cy: float) -> float:
    t, b = f.getbbox("H")[1], f.getbbox("H")[3]
    return cy - (t + b) / 2


def shell(b: Board) -> None:
    """Zemin, çift çerçeve ve kordon kılavuzu."""
    b.im.paste(gradient((b.W, b.H),
                        [(0.0, (252, 253, 254)), (0.45, (243, 250, 252)),
                         (1.0, (223, 240, 245))], angle=0.18), (0, 0))
    b.im.alpha_composite(glow((b.W, b.H), b.W * 0.5, b.H * 0.26, b.W * 0.9,
                              WHITE, 0.55))
    dr = b.draw

    # Çift çerçeve: dıştaki petrol, içteki ince buz mavisi.
    o = b.p(2.6)
    dr.rounded_rectangle([o, o, b.W - o, b.H - o], radius=b.p(6.5),
                         outline=(*DARK, 235), width=max(2, b.p(0.55)))
    i = b.p(5.2)
    overlay(b, lambda d: d.rounded_rectangle([i, i, b.W - i, b.H - i],
                                             radius=b.p(4.6),
                                             outline=(*PALE, 150),
                                             width=max(1, b.p(0.3))))

    # Kordon deliği kılavuzu — kesimci nereye zımbalayacağını görsün.
    sw, sh = b.p(17), b.p(3.8)
    sx, sy = (b.W - sw) // 2, b.p(6.2)
    overlay(b, lambda d: d.rounded_rectangle([sx, sy, sx + sw, sy + sh],
                                             radius=sh // 2,
                                             outline=(*PALE, 210),
                                             width=max(1, b.p(0.4))))


def logo(b: Board, width_mm: float = 60, top_mm: float = 19) -> None:
    im = Image.open(os.path.join(bs.BRAND, "logo-ocean-trim.png")).convert("RGBA")
    box = im.getbbox()
    if box:
        im = im.crop(box)
    lg = crisp(im, b.p(width_mm))
    b.im.alpha_composite(lg, ((b.W - lg.width) // 2, b.p(top_mm)))


def name_font(b: Board):
    """Altı kartın ortak isim puntosu — en uzun isme göre bir kez ölçülür."""
    dr = b.draw
    longest = max((f"{f} {l}" for f, l, _ in EKIP), key=len)
    s = 11.5
    while s > 6.5 and dr.textlength(longest, font=b.serif(s, "700")) > b.p(W_MM - PAD * 2):
        s *= 0.97
    return b.serif(s, "700")


def card(first: str, last: str, title: str, nf) -> Image.Image:
    b = Board(W_MM, H_MM, DPI)
    shell(b)
    logo(b)
    dr = b.draw
    x = b.p(PAD)

    dr.text((x, cap_top(nf, b.p(78))), f"{first} {last}", font=nf, fill=DEEP)

    ft, spt = fit_track(b, dr, [t for _, _, t in EKIP], b.p(W_MM - PAD * 2 - 4),
                        3.6, 0.16, lambda s: b.sans(s, "700"), floor_mm=2.0)
    track(b, dr, (x, cap_top(ft, b.p(88.5))), title, ft, (*DARK, 255), spt)

    dr.rectangle([x, b.p(96), x + b.p(22), b.p(97.4)], fill=OCEAN)

    # ---- alt blok: solda künye, sağda karekod, ARALARINDA GERÇEK PAY
    # Karekod ilk denemede yazının üstüne biniyordu. Sebep punto değil
    # fit_track'in TABANI: imzalar için yazılmış 5 mm'lik alt sınır, 3,1 mm'den
    # başlayan yaka yazısından büyük olduğu için küçültme döngüsü hiç
    # çalışmıyor, satır kutuya sığmasa da olduğu gibi basılıyordu. Taban
    # 1,8 mm'ye indirildi ve künyenin kutusu karekod sütunu düşülerek
    # hesaplanıyor.
    qmm, gap = 20.0, 5.0
    q = b.p(qmm)
    qx, qy = b.W - b.p(PAD) - q, b.p(103)
    plate = b.p(1.8)
    dr.rounded_rectangle([qx - plate, qy - plate, qx + q + plate, qy + q + plate],
                         radius=b.p(1.6), fill=WHITE, outline=(*PALE, 200),
                         width=max(1, b.p(0.3)))
    b.im.alpha_composite(qr_image(QR_URL, q, DEEP), (qx, qy))

    lines = [SELLER] + EVENT
    fi, spi = fit_track(b, dr, lines, b.p(W_MM - PAD * 2 - qmm - gap),
                        3.2, 0.14, lambda s: b.sans(s, "600"), floor_mm=1.8)
    lh = 5.4
    y0 = 103 + qmm / 2 - (len(lines) - 1) * lh / 2
    for i, line in enumerate(lines):
        track(b, dr, (x, cap_top(fi, b.p(y0 + i * lh))), line, fi,
              DEEP if i == 0 else (*DARK, 235), spi)

    return b.im.convert("RGB")


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(PREVIEW, exist_ok=True)
    nf = name_font(Board(W_MM, H_MM, DPI))
    print(f"Ekip yaka kartları — {W_MM}x{H_MM} mm @ {DPI} dpi "
          f"({round(W_MM / 25.4 * DPI)}x{round(H_MM / 25.4 * DPI)} px)")
    for first, last, title in EKIP:
        im = card(first, last, title, nf)
        name = f"yaka-{slug(first, last)}"
        im.save(os.path.join(OUT, name + ".jpg"), quality=95, subsampling=0,
                optimize=True, dpi=(DPI, DPI))
        im.resize((im.width // 3, im.height // 3), Image.LANCZOS).save(
            os.path.join(PREVIEW, name + ".jpg"), quality=90, optimize=True)
        print(f"  -> {name}.jpg   {first} {last} · {title}")


if __name__ == "__main__":
    main()
