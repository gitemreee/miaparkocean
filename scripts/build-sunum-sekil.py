#!/usr/bin/env python3
"""
MİA PARK OCEAN — lansman sunumu şekil motoru.

PowerPoint (pptxgenjs) bezier eğri çizemez ve fotoğrafı organik bir şeklin
içine maskeleyemez. Sunumun görsel dili tam olarak buna dayandığı için
bütün organik parçalar burada, PIL + numpy ile üretilip şeffaf PNG olarak
`sunum/kaynak/sekil/` altına yazılır; build-sunum.js sadece yerleştirir.

Maskeler analitik: her piksel için sınıra olan işaretli uzaklık hesaplanıp
1 piksellik yumuşak geçişe çevriliyor. Süper örnekleme gerekmiyor, kenarlar
pürüzsüz çıkıyor.

    python3 scripts/build-sunum-sekil.py
"""

import os
import math
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "public", "images")
OUT = os.path.join(ROOT, "sunum", "kaynak", "sekil")
os.makedirs(OUT, exist_ok=True)

# slayt 13.333 x 7.5 inç — 150 dpi
W, H = 2000, 1125
ASPECT = W / H

# ---------------------------------------------------------------- palet
INK = (4, 40, 58)        # #04283A  en koyu lacivert
DEEP = (7, 88, 120)      # #075878
OCEAN = (26, 116, 150)   # #1A7496
AZURE = (23, 137, 199)   # #1789C7  parlak mavi (referanstaki canlı ton)
CYAN = (72, 171, 197)    # #48ABC5
ICE = (221, 247, 250)    # #DDF7FA
PAPER = (245, 250, 252)  # #F5FAFC
WHITE = (255, 255, 255)
CORAL = (242, 112, 75)   # #F2704B


def _grid(w, h):
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    return x, y


def _aa(d):
    """İşaretli uzaklık -> 0..1 kapsama. Sınırda 1 piksel yumuşama."""
    return np.clip(0.5 - d, 0.0, 1.0)


# ------------------------------------------------------------ eğri sınır
def wave_x(t, base, amp, k=1.0, phase=0.0, skew=0.0):
    """
    Dikey dalga sınırının x konumu (0..1 normalize).
    t     : 0 üst, 1 alt
    base  : sınırın orta ekseni (0..1)
    amp   : salınım genliği
    k     : kaç periyot
    phase : faz kayması (periyot cinsinden)
    skew  : yukarıdan aşağıya doğrusal kayma (S hissi verir)
    """
    return base + amp * np.cos(2 * math.pi * (k * t + phase)) + skew * (t - 0.5)


def wave_mask(w, h, base, amp, k=1.0, phase=0.0, skew=0.0, side="right"):
    """Dalga sınırının bir tarafını dolduran 0..1 maske."""
    x, y = _grid(w, h)
    t = y / (h - 1)
    xb = wave_x(t, base, amp, k, phase, skew) * (w - 1)
    d = (xb - x) if side == "right" else (x - xb)
    return _aa(d)


def wave_mask_h(w, h, base, amp, k=1.0, phase=0.0, skew=0.0, side="bottom"):
    """Yatay dalga sınırı — üst/alt bantlar için."""
    x, y = _grid(w, h)
    t = x / (w - 1)
    yb = wave_x(t, base, amp, k, phase, skew) * (h - 1)
    d = (yb - y) if side == "bottom" else (y - yb)
    return _aa(d)


def disc_mask(w, h, cx, cy, r, inner=None):
    """Daire / halka maskesi. cx,cy,r piksel."""
    x, y = _grid(w, h)
    d = np.hypot(x - cx, y - cy)
    m = _aa(d - r)
    if inner is not None:
        m = np.clip(m - _aa(d - inner), 0, 1)
    return m


