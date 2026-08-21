#!/usr/bin/env python3
"""
MİA PARK OCEAN — Meta reklam seti v5 (10 kreatif, 1080x1350).

Referans teknikleri (Katılımevim, arsaVev, Eminevim, Fuzul, Toprak Tan,
Turyap): sarı fosforlu çip rakam vurgusu, canlı tek renk bloklar + foto
kartı, üçlü istatistik çipi, şehir başlığı, kırmızı "üstelik" yıldızı.

Sabit kurallar (işveren):
- Her kreatifin TEPESİNDE: solda MİA PARK OCEAN, sağda OCEAN GAYRİMENKUL
  logosu — pedsiz, şeffaf PNG (açık zeminde renkli, koyu zeminde beyaz).
- "Görseller temsilidir" ve kooperatif adı HİÇBİR görselde yazmaz.
  Fiyat geçenlerde yalnız dönemsellik dipnotu kalır.
- Fotoğraflar YALNIZ dış cephe; bina üzerine yazı binmez.
- "Peşinatsız" geçmez; "%30 peşinat" ORANI da görsellerde yazılmaz
  (yalnız TL tutarlar). Fiyatlar onaylı örnekler:
  1+0: 699.000 / 29.900 · 1+1: 999.000 / 39.900.

    python3 scripts/build-meta-reklam-v5.py
"""

import math
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "public", "images")
YAZI = os.path.join(ROOT, "sunum", "yazitipi")
OUT = os.path.join(ROOT, "sosyal-medya", "meta-reklam")
os.makedirs(OUT, exist_ok=True)

W, H = 1080, 1350

# ------------------------------------------------------------------ renkler
NAVY = (10, 42, 74)
SARI = (255, 209, 74)
KIRMIZI = (200, 32, 42)
CANLI_K = (196, 40, 54)      # canlı kırmızı alan
YESIL = (16, 118, 90)        # canlı yeşil alan
YESIL_A = (22, 140, 108)
BEYAZ = (255, 255, 255)
KURSUN = (71, 96, 110)

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


def ust_logolar(im, koyu):
    """Solda MİA, sağda Ocean Gayrimenkul — her kreatifte aynı hat,
    pedsiz şeffaf PNG; zemine göre beyaz/renkli sürüm seçilir."""
    mia = os.path.join(ROOT, "public", "brand",
                       "logo-ocean-white.png" if koyu else "logo-ocean-trim.png")
    oce = (os.path.join(ROOT, "public", "ocean-logo-white.png") if koyu
           else os.path.join(ROOT, "sunum", "kaynak", "sekil", "ocean-logo-renkli.png"))
    lg = Image.open(mia).convert("RGBA")
    lg = lg.resize((170, int(lg.height * 170 / lg.width)), Image.LANCZOS)   # h≈116
    im.alpha_composite(lg, (56, 28))
    og = Image.open(oce).convert("RGBA")
    og = og.resize((170, int(og.height * 170 / og.width)), Image.LANCZOS)   # h≈71
    im.alpha_composite(og, (W - 56 - 170, 50))


def cip(dr, cx, cy, t, f, dolgu=SARI, yazi=NAVY, pad_x=26, pad_y=12, radius=14):
    tw = dr.textlength(t, font=f)
    h = f.size + 2 * pad_y
    dr.rounded_rectangle([cx - tw / 2 - pad_x, cy - h / 2,
                          cx + tw / 2 + pad_x, cy + h / 2], radius=radius, fill=dolgu)
    dr.text((cx, cy - f.size * 0.06), t, font=f, fill=yazi, anchor="mm")


def cip_sol(dr, x, cy, t, f, dolgu=SARI, yazi=NAVY, pad_x=24, pad_y=11, radius=12):
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


def gok_uzat(kaynak, foto_h, focus=0.5, zoom=1.0, gok=(150, 202, 226), focus_y=0.0):
    im = Image.new("RGB", (W, H), gok)
    t = np.linspace(0, 1, H - foto_h, dtype=np.float32)[:, None, None]
    g1 = np.array([min(255, c * 0.55 + 8) for c in gok], np.float32)
    grad = (g1 * (1 - t) + np.array(gok, np.float32) * t).astype(np.uint8)
    im.paste(Image.fromarray(np.repeat(grad, W, axis=1), "RGB"), (0, 0))
    ft = foto(kaynak, W, foto_h, focus, zoom, focus_y=focus_y)
    im.paste(ft, (0, H - foto_h))
    bl = 110
    band = np.asarray(ft.crop((0, 0, W, bl)), np.float32)
    alfa = np.linspace(1, 0, bl, dtype=np.float32)[:, None, None]
    kar = (np.array(gok, np.float32) * alfa + band * (1 - alfa)).astype(np.uint8)
    im.paste(Image.fromarray(kar, "RGB"), (0, H - foto_h))
    return im.convert("RGBA")


