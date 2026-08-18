#!/usr/bin/env python3
"""
MİA PARK OCEAN — Instagram Reels (3 adet dikey video).

1080x1920 · 25 fps · her biri ~22 sn. Kaynak, iki dakikalık tanıtım
filminin ÇEKİMLERİ: film-source/clips/ altındaki aynı mp4'ler.

NEDEN YENİDEN KURGU, NEDEN KIRPMA DEĞİL
───────────────────────────────────────
Filmi 9:16'ya kırpmak iki şeyi bozuyordu: yazılar 16:9'a göre
yerleştirildiği için kenarlardan kesiliyor, kadraj da yatay kompozisyona
göre kurulduğu için ortası boş kalıyordu. Bunun yerine çekimler dikey
olarak yeniden kadrajlanıyor ve tipografi baştan dikeye kuruluyor.

GÜVENLİ ALAN
────────────
Instagram reels arayüzü altta ~340 px (kullanıcı adı, açıklama), sağda
~160 px (beğeni/yorum tuşları) kaplıyor. Bu yüzden yazılar y 1200-1460
bandında ve solda duruyor; alt üçlük ekranda hiçbir tuşun altında kalmıyor.

KAPAKLAR
────────
Üç reels'in kapağı TEK bir geniş görselin üç parçası. Profil ızgarasında
yan yana gelip kesintisiz bir satır oluşturuyor. Ayrıntı: cover_panel().

Çıktı → social-media/reels/
"""

from __future__ import annotations

import math
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# Film betiği tire içerdiği için doğrudan import edilemiyor; yoldan yükleniyor.
# Çekim önbelleği, derecelendirme ve müzik onunla ORTAK: reels'ler filmin
# kendi kareleriyle kuruluyor, ikinci bir kaynak yok.
import importlib.util as _il                                   # noqa: E402

_spec = _il.spec_from_file_location(
    "build_film", os.path.join(os.path.dirname(os.path.abspath(__file__)), "build-film.py"))
bf = _il.module_from_spec(_spec)
sys.modules["build_film"] = bf
_spec.loader.exec_module(bf)

ROOT = bf.ROOT
FONTS = bf.FONTS
OUT = os.path.join(ROOT, "social-media", "reels")

W, H = 1080, 1920
FPS = bf.FPS
FF = bf.FF
SRC_W, SRC_H = bf.W, bf.H          # kaynak karelerin ölçüsü (1920x1080)

NAVY = bf.NAVY
MIA_DEEP = bf.MIA_DEEP
MIA_DARK = bf.MIA_DARK
MIA_CYAN = bf.MIA_CYAN
MIA_AQUA = bf.MIA_AQUA
MIA_LIGHT = bf.MIA_LIGHT
MIA_PALE = bf.MIA_PALE
MIA_ICE = (221, 247, 250)
WHITE = (255, 255, 255)

XFADE = 0.5
WORD_Y = 1330          # büyük kelimenin taban çizgisi
CAP_Y = 1398           # alt başlık
SAFE_X = 78


# ---------------------------------------------------------------- yazı
def serif(s: int, w: str = "500") -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(os.path.join(FONTS, f"Fraunces-{w}.ttf"), s)


def sans(s: int, w: str = "400") -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(os.path.join(FONTS, f"Manrope-{w}.ttf"), s)


def track(dr, xy, text, f, fill, sp, anchor="la"):
    widths = [dr.textlength(c, font=f) for c in text]
    total = sum(widths) + sp * max(len(text) - 1, 0)
    x, y = xy
    if anchor[0] == "m":
        x -= total / 2
    elif anchor[0] == "r":
        x -= total
    for c, w in zip(text, widths):
        dr.text((x, y), c, font=f, fill=fill)
        x += w + sp
    return total


def wrap(dr, text: str, f, max_w: int):
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


def fit_lines(dr, text: str, start: int, max_w: int, max_lines: int = 2, w: str = "600"):
    """En çok `max_lines` satıra sığan en büyük punto.

    Uzun bir cümleyi tek satıra sıkıştırmak reels'te puntoyu telefonda
    okunmayacak kadar küçültüyor; iki satıra bölmek hem büyük hem okunur
    tutuyor.
    """
    size = start
    while size > 48:
        f = serif(size, w)
        if len(wrap(dr, text, f, max_w)) <= max_lines:
            return f, wrap(dr, text, f, max_w)
        size -= 3
    f = serif(size, w)
    return f, wrap(dr, text, f, max_w)


