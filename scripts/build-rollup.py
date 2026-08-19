#!/usr/bin/env python3
"""
MİA PARK OCEAN — roll-up.

TİPOGRAFİ KÜTÜPHANESİ
─────────────────────
Önceki sürümlerde elde yalnızca Fraunces ve Manrope vardı; iki yazı
tipiyle yapılan her tasarım birbirinin aynısı çıkıyordu. Kütüphane
genişletildi (hepsi açık lisanslı, Türkçe tam):

    Oswald       sıkışık grotesk — vurucu manşet
    Playfair     display serif — proje adı
    Cormorant    ince zarif serif
    Montserrat   geometrik sans — veri, etiket
    BarlowCond   sıkışık sans — küçük etiket
    Marcellus    rafine roman kapital
    Dancing      el yazısı vurgu

DERİNLİK
────────
Referanslardaki "tasarlanmış" his düz dikdörtgenden gelmiyor: binanın
arkasında hale, kenarlarda vinyet, bandın üstünde yumuşak geçiş,
rozetlerin altında gölge var. Hepsi burada kuruluyor.

Ölçü: 800 x 2000 mm, 1:1 ölçekte 100 dpi.

    python scripts/build-rollup.py
"""

from __future__ import annotations

import importlib.util
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

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
FONTS = bs.FONTS

OUT = os.path.join(ROOT, "tabela", "rollup")
PREVIEW = os.path.join(OUT, "onizleme")
SRC_OUT = os.path.join(OUT, "kaynak")

W_MM, H_MM, DPI = 800, 2000, 100
M = 58

WHITE = (255, 255, 255)
NIGHT = (6, 14, 26)
NAVY = (10, 26, 44)
SKY = (18, 44, 70)
ICE = (206, 228, 240)
SAND = (214, 186, 132)
SAND_HI = (240, 220, 176)

SITE, PHONES = bs.SITE, bs.PHONES
SELLER, SELLER_ROLE = bs.SELLER, bs.SELLER_ROLE
QR_URL = "https://miaparkocean.com/?utm_source=rollup"

UNITS = ["1+0", "1+1", "1+1 LOFT"]
PESIN = "699.000"

_FC = {}


class B(Board):
    """Board + yazı tipi kütüphanesi. Değişken eksenli fontlar ağırlık
    parametresiyle örnekleniyor; PIL nesneyi yerinde değiştirdiği için
    her (dosya, punto, ağırlık) üçlüsü ayrı önbellekleniyor."""

    def f(self, name: str, size_mm: float, w: int = None) -> ImageFont.FreeTypeFont:
        key = (name, round(size_mm, 3), w)
        if key not in _FC:
            ft = ImageFont.truetype(os.path.join(FONTS, name), self.p(size_mm))
            if w is not None:
                try:
                    ft.set_variation_by_axes([w])
                except Exception:
                    pass
            _FC[key] = ft
        return _FC[key]

    def oswald(self, s, w=600):      return self.f("Oswald-var.ttf", s, w)
    def playfair(self, s, w=700):    return self.f("Playfair-var.ttf", s, w)
    def cormorant(self, s, w=300):   return self.f("Cormorant-var.ttf", s, w)
    def mont(self, s, w=500):        return self.f("Montserrat-var.ttf", s, w)
    def cond(self, s, bold=True):
        return self.f("BarlowCond-700.ttf" if bold else "BarlowCond-500.ttf", s)
    def marcellus(self, s):          return self.f("Marcellus-400.ttf", s)
    def script(self, s, w=600):      return self.f("Dancing-var.ttf", s, w)


def board() -> B:
    return B(W_MM, H_MM, DPI)


def cap_h(f) -> float:
    bb = f.getbbox("H")
    return bb[3] - bb[1]


def cap_top(f, cy: float) -> float:
    bb = f.getbbox("H")
    return cy - (bb[1] + bb[3]) / 2


def ocean_logo(b: B, w_mm: float, white: bool = True) -> Image.Image:
    name = "ocean-logo-white.png" if white else "ocean-logo.webp"
    im = Image.open(os.path.join(ROOT, "public", name)).convert("RGBA")
    if not white:
        a = np.asarray(im.convert("RGB"), np.float32)
        im = Image.merge("RGBA", (*im.convert("RGB").split(),
                                  Image.fromarray((255 - a.min(axis=2)).astype(np.uint8), "L")))
    box = im.getbbox()
    return crisp(im.crop(box) if box else im, b.p(w_mm))


