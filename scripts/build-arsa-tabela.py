#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MİA PARK OCEAN — arsa çevre tabelaları (10 pano).

Arsanın DIŞINDAN okunan çit panoları. Yoldan geçen tek bir panoya bakar;
bu yüzden her pano tek mesaj taşır, kimlik ve iletişim ise hepsinde
tekrarlanır.

ÖLÇÜ: 3000 x 2000 mm, 1:1 ölçekte 50 dpi (5906 x 3937 px).

DALGA
─────
Kimlik bandı ve künye şeridi DÜZ ÇİZGİYLE bitmiyor: logonun kendi
dalgasıyla bitiyor. public/brand/wave-mask-end.png ile alt kenarı dalga
şeklinde kesilen okyanus gradyanı, üstüne de dalganın kendi renkli
kurdelesi (wave.png) biniyor — sitedeki kartların üst köşesindeki imzanın
tabela ölçeğindeki karşılığı. Elle çizilmiş "dalgamsı" eğri yok, kaynak
grafiğin pikselleri kullanılıyor.

YERLEŞİM AİLELERİ
─────────────────
On pano tek kalıptan çıkmıyor; fotoğrafın biçimi panodan panoya değişiyor:

    1  kimlik      tam sayfa gece render'ı
    2  yaşam       ÜÇ YUVARLAK fotoğraf, okyanus gradyanı üstünde
    3  ödeme       saf tipografi, dev rakam
    4  finansman   üç kart (Higgsfield)
    5  daireler    TEK BÜYÜK KARE fotoğraf + yanında liste
    6  sosyal      fotoğraf + perde (Higgsfield)
    7  manzara     tam sayfa (Higgsfield)
    8  ulaşım      açık zemin, sekiz veri kartı
    9  konum       gradyan + konum pini (Higgsfield)
   10  karekod     dev karekod + iki yuvarlak fotoğraf

BANT DÜZENİ (mm, üstten)
────────────────────────
    0 –  250   kimlik bandı gövdesi   MİA PARK OCEAN kilidi + "PROJE ALANI"
  250 –  380   dalga inişi            banttan panoya geçiş
  380 – 1620   mesaj alanı            güvenli alan
 1620 – 1750   dalga çıkışı
 1750 – 2000   künye şeridi           karekod · web · Instagram · telefon

Bantlar onunda da birebir aynı; panolar aynı hizada asılınca çit boyunca
kesintisiz iki dalga oluşur. "PROJE ALANI" ibaresi her panonun sağ
üstündedir.

    python scripts/build-arsa-tabela.py
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

Board, gradient, glow, scrim = bs.Board, bs.gradient, bs.glow, bs.scrim
cover, overlay, crisp, lockup = bs.cover, bs.overlay, bs.crisp, bs.lockup
track, fit, fit_track, qr_image = bs.track, bs.fit, bs.fit_track, bs.qr_image

WHITE, INK = bs.WHITE, bs.INK
DEEP, DARK, OCEAN = bs.MIA_DEEP, bs.MIA_DARK, bs.MIA_OCEAN
CYAN, AQUA, PALE, ICE = bs.MIA_CYAN, bs.MIA_AQUA, bs.MIA_PALE, bs.MIA_ICE
NAVY = bs.NAVY
CORAL = (242, 112, 75)
BONE = (246, 244, 240)

SITE, PHONES = bs.SITE, bs.PHONES
SELLER, SELLER_ROLE = bs.SELLER, bs.SELLER_ROLE
UNITS, DISTANCES, AMENITIES = bs.UNITS, bs.DISTANCES, bs.AMENITIES
TOTAL = bs.TOTAL_UNITS

IG = "@miaparkocean"
QR_URL = "https://miaparkocean.com/?utm_source=arsa"

SRC = os.path.join(ROOT, "signage-source", "hf-arsa")
OUT = os.path.join(ROOT, "tabela", "arsa")
PREVIEW = os.path.join(OUT, "onizleme")

W_MM, H_MM, DPI = 3000, 2000, 50
HEAD, FOOT = 250, 1750          # bant gövdelerinin sınırı
WAVE = 130                      # dalganın banttan taşma payı
SAFE_TOP, SAFE_BOT = 400, 1620  # yazının girebileceği alan
PAD = 120

