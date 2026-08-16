#!/usr/bin/env python3
"""
MİA PARK OCEAN — sinematik tanıtım filmi.

1920x1080 · 25 fps · ~80 saniye. Kareler PIL ile üretilip ffmpeg'e ham RGB
olarak akıtılır; ara PNG yazılmaz.

KAMERA
──────
Elimizde video değil, yüksek çözünürlüklü render'lar var. Bu yüzden kamera
sanal: kaynak görselin içinden zamanla kayan bir dikdörtgen kırpılıp kadraja
ölçeklenir. Kırpma dikdörtgeni 1920'den geniş başladığı için yakınlaşma
gerçek çözünürlükten yenir, yumuşama olmaz.

İNŞAAT YÜKSELİŞİ
────────────────
Boş arazi planı, render'ın kendi gökyüzünden üretilir: ufuk çizgisinin
üstündeki her şey, görselin en üst şeridinden esnetilen gökyüzüyle boyanır.
Sonra gerçek render alttan yukarı yumuşak kenarlı bir maskeyle açılır —
binalar topraktan yükseliyormuş gibi görünür. Uydurma bina yok; ortaya çıkan
şey projenin kendi render'ı.

Çıktı → public/videos/mia-park-ocean-tanitim.mp4
"""

from __future__ import annotations

import math
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import imageio_ffmpeg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "public", "images")
BRAND = os.path.join(ROOT, "public", "brand")
PUBLIC = os.path.join(ROOT, "public")
FONTS = os.path.join(ROOT, "brand-source", "fonts")
OUT = os.path.join(ROOT, "public", "videos", "mia-park-ocean-tanitim.mp4")

W, H = 1920, 1080
FPS = 25

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


# ---------------------------------------------------------------- yardımcı
def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def serif(s: int, w: str = "500") -> ImageFont.FreeTypeFont:
    return font(f"Fraunces-{w}.ttf", s)


def sans(s: int) -> ImageFont.FreeTypeFont:
    return font("Manrope-400.ttf", s)


def sans_b(s: int) -> ImageFont.FreeTypeFont:
    return font("Manrope-700.ttf", s)


def ease(t: float) -> float:
    """Yumuşak giriş-çıkış — kamera hiçbir yerde sertçe durmasın."""
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)


def ease_out(t: float) -> float:
    t = min(max(t, 0.0), 1.0)
    return 1 - (1 - t) ** 3


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def fade(t: float, dur: float, tin: float = 0.6, tout: float = 0.6) -> float:
    """Sahne başında ve sonunda 0-1 arası opaklık zarfı."""
    a = ease(t / tin) if tin > 0 else 1.0
    b = ease((dur - t) / tout) if tout > 0 else 1.0
    return min(a, b)


def track(dr, xy, text, f, fill, sp, anchor="la"):
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


# ---------------------------------------------------------------- kaynaklar
_cache: dict[str, Image.Image] = {}


def source(name: str, scale: float = 1.0) -> Image.Image:
    """Render'ı kamera hareketine yetecek kadar büyütüp önbellekler."""
    key = f"{name}@{scale:.3f}"
    if key not in _cache:
        im = Image.open(os.path.join(IMG, f"{name}.webp")).convert("RGB")
        if scale != 1.0:
            im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
        _cache[key] = im
    return _cache[key]


def logo_white(width: int) -> Image.Image:
    key = f"logo@{width}"
    if key not in _cache:
        im = Image.open(os.path.join(BRAND, "logo-ocean-white.png")).convert("RGBA")
        im = im.crop((0, 0, im.width, 752))
        box = im.getbbox()
        if box:
            im = im.crop(box)
        _cache[key] = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    return _cache[key]


def mark_white(width: int) -> Image.Image:
    key = f"mark@{width}"
    if key not in _cache:
        im = Image.open(os.path.join(BRAND, "mark-ocean-white.png")).convert("RGBA")
        _cache[key] = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    return _cache[key]


def partner_white(width: int) -> Image.Image:
    key = f"partner@{width}"
    if key not in _cache:
        im = Image.open(os.path.join(PUBLIC, "ocean-logo-white.png")).convert("RGBA")
        _cache[key] = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    return _cache[key]


# ---------------------------------------------------------------- kamera
def camera(im: Image.Image, box0, box1, t: float, e=ease) -> Image.Image:
    """
    box = (cx, cy, genişlik_oranı) — kaynak görselin normalize koordinatları.
    Kırpma dikdörtgeni 16:9'a sabitlenir, kadraj dışına taşmaz.
    """
    k = e(t)
    cx = lerp(box0[0], box1[0], k)
    cy = lerp(box0[1], box1[1], k)
    fw = lerp(box0[2], box1[2], k)

    cw = im.width * fw
    ch = cw * H / W
    if ch > im.height:
        ch = im.height
        cw = ch * W / H
    x = min(max(cx * im.width - cw / 2, 0), im.width - cw)
    y = min(max(cy * im.height - ch / 2, 0), im.height - ch)
    crop = im.crop((round(x), round(y), round(x + cw), round(y + ch)))
    return crop.resize((W, H), Image.LANCZOS)


