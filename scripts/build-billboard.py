#!/usr/bin/env python3
"""
MİA PARK OCEAN — bilbord serisi (5 tasarım).

Roll-up'ların yatay karşılığı. Aynı tasarım sistemi: iki logo, dev
manşet, dikey çizgiyle ayrılmış üç olgu, üç yuvarlak fotoğraf, şok
mührü, künye şeridi. Tipografi kütüphanesi ve derinlik parçaları
build-rollup.py'den geliyor; burada yalnızca YATAY kompozisyon var.

ÖLÇÜ: 5000 x 3000 mm, 1:1 ölçekte 40 dpi (7874 x 4724 px).

Render'lar 4096x2304; 5:3'lük panoya tam sayfa girerken yalnızca %6
yanlardan kırpılıyor. Roll-up'ta gereken gökyüzü uzatması burada
gerekmiyor — kare doğal haliyle tüm panoyu kaplıyor.

OKUNURLUK
─────────
Bilbord 30-100 m'den okunur. Manşet 300 mm, olgu değerleri 150 mm
punto; roll-up'taki küçük satırlar (satıcı alt künyesi, uzun açıklama)
buraya alınmadı — o mesafeden okunmaz, yalnızca kalabalık eder.

DAİRELER: 1+0, 1+1, 1+1 Bahçe Loft. 2+1 gösterilmiyor.

    python scripts/build-billboard.py
"""

from __future__ import annotations

import importlib.util
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_spec = importlib.util.spec_from_file_location(
    "ru", os.path.join(ROOT, "scripts", "build-rollup.py"))
ru = importlib.util.module_from_spec(_spec)
sys.modules["ru"] = ru
_spec.loader.exec_module(ru)

bs = ru.bs
Board = ru.Board
gradient, cover, scrim, overlay = ru.gradient, ru.cover, ru.scrim, ru.overlay
track, fit, fit_track = ru.track, ru.fit, ru.fit_track
qr_image, lockup = ru.qr_image, ru.lockup
cap_h, cap_top = ru.cap_h, ru.cap_top
halo, vignette, soft_shadow = ru.halo, ru.vignette, ru.soft_shadow
ocean_logo = ru.ocean_logo

WHITE, NIGHT, ICE = ru.WHITE, ru.NIGHT, ru.ICE
SAND, SAND_HI = ru.SAND, ru.SAND_HI
SITE, PHONES = ru.SITE, ru.PHONES
QR_URL = "https://miaparkocean.com/?utm_source=bilbord"
UNITS, PESIN = ru.UNITS, ru.PESIN

OUT = os.path.join(ROOT, "tabela", "bilbord")
PREVIEW = os.path.join(OUT, "onizleme")

W_MM, H_MM, DPI = 5000, 3000, 40
M = 190
FOOT_H = 400


def board() -> ru.B:
    # Parçalar modül düzeyindeki ölçüleri okuyor; yatay geometriye çeviriyoruz.
    ru.W_MM, ru.H_MM, ru.M = W_MM, H_MM, M
    return ru.B(W_MM, H_MM, DPI)


def hscrim(b, x0: float, x1: float, a0: int, a1: int, col=NIGHT) -> None:
    """Yatay perde — bilbordda yazı hep SOL yarıda, perde de öyle."""
    w = b.p(x1) - b.p(x0)
    arr = np.zeros((1, max(w, 2), 4), np.float32)
    t = np.linspace(0, 1, max(w, 2))
    arr[0, :, 0], arr[0, :, 1], arr[0, :, 2] = col
    arr[0, :, 3] = a0 + (a1 - a0) * t
    im = Image.fromarray(arr.astype(np.uint8), "RGBA").resize((w, b.H), Image.LANCZOS)
    b.im.alpha_composite(im, (b.p(x0), 0))


def logos(b, white: bool = True) -> None:
    lg = lockup(b.p(620), white=white)
    b.im.alpha_composite(lg, (b.p(M), b.p(150)))
    oc = ocean_logo(b, 360, white=white)
    b.im.alpha_composite(oc, (b.p(W_MM - M) - oc.width, b.p(190)))


