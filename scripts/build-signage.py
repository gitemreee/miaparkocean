#!/usr/bin/env python3
"""
MİA PARK OCEAN — saha tabelaları (totem + şantiye çevre afişleri).

ÜRETİLENLER → tabela/
    totem-on-yuz.jpg        1200 x 4000 mm   1:1 @ 75 dpi   (3543 x 11811 px)
    totem-arka-yuz.jpg      1200 x 4000 mm   1:1 @ 75 dpi
    afis-1-kimlik.jpg       3000 x 2400 mm   1:1 @ 50 dpi   (5906 x 4724 px)
    afis-2-finansman.jpg    3000 x 2400 mm
    afis-3-daireler.jpg     3000 x 2400 mm
    afis-4-konum.jpg        3000 x 2400 mm
    afis-5-sosyal-yasam.jpg 3000 x 2400 mm
    onizleme/*.jpg          küçültülmüş kontrol kopyaları
    onizleme/cit-dizilimi.jpg   beş afişin çit boyunca yan yana görünümü

ÖLÇÜ MANTIĞI
────────────
Tasarımın tamamı MİLİMETRE cinsinden yazılır; piksele çeviren tek yer
Board.p(). Tabelacı hangi ölçüde basarsa bassın oran ve güvenli alan
bozulmaz, DPI'ı değiştirip yeniden üretmek yeterlidir.

Büyük format baskıda 1:1 ölçekte 50-75 dpi standarttır: afiş 3-30 m'den,
totem 5-50 m'den okunur. Punto da mm cinsinden verilir — 100 mm'lik bir
em, yaklaşık 72 mm harf yüksekliği demektir ve 30 m'den rahat okunur.

ÇİT BOYUNCA SÜREKLİLİK
──────────────────────
Beş afişin altındaki beyaz künye şeridi aynı yükseklikte durur. Yan yana
asıldıklarında çit boyunca kesintisiz beyaz bir çizgi oluşur; set tek bir
tasarım gibi okunur. Afişlerin sırası değişse de bu bozulmaz.

MARKA KURALLARI
───────────────
· Logo hiçbir zaman renklendirilmez ve daima BEYAZ zemindedir. Bu yüzden
  hem totemin baş bandı hem afişlerin logo plaketi beyazdır.
· Totemde ve afişte tam kilit kullanılır — "İZMİT MİA BÖLGESİ" alt satırı
  bu ölçekte rahat okunur, kırpılmaz.
· Yalnızca projenin belgelenmiş verisi yazılır (units.ts, location.ts,
  amenities.ts, site.ts). Tabelaya uydurma özellik girmez.

Kullanım:
    pip install pillow numpy segno
    python scripts/build-signage.py
"""

from __future__ import annotations

import os
import shutil
import sys

import numpy as np
import segno
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "public", "images")
HIRES = os.path.join(ROOT, "signage-source")     # baskı için büyütülmüş render'lar
BRAND = os.path.join(ROOT, "public", "brand")
PUBLIC = os.path.join(ROOT, "public")
FONTS = os.path.join(ROOT, "brand-source", "fonts")
# Baskı dosyaları siteye konmuyor: 22 MB'lık JPEG'ler her derlemede out/
# içine kopyalanıp yayına çıkardı. Instagram setinde olduğu gibi depo
# içinde duruyor, tabelacıya dosya olarak gidiyor.
OUT = os.path.join(ROOT, "tabela")
PREVIEW = os.path.join(OUT, "onizleme")

# ---------------------------------------------------------------- renkler
# globals.css / mia-brand.css ile birebir
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

DEEP_STOPS = [(0.0, (3, 30, 44)), (0.28, NAVY), (0.62, MIA_DEEP), (1.0, MIA_DARK)]
SURF_STOPS = [(0.0, MIA_DEEP), (0.45, MIA_DARK), (1.0, MIA_OCEAN)]
LIGHT_STOPS = [(0.0, WHITE), (0.42, (240, 251, 253)), (1.0, MIA_PALE)]

# ---------------------------------------------------------------- içerik
# Kaynak: src/data/site.ts, units.ts, location.ts, amenities.ts
SITE = "miaparkocean.com"
PHONES = ["0540 028 00 41", "0541 128 40 41"]
SELLER = "OCEAN GAYRİMENKUL"
SELLER_ROLE = "TEK YETKİLİ SATICI"
QR_TOTEM = "https://miaparkocean.com/?utm_source=totem"
QR_AFIS = "https://miaparkocean.com/?utm_source=saha-afis"
QR_ROLLUP = "https://miaparkocean.com/?utm_source=rollup"
QR_BILBORD = "https://miaparkocean.com/?utm_source=bilbord"
QR_YAKA = "https://miaparkocean.com/?utm_source=lansman"

UNITS = [
    ("1+0", "1+0 Daire", "28 m²", 472),
    ("1+1", "1+1 Daire", "50 m²", 96),
    ("1+1", "1+1 Bahçe Loft", "50 m²", 16),
    ("2+1", "2+1 Bahçe Dubleks", "100 m²", 16),
]
TOTAL_UNITS = sum(u[3] for u in UNITS)          # 600

DISTANCES = [
    ("D100 Karayolu", "1 dk"),
    ("İzmit Sahili", "2 dk"),
    ("41 Burada AVM", "3 dk"),
    ("Şehir Merkezi", "5 dk"),
    ("Şehir Hastanesi", "5 dk"),
    ("TEM Otoyolu", "5 dk"),
    ("Symbol AVM", "7 dk"),
    ("Kocaeli Üniversitesi", "10 dk"),
]

AMENITIES = [
    "MERKEZİ AVLU",
    "SÜS HAVUZLARI",
    "GENİŞ PEYZAJ",
    "YÜRÜYÜŞ YOLLARI",
    "ÇOCUK OYUN PARKI",
    "KAPALI OTOPARK",
    "7/24 GÜVENLİK",
    "GECE AYDINLATMASI",
]


# ---------------------------------------------------------------- tuval
class Board:
    """Milimetre ile çizilen baskı tuvali. p() tek dönüşüm noktasıdır."""

    def __init__(self, w_mm: float, h_mm: float, dpi: int):
        self.w_mm, self.h_mm, self.dpi = w_mm, h_mm, dpi
        self.W, self.H = self.p(w_mm), self.p(h_mm)
        self.im = Image.new("RGBA", (self.W, self.H), (255, 255, 255, 255))

    def p(self, v_mm: float) -> int:
        return round(v_mm * self.dpi / 25.4)

    # -- tipografi: punto da mm cinsinden verilir --------------------------
    def serif(self, size_mm: float, w: str = "500") -> ImageFont.FreeTypeFont:
        return ImageFont.truetype(os.path.join(FONTS, f"Fraunces-{w}.ttf"), self.p(size_mm))

    def sans(self, size_mm: float, w: str = "400") -> ImageFont.FreeTypeFont:
        return ImageFont.truetype(os.path.join(FONTS, f"Manrope-{w}.ttf"), self.p(size_mm))

    @property
    def draw(self) -> ImageDraw.ImageDraw:
        return ImageDraw.Draw(self.im)


def _small(size, cap: int = 1400):
    """Gradyan/ışık gibi yumuşak katmanlar küçük üretilip büyütülür.

    3543 x 11811'lik totemde float32 dizi yarım gigabayt yer kaplıyor;
    yumuşak geçişlerde küçük üretip LANCZOS ile açmak görsel olarak
    ayırt edilemiyor, bellek ise otuzda birine iniyor.
    """
    w, h = size
    s = min(1.0, cap / max(w, h))
    return max(2, round(w * s)), max(2, round(h * s))


def gradient(size, stops, angle: float = 0.5) -> Image.Image:
    sw, sh = _small(size)
    yy, xx = np.mgrid[0:sh, 0:sw].astype(np.float32)
    t = np.clip((xx / max(sw - 1, 1)) * angle + (yy / max(sh - 1, 1)) * (1 - angle), 0, 1)
    arr = np.zeros((sh, sw, 3), np.float32)
    for i in range(len(stops) - 1):
        t0, c0 = stops[i]
        t1, c1 = stops[i + 1]
        m = (t >= t0) & (t <= t1)
        k = np.clip((t - t0) / max(t1 - t0, 1e-6), 0, 1)
        for c in range(3):
            arr[:, :, c] = np.where(m, c0[c] + (c1[c] - c0[c]) * k, arr[:, :, c])
    im = Image.fromarray(arr.astype(np.uint8), "RGB")
    return im.resize(size, Image.LANCZOS).convert("RGBA")


def glow(size, cx: float, cy: float, r: float, color, strength: float = 0.3) -> Image.Image:
    sw, sh = _small(size, 900)
    fx, fy = sw / size[0], sh / size[1]
    yy, xx = np.mgrid[0:sh, 0:sw].astype(np.float32)
    d = np.sqrt(((xx - cx * fx) / (r * fx)) ** 2 + ((yy - cy * fy) / (r * fy)) ** 2)
    a = np.clip(1.0 - d, 0, 1) ** 2.1 * strength
    arr = np.zeros((sh, sw, 4), np.float32)
    for c in range(3):
        arr[:, :, c] = color[c]
    arr[:, :, 3] = a * 255
    im = Image.fromarray(arr.astype(np.uint8), "RGBA")
    return im.resize(size, Image.LANCZOS)


def scrim(size, stops) -> Image.Image:
    """Dikey saydamlık perdesi: [(0-1 konum, (r,g,b,a)), ...]"""
    w, h = size
    sh = min(h, 1600)
    arr = np.zeros((sh, 1, 4), np.float32)
    ys = np.linspace(0, 1, sh)
    for i in range(len(stops) - 1):
        t0, c0 = stops[i]
        t1, c1 = stops[i + 1]
        idx = np.where((ys >= t0) & (ys <= t1))[0]
        if not len(idx):
            continue
        k = (ys[idx] - t0) / max(t1 - t0, 1e-6)
        for c in range(4):
            arr[idx, 0, c] = c0[c] + (c1[c] - c0[c]) * k
    im = Image.fromarray(arr.astype(np.uint8), "RGBA")
    return im.resize((w, h), Image.LANCZOS)


# ---------------------------------------------------------------- görseller
def load(name: str) -> Image.Image:
    """Baskı için büyütülmüş kopya varsa onu, yoksa siteyi kullanır.

    name alt klasör içerebilir: "ic-mekan/09-loft-salon".
    """
    for p in (os.path.join(HIRES, name + ".png"), os.path.join(HIRES, name + ".jpg"),
              os.path.join(IMG, name + ".webp")):
        if os.path.exists(p):
            return Image.open(p).convert("RGB")
    raise SystemExit(f"görsel bulunamadı: {name}")


def overlay(b: "Board", fn) -> None:
    """Yarı saydam çizimi doğru harmanlar.

    ImageDraw bir RGBA görsele çizerken pikselleri harmanlamaz, ALFASIYLA
    BİRLİKTE değiştirir; convert("RGB") sırasında da alfa düşer. Yani
    fill=(255,255,255,38) diye çizilen kart baskıda dümdüz beyaz çıkar.
    Çizimi ayrı katmana yapıp alpha_composite ile bindirmek gerekiyor.
    """
    layer = Image.new("RGBA", b.im.size, (0, 0, 0, 0))
    fn(ImageDraw.Draw(layer))
    b.im.alpha_composite(layer)


def grade(im: Image.Image) -> Image.Image:
    """Büyütme sonrası hafif doygunluk/kontrast toparlaması."""
    from PIL import ImageEnhance
    im = ImageEnhance.Color(im).enhance(1.12)
    return ImageEnhance.Contrast(im).enhance(1.05)


def cover(name: str, size, focus: float = 0.5, sharpen: bool = True) -> Image.Image:
    """Görseli kutuya kırparak sığdırır (focus: dikey odak 0-1)."""
    im = grade(load(name))
    w, h = size
    s = max(w / im.width, h / im.height)
    im = im.resize((max(w, round(im.width * s)), max(h, round(im.height * s))), Image.LANCZOS)
    if sharpen and s > 1.3:
        # Büyütülen render'da cephe hatları ve korkuluklar yeniden toplansın.
        im = im.filter(ImageFilter.UnsharpMask(radius=max(2, round(s)), percent=58, threshold=3))
    x = (im.width - w) // 2
    y = round((im.height - h) * focus)
    return im.crop((x, y, x + w, y + h)).convert("RGBA")


def fit_box(name: str, size, focus: float = 0.5) -> Image.Image:
    return cover(name, size, focus)