def round_rect_mask(w, h, x0, y0, x1, y1, r, corners=(1, 1, 1, 1)):
    """
    Köşe yarıçapları seçilebilen dikdörtgen maskesi.
    corners = (sol-üst, sağ-üst, sağ-alt, sol-alt); 1 yuvarlak, 0 keskin.
    Kemer kart (üst iki köşe yuvarlak) bununla çıkıyor.
    """
    x, y = _grid(w, h)
    dx = np.maximum(x0 - x, x - x1)
    dy = np.maximum(y0 - y, y - y1)
    d = np.maximum(dx, dy)                      # keskin dikdörtgen
    for (cx, cy, on) in ((x0 + r, y0 + r, corners[0]), (x1 - r, y0 + r, corners[1]),
                         (x1 - r, y1 - r, corners[2]), (x0 + r, y1 - r, corners[3])):
        if not on:
            continue
        inq = (np.abs(x - cx) > 0) & (np.abs(y - cy) > 0)
        q = ((x < cx) if cx == x0 + r else (x > cx)) & ((y < cy) if cy == y0 + r else (y > cy))
        q &= inq
        dd = np.hypot(x - cx, y - cy) - r
        d = np.where(q, dd, d)
    return _aa(d)


# --------------------------------------------------------------- tuval
class Canvas:
    def __init__(self, w=W, h=H, bg=None):
        self.w, self.h = w, h
        self.a = np.zeros((h, w, 4), np.float32)
        if bg is not None:
            self.fill_all(bg)

    def fill_all(self, col, alpha=1.0):
        self.a[..., :3] = np.array(col, np.float32)
        self.a[..., 3] = alpha

    def paint(self, mask, col, alpha=1.0):
        """Maskeyi verilen renkle 'over' modunda basar."""
        m = (mask * alpha)[..., None]
        c = np.array(col, np.float32)
        self.a[..., :3] = self.a[..., :3] * (1 - m) + c * m
        self.a[..., 3:4] = self.a[..., 3:4] * (1 - m) + m

    def paint_img(self, mask, img):
        """RGB dizisini maskeyle basar (fotoğrafı eğrinin içine maskeler)."""
        m = mask[..., None]
        self.a[..., :3] = self.a[..., :3] * (1 - m) + img * m
        self.a[..., 3:4] = self.a[..., 3:4] * (1 - m) + m

    def save(self, name):
        arr = np.clip(self.a, 0, 1 if self.a.max() <= 1.001 else 255)
        rgb = np.clip(self.a[..., :3], 0, 255).astype(np.uint8)
        al = np.clip(self.a[..., 3] * 255, 0, 255).astype(np.uint8)
        out = np.dstack([rgb, al])
        p = os.path.join(OUT, name + ".png")
        Image.fromarray(out, "RGBA").save(p, optimize=True)
        return p


# ------------------------------------------------------------- fotoğraf
_cache = {}


def photo(name, w, h, focus=0.5, gamma=1.0, zoom=1.0):
    """
    Kaynak görseli w x h kutusuna EN-BOY ORANINI KORUYARAK kırpar (cover).
    focus: yatay/dikey kırpma merkezi (0 sol/üst, 1 sağ/alt).
    zoom : 1'den büyükse önce büyütür, sonra focus'a göre pencere keser.
           Kaynakla kutu aynı oranda olduğunda focus tek başına hiçbir şey
           yapmaz (kırpılacak pay yoktur); kadrajı ancak zoom oynatır.
    """
    key = (name, w, h, focus, gamma, zoom)
    if key in _cache:
        return _cache[key]
    p = os.path.join(SRC, name)
    im = Image.open(p).convert("RGB")
    iw, ih = im.size
    s = max(w / iw, h / ih) * max(1.0, zoom)
    nw, nh = max(w, int(round(iw * s))), max(h, int(round(ih * s)))
    im = im.resize((nw, nh), Image.LANCZOS)
    ox = int((nw - w) * focus)
    oy = int((nh - h) * focus)
    im = im.crop((ox, oy, ox + w, oy + h))
    a = np.asarray(im, np.float32)
    if gamma != 1.0:
        a = 255.0 * (a / 255.0) ** gamma
    _cache[key] = a
    return a