# ---------------------------------------------------------------- görüntü
_VIG: Image.Image | None = None


def vignette() -> Image.Image:
    """Dikey kadraja göre köşe karartma — filmin yataydakinin dikey eşi."""
    global _VIG
    if _VIG is None:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        dx = (xx - W / 2) / (W / 2)
        dy = (yy - H / 2) / (H / 2)
        r = np.sqrt(dx * dx + dy * dy) / 1.42
        a = np.clip((r - 0.50) / 0.55, 0, 1) ** 1.7 * 86
        arr = np.zeros((H, W, 4), np.uint8)
        arr[:, :, 3] = a.astype(np.uint8)
        _VIG = Image.fromarray(arr, "RGBA")
    return _VIG


def grade(im: Image.Image, teal: float = 0.09, bloom: float = 0.12) -> Image.Image:
    a = np.asarray(im).astype(np.float32) / 255.0
    lum = a @ np.array([0.299, 0.587, 0.114], np.float32)
    sh = np.clip(1.0 - lum * 1.9, 0, 1)[:, :, None]
    hi = np.clip(lum * 1.5 - 0.45, 0, 1)[:, :, None]
    a += sh * np.array([-0.030, 0.018, 0.048], np.float32) * (teal / 0.09)
    a += hi * np.array([0.026, 0.010, -0.010], np.float32)
    a = (a - 0.5) * 1.045 + 0.5
    out = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8), "RGB")
    if bloom > 0:
        gl = bf.blur_fast(out, 24)
        out = Image.fromarray(
            np.clip(np.asarray(out).astype(np.float32)
                    + np.asarray(gl).astype(np.float32) * bloom * 0.30, 0, 255).astype(np.uint8), "RGB")
    out = out.convert("RGBA")
    out.alpha_composite(vignette())
    return out.convert("RGB")


def vcrop(im: Image.Image, px: float, zoom: float) -> Image.Image:
    """
    1920x1080 kareden 9:16 pencere keser.

    px pencerenin yatay konumu (0 sol, 1 sağ). Sahne boyunca kaydırmak
    hem hareket katıyor hem de yatay kadrajın daha çoğunu gösteriyor —
    sabit orta kırpma dikeyde çok şey kaybettiriyor.
    """
    ch = SRC_H / zoom
    cw = ch * W / H
    x = (SRC_W - cw) * min(max(px, 0.0), 1.0)
    y = (SRC_H - ch) / 2
    box = (round(x), round(y), round(x + cw), round(y + ch))
    return im.crop(box).resize((W, H), Image.LANCZOS)


_FC: dict = {}


def clip_frame_smooth(name: str, t: float, speed: float = 1.0, offset: float = 0.0) -> Image.Image:
    """
    Klibin t anındaki karesi — komşu iki kare harmanlanarak.

    build_film.clip_frame kare indisini YUVARLIYOR. Hız 1'in altındayken
    indis her çıktı karesinde bir artmıyor, aynı kaynak karesi üst üste
    basılıyor: hız 0,5'te çıktının yarısı tekrar, ekranda tak tak eden
    bir titreme. Kesirli indiste iki komşu kareyi karıştırmak indisi
    sürekli kılıyor, tekrar eden kare kalmıyor.
    """
    fs = bf.clip_dir(name)
    x = (offset + t * speed) * FPS
    i0 = min(max(int(math.floor(x)), 0), len(fs) - 1)
    frac = x - math.floor(x)
    i1 = min(i0 + 1, len(fs) - 1)

    def read(i):
        p = fs[i]
        im = _FC.get(p)
        if im is None:
            im = Image.open(p).convert("RGB")
            if len(_FC) > 6:
                _FC.clear()
            _FC[p] = im
        return im

    a = read(i0)
    if frac < 0.02 or i1 == i0:
        return a
    return Image.blend(a, read(i1), frac)


def text_layer(fn) -> Image.Image:
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fn(ImageDraw.Draw(layer))
    return layer


