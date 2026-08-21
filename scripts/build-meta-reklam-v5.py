#!/usr/bin/env python3
"""
MİA PARK OCEAN — Meta reklam seti v5 (10 kreatif, 1080x1350).

Kullanıcının verdiği 9 referansın (Toprak Tan, Eminevim, Fuzul, arsaVev
mavi/yeşil/kırmızı, Katılımevim, Turyap) ortak teknikleri:

- SARI FOSFORLU ÇİP rakamların arkasında (Katılımevim'in imzası)
- Tek renk BLOK tasarımlar: koyu yeşil / koyu kırmızı alan + foto kartı
- Üçlü istatistik çipi: peşinat / %0 faiz / taksit
- Şehir adıyla başlık: "İZMİT EV SAHİBİ OLUYOR"
- Kırmızı yıldız "ÜSTELİK …!" ikinci iddiası
- Yazı gökyüzünde / renk alanında — bina hiç kapatılmıyor

Renk-font marka paletiyle sınırlı DEĞİL (işveren serbest bıraktı); sarı,
bordo, koyu yeşil reklam renkleri kullanılıyor. Fiyatlı kreatifler onaylı
örnek rakamları (1+0: 699.000 / 29.900 · 1+1: 999.000 / 39.900) dönemsellik
dipnotuyla taşır. "Peşinatsız" HİÇBİR YERDE geçmez (bizde %30 peşinat var).

    python3 scripts/build-meta-reklam-v5.py
"""

import math
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "public", "images")
YAZI = os.path.join(ROOT, "sunum", "yazitipi")
OUT = os.path.join(ROOT, "sosyal-medya", "meta-reklam")
os.makedirs(OUT, exist_ok=True)

W, H = 1080, 1350

# ------------------------------------------------------------------ renkler
NAVY = (10, 42, 74)          # başlık laciverti (Katılımevim tonu)
GECE = (4, 40, 58)           # marka laciverti
SARI = (255, 209, 74)        # fosforlu vurgu çipi
KIRMIZI = (200, 32, 42)      # yıldız / kırmızı alan
BORDO = (196, 40, 54)        # canlı kırmızı alan (koyu bordo açıldı)
YESIL = (16, 118, 90)        # canlı yeşil alan (koyu yeşil açıldı)
YESIL_A = (22, 140, 108)
GOK = (129, 195, 224)        # açık gök
BEYAZ = (255, 255, 255)
KAGIT = (245, 250, 252)
KURSUN = (71, 96, 110)

YASAL = "S.S. Yahya Kaptan Birlik Yapı Kooperatifi · Ocean Gayrimenkul, Tek Yetkili Satıcı · Görseller temsilidir."
DONEM = "Fiyatlar ve kampanya koşulları dönemsel olarak değişebilir."
TEL = "0540 028 00 41"
SITE = "miaparkocean.com"


def mont(kes, boy):
    return ImageFont.truetype(os.path.join(YAZI, "Montserrat-%s.ttf" % kes), boy)


def foto(ad, w, h, focus=0.5, zoom=1.0, focus_y=None):
    im = Image.open(os.path.join(SRC, ad)).convert("RGB")
    iw, ih = im.size
    s = max(w / iw, h / ih) * max(1.0, zoom)
    nw, nh = max(w, int(iw * s)), max(h, int(ih * s))
    im = im.resize((nw, nh), Image.LANCZOS)
    ox = int((nw - w) * focus)
    oy = int((nh - h) * (focus if focus_y is None else focus_y))
    return im.crop((ox, oy, ox + w, oy + h))


def kaydet(im, ad):
    im.convert("RGB").save(os.path.join(OUT, ad + ".jpg"), quality=92, optimize=True)
    print("  ", ad)


def logo(im, tur, x, y, gen):
    yol = {"beyaz": "public/brand/logo-ocean-white.png",
           "renkli": "public/brand/logo-ocean-trim.png"}[tur]
    lg = Image.open(os.path.join(ROOT, yol)).convert("RGBA")
    lg = lg.resize((gen, int(lg.height * gen / lg.width)), Image.LANCZOS)
    im.alpha_composite(lg, (int(x), int(y)))
    return lg.height


