#!/usr/bin/env python3
"""
MİA PARK OCEAN — Meta v5 reklam dilinde İKİLİ bilbord seti (10 çift = 20 pano).

Bilbordlar YAN YANA İKİ PANO olarak kiralanıyor. Her çift, Facebook/Meta
v5 kreatifinin İKİYE BÖLÜNMÜŞ hâli — tek reklam gibi okunur:

    ┌───────────────┬───────────────┐
    │ SOL: manşet   │ SAĞ: çipler,  │   üst: aynı dikey gradyan zemin
    │ + alt satır   │ yıldız, tel   │   (çift boyunca kesintisiz)
    ├───────────────┴───────────────┤
    │ dış cephe FOTO ŞERİDİ — kartsız, iki panoda devam eder,        │
    │ üst kenarı zemine yumuşak karışır (meta foto_alt dili)         │
    └───────────────────────────────┘

Yazılar HİÇBİR ZAMAN iki panoya bölünmez (arada çerçeve boşluğu var);
fotoğraf şeridi bölünebilir — asıldığında tek görüntünün devamı gibi
okunur. Logolar çift düzeyinde: MİA sol panonun soluna, OCEAN
GAYRİMENKUL sağ panonun sağına.

Meta v5 kuralları burada da geçerli (işveren):
- "Görseller temsilidir", kooperatif adı ve dönemsellik dipnotu YOK.
- Fotoğraflar yalnız dış cephe; bina üzerine yazı binmez (yazılar
  gradyan zeminde, telefon çipi fotonun yol/peyzaj bandında).
- Zeminler dikey gradyan; kırmızı yalnız yıldız rozetlerde ve 60 AY
  vurgusunda. Sarı fosforlu çipler rakamlar için.
- "Peşinatsız" ve "%30" oranı geçmez; onaylı örnek fiyatlar:
  1+0: 699.000 / 29.900 · 1+1: 999.000 / 39.900.

ÖLÇÜ: pano başına 5000 x 3000 mm, 1:1 ölçekte 40 dpi = 7874 x 4724 px
(mevcut ikili setle aynı; tabela/OLCULER.md). Manşetler 500-900 px
(320-570 mm), telefon 300 px (190 mm) — 30-100 m'den okunur.

    python3 scripts/build-bilbord-v5.py
"""

import math
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "public", "images")
YAZI = os.path.join(ROOT, "sunum", "yazitipi")
OUT = os.path.join(ROOT, "tabela", "bilbord-v5")
ONIZ = os.path.join(OUT, "onizleme")
os.makedirs(OUT, exist_ok=True)
os.makedirs(ONIZ, exist_ok=True)

W, H, DPI = 7874, 4724, 40           # pano: 5000 x 3000 mm @ 40 dpi
P = W * 2                            # çift kanvası (iki pano yan yana)
PAD = 340
CS = W / 2                           # sol panonun merkezi
CD = W * 1.5                         # sağ panonun merkezi

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
    """Metni verilen genişliğe sığana kadar küçültülmüş font döndürür."""
    f = mont(kes, boy)
    while boy > 60 and dr.textlength(t, font=f) > maxw:
        boy = int(boy * 0.96)
        f = mont(kes, boy)
    return f


def foto(ad, w, h, focus=0.5, zoom=1.0, focus_y=None):
    """Kapak kırpımı — önce kaynakta kırpar, sonra hedefe büyütür
    (15748 px'lik şeritlerde belleği ve süreyi düşük tutar)."""
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
    """Çift boyunca kesintisiz dikey gradyan."""
    t = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    g = (np.array(ust, np.float32) * (1 - t)
         + np.array(alt, np.float32) * t).astype(np.uint8)
    im = Image.new("RGBA", (P, H))
    im.paste(Image.fromarray(np.repeat(g, P, axis=1), "RGB"), (0, 0))
    return im


def grad_renk(ust, alt, y):
    t = y / H
    return tuple(int(u * (1 - t) + a * t) for u, a in zip(ust, alt))


