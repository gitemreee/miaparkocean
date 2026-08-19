#!/usr/bin/env python3
"""
MİA PARK OCEAN — roll-up serisi (5 tasarım).

Verilen beş emlak referansının ortak dili:

  · BİNA TEK BAŞINA KAHRAMAN. Fotoğraf ızgarası, ikon listesi, kolaj yok.
  · Cam hap rozetler taşıyor sayıları — ödeme planı, peşinat, m².
  · Bölmeli bilgi şeridi: dikey çizgiyle ayrılmış üç olgu.
  · İnce tipografi, geniş harf aralığı, az renk, çok boşluk.

    1 · cam-panel   gece render üstünde büyük cam panel      (mavi)
    2 · kunye       gökyüzü üstte, bina altta, bölmeli şerit  (mavi)
    3 · rozet       cam haplar + mesafe ikonları              (mavi)
    4 · beyaz-plan  segment hap + binadan çıkan etiketler     (beyaz)
    5 · beyaz-baslik iki tonlu manşet + yuvarlak ikon hapları (beyaz)

ŞOK ROZETİ hepsinde: 699.000 ₺ peşinat, banka/kredi/faiz yok.

DAİRELER: 1+0, 1+1 ve 1+1 Bahçe Loft. 2+1 gösterilmiyor.

Ölçü: 800 x 2000 mm, 1:1 ölçekte 100 dpi. Kaset alt 40 mm'yi yutar.

    python scripts/build-rollup.py
    python scripts/build-rollup.py cam-panel      # tek tasarım
"""

from __future__ import annotations

import importlib.util
import math
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
qr_image, lockup, crisp = bs.qr_image, bs.lockup, bs.crisp

OUT = os.path.join(ROOT, "tabela", "rollup")
PREVIEW = os.path.join(OUT, "onizleme")
SRC_OUT = os.path.join(OUT, "kaynak")

W_MM, H_MM, DPI = 800, 2000, 100
M = 56

WHITE = (255, 255, 255)
NAVY_DEEP = (5, 18, 30)
NAVY = (8, 32, 50)
NAVY_MID = (14, 54, 80)
ICE = (221, 247, 250)
AQUA = (126, 196, 214)
GOLD = (200, 168, 108)
PAPER = (248, 246, 241)
INK = (26, 32, 40)
GREY = (122, 130, 140)
LINE_L = (222, 218, 211)

SITE, PHONES = bs.SITE, bs.PHONES
SELLER, SELLER_ROLE = bs.SELLER, bs.SELLER_ROLE
QR_URL = "https://miaparkocean.com/?utm_source=rollup"

UNITS = [("1+0", "28 m²", 472), ("1+1", "50 m²", 96), ("1+1 Loft", "50 m²", 16)]
PESIN = "699.000"
SHOCK = ["699.000 ₺", "PEŞİNATLA", "EV SAHİBİ OLUN"]
SHOCK_SUB = ["BANKA YOK", "KREDİ YOK", "FAİZ YOK"]


def board(light: bool = False) -> Board:
    b = Board(W_MM, H_MM, DPI)
    if light:
        b.im = Image.new("RGBA", (b.W, b.H), (*PAPER, 255))
    return b


def cap_h(f) -> float:
    bb = f.getbbox("H")
    return bb[3] - bb[1]


def cap_top(f, cy: float) -> float:
    bb = f.getbbox("H")
    return cy - (bb[1] + bb[3]) / 2


def ocean_logo(b: Board, w_mm: float, white: bool = False) -> Image.Image:
    """OCEAN GAYRİMENKUL. Beyaz sürüm markanın kendi varyantı — boyama yok."""
    name = "ocean-logo-white.png" if white else "ocean-logo.webp"
    im = Image.open(os.path.join(ROOT, "public", name)).convert("RGBA")
    if not white:
        a = np.asarray(im.convert("RGB"), np.float32)
        alpha = 255 - a.min(axis=2)
        im = Image.merge("RGBA", (*im.convert("RGB").split(),
                                  Image.fromarray(alpha.astype(np.uint8), "L")))
    box = im.getbbox()
    if box:
        im = im.crop(box)
    return crisp(im, b.p(w_mm))


