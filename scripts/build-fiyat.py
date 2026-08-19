#!/usr/bin/env python3
"""
MİA PARK OCEAN — fiyat afişi.

Gönderilen "FİYAT AVANTAJI" afişinin birebir kurgusu, üç daire tipiyle:
üstte logo, çizgiler arasında üst satır, iki renkli dev manşet, el yazısı
alt satır ve altı çizgisi, lacivert fiyat kartları (altın rozetli), beyaz
özellik hapları, gün batımı render'ı, "SINIRLI SAYIDA" mührü, konum hapı
ve altta faizsiz finansman şeridi.

İKİ SÜRÜM
─────────
    fiyat-afis.jpg           rakamlı  — peşinat ve aylık taksit
    fiyat-afis-fiyatsiz.jpg  rakamsız — m² ve vade, fiyat için karekod

Orijinalde iki kart vardı ve sağda dört hap sütunu duruyordu. Üçüncü kart
girince kartlar TAM GENİŞLİĞE yayıldı, haplar da altlarında yatay şeride
indi; üç kart + sütun aynı satıra sığdırılınca 2.000.000 rakamı okunmaz
puntoya iniyordu.

Ölçü: 700 x 990 mm (A serisi oranı), 120 dpi → 3307 x 4677 px.

    python scripts/build-fiyat.py
"""

from __future__ import annotations

import importlib.util
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_spec = importlib.util.spec_from_file_location(
    "ru", os.path.join(ROOT, "scripts", "build-rollup.py"))
ru = importlib.util.module_from_spec(_spec)
sys.modules["ru"] = ru
_spec.loader.exec_module(ru)

gradient, cover, scrim, overlay = ru.gradient, ru.cover, ru.scrim, ru.overlay
track, fit, fit_track = ru.track, ru.fit, ru.fit_track
qr_image, lockup = ru.qr_image, ru.lockup
cap_h, cap_top = ru.cap_h, ru.cap_top
soft_shadow = ru.soft_shadow
PRICES, SIZES = ru.PRICES, ru.SIZES
SITE, PHONES = ru.SITE, ru.PHONES

OUT = os.path.join(ROOT, "tabela", "fiyat")
PREVIEW = os.path.join(OUT, "onizleme")

W_MM, H_MM, DPI = 800, 2000, 100
M = 58

# Onaylanan beş panonun paleti. Önceki sürümdeki kraliyet mavisi +
# hardal altını şablon gibi duruyordu; zemin gece laciverti, vurgu açık
# şampanya. Kartlar SAYDAM DEĞİL — render kartın içinden sızınca yazı
# çamurlanıyordu.
WHITE = (255, 255, 255)
NIGHT = (5, 18, 30)
NAVY = (10, 30, 48)                 # kart ve şerit gövdesi
NAVY_D = (7, 22, 36)
GOLD = (223, 199, 154)              # şampanya
GOLD_HI = (240, 224, 190)
GOLD_DIM = (176, 150, 106)
ICE = (206, 228, 240)
INK = (16, 26, 38)
QR_URL = "https://miaparkocean.com/?utm_source=fiyat"


def board() -> ru.B:
    ru.W_MM, ru.H_MM, ru.M = W_MM, H_MM, M
    return ru.B(W_MM, H_MM, DPI)


