#!/usr/bin/env python3
"""
MİA PARK OCEAN — turkuaz-01 "KOCAELİ EV SAHİBİ OLUYOR!" bilbordunun
SOSYAL MEDYA uyarlaması (aynı içerik ve dil, 3 format):

    sosyal-turkuaz-45.jpg     1080 x 1350  (Instagram/Facebook akış, 4:5)
    sosyal-turkuaz-kare.jpg   1080 x 1080  (kare gönderi)
    sosyal-turkuaz-story.jpg  1080 x 1920  (story / reels kapak, 9:16)

Ortak öğeler (bilborddaki gibi):
- Gök-buz dikey gradyan; giriş kapısı fotoğrafı ALTTA çerçevesiz, üst
  kenarı zemine karışır.
- MİA (2026 kurumsal) solda, OCEAN sağda — kendi renklerinde, plakasız;
  üst köşeler logoya doğru yavaşça beyazlar.
- KOCAELİ EV SAHİBİ OLUYOR! + kırmızı BANKA/FAİZ/KREDİ/ARA ÖDEME YOK
  çipleri + 1+0 ve 1+1 ödeme kartları + kırmızı 60 AY SABİT TAKSİT!
  burgu rozeti.
- Altta "Satış Ofisi: numara | web | sosyal ikonlar" tek satır.

    python3 scripts/build-sosyal-turkuaz.py
"""

import math
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "public", "images")
YAZI = os.path.join(ROOT, "sunum", "yazitipi")
OUT = os.path.join(ROOT, "sosyal-medya", "turkuaz-kampanya")
os.makedirs(OUT, exist_ok=True)

KIRMIZI = (200, 32, 42)
TURKUAZ = (0, 154, 168)
TURKUAZ_K = (0, 106, 118)
PETROL = (4, 66, 76)
BEYAZ = (255, 255, 255)
GRI = (66, 108, 116)
Z_UST, Z_ALT = (255, 255, 255), (224, 246, 248)

TEL = "0540 028 00 41"
SITE = "miaparkocean.com"


def mont(kes, boy):
    return ImageFont.truetype(os.path.join(YAZI, "Montserrat-%s.ttf" % kes), boy)


def sigdir(dr, t, kes, boy, maxw):
    f = mont(kes, boy)
    while boy > 10 and dr.textlength(t, font=f) > maxw:
        boy -= 1
        f = mont(kes, boy)
    return f


def foto(ad, w, h, focus=0.5, zoom=1.0, focus_y=None):
    im = Image.open(os.path.join(SRC, ad)).convert("RGB")
    iw, ih = im.size
    s = max(w / iw, h / ih) * max(1.0, zoom)
    sw, sh = w / s, h / s
    ox = (iw - sw) * focus
    oy = (ih - sh) * (focus if focus_y is None else focus_y)
    im = im.crop((int(ox), int(oy), int(ox + sw), int(oy + sh)))
    return im.resize((w, h), Image.LANCZOS)


def zemin(W, H):
    t = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    g = (np.array(Z_UST, np.float32) * (1 - t)
         + np.array(Z_ALT, np.float32) * t).astype(np.uint8)
    im = Image.new("RGBA", (W, H))
    im.paste(Image.fromarray(np.repeat(g, W, axis=1), "RGB"), (0, 0))
    return im


def grad_renk(H, y):
    t = y / H
    return tuple(int(u * (1 - t) + a * t) for u, a in zip(Z_UST, Z_ALT))


def foto_alt(im, yuk, focus=0.5, zoom=1.05, focus_y=0.45, bl=100):
    W, H = im.size
    ft = foto("entrance-gate.webp", W, yuk, focus, zoom, focus_y=focus_y)
    im.paste(ft, (0, H - yuk))
    band = np.asarray(ft.crop((0, 0, W, bl)), np.float32)
    alfa = np.linspace(1, 0, bl, dtype=np.float32)[:, None, None]
    zc = np.array(grad_renk(H, H - yuk), np.float32)
    kar = (zc * alfa + band * (1 - alfa)).astype(np.uint8)
    im.paste(Image.fromarray(kar, "RGB"), (0, H - yuk))