def tint(img, col, k):
    """Fotoğrafı marka rengine doğru k kadar çeker (bütünlük için)."""
    c = np.array(col, np.float32)
    return img * (1 - k) + c * k


# ============================================================== ŞEKİLLER
def kapak(name, pic, focus=0.5, eksen=0.60):
    """
    Kapak: sağdan giren büyük organik blok. Katmanlı şeritler, en içte
    fotoğraf. Sol taraf başlığa kalır — genlik bilerek küçük tutuldu,
    yoksa güvenli açık alan 3 inçe düşüyor (ölçüldü, sunum-alan.py).
    """
    A, K, SK = 0.050, 1.0, 0.040
    c = Canvas()
    c.fill_all(PAPER)
    for b, col in [(eksen - 0.150, ICE), (eksen - 0.042, INK),
                   (eksen - 0.016, AZURE), (eksen - 0.003, WHITE)]:
        c.paint(wave_mask(W, H, b, A, k=K, phase=0.10, skew=SK), col)
    m = wave_mask(W, H, eksen + 0.020, A, k=K, phase=0.10, skew=SK)
    c.paint_img(m, photo(pic, W, H, focus))
    c.paint(m, INK, alpha=0.16)
    # köşe halkaları — sol ÜST logoya ayrıldığı için sol ALTA
    c.paint(disc_mask(W, H, -70, H + 60, 360, 292), AZURE, alpha=0.26)
    c.paint(disc_mask(W, H, -70, H + 60, 232, 178), CYAN, alpha=0.22)
    return c.save(name)


def yan_blok(name, pic, side="right", focus=0.5, koyu=False, eksen=0.66, zoom=1.0):
    """
    İçerik slaytları: bir yandan giren organik fotoğraf bloğu + şeritler.
    eksen : fotoğraf sınırının ekseni, slaydın SOLUNDAN 0..1 oranla.
            Büyütmek fotoğrafı küçültür, yazıya yer açar.
    side  : fotoğraf hangi tarafta ("right" için eksen doğrudan,
            "left" için aynası alınır)
    koyu  : slaydın zemini lacivert olsun
    """
    A, K, SK = 0.045, 0.85, 0.035
    c = Canvas()
    c.fill_all(INK if koyu else PAPER)
    kat = [(-0.085, DEEP if koyu else ICE), (-0.042, INK),
           (-0.016, AZURE), (-0.003, WHITE)]
    if side == "left":
        sd, e = "left", 1.0 - eksen
        seq = [(e - d, col) for d, col in kat]
        pb = e - 0.020
    else:
        sd, e = "right", eksen
        seq = [(e + d, col) for d, col in kat]
        pb = e + 0.020
    for b, col in seq:
        c.paint(wave_mask(W, H, b, A, k=K, phase=0.18, skew=-SK, side=sd), col)
    m = wave_mask(W, H, pb, A, k=K, phase=0.18, skew=-SK, side=sd)
    c.paint_img(m, photo(pic, W, H, focus, zoom=zoom))
    c.paint(m, INK, alpha=0.14)
    return c.save(name)


def koyu_panel(name, pic, focus=0.5, kenar=0.66):
    """
    Referanstaki 'Proposed Solution' düzeni: solda lacivert panel, sınırı
    dalgalı; sağda fotoğraf. Koyu zeminde beyaz yazı, sağda görsel.
    kenar: lacivert panelin bittiği eksen (0..1)
    """
    c = Canvas()
    c.fill_all(PAPER)
    full = np.ones((H, W), np.float32)
    c.paint_img(full, photo(pic, W, H, focus))
    c.paint(full, INK, alpha=0.30)
    # panel: solu kaplayan lacivert, sağ sınırı dalgalı
    pm = wave_mask(W, H, kenar, 0.055, k=0.8, phase=0.30, skew=-0.05, side="left")
    c.paint(pm, INK, alpha=0.97)
    # sınıra oturan iki şerit
    e1 = np.clip(pm - wave_mask(W, H, kenar - 0.012, 0.055, k=0.8, phase=0.30,
                                skew=-0.05, side="left"), 0, 1)
    c.paint(e1, AZURE)
    e2 = np.clip(wave_mask(W, H, kenar + 0.026, 0.055, k=0.8, phase=0.30, skew=-0.05, side="left")
                 - wave_mask(W, H, kenar + 0.008, 0.055, k=0.8, phase=0.30,
                             skew=-0.05, side="left"), 0, 1)
    c.paint(e2, CYAN, alpha=0.7)
    c.paint(disc_mask(W, H, -60, H + 70, 330, 262), AZURE, alpha=0.22)
    return c.save(name)