def gok_uzat(kaynak, foto_h, focus=0.5, zoom=1.0, gok=(8, 34, 56), focus_y=0.0):
    """Foto altta; üstü fotoğrafın göğüyle harmanlanan alan."""
    im = Image.new("RGB", (W, H), gok)
    t = np.linspace(0, 1, H - foto_h, dtype=np.float32)[:, None, None]
    g1 = np.array([min(255, c * 0.55 + 8) for c in gok], np.float32)
    g2 = np.array(gok, np.float32)
    grad = (g1 * (1 - t) + g2 * t).astype(np.uint8)
    im.paste(Image.fromarray(np.repeat(grad, W, axis=1), "RGB"), (0, 0))
    ft = foto(kaynak, W, foto_h, focus, zoom, focus_y=focus_y)
    im.paste(ft, (0, H - foto_h))
    bl = 110
    band = np.asarray(ft.crop((0, 0, W, bl)), np.float32)
    alfa = np.linspace(1, 0, bl, dtype=np.float32)[:, None, None]
    kar = (np.array(gok, np.float32) * alfa + band * (1 - alfa)).astype(np.uint8)
    im.paste(Image.fromarray(kar, "RGB"), (0, H - foto_h))
    return im.convert("RGBA")


def cip(dr, cx, cy, t, f, dolgu=SARI, yazi=NAVY, pad_x=26, pad_y=12, radius=14):
    """Fosforlu vurgu çipi — Katılımevim'in rakam vurgusu."""
    tw = dr.textlength(t, font=f)
    h = f.size + 2 * pad_y
    x0 = cx - tw / 2 - pad_x
    dr.rounded_rectangle([x0, cy - h / 2, cx + tw / 2 + pad_x, cy + h / 2],
                         radius=radius, fill=dolgu)
    dr.text((cx, cy - f.size * 0.06), t, font=f, fill=yazi, anchor="mm")
    return tw + 2 * pad_x, h


def cip_sol(dr, x, cy, t, f, dolgu=SARI, yazi=NAVY, pad_x=24, pad_y=11, radius=12):
    """Sola hizalı çip; sağ kenar x'ini döndürür."""
    tw = dr.textlength(t, font=f)
    h = f.size + 2 * pad_y
    dr.rounded_rectangle([x, cy - h / 2, x + tw + 2 * pad_x, cy + h / 2],
                         radius=radius, fill=dolgu)
    dr.text((x + pad_x + tw / 2, cy - f.size * 0.06), t, font=f, fill=yazi, anchor="mm")
    return x + tw + 2 * pad_x


def yildiz(im, cx, cy, r, satirlar, dolgu=KIRMIZI, yazi=BEYAZ, don=-12, N=26):
    kat = Image.new("RGBA", (r * 3, r * 3), (0, 0, 0, 0))
    kd = ImageDraw.Draw(kat)
    c = r * 1.5
    pts = []
    for i in range(N * 2):
        rr = r if i % 2 == 0 else r * 0.84
        a = math.pi * i / N
        pts.append((c + rr * math.cos(a), c + rr * math.sin(a)))
    kd.polygon(pts, fill=dolgu + (255,))
    fb = mont("ExtraBold", int(r * (0.30 if len(satirlar) > 1 else 0.36)))
    y0 = c - (len(satirlar) - 1) * r * 0.20
    for i, t in enumerate(satirlar):
        kd.text((c, y0 + i * r * 0.40), t, font=fb, fill=yazi, anchor="mm")
    kat = kat.rotate(don, resample=Image.BICUBIC, expand=False)
    im.alpha_composite(kat, (int(cx - c), int(cy - c)))


def foto_kart(im, kaynak, x0, y0, x1, y1, focus=0.5, zoom=1.0, radius=24, focus_y=None):
    kf = foto(kaynak, x1 - x0, y1 - y0, focus, zoom, focus_y=focus_y)
    m = Image.new("L", kf.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, kf.width, kf.height], radius=radius, fill=255)
    im.paste(kf, (x0, y0), m)


def dipnot(dr, satirlar, y=None, renk=(150, 175, 190)):
    y = y or H - 20
    for i, t in enumerate(reversed(satirlar)):
        dr.text((W / 2, y - i * 28), t, font=mont("Regular", 15), fill=renk, anchor="mm")