def kose(im, cx, cy, R):
    yy, xx = np.mgrid[0:2 * R, 0:2 * R].astype(np.float32)
    d = np.sqrt((xx - R) ** 2 + ((yy - R) * 1.25) ** 2)
    a = (np.clip(1 - d / R, 0, 1) ** 1.2 * 250).astype(np.uint8)
    kat = np.zeros((2 * R, 2 * R, 4), np.uint8)
    kat[..., :3] = 255
    kat[..., 3] = a
    im.alpha_composite(Image.fromarray(kat, "RGBA"), (int(cx - R), int(cy - R)))


def logolar(im, mia_w, oce_w, pad, y_mia, y_oce, R):
    W = im.width
    kose(im, pad + mia_w * 0.45, y_mia + mia_w * 0.25, R)
    kose(im, W - pad - oce_w * 0.45, y_oce + oce_w * 0.18, R)
    lg = Image.open(os.path.join(ROOT, "public", "brand",
                                 "logo-mia-2026.png")).convert("RGBA")
    lg = lg.resize((mia_w, int(lg.height * mia_w / lg.width)), Image.LANCZOS)
    im.alpha_composite(lg, (pad, y_mia))
    og = Image.open(os.path.join(ROOT, "sunum", "kaynak", "sekil",
                                 "ocean-logo-renkli2.png")).convert("RGBA")
    og = og.resize((oce_w, int(og.height * oce_w / og.width)), Image.LANCZOS)
    im.alpha_composite(og, (W - pad - oce_w, y_oce))


def cip(dr, cx, cy, t, f, dolgu=KIRMIZI, yazi=BEYAZ, pad_x=18, pad_y=9, r=10):
    tw = dr.textlength(t, font=f)
    h = f.size + 2 * pad_y
    dr.rounded_rectangle([cx - tw / 2 - pad_x, cy - h / 2,
                          cx + tw / 2 + pad_x, cy + h / 2], radius=r, fill=dolgu)
    dr.text((cx, cy - f.size * 0.06), t, font=f, fill=yazi, anchor="mm")


def yok_izgara(dr, cx, y, boy, satirda2=True):
    f = mont("ExtraBold", boy)
    ts = ["BANKA YOK", "FAİZ YOK", "KREDİ YOK", "ARA ÖDEME YOK"]
    if satirda2:
        gruplar = [ts[:2], ts[2:]]
    else:
        gruplar = [ts]
    adim = boy + 2 * 9 + 14
    for i, grup in enumerate(gruplar):
        gs = [dr.textlength(t, font=f) + 36 for t in grup]
        ara = 16
        x = cx - (sum(gs) + (len(grup) - 1) * ara) / 2
        for t, g in zip(grup, gs):
            cip(dr, x + g / 2, y + i * adim, t, f)
            x += g + ara


def kartlar(dr, cx, y, kw, kh, gap, boy):
    veriler = [("1+0", "699.000 TL", "29.900 TL"),
               ("1+1", "999.000 TL", "39.900 TL")]
    for i, (tip, pesin, taksit) in enumerate(veriler):
        bx = cx + (i - 0.5) * (kw + gap)
        dr.rounded_rectangle([bx - kw / 2, y, bx + kw / 2, y + kh],
                             radius=16, fill=(255, 255, 255, 255),
                             outline=TURKUAZ_K + (255,), width=3)
        cip(dr, bx, y, tip, mont("ExtraBold", int(boy * 0.62)), dolgu=TURKUAZ,
            pad_x=14, pad_y=5, r=8)
        dr.text((bx, y + kh * 0.34), pesin, font=mont("ExtraBold", boy),
                fill=PETROL, anchor="mm")
        dr.text((bx, y + kh * 0.53), "peşinat", font=mont("SemiBold", int(boy * 0.55)),
                fill=GRI, anchor="mm")
        cip(dr, bx, y + kh * 0.76, taksit + " TAKSİT",
            mont("ExtraBold", int(boy * 0.62)), dolgu=TURKUAZ_K, pad_x=14,
            pad_y=7, r=9)


