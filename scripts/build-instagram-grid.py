#!/usr/bin/env python3
"""
MİA PARK OCEAN — Instagram "grid split" (ızgara bölme) seti.

Her panel 3 gönderiye bölünür; panel sayısı PANELS listesinden gelir.
Profil ızgarasında her panel TEK BİR geniş görsel gibi görünür.

ÖLÇÜ MANTIĞI
────────────
Instagram akışta en fazla 4:5 dikey görsel kabul eder → parça 1080x1350.
Profil ızgarası ise kareyi 3:4 kırpar, yani her parçanın SAĞINDAN VE
SOLUNDAN 34'er piksel gizlenir. Parçalar basitçe yan yana kesilirse
ızgarada 68 piksellik içerik kaybolur ve tipografi kenarlarda atlar.

Bu yüzden panel, ızgarada görünecek genişlikten (3 x 1012 = 3036) 68 piksel
DAHA GENİŞ çizilir ve parçalar üst üste binecek şekilde kesilir:

  panel genişliği  3104
  parça 1          x    0 – 1080
  parça 2          x 1012 – 2092      (68 px bindirme)
  parça 3          x 2024 – 3104
  ızgarada görünen x   34 – 3070      (kesintisiz)

Tek gönderi olarak bakıldığında bindirme fark edilmez; ızgarada ise
kompozisyon kusursuz devam eder.

PAYLAŞIM SIRASI
───────────────
Instagram en yeni gönderiyi sol üste koyar. Bir satırın soldan sağa
okunması için parçalar TERS sırayla paylaşılır: önce 3, sonra 2, sonra 1.
Üretilen dosya adları bu sırayı taşır.

MARKA KURALLARI
───────────────
· Sol üstte MİA PARK OCEAN logosu — yalnızca amblem + kelime markası.
  "İZMİT MİA BÖLGESİ" alt satırı kırpılır (bu ölçekte okunmuyor).
· Sağ altta OCEAN GAYRİMENKUL logosu, küçük.
· Dalga ayrıca kullanılmaz — dalga zaten logonun içinde.
· Web adresi görselin üstüne yazılmaz; profil biyografisinde durur.

Çıktılar → social-media/instagram/
"""

from __future__ import annotations

import math
import os
import shutil

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "public", "images")
BRAND = os.path.join(ROOT, "public", "brand")
PUBLIC = os.path.join(ROOT, "public")
FONTS = os.path.join(ROOT, "brand-source", "fonts")
OUT = os.path.join(ROOT, "social-media", "instagram")

# ---------------------------------------------------------------- ölçüler
TILE_W, TILE_H = 1080, 1350          # akış gönderisi (4:5)
GRID_W = 1012                        # ızgarada görünen genişlik (3:4)
BLEED = (TILE_W - GRID_W) // 2       # 34
PANEL_W = GRID_W * 3 + BLEED * 2     # 3104
PANEL_H = TILE_H
OFFSETS = [0, GRID_W, GRID_W * 2]    # parça kesim noktaları
SAFE = BLEED + 60                    # kenar güvenli alan

# ---------------------------------------------------------------- renkler
NAVY = (4, 40, 58)
MIA_DEEP = (9, 86, 120)
MIA_DARK = (26, 116, 150)
MIA_OCEAN = (44, 148, 180)
MIA_CYAN = (72, 171, 197)
MIA_AQUA = (110, 189, 208)
MIA_LIGHT = (146, 209, 223)
MIA_PALE = (184, 228, 236)
MIA_ICE = (221, 247, 250)
WHITE = (255, 255, 255)
INK = (4, 40, 58)

DEEP_STOPS = [(0.0, NAVY), (0.3, (6, 64, 90)), (0.62, MIA_DEEP), (1.0, MIA_DARK)]
SURF_STOPS = [(0.0, MIA_DEEP), (0.4, MIA_DARK), (0.75, MIA_OCEAN), (1.0, MIA_CYAN)]
LIGHT_STOPS = [(0.0, WHITE), (0.45, (244, 252, 253)), (1.0, (206, 236, 244))]


# ---------------------------------------------------------------- yardımcı
def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def serif(s: int, w: str = "500") -> ImageFont.FreeTypeFont:
    return font(f"Fraunces-{w}.ttf", s)


def sans(s: int) -> ImageFont.FreeTypeFont:
    return font("Manrope-400.ttf", s)


def sans_sb(s: int) -> ImageFont.FreeTypeFont:
    return font("Manrope-600.ttf", s)


def sans_b(s: int) -> ImageFont.FreeTypeFont:
    return font("Manrope-700.ttf", s)


def gradient(size, stops, angle: float = 0.5) -> Image.Image:
    w, h = size
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    t = np.clip((xx / max(w - 1, 1)) * angle + (yy / max(h - 1, 1)) * (1 - angle), 0, 1)
    arr = np.zeros((h, w, 3), np.float32)
    for i in range(len(stops) - 1):
        t0, c0 = stops[i]
        t1, c1 = stops[i + 1]
        m = (t >= t0) & (t <= t1)
        k = np.clip((t - t0) / max(t1 - t0, 1e-6), 0, 1)
        for c in range(3):
            arr[:, :, c] = np.where(m, c0[c] + (c1[c] - c0[c]) * k, arr[:, :, c])
    return Image.fromarray(arr.astype(np.uint8), "RGB").convert("RGBA")


def glow(cx: float, cy: float, r: float, color, strength: float = 0.3) -> Image.Image:
    """Yumuşak ışık odağı — düz zemine derinlik katar."""
    yy, xx = np.mgrid[0:PANEL_H, 0:PANEL_W].astype(np.float32)
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / r
    a = np.clip(1.0 - d, 0, 1) ** 2.1 * strength
    arr = np.zeros((PANEL_H, PANEL_W, 4), np.float32)
    for c in range(3):
        arr[:, :, c] = color[c]
    arr[:, :, 3] = a * 255
    return Image.fromarray(arr.astype(np.uint8), "RGBA")


def cover(name: str, size, focus: float = 0.5) -> Image.Image:
    """Görseli kutuya kırparak sığdırır (focus: dikey odak 0-1)."""
    im = Image.open(os.path.join(IMG, name)).convert("RGB")
    w, h = size
    s = max(w / im.width, h / im.height)
    im = im.resize((max(w, int(im.width * s)), max(h, int(im.height * s))), Image.LANCZOS)
    x = (im.width - w) // 2
    y = int((im.height - h) * focus)
    return im.crop((x, y, x + w, y + h)).convert("RGBA")


def scrim(size, stops) -> Image.Image:
    """Dikey saydamlık perdesi: [(konum, (r,g,b,a)), ...]"""
    w, h = size
    arr = np.zeros((h, w, 4), np.float32)
    ys = np.linspace(0, 1, h)
    for i in range(len(stops) - 1):
        t0, c0 = stops[i]
        t1, c1 = stops[i + 1]
        idx = np.where((ys >= t0) & (ys <= t1))[0]
        if not len(idx):
            continue
        k = (ys[idx] - t0) / max(t1 - t0, 1e-6)
        for c in range(4):
            arr[idx, :, c] = (c0[c] + (c1[c] - c0[c]) * k)[:, None]
    return Image.fromarray(arr.astype(np.uint8), "RGBA")