def ust_bant(name, pic=None, yuk=0.34, focus=0.5):
    """Üstte dalgalı kenarlı lacivert bant; altı beyaz kalır."""
    c = Canvas()
    c.fill_all(PAPER)
    band = wave_mask_h(W, H, yuk, 0.022, k=1.1, phase=0.2, side="above")
    if pic:
        # fotoğraf bandın TAMAMINI doldurur; koyulaştırma yazı için
        ph = photo(pic, W, int(H * (yuk + 0.10)), focus)
        img = np.zeros((H, W, 3), np.float32)
        img[:ph.shape[0]] = ph
        img[ph.shape[0]:] = ph[-1]
        c.paint_img(band, tint(img, INK, 0.34))
        c.paint(band, INK, alpha=0.68)
    else:
        c.paint(band, INK)
    # dalgalı alt kenara oturan iki ince şerit
    edge = band - wave_mask_h(W, H, yuk - 0.016, 0.022, k=1.1, phase=0.2, side="above")
    c.paint(np.clip(edge, 0, 1), AZURE)
    edge2 = (wave_mask_h(W, H, yuk + 0.026, 0.022, k=1.1, phase=0.2, side="above")
             - wave_mask_h(W, H, yuk + 0.006, 0.022, k=1.1, phase=0.2, side="above"))
    c.paint(np.clip(edge2, 0, 1), CYAN, alpha=0.55)
    c.paint(disc_mask(W, H, W + 40, H + 40, 330, 262), ICE)
    return c.save(name)


def alt_bant(name, yuk=0.72):
    """Altta dalgalı kenarlı lacivert bant."""
    c = Canvas()
    c.fill_all(PAPER)
    c.paint(wave_mask_h(W, H, yuk, 0.024, k=1.0, phase=0.55, side="bottom"), ICE)
    c.paint(wave_mask_h(W, H, yuk + 0.030, 0.024, k=1.0, phase=0.55, side="bottom"), AZURE)
    c.paint(wave_mask_h(W, H, yuk + 0.048, 0.024, k=1.0, phase=0.55, side="bottom"), INK)
    c.paint(disc_mask(W, H, -50, 120, 260, 205), AZURE, alpha=0.22)
    return c.save(name)


def sade(name, kose="sag-ust"):
    """İçeriği yoğun slaytlar: sadece köşe halkaları."""
    c = Canvas()
    c.fill_all(PAPER)
    pos = {"sag-ust": (W + 30, -40), "sol-ust": (-30, -40),
           "sag-alt": (W + 30, H + 40), "sol-alt": (-30, H + 40)}[kose]
    c.paint(disc_mask(W, H, pos[0], pos[1], 430, 340), ICE)
    c.paint(disc_mask(W, H, pos[0], pos[1], 320, 250), AZURE, alpha=0.30)
    c.paint(disc_mask(W, H, pos[0], pos[1], 200, 0), INK, alpha=0.06)
    ters = {"sag-ust": (-40, H + 50), "sol-ust": (W + 40, H + 50),
            "sag-alt": (-40, -50), "sol-alt": (W + 40, -50)}[kose]
    c.paint(disc_mask(W, H, ters[0], ters[1], 300, 235), ICE)
    return c.save(name)