# ---------------------------------------------------------------- logolar
def crisp(im: Image.Image, w: int) -> Image.Image:
    """Rasterlanmış logoyu vektöre yakın keskinlikte büyütür.

    Kaynak kilit 1200 px. Totemin baş bandında 900 mm'ye açılıyor; düz
    LANCZOS kenarları yumuşatıp baskıda pofuduk gösteriyor. Alfa geçişini
    dar bir aralığa sıkıştırmak dış hattı geri topluyor, iç gradyan ise
    olduğu gibi kalıyor.
    """
    h = round(im.height * w / im.width)
    im = im.resize((w, h), Image.LANCZOS)
    if w <= im.width:
        pass
    r, g, b, a = im.split()
    lo, hi = 96, 168
    a = a.point(lambda v: 0 if v <= lo else (255 if v >= hi else round((v - lo) * 255 / (hi - lo))))
    rgb = Image.merge("RGB", (r, g, b)).filter(ImageFilter.UnsharpMask(radius=2, percent=70, threshold=2))
    return Image.merge("RGBA", (*rgb.split(), a))


def lockup(width: int, white: bool = False) -> Image.Image:
    """Amblem + MİA PARK OCEAN + İZMİT MİA BÖLGESİ — tam kilit."""
    name = "logo-ocean-white.png" if white else "logo-ocean-trim.png"
    im = Image.open(os.path.join(BRAND, name)).convert("RGBA")
    box = im.getbbox()
    if box:
        im = im.crop(box)
    return crisp(im, width)


def seller_block(b: Board, dr, x: int, y: int, size_mm: float, fill=INK,
                 sub_fill=None, anchor: str = "la") -> None:
    """OCEAN GAYRİMENKUL imzası.

    Elimizdeki ortak logosu 298 px — 400 mm'ye açılınca baskıda dağılıyor.
    Bu yüzden imza tipografik kuruluyor: büyük formatta hem daha temiz
    çıkıyor hem de ölçekten bağımsız keskin kalıyor. Vektör logo gelirse
    signage-source/ocean-logo-hi.png olarak konulup buraya bağlanabilir.
    """
    sub_fill = sub_fill or (*MIA_DARK, 235)
    track(b, dr, (x, y), SELLER, b.sans(size_mm, "700"), fill, b.p(size_mm * 0.16), anchor)
    track(b, dr, (x, y + b.p(size_mm * 1.5)), SELLER_ROLE, b.sans(size_mm * 0.56, "600"),
          sub_fill, b.p(size_mm * 0.2), anchor)


# ---------------------------------------------------------------- tipografi
def track(b: Board, dr, xy, text: str, f, fill, sp: int, anchor: str = "la") -> float:
    """Harf aralıklı metin. anchor ilk harfi: l / m / r"""
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


def fit(b: Board, dr, texts, max_px: int, start_mm: float, maker, floor_mm: float = 8):
    """Hepsinin sığdığı ortak punto — satırlar aynı boyda kalsın."""
    s = start_mm
    texts = [t for t in texts if t]
    while s > floor_mm and max(dr.textlength(t, font=maker(s)) for t in texts) > max_px:
        s *= 0.96
    return maker(s)


def fit_track(b: Board, dr, texts, max_px: int, start_mm: float, sp_ratio: float,
              maker, floor_mm: float = 5):
    s = start_mm
    texts = [t for t in texts if t]
    while s > floor_mm:
        f, sp = maker(s), b.p(s * sp_ratio)
        widest = max(sum(dr.textlength(c, font=f) for c in t) + sp * max(len(t) - 1, 0)
                     for t in texts)
        if widest <= max_px:
            return f, sp
        s *= 0.96
    return maker(s), b.p(s * sp_ratio)


def wrap(dr, text: str, f, max_px: int):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = f"{cur} {w}".strip()
        if dr.textlength(t, font=f) <= max_px:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def soft_text(b: Board, fn, blur_mm: float = 14, alpha: float = 0.62) -> None:
    """Metni önce bulanık koyu bir kopya olarak basar.

    Perdeyi koyulaştırmak yerine yalnızca yazının arkasını gölgeliyoruz:
    render aydınlık kalıyor, yazı her zeminde okunuyor.
    """
    layer = Image.new("RGBA", b.im.size, (0, 0, 0, 0))
    fn(ImageDraw.Draw(layer))
    layer = layer.filter(ImageFilter.GaussianBlur(b.p(blur_mm)))
    a = layer.split()[3].point(lambda v: min(255, round(v * alpha * 2.4)))
    dark = Image.new("RGBA", b.im.size, (2, 22, 34, 0))
    dark.putalpha(a)
    b.im.alpha_composite(dark)
    fn(ImageDraw.Draw(b.im))