# ------------------------------------------------------------------ derinlik
def halo(b: B, cx: float, cy: float, rx: float, ry: float, color, strength: float,
         power: float = 2.0) -> None:
    """Binanın arkasındaki ışık halesi. Düz zemin ile render arasındaki
    geçişi yumuşatır; referanslardaki atmosfer bundan geliyor."""
    sw, sh = 700, round(700 * b.H / b.W)
    fx, fy = sw / b.W, sh / b.H
    yy, xx = np.mgrid[0:sh, 0:sw].astype(np.float32)
    d = np.sqrt(((xx - b.p(cx) * fx) / max(b.p(rx) * fx, 1)) ** 2 +
                ((yy - b.p(cy) * fy) / max(b.p(ry) * fy, 1)) ** 2)
    a = np.clip(1.0 - d, 0, 1) ** power * strength
    arr = np.zeros((sh, sw, 4), np.float32)
    for c in range(3):
        arr[:, :, c] = color[c]
    arr[:, :, 3] = a * 255
    b.im.alpha_composite(
        Image.fromarray(arr.astype(np.uint8), "RGBA").resize((b.W, b.H), Image.LANCZOS))


def vignette(b: B, strength: float = 0.42, power: float = 2.4) -> None:
    """Kenarları hafif karartır; göz merkeze toplanır."""
    sw, sh = 600, round(600 * b.H / b.W)
    yy, xx = np.mgrid[0:sh, 0:sw].astype(np.float32)
    nx = (xx / (sw - 1) - 0.5) * 2
    ny = (yy / (sh - 1) - 0.5) * 2
    d = np.sqrt(nx ** 2 * 1.0 + ny ** 2 * 0.62)
    a = np.clip(d - 0.42, 0, 1) ** power * strength
    arr = np.zeros((sh, sw, 4), np.float32)
    arr[:, :, 3] = a * 255
    b.im.alpha_composite(
        Image.fromarray(arr.astype(np.uint8), "RGBA").resize((b.W, b.H), Image.LANCZOS))


def band(b: B, name: str, top: float, h: float, focus: float = 0.5,
         feather: float = 90, bottom_fade: float = 0) -> None:
    """Render bandı, üst kenarı yumuşak geçişle zemine erir.

    Sert dikdörtgen kenar 'yapıştırılmış' duruyordu; kenar alfası
    yumuşatılınca bina zeminden çıkıyormuş gibi oturuyor.
    """
    ph = b.p(h)
    im = cover(name, (b.W, ph), focus)
    a = np.asarray(im.split()[3], np.float32)
    fp = min(b.p(feather), ph - 2)
    ramp = np.ones(ph, np.float32)
    ramp[:fp] = np.linspace(0, 1, fp) ** 1.35
    if bottom_fade:
        bp = min(b.p(bottom_fade), ph - fp - 2)
        ramp[ph - bp:] *= np.linspace(1, 0, bp) ** 1.2
    im.putalpha(Image.fromarray((a * ramp[:, None]).astype(np.uint8), "L"))
    b.im.alpha_composite(im, (0, b.p(top)))


