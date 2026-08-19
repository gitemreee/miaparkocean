#!/usr/bin/env python3
"""
Roll-up yön denemesi — AYNI pano, üç farklı dilde.

Amaç seçim yaptırmak: sekiz panoyu yanlış yöne üretmeden önce tek panoyu
üç ayrı dilde kurup hangisinin tutacağını görmek.

    A · REFERANS   gün batımı zemin, ortalanmış altın tipografi, rozetli
                   ikonlar — gönderilen afişlerin dili
    B · KREM       sıcak krem zemin, koyu mürekkep, altın saç teli;
                   fotoğraf altta çapa — lüks broşür dili
    C · CAM        tam sayfa render üstünde buzlu cam panel, sans manşet

ZEMİNDE DÜZ RENK YOK
────────────────────
Yatay render (4096x2304) dikey panoya tam sayfa girmiyor; kırpınca
kompozisyon gidiyor. Çözüm: kareyi doğal en-boyunda bant olarak koyup
GÖKYÜZÜNÜ YUKARI, YOLU AŞAĞI uzatmak. İkisi de düz yüzey olduğu için
dikey esnetme görünmüyor, pano baştan sona fotoğraf oluyor.

    python scripts/build-rollup-yon.py
"""

from __future__ import annotations

import importlib.util
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_spec = importlib.util.spec_from_file_location(
    "bs", os.path.join(ROOT, "scripts", "build-signage.py"))
bs = importlib.util.module_from_spec(_spec)
sys.modules["bs"] = bs
_spec.loader.exec_module(bs)

Board = bs.Board
gradient, cover, scrim, overlay = bs.gradient, bs.cover, bs.scrim, bs.overlay
track, fit, fit_track, wrap = bs.track, bs.fit, bs.fit_track, bs.wrap
qr_image, lockup, load, grade = bs.qr_image, bs.lockup, bs.load, bs.grade

OUT = os.path.join(ROOT, "tabela", "yon")
PREVIEW = os.path.join(OUT, "onizleme")

W_MM, H_MM, DPI = 800, 2000, 100
WHITE = (255, 255, 255)
SITE, PHONES = bs.SITE, bs.PHONES
SELLER, SELLER_ROLE = bs.SELLER, bs.SELLER_ROLE
QR_URL = "https://miaparkocean.com/?utm_source=rollup"
UNITS, TOTAL = bs.UNITS, bs.TOTAL_UNITS

GOLD = (208, 168, 92)
GOLD_STOPS = [(0.0, (150, 106, 38)), (0.22, (234, 202, 128)), (0.45, (252, 238, 194)),
              (0.70, (202, 156, 72)), (1.0, (138, 96, 30))]
CREAM = (246, 240, 229)
INKD = (26, 32, 44)


def board() -> Board:
    return Board(W_MM, H_MM, DPI)


def cap_h(f) -> float:
    bb = f.getbbox("H")
    return bb[3] - bb[1]


def cap_top(f, cy: float) -> float:
    bb = f.getbbox("H")
    return cy - (bb[1] + bb[3]) / 2


def metal(b, xy, text, font, stops=GOLD_STOPS, anchor="ls") -> None:
    mask = Image.new("L", b.im.size, 0)
    ImageDraw.Draw(mask).text(xy, text, font=font, fill=255, anchor=anchor)
    box = mask.getbbox()
    if not box:
        return
    x0, y0, x1, y1 = box
    g = gradient((x1 - x0, y1 - y0), stops, angle=0.0)
    layer = Image.new("RGBA", b.im.size, (0, 0, 0, 0))
    layer.paste(g, (x0, y0), mask.crop(box))
    b.im.alpha_composite(layer)


def _avg(im: Image.Image, y0: int, y1: int):
    a = np.asarray(im.convert("RGB"), np.float32)[max(0, y0):max(1, y1)]
    return tuple(a.mean(axis=(0, 1)))