# ---------------------------------------------------- maskeli fotoğraflar
def daire(name, pic, px=520, focus=0.5, halka=True, halka_col=AZURE):
    """Halkalı yuvarlak fotoğraf — referanstaki portre/görsel madalyonları."""
    s = px
    c = Canvas(s, s)
    r = s / 2 - (s * 0.055 if halka else 1)
    if halka:
        c.paint(disc_mask(s, s, s / 2, s / 2, s / 2 - 1, s / 2 - s * 0.022), halka_col)
        c.paint(disc_mask(s, s, s / 2, s / 2, s / 2 - s * 0.030, s / 2 - s * 0.052), WHITE)
    m = disc_mask(s, s, s / 2, s / 2, r)
    c.paint_img(m, photo(pic, s, s, focus))
    return c.save(name)


def kemer(name, pic, w=560, h=760, focus=0.5, ters=False):
    """
    Kemer form: üst iki köşe tam yuvarlak, alt köşeler hafif.
    Referanstaki 'Background / Mission Statement' kartlarının formu.
    """
    c = Canvas(w, h)
    r = w / 2
    cor = (0, 0, 1, 1) if ters else (1, 1, 0, 0)
    m = round_rect_mask(w, h, 0, 0, w - 1, h - 1, r, corners=cor)
    m = np.minimum(m, round_rect_mask(w, h, 0, 0, w - 1, h - 1, w * 0.10,
                                      corners=(1, 1, 1, 1) if ters else (0, 0, 1, 1)))
    c.paint_img(m, photo(pic, w, h, focus))
    c.paint(m, INK, alpha=0.10)
    return c.save(name)


def yaprak(name, pic, w=700, h=520, focus=0.5, yon=0):
    """Yaprak form: iki çapraz köşe yuvarlak, diğer ikisi keskin."""
    c = Canvas(w, h)
    r = min(w, h) * 0.42
    cor = [(1, 0, 1, 0), (0, 1, 0, 1)][yon % 2]
    m = round_rect_mask(w, h, 0, 0, w - 1, h - 1, r, corners=cor)
    c.paint_img(m, photo(pic, w, h, focus))
    return c.save(name)


def hap(name, pic, w=760, h=430, focus=0.5):
    """Hap form: iki uçu tam yuvarlak yatay kart."""
    c = Canvas(w, h)
    m = round_rect_mask(w, h, 0, 0, w - 1, h - 1, h / 2, corners=(1, 1, 1, 1))
    c.paint_img(m, photo(pic, w, h, focus))
    return c.save(name)


def malzeme(name, src_path, w, h, cerceve=True):
    """
    Materyal önizlemesi: kaynak EN-BOY ORANI KORUNARAK kutuya oturur
    (contain), etrafında ince mavi çerçeve. Gerdirme yok.
    """
    im = Image.open(src_path).convert("RGB")
    iw, ih = im.size
    pad = int(min(w, h) * 0.035) if cerceve else 0
    bw, bh = w - 2 * pad, h - 2 * pad
    s = min(bw / iw, bh / ih)
    nw, nh = int(round(iw * s)), int(round(ih * s))
    im = im.resize((nw, nh), Image.LANCZOS)
    c = Canvas(w, h)
    if cerceve:
        c.paint(round_rect_mask(w, h, 0, 0, w - 1, h - 1, min(w, h) * 0.05), WHITE)
        c.paint(round_rect_mask(w, h, 0, 0, w - 1, h - 1, min(w, h) * 0.05,
                                ) - round_rect_mask(w, h, 2, 2, w - 3, h - 3,
                                                    min(w, h) * 0.05), AZURE)
    ox, oy = (w - nw) // 2, (h - nh) // 2
    m = np.zeros((h, w), np.float32)
    m[oy:oy + nh, ox:ox + nw] = 1.0
    img = np.zeros((h, w, 3), np.float32)
    img[oy:oy + nh, ox:ox + nw] = np.asarray(im, np.float32)
    c.paint_img(m, img)
    return c.save(name)


def rozet(name, sekil="daire", col=AZURE, px=260):
    """Sayı/ikon rozetlerinin zemini — pptx dairesi yerine yumuşak kenarlı."""
    c = Canvas(px, px)
    if sekil == "daire":
        c.paint(disc_mask(px, px, px / 2, px / 2, px / 2 - 1), col)
    else:
        c.paint(round_rect_mask(px, px, 0, 0, px - 1, px - 1, px * 0.30), col)
    return c.save(name)