def soft_shadow(b: B, draw_fn, blur: float = 5, alpha: float = 110,
                dy: float = 3) -> None:
    """Çizimin gölgesini önce basar. Rozet ve haplar zeminden kalkıyor."""
    lay = Image.new("RGBA", b.im.size, (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(lay))
    sh = lay.split()[3].point(lambda v: min(255, round(v * alpha / 255)))
    sh = sh.filter(ImageFilter.GaussianBlur(b.p(blur)))
    dark = Image.new("RGBA", b.im.size, (0, 0, 0, 0))
    dark.putalpha(sh)
    b.im.alpha_composite(dark, (0, b.p(dy)))
    b.im.alpha_composite(lay)


# ------------------------------------------------------------------ parçalar
def sky(b: B) -> None:
    """Gece göğü: derin lacivertten siyaha, ufukta hafif ısınma."""
    b.im = gradient((b.W, b.H), [
        (0.0, NIGHT), (0.24, NAVY), (0.48, SKY), (0.68, NAVY), (1.0, NIGHT),
    ], angle=0.12)


def head_logos(b: B, y: float = 84) -> None:
    lg = lockup(b.p(150), white=True)
    b.im.alpha_composite(lg, (b.p(M), b.p(y)))
    oc = ocean_logo(b, 88, white=True)
    b.im.alpha_composite(oc, (b.p(W_MM - M) - oc.width,
                              b.p(y) + (lg.height - oc.height) // 2))


def rule(b: B, y: float, x0: float = None, x1: float = None, col=WHITE,
         a: int = 70, w: float = 0.5) -> None:
    x0 = M if x0 is None else x0
    x1 = W_MM - M if x1 is None else x1

    def paint(d):
        d.line([b.p(x0), b.p(y), b.p(x1), b.p(y)], fill=(*col, a),
               width=max(1, b.p(w)))
    overlay(b, paint)


def chips(b: B, y: float, labels, ink=WHITE, size: float = 15) -> None:
    """[1+0] [1+1] [1+1 LOFT] — referans 2'nin kutulu tipleri."""
    dr = b.draw
    f = b.mont(size, 500)
    ws = [dr.textlength(t, font=f) for t in labels]
    pad, gap = b.p(15), b.p(10)
    h = cap_h(f) + pad * 1.8
    total = sum(w + pad * 2 for w in ws) + gap * (len(labels) - 1)
    x = b.p(W_MM / 2) - total / 2

    def paint(d):
        nonlocal x
        for t, w in zip(labels, ws):
            d.rounded_rectangle([x, b.p(y), x + w + pad * 2, b.p(y) + h],
                                radius=b.p(2), outline=(*ink, 130),
                                width=max(1, b.p(0.55)))
            d.text((x + pad + w / 2, cap_top(f, b.p(y) + h / 2)), t, font=f,
                   fill=(*ink, 245), anchor="ma")
            x += w + pad * 2 + gap
    overlay(b, paint)


def facts(b: B, y: float, items, ink=WHITE, sub=ICE) -> None:
    """Dikey çizgiyle ayrılmış üç olgu. Etiket Barlow Condensed, değer
    Montserrat — iki ayrı ailenin kontrastı veriyi öne çıkarıyor."""
    n = len(items)
    step = (W_MM - M * 2) / n
    dr = b.draw
    fl, spl = fit_track(b, dr, [a for a, _ in items], b.p(step - 24), 9.5, 0.22,
                        lambda s: b.cond(s))
    fv = fit(b, dr, [v for _, v in items], b.p(step - 26), 24,
             lambda s: b.mont(s, 600))

    def paint(d):
        for i, (lab, val) in enumerate(items):
            cx = b.p(M + step * (i + 0.5))
            track(b, d, (cx, b.p(y)), lab, fl, (*sub, 215), spl, "ma")
            d.text((cx, b.p(y + 42)), val, font=fv, fill=(*ink, 255), anchor="ms")
            if i:
                xv = b.p(M + step * i)
                d.line([xv, b.p(y - 4), xv, b.p(y + 50)], fill=(*sub, 90),
                       width=max(1, b.p(0.5)))
    overlay(b, paint)


def arc_distances(b: B, cy: float, r: float, items) -> None:
    """Referans 2'nin bağlantı yayı: ince kavis, üstünde üç durak."""
    def paint(d):
        d.arc([b.p(W_MM / 2 - r), b.p(cy - r), b.p(W_MM / 2 + r), b.p(cy + r)],
              196, 344, fill=(*SAND, 150), width=max(2, b.p(0.8)))
    overlay(b, paint)

    dr = b.draw
    fv = b.mont(15, 600)
    fl = b.cond(9.4)
    for i, (ang, val, lab) in enumerate(items):
        a = math.radians(ang)
        px = b.p(W_MM / 2) + b.p(r) * math.cos(a)
        py = b.p(cy) + b.p(r) * math.sin(a)

        def one(d, px=px, py=py, val=val, lab=lab):
            d.ellipse([px - b.p(4), py - b.p(4), px + b.p(4), py + b.p(4)],
                      fill=(*SAND_HI, 255))
            d.text((px, py - b.p(30)), val, font=fv, fill=WHITE, anchor="ms")
            track(b, d, (px, py - b.p(26)), lab, fl, (*ICE, 210), b.p(1.4), "ma")
        overlay(b, one)


def shock(b: B, cx: float, cy: float, r: float) -> None:
    """Şok rozeti — ince dişli mühür, altında gölge."""
    pts = []
    teeth = 36
    for i in range(teeth * 2):
        rad = b.p(r) if i % 2 == 0 else b.p(r * 0.935)
        a = math.pi * 2 * i / (teeth * 2) - math.pi / 2
        pts.append((b.p(cx) + rad * math.cos(a), b.p(cy) + rad * math.sin(a)))

    dr = b.draw
    fbig = b.playfair(27, 700)
    fmid = b.cond(11.5)
    fsub = b.cond(8.6)

    def paint(d):
        d.polygon(pts, fill=(*SAND_HI, 255))
        d.ellipse([b.p(cx - r * .87), b.p(cy - r * .87),
                   b.p(cx + r * .87), b.p(cy + r * .87)],
                  outline=(*NIGHT, 70), width=max(1, b.p(0.6)))
        y = b.p(cy - r * 0.46)
        track(b, d, (b.p(cx), y), "PEŞİNATLA", fsub, (*NIGHT, 215), b.p(1.6), "ma")
        # Playfair'de ₺ yok, kutu basıyordu: rakam Playfair, simge Montserrat.
        ftl = b.mont(15, 600)
        wn = d.textlength(PESIN, font=fbig)
        wt = d.textlength(" ₺", font=ftl)
        x0 = b.p(cx) - (wn + wt) / 2
        d.text((x0, b.p(cy + r * 0.06)), PESIN, font=fbig, fill=NIGHT, anchor="ls")
        d.text((x0 + wn, b.p(cy + r * 0.06)), " ₺", font=ftl, fill=NIGHT, anchor="ls")
        d.line([b.p(cx - r * .46), b.p(cy + r * .18), b.p(cx + r * .46),
                b.p(cy + r * .18)], fill=(*NIGHT, 90), width=max(1, b.p(0.5)))
        track(b, d, (b.p(cx), b.p(cy + r * .30)), "EV SAHİBİ OLUN", fmid,
              (*NIGHT, 250), b.p(1.0), "ma")
        track(b, d, (b.p(cx), b.p(cy + r * .52)), "BANKA · KREDİ · FAİZ YOK", fsub,
              (*NIGHT, 200), b.p(1.0), "ma")
    soft_shadow(b, paint, blur=7, alpha=150, dy=5)


def foot(b: B, y: float = 1836) -> None:
    rule(b, y - 30, col=SAND, a=110, w=0.6)
    qs = b.p(54)
    qx, qy = b.p(W_MM - M) - qs, b.p(y - 10)

    def plate(d):
        d.rounded_rectangle([qx - b.p(5), qy - b.p(5), qx + qs + b.p(5),
                             qy + qs + b.p(5)], radius=b.p(4), fill=(255, 255, 255, 252))
    overlay(b, plate)
    b.im.alpha_composite(qr_image(QR_URL, qs, NIGHT), (qx, qy))

    dr = b.draw
    fs, sps = fit_track(b, dr, [f"{SELLER} · {SELLER_ROLE}"], b.p(380), 7.6, 0.16,
                        lambda s: b.cond(s))

    def paint(d):
        d.text((b.p(M), b.p(y + 20)), SITE, font=b.marcellus(21), fill=WHITE,
               anchor="ls")
        d.text((b.p(M), b.p(y + 50)), "  ·  ".join(PHONES), font=b.mont(13, 600),
               fill=WHITE, anchor="ls")
        track(b, d, (b.p(M), b.p(y + 60)), f"{SELLER} · {SELLER_ROLE}", fs,
              (*ICE, 200), sps)
    overlay(b, paint)


# ==================================================================== tasarım
def ru_gece() -> Image.Image:
    b = board()
    sky(b)
    halo(b, W_MM / 2, 1140, 620, 470, (86, 150, 190), 0.34, 2.2)
    band(b, "night-gate", 1010, 470, 0.5, feather=130, bottom_fade=150)
    halo(b, W_MM / 2, 1100, 420, 240, (255, 218, 160), 0.16, 2.6)

    head_logos(b, 88)

    dr = b.draw

    def script_word(d):
        d.text((b.p(W_MM / 2), b.p(322)), "Yeni bir başlangıç", font=b.script(30, 600),
               fill=(*SAND_HI, 250), anchor="ms")
    overlay(b, script_word)

    fn, spn = fit_track(b, dr, ["MİA PARK OCEAN"], b.p(660), 52, 0.03,
                        lambda s: b.playfair(s, 600))

    def name(d):
        track(b, d, (b.p(W_MM / 2), cap_top(fn, b.p(400))), "MİA PARK OCEAN", fn,
              WHITE, spn, "ma")
    overlay(b, name)

    chips(b, 452, UNITS, WHITE, 15)

    fsub, spsub = fit_track(b, dr, ["İZMİT MİA BÖLGESİ · KOCAELİ"], b.p(500), 10,
                            0.32, lambda s: b.cond(s))

    def subline(d):
        track(b, d, (b.p(W_MM / 2), b.p(536)), "İZMİT MİA BÖLGESİ · KOCAELİ", fsub,
              (*ICE, 225), spsub, "ma")
    overlay(b, subline)

    rule(b, 586, 190, W_MM - 190, SAND, 120, 0.6)

    facts(b, 636, [("BAŞLANGIÇ PEŞİNAT", f"{PESIN} ₺"),
                   ("ÖDEME PLANI", "60 AY"),
                   ("VADE FARKI", "%0")])

    arc_distances(b, 1140, 320, [(214, "2 dk", "İZMİT SAHİLİ"),
                                 (270, "1 dk", "D100"),
                                 (326, "5 dk", "ŞEHİR MERKEZİ")])

    shock(b, 636, 1480, 118)
    vignette(b, 0.40, 2.3)
    foot(b, 1836)
    return b.im.convert("RGB")


DESIGNS = [("rollup-gece", ru_gece, "gece · playfair + oswald")]


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
        print(f"  {name:<20} {label:<28} {os.path.getsize(p)/1e6:.1f} MB")
    print(f"\n  → {OUT}")


if __name__ == "__main__":
    main()