# ---------------------------------------------------------------- QR
def qr_image(url: str, px: int, dark=INK) -> Image.Image:
    q = segno.make(url, error="h")
    scale = max(1, px // (q.symbol_size(border=2)[0]))
    buf = os.path.join(OUT, "_qr.png")
    q.save(buf, kind="png", scale=scale, border=2,
           dark="#%02x%02x%02x" % dark, light=None)
    im = Image.open(buf).convert("RGBA").resize((px, px), Image.NEAREST)
    os.remove(buf)
    return im


# ================================================================== TOTEM
# 1200 x 4000 mm, çift yüzlü, ışıklı kutu tabela olarak üretilir.
# Bant düzeni (mm, üstten):
#     0 –  940   beyaz baş bandı        → tam logo kilidi
#   940 – 3280   gradyan gövde          → mesaj
#  3280 – 4000   beyaz ayak künyesi     → QR, web, telefon, satıcı
TOTEM_W, TOTEM_H, TOTEM_DPI = 1200, 4000, 75
HEAD_H, FOOT_Y = 940, 3280
TOTEM_PAD = 95


def totem_shell() -> Board:
    b = Board(TOTEM_W, TOTEM_H, TOTEM_DPI)
    b.im = gradient((b.W, b.H), DEEP_STOPS, angle=0.72)
    b.im.alpha_composite(glow((b.W, b.H), b.p(TOTEM_W * 0.5), b.p(1900),
                              b.p(1500), MIA_CYAN, 0.30))
    b.im.alpha_composite(glow((b.W, b.H), b.p(TOTEM_W), b.p(3200),
                              b.p(1300), MIA_OCEAN, 0.22))

    # -- beyaz baş bandı: logo daima beyaz zeminde --
    dr = b.draw
    dr.rectangle([0, 0, b.W, b.p(HEAD_H)], fill=WHITE)
    lg = lockup(b.p(900))
    b.im.alpha_composite(lg, ((b.W - lg.width) // 2, b.p((HEAD_H - 900 * lg.height / lg.width) / 2)))

    # -- beyaz ayak künyesi --
    dr = b.draw
    dr.rectangle([0, b.p(FOOT_Y), b.W, b.H], fill=WHITE)
    foot(b)
    return b


def foot(b: Board) -> None:
    """Totem ayağı: QR + web + telefon + satıcı imzası."""
    dr = b.draw
    x0, x1 = b.p(TOTEM_PAD), b.p(TOTEM_W - TOTEM_PAD)

    qr_mm = 290
    q = qr_image(QR_TOTEM, b.p(qr_mm))
    qy = b.p(FOOT_Y + 105)
    b.im.alpha_composite(q, (x0, qy))
    f = b.sans(19, "600")
    track(b, b.draw, (x0, qy + b.p(qr_mm + 34)), "PROJEYİ GEZ", f, (*MIA_DARK, 235), b.p(3.4))

    tx = x0 + b.p(qr_mm + 78)
    dr = b.draw
    dr.text((tx, b.p(FOOT_Y + 96)), SITE, font=b.serif(72, "600"), fill=MIA_DEEP, anchor="la")
    fp = b.sans(50, "700")
    dr.text((tx, b.p(FOOT_Y + 218)), PHONES[0], font=fp, fill=INK, anchor="la")
    dr.text((tx, b.p(FOOT_Y + 288)), PHONES[1], font=fp, fill=INK, anchor="la")
    seller_block(b, dr, tx, b.p(FOOT_Y + 400), 26)


def totem_front() -> Image.Image:
    b = totem_shell()
    dr = b.draw
    cx = b.W / 2
    inner = b.p(TOTEM_W - TOTEM_PAD * 2)

    f, sp = fit_track(b, dr, ["TASARRUFA DAYALI FAİZSİZ FİNANSMAN"], inner, 26, 0.22, lambda s: b.sans(s, "600"))
    track(b, dr, (cx, b.p(1090)), "TASARRUFA DAYALI FAİZSİZ FİNANSMAN", f, (*MIA_LIGHT, 245), sp, "ma")

    # -- tek büyük vaat --
    lines = ["Lüks artık", "ulaşılabilir."]
    fs = fit(b, dr, lines, inner, 155, lambda s: b.serif(s, "600"))
    for i, ln in enumerate(lines):
        dr.text((cx, b.p(1400 + i * 215)), ln, font=fs, fill=WHITE, anchor="ms")

    dr.line([cx - b.p(110), b.p(1800), cx + b.p(110), b.p(1800)],
            fill=(*MIA_AQUA, 210), width=b.p(4))

    # -- iki sayı: kaç daire, kaç yaşam tipi --
    for i, (num, cap) in enumerate([(str(TOTAL_UNITS), "DAİRE"), (str(len(UNITS)), "YAŞAM TİPİ")]):
        col = b.W * (0.28 + 0.44 * i)
        dr.text((col, b.p(2380)), num, font=b.serif(200, "700"), fill=WHITE, anchor="ms")
        fc, spc = fit_track(b, dr, [cap], b.p(500), 27, 0.2, lambda s: b.sans(s, "600"))
        track(b, dr, (col, b.p(2445)), cap, fc, (*MIA_PALE, 245), spc, "ma")

    # -- ters bant: totemin kaidesi, beyaz künyeye dayanır --
    # Bandın altında koyu bir şerit bırakılırsa kaza gibi duruyor; ayakla
    # birleşince tabelanın altı tek bir aydınlık blok olarak okunuyor.
    dr.rectangle([0, b.p(2830), b.W, b.p(FOOT_Y)], fill=MIA_ICE)
    fb = fit(b, dr, ["60 AY VADE"], inner, 112, lambda s: b.serif(s, "700"))
    dr.text((cx, b.p(3010)), "60 AY VADE", font=fb, fill=MIA_DEEP, anchor="ms")
    fz, spz = fit_track(b, dr, ["%0 FAİZ · VADE FARKI YOK"], inner, 40, 0.16, lambda s: b.sans(s, "700"))
    track(b, dr, (cx, b.p(3060)), "%0 FAİZ · VADE FARKI YOK", fz, NAVY, spz, "ma")

    return b.im.convert("RGB")


def totem_back() -> Image.Image:
    b = totem_shell()
    dr = b.draw
    cx = b.W / 2
    x0, x1 = b.p(TOTEM_PAD), b.p(TOTEM_W - TOTEM_PAD)
    inner = x1 - x0

    def eyebrow(text: str, y: int) -> None:
        f, sp = fit_track(b, dr, [text], inner, 27, 0.24, lambda s: b.sans(s, "600"))
        track(b, dr, (cx, b.p(y)), text, f, (*MIA_LIGHT, 245), sp, "ma")

    # -- dört yaşam tipi --
    eyebrow("DÖRT YAŞAM TİPİ", 1055)
    names = [u[1] for u in UNITS]
    fn = fit(b, dr, names, inner - b.p(300), 62, lambda s: b.serif(s, "600"))
    for i, (_, name, area, count) in enumerate(UNITS):
        y = 1215 + i * 235
        dr.text((x0, b.p(y)), name, font=fn, fill=WHITE, anchor="ls")
        dr.text((x1, b.p(y)), area, font=b.sans(52, "700"), fill=MIA_PALE, anchor="rs")
        track(b, dr, (x0, b.p(y + 42)), f"{count} DAİRE", b.sans(26, "600"),
              (*MIA_AQUA, 240), b.p(5))
        dr.line([x0, b.p(y + 128), x1, b.p(y + 128)], fill=(*MIA_LIGHT, 90), width=b.p(2))

    # -- konum: noktalı kılavuzlu mesafe listesi --
    eyebrow("HER YERE DAKİKALAR İÇİNDE", 2320)
    fp = b.sans(46, "600")
    ft = b.sans(46, "700")
    for i, (place, time) in enumerate(DISTANCES[:6]):
        y = b.p(2470 + i * 128)
        dr.text((x0, y), place, font=fp, fill=(*MIA_ICE, 250), anchor="ls")
        dr.text((x1, y), time, font=ft, fill=WHITE, anchor="rs")
        lead_x0 = x0 + round(dr.textlength(place, font=fp)) + b.p(22)
        lead_x1 = x1 - round(dr.textlength(time, font=ft)) - b.p(22)
        dot = b.p(4)
        step = b.p(22)
        xx = lead_x0
        while xx < lead_x1:
            dr.ellipse([xx, y - b.p(14), xx + dot, y - b.p(14) + dot], fill=(*MIA_LIGHT, 150))
            xx += step

    return b.im.convert("RGB")


# ================================================================== AFİŞLER
# 3000 x 2400 mm modüller. Alt künye şeridi hepsinde aynı yükseklikte.
AF_W, AF_H, AF_DPI = 3000, 2400, 50
AF_PAD = 130
RAIL_Y = 2020                      # künye şeridinin üst kenarı
LOGO_W = 640                       # afişteki logo kilidi genişliği


def afis() -> Board:
    return Board(AF_W, AF_H, AF_DPI)


def rail(b: Board, on_light: bool = False) -> None:
    """Ortak alt künye şeridi — çit boyunca kesintisiz beyaz çizgi."""
    dr = b.draw
    y0 = b.p(RAIL_Y)
    dr.rectangle([0, y0, b.W, b.H], fill=WHITE)
    dr.rectangle([0, y0, b.W, y0 + b.p(7)], fill=MIA_DEEP)

    x = b.p(AF_PAD)
    dr.text((x, b.p(RAIL_Y + 118)), SITE, font=b.serif(88, "600"), fill=MIA_DEEP, anchor="ls")
    seller_block(b, dr, x, b.p(RAIL_Y + 175), 26)

    # telefonlar
    xp = b.p(1360)
    fp = b.sans(62, "700")
    dr.text((xp, b.p(RAIL_Y + 135)), PHONES[0], font=fp, fill=INK, anchor="ls")
    dr.text((xp, b.p(RAIL_Y + 232)), PHONES[1], font=fp, fill=INK, anchor="ls")
    dr.line([xp - b.p(70), b.p(RAIL_Y + 70), xp - b.p(70), b.p(RAIL_Y + 300)],
            fill=MIA_PALE, width=b.p(3))

    # QR + etiketi
    qr_mm = 240
    q = qr_image(QR_AFIS, b.p(qr_mm))
    qx = b.W - b.p(AF_PAD + qr_mm)
    b.im.alpha_composite(q, (qx, b.p(RAIL_Y + 68)))
    lx = qx - b.p(48)
    dr.text((lx, b.p(RAIL_Y + 168)), "Kat planları,", font=b.sans(40, "600"), fill=INK, anchor="rs")
    dr.text((lx, b.p(RAIL_Y + 238)), "fiyat ve randevu", font=b.sans(40, "600"), fill=INK, anchor="rs")
    track(b, dr, (lx, b.p(RAIL_Y + 268)), "KAREKODU OKUTUN", b.sans(26, "700"),
          MIA_DARK, b.p(4.5), "ra")


def brandmark(b: Board, white: bool = True, shadow: bool = True) -> None:
    """Afişin sol üst köşesi — hepsinde aynı yerde, aynı boyda."""
    lg = lockup(b.p(LOGO_W), white)
    pos = (b.p(AF_PAD), b.p(AF_PAD))
    if shadow:
        sh = Image.new("RGBA", b.im.size, (0, 0, 0, 0))
        sh.alpha_composite(lg, pos)
        sh = sh.filter(ImageFilter.GaussianBlur(b.p(9)))
        dark = Image.new("RGBA", b.im.size, (2, 22, 34, 0))
        dark.putalpha(sh.split()[3].point(lambda v: min(255, round(v * 1.7))))
        b.im.alpha_composite(dark)
    b.im.alpha_composite(lg, pos)


def photo_board(name: str, focus: float = 0.5, top: int = 120, bot: int = 150) -> Board:
    b = afis()
    b.im = cover(name, (b.W, b.H), focus)
    b.im.alpha_composite(scrim((b.W, b.H), [
        (0.0, (3, 32, 48, top)),
        (0.30, (3, 32, 48, 20)),
        (0.62, (3, 32, 48, 60)),
        (1.0, (3, 32, 48, bot)),
    ]))
    return b


# ── afiş 1 · kimlik ─────────────────────────────────────────────────────
def afis_kimlik() -> Image.Image:
    """Akşam görüntüsü: yazı gökyüzünde, aydınlık cepheler altında kalır.

    Gündüz render'ında projenin KENDİ giriş tabelası tam da başlığın
    oturduğu yere denk geliyordu; iki yazı üst üste binince ikisi de
    okunmuyordu. Akşam karesinde üst şerit boş gökyüzü — başlık oraya
    çıkınca giriş tabelası da görünür kalıyor, başlık da temiz.
    """
    b = afis()
    b.im = cover("night-gate", (b.W, b.H), 0.5)
    b.im.alpha_composite(scrim((b.W, b.H), [
        (0.00, (2, 20, 38, 236)),
        (0.26, (2, 20, 38, 150)),
        (0.42, (2, 20, 38, 30)),
        (0.70, (2, 20, 38, 24)),
        (1.00, (2, 20, 38, 200)),
    ]))
    brandmark(b, shadow=False)
    stats = f"{TOTAL_UNITS} DAİRE   ·   {len(UNITS)} YAŞAM TİPİ   ·   60 AY VADE   ·   %0 FAİZ"
    xr = b.p(AF_W - AF_PAD)

    def paint(dr):
        f, sp = fit_track(b, dr, ["İZMİT MİA BÖLGESİ'NDE YÜKSELİYOR"], b.p(1500), 34, 0.2,
                          lambda s: b.sans(s, "600"))
        track(b, dr, (xr, b.p(255)), "İZMİT MİA BÖLGESİ'NDE YÜKSELİYOR", f, (*MIA_ICE, 250), sp, "ra")
        lines = ["Lüks artık", "ulaşılabilir."]
        fs = fit(b, dr, lines, b.p(1750), 165, lambda s: b.serif(s, "600"))
        for i, ln in enumerate(lines):
            dr.text((xr, b.p(560 + i * 225)), ln, font=fs, fill=WHITE, anchor="rs")
        fc, spc = fit_track(b, dr, [stats], b.p(AF_W - AF_PAD * 2), 44, 0.14, lambda s: b.sans(s, "700"))
        track(b, dr, (b.W / 2, b.p(1830)), stats, fc, WHITE, spc, "ma")

    soft_text(b, paint, blur_mm=18, alpha=0.7)
    rail(b)
    return b.im.convert("RGB")


# ── afiş 2 · finansman ──────────────────────────────────────────────────
def afis_finansman() -> Image.Image:
    b = afis()
    b.im = gradient((b.W, b.H), DEEP_STOPS, angle=0.8)
    b.im.alpha_composite(glow((b.W, b.H), b.p(700), b.p(900), b.p(1500), MIA_CYAN, 0.32))
    b.im.alpha_composite(glow((b.W, b.H), b.p(2900), b.p(2100), b.p(1400), MIA_OCEAN, 0.22))
    brandmark(b, shadow=False)
    dr = b.draw
    cx = b.W / 2

    f, sp = fit_track(b, dr, ["TASARRUFA DAYALI FAİZSİZ FİNANSMAN SİSTEMİ"], b.p(2400), 40, 0.2,
                      lambda s: b.sans(s, "600"))
    track(b, dr, (cx, b.p(640)), "TASARRUFA DAYALI FAİZSİZ FİNANSMAN SİSTEMİ",
          f, (*MIA_LIGHT, 245), sp, "ma")

    # iki dev rakam
    for i, (num, cap) in enumerate([("%0", "FAİZ · VADE FARKI YOK"), ("60", "AY SABİT TAKSİT")]):
        col = b.W * (0.28 + 0.44 * i)
        dr.text((col, b.p(1210)), num, font=b.serif(400, "700"), fill=WHITE, anchor="ms")
        fc, spc = fit_track(b, dr, [cap], b.p(1150), 44, 0.16, lambda s: b.sans(s, "700"))
        track(b, dr, (col, b.p(1275)), cap, fc, (*MIA_PALE, 248), spc, "ma")

    dr.line([cx, b.p(960), cx, b.p(1260)], fill=(*MIA_LIGHT, 110), width=b.p(3))

    # üç hap
    chips = ["BANKASIZ", "FAİZSİZ", "KEFİLSİZ"]
    fch, spch = fit_track(b, dr, chips, b.p(560), 46, 0.16, lambda s: b.sans(s, "700"))
    cw, ch, gap = b.p(760), b.p(180), b.p(70)
    total = cw * 3 + gap * 2

    def chip_row(d):
        x = (b.W - total) / 2
        for c in chips:
            d.rounded_rectangle([x, b.p(1520), x + cw, b.p(1520) + ch], radius=ch // 2,
                                fill=(255, 255, 255, 26), outline=(*MIA_AQUA, 225), width=b.p(4))
            track(b, d, (x + cw / 2, b.p(1520) + ch * 0.30), c, fch, WHITE, spch, "ma")
            x += cw + gap

    overlay(b, chip_row)
    dr = b.draw

    fl = fit(b, dr, ["Peşinatın ardından 60 aya kadar sabit taksit. Ara ödeme yok."],
             b.p(2500), 52, lambda s: b.sans(s, "400"))
    dr.text((cx, b.p(1880)), "Peşinatın ardından 60 aya kadar sabit taksit. Ara ödeme yok.",
            font=fl, fill=(*MIA_ICE, 245), anchor="ms")

    rail(b)
    return b.im.convert("RGB")


# ── afiş 3 · daire tipleri ──────────────────────────────────────────────
# Her tipin KENDİ iç mekân görseli. Aynı kareyi iki tipte kullanmak
# afişi tek bakışta çürütür — dubleks ile loft aynı salonda oturamaz.
UNIT_SHOTS = [
    "ic-mekan/01-1plus0-salon",
    "ic-mekan/05-1plus1-salon",
    "ic-mekan/09-loft-salon",
    "ic-mekan/14-dubleks-bahcesi",
]


def afis_daireler() -> Image.Image:
    b = afis()
    b.im = gradient((b.W, b.H), LIGHT_STOPS, angle=0.35)
    brandmark(b, white=False, shadow=False)
    dr = b.draw

    dr.text((b.W - b.p(AF_PAD), b.p(300)), "Dört yaşam tipi",
            font=b.serif(130, "600"), fill=MIA_DEEP, anchor="rs")
    track(b, dr, (b.W - b.p(AF_PAD), b.p(345)),
          f"{TOTAL_UNITS} DAİRE · 28 m²'DEN 100 m²'YE", b.sans(34, "600"),
          MIA_DARK, b.p(6), "ra")

    n = len(UNITS)
    gap = b.p(60)
    cw = (b.p(AF_W - AF_PAD * 2) - gap * (n - 1)) // n
    # Kaynak render'lar 16:9. Kartı fazla dikey yaparsak kadrajın yarısı
    # kesiliyor ve odanın kendisi kalmıyor; kareye yakın oran hem kırpmayı
    # azaltıyor hem de dört kart yan yana daha dengeli duruyor.
    card_h = b.p(700)
    top = b.p(680)                       # logo kilidinin alt satırının altında
    fn = fit(b, dr, [u[1] for u in UNITS], cw, 62, lambda s: b.serif(s, "600"))
    for i, ((_, name, area, count), shot) in enumerate(zip(UNITS, UNIT_SHOTS)):
        x = b.p(AF_PAD) + i * (cw + gap)
        im = fit_box(shot, (cw, card_h), 0.5)
        mask = Image.new("L", (cw, card_h), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, cw - 1, card_h - 1], radius=b.p(28), fill=255)
        b.im.paste(im.convert("RGB"), (x, top), mask)

        y = top + card_h + b.p(130)
        dr.line([x, top + card_h + b.p(48), x + b.p(120), top + card_h + b.p(48)],
                fill=MIA_OCEAN, width=b.p(6))
        dr.text((x, y), name, font=fn, fill=MIA_DEEP, anchor="ls")
        dr.text((x, y + b.p(112)), area, font=b.sans(58, "700"), fill=INK, anchor="ls")
        track(b, dr, (x, y + b.p(158)), f"{count} DAİRE", b.sans(30, "600"), MIA_DARK, b.p(5))

    # units.ts'teki özellik listelerinden birebir: balkon 1+0/1+1'de,
    # özel bahçe ise Bahçe Loft ve Bahçe Dubleks'te var.
    note = "1+0 ve 1+1 dairelerde geniş balkon   ·   Bahçe Loft ve Bahçe Dubleks'te özel kullanım bahçesi"
    fnote = fit(b, dr, [note], b.p(AF_W - AF_PAD * 2), 46, lambda s: b.sans(s, "400"))
    dr.text((b.W / 2, b.p(1880)), note, font=fnote, fill=MIA_DEEP, anchor="ms")

    rail(b)
    return b.im.convert("RGB")


# ── afiş 4 · konum ──────────────────────────────────────────────────────
def afis_konum() -> Image.Image:
    b = afis()
    b.im = gradient((b.W, b.H), SURF_STOPS, angle=0.62)
    # arkada çok soluk, hafif bulanık bir hava fotoğrafı — düz zemin olmasın
    bg = cover("aerial-pools", (b.W, b.p(RAIL_Y)), 0.5, sharpen=False)
    bg = bg.filter(ImageFilter.GaussianBlur(b.p(28)))
    bg.putalpha(26)
    b.im.alpha_composite(bg, (0, 0))
    b.im.alpha_composite(glow((b.W, b.H), b.p(1500), b.p(1100), b.p(1700), MIA_DEEP, 0.42))
    brandmark(b, shadow=False)
    dr = b.draw

    dr.text((b.W - b.p(AF_PAD), b.p(300)), "Her yere dakikalar içinde",
            font=b.serif(122, "600"), fill=WHITE, anchor="rs")
    track(b, dr, (b.W - b.p(AF_PAD), b.p(345)), "İZMİT MİA BÖLGESİ", b.sans(34, "600"),
          (*MIA_ICE, 245), b.p(7), "ra")

    cols = 4
    gap = b.p(56)
    cw = (b.p(AF_W - AF_PAD * 2) - gap * (cols - 1)) // cols
    chh = b.p(480)
    top = b.p(640)
    fp, spp = fit_track(b, dr, [p.upper() for p, _ in DISTANCES], cw - b.p(70), 30, 0.14,
                        lambda s: b.sans(s, "600"))

    def cards(d):
        for i, (place, time) in enumerate(DISTANCES):
            r, c = divmod(i, cols)
            x = b.p(AF_PAD) + c * (cw + gap)
            y = top + r * (chh + gap)
            d.rounded_rectangle([x, y, x + cw, y + chh], radius=b.p(26),
                                fill=(255, 255, 255, 34), outline=(255, 255, 255, 105), width=b.p(3))
            d.text((x + cw / 2, y + b.p(245)), time, font=b.serif(130, "700"), fill=WHITE, anchor="ms")
            track(b, d, (x + cw / 2, y + b.p(305)), place.upper(), fp, (*MIA_ICE, 250), spp, "ma")

    overlay(b, cards)

    # Süreler location.ts'ten geliyor ve araçla yaklaşık değerler.
    dr = b.draw
    dr.text((b.W / 2, b.p(1870)), "Süreler araçla yaklaşık ulaşım süreleridir.",
            font=b.sans(40, "400"), fill=(*MIA_ICE, 225), anchor="ms")

    rail(b)
    return b.im.convert("RGB")


# ── afiş 5 · sosyal yaşam ───────────────────────────────────────────────
def afis_sosyal() -> Image.Image:
    b = photo_board("courtyard-pools", 0.55, top=170, bot=130)
    brandmark(b)
    dr = b.draw

    def paint(dr):
        f, sp = fit_track(b, dr, ["ORTAK YAŞAM ALANLARI"], b.p(1400), 34, 0.22,
                          lambda s: b.sans(s, "600"))
        track(b, dr, (b.p(AF_PAD), b.p(1000)), "ORTAK YAŞAM ALANLARI", f, (*MIA_ICE, 250), sp)
        lines = ["Avlu, havuzlar,", "yürüyüş yolları."]
        fs = fit(b, dr, lines, b.p(2000), 150, lambda s: b.serif(s, "600"))
        for i, ln in enumerate(lines):
            dr.text((b.p(AF_PAD), b.p(1230 + i * 200)), ln, font=fs, fill=WHITE, anchor="ls")

    soft_text(b, paint)

    # rozet dizisi — iki satır
    dr = b.draw
    fch, spch = fit_track(b, dr, AMENITIES, b.p(620), 32, 0.16, lambda s: b.sans(s, "700"))

    def chips(d):
        x, y = b.p(AF_PAD), b.p(1640)
        row_h = b.p(120)
        for a in AMENITIES:
            w = sum(dr.textlength(c, font=fch) for c in a) + spch * (len(a) - 1) + b.p(90)
            if x + w > b.p(AF_W - AF_PAD):
                x, y = b.p(AF_PAD), y + row_h
            d.rounded_rectangle([x, y, x + w, y + b.p(96)], radius=b.p(48),
                                fill=(4, 34, 52, 165), outline=(*MIA_PALE, 155), width=b.p(3))
            track(b, d, (x + w / 2, y + b.p(28)), a, fch, WHITE, spch, "ma")
            x += w + b.p(26)

    overlay(b, chips)

    rail(b)
    return b.im.convert("RGB")


# ---------------------------------------------------------------- üretim
BOARDS = [
    ("totem-on-yuz", totem_front, TOTEM_W, TOTEM_H, TOTEM_DPI, "Totem · ön yüz"),
    ("totem-arka-yuz", totem_back, TOTEM_W, TOTEM_H, TOTEM_DPI, "Totem · arka yüz"),
    ("afis-1-kimlik", afis_kimlik, AF_W, AF_H, AF_DPI, "Çevre afişi 1 · kimlik"),
    ("afis-2-finansman", afis_finansman, AF_W, AF_H, AF_DPI, "Çevre afişi 2 · finansman"),
    ("afis-3-daireler", afis_daireler, AF_W, AF_H, AF_DPI, "Çevre afişi 3 · daire tipleri"),
    ("afis-4-konum", afis_konum, AF_W, AF_H, AF_DPI, "Çevre afişi 4 · konum"),
    ("afis-5-sosyal-yasam", afis_sosyal, AF_W, AF_H, AF_DPI, "Çevre afişi 5 · sosyal yaşam"),
]


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(PREVIEW, exist_ok=True)
    previews = {}
    for name, fn, w_mm, h_mm, dpi, label in BOARDS + EXTRA:
        im = fn()
        path = os.path.join(OUT, f"{name}.jpg")
        im.save(path, "JPEG", quality=94, subsampling=0, optimize=True, dpi=(dpi, dpi))
        mb = os.path.getsize(path) / 1e6
        print(f"  {name:<22} {w_mm}x{h_mm} mm  {im.width}x{im.height} px  {dpi} dpi  {mb:.1f} MB")

        small = im.copy()
        small.thumbnail((1400, 1400), Image.LANCZOS)
        small.save(os.path.join(PREVIEW, f"{name}.jpg"), "JPEG", quality=88, optimize=True)
        previews[name] = small

    fence_run(previews)
    presentation(previews)
    print(f"\n  → {OUT}")


def fence_run(previews) -> None:
    """Beş afişi çit boyunca yan yana dizip künye şeridinin sürekliliğini gösterir."""
    keys = [k for k in previews if k.startswith("afis-")]
    tiles = [previews[k] for k in sorted(keys)]
    h = min(t.height for t in tiles)
    tiles = [t.resize((round(t.width * h / t.height), h), Image.LANCZOS) for t in tiles]
    gap = 10
    W = sum(t.width for t in tiles) + gap * (len(tiles) - 1)
    strip = Image.new("RGB", (W, h + 120), (238, 246, 249))
    x = 0
    for t in tiles:
        strip.paste(t, (x, 60))
        x += t.width + gap
    strip.thumbnail((3600, 3600), Image.LANCZOS)
    strip.save(os.path.join(PREVIEW, "cit-dizilimi.jpg"), "JPEG", quality=88, optimize=True)


# --------------------------------------------------------------- sunum pdf
# Baskı dosyaları tabelacıya gider; müşteriye/ekibe gösterilecek olan bu
# PDF. A4 yatay, her sayfada bir tabela ve gerçek ölçüsü.
A4 = (1754, 1240)          # 297 x 210 mm @ 150 dpi


def _page(title: str, sub: str) -> tuple:
    page = Image.new("RGB", A4, WHITE)
    dr = ImageDraw.Draw(page)
    f = lambda n, s: ImageFont.truetype(os.path.join(FONTS, n), s)
    dr.rectangle([0, 0, A4[0], 8], fill=MIA_DEEP)
    dr.text((70, 74), title, font=f("Fraunces-600.ttf", 46), fill=MIA_DEEP, anchor="ls")
    dr.text((A4[0] - 70, 74), sub, font=f("Manrope-600.ttf", 26), fill=INK, anchor="rs")
    return page, dr


def presentation(previews) -> None:
    pages = []

    cover = Image.new("RGB", A4, WHITE)
    lg = lockup(700)
    cover.paste(lg, ((A4[0] - lg.width) // 2, 210), lg)
    dr = ImageDraw.Draw(cover)
    dr.rectangle([0, 0, A4[0], 8], fill=MIA_DEEP)
    dr.text((A4[0] / 2, 830), "Saha Tabelaları",
            font=ImageFont.truetype(os.path.join(FONTS, "Fraunces-600.ttf"), 74),
            fill=MIA_DEEP, anchor="ms")
    dr.text((A4[0] / 2, 900), "1 totem (çift yüz)  ·  5 şantiye çevre afişi",
            font=ImageFont.truetype(os.path.join(FONTS, "Manrope-400.ttf"), 32),
            fill=INK, anchor="ms")
    dr.text((A4[0] / 2, 1150), SITE,
            font=ImageFont.truetype(os.path.join(FONTS, "Manrope-600.ttf"), 26),
            fill=MIA_DARK, anchor="ms")
    pages.append(cover)

    # Totem çift yüzlü: iki yüz aynı sayfada yan yana dursun. Dikey bir
    # tabelayı yatay sayfaya tek başına koyunca sayfanın dörtte üçü boş
    # kalıyor ve tabela olduğundan küçük görünüyor.
    page, dr = _page("Totem  ·  ön ve arka yüz",
                     f"{TOTEM_W} x {TOTEM_H} mm  ·  çift yüzlü  ·  1:1 @ {TOTEM_DPI} dpi")
    faces = [previews["totem-on-yuz"].copy(), previews["totem-arka-yuz"].copy()]
    fh = A4[1] - 300
    faces = [f.resize((round(f.width * fh / f.height), fh), Image.LANCZOS) for f in faces]
    gapx = 150
    total = sum(f.width for f in faces) + gapx
    x = (A4[0] - total) // 2
    fcap = ImageFont.truetype(os.path.join(FONTS, "Manrope-600.ttf"), 24)
    for f, cap in zip(faces, ["ÖN YÜZ", "ARKA YÜZ"]):
        page.paste(f, (x, 150))
        dr.text((x + f.width / 2, A4[1] - 78), cap, font=fcap, fill=MIA_DARK, anchor="ms")
        x += f.width + gapx
    pages.append(page)

    for name, _, w_mm, h_mm, dpi, label in BOARDS + EXTRA:
        if name.startswith("totem-"):
            continue
        page, _ = _page(label, f"{w_mm} x {h_mm} mm  ·  1:1 @ {dpi} dpi")
        im = previews[name].copy()
        box = (A4[0] - 140, A4[1] - 260)
        im.thumbnail(box, Image.LANCZOS)
        page.paste(im, ((A4[0] - im.width) // 2, 120 + (box[1] - im.height) // 2))
        pages.append(page)

    strip = Image.open(os.path.join(PREVIEW, "cit-dizilimi.jpg"))
    page, _ = _page("Çit dizilimi", "beş afiş yan yana  ·  15 m cephe")
    strip.thumbnail((A4[0] - 140, A4[1] - 400), Image.LANCZOS)
    page.paste(strip, ((A4[0] - strip.width) // 2, (A4[1] - strip.height) // 2))
    pages.append(page)

    pages[0].save(os.path.join(OUT, "MIA-PARK-OCEAN-TABELA-SUNUMU.pdf"),
                  save_all=True, append_images=pages[1:], resolution=150)




# ================================================================== ROLLUP
# 800 x 2000 mm, 1:1 @ 100 dpi. Yakından okunur (1-3 m), bu yüzden afişten
# yüksek çözünürlük.
#
# ALT KASET PAYI
# ──────────────
# Roll-up'ın alt ~130 mm'si kasetin içinde kalır ve görünmez. Kritik hiçbir
# şey oraya konmuyor; künye şeridi beyaz olduğu için kasete giren kısım da
# beyaz devam ediyor, kesildiği belli olmuyor.
RU_W, RU_H, RU_DPI = 800, 2000, 100
RU_PAD = 62
RU_RAIL = 1560            # beyaz künye şeridinin üst kenarı
RU_SAFE_BOT = 1860        # bunun altı kasete girer


def rollup() -> Board:
    return Board(RU_W, RU_H, RU_DPI)


def info_rail(b: Board, y0: float, pad: float, qr_mm: float, qr_url: str,
              u: float = 1.0, wide: bool = False) -> None:
    """
    Ortak künye şeridi: web, Instagram, telefonlar, karekod, satıcı imzası.

    Bütün ölçüler `u` ile çarpılır — aynı düzen roll-up'ta 1x, bilbordda
    2.2x olarak kuruluyor. Böylece iki üründe künye aynı kompozisyonda
    duruyor, sadece büyüklüğü değişiyor.
    """
    dr = b.draw
    # Düz beyaz blok baskıda ölü bir alan bırakıyordu; beyazdan buz mavisine
    # çok hafif bir geçiş şeridi canlandırıyor, yazının kontrastı bozulmuyor.
    h = b.H - b.p(y0)
    g = gradient((b.W, h), [(0.0, WHITE), (0.55, (247, 252, 254)), (1.0, MIA_ICE)], angle=0.25)
    b.im.alpha_composite(g, (0, b.p(y0)))
    dr = b.draw
    dr.rectangle([0, b.p(y0), b.W, b.p(y0 + 2.4 * u)], fill=MIA_DEEP)

    x = b.p(pad)
    q = qr_image(qr_url, b.p(qr_mm))
    qx = b.W - b.p(pad + qr_mm)
    qy = b.p(y0 + 26 * u)
    b.im.alpha_composite(q, (qx, qy))
    track(b, dr, (qx + b.p(qr_mm) / 2, qy + b.p(qr_mm) + b.p(11 * u)),
          "PROJEYİ GEZ", b.sans(9 * u, "700"), MIA_DARK, b.p(1.6 * u), "ma")

    if wide:
        # Bilbord 5 metre geniş: her şeyi sola yığmak şeridin ortasını
        # bomboş bırakıyordu. Bloklar yatayda dağıtılıyor, punto büyüyor.
        dr.text((x, b.p(y0 + 128 * u)), SITE, font=b.serif(40 * u, "600"),
                fill=MIA_DEEP, anchor="ls")
        track(b, dr, (x, b.p(y0 + 148 * u)), "INSTAGRAM   @MIAPARKOCEAN",
              b.sans(12 * u, "700"), MIA_DARK, b.p(2.6 * u))
        xp = round(b.W * 0.40)
        fp = b.sans(26 * u, "700")
        dr.text((xp, b.p(y0 + 100 * u)), PHONES[0], font=fp, fill=INK, anchor="ls")
        dr.text((xp, b.p(y0 + 148 * u)), PHONES[1], font=fp, fill=INK, anchor="ls")
        dr.line([xp - b.p(26 * u), b.p(y0 + 46 * u), xp - b.p(26 * u), b.p(y0 + 168 * u)],
                fill=MIA_PALE, width=b.p(1.4 * u))
        seller_block(b, dr, round(b.W * 0.655), b.p(y0 + 108 * u), 13 * u)
        return

    dr.text((x, b.p(y0 + 72 * u)), SITE, font=b.serif(30 * u, "600"),
            fill=MIA_DEEP, anchor="ls")
    track(b, dr, (x, b.p(y0 + 84 * u)), "INSTAGRAM   @MIAPARKOCEAN",
          b.sans(9.5 * u, "700"), MIA_DARK, b.p(2 * u))

    fp = b.sans(19 * u, "700")
    dr.text((x, b.p(y0 + 130 * u)), PHONES[0], font=fp, fill=INK, anchor="ls")
    dr.text((x, b.p(y0 + 158 * u)), PHONES[1], font=fp, fill=INK, anchor="ls")
    seller_block(b, dr, x, b.p(y0 + 172 * u), 8 * u)


def ru_rail(b: Board) -> None:
    info_rail(b, RU_RAIL, RU_PAD, 132, QR_ROLLUP, 1.0)


def ru_brand(b: Board, white: bool = True, shadow: bool = True) -> None:
    lg = lockup(b.p(430), white)
    pos = (b.p(RU_PAD), b.p(58))
    if shadow:
        sh = Image.new("RGBA", b.im.size, (0, 0, 0, 0))
        sh.alpha_composite(lg, pos)
        sh = sh.filter(ImageFilter.GaussianBlur(b.p(8)))
        dark = Image.new("RGBA", b.im.size, (2, 22, 34, 0))
        dark.putalpha(sh.split()[3].point(lambda v: min(255, round(v * 1.7))))
        b.im.alpha_composite(dark)
    b.im.alpha_composite(lg, pos)


def veil(b: Board, y_from: float, y_to: float, color=(4, 34, 52), a0: int = 0,
         a1: int = 245) -> None:
    """
    Görselden marka rengine GRADYANLI GEÇİŞ.

    Fotoğrafı sert bir çizgiyle kesip altına renk koymak roll-up'ta ucuz
    duruyordu; perde yumuşak inince görsel markaya karışıyor ve yazı
    boşlukta değil, kendi zemininde oturuyor.
    """
    h = b.p(y_to) - b.p(y_from)
    arr = np.zeros((max(h, 2), 1, 4), np.float32)
    ys = np.linspace(0, 1, max(h, 2))
    arr[:, 0, 3] = (a0 + (a1 - a0) * ys ** 1.25)
    arr[:, :, 0], arr[:, :, 1], arr[:, :, 2] = color
    im = Image.fromarray(arr.astype(np.uint8), "RGBA").resize((b.W, max(h, 2)), Image.BILINEAR)
    b.im.alpha_composite(im, (0, b.p(y_from)))
    d = b.draw
    d.rectangle([0, b.p(y_to), b.W, b.p(RU_RAIL)], fill=(*color, 255))


def ru_photo(b: Board, name: str, focus: float = 0.5, fade_from: float = 620,
             fade_to: float = 1080) -> None:
    """Üstte fotoğraf, ortada gradyanla markaya geçiş, altta düz zemin."""
    b.im = cover(name, (b.W, b.p(RU_RAIL)), focus)
    full = Image.new("RGBA", (b.W, b.H), (255, 255, 255, 255))
    full.alpha_composite(b.im, (0, 0))
    b.im = full
    b.im.alpha_composite(scrim((b.W, b.p(fade_from)), [
        (0.0, (2, 22, 40, 150)), (0.45, (2, 22, 40, 20)), (1.0, (2, 22, 40, 40)),
    ]), (0, 0))
    veil(b, fade_from, fade_to)


def ru_title(b: Board, eyebrow: str, lines, y: float, size: float = 66,
             lh: float = 88, sub: str = "") -> None:
    """
    Başlık bloğu — logodan güvenli uzaklıkta, satırlar birbirine girmez.

    Önceki kurguda alt başlık logonun alt satırıyla çakışıyordu; blok artık
    kendi y'sinden başlıyor ve satır yüksekliği punto ile birlikte artıyor.
    """
    dr = b.draw
    inner = b.p(RU_W - RU_PAD * 2)
    fs = fit(b, dr, lines, inner, size, lambda s: b.serif(s, "600"))
    fsub = fit(b, dr, [sub], inner, 22, lambda s: b.sans(s, "400")) if sub else None
    fe = sp = None
    if eyebrow:
        fe, sp = fit_track(b, dr, [eyebrow], inner, 17, 0.22, lambda s: b.sans(s, "700"))

    # Başlığın ilk satırının tepesi; alt başlık bunun ÜSTÜNE yerleşir.
    asc = fs.getmetrics()[0]
    top = b.p(y + 74) - asc

    def paint(d):
        if fe:
            # Gradyanın orta tonunda buz mavisi siliniyordu; alt başlık beyaz.
            track(b, d, (b.p(RU_PAD), top - b.p(16) - fe.getmetrics()[1]), eyebrow,
                  fe, WHITE, sp)
        for i, ln in enumerate(lines):
            d.text((b.p(RU_PAD), b.p(y + 74 + i * lh)), ln, font=fs, fill=WHITE, anchor="ls")
        if fsub:
            yy = y + 74 + len(lines) * lh + 30
            for k, sl in enumerate(wrap(dr, sub, fsub, inner)):
                d.text((b.p(RU_PAD), b.p(yy + k * 32)), sl, font=fsub,
                       fill=(*MIA_ICE, 245), anchor="ls")

    # Perde yerine yazı gölgesi: gradyanın açık yerinde alt başlık siliniyordu.
    soft_text(b, paint, blur_mm=7, alpha=0.62)


# ── roll-up 1 · kimlik ─────────────────────────────────────────────────
def rollup_kimlik() -> Image.Image:
    b = rollup()
    ru_photo(b, "night-gate", 0.5, 560, 1010)
    ru_brand(b, white=True, shadow=False)
    ru_title(b, "İZMİT MİA BÖLGESİ'NDE YÜKSELİYOR",
             ["Lüks artık", "ulaşılabilir."], 1060, size=92, lh=118,
             sub="600 daire · dört yaşam tipi · dört blok, sekiz kat")
    ru_rail(b)
    return b.im.convert("RGB")


# ── roll-up 2 · finansman ──────────────────────────────────────────────
def rollup_finansman() -> Image.Image:
    """Kalabalık yok: dört kısa cümle ve iki rakam."""
    b = rollup()
    ru_photo(b, "courtyard-pools", 0.5, 520, 940)
    ru_brand(b, white=True, shadow=False)
    dr = b.draw
    inner = b.p(RU_W - RU_PAD * 2)

    f, sp = fit_track(b, dr, ["TASARRUFA DAYALI FAİZSİZ FİNANSMAN"], inner, 14, 0.2,
                      lambda s: b.sans(s, "600"))
    track(b, dr, (b.p(RU_PAD), b.p(1010)), "TASARRUFA DAYALI FAİZSİZ FİNANSMAN",
          f, (*MIA_ICE, 250), sp)

    lines = ["Banka yok.", "Kredi yok.", "Kefil yok.", "Faiz yok."]
    fs = fit(b, dr, lines, inner, 78, lambda s: b.serif(s, "600"))
    for i, ln in enumerate(lines):
        dr.text((b.p(RU_PAD), b.p(1130 + i * 98)), ln, font=fs, fill=WHITE, anchor="ls")

    # ters bant: gözün takıldığı tek yer
    dr.rectangle([0, b.p(1540), b.W, b.p(RU_RAIL)], fill=MIA_ICE)
    fb = fit(b, dr, ["60 AY VADE"], inner, 74, lambda s: b.serif(s, "700"))
    dr.text((b.W / 2, b.p(1630)), "60 AY VADE", font=fb, fill=MIA_DEEP, anchor="ms")
    fz, spz = fit_track(b, dr, ["%0 FAİZ · VADE FARKI YOK"], inner, 26, 0.16,
                        lambda s: b.sans(s, "700"))
    track(b, dr, (b.W / 2, b.p(1665)), "%0 FAİZ · VADE FARKI YOK", fz, NAVY, spz, "ma")
    ru_rail(b)
    return b.im.convert("RGB")


# ── roll-up 3 · daire tipleri ──────────────────────────────────────────
UNIT_SHOTS_RU = ["ic-mekan/01-1plus0-salon", "ic-mekan/05-1plus1-salon",
                 "ic-mekan/09-loft-salon", "ic-mekan/14-dubleks-bahcesi"]


def rollup_daireler() -> Image.Image:
    """
    Dört tip, dört şerit — aralarında gradyanlı geçiş.

    Kareler sert çizgilerle bölünürse katalog sayfası gibi duruyor; her
    şeridin üstü bir öncekine eriyince tek bir dikey akış oluyor.
    """
    b = rollup()
    b.im = gradient((b.W, b.H), DEEP_STOPS, angle=0.7)
    top, band = 380, 290
    for i, shot in enumerate(UNIT_SHOTS_RU):
        y = top + i * band
        im = cover(shot, (b.W, b.p(band)), 0.5)
        # üst kenarı eriyerek gelsin
        m = np.zeros((b.p(band), 1), np.float32)
        m[:, 0] = np.clip(np.linspace(0, 1, b.p(band)) * 4.0, 0, 1)
        mask = Image.fromarray((m * 255).astype(np.uint8), "L").resize((b.W, b.p(band)))
        b.im.paste(im.convert("RGB"), (0, b.p(y)), mask)
    b.im.alpha_composite(scrim((b.W, b.p(RU_RAIL)), [
        (0.0, (2, 22, 40, 120)), (0.18, (2, 22, 40, 30)),
        (0.55, (2, 22, 40, 90)), (1.0, (2, 22, 40, 210)),
    ]), (0, 0))
    ru_brand(b, white=True, shadow=False)

    dr = b.draw
    names = [u[1] for u in UNITS]
    fn = fit(b, dr, names, b.p(RU_W - RU_PAD * 2 - 190), 36, lambda s: b.serif(s, "600"))

    def paint(d):
        for i, (_, name, area, count) in enumerate(UNITS):
            y = top + i * band + band - 54
            d.text((b.p(RU_PAD), b.p(y)), name, font=fn, fill=WHITE, anchor="ls")
            d.text((b.p(RU_W - RU_PAD), b.p(y)), area, font=b.sans(30, "700"),
                   fill=WHITE, anchor="rs")
            track(b, d, (b.p(RU_PAD), b.p(y + 16)), f"{count} DAİRE",
                  b.sans(13, "600"), (*MIA_PALE, 245), b.p(2.4))

    soft_text(b, paint, blur_mm=8, alpha=0.8)
    ru_rail(b)
    return b.im.convert("RGB")


# ── roll-up 4 · yaşam ──────────────────────────────────────────────────
def rollup_yasam() -> Image.Image:
    b = rollup()
    ru_photo(b, "ic-mekan/18-yuruyus-yolu", 0.5, 620, 1080)
    ru_brand(b, white=True, shadow=False)
    ru_title(b, "ORTAK YAŞAM ALANLARI",
             ["Bahçesi olan", "ev değil,", "parkı olan ev."], 1120, size=68, lh=92,
             sub="Yürüyüş yolları · süs havuzları · çocuk oyun parkı · kapalı yüzme havuzu · fitness · sauna ve Türk hamamı")
    ru_rail(b)
    return b.im.convert("RGB")


# ── roll-up 5 · balkondan körfez ───────────────────────────────────────
def rollup_deniz() -> Image.Image:
    b = rollup()
    ru_photo(b, "balkondan-deniz", 0.5, 600, 1050)
    ru_brand(b, white=True, shadow=False)
    ru_title(b, "SAHİLE YÜRÜME MESAFESİ",
             ["İster havuzu", "izleyin,", "ister denizi."], 1090, size=76, lh=100,
             sub="Geniş balkon · merkezi avlu · süs havuzları")
    ru_rail(b)
    return b.im.convert("RGB")


# ── roll-up 6 · gece ───────────────────────────────────────────────────
def rollup_gece() -> Image.Image:
    b = rollup()
    ru_photo(b, "ic-mekan/05-1plus1-salon", 0.5, 600, 1050)
    ru_brand(b, white=True, shadow=False)
    ru_title(b, "YÜKSEK KALİTELİ İÇ MEKÂN",
             ["Ev burada", "başlıyor."], 1090, size=92, lh=118,
             sub="Açık plan yaşam alanı · modern mutfak · geniş cam yüzeyler")
    ru_rail(b)
    return b.im.convert("RGB")



# ================================================================ BİLBORD
# 5000 x 3000 mm yatay, 1:1 @ 40 dpi. Uzaktan ve çoğu zaman HAREKET
# HALİNDE okunur: her tasarımda tek bir cümle, tek bir rakam. Künye şeridi
# roll-up'takinin 2.2 katı ölçekte, aynı kompozisyonda.
BB_W, BB_H, BB_DPI = 5000, 3000, 40
BB_PAD = 180
BB_RAIL = 2480
BB_U = 2.2


def bilbord() -> Board:
    return Board(BB_W, BB_H, BB_DPI)


def bb_qr_plate(b: Board, x: int, y: int, size_mm: float) -> None:
    """Karekod beyaz plaket içinde — görselin üstüne doğrudan basılanı
    telefon kamerası zeminden ayıramıyor."""
    pad = b.p(size_mm * 0.10)
    d = b.draw
    d.rounded_rectangle([x - pad, y - pad, x + b.p(size_mm) + pad, y + b.p(size_mm) + pad],
                        radius=b.p(size_mm * 0.09), fill=WHITE)
    b.im.alpha_composite(qr_image(QR_BILBORD, b.p(size_mm)), (x, y))


def bb_info(b: Board) -> None:
    """Tam boy baskıda künye: BEYAZ yazı, doğrudan görselin üstünde.

    Beyaz şerit yok — bilbord şehrin görünür noktalarına asılıyor, alttan
    yarım metreyi beyaza vermek görselin en iyi kısmını kesiyordu.
    """
    x = b.p(BB_PAD)

    def paint(d):
        d.text((x, b.p(2700)), SITE, font=b.serif(112, "600"), fill=WHITE, anchor="ls")
        track(b, d, (x, b.p(2745)), "INSTAGRAM   @MIAPARKOCEAN",
              b.sans(34, "700"), (*MIA_ICE, 250), b.p(7))
        xp = round(b.W * 0.40)
        fp = b.sans(68, "700")
        d.text((xp, b.p(2660)), PHONES[0], font=fp, fill=WHITE, anchor="ls")
        d.text((xp, b.p(2775)), PHONES[1], font=fp, fill=WHITE, anchor="ls")
        d.line([xp - b.p(70), b.p(2560), xp - b.p(70), b.p(2800)],
               fill=(*MIA_PALE, 170), width=b.p(4))
        track(b, d, (round(b.W * 0.655), b.p(2680)), SELLER,
              b.sans(46, "700"), WHITE, b.p(8))
        track(b, d, (round(b.W * 0.655), b.p(2748)), SELLER_ROLE,
              b.sans(28, "600"), (*MIA_ICE, 240), b.p(6))

    soft_text(b, paint, blur_mm=20, alpha=0.78)
    qs = 300
    bb_qr_plate(b, b.W - b.p(BB_PAD + qs), b.p(2480), qs)
    track(b, b.draw, (b.W - b.p(BB_PAD + qs / 2), b.p(2830)), "PROJEYİ GEZ",
          b.sans(30, "700"), WHITE, b.p(6), "ma")


def bb_full(b: Board, name: str, focus: float = 0.5, side: float = 0.5,
            top: int = 165, bot: int = 210) -> None:
    """
    Görsel TAM BOY. `side` yatay kırpma noktası (0 sol, 1 sağ).

    İkili sette iki pano yan yana asıldığı için tek bir geniş kareyi ikiye
    bölmek gerekebiliyor: sol panoya karenin solu, sağ panoya sağı.
    """
    im = grade(load(name))
    w, h = b.W, b.H
    sc = max(w / im.width, h / im.height)
    im = im.resize((max(w, round(im.width * sc)), max(h, round(im.height * sc))), Image.LANCZOS)
    if sc > 1.3:
        im = im.filter(ImageFilter.UnsharpMask(radius=max(2, round(sc)), percent=58, threshold=3))
    x = round((im.width - w) * min(max(side, 0.0), 1.0))
    y = round((im.height - h) * focus)
    b.im = im.crop((x, y, x + w, y + h)).convert("RGBA")
    b.im.alpha_composite(scrim((w, h), [
        (0.00, (2, 22, 40, top)), (0.26, (2, 22, 40, 45)),
        (0.58, (2, 22, 40, 50)), (0.80, (2, 22, 40, 155)),
        (1.00, (2, 22, 40, bot)),
    ]))


def bb_brand(b: Board, right: bool = False) -> None:
    """Logo — sol panoda sola, sağ panoda sağa. İkisi de logo taşır."""
    lg = lockup(b.p(1000), white=True)
    x = b.W - b.p(BB_PAD) - lg.width if right else b.p(BB_PAD)
    b.im.alpha_composite(lg, (x, b.p(150)))


def bb_line(b: Board, eyebrow: str, lines, y0: float = 1250, lh: float = 320,
            size: float = 250) -> None:
    """İkili sette cümlenin yarısı — kendi panosunda ORTALANIR.

    İki pano arasında çerçeve boşluğu var; yazıyı dikişe yaslamak yerine
    her yarıyı kendi panosuna ortalamak iki tarafta da dengeli duruyor.
    """
    cx = b.W / 2
    inner = b.p(BB_W - BB_PAD * 2)

    def paint(dr):
        fs = fit(b, dr, lines, inner, size, lambda s: b.serif(s, "600"))
        if eyebrow:
            f, sp = fit_track(b, dr, [eyebrow], inner, 48, 0.2, lambda s: b.sans(s, "600"))
            # Alt başlığı orana göre değil, BAŞLIĞIN GERÇEK TEPESİNE göre
            # koy: punto küçülünce sabit oran yetmiyor ve ikisi giriyordu.
            asc = fs.getmetrics()[0]
            _, fdesc = f.getmetrics()
            track(b, dr, (cx, b.p(y0) - asc - b.p(30) - fdesc), eyebrow,
                  f, (*MIA_ICE, 250), sp, "ma")
        for i, ln in enumerate(lines):
            dr.text((cx, b.p(y0 + i * lh)), ln, font=fs, fill=WHITE, anchor="ms")

    soft_text(b, paint, blur_mm=28, alpha=0.84)


def bb_panel(img: str, focus: float, side: float, eyebrow: str, lines,
             right: bool, size: float = 250) -> Image.Image:
    b = bilbord()
    bb_full(b, img, focus, side)
    bb_brand(b, right=right)
    bb_line(b, eyebrow, lines, size=size)
    bb_info(b)
    return b.im.convert("RGB")


# ── ikili setler ───────────────────────────────────────────────────────
# Her set YAN YANA iki panoya asılır. Cümle ikiye bölünür, logo ve iletişim
# İKİSİNDE DE bulunur; sol pano logoyu sola, sağ pano sağa alır — ikisi
# birlikte simetrik bir çift olur.
#
# Bazı setlerde iki farklı kare (gündüz/gece gibi karşıtlıklar), bazılarında
# TEK geniş karenin sol ve sağ yarısı kullanılır; ikincisinde iki pano tek
# bir görüntünün devamı gibi okunur.
#
#   slug, (sol görsel, sol odak, sol yatay kırpma), (sağ ...),
#   üst başlık, sol cümle, sağ cümle
PAIRS = [
    ("01-gunduz-gece",
     ("aerial-pools", 0.5, 0.5), ("night-gate", 0.5, 0.5),
     ("İZMİT MİA BÖLGESİ", "ÖZEL GECE AYDINLATMASI"),
     ["Gündüz", "başka,"], ["gece", "başka."], 260),

    ("02-disarisi-icerisi",
     ("entrance-gate", 0.48, 0.5), ("ic-mekan/05-1plus1-salon", 0.5, 0.5),
     ("MİMARİ VE PEYZAJ", "YÜKSEK KALİTELİ İÇ MEKÂN"),
     ["Dışarısı", "ne kadar iyiyse,"], ["içerisi", "de o kadar."], 190),

    ("03-havuz-deniz",
     ("courtyard-pools", 0.55, 0.35), ("balkondan-deniz", 0.5, 0.62),
     ("MERKEZİ AVLU", "SAHİLE YÜRÜME MESAFESİ"),
     ["İster havuzu", "izleyin,"], ["ister", "denizi."], 220),

    ("04-banka-faiz",
     ("night-gate", 0.5, 0.28), ("night-gate", 0.5, 0.72),
     ("TASARRUFA DAYALI FİNANSMAN", "60 AY VADE"),
     ["Banka yok,", "kefil yok."], ["Kredi yok,", "faiz yok."], 230),

    ("05-balkon-bahce",
     ("balcony-dusk", 0.5, 0.5), ("ic-mekan/13-bahceli-daire-terasi", 0.5, 0.5),
     ("1+0 VE 1+1 DAİRELERDE", "BAHÇE LOFT VE BAHÇE DUBLEKS'TE"),
     ["Kimine", "balkon,"], ["kimine", "bahçe."], 260),

    ("06-rakamlar",
     ("aerial-pools", 0.5, 0.32), ("aerial-pools", 0.5, 0.68),
     ("10 DÖNÜM ARAZİ", "DÖRT BLOK · SEKİZ KAT"),
     ["600", "daire,"], ["dört", "yaşam tipi."], 270),

    ("07-yurumek-oynamak",
     ("ic-mekan/18-yuruyus-yolu", 0.5, 0.5), ("ic-mekan/19-cocuk-oyun-parki", 0.5, 0.5),
     ("GENİŞ PEYZAJ", "GÜVENLİ OYUN ALANI"),
     ["Yürüyüş yolu", "kapınızın önünde,"], ["oyun parkı", "gözünüzün önünde."], 165),

    ("08-sehir-deniz",
     ("street-corner", 0.5, 0.5), ("balkondan-deniz", 0.42, 0.5),
     ("İZMİT MİA BÖLGESİ", "SAHİLE İKİ DAKİKA"),
     ["Şehrin", "içinde,"], ["denizin", "yanında."], 260),

    ("09-ilk-ev-aile",
     ("ic-mekan/01-1plus0-salon", 0.5, 0.72), ("ic-mekan/12-dubleks-yatak-odasi", 0.5, 0.5),
     ("1+0 · BRÜT 28 m²", "2+1 BAHÇE DUBLEKS · BRÜT 100 m²"),
     ["İlk eviniz", "de burada,"], ["büyüyen", "aileniz de."], 205),

    ("10-kimlik",
     ("night-gate", 0.5, 0.22), ("night-gate", 0.5, 0.78),
     ("İZMİT MİA BÖLGESİ'NDE YÜKSELİYOR", "600 DAİRE · DÖRT YAŞAM TİPİ"),
     ["Lüks", "artık"], ["ulaşılabilir."], 280),
]


def _pair_fn(spec, right: bool):
    slug, L, R, eyes, lw, rw, size = spec
    img, focus, side = R if right else L
    return lambda: bb_panel(img, focus, side, eyes[1] if right else eyes[0],
                            rw if right else lw, right, size)



# ============================================================== YAKA KARTI
# 90 x 130 mm dikey, 300 dpi. Lansman günü (21 Ağustos 2026, Emex Otel)
# takılacak kartlar.
#
# ASKI DELİĞİ
# ───────────
# Kordon deliği üstten ~10 mm'ye açılır. O bant boş bırakılıyor; logo ya da
# yazı oraya girerse zımba deliği tam ortasından geçiyor.
YK_W, YK_H, YK_DPI = 90, 130, 300
YK_PAD = 8
YK_SLOT = 14              # üstten bu kadarı asma deliğine ayrıldı

# Soyadı BÜYÜK harf: yaka kartında isimle soyadı bir bakışta ayrılıyor,
# uzaktan da soyadı okunuyor.
BADGE_FIRST = "Engin"
BADGE_LAST = "KOÇAK"
BADGE_NAME = f"{BADGE_FIRST} {BADGE_LAST}"
BADGE_ROLE = "İşletme Brokerı"
EVENT_LINE = "21 AĞUSTOS 2026 · EMEX OTEL"


def badge() -> Board:
    return Board(YK_W, YK_H, YK_DPI)


def yk_slot(b: Board, dark: bool = False) -> None:
    """Kordon deliğinin yerini gösteren ince kılavuz — kesimci nereye
    zımbalayacağını görsün."""
    dr = b.draw
    w, h = b.p(16), b.p(3.5)
    x = (b.W - w) // 2
    y = b.p(6)
    dr.rounded_rectangle([x, y, x + w, y + h], radius=h // 2,
                         outline=(255, 255, 255, 90) if dark else (*MIA_PALE, 200),
                         width=max(1, b.p(0.4)))


def yk_qr(b: Board, x: int, y: int, size_mm: float = 18, dark=INK) -> None:
    b.im.alpha_composite(qr_image(QR_YAKA, b.p(size_mm), dark), (x, y))


def yk_body(b: Board, on_dark: bool, name_y: float = 78) -> None:
    """
    Ortak gövde: isim, unvan, satıcı, karekod, etkinlik satırı.

    Karekod SAĞ ALTTA, yazı sütunu solda ve dar tutuluyor. İlk kurguda
    22 mm'lik karekod "OCEAN GAYRİMENKUL" ve etkinlik satırının üstüne
    biniyordu; 90 mm genişlikte ikisi ancak yan yana sığıyor.
    """
    dr = b.draw
    ink = WHITE if on_dark else MIA_DEEP
    soft = (*MIA_PALE, 245) if on_dark else (*MIA_DARK, 255)
    x = b.p(YK_PAD + 5)
    qr_mm = 18
    qx = b.W - b.p(YK_PAD + 5 + qr_mm)
    text_w = qx - x - b.p(4)              # karekoda çarpmadan kalan genişlik

    fn = fit(b, dr, [BADGE_NAME], b.p(YK_W - YK_PAD * 2 - 10), 11,
             lambda s: b.serif(s, "600"))
    dr.text((x, b.p(name_y)), BADGE_NAME, font=fn, fill=ink, anchor="ls")
    frole, sprole = fit_track(b, dr, [BADGE_ROLE.upper()], text_w, 3.1, 0.16,
                              lambda s: b.sans(s, "600"), floor_mm=1.2)
    track(b, dr, (x, b.p(name_y + 4)), BADGE_ROLE.upper(), frole, soft, sprole)
    dr.line([x, b.p(name_y + 12), x + b.p(17), b.p(name_y + 12)],
            fill=(*MIA_AQUA, 220) if on_dark else (*MIA_OCEAN, 220), width=b.p(0.9))

    fs, sps = fit_track(b, dr, [SELLER], text_w, 3.6, 0.18,
                        lambda s: b.sans(s, "700"), floor_mm=1.2)
    track(b, dr, (x, b.p(name_y + 20)), SELLER, fs, ink, sps)

    yk_qr(b, qx, b.p(YK_H - YK_PAD - 4 - qr_mm), qr_mm)

    fe, spe = fit_track(b, dr, ["21 AĞUSTOS 2026", "EMEX OTEL · KOCAELİ", SITE.upper()],
                        text_w, 3.0, 0.16, lambda s: b.sans(s, "700"), floor_mm=1.2)
    track(b, dr, (x, b.p(YK_H - YK_PAD - 18)), "21 AĞUSTOS 2026", fe, soft, spe)
    track(b, dr, (x, b.p(YK_H - YK_PAD - 12)), "EMEX OTEL · KOCAELİ", fe, soft, spe)
    track(b, dr, (x, b.p(YK_H - YK_PAD - 5)), SITE.upper(), fe,
          (*MIA_LIGHT, 255) if on_dark else (*MIA_OCEAN, 255), spe)


# ── yaka 1 · beyaz zemin, mavi baş bandı ───────────────────────────────
def yaka_1() -> Image.Image:
    b = badge()
    # Düz beyaz gövde cansız duruyordu; beyazdan buza çok hafif bir geçiş.
    b.im = gradient((b.W, b.H), [(0.0, WHITE), (0.5, (247, 252, 254)), (1.0, MIA_PALE)],
                    angle=0.3)
    b.im.alpha_composite(gradient((b.W, b.p(58)), DEEP_STOPS, angle=0.7), (0, 0))
    lg = lockup(b.p(52), white=True)
    b.im.alpha_composite(lg, ((b.W - lg.width) // 2, b.p(YK_SLOT + 5)))
    yk_slot(b, dark=True)
    yk_body(b, on_dark=False)
    return b.im.convert("RGB")


# ── yaka 2 · tam mavi ──────────────────────────────────────────────────
def yaka_2() -> Image.Image:
    b = badge()
    b.im = gradient((b.W, b.H), DEEP_STOPS, angle=0.72)
    b.im.alpha_composite(glow((b.W, b.H), b.p(45), b.p(40), b.p(70), MIA_CYAN, 0.30))
    lg = lockup(b.p(50), white=True)
    b.im.alpha_composite(lg, ((b.W - lg.width) // 2, b.p(YK_SLOT + 6)))
    yk_slot(b, dark=True)
    # Karekod koyu zeminde okunmaz; beyaz plakete alınıyor.
    dr = b.draw
    qs = b.p(18)
    qx = b.W - b.p(YK_PAD + 5 + 18)
    qy = b.p(YK_H - YK_PAD - 4 - 18)
    dr.rounded_rectangle([qx - b.p(2), qy - b.p(2), qx + qs + b.p(2), qy + qs + b.p(2)],
                         radius=b.p(2), fill=WHITE)
    yk_body(b, on_dark=True)
    return b.im.convert("RGB")


# ── yaka 3 · buz mavisi, çerçeveli ─────────────────────────────────────
def yaka_3() -> Image.Image:
    b = badge()
    b.im = gradient((b.W, b.H), LIGHT_STOPS, angle=0.3)
    dr = b.draw
    dr.rounded_rectangle([b.p(4), b.p(4), b.W - b.p(4), b.H - b.p(4)],
                         radius=b.p(4), outline=(*MIA_OCEAN, 150), width=b.p(0.7))
    lg = lockup(b.p(50), white=False)
    b.im.alpha_composite(lg, ((b.W - lg.width) // 2, b.p(YK_SLOT + 6)))
    yk_slot(b)
    yk_body(b, on_dark=False)
    return b.im.convert("RGB")


# ── yaka 4 · üstte proje karesi ────────────────────────────────────────
def yaka_4() -> Image.Image:
    b = badge()
    b.im = gradient((b.W, b.H), [(0.0, WHITE), (0.5, (247, 252, 254)), (1.0, MIA_PALE)],
                    angle=0.3)
    head = b.p(58)
    b.im.alpha_composite(cover("night-gate", (b.W, head), 0.5), (0, 0))
    b.im.alpha_composite(scrim((b.W, head), [
        (0.0, (2, 20, 38, 205)), (0.5, (2, 20, 38, 150)), (1.0, (2, 20, 38, 210)),
    ]), (0, 0))
    lg = lockup(b.p(50), white=True)
    b.im.alpha_composite(lg, ((b.W - lg.width) // 2, b.p(YK_SLOT + 5)))
    yk_slot(b, dark=True)
    yk_body(b, on_dark=False)
    return b.im.convert("RGB")


def yk_photo(b: Board, name: str, light: bool = True, focus: float = 0.5,
             fade_from: float = 50, fade_to: float = 68, veil_top: int = 70) -> None:
    """
    Kartın tamamına projenin kendi karesi — üstte açık, altta GEÇİŞLİ.

    Düz perde kartı dümdüz beyaz bırakıyordu: fotoğraf hem seçilmiyor hem
    de kart cansız duruyordu. Kare üst yarıda neredeyse tam güçte kalıyor,
    aşağı indikçe zemine eriyor; isim ve karekod eridiği yerde, tam
    kontrastlı bir alanda oturuyor. Roll-up'ta kurduğumuz geçişin kart
    ölçeğindeki karşılığı.
    """
    base = (255, 255, 255) if light else (4, 32, 50)
    b.im = cover(name, (b.W, b.H), focus)

    # üstte ince perde: logo her karede okunsun
    b.im.alpha_composite(scrim((b.W, b.p(fade_from)), [
        (0.0, (2, 22, 40, veil_top + 60)), (0.55, (2, 22, 40, veil_top)),
        (1.0, (2, 22, 40, veil_top - 20)),
    ]), (0, 0))

    # geçiş bandı + altında düz zemin
    h = b.p(fade_to) - b.p(fade_from)
    arr = np.zeros((max(h, 2), 1, 4), np.float32)
    ys = np.linspace(0, 1, max(h, 2))
    arr[:, 0, 3] = 255 * ys ** 1.15
    arr[:, :, 0], arr[:, :, 1], arr[:, :, 2] = base
    b.im.alpha_composite(
        Image.fromarray(arr.astype(np.uint8), "RGBA").resize((b.W, max(h, 2)), Image.BILINEAR),
        (0, b.p(fade_from)))
    b.draw.rectangle([0, b.p(fade_to), b.W, b.H], fill=(*base, 255))


def yk_qr_plate(b: Board) -> None:
    """Koyu kartta karekod beyaz plakete alınır."""
    dr = b.draw
    qs, qx = b.p(18), b.W - b.p(YK_PAD + 5 + 18)
    qy = b.p(YK_H - YK_PAD - 4 - 18)
    dr.rounded_rectangle([qx - b.p(2), qy - b.p(2), qx + qs + b.p(2), qy + qs + b.p(2)],
                         radius=b.p(2), fill=WHITE)


def yk_logo(b: Board, white: bool = True, w: float = 46) -> None:
    """Logo geçiş bandının üstünde kalmalı; aşağı inerse beyaza karışıyor."""
    lg = lockup(b.p(w), white=white)
    b.im.alpha_composite(lg, ((b.W - lg.width) // 2, b.p(YK_SLOT - 2)))


# ── yaka 5 · yürüyüş yolu ──────────────────────────────────────────────
def yaka_5() -> Image.Image:
    b = badge()
    yk_photo(b, "ic-mekan/18-yuruyus-yolu", light=True, veil_top=60)
    yk_logo(b); yk_slot(b, dark=True); yk_body(b, on_dark=False)
    return b.im.convert("RGB")


# ── yaka 6 · dış cephe, koyu ───────────────────────────────────────────
def yaka_6() -> Image.Image:
    b = badge()
    yk_photo(b, "night-gate", light=False, veil_top=42)
    yk_logo(b); yk_slot(b, dark=True); yk_qr_plate(b); yk_body(b, on_dark=True)
    return b.im.convert("RGB")


# ── yaka 7 · balkondan körfez ──────────────────────────────────────────
def yaka_7() -> Image.Image:
    b = badge()
    yk_photo(b, "balkondan-deniz", light=True, veil_top=58)
    dr = b.draw
    dr.rounded_rectangle([b.p(4), b.p(4), b.W - b.p(4), b.H - b.p(4)],
                         radius=b.p(4), outline=(*MIA_OCEAN, 130), width=b.p(0.7))
    yk_logo(b); yk_slot(b, dark=True); yk_body(b, on_dark=False)
    return b.im.convert("RGB")


# ── yaka 8 · avlu, koyu ────────────────────────────────────────────────
def yaka_8() -> Image.Image:
    b = badge()
    yk_photo(b, "courtyard-pools", light=False, focus=0.55, veil_top=46)
    yk_logo(b); yk_slot(b, dark=True); yk_qr_plate(b); yk_body(b, on_dark=True)
    return b.im.convert("RGB")



def yk_band(b: Board, name: str, light: bool = True, band: float = 50.6,
            soft: float = 15, veil: int = 55) -> None:
    """
    Projenin ÖNDEN TAM görünümü — kırpılmadan, kart boyu bant olarak.

    Bant yüksekliği 16:9 render'ın 90 mm genişlikteki birebir karşılığı
    (50,6 mm). Daha uzun bir bant kareyi yanlardan kırpar, proje "tam"
    görünmez; bu yüzden yükseklik ölçüden değil, kaynağın en-boyundan
    çıkıyor.

    Bandın altı SERT KESİLMİYOR: fotoğrafın kendi alt kenarı saydama
    eriyip zemindeki gradyanı açığa çıkarıyor. Önceki kurguda bandın
    altına düz bir renk sürülüyordu; o rengin bittiği yerde gradyanla
    arasında görünür bir dikiş kalıyordu.
    """
    stops = ([(0.0, WHITE), (0.5, (247, 252, 254)), (1.0, MIA_PALE)] if light
             else DEEP_STOPS)
    b.im = gradient((b.W, b.H), stops, angle=0.3)

    bh = b.p(band)
    im = cover(name, (b.W, bh), 0.5)
    im.alpha_composite(scrim((b.W, bh), [
        (0.0, (2, 22, 40, veil + 45)), (0.5, (2, 22, 40, veil)),
        (1.0, (2, 22, 40, veil - 15)),
    ]))

    # Erime yalnız fotoğrafın alt şeridinde: bina siluetleri bandın üst
    # üçte ikisinde, erimenin girdiği yer yol ve peyzaj.
    sh = min(b.p(soft), bh - 2)
    ramp = np.ones(bh, np.float32)
    ramp[bh - sh:] = np.linspace(1.0, 0.0, sh) ** 1.5
    a = np.asarray(im.split()[3], np.float32) * ramp[:, None]
    im.putalpha(Image.fromarray(a.astype(np.uint8), "L"))
    b.im.alpha_composite(im, (0, 0))


# ── yaka 9 · önden gündüz ──────────────────────────────────────────────
def yaka_9() -> Image.Image:
    b = badge()
    yk_band(b, "entrance-gate", light=True, veil=50)
    yk_logo(b, white=True, w=44)
    yk_slot(b, dark=True)
    yk_body(b, on_dark=False, name_y=72)
    return b.im.convert("RGB")


# ── yaka 10 · önden gece ───────────────────────────────────────────────
def yaka_10() -> Image.Image:
    b = badge()
    yk_band(b, "night-gate", light=False, veil=42)
    yk_logo(b, white=True, w=44)
    yk_slot(b, dark=True)
    yk_qr_plate(b)
    yk_body(b, on_dark=True, name_y=72)
    return b.im.convert("RGB")


ROLLUPS = [
    ("rollup-1-kimlik", rollup_kimlik, "Roll-up 1 · kimlik"),
    ("rollup-2-finansman", rollup_finansman, "Roll-up 2 · finansman"),
    ("rollup-3-daireler", rollup_daireler, "Roll-up 3 · daire tipleri"),
    ("rollup-4-yasam", rollup_yasam, "Roll-up 4 · ortak yaşam"),
    ("rollup-5-deniz", rollup_deniz, "Roll-up 5 · balkondan körfez"),
    ("rollup-6-ic-mekan", rollup_gece, "Roll-up 6 · iç mekân"),
]
BILBORDS = []
for _sp in PAIRS:
    _slug = _sp[0]
    BILBORDS.append((f"bilbord-{_slug}-SOL", _pair_fn(_sp, False), f"Bilbord {_slug} · sol pano"))
    BILBORDS.append((f"bilbord-{_slug}-SAG", _pair_fn(_sp, True), f"Bilbord {_slug} · sağ pano"))
BADGES = [
    ("yaka-1-beyaz", yaka_1, "Yaka kartı 1 · beyaz"),
    ("yaka-2-mavi", yaka_2, "Yaka kartı 2 · mavi"),
    ("yaka-3-buz", yaka_3, "Yaka kartı 3 · buz mavisi"),
    ("yaka-4-fotografli", yaka_4, "Yaka kartı 4 · fotoğraflı başlık"),
    ("yaka-5-yuruyus", yaka_5, "Yaka kartı 5 · yürüyüş yolu"),
    ("yaka-6-cephe", yaka_6, "Yaka kartı 6 · dış cephe"),
    ("yaka-7-deniz", yaka_7, "Yaka kartı 7 · balkondan körfez"),
    ("yaka-8-avlu", yaka_8, "Yaka kartı 8 · avlu"),
    ("yaka-9-on-gunduz", yaka_9, "Yaka kartı 9 · önden gündüz"),
    ("yaka-10-on-gece", yaka_10, "Yaka kartı 10 · önden gece"),
]

# Totem/afiş dışındaki ürünler. Aynı Board motoru, aynı künye şeridi.
EXTRA = (
    [(n, f, RU_W, RU_H, RU_DPI, t) for n, f, t in ROLLUPS] +
    [(n, f, BB_W, BB_H, BB_DPI, t) for n, f, t in BILBORDS] +
    [(n, f, YK_W, YK_H, YK_DPI, t) for n, f, t in BADGES]
)



# =========================================================== KATMANLI KAYNAK
# `--katman` ile her tasarım İKİ dosyaya ayrılır:
#
#     <ad>-zemin.jpg   fotoğraf, gradyan, logo, karekod — yazı YOK
#     <ad>-yazi.png    yalnızca tipografi, saydam zeminde
#
# İkisi üst üste konunca birebir onaylanan tasarım çıkar. Matbaa ya da
# tasarımcı yazı katmanını silip yenisini yazabilir; zemine dokunmaz.
#
# NASIL AYRIŞTIRILIYOR
# ────────────────────
# Tasarım iki kez üretiliyor: bir kez normal, bir kez bütün yazılar
# bastırılarak. İkisinin farkından yazı katmanı ÇÖZÜLÜYOR — tahmin değil,
# birebir tersine çözüm:
#
#     tam = zemin * (1 - a) + c * a          (alfa harmanlama)
#     c   = zemin + (tam - zemin) / a
#
# a, c'nin 0-255 dışına taşmayacağı en küçük değer seçilerek bulunuyor.
#
# Böylece yumuşak gölgeler ve yarı saydam kenarlar da doğru çıkıyor;
# katman zeminin üstüne konduğunda piksel piksel aynı sonucu veriyor.
SRC_OUT = os.path.join(OUT, "kaynak")

_NO_TEXT = False
_orig_text = ImageDraw.ImageDraw.text


def _patched_text(self, xy, text, *a, **k):
    if _NO_TEXT:
        return None
    return _orig_text(self, xy, text, *a, **k)


ImageDraw.ImageDraw.text = _patched_text


def _split(full: Image.Image, bg: Image.Image, rows: int = 900):
    """Yazı katmanını çözer. Şeritler halinde: bilbordda tam boy float32
    dizi bir gigabaytı geçiyor."""
    w, h = full.size
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for y0 in range(0, h, rows):
        y1 = min(y0 + rows, h)
        f = np.asarray(full.crop((0, y0, w, y1)), np.float32)
        b = np.asarray(bg.crop((0, y0, w, y1)), np.float32)
        # Alfa, rengin 0-255 dışına taşmayacağı EN KÜÇÜK değer seçilir.
        # Sadece kanal farkını alfa saymak, farkın küçük olduğu yerde
        # rengi uçuruyor ve kırpılınca katman zemine tam oturmuyordu.
        up = np.where(f > b, (f - b) / np.maximum(255.0 - b, 1.0), 0.0)
        dn = np.where(f < b, (b - f) / np.maximum(b, 1.0), 0.0)
        a = np.clip(np.maximum(up, dn).max(axis=2), 0.0, 1.0)
        safe = np.maximum(a, 1.0 / 255.0)[:, :, None]
        c = np.clip(b + (f - b) / safe, 0, 255)

        # Alfası sıfır olan yerde renk zaten hiçbir şeye karışmıyor ama
        # (f-b)/safe orada JPEG gürültüsünü 255 katına çıkarıp rastgele
        # renk üretiyordu. Rastgele renk PNG'de sıkışmıyor: bilbordun
        # yazı katmanı 38 MB'a çıkmıştı. Görünmeyen yeri siyaha çekmek
        # sonucu değiştirmiyor, dosyayı onda birine indiriyor.
        a8 = np.round(a * 255.0)
        c = np.where(a8[:, :, None] > 0, c, 0.0)
        strip = np.dstack([c, a8]).astype(np.uint8)
        out.paste(Image.fromarray(strip, "RGBA"), (0, y0))
    return out


def build_layers() -> None:
    global _NO_TEXT
    os.makedirs(SRC_OUT, exist_ok=True)
    for name, fn, w_mm, h_mm, dpi, label in BOARDS + EXTRA:
        _NO_TEXT = False
        full = fn().convert("RGB")
        _NO_TEXT = True
        bg = fn().convert("RGB")
        _NO_TEXT = False

        bp = os.path.join(SRC_OUT, f"{name}-zemin.jpg")
        bg.save(bp, "JPEG", quality=94, subsampling=0, optimize=True, dpi=(dpi, dpi))

        # Matbaa yazıyı SIKIŞTIRILMIŞ zeminin üstüne koyacak; çözüm de
        # onun üstünden yapılmalı. Bellekteki zemine göre çözülünce
        # JPEG'in kendi kaybı hesaba girmiyor, iki dosya üst üste
        # konunca harf kenarlarında fark kalıyordu.
        bg = Image.open(bp).convert("RGB")

        # Hedef, onaylanan dosyanın kendisi — yeniden render değil.
        ap = os.path.join(OUT, f"{name}.jpg")
        if os.path.exists(ap):
            full = Image.open(ap).convert("RGB")

        tp = os.path.join(SRC_OUT, f"{name}-yazi.png")
        _split(full, bg).save(tp, optimize=True)
        print(f"  {name:<34} zemin {os.path.getsize(bp)/1e6:5.1f} MB · "
              f"yazı {os.path.getsize(tp)/1e6:5.1f} MB")

    # matbaanın ihtiyacı olan yazı tipleri
    fd = os.path.join(SRC_OUT, "yazi-tipleri")
    os.makedirs(fd, exist_ok=True)
    for f in os.listdir(FONTS):
        if f.endswith((".ttf", ".otf")):
            shutil.copy2(os.path.join(FONTS, f), os.path.join(fd, f))
    print(f"\n  → {SRC_OUT}")

if __name__ == "__main__":
    if "--katman" in sys.argv:
        build_layers()
    else:
        main()
