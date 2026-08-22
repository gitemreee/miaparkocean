#!/usr/bin/env python3
"""
MİA PARK OCEAN — v5 kampanya dilinde TEK PARÇA bilbord (10 tasarım).

3 x 5 metre tek pano: mesaj, fiyat çipleri, yıldız rozet, foto şeridi ve
telefon aynı panoda. İkili setin (build-bilbord-v5.py) kardeşi — aynı
Meta/Facebook v5 reklam dili:

    üst: dikey gradyan zemin, solda MİA + sağda OCEAN logosu (pedsiz PNG)
    orta: dev manşet + fosforlu sarı çipler
    alt: dış cephe FOTO ŞERİDİ — kartsız, üst kenarı zemine karışır;
         kırmızı yıldız rozet foto üzerine biner, telefon çipi altta

Görseller GÜNDÜZ: giriş kapısı ve pergola terası, tasarım başına farklı
kadraj. Kurallar (işveren): dipnot/koop adı/"temsilidir" YOK, "%30" ve
"peşinatsız" geçmez, bina üzerine yazı binmez, onaylı örnek fiyatlar
(1+0: 699.000 / 29.900 · 1+1: 999.000 / 39.900).

ÖLÇÜ: 5000 x 3000 mm, 1:1 ölçekte 40 dpi = 7874 x 4724 px (dpi gömülü).
Manşetler 320-570 mm, telefon 190 mm — 30-100 m'den okunur.

    python3 scripts/build-bilbord-tek.py
"""

import math
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "public", "images")
YAZI = os.path.join(ROOT, "sunum", "yazitipi")
OUT = os.path.join(ROOT, "tabela", "bilbord-tek")
ONIZ = os.path.join(OUT, "onizleme")
os.makedirs(OUT, exist_ok=True)
os.makedirs(ONIZ, exist_ok=True)

W, H, DPI = 7874, 4724, 40           # 5000 x 3000 mm @ 40 dpi
PAD = 340

NAVY = (10, 42, 74)
SARI = (255, 209, 74)
KIRMIZI = (200, 32, 42)
MAVI_U = (12, 102, 150)
MAVI_A = (26, 146, 198)
YESIL_U = (8, 92, 70)
YESIL_A = (24, 146, 112)
BEYAZ = (255, 255, 255)

TEL = "0540 028 00 41"
SITE = "miaparkocean.com"


def mont(kes, boy):
    return ImageFont.truetype(os.path.join(YAZI, "Montserrat-%s.ttf" % kes), boy)


def sigdir(dr, t, kes, boy, maxw):
    f = mont(kes, boy)
    while boy > 60 and dr.textlength(t, font=f) > maxw:
        boy = int(boy * 0.96)
        f = mont(kes, boy)
    return f


def foto(ad, w, h, focus=0.5, zoom=1.0, focus_y=None):
    """Kapak kırpımı — önce kaynakta kırpar, sonra hedefe büyütür."""
    im = Image.open(os.path.join(SRC, ad)).convert("RGB")
    iw, ih = im.size
    s = max(w / iw, h / ih) * max(1.0, zoom)
    sw, sh = w / s, h / s
    ox = (iw - sw) * focus
    oy = (ih - sh) * (focus if focus_y is None else focus_y)
    im = im.crop((int(ox), int(oy), int(ox + sw), int(oy + sh)))
    im = im.resize((w, h), Image.LANCZOS)
    if s > 1.6:
        im = im.filter(ImageFilter.UnsharpMask(radius=3, percent=52, threshold=3))
    return im


def grad_zemin(ust, alt):
    t = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    g = (np.array(ust, np.float32) * (1 - t)
         + np.array(alt, np.float32) * t).astype(np.uint8)
    im = Image.new("RGBA", (W, H))
    im.paste(Image.fromarray(np.repeat(g, W, axis=1), "RGB"), (0, 0))
    return im


def grad_renk(ust, alt, y):
    t = y / H
    return tuple(int(u * (1 - t) + a * t) for u, a in zip(ust, alt))