# ═══════════════════════════════════════════════════════════════ KREATİFLER
def k01():
    """Katılımevim klonu: İZMİT EV SAHİBİ OLUYOR + sarı çipler + yıldız."""
    im = gok_uzat("street-corner.webp", 640, 0.40, 1.05, gok=(150, 202, 226))
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 118), "İZMİT", font=mont("Black", 76), fill=NAVY, anchor="mm")
    dr.text((W / 2, 200), "EV SAHİBİ OLUYOR", font=mont("Black", 62), fill=NAVY, anchor="mm")
    f1 = mont("ExtraBold", 44)
    f2 = mont("ExtraBold", 38)
    # satır 1: [699.000 TL] PEŞİNATLA
    c1w = dr.textlength("699.000 TL", font=f1) + 52
    top1 = c1w + 26 + dr.textlength("PEŞİNATLA", font=f2)
    x = (W - top1) / 2
    x2 = cip_sol(dr, x, 300, "699.000 TL", f1)
    dr.text((x2 + 26, 300 - 3), "PEŞİNATLA", font=f2, fill=NAVY, anchor="lm")
    # satır 2: [29.900 TL] TAKSİTLE KAVUŞUN!
    c2w = dr.textlength("29.900 TL", font=f1) + 52
    top2 = c2w + 26 + dr.textlength("TAKSİTLE KAVUŞUN!", font=f2)
    x = (W - top2) / 2
    x2 = cip_sol(dr, x, 386, "29.900 TL", f1)
    dr.text((x2 + 26, 386 - 3), "TAKSİTLE KAVUŞUN!", font=f2, fill=NAVY, anchor="lm")
    dr.text((W / 2, 462), "1+0 dairelerde · Banka yok · Faiz yok · Kefil yok",
            font=mont("SemiBold", 27), fill=(36, 74, 108), anchor="mm")
    yildiz(im, W - 168, 585, 112, ["ÜSTELİK", "FAİZSİZ!"])
    dr = ImageDraw.Draw(im)
    # alt logo çipi
    dr.rounded_rectangle([(W - 320) / 2, H - 200, (W + 320) / 2, H - 88],
                         radius=18, fill=NAVY)
    logo(im, "beyaz", (W - 140) / 2, H - 196, 140)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, H - 56), TEL + "  ·  " + SITE, font=mont("Bold", 26),
            fill=BEYAZ, anchor="mm")
    dipnot(dr, [DONEM + " " + YASAL], renk=(52, 74, 92))
    kaydet(im, "meta-v5-01-izmit-oluyor")