BRAND = bs.BRAND
# Bant gradyanı: soldan sağa açılan okyanus. Marka paketindeki metalik
# gradyanın koyu ucu — beyaz yazı sağ uçta da okunsun diye en açık durak
# #1A7496'da kesiliyor.
BAND_STOPS = [(0.0, (4, 40, 58)), (0.34, (7, 88, 120)), (0.62, (18, 104, 140)),
              (0.84, (26, 116, 150)), (1.0, (12, 92, 126))]


def board() -> Board:
    return Board(W_MM, H_MM, DPI)


def cap_top(b: Board, f, cy: float) -> float:
    """Metni ortasından hizala — PIL üst kenardan yazıyor."""
    t, bo = f.getbbox("H")[1], f.getbbox("H")[3]
    return cy - (t + bo) / 2


def tr_upper(t: str) -> str:
    """Türkçe büyük harf. Python'un upper()'ı i -> I yapıyor, İ değil."""
    return t.replace("i", "İ").replace("ı", "I").upper()


def mid(b: Board):
    """Mesaj alanının kutusu (px) — dalga inişinin altı, çıkışının üstü."""
    return b.p(SAFE_TOP), b.p(SAFE_BOT), b.p(SAFE_BOT) - b.p(SAFE_TOP)


# ------------------------------------------------------------------ dalga
def _wave(name: str, size, flip: bool = False) -> Image.Image:
    im = Image.open(os.path.join(BRAND, name))
    if flip:
        im = im.transpose(Image.FLIP_TOP_BOTTOM)
    return im.resize(size, Image.LANCZOS)


def wave_band(b: Board, top: bool) -> None:
    """Okyanus gradyanlı bant — alt (ya da üst) kenarı logonun dalgası.

    Düz dikdörtgen bant panoyu ikiye bölüyordu. Burada gradyanın alfası
    wave-mask-end.png ile kesiliyor: bant dalga şeklinde bitiyor, altındaki
    tasarım olduğu gibi görünüyor. Üstüne dalganın KENDİ renkli kurdelesi
    biniyor; başka bir eğri çizilmiyor, kaynak grafiğin pikselleri
    kullanılıyor.
    """
    body = b.p(HEAD) if top else b.H - b.p(FOOT)
    wv = b.p(WAVE)
    h = body + wv
    y = 0 if top else b.p(FOOT) - wv

    g = gradient((b.W, h), BAND_STOPS, angle=0.92)
    g.alpha_composite(glow((b.W, h), b.W * (0.72 if top else 0.28), h * 0.5,
                           b.W * 0.42, AQUA, 0.20))

    a = np.zeros((h, b.W), np.uint8)
    m = np.asarray(_wave("wave-mask-end.png", (b.W, wv), flip=not top), np.uint8)
    if m.ndim == 3:
        m = m[:, :, -1]
    if top:
        a[:body] = 255
        a[body:] = m
    else:
        a[:wv] = m
        a[wv:] = 255
    g.putalpha(Image.fromarray(a, "L"))
    b.im.alpha_composite(g, (0, y))

    ribbon = _wave("wave.png", (b.W, wv), flip=not top).convert("RGBA")
    ribbon.putalpha(ribbon.split()[3].point(lambda v: round(v * 0.85)))
    b.im.alpha_composite(ribbon, (0, y + (body if top else 0)))