# ------------------------------------------------------------------ zemin
def full_render(b: Board, name: str, band_top: float = None, focus: float = 0.5,
                warm: float = 1.0, stops=None) -> None:
    """Bina tek başına kahraman: render tam sayfa, üstünde ince perde.

    Yatay render dikey panoya tam girmiyor; kare doğal en-boyunda bant
    olarak konup gökyüzü yukarı, zemin aşağı uzatılıyor. İnce şeridi
    doğrudan esnetmek bulutu dikey çizgiye çeviriyordu — uzatma
    örneklenen renkten gradyan kurup kaynağı ağır bulanıklıkla bindiriyor.
    """
    bh = round(W_MM * 2304 / 4096)
    top = round((H_MM - bh) * 0.62) if band_top is None else band_top
    im = cover(name, (b.W, b.p(bh)), focus)
    if warm != 1.0:
        im = ImageEnhance.Color(im.convert("RGB")).enhance(warm).convert("RGBA")

    def ext(h, y0, y1, dark, flip):
        a = np.asarray(im.convert("RGB"), np.float32)
        c_e = tuple(a[y0:y0 + max(2, (y1 - y0) // 8)].mean(axis=(0, 1)))
        c_f = tuple(a[y1 - max(2, (y1 - y0) // 8):y1].mean(axis=(0, 1)))
        st = ([(0.0, tuple(c * dark for c in c_f)), (0.62, c_f), (1.0, c_e)]
              if not flip else
              [(0.0, c_e), (0.45, c_f), (1.0, tuple(c * dark for c in c_f))])
        lay = gradient((b.W, h), st, angle=0.0)
        tex = im.crop((0, y0, b.W, y1)).resize((b.W, h), Image.LANCZOS)
        tex = tex.filter(ImageFilter.GaussianBlur(max(4, h // 9)))
        tex.putalpha(150)
        lay.alpha_composite(tex)
        return lay

    tp = b.p(top)
    if tp > 0:
        b.im.alpha_composite(ext(tp, 0, round(b.p(bh) * 0.26), 0.40, False), (0, 0))
    b.im.alpha_composite(im, (0, tp))
    bot = b.H - tp - b.p(bh)
    if bot > 0:
        b.im.alpha_composite(
            ext(bot, round(b.p(bh) * 0.90), b.p(bh), 0.34, True), (0, tp + b.p(bh)))

    b.im.alpha_composite(scrim((b.W, b.H), stops or [
        (0.0, (*NAVY_DEEP, 215)), (0.30, (*NAVY_DEEP, 120)),
        (0.60, (*NAVY_DEEP, 95)), (1.0, (*NAVY_DEEP, 225)),
    ]), (0, 0))


# ------------------------------------------------------------------ parçalar
def glass(b: Board, x0, y0, x1, y1, r: float = 14, tint=(255, 255, 255),
          a: int = 14, blur: float = 1.6, border: int = 90) -> None:
    """Buzlu cam panel — referansların taşıyıcı yüzeyi."""
    X0, Y0, X1, Y1 = b.p(x0), b.p(y0), b.p(x1), b.p(y1)
    reg = b.im.crop((X0, Y0, X1, Y1)).filter(ImageFilter.GaussianBlur(b.p(blur)))
    lay = Image.new("RGBA", reg.size, (*tint, a))
    reg = reg.convert("RGBA")
    reg.alpha_composite(lay)
    mask = Image.new("L", reg.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, reg.width - 1, reg.height - 1],
                                           radius=b.p(r), fill=255)
    reg.putalpha(mask)
    b.im.alpha_composite(reg, (X0, Y0))

    def edge(d):
        d.rounded_rectangle([X0, Y0, X1, Y1], radius=b.p(r),
                            outline=(255, 255, 255, border), width=max(2, b.p(0.7)))
    overlay(b, edge)


def pill(b: Board, cx, cy, w, h, text: str, fill, ink, size: float = 13,
         sp_ratio: float = 0.08, r: float = None, outline=None) -> None:
    """Yuvarlak uçlu rozet — referanslardaki '15% ONLY' hapı."""
    X0, Y0 = b.p(cx - w / 2), b.p(cy - h / 2)
    X1, Y1 = b.p(cx + w / 2), b.p(cy + h / 2)
    rad = b.p(r if r is not None else h / 2)
    f, sp = fit_track(b, b.draw, [text], b.p(w - 18), size, sp_ratio,
                      lambda s: b.sans(s, "700"))

    def paint(d):
        d.rounded_rectangle([X0, Y0, X1, Y1], radius=rad, fill=fill,
                            outline=outline, width=max(2, b.p(0.7)) if outline else 0)
        track(b, d, ((X0 + X1) / 2, cap_top(f, (Y0 + Y1) / 2)), text, f, ink, sp, "ma")
    overlay(b, paint)


def stat_row(b: Board, y: float, items, ink=WHITE, sub=None, x0=None, x1=None,
             big: float = 21, small: float = 8.6) -> None:
    """Dikey çizgiyle ayrılmış üç olgu — referans 2'nin künye şeridi."""
    x0 = M if x0 is None else x0
    x1 = W_MM - M if x1 is None else x1
    sub = sub or (AQUA if ink == WHITE else GREY)
    n = len(items)
    step = (x1 - x0) / n
    dr = b.draw
    fb, spb = fit_track(b, dr, [a for a, _ in items], b.p(step - 26), big, 0.06,
                        lambda s: b.sans(s, "700"))
    fs, sps = fit_track(b, dr, [c for _, c in items], b.p(step - 20), small, 0.24,
                        lambda s: b.sans(s, "700"))

    def paint(d):
        for i, (a, c) in enumerate(items):
            cx = b.p(x0 + step * (i + 0.5))
            track(b, d, (cx, b.p(y)), a, fb, ink, spb, "ma")
            track(b, d, (cx, b.p(y) + cap_h(fb) * 1.85), c, fs, (*sub, 250), sps, "ma")
            if i:
                xv = b.p(x0 + step * i)
                d.line([xv, b.p(y) - cap_h(fb) * 0.3, xv, b.p(y) + cap_h(fb) * 2.9],
                       fill=(*sub, 130), width=max(1, b.p(0.5)))
    overlay(b, paint)


def shock(b: Board, cx: float, cy: float, r: float, lines, subs,
          fill=GOLD, ink=NAVY_DEEP, teeth: int = 34) -> None:
    """Şok rozeti. Diş çok ve ince: az dişli yıldız 'yıldız' okunuyor,
    otuz dört diş klasik şok etiketini veriyor."""
    pts = []
    for i in range(teeth * 2):
        rad = b.p(r) if i % 2 == 0 else b.p(r * 0.925)
        a = math.pi * 2 * i / (teeth * 2) - math.pi / 2
        pts.append((b.p(cx) + rad * math.cos(a), b.p(cy) + rad * math.sin(a)))

    dr = b.draw
    f1, sp1 = fit_track(b, dr, [lines[0]], b.p(r * 1.5), 26, 0.02,
                        lambda s: b.serif(s, "700"))
    f2, sp2 = fit_track(b, dr, lines[1:], b.p(r * 1.42), 11, 0.10,
                        lambda s: b.sans(s, "700"))
    f3, sp3 = fit_track(b, dr, subs, b.p(r * 1.30), 8.6, 0.10,
                        lambda s: b.sans(s, "700"))

    def paint(d):
        d.polygon(pts, fill=(*fill, 255))
        d.ellipse([b.p(cx - r * 0.86), b.p(cy - r * 0.86),
                   b.p(cx + r * 0.86), b.p(cy + r * 0.86)],
                  outline=(*ink, 80), width=max(1, b.p(0.6)))
        y = b.p(cy) - cap_h(f1) * 1.55
        track(b, d, (b.p(cx), y), lines[0], f1, ink, sp1, "ma")
        y += cap_h(f1) * 1.45
        for t in lines[1:]:
            track(b, d, (b.p(cx), y), t, f2, ink, sp2, "ma")
            y += cap_h(f2) * 1.75
        y += cap_h(f3) * 0.5
        d.line([b.p(cx - r * 0.44), y, b.p(cx + r * 0.44), y], fill=(*ink, 110),
               width=max(1, b.p(0.5)))
        y += cap_h(f3) * 1.5
        track(b, d, (b.p(cx), y), " · ".join(subs), f3, ink, sp3, "ma")
    overlay(b, paint)


def unit_chips(b: Board, y: float, ink=WHITE, box=True, size: float = 17) -> None:
    """[1+0] [1+1] [1+1 LOFT] — referans 2'nin kutulu rakamları."""
    dr = b.draw
    labels = [u[0] for u in UNITS]
    f, sp = fit_track(b, dr, labels, b.p(150), size, 0.06, lambda s: b.sans(s, "700"))
    ws = [sum(dr.textlength(c, font=f) for c in t) + sp * (len(t) - 1) for t in labels]
    pad = b.p(13)
    gap = b.p(9)
    total = sum(w + pad * 2 for w in ws) + gap * (len(labels) - 1)
    x = b.p(W_MM / 2) - total / 2
    h = cap_h(f) + pad * 1.7

    def paint(d):
        nonlocal x
        for t, w in zip(labels, ws):
            if box:
                d.rounded_rectangle([x, b.p(y), x + w + pad * 2, b.p(y) + h],
                                    radius=b.p(2.5), outline=(*ink, 150),
                                    width=max(1, b.p(0.6)))
            track(b, d, (x + pad + w / 2, cap_top(f, b.p(y) + h / 2)), t, f,
                  (*ink, 255), sp, "ma")
            x += w + pad * 2 + gap
    overlay(b, paint)


def pin_pill(b: Board, cy: float, text: str, w: float = 400, h: float = 34,
             ink=WHITE, outline=(255, 255, 255, 120)) -> None:
    cx = W_MM / 2
    X0, Y0 = b.p(cx - w / 2), b.p(cy - h / 2)
    X1, Y1 = b.p(cx + w / 2), b.p(cy + h / 2)
    f, sp = fit_track(b, b.draw, [text], b.p(w - 70), 11, 0.18,
                      lambda s: b.sans(s, "700"))

    def paint(d):
        d.rounded_rectangle([X0, Y0, X1, Y1], radius=b.p(h / 2), outline=outline,
                            width=max(2, b.p(0.7)))
        px, py, r = X0 + b.p(20), (Y0 + Y1) / 2, b.p(6)
        d.ellipse([px - r * .7, py - r, px + r * .7, py + r * .3], outline=(*ink, 255),
                  width=max(2, b.p(0.7)))
        d.polygon([(px - r * .34, py + r * .16), (px + r * .34, py + r * .16),
                   (px, py + r * 1.0)], fill=(*ink, 255))
        d.line([X0 + b.p(36), Y0 + b.p(7), X0 + b.p(36), Y1 - b.p(7)],
               fill=(*ink, 110), width=max(1, b.p(0.5)))
        track(b, d, ((X0 + X1) / 2 + b.p(14), cap_top(f, (Y0 + Y1) / 2)), text, f,
              (*ink, 250), sp, "ma")
    overlay(b, paint)


def dual_logo(b: Board, y: float, w1: float = 190, w2: float = 104,
              white: bool = True, gap: float = 30) -> None:
    """MİA kilidi | OCEAN — referans 1'in ikili logo satırı, arada çizgi.

    Ocean'ın BEYAZ SÜRÜMÜ markanın kendi varyantı; renklendirme yok.
    """
    lg = lockup(b.p(w1), white=white)
    oc = ocean_logo(b, w2, white=white)
    h = max(lg.height, oc.height)
    total = lg.width + b.p(gap) * 2 + oc.width
    x = b.p(W_MM / 2) - total // 2
    b.im.alpha_composite(lg, (x, b.p(y) + (h - lg.height) // 2))
    b.im.alpha_composite(oc, (x + lg.width + b.p(gap) * 2,
                              b.p(y) + (h - oc.height) // 2))

    ink = (255, 255, 255, 120) if white else (*GREY, 150)

    def rule(d):
        xr = x + lg.width + b.p(gap)
        d.line([xr, b.p(y) + h * 0.16, xr, b.p(y) + h * 0.84], fill=ink,
               width=max(1, b.p(0.6)))
    overlay(b, rule)


def contact_line(b: Board, y: float, ink=WHITE, sub=None, qr_dark=NAVY_DEEP,
                 qr: bool = True) -> None:
    """Alt iletişim satırı — tek çizgi, kalabalık yok."""
    sub = sub or (AQUA if ink == WHITE else GREY)
    dr = b.draw

    def rule(d):
        d.line([b.p(M), b.p(y - 34), b.p(W_MM - M), b.p(y - 34)],
               fill=(*sub, 120), width=max(1, b.p(0.5)))
    overlay(b, rule)

    if qr:
        qs = b.p(52)
        qx, qy = b.p(W_MM - M) - qs, b.p(y - 14)

        def plate(d):
            d.rounded_rectangle([qx - b.p(5), qy - b.p(5), qx + qs + b.p(5),
                                 qy + qs + b.p(5)], radius=b.p(4),
                                fill=(255, 255, 255, 252))
        overlay(b, plate)
        b.im.alpha_composite(qr_image(QR_URL, qs, qr_dark), (qx, qy))

    f, sp = fit_track(b, dr, [f"{SELLER} · {SELLER_ROLE}"], b.p(380), 7.4, 0.16,
                      lambda s: b.sans(s, "700"))

    def paint(d):
        d.text((b.p(M), b.p(y + 14)), SITE, font=b.serif(22, "600"), fill=(*ink, 255),
               anchor="ls")
        d.text((b.p(M), b.p(y + 44)), "  ·  ".join(PHONES), font=b.sans(13, "700"),
               fill=(*ink, 255), anchor="ls")
        track(b, d, (b.p(M), b.p(y + 54)), f"{SELLER} · {SELLER_ROLE}", f,
              (*sub, 235), sp)
    overlay(b, paint)


# ============================================================ 1 · CAM PANEL
def ru_cam_panel() -> Image.Image:
    b = board()
    full_render(b, "night-gate", 520, 0.5, 1.04, stops=[
        (0.0, (*NAVY_DEEP, 200)), (0.34, (*NAVY_DEEP, 110)),
        (0.62, (*NAVY_DEEP, 105)), (1.0, (*NAVY_DEEP, 232)),
    ])
    # Panel binayı GÖSTERMELİ, örtmemeli: hafif bulanıklık ve ince perde.
    glass(b, M, 150, W_MM - M, 1560, r=18, a=13, blur=1.5, border=100)

    dual_logo(b, 206, 186, 100, white=True)

    dr = b.draw
    fh = fit(b, dr, ["1+0, 1+1 ve Loft"], b.p(600), 46, lambda s: b.serif(s, "600"))
    fs = fit(b, dr, ["Daireler satışta"], b.p(560), 30, lambda s: b.serif(s, "500"))

    def head(d):
        d.text((b.p(W_MM / 2), b.p(1132)), "1+0, 1+1 ve Loft", font=fh, fill=WHITE,
               anchor="ms")
        d.text((b.p(W_MM / 2), b.p(1182)), "Daireler satışta", font=fs,
               fill=(*ICE, 245), anchor="ms")
        d.line([b.p(180), b.p(1208), b.p(W_MM - 180), b.p(1208)],
               fill=(255, 255, 255, 130), width=max(1, b.p(0.5)))
    overlay(b, head)

    fq, spq = fit_track(b, dr, ["BUGÜN YERİNİZİ AYIRIN, FİYATI SABİTLEYİN"],
                        b.p(560), 10.5, 0.20, lambda s: b.sans(s, "700"))

    def note(d):
        track(b, d, (b.p(W_MM / 2), b.p(1234)),
              "BUGÜN YERİNİZİ AYIRIN, FİYATI SABİTLEYİN", fq, (*ICE, 235), spq, "ma")
    overlay(b, note)

    stat_row(b, 1310, [(f"{PESIN} ₺", "PEŞİNAT"), ("60 AY", "VADE FARKSIZ"),
                       ("%0", "FAİZ")], x0=110, x1=W_MM - 110)

    pin_pill(b, 1470, "İZMİT MİA BÖLGESİ · KOCAELİ", 380, 36)

    shock(b, 640, 1618, 118, SHOCK, SHOCK_SUB)
    contact_line(b, 1830)
    return b.im.convert("RGB")


# ============================================================ 2 · KÜNYE
def ru_kunye() -> Image.Image:
    b = board()
    full_render(b, "entrance-gate", 1150, 0.46, 1.0, stops=[
        (0.0, (*NAVY_DEEP, 248)), (0.34, (*NAVY_DEEP, 240)),
        (0.57, (*NAVY_DEEP, 100)), (0.79, (*NAVY_DEEP, 70)),
        (0.815, (*NAVY_DEEP, 246)), (1.0, (*NAVY_DEEP, 253)),
    ])

    lg = lockup(b.p(168), white=True)
    b.im.alpha_composite(lg, (b.p(M), b.p(70)))
    oc = ocean_logo(b, 96, white=True)
    b.im.alpha_composite(oc, (b.p(W_MM - M) - oc.width, b.p(94)))

    dr = b.draw
    fh = fit(b, dr, ["MİA PARK OCEAN"], b.p(660), 52, lambda s: b.serif(s, "600"))

    def head(d):
        d.text((b.p(W_MM / 2), b.p(330)), "MİA PARK OCEAN", font=fh, fill=WHITE,
               anchor="ms")
    overlay(b, head)

    unit_chips(b, 372, WHITE, True, 18)

    fsub, spsub = fit_track(b, dr, ["DAİRE SEÇENEKLERİ"], b.p(400), 10.5, 0.28,
                            lambda s: b.sans(s, "700"))

    def sub(d):
        track(b, d, (b.p(W_MM / 2), b.p(452)), "DAİRE SEÇENEKLERİ", fsub,
              (*AQUA, 250), spsub, "ma")
    overlay(b, sub)

    stat_row(b, 526, [(f"{PESIN} ₺", "PEŞİNAT"), ("60 AY", "VADE FARKSIZ"),
                      ("%0", "FAİZ")], x0=90, x1=W_MM - 90)

    pin_pill(b, 686, "İZMİT MİA BÖLGESİ · KOCAELİ", 380, 36)
    shock(b, 620, 880, 116, SHOCK, SHOCK_SUB)
    contact_line(b, 1830)
    return b.im.convert("RGB")


# ============================================================ 3 · ROZET
def ru_rozet() -> Image.Image:
    b = board()
    full_render(b, "aerial-pools", 820, 0.5, 1.02, stops=[
        (0.0, (*NAVY_DEEP, 238)), (0.30, (*NAVY_DEEP, 212)),
        (0.42, (*NAVY_DEEP, 92)), (0.63, (*NAVY_DEEP, 82)),
        (0.645, (*NAVY_DEEP, 246)), (1.0, (*NAVY_DEEP, 253)),
    ])

    dual_logo(b, 84, 176, 96, white=True)

    dr = b.draw
    fh, sph = fit_track(b, dr, ["DENİZE İKİ DAKİKA"], b.p(680), 40, 0.04,
                        lambda s: b.sans(s, "700"))
    fi = fit(b, dr, ["İzmit MİA Bölgesi'nde yeni yaşam"], b.p(600), 22,
             lambda s: b.serif(s, "500"))

    def head(d):
        track(b, d, (b.p(W_MM / 2), b.p(300)), "DENİZE İKİ DAKİKA", fh, WHITE,
              sph, "ma")
        d.text((b.p(W_MM / 2), b.p(374)), "İzmit MİA Bölgesi'nde yeni yaşam",
               font=fi, fill=(*ICE, 245), anchor="ms")
    overlay(b, head)

    pill(b, 232, 452, 300, 58, f"PEŞİNAT  {PESIN} ₺", (255, 255, 255, 32),
         WHITE, 15, 0.06, outline=(255, 255, 255, 120))
    pill(b, 568, 452, 300, 58, "VADE  60 AY · %0 FAİZ", (255, 255, 255, 32),
         WHITE, 15, 0.06, outline=(255, 255, 255, 120))
    pill(b, W_MM / 2, 524, 300, 50, "1+0 · 1+1 · 1+1 LOFT", (255, 255, 255, 32),
         WHITE, 13, 0.10, outline=(255, 255, 255, 120))

    stat_row(b, 1400, [("2 dk", "İZMİT SAHİLİ"), ("1 dk", "D100 KARAYOLU"),
                       ("5 dk", "ŞEHİR MERKEZİ")], x0=80, x1=W_MM - 80,
             big=26, small=8.4)

    shock(b, 636, 1248, 108, SHOCK, SHOCK_SUB)
    pin_pill(b, 1580, "İZMİT MİA BÖLGESİ · KOCAELİ", 380, 36)
    contact_line(b, 1830)
    return b.im.convert("RGB")


# ============================================================ 4 · BEYAZ PLAN
def ru_beyaz_plan() -> Image.Image:
    """Referans 4: açık zemin, segment hap, bina ve mesafe şeridi."""
    b = board(light=True)
    b.im = gradient((b.W, b.H), [(0.0, (252, 251, 249)), (0.5, PAPER),
                                 (1.0, (238, 236, 231))], angle=0.3)

    bh = round(W_MM * 2304 / 4096)
    top = 590
    im = cover("entrance-gate", (b.W, b.p(bh)), 0.46)
    b.im.alpha_composite(im, (0, b.p(top)))
    b.im.alpha_composite(scrim((b.W, b.p(bh)), [
        (0.0, (*PAPER, 200)), (0.24, (*PAPER, 30)), (1.0, (*PAPER, 18)),
    ]), (0, b.p(top)))

    lg = lockup(b.p(196), white=False)
    b.im.alpha_composite(lg, ((b.W - lg.width) // 2, b.p(74)))

    dr = b.draw
    fh, sph = fit_track(b, dr, ["1+0, 1+1 ve 1+1 LOFT DAİRELER"], b.p(660), 20,
                        0.12, lambda s: b.sans(s, "700"))

    def head(d):
        track(b, d, (b.p(W_MM / 2), b.p(316)), "1+0, 1+1 ve 1+1 LOFT DAİRELER", fh,
              (*INK, 255), sph, "ma")
    overlay(b, head)

    segs = [("PEŞİNAT", f"{PESIN} ₺", WHITE, INK),
            ("VADE", "60 AY", INK, WHITE),
            ("FAİZ", "%0", WHITE, INK)]
    sw, sh, sy = 224, 76, 400
    x0 = (W_MM - sw * 3) / 2
    for i2, (lab, val, fillc, inkc) in enumerate(segs):
        cx = x0 + sw * (i2 + 0.5)
        X0, Y0 = b.p(cx - sw / 2), b.p(sy - sh / 2)
        X1, Y1 = b.p(cx + sw / 2), b.p(sy + sh / 2)
        rad = b.p(sh / 2)
        fl, spl = fit_track(b, dr, [lab], b.p(sw - 40), 8.6, 0.22,
                            lambda s: b.sans(s, "700"))
        fv = fit(b, dr, [val], b.p(sw - 34), 24, lambda s: b.serif(s, "700"))

        def seg(d, X0=X0, Y0=Y0, X1=X1, Y1=Y1, rad=rad, i2=i2, lab=lab, val=val,
                fillc=fillc, inkc=inkc, fl=fl, spl=spl, fv=fv):
            d.rounded_rectangle([X0, Y0, X1, Y1], radius=rad, fill=(*fillc, 255),
                                outline=(*LINE_L, 255) if fillc == WHITE else None,
                                width=max(1, b.p(0.6)) if fillc == WHITE else 0)
            if i2 == 1:
                d.rectangle([X0, Y0, X0 + rad, Y1], fill=(*fillc, 255))
                d.rectangle([X1 - rad, Y0, X1, Y1], fill=(*fillc, 255))
            track(b, d, ((X0 + X1) / 2, Y0 + b.p(15)), lab, fl, (*inkc, 220), spl, "ma")
            d.text(((X0 + X1) / 2, Y1 - b.p(16)), val, font=fv, fill=(*inkc, 255),
                   anchor="ms")
        overlay(b, seg)

    pill(b, W_MM / 2, 500, 340, 44, "TASARRUFA DAYALI FAİZSİZ FİNANSMAN",
         (255, 255, 255, 255), INK, 9.4, 0.18, outline=(*LINE_L, 255))

    stat_row(b, 1250, [("2 dk", "İZMİT SAHİLİ"), ("1 dk", "D100 KARAYOLU"),
                       ("5 dk", "ŞEHİR MERKEZİ")], ink=INK, sub=GREY,
             x0=M, x1=W_MM - M, big=26, small=8.4)

    shock(b, 648, 1022, 110, SHOCK, SHOCK_SUB, fill=GOLD, ink=INK)

    oc = ocean_logo(b, 128, white=False)
    b.im.alpha_composite(oc, ((b.W - oc.width) // 2, b.p(1560)))
    contact_line(b, 1830, ink=INK, sub=GREY, qr_dark=INK)
    return b.im.convert("RGB")


# ============================================================ 5 · BEYAZ BAŞLIK
def ru_beyaz_baslik() -> Image.Image:
    """Referans 5: iki tonlu manşet solda, yuvarlak ikon hapları sağda."""
    b = board(light=True)
    b.im = gradient((b.W, b.H), [(0.0, (253, 252, 250)), (0.55, PAPER),
                                 (1.0, (236, 233, 227))], angle=0.35)

    bh = round(W_MM * 2304 / 4096)
    im = cover("aerial-pools", (b.W, b.p(bh)), 0.5)
    b.im.alpha_composite(im, (0, b.p(730)))
    b.im.alpha_composite(scrim((b.W, b.p(bh)), [
        (0.0, (*PAPER, 205)), (0.30, (*PAPER, 30)), (1.0, (*PAPER, 22)),
    ]), (0, b.p(730)))

    dr = b.draw
    fh = fit(b, dr, ["MİA PARK", "OCEAN"], b.p(420), 62, lambda s: b.sans(s, "700"))
    step = cap_h(fh) * 1.24

    def head(d):
        d.text((b.p(M), b.p(196)), "MİA PARK", font=fh, fill=(*GOLD, 255), anchor="ls")
        d.text((b.p(M), b.p(196) + step), "OCEAN", font=fh, fill=(*INK, 255),
               anchor="ls")
    overlay(b, head)

    fb = b.sans(13, "400")

    def body(d):
        for i, ln in enumerate(wrap(d, "İzmit MİA Bölgesi'nde 1+0, 1+1 ve 1+1 Loft "
                                       "daireler. Tasarrufa dayalı faizsiz "
                                       "finansmanla.", fb, b.p(360))):
            d.text((b.p(M), b.p(330 + i * 24)), ln, font=fb, fill=(*GREY, 255),
                   anchor="ls")
    overlay(b, body)

    # Sağda yuvarlak ikonlu haplar
    items = [("PRESTİJLİ", "LOKASYON"), ("MODERN", "MİMARİ"),
             ("FAİZSİZ", "ÖDEME PLANI")]
    pw, ph2 = 300, 62
    px = W_MM - M - pw
    fl3, spl3 = fit_track(b, dr, [a for a, _ in items], b.p(pw - 90), 8, 0.20,
                          lambda s: b.sans(s, "700"))
    fv3, spv3 = fit_track(b, dr, [c for _, c in items], b.p(pw - 90), 12, 0.10,
                          lambda s: b.sans(s, "700"))

    def pills(d):
        for i, (a, c) in enumerate(items):
            y = 176 + i * 76
            d.rounded_rectangle([b.p(px), b.p(y), b.p(px + pw), b.p(y + ph2)],
                                radius=b.p(ph2 / 2), fill=(255, 255, 255, 255),
                                outline=(*LINE_L, 255), width=max(1, b.p(0.6)))
            cx, cy = b.p(px + 32), b.p(y + ph2 / 2)
            d.ellipse([cx - b.p(21), cy - b.p(21), cx + b.p(21), cy + b.p(21)],
                      fill=(*GOLD, 255))
            track(b, d, (b.p(px + 66), b.p(y + 16)), a, fl3, (*GREY, 255), spl3)
            track(b, d, (b.p(px + 66), b.p(y + 32)), c, fv3, (*INK, 255), spv3)
    overlay(b, pills)

    stat_row(b, 560, [(f"{PESIN} ₺", "PEŞİNAT"), ("60 AY", "VADE FARKSIZ"),
                      ("%0", "FAİZ")], ink=INK, sub=GREY, x0=M, x1=W_MM - M)

    unit_chips(b, 660, INK, True, 17)

    shock(b, 648, 1162, 108, SHOCK, SHOCK_SUB, fill=GOLD, ink=INK)

    stat_row(b, 1340, [("2 dk", "İZMİT SAHİLİ"), ("1 dk", "D100 KARAYOLU"),
                       ("5 dk", "ŞEHİR MERKEZİ")], ink=INK, sub=GREY,
             x0=M, x1=W_MM - M, big=26, small=8.4)

    oc = ocean_logo(b, 128, white=False)
    b.im.alpha_composite(oc, ((b.W - oc.width) // 2, b.p(1580)))
    contact_line(b, 1830, ink=INK, sub=GREY, qr_dark=INK)
    return b.im.convert("RGB")


DESIGNS = [
    ("rollup-1-cam-panel", ru_cam_panel, "mavi · cam panel"),
    ("rollup-2-kunye", ru_kunye, "mavi · künye şeridi"),
    ("rollup-3-rozet", ru_rozet, "mavi · cam rozetler"),
    ("rollup-4-beyaz-plan", ru_beyaz_plan, "beyaz · segment hap"),
    ("rollup-5-beyaz-baslik", ru_beyaz_baslik, "beyaz · iki tonlu başlık"),
]


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(PREVIEW, exist_ok=True)
    only = [a for a in sys.argv[1:] if not a.startswith("--")]
    for name, fn, label in DESIGNS:
        if only and not any(o in name for o in only):
            continue
        im = fn()
        p = os.path.join(OUT, f"{name}.jpg")
        im.save(p, "JPEG", quality=94, subsampling=0, optimize=True, dpi=(DPI, DPI))
        small = im.copy()
        small.thumbnail((1400, 1400), Image.LANCZOS)
        small.save(os.path.join(PREVIEW, f"{name}.jpg"), "JPEG", quality=88,
                   optimize=True)
        print(f"  {name:<24} {label:<26} {os.path.getsize(p)/1e6:.1f} MB")
    print(f"\n  → {OUT}")


def build_layers() -> None:
    os.makedirs(SRC_OUT, exist_ok=True)
    for name, fn, label in DESIGNS:
        bs._NO_TEXT = True
        bg = fn().convert("RGB")
        bs._NO_TEXT = False
        bp = os.path.join(SRC_OUT, f"{name}-zemin.jpg")
        bg.save(bp, "JPEG", quality=94, subsampling=0, optimize=True, dpi=(DPI, DPI))
        bg = Image.open(bp).convert("RGB")
        tam = Image.open(os.path.join(OUT, f"{name}.jpg")).convert("RGB")
        tp = os.path.join(SRC_OUT, f"{name}-yazi.png")
        bs._split(tam, bg).save(tp, optimize=True)
        print(f"  {name:<24} zemin {os.path.getsize(bp)/1e6:5.1f} MB · "
              f"yazı {os.path.getsize(tp)/1e6:5.1f} MB")
    print(f"\n  → {SRC_OUT}")


if __name__ == "__main__":
    if "--katman" in sys.argv:
        build_layers()
    else:
        main()