def k02():
    """arsaVev yeşil klonu: mono yeşil alan + çipler + foto kartları."""
    im = Image.new("RGBA", (W, H), YESIL + (255,))
    dr = ImageDraw.Draw(im)
    # doku: köşe şeritleri
    for i in range(4):
        dr.line([(W - 260 + i * 60, 0), (W + 40 + i * 60, 300)],
                fill=YESIL_A + (255,), width=22)
        dr.line([(-40 - i * 60, H - 300), (260 - i * 60 + 60, H)],
                fill=YESIL_A + (255,), width=22)
    logo(im, "beyaz", (W - 230) / 2, 56, 230)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 268), "1+0 stüdyo dairelerde", font=mont("SemiBold", 38),
            fill=(196, 226, 214), anchor="mm")
    dr.text((W / 2, 336), "avantajlı yatırım fırsatı", font=mont("ExtraBold", 56),
            fill=BEYAZ, anchor="mm")
    # çift çip
    f1 = mont("ExtraBold", 40)
    fk = mont("SemiBold", 24)
    for i, (buyuk, kucuk) in enumerate([("699.000 TL", "peşinat"), ("29.900 TL", "taksit")]):
        cx = W / 2 - 235 + i * 470
        dr.rounded_rectangle([cx - 205, 412, cx + 205, 540], radius=20,
                             outline=BEYAZ, width=3)
        dr.text((cx, 462), buyuk, font=f1, fill=SARI, anchor="mm")
        dr.text((cx, 512), kucuk, font=fk, fill=BEYAZ, anchor="mm")
    cip(dr, W / 2, 596, "60 AY VADE FARKSIZ · BANKA YOK", mont("ExtraBold", 27),
        dolgu=SARI, yazi=YESIL)
    foto_kart(im, "facade-warm.webp", 90, 660, W // 2 - 12, 1030, zoom=1.0)
    foto_kart(im, "night-gate.webp", W // 2 + 12, 660, W - 90, 1030, 0.5, 1.10)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 1084), "İzmit MİA Bölgesi", font=mont("Bold", 30),
            fill=(196, 226, 214), anchor="mm")
    dr.text((W / 2, 1160), TEL + "  ·  " + SITE, font=mont("Bold", 30),
            fill=BEYAZ, anchor="mm")
    dipnot(dr, [DONEM, YASAL], renk=(178, 212, 200))
    kaydet(im, "meta-v5-02-yesil")


def k03():
    """arsaVev kırmızı klonu: bordo alan + üç istatistik çipi + foto kartı."""
    im = Image.new("RGBA", (W, H), BORDO + (255,))
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 130), "60 AY VADEYLE", font=mont("Black", 58), fill=BEYAZ, anchor="mm")
    dr.text((W / 2, 196), "EV SAHİBİ OLMAK İÇİN", font=mont("Black", 58),
            fill=BEYAZ, anchor="mm")
    dr.text((W / 2, 262), "SATIŞ OFİSİMİZE BEKLERİZ", font=mont("SemiBold", 34),
            fill=(255, 205, 205), anchor="mm")
    # üç çip
    fs1 = mont("ExtraBold", 30)
    fs2 = mont("SemiBold", 21)
    ic = [("699.000 TL'den", "başlayan peşinat"), ("%0", "faiz"),
          ("29.900 TL", "taksit")]
    for i, (a, b) in enumerate(ic):
        cx = W / 2 - 348 + i * 348
        dr.rounded_rectangle([cx - 166, 328, cx + 166, 446], radius=16,
                             outline=BEYAZ, width=3)
        dr.text((cx, 372), a, font=fs1, fill=SARI, anchor="mm")
        dr.text((cx, 416), b, font=fs2, fill=BEYAZ, anchor="mm")
    foto_kart(im, "night-gate.webp", 90, 500, W - 90, 1090, 0.5, 1.05, radius=22)
    dr = ImageDraw.Draw(im)
    logo(im, "beyaz", (W - 190) / 2, 1112, 190)
    dr = ImageDraw.Draw(im)
    dr.rounded_rectangle([W - 400, 1262, W - 60, 1320], radius=29, fill=BEYAZ)
    dr.text((W - 230, 1289), TEL, font=mont("ExtraBold", 26), fill=BORDO, anchor="mm")
    dr.text((60, 1289), "İzmit satış ofisi", font=mont("SemiBold", 25),
            fill=(255, 216, 216), anchor="lm")
    dipnot(dr, [DONEM + " " + YASAL], renk=(232, 178, 178))
    kaydet(im, "meta-v5-03-bordo")


def k04():
    """arsaVev mavi: 'Aylık 29.900 TL'ye ev sahibi olun.' gök + kule."""
    im = gok_uzat("entrance-gate.webp", 660, 0.45, 1.1, gok=(96, 154, 190))
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 130), "İzmit MİA'da", font=mont("SemiBold", 34),
            fill=(232, 244, 250), anchor="mm")
    dr.text((W / 2, 226), "Aylık 29.900 TL'ye", font=mont("ExtraBold", 66),
            fill=BEYAZ, anchor="mm")
    dr.text((W / 2, 302), "ev sahibi olun.", font=mont("ExtraBold", 66),
            fill=BEYAZ, anchor="mm")
    dr.text((W / 2, 388), "Üstelik 60 aya varan vade ve 0 faizle",
            font=mont("SemiBold", 30), fill=(226, 240, 248), anchor="mm")
    dr.text((W / 2, 430), "yeni evinize kavuşun!", font=mont("SemiBold", 30),
            fill=(226, 240, 248), anchor="mm")
    logo(im, "beyaz", (W - 240) / 2, 486, 240)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, H - 56), TEL + "  ·  " + SITE, font=mont("Bold", 27),
            fill=BEYAZ, anchor="mm")
    dipnot(dr, [DONEM + " " + YASAL])
    kaydet(im, "meta-v5-04-aylik")


