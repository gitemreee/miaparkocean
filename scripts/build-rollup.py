#!/usr/bin/env python3
"""
MİA PARK OCEAN — roll-up serisi.

Referans olarak verilen iki emlak roll-up'ının düzenini kurar: açık zemin,
üstte logo bandı, büyük render, renkli bilgi şeridi, fotoğraf ızgarası,
ikonlu özellik listesi, altta koyu iletişim bandı. Yoğun bilgi düzeni —
roll-up satış masasının yanında durur, insan yanına gelip okur.

    1 · proje      render + bilgi şeridi + daire tipleri + ızgara + ikonlar
    2 · odeme      ödeme planı, büyük rakamlar, madde listesi
    3 · daireler   üç daire tipi, her biri fotoğraf + m² + özellik
    4 · yasam      ortak alanlar, fotoğraf ızgarası + ikon listesi

İKİ LOGO
────────
Üstte MİA PARK OCEAN kilidi, altta künye bandında OCEAN GAYRİMENKUL.
Ocean logosu 298 px; 75 mm'ye kadar birebir basılıyor, künye ölçüsü ona
göre seçildi.

DAİRE TİPLERİ
─────────────
2+1 Bahçe Dubleks panolarda GÖSTERİLMİYOR. Kalan üç tip pazarlanıyor.
Projenin toplam 600 daire olduğu bilgisi ayrı bir olgu; tip listesinin
toplamı değil.

Ölçü: 800 x 2000 mm, 1:1 ölçekte 100 dpi. Kaset alt 40 mm'yi yutar.

    python scripts/build-rollup.py
    python scripts/build-rollup.py proje       # tek tasarım
"""

from __future__ import annotations

import importlib.util
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

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
M = 44                                    # yan pay
FOOT_Y = 1800                             # künye bandının üst kenarı

# ---------------------------------------------------------------- palet
# Render'lar SICAK: mor-turuncu gün batımı, kehribar iç ışıklar, taş cephe.
# Marka teali (#095678) bu görselin üstünde kavga ediyordu; zemin
# neredeyse siyah laciverte indirildi, sıcak görselin altında sessiz
# kalıyor. Tek kromatik vurgu açık ŞAMPANYA — hardal (#BF943F) altın
# değil çamur okunuyordu ve koyu zeminde kontrastı yetmiyordu.
WHITE = (255, 255, 255)
PAPER = (247, 244, 238)          # sıcak kırık beyaz; soğuk beyaz görselle uyuşmuyor
INK = (24, 30, 38)
GREY = (122, 131, 144)
LINE = (222, 217, 208)
DEEP = (10, 24, 34)              # zemin, panel, künye
MID = (16, 40, 55)               # üst üste binen panel
SAND = (223, 199, 154)           # TEK vurgu: ince çizgi, küçük etiket, madde
SAND_DIM = (176, 150, 106)       # açık zeminde saç teli
OCEAN = bs.MIA_OCEAN

SITE, PHONES = bs.SITE, bs.PHONES
SELLER, SELLER_ROLE = bs.SELLER, bs.SELLER_ROLE
QR_URL = "https://miaparkocean.com/?utm_source=rollup"

# 2+1 Bahçe Dubleks panolarda gösterilmiyor.
UNITS = [u for u in bs.UNITS if not u[1].startswith("2+1")]
TOTAL = bs.TOTAL_UNITS

PRICES = [("1+0", "699.000", "29.900"), ("1+1", "999.000", "39.900")]


def board() -> Board:
    b = Board(W_MM, H_MM, DPI)
    b.im = Image.new("RGBA", (b.W, b.H), (*PAPER, 255))
    return b


def cap_h(f) -> float:
    bb = f.getbbox("H")
    return bb[3] - bb[1]


def cap_top(f, cy: float) -> float:
    bb = f.getbbox("H")
    return cy - (bb[1] + bb[3]) / 2