# ---------------------------------------------------------------- logolar
# Kaynak kilit 1200x822. Satır bantları: amblem 0-589, kelime markası
# 634-726, "İZMİT MİA BÖLGESİ" alt satırı 779-818. Alt satır kırpılır —
# Instagram ölçeğinde okunmuyor, yalnızca lekeli görünüyor.
LOCKUP_CROP_H = 752


def lockup(width: int, white: bool = True) -> Image.Image:
    """Amblem + MİA PARK OCEAN — alt satır olmadan."""
    name = "logo-ocean-white.png" if white else "logo-ocean-trim.png"
    im = Image.open(os.path.join(BRAND, name)).convert("RGBA")
    im = im.crop((0, 0, im.width, LOCKUP_CROP_H))
    box = im.getbbox()
    if box:
        im = im.crop(box)
    return im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)


def mark(width: int, white: bool = True) -> Image.Image:
    name = "mark-ocean-white.png" if white else "mark-ocean-trim.png"
    im = Image.open(os.path.join(BRAND, name)).convert("RGBA")
    return im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)


def partner(width: int, white: bool = True) -> Image.Image:
    """OCEAN GAYRİMENKUL — iş ortağı imzası."""
    name = "ocean-logo-white.png" if white else "ocean-logo.webp"
    im = Image.open(os.path.join(PUBLIC, name)).convert("RGBA")
    return im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)


def track(dr, xy, text, f, fill, sp, anchor="la"):
    """Harf aralıklı metin. anchor: la / ma / ra"""
    widths = [dr.textlength(ch, font=f) for ch in text]
    total = sum(widths) + sp * max(len(text) - 1, 0)
    x, y = xy
    if anchor[0] == "m":
        x -= total / 2
    elif anchor[0] == "r":
        x -= total
    for ch, w in zip(text, widths):
        dr.text((x, y), ch, font=f, fill=fill)
        x += w + sp
    return total


