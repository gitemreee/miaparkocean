#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MİA PARK OCEAN — arsa çevre tabelaları (10 pano).

Arsanın DIŞINDAN okunan çit panoları: yoldan geçen görüyor, o yüzden her
pano tek bir mesaj taşıyor ve her panonun üstünde aynı kimlik bandı var.

ÖLÇÜ: 3000 x 2000 mm, 1:1 ölçekte 50 dpi (5906 x 3937 px).

BANT DÜZENİ (mm, üstten)
────────────────────────
    0 –  280   kimlik bandı   MİA PARK OCEAN kilidi + "PROJE ALANI"
  280 – 1740   mesaj alanı    panodan panoya değişen tek konu
 1740 – 2000   künye şeridi   karekod, web, Instagram, telefonlar, satıcı

Kimlik bandı ve künye şeridi ONUNDA DA AYNI: paneller yan yana asılınca
çit boyunca kesintisiz iki mavi çizgi oluşuyor, set tek tasarım gibi
okunuyor. "PROJE ALANI" ibaresi bu yüzden tek bir panoda değil, HER
PANODA duruyor — hangi panonun önünden geçerseniz geçin arsanın kime ait
olduğu yazıyor.

ÜRETİM
──────
Altı pano bu betikte çiziliyor. Dördü (finansman, sosyal yaşam, manzara,
konum) Higgsfield ile üretildi ve signage-source/hf-arsa/ altında duruyor;
istemleri tabela/arsa/PROMPT.md'de. Kaynağı ne olursa olsun kimlik bandını
ve künye şeridini hep bu betik basıyor — logo yapay zekâya çizdirilmiyor.

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
HEAD, FOOT = 280, 1740          # kimlik bandının altı / künye şeridinin üstü
PAD = 110


def board() -> Board:
    return Board(W_MM, H_MM, DPI)


# --------------------------------------------------------- ortak bantlar
def tr_upper(t: str) -> str:
    """Türkçe büyük harf. Python'un upper()'ı i -> I yapıyor, İ değil."""
    return t.replace("i", "İ").replace("ı", "I").upper()


def logo_h(b: Board, h_mm: float, white: bool = True) -> Image.Image:
    """Kilidi YÜKSEKLİĞE göre ölçekle.

    lockup() genişlik alıyor; 280 mm'lik kimlik bandında genişlikten
    gitmek kilidi bandın altına taşırıyordu. Kaynak oranını ölçüp
    genişliği yükseklikten türetiyoruz.
    """
    src = Image.open(os.path.join(bs.BRAND,
                                  "logo-ocean-white.png" if white else "logo-ocean-trim.png"))
    box = src.getbbox()
    ar = (box[2] - box[0]) / (box[3] - box[1]) if box else src.width / src.height
    return lockup(round(b.p(h_mm) * ar), white=white)