def yildiz(im, cx, cy, r, don=10):
    kat = Image.new("RGBA", (r * 3, r * 3), (0, 0, 0, 0))
    kd = ImageDraw.Draw(kat)
    c = r * 1.5
    pts = []
    for i in range(52):
        rr = r if i % 2 == 0 else r * 0.84
        a = math.pi * i / 26
        pts.append((c + rr * math.cos(a), c + rr * math.sin(a)))
    kd.polygon(pts, fill=KIRMIZI + (255,))
    fb = mont("ExtraBold", int(r * 0.28))
    for i, t in enumerate(["60 AY", "SABİT", "TAKSİT!"]):
        kd.text((c, c - r * 0.38 + i * r * 0.38), t, font=fb, fill=BEYAZ,
                anchor="mm")
    kat = kat.rotate(don, resample=Image.BICUBIC, expand=False)
    im.alpha_composite(kat, (int(cx - c), int(cy - c)))


def iletisim(dr, W, cy, maxw, acik=False):
    """Satış Ofisi: numara | web | [ig][f] miaparkocean — ortalı."""
    boy = 40
    while boy > 14:
        fe, f = mont("SemiBold", boy), mont("Bold", boy)
        ik = int(boy * 1.05)
        bosluk = int(boy * 1.1)
        w_l = dr.textlength("Satış Ofisi:", font=fe)
        w_t = dr.textlength(TEL, font=f)
        w_s = dr.textlength(SITE, font=f)
        w_h = dr.textlength("miaparkocean", font=f)
        w_sos = ik * 2 + int(boy * 0.5) + int(boy * 0.55) + w_h
        toplam = (w_l + boy * 0.8 + w_t + (bosluk * 2 + 2) * 2 + w_s + w_sos)
        if toplam <= maxw:
            break
        boy -= 1
    kal = max(2, int(boy * 0.09))
    x = W / 2 - toplam / 2
    r1 = (46, 96, 106) if acik else (214, 234, 238)
    r2 = PETROL if acik else BEYAZ
    r3 = (110, 150, 160) if acik else (200, 222, 228)
    dr.text((x, cy), "Satış Ofisi:", font=fe, fill=r1, anchor="lm")
    x += w_l + boy * 0.8
    dr.text((x, cy), TEL, font=f, fill=r2, anchor="lm")
    x += w_t + bosluk
    dr.line([(x, cy - boy * 0.62), (x, cy + boy * 0.62)],
            fill=r3, width=2)
    x += 2 + bosluk
    dr.text((x, cy), SITE, font=f, fill=r2, anchor="lm")
    x += w_s + bosluk
    dr.line([(x, cy - boy * 0.62), (x, cy + boy * 0.62)],
            fill=r3, width=2)
    x += 2 + bosluk
    dr.rounded_rectangle([x, cy - ik / 2, x + ik, cy + ik / 2],
                         radius=int(ik * 0.24), outline=r2, width=kal)
    dr.ellipse([x + ik * 0.26, cy - ik * 0.24, x + ik * 0.74, cy + ik * 0.24],
               outline=r2, width=kal)
    dr.ellipse([x + ik * 0.70, cy - ik * 0.40, x + ik * 0.87, cy - ik * 0.23],
               fill=r2)
    x += ik + int(boy * 0.5)
    dr.rounded_rectangle([x, cy - ik / 2, x + ik, cy + ik / 2],
                         radius=int(ik * 0.24), outline=r2, width=kal)
    dr.text((x + ik * 0.55, cy + 1), "f", font=mont("Bold", int(ik * 0.8)),
            fill=r2, anchor="mm")
    x += ik + int(boy * 0.55)
    dr.text((x, cy), "miaparkocean", font=f, fill=r2, anchor="lm")


