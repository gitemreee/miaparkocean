#!/usr/bin/env python3
"""
MİA PARK OCEAN — Meta reklam seti v5 (10 kreatif, 1080x1350).

Referans teknikleri (Katılımevim, arsaVev, Eminevim, Fuzul, Toprak Tan,
Turyap): sarı fosforlu çip rakam vurgusu, canlı tek renk bloklar + foto
kartı, üçlü istatistik çipi, şehir başlığı, kırmızı "üstelik" yıldızı.

Sabit kurallar (işveren):
- Her kreatifin TEPESİNDE: solda MİA PARK OCEAN, sağda OCEAN GAYRİMENKUL
  logosu — pedsiz, şeffaf PNG (açık zeminde renkli, koyu zeminde beyaz).
- "Görseller temsilidir", kooperatif adı ve dönemsellik dipnotu HİÇBİR
  görselde yazmaz (işveren talebi, 21.08).
- Fotoğraflar YALNIZ dış cephe; kart/çerçeve YOK — k04'teki gibi tam
  genişlik alta yayılır, üst kenarı zemine yumuşak karışır.
- Zeminler düz renk değil dikey gradyan; kırmızı blok yerine canlı
  okyanus mavisi kullanılır (kırmızı yalnız yıldız rozetlerde).
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
KIRMIZI = (200, 32, 42)      # yalnız yıldız rozetler + k07 vurgusu
MAVI_U = (12, 102, 150)      # canlı okyanus mavisi (gradyan üst)
MAVI_A = (26, 146, 198)      # canlı okyanus mavisi (gradyan alt)
YESIL = (16, 118, 90)        # canlı yeşil alan
YESIL_A = (22, 140, 108)
BEYAZ = (255, 255, 255)
KURSUN = (71, 96, 110)

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


def grad_zemin(ust, alt):
    """Dikey gradyan zemin (üst renk -> alt renk)."""
    t = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    g = (np.array(ust, np.float32) * (1 - t)
         + np.array(alt, np.float32) * t).astype(np.uint8)
    im = Image.new("RGBA", (W, H))
    im.paste(Image.fromarray(np.repeat(g, W, axis=1), "RGB"), (0, 0))
    return im


def grad_renk(ust, alt, y):
    """Gradyanın y satırındaki rengi (foto karışım bandı için)."""
    t = y / H
    return tuple(int(u * (1 - t) + a * t) for u, a in zip(ust, alt))


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


def foto_alt(im, kaynak, yuk, zemin, focus=0.5, zoom=1.0, focus_y=None, bl=110):
    """Kartsız-çerçevesiz foto: alta tam genişlik yayılır (k04 dili),
    üst kenarı zeminin o satırdaki rengine yumuşak karışır."""
    ft = foto(kaynak, W, yuk, focus, zoom, focus_y=focus_y)
    im.paste(ft, (0, H - yuk))
    band = np.asarray(ft.crop((0, 0, W, bl)), np.float32)
    alfa = np.linspace(1, 0, bl, dtype=np.float32)[:, None, None]
    kar = (np.array(zemin, np.float32) * alfa + band * (1 - alfa)).astype(np.uint8)
    im.paste(Image.fromarray(kar, "RGB"), (0, H - yuk))


def tel_cip(dr, cy, dolgu=NAVY, yazi=BEYAZ, site=True, gen=640):
    t = TEL + ("  ·  " + SITE if site else "")
    dr.rounded_rectangle([(W - gen) / 2, cy - 34, (W + gen) / 2, cy + 34],
                         radius=34, fill=dolgu)
    dr.text((W / 2, cy), t, font=mont("Bold", 28), fill=yazi, anchor="mm")


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
    kaydet(im, "meta-v5-01-izmit-oluyor")


def k02():
    """Canlı yeşil gradyan — çerçeve çipler + tam genişlik dış cephe."""
    G_U, G_A = (8, 92, 70), (24, 146, 112)
    im = grad_zemin(G_U, G_A)
    dr = ImageDraw.Draw(im)
    for i in range(4):
        dr.line([(W - 260 + i * 60, 0), (W + 40 + i * 60, 300)],
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
    dr.text((W / 2, 622), "İzmit MİA Bölgesi", font=mont("Bold", 30),
            fill=(206, 236, 224), anchor="mm")
    foto_alt(im, "entrance-gate.webp", 680, grad_renk(G_U, G_A, H - 680),
             0.45, 1.0, focus_y=0.62)
    dr = ImageDraw.Draw(im)
    tel_cip(dr, H - 92, dolgu=BEYAZ, yazi=YESIL)
    kaydet(im, "meta-v5-02-yesil")


def k03():
    """Canlı okyanus mavisi gradyan — üçlü istatistik çipi + gece cephesi."""
    im = grad_zemin(MAVI_U, MAVI_A)
    dr = ImageDraw.Draw(im)
    ust_logolar(im, koyu=True)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 226), "60 AY VADEYLE", font=mont("Black", 56), fill=BEYAZ, anchor="mm")
    dr.text((W / 2, 290), "EV SAHİBİ OLMAK İÇİN", font=mont("Black", 56),
            fill=BEYAZ, anchor="mm")
    dr.text((W / 2, 352), "SATIŞ OFİSİMİZE BEKLERİZ", font=mont("SemiBold", 34),
            fill=(206, 234, 248), anchor="mm")
    fs1, fs2 = mont("ExtraBold", 30), mont("SemiBold", 21)
    for i, (a, b) in enumerate([("699.000 TL'den", "başlayan peşinat"),
                                ("%0", "faiz"), ("29.900 TL", "taksit")]):
        cx = W / 2 - 348 + i * 348
        dr.rounded_rectangle([cx - 166, 412, cx + 166, 530], radius=16,
                             outline=BEYAZ, width=3)
        dr.text((cx, 456), a, font=fs1, fill=SARI, anchor="mm")
        dr.text((cx, 500), b, font=fs2, fill=BEYAZ, anchor="mm")
    foto_alt(im, "night-gate.webp", 700, grad_renk(MAVI_U, MAVI_A, H - 700), 0.5, 1.05)
    dr = ImageDraw.Draw(im)
    dr.rounded_rectangle([W - 400, H - 99, W - 60, H - 41], radius=29, fill=BEYAZ)
    dr.text((W - 230, H - 71), TEL, font=mont("ExtraBold", 26), fill=MAVI_U, anchor="mm")
    dr.text((60, H - 71), "İzmit satış ofisi", font=mont("SemiBold", 25),
            fill=BEYAZ, anchor="lm")
    kaydet(im, "meta-v5-03-mavi")


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
    kaydet(im, "meta-v5-04-aylik")


def k05():
    """Açık YOK duvarı — sarı çipler, dış cephe altta."""
    A_U, A_A = (240, 246, 251), (252, 253, 255)
    im = grad_zemin(A_U, A_A)
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
    foto_alt(im, "entrance-gate.webp", 500, grad_renk(A_U, A_A, H - 500),
             0.5, 1.0, focus_y=0.55, bl=90)
    dr = ImageDraw.Draw(im)
    tel_cip(dr, H - 92)
    kaydet(im, "meta-v5-05-yok-cipleri")


def k06():
    """Canlı yeşil gradyan %0 — dev sarı rakam + tam genişlik cephe."""
    G_U, G_A = (20, 138, 104), (8, 86, 66)
    im = grad_zemin(G_U, G_A)
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
    cip(dr, W / 2, 614, "İZMİT MİA BÖLGESİ", mont("ExtraBold", 28),
        dolgu=SARI, yazi=YESIL)
    foto_alt(im, "entrance-gate.webp", 660, grad_renk(G_U, G_A, H - 660), 0.45, 1.05)
    dr = ImageDraw.Draw(im)
    tel_cip(dr, H - 92, dolgu=BEYAZ, yazi=YESIL)
    kaydet(im, "meta-v5-06-yesil-sifir")


def k07():
    """Açık gradyan 60 AY — kırmızı dev rakam + tam genişlik cephe."""
    A_U, A_A = (253, 251, 249), (244, 238, 232)
    im = grad_zemin(A_U, A_A)
    dr = ImageDraw.Draw(im)
    ust_logolar(im, koyu=False)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 300), "60 AY", font=mont("Black", 185), fill=KIRMIZI, anchor="mm")
    cip(dr, W / 2, 442, "VADE FARKSIZ · SABİT TAKSİT", mont("ExtraBold", 36),
        pad_x=34, pad_y=14)
    dr.text((W / 2, 522), "Banka yok · Faiz yok · Kefil yok · Komisyon yok",
            font=mont("SemiBold", 29), fill=(96, 74, 70), anchor="mm")
    foto_alt(im, "entrance-gate.webp", 700, grad_renk(A_U, A_A, H - 700),
             0.45, 1.05, focus_y=0.5)
    dr = ImageDraw.Draw(im)
    tel_cip(dr, H - 92, dolgu=KIRMIZI, site=False, gen=520)
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
    kaydet(im, "meta-v5-08-kocaeli")


def k09():
    """Açık gök gradyan — lacivert afiş + sarı çipler + tam genişlik cephe."""
    G_U, G_A = (140, 198, 224), (235, 246, 251)
    im = grad_zemin(G_U, G_A)
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
    foto_alt(im, "entrance-gate.webp", 690, grad_renk(G_U, G_A, H - 690),
             0.45, 1.0, focus_y=0.58)
    dr = ImageDraw.Draw(im)
    yildiz(im, W - 172, 700, 100, ["ARA", "ÖDEME", "YOK!"], don=10)
    dr = ImageDraw.Draw(im)
    tel_cip(dr, H - 92)
    kaydet(im, "meta-v5-09-acik")


def k10():
    """Lacivert gradyan-sarı kampanya — 'EV SAHİBİ [OLMA ZAMANI]'."""
    G_U, G_A = (12, 48, 92), (26, 80, 132)
    im = grad_zemin(G_U, G_A)
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
    foto_alt(im, "entrance-gate.webp", 700, grad_renk(G_U, G_A, H - 700),
             0.5, 1.1, focus_y=0.55, bl=140)
    dr = ImageDraw.Draw(im)
    yildiz(im, W - 170, 690, 98, ["60 AY", "VADE", "FARKSIZ"], don=12)
    dr = ImageDraw.Draw(im)
    tel_cip(dr, H - 92, dolgu=SARI, yazi=NAVY)
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