def foto_alt_beyaz(im, kaynak, yuk, focus=0.5, zoom=1.0, zemin=(250, 252, 254),
                   focus_y=None):
    """Açık zeminli kreatifte alta tam genişlik dış cephe, üstü yumuşak."""
    ft = foto(kaynak, W, yuk, focus, zoom, focus_y=focus_y)
    im.paste(ft, (0, H - yuk))
    bl = 90
    band = np.asarray(ft.crop((0, 0, W, bl)), np.float32)
    alfa = np.linspace(1, 0, bl, dtype=np.float32)[:, None, None]
    kar = (np.array(zemin, np.float32) * alfa + band * (1 - alfa)).astype(np.uint8)
    im.paste(Image.fromarray(kar, "RGB"), (0, H - yuk))


def tel_cip(dr, cy, dolgu=NAVY, yazi=BEYAZ, site=True, gen=640):
    t = TEL + ("  ·  " + SITE if site else "")
    dr.rounded_rectangle([(W - gen) / 2, cy - 34, (W + gen) / 2, cy + 34],
                         radius=34, fill=dolgu)
    dr.text((W / 2, cy), t, font=mont("Bold", 28), fill=yazi, anchor="mm")


def dipnot_donem(dr, koyu_zemin=False):
    dr.text((W / 2, H - 22), DONEM, font=mont("Regular", 16),
            fill=(214, 226, 234) if koyu_zemin else (96, 116, 130), anchor="mm")


# ═══════════════════════════════════════════════════════════════ KREATİFLER
def k01():
    """İZMİT EV SAHİBİ OLUYOR — sarı çipler, yıldız, gök başlığı."""
    im = gok_uzat("street-corner.webp", 620, 0.40, 1.05)
    dr = ImageDraw.Draw(im)
    ust_logolar(im, koyu=True)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 236), "İZMİT", font=mont("Black", 74), fill=NAVY, anchor="mm")
    dr.text((W / 2, 316), "EV SAHİBİ OLUYOR", font=mont("Black", 60), fill=NAVY, anchor="mm")
    f1, f2 = mont("ExtraBold", 44), mont("ExtraBold", 38)
    for cy, buyuk, kucuk in [(414, "699.000 TL", "PEŞİNATLA"),
                             (500, "29.900 TL", "TAKSİTLE KAVUŞUN!")]:
        top = dr.textlength(buyuk, font=f1) + 48 + 26 + dr.textlength(kucuk, font=f2)
        x = (W - top) / 2
        x2 = cip_sol(dr, x, cy, buyuk, f1)
        dr.text((x2 + 26, cy - 3), kucuk, font=f2, fill=NAVY, anchor="lm")
    dr.text((W / 2, 576), "1+0 dairelerde · Banka yok · Faiz yok · Kefil yok",
            font=mont("SemiBold", 27), fill=(36, 74, 108), anchor="mm")
    yildiz(im, W - 162, 662, 108, ["ÜSTELİK", "FAİZSİZ!"])
    dr = ImageDraw.Draw(im)
    tel_cip(dr, H - 96)
    dipnot_donem(dr)
    kaydet(im, "meta-v5-01-izmit-oluyor")