def foto_alt(im, ad, yuk, zemin, focus=0.5, zoom=1.0, focus_y=None, bl=300):
    """Meta v5 foto dili: kartsız-çerçevesiz şerit, çiftin tamamına
    yayılır, üst kenarı zeminin o satırdaki rengine yumuşak karışır."""
    ft = foto(ad, P, yuk, focus, zoom, focus_y=focus_y)
    im.paste(ft, (0, H - yuk))
    band = np.asarray(ft.crop((0, 0, P, bl)), np.float32)
    alfa = np.linspace(1, 0, bl, dtype=np.float32)[:, None, None]
    kar = (np.array(zemin, np.float32) * alfa + band * (1 - alfa)).astype(np.uint8)
    im.paste(Image.fromarray(kar, "RGB"), (0, H - yuk))


def ust_logolar(im, koyu):
    """Çift düzeyinde: MİA sol panonun soluna, Ocean sağ panonun sağına."""
    mia = os.path.join(ROOT, "public", "brand",
                       "logo-ocean-white.png" if koyu else "logo-ocean-trim.png")
    oce = (os.path.join(ROOT, "public", "ocean-logo-white.png") if koyu
           else os.path.join(ROOT, "sunum", "kaynak", "sekil", "ocean-logo-renkli.png"))
    lg = Image.open(mia).convert("RGBA")
    lg = lg.resize((950, int(lg.height * 950 / lg.width)), Image.LANCZOS)   # h≈650
    im.alpha_composite(lg, (PAD, 140))
    og = Image.open(oce).convert("RGBA")
    og = og.resize((950, int(og.height * 950 / og.width)), Image.LANCZOS)   # h≈400
    im.alpha_composite(og, (P - PAD - 950, 250))


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


def fiyat_satiri(dr, cx, cy, buyuk, kucuk, boy=320, yazi=BEYAZ):
    """Meta'daki gibi: sarı çipte rakam + yanında açıklama."""
    f1, f2 = mont("ExtraBold", boy), mont("ExtraBold", int(boy * 0.87))
    top = dr.textlength(buyuk, font=f1) + 240 + 160 + dr.textlength(kucuk, font=f2)
    x = cx - top / 2
    x2 = cip_sol(dr, x, cy, buyuk, f1)
    dr.text((x2 + 160, cy - 20), kucuk, font=f2, fill=yazi, anchor="lm")


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


def tel_cip(dr, cx, cy, dolgu=NAVY, yazi=BEYAZ, site=True, boy=300):
    t = TEL + ("   ·   " + SITE if site else "")
    f = mont("Bold", boy)
    gen = dr.textlength(t, font=f) + 480
    dr.rounded_rectangle([cx - gen / 2, cy - boy * 0.85, cx + gen / 2, cy + boy * 0.85],
                         radius=boy * 0.85, fill=dolgu)
    dr.text((cx, cy - boy * 0.05), t, font=f, fill=yazi, anchor="mm")


def kaydet(cift, im):
    """Çift kanvasını SOL/SAĞ panolara böler ve kaydeder."""
    im = im.convert("RGB")
    for yon, x0 in [("SOL", 0), ("SAG", W)]:
        pano = im.crop((x0, 0, x0 + W, H))
        ad = "bilbord-v5-%s-%s" % (cift, yon)
        p = os.path.join(OUT, ad + ".jpg")
        pano.save(p, "JPEG", quality=90, optimize=True, dpi=(DPI, DPI))
        kucuk = pano.copy()
        kucuk.thumbnail((1400, 1400), Image.LANCZOS)
        kucuk.save(os.path.join(ONIZ, ad + ".jpg"), quality=86, optimize=True)
        print("   %s  %.1f MB" % (ad, os.path.getsize(p) / 1e6))