def ikon(name, tur, px=220, col=AZURE, cizgi=WHITE):
    """
    İletişim/anlam ikonları — daire zemin üstüne beyaz çizgi piktogram.
    Yazı tipi glifine güvenmemek için elle çiziliyor (Calibri'de sembol
    kapsaması makineden makineye değişiyor).
    """
    from PIL import ImageDraw
    S = px * 4                                  # süper örnekleme
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([0, 0, S - 1, S - 1], fill=col + (255,))
    w = int(S * 0.055)
    c = S / 2
    r = S * 0.26                                # ikon yarıçapı
    L = cizgi + (255,)

    if tur == "telefon":
        d.rounded_rectangle([c - r * 0.62, c - r, c + r * 0.62, c + r],
                            radius=r * 0.3, outline=L, width=w)
        d.line([c - r * 0.22, c + r * 0.72, c + r * 0.22, c + r * 0.72], fill=L, width=w)
    elif tur == "web":
        d.ellipse([c - r, c - r, c + r, c + r], outline=L, width=w)
        d.ellipse([c - r * 0.45, c - r, c + r * 0.45, c + r], outline=L, width=w)
        d.line([c - r, c, c + r, c], fill=L, width=w)
    elif tur == "instagram":
        d.rounded_rectangle([c - r, c - r, c + r, c + r], radius=r * 0.34,
                            outline=L, width=w)
        d.ellipse([c - r * 0.42, c - r * 0.42, c + r * 0.42, c + r * 0.42],
                  outline=L, width=w)
        d.ellipse([c + r * 0.48, c - r * 0.68, c + r * 0.72, c - r * 0.44], fill=L)
    elif tur == "konum":
        d.ellipse([c - r * 0.78, c - r, c + r * 0.78, c + r * 0.56],
                  outline=L, width=w)
        d.polygon([(c - r * 0.36, c + r * 0.30), (c + r * 0.36, c + r * 0.30),
                   (c, c + r)], fill=L)
        d.ellipse([c - r * 0.26, c - r * 0.48, c + r * 0.26, c + r * 0.04], fill=L)
    elif tur == "onay":
        d.line([c - r * 0.62, c, c - r * 0.12, c + r * 0.48], fill=L, width=w)
        d.line([c - r * 0.12, c + r * 0.48, c + r * 0.66, c - r * 0.52], fill=L, width=w)
    elif tur == "kalkan":
        d.polygon([(c - r * 0.8, c - r * 0.75), (c + r * 0.8, c - r * 0.75),
                   (c + r * 0.8, c + r * 0.12), (c, c + r), (c - r * 0.8, c + r * 0.12)],
                  outline=L, width=w)
    im = im.resize((px, px), Image.LANCZOS)
    p = os.path.join(OUT, name + ".png")
    im.save(p, optimize=True)
    return p