def k02():
    """Canlı yeşil blok — çerçeve çipler + iki dış cephe kartı."""
    im = Image.new("RGBA", (W, H), YESIL + (255,))
    dr = ImageDraw.Draw(im)
    for i in range(4):
        dr.line([(W - 260 + i * 60, 0), (W + 40 + i * 60, 300)],
                fill=YESIL_A + (255,), width=22)
        dr.line([(-40 - i * 60, H - 300), (320 - i * 60, H)],
                fill=YESIL_A + (255,), width=22)
    ust_logolar(im, koyu=True)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 234), "1+0 stüdyo dairelerde", font=mont("SemiBold", 38),
            fill=(206, 236, 224), anchor="mm")
    dr.text((W / 2, 302), "avantajlı yatırım fırsatı", font=mont("ExtraBold", 56),
            fill=BEYAZ, anchor="mm")
    f1, fk = mont("ExtraBold", 40), mont("SemiBold", 24)
    for i, (buyuk, kucuk) in enumerate([("699.000 TL", "peşinat"), ("29.900 TL", "taksit")]):
        cx = W / 2 - 235 + i * 470
        dr.rounded_rectangle([cx - 205, 376, cx + 205, 504], radius=20,
                             outline=BEYAZ, width=3)
        dr.text((cx, 426), buyuk, font=f1, fill=SARI, anchor="mm")
        dr.text((cx, 476), kucuk, font=fk, fill=BEYAZ, anchor="mm")
    cip(dr, W / 2, 560, "60 AY VADE FARKSIZ · BANKA YOK", mont("ExtraBold", 27),
        dolgu=SARI, yazi=YESIL)
    foto_kart(im, "entrance-gate.webp", 90, 622, W - 90, 1010, 0.45, 1.0, focus_y=0.62)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 1062), "İzmit MİA Bölgesi", font=mont("Bold", 30),
            fill=(206, 236, 224), anchor="mm")
    tel_cip(dr, 1146, dolgu=BEYAZ, yazi=YESIL)
    dipnot_donem(dr, koyu_zemin=True)
    kaydet(im, "meta-v5-02-yesil")


def k03():
    """Canlı kırmızı blok — üçlü istatistik çipi + gece cephesi kartı."""
    im = Image.new("RGBA", (W, H), CANLI_K + (255,))
    dr = ImageDraw.Draw(im)
    ust_logolar(im, koyu=True)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 226), "60 AY VADEYLE", font=mont("Black", 56), fill=BEYAZ, anchor="mm")
    dr.text((W / 2, 290), "EV SAHİBİ OLMAK İÇİN", font=mont("Black", 56),
            fill=BEYAZ, anchor="mm")
    dr.text((W / 2, 352), "SATIŞ OFİSİMİZE BEKLERİZ", font=mont("SemiBold", 34),
            fill=(255, 216, 216), anchor="mm")
    fs1, fs2 = mont("ExtraBold", 30), mont("SemiBold", 21)
    for i, (a, b) in enumerate([("699.000 TL'den", "başlayan peşinat"),
                                ("%0", "faiz"), ("29.900 TL", "taksit")]):
        cx = W / 2 - 348 + i * 348
        dr.rounded_rectangle([cx - 166, 412, cx + 166, 530], radius=16,
                             outline=BEYAZ, width=3)
        dr.text((cx, 456), a, font=fs1, fill=SARI, anchor="mm")
        dr.text((cx, 500), b, font=fs2, fill=BEYAZ, anchor="mm")
    foto_kart(im, "night-gate.webp", 90, 584, W - 90, 1150, 0.5, 1.05, radius=22)
    dr = ImageDraw.Draw(im)
    dr.rounded_rectangle([W - 400, 1198, W - 60, 1256], radius=29, fill=BEYAZ)
    dr.text((W - 230, 1225), TEL, font=mont("ExtraBold", 26), fill=CANLI_K, anchor="mm")
    dr.text((60, 1225), "İzmit satış ofisi", font=mont("SemiBold", 25),
            fill=(255, 222, 222), anchor="lm")
    dipnot_donem(dr, koyu_zemin=True)
    kaydet(im, "meta-v5-03-kirmizi")


def k04():
    """'Aylık 29.900 TL'ye ev sahibi olun.' — gök + dış cephe."""
    im = gok_uzat("entrance-gate.webp", 650, 0.45, 1.1, gok=(96, 154, 190))
    dr = ImageDraw.Draw(im)
    ust_logolar(im, koyu=True)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 224), "İzmit MİA'da", font=mont("SemiBold", 34),
            fill=(232, 244, 250), anchor="mm")
    dr.text((W / 2, 312), "Aylık 29.900 TL'ye", font=mont("ExtraBold", 64),
            fill=BEYAZ, anchor="mm")
    dr.text((W / 2, 386), "ev sahibi olun.", font=mont("ExtraBold", 64),
            fill=BEYAZ, anchor="mm")
    dr.text((W / 2, 468), "Üstelik 60 aya varan vade ve 0 faizle",
            font=mont("SemiBold", 30), fill=(226, 240, 248), anchor="mm")
    dr.text((W / 2, 510), "yeni evinize kavuşun!", font=mont("SemiBold", 30),
            fill=(226, 240, 248), anchor="mm")
    dr.text((W / 2, 590), TEL + "  ·  " + SITE, font=mont("Bold", 28),
            fill=BEYAZ, anchor="mm")
    dipnot_donem(dr, koyu_zemin=True)
    kaydet(im, "meta-v5-04-aylik")