def wrap(dr, text, f, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = f"{cur} {w}".strip()
        if dr.textlength(t, font=f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def tile_centers():
    """Parçaların panel içindeki görünür merkezleri (ızgara görünümü)."""
    return [BLEED + GRID_W * i + GRID_W / 2 for i in range(3)]


# ---------------------------------------------------------------- paneller
# Ortak kurgu:
#   · Sol üst köşe → MİA PARK OCEAN logosu (amblem + kelime markası).
#   · Sağ alt köşe → OCEAN GAYRİMENKUL logosu, küçük.
#   · Fotoğraf panellerinde perde HAFİF; okunurluğu perde değil, metnin
#     arkasındaki yumuşak gölge sağlar — böylece render aydınlık kalır.
#   · Tipografik paneller marka gradyanı üstünde; ızgaraya ritim verir.
#
# TEK PARÇA DA OKUNMALI
# ─────────────────────
# Izgara bölme setlerinin klasik hatası: cümle panele ortalanır, tek tek
# bakıldığında her gönderide kelimenin ortasından kesilmiş bir hece kalır.
# Burada her PARÇAYA bir kelime düşüyor: gönderi tek başına da tam bir söz,
# ızgarada üçü birleşince cümle. Panel geneline yayılan tek satırlar ise
# orta parçanın içinde kalacak şekilde otomatik küçültülüyor.

LOGO_W = 300
PARTNER_W = 190
TILE_TEXT_W = GRID_W - 140   # 872 — bir parçanın içinde kalması gereken en
WORD_BASE = 1012             #        genişlik; tüm metinler buna sığdırılır
CAP_Y = 1080


def paste_soft(p: Image.Image, im: Image.Image, pos, blur: int = 22,
               boost: float = 1.7) -> None:
    """Görseli arkasına yumuşak gölge koyarak yapıştırır."""
    sh = Image.new("RGBA", p.size, (0, 0, 0, 0))
    sh.alpha_composite(im, pos)
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    dark = Image.new("RGBA", p.size, (3, 26, 38, 0))
    dark.putalpha(sh.split()[3].point(lambda v: min(255, int(v * boost))))
    p.alpha_composite(dark)
    p.alpha_composite(im, pos)


def brandmark(p: Image.Image, white: bool = True, shadow: bool = True) -> None:
    """Sol parçanın sol üst köşesi — her panelde aynı yerde."""
    lg = lockup(LOGO_W, white)
    if shadow:
        paste_soft(p, lg, (SAFE, 64))
    else:
        p.alpha_composite(lg, (SAFE, 64))


def partner_mark(p: Image.Image, white: bool = True, shadow: bool = True) -> None:
    """Sağ parçanın sağ alt köşesi."""
    pm = partner(PARTNER_W, white)
    if white:
        pm.putalpha(pm.split()[3].point(lambda v: int(v * 0.9)))
    pos = (PANEL_W - SAFE - pm.width, PANEL_H - 66 - pm.height)
    if shadow:
        paste_soft(p, pm, pos, blur=18, boost=1.5)
    else:
        p.alpha_composite(pm, pos)


def frame(p: Image.Image, white: bool = True, shadow: bool = True) -> None:
    brandmark(p, white, shadow)
    partner_mark(p, white, shadow)


def soft_shadow(p: Image.Image, draw_fn, blur: int = 26, alpha: int = 150) -> None:
    """
    Metni önce bulanık koyu bir kopya olarak basar.

    Perdeyi koyulaştırmak yerine yalnızca metnin arkasına gölge koyuyoruz:
    render aydınlık kalıyor, yazı her zeminde okunuyor.
    """
    layer = Image.new("RGBA", p.size, (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(layer))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    a = layer.split()[3].point(lambda v: min(255, int(v * alpha / 255 * 2.2)))
    dark = Image.new("RGBA", p.size, (3, 26, 38, 0))
    dark.putalpha(a)
    p.alpha_composite(dark)


def draw_with_shadow(p: Image.Image, fn) -> None:
    """Önce gölge katmanı, sonra asıl metin."""
    soft_shadow(p, fn)
    fn(ImageDraw.Draw(p))


def photo(name: str, focus: float = 0.5, top: int = 105, bot: int = 195,
          bot_start: float = 0.5) -> Image.Image:
    """Fotoğraf + yalnızca metnin oturduğu yerde perde."""
    p = cover(name, (PANEL_W, PANEL_H), focus)
    p.alpha_composite(
        scrim((PANEL_W, PANEL_H), [
            (0.0, (4, 40, 58, top)),
            (0.20, (4, 40, 58, 0)),
            (bot_start, (4, 40, 58, 0)),
            (max(bot_start + 0.16, 0.7), (4, 40, 58, int(bot * 0.42))),
            (1.0, (4, 40, 58, bot)),
        ])
    )
    return p


# ------------------------------------------------- parçaya sığdıran tipografi
def fit_serif(dr, texts, max_w: int, start: int, w: str = "500"):
    """Üç kelimenin da sığdığı ortak punto — hepsi aynı boyda kalsın."""
    s = start
    while s > 46 and max(dr.textlength(t, font=serif(s, w)) for t in texts if t) > max_w:
        s -= 3
    return serif(s, w)


def fit_track(dr, texts, max_w: int, start: int, sp: int, maker=None):
    """Harf aralıklı küçük başlıklar için ortak punto."""
    maker = maker or sans_b
    s = start
    while s > 20:
        f = maker(s)
        widest = max(sum(dr.textlength(c, font=f) for c in t) + sp * max(len(t) - 1, 0)
                     for t in texts if t)
        if widest <= max_w:
            break
        s -= 2
    return maker(s)


def line_center(dr, text: str, y: int, size: int, fill, sp: int = 0, maker=None):
    """Panel ortasına ama ORTA PARÇANIN içinde kalacak şekilde tek satır."""
    if sp:
        f = fit_track(dr, [text], TILE_TEXT_W, size, sp, maker)
        return track(dr, (PANEL_W / 2, y), text, f, fill, sp, "ma")
    maker = maker or sans
    s = size
    while s > 22 and dr.textlength(text, font=maker(s)) > TILE_TEXT_W:
        s -= 2
    dr.text((PANEL_W / 2, y), text, font=maker(s), fill=fill, anchor="ma")


def word_row(dr, words, caps, size: int = 200, w: str = "500",
             base: int = WORD_BASE, cap_y: int = CAP_Y,
             fill=WHITE, cap_fill=(*MIA_ICE, 248), cap_size: int = 40):
    """
    Her parçaya bir kelime, altına küçük bir başlık.

    Kelimeler ortak puntoda ve ortak taban çizgisinde durur; punto,
    üçünün de parça içinde kalacağı en büyük değere göre seçilir.
    """
    f = fit_serif(dr, words, TILE_TEXT_W, size, w)
    fc = fit_track(dr, caps, TILE_TEXT_W, cap_size, 14) if any(caps) else None
    for cx, word, cap in zip(tile_centers(), words, caps):
        if word:
            dr.text((cx, base), word, font=f, fill=fill, anchor="ms")
        if cap and fc:
            track(dr, (cx, cap_y), cap, fc, cap_fill, 14, "ma")


# ── 01 · sabitlenecek: projeyi karşıdan gösteren ana kare ──────────────
def panel_entrance() -> Image.Image:
    p = photo("entrance-gate.webp", 0.46, top=118, bot=205, bot_start=0.5)
    frame(p)

    def paint(dr):
        word_row(dr, ["Lüks", "artık", "ulaşılabilir."],
                 ["İZMİT MİA BÖLGESİ", "600 DAİRE · 4 BLOK", "4 YAŞAM TİPİ"], 190)

    draw_with_shadow(p, paint)
    return p


# ── 02 · %0 · tipografik ───────────────────────────────────────────────
def panel_zero() -> Image.Image:
    """Kampanyanın tek cümlesi, üç dev rakama bölünmüş."""
    p = gradient((PANEL_W, PANEL_H), [(0.0, NAVY), (0.32, (6, 64, 90)),
                                      (0.7, MIA_DEEP), (1.0, MIA_DARK)], angle=0.78)
    p.alpha_composite(glow(tile_centers()[0], 640, 1450, MIA_CYAN, 0.32))
    p.alpha_composite(glow(PANEL_W, PANEL_H, 1500, MIA_OCEAN, 0.2))
    dr = ImageDraw.Draw(p)

    line_center(dr, "TASARRUFA DAYALI FİNANSMAN", 296, 40, (*MIA_LIGHT, 240), 16)
    word_row(dr, ["%0", "60", "Yok"], ["FAİZ", "AY VADE", "VADE FARKI"],
             400, "700", base=820, cap_y=884, cap_size=48)
    dr.line([PANEL_W / 2 - 90, 1022, PANEL_W / 2 + 90, 1022], fill=(*MIA_AQUA, 200), width=4)
    line_center(dr, "Bankasız, faizsiz, kefilsiz konut edinme modeli.",
                1074, 50, (*MIA_ICE, 240))

    frame(p, shadow=False)
    return p


# ── 03 · 60 ay vade · fotoğraf ─────────────────────────────────────────
def panel_term() -> Image.Image:
    p = photo("street-corner.webp", 0.5, top=118, bot=205, bot_start=0.48)
    frame(p)

    def paint(dr):
        word_row(dr, ["60", "ay", "vade"],
                 ["VADE FARKI YOK", "ARA ÖDEME YOK", "SABİT TAKSİT"], 240, "600")

    draw_with_shadow(p, paint)
    return p


# ── 04 · Banka yok. Faiz yok. Kefil yok. · tipografik ──────────────────
def panel_nobank() -> Image.Image:
    """Her parçada tek cümle — tek başına da, ızgarada da tam okunur."""
    p = gradient((PANEL_W, PANEL_H), [(0.0, (3, 30, 44)), (0.5, NAVY),
                                      (1.0, (7, 74, 104))], angle=0.3)
    p.alpha_composite(glow(PANEL_W / 2, 1480, 1900, MIA_DEEP, 0.5))
    dr = ImageDraw.Draw(p)

    line_center(dr, "KONUT FİNANSMANI", 258, 42, (*MIA_LIGHT, 230), 18)

    words = ["Banka yok.", "Faiz yok.", "Kefil yok."]
    notes = ["Kredi başvurusu, dosya masrafı yok.",
             "Tasarrufa dayalı, %0 faizli model.",
             "Teminat ya da kefil aranmaz."]
    f = fit_serif(dr, words, TILE_TEXT_W, 168)
    for cx, big, note in zip(tile_centers(), words, notes):
        dr.text((cx, 700), big, font=f, fill=WHITE, anchor="ms")
        dr.line([cx - 110, 786, cx + 110, 786], fill=(*MIA_AQUA, 200), width=4)
        fn = sans(46)
        while dr.textlength(max(notes, key=len), font=fn) > TILE_TEXT_W and fn.size > 26:
            fn = sans(fn.size - 2)
        for i, ln in enumerate(wrap(dr, note, fn, TILE_TEXT_W)):
            dr.text((cx, 842 + i * 62), ln, font=fn, fill=(*MIA_PALE, 236), anchor="ma")

    line_center(dr, "60 AY VADE · VADE FARKI YOK", 1096, 44, (*MIA_ICE, 250), 18)

    frame(p, shadow=False)
    return p


# ── 05 · rakamlar · fotoğraf ───────────────────────────────────────────
def panel_stats() -> Image.Image:
    p = photo("aerial-pools.webp", 0.5, top=118, bot=212, bot_start=0.52)
    frame(p)

    def paint(dr):
        word_row(dr, ["600", "4 + 8", "4"], ["DAİRE", "BLOK & KAT", "YAŞAM TİPİ"], 210, "600")

    draw_with_shadow(p, paint)
    return p


# ── 06 · finansman · fotoğraf ──────────────────────────────────────────
def panel_finance() -> Image.Image:
    p = photo("facade-warm.webp", 0.42, top=126, bot=215, bot_start=0.52)
    frame(p)

    def paint(dr):
        word_row(dr, ["Bankasız", "Faizsiz", "Kefilsiz"],
                 ["KREDİYE GEREK YOK", "%0 FAİZ", "KEFİL ARANMAZ"], 160, "600")

    draw_with_shadow(p, paint)
    return p


# ── 07 · sabit taksit · tipografik (aydınlık panel) ────────────────────
def panel_fixed() -> Image.Image:
    """60 eşit çubuk = 60 eşit taksit. Izgaraya aydınlık bir satır katar."""
    p = gradient((PANEL_W, PANEL_H), LIGHT_STOPS, angle=0.35)
    dr = ImageDraw.Draw(p)

    line_center(dr, "ÖDEME PLANI", 340, 42, (*MIA_DEEP, 235), 20)
    word_row(dr, ["Sabit", "taksit,", "sürpriz yok."],
             ["60 EŞİT ÖDEME", "AYNI TUTAR", "ARA ÖDEME YOK"], 175,
             base=600, cap_y=668, fill=INK, cap_fill=(*MIA_DEEP, 230))

    # 60 eşit çubuk
    x0, x1 = 230, PANEL_W - 230
    n, gap = 60, 14
    bw = (x1 - x0 - gap * (n - 1)) / n
    base, bh = 1070, 310
    bar = gradient((max(int(bw), 1), bh), [(0.0, MIA_CYAN), (1.0, MIA_DEEP)], angle=0.0)
    for i in range(n):
        p.alpha_composite(bar, (int(round(x0 + i * (bw + gap))), base - bh))
    dr.line([x0, base + 3, x1, base + 3], fill=(*MIA_DEEP, 70), width=3)
    track(dr, (x0, base + 26), "1. AY", sans_b(34), (*MIA_DEEP, 215), 12)
    track(dr, (x1, base + 26), "60. AY", sans_b(34), (*MIA_DEEP, 215), 12, "ra")

    frame(p, white=False, shadow=False)
    return p


# ── 08 · faizsiz finansman · fotoğraf ──────────────────────────────────
def panel_dusk() -> Image.Image:
    p = photo("hero-courtyard-dusk.webp", 0.5, top=115, bot=208, bot_start=0.48)
    frame(p)

    def paint(dr):
        word_row(dr, ["Tasarrufa", "dayalı", "model."],
                 ["KREDİ YOK", "%0 FAİZ", "60 AY VADE"], 175)

    draw_with_shadow(p, paint)
    return p


# ── 09 · daire tipleri · üç iç mekân ───────────────────────────────────
def panel_units() -> Image.Image:
    p = Image.new("RGBA", (PANEL_W, PANEL_H), WHITE)
    shots = [("unit-1plus0-a.webp", "1+0", "28 m² · 472 ADET"),
             ("unit-1plus1-a.webp", "1+1", "50 m² · 96 ADET"),
             ("unit-2plus1-a.webp", "2+1", "100 m² · 16 ADET")]
    for i, (img, _t, _a) in enumerate(shots):
        x0 = 0 if i == 0 else BLEED + GRID_W * i
        x1 = PANEL_W if i == 2 else BLEED + GRID_W * (i + 1)
        w = x1 - x0
        p.alpha_composite(cover(img, (w, PANEL_H), 0.45), (x0, 0))
        p.alpha_composite(
            scrim((w, PANEL_H), [(0.0, (4, 40, 58, 112)), (0.22, (4, 40, 58, 0)),
                                 (0.52, (4, 40, 58, 0)), (0.78, (4, 40, 58, 90)),
                                 (1.0, (4, 40, 58, 215))]), (x0, 0)
        )
    frame(p)

    def paint(dr):
        word_row(dr, [t for _, t, _ in shots], [a for _, _, a in shots], 200, "600")

    draw_with_shadow(p, paint)
    return p


# ── 10 · sosyal yaşam · fotoğraf ───────────────────────────────────────
def panel_social() -> Image.Image:
    p = photo("courtyard-pools.webp", 0.5, top=118, bot=202, bot_start=0.5)
    frame(p)

    def paint(dr):
        word_row(dr, ["Her gün", "tatil", "konforu"],
                 ["SÜS HAVUZLARI", "KAPALI HAVUZ", "FİTNESS & YÜRÜYÜŞ"], 185)

    draw_with_shadow(p, paint)
    return p


# ── 11 · konum haritası · tipografik ───────────────────────────────────
def panel_map() -> Image.Image:
    """Soyut mesafe haritası: merkezde proje, halkalar dakikalar."""
    p = gradient((PANEL_W, PANEL_H), [(0.0, (5, 46, 66)), (0.55, MIA_DEEP),
                                      (1.0, (7, 70, 98))], angle=0.45)
    cx, cy = PANEL_W / 2, 600
    p.alpha_composite(glow(cx, cy, 1350, MIA_CYAN, 0.3))

    rings = Image.new("RGBA", (PANEL_W, PANEL_H), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rings)
    for i, r in enumerate([190, 360, 545, 745, 960, 1190, 1440, 1700]):
        rd.ellipse([cx - r, cy - r, cx + r, cy + r],
                   outline=(*MIA_LIGHT, int(78 * (0.92 ** i))), width=3)
    for k in range(12):
        ang = math.radians(k * 30)
        rd.line([cx + 190 * math.cos(ang), cy + 190 * math.sin(ang),
                 cx + 1700 * math.cos(ang), cy + 1700 * math.sin(ang)],
                fill=(*MIA_LIGHT, 26), width=2)
    p.alpha_composite(rings)

    dr = ImageDraw.Draw(p)
    r = 128
    dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*MIA_ICE, 34),
               outline=(*MIA_ICE, 190), width=4)
    m = mark(148)
    p.alpha_composite(m, (int(cx - m.width / 2), int(cy - m.height / 2 - 4)))
    dr = ImageDraw.Draw(p)

    # Yalnızca sitede iddia edilen mesafeler
    pins = [(tile_centers()[0], 330, "D-100 KARAYOLU", "1 dk"),
            (tile_centers()[2], 330, "ŞEHİR MERKEZİ", "5 dk"),
            (tile_centers()[0], 850, "ÜNİVERSİTE", "yakın"),
            (tile_centers()[2], 850, "HASTANE", "yakın")]
    fp = fit_track(dr, [t for _, _, t, _ in pins], TILE_TEXT_W, 40, 14)
    for px, py, label, dist in pins:
        dr.ellipse([px - 11, py - 11, px + 11, py + 11], fill=(*MIA_ICE, 255))
        dr.ellipse([px - 26, py - 26, px + 26, py + 26], outline=(*MIA_AQUA, 170), width=3)
        track(dr, (px, py + 52), label, fp, (*MIA_ICE, 250), 14, "ma")
        dr.text((px, py + 106), dist, font=serif(84, "600"), fill=WHITE, anchor="ma")

    line_center(dr, "İzmit MİA Bölgesi", 1000, 124, WHITE, maker=lambda s: serif(s, "600"))
    line_center(dr, "ŞEHRİN YENİ MERKEZİ", 1178, 40, (*MIA_LIGHT, 240), 18)

    frame(p, shadow=False)
    return p


# ── 12 · lokasyon · fotoğraf ───────────────────────────────────────────
def panel_location() -> Image.Image:
    p = photo("balcony-dusk.webp", 0.45, top=122, bot=215, bot_start=0.52)
    frame(p)

    def paint(dr):
        word_row(dr, ["1 dk", "5 dk", "Yakın"],
                 ["D-100 KARAYOLU", "ŞEHİR MERKEZİ", "ÜNİVERSİTE & HASTANE"], 195, "600")

    draw_with_shadow(p, paint)
    return p


# ── 13 · gece · fotoğraf ───────────────────────────────────────────────
def panel_night() -> Image.Image:
    p = photo("night-gate.webp", 0.5, top=108, bot=200, bot_start=0.48)
    frame(p)

    def paint(dr):
        word_row(dr, ["Gece", "bile", "büyüleyici"],
                 ["MİMARİ AYDINLATMA", "GÜVENLİ GİRİŞ", "7/24 SİTE YÖNETİMİ"], 200)

    draw_with_shadow(p, paint)
    return p


# ── 14 · iletişim · fotoğraf ───────────────────────────────────────────
def panel_contact() -> Image.Image:
    p = photo("terrace-pergola.webp", 0.45, top=122, bot=212, bot_start=0.48)
    frame(p)

    def paint(dr):
        word_row(dr, ["Dairenizi", "seçin.", ""],
                 ["1+0 · 1+1 · 2+1", "600 DAİREDEN BİRİ", "RANDEVU İÇİN ARAYIN"], 190)
        cx = tile_centers()[2]
        f = sans_b(96)
        while dr.textlength("0540 028 00 41", font=f) > TILE_TEXT_W and f.size > 40:
            f = sans_b(f.size - 4)
        dr.text((cx, WORD_BASE - 8), "0540 028 00 41", font=f, fill=WHITE, anchor="ms")

    draw_with_shadow(p, paint)
    return p


# ── 15 · sosyal donatılar · tipografik ─────────────────────────────────
def panel_amenities() -> Image.Image:
    """
    Ortak alanların dökümü — üç başlık, üç liste.

    Fotoğraf yok: donatı listesi render'ın üstünde okunmaz, kalabalık
    görünür. Marka mavisi üstünde tipografi hem net hem de ızgarada
    fotoğraf satırlarının arasına nefes koyuyor.
    """
    p = blue("mid")
    dr = ImageDraw.Draw(p)

    line_center(dr, "SOSYAL DONATILAR", 258, 42, (*MIA_LIGHT, 235), 20)

    # 3 / 4 / 3 — uzun sütun ortada dursun, ızgarada dengeli görünüyor
    cols = [
        ("Açık alan", ["Geniş peyzaj alanları", "Dekoratif süs havuzları",
                       "Yürüyüş ve dinlenme yolları"]),
        ("Yaşam", ["Merkezi avlu", "Sosyal ve spor alanları",
                   "Çocuk oyun parkı", "Bahçeli zemin daireler"]),
        ("Güven", ["7/24 güvenlik", "Kapalı otopark",
                   "Özel gece aydınlatması"]),
    ]
    col_list(dr, cols)

    line_center(dr, "Ortak alanların tamamı proje kapsamındadır.",
                1152, 48, (*MIA_ICE, 238))

    frame(p, shadow=False)
    return p


# ------------------------------------------------- mavi tipografik paneller
# Fotoğraf panelleri arasında nefes açan, katalog bilgisi taşıyan satırlar.
# Üç zemin tonu dönüşümlü kullanılır ki ardışık mavi satırlar birbirine
# yapışmasın; en açığı bile beyaz metinle 4.9:1 kontrastın altına inmez.

BLUE_GROUNDS = {
    "deep": ([(0.0, (3, 30, 44)), (0.5, NAVY), (1.0, (8, 80, 112))], 0.32),
    "mid": ([(0.0, (6, 58, 82)), (0.45, MIA_DEEP), (1.0, (20, 108, 140))], 0.62),
    "soft": ([(0.0, (9, 86, 120)), (0.5, (20, 108, 140)), (1.0, MIA_DARK)], 0.5),
}


def blue(kind: str = "mid") -> Image.Image:
    """Marka mavisi zemin + her parçaya bir ışık odağı."""
    stops, angle = BLUE_GROUNDS[kind]
    p = gradient((PANEL_W, PANEL_H), stops, angle=angle)
    for cx in tile_centers():
        p.alpha_composite(glow(cx, 500, 1180, MIA_CYAN, 0.2))
    return p


def col_list(dr, cols, title_size: int = 140, item_size: int = 54,
             title_base: int = 516, rule_y: int = 584,
             item_y: int = 664, lh: int = 102):
    """Üç sütun: başlık, ince çizgi, altında maddeler."""
    titles = [t for t, _ in cols]
    items = [i for _, lst in cols for i in lst]
    ft = fit_serif(dr, titles, TILE_TEXT_W, title_size)
    fi = sans(item_size)
    while max(dr.textlength(t, font=fi) for t in items) > TILE_TEXT_W and fi.size > 32:
        fi = sans(fi.size - 2)
    for cx, (title, lst) in zip(tile_centers(), cols):
        dr.text((cx, title_base), title, font=ft, fill=WHITE, anchor="ms")
        dr.line([cx - 100, rule_y, cx + 100, rule_y], fill=(*MIA_AQUA, 205), width=4)
        for i, it in enumerate(lst):
            dr.text((cx, item_y + i * lh), it, font=fi, fill=(*MIA_PALE, 240), anchor="ma")


def unit_panel(kind: str, eyebrow: str, area: str, count: str,
               word: str, cap: str, note: str) -> Image.Image:
    """
    Daire tipi vitrini — üç kardeş panel aynı kalıptan çıkar.

    Parça 1 metrekare, parça 2 adet, parça 3 tipin karakteri. Zemin tonu
    her tipte değişir, yoksa ızgarada üç satır birbirinin kopyası görünür.
    """
    p = blue(kind)
    dr = ImageDraw.Draw(p)
    line_center(dr, eyebrow, 262, 42, (*MIA_LIGHT, 235), 20)
    word_row(dr, [area, count, word], ["BRÜT ALAN", "DAİRE", cap],
             210, "600", base=760, cap_y=834, cap_size=46)
    dr.line([PANEL_W / 2 - 90, 962, PANEL_W / 2 + 90, 962], fill=(*MIA_AQUA, 200), width=4)
    line_center(dr, note, 1022, 50, (*MIA_ICE, 238))
    frame(p, shadow=False)
    return p


# ── 16 · kimler için ───────────────────────────────────────────────────
def panel_audience() -> Image.Image:
    """Aynı projeden üç farklı beklentiye üç farklı cevap."""
    p = blue("deep")
    dr = ImageDraw.Draw(p)
    line_center(dr, "KİMLER İÇİN?", 258, 42, (*MIA_LIGHT, 235), 20)
    col_list(dr, [
        ("İlk ev", ["1+0 · Brüt 28 m²", "Açık plan, geniş balkon",
                    "Bakımı kolay düzen"]),
        ("Yatırım", ["472 daire · en çok tip", "Merkezî konum",
                     "Kompakt plan, kiralamaya uygun"]),
        ("Aile", ["2+1 Bahçe Dubleks", "Brüt 100 m²",
                  "Zemin katta kendi bahçesi"]),
    ])
    line_center(dr, "600 dairede dört farklı yaşam tipi.", 1112, 48, (*MIA_ICE, 238))
    frame(p, shadow=False)
    return p


# ── 17 · daire künyesi ─────────────────────────────────────────────────
def panel_spec() -> Image.Image:
    """
    Dört tipin tamamı, üç parçaya sığdırılmış.

    Bahçe Loft da 1+1 ve 50 m² olduğu için orta parçaya alt satır olarak
    giriyor; böylece hiçbir tip listenin dışında kalmıyor.
    """
    p = blue("mid")
    dr = ImageDraw.Draw(p)
    line_center(dr, "DAİRE KÜNYESİ", 258, 42, (*MIA_LIGHT, 235), 20)

    rows = [("1+0", "BRÜT 28 m²", "472 daire", "PROJENİN %79'U"),
            ("1+1", "BRÜT 50 m²", "96 daire", "1+1 BAHÇE LOFT · 16 DAİRE"),
            ("2+1", "BRÜT 100 m²", "16 daire", "BAHÇE DUBLEKS")]
    ft = fit_serif(dr, [r[0] for r in rows], TILE_TEXT_W, 230, "600")
    fc = fit_track(dr, [r[1] for r in rows], TILE_TEXT_W, 48, 14)
    fn = fit_track(dr, [r[3] for r in rows], TILE_TEXT_W, 38, 12)
    for cx, (typ, area, cnt, note) in zip(tile_centers(), rows):
        dr.text((cx, 640), typ, font=ft, fill=WHITE, anchor="ms")
        track(dr, (cx, 706), area, fc, (*MIA_ICE, 248), 14, "ma")
        dr.text((cx, 800), cnt, font=sans_sb(64), fill=(*MIA_PALE, 245), anchor="ma")
        dr.line([cx - 90, 916, cx + 90, 916], fill=(*MIA_AQUA, 190), width=3)
        track(dr, (cx, 956), note, fn, (*MIA_LIGHT, 235), 12, "ma")

    line_center(dr, "Toplam 600 daire · 4 yaşam tipi.", 1094, 50, (*MIA_ICE, 238))
    frame(p, shadow=False)
    return p


# ── 18 · bahçeli daireler ──────────────────────────────────────────────
def panel_garden() -> Image.Image:
    """32 bahçeli daire — sette hiç anlatılmamış en ayrıştırıcı özellik."""
    p = blue("soft")
    dr = ImageDraw.Draw(p)
    line_center(dr, "BAHÇELİ DAİRELER", 262, 42, (*MIA_LIGHT, 238), 20)
    word_row(dr, ["Bahçe Loft", "Bahçe Dubleks", "32 daire"],
             ["1+1 · 50 m² · 16 DAİRE", "2+1 · 100 m² · 16 DAİRE",
              "ZEMİN KATTA KENDİ BAHÇESİ"],
             180, "500", base=740, cap_y=816, cap_size=44)
    dr.line([PANEL_W / 2 - 90, 946, PANEL_W / 2 + 90, 946], fill=(*MIA_AQUA, 200), width=4)
    line_center(dr, "Zemin katta kendi bahçeniz — apartmanda müstakil ev hissi.",
                1006, 50, (*MIA_ICE, 238))
    frame(p, shadow=False)
    return p


# ── 19 · 1+0 vitrini ───────────────────────────────────────────────────
def panel_unit_1plus0() -> Image.Image:
    return unit_panel("deep", "1+0 DAİRELER", "28 m²", "472", "Akıllı",
                      "TASARIM, MAKSİMUM KONFOR",
                      "Küçük ama nefes alan, bakımı kolay bir ev.")


# ── 20 · 1+1 vitrini ───────────────────────────────────────────────────
def panel_unit_1plus1() -> Image.Image:
    return unit_panel("mid", "1+1 DAİRELER", "50 m²", "96", "Ferah",
                      "KONFORLU VE FONKSİYONEL",
                      "Yalnız ya da çift yaşayanlar için rahat bir düzen.")


# ── 21 · 2+1 Bahçe Dubleks vitrini ─────────────────────────────────────
def panel_unit_2plus1() -> Image.Image:
    return unit_panel("soft", "2+1 BAHÇE DUBLEKS", "100 m²", "16", "Dubleks",
                      "PROJENİN EN BÜYÜK TİPİ",
                      "Bahçeniz, evinizin devamı.")


# ── 22 · daire içi ─────────────────────────────────────────────────────
def panel_interior() -> Image.Image:
    p = blue("mid")
    dr = ImageDraw.Draw(p)
    line_center(dr, "DAİRE İÇİ", 258, 42, (*MIA_LIGHT, 235), 20)
    col_list(dr, [
        ("Açık plan", ["Ferah yaşam alanı", "Aydınlık ve konforlu",
                       "Bakımı kolay düzen"]),
        ("Geniş balkon", ["Doğayla iç içe", "Gün boyu ferah",
                          "1+0 ve 1+1 dairelerde"]),
        ("Modern mutfak", ["Fonksiyonel tasarım", "Pratik ve estetik",
                           "Açık mutfak düzeni"]),
    ])
    line_center(dr, "Yüksek kaliteli iç mekân malzemeleri.", 1112, 48, (*MIA_ICE, 238))
    frame(p, shadow=False)
    return p


# ── 23 · açık plan ─────────────────────────────────────────────────────
def panel_openplan() -> Image.Image:
    """
    Balkon, mutfak ve yaşam alanı — her parçada bir mekân.

    Balkon 1+0 ve 1+1'de var; zemin kattaki tipte yerini bahçe alıyor.
    Bu yüzden "her dairede balkon" denmiyor, alt satır durumu söylüyor.
    """
    p = blue("deep")
    dr = ImageDraw.Draw(p)
    line_center(dr, "AÇIK PLAN", 262, 42, (*MIA_LIGHT, 235), 20)
    word_row(dr, ["Balkon", "Mutfak", "Yaşam alanı"],
             ["GENİŞ, DOĞAYLA İÇ İÇE", "AÇIK, YAŞAM ALANIYLA BÜTÜN",
              "FERAH VE AYDINLIK"],
             190, "500", base=740, cap_y=816, cap_size=44)
    dr.line([PANEL_W / 2 - 90, 946, PANEL_W / 2 + 90, 946], fill=(*MIA_AQUA, 200), width=4)
    line_center(dr, "Üçü tek bir ferah düzende buluşuyor.", 1006, 50, (*MIA_ICE, 238))
    frame(p, shadow=False)
    return p


# ---------------------------------------------------- basın panelleri
# Haber gönderilerinde her PARÇA bir gazete: sol üstünde MİA amblemi ile
# o yayının logosu yan yana, altında gazetenin haberde kullandığı KENDİ
# fotoğrafı, en altta gazetenin manşeti.
#
# Fotoğraf parçayı tam kaplamıyor, kart olarak duruyor: basın toplantısı
# kareleri 16:9 ve içinde insanlar var; 4:5'e kırpınca masadakilerin
# yarısı dışarıda kalıyordu.
#
# Logolar beyaz plaketin içinde. Altı yayının logosu altı farklı zemine
# göre çizilmiş (Gündem beyaz, İlke ve Fikir siyah); beyaz plaket hepsini
# kendi renkleriyle okunur kılan tek ortak zemin — zaten bizim altın
# kuralımız da logonun beyaz zeminde durması.
PRESS_LOGO_DIR = os.path.join(IMG, "basin")


def tile_left(i: int) -> int:
    """Parçanın ızgarada görünen sol kenarı + güvenli boşluk."""
    return BLEED + GRID_W * i + 60


def outlet_logo(slug: str, max_w: int, max_h: int) -> Image.Image:
    im = Image.open(os.path.join(PRESS_LOGO_DIR, f"logo-{slug}.png")).convert("RGBA")
    s = min(max_w / im.width, max_h / im.height)
    return im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)


