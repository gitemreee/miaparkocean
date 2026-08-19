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

# Fiyat tablosu. TEK DEĞİŞTİRME NOKTASI — bilbord betiği de buradan okuyor.
# (tip, peşinat, aylık taksit). Vade hepsinde 60 ay, vade farkı yok.
PRICES = [("1+0", "699.000", "29.900"),
          ("1+1", "999.000", "39.900"),
          ("2+1", "2.000.000", "50.000")]

# Fiyatsız sürüm: rakamların yerinde m² ve vade. Fiyat her yerde
# yayımlanmasın istendiğinde bu pano kullanılır, yönlendirme karekoda.
SIZES = [("1+0", "28 m²", "60 AY"),
         ("1+1", "50 m²", "60 AY"),
         ("2+1", "100 m²", "60 AY")]
LBL_PRICE = ("PEŞİNAT", "AYLIK SADECE", "VADE FARKSIZ 60 AY")
LBL_FREE = ("DAİRE BÜYÜKLÜĞÜ", "ÖDEME PLANI", "VADE FARKSIZ · %0 FAİZ")

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


def head_logos(b: B, y: float = 84, white: bool = True) -> None:
    lg = lockup(b.p(180), white=white)
    b.im.alpha_composite(lg, (b.p(M), b.p(y)))
    oc = ocean_logo(b, 110, white=white)
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
    f = b.mont(size, 600)
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
    fl, spl = fit_track(b, dr, [a for a, _ in items], b.p(step - 18), 13, 0.18,
                        lambda s: b.cond(s))
    fv = fit(b, dr, [v for _, v in items], b.p(step - 20), 38,
             lambda s: b.mont(s, 700))

    def paint(d):
        for i, (lab, val) in enumerate(items):
            cx = b.p(M + step * (i + 0.5))
            track(b, d, (cx, b.p(y)), lab, fl, (*sub, 215), spl, "ma")
            d.text((cx, b.p(y + 60)), val, font=fv, fill=(*ink, 255), anchor="ms")
            if i:
                xv = b.p(M + step * i)
                d.line([xv, b.p(y - 6), xv, b.p(y + 70)], fill=(*sub, 90),
                       width=max(1, b.p(0.5)))
    overlay(b, paint)


def arc_distances(b: B, cy: float, r: float, items) -> None:
    """Referans 2'nin bağlantı yayı: ince kavis, üstünde üç durak."""
    def paint(d):
        d.arc([b.p(W_MM / 2 - r), b.p(cy - r), b.p(W_MM / 2 + r), b.p(cy + r)],
              196, 344, fill=(*SAND, 150), width=max(2, b.p(0.8)))
    overlay(b, paint)

    dr = b.draw
    fv = b.mont(19, 700)
    fl = b.cond(11.5)
    for i, (ang, val, lab) in enumerate(items):
        a = math.radians(ang)
        px = b.p(W_MM / 2) + b.p(r) * math.cos(a)
        py = b.p(cy) + b.p(r) * math.sin(a)

        def one(d, px=px, py=py, val=val, lab=lab):
            d.ellipse([px - b.p(4), py - b.p(4), px + b.p(4), py + b.p(4)],
                      fill=(*SAND_HI, 255))
            d.text((px, py - b.p(34)), val, font=fv, fill=WHITE, anchor="ms")
            track(b, d, (px, py - b.p(26)), lab, fl, (*ICE, 210), b.p(1.4), "ma")
        overlay(b, one)