def kaydet(im, ad):
    p = os.path.join(OUT, ad + ".jpg")
    im.convert("RGB").save(p, quality=92, optimize=True)
    print("   %s  %dx%d" % (ad, im.width, im.height))


def s45():
    W, H = 1080, 1350
    im = zemin(W, H)
    foto_alt(im, 500, 0.5, 1.05, 0.45)
    logolar(im, 260, 235, 44, 28, 46, 600)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 306), "KOCAELİ", font=mont("Black", 96), fill=PETROL,
            anchor="mm")
    dr.text((W / 2, 398), "EV SAHİBİ OLUYOR!",
            font=sigdir(dr, "EV SAHİBİ OLUYOR!", "Black", 62, W - 100),
            fill=PETROL, anchor="mm")
    yok_izgara(dr, W / 2, 486, 30)
    kartlar(dr, W / 2, 592, 470, 226, 26, 46)
    yildiz(im, W - 172, 940, 112)
    dr = ImageDraw.Draw(im)
    iletisim(dr, W, H - 44, W - 70)
    kaydet(im, "sosyal-turkuaz-45")


def skare():
    W, H = 1080, 1080
    im = zemin(W, H)
    foto_alt(im, 385, 0.5, 1.05, 0.45, bl=80)
    logolar(im, 240, 220, 40, 24, 40, 560)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 262), "KOCAELİ", font=mont("Black", 84), fill=PETROL,
            anchor="mm")
    dr.text((W / 2, 344), "EV SAHİBİ OLUYOR!",
            font=sigdir(dr, "EV SAHİBİ OLUYOR!", "Black", 54, W - 100),
            fill=PETROL, anchor="mm")
    yok_izgara(dr, W / 2, 422, 27)
    kartlar(dr, W / 2, 516, 452, 210, 24, 43)
    yildiz(im, W - 155, 845, 98)
    dr = ImageDraw.Draw(im)
    iletisim(dr, W, H - 40, W - 64)
    kaydet(im, "sosyal-turkuaz-kare")


def sstory():
    W, H = 1080, 1920
    im = zemin(W, H)
    foto_alt(im, 760, 0.5, 1.05, 0.45, bl=130)
    logolar(im, 300, 265, 50, 40, 66, 660)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 430), "KOCAELİ", font=mont("Black", 128), fill=PETROL,
            anchor="mm")
    dr.text((W / 2, 548), "EV SAHİBİ OLUYOR!",
            font=sigdir(dr, "EV SAHİBİ OLUYOR!", "Black", 72, W - 90),
            fill=PETROL, anchor="mm")
    yok_izgara(dr, W / 2, 656, 32)
    kartlar(dr, W / 2, 790, 480, 250, 28, 48)
    yildiz(im, W - 180, 1290, 122)
    dr = ImageDraw.Draw(im)
    iletisim(dr, W, H - 52, W - 80)
    kaydet(im, "sosyal-turkuaz-story")


def kontak():
    ths = []
    for ad in ["sosyal-turkuaz-45", "sosyal-turkuaz-kare", "sosyal-turkuaz-story"]:
        im = Image.open(os.path.join(OUT, ad + ".jpg"))
        im.thumbnail((520, 640), Image.LANCZOS)
        ths.append(im)
    hh = max(t.height for t in ths) + 24
    sheet = Image.new("RGB", (sum(t.width for t in ths) + 48, hh), (16, 20, 26))
    x = 12
    for t in ths:
        sheet.paste(t, (x, 12))
        x += t.width + 12
    sheet.save(os.path.join(OUT, "kontak-sosyal-turkuaz.jpg"), quality=88)
    print("   kontak-sosyal-turkuaz.jpg")


if __name__ == "__main__":
    s45()
    skare()
    sstory()
    kontak()
    print("tamam ->", OUT)