def press_badge(p: Image.Image, i: int, slug: str, y: int = 56, h: int = 132) -> int:
    """Parçanın sol üstüne beyaz plaket: MİA amblemi | gazetenin logosu."""
    pad, gap = 24, 22
    mk = mark(70, white=False)
    lg = outlet_logo(slug, 228, 68)
    w = pad + mk.width + gap + 2 + gap + lg.width + pad
    x = tile_left(i)

    plate = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(plate)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=24, fill=(255, 255, 255, 255))
    plate.alpha_composite(mk, (pad, (h - mk.height) // 2))
    d.line([pad + mk.width + gap, 30, pad + mk.width + gap, h - 30], fill=(*MIA_PALE, 255), width=2)
    plate.alpha_composite(lg, (pad + mk.width + gap + 2 + gap, (h - lg.height) // 2))
    paste_soft(p, plate, (x, y), blur=20, boost=1.3)
    return y + h


def photo_card(p: Image.Image, i: int, name: str, y: int, h: int, focus: float = 0.5) -> None:
    """Parçanın içine yuvarlatılmış köşeli fotoğraf kartı."""
    w = TILE_TEXT_W
    im = cover(name, (w, h), focus).convert("RGB")
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], radius=28, fill=255)
    card = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    card.paste(im, (0, 0), mask)
    paste_soft(p, card, (tile_left(i), y), blur=26, boost=1.1)


def fit_wrap(dr, texts, max_w: int, start: int, max_lines: int, w: str = "500"):
    """Hepsi en çok `max_lines` satıra sığacak ortak punto."""
    size = start
    while size > 38:
        f = serif(size, w)
        if all(len(wrap(dr, t, f, max_w)) <= max_lines for t in texts):
            return f
        size -= 2
    return serif(size, w)


def press_panel(kind: str, items) -> Image.Image:
    """items: [(slug, manşet, odak), x3] — odak fotoğrafın dikey kırpma noktası."""
    p = blue(kind)
    dr = ImageDraw.Draw(p)
    heads = [h for _, h, _ in items]
    fh = fit_wrap(dr, heads, TILE_TEXT_W, 74, 3, "600")
    lh = round(fh.size * 1.26)

    for i, (slug, head, focus) in enumerate(items):
        x = tile_left(i)
        press_badge(p, i, slug)
        photo_card(p, i, f"basin/haber-{slug}.webp", 232, 566, focus)
        track(dr, (x, 852), "18 AĞUSTOS 2026", sans_b(32), (*MIA_AQUA, 240), 11)
        for k, line in enumerate(wrap(dr, head, fh, TILE_TEXT_W)):
            dr.text((x, 928 + k * lh), line, font=fh, fill=WHITE, anchor="la")
        dr.line([x, 1216, x + 90, 1216], fill=(*MIA_AQUA, 190), width=4)
        track(dr, (x, 1252), "HABERİN TAMAMI PROFİLDE", sans_sb(27), (*MIA_PALE, 228), 8)
        if i:
            xs = BLEED + GRID_W * i
            dr.line([xs, 240, xs, PANEL_H - 240], fill=(*MIA_LIGHT, 55), width=2)

    partner_mark(p, shadow=False)
    return p


# ── 24 · basında biz I ─────────────────────────────────────────────────
def panel_press_a() -> Image.Image:
    return press_panel("deep", [
        ("kocaeligazetesi", "600 konutluk projede faizsiz ödeme modeli", 0.45),
        ("ozgunkocaeli", "Kocaeli'ye 600 dairelik yeni proje", 0.42),
        ("ilkekocaeli", "MİA Park Ocean Kocaeli'de tanıtıldı", 0.40),
    ])


# ── 25 · basında biz II ────────────────────────────────────────────────
def panel_press_b() -> Image.Image:
    return press_panel("soft", [
        ("kocaeligundem", "MİA Bölgesine 600 dairelik dev proje", 0.42),
        ("kocaelifikir", "MİA Park Ocean basına tanıtıldı", 0.45),
        ("kocaelikoz", "Kocaeli'nin yeni yaşam projesi tanıtıldı", 0.42),
    ])


# ── 26 · balkondan avluya ──────────────────────────────────────────────
def panel_balcony_view() -> Image.Image:
    """
    Balkondan avlu ve körfez — projenin iki manzarası tek karede.

    Basın bülteninde dairelerin "deniz ve şehir manzarasına" sahip olacağı,
    projenin sahile yaklaşık 500 metre mesafede olduğu yazıyor; kare buna
    göre üretildi. Sattığı şey manzaranın kendisi değil, seçme hakkı.
    """
    p = photo("ic-mekan/21-balkondan-deniz.webp", 0.5, top=112, bot=200, bot_start=0.46)
    frame(p)

    def paint(dr):
        word_row(dr, ["İster havuzu", "izleyin,", "ister denizi."],
                 ["GENİŞ BALKON", "MERKEZİ AVLU · SÜS HAVUZLARI",
                  "SAHİLE YÜRÜME MESAFESİ"], 180)

    draw_with_shadow(p, paint)
    return p


# ── 27 · yürüyüş yolları ───────────────────────────────────────────────
def panel_walkways() -> Image.Image:
    """Peyzajın içinden geçen yürüyüş yolları — site değil, park içinde yaşamak."""
    p = photo("ic-mekan/18-yuruyus-yolu.webp", 0.5, top=112, bot=205, bot_start=0.46)
    frame(p)

    def paint(dr):
        word_row(dr, ["Bahçesi olan", "ev değil,", "parkı olan ev."],
                 ["YÜRÜYÜŞ VE DİNLENME YOLLARI", "GENİŞ PEYZAJ",
                  "ÇOCUK OYUN PARKI"], 185)

    draw_with_shadow(p, paint)
    return p


PANELS = [
    ("01-karsidan-sabit", "Karşıdan görünüm · sabitlenecek", panel_entrance),
    ("02-sifir-faiz", "%0 faiz · 60 ay vade", panel_zero),
    ("03-60-ay-vade", "60 ay vade · vade farkı yok", panel_term),
    ("04-banka-yok", "Banka yok · Faiz yok · Kefil yok", panel_nobank),
    ("05-rakamlar", "600 daire · 4 blok · 4 tip", panel_stats),
    ("06-finansman", "Bankasız · Faizsiz · Kefilsiz", panel_finance),
    ("07-sabit-taksit", "Sabit taksit · 60 eşit ödeme", panel_fixed),
    ("08-faizsiz-finansman", "Tasarrufa dayalı faizsiz model", panel_dusk),
    ("09-daire-tipleri", "1+0 · 1+1 · 2+1", panel_units),
    ("10-sosyal-yasam", "Her gün tatil konforu", panel_social),
    ("11-konum-haritasi", "Konum haritası · mesafeler", panel_map),
    ("12-lokasyon", "Konum avantajı", panel_location),
    ("13-gece", "Gece bile büyüleyici", panel_night),
    ("14-iletisim", "Dairenizi seçin", panel_contact),
    ("15-sosyal-donatilar", "Sosyal donatılar · ortak alanlar", panel_amenities),
    ("16-kimler-icin", "Kimler için · ilk ev, yatırım, aile", panel_audience),
    ("17-daire-kunyesi", "Daire künyesi · 4 yaşam tipi", panel_spec),
    ("18-bahceli-daireler", "Zemin katta kendi bahçeniz", panel_garden),
    ("19-daire-1plus0", "1+0 · 28 m² · 472 daire", panel_unit_1plus0),
    ("20-daire-1plus1", "1+1 · 50 m² · 96 daire", panel_unit_1plus1),
    ("21-daire-2plus1", "2+1 Bahçe Dubleks · 100 m² · 16 daire", panel_unit_2plus1),
    ("22-daire-ici", "Daire içi · açık plan, balkon, mutfak", panel_interior),
    ("23-acik-plan", "Balkon · mutfak · yaşam alanı", panel_openplan),
    ("24-basinda-biz-1", "Basında biz I · Gazetesi, Özgün, İlke", panel_press_a),
    ("25-basinda-biz-2", "Basında biz II · Gündem, Fikir, Koz", panel_press_b),
    ("26-havuz-deniz", "İster havuzu izleyin, ister denizi", panel_balcony_view),
    ("27-yuruyus-yollari", "Bahçesi olan ev değil, parkı olan ev", panel_walkways),
]


# ---------------------------------------------------------------- profil
def profile_picture() -> Image.Image:
    """1080x1080 profil fotoğrafı — daire içinde kalacak şekilde."""
    size = 1080
    p = gradient((size, size), [(0.0, NAVY), (0.45, MIA_DEEP), (1.0, MIA_DARK)], angle=0.6)
    m = mark(660)
    p.alpha_composite(m, ((size - m.width) // 2, (size - m.height) // 2))
    return p.convert("RGB")


README = """# Instagram ızgara seti — MİA PARK OCEAN

Bu klasörü `scripts/build-instagram-grid.py` üretir; elle düzenlemeyin,
betiği çalıştırın:

    python3 scripts/build-instagram-grid.py

## Ne var burada

* `01-…` … `{son}` — her klasör TEK bir geniş görselin üç parçası.
  Profil ızgarasında bu üç parça yan yana gelip tek kare gibi görünür.
* `_izgara-gorunumu.jpg` — o panelin ızgarada nasıl görüneceği.
* `IZGARA-ONIZLEME.jpg` — profilin tamamının maketi (en yeni üstte).
* `profil-fotografi.jpg` — profil resmi (1080x1080).

## Nasıl paylaşılır

1. Parçaları **dosya adındaki sıraya göre** paylaşın: `paylasim-1`,
   sonra `paylasim-2`, sonra `paylasim-3`. Instagram en yeniyi sola
   koyduğu için satır bu sırayla soldan sağa dizilir.
2. Bir paneli bitirmeden diğerine geçmeyin; yarım kalan satır ızgarayı
   bozar.
3. Panel klasörlerini numara sırasıyla ilerletin (01 → {no}).
4. `01-karsidan-sabit` klasörünün üç parçasını **sabitleyin**. Instagram
   üç gönderi sabitlemeye izin verir; böylece o panel her zaman en üst
   satırda tek bir geniş görsel olarak durur.
5. Kırpma ekranında görsel tam oturur: akışta 4:5 yüklenir, ızgarada 3:4
   kırpılır ve fazlalık zaten hesaba katılmıştır.

## Ölçüler

| | |
|---|---|
| Akış gönderisi | 1080 x 1350 (4:5) |
| Izgarada görünen | 1012 x 1350 (3:4) |
| Panel | 3104 x 1350 |
| Parça bindirmesi | 68 px |
"""


# ---------------------------------------------------------------- ana akış
def main() -> None:
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)

    names = ["sol", "orta", "sag"]
    previews = []
    for slug, title, fn in PANELS:
        panel = fn().convert("RGB")
        d = os.path.join(OUT, slug)
        os.makedirs(d)

        # Parçalar — dosya adı paylaşım sırasını taşır
        for i, off in enumerate(OFFSETS):
            tile = panel.crop((off, 0, off + TILE_W, TILE_H))
            order = 3 - i  # önce sağdaki paylaşılır
            tile.save(os.path.join(d, f"paylasim-{order}--parca-{i + 1}-{names[i]}.jpg"),
                      quality=94, optimize=True)

        # Panelin ızgarada görüneceği hâli — yalnızca referans, yarı ölçek
        grid_view = panel.crop((BLEED, 0, PANEL_W - BLEED, PANEL_H))
        grid_view.resize((GRID_W * 3 // 2, PANEL_H // 2), Image.LANCZOS).save(
            os.path.join(d, "_izgara-gorunumu.jpg"), quality=86, optimize=True)
        previews.append((title, grid_view))
        print(f"  {slug}: 3 parça + ızgara önizlemesi")

    pp = profile_picture()
    pp.save(os.path.join(OUT, "profil-fotografi.jpg"), quality=95, optimize=True)
    print("  profil-fotografi.jpg 1080x1080")

    # Profil maketi — sabitlenen panel üstte, kalanlar EN YENİDEN eskiye
    order = [previews[0]] + previews[1:][::-1]
    gap, tw = 8, 360
    th = round(tw * PANEL_H / GRID_W)
    board = Image.new("RGB", (tw * 3 + gap * 2, (th + gap) * len(order) - gap), (250, 252, 253))
    for r, (_, gv) in enumerate(order):
        row = gv.resize((tw * 3 + gap * 2, th), Image.LANCZOS)
        for c in range(3):
            piece = row.crop((c * (tw + gap), 0, c * (tw + gap) + tw, th))
            board.paste(piece, (c * (tw + gap), r * (th + gap)))
    board.save(os.path.join(OUT, "IZGARA-ONIZLEME.jpg"), quality=84, optimize=True)
    print(f"  IZGARA-ONIZLEME.jpg {board.width}x{board.height}")

    with open(os.path.join(OUT, "README.md"), "w", encoding="utf-8") as f:
        f.write(README.format(son=PANELS[-1][0], no=f"{len(PANELS):02d}"))
    print(f"  README.md · {len(PANELS)} panel = {len(PANELS) * 3} gönderi")


if __name__ == "__main__":
    main()