def circles(b: B, cy: float, shots, caps, r: float = 98, sub=None,
            ring=SAND) -> None:
    """Üç yuvarlak fotoğraf, ince halkayla — referansların yaşam vitrini."""
    sub = sub or ICE
    gap = (W_MM - M * 2 - r * 2 * 3) / 2
    dr = b.draw
    fc, spc = fit_track(b, dr, caps, b.p(r * 2 - 4), 11.5, 0.18,
                        lambda s_: b.cond(s_))

    for i, (shot, cap) in enumerate(zip(shots, caps)):
        cx = M + r + i * (r * 2 + gap)
        dd = b.p(r * 2)
        im = cover(shot, (dd, dd), 0.5)
        mask = Image.new("L", (dd, dd), 0)
        ImageDraw.Draw(mask).ellipse([0, 0, dd - 1, dd - 1], fill=255)
        im.putalpha(mask)

        def ring_fn(d, cx=cx, dd=dd):
            d.ellipse([b.p(cx) - dd // 2 - b.p(3), b.p(cy) - dd // 2 - b.p(3),
                       b.p(cx) + dd // 2 + b.p(3), b.p(cy) + dd // 2 + b.p(3)],
                      fill=(*ring, 205))
        overlay(b, ring_fn)
        b.im.alpha_composite(im, (b.p(cx) - dd // 2, b.p(cy) - dd // 2))

        def capt(d, cx=cx, cap=cap, dd=dd):
            track(b, d, (b.p(cx), b.p(cy) + dd // 2 + b.p(18)), cap, fc,
                  (*sub, 245), spc, "ma")
        overlay(b, capt)


NEAR = "SAHİLE 2 DK · D100'E 1 DK · MERKEZE 5 DK"


def near_line(b: B, y: float, ink=None) -> None:
    ink = ink or SAND_HI
    f, sp = fit_track(b, b.draw, [NEAR], b.p(650), 15, 0.20, lambda s_: b.cond(s_))

    def paint(d):
        track(b, d, (b.p(W_MM / 2), b.p(y)), NEAR, f, (*ink, 250), sp, "ma")
    overlay(b, paint)


def shock(b: B, cx: float, cy: float, r: float) -> None:
    """Şok rozeti — ince dişli mühür, altında gölge."""
    pts = []
    teeth = 36
    for i in range(teeth * 2):
        rad = b.p(r) if i % 2 == 0 else b.p(r * 0.935)
        a = math.pi * 2 * i / (teeth * 2) - math.pi / 2
        pts.append((b.p(cx) + rad * math.cos(a), b.p(cy) + rad * math.sin(a)))

    dr = b.draw
    fbig = b.playfair(35, 800)
    fmid = b.cond(15.5)
    fsub = b.cond(11)

    def paint(d):
        d.polygon(pts, fill=(*SAND_HI, 255))
        d.ellipse([b.p(cx - r * .87), b.p(cy - r * .87),
                   b.p(cx + r * .87), b.p(cy + r * .87)],
                  outline=(*NIGHT, 70), width=max(1, b.p(0.6)))
        y = b.p(cy - r * 0.46)
        track(b, d, (b.p(cx), y), "PEŞİNATLA", fsub, (*NIGHT, 215), b.p(1.6), "ma")
        # Playfair'de ₺ yok, kutu basıyordu: rakam Playfair, simge Montserrat.
        ftl = b.mont(19, 700)
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


def price_rows(b: B, y: float, rows, ink=WHITE, sub=ICE, card=(14, 34, 52),
               step: float = 214, labels=None, unit: bool = True) -> None:
    """Fiyat satırları. Roll-up dar olduğu için kartlar yan yana değil ALT
    ALTA: 800 mm'de üç kart 217 mm'ye düşüyor ve 2.000.000 rakamı
    okunmaz puntoya iniyordu."""
    l1, l2, l3 = labels or LBL_PRICE
    dr = b.draw
    ftyp = fit(b, dr, [r[0] for r in rows], b.p(120), 30, lambda s_: b.mont(s_, 700))
    fl, spl = fit_track(b, dr, [l1, l2], b.p(210), 10, 0.20,
                        lambda s_: b.cond(s_))
    fnum = fit(b, dr, [r[1] for r in rows], b.p(260), 40,
               lambda s_: b.mont(s_, 700))
    fay = fit(b, dr, [r[2] for r in rows], b.p(200), 34,
              lambda s_: b.mont(s_, 700))
    ftl = b.mont(14, 700)

    for i, (typ, pesin, aylik) in enumerate(rows):
        yy = y + i * step

        def row(d, yy=yy, typ=typ, pesin=pesin, aylik=aylik):
            d.rounded_rectangle([b.p(M), b.p(yy), b.p(W_MM - M), b.p(yy + step - 22)],
                                radius=b.p(6), fill=(*card, 226),
                                outline=(*SAND, 190), width=max(2, b.p(0.8)))
            # Tip rozeti kartın üst kenarına oturur.
            bw, bh = b.p(112), b.p(38)
            bx = b.p(M) + b.p(26)
            d.rounded_rectangle([bx, b.p(yy) - bh // 2, bx + bw, b.p(yy) + bh // 2],
                                radius=bh // 2, fill=(*SAND_HI, 255))
            d.text((bx + bw / 2, cap_top(ftyp, b.p(yy))), typ, font=ftyp,
                   fill=NIGHT, anchor="ma")

            track(b, d, (b.p(M + 32), b.p(yy + 52)), l1, fl, (*sub, 225), spl)
            wn = d.textlength(pesin, font=fnum)
            d.text((b.p(M + 32), b.p(yy + 132)), pesin, font=fnum, fill=(*ink, 255),
                   anchor="ls")
            if unit:
                d.text((b.p(M + 32) + wn + b.p(4), b.p(yy + 132)), " ₺", font=ftl,
                       fill=(*SAND_HI, 255), anchor="ls")

            d.line([b.p(430), b.p(yy + 46), b.p(430), b.p(yy + 148)],
                   fill=(*SAND, 130), width=max(1, b.p(0.6)))

            track(b, d, (b.p(462), b.p(yy + 52)), l2, fl, (*sub, 225), spl)
            wa = d.textlength(aylik, font=fay)
            d.text((b.p(462), b.p(yy + 126)), aylik, font=fay, fill=(*ink, 255),
                   anchor="ls")
            if unit:
                d.text((b.p(462) + wa + b.p(4), b.p(yy + 126)), " ₺", font=ftl,
                       fill=(*SAND_HI, 255), anchor="ls")
            fv, spv = fit_track(b, d, [l3], b.p(240), 9.5, 0.14,
                                lambda s_: b.cond(s_))
            track(b, d, (b.p(462), b.p(yy + 150)), l3, fv, (*SAND_HI, 250), spv)
        overlay(b, row)


def foot(b: B, y: float = 1836, ink=WHITE, sub=ICE, qr_dark=None) -> None:
    qr_dark = qr_dark or NIGHT
    rule(b, y - 30, col=SAND, a=110, w=0.6)
    qs = b.p(54)
    qx, qy = b.p(W_MM - M) - qs, b.p(y - 10)

    def plate(d):
        d.rounded_rectangle([qx - b.p(5), qy - b.p(5), qx + qs + b.p(5),
                             qy + qs + b.p(5)], radius=b.p(4), fill=(255, 255, 255, 252))
    overlay(b, plate)
    b.im.alpha_composite(qr_image(QR_URL, qs, qr_dark), (qx, qy))

    dr = b.draw
    fs, sps = fit_track(b, dr, [f"{SELLER} · {SELLER_ROLE}"], b.p(420), 9, 0.16,
                        lambda s: b.cond(s))

    def paint(d):
        d.text((b.p(M), b.p(y + 20)), SITE, font=b.marcellus(28), fill=(*ink, 255),
               anchor="ls")
        d.text((b.p(M), b.p(y + 50)), "  ·  ".join(PHONES), font=b.mont(17, 700),
               fill=(*ink, 255), anchor="ls")
        track(b, d, (b.p(M), b.p(y + 60)), f"{SELLER} · {SELLER_ROLE}", fs,
              (*sub, 215), sps)
    overlay(b, paint)


# ==================================================================== tasarım
def ru_gece() -> Image.Image:
    b = board()
    sky(b)
    halo(b, W_MM / 2, 1330, 620, 440, (86, 150, 190), 0.34, 2.2)
    band(b, "night-gate", 1120, 470, 0.5, feather=130, bottom_fade=150)
    halo(b, W_MM / 2, 1290, 420, 240, (255, 218, 160), 0.16, 2.6)

    head_logos(b, 88)

    dr = b.draw

    def script_word(d):
        d.text((b.p(W_MM / 2), b.p(330)), "Yeni bir başlangıç", font=b.script(42, 700),
               fill=(*SAND_HI, 250), anchor="ms")
    overlay(b, script_word)

    fn, spn = fit_track(b, dr, ["MİA PARK OCEAN"], b.p(684), 74, 0.02,
                        lambda s: b.playfair(s, 800))

    def name(d):
        track(b, d, (b.p(W_MM / 2), cap_top(fn, b.p(412))), "MİA PARK OCEAN", fn,
              WHITE, spn, "ma")
    overlay(b, name)

    chips(b, 470, UNITS, WHITE, 22)

    fsub, spsub = fit_track(b, dr, ["İZMİT MİA BÖLGESİ · KOCAELİ"], b.p(604), 15.5,
                            0.28, lambda s: b.cond(s))

    def subline(d):
        track(b, d, (b.p(W_MM / 2), b.p(562)), "İZMİT MİA BÖLGESİ · KOCAELİ", fsub,
              (*ICE, 225), spsub, "ma")
    overlay(b, subline)

    rule(b, 612, 180, W_MM - 180, SAND, 120, 0.6)

    facts(b, 664, [("BAŞLANGIÇ PEŞİNAT", f"{PESIN} ₺"),
                   ("ÖDEME PLANI", "60 AY"),
                   ("VADE FARKI", "%0")])

    circles(b, 924, ["ic-mekan/17-sus-havuzu", "ic-mekan/18-yuruyus-yolu",
             "ic-mekan/05-1plus1-salon"],
            ["SÜS HAVUZLARI", "YÜRÜYÜŞ YOLLARI", "İÇ MEKÂN"])
    near_line(b, 1098)

    shock(b, 632, 1500, 126)
    vignette(b, 0.40, 2.3)
    foot(b, 1836)
    return b.im.convert("RGB")


# ============================================================ 2 · OSWALD
def ru_oswald() -> Image.Image:
    """Sıkışık grotesk manşet. Gündüz render, açık gökyüzü."""
    b = board()
    b.im = gradient((b.W, b.H), [
        (0.0, (12, 30, 48)), (0.30, (22, 56, 84)), (0.55, (34, 78, 108)),
        (0.78, (16, 38, 58)), (1.0, NIGHT),
    ], angle=0.16)
    halo(b, W_MM / 2, 1390, 640, 420, (120, 178, 214), 0.30, 2.2)
    band(b, "entrance-gate", 1250, 470, 0.46, feather=140, bottom_fade=150)

    head_logos(b, 88)
    dr = b.draw

    fe, spe = fit_track(b, dr, ["İZMİT MİA BÖLGESİ'NDE"], b.p(560), 13, 0.30,
                        lambda s_: b.cond(s_))

    def eb(d):
        track(b, d, (b.p(W_MM / 2), b.p(306)), "İZMİT MİA BÖLGESİ'NDE", fe,
              (*SAND_HI, 250), spe, "ma")
    overlay(b, eb)

    lines = ["SATIŞ", "BAŞLADI"]
    fh, sph = fit_track(b, dr, lines, b.p(660), 96, 0.01,
                        lambda s_: b.f("Oswald-var.ttf", s_, 700))
    step = cap_h(fh) * 1.10

    def head(d):
        for i2, t in enumerate(lines):
            track(b, d, (b.p(W_MM / 2), b.p(360) + i2 * step), t, fh, WHITE, sph, "ma")
    overlay(b, head)

    chips(b, 610, UNITS, WHITE, 22)
    rule(b, 700, 180, W_MM - 180, SAND, 120, 0.6)
    facts(b, 752, [("BAŞLANGIÇ PEŞİNAT", f"{PESIN} ₺"),
                   ("ÖDEME PLANI", "60 AY"),
                   ("VADE FARKI", "%0")])

    fq, spq = fit_track(b, dr, ["BANKA YOK · KREDİ YOK · KEFİL YOK"], b.p(646), 16,
                        0.18, lambda s_: b.cond(s_))

    def note(d):
        track(b, d, (b.p(W_MM / 2), b.p(868)), "BANKA YOK · KREDİ YOK · KEFİL YOK",
              fq, (*SAND_HI, 250), spq, "ma")
    overlay(b, note)

    circles(b, 1000, ["ic-mekan/17-sus-havuzu", "ic-mekan/18-yuruyus-yolu",
             "ic-mekan/05-1plus1-salon"],
            ["SÜS HAVUZLARI", "YÜRÜYÜŞ YOLLARI", "İÇ MEKÂN"])
    near_line(b, 1214)

    shock(b, 632, 1520, 126)
    vignette(b, 0.38, 2.3)
    foot(b, 1836)
    return b.im.convert("RGB")


# ============================================================ 3 · CORMORANT
def ru_beyaz() -> Image.Image:
    """İnce zarif serif, sıcak beyaz zemin. Kütüphanenin öbür ucu."""
    b = board()
    b.im = gradient((b.W, b.H), [(0.0, (253, 252, 249)), (0.5, (247, 244, 238)),
                                 (1.0, (234, 229, 220))], angle=0.3)
    ink, sub, line = (30, 34, 40), (128, 130, 134), (216, 210, 200)

    ph = 470
    # Cephe yakın planı duvar gibi okunuyordu; gündüz dış görünüm.
    im = cover("entrance-gate", (b.W, b.p(ph)), 0.46)
    a = np.asarray(im.split()[3], np.float32)
    fp = b.p(120)
    ramp = np.ones(b.p(ph), np.float32)
    ramp[:fp] = np.linspace(0, 1, fp) ** 1.3
    ramp[b.p(ph) - fp:] *= np.linspace(1, 0, fp) ** 1.2
    im.putalpha(Image.fromarray((a * ramp[:, None]).astype(np.uint8), "L"))
    b.im.alpha_composite(im, (0, b.p(1200)))

    head_logos(b, 88, white=False)
    dr = b.draw

    def script_word(d):
        d.text((b.p(W_MM / 2), b.p(330)), "Yeni bir başlangıç",
               font=b.script(42, 700), fill=(*SAND, 255), anchor="ms")
    overlay(b, script_word)

    fn, spn = fit_track(b, dr, ["MİA PARK OCEAN"], b.p(680), 68, 0.04,
                        lambda s_: b.cormorant(s_, 600))

    def name(d):
        track(b, d, (b.p(W_MM / 2), cap_top(fn, b.p(416))), "MİA PARK OCEAN", fn,
              ink, spn, "ma")
    overlay(b, name)

    chips(b, 470, UNITS, ink, 22)

    fsub, spsub = fit_track(b, dr, ["İZMİT MİA BÖLGESİ · KOCAELİ"], b.p(604), 15.5,
                            0.28, lambda s_: b.cond(s_))

    def subline(d):
        track(b, d, (b.p(W_MM / 2), b.p(562)), "İZMİT MİA BÖLGESİ · KOCAELİ", fsub,
              (*sub, 245), spsub, "ma")
    overlay(b, subline)

    rule(b, 612, 180, W_MM - 180, SAND, 190, 0.7)
    facts(b, 664, [("BAŞLANGIÇ PEŞİNAT", f"{PESIN} ₺"),
                   ("ÖDEME PLANI", "60 AY"),
                   ("VADE FARKI", "%0")], ink=ink, sub=sub)

    fq, spq = fit_track(b, dr, ["BANKA YOK · KREDİ YOK · KEFİL YOK"], b.p(646), 16,
                        0.18, lambda s_: b.cond(s_))

    def note(d):
        # Açık zeminde açık şampanya okunmuyor; koyu tonu.
        track(b, d, (b.p(W_MM / 2), b.p(800)), "BANKA YOK · KREDİ YOK · KEFİL YOK",
              fq, (150, 116, 56, 255), spq, "ma")
    overlay(b, note)

    circles(b, 966, ["ic-mekan/17-sus-havuzu", "ic-mekan/18-yuruyus-yolu",
             "ic-mekan/05-1plus1-salon"],
            ["SÜS HAVUZLARI", "YÜRÜYÜŞ YOLLARI", "İÇ MEKÂN"], sub=(120, 124, 130))
    near_line(b, 1140, ink=(150, 116, 56))

    shock(b, 632, 1500, 126)
    foot(b, 1836, ink=ink, sub=sub, qr_dark=ink)
    return b.im.convert("RGB")


# ============================================================ 4 · MARCELLUS
def ru_klasik() -> Image.Image:
    """Rafine roman kapital, geniş harf aralığı. En sakin pano."""
    b = board()
    b.im = gradient((b.W, b.H), [
        (0.0, (4, 16, 24)), (0.28, (8, 32, 46)), (0.54, (12, 48, 66)),
        (0.80, (7, 26, 38)), (1.0, (3, 12, 20)),
    ], angle=0.14)
    halo(b, W_MM / 2, 1330, 600, 430, (96, 168, 196), 0.30, 2.2)
    band(b, "aerial-pools", 1120, 470, 0.5, feather=140, bottom_fade=160)

    head_logos(b, 88)
    dr = b.draw

    fn, spn = fit_track(b, dr, ["MİA PARK OCEAN"], b.p(672), 50, 0.16,
                        lambda s_: b.marcellus(s_))

    def name(d):
        track(b, d, (b.p(W_MM / 2), cap_top(fn, b.p(330))), "MİA PARK OCEAN", fn,
              WHITE, spn, "ma")
    overlay(b, name)

    rule(b, 392, 230, W_MM - 230, SAND, 150, 0.6)

    fi = b.cormorant(30, 400)

    def line2(d):
        d.text((b.p(W_MM / 2), b.p(452)), "İzmit MİA Bölgesi'nde yeni yaşam",
               font=fi, fill=(*ICE, 250), anchor="ms")
    overlay(b, line2)

    chips(b, 500, UNITS, WHITE, 22)
    facts(b, 626, [("BAŞLANGIÇ PEŞİNAT", f"{PESIN} ₺"),
                   ("ÖDEME PLANI", "60 AY"),
                   ("VADE FARKI", "%0")])

    circles(b, 900, ["ic-mekan/17-sus-havuzu", "ic-mekan/18-yuruyus-yolu",
             "ic-mekan/05-1plus1-salon"],
            ["SÜS HAVUZLARI", "YÜRÜYÜŞ YOLLARI", "İÇ MEKÂN"])
    near_line(b, 1074)

    shock(b, 632, 1500, 126)
    vignette(b, 0.42, 2.3)
    foot(b, 1836)
    return b.im.convert("RGB")


# ============================================================ 5 · MONTSERRAT
def ru_modern() -> Image.Image:
    """Geometrik sans, en çağdaş dil. Avlu render'ı."""
    b = board()
    b.im = gradient((b.W, b.H), [
        (0.0, (8, 20, 32)), (0.32, (14, 42, 62)), (0.60, (10, 34, 52)),
        (1.0, (4, 14, 24)),
    ], angle=0.2)
    halo(b, W_MM / 2, 1340, 620, 430, (104, 172, 200), 0.32, 2.2)
    band(b, "courtyard-pools", 1130, 470, 0.5, feather=140, bottom_fade=160)

    head_logos(b, 88)
    dr = b.draw

    lines = ["1+0 · 1+1 · LOFT", "DAİRELER SATIŞTA"]
    fh, sph = fit_track(b, dr, lines, b.p(670), 42, 0.02,
                        lambda s_: b.mont(s_, 800))
    step = cap_h(fh) * 1.44

    def head(d):
        for i2, t in enumerate(lines):
            track(b, d, (b.p(W_MM / 2), b.p(322) + i2 * step), t, fh, WHITE, sph, "ma")
    overlay(b, head)

    fsub, spsub = fit_track(b, dr, ["İZMİT MİA BÖLGESİ · KOCAELİ"], b.p(604), 15.5,
                            0.28, lambda s_: b.cond(s_))

    def subline(d):
        track(b, d, (b.p(W_MM / 2), b.p(470)), "İZMİT MİA BÖLGESİ · KOCAELİ", fsub,
              (*SAND_HI, 245), spsub, "ma")
    overlay(b, subline)

    rule(b, 528, 180, W_MM - 180, SAND, 120, 0.6)
    facts(b, 584, [("BAŞLANGIÇ PEŞİNAT", f"{PESIN} ₺"),
                   ("ÖDEME PLANI", "60 AY"),
                   ("VADE FARKI", "%0")])

    fq, spq = fit_track(b, dr, ["BANKA YOK · KREDİ YOK · KEFİL YOK"], b.p(646), 16,
                        0.18, lambda s_: b.cond(s_))

    def note(d):
        track(b, d, (b.p(W_MM / 2), b.p(724)), "BANKA YOK · KREDİ YOK · KEFİL YOK",
              fq, (*SAND_HI, 250), spq, "ma")
    overlay(b, note)

    circles(b, 924, ["ic-mekan/17-sus-havuzu", "ic-mekan/18-yuruyus-yolu",
             "ic-mekan/05-1plus1-salon"],
            ["SÜS HAVUZLARI", "YÜRÜYÜŞ YOLLARI", "İÇ MEKÂN"])
    near_line(b, 1098)

    shock(b, 632, 1500, 126)
    vignette(b, 0.38, 2.3)
    foot(b, 1836)
    return b.im.convert("RGB")


# ============================================================ 6 · ÖDEME
def _odeme(priced: bool) -> Image.Image:
    """Üç daire tipi. 2+1 bu panoda var. priced=False ise rakam yok."""
    b = board()
    b.im = gradient((b.W, b.H), [
        (0.0, NIGHT), (0.22, NAVY), (0.44, SKY), (0.66, NAVY), (1.0, NIGHT),
    ], angle=0.12)
    halo(b, W_MM / 2, 1620, 620, 400, (86, 150, 190), 0.30, 2.2)
    band(b, "night-gate", 1420, 470, 0.5, feather=140, bottom_fade=150)

    head_logos(b, 88)
    dr = b.draw

    def script_word(d):
        d.text((b.p(W_MM / 2), b.p(318)), "Kaçırılmayacak fırsat!",
               font=b.script(40, 700), fill=(*SAND_HI, 250), anchor="ms")
    overlay(b, script_word)

    fn, spn = fit_track(b, dr, ["FİYAT AVANTAJI"], b.p(684), 74, 0.02,
                        lambda s_: b.playfair(s_, 800))

    def name(d):
        track(b, d, (b.p(W_MM / 2), cap_top(fn, b.p(404))), "FİYAT AVANTAJI", fn,
              WHITE, spn, "ma")
    overlay(b, name)

    fsub, spsub = fit_track(b, dr, ["İZMİT'İN EN DEĞERLİ LOKASYONUNDA"], b.p(620),
                            14, 0.26, lambda s_: b.cond(s_))

    def subline(d):
        track(b, d, (b.p(W_MM / 2), b.p(462)), "İZMİT'İN EN DEĞERLİ LOKASYONUNDA",
              fsub, (*ICE, 235), spsub, "ma")
    overlay(b, subline)

    price_rows(b, 560, PRICES if priced else SIZES,
               labels=LBL_PRICE if priced else LBL_FREE, unit=priced)

    fq, spq = fit_track(b, dr, ["BANKA YOK · FAİZ YOK · KEFİL YOK"], b.p(646), 17,
                        0.18, lambda s_: b.cond(s_))

    def note(d):
        d.rounded_rectangle([b.p(M), b.p(1216), b.p(W_MM - M), b.p(1300)],
                            radius=b.p(6), fill=(*SAND_HI, 255))
        track(b, d, (b.p(W_MM / 2), cap_top(fq, b.p(1258))),
              "BANKA YOK · FAİZ YOK · KEFİL YOK", fq, NIGHT, spq, "ma")
    overlay(b, note)

    kick = ("TASARRUFA DAYALI FAİZSİZ FİNANSMAN SİSTEMİ" if priced
            else "FİYAT VE KAT PLANLARI İÇİN KAREKODU OKUTUN")
    fk, spk = fit_track(b, dr, [kick], b.p(646), 13, 0.20, lambda s_: b.cond(s_))

    def kicker(d):
        track(b, d, (b.p(W_MM / 2), b.p(1340)), kick, fk, (*ICE, 235), spk, "ma")
    overlay(b, kicker)

    vignette(b, 0.38, 2.3)
    foot(b, 1836)
    return b.im.convert("RGB")


def ru_odeme() -> Image.Image:
    return _odeme(True)


def ru_odeme_fiyatsiz() -> Image.Image:
    return _odeme(False)


DESIGNS = [
    ("rollup-1-gece", ru_gece, "gece · Playfair"),
    ("rollup-2-oswald", ru_oswald, "gündüz · Oswald sıkışık"),
    ("rollup-3-beyaz", ru_beyaz, "beyaz · Cormorant"),
    ("rollup-4-klasik", ru_klasik, "klasik · Marcellus"),
    ("rollup-5-modern", ru_modern, "modern · Montserrat"),
    ("rollup-6-odeme", ru_odeme, "ödeme · üç fiyat"),
    ("rollup-7-odeme-fiyatsiz", ru_odeme_fiyatsiz, "ödeme · fiyatsız"),
]


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