def k05():
    """AÇIK YOK duvarı: beyaz zemin, sarı çipli YOK'lar, dış cephe altta."""
    im = Image.new("RGBA", (W, H), (250, 252, 254, 255))
    dr = ImageDraw.Draw(im)
    logo(im, "renkli", (W - 210) / 2, 44, 210)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 240), "EV SAHİBİ OLMAK İÇİN", font=mont("ExtraBold", 42),
            fill=NAVY, anchor="mm")
    f1 = mont("Black", 56)
    y = 330
    for a in ["BANKA", "FAİZ", "KEFİL"]:
        aw = dr.textlength(a + "  ", font=f1)
        bw = dr.textlength("YOK", font=f1) + 44
        x = (W - aw - bw - 16) / 2
        dr.text((x, y), a, font=f1, fill=NAVY, anchor="lm")
        cip(dr, x + aw + 16 + bw / 2, y, "YOK", f1, dolgu=SARI, yazi=NAVY,
            pad_x=22, pad_y=6)
        y += 96
    cip(dr, W / 2, y + 26, "60 AY SABİT TAKSİT", mont("ExtraBold", 40),
        dolgu=NAVY, yazi=BEYAZ, pad_x=36, pad_y=14)
    yildiz(im, W - 150, 210, 100, ["%30", "PEŞİNAT"], dolgu=KIRMIZI, don=10)
    dr = ImageDraw.Draw(im)
    ft = foto("hero-courtyard-dusk.webp", W, 520, 0.5, 1.02)
    im.paste(ft, (0, H - 520))
    bl = 90
    band = np.asarray(ft.crop((0, 0, W, bl)), np.float32)
    alfa = np.linspace(1, 0, bl, dtype=np.float32)[:, None, None]
    kar = (np.array((250, 252, 254), np.float32) * alfa + band * (1 - alfa)).astype(np.uint8)
    im.paste(Image.fromarray(kar, "RGB"), (0, H - 520))
    dr = ImageDraw.Draw(im)
    dr.rounded_rectangle([(W - 620) / 2, H - 120, (W + 620) / 2, H - 56],
                         radius=32, fill=NAVY)
    dr.text((W / 2, H - 88), TEL + "  ·  " + SITE, font=mont("Bold", 27),
            fill=BEYAZ, anchor="mm")
    dipnot(dr, [YASAL], renk=(210, 224, 232))
    kaydet(im, "meta-v5-05-yok-cipleri")


def k06():
    """Yeşil varyant: dev %0 FAİZ + tek geniş foto kartı."""
    im = Image.new("RGBA", (W, H), YESIL + (255,))
    dr = ImageDraw.Draw(im)
    for i in range(5):
        dr.line([(W - 200 + i * 52, 0), (W + 120 + i * 52, 360)],
                fill=YESIL_A + (255,), width=18)
    logo(im, "beyaz", (W - 220) / 2, 52, 220)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 300), "%0", font=mont("Black", 250), fill=SARI, anchor="mm")
    dr.text((W / 2, 470), "FAİZ · VADE FARKI · KOMİSYON", font=mont("ExtraBold", 40),
            fill=BEYAZ, anchor="mm")
    dr.text((W / 2, 534), "60 ay sabit taksit · %30 peşinat",
            font=mont("SemiBold", 30), fill=(196, 226, 214), anchor="mm")
    foto_kart(im, "entrance-gate.webp", 90, 600, W - 90, 1120, 0.45, 1.05)
    dr = ImageDraw.Draw(im)
    cip(dr, W / 2, 1180, "İZMİT MİA BÖLGESİ", mont("ExtraBold", 28),
        dolgu=SARI, yazi=YESIL)
    dr.text((W / 2, 1246), TEL + "  ·  " + SITE, font=mont("Bold", 29),
            fill=BEYAZ, anchor="mm")
    dipnot(dr, [YASAL], renk=(178, 212, 200))
    kaydet(im, "meta-v5-06-yesil-sifir")