def ocean_logo(b: Board, w_mm: float, white: bool = False) -> Image.Image:
    """OCEAN GAYRİMENKUL logosu. 298 px kaynak — 75 mm'ye kadar birebir."""
    name = "ocean-logo-white.png" if white else "ocean-logo.webp"
    im = Image.open(os.path.join(ROOT, "public", name)).convert("RGBA")
    if not white:
        # webp'te alfa yok; beyazı saydama çeviriyoruz ki açık zemine otursun.
        a = np.asarray(im.convert("RGB"), np.float32)
        alpha = 255 - a.min(axis=2)
        im = Image.merge("RGBA", (*im.convert("RGB").split(),
                                  Image.fromarray(alpha.astype(np.uint8), "L")))
    box = im.getbbox()
    if box:
        im = im.crop(box)
    return crisp(im, b.p(w_mm))


# ------------------------------------------------------------------ ikonlar
def icon(d, kind, cx, cy, r, col, t):
    if kind == "pin":
        d.ellipse([cx - r * .62, cy - r * .92, cx + r * .62, cy + r * .32],
                  outline=col, width=t)
        d.polygon([(cx - r * .3, cy + r * .12), (cx + r * .3, cy + r * .12),
                   (cx, cy + r * .95)], fill=col)
        d.ellipse([cx - r * .2, cy - r * .5, cx + r * .2, cy - r * .1],
                  outline=col, width=t)
    elif kind == "tel":
        d.rounded_rectangle([cx - r * .5, cy - r * .92, cx + r * .5, cy + r * .92],
                            radius=int(r * .2), outline=col, width=t)
        d.line([cx - r * .18, cy + r * .62, cx + r * .18, cy + r * .62],
               fill=col, width=t)
    elif kind == "web":
        d.ellipse([cx - r * .9, cy - r * .9, cx + r * .9, cy + r * .9],
                  outline=col, width=t)
        d.ellipse([cx - r * .36, cy - r * .9, cx + r * .36, cy + r * .9],
                  outline=col, width=t)
        d.line([cx - r * .9, cy, cx + r * .9, cy], fill=col, width=t)


# ------------------------------------------------------------------ parçalar
def hero_bg(b: Board, name: str, h: float, focus: float = 0.5) -> None:
    """Arka plandaki tek ana fotoğraf. Alt yarısı yazı için koyulaşır."""
    im = cover(name, (b.W, b.p(h)), focus)
    im.alpha_composite(scrim((b.W, b.p(h)), [
        (0.0, (4, 18, 32, 95)), (0.26, (4, 18, 32, 38)),
        (0.44, (4, 18, 32, 120)), (0.56, (4, 18, 32, 212)),
        (0.72, (4, 18, 32, 235)), (1.0, (4, 18, 32, 246)),
    ]))
    b.im.alpha_composite(im, (0, 0))


