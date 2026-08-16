#!/usr/bin/env python3
"""
MİA PARK OCEAN — sinematik tanıtım filmi (sürüm 2).

1920x1080 · 25 fps · ~2 dakika. Bu sürümde sahneler GERÇEK VİDEO:
Higgsfield'de projenin kendi render'larından üretilen kamera hareketli
çekimler. Önceki sürümde durağan görsel üstünde kırpma gezdiriliyordu ve
sunumda slayt gibi duruyordu.

ÇEKİMLER
────────
film-source/clips/ altındaki mp4'ler. Her biri projenin bir render'ından
başlatıldı (start_image), böylece ekranda görünen bina uydurma değil:
mimarisi, kapısı, avlusu projenin kendisi. Yeniden üretmek için
film-source/CEKIMLER.md'deki komutlar.

SES
───
scripts/film_score.py — tempolu, davullu, bölüm geçişlerinde yükselişli.
Kurgu kesme noktaları müziğin bölümleriyle hizalı: logo 22. saniyedeki
vuruşta açılır, daire tipleri müzik seyrelince gelir, finansman finalde.

Kendi müziğinizi koymak için: public/videos/muzik.wav → npm run film

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
CLIPS = os.path.join(ROOT, "film-source", "clips")
CACHE = os.path.join(ROOT, "film-source", ".kare-onbellek")
OUT = os.path.join(ROOT, "public", "videos", "mia-park-ocean-tanitim.mp4")

W, H = 1920, 1080
FPS = 25
FF = imageio_ffmpeg.get_ffmpeg_exe()

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
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)


def ease_out(t: float) -> float:
    t = min(max(t, 0.0), 1.0)
    return 1 - (1 - t) ** 3


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def fade(t: float, dur: float, tin: float = 0.5, tout: float = 0.5) -> float:
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


# ---------------------------------------------------------------- çekimler
_index: dict[str, list[str]] = {}


def clip_dir(name: str) -> list[str]:
    """
    mp4'ü bir kez JPEG karelere açar, sonra kare kare okunur.

    8 saniyelik 1080p klibi belleğe almak 1 GB'ı buluyor; diske açmak hem
    ucuz hem de yeniden çalıştırmalarda anında hazır.
    """
    if name in _index:
        return _index[name]
    d = os.path.join(CACHE, name)
    if not os.path.isdir(d) or not os.listdir(d):
        os.makedirs(d, exist_ok=True)
        src = os.path.join(CLIPS, f"{name}.mp4")
        if not os.path.exists(src):
            raise SystemExit(f"çekim yok: {src}")
        subprocess.run(
            [FF, "-y", "-v", "error", "-i", src,
             "-vf", f"fps={FPS},scale={W}:{H}:flags=lanczos",
             "-q:v", "2", os.path.join(d, "%04d.jpg")], check=True)
    _index[name] = sorted(os.path.join(d, f) for f in os.listdir(d) if f.endswith(".jpg"))
    return _index[name]


_frame_cache: tuple[str, Image.Image] | None = None


def clip_frame(name: str, t: float, speed: float = 1.0, offset: float = 0.0) -> Image.Image:
    """Klibin t anındaki karesi. speed<1 ağırlaştırır, sahneyi uzatır."""
    global _frame_cache
    fs = clip_dir(name)
    i = int(round((offset + t * speed) * FPS))
    i = min(max(i, 0), len(fs) - 1)
    p = fs[i]
    if _frame_cache and _frame_cache[0] == p:
        return _frame_cache[1]
    im = Image.open(p).convert("RGB")
    _frame_cache = (p, im)
    return im


def clip_len(name: str) -> float:
    return len(clip_dir(name)) / FPS


# ---------------------------------------------------------------- kaynak
_cache: dict[str, Image.Image] = {}


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


# ---------------------------------------------------------------- görüntü
def blur_fast(im: Image.Image, radius: float, f: int = 4) -> Image.Image:
    small = im.resize((max(im.width // f, 8), max(im.height // f, 8)), Image.BILINEAR)
    small = small.filter(ImageFilter.GaussianBlur(max(radius / f, 0.6)))
    return small.resize(im.size, Image.BILINEAR)


_VIG: Image.Image | None = None


def vignette() -> Image.Image:
    global _VIG
    if _VIG is None:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        dx = (xx - W / 2) / (W / 2)
        dy = (yy - H / 2) / (H / 2)
        r = np.sqrt(dx * dx + dy * dy) / 1.42
        a = np.clip((r - 0.45) / 0.55, 0, 1) ** 1.7 * 96
        arr = np.zeros((H, W, 4), np.uint8)
        arr[:, :, 3] = a.astype(np.uint8)
        _VIG = Image.fromarray(arr, "RGBA")
    return _VIG


def grade(im: Image.Image, teal: float = 0.09, bloom: float = 0.12) -> Image.Image:
    """Hafif sinematik derecelendirme — çekimler zaten güzel ışıklı."""
    a = np.asarray(im).astype(np.float32) / 255.0
    lum = a @ np.array([0.299, 0.587, 0.114], np.float32)
    sh = np.clip(1.0 - lum * 1.9, 0, 1)[:, :, None]
    hi = np.clip(lum * 1.5 - 0.45, 0, 1)[:, :, None]
    a += sh * np.array([-0.030, 0.018, 0.048], np.float32) * (teal / 0.09)
    a += hi * np.array([0.026, 0.010, -0.010], np.float32)
    a = (a - 0.5) * 1.045 + 0.5
    out = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8), "RGB")
    if bloom > 0:
        gl = blur_fast(out, 24)
        out = Image.fromarray(
            np.clip(np.asarray(out).astype(np.float32)
                    + np.asarray(gl).astype(np.float32) * bloom * 0.30, 0, 255).astype(np.uint8), "RGB")
    out = out.convert("RGBA")
    out.alpha_composite(vignette())
    return out.convert("RGB")


def punch(im: Image.Image, k: float) -> Image.Image:
    """Çekimin üstüne hafif ek yakınlaşma — kesmeler daha canlı olur."""
    if k <= 1.0005:
        return im
    cw, ch = W / k, H / k
    x, y = (W - cw) / 2, (H - ch) / 2
    return im.crop((round(x), round(y), round(x + cw), round(y + ch))).resize((W, H), Image.LANCZOS)


# ---------------------------------------------------------------- tipografi
def text_layer(fn) -> Image.Image:
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fn(ImageDraw.Draw(layer))
    return layer


def with_shadow(base, layer, blur: int = 22, boost: float = 1.9, opacity: float = 1.0):
    if opacity <= 0.004:
        return base
    sh = blur_fast(layer, blur)
    dark = Image.new("RGBA", (W, H), (2, 20, 32, 0))
    dark.putalpha(sh.split()[3].point(lambda v: min(255, int(v * boost * opacity))))
    out = base.convert("RGBA")
    out.alpha_composite(dark)
    if opacity < 1.0:
        layer = layer.copy()
        layer.putalpha(layer.split()[3].point(lambda v: int(v * opacity)))
    out.alpha_composite(layer)
    return out.convert("RGB")


def lower_third(base, title, sub, o: float, y: int = 840, size: int = 84,
                weight: str = "500"):
    """Sol alt künye — çizgi soldan açılır, yazı belirir."""
    if o <= 0.004:
        return base
    x = 140

    def paint(dr):
        w = int(88 * min(o * 1.7, 1.0))
        if w > 2:
            dr.line([x, y - 30, x + w, y - 30], fill=(*MIA_AQUA, 255), width=5)
        dr.text((x, y), title, font=serif(size, weight), fill=(*WHITE, 255))
        if sub:
            track(dr, (x + 3, y + size + 22), sub, sans_b(28), (*MIA_ICE, 255), 11)

    return with_shadow(base, text_layer(paint), opacity=o)


def brandbar(base, o: float = 1.0):
    if o <= 0.01:
        return base
    lg = logo_white(190)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    layer.alpha_composite(lg, (W - 140 - lg.width, 72))
    return with_shadow(base, layer, blur=16, boost=1.3, opacity=o * 0.9)


# ---------------------------------------------------------------- sahneler
def shot(name, title=None, sub=None, zoom=1.0, offset=0.0, speed=1.0,
         teal=0.09, bloom=0.12, bar=True, ty=840, tsize=84):
    """Bir çekim + sol alt künye. Sahnelerin çoğu bu kalıptan."""
    def fn(t: float, d: float) -> Image.Image:
        f = clip_frame(name, t, speed, offset)
        f = punch(f, lerp(1.0, zoom, ease(t / d)) if zoom > 1 else 1.0)
        f = grade(f, teal, bloom)
        o = fade(t, d, 0.5, 0.5)
        if title:
            f = lower_third(f, title, sub, o * ease(min(max(t - 0.5, 0) / 0.8, 1.0)),
                            y=ty, size=tsize)
        return brandbar(f, o) if bar else f
    return fn


# ── 01 · açılış: drone iniyor ──────────────────────────────────────────
def sc_open(t: float, d: float) -> Image.Image:
    f = clip_frame("13-giris-drone", t, 0.92)
    f = grade(f, 0.11, 0.16)
    o = fade(t, d, 1.2, 0.6)

    def paint(dr):
        track(dr, (W / 2, 402), "İZMİT MİA BÖLGESİ", sans_b(36), (*MIA_ICE, 255), 18, "ma")
        dr.text((W / 2, 468), "Burada yeni bir hayat başlıyor.",
                font=serif(96, "500"), fill=(*WHITE, 255), anchor="ma")

    return with_shadow(f, text_layer(paint), opacity=o * 0.97)


# ── 03 · logo açılışı ──────────────────────────────────────────────────
def sc_logo(t: float, d: float) -> Image.Image:
    f = clip_frame("02-sokak-drone", t, 0.95)
    f = grade(f, 0.10, 0.18)
    dim = ease(min(t / 1.1, 1.0))
    veil = Image.new("RGBA", (W, H), (3, 24, 38, int(110 * dim)))
    f = Image.alpha_composite(f.convert("RGBA"), veil).convert("RGB")
    o = fade(t, d, 0.6, 0.7)
    k = ease_out(min(t / 1.6, 1.0))
    lg = logo_white(int(lerp(430, 560, k)))
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    layer.alpha_composite(lg, ((W - lg.width) // 2, 318))
    f = with_shadow(f, layer, blur=30, boost=1.5, opacity=o * k)
    return with_shadow(f, text_layer(lambda dr: track(
        dr, (W / 2, 742), "OCEAN GAYRİMENKUL GÜVENCESİYLE", sans_b(32),
        (*MIA_ICE, 255), 16, "ma")), opacity=o * ease(min(max(t - 1.6, 0) / 1.0, 1.0)))


# ── daire tipi künyesi ─────────────────────────────────────────────────
_SIDE_SCRIM: dict[int, Image.Image] = {}


def side_scrim(side: int) -> Image.Image:
    """Künyenin olduğu yarıyı koyulaştıran yatay perde."""
    if side not in _SIDE_SCRIM:
        x = np.linspace(0, 1, W, dtype=np.float32)
        if side > 0:
            a = np.clip((0.62 - x) / 0.62, 0, 1) ** 1.5
        else:
            a = np.clip((x - 0.38) / 0.62, 0, 1) ** 1.5
        arr = np.zeros((H, W, 4), np.uint8)
        arr[:, :, 0], arr[:, :, 1], arr[:, :, 2] = 2, 20, 32
        arr[:, :, 3] = (a * 168).astype(np.uint8)[None, :]
        _SIDE_SCRIM[side] = Image.fromarray(arr, "RGBA")
    return _SIDE_SCRIM[side]


def unit_shot(name, big, area, count, note, side=1, offset=0.0, speed=0.95):
    def fn(t: float, d: float) -> Image.Image:
        f = clip_frame(name, t, speed, offset)
        f = grade(f, 0.08, 0.10)
        sc = side_scrim(side).copy()
        sc.putalpha(sc.split()[3].point(
            lambda v: int(v * ease(min(max(t - 0.2, 0) / 0.8, 1.0)))))
        f = Image.alpha_composite(f.convert("RGBA"), sc).convert("RGB")
        o = fade(t, d, 0.5, 0.5)
        k = ease_out(min(max(t - 0.3, 0) / 1.1, 1.0))
        if k <= 0.01:
            return brandbar(f, o)
        x = 150 if side > 0 else W - 150
        anc = "la" if side > 0 else "ra"

        def paint(dr):
            wline = int(340 * k)
            dr.line([x, 470, x + side * wline, 470], fill=(*MIA_AQUA, 255), width=5)
            to = ease(max(k - 0.35, 0) / 0.65)
            if to <= 0.01:
                return
            c = int(255 * to)
            dr.text((x, 506), big, font=serif(112, "600"), fill=(*WHITE, c), anchor=anc)
            track(dr, (x + side * 4, 654), f"BRÜT {area}", sans_b(34), (*MIA_ICE, c), 13, anc)
            dr.text((x, 706), count, font=sans_b(52), fill=(*MIA_PALE, c), anchor=anc)
            dr.text((x, 786), note, font=sans(38), fill=(*MIA_ICE, int(232 * to)), anchor=anc)

        f = with_shadow(f, text_layer(paint), opacity=o)
        return brandbar(f, o)
    return fn


# ---------------------------------------------------------------- zeminler
def brand_bg(t: float, d: float, drift: float = 1.0) -> Image.Image:
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    k = xx / W * 0.6 + yy / H * 0.4
    stops = [(0.0, np.array((5, 44, 64), np.float32)),
             (0.55, np.array(MIA_DEEP, np.float32)),
             (1.0, np.array((22, 112, 144), np.float32))]
    arr = np.zeros((H, W, 3), np.float32)
    for i in range(len(stops) - 1):
        t0, c0 = stops[i]
        t1, c1 = stops[i + 1]
        m = (k >= t0) & (k <= t1)
        q = np.clip((k - t0) / (t1 - t0), 0, 1)[:, :, None]
        arr = np.where(m[:, :, None], c0 + (c1 - c0) * q, arr)
    cx = W * (0.5 + 0.07 * math.sin(t / max(d, 1e-6) * math.pi * drift))
    dd = np.sqrt((xx - cx) ** 2 + (yy - H * 0.42) ** 2) / (W * 0.7)
    arr += np.clip(1 - dd, 0, 1)[:, :, None] ** 2.1 * np.array(MIA_CYAN, np.float32) * 0.32
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")


# ── konum · mavi kartlar ───────────────────────────────────────────────
LOC_CARDS = [
    ("D-100 KARAYOLU", "1 dk", "Ana yollara birkaç dakikada"),
    ("ŞEHİR MERKEZİ", "5 dk", "İzmit çarşısı ve sahil bandı"),
    ("ÜNİVERSİTE", "yakın", "Kocaeli Üniversitesi"),
    ("ŞEHİR HASTANESİ", "yakın", "Sağlık kampüsü"),
]


def sc_location(t: float, d: float) -> Image.Image:
    f = brand_bg(t, d)
    cx, cy = W / 2, H * 0.46

    rings = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rings)
    g = ease(min(t / 1.6, 1.0))
    for i, r0 in enumerate([150, 300, 470, 660, 870, 1100]):
        r = r0 * lerp(0.6, 1.0, ease(min(max(t - i * 0.1, 0) / 1.4, 1.0)))
        rd.ellipse([cx - r, cy - r, cx + r, cy + r],
                   outline=(*MIA_LIGHT, int(70 * (0.88 ** i) * g)), width=3)
    f = Image.alpha_composite(f.convert("RGBA"), rings).convert("RGB")

    o = fade(t, d, 0.5, 0.6)

    def paint(dr):
        track(dr, (W / 2, 118), "KONUM AVANTAJI", sans_b(34), (*MIA_LIGHT, int(240 * g)), 18, "ma")
        # dört kart, ikişer sıra
        bw, bh, gap = 620, 176, 34
        x0 = cx - bw - gap / 2
        y0 = cy - bh - gap / 2 + 40
        for i, (label, val, note) in enumerate(LOC_CARDS):
            k = ease(min(max(t - 0.7 - i * 0.28, 0) / 0.85, 1.0))
            if k <= 0.01:
                continue
            bx = x0 + (i % 2) * (bw + gap)
            by = y0 + (i // 2) * (bh + gap) + (1 - k) * 26
            a = int(255 * k)
            dr.rounded_rectangle([bx, by, bx + bw, by + bh], 20,
                                 fill=(*MIA_ICE, int(24 * k)), outline=(*MIA_AQUA, int(120 * k)), width=3)
            track(dr, (bx + 40, by + 28), label, sans_b(29), (*MIA_ICE, a), 12)
            dr.text((bx + 40, by + 68), val, font=serif(70, "600"),
                    fill=(*WHITE, a), anchor="la")
            dr.text((bx + bw - 40, by + 116), note, font=sans(30),
                    fill=(*MIA_PALE, int(228 * k)), anchor="ra")

    # Ortadaki amblem kartların arasından sızıyordu; kartlar zaten alanı
    # dolduruyor, marka imzası sağ üstteki brandbar'da duruyor.
    f = with_shadow(f, text_layer(paint), blur=18, boost=1.2, opacity=o)
    return with_shadow(f, text_layer(lambda dr: dr.text(
        (W / 2, H - 132), "İzmit MİA Bölgesi — şehrin yeni merkezi",
        font=sans(40), fill=(*MIA_ICE, 240), anchor="ma")),
        opacity=o * ease(min(max(t - 2.6, 0) / 1.0, 1.0)))


# ── finansman ──────────────────────────────────────────────────────────
def sc_finance(t: float, d: float) -> Image.Image:
    f = brand_bg(t, d, drift=1.4)
    o = fade(t, d, 0.5, 0.6)
    k1 = ease(min(max(t - 0.3, 0) / 0.9, 1.0))
    k2 = ease(min(max(t - 0.8, 0) / 1.2, 1.0))
    ay = int(round(60 * k2))

    def paint(dr):
        track(dr, (W / 2, 132), "TASARRUFA DAYALI FİNANSMAN", sans_b(36),
              (*MIA_LIGHT, 240), 17, "ma")
        dr.text((W * 0.30, 448), "%0", font=serif(210, "700"),
                fill=(*WHITE, int(255 * k1)), anchor="ms")
        track(dr, (W * 0.30, 484), "FAİZ", sans_b(36), (*MIA_ICE, int(250 * k1)), 18, "ma")
        dr.line([W / 2, 300, W / 2, 500], fill=(*MIA_LIGHT, int(90 * k1)), width=3)
        dr.text((W * 0.70, 448), f"{ay}", font=serif(210, "700"),
                fill=(*WHITE, int(255 * k2)), anchor="ms")
        track(dr, (W * 0.70, 484), "AY VADE", sans_b(36), (*MIA_ICE, int(250 * k2)), 18, "ma")

        k3 = ease(min(max(t - 2.2, 0) / 0.9, 1.0))
        if k3 > 0.01:
            for i, w in enumerate(["Bankasız.", "Faizsiz.", "Kefilsiz."]):
                kk = ease(min(max(t - 2.2 - i * 0.22, 0) / 0.7, 1.0))
                dr.text((W * (0.22 + i * 0.28), 656), w, font=serif(70, "500"),
                        fill=(*MIA_PALE, int(255 * kk)), anchor="ma")
        k4 = ease(min(max(t - 3.4, 0) / 0.9, 1.0))
        if k4 > 0.01:
            dr.text((W / 2, 790), "Vade farkı yok · Ara ödeme yok · Taksit 60 ay sabit",
                    font=sans(40), fill=(*MIA_ICE, int(238 * k4)), anchor="ma")

    return with_shadow(f, text_layer(paint), blur=18, boost=1.2, opacity=o)


# ── kapanış ────────────────────────────────────────────────────────────
def sc_close(t: float, d: float) -> Image.Image:
    f = clip_frame("14-gece-yaklasim", t, 0.9, 1.0)
    f = grade(f, 0.14, 0.22)
    dim = ease(min(max(t - 0.8, 0) / 1.6, 1.0))
    veil = Image.new("RGBA", (W, H), (3, 24, 38, int(196 * dim)))
    f = Image.alpha_composite(f.convert("RGBA"), veil).convert("RGB")
    o = fade(t, d, 0.6, 1.4)
    k = ease_out(min(max(t - 1.0, 0) / 1.3, 1.0))
    if k > 0.01:
        lg = logo_white(600)
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        layer.alpha_composite(lg, ((W - lg.width) // 2, 232))
        pm = partner_white(200)
        layer.alpha_composite(pm, ((W - pm.width) // 2, 902))
        layer.putalpha(layer.split()[3].point(lambda v: int(v * k)))
        f = with_shadow(f, layer, blur=28, boost=1.4, opacity=o)
    k2 = ease(min(max(t - 2.2, 0) / 1.0, 1.0))

    def paint(dr):
        dr.text((W / 2, 660), "miaparkocean.com", font=sans(48),
                fill=(*MIA_ICE, int(250 * k2)), anchor="ma")
        dr.text((W / 2, 736), "0540 028 00 41", font=sans_b(52),
                fill=(*WHITE, int(255 * k2)), anchor="ma")

    return with_shadow(f, text_layer(paint), opacity=o * k2)


# ---------------------------------------------------------------- zaman çizgisi
# Kesmeler müzikle hizalı: 22. saniyedeki vuruşta logo, 58'de müzik seyrelir
# ve daire tipleri başlar, 100'de final bölümü ile finansman gelir.
TIMELINE = [
    ("acilis", sc_open, 8.2),
    ("gunduz-gece", shot("01-gunduz-gece", "Sabahtan geceye", "MİMARİ AYDINLATMA · 7/24 GÜVENLİK", bar=False), 8.0),
    ("gece-yaklasim", shot("14-gece-yaklasim", None, None, bar=False, teal=0.13), 6.4),
    ("logo", sc_logo, 7.6),
    ("cephe", shot("08-cephe-yukselis", "600 daire", "4 BLOK · 8 KAT · 4 YAŞAM TİPİ"), 7.0),
    ("sokak", shot("02-sokak-drone", "Modern mimari", "GENİŞ BALKONLAR · AÇIK PLAN", offset=1.0), 6.8),
    ("havadan", shot("03-havadan-yorunge", "Merkezi avlu", "SÜS HAVUZLARI · GENİŞ PEYZAJ"), 7.0),
    ("avlu", shot("04-avlu-suzulme", "Yürüyüş yolları", "ÇOCUK OYUN PARKI · YEŞİL ALAN"), 6.8),
    ("teras", shot("06-teras-sosyal", "Sosyal ve spor alanları", "KAPALI OTOPARK · 7/24 GÜVENLİK"), 6.8),
    ("balkon", shot("05-balkon-cift", "Geniş balkonlar", "1+0 VE 1+1 DAİRELERDE · ZEMİNDE BAHÇE"), 6.8),
    ("aksam", shot("07-aksam-avlu", "Akşamları başka", "ÖZEL GECE AYDINLATMASI"), 6.6),
    ("u-1plus0", unit_shot("09-daire-1plus0", "1+0", "28 m²", "472 daire", "Akıllı tasarım, maksimum konfor"), 6.8),
    ("u-1plus1", unit_shot("10-daire-1plus1", "1+1", "50 m²", "96 daire", "Ferah, konforlu ve fonksiyonel", side=-1), 6.8),
    ("u-loft", unit_shot("11-bahce-loft", "1+1 Bahçe Loft", "50 m²", "16 daire", "Zemin katta kendi bahçeniz"), 6.8),
    ("u-dubleks", unit_shot("12-bahce-dubleks", "2+1 Bahçe Dubleks", "100 m²", "16 daire", "Bahçeniz, evinizin devamı", side=-1, speed=0.5), 7.2),
    ("konum", sc_location, 8.4),
    ("finansman", sc_finance, 8.4),
    ("kapanis", sc_close, 8.6),
]

XFADE = 0.6


def total_duration() -> float:
    return sum(d for _, _, d in TIMELINE) - XFADE * (len(TIMELINE) - 1)


def scene_starts():
    s, out = 0.0, []
    for _, _, d in TIMELINE:
        out.append(s)
        s += d - XFADE
    return out


def frame_at(T: float, starts) -> Image.Image:
    act = [(i, T - starts[i]) for i in range(len(TIMELINE))
           if 0 <= T - starts[i] < TIMELINE[i][2]]
    if not act:
        act = [(len(TIMELINE) - 1, TIMELINE[-1][2] - 0.001)]
    if len(act) == 1:
        i, lt = act[0]
        return TIMELINE[i][1](lt, TIMELINE[i][2])
    (i0, t0), (i1, t1) = act[0], act[1]
    a = TIMELINE[i0][1](t0, TIMELINE[i0][2])
    b = TIMELINE[i1][1](t1, TIMELINE[i1][2])
    return Image.blend(a, b, ease(min(t1 / XFADE, 1.0)))


# ---------------------------------------------------------------- ses
def user_track():
    for ext in ("wav", "mp3", "m4a", "aac"):
        p = os.path.join(os.path.dirname(OUT), f"muzik.{ext}")
        if os.path.exists(p):
            return p
    return None


def write_score(path: str, dur: float) -> None:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import film_score
    film_score.write(path, dur)


# ---------------------------------------------------------------- ana akış
_STARTS = None


def _init(starts):
    global _STARTS
    _STARTS = starts


def _render(k: int) -> bytes:
    return frame_at(k / FPS, _STARTS).tobytes()


def main() -> None:
    dur = total_duration()
    starts = scene_starts()

    if "--sure" in sys.argv:
        for (n, _, d), s in zip(TIMELINE, starts):
            print(f"  {s:6.1f}  {d:4.1f}  {n}")
        print(f"toplam {dur:.1f} s")
        return

    if "--onizle" in sys.argv:
        outdir = sys.argv[sys.argv.index("--onizle") + 1]
        os.makedirs(outdir, exist_ok=True)
        for (n, _, d), s in zip(TIMELINE, starts):
            T = s + d * 0.55
            frame_at(min(T, dur - 0.05), starts).save(
                os.path.join(outdir, f"{s:06.1f}-{n}.jpg"), quality=88)
            print(f"  {s:6.1f}s {n}")
        return

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    wav = user_track()
    own = wav is None
    if own:
        wav = os.path.join(os.path.dirname(OUT), "_muzik.wav")
        write_score(wav, dur)
        print(f"müzik (sentez) · {dur:.1f} s")
    else:
        print(f"müzik (dosya) · {os.path.basename(wav)}")

    cmd = [FF, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-i", wav,
           "-c:v", "libx264", "-preset", "medium", "-crf", "20",
           "-pix_fmt", "yuv420p", "-profile:v", "high", "-movflags", "+faststart",
           "-c:a", "aac", "-b:a", "160k", "-shortest", OUT]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    total = int(dur * FPS)
    workers = max(1, min(4, (os.cpu_count() or 2)))
    import multiprocessing as mp
    with mp.Pool(workers, initializer=_init, initargs=(starts,)) as pool:
        for k, buf in enumerate(pool.imap(_render, range(total), chunksize=6)):
            proc.stdin.write(buf)
            if k % 150 == 0:
                print(f"  {k:4d}/{total}  ({k / FPS:5.1f} s)", flush=True)
    proc.stdin.close()
    proc.wait()
    if own:
        os.remove(wav)
    print(f"{os.path.basename(OUT)} · {dur:.1f} s · {os.path.getsize(OUT) / 1048576:.1f} MB")


if __name__ == "__main__":
    main()