# ---------------------------------------------------------------- renk/ışık
def blur_fast(im: Image.Image, radius: float, f: int = 4) -> Image.Image:
    """
    Geniş yarıçaplı bulanıklık.

    1920x1080'de doğrudan GaussianBlur(26) kare başına yüzlerce ms yiyor.
    Küçültüp bulanıklaştırıp geri büyütmek gözle aynı sonucu veriyor —
    parlama ve gölge zaten düşük frekanslı katmanlar.
    """
    small = im.resize((max(im.width // f, 8), max(im.height // f, 8)), Image.BILINEAR)
    small = small.filter(ImageFilter.GaussianBlur(max(radius / f, 0.6)))
    return small.resize(im.size, Image.BILINEAR)


_VIGNETTE: Image.Image | None = None


def vignette() -> Image.Image:
    global _VIGNETTE
    if _VIGNETTE is None:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        dx = (xx - W / 2) / (W / 2)
        dy = (yy - H / 2) / (H / 2)
        r = np.sqrt(dx * dx + dy * dy) / 1.42
        a = np.clip((r - 0.42) / 0.58, 0, 1) ** 1.7 * 118
        arr = np.zeros((H, W, 4), np.uint8)
        arr[:, :, 3] = a.astype(np.uint8)
        _VIGNETTE = Image.fromarray(arr, "RGBA")
    return _VIGNETTE


def grade(im: Image.Image, teal: float = 0.10, lift: float = 0.0,
          bloom: float = 0.16) -> Image.Image:
    """
    Sinematik derecelendirme: gölgelere petrol mavisi, ışıklara sıcaklık,
    üstüne hafif bir parlama. Render'lar zaten temiz; abartmıyoruz.
    """
    a = np.asarray(im).astype(np.float32) / 255.0
    lum = a @ np.array([0.299, 0.587, 0.114], np.float32)
    sh = np.clip(1.0 - lum * 1.9, 0, 1)[:, :, None]
    hi = np.clip(lum * 1.5 - 0.45, 0, 1)[:, :, None]
    a += sh * np.array([-0.035, 0.020, 0.055], np.float32) * (teal / 0.10)
    a += hi * np.array([0.030, 0.012, -0.012], np.float32)
    a = (a - 0.5) * 1.055 + 0.5 + lift
    out = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8), "RGB")
    if bloom > 0:
        gl = blur_fast(out, 26)
        out = Image.blend(out, Image.blend(out, gl, 1.0), bloom * 0.6)
        out = Image.fromarray(
            np.clip(np.asarray(out).astype(np.float32)
                    + np.asarray(gl).astype(np.float32) * bloom * 0.22, 0, 255).astype(np.uint8), "RGB")
    out = out.convert("RGBA")
    out.alpha_composite(vignette())
    return out.convert("RGB")


# ---------------------------------------------------------------- tipografi
def text_layer(draw_fn) -> Image.Image:
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(layer))
    return layer


def with_shadow(base: Image.Image, layer: Image.Image, blur: int = 22,
                boost: float = 1.9, opacity: float = 1.0) -> Image.Image:
    """Metni okunur kılan yumuşak gölge — perde koyulaştırmadan."""
    if opacity <= 0.003:
        return base
    sh = blur_fast(layer, blur)
    dark = Image.new("RGBA", (W, H), (2, 22, 34, 0))
    dark.putalpha(sh.split()[3].point(lambda v: min(255, int(v * boost * opacity))))
    out = base.convert("RGBA")
    out.alpha_composite(dark)
    if opacity < 1.0:
        layer = layer.copy()
        layer.putalpha(layer.split()[3].point(lambda v: int(v * opacity)))
    out.alpha_composite(layer)
    return out.convert("RGB")


def lower_third(base, title, sub, o: float, y: int = 830, size: int = 96,
                weight: str = "500") -> Image.Image:
    """Sol alt köşe künyesi — çizgi soldan açılır, yazı belirir."""
    if o <= 0.004:
        return base
    x = 150

    def paint(dr):
        w = int(96 * min(o * 1.6, 1.0))
        if w > 2:
            dr.line([x, y - 34, x + w, y - 34], fill=(*MIA_AQUA, 255), width=5)
        dr.text((x, y), title, font=serif(size, weight), fill=(*WHITE, 255))
        if sub:
            track(dr, (x + 3, y + size + 26), sub, sans_b(30), (*MIA_ICE, 255), 12)

    return with_shadow(base, text_layer(paint), opacity=o)


def centered(base, lines, o: float, y0: int = 430) -> Image.Image:
    """Ortada tipografi bloğu: (metin, punto, font_tipi, renk, satır_arası)."""
    if o <= 0.004:
        return base

    def paint(dr):
        y = y0
        for text, size, kind, color, gap in lines:
            if kind == "serif":
                dr.text((W / 2, y), text, font=serif(size, "600"), fill=(*color, 255), anchor="ma")
            elif kind == "serif-light":
                dr.text((W / 2, y), text, font=serif(size, "500"), fill=(*color, 255), anchor="ma")
            elif kind == "track":
                track(dr, (W / 2, y), text, sans_b(size), (*color, 255), 16, "ma")
            else:
                dr.text((W / 2, y), text, font=sans(size), fill=(*color, 255), anchor="ma")
            y += gap

    return with_shadow(base, text_layer(paint), opacity=o)