# ═══════════════════════════════════════════════════════════ 10 İKİLİ SET
def c01():
    """İZMİT EV SAHİBİ OLUYOR — gök zemin, sokak köşesi şeridi (meta k01)."""
    G_U, G_A = (88, 118, 132), (150, 202, 226)
    im = grad_zemin(G_U, G_A)
    ust_logolar(im, koyu=True)
    dr = ImageDraw.Draw(im)
    dr.text((CS, 1180), "İZMİT", font=mont("Black", 780), fill=BEYAZ, anchor="mm")
    f = sigdir(dr, "EV SAHİBİ OLUYOR", "Black", 490, W - 2 * PAD)
    dr.text((CS, 1900), "EV SAHİBİ OLUYOR", font=f, fill=BEYAZ, anchor="mm")
    dr.text((CS, 2440), "1+0 dairelerde · Banka yok · Faiz yok · Kefil yok",
            font=mont("SemiBold", 210), fill=(20, 52, 80), anchor="mm")
    fiyat_satiri(dr, CD - 200, 1120, "699.000 TL", "PEŞİNATLA")
    fiyat_satiri(dr, CD - 200, 1720, "29.900 TL", "TAKSİTLE KAVUŞUN!")
    foto_alt(im, "entrance-gate.webp", 2080, grad_renk(G_U, G_A, H - 2080),
             0.5, 1.2, focus_y=0.50)
    yildiz(im, P - 1550, 2750, 850, ["ÜSTELİK", "FAİZSİZ!"])
    dr = ImageDraw.Draw(im)
    tel_cip(dr, CD, H - 400)
    kaydet("01-izmit", im)


def c02():
    """YOK duvarı — açık zemin, giriş kapısı şeridi (meta k05)."""
    A_U, A_A = (240, 246, 251), (252, 253, 255)
    im = grad_zemin(A_U, A_A)
    ust_logolar(im, koyu=False)
    dr = ImageDraw.Draw(im)
    dr.text((CS, 1080), "EV SAHİBİ OLMAK İÇİN", font=mont("ExtraBold", 300),
            fill=NAVY, anchor="mm")
    f1 = mont("Black", 440)
    y = 1540
    for a in ["BANKA", "FAİZ", "KEFİL"]:
        aw = dr.textlength(a + "  ", font=f1)
        bw = dr.textlength("YOK", font=f1) + 240
        x = CS - (aw + bw + 80) / 2
        dr.text((x, y), a, font=f1, fill=NAVY, anchor="lm")
        cip(dr, x + aw + 80 + bw / 2, y, "YOK", f1, pad_x=120, pad_y=36)
        y += 520
    cip(dr, CD, 1250, "60 AY SABİT TAKSİT", mont("ExtraBold", 330),
        dolgu=NAVY, yazi=BEYAZ, pad_x=200, pad_y=110)
    foto_alt(im, "entrance-gate.webp", 1900, grad_renk(A_U, A_A, H - 1900),
             0.45, 1.0, focus_y=0.42, bl=260)
    yildiz(im, P - 1550, 2350, 850, ["KOMİSYON", "YOK!"], don=10)
    dr = ImageDraw.Draw(im)
    tel_cip(dr, CD, H - 400)
    kaydet("02-yok-duvari", im)


def c03():
    """%0 — canlı yeşil gradyan, giriş kapısı şeridi (meta k06)."""
    G_U, G_A = (20, 138, 104), (8, 86, 66)
    im = grad_zemin(G_U, G_A)
    ust_logolar(im, koyu=True)
    dr = ImageDraw.Draw(im)
    dr.text((CS, 1400), "%0", font=mont("Black", 1450), fill=SARI, anchor="mm")
    dr.text((CS, 2400), "FAİZ · VADE FARKI · KOMİSYON", font=mont("ExtraBold", 290),
            fill=BEYAZ, anchor="mm")
    dr.text((CD, 1100), "60 ay sabit taksit · banka yok",
            font=mont("SemiBold", 250), fill=(206, 236, 224), anchor="mm")
    cip(dr, CD, 1650, "İZMİT MİA BÖLGESİ", mont("ExtraBold", 320),
        dolgu=SARI, yazi=YESIL_U, pad_x=200, pad_y=100)
    foto_alt(im, "entrance-gate.webp", 2140, grad_renk(G_U, G_A, H - 2140),
             0.52, 1.15, focus_y=0.45)
    dr = ImageDraw.Draw(im)
    tel_cip(dr, CD, H - 400, dolgu=BEYAZ, yazi=YESIL_U)
    kaydet("03-sifir", im)