def k07():
    """AÇIK 60 AY: beyaz zemin, kırmızı dev rakam, dış cephe kartı."""
    im = Image.new("RGBA", (W, H), (252, 250, 248, 255))
    dr = ImageDraw.Draw(im)
    logo(im, "renkli", (W - 210) / 2, 44, 210)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 300), "60 AY", font=mont("Black", 190), fill=KIRMIZI, anchor="mm")
    cip(dr, W / 2, 448, "VADE FARKSIZ · SABİT TAKSİT", mont("ExtraBold", 36),
        dolgu=SARI, yazi=NAVY, pad_x=34, pad_y=14)
    dr.text((W / 2, 528), "Banka yok · Faiz yok · Kefil yok · Komisyon yok",
            font=mont("SemiBold", 29), fill=(96, 74, 70), anchor="mm")
    foto_kart(im, "terrace-pergola.webp", 90, 592, W - 90, 1140, 0.5, 1.05)
    dr = ImageDraw.Draw(im)
    dr.rounded_rectangle([(W - 560) / 2, 1188, (W + 560) / 2, 1256], radius=34,
                         fill=KIRMIZI)
    dr.text((W / 2, 1222), TEL, font=mont("ExtraBold", 34), fill=BEYAZ, anchor="mm")
    dipnot(dr, [YASAL], renk=KURSUN)
    kaydet(im, "meta-v5-07-acik-60")


def k08():
    """Katılımevim varyantı: KOCAELİ + deniz göklü foto."""
    im = gok_uzat("ic-mekan/21-balkondan-deniz.webp", 700, 0.5, 1.0,
                  gok=(140, 194, 220), focus_y=0.15)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 112), "KOCAELİ", font=mont("Black", 74), fill=NAVY, anchor="mm")
    dr.text((W / 2, 192), "DENİZE YAKIN EV SAHİBİ OLUYOR", font=mont("Black", 40),
            fill=NAVY, anchor="mm")
    f1 = mont("ExtraBold", 42)
    f2 = mont("ExtraBold", 36)
    c1w = dr.textlength("999.000 TL", font=f1) + 52
    top1 = c1w + 24 + dr.textlength("PEŞİNATLA 1+1", font=f2)
    x = (W - top1) / 2
    x2 = cip_sol(dr, x, 286, "999.000 TL", f1)
    dr.text((x2 + 24, 283), "PEŞİNATLA 1+1", font=f2, fill=NAVY, anchor="lm")
    c2w = dr.textlength("39.900 TL", font=f1) + 52
    top2 = c2w + 24 + dr.textlength("TAKSİTLE!", font=f2)
    x = (W - top2) / 2
    x2 = cip_sol(dr, x, 368, "39.900 TL", f1)
    dr.text((x2 + 24, 365), "TAKSİTLE!", font=f2, fill=NAVY, anchor="lm")
    dr.text((W / 2, 440), "İzmit sahiline 2 dk · 60 ay vade farksız",
            font=mont("SemiBold", 27), fill=(36, 74, 108), anchor="mm")
    yildiz(im, 158, 545, 104, ["BANKA", "YOK!"])
    dr = ImageDraw.Draw(im)
    dr.rounded_rectangle([(W - 320) / 2, H - 196, (W + 320) / 2, H - 86],
                         radius=18, fill=NAVY)
    logo(im, "beyaz", (W - 140) / 2, H - 192, 140)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, H - 54), TEL + "  ·  " + SITE, font=mont("Bold", 26),
            fill=BEYAZ, anchor="mm")
    dipnot(dr, [DONEM + " " + YASAL], renk=(52, 74, 92))
    kaydet(im, "meta-v5-08-kocaeli")