def foto_alt(im, ad, yuk, zemin, focus=0.5, zoom=1.0, focus_y=None, bl=300):
    """Kartsız foto şeridi: alta tam genişlik, üst kenar zemine karışır."""
    ft = foto(ad, W, yuk, focus, zoom, focus_y=focus_y)
    im.paste(ft, (0, H - yuk))
    band = np.asarray(ft.crop((0, 0, W, bl)), np.float32)
    alfa = np.linspace(1, 0, bl, dtype=np.float32)[:, None, None]
    kar = (np.array(zemin, np.float32) * alfa + band * (1 - alfa)).astype(np.uint8)
    im.paste(Image.fromarray(kar, "RGB"), (0, H - yuk))


def ust_logolar(im, koyu):
    """Solda MİA, sağda Ocean Gayrimenkul — pedsiz şeffaf PNG."""
    mia = os.path.join(ROOT, "public", "brand",
                       "logo-ocean-white.png" if koyu else "logo-ocean-trim.png")
    oce = (os.path.join(ROOT, "public", "ocean-logo-white.png") if koyu
           else os.path.join(ROOT, "sunum", "kaynak", "sekil", "ocean-logo-renkli.png"))
    lg = Image.open(mia).convert("RGBA")
    lg = lg.resize((950, int(lg.height * 950 / lg.width)), Image.LANCZOS)
    im.alpha_composite(lg, (PAD, 140))
    og = Image.open(oce).convert("RGBA")
    og = og.resize((950, int(og.height * 950 / og.width)), Image.LANCZOS)
    im.alpha_composite(og, (W - PAD - 950, 250))


def cip(dr, cx, cy, t, f, dolgu=SARI, yazi=NAVY, pad_x=140, pad_y=70, radius=70):
    tw = dr.textlength(t, font=f)
    h = f.size + 2 * pad_y
    dr.rounded_rectangle([cx - tw / 2 - pad_x, cy - h / 2,
                          cx + tw / 2 + pad_x, cy + h / 2], radius=radius, fill=dolgu)
    dr.text((cx, cy - f.size * 0.06), t, font=f, fill=yazi, anchor="mm")


def cip_sol(dr, x, cy, t, f, dolgu=SARI, yazi=NAVY, pad_x=120, pad_y=60, radius=60):
    tw = dr.textlength(t, font=f)
    h = f.size + 2 * pad_y
    dr.rounded_rectangle([x, cy - h / 2, x + tw + 2 * pad_x, cy + h / 2],
                         radius=radius, fill=dolgu)
    dr.text((x + pad_x + tw / 2, cy - f.size * 0.06), t, font=f, fill=yazi, anchor="mm")
    return x + tw + 2 * pad_x


def fiyat_satiri(dr, cx, cy, parcalar, boy=300):
    """[sarı çipte rakam] açıklama · [çip] açıklama — tek satır, ortalı."""
    f1, f2 = mont("ExtraBold", boy), mont("ExtraBold", int(boy * 0.85))
    genlik = []
    for buyuk, kucuk in parcalar:
        genlik.append(dr.textlength(buyuk, font=f1) + 240 + 150
                      + dr.textlength(kucuk, font=f2))
    x = cx - (sum(genlik) + (len(parcalar) - 1) * 420) / 2
    for (buyuk, kucuk), g in zip(parcalar, genlik):
        x2 = cip_sol(dr, x, cy, buyuk, f1)
        dr.text((x2 + 150, cy - 18), kucuk, font=f2, fill=BEYAZ, anchor="lm")
        x += g + 420
    return x


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
    fb = mont("ExtraBold", int(r * (0.28 if len(satirlar) > 1 else 0.34)))
    y0 = c - (len(satirlar) - 1) * r * 0.19
    for i, t in enumerate(satirlar):
        kd.text((c, y0 + i * r * 0.38), t, font=fb, fill=yazi, anchor="mm")
    kat = kat.rotate(don, resample=Image.BICUBIC, expand=False)
    im.alpha_composite(kat, (int(cx - c), int(cy - c)))