def with_shadow(base: Image.Image, layer: Image.Image, blur: int = 20,
                boost: float = 1.9, opacity: float = 1.0) -> Image.Image:
    sh = layer.filter(ImageFilter.GaussianBlur(blur))
    dark = Image.new("RGBA", (W, H), (2, 22, 34, 0))
    dark.putalpha(sh.split()[3].point(lambda v: min(255, int(v * boost * opacity))))
    base = base.convert("RGBA")
    base.alpha_composite(dark)
    if opacity < 1.0:
        layer = layer.copy()
        layer.putalpha(layer.split()[3].point(lambda v: int(v * opacity)))
    base.alpha_composite(layer)
    return base.convert("RGB")


def brandmark(base: Image.Image, o: float = 1.0) -> Image.Image:
    """Sol üstte logo — reels boyunca sabit."""
    lg = bf.logo_white(300)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    layer.alpha_composite(lg, (SAFE_X, 108))
    if o < 1:
        layer.putalpha(layer.split()[3].point(lambda v: int(v * o)))
    return with_shadow(base, layer, blur=18, boost=1.4)


def bottom_scrim() -> Image.Image:
    """Yalnızca yazının oturduğu alt banda perde."""
    arr = np.zeros((H, 1, 4), np.float32)
    ys = np.linspace(0, 1, H)
    stops = [(0.0, 90), (0.13, 0), (0.52, 0), (0.72, 70), (0.86, 165), (1.0, 205)]
    for i in range(len(stops) - 1):
        t0, a0 = stops[i]
        t1, a1 = stops[i + 1]
        idx = np.where((ys >= t0) & (ys <= t1))[0]
        if len(idx):
            k = (ys[idx] - t0) / max(t1 - t0, 1e-6)
            arr[idx, 0, 3] = a0 + (a1 - a0) * k
    arr[:, :, 0], arr[:, :, 1], arr[:, :, 2] = 3, 32, 48
    return Image.fromarray(arr.astype(np.uint8), "RGBA").resize((W, H), Image.BILINEAR)


_SCRIM: Image.Image | None = None


def scrim() -> Image.Image:
    global _SCRIM
    if _SCRIM is None:
        _SCRIM = bottom_scrim()
    return _SCRIM


# ---------------------------------------------------------------- sahne
def vshot(name: str, word: str, cap: str, pan=(0.5, 0.5), zoom=(1.0, 1.06),
          offset: float = 0.0, speed: float = 1.0):
    """Dikey kadrajlı çekim + alt üçlükte kelime ve başlık."""
    def scene(t: float, d: float) -> Image.Image:
        # Kaydırma DOĞRUSAL. smoothstep ile yumuşatılınca sahnenin başında
        # ve sonunda kamera hızı sıfıra iniyordu; iki kesmenin arasında
        # görüntü donuyormuş gibi duruyordu. Sabit hızda kayan pencere
        # kesmeden kesmeye akışı kesmiyor.
        k = min(max(t / d, 0.0), 1.0)
        im = clip_frame_smooth(name, t, speed, offset)
        im = vcrop(im, pan[0] + (pan[1] - pan[0]) * k, zoom[0] + (zoom[1] - zoom[0]) * k)
        im = grade(im)
        im = Image.alpha_composite(im.convert("RGBA"), scrim()).convert("RGB")

        o = bf.fade(t, d, 0.55, 0.45)
        if o > 0.01 and word:
            rise = round((1 - bf.ease_out(min(t / 0.7, 1.0))) * 26)

            def paint(dr):
                f, lines = fit_lines(dr, word, 122, W - SAFE_X * 2 - 90)
                lh = round(f.size * 1.18)
                top = WORD_Y - lh * (len(lines) - 1)
                for k, ln in enumerate(lines):
                    dr.text((SAFE_X, top + k * lh + rise), ln, font=f, fill=WHITE, anchor="ls")
                if cap:
                    track(dr, (SAFE_X, CAP_Y + rise), cap, sans(34, "600"), (*MIA_ICE, 246), 9)

            im = with_shadow(im, text_layer(paint), opacity=o)
        return brandmark(im)
    return scene