def k09():
    """Açık gök + sarı çipli mini liste + foto kartı (Fuzul ferahlığı)."""
    im = Image.new("RGBA", (W, H))
    t = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    g1 = np.array((140, 198, 224), np.float32)
    g2 = np.array((235, 246, 251), np.float32)
    im.paste(Image.fromarray(np.repeat((g1 * (1 - t) + g2 * t).astype(np.uint8), W, axis=1),
                             "RGB"), (0, 0))
    dr = ImageDraw.Draw(im)
    dr.rounded_rectangle([110, 84, W - 110, 264], radius=36, fill=NAVY)
    dr.text((W / 2, 144), "Tasarrufa dayalı finansmanla", font=mont("SemiBold", 32),
            fill=(150, 205, 228), anchor="mm")
    dr.text((W / 2, 204), "EV SAHİBİ OL!", font=mont("Black", 58), fill=BEYAZ, anchor="mm")
    y = 330
    for a, b in [("BANKA YOK", None), ("FAİZ YOK", None), ("60 AY SABİT TAKSİT", None)]:
        cip(dr, W / 2, y, a, mont("ExtraBold", 32), dolgu=SARI, yazi=NAVY,
            pad_x=32, pad_y=12)
        y += 84
    foto_kart(im, "facade-warm.webp", 120, 606, W - 120, 1130, 0.5, 1.0, radius=28)
    dr = ImageDraw.Draw(im)
    yildiz(im, W - 175, 640, 102, ["%30", "PEŞİNAT"], dolgu=KIRMIZI, don=10)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 1190), TEL + "  ·  " + SITE, font=mont("ExtraBold", 30),
            fill=NAVY, anchor="mm")
    dr.text((W / 2, 1246), "MİA PARK OCEAN · İZMİT MİA BÖLGESİ",
            font=mont("Bold", 24), fill=(36, 90, 122), anchor="mm")
    dipnot(dr, [YASAL], renk=KURSUN)
    kaydet(im, "meta-v5-09-acik")


def k10():
    """Lacivert-sarı kampanya: 'taksitle EV SAHİBİ OL' karışık vurgu."""
    im = Image.new("RGBA", (W, H), (16, 58, 100, 255))
    dr = ImageDraw.Draw(im)
    for i in range(5):
        dr.line([(-60 + i * 46, 0), (240 + i * 46, 300)],
                fill=(24, 74, 122, 255), width=16)
    logo(im, "beyaz", (W - 230) / 2, 58, 230)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 268), "29.900 TL taksitle", font=mont("SemiBold", 44),
            fill=(150, 205, 228), anchor="mm")
    dr.text((W / 2, 366), "EV SAHİBİ", font=mont("Black", 104), fill=BEYAZ, anchor="mm")
    olw, olh = cip(dr, W / 2, 480, "OLMA ZAMANI", mont("Black", 80),
                   dolgu=SARI, yazi=NAVY, pad_x=36, pad_y=10)
    dr.text((W / 2, 580), "Banka yok · Faiz yok · Kefil yok · Ara ödeme yok",
            font=mont("SemiBold", 29), fill=(180, 208, 226), anchor="mm")
    foto_kart(im, "balcony-dusk.webp", 90, 646, W - 90, 1140, 0.55, 1.05)
    dr = ImageDraw.Draw(im)
    yildiz(im, W - 172, 680, 100, ["60 AY", "VADE", "FARKSIZ"], dolgu=KIRMIZI, don=12)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 1196), TEL + "  ·  " + SITE, font=mont("ExtraBold", 30),
            fill=SARI, anchor="mm")
    dipnot(dr, [DONEM, YASAL])
    kaydet(im, "meta-v5-10-navy-sari")


def kontak():
    fs = sorted(f for f in os.listdir(OUT) if f.startswith("meta-v5-") and f.endswith(".jpg"))
    tw = 360
    th = int(tw * H / W)
    cols, rows = 5, 2
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * 8, rows * th + (rows + 1) * 8),
                      (16, 20, 26))
    for i, f in enumerate(fs[:10]):
        im = Image.open(os.path.join(OUT, f)).resize((tw, th), Image.LANCZOS)
        sheet.paste(im, (8 + (i % cols) * (tw + 8), 8 + (i // cols) * (th + 8)))
    sheet.save(os.path.join(OUT, "kontak-v5.jpg"), quality=88)
    print("   kontak-v5.jpg")


if __name__ == "__main__":
    for k in [k01, k02, k03, k04, k05, k06, k07, k08, k09, k10]:
        k()
    kontak()
    print("tamam ->", OUT)