def tel_cip(dr, cy, dolgu=NAVY, yazi=BEYAZ, site=True, boy=300, cx=None):
    cx = W / 2 if cx is None else cx
    t = TEL + ("   ·   " + SITE if site else "")
    f = mont("Bold", boy)
    gen = dr.textlength(t, font=f) + 480
    dr.rounded_rectangle([cx - gen / 2, cy - boy * 0.85, cx + gen / 2, cy + boy * 0.85],
                         radius=boy * 0.85, fill=dolgu)
    dr.text((cx, cy - boy * 0.05), t, font=f, fill=yazi, anchor="mm")


def kaydet(ad, im):
    im = im.convert("RGB")
    p = os.path.join(OUT, ad + ".jpg")
    im.save(p, "JPEG", quality=90, optimize=True, dpi=(DPI, DPI))
    kucuk = im.copy()
    kucuk.thumbnail((1400, 1400), Image.LANCZOS)
    kucuk.save(os.path.join(ONIZ, ad + ".jpg"), quality=86, optimize=True)
    print("   %s  %.1f MB" % (ad, os.path.getsize(p) / 1e6))


# ═══════════════════════════════════════════════════════════ 10 TASARIM
def t01():
    """İZMİT EV SAHİBİ OLUYOR — gök zemin (meta k01)."""
    G_U, G_A = (88, 118, 132), (150, 202, 226)
    im = grad_zemin(G_U, G_A)
    ust_logolar(im, koyu=True)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 1080), "İZMİT", font=mont("Black", 660), fill=BEYAZ, anchor="mm")
    f = sigdir(dr, "EV SAHİBİ OLUYOR", "Black", 430, W - 2 * PAD)
    dr.text((W / 2, 1720), "EV SAHİBİ OLUYOR", font=f, fill=BEYAZ, anchor="mm")
    fiyat_satiri(dr, W / 2 - 500, 2150, [("699.000 TL", "PEŞİNATLA")], 290)
    fiyat_satiri(dr, W / 2 - 500, 2620, [("29.900 TL", "TAKSİTLE KAVUŞUN!")], 290)
    foto_alt(im, "entrance-gate.webp", 2080, grad_renk(G_U, G_A, H - 2080),
             0.5, 1.1, focus_y=0.48)
    yildiz(im, W - 1350, 2850, 820, ["ÜSTELİK", "FAİZSİZ!"])
    dr = ImageDraw.Draw(im)
    tel_cip(dr, H - 400)
    kaydet("bilbord-tek-01-izmit", im)


def t02():
    """YOK duvarı — açık zemin (meta k05)."""
    A_U, A_A = (240, 246, 251), (252, 253, 255)
    im = grad_zemin(A_U, A_A)
    ust_logolar(im, koyu=False)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 1060), "EV SAHİBİ OLMAK İÇİN", font=mont("ExtraBold", 300),
            fill=NAVY, anchor="mm")
    f1 = mont("Black", 300)
    grup, ara = [], 380
    for a in ["BANKA", "FAİZ", "KEFİL"]:
        aw = dr.textlength(a + " ", font=f1)
        bw = dr.textlength("YOK", font=f1) + 200
        grup.append((a, aw, bw))
    top = sum(aw + 60 + bw for _, aw, bw in grup) + ara * 2
    x = (W - top) / 2
    for a, aw, bw in grup:
        dr.text((x, 1640), a, font=f1, fill=NAVY, anchor="lm")
        cip(dr, x + aw + 60 + bw / 2, 1640, "YOK", f1, pad_x=100, pad_y=34)
        x += aw + 60 + bw + ara
    cip(dr, W / 2, 2250, "60 AY SABİT TAKSİT", mont("ExtraBold", 330),
        dolgu=NAVY, yazi=BEYAZ, pad_x=200, pad_y=110)
    foto_alt(im, "entrance-gate.webp", 2020, grad_renk(A_U, A_A, H - 2020),
             0.42, 1.0, focus_y=0.40, bl=260)
    yildiz(im, W - 1350, 2900, 820, ["KOMİSYON", "YOK!"], don=10)
    dr = ImageDraw.Draw(im)
    tel_cip(dr, H - 400)
    kaydet("bilbord-tek-02-yok-duvari", im)