def _extend(b: Board, im: Image.Image, h: int, src_box, dark: float,
            flip: bool) -> Image.Image:
    """Gökyüzünü/yolu uzatan katman.

    İnce bir şeridi doğrudan esnetmek OLMUYOR: 200 pikseli 4000 piksele
    çekince bulutun yatay dokusu dikey çizgilere dönüşüyordu. Onun yerine
    renk gradyanı örneklenen renklerden kuruluyor, kaynak bölge de AĞIR
    BULANIKLIKLA üstüne bindiriliyor — doku kalıyor, çizgi kalmıyor.
    """
    y0, y1 = src_box
    c_edge = _avg(im, y0, y0 + max(2, (y1 - y0) // 8))
    c_far = _avg(im, y1 - max(2, (y1 - y0) // 8), y1)
    stops = ([(0.0, tuple(c * dark for c in c_far)), (0.62, c_far), (1.0, c_edge)]
             if not flip else
             [(0.0, c_edge), (0.45, c_far), (1.0, tuple(c * dark for c in c_far))])
    layer = gradient((b.W, h), stops, angle=0.0)

    tex = im.crop((0, y0, b.W, y1)).resize((b.W, h), Image.LANCZOS)
    tex = tex.filter(ImageFilter.GaussianBlur(max(4, h // 9)))
    tex.putalpha(150)
    layer.alpha_composite(tex)
    return layer


def photo_full(b: Board, name: str, band_top: float, band_h: float,
               focus: float = 0.5, warm: float = 1.0) -> None:
    """Kare doğal en-boyunda bant; üstü gökyüzüyle, altı yolla uzatılır.

    Kareyi dikey panoya kırparak sığdırmak yerine bu yol seçildi: kırpınca
    simetrik ikiz blok kompozisyonu yarısından kesiliyordu.
    """
    bh = b.p(band_h)
    im = cover(name, (b.W, bh), focus)
    if warm != 1.0:
        im = ImageEnhance.Color(im.convert("RGB")).enhance(warm).convert("RGBA")

    top_px = b.p(band_top)
    if top_px > 0:
        b.im.alpha_composite(
            _extend(b, im, top_px, (0, round(bh * 0.26)), 0.42, False), (0, 0))

    b.im.alpha_composite(im, (0, top_px))

    bot = b.H - (top_px + bh)
    if bot > 0:
        b.im.alpha_composite(
            _extend(b, im, bot, (round(bh * 0.90), bh), 0.34, True),
            (0, top_px + bh))


def veil(b: Board, y0: float, y1: float, a0: int, a1: int,
         col=(4, 10, 22)) -> None:
    h = b.p(y1) - b.p(y0)
    if h <= 0:
        return
    b.im.alpha_composite(scrim((b.W, h), [
        (0.0, (*col, a0)), (1.0, (*col, a1)),
    ]), (0, b.p(y0)))


def orn(b: Board, cx: float, y: float, half: float, color=GOLD, a: int = 235,
        w: float = 0.7, diamond: bool = True) -> None:
    def paint(d):
        px, py, hw = b.p(cx), b.p(y), b.p(half)
        t = max(1, b.p(w))
        d.line([px - hw, py, px + hw, py], fill=(*color, a), width=t)
        if diamond:
            s = b.p(2.4)
            d.polygon([(px, py - s), (px + s, py), (px, py + s), (px - s, py)],
                      fill=(*color, a))
    overlay(b, paint)


def icon(d, kind, cx, cy, r, col, t):
    if kind == "rozet":
        d.ellipse([cx - r * .72, cy - r * .72, cx + r * .72, cy + r * .72],
                  outline=col, width=t)
        s = r * .30
        d.polygon([(cx, cy - s), (cx + s * .34, cy - s * .28), (cx + s, cy - s * .22),
                   (cx + s * .44, cy + s * .24), (cx + s * .6, cy + s), (cx, cy + s * .5),
                   (cx - s * .6, cy + s), (cx - s * .44, cy + s * .24),
                   (cx - s, cy - s * .22), (cx - s * .34, cy - s * .28)], fill=col)
        for sx in (-1, 1):
            d.line([cx + sx * r * .40, cy + r * .62, cx + sx * r * .56, cy + r * 1.05],
                   fill=col, width=t)
    elif kind == "kalkan":
        d.polygon([(cx, cy - r), (cx + r * .78, cy - r * .62), (cx + r * .78, cy + r * .18),
                   (cx, cy + r), (cx - r * .78, cy + r * .18), (cx - r * .78, cy - r * .62)],
                  outline=col, width=t)
        d.line([cx - r * .34, cy, cx - r * .06, cy + r * .30], fill=col, width=t)
        d.line([cx - r * .06, cy + r * .30, cx + r * .40, cy - r * .34], fill=col, width=t)
    elif kind == "ev":
        d.polygon([(cx, cy - r * .92), (cx + r * .88, cy - r * .05), (cx - r * .88, cy - r * .05)],
                  outline=col, width=t)
        d.rectangle([cx - r * .60, cy - r * .05, cx + r * .60, cy + r * .86],
                    outline=col, width=t)
        d.rectangle([cx - r * .18, cy + r * .30, cx + r * .18, cy + r * .86],
                    outline=col, width=t)
    elif kind == "takvim":
        d.rounded_rectangle([cx - r * .84, cy - r * .66, cx + r * .84, cy + r * .82],
                            radius=int(r * .16), outline=col, width=t)
        d.line([cx - r * .84, cy - r * .24, cx + r * .84, cy - r * .24], fill=col, width=t)
        for sx in (-.44, .44):
            d.line([cx + r * sx, cy - r * .90, cx + r * sx, cy - r * .52], fill=col, width=t)


# ==================================================================== A · REFERANS
def yon_a() -> Image.Image:
    """Gönderilen afişlerin dili: gün batımı zemin, ortalanmış altın
    tipografi, rozetli ikonlar, altta daire şeridi. Sıcak ve dolu."""
    b = board()
    photo_full(b, "night-gate", 900, 450, 0.5, warm=1.06)

    # Yazının oturacağı yerler koyulaşsın, render sönmesin.
    veil(b, 0, 660, 190, 35)
    veil(b, 660, 900, 35, 0)
    veil(b, 1350, 2000, 0, 232)

    lg = lockup(b.p(330), white=True)
    g = gradient(lg.size, GOLD_STOPS, angle=0.2)
    g.putalpha(lg.split()[3])
    b.im.alpha_composite(g, ((b.W - g.width) // 2, b.p(74)))

    dr = b.draw
    cx = W_MM / 2

    fh = fit(b, dr, ["Lüks Artık", "Ulaşılabilir."], b.p(690), 66,
             lambda s: b.serif(s, "700"))
    step = cap_h(fh) * 1.30
    w1 = dr.textlength("Lüks ", font=fh)
    t1 = dr.textlength("Lüks Artık", font=fh)
    x1 = b.p(cx) - t1 / 2
    metal(b, (x1, b.p(400)), "Lüks", fh)

    def head(d):
        d.text((x1 + w1, b.p(400)), "Artık", font=fh, fill=WHITE, anchor="ls")
        d.text((b.p(cx), b.p(400) + step), "Ulaşılabilir.", font=fh, fill=WHITE,
               anchor="ms")
    overlay(b, head)

    fs = b.sans(17, "400")

    def sub(d):
        d.text((b.p(cx), b.p(508)), "Avantajlı peşinat,", font=fs,
               fill=(238, 228, 210, 250), anchor="ms")
        d.text((b.p(cx), b.p(536)), "vade farksız 60 ay.", font=fs,
               fill=(238, 228, 210, 250), anchor="ms")
    overlay(b, sub)

    orn(b, cx, 588, 120)

    items = [("rozet", "YÜKSEK KALİTE", "MODERN YAŞAM"),
             ("kalkan", "GÜVENLİ YATIRIM", "GÜÇLÜ GELECEK"),
             ("ev", "KONFORLU YAŞAM", "ESTETİK MİMARİ")]
    step_x = (W_MM - 120) / 3
    fi, spi = fit_track(b, dr, [t for _, a, c in items for t in (a, c)],
                        b.p(step_x - 20), 8.6, 0.16, lambda s: b.sans(s, "700"))

    def row(d):
        for i, (kind, l1, l2) in enumerate(items):
            ix = b.p(60 + step_x * (i + 0.5))
            icon(d, kind, ix, b.p(650), b.p(15), (*GOLD, 255), max(2, b.p(1.1)))
            y1 = b.p(676)
            track(b, d, (ix, y1), l1, fi, (*WHITE, 248), spi, "ma")
            track(b, d, (ix, y1 + cap_h(fi) * 1.7), l2, fi, (232, 220, 200, 235),
                  spi, "ma")
            if i:
                x = b.p(60 + step_x * i)
                d.line([x, b.p(630), x, b.p(700)], fill=(*GOLD, 140),
                       width=max(1, b.p(0.5)))
    overlay(b, row)

    # Alt: daire şeridi
    ys = 1494
    fa, spa = fit_track(b, dr, [f"{c} ADET" for *_, c in UNITS], b.p(160), 8.4, 0.15,
                        lambda s: b.sans(s, "700"))
    ft = fit(b, dr, [u[0] for u in UNITS], b.p(150), 27, lambda s: b.serif(s, "700"))
    fm, spm = fit_track(b, dr, [u[2] for u in UNITS], b.p(150), 7.6, 0.14,
                        lambda s: b.sans(s, "700"))
    stepu = (W_MM - 120) / 4

    def units(d):
        for i, (typ, name, area, count) in enumerate(UNITS):
            ux = b.p(60 + stepu * (i + 0.5))
            icon(d, "ev", ux, b.p(ys), b.p(9), (*GOLD, 250), max(1, b.p(0.7)))
            track(b, d, (ux, b.p(ys + 18)), f"{count} ADET", fa, (*GOLD, 252), spa, "ma")
            d.text((ux, b.p(ys + 56)), typ, font=ft, fill=WHITE, anchor="ms")
            track(b, d, (ux, b.p(ys + 64)), area, fm, (228, 218, 200, 240), spm, "ma")
            if i:
                x = b.p(60 + stepu * i)
                d.line([x, b.p(ys - 12), x, b.p(ys + 76)], fill=(*GOLD, 130),
                       width=max(1, b.p(0.5)))
    overlay(b, units)

    orn(b, cx, 1640, 300)
    fq, spq = fit_track(b, dr, ["HAYALİNİZDEKİ YAŞAM, ŞİMDİ ÇOK DAHA YAKIN."],
                        b.p(690), 12, 0.26, lambda s: b.sans(s, "700"))

    def tag(d):
        track(b, d, (b.p(cx), b.p(1676)),
              "HAYALİNİZDEKİ YAŞAM, ŞİMDİ ÇOK DAHA YAKIN.", fq, (*GOLD, 252), spq, "ma")
    overlay(b, tag)

    foot_a(b)
    return b.im.convert("RGB")


def foot_a(b: Board) -> None:
    dr = b.draw
    qs = b.p(44)
    qx, qy = b.W - b.p(60) - qs, b.p(1858)

    def plate(d):
        d.rounded_rectangle([qx - b.p(4), qy - b.p(4), qx + qs + b.p(4), qy + qs + b.p(4)],
                            radius=b.p(3), fill=(255, 255, 255, 250))
    overlay(b, plate)
    b.im.alpha_composite(qr_image(QR_URL, qs, (14, 22, 38)), (qx, qy))

    fi, spi = fit_track(b, dr, [f"{SELLER} · {SELLER_ROLE}"], b.p(340), 7.4, 0.16,
                        lambda s: b.sans(s, "700"))

    def paint(d):
        d.text((b.p(60), b.p(1888)), SITE, font=b.serif(23, "600"), fill=WHITE,
               anchor="ls")
        d.text((b.p(60), b.p(1922)), "  ·  ".join(PHONES), font=b.sans(12.5, "700"),
               fill=(*GOLD, 255), anchor="ls")
        track(b, d, (b.p(60), b.p(1932)), f"{SELLER} · {SELLER_ROLE}", fi,
              (224, 214, 198, 225), spi)
    overlay(b, paint)


# ==================================================================== B · KREM
def yon_b() -> Image.Image:
    """Sıcak krem zemin, koyu mürekkep, altın saç teli. Fotoğraf altta
    çapa. Koyu panonun tam tersi: aydınlık, ferah, lüks broşür dili."""
    b = board()
    b.im = gradient((b.W, b.H), [(0.0, (252, 249, 242)), (0.55, CREAM),
                                 (1.0, (238, 229, 214))], angle=0.3)

    bandtop, bandh = 1290, 450
    bh = b.p(bandh)
    im = cover("night-gate", (b.W, bh), 0.5)
    b.im.alpha_composite(im, (0, b.p(bandtop)))
    bot = b.H - b.p(bandtop + bandh)
    if bot > 0:
        b.im.alpha_composite(_extend(b, im, bot, (round(bh * 0.90), bh), 0.34, True),
                             (0, b.p(bandtop + bandh)))
    veil(b, 1740, 2000, 40, 235)

    lg = lockup(b.p(240), white=False)
    b.im.alpha_composite(lg, (b.p(60), b.p(84)))

    dr = b.draw
    fe, spe = fit_track(b, dr, ["İZMİT MİA BÖLGESİ · 600 DAİRE"], b.p(560), 11, 0.30,
                        lambda s: b.sans(s, "700"))

    def eb(d):
        track(b, d, (b.p(60), b.p(370)), "İZMİT MİA BÖLGESİ · 600 DAİRE", fe,
              (*bs.MIA_DEEP, 255), spe)
    overlay(b, eb)
    orn(b, 60 + 90, 352, 90, GOLD, 255, 0.9, diamond=False)

    fh = fit(b, dr, ["Lüks artık", "ulaşılabilir."], b.p(680), 92,
             lambda s: b.serif(s, "600"))
    step = cap_h(fh) * 1.22

    def head(d):
        d.text((b.p(60), b.p(500)), "Lüks artık", font=fh, fill=INKD, anchor="ls")
        d.text((b.p(60), b.p(500) + step), "ulaşılabilir.", font=fh, fill=INKD,
               anchor="ls")
    overlay(b, head)

    fb = b.sans(16, "400")

    def body(d):
        for i, ln in enumerate(wrap(d, "Avantajlı peşinatla başlarsınız, kalanı "
                                       "60 aya kadar sabit taksitlerle ödersiniz. "
                                       "Banka yok, faiz yok, kefil yok.",
                                    fb, b.p(600))):
            d.text((b.p(60), b.p(690 + i * 26)), ln, font=fb, fill=(74, 84, 100),
                   anchor="ls")
    overlay(b, body)

    # Daire listesi — krem zeminde altın çizgilerle
    y = 810
    ft = fit(b, dr, [u[0] for u in UNITS], b.p(150), 30, lambda s: b.serif(s, "700"))
    fn, spn = fit_track(b, dr, [u[1].upper() for u in UNITS], b.p(330), 9, 0.16,
                        lambda s: b.sans(s, "700"))
    fc, spc = fit_track(b, dr, [f"{u[3]} DAİRE · {u[2]}" for u in UNITS], b.p(250),
                        9, 0.16, lambda s: b.sans(s, "700"))
    for i, (typ, name, area, count) in enumerate(UNITS):
        yy = y + i * 84

        def r(d, yy=yy, typ=typ, name=name, area=area, count=count):
            d.line([b.p(60), b.p(yy - 34), b.p(740), b.p(yy - 34)],
                   fill=(*GOLD, 150), width=max(1, b.p(0.5)))
            d.text((b.p(60), b.p(yy)), typ, font=ft, fill=INKD, anchor="ls")
            track(b, d, (b.p(190), b.p(yy - 12)), name.upper(), fn, (90, 100, 116), spn)
            track(b, d, (b.p(740), b.p(yy - 12)), f"{count} DAİRE · {area}", fc,
                  (*bs.MIA_DEEP, 245), spc, "ra")
        overlay(b, r)

    def last(d):
        d.line([b.p(60), b.p(y + 4 * 84 - 34), b.p(740), b.p(y + 4 * 84 - 34)],
               fill=(*GOLD, 150), width=max(1, b.p(0.5)))
    overlay(b, last)

    fq, spq = fit_track(b, dr, ["VADE FARKSIZ 60 AY · %0 FAİZ"], b.p(560), 13, 0.26,
                        lambda s: b.sans(s, "700"))

    def tag(d):
        track(b, d, (b.p(60), b.p(1180)), "VADE FARKSIZ 60 AY · %0 FAİZ", fq,
              (*bs.MIA_DEEP, 255), spq)
    overlay(b, tag)

    # künye — fotoğrafın koyu altında
    qs = b.p(44)
    qx, qy = b.W - b.p(60) - qs, b.p(1858)

    def plate(d):
        d.rounded_rectangle([qx - b.p(4), qy - b.p(4), qx + qs + b.p(4), qy + qs + b.p(4)],
                            radius=b.p(3), fill=(255, 255, 255, 250))
    overlay(b, plate)
    b.im.alpha_composite(qr_image(QR_URL, qs, (14, 22, 38)), (qx, qy))
    fi, spi = fit_track(b, dr, [f"{SELLER} · {SELLER_ROLE}"], b.p(340), 7.4, 0.16,
                        lambda s: b.sans(s, "700"))

    def foot(d):
        d.text((b.p(60), b.p(1888)), SITE, font=b.serif(23, "600"), fill=WHITE,
               anchor="ls")
        d.text((b.p(60), b.p(1922)), "  ·  ".join(PHONES), font=b.sans(12.5, "700"),
               fill=(*GOLD, 255), anchor="ls")
        track(b, d, (b.p(60), b.p(1932)), f"{SELLER} · {SELLER_ROLE}", fi,
              (228, 220, 206, 230), spi)
    overlay(b, foot)
    return b.im.convert("RGB")


# ==================================================================== C · CAM
def yon_c() -> Image.Image:
    """Tam sayfa render üstünde buzlu cam panel; manşet sans, geniş
    harf aralığıyla. En çağdaş dil."""
    b = board()
    photo_full(b, "night-gate", 1140, 560, 0.5, warm=1.04)
    veil(b, 0, 400, 150, 30)
    veil(b, 1500, 2000, 0, 215)

    # Buzlu cam panel
    px0, py0, px1, py1 = b.p(56), b.p(300), b.W - b.p(56), b.p(1180)
    region = b.im.crop((px0, py0, px1, py1)).filter(
        ImageFilter.GaussianBlur(b.p(9)))
    region = ImageEnhance.Brightness(region.convert("RGB")).enhance(0.66)
    glass = Image.new("RGBA", (px1 - px0, py1 - py0), (10, 20, 36, 150))
    region = region.convert("RGBA")
    region.alpha_composite(glass)
    mask = Image.new("L", region.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, region.width - 1, region.height - 1],
                                           radius=b.p(8), fill=255)
    region.putalpha(mask)
    b.im.alpha_composite(region, (px0, py0))

    def frame(d):
        d.rounded_rectangle([px0, py0, px1, py1], radius=b.p(8),
                            outline=(*GOLD, 200), width=max(2, b.p(0.9)))
    overlay(b, frame)

    lg = lockup(b.p(250), white=True)
    b.im.alpha_composite(lg, ((b.W - lg.width) // 2, b.p(96)))

    dr = b.draw
    cx = W_MM / 2
    fe, spe = fit_track(b, dr, ["İZMİT MİA BÖLGESİ"], b.p(500), 11, 0.36,
                        lambda s: b.sans(s, "700"))

    def eb(d):
        track(b, d, (b.p(cx), b.p(356)), "İZMİT MİA BÖLGESİ", fe, (*GOLD, 255),
              spe, "ma")
    overlay(b, eb)

    # Sans manşet — geniş aralık, üç satır
    lines = ["LÜKS", "ARTIK", "ULAŞILABİLİR"]
    fh, sph = fit_track(b, dr, lines, b.p(600), 62, 0.06, lambda s: b.sans(s, "700"))
    step = cap_h(fh) * 1.42

    def head(d):
        for i, ln in enumerate(lines):
            track(b, d, (b.p(cx), b.p(440) + i * step), ln, fh, (*WHITE, 252),
                  sph, "ma")
    overlay(b, head)

    orn(b, cx, 700, 130)

    fs = b.sans(15.5, "400")

    def sub(d):
        d.text((b.p(cx), b.p(752)), "Avantajlı peşinat · vade farksız 60 ay",
               font=fs, fill=(232, 240, 246, 250), anchor="ms")
        d.text((b.p(cx), b.p(780)), "Banka yok · faiz yok · kefil yok",
               font=fs, fill=(232, 240, 246, 250), anchor="ms")
    overlay(b, sub)

    stepu = 688 / 4
    fa, spa = fit_track(b, dr, [f"{u[3]}" for u in UNITS], b.p(140), 22, 0.06,
                        lambda s: b.serif(s, "700"))
    fn, spn = fit_track(b, dr, [u[0] for u in UNITS], b.p(140), 9, 0.16,
                        lambda s: b.sans(s, "700"))

    def units(d):
        d.line([px0 + b.p(26), b.p(846), px1 - b.p(26), b.p(846)],
               fill=(*GOLD, 150), width=max(1, b.p(0.5)))
        for i, (typ, name, area, count) in enumerate(UNITS):
            ux = b.p(56 + 26 + stepu * (i + 0.5)) - b.p(6)
            track(b, d, (ux, b.p(900)), str(count), fa, (*WHITE, 252), spa, "ma")
            track(b, d, (ux, b.p(936)), typ, fn, (*GOLD, 252), spn, "ma")
            track(b, d, (ux, b.p(952)), area, fn, (216, 228, 238, 230), spn, "ma")
    overlay(b, units)

    def bottom(d):
        d.line([px0 + b.p(26), b.p(1000), px1 - b.p(26), b.p(1000)],
               fill=(*GOLD, 150), width=max(1, b.p(0.5)))
    overlay(b, bottom)

    items = [("rozet", "YÜKSEK KALİTE"), ("kalkan", "GÜVENLİ YATIRIM"),
             ("takvim", "60 AY VADE")]
    stepi = 688 / 3
    fi, spi = fit_track(b, dr, [t for _, t in items], b.p(stepi - 20), 8.6, 0.16,
                        lambda s: b.sans(s, "700"))

    def icons(d):
        for i, (kind, t) in enumerate(items):
            ix = b.p(56 + 26 + stepi * (i + 0.5)) - b.p(6)
            icon(d, kind, ix, b.p(1058), b.p(13), (*GOLD, 255), max(2, b.p(1.0)))
            track(b, d, (ix, b.p(1096)), t, fi, (*WHITE, 246), spi, "ma")
    overlay(b, icons)

    foot_a(b)
    return b.im.convert("RGB")


YONLER = [("yon-A-referans", yon_a, "A · referans dili"),
          ("yon-B-krem", yon_b, "B · krem / aydınlık"),
          ("yon-C-cam", yon_c, "C · cam panel / sans")]


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(PREVIEW, exist_ok=True)
    for name, fn, label in YONLER:
        im = fn()
        p = os.path.join(OUT, f"{name}.jpg")
        im.save(p, "JPEG", quality=94, subsampling=0, optimize=True, dpi=(DPI, DPI))
        small = im.copy()
        small.thumbnail((1400, 1400), Image.LANCZOS)
        small.save(os.path.join(PREVIEW, f"{name}.jpg"), "JPEG", quality=88,
                   optimize=True)
        print(f"  {name:<22} {label:<24} {os.path.getsize(p)/1e6:.1f} MB")
    print(f"\n  → {OUT}")


if __name__ == "__main__":
    main()