def c04():
    """60 AY — krem zemin, pergola terası şeridi (meta k07)."""
    A_U, A_A = (253, 251, 249), (244, 238, 232)
    im = grad_zemin(A_U, A_A)
    ust_logolar(im, koyu=False)
    dr = ImageDraw.Draw(im)
    dr.text((CS, 1400), "60 AY", font=mont("Black", 1150), fill=KIRMIZI, anchor="mm")
    cip(dr, CS, 2380, "VADE FARKSIZ · SABİT TAKSİT", mont("ExtraBold", 290),
        pad_x=200, pad_y=110)
    dr.text((CD, 1150), "Banka yok · Faiz yok", font=mont("ExtraBold", 330),
            fill=NAVY, anchor="mm")
    dr.text((CD, 1650), "Kefil yok · Komisyon yok", font=mont("ExtraBold", 330),
            fill=NAVY, anchor="mm")
    foto_alt(im, "terrace-pergola.webp", 2150, grad_renk(A_U, A_A, H - 2150),
             0.5, 1.0, focus_y=0.40, bl=260)
    dr = ImageDraw.Draw(im)
    tel_cip(dr, CD, H - 400, dolgu=KIRMIZI, site=False)
    kaydet("04-60ay", im)


def c05():
    """Aylık 29.900 — okyanus mavisi, gece kapısı şeridi (meta k04)."""
    im = grad_zemin(MAVI_U, MAVI_A)
    ust_logolar(im, koyu=True)
    dr = ImageDraw.Draw(im)
    dr.text((CS, 1000), "İzmit MİA'da", font=mont("SemiBold", 270),
            fill=(206, 234, 248), anchor="mm")
    f = sigdir(dr, "Aylık 29.900 TL'ye", "ExtraBold", 490, W - 2 * PAD)
    dr.text((CS, 1560), "Aylık 29.900 TL'ye", font=f, fill=BEYAZ, anchor="mm")
    dr.text((CS, 2140), "ev sahibi olun.", font=f, fill=BEYAZ, anchor="mm")
    dr.text((CD, 1100), "Üstelik 60 aya varan vade ve", font=mont("SemiBold", 250),
            fill=(206, 234, 248), anchor="mm")
    dr.text((CD, 1480), "0 faizle yeni evinize kavuşun!", font=mont("SemiBold", 250),
            fill=(206, 234, 248), anchor="mm")
    foto_alt(im, "entrance-gate.webp", 2200, grad_renk(MAVI_U, MAVI_A, H - 2200),
             0.62, 1.25, focus_y=0.35)
    yildiz(im, P - 1550, 2600, 850, ["FAİZ", "YOK!"], don=10)
    dr = ImageDraw.Draw(im)
    tel_cip(dr, CD, H - 400, dolgu=BEYAZ, yazi=MAVI_U)
    kaydet("05-aylik", im)


def c06():
    """KOCAELİ DENİZE YAKIN — gök, balkondan deniz şeridi (meta k08)."""
    G_U, G_A = (96, 138, 158), (168, 210, 230)
    im = grad_zemin(G_U, G_A)
    ust_logolar(im, koyu=True)
    dr = ImageDraw.Draw(im)
    dr.text((CS, 1150), "KOCAELİ", font=mont("Black", 720), fill=BEYAZ, anchor="mm")
    f = sigdir(dr, "DENİZE YAKIN EV SAHİBİ OLUYOR", "Black", 290, W - 2 * PAD)
    dr.text((CS, 1830), "DENİZE YAKIN EV SAHİBİ OLUYOR", font=f, fill=BEYAZ,
            anchor="mm")
    dr.text((CS, 2360), "İzmit sahiline 2 dk · 60 ay vade farksız",
            font=mont("SemiBold", 210), fill=(16, 58, 92), anchor="mm")
    fiyat_satiri(dr, CD - 200, 1120, "999.000 TL", "PEŞİNATLA 1+1", 310)
    fiyat_satiri(dr, CD - 200, 1700, "39.900 TL", "TAKSİTLE!", 310)
    foto_alt(im, "entrance-gate.webp", 2250,
             grad_renk(G_U, G_A, H - 2250), 0.5, 1.0, focus_y=0.25)
    yildiz(im, P - 1550, 2500, 850, ["BANKA", "YOK!"])
    dr = ImageDraw.Draw(im)
    tel_cip(dr, CD, H - 400)
    kaydet("06-kocaeli", im)