def t03():
    """%0 — canlı yeşil gradyan (meta k06)."""
    G_U, G_A = (20, 138, 104), (8, 86, 66)
    im = grad_zemin(G_U, G_A)
    ust_logolar(im, koyu=True)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 1230), "%0", font=mont("Black", 1150), fill=SARI, anchor="mm")
    dr.text((W / 2, 2080), "FAİZ · VADE FARKI · KOMİSYON", font=mont("ExtraBold", 290),
            fill=BEYAZ, anchor="mm")
    cip(dr, W / 2, 2500, "İZMİT MİA BÖLGESİ", mont("ExtraBold", 260),
        dolgu=SARI, yazi=YESIL_U, pad_x=170, pad_y=85)
    foto_alt(im, "entrance-gate.webp", 2000, grad_renk(G_U, G_A, H - 2000),
             0.55, 1.2, focus_y=0.45)
    dr = ImageDraw.Draw(im)
    tel_cip(dr, H - 400, dolgu=BEYAZ, yazi=YESIL_U)
    kaydet("bilbord-tek-03-sifir", im)


def t04():
    """60 AY — krem zemin (meta k07)."""
    A_U, A_A = (253, 251, 249), (244, 238, 232)
    im = grad_zemin(A_U, A_A)
    ust_logolar(im, koyu=False)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 1230), "60 AY", font=mont("Black", 950), fill=KIRMIZI, anchor="mm")
    cip(dr, W / 2, 2060, "VADE FARKSIZ · SABİT TAKSİT", mont("ExtraBold", 290),
        pad_x=200, pad_y=110)
    dr.text((W / 2, 2520), "Banka yok · Faiz yok · Kefil yok · Komisyon yok",
            font=mont("SemiBold", 230), fill=(96, 74, 70), anchor="mm")
    foto_alt(im, "terrace-pergola.webp", 1980, grad_renk(A_U, A_A, H - 1980),
             0.5, 1.0, focus_y=0.40, bl=260)
    dr = ImageDraw.Draw(im)
    tel_cip(dr, H - 400, dolgu=KIRMIZI, site=False)
    kaydet("bilbord-tek-04-60ay", im)


def t05():
    """Aylık 29.900 — canlı okyanus mavisi (meta k04)."""
    im = grad_zemin(MAVI_U, MAVI_A)
    ust_logolar(im, koyu=True)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 1000), "İzmit MİA'da", font=mont("SemiBold", 270),
            fill=(206, 234, 248), anchor="mm")
    f = sigdir(dr, "Aylık 29.900 TL'ye ev sahibi olun.", "ExtraBold", 400,
               W - 2 * PAD)
    dr.text((W / 2, 1560), "Aylık 29.900 TL'ye ev sahibi olun.", font=f,
            fill=BEYAZ, anchor="mm")
    dr.text((W / 2 - 300, 2160), "Üstelik 60 aya varan vade ve 0 faizle!",
            font=mont("SemiBold", 235), fill=(206, 234, 248), anchor="mm")
    foto_alt(im, "entrance-gate.webp", 2150, grad_renk(MAVI_U, MAVI_A, H - 2150),
             0.65, 1.25, focus_y=0.35)
    yildiz(im, W - 1350, 2950, 820, ["FAİZ", "YOK!"], don=10)
    dr = ImageDraw.Draw(im)
    tel_cip(dr, H - 400, dolgu=BEYAZ, yazi=MAVI_U)
    kaydet("bilbord-tek-05-aylik", im)