def facts_h(b, y: float, items, ink=WHITE, sub=ICE, x0=None, x1=None) -> None:
    """Üç olgu, dikey çizgiyle ayrılmış. Sol yarıya sığar."""
    x0 = M if x0 is None else x0
    x1 = 2680 if x1 is None else x1
    n = len(items)
    step = (x1 - x0) / n
    dr = b.draw
    fl, spl = fit_track(b, dr, [a for a, _ in items], b.p(step - 90), 62, 0.18,
                        lambda s: b.cond(s))
    fv = fit(b, dr, [v for _, v in items], b.p(step - 80), 165,
             lambda s: b.mont(s, 700))

    def paint(d):
        for i, (lab, val) in enumerate(items):
            cx = b.p(x0 + step * (i + 0.5))
            track(b, d, (cx, b.p(y)), lab, fl, (*sub, 220), spl, "ma")
            d.text((cx, b.p(y + 262)), val, font=fv, fill=(*ink, 255), anchor="ms")
            if i:
                xv = b.p(x0 + step * i)
                d.line([xv, b.p(y - 26), xv, b.p(y + 300)], fill=(*sub, 100),
                       width=max(2, b.p(2.4)))
    overlay(b, paint)


def circles_h(b, cx: float, cy: float, shots, caps, r: float = 300,
              sub=ICE, plate=None) -> None:
    """Üç yuvarlak, DİKEY sütun halinde sağda — yatay panoda satır olarak
    dizilseler manşetin altını kaplayıp okunurluğu düşürüyordu."""
    dr = b.draw
    # Alt yazı için sağda kalan gerçek genişliğe sığdırılıyor; sabit
    # genişlikle en uzun etiket pano kenarından taşıyordu.
    room = (W_MM - M) - (cx + r + 50)
    fc, spc = fit_track(b, dr, caps, b.p(room), 50, 0.14, lambda s_: b.cond(s_))
    gap = r * 2 + 90
    for i, (shot, cap) in enumerate(zip(shots, caps)):
        y = cy + (i - 1) * gap
        d = b.p(r * 2)
        im = cover(shot, (d, d), 0.5)
        mask = Image.new("L", (d, d), 0)
        ImageDraw.Draw(mask).ellipse([0, 0, d - 1, d - 1], fill=255)
        im.putalpha(mask)

        def ring(dd, y=y, d=d):
            dd.ellipse([b.p(cx) - d // 2 - b.p(8), b.p(y) - d // 2 - b.p(8),
                        b.p(cx) + d // 2 + b.p(8), b.p(y) + d // 2 + b.p(8)],
                       fill=(*SAND, 210))
        overlay(b, ring)
        b.im.alpha_composite(im, (b.p(cx) - d // 2, b.p(y) - d // 2))

        def capt(dd, y=y, cap=cap, d=d):
            tx = b.p(cx) + d // 2 + b.p(50)
            if plate:
                w = sum(dd.textlength(c, font=fc) for c in cap) + spc * (len(cap) - 1)
                hh = cap_h(fc)
                dd.rounded_rectangle([tx - b.p(26), b.p(y) - hh * 1.3,
                                      tx + w + b.p(26), b.p(y) + hh * 1.3],
                                     radius=int(hh * 1.3), fill=(*plate, 236))
            track(b, dd, (tx, cap_top(fc, b.p(y))), cap, fc, (*sub, 250), spc)
        overlay(b, capt)


def foot_h(b, ink=WHITE, sub=ICE, band=True) -> None:
    """Alt künye şeridi: web ve telefon solda, karekod sağda."""
    y0 = b.p(H_MM - FOOT_H)

    if band:
        def bandp(d):
            d.rectangle([0, y0, b.W, b.H], fill=(*NIGHT, 232))
            d.line([0, y0, b.W, y0], fill=(*SAND, 200), width=max(2, b.p(3)))
        overlay(b, bandp)

    qs = b.p(230)
    qx, qy = b.p(W_MM - M) - qs, y0 + b.p(84)

    def plate(d):
        d.rounded_rectangle([qx - b.p(18), qy - b.p(18), qx + qs + b.p(18),
                             qy + qs + b.p(18)], radius=b.p(16),
                            fill=(255, 255, 255, 252))
    overlay(b, plate)
    b.im.alpha_composite(qr_image(QR_URL, qs, NIGHT), (qx, qy))

    dr = b.draw

    def paint(d):
        d.text((b.p(M), y0 + b.p(180)), SITE, font=b.marcellus(120),
               fill=(*ink, 255), anchor="ls")
        d.text((b.p(M), y0 + b.p(310)), "  ·  ".join(PHONES), font=b.mont(78, 700),
               fill=(*ink, 255), anchor="ls")
        f2, sp2 = fit_track(b, d, ["OCEAN GAYRİMENKUL · TEK YETKİLİ SATICI"],
                            b.p(1700), 56, 0.18, lambda s_: b.cond(s_))
        track(b, d, (b.p(2500), y0 + b.p(260)),
              "OCEAN GAYRİMENKUL · TEK YETKİLİ SATICI", f2, (*sub, 225), sp2)
    overlay(b, paint)


def chips_h(b, x: float, y: float, ink=WHITE, size: float = 96) -> None:
    dr = b.draw
    f = b.mont(size, 600)
    ws = [dr.textlength(t, font=f) for t in UNITS]
    pad, gap = b.p(64), b.p(44)
    h = cap_h(f) + pad * 1.8

    def paint(d):
        cx = b.p(x)
        for t, w in zip(UNITS, ws):
            d.rounded_rectangle([cx, b.p(y), cx + w + pad * 2, b.p(y) + h],
                                radius=b.p(10), outline=(*ink, 140),
                                width=max(2, b.p(2.4)))
            d.text((cx + pad + w / 2, cap_top(f, b.p(y) + h / 2)), t, font=f,
                   fill=(*ink, 248), anchor="ma")
            cx += w + pad * 2 + gap
    overlay(b, paint)


def shock_h(b, cx: float, cy: float, r: float = 470) -> None:
    """Şok mührü — roll-up'takinin yatay ölçekli hali."""
    import math
    pts = []
    teeth = 40
    for i in range(teeth * 2):
        rad = b.p(r) if i % 2 == 0 else b.p(r * 0.935)
        a = math.pi * 2 * i / (teeth * 2) - math.pi / 2
        pts.append((b.p(cx) + rad * math.cos(a), b.p(cy) + rad * math.sin(a)))

    dr = b.draw
    fbig = b.playfair(150, 800)
    ftl = b.mont(80, 700)
    fmid = b.cond(66)
    fsub = b.cond(46)

    def paint(d):
        d.polygon(pts, fill=(*SAND_HI, 255))
        d.ellipse([b.p(cx - r * .87), b.p(cy - r * .87), b.p(cx + r * .87),
                   b.p(cy + r * .87)], outline=(*NIGHT, 70), width=max(2, b.p(2.4)))
        track(b, d, (b.p(cx), b.p(cy - r * 0.48)), "PEŞİNATLA", fsub, (*NIGHT, 215),
              b.p(7), "ma")
        wn = d.textlength(PESIN, font=fbig)
        wt = d.textlength(" ₺", font=ftl)
        x0 = b.p(cx) - (wn + wt) / 2
        d.text((x0, b.p(cy + r * 0.06)), PESIN, font=fbig, fill=NIGHT, anchor="ls")
        d.text((x0 + wn, b.p(cy + r * 0.06)), " ₺", font=ftl, fill=NIGHT, anchor="ls")
        d.line([b.p(cx - r * .46), b.p(cy + r * .19), b.p(cx + r * .46),
                b.p(cy + r * .19)], fill=(*NIGHT, 90), width=max(2, b.p(2.2)))
        track(b, d, (b.p(cx), b.p(cy + r * .30)), "EV SAHİBİ OLUN", fmid,
              (*NIGHT, 250), b.p(4), "ma")
        track(b, d, (b.p(cx), b.p(cy + r * .54)), "BANKA · KREDİ · FAİZ YOK", fsub,
              (*NIGHT, 200), b.p(4), "ma")
    soft_shadow(b, paint, blur=26, alpha=150, dy=18)


SHOTS = ["ic-mekan/17-sus-havuzu", "ic-mekan/18-yuruyus-yolu",
         "ic-mekan/05-1plus1-salon"]
CAPS = ["SÜS HAVUZLARI", "YÜRÜYÜŞ YOLLARI", "İÇ MEKÂN"]
FACTS = [("BAŞLANGIÇ PEŞİNAT", f"{PESIN} ₺"), ("ÖDEME PLANI", "60 AY"),
         ("VADE FARKI", "%0")]


def _base(shot: str, focus: float = 0.5, light: bool = False) -> ru.B:
    """Ortak zemin: tam sayfa render, solda perde, kenarda vinyet."""
    b = board()
    im = cover(shot, (b.W, b.H), focus)
    b.im.alpha_composite(im, (0, 0))
    if light:
        # Tüm kareyi soldurmak binayı sisin içinde bırakıyordu; yalnızca
        # yazının oturduğu SOL yarı beyazlıyor, sağ yarı net kalıyor.
        b.im.alpha_composite(scrim((b.W, b.H), [
            (0.0, (250, 248, 244, 96)), (0.55, (250, 248, 244, 30)),
            (1.0, (250, 248, 244, 70)),
        ]), (0, 0))
        hscrim(b, 0, 3050, 248, 0, (252, 250, 246))
    else:
        b.im.alpha_composite(scrim((b.W, b.H), [
            (0.0, (*NIGHT, 150)), (0.45, (*NIGHT, 70)), (1.0, (*NIGHT, 190)),
        ]), (0, 0))
        hscrim(b, 0, 3500, 238, 0)
    return b


# ============================================================ 1 · GECE
def bb_gece() -> Image.Image:
    b = _base("night-gate", 0.5)
    logos(b)
    dr = b.draw

    def script_word(d):
        d.text((b.p(M), b.p(1000)), "Yeni bir başlangıç", font=b.script(170, 700),
               fill=(*SAND_HI, 250), anchor="ls")
    overlay(b, script_word)

    fn, spn = fit_track(b, dr, ["MİA PARK OCEAN"], b.p(2540), 300, 0.02,
                        lambda s: b.playfair(s, 800))

    def name(d):
        track(b, d, (b.p(M), cap_top(fn, b.p(1300))), "MİA PARK OCEAN", fn, WHITE,
              spn, "la")
    overlay(b, name)

    chips_h(b, M, 1520)
    facts_h(b, 1880, FACTS)
    circles_h(b, 3900, 1450, SHOTS, CAPS, 280)
    shock_h(b, 3180, 2130, 440)
    vignette(b, 0.34, 2.4)
    foot_h(b)
    return b.im.convert("RGB")


# ============================================================ 2 · OSWALD
def bb_oswald() -> Image.Image:
    b = _base("entrance-gate", 0.46)
    logos(b)
    dr = b.draw

    fe, spe = fit_track(b, dr, ["İZMİT MİA BÖLGESİ'NDE"], b.p(1900), 66, 0.28,
                        lambda s: b.cond(s))

    def eb(d):
        track(b, d, (b.p(M), b.p(900)), "İZMİT MİA BÖLGESİ'NDE", fe,
              (*SAND_HI, 250), spe, "la")
    overlay(b, eb)

    lines = ["SATIŞ", "BAŞLADI"]
    fh, sph = fit_track(b, dr, lines, b.p(2420), 360, 0.01,
                        lambda s: b.f("Oswald-var.ttf", s, 700))
    step = cap_h(fh) * 1.06

    def head(d):
        for i, t in enumerate(lines):
            track(b, d, (b.p(M), b.p(1080) + i * step), t, fh, WHITE, sph, "la")
    overlay(b, head)

    chips_h(b, M, 1770)
    facts_h(b, 2090, FACTS)
    circles_h(b, 3900, 1450, SHOTS, CAPS, 280)
    shock_h(b, 3180, 2130, 440)
    vignette(b, 0.32, 2.4)
    foot_h(b)
    return b.im.convert("RGB")


# ============================================================ 3 · BEYAZ
def bb_beyaz() -> Image.Image:
    b = _base("entrance-gate", 0.46, light=True)
    ink, sub = (30, 34, 40), (120, 124, 130)
    logos(b, white=False)
    dr = b.draw

    def script_word(d):
        d.text((b.p(M), b.p(1000)), "Yeni bir başlangıç", font=b.script(170, 700),
               fill=(150, 116, 56, 255), anchor="ls")
    overlay(b, script_word)

    fn, spn = fit_track(b, dr, ["MİA PARK OCEAN"], b.p(2540), 300, 0.03,
                        lambda s: b.cormorant(s, 600))

    def name(d):
        track(b, d, (b.p(M), cap_top(fn, b.p(1310))), "MİA PARK OCEAN", fn, ink,
              spn, "la")
    overlay(b, name)

    chips_h(b, M, 1530, ink)
    facts_h(b, 1890, FACTS, ink=ink, sub=sub)
    circles_h(b, 3900, 1450, SHOTS, CAPS, 280, sub=(28, 32, 38),
              plate=(252, 250, 246))
    shock_h(b, 3180, 2130, 440)
    foot_h(b)
    return b.im.convert("RGB")


# ============================================================ 4 · KLASİK
def bb_klasik() -> Image.Image:
    b = _base("aerial-pools", 0.5)
    logos(b)
    dr = b.draw

    fn, spn = fit_track(b, dr, ["MİA PARK OCEAN"], b.p(2560), 230, 0.16,
                        lambda s: b.marcellus(s))

    def name(d):
        track(b, d, (b.p(M), cap_top(fn, b.p(1020))), "MİA PARK OCEAN", fn, WHITE,
              spn, "la")
    overlay(b, name)

    def line2(d):
        d.line([b.p(M), b.p(1200), b.p(2560), b.p(1200)], fill=(*SAND, 160),
               width=max(2, b.p(2.4)))
        d.text((b.p(M), b.p(1400)), "İzmit MİA Bölgesi'nde yeni yaşam",
               font=b.cormorant(140, 400), fill=(*ICE, 250), anchor="ls")
    overlay(b, line2)

    chips_h(b, M, 1540)
    facts_h(b, 1900, FACTS)
    circles_h(b, 3900, 1450, SHOTS, CAPS, 280)
    shock_h(b, 3180, 2130, 440)
    vignette(b, 0.36, 2.4)
    foot_h(b)
    return b.im.convert("RGB")


# ============================================================ 5 · MODERN
def bb_modern() -> Image.Image:
    b = _base("courtyard-pools", 0.5)
    logos(b)
    dr = b.draw

    lines = ["1+0 · 1+1 · LOFT", "DAİRELER SATIŞTA"]
    fh, sph = fit_track(b, dr, lines, b.p(2560), 165, 0.02,
                        lambda s: b.mont(s, 800))
    step = cap_h(fh) * 1.42

    def head(d):
        for i, t in enumerate(lines):
            track(b, d, (b.p(M), b.p(1010) + i * step), t, fh, WHITE, sph, "la")
    overlay(b, head)

    fq, spq = fit_track(b, dr, ["BANKA YOK · KREDİ YOK · KEFİL YOK"], b.p(2200), 72,
                        0.18, lambda s: b.cond(s))

    def note(d):
        track(b, d, (b.p(M), b.p(1520)), "BANKA YOK · KREDİ YOK · KEFİL YOK", fq,
              (*SAND_HI, 250), spq, "la")
    overlay(b, note)

    facts_h(b, 1830, FACTS)
    circles_h(b, 3900, 1450, SHOTS, CAPS, 280)
    shock_h(b, 3180, 2130, 440)
    vignette(b, 0.32, 2.4)
    foot_h(b)
    return b.im.convert("RGB")


DESIGNS = [
    ("bilbord-1-gece", bb_gece, "gece · Playfair"),
    ("bilbord-2-oswald", bb_oswald, "gündüz · Oswald"),
    ("bilbord-3-beyaz", bb_beyaz, "beyaz · Cormorant"),
    ("bilbord-4-klasik", bb_klasik, "klasik · Marcellus"),
    ("bilbord-5-modern", bb_modern, "modern · Montserrat"),
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
        im.save(p, "JPEG", quality=93, subsampling=0, optimize=True, dpi=(DPI, DPI))
        sm = im.copy()
        sm.thumbnail((1500, 1500), Image.LANCZOS)
        sm.save(os.path.join(PREVIEW, f"{name}.jpg"), "JPEG", quality=88, optimize=True)
        print(f"  {name:<20} {label:<24} {im.width}x{im.height} px  "
              f"{os.path.getsize(p)/1e6:.1f} MB")
    print(f"\n  → {OUT}")


if __name__ == "__main__":
    main()