def k05():
    """Açık YOK duvarı — sarı çipler, dış cephe altta."""
    im = Image.new("RGBA", (W, H), (250, 252, 254, 255))
    dr = ImageDraw.Draw(im)
    ust_logolar(im, koyu=False)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 226), "EV SAHİBİ OLMAK İÇİN", font=mont("ExtraBold", 42),
            fill=NAVY, anchor="mm")
    f1 = mont("Black", 56)
    y = 318
    for a in ["BANKA", "FAİZ", "KEFİL"]:
        aw = dr.textlength(a + "  ", font=f1)
        bw = dr.textlength("YOK", font=f1) + 44
        x = (W - aw - bw - 16) / 2
        dr.text((x, y), a, font=f1, fill=NAVY, anchor="lm")
        cip(dr, x + aw + 16 + bw / 2, y, "YOK", f1, pad_x=22, pad_y=6)
        y += 96
    cip(dr, W / 2, y + 24, "60 AY SABİT TAKSİT", mont("ExtraBold", 40),
        dolgu=NAVY, yazi=BEYAZ, pad_x=36, pad_y=14)
    yildiz(im, W - 148, 300, 98, ["KOMİSYON", "YOK!"], don=10)
    dr = ImageDraw.Draw(im)
    foto_alt_beyaz(im, "entrance-gate.webp", 500, 0.5, 1.0, focus_y=0.55)
    dr = ImageDraw.Draw(im)
    tel_cip(dr, H - 92)
    kaydet(im, "meta-v5-05-yok-cipleri")


def k06():
    """Canlı yeşil %0 — dev sarı rakam + gündüz cephe kartı."""
    im = Image.new("RGBA", (W, H), YESIL + (255,))
    dr = ImageDraw.Draw(im)
    for i in range(5):
        dr.line([(W - 200 + i * 52, 0), (W + 120 + i * 52, 360)],
                fill=YESIL_A + (255,), width=18)
    ust_logolar(im, koyu=True)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 320), "%0", font=mont("Black", 240), fill=SARI, anchor="mm")
    dr.text((W / 2, 484), "FAİZ · VADE FARKI · KOMİSYON", font=mont("ExtraBold", 40),
            fill=BEYAZ, anchor="mm")
    dr.text((W / 2, 546), "60 ay sabit taksit · banka yok",
            font=mont("SemiBold", 30), fill=(206, 236, 224), anchor="mm")
    foto_kart(im, "entrance-gate.webp", 90, 606, W - 90, 1116, 0.45, 1.05)
    dr = ImageDraw.Draw(im)
    cip(dr, W / 2, 1172, "İZMİT MİA BÖLGESİ", mont("ExtraBold", 28),
        dolgu=SARI, yazi=YESIL)
    dr.text((W / 2, 1240), TEL + "  ·  " + SITE, font=mont("Bold", 29),
            fill=BEYAZ, anchor="mm")
    kaydet(im, "meta-v5-06-yesil-sifir")


def k07():
    """Açık 60 AY — kırmızı dev rakam + dış cephe kartı."""
    im = Image.new("RGBA", (W, H), (252, 250, 248, 255))
    dr = ImageDraw.Draw(im)
    ust_logolar(im, koyu=False)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 300), "60 AY", font=mont("Black", 185), fill=KIRMIZI, anchor="mm")
    cip(dr, W / 2, 442, "VADE FARKSIZ · SABİT TAKSİT", mont("ExtraBold", 36),
        pad_x=34, pad_y=14)
    dr.text((W / 2, 522), "Banka yok · Faiz yok · Kefil yok · Komisyon yok",
            font=mont("SemiBold", 29), fill=(96, 74, 70), anchor="mm")
    foto_kart(im, "entrance-gate.webp", 90, 584, W - 90, 1136, 0.45, 1.05, focus_y=0.5)
    dr = ImageDraw.Draw(im)
    tel_cip(dr, 1216, dolgu=KIRMIZI, site=False, gen=520)
    kaydet(im, "meta-v5-07-acik-60")