def c07():
    """EV SAHİBİ OLMA ZAMANI — lacivert, balkon alacakaranlık (meta k10)."""
    G_U, G_A = (12, 48, 92), (26, 80, 132)
    im = grad_zemin(G_U, G_A)
    ust_logolar(im, koyu=True)
    dr = ImageDraw.Draw(im)
    dr.text((CS, 1030), "29.900 TL taksitle", font=mont("SemiBold", 300),
            fill=(150, 205, 228), anchor="mm")
    dr.text((CS, 1620), "EV SAHİBİ", font=mont("Black", 640), fill=BEYAZ, anchor="mm")
    cip(dr, CS, 2320, "OLMA ZAMANI", mont("Black", 510), pad_x=220, pad_y=70)
    dr.text((CD, 1100), "Banka yok · Faiz yok", font=mont("SemiBold", 260),
            fill=(180, 208, 226), anchor="mm")
    dr.text((CD, 1490), "Kefil yok · Ara ödeme yok", font=mont("SemiBold", 260),
            fill=(180, 208, 226), anchor="mm")
    foto_alt(im, "terrace-pergola.webp", 2150, grad_renk(G_U, G_A, H - 2150),
             0.68, 1.25, focus_y=0.45, bl=360)
    yildiz(im, P - 1550, 2300, 800, ["60 AY", "VADE", "FARKSIZ"], don=12)
    dr = ImageDraw.Draw(im)
    tel_cip(dr, CD, H - 400, dolgu=SARI, yazi=NAVY)
    kaydet("07-olma-zamani", im)


def c08():
    """1+0 stüdyo yatırım — canlı yeşil, avlu şeridi (meta k02)."""
    im = grad_zemin(YESIL_U, YESIL_A)
    ust_logolar(im, koyu=True)
    dr = ImageDraw.Draw(im)
    dr.text((CS, 1030), "1+0 stüdyo dairelerde", font=mont("SemiBold", 280),
            fill=(206, 236, 224), anchor="mm")
    f = sigdir(dr, "avantajlı yatırım", "ExtraBold", 440, W - 2 * PAD)
    dr.text((CS, 1580), "avantajlı yatırım", font=f, fill=BEYAZ, anchor="mm")
    dr.text((CS, 2130), "fırsatı", font=f, fill=BEYAZ, anchor="mm")
    f1, fk = mont("ExtraBold", 300), mont("SemiBold", 200)
    for i, (buyuk, kucuk) in enumerate([("699.000 TL", "peşinat"),
                                        ("29.900 TL", "taksit")]):
        cx = CD - 1560 + i * 3120
        dr.rounded_rectangle([cx - 1380, 850, cx + 1380, 1750], radius=100,
                             outline=BEYAZ, width=18)
        dr.text((cx, 1190), buyuk, font=f1, fill=SARI, anchor="mm")
        dr.text((cx, 1540), kucuk, font=fk, fill=BEYAZ, anchor="mm")
    cip(dr, CD, 2140, "60 AY VADE FARKSIZ · BANKA YOK", mont("ExtraBold", 240),
        dolgu=SARI, yazi=YESIL_U, pad_x=180, pad_y=90)
    foto_alt(im, "terrace-pergola.webp", 2100,
             grad_renk(YESIL_U, YESIL_A, H - 2100), 0.32, 1.2, focus_y=0.50)
    dr = ImageDraw.Draw(im)
    tel_cip(dr, CD, H - 400, dolgu=BEYAZ, yazi=YESIL_U)
    kaydet("08-studyo", im)