def banner(b: Board, w: float = 424, h: float = 176, notch: float = 38) -> None:
    """Tepeden sarkan çentikli bayrak; MİA kilidi içinde. Referansın açılışı."""
    x0, x1 = b.p((W_MM - w) / 2), b.p((W_MM + w) / 2)
    cx = (x0 + x1) // 2

    def paint(d):
        d.polygon([(x0, 0), (x1, 0), (x1, b.p(h)), (cx, b.p(h + notch)),
                   (x0, b.p(h))], fill=(*DEEP, 255))
        # Kenarda kalın hardal bant vardı; tek saç teli çizgi yeterli.
        d.line([(x0, 0), (x0, b.p(h)), (cx, b.p(h + notch)), (x1, b.p(h)), (x1, 0)],
               fill=(*SAND, 210), width=max(2, b.p(0.8)), joint="curve")
    overlay(b, paint)

    lg = lockup(b.p(224), white=True)
    b.im.alpha_composite(lg, (cx - lg.width // 2, b.p(14)))


def stack_head(b: Board, y: float, lines, size: float = 74) -> float:
    """Üst üste yığılmış dev manşet — referansın MODERN / HOME / FOR SALE'i.

    Satır adımı puntonun değil BÜYÜK HARF YÜKSEKLİĞİNİN katı; yığın ancak
    böyle blok gibi duruyor, arada boşluk kalmıyor.
    """
    dr = b.draw
    f, sp = fit_track(b, dr, [t for t, _ in lines], b.p(W_MM - M * 2), size, 0.02,
                      lambda s: b.sans(s, "700"))
    step = cap_h(f) * 1.18

    def paint(d):
        for i, (t, colr) in enumerate(lines):
            track(b, d, (b.p(M), b.p(y) + i * step), t, f, colr, sp)
    overlay(b, paint)
    return (b.p(y) + (len(lines) - 1) * step + cap_h(f)) * 25.4 / b.dpi


def three_cards(b: Board, y: float, items, ph: float = 168,
                cap: float = 132) -> float:
    """Üç fotoğraf, altlarında renkli künye paneli. Ortadaki altın."""
    gap = 10
    cw = (W_MM - M * 2 - gap * 2) / 3
    dr = b.draw
    ft = fit(b, dr, [t for t, _, _ in items], b.p(cw - 18), 17,
             lambda s: b.serif(s, "600"))
    fa, spa = fit_track(b, dr, [a for _, a, _ in items], b.p(cw - 18), 8.6, 0.16,
                        lambda s: b.sans(s, "700"))
    fb = b.sans(9.6, "400")

    for i, (title, area, note) in enumerate(items):
        x = M + i * (cw + gap)
        pw, phh = b.p(cw), b.p(ph)
        im = cover(SHOTS[i], (pw, phh), 0.5)
        b.im.alpha_composite(im, (b.p(x), b.p(y)))

        def card(d, x=x, title=title, area=area, note=note,
                 ink=(*WHITE, 255), soft=(214, 206, 192, 240)):
            d.rectangle([b.p(x), b.p(y + ph), b.p(x + cw), b.p(y + ph + cap)],
                        fill=(*DEEP, 255))
            d.rectangle([b.p(x), b.p(y + ph), b.p(x + cw), b.p(y + ph) + b.p(2)],
                        fill=(*SAND, 255))
            d.text((b.p(x + cw / 2), b.p(y + ph + 34)), title, font=ft, fill=ink,
                   anchor="ms")
            track(b, d, (b.p(x + cw / 2), b.p(y + ph + 46)), area, fa, soft, spa, "ma")
            for k, ln in enumerate(wrap(d, note, fb, b.p(cw - 22))[:3]):
                d.text((b.p(x + cw / 2), b.p(y + ph + 82 + k * 16)), ln, font=fb,
                       fill=soft, anchor="ms")
        overlay(b, card)
    return y + ph + cap


def price_block(b: Board, y: float, label: str, big: str, sub: str,
                bullets) -> None:
    """Solda büyük rakam, sağda madde listesi — referansın beyaz bölümü."""
    dr = b.draw
    fl, spl = fit_track(b, dr, [label], b.p(300), 10, 0.24,
                        lambda s: b.sans(s, "700"))
    fn = fit(b, dr, [big], b.p(340), 52, lambda s: b.serif(s, "700"))
    fs = b.sans(12.5, "400")
    fbu, spbu = fit_track(b, dr, bullets, b.p(280), 11, 0.10,
                          lambda s: b.sans(s, "700"))

    def paint(d):
        track(b, d, (b.p(M), b.p(y)), label, fl, (*GREY, 255), spl)
        wn = d.textlength(big, font=fn)
        d.text((b.p(M), b.p(y + 62)), big, font=fn, fill=(*DEEP, 255), anchor="ls")
        d.text((b.p(M) + wn + b.p(4), b.p(y + 62)), "₺", font=b.sans(18, "700"),
               fill=(*SAND_DIM, 255), anchor="ls")
        for k, ln in enumerate(wrap(d, sub, fs, b.p(300))):
            d.text((b.p(M), b.p(y + 90 + k * 20)), ln, font=fs, fill=(*GREY, 255),
                   anchor="ls")
        bx = b.p(430)
        for k, t in enumerate(bullets):
            yy = b.p(y - 4 + k * 34)
            # Açık zeminde açık şampanya görünmüyor; koyu tonu.
            d.ellipse([bx, yy, bx + b.p(8), yy + b.p(8)], fill=(*SAND_DIM, 255))
            track(b, d, (bx + b.p(18), cap_top(fbu, yy + b.p(4))), t, fbu,
                  (*INK, 255), spbu)
    overlay(b, paint)


def burst(b: Board, cx: float, cy: float, r: float, lines,
          teeth: int = 30, inner: float = 0.87) -> None:
    """Şok rozeti — perakende baskının testere kenarlı etiketi.

    Diş sayısı çift ve çok tutuluyor: az dişli yıldız "yıldız" gibi
    okunuyor, otuz diş klasik şok etiketini veriyor.
    """
    import math
    pts = []
    for i in range(teeth * 2):
        rad = b.p(r) if i % 2 == 0 else b.p(r * inner)
        a = math.pi * 2 * i / (teeth * 2) - math.pi / 2
        pts.append((b.p(cx) + rad * math.cos(a), b.p(cy) + rad * math.sin(a)))

    dr = b.draw
    f, sp = fit_track(b, dr, lines, b.p(r * 1.42), 17, 0.06,
                      lambda s_: b.sans(s_, "700"))
    step = cap_h(f) * 1.62

    def paint(d):
        d.polygon(pts, fill=(*SAND, 255))
        d.ellipse([b.p(cx - r * inner + 5), b.p(cy - r * inner + 5),
                   b.p(cx + r * inner - 5), b.p(cy + r * inner - 5)],
                  outline=(*DEEP, 90), width=max(1, b.p(0.6)))
        y0 = b.p(cy) - (len(lines) - 1) * step / 2
        for i, t in enumerate(lines):
            track(b, d, (b.p(cx), cap_top(f, y0 + i * step)), t, f, (*DEEP, 255),
                  sp, "ma")
    overlay(b, paint)


def contact_footer(b: Board) -> None:
    """Koyu iletişim bandı: Ocean logosu, konum, telefon, web, karekod."""
    y0 = b.p(FOOT_Y)

    def band(d):
        d.rectangle([0, y0, b.W, b.H], fill=(*DEEP, 255))
        d.rectangle([0, y0, b.W, y0 + b.p(5)], fill=(*SAND, 255))
    overlay(b, band)

    lg = ocean_logo(b, 82, white=True)
    b.im.alpha_composite(lg, (b.p(M), y0 + b.p(34)))

    dr = b.draw
    fr, spr = fit_track(b, dr, [SELLER_ROLE], b.p(200), 6.4, 0.20,
                        lambda s: b.sans(s, "700"))
    rows = [("pin", "İzmit MİA Bölgesi · Kocaeli"),
            ("tel", "  ·  ".join(PHONES)),
            ("web", f"{SITE}  ·  @miaparkocean")]
    fi = b.sans(12, "700")

    def paint(d):
        track(b, d, (b.p(M), y0 + b.p(84)), SELLER_ROLE, fr, (*bs.MIA_LIGHT, 235), spr)
        d.line([b.p(178), y0 + b.p(30), b.p(178), y0 + b.p(96)],
               fill=(*bs.MIA_DARK, 255), width=max(1, b.p(0.6)))
        for k, (kind, txt) in enumerate(rows):
            yy = y0 + b.p(42 + k * 30)
            icon(d, kind, b.p(206), yy, b.p(8), (*SAND, 255), max(2, b.p(0.8)))
            d.text((b.p(226), yy + b.p(4)), txt, font=fi, fill=WHITE, anchor="ls")
    overlay(b, paint)

    qs = b.p(58)
    qx, qy = b.W - b.p(M) - qs, y0 + b.p(36)

    def plate(d):
        d.rounded_rectangle([qx - b.p(5), qy - b.p(5), qx + qs + b.p(5),
                             qy + qs + b.p(5)], radius=b.p(4),
                            fill=(255, 255, 255, 252))
    overlay(b, plate)
    b.im.alpha_composite(qr_image(QR_URL, qs, DEEP), (qx, qy))


# ==================================================================== tasarım
FINE = "TASARRUFA DAYALI FAİZSİZ FİNANSMAN · KOOPBİS KAYITLI KOOPERATİF"

SHOTS = ["ic-mekan/01-1plus0-salon", "ic-mekan/05-1plus1-salon",
         "ic-mekan/07-1plus1-mutfak"]

CARDS = [("1+0 Salon", "28 m² · 472 DAİRE", "Açık plan salon, ankastre mutfak."),
         ("1+1 Salon", "50 m² · 96 DAİRE", "Ayrı yatak odası, geniş balkon."),
         ("1+1 Mutfak", "50 m² · 96 DAİRE", "Ankastre set, geniş tezgâh.")]


def ru_kimlik() -> Image.Image:
    b = board()
    hero_bg(b, "night-gate", 1120, 0.5)
    banner(b)
    stack_head(b, 812, [("1+0 ve 1+1", (*WHITE, 255)), ("DAİRELER", (*WHITE, 255)),
                        ("SATIŞTA", (*WHITE, 255))], 76)
    burst(b, 650, 946, 96, ["KREDİ YOK", "BANKA YOK", "KEFİL YOK"])
    three_cards(b, 1086, CARDS)
    price_block(b, 1470, "PEŞİNAT", "699.000",
                "1+0 daire için. Kalanı 60 aya kadar sabit taksitle.",
                ["60 AY VADE FARKSIZ", "%0 FAİZ", "SABİT TAKSİT",
                 "ARA ÖDEME YOK", "KOOPBİS KAYITLI"])

    f, sp = fit_track(b, b.draw, [FINE], b.p(W_MM - M * 2), 9.4, 0.18,
                      lambda s_: b.sans(s_, "700"))

    def fine(d):
        d.line([b.p(M), b.p(1656), b.W - b.p(M), b.p(1656)], fill=(*LINE, 255),
               width=max(1, b.p(0.5)))
        track(b, d, (b.p(W_MM / 2), b.p(1692)), FINE, f, (*GREY, 255), sp, "ma")
    overlay(b, fine)

    contact_footer(b)
    return b.im.convert("RGB")


DESIGNS = [("rollup-1-kimlik", ru_kimlik, "kimlik")]


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(PREVIEW, exist_ok=True)
    for name, fn, label in DESIGNS:
        im = fn()
        p = os.path.join(OUT, f"{name}.jpg")
        im.save(p, "JPEG", quality=94, subsampling=0, optimize=True, dpi=(DPI, DPI))
        small = im.copy()
        small.thumbnail((1400, 1400), Image.LANCZOS)
        small.save(os.path.join(PREVIEW, f"{name}.jpg"), "JPEG", quality=88,
                   optimize=True)
        print(f"  {name:<22} {label:<16} {im.width}x{im.height} px  "
              f"{os.path.getsize(p)/1e6:.1f} MB")
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
        print(f"  {name:<22} zemin {os.path.getsize(bp)/1e6:5.1f} MB · "
              f"yazı {os.path.getsize(tp)/1e6:5.1f} MB")
    print(f"\n  → {SRC_OUT}")


if __name__ == "__main__":
    if "--katman" in sys.argv:
        build_layers()
    else:
        main()