def k08():
    """KOCAELİ DENİZE YAKIN — deniz göğü, 1+1 rakamları."""
    im = gok_uzat("ic-mekan/21-balkondan-deniz.webp", 690, 0.5, 1.0,
                  gok=(140, 194, 220), focus_y=0.15)
    dr = ImageDraw.Draw(im)
    ust_logolar(im, koyu=True)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 230), "KOCAELİ", font=mont("Black", 72), fill=NAVY, anchor="mm")
    dr.text((W / 2, 308), "DENİZE YAKIN EV SAHİBİ OLUYOR", font=mont("Black", 38),
            fill=NAVY, anchor="mm")
    f1, f2 = mont("ExtraBold", 42), mont("ExtraBold", 36)
    for cy, buyuk, kucuk in [(398, "999.000 TL", "PEŞİNATLA 1+1"),
                             (480, "39.900 TL", "TAKSİTLE!")]:
        top = dr.textlength(buyuk, font=f1) + 48 + 24 + dr.textlength(kucuk, font=f2)
        x = (W - top) / 2
        x2 = cip_sol(dr, x, cy, buyuk, f1)
        dr.text((x2 + 24, cy - 3), kucuk, font=f2, fill=NAVY, anchor="lm")
    dr.text((W / 2, 552), "İzmit sahiline 2 dk · 60 ay vade farksız",
            font=mont("SemiBold", 27), fill=(36, 74, 108), anchor="mm")
    yildiz(im, 156, 636, 100, ["BANKA", "YOK!"])
    dr = ImageDraw.Draw(im)
    tel_cip(dr, H - 96)
    dipnot_donem(dr)
    kaydet(im, "meta-v5-08-kocaeli")


def k09():
    """Açık gök — lacivert afiş + sarı çipler + cephe kartı."""
    im = Image.new("RGBA", (W, H))
    t = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    g1 = np.array((140, 198, 224), np.float32)
    g2 = np.array((235, 246, 251), np.float32)
    im.paste(Image.fromarray(np.repeat((g1 * (1 - t) + g2 * t).astype(np.uint8), W, axis=1),
                             "RGB"), (0, 0))
    dr = ImageDraw.Draw(im)
    ust_logolar(im, koyu=False)
    dr = ImageDraw.Draw(im)
    dr.rounded_rectangle([110, 176, W - 110, 356], radius=36, fill=NAVY)
    dr.text((W / 2, 236), "Tasarrufa dayalı finansmanla", font=mont("SemiBold", 32),
            fill=(150, 205, 228), anchor="mm")
    dr.text((W / 2, 296), "EV SAHİBİ OL!", font=mont("Black", 58), fill=BEYAZ, anchor="mm")
    y = 424
    for a in ["BANKA YOK", "FAİZ YOK", "60 AY SABİT TAKSİT"]:
        cip(dr, W / 2, y, a, mont("ExtraBold", 32), pad_x=32, pad_y=12)
        y += 84
    foto_kart(im, "entrance-gate.webp", 120, 690, W - 120, 1180, 0.45, 1.0,
              radius=28, focus_y=0.58)
    dr = ImageDraw.Draw(im)
    yildiz(im, W - 172, 724, 100, ["ARA", "ÖDEME", "YOK!"], don=10)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 1240), TEL + "  ·  " + SITE, font=mont("ExtraBold", 30),
            fill=NAVY, anchor="mm")
    kaydet(im, "meta-v5-09-acik")


def k10():
    """Lacivert-sarı kampanya — 'EV SAHİBİ [OLMA ZAMANI]'."""
    im = Image.new("RGBA", (W, H), (16, 58, 100, 255))
    dr = ImageDraw.Draw(im)
    for i in range(5):
        dr.line([(-60 + i * 46, 0), (240 + i * 46, 300)],
                fill=(24, 74, 122, 255), width=16)
    ust_logolar(im, koyu=True)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 234), "29.900 TL taksitle", font=mont("SemiBold", 44),
            fill=(150, 205, 228), anchor="mm")
    dr.text((W / 2, 330), "EV SAHİBİ", font=mont("Black", 100), fill=BEYAZ, anchor="mm")
    cip(dr, W / 2, 442, "OLMA ZAMANI", mont("Black", 78), pad_x=36, pad_y=10)
    dr.text((W / 2, 540), "Banka yok · Faiz yok · Kefil yok · Ara ödeme yok",
            font=mont("SemiBold", 29), fill=(180, 208, 226), anchor="mm")
    foto_kart(im, "entrance-gate.webp", 90, 600, W - 90, 1140, 0.5, 1.1, focus_y=0.55)
    dr = ImageDraw.Draw(im)
    yildiz(im, W - 170, 634, 98, ["60 AY", "VADE", "FARKSIZ"], don=12)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 1196), TEL + "  ·  " + SITE, font=mont("ExtraBold", 30),
            fill=SARI, anchor="mm")
    dipnot_donem(dr, koyu_zemin=True)
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