def c09():
    """Tasarrufa dayalı finansman — açık gök, sıcak cephe şeridi (meta k09)."""
    G_U, G_A = (140, 198, 224), (225, 242, 250)
    im = grad_zemin(G_U, G_A)
    ust_logolar(im, koyu=False)
    dr = ImageDraw.Draw(im)
    dr.rounded_rectangle([CS - 3100, 950, CS + 3100, 2200], radius=170, fill=NAVY)
    dr.text((CS, 1370), "Tasarrufa dayalı finansmanla", font=mont("SemiBold", 250),
            fill=(150, 205, 228), anchor="mm")
    dr.text((CS, 1830), "EV SAHİBİ OL!", font=mont("Black", 430), fill=BEYAZ,
            anchor="mm")
    y = 1150
    for a in ["BANKA YOK", "FAİZ YOK", "60 AY SABİT TAKSİT"]:
        cip(dr, CD, y, a, mont("ExtraBold", 250), pad_x=190, pad_y=85)
        y += 560
    foto_alt(im, "terrace-pergola.webp", 2100,
             grad_renk(G_U, G_A, H - 2100), 0.5, 1.1, focus_y=0.28, bl=340)
    yildiz(im, P - 1550, 2650, 820, ["ARA", "ÖDEME", "YOK!"], don=10)
    dr = ImageDraw.Draw(im)
    tel_cip(dr, CD, H - 400)
    kaydet("09-tasarruf", im)


def c10():
    """SATIŞ OFİSİMİZE BEKLERİZ — okyanus mavisi, avlu dusk şeridi (meta k03)."""
    im = grad_zemin(MAVI_U, MAVI_A)
    ust_logolar(im, koyu=True)
    dr = ImageDraw.Draw(im)
    dr.text((CS, 1030), "60 AY VADEYLE", font=mont("Black", 420), fill=BEYAZ,
            anchor="mm")
    f = sigdir(dr, "EV SAHİBİ OLMAK İÇİN", "Black", 420, W - 2 * PAD)
    dr.text((CS, 1560), "EV SAHİBİ OLMAK İÇİN", font=f, fill=BEYAZ, anchor="mm")
    cip(dr, CS, 2200, "SATIŞ OFİSİMİZE BEKLERİZ", mont("ExtraBold", 280),
        pad_x=220, pad_y=110)
    fs1, fs2 = mont("ExtraBold", 235), mont("SemiBold", 170)
    for i, (a, b) in enumerate([("699.000 TL'den", "başlayan peşinat"),
                                ("%0", "faiz"), ("29.900 TL", "taksit")]):
        cx = CD + (i - 1) * 2360
        dr.rounded_rectangle([cx - 1090, 900, cx + 1090, 1750], radius=100,
                             outline=BEYAZ, width=16)
        dr.text((cx, 1220), a, font=fs1, fill=SARI, anchor="mm")
        dr.text((cx, 1550), b, font=fs2, fill=BEYAZ, anchor="mm")
    dr.text((CD, 2130), "İzmit satış ofisi", font=mont("ExtraBold", 280),
            fill=BEYAZ, anchor="mm")
    foto_alt(im, "entrance-gate.webp", 2150,
             grad_renk(MAVI_U, MAVI_A, H - 2150), 0.4, 1.05, focus_y=0.55)
    dr = ImageDraw.Draw(im)
    tel_cip(dr, CD, H - 400, dolgu=BEYAZ, yazi=MAVI_U)
    kaydet("10-satis-ofisi", im)


def kontak():
    """Her satırda bir çift (SOL + SAĞ), arada çerçeve boşluğu."""
    fs = sorted(f for f in os.listdir(ONIZ)
                if f.startswith("bilbord-v5-") and f.endswith(".jpg"))
    ciftler = {}
    for f in fs:
        kok = f.rsplit("-", 1)[0]
        ciftler.setdefault(kok, {})["SOL" if "SOL" in f else "SAG"] = f
    tw = 660
    th = int(tw * H / W)
    ara, dis = 28, 20
    kokler = sorted(ciftler)
    sh = len(kokler) * (th + dis) + dis
    sheet = Image.new("RGB", (2 * tw + ara + 2 * dis, sh), (16, 20, 26))
    for i, kok in enumerate(kokler):
        y = dis + i * (th + dis)
        for j, yon in enumerate(["SOL", "SAG"]):
            im = Image.open(os.path.join(ONIZ, ciftler[kok][yon])).resize(
                (tw, th), Image.LANCZOS)
            sheet.paste(im, (dis + j * (tw + ara), y))
    sheet.save(os.path.join(OUT, "kontak-bilbord-v5.jpg"), quality=88)
    print("   kontak-bilbord-v5.jpg")


if __name__ == "__main__":
    for c in [c01, c02, c03, c04, c05, c06, c07, c08, c09, c10]:
        c()
    kontak()
    print("tamam ->", OUT)