def vc_end(clip: str, offset: float = 0.0, speed: float = 0.8):
    """
    Kapanış kartı — koyulaştırılmış GERÇEK çekim üstünde logo.

    Önce marka gradyanı kullanılıyordu ve kartın 4,6 saniyesi boyunca
    ekranda hiçbir şey kıpırdamıyordu; ölçtüğümüzde her üç reels'in de
    son 3,7 saniyesi kare kare aynı çıktı. Arkaya ağır perdeli bir çekim
    koyup yavaşça içeri girmek, hem donmayı bitiriyor hem de kart marka
    zemininde durmaya devam ediyor.
    """
    def scene(t: float, d: float) -> Image.Image:
        k = min(max(t / d, 0.0), 1.0)
        im = clip_frame_smooth(clip, t, speed, offset)
        im = vcrop(im, 0.5, 1.04 + 0.10 * k)          # yavaş içeri giriş
        im = grade(im, teal=0.14, bloom=0.06)
        # Perde 205 alfayla neredeyse opaktı, üstüne 9 piksel bulanıklık
        # binince arkadaki hareket hiç görünmüyordu. Yazının okunurluğunu
        # zaten with_shadow sağlıyor; perde hafifleyince kart yaşıyor.
        im = bf.blur_fast(im, 4)
        im = Image.alpha_composite(
            im.convert("RGBA"),
            Image.new("RGBA", (W, H), (3, 30, 46, 152))).convert("RGB")

        o = bf.fade(t, d, 0.6, 0.4)
        lg = bf.logo_white(660)
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        layer.alpha_composite(lg, ((W - lg.width) // 2, 700))
        dr = ImageDraw.Draw(layer)
        track(dr, (W / 2, 1170), "İZMİT MİA BÖLGESİ", sans(36, "600"), (*MIA_PALE, 240), 14, "ma")
        dr.line([W / 2 - 90, 1268, W / 2 + 90, 1268], fill=(*MIA_AQUA, 210), width=4)
        dr.text((W / 2, 1410), "600 daire, dört yaşam tipi", font=serif(72, "500"),
                fill=WHITE, anchor="ms")
        track(dr, (W / 2, 1480), "DETAYLAR PROFİLDEKİ BAĞLANTIDA", sans(32, "700"),
              (*MIA_ICE, 240), 10, "ma")
        pm = bf.partner_white(210)
        layer.alpha_composite(pm, ((W - pm.width) // 2, 1630))
        if o < 1:
            layer.putalpha(layer.split()[3].point(lambda v: int(v * o)))
        return with_shadow(im, layer, blur=18, boost=1.2)
    return scene


# ---------------------------------------------------------------- reels
REELS = [
    ("reel-1-proje", "Proje", [
        (vshot("13-giris-drone", "Sahile iki dakika", "İZMİT MİA BÖLGESİ",
               pan=(0.62, 0.42), zoom=(1.08, 1.0)), 5.4),
        (vshot("08-cephe-yukselis", "Dört blok, sekiz kat", "600 DAİRE · DÖRT YAŞAM TİPİ",
               pan=(0.40, 0.60)), 5.2),
        (vshot("02-sokak-drone", "D100'e bir dakika", "ŞEHİR MERKEZİ VE HASTANE 5 DAKİKA",
               pan=(0.58, 0.40), offset=1.0), 5.2),
        (vshot("01-gunduz-gece", "Işıklar yanınca başka", "ÖZEL GECE AYDINLATMASI",
               pan=(0.45, 0.55)), 5.4),
        (vc_end("14-gece-yaklasim"), 3.8),
    ]),
    ("reel-2-sosyal-yasam", "Sosyal yaşam", [
        (vshot("03-havadan-yorunge", "İster havuzu izleyin, ister denizi",
               "MERKEZİ AVLU · SÜS HAVUZLARI", pan=(0.38, 0.62), zoom=(1.0, 1.08)), 5.6),
        (vshot("04-avlu-suzulme", "Bahçesi olan ev değil, parkı olan ev",
               "YÜRÜYÜŞ YOLLARI · ÇOCUK OYUN PARKI", pan=(0.55, 0.42)), 5.6),
        (vshot("06-teras-sosyal", "Havuz, fitness, hamam",
               "KAPALI YÜZME HAVUZU · SAUNA", pan=(0.42, 0.58)), 5.2),
        (vshot("07-aksam-avlu", "Akşamları başka", "AVLUDA GECE AYDINLATMASI",
               pan=(0.60, 0.44)), 5.2),
        (vc_end("13-giris-drone", offset=1.2), 3.8),
    ]),
    ("reel-3-daireler", "Daireler", [
        (vshot("09-daire-1plus0", "İlk evin tam ölçüsü", "1+0 · BRÜT 28 m² · AÇIK PLAN",
               pan=(0.44, 0.56)), 5.2),
        (vshot("10-daire-1plus1", "Yatak odası ayrı", "1+1 · BRÜT 50 m² · GENİŞ BALKON",
               pan=(0.56, 0.44)), 5.2),
        (vshot("11-bahce-loft", "Zemin katta kendi bahçeniz", "1+1 BAHÇE LOFT · BRÜT 50 m²",
               pan=(0.42, 0.58)), 5.4),
        (vshot("12-bahce-dubleks", "Bahçeniz, evinizin devamı", "2+1 BAHÇE DUBLEKS · BRÜT 100 m²",
               pan=(0.58, 0.42), speed=0.5), 5.6),
        (vc_end("14-gece-yaklasim", offset=2.0), 3.8),
    ]),
]


def starts_of(scenes):
    s, out = 0.0, []
    for _, d in scenes:
        out.append(s)
        s += d - XFADE
    return out


def duration_of(scenes) -> float:
    return sum(d for _, d in scenes) - XFADE * (len(scenes) - 1)


def frame_at(T: float, scenes, starts) -> Image.Image:
    """
    Sahneler XFADE kadar bindirilir; bindirme aralığında iki kare karışır.

    Önceki kurguda geçiş hiç çalışmıyordu: `cur` zaten T'yi içeren SON
    sahne olduğu için "T >= bir sonrakinin başlangıcı" koşulu hiçbir
    zaman sağlanmıyor, her yer sert kesme oluyordu. Doğrusu, yeni sahnenin
    ilk XFADE saniyesinde bir ÖNCEKİ sahneyle karıştırmak.
    """
    cur = 0
    for i, s in enumerate(starts):
        if T >= s:
            cur = i
    fn, d = scenes[cur]
    im = fn(min(T - starts[cur], d), d)
    local = T - starts[cur]
    if cur > 0 and local < XFADE:
        fp, dp = scenes[cur - 1]
        prev = fp(min(T - starts[cur - 1], dp), dp)
        im = Image.blend(prev, im, bf.ease(local / XFADE))
    return im


# ---------------------------------------------------------------- kapaklar
# Üç kapak TEK bir geniş görselin üç parçası.
#
# Instagram profil ızgarası her hücreyi 3:4 gösterir. Reels kapağı ise
# 1080x1920 (9:16) yüklenir ve ızgarada DİKEY ORTASINDAN 3:4 kırpılır:
# 1080x1440, yani y 240-1680 arası. Tasarım o banda kuruluyor; üstteki ve
# alttaki 240'ar piksel yalnızca Reels sekmesinde görünen taşma payı.
COVER_W, COVER_H = W * 3, H          # 3240 x 1920
GRID_TOP, GRID_BOT = 240, 1680       # ızgarada görünen bant


def cover_panel() -> Image.Image:
    src = os.path.join(ROOT, "signage-source", "night-gate.jpg")
    if not os.path.exists(src):
        src = os.path.join(ROOT, "public", "images", "night-gate.webp")
    im = Image.open(src).convert("RGB")
    s = max(COVER_W / im.width, COVER_H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im.width - COVER_W) // 2
    y = round((im.height - COVER_H) * 0.5)
    p = im.crop((x, y, x + COVER_W, y + COVER_H)).convert("RGBA")

    # perde: ızgara bandının alt yarısı koyulaşsın, yazı otursun
    arr = np.zeros((COVER_H, 1, 4), np.float32)
    ys = np.linspace(0, 1, COVER_H)
    for t0, a0, t1, a1 in [(0.0, 150, 0.18, 60), (0.18, 60, 0.46, 40),
                           (0.46, 40, 0.72, 140), (0.72, 140, 1.0, 232)]:
        idx = np.where((ys >= t0) & (ys <= t1))[0]
        if len(idx):
            k = (ys[idx] - t0) / max(t1 - t0, 1e-6)
            arr[idx, 0, 3] = a0 + (a1 - a0) * k
    arr[:, :, 0], arr[:, :, 1], arr[:, :, 2] = 3, 30, 46
    p.alpha_composite(Image.fromarray(arr.astype(np.uint8), "RGBA").resize((COVER_W, COVER_H), Image.BILINEAR))

    dr = ImageDraw.Draw(p)
    words = [("Proje", "MİMARİ · KONUM"), ("Sosyal yaşam", "AVLU · HAVUZ · PEYZAJ"),
             ("Daireler", "DÖRT YAŞAM TİPİ")]
    # Ortak punto: üç kelime de aynı boyda olsun, satır tek parça okunsun
    size = 150
    while size > 60 and max(dr.textlength(w, font=serif(size, "600")) for w, _ in words) > W - 150:
        size -= 4
    f = serif(size, "600")

    layer = Image.new("RGBA", (COVER_W, COVER_H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    for i, (word, cap) in enumerate(words):
        cx = W * i + W / 2
        ld.text((cx, 1180), word, font=f, fill=WHITE, anchor="ms")
        track(ld, (cx, 1240), cap, sans(34, "600"), (*MIA_ICE, 244), 10, "ma")
        # oynat işareti — kapağın reels olduğu belli olsun
        r = 34
        ld.ellipse([cx - r, 1350 - r, cx + r, 1350 + r], outline=(*MIA_PALE, 210), width=4)
        ld.polygon([(cx - 10, 1350 - 15), (cx - 10, 1350 + 15), (cx + 17, 1350)], fill=(255, 255, 255, 230))
        if i:
            ld.line([W * i, GRID_TOP + 60, W * i, GRID_BOT - 60], fill=(*MIA_LIGHT, 55), width=2)

    sh = layer.filter(ImageFilter.GaussianBlur(24))
    dark = Image.new("RGBA", (COVER_W, COVER_H), (2, 22, 34, 0))
    dark.putalpha(sh.split()[3].point(lambda v: min(255, int(v * 1.9))))
    p.alpha_composite(dark)
    p.alpha_composite(layer)

    lg = bf.logo_white(300)
    p.alpha_composite(lg, (SAFE_X, GRID_TOP + 60))
    pm = bf.partner_white(200)
    p.alpha_composite(pm, (COVER_W - SAFE_X - pm.width, GRID_BOT - 60 - pm.height))
    return p.convert("RGB")


# ---------------------------------------------------------------- üretim
_SC = _ST = None


def _init(sc, st):
    global _SC, _ST
    _SC, _ST = sc, st


def _render(k: int) -> bytes:
    return frame_at(k / FPS, _SC, _ST).tobytes()


def build_reel(slug: str, scenes) -> None:
    dur = duration_of(scenes)
    starts = starts_of(scenes)
    wav = os.path.join(OUT, f"_{slug}.wav")
    bf.write_score(wav, dur)

    path = os.path.join(OUT, f"{slug}.mp4")
    cmd = [FF, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-i", wav,
           "-c:v", "libx264", "-preset", "medium", "-crf", "20",
           "-pix_fmt", "yuv420p", "-profile:v", "high", "-movflags", "+faststart",
           "-c:a", "aac", "-b:a", "160k", "-shortest", path]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    total = int(dur * FPS)
    import multiprocessing as mp
    workers = max(1, min(4, (os.cpu_count() or 2)))
    with mp.Pool(workers, initializer=_init, initargs=(scenes, starts)) as pool:
        for k, buf in enumerate(pool.imap(_render, range(total), chunksize=6)):
            proc.stdin.write(buf)
    proc.stdin.close()
    proc.wait()
    os.remove(wav)
    print(f"  {slug}.mp4 · {dur:.1f} s · {os.path.getsize(path) / 1048576:.1f} MB")


def main() -> None:
    os.makedirs(OUT, exist_ok=True)

    # kapaklar
    panel = cover_panel()
    panel.save(os.path.join(OUT, "kapaklar-panel.jpg"), quality=92)
    grid = panel.crop((0, GRID_TOP, COVER_W, GRID_BOT))
    grid.resize((COVER_W // 2, (GRID_BOT - GRID_TOP) // 2), Image.LANCZOS).save(
        os.path.join(OUT, "kapaklar-izgara-onizleme.jpg"), quality=88)
    for i, (slug, _t, _s) in enumerate(REELS):
        panel.crop((W * i, 0, W * (i + 1), COVER_H)).save(
            os.path.join(OUT, f"{slug}-kapak.jpg"), quality=92)
    print(f"  kapaklar: 3 x {W}x{COVER_H} + panel {COVER_W}x{COVER_H}")

    if "--sadece-kapak" in sys.argv:
        return

    for slug, _title, scenes in REELS:
        build_reel(slug, scenes)
    print(f"\n  → {OUT}")


if __name__ == "__main__":
    main()