def bands(b: Board) -> None:
    """Kimlik bandı + künye şeridi. On panonun onunda da birebir aynı."""
    wave_band(b, True)
    wave_band(b, False)
    dr = b.draw

    lg = logo_h(b, 190)
    b.im.alpha_composite(lg, (b.p(PAD), (b.p(HEAD) - lg.height) // 2))
    f, sp = fit_track(b, dr, ["PROJE ALANI"], b.p(1000), 74, 0.22,
                      lambda s: b.sans(s, "700"))
    track(b, dr, (b.W - b.p(PAD), cap_top(b, f, b.p(HEAD) / 2)), "PROJE ALANI",
          f, WHITE, sp, "ra")

    y0, band = b.p(FOOT), b.H - b.p(FOOT)
    q = b.p(168)
    plate = q + b.p(22)
    px, py = b.p(PAD), y0 + (band - plate) // 2
    dr.rounded_rectangle([px, py, px + plate, py + plate], radius=b.p(10), fill=WHITE)
    b.im.alpha_composite(qr_image(QR_URL, q, DEEP), (px + b.p(11), py + b.p(11)))

    tx = px + plate + b.p(64)
    cy = y0 + band / 2
    f1, f2 = b.sans(50, "700"), b.sans(40, "600")
    dr.text((tx, cap_top(b, f1, cy - b.p(40))), f"{SITE}   ·   {IG}", font=f1, fill=WHITE)
    dr.text((tx, cap_top(b, f2, cy + b.p(44))), "   ·   ".join(PHONES), font=f2,
            fill=(*PALE, 255))

    fx = b.W - b.p(PAD)
    f3, sp3 = fit_track(b, dr, [SELLER], b.p(760), 42, 0.14, lambda s: b.sans(s, "700"))
    track(b, dr, (fx, cap_top(b, f3, cy - b.p(36))), SELLER, f3, WHITE, sp3, "ra")
    f4, sp4 = fit_track(b, dr, [SELLER_ROLE], b.p(760), 27, 0.22,
                        lambda s: b.sans(s, "600"))
    track(b, dr, (fx, cap_top(b, f4, cy + b.p(40))), SELLER_ROLE, f4, (*PALE, 255),
          sp4, "ra")


def logo_h(b: Board, h_mm: float, white: bool = True) -> Image.Image:
    """Kilidi YÜKSEKLİĞE göre ölçekle — lockup() genişlik alıyor, banttan
    taşırıyordu."""
    src = Image.open(os.path.join(BRAND, "logo-ocean-white.png" if white
                                  else "logo-ocean-trim.png"))
    box = src.getbbox()
    ar = (box[2] - box[0]) / (box[3] - box[1]) if box else src.width / src.height
    return lockup(round(b.p(h_mm) * ar), white=white)


# ------------------------------------------------------------ yapı taşları
def full_photo(b: Board, name: str, focus: float = 0.5) -> None:
    """Tam sayfa render — bantların altına da giriyor ki dalga fotoğrafın
    üstünde kessin, fotoğraf bandın altında bitmesin."""
    b.im.paste(cover(name, (b.W, b.H), focus), (0, 0))


def circle_photo(b: Board, name: str, cx: float, cy: float, d: float,
                 focus: float = 0.5, ring=None) -> None:
    """Yuvarlak fotoğraf — kenarında ince halka."""
    px = b.p(d)
    im = cover(name, (px, px), focus)
    mask = Image.new("L", (px, px), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, px - 1, px - 1], fill=255)
    x, y = b.p(cx) - px // 2, b.p(cy) - px // 2
    b.im.paste(im, (x, y), mask)
    r = b.p(d / 2)
    overlay(b, lambda d_: d_.ellipse([b.p(cx) - r, b.p(cy) - r, b.p(cx) + r,
                                      b.p(cy) + r],
                                     outline=ring or (*ICE, 150),
                                     width=max(3, b.p(3.5))))


def square_photo(b: Board, name: str, x: float, y: float, w: float, h: float,
                 focus: float = 0.5, r: float = 26) -> None:
    box = (b.p(x), b.p(y), b.p(x + w), b.p(y + h))
    im = cover(name, (box[2] - box[0], box[3] - box[1]), focus)
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, im.width - 1, im.height - 1],
                                           radius=b.p(r), fill=255)
    b.im.paste(im, box[:2], mask)


def field(b: Board, stops, angle: float = 0.35) -> None:
    """Panonun tamamını kaplayan gradyan zemin."""
    b.im.paste(gradient((b.W, b.H), stops, angle=angle), (0, 0))


def veil(b: Board, color=NAVY, a0: int = 0, a1: int = 215, frm: float = 0.28) -> None:
    ys = np.linspace(0, 1, b.H, dtype=np.float32)
    a = np.clip((ys - frm) / max(1 - frm, 1e-6), 0, 1) * (a1 - a0) + a0
    arr = np.zeros((b.H, 1, 4), np.float32)
    for c in range(3):
        arr[:, 0, c] = color[c]
    arr[:, 0, 3] = a
    b.im.alpha_composite(Image.fromarray(arr.astype(np.uint8), "RGBA")
                         .resize((b.W, b.H), Image.BILINEAR), (0, 0))