def t06():
    """KOCAELİ DENİZE YAKIN — gök (meta k08)."""
    G_U, G_A = (96, 138, 158), (168, 210, 230)
    im = grad_zemin(G_U, G_A)
    ust_logolar(im, koyu=True)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 1060), "KOCAELİ", font=mont("Black", 620), fill=BEYAZ, anchor="mm")
    f = sigdir(dr, "DENİZE YAKIN EV SAHİBİ OLUYOR", "Black", 300, W - 2 * PAD)
    dr.text((W / 2, 1650), "DENİZE YAKIN EV SAHİBİ OLUYOR", font=f, fill=BEYAZ,
            anchor="mm")
    fiyat_satiri(dr, W / 2 - 500, 2160, [("999.000 TL", "PEŞİNATLA 1+1")], 280)
    fiyat_satiri(dr, W / 2 - 500, 2620, [("39.900 TL", "TAKSİTLE!")], 280)
    foto_alt(im, "entrance-gate.webp", 2150, grad_renk(G_U, G_A, H - 2150),
             0.5, 1.0, focus_y=0.25)
    yildiz(im, W - 1350, 2800, 820, ["BANKA", "YOK!"])
    dr = ImageDraw.Draw(im)
    tel_cip(dr, H - 400)
    kaydet("bilbord-tek-06-kocaeli", im)


def t07():
    """EV SAHİBİ OLMA ZAMANI — lacivert gradyan (meta k10)."""
    G_U, G_A = (12, 48, 92), (26, 80, 132)
    im = grad_zemin(G_U, G_A)
    ust_logolar(im, koyu=True)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 1000), "29.900 TL taksitle", font=mont("SemiBold", 280),
            fill=(150, 205, 228), anchor="mm")
    dr.text((W / 2, 1540), "EV SAHİBİ", font=mont("Black", 560), fill=BEYAZ,
            anchor="mm")
    cip(dr, W / 2, 2170, "OLMA ZAMANI", mont("Black", 450), pad_x=200, pad_y=60)
    foto_alt(im, "terrace-pergola.webp", 2050, grad_renk(G_U, G_A, H - 2050),
             0.68, 1.25, focus_y=0.45, bl=360)
    yildiz(im, W - 1350, 2850, 800, ["60 AY", "VADE", "FARKSIZ"], don=12)
    dr = ImageDraw.Draw(im)
    tel_cip(dr, H - 400, dolgu=SARI, yazi=NAVY)
    kaydet("bilbord-tek-07-olma-zamani", im)


def t08():
    """1+0 stüdyo yatırım — canlı yeşil (meta k02)."""
    im = grad_zemin(YESIL_U, YESIL_A)
    ust_logolar(im, koyu=True)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 1010), "1+0 stüdyo dairelerde", font=mont("SemiBold", 270),
            fill=(206, 236, 224), anchor="mm")
    f = sigdir(dr, "avantajlı yatırım fırsatı", "ExtraBold", 400, W - 2 * PAD)
    dr.text((W / 2, 1540), "avantajlı yatırım fırsatı", font=f, fill=BEYAZ,
            anchor="mm")
    f1, fk = mont("ExtraBold", 280), mont("SemiBold", 190)
    for i, (buyuk, kucuk) in enumerate([("699.000 TL", "peşinat"),
                                        ("29.900 TL", "taksit")]):
        cx = W / 2 - 1560 + i * 3120
        dr.rounded_rectangle([cx - 1380, 1960, cx + 1380, 2760], radius=100,
                             outline=BEYAZ, width=18)
        dr.text((cx, 2260), buyuk, font=f1, fill=SARI, anchor="mm")
        dr.text((cx, 2580), kucuk, font=fk, fill=BEYAZ, anchor="mm")
    foto_alt(im, "terrace-pergola.webp", 1830, grad_renk(YESIL_U, YESIL_A, H - 1830),
             0.32, 1.2, focus_y=0.50)
    dr = ImageDraw.Draw(im)
    tel_cip(dr, H - 400, dolgu=BEYAZ, yazi=YESIL_U)
    kaydet("bilbord-tek-08-studyo", im)