def sky_and_render(b, name: str = "night-gate", top: float = 596) -> None:
    """Altta render, üstünde kendi gökyüzünden uzatılmış gradyan.

    İnce şeridi doğrudan esnetmek bulutu dikey çizgiye çeviriyordu;
    uzatma örneklenen renkten gradyan kurup kaynağı ağır bulanıklıkla
    üstüne bindiriyor."""
    bh = round(W_MM * 2304 / 4096)
    im = cover(name, (b.W, b.p(bh)), 0.5)
    a = np.asarray(im.convert("RGB"), np.float32)
    c_e = tuple(a[:30].mean(axis=(0, 1)))
    c_f = tuple(a[round(b.p(bh) * 0.20):round(b.p(bh) * 0.26)].mean(axis=(0, 1)))
    tp = b.p(top)
    lay = gradient((b.W, tp), [(0.0, tuple(c * 0.72 for c in c_f)),
                               (0.45, c_f), (1.0, c_e)], angle=0.0)
    tex = im.crop((0, 0, b.W, round(b.p(bh) * 0.26))).resize((b.W, tp), Image.LANCZOS)
    tex = tex.filter(ImageFilter.GaussianBlur(max(4, tp // 9)))
    tex.putalpha(140)
    lay.alpha_composite(tex)
    b.im.alpha_composite(lay, (0, 0))
    b.im.alpha_composite(im, (0, tp))
    bot = b.H - tp - b.p(bh)
    if bot > 0:
        # İnce şeridi doğrudan esnetmek dikey çizgi üretiyordu; örneklenen
        # renkten gradyan kurulup kaynak ağır bulanıklıkla bindiriliyor.
        c_b = tuple(a[-round(b.p(bh) * 0.06):].mean(axis=(0, 1)))
        lay2 = gradient((b.W, bot), [(0.0, c_b), (0.45, tuple(c * 0.55 for c in c_b)),
                                     (1.0, NIGHT)], angle=0.0)
        tex2 = im.crop((0, b.p(bh) - round(b.p(bh) * 0.10), b.W, b.p(bh)))
        tex2 = tex2.resize((b.W, bot), Image.LANCZOS).filter(
            ImageFilter.GaussianBlur(max(6, bot // 8)))
        tex2.putalpha(110)
        lay2.alpha_composite(tex2)
        b.im.alpha_composite(lay2, (0, tp + b.p(bh)))
    # Üst yarı yazı için hafif açılır.
    b.im.alpha_composite(scrim((b.W, b.p(top)), [
        (0.0, (*NIGHT, 232)), (0.42, (*NIGHT, 188)), (1.0, (*NIGHT, 70)),
    ]), (0, 0))


def eyebrow(b, y: float, text: str) -> None:
    """Üst satır, iki yanında kısa çizgi — orijinalin açılışı."""
    dr = b.draw
    f, sp = fit_track(b, dr, [text], b.p(600), 16, 0.26, lambda s: b.cond(s))
    w = sum(dr.textlength(c, font=f) for c in text) + sp * (len(text) - 1)

    def paint(d):
        cx = b.p(W_MM / 2)
        track(b, d, (cx, cap_top(f, b.p(y))), text, f, (*GOLD, 250), sp, "ma")
        for s_ in (-1, 1):
            x0 = cx + s_ * (w / 2 + b.p(18))
            x1 = cx + s_ * (w / 2 + b.p(64))
            d.line([x0, b.p(y), x1, b.p(y)], fill=(*GOLD_DIM, 235),
                   width=max(2, b.p(0.9)))
    overlay(b, paint)


def headline(b, y: float, a: str, c: str) -> None:
    """İki renkli dev manşet, altında gölge."""
    dr = b.draw
    f = fit(b, dr, [f"{a} {c}"], b.p(W_MM - M * 2), 84,
            lambda s: b.playfair(s, 800))
    wa = dr.textlength(a + " ", font=f)
    tot = dr.textlength(f"{a} {c}", font=f)
    x0 = b.p(W_MM / 2) - tot / 2

    def paint(d):
        d.text((x0, b.p(y)), a, font=f, fill=WHITE, anchor="ls")
        d.text((x0 + wa, b.p(y)), c, font=f, fill=GOLD, anchor="ls")
    soft_shadow(b, paint, blur=6, alpha=120, dy=4)


def script_line(b, y: float, text: str) -> None:
    dr = b.draw
    f = fit(b, dr, [text], b.p(600), 44, lambda s: b.script(s, 700))
    w = dr.textlength(text, font=f)

    def paint(d):
        d.text((b.p(W_MM / 2), b.p(y)), text, font=f, fill=(*GOLD_HI, 252),
               anchor="ms")
        d.arc([b.p(W_MM / 2) - w / 2, b.p(y) + b.p(2), b.p(W_MM / 2) + w / 2,
               b.p(y) + b.p(26)], 0, 180, fill=(*GOLD_DIM, 235), width=max(2, b.p(1.2)))
    overlay(b, paint)


def cards(b, y: float, h: float, rows, priced: bool, x0: float = None,
          span: float = None) -> None:
    """Lacivert fiyat kartı: üst kenarında altın rozet, ortada dev rakam,
    beyaz hapta aylık, altta altın vade bandı."""
    x0 = M if x0 is None else x0
    span = (W_MM - M * 2) if span is None else span
    gap = 10
    cw = (span - gap * (len(rows) - 1)) / len(rows)
    l1 = "PEŞİNAT" if priced else "DAİRE BÜYÜKLÜĞÜ"
    l2 = "AYLIK SADECE" if priced else "ÖDEME PLANI"
    l3 = "VADE FARKSIZ 60 AY" if priced else "VADE FARKSIZ · %0 FAİZ"

    dr = b.draw
    ftyp = fit(b, dr, [r[0] for r in rows], b.p(88), 26, lambda s: b.mont(s, 700))
    fl, spl = fit_track(b, dr, [l1, l2], b.p(cw - 22), 11, 0.20,
                        lambda s: b.cond(s))
    fnum = fit(b, dr, [r[1] for r in rows], b.p(cw - 40), 44,
               lambda s: b.mont(s, 700))
    fay = fit(b, dr, [r[2] for r in rows], b.p(cw - 58), 36,
              lambda s: b.mont(s, 700))
    ftl = b.mont(15, 700)
    fv, spv = fit_track(b, dr, [l3], b.p(cw - 26), 11, 0.10, lambda s: b.cond(s))

    for i, (typ, big, small) in enumerate(rows):
        x = x0 + i * (cw + gap)

        def card(d, x=x, typ=typ, big=big, small=small):
            # Dolu zemin: saydam kartın altından render sızıp yazıyı
            # çamurlandırıyordu.
            d.rounded_rectangle([b.p(x), b.p(y), b.p(x + cw), b.p(y + h)],
                                radius=b.p(8), fill=(*NAVY, 255),
                                outline=(*GOLD_DIM, 200), width=max(2, b.p(0.9)))
            bw, bh = b.p(cw * 0.56), b.p(32)
            bx = b.p(x + cw / 2) - bw // 2
            d.rounded_rectangle([bx, b.p(y) - bh // 2, bx + bw, b.p(y) + bh // 2],
                                radius=bh // 2, fill=(*GOLD, 255))
            d.text((bx + bw / 2, cap_top(ftyp, b.p(y))), typ, font=ftyp,
                   fill=NIGHT, anchor="ma")

            cx = b.p(x + cw / 2)
            track(b, d, (cx, b.p(y + 52)), l1, fl, (*ICE, 235), spl, "ma")
            wn = d.textlength(big, font=fnum)
            wt = d.textlength("TL", font=ftl) if priced else 0
            x0 = cx - (wn + wt) / 2
            d.text((x0, b.p(y + 128)), big, font=fnum, fill=GOLD_HI, anchor="ls")
            if priced:
                d.text((x0 + wn, b.p(y + 128)), "TL", font=ftl, fill=GOLD_HI,
                       anchor="ls")
            d.line([b.p(x + 20), b.p(y + 154), b.p(x + cw - 20), b.p(y + 154)],
                   fill=(*GOLD_DIM, 170), width=max(1, b.p(0.6)))
            track(b, d, (cx, b.p(y + 186)), l2, fl, (*ICE, 235), spl, "ma")

            pw, ph = b.p(cw - 28), b.p(66)
            px, py = b.p(x + 14), b.p(y + 218)
            d.rounded_rectangle([px, py, px + pw, py + ph], radius=b.p(6),
                                fill=(255, 255, 255, 255))
            wa = d.textlength(small, font=fay)
            wt2 = d.textlength("TL", font=ftl) if priced else 0
            ax = cx - (wa + wt2) / 2
            d.text((ax, py + ph - b.p(15)), small, font=fay, fill=NIGHT, anchor="ls")
            if priced:
                d.text((ax + wa, py + ph - b.p(15)), "TL", font=ftl, fill=NIGHT,
                       anchor="ls")

            vy = b.p(y + h) - b.p(50)
            d.rounded_rectangle([px, vy, px + pw, vy + b.p(36)], radius=b.p(5),
                                fill=(*GOLD, 255))
            track(b, d, (cx, cap_top(fv, vy + b.p(18))), l3, fv, NIGHT, spv, "ma")
        overlay(b, card)


def _picto(d, kind, cx, cy, r, col, t):
    if kind == "onay":
        d.line([cx - r * .46, cy, cx - r * .1, cy + r * .36], fill=col, width=t)
        d.line([cx - r * .1, cy + r * .36, cx + r * .5, cy - r * .42], fill=col, width=t)
    elif kind == "grafik":
        d.line([cx - r * .6, cy + r * .55, cx + r * .62, cy + r * .55], fill=col, width=t)
        for i, hh in enumerate((0.28, 0.58, 0.9)):
            x = cx - r * .38 + i * r * .38
            d.rectangle([x - r * .12, cy + r * .55 - r * hh, x + r * .12,
                         cy + r * .55], outline=col, width=t)
    elif kind == "pin":
        d.ellipse([cx - r * .44, cy - r * .72, cx + r * .44, cy + r * .16],
                  outline=col, width=t)
        d.polygon([(cx - r * .2, cy + r * .02), (cx + r * .2, cy + r * .02),
                   (cx, cy + r * .72)], fill=col)
    elif kind == "el":
        d.arc([cx - r * .7, cy - r * .5, cx + r * .7, cy + r * .5], 200, 340,
              fill=col, width=t)
        d.line([cx - r * .5, cy + r * .3, cx + r * .5, cy + r * .3], fill=col, width=t)
        d.ellipse([cx - r * .18, cy - r * .62, cx + r * .18, cy - r * .26],
                  outline=col, width=t)


def feat_pills(b, x: float, y0: float, pw: float, h: float, items,
               gapy: float = 10) -> None:
    """Beyaz özellik hapları — orijinaldeki gibi SAĞDA DİKEY SÜTUN,
    kartların yanında. Alta indirilince afişin yapısı bozuluyordu."""
    dr = b.draw
    f, sp = fit_track(b, dr, [t for a in items for t in a[:2]], b.p(pw - h - 18), 11,
                      0.04, lambda s: b.mont(s, 600))

    for i, (l1, l2, kind) in enumerate(items):
        y = y0 + i * (h + gapy)

        def pill(d, y=y, l1=l1, l2=l2, kind=kind):
            d.rounded_rectangle([b.p(x), b.p(y), b.p(x + pw), b.p(y + h)],
                                radius=b.p(6), fill=(255, 255, 255, 255))
            r = b.p(h * 0.32)
            cx, cy = b.p(x + h * 0.5), b.p(y + h / 2)
            d.rounded_rectangle([cx - r, cy - r, cx + r, cy + r], radius=b.p(5),
                                fill=(*NAVY, 255))
            _picto(d, kind, cx, cy, r * 0.92, GOLD, max(2, b.p(1.2)))
            tx = b.p(x + h * 0.96)
            track(b, d, (tx, b.p(y + h * 0.26)), l1, f, (*INK, 255), sp)
            track(b, d, (tx, b.p(y + h * 0.58)), l2, f, (*INK, 255), sp)
        overlay(b, pill)


def seal(b, cx: float, cy: float, r: float) -> None:
    """SINIRLI SAYIDA mührü, altında kurdele."""
    dr = b.draw
    f1, sp1 = fit_track(b, dr, ["SINIRLI", "SAYIDA"], b.p(r * 1.5), 21, 0.04,
                        lambda s: b.mont(s, 800))
    f2, sp2 = fit_track(b, dr, ["BU FIRSAT", "KAÇMAZ!"], b.p(r * 1.9), 15, 0.04,
                        lambda s: b.mont(s, 800))

    def paint(d):
        d.ellipse([b.p(cx - r), b.p(cy - r), b.p(cx + r), b.p(cy + r)],
                  fill=(*GOLD, 255), outline=(*GOLD_HI, 255), width=max(2, b.p(1.4)))
        d.ellipse([b.p(cx - r * .88), b.p(cy - r * .88), b.p(cx + r * .88),
                   b.p(cy + r * .88)], outline=(255, 255, 255, 160),
                  width=max(1, b.p(0.9)))
        for k in (-1, 0, 1):
            sx, sy, ss = b.p(cx + k * r * 0.26), b.p(cy - r * 0.46), b.p(r * 0.09)
            d.polygon([(sx, sy - ss), (sx + ss * .32, sy - ss * .28),
                       (sx + ss, sy - ss * .2), (sx + ss * .42, sy + ss * .24),
                       (sx + ss * .6, sy + ss), (sx, sy + ss * .46),
                       (sx - ss * .6, sy + ss), (sx - ss * .42, sy + ss * .24),
                       (sx - ss, sy - ss * .2), (sx - ss * .32, sy - ss * .28)],
                      fill=WHITE)
        track(b, d, (b.p(cx), b.p(cy - r * 0.24)), "SINIRLI", f1, NIGHT, sp1, "ma")
        track(b, d, (b.p(cx), b.p(cy + r * 0.04)), "SAYIDA", f1, NIGHT, sp1, "ma")

        rw, rh = b.p(r * 2.05), b.p(r * 0.58)
        rx, ry = b.p(cx) - rw // 2, b.p(cy + r * 0.34)
        d.polygon([(rx, ry), (rx + rw, ry), (rx + rw - b.p(r * .16), ry + rh // 2),
                   (rx + rw, ry + rh), (rx, ry + rh),
                   (rx + b.p(r * .16), ry + rh // 2)], fill=(*NAVY, 255))
        track(b, d, (b.p(cx), ry + rh * 0.28), "BU FIRSAT", f2, WHITE, sp2, "ma")
        track(b, d, (b.p(cx), ry + rh * 0.60), "KAÇMAZ!", f2, WHITE, sp2, "ma")
    soft_shadow(b, paint, blur=6, alpha=120, dy=4)


def pin_pill(b, x: float, y: float, w: float, h: float, lines) -> None:
    dr = b.draw
    f, sp = fit_track(b, dr, lines, b.p(w - 58), 13, 0.08, lambda s: b.mont(s, 800))

    def paint(d):
        d.rounded_rectangle([b.p(x), b.p(y), b.p(x + w), b.p(y + h)],
                            radius=b.p(6), fill=(*NAVY, 255),
                            outline=(*GOLD_DIM, 170), width=max(2, b.p(0.9)))
        cx, cy, r = b.p(x + h * 0.52), b.p(y + h / 2), b.p(h * 0.26)
        d.ellipse([cx - r, cy - r * 1.15, cx + r, cy + r * 0.55], fill=(*GOLD, 255))
        d.polygon([(cx - r * .5, cy + r * .3), (cx + r * .5, cy + r * .3),
                   (cx, cy + r * 1.25)], fill=(*GOLD, 255))
        d.ellipse([cx - r * .3, cy - r * .55, cx + r * .3, cy + r * .05],
                  fill=(*NAVY, 255))
        tx = b.p(x + h * 0.96)
        for i, t in enumerate(lines):
            track(b, d, (tx, b.p(y + h * (0.26 + i * 0.32))), t, f, WHITE, sp)
    overlay(b, paint)


def bottom_bar(b, y: float, h: float) -> None:
    """Tasarrufa dayalı faizsiz finansman şeridi + üç ret."""
    dr = b.draw
    fh = fit(b, dr, ["Tasarrufa Dayalı Faizsiz Finansman Sistemi ile"],
             b.p(W_MM - M * 2 - 50), 20, lambda s: b.cormorant(s, 500))
    items = ["BANKA YOK", "FAİZ YOK", "KEFİL YOK"]
    fi, spi = fit_track(b, dr, items, b.p((W_MM - M * 2) / 3 - 76), 17, 0.06,
                        lambda s: b.mont(s, 700))

    def paint(d):
        d.rounded_rectangle([b.p(M), b.p(y), b.p(W_MM - M), b.p(y + h)],
                            radius=b.p(8), fill=(*NAVY, 255),
                            outline=(*GOLD_DIM, 180), width=max(2, b.p(0.9)))
        a, bpart, c = "Tasarrufa Dayalı ", "Faizsiz", " Finansman Sistemi ile"
        wa = d.textlength(a, font=fh)
        wb = d.textlength(bpart, font=fh)
        wc = d.textlength(c, font=fh)
        x0 = b.p(W_MM / 2) - (wa + wb + wc) / 2
        d.text((x0, b.p(y + 27)), a, font=fh, fill=WHITE, anchor="ls")
        d.text((x0 + wa, b.p(y + 27)), bpart, font=fh, fill=GOLD, anchor="ls")
        d.text((x0 + wa + wb, b.p(y + 27)), c, font=fh, fill=WHITE, anchor="ls")

        step = (W_MM - M * 2) / 3
        for i, t in enumerate(items):
            cx = b.p(M + step * (i + 0.5))
            w = sum(d.textlength(ch, font=fi) for ch in t) + spi * (len(t) - 1)
            ix = cx - w / 2 - b.p(26)
            iy = b.p(y + 56)
            d.rectangle([ix - b.p(9), iy - b.p(2), ix + b.p(9), iy + b.p(1)],
                        fill=GOLD)
            d.polygon([(ix, iy - b.p(12)), (ix + b.p(10), iy - b.p(3)),
                       (ix - b.p(10), iy - b.p(3))], fill=GOLD)
            for k in (-5, 0, 5):
                d.line([ix + b.p(k), iy + b.p(1), ix + b.p(k), iy + b.p(9)],
                       fill=GOLD, width=max(2, b.p(1.2)))
            track(b, d, (cx + b.p(14), cap_top(fi, iy + b.p(3))), t, fi, WHITE,
                  spi, "ma")
            if i:
                xv = b.p(M + step * i)
                d.line([xv, b.p(y + 40), xv, b.p(y + h - 8)],
                       fill=(255, 255, 255, 90), width=max(1, b.p(0.8)))
    overlay(b, paint)


FEATS = [("EN UYGUN", "FİYATLAR", "onay"),
         ("YÜKSEK YATIRIM", "POTANSİYELİ", "grafik"),
         ("İZMİT MİA BÖLGESİ'NDE", "EŞSİZ KONUM", "pin"),
         ("VADE FARKSIZ", "60 AY TAKSİT", "el")]


def foot(b, y: float = 1836) -> None:
    """Alt künye — onaylanan roll-up'larla aynı."""
    dr = b.draw

    def rule(d):
        d.line([b.p(M), b.p(y - 30), b.p(W_MM - M), b.p(y - 30)],
               fill=(*GOLD_DIM, 150), width=max(1, b.p(0.6)))
    overlay(b, rule)

    qs = b.p(54)
    qx, qy = b.p(W_MM - M) - qs, b.p(y - 10)

    def plate(d):
        d.rounded_rectangle([qx - b.p(5), qy - b.p(5), qx + qs + b.p(5),
                             qy + qs + b.p(5)], radius=b.p(4), fill=(255, 255, 255, 252))
    overlay(b, plate)
    b.im.alpha_composite(qr_image(QR_URL, qs, NIGHT), (qx, qy))

    fs, sps = fit_track(b, dr, [f"{ru.SELLER} · {ru.SELLER_ROLE}"], b.p(440), 10,
                        0.16, lambda s_: b.cond(s_))

    def paint(d):
        d.text((b.p(M), b.p(y + 20)), SITE, font=b.marcellus(28), fill=WHITE,
               anchor="ls")
        d.text((b.p(M), b.p(y + 50)), "  ·  ".join(PHONES), font=b.mont(17, 700),
               fill=WHITE, anchor="ls")
        track(b, d, (b.p(M), b.p(y + 60)), f"{ru.SELLER} · {ru.SELLER_ROLE}", fs,
              (*ICE, 215), sps)
    overlay(b, paint)


def afis(priced: bool) -> Image.Image:
    b = board()
    sky_and_render(b, "night-gate", 980)

    lg = lockup(b.p(190), white=True)
    b.im.alpha_composite(lg, ((b.W - lg.width) // 2, b.p(70)))

    eyebrow(b, 264, "İZMİT'İN EN DEĞERLİ LOKASYONUNDA")
    headline(b, 372, "FİYAT", "AVANTAJI")
    script_line(b, 448, "Kaçırılmayacak fırsat!")

    # Kartlar SOLDA, haplar SAĞDA dikey sütun — referansın yapısı.
    cards(b, 546, 374, PRICES if priced else SIZES, priced, x0=M, span=488)
    feat_pills(b, 564, 546, 178, 85, FEATS, gapy=11)

    pin_pill(b, M, 1276, 216, 64, ["İZMİT MİA", "BÖLGESİ"])
    seal(b, 616, 1306, 94)
    bottom_bar(b, 1524, 122)

    if not priced:
        dr = b.draw
        fq, spq = fit_track(b, dr, ["FİYAT VE KAT PLANLARI İÇİN KAREKODU OKUTUN"],
                            b.p(560), 13, 0.16, lambda s: b.cond(s))

        def note(d):
            track(b, d, (b.p(M), b.p(1690)),
                  "FİYAT VE KAT PLANLARI İÇİN KAREKODU OKUTUN", fq, (*GOLD, 250), spq)
        overlay(b, note)

    ru.vignette(b, 0.36, 2.3)
    foot(b, 1836)
    return b.im.convert("RGB")


DESIGNS = [("fiyat-afis", lambda: afis(True), "rakamlı"),
           ("fiyat-afis-fiyatsiz", lambda: afis(False), "rakamsız")]


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(PREVIEW, exist_ok=True)
    for name, fn, label in DESIGNS:
        im = fn()
        p = os.path.join(OUT, f"{name}.jpg")
        im.save(p, "JPEG", quality=94, subsampling=0, optimize=True, dpi=(DPI, DPI))
        sm = im.copy()
        sm.thumbnail((1400, 1400), Image.LANCZOS)
        sm.save(os.path.join(PREVIEW, f"{name}.jpg"), "JPEG", quality=88, optimize=True)
        print(f"  {name:<24} {label:<12} {im.width}x{im.height} px  "
              f"{os.path.getsize(p)/1e6:.1f} MB")
    print(f"\n  → {OUT}")


if __name__ == "__main__":
    main()