# ================================================================= ÜRET
def main():
    n = 0

    # --- slayt zeminleri
    n += 1; kapak("bg-01-kapak", "hero-courtyard-dusk.webp", focus=0.45, eksen=0.58)
    n += 1; yan_blok("bg-02-gundem", "aerial-pools.webp", side="left", focus=0.58,
                     eksen=0.68, zoom=1.9)
    n += 1; ust_bant("bg-03-kunye", "entrance-gate.webp", yuk=0.40, focus=0.5)
    n += 1; yan_blok("bg-04-konum", "street-corner.webp", side="right", focus=0.45, eksen=0.68)
    n += 1; alt_bant("bg-05-stok", yuk=0.70)
    n += 1; yan_blok("bg-06-yasam", "courtyard-pools.webp", side="left", focus=0.5, eksen=0.62)
    n += 1; koyu_panel("bg-07-odeme", "night-gate.webp", focus=0.42, kenar=0.60)
    n += 1; yan_blok("bg-08-yatirim", "ic-mekan/21-balkondan-deniz.webp", side="right",
                     focus=0.55, eksen=0.78)
    n += 1; yan_blok("bg-09-guvence", "balcony-dusk.webp", side="left", focus=0.5, eksen=0.70)
    n += 1; koyu_panel("bg-10-itiraz", "hero-courtyard-dusk.webp", focus=0.6, kenar=0.74)
    n += 1; ust_bant("bg-11-kitle", "facade-warm.webp", yuk=0.30, focus=0.5)
    n += 1; sade("bg-12-destek", kose="sol-alt")
    n += 1; yan_blok("bg-13-isbirligi", "loft-living.webp", side="right", focus=0.5, eksen=0.70)
    n += 1; yan_blok("bg-14-surec", "terrace-pergola.webp", side="right", focus=0.5, koyu=True, eksen=0.72)
    n += 1; kapak("bg-15-kapanis", "ic-mekan/21-balkondan-deniz.webp", focus=0.5, eksen=0.62)

    # --- daire fotoğraflar (künye, hedef kitle, yaşam)
    for nm, pic, fc in [
        ("d-studyo", "ic-mekan/01-1plus0-salon.webp", 0.5),
        ("d-salon", "ic-mekan/05-1plus1-salon.webp", 0.5),
        ("d-teras", "ic-mekan/13-bahceli-daire-terasi.webp", 0.5),
        ("d-dubleks", "ic-mekan/14-dubleks-bahcesi.webp", 0.5),
        ("d-sus", "ic-mekan/17-sus-havuzu.webp", 0.5),
        ("d-yuruyus", "ic-mekan/18-yuruyus-yolu.webp", 0.5),
        ("d-oyun", "ic-mekan/19-cocuk-oyun-parki.webp", 0.5),
        ("d-otopark", "ic-mekan/20-kapali-otopark.webp", 0.5),
        ("d-hol", "ic-mekan/16-giris-holu.webp", 0.5),
        ("d-avlu", "ic-mekan/15-balkondan-avlu.webp", 0.5),
    ]:
        n += 1; daire(nm, pic, px=560, focus=fc)

    # --- kemer kartlar (stok slaytı)
    for nm, pic in [("k-1plus0", "ic-mekan/02-1plus0-mutfak.webp"),
                    ("k-1plus1", "ic-mekan/06-1plus1-yatak-odasi.webp"),
                    ("k-loft", "ic-mekan/10-loft-mezanin.webp"),
                    ("k-dubleks", "ic-mekan/11-dubleks-salon.webp")]:
        n += 1; kemer(nm, pic, w=560, h=700)

    # --- materyal önizlemeleri (oran korunarak; gerdirme yok)
    kay = os.path.join(ROOT, "sunum", "kaynak")
    for nm, rel, w, h in [
        ("m-bilbord",  "tabela/bilbord-mia/onizleme/bilbord-2-kemer.jpg", 900, 560),
        ("m-bilbord2", "tabela/bilbord-mia/onizleme/bilbord-6-sutunlu.jpg", 900, 560),
        ("m-arsa",     "tabela/arsa-mia/onizleme/arsa-5-duotone.jpg", 900, 620),
        # roll-up'ın FİYATSIZ sürümü — sunumda fiyat yok, materyal de öyle görünsün
        ("m-rollup",   "tabela/fiyat-rollup/onizleme/fiyat-rollup-gunduz-2-fiyatsiz.jpg", 520, 1020),
        ("m-yaka",     "sunum/kaynak/m-yaka.jpg", 520, 740),
        ("m-katalog",  "public/images/catalog-1.webp", 520, 740),
    ]:
        pth = os.path.join(ROOT, rel)
        if os.path.exists(pth):
            n += 1; malzeme(nm, pth, w, h)
        else:
            print("EKSIK:", rel)

    # --- ikonlar
    for t in ["telefon", "web", "instagram", "konum", "onay", "kalkan"]:
        n += 1; ikon("i-" + t, t, px=220)

    print("uretildi:", n, "->", OUT)


if __name__ == "__main__":
    main()