def t09():
    """Tasarrufa dayalı finansman — açık gök (meta k09)."""
    G_U, G_A = (140, 198, 224), (225, 242, 250)
    im = grad_zemin(G_U, G_A)
    ust_logolar(im, koyu=False)
    dr = ImageDraw.Draw(im)
    dr.rounded_rectangle([W / 2 - 2900, 940, W / 2 + 2900, 2100], radius=170,
                         fill=NAVY)
    dr.text((W / 2, 1330), "Tasarrufa dayalı finansmanla", font=mont("SemiBold", 240),
            fill=(150, 205, 228), anchor="mm")
    dr.text((W / 2, 1760), "EV SAHİBİ OL!", font=mont("Black", 400), fill=BEYAZ,
            anchor="mm")
    y = 2420
    f = mont("ExtraBold", 230)
    genlik = [dr.textlength(t, font=f) + 340 for t in
              ["BANKA YOK", "FAİZ YOK", "60 AY SABİT TAKSİT"]]
    x = (W - sum(genlik) - 2 * 300) / 2
    for t, g in zip(["BANKA YOK", "FAİZ YOK", "60 AY SABİT TAKSİT"], genlik):
        cip(dr, x + g / 2, y, t, f, pad_x=170, pad_y=80)
        x += g + 300
    foto_alt(im, "terrace-pergola.webp", 1900, grad_renk(G_U, G_A, H - 1900),
             0.5, 1.1, focus_y=0.28, bl=340)
    dr = ImageDraw.Draw(im)
    tel_cip(dr, H - 400)
    kaydet("bilbord-tek-09-tasarruf", im)


def t10():
    """SATIŞ OFİSİMİZE BEKLERİZ — okyanus mavisi (meta k03)."""
    im = grad_zemin(MAVI_A, MAVI_U)
    ust_logolar(im, koyu=True)
    dr = ImageDraw.Draw(im)
    f = sigdir(dr, "60 AY VADEYLE EV SAHİBİ OLMAK İÇİN", "Black", 330, W - 2 * PAD)
    dr.text((W / 2, 1060), "60 AY VADEYLE EV SAHİBİ OLMAK İÇİN", font=f,
            fill=BEYAZ, anchor="mm")
    cip(dr, W / 2, 1620, "SATIŞ OFİSİMİZE BEKLERİZ", mont("ExtraBold", 280),
        pad_x=220, pad_y=110)
    fs1, fs2 = mont("ExtraBold", 235), mont("SemiBold", 170)
    for i, (a, b) in enumerate([("699.000 TL'den", "başlayan peşinat"),
                                ("%0", "faiz"), ("29.900 TL", "taksit")]):
        cx = W / 2 + (i - 1) * 2360
        dr.rounded_rectangle([cx - 1090, 2050, cx + 1090, 2820], radius=100,
                             outline=BEYAZ, width=16)
        dr.text((cx, 2340), a, font=fs1, fill=SARI, anchor="mm")
        dr.text((cx, 2650), b, font=fs2, fill=BEYAZ, anchor="mm")
    foto_alt(im, "entrance-gate.webp", 1780, grad_renk(MAVI_A, MAVI_U, H - 1780),
             0.4, 1.05, focus_y=0.55)
    dr = ImageDraw.Draw(im)
    tel_cip(dr, H - 380, dolgu=BEYAZ, yazi=MAVI_U)
    kaydet("bilbord-tek-10-satis-ofisi", im)


def kontak():
    fs = sorted(f for f in os.listdir(ONIZ)
                if f.startswith("bilbord-tek-") and f.endswith(".jpg"))
    tw = 680
    th = int(tw * H / W)
    ara = 20
    cols, rows = 2, 5
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * ara,
                              rows * th + (rows + 1) * ara), (16, 20, 26))
    for i, f in enumerate(fs[:10]):
        im = Image.open(os.path.join(ONIZ, f)).resize((tw, th), Image.LANCZOS)
        sheet.paste(im, (ara + (i % cols) * (tw + ara),
                         ara + (i // cols) * (th + ara)))
    sheet.save(os.path.join(OUT, "kontak-bilbord-tek.jpg"), quality=88)
    print("   kontak-bilbord-tek.jpg")


if __name__ == "__main__":
    for t in [t01, t02, t03, t04, t05, t06, t07, t08, t09, t10]:
        t()
    kontak()
    print("tamam ->", OUT)