def flat_veil(b: Board, color, alpha: int) -> None:
    overlay(b, lambda d: d.rectangle([0, 0, b.W, b.H], fill=(*color, alpha)))


def headline(b: Board, lines, y: float, size: float, fill=WHITE, x: float = PAD,
             lh: float = 1.06, anchor: str = "la"):
    dr = b.draw
    f = fit(b, dr, lines, b.W - b.p(PAD * 2), size, lambda s: b.sans(s, "700"))
    step = f.size * lh
    px = b.p(x) if anchor == "la" else (b.W - b.p(x) if anchor == "ra" else b.W // 2)
    for i, t in enumerate(lines):
        dr.text((px, cap_top(b, f, b.p(y) + i * step)), t, font=f, fill=fill,
                anchor=anchor)
    return b.p(y) + (len(lines) - 1) * step


def eyebrow(b: Board, text: str, y: float, size: float = 46, fill=None,
            x: float = PAD, anchor: str = "la") -> None:
    dr = b.draw
    f, sp = fit_track(b, dr, [text], b.W - b.p(PAD * 2), size, 0.26,
                      lambda s: b.sans(s, "600"))
    px = b.p(x) if anchor == "la" else (b.W - b.p(x) if anchor == "ra" else b.W // 2)
    track(b, dr, (px, cap_top(b, f, b.p(y))), text, f, fill or (*AQUA, 255), sp, anchor)


def rule(b: Board, x: float, y: float, w: float, color=CORAL, t: float = 10) -> None:
    b.draw.rectangle([b.p(x), b.p(y), b.p(x + w), b.p(y + t)], fill=color)


# ================================================================= panolar
def p01_kimlik() -> Image.Image:
    """Tam sayfa gece render'ı. Fotoğraf bantların altına da giriyor;
    dalga onun üstünde kesiyor."""
    b = board()
    full_photo(b, "night-gate", 0.52)
    veil(b, NAVY, 0, 220, 0.22)
    headline(b, ["LÜKS ARTIK", "ULAŞILABİLİR."], 1030, 190)
    rule(b, PAD, 1385, 420)
    eyebrow(b, f"{TOTAL} KONUTLUK YAŞAM PROJESİ  ·  İZMİT MİA BÖLGESİ", 1500, 50,
            (*ICE, 255))
    bands(b)
    return b.im.convert("RGB")


def p02_yasam() -> Image.Image:
    """Üç yuvarlak fotoğraf. Kalıbı kıran pano bu: dikdörtgen yok."""
    b = board()
    field(b, [(0.0, (4, 40, 58)), (0.42, (7, 88, 120)), (1.0, (26, 116, 150))], 0.28)
    b.im.alpha_composite(glow((b.W, b.H), b.W * 0.5, b.H * 0.62, b.W * 0.62,
                              AQUA, 0.22))
    eyebrow(b, "KAPINIZIN ÖNÜNDE", 470, 52, (*AQUA, 255), anchor="ma")
    headline(b, ["SOSYAL YAŞAM"], 600, 130, WHITE, anchor="ma")

    shots = [("courtyard-pools", "YÜZME HAVUZU", 0.5),
             ("entrance-gate", "GENİŞ PEYZAJ", 0.55),
             ("balkondan-deniz", "YÜRÜYÜŞ YOLLARI", 0.45)]
    d, gap = 520, 190
    x0 = (W_MM - (d * 3 + gap * 2)) / 2 + d / 2
    dr = b.draw
    f, sp = fit_track(b, dr, [s[1] for s in shots], b.p(d + 120), 46, 0.16,
                      lambda s: b.sans(s, "600"))
    for i, (img, cap, foc) in enumerate(shots):
        cx = x0 + i * (d + gap)
        circle_photo(b, img, cx, 1080, d, foc)
        track(b, dr, (b.p(cx), cap_top(b, f, b.p(1440))), cap, f, (*ICE, 255), sp, "ma")
    bands(b)
    return b.im.convert("RGB")


def p03_odeme() -> Image.Image:
    """Saf tipografi. Otuz metreden okunacak tek şey: 60."""
    b = board()
    field(b, [(0.0, (7, 88, 120)), (0.5, (26, 116, 150)), (1.0, (44, 148, 180))], 0.75)
    b.im.alpha_composite(glow((b.W, b.H), b.W * 0.24, b.H * 0.72, b.W * 0.55,
                              ICE, 0.26))
    gh = b.p(H_MM * 0.5)
    ghost = cover("entrance-gate", (b.W, gh), 0.45)
    ramp = np.clip(np.linspace(-0.4, 1.0, gh), 0, 1) ** 1.7 * 42
    ghost.putalpha(Image.fromarray(
        np.repeat(ramp[:, None], b.W, axis=1).astype(np.uint8), "L"))
    b.im.alpha_composite(ghost, (0, b.H - gh))

    eyebrow(b, "TASARRUFA DAYALI FAİZSİZ FİNANSMAN", 490, 52, (*ICE, 255),
            anchor="ma")
    headline(b, ["VADE FARKSIZ"], 640, 124, WHITE, anchor="ma")
    headline(b, ["60 AY TAKSİT"], 900, 290, WHITE, anchor="ma")

    pw, ph = 1520, 140
    px, py = (W_MM - pw) / 2, 1270
    dr = b.draw
    dr.rounded_rectangle([b.p(px), b.p(py), b.p(px + pw), b.p(py + ph)],
                         radius=b.p(ph / 2), fill=CORAL)
    f, sp = fit_track(b, dr, ["PEŞİN FİYATINA VADE"], b.p(pw - 140), 60, 0.20,
                      lambda s: b.sans(s, "700"))
    track(b, dr, (b.W // 2, cap_top(b, f, b.p(py + ph / 2))), "PEŞİN FİYATINA VADE",
          f, WHITE, sp, "ma")
    bands(b)
    return b.im.convert("RGB")


def p05_daireler() -> Image.Image:
    """Tek büyük kare fotoğraf solda, tipler sağda satır satır."""
    b = board()
    field(b, [(0.0, WHITE), (0.55, (240, 251, 253)), (1.0, PALE)], 0.6)
    sq = SAFE_BOT - SAFE_TOP
    square_photo(b, "entrance-gate", PAD, SAFE_TOP, sq, sq, 0.5, r=30)

    x = PAD + sq + 120
    dr = b.draw
    eyebrow(b, "DAİRE TİPLERİ", SAFE_TOP + 40, 48, (*DEEP, 255), x=x)
    rule(b, x, SAFE_TOP + 110, 260, CORAL)

    rows = [(u[0], tr_upper(u[1].replace(u[0], "", 1).strip()), u[2], u[3])
            for u in UNITS]
    fc = b.sans(96, "700")
    fl, spl = fit_track(b, dr, [r[1] for r in rows], b.p(560), 38, 0.14,
                        lambda s: b.sans(s, "600"))
    fm = b.sans(78, "700")
    fa = b.sans(36, "600")
    y = SAFE_TOP + 250
    step = 250
    for i, (code, tag, area, adet) in enumerate(rows):
        yy = y + i * step
        dr.text((b.p(x), cap_top(b, fc, b.p(yy))), code, font=fc, fill=DEEP)
        track(b, dr, (b.p(x + 300), cap_top(b, fl, b.p(yy - 34))), tag, fl,
              (*DARK, 255), spl)
        dr.text((b.p(x + 300), cap_top(b, fa, b.p(yy + 42))), f"{adet} ADET",
                font=fa, fill=(*OCEAN, 255))
        dr.text((b.W - b.p(PAD), cap_top(b, fm, b.p(yy))), area, font=fm,
                fill=INK, anchor="ra")
        if i < len(rows) - 1:
            dr.rectangle([b.p(x), b.p(yy + step / 2 - 2), b.W - b.p(PAD),
                          b.p(yy + step / 2 + 2)], fill=(*PALE, 255))
    bands(b)
    return b.im.convert("RGB")


def p08_ulasim() -> Image.Image:
    """Sekiz mesafe. 'Neredeyim' değil 'neye yakınım'."""
    b = board()
    field(b, [(0.0, WHITE), (0.5, (240, 251, 253)), (1.0, PALE)], 0.7)
    eyebrow(b, "HER YERE YAKIN", SAFE_TOP + 30, 50, (*DEEP, 255))
    headline(b, ["ULAŞIM"], SAFE_TOP + 150, 140, DEEP)
    rule(b, PAD, SAFE_TOP + 250, 380)

    cw, ch, gx, gy = 660, 300, 30, 40
    x0 = (W_MM - (cw * 4 + gx * 3)) / 2
    dr = b.draw
    fn, _ = fit_track(b, dr, [d[0] for d in DISTANCES], b.p(cw - 80), 48, 0.04,
                      lambda s: b.sans(s, "600"))
    fv = b.sans(104, "700")
    for i, (name, mins) in enumerate(DISTANCES):
        cx = x0 + (i % 4) * (cw + gx)
        cy = SAFE_TOP + 420 + (i // 4) * (ch + gy)
        dr.rounded_rectangle([b.p(cx), b.p(cy), b.p(cx + cw), b.p(cy + ch)],
                             radius=b.p(18), fill=WHITE, outline=(*PALE, 255),
                             width=max(2, b.p(2)))
        dr.text((b.p(cx + 40), cap_top(b, fn, b.p(cy + 92))), name, font=fn, fill=INK)
        dr.text((b.p(cx + cw - 40), cap_top(b, fv, b.p(cy + 214))), mins, font=fv,
                fill=DEEP, anchor="ra")
    bands(b)
    return b.im.convert("RGB")


def p10_karekod() -> Image.Image:
    """Dev karekod solda, iki yuvarlak fotoğraf sağda."""
    b = board()
    full_photo(b, "night-gate", 0.35)
    flat_veil(b, NAVY, 218)

    q = b.p(560)
    plate = q + b.p(64)
    px, py = b.p(PAD + 60), b.p(SAFE_TOP + 190)
    b.draw.rounded_rectangle([px, py, px + plate, py + plate], radius=b.p(24),
                             fill=WHITE)
    b.im.alpha_composite(qr_image(QR_URL, q, DEEP), (px + b.p(32), py + b.p(32)))

    x = PAD + 60 + 620 + 130
    eyebrow(b, "BİLGİ VE RANDEVU İÇİN", SAFE_TOP + 150, 50, (*AQUA, 255), x=x)
    headline(b, ["KAREKODU", "OKUTUN"], SAFE_TOP + 300, 128, WHITE, x=x)
    dr = b.draw
    items = ["DAİRE PLANLARI", "ÖDEME SEÇENEKLERİ", "SANAL TUR"]
    f, sp = fit_track(b, dr, items, b.p(900), 46, 0.12, lambda s: b.sans(s, "600"))
    for i, t in enumerate(items):
        yy = SAFE_TOP + 700 + i * 110
        dr.rectangle([b.p(x), b.p(yy - 12), b.p(x + 26), b.p(yy + 14)], fill=CORAL)
        track(b, dr, (b.p(x + 64), cap_top(b, f, b.p(yy))), t, f, (*ICE, 255), sp)

    circle_photo(b, "courtyard-pools", W_MM - PAD - 230, SAFE_TOP + 300, 460, 0.5)
    circle_photo(b, "balkondan-deniz", W_MM - PAD - 430, SAFE_TOP + 860, 400, 0.45)
    bands(b)
    return b.im.convert("RGB")


# ---------------------------------------------------- Higgsfield panoları
def clean_seam(b: Board, limit: float = 120) -> None:
    """Üretimin bant sınırına koyduğu ince şeridi ölç ve sil.

    Satır yatayda düz kaldığı sürece siliniyor; fotoğrafla başlayan
    panolara dokunulmuyor. Dalga bandı artık daha aşağı indiği için
    ölçüm de o sınırdan başlıyor.
    """
    a = np.asarray(b.im.convert("RGB"), np.float32)
    top, bot, lim = b.p(HEAD), b.p(FOOT), b.p(limit)
    flat = lambda y: a[y].std(axis=0).max() < 6
    n = 0
    while n < lim and flat(top + n):
        n += 1
    if n:
        b.im.paste(b.im.crop((0, top + n, b.W, top + n + 1)).resize((b.W, n)), (0, top))
    m = 0
    while m < lim and flat(bot - 1 - m):
        m += 1
    if m:
        b.im.paste(b.im.crop((0, bot - m - 1, b.W, bot - m)).resize((b.W, m)),
                   (0, bot - m))


def from_ai(name: str) -> Image.Image:
    """Üretilen panoyu 3:2'ye oturt, dikişi temizle, dalga bantlarını bas."""
    im = Image.open(os.path.join(SRC, name + ".png")).convert("RGB")
    b = board()
    s = max(b.W / im.width, b.H / im.height)
    im = im.resize((max(b.W, round(im.width * s)), max(b.H, round(im.height * s))),
                   Image.LANCZOS)
    x, y = (im.width - b.W) // 2, (im.height - b.H) // 2
    b.im.paste(im.crop((x, y, x + b.W, y + b.H)).convert("RGBA"), (0, 0))
    clean_seam(b)
    bands(b)
    return b.im.convert("RGB")


BOARDS = [
    ("arsa-01-proje-alani", p01_kimlik),
    ("arsa-02-yasam",       p02_yasam),
    ("arsa-03-odeme",       p03_odeme),
    ("arsa-04-finansman",   lambda: from_ai("arsa-4-finansman")),
    ("arsa-05-daireler",    p05_daireler),
    ("arsa-06-sosyal",      lambda: from_ai("arsa-6-sosyal")),
    ("arsa-07-manzara",     lambda: from_ai("arsa-7-manzara")),
    ("arsa-08-ulasim",      p08_ulasim),
    ("arsa-09-konum",       lambda: from_ai("arsa-9-konum")),
    ("arsa-10-karekod",     p10_karekod),
]

# Seçim için üretilen ek panolar. Aynı ölçü, aynı dalga bandı — hangisi
# seçilirse çite doğrudan girer, sıraya da sokulabilir.
EXTRA = [
    ("arsa-11-ic-mekan",    lambda: from_ai("arsa-11-ic-mekan")),
    ("arsa-12-dis-mekan",   lambda: from_ai("arsa-12-dis-mekan")),
    ("arsa-13-sifir-faiz",  lambda: from_ai("arsa-13-sifir-faiz")),
    ("arsa-14-pesinat",     lambda: from_ai("arsa-14-pesinat")),
    ("arsa-15-burada",      lambda: from_ai("arsa-15-burada")),
]


def fence_run(paths) -> None:
    """On panoyu yan yana dizip çitin dışarıdan görünüşünü çıkarır."""
    ims = [Image.open(p) for p in paths]
    h = 460
    ws = [round(im.width * h / im.height) for im in ims]
    gap = 10
    run = Image.new("RGB", (sum(ws) + gap * (len(ims) - 1), h), (232, 236, 238))
    x = 0
    for im, w in zip(ims, ws):
        run.paste(im.resize((w, h), Image.LANCZOS), (x, 0))
        x += w + gap
    run.save(os.path.join(PREVIEW, "cit-dizilimi.jpg"), quality=88, optimize=True)
    print(f"  -> onizleme/cit-dizilimi.jpg ({run.width}x{run.height})")


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(PREVIEW, exist_ok=True)
    print(f"Arsa tabelaları — {W_MM}x{H_MM} mm @ {DPI} dpi "
          f"({round(W_MM / 25.4 * DPI)}x{round(H_MM / 25.4 * DPI)} px)")
    made = []
    for name, fn in BOARDS + [e for e in EXTRA
                              if os.path.exists(os.path.join(SRC, e[0] + ".png"))]:
        im = fn()
        im.save(os.path.join(OUT, name + ".jpg"), quality=92, subsampling=0,
                optimize=True, dpi=(DPI, DPI))
        im.resize((im.width // 5, im.height // 5), Image.LANCZOS).save(
            os.path.join(PREVIEW, name + ".jpg"), quality=88, optimize=True)
        print(f"  -> {name}.jpg")
        made.append(os.path.join(PREVIEW, name + ".jpg"))
    fence_run(made[:len(BOARDS)])


if __name__ == "__main__":
    main()