def brandbar(base: Image.Image, o: float = 1.0) -> Image.Image:
    """Sağ üstte küçük marka imzası — film boyunca sabit."""
    if o <= 0.01:
        return base
    lg = logo_white(210)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    layer.alpha_composite(lg, (W - 150 - lg.width, 78))
    return with_shadow(base, layer, blur=18, boost=1.4, opacity=o * 0.92)


# ---------------------------------------------------------------- inşaat
_GRAD: dict[tuple[int, int], Image.Image] = {}


def _band(w: int, h: int) -> Image.Image:
    if (w, h) not in _GRAD:
        col = (np.linspace(0, 1, h, dtype=np.float32) ** 0.85 * 255).astype(np.uint8)
        _GRAD[(w, h)] = Image.fromarray(np.repeat(col[:, None], w, axis=1), "L")
    return _GRAD[(w, h)]


def rise_mask(size, edge: int, soft: int = 130) -> Image.Image:
    """Kenarın ALTI beyaz (gerçek render), ÜSTÜ siyah (boş arazi)."""
    w, h = size
    m = Image.new("L", (w, h), 255)
    top = max(edge - soft, 0)
    if top > 0:
        ImageDraw.Draw(m).rectangle([0, 0, w, top], fill=0)
    if edge > 0:
        band = _band(w, min(soft, max(edge, 1)))
        m.paste(band, (0, top))
    return m


_PLATE: dict[str, Image.Image] = {}


def empty_plate(name: str, scale: float, horizon: float) -> Image.Image:
    """
    Boş arazi planı — render'ın KENDİ gökyüzünden üretilir.

    Ufkun üstü, görselin en üst şeridinden esnetilerek boyanır; ufka ince bir
    pus bandı konur. Böylece binalar yokken de ışık, renk ve hava aynı kalır.
    """
    key = f"{name}@{scale}"
    if key in _PLATE:
        return _PLATE[key]
    im = source(name, scale)
    w, h = im.size
    hy = int(h * horizon)
    sky = im.crop((0, 0, w, max(int(h * 0.05), 8))).resize((w, hy + 60), Image.BICUBIC)
    sky = sky.filter(ImageFilter.GaussianBlur(14))
    plate = im.copy()
    plate.paste(sky, (0, 0))
    # ufuk pusu — uzaktaki ağaç hattının yerini tutar
    haze = im.crop((0, hy - 14, w, hy + 34)).resize((w, 120), Image.BICUBIC)
    haze = haze.filter(ImageFilter.GaussianBlur(34))
    plate.paste(haze, (0, hy - 96), _band(w, 120).point(lambda v: 30 + int(v * 0.55)))
    plate = Image.composite(plate, im, rise_mask((w, h), hy + 30, 90).point(lambda v: 255 - v))
    _PLATE[key] = plate
    return plate


# ---------------------------------------------------------------- sahneler
# (isim, süre) sırası TIMELINE'da. Her sahne yerel t saniyesini alır.

GATE_SCALE = 1.55
GATE_HORIZON = 0.70        # entrance-gate'te binaların oturduğu hat
GATE_GROUND = 0.695


def sc_land(t: float, d: float) -> Image.Image:
    """01 · Boş arazi. Kamera yolun üstünden yavaşça yükselir."""
    plate = empty_plate("entrance-gate", GATE_SCALE, GATE_HORIZON)
    f = camera(plate, (0.52, 0.86, 0.52), (0.50, 0.62, 0.72), t / d)
    f = grade(f, teal=0.13, bloom=0.2)
    o = fade(t, d, 1.4, 0.7)
    f = centered(f, [
        ("İZMİT MİA BÖLGESİ", 40, "track", MIA_ICE, 96),
        ("Burada bir şey başlıyor.", 104, "serif-light", WHITE, 0),
    ], o * 0.96, y0=430)
    return f


def sc_rise(t: float, d: float) -> Image.Image:
    """02 · Binalar yükseliyor. Gerçek render alttan yukarı açılır."""
    real = source("entrance-gate", GATE_SCALE)
    plate = empty_plate("entrance-gate", GATE_SCALE, GATE_HORIZON)
    w, h = real.size
    k = ease(min(t / (d * 0.82), 1.0))
    edge = int(h * GATE_GROUND * (1 - k))
    frame = Image.composite(real, plate, rise_mask((w, h), edge, 140))

    # yükselen kenarda ışık — "büyüme" hissi
    if 0.02 < k < 0.99:
        glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        a = int(150 * math.sin(min(k, 1.0) * math.pi) ** 0.6)
        gd.rectangle([0, edge - 8, w, edge + 8], fill=(*MIA_ICE, a))
        glow = glow.filter(ImageFilter.GaussianBlur(26))
        frame = Image.alpha_composite(frame.convert("RGBA"), glow).convert("RGB")

    f = camera(frame, (0.50, 0.62, 0.72), (0.50, 0.55, 0.94), t / d)
    f = grade(f, teal=0.11, bloom=0.18)
    o = fade(t, d, 0.7, 0.8)
    f = lower_third(f, "600 daire", "4 BLOK · 8 KAT · 4 YAŞAM TİPİ", o * ease(max(t - d * 0.45, 0) / 0.9))
    return f


