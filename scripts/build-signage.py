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
    "ic-mekan/11-dubleks-salon",
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
    for name, fn, w_mm, h_mm, dpi, label in BOARDS:
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

    for name, _, w_mm, h_mm, dpi, label in BOARDS:
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


if __name__ == "__main__":
    main()