def bands(b: Board) -> None:
    """Kimlik bandı + künye şeridi. On panonun onunda da birebir aynı."""
    dr = b.draw
    dr.rectangle([0, 0, b.W, b.p(HEAD)], fill=DEEP)
    dr.rectangle([0, b.p(FOOT), b.W, b.H], fill=DEEP)

    # --- üst: logo kilidi solda, PROJE ALANI sağda
    lg = logo_h(b, 216)
    b.im.alpha_composite(lg, (b.p(PAD), (b.p(HEAD) - lg.height) // 2))
    f, sp = fit_track(b, dr, ["PROJE ALANI"], b.p(1100), 78, 0.20,
                      lambda s: b.sans(s, "700"))
    track(b, dr, (b.W - b.p(PAD), cap_top(b, f, b.p(HEAD) / 2)), "PROJE ALANI",
          f, WHITE, sp, "ra")

    # --- alt: karekod, iletişim, satıcı
    y0, band = b.p(FOOT), b.p(H_MM - FOOT)
    q = b.p(180)
    plate = q + b.p(24)
    px, py = b.p(PAD), y0 + (band - plate) // 2
    dr.rounded_rectangle([px, py, px + plate, py + plate], radius=b.p(10), fill=WHITE)
    b.im.alpha_composite(qr_image(QR_URL, q, DEEP), (px + b.p(12), py + b.p(12)))

    tx = px + plate + b.p(70)
    cy = y0 + band / 2
    f1 = b.sans(52, "700")
    f2 = b.sans(42, "600")
    dr.text((tx, cap_top(b, f1, cy - b.p(42))), f"{SITE}   ·   {IG}", font=f1, fill=WHITE)
    dr.text((tx, cap_top(b, f2, cy + b.p(46))), "   ·   ".join(PHONES), font=f2,
            fill=(*PALE, 255))

    fx = b.W - b.p(PAD)
    f3, sp3 = fit_track(b, dr, [SELLER], b.p(760), 44, 0.14, lambda s: b.sans(s, "700"))
    track(b, dr, (fx, cap_top(b, f3, cy - b.p(38))), SELLER, f3, WHITE, sp3, "ra")
    f4, sp4 = fit_track(b, dr, [SELLER_ROLE], b.p(760), 28, 0.22,
                        lambda s: b.sans(s, "600"))
    track(b, dr, (fx, cap_top(b, f4, cy + b.p(42))), SELLER_ROLE, f4, (*PALE, 255),
          sp4, "ra")


def cap_top(b: Board, f, cy: float) -> float:
    """Metni ortasından hizala — PIL üst kenardan yazıyor."""
    t, bo = f.getbbox("H")[1], f.getbbox("H")[3]
    return cy - (t + bo) / 2


def mid(b: Board):
    """Mesaj alanının kutusu (px)."""
    return b.p(HEAD), b.p(FOOT), b.p(FOOT) - b.p(HEAD)


# ------------------------------------------------------------ yapı taşları
def photo(b: Board, name: str, focus: float = 0.5) -> None:
    y0, y1, h = mid(b)
    b.im.paste(cover(name, (b.W, h), focus), (0, y0))


def veil(b: Board, color=NAVY, a0: int = 0, a1: int = 210, frm: float = 0.25) -> None:
    """Mesaj alanına dikey perde — yazı her render'da okunsun."""
    y0, y1, h = mid(b)
    ys = np.linspace(0, 1, h, dtype=np.float32)
    a = np.clip((ys - frm) / max(1 - frm, 1e-6), 0, 1) * (a1 - a0) + a0
    arr = np.zeros((h, 1, 4), np.float32)
    for c in range(3):
        arr[:, 0, c] = color[c]
    arr[:, 0, 3] = a
    im = Image.fromarray(arr.astype(np.uint8), "RGBA").resize((b.W, h), Image.BILINEAR)
    b.im.alpha_composite(im, (0, y0))


def flat_veil(b: Board, color, alpha: int) -> None:
    y0, y1, h = mid(b)
    overlay(b, lambda d: d.rectangle([0, y0, b.W, y1], fill=(*color, alpha)))


def headline(b: Board, lines, y: float, size: float, fill=WHITE, x: float = PAD,
             lh: float = 1.06, anchor: str = "la"):
    """Büyük manşet. y = ilk satırın ORTASI (mm)."""
    dr = b.draw
    f = fit(b, dr, lines, b.W - b.p(PAD * 2), size, lambda s: b.sans(s, "700"))
    step = f.size * lh
    px = b.p(x) if anchor == "la" else (b.W - b.p(x) if anchor == "ra" else b.W // 2)
    for i, t in enumerate(lines):
        dr.text((px, cap_top(b, f, b.p(y) + i * step)), t, font=f, fill=fill,
                anchor={"la": "la", "ra": "ra", "ma": "ma"}[anchor])
    return b.p(y) + (len(lines) - 1) * step + f.size * 0.6


def eyebrow(b: Board, text: str, y: float, size: float = 44, fill=None,
            x: float = PAD, anchor: str = "la") -> None:
    dr = b.draw
    f, sp = fit_track(b, dr, [text], b.W - b.p(PAD * 2), size, 0.26,
                      lambda s: b.sans(s, "600"))
    px = b.p(x) if anchor == "la" else (b.W - b.p(x) if anchor == "ra" else b.W // 2)
    track(b, dr, (px, cap_top(b, f, b.p(y))), text, f, fill or (*AQUA, 255), sp,
          {"la": "la", "ra": "ra", "ma": "ma"}[anchor])


def rule(b: Board, x: float, y: float, w: float, color=CORAL, t: float = 10) -> None:
    b.draw.rectangle([b.p(x), b.p(y), b.p(x + w), b.p(y + t)], fill=color)


def glass(b: Board, x, y, w, h, r=26, a=150, border=None) -> None:
    """Buzlu cam kart: altı bulanıklaşıyor, üstüne yarı saydam mavi biniyor."""
    box = (b.p(x), b.p(y), b.p(x + w), b.p(y + h))
    reg = b.im.crop(box).filter(ImageFilter.GaussianBlur(b.p(6)))
    tint = gradient((box[2] - box[0], box[3] - box[1]),
                    [(0.0, DARK), (1.0, OCEAN)], angle=0.35)
    tint.putalpha(a)
    body = reg.convert("RGBA")
    body.alpha_composite(tint)
    mask = Image.new("L", body.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, body.width - 1, body.height - 1],
                                           radius=b.p(r), fill=255)
    b.im.paste(body, box[:2], mask)
    overlay(b, lambda d: d.rounded_rectangle(box, radius=b.p(r), outline=border or
                                             (*PALE, 120), width=max(2, b.p(1.6))))


# ================================================================ panolar
def p1_proje_alani() -> Image.Image:
    """Ana kimlik panosu — gece render'ı, slogan, proje büyüklüğü."""
    b = board()
    photo(b, "night-gate", 0.52)
    veil(b, NAVY, 0, 225, 0.18)
    headline(b, ["LÜKS ARTIK", "ULAŞILABİLİR."], 1120, 190)
    rule(b, PAD, 1470, 420)
    eyebrow(b, f"{TOTAL} KONUTLUK YAŞAM PROJESİ  ·  İZMİT MİA BÖLGESİ", 1590, 50,
            (*ICE, 255))
    bands(b)
    return b.im.convert("RGB")


def p2_ulasim() -> Image.Image:
    """Sekiz mesafe. Arsa yoldan geçene 'neredeyim' değil 'neye yakınım' der."""
    b = board()
    y0, y1, h = mid(b)
    b.im.paste(gradient((b.W, h), [(0.0, WHITE), (0.5, (240, 251, 253)), (1.0, PALE)],
                        angle=0.7), (0, y0))
    eyebrow(b, "HER YERE YAKIN", 400, 50, (*DEEP, 255))
    headline(b, ["ULAŞIM"], 520, 150, DEEP)
    rule(b, PAD, 640, 380)

    cw, ch, gx, gy = 660, 372, 30, 66
    x0 = (W_MM - (cw * 4 + gx * 3)) / 2
    dr = b.draw
    fn, _ = fit_track(b, dr, [d[0] for d in DISTANCES], b.p(cw - 80), 52, 0.04,
                      lambda s: b.sans(s, "600"))
    fv = b.sans(120, "700")
    for i, (name, mins) in enumerate(DISTANCES):
        cx = x0 + (i % 4) * (cw + gx)
        cy = 800 + (i // 4) * (ch + gy)
        box = [b.p(cx), b.p(cy), b.p(cx + cw), b.p(cy + ch)]
        dr.rounded_rectangle(box, radius=b.p(18), fill=WHITE, outline=(*PALE, 255),
                             width=max(2, b.p(2)))
        dr.text((b.p(cx + 44), cap_top(b, fn, b.p(cy + 110))), name, font=fn, fill=INK)
        dr.text((b.p(cx + cw - 44), cap_top(b, fv, b.p(cy + 262))), mins, font=fv,
                fill=DEEP, anchor="ra")
    bands(b)
    return b.im.convert("RGB")


def p3_odeme() -> Image.Image:
    """Tek mesaj: 60 ay. Otuz metreden okunacak tek şey bu."""
    b = board()
    y0, y1, h = mid(b)
    b.im.paste(gradient((b.W, h), bs.SURF_STOPS, angle=0.62), (0, y0))
    b.im.alpha_composite(glow((b.W, h), b.W * 0.78, h * 0.72, b.W * 0.55,
                              AQUA, 0.30), (0, y0))
    # Hayalet render: düz alfa verilince üst kenarı çizgi gibi görünüyordu,
    # dikey rampayla gradyandan doğuyor.
    gh = b.p(h * 0.56)
    ghost = cover("entrance-gate", (b.W, gh), 0.45)
    ramp = np.clip(np.linspace(-0.35, 1.0, gh), 0, 1) ** 1.6 * 46
    ghost.putalpha(Image.fromarray(
        np.repeat(ramp[:, None], b.W, axis=1).astype(np.uint8), "L"))
    b.im.alpha_composite(ghost, (0, y1 - gh))

    eyebrow(b, "TASARRUFA DAYALI FAİZSİZ FİNANSMAN", 430, 52, (*ICE, 255),
            anchor="ma")
    headline(b, ["VADE FARKSIZ"], 610, 130, WHITE, anchor="ma")
    headline(b, ["60 AY TAKSİT"], 900, 300, WHITE, anchor="ma")

    pw, ph = 1560, 150
    px, py = (W_MM - pw) / 2, 1290
    b.draw.rounded_rectangle([b.p(px), b.p(py), b.p(px + pw), b.p(py + ph)],
                             radius=b.p(ph / 2), fill=CORAL)
    dr = b.draw
    f, sp = fit_track(b, dr, ["PEŞİN FİYATINA VADE"], b.p(pw - 140), 62, 0.20,
                      lambda s: b.sans(s, "700"))
    track(b, dr, (b.W // 2, cap_top(b, f, b.p(py + ph / 2))), "PEŞİN FİYATINA VADE",
          f, WHITE, sp, "ma")
    bands(b)
    return b.im.convert("RGB")


def p5_daireler() -> Image.Image:
    """Dört tip, m² ve adet. Fiyat yok — arayan telefonu açsın."""
    b = board()
    photo(b, "entrance-gate", 0.5)
    flat_veil(b, DEEP, 172)
    eyebrow(b, "DAİRE TİPLERİ", 400, 52, (*PALE, 255), anchor="ma")

    cw, chh = 660, 700
    gx = 40
    x0 = (W_MM - (cw * 4 + gx * 3)) / 2
    dr = b.draw
    ft = b.sans(120, "700")
    fm = b.sans(64, "700")
    tags = [tr_upper(u[1].replace(u[0], "", 1).strip()) for u in UNITS]
    fa, spa = fit_track(b, dr, tags, b.p(cw - 80), 42, 0.14,
                        lambda s: b.sans(s, "600"))
    fc = b.sans(40, "600")
    for i, (code, label, area, adet) in enumerate(UNITS):
        cx = x0 + i * (cw + gx)
        glass(b, cx, 560, cw, chh, r=28, a=185, border=(*PALE, 190))
        dr.text((b.p(cx + cw / 2), cap_top(b, ft, b.p(700))), code, font=ft,
                fill=WHITE, anchor="ma")
        # Alt satır kodun tekrarı değil, kodtan arta kalan tip adı:
        # "1+0 Daire" -> DAİRE, "1+1 Bahçe Loft" -> BAHÇE LOFT.
        track(b, dr, (b.p(cx + cw / 2), cap_top(b, fa, b.p(838))), tags[i], fa,
              (*ICE, 255), spa, "ma")
        dr.rectangle([b.p(cx + cw / 2 - 90), b.p(900), b.p(cx + cw / 2 + 90),
                      b.p(904)], fill=(*PALE, 200))
        dr.text((b.p(cx + cw / 2), cap_top(b, fm, b.p(990))), area, font=fm,
                fill=WHITE, anchor="ma")
        dr.text((b.p(cx + cw / 2), cap_top(b, fc, b.p(1120))), f"{adet} ADET",
                font=fc, fill=(*AQUA, 255), anchor="ma")

    pw, ph = 1560, 130
    px, py = (W_MM - pw) / 2, 1400
    b.draw.rounded_rectangle([b.p(px), b.p(py), b.p(px + pw), b.p(py + ph)],
                             radius=b.p(ph / 2), fill=(*ICE, 255))
    f, sp = fit_track(b, dr, ["TÜM TİPLERDE 60 AY VADE"], b.p(pw - 140), 56, 0.18,
                      lambda s: b.sans(s, "700"))
    track(b, dr, (b.W // 2, cap_top(b, f, b.p(py + ph / 2))), "TÜM TİPLERDE 60 AY VADE",
          f, DEEP, sp, "ma")
    bands(b)
    return b.im.convert("RGB")


def p8_yatirim() -> Image.Image:
    """Sol yarı fotoğraf, sağ yarı söz. Ortada sert dikey kesik."""
    b = board()
    y0, y1, h = mid(b)
    half = b.p(W_MM * 0.54)
    b.im.paste(cover("courtyard-pools", (half, h), 0.45), (0, y0))
    b.draw.rectangle([half, y0, b.W, y1], fill=BONE)

    x = W_MM * 0.54 + 90
    dr = b.draw
    f = fit(b, dr, ["YÜKSEK YATIRIM", "POTANSİYELİ"], b.W - b.p(x + PAD), 118,
            lambda s: b.sans(s, "700"))
    for i, t in enumerate(["YÜKSEK YATIRIM", "POTANSİYELİ"]):
        dr.text((b.p(x), cap_top(b, f, b.p(560) + i * f.size * 1.08)), t, font=f,
                fill=DEEP)
    rule(b, x, 800, 300, CORAL)

    fb, spb = fit_track(b, dr, ["GELİŞEN BÖLGE", "ARTAN DEĞER", "600 KONUTLUK ÖLÇEK"],
                        b.W - b.p(x + PAD + 70), 52, 0.10, lambda s: b.sans(s, "600"))
    for i, t in enumerate(["GELİŞEN BÖLGE", "ARTAN DEĞER", "600 KONUTLUK ÖLÇEK"]):
        yy = 940 + i * 130
        dr.rectangle([b.p(x), b.p(yy - 14), b.p(x + 28), b.p(yy + 14)], fill=CORAL)
        track(b, dr, (b.p(x + 70), cap_top(b, fb, b.p(yy))), t, fb, INK, spb)
    bands(b)
    return b.im.convert("RGB")


def p10_satis() -> Image.Image:
    """Karekod panosu — yoldan geçen telefonu kaldırıp okutsun."""
    b = board()
    photo(b, "night-gate", 0.35)
    flat_veil(b, NAVY, 215)
    eyebrow(b, "BİLGİ VE RANDEVU İÇİN", 430, 54, (*AQUA, 255), anchor="ma")
    headline(b, ["KAREKODU OKUTUN"], 590, 150, WHITE, anchor="ma")

    q = b.p(560)
    plate = q + b.p(60)
    px, py = (b.W - plate) // 2, b.p(830)
    b.draw.rounded_rectangle([px, py, px + plate, py + plate], radius=b.p(22),
                             fill=WHITE)
    b.im.alpha_composite(qr_image(QR_URL, q, DEEP), (px + b.p(30), py + b.p(30)))

    dr = b.draw
    f, sp = fit_track(b, dr, ["DAİRE PLANLARI · ÖDEME SEÇENEKLERİ · SANAL TUR"],
                      b.p(2200), 48, 0.16, lambda s: b.sans(s, "600"))
    track(b, dr, (b.W // 2, cap_top(b, f, b.p(1620))),
          "DAİRE PLANLARI · ÖDEME SEÇENEKLERİ · SANAL TUR", f, (*ICE, 255), sp, "ma")
    bands(b)
    return b.im.convert("RGB")


# --------------------------------------------------- Higgsfield panoları
def clean_seam(b: Board, limit: float = 90) -> None:
    """Bandın hemen altındaki/üstündeki üretim artığını sil.

    Üretim, ayrılan bantların sınırına kendi ince çizgisini koyabiliyor
    (konum panosunda beyaz bir şerit kalmıştı). Bandı kalınlaştırmak çiti
    bozardı — panolar aynı hizada olmalı. Onun yerine artığı ÖLÇÜP
    siliyoruz: sınırdan içeri doğru yürüyüp satır yatayda düz kaldığı
    sürece (çizgi düzdür, fotoğraf değildir) o satırları ilk dokulu
    satırla dolduruyoruz. Fotoğrafla başlayan panolarda hiçbir şey
    değişmiyor.
    """
    a = np.asarray(b.im.convert("RGB"), np.float32)
    top, bot, lim = b.p(HEAD), b.p(FOOT), b.p(limit)

    def flat(y):
        return a[y].std(axis=0).max() < 6

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
    """Üretilen panoyu 3:2'ye oturt, sonra ortak bantları bas.

    İstemde üstteki %14 ve alttaki %13 boş bırakılmıştı; bantlar oraya
    denk geliyor ve üretimin bant rengi ne olursa olsun üzerine marka
    mavisi basılıyor. Böylece on pano tek çizgide buluşuyor.
    """
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
    ("arsa-01-proje-alani", p1_proje_alani),
    ("arsa-02-ulasim",      p2_ulasim),
    ("arsa-03-odeme",       p3_odeme),
    ("arsa-04-finansman",   lambda: from_ai("arsa-4-finansman")),
    ("arsa-05-daireler",    p5_daireler),
    ("arsa-06-sosyal",      lambda: from_ai("arsa-6-sosyal")),
    ("arsa-07-manzara",     lambda: from_ai("arsa-7-manzara")),
    ("arsa-08-yatirim",     p8_yatirim),
    ("arsa-09-konum",       lambda: from_ai("arsa-9-konum")),
    ("arsa-10-karekod",     p10_satis),
]


def fence_run(paths) -> None:
    """On panoyu yan yana dizip çitin dışarıdan görünüşünü çıkarır.

    Panoların asıl sınavı tek tek değil, sıradaki hâlleri: kimlik bandı ve
    künye şeridi çit boyunca kesintisiz iki mavi çizgi oluşturmalı.
    """
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
    for name, fn in BOARDS:
        im = fn()
        im.save(os.path.join(OUT, name + ".jpg"), quality=92, subsampling=0,
                optimize=True, dpi=(DPI, DPI))
        im.resize((im.width // 5, im.height // 5), Image.LANCZOS).save(
            os.path.join(PREVIEW, name + ".jpg"), quality=88, optimize=True)
        print(f"  -> {name}.jpg")
        made.append(os.path.join(PREVIEW, name + ".jpg"))
    fence_run(made)


if __name__ == "__main__":
    main()