def sc_reveal(t: float, d: float) -> Image.Image:
    """03 · Proje adı."""
    f = camera(source("entrance-gate", GATE_SCALE), (0.50, 0.55, 0.94), (0.48, 0.53, 0.80), t / d)
    f = grade(f, teal=0.10, bloom=0.2)
    o = fade(t, d, 0.8, 0.8)
    lg = logo_white(560)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    layer.alpha_composite(lg, ((W - lg.width) // 2, 300))
    f = with_shadow(f, layer, blur=30, boost=1.6, opacity=o)
    f = centered(f, [("İZMİT'İN YENİ MERKEZİNDE", 38, "track", MIA_ICE, 0)],
                 o * ease(max(t - 1.2, 0) / 1.0), y0=760)
    return f


def sc_aerial(t: float, d: float) -> Image.Image:
    """04 · Havadan geçiş."""
    f = camera(source("aerial-pools", 1.45), (0.36, 0.46, 0.62), (0.64, 0.54, 0.72), t / d)
    f = grade(f, teal=0.12)
    o = fade(t, d, 0.7, 0.7)
    f = lower_third(f, "Merkezi avlu", "SÜS HAVUZLARI · GENİŞ PEYZAJ", o)
    return brandbar(f, o)


def sc_dusk(t: float, d: float) -> Image.Image:
    """05 · Akşam avlusu."""
    f = camera(source("hero-courtyard-dusk", 1.5), (0.50, 0.58, 0.86), (0.50, 0.50, 0.66), t / d)
    f = grade(f, teal=0.15, bloom=0.24)
    o = fade(t, d, 0.7, 0.7)
    f = lower_third(f, "Akşamları başka", "MİMARİ AYDINLATMA", o)
    return brandbar(f, o)


def sc_street(t: float, d: float) -> Image.Image:
    """06 · Sokak cephesi."""
    f = camera(source("street-corner", 1.5), (0.62, 0.44, 0.66), (0.40, 0.54, 0.80), t / d)
    f = grade(f, teal=0.11)
    o = fade(t, d, 0.7, 0.7)
    f = lower_third(f, "Zemin katta ticaret", "GÜVENLİ, YAŞAYAN BİR SOKAK", o)
    return brandbar(f, o)


# ---------------------------------------------------------------- callout
def callout(base: Image.Image, o: float, k: float, anchor, side: int,
            big: str, rows) -> Image.Image:
    """
    Daire tipi etiketi: noktadan çıkan çizgi, ucunda künye.

    k 0→1 çizgiyi uzatır, ardından yazı belirir. side +1 sağa, -1 sola.
    """
    if o <= 0.004:
        return base
    ax, ay = anchor[0] * W, anchor[1] * H
    diag = 150.0
    lx = ax + side * diag
    ly = ay - diag
    run = 300.0 * ease(min(k * 1.35, 1.0))
    ex = lx + side * run

    def paint(dr):
        r = 9
        dr.ellipse([ax - r, ay - r, ax + r, ay + r], fill=(*MIA_ICE, 255))
        dr.ellipse([ax - 22, ay - 22, ax + 22, ay + 22], outline=(*MIA_AQUA, 180), width=3)
        kk = ease(min(k * 1.6, 1.0))
        dr.line([ax, ay, ax + side * diag * kk, ay - diag * kk], fill=(*MIA_ICE, 230), width=4)
        if run > 4:
            dr.line([lx, ly, ex, ly], fill=(*MIA_ICE, 230), width=4)
        to = ease(max(k - 0.42, 0) / 0.5)
        if to <= 0.01:
            return
        tx = lx + side * 34
        anc = "la" if side > 0 else "ra"
        col = (*WHITE, int(255 * to))
        dr.text((tx, ly - 118), big, font=serif(96, "600"), fill=col, anchor=anc)
        y = ly + 22
        for row in rows:
            track(dr, (tx, y), row, sans_b(32), (*MIA_ICE, int(250 * to)), 12,
                  "la" if side > 0 else "ra")
            y += 50

    return with_shadow(base, text_layer(paint), blur=20, boost=1.7, opacity=o)


def unit_scene(name, scale, box0, box1, anchor, side, big, rows, label):
    def fn(t: float, d: float) -> Image.Image:
        f = camera(source(name, scale), box0, box1, t / d)
        f = grade(f, teal=0.10, bloom=0.14)
        o = fade(t, d, 0.5, 0.5)
        k = ease_out(min(max(t - 0.25, 0) / 1.05, 1.0))
        f = callout(f, o, k, anchor, side, big, rows)
        f = brandbar(f, o)
        if label:
            f = lower_third(f, label, "", o * 0.9, y=940, size=54)
        return f
    return fn


sc_u1 = unit_scene("unit-1plus0-a", 1.35, (0.46, 0.50, 0.70), (0.54, 0.52, 0.60),
                   (0.30, 0.60), 1, "1+0", ["BRÜT 28 m²", "472 DAİRE"], "")
sc_u2 = unit_scene("unit-1plus1-a", 1.35, (0.56, 0.50, 0.70), (0.46, 0.52, 0.60),
                   (0.70, 0.62), -1, "1+1", ["BRÜT 50 m²", "96 DAİRE"], "")
sc_u3 = unit_scene("loft-living", 1.4, (0.42, 0.52, 0.68), (0.56, 0.50, 0.60),
                   (0.28, 0.64), 1, "1+1 Bahçe Loft", ["BRÜT 50 m²", "16 DAİRE"], "")
sc_u4 = unit_scene("duplex-cutaway", 1.5, (0.50, 0.50, 0.86), (0.50, 0.52, 0.66),
                   (0.66, 0.66), -1, "2+1 Bahçe Dubleks", ["BRÜT 100 m²", "16 DAİRE"], "")


def sc_social(t: float, d: float) -> Image.Image:
    """11 · Sosyal donatılar."""
    f = camera(source("courtyard-pools", 1.45), (0.40, 0.52, 0.64), (0.60, 0.48, 0.74), t / d)
    f = grade(f, teal=0.12, bloom=0.18)
    o = fade(t, d, 0.6, 0.7)
    f = lower_third(f, "Her gün tatil konforu", "HAVUZLAR · YÜRÜYÜŞ YOLLARI · SPOR ALANLARI", o)
    return brandbar(f, o)


# ---------------------------------------------------------------- konum
def bg_gradient(t: float, d: float) -> Image.Image:
    """Marka mavisi zemin — yavaşça kayan bir ışıkla."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    k = xx / W * 0.6 + yy / H * 0.4
    stops = [(0.0, np.array((5, 46, 66), np.float32)),
             (0.55, np.array(MIA_DEEP, np.float32)),
             (1.0, np.array((20, 108, 140), np.float32))]
    arr = np.zeros((H, W, 3), np.float32)
    for i in range(len(stops) - 1):
        t0, c0 = stops[i]
        t1, c1 = stops[i + 1]
        m = (k >= t0) & (k <= t1)
        q = np.clip((k - t0) / (t1 - t0), 0, 1)[:, :, None]
        arr = np.where(m[:, :, None], c0 + (c1 - c0) * q, arr)
    cx = W * (0.5 + 0.06 * math.sin(t / d * math.pi))
    dd = np.sqrt((xx - cx) ** 2 + (yy - H * 0.42) ** 2) / (W * 0.72)
    arr += np.clip(1 - dd, 0, 1)[:, :, None] ** 2.1 * np.array(MIA_CYAN, np.float32) * 0.30
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")


def sc_map(t: float, d: float) -> Image.Image:
    """12 · Konum — halkalar açılır, mesafeler belirir."""
    f = bg_gradient(t, d)
    cx, cy = W / 2, H * 0.46
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dr = ImageDraw.Draw(layer)
    g = ease(min(t / 2.2, 1.0))
    for i, r0 in enumerate([120, 235, 365, 510, 670, 850, 1050]):
        r = r0 * lerp(0.55, 1.0, ease(min(max(t - i * 0.13, 0) / 1.5, 1.0)))
        a = int(84 * (0.9 ** i) * g)
        dr.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(*MIA_LIGHT, a), width=3)
    for kk in range(12):
        ang = math.radians(kk * 30)
        dr.line([cx + 120 * math.cos(ang), cy + 120 * math.sin(ang),
                 cx + 1050 * math.cos(ang), cy + 1050 * math.sin(ang)],
                fill=(*MIA_LIGHT, int(24 * g)), width=2)
    r = 86
    dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*MIA_ICE, int(34 * g)),
               outline=(*MIA_ICE, int(190 * g)), width=4)
    f = Image.alpha_composite(f.convert("RGBA"), layer).convert("RGB")

    m = mark_white(96)
    ml = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ml.alpha_composite(m, (int(cx - m.width / 2), int(cy - m.height / 2 - 2)))
    f = with_shadow(f, ml, blur=16, boost=1.2, opacity=g)

    pins = [(-1, -1, "D-100 KARAYOLU", "1 dk", 0.9),
            (1, -1, "ŞEHİR MERKEZİ", "5 dk", 1.5),
            (-1, 1, "ÜNİVERSİTE", "yakın", 2.1),
            (1, 1, "HASTANE", "yakın", 2.7)]

    def paint(dr2):
        for sx, sy, label, dist, t0 in pins:
            o2 = ease(min(max(t - t0, 0) / 0.9, 1.0))
            if o2 <= 0.01:
                continue
            px = cx + sx * W * 0.29
            py = cy + sy * H * 0.27
            a = int(255 * o2)
            dr2.ellipse([px - 9, py - 9, px + 9, py + 9], fill=(*MIA_ICE, a))
            dr2.ellipse([px - 24, py - 24, px + 24, py + 24], outline=(*MIA_AQUA, int(170 * o2)), width=3)
            track(dr2, (px, py + 42), label, sans_b(31), (*MIA_ICE, a), 12, "ma")
            dr2.text((px, py + 88), dist, font=serif(64, "600"), fill=(*WHITE, a), anchor="ma")

    f = with_shadow(f, text_layer(paint), blur=18, boost=1.3, opacity=fade(t, d, 0.5, 0.7))
    o = fade(t, d, 0.6, 0.7)
    f = centered(f, [("İzmit MİA Bölgesi", 74, "serif", WHITE, 0)],
                 o * ease(max(t - 3.2, 0) / 1.0), y0=int(H * 0.86))
    return f


# ---------------------------------------------------------------- finansman
def sc_finance(t: float, d: float) -> Image.Image:
    """13 · Faizsiz finansman — rakamlar sayarak gelir."""
    f = bg_gradient(t, d)
    o = fade(t, d, 0.6, 0.7)

    k1 = ease(min(max(t - 0.4, 0) / 1.1, 1.0))
    k2 = ease(min(max(t - 1.0, 0) / 1.3, 1.0))
    ay = int(round(60 * k2))

    def paint(dr):
        track(dr, (W / 2, 200), "TASARRUFA DAYALI FİNANSMAN", sans_b(38), (*MIA_LIGHT, 240), 16, "ma")
        dr.text((W * 0.30, 560), "%0", font=serif(230, "700"), fill=(*WHITE, int(255 * k1)), anchor="ms")
        track(dr, (W * 0.30, 610), "FAİZ", sans_b(40), (*MIA_ICE, int(250 * k1)), 20, "ma")
        dr.line([W / 2, 380, W / 2, 640], fill=(*MIA_LIGHT, int(90 * k1)), width=3)
        dr.text((W * 0.70, 560), f"{ay}", font=serif(230, "700"), fill=(*WHITE, int(255 * k2)), anchor="ms")
        track(dr, (W * 0.70, 610), "AY VADE", sans_b(40), (*MIA_ICE, int(250 * k2)), 20, "ma")
        k3 = ease(min(max(t - 2.6, 0) / 1.0, 1.0))
        if k3 > 0.01:
            dr.text((W / 2, 760), "Bankasız. Faizsiz. Kefilsiz.",
                    font=serif(78, "500"), fill=(*MIA_PALE, int(255 * k3)), anchor="ma")
            dr.text((W / 2, 880), "Vade farkı yok, ara ödeme yok, taksit sabit.",
                    font=sans(42), fill=(*MIA_ICE, int(235 * k3)), anchor="ma")

    return with_shadow(f, text_layer(paint), blur=20, boost=1.2, opacity=o)


# ---------------------------------------------------------------- kapanış
def sc_close(t: float, d: float) -> Image.Image:
    """14 · Gece + logo kapanışı."""
    f = camera(source("night-gate", 1.5), (0.50, 0.52, 0.90), (0.50, 0.50, 0.70), t / d)
    f = grade(f, teal=0.16, bloom=0.28)

    dim = ease(min(max(t - 1.6, 0) / 1.8, 1.0))
    if dim > 0.01:
        veil = Image.new("RGBA", (W, H), (3, 26, 40, int(190 * dim)))
        f = Image.alpha_composite(f.convert("RGBA"), veil).convert("RGB")

    o = fade(t, d, 0.8, 1.2)
    ko = ease(min(max(t - 2.0, 0) / 1.4, 1.0))
    if ko > 0.01:
        lg = logo_white(620)
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        layer.alpha_composite(lg, ((W - lg.width) // 2, 250))
        pm = partner_white(210)
        layer.alpha_composite(pm, ((W - pm.width) // 2, 900))
        layer.putalpha(layer.split()[3].point(lambda v: int(v * ko)))
        f = with_shadow(f, layer, blur=28, boost=1.4, opacity=o)

    k4 = ease(min(max(t - 3.2, 0) / 1.2, 1.0))
    f = centered(f, [
        ("miaparkocean.com", 52, "sans", MIA_ICE, 78),
        ("0540 028 00 41", 52, "sans", MIA_ICE, 0),
    ], o * k4, y0=700)
    return f


# ---------------------------------------------------------------- zaman çizgisi
TIMELINE = [
    ("bos-arazi", sc_land, 6.4),
    ("yukselis", sc_rise, 8.2),
    ("proje", sc_reveal, 6.0),
    ("havadan", sc_aerial, 5.8),
    ("aksam", sc_dusk, 5.4),
    ("sokak", sc_street, 5.0),
    ("1plus0", sc_u1, 4.6),
    ("1plus1", sc_u2, 4.6),
    ("loft", sc_u3, 4.6),
    ("dubleks", sc_u4, 5.0),
    ("donati", sc_social, 5.4),
    ("konum", sc_map, 7.0),
    ("finansman", sc_finance, 6.6),
    ("kapanis", sc_close, 7.4),
]

XFADE = 0.55   # sahneler arası çapraz geçiş


def total_duration() -> float:
    return sum(d for _, _, d in TIMELINE) - XFADE * (len(TIMELINE) - 1)


# ---------------------------------------------------------------- müzik
SR = 44100

# Dm – Bb – F – C · her akor 8 sn. Alt oktavda kök, üstte açık aralıklar:
# sinematik yatak burada; melodi yok, çünkü altına konuşma/alt yazı gelebilir.
CHORDS = [
    (62, [50, 57, 62, 65, 69]),   # Dm
    (58, [46, 53, 58, 62, 65]),   # Bb
    (53, [41, 48, 53, 57, 60]),   # F
    (60, [48, 55, 60, 64, 67]),   # C
]
CHORD_LEN = 8.0


def _hz(midi: float) -> float:
    return 440.0 * 2 ** ((midi - 69) / 12.0)


def _voice(f: float, n: int, detune: float = 0.0) -> np.ndarray:
    """Yumuşak, harmonikleri sönen bir ses — tek sinüs kadar cansız değil."""
    tt = np.arange(n, dtype=np.float32) / SR
    out = np.zeros(n, np.float32)
    for h, amp in ((1, 1.0), (2, 0.42), (3, 0.20), (4, 0.11), (5, 0.06), (6, 0.035)):
        ph = 2 * math.pi * f * h * (1 + detune) * tt
        out += amp * np.sin(ph + h * 0.7)
    # yavaş nefes
    out *= 1.0 + 0.06 * np.sin(2 * math.pi * 0.13 * tt + f % 3)
    return out / 1.85


def _env(n: int, attack: float, release: float) -> np.ndarray:
    e = np.ones(n, np.float32)
    a = int(SR * attack)
    r = int(SR * release)
    if a > 0:
        x = np.linspace(0, 1, min(a, n), dtype=np.float32)
        e[:min(a, n)] *= x * x * (3 - 2 * x)
    if r > 0 and r < n:
        x = np.linspace(1, 0, r, dtype=np.float32)
        e[-r:] *= x * x * (3 - 2 * x)
    return e


def _reverb(x: np.ndarray, mix: float = 0.34) -> np.ndarray:
    """Schroeder tarzı basit yankı — mekân hissi için yeterli."""
    out = np.zeros_like(x)
    for delay_ms, g in ((37.1, 0.78), (41.9, 0.75), (49.3, 0.72), (58.7, 0.70)):
        d = int(SR * delay_ms / 1000)
        buf = np.zeros_like(x)
        buf[d:] = x[:-d]
        # geri beslemeli sönüm
        acc = buf.copy()
        for _ in range(4):
            nxt = np.zeros_like(acc)
            nxt[d:] = acc[:-d] * g
            acc = nxt
            out += acc
    out /= 9.0
    return x * (1 - mix) + out * mix


def score(duration: float) -> np.ndarray:
    """Filmle aynı uzunlukta, iki kanallı sinematik yatak."""
    n = int(SR * duration)
    tt = np.arange(n, dtype=np.float32) / SR
    pad = np.zeros(n, np.float32)
    sub = np.zeros(n, np.float32)
    shimmer = np.zeros(n, np.float32)

    i = 0
    pos = 0.0
    while pos < duration:
        root, notes = CHORDS[i % len(CHORDS)]
        seg = int(SR * min(CHORD_LEN + 2.2, duration - pos + 2.2))
        if seg <= 0:
            break
        start = int(SR * pos)
        env = _env(seg, 1.5, 2.4)
        for j, m in enumerate(notes):
            v = _voice(_hz(m), seg, detune=0.0018 * (j - 2))
            end = min(start + seg, n)
            pad[start:end] += (v * env)[:end - start] * (0.34 if j else 0.42)
        v = np.sin(2 * math.pi * _hz(root - 24) * np.arange(seg, dtype=np.float32) / SR)
        end = min(start + seg, n)
        sub[start:end] += (v * env)[:end - start] * 0.5

        # parlaklık — akorun üst sesleri iki oktav yukarıda, çok kısık.
        # Yatağın tamamı bas bölgede kalırsa film boğuk duyuluyor.
        ts = np.arange(seg, dtype=np.float32) / SR
        for j, mn in enumerate(notes[-2:]):
            sh = np.sin(2 * math.pi * _hz(mn + 24) * ts)
            sh *= 1.0 + 0.3 * np.sin(2 * math.pi * (0.6 + 0.13 * j) * ts + j)
            shimmer[start:end] += (sh * env)[:end - start] * 0.055

        pos += CHORD_LEN
        i += 1

    # hava — çok kısık, sadece dokusu için
    rng = np.random.default_rng(11)
    raw = rng.normal(0, 1, n).astype(np.float32)
    k = 24
    low = np.convolve(raw, np.ones(k, np.float32) / k, mode="same")
    air = (raw - low) * 0.055          # tiz "hava"
    air += low * 0.9                   # altında ince bir uğultu

    # nabız: binalar yükselmeye başlayınca girer
    pulse = np.zeros(n, np.float32)
    beat = 2.0
    b = 6.0
    while b < duration - 1.0:
        s0 = int(SR * b)
        ln = int(SR * 1.1)
        e = np.exp(-np.linspace(0, 7, ln, dtype=np.float32))
        f0 = np.sin(2 * math.pi * 52 * np.arange(ln, dtype=np.float32) / SR)
        end = min(s0 + ln, n)
        pulse[s0:end] += (f0 * e)[:end - s0] * 0.34
        b += beat

    mix = pad * 0.5 + sub * 0.40 + shimmer * 0.9 + air * 0.5 + pulse
    mix = _reverb(mix, 0.32)

    # filmin yayı: açılış kısık, yükseliş büyür, kapanışta iner
    shape = np.interp(tt, [0, 5, 8, 20, duration - 12, duration - 2, duration],
                      [0.42, 0.55, 0.95, 0.85, 0.9, 0.62, 0.0]).astype(np.float32)
    mix *= shape
    mix = np.tanh(mix * 1.30) * 0.80

    # hafif genişlik: kanallar arasında birkaç örneklik kayma
    d = 380
    left = mix.copy()
    right = np.zeros_like(mix)
    right[d:] = mix[:-d]
    right = right * 0.94 + mix * 0.06
    st = np.stack([left, right], axis=1)
    st *= _env(n, 1.2, 1.6)[:, None]
    return np.clip(st, -1, 1)


# ---------------------------------------------------------------- kurgu
def scene_starts():
    s, out = 0.0, []
    for _, _, d in TIMELINE:
        out.append(s)
        s += d - XFADE
    return out


def frame_at(T: float, starts) -> Image.Image:
    """T anındaki kare; sahneler XFADE kadar üst üste binerek geçer."""
    active = [(i, T - starts[i]) for i in range(len(TIMELINE))
              if 0 <= T - starts[i] < TIMELINE[i][2]]
    if not active:
        active = [(len(TIMELINE) - 1, TIMELINE[-1][2] - 0.001)]
    if len(active) == 1:
        i, lt = active[0]
        return TIMELINE[i][1](lt, TIMELINE[i][2])
    (i0, t0), (i1, t1) = active[0], active[1]
    a = TIMELINE[i0][1](t0, TIMELINE[i0][2])
    b = TIMELINE[i1][1](t1, TIMELINE[i1][2])
    return Image.blend(a, b, ease(min(t1 / XFADE, 1.0)))


_STARTS = None


def _init_worker(starts) -> None:
    global _STARTS
    _STARTS = starts


def _render_frame(k: int) -> bytes:
    return frame_at(k / FPS, _STARTS).tobytes()


def write_score(path: str, dur: float) -> None:
    import wave
    st = (score(dur) * 32767).astype(np.int16)
    with wave.open(path, "wb") as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes(st.tobytes())


def user_track() -> str | None:
    """public/videos/muzik.(wav|mp3|m4a) varsa sentezlenen yatak yerine o kullanılır."""
    for ext in ("wav", "mp3", "m4a", "aac"):
        p = os.path.join(os.path.dirname(OUT), f"muzik.{ext}")
        if os.path.exists(p):
            return p
    return None


def remux_audio() -> None:
    """Görüntüyü yeniden üretmeden yalnızca sesi değiştirir."""
    dur = total_duration()
    src = user_track()
    tmp = os.path.join(os.path.dirname(OUT), "_ses.wav")
    if src is None:
        write_score(tmp, dur)
        src = tmp
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    tmp_out = OUT + ".tmp.mp4"
    subprocess.run([ff, "-y", "-i", OUT, "-i", src, "-map", "0:v:0", "-map", "1:a:0",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest",
                    "-movflags", "+faststart", tmp_out],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    os.replace(tmp_out, OUT)
    if os.path.exists(tmp):
        os.remove(tmp)
    print(f"ses yenilendi · {os.path.getsize(OUT) / 1048576:.1f} MB")


def main() -> None:
    if "--ses" in sys.argv:
        remux_audio()
        return
    dur = total_duration()
    starts = scene_starts()

    if "--preview" in sys.argv:
        outdir = sys.argv[sys.argv.index("--preview") + 1]
        os.makedirs(outdir, exist_ok=True)
        for T in [1.0, 4.0, 8.0, 11.0, 14.0, 18.0, 23.0, 28.0, 34.0, 38.5,
                  43.0, 47.5, 52.5, 58.0, 63.0, 70.0, 76.0, 80.0]:
            if T >= dur:
                continue
            frame_at(T, starts).save(os.path.join(outdir, f"t{T:05.1f}.jpg"), quality=88)
            print(f"  kare {T:5.1f}s")
        print(f"süre: {dur:.2f} s")
        return

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    wav = user_track()
    own = wav is None
    if own:
        wav = os.path.join(os.path.dirname(OUT), "_muzik.wav")
        write_score(wav, dur)
        print(f"müzik (sentez): {dur:.1f} s")
    else:
        print(f"müzik (dosya): {os.path.basename(wav)}")

    ff = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [ff, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-i", wav,
           "-c:v", "libx264", "-preset", "slow", "-crf", "20",
           "-pix_fmt", "yuv420p", "-profile:v", "high", "-movflags", "+faststart",
           "-c:a", "aac", "-b:a", "160k", "-shortest", OUT]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    total = int(dur * FPS)

    # Kareler birbirinden bağımsız; çekirdek sayısı kadar paralel üretilip
    # sıraya girerek ffmpeg'e yazılır. Tek çekirdekte ~15 dk süren iş
    # dört çekirdekte ~5 dk'ya iniyor.
    workers = max(1, min(4, (os.cpu_count() or 2)))
    if workers > 1:
        import multiprocessing as mp
        with mp.Pool(workers, initializer=_init_worker, initargs=(starts,)) as pool:
            for k, buf in enumerate(pool.imap(_render_frame, range(total), chunksize=8)):
                proc.stdin.write(buf)
                if k % 100 == 0:
                    print(f"  {k:4d}/{total}  ({k / FPS:5.1f} s)", flush=True)
    else:
        for k in range(total):
            proc.stdin.write(frame_at(k / FPS, starts).tobytes())
            if k % 100 == 0:
                print(f"  {k:4d}/{total}  ({k / FPS:5.1f} s)", flush=True)
    proc.stdin.close()
    proc.wait()
    if own:
        os.remove(wav)
    mb = os.path.getsize(OUT) / 1048576
    print(f"{os.path.basename(OUT)} · {dur:.1f} s · {mb:.1f} MB")


if __name__ == "__main__":
    main()
