#!/usr/bin/env python3
"""
MİA PARK OCEAN — 15 BAĞIMSIZ gönderi (grid değil, tek tek paylaşılır).

Facebook + Instagram akışı için 1080x1350 (4:5) seri; turkuaz kampanya
dili: gradyan zemin, kırmızı YOK çipleri, turkuaz kartlar, kırmızı burgu,
beyazlaşan köşelerde renkli logolar, altta Satış Ofisi iletişim satırı.

Kurallar: onaylı örnek fiyatlar dışında fiyat yok; "peşinatsız"/"%30"
geçmez; yalnız projenin kendi render'ları; koop adı/dipnot yok.

    python3 scripts/build-post-serisi.py
"""

import importlib.util
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_spec = importlib.util.spec_from_file_location(
    "st", os.path.join(ROOT, "scripts", "build-sosyal-turkuaz.py"))
st = importlib.util.module_from_spec(_spec)
sys.modules["st"] = st
_spec.loader.exec_module(st)

W, H = 1080, 1350
OUT = os.path.join(ROOT, "sosyal-medya", "turkuaz-kampanya", "postlar")
os.makedirs(OUT, exist_ok=True)

KIRMIZI, TURKUAZ, TURKUAZ_K = st.KIRMIZI, st.TURKUAZ, st.TURKUAZ_K
PETROL, BEYAZ, GRI = st.PETROL, st.BEYAZ, st.GRI
mont, sigdir, cip = st.mont, st.sigdir, st.cip


def zemin2(ust, alt):
    t = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    g = (np.array(ust, np.float32) * (1 - t)
         + np.array(alt, np.float32) * t).astype(np.uint8)
    im = Image.new("RGBA", (W, H))
    im.paste(Image.fromarray(np.repeat(g, W, axis=1), "RGB"), (0, 0))
    return im


def foto_alt2(im, ad, yuk, krop, ust, alt, bl=100):
    f, z, fy = krop
    ft = st.foto(ad, W, yuk, f, z, focus_y=fy)
    im.paste(ft, (0, H - yuk))
    t = (H - yuk) / H
    zc = np.array([u * (1 - t) + a * t for u, a in zip(ust, alt)], np.float32)
    band = np.asarray(ft.crop((0, 0, W, bl)), np.float32)
    alfa = np.linspace(1, 0, bl, dtype=np.float32)[:, None, None]
    kar = (zc * alfa + band * (1 - alfa)).astype(np.uint8)
    im.paste(Image.fromarray(kar, "RGB"), (0, H - yuk))


def yildiz2(im, metinler, cx, cy, r, don=10):
    kat = Image.new("RGBA", (r * 3, r * 3), (0, 0, 0, 0))
    kd = ImageDraw.Draw(kat)
    c = r * 1.5
    pts = []
    for i in range(52):
        rr = r if i % 2 == 0 else r * 0.84
        a = math.pi * i / 26
        pts.append((c + rr * math.cos(a), c + rr * math.sin(a)))
    kd.polygon(pts, fill=KIRMIZI + (255,))
    fb = mont("ExtraBold", int(r * (0.28 if len(metinler) > 1 else 0.32)))
    y0 = c - (len(metinler) - 1) * r * 0.19
    for i, t in enumerate(metinler):
        kd.text((c, y0 + i * r * 0.38), t, font=fb, fill=BEYAZ, anchor="mm")
    kat = kat.rotate(don, resample=Image.BICUBIC, expand=False)
    im.alpha_composite(kat, (int(cx - c), int(cy - c)))


def taban(gece=False):
    if gece:
        U, A = (3, 48, 56), (0, 96, 108)
    else:
        U, A = st.Z_UST, st.Z_ALT
    return zemin2(U, A), U, A


def kaydet(im, ad):
    p = os.path.join(OUT, ad + ".jpg")
    im.convert("RGB").save(p, quality=92, optimize=True)
    print("   " + ad)


def govde(ad, gece, foto_ad, krop, yuk, ciz, yildiz_m=None, yc=(905, 108)):
    im, U, A = taban(gece)
    foto_alt2(im, foto_ad, yuk, krop, U, A, bl=90 if yuk < 460 else 100)
    st.logolar(im, 260, 235, 44, 28, 46, 600)
    dr = ImageDraw.Draw(im)
    ciz(dr, im, gece)
    if yildiz_m:
        yildiz2(im, yildiz_m, W - 168, yc[0], yc[1])
    dr = ImageDraw.Draw(im)
    st.iletisim(dr, W, H - 44, W - 70, acik=False)
    kaydet(im, ad)


M = PETROL


def b(dr, y, t, kes, boy, renk, maxw=W - 90):
    dr.text((W / 2, y), t, font=sigdir(dr, t, kes, boy, maxw),
            fill=renk, anchor="mm")


# ═══════════════════════════════════════════════ 15 GÖNDERİ
def p01():
    def c(dr, im, g):
        b(dr, 306, "KOCAELİ", "Black", 96, M)
        b(dr, 398, "EV SAHİBİ OLUYOR!", "Black", 62, M)
        st.yok_izgara(dr, W / 2, 486, 30)
        st.kartlar(dr, W / 2, 592, 470, 226, 26, 46)
    govde("post-01-kocaeli", False, "entrance-gate.webp", (0.5, 1.05, 0.45),
          500, c, ["60 AY", "SABİT", "TAKSİT!"], (940, 112))


def p02():
    def c(dr, im, g):
        b(dr, 330, "60 AY", "Black", 150, TURKUAZ_K)
        b(dr, 452, "SABİT TAKSİT!", "Black", 74, M)
        st.yok_izgara(dr, W / 2, 560, 30)
        b(dr, 660, "1+0 ve 1+1 dairelerde", "SemiBold", 34, GRI)
    govde("post-02-60ay", False, "entrance-gate.webp", (0.72, 1.3, 0.5), 560, c)


def p03():
    def c(dr, im, g):
        b(dr, 300, "1+0 STÜDYO", "Black", 84, M)
        b(dr, 384, "avantajlı yatırım fırsatı", "SemiBold", 40, GRI)
        st.kartlar(dr, W / 2 + 110, 460, 470, 226, 26, 46)
        dr.rounded_rectangle([70, 460, 540, 686], radius=16, width=0)
    def c2(dr, im, g):
        b(dr, 300, "1+0 STÜDYO", "Black", 84, M)
        b(dr, 386, "avantajlı yatırım fırsatı", "SemiBold", 40, GRI)
        bx, y, kw, kh = W / 2, 470, 560, 250
        dr.rounded_rectangle([bx - kw / 2, y, bx + kw / 2, y + kh], radius=18,
                             fill=(255, 255, 255, 255),
                             outline=TURKUAZ_K + (255,), width=3)
        cip(dr, bx, y, "1+0", mont("ExtraBold", 32), dolgu=TURKUAZ,
            pad_x=16, pad_y=6, r=9)
        dr.text((bx, y + 92), "699.000 TL", font=mont("ExtraBold", 56),
                fill=M, anchor="mm")
        dr.text((bx, y + 138), "peşinat", font=mont("SemiBold", 28),
                fill=GRI, anchor="mm")
        cip(dr, bx, y + 196, "29.900 TL TAKSİT", mont("ExtraBold", 32),
            dolgu=TURKUAZ_K, pad_x=18, pad_y=9, r=10)
    govde("post-03-studyo", False, "terrace-pergola.webp", (0.5, 1.0, 0.42),
          520, c2, ["FAİZSİZ!"], (900, 100))


def p04():
    def c(dr, im, g):
        b(dr, 300, "1+1 DAİRELER", "Black", 80, M)
        b(dr, 386, "ailenize ferah bir başlangıç", "SemiBold", 38, GRI)
        bx, y, kw, kh = W / 2, 470, 560, 250
        dr.rounded_rectangle([bx - kw / 2, y, bx + kw / 2, y + kh], radius=18,
                             fill=(255, 255, 255, 255),
                             outline=TURKUAZ_K + (255,), width=3)
        cip(dr, bx, y, "1+1", mont("ExtraBold", 32), dolgu=TURKUAZ,
            pad_x=16, pad_y=6, r=9)
        dr.text((bx, y + 92), "999.000 TL", font=mont("ExtraBold", 56),
                fill=M, anchor="mm")
        dr.text((bx, y + 138), "peşinat", font=mont("SemiBold", 28),
                fill=GRI, anchor="mm")
        cip(dr, bx, y + 196, "39.900 TL TAKSİT", mont("ExtraBold", 32),
            dolgu=TURKUAZ_K, pad_x=18, pad_y=9, r=10)
    govde("post-04-birarti1", False, "facade-warm.webp", (0.5, 1.0, 0.2),
          520, c, ["60 AY", "VADE"], (900, 100))


def p05():
    def c(dr, im, g):
        b(dr, 350, "%0", "Black", 210, (255, 209, 74))
        b(dr, 500, "FAİZ · VADE FARKI · KOMİSYON", "ExtraBold", 40, BEYAZ)
        b(dr, 570, "60 ay sabit taksit · banka yok", "SemiBold", 32,
          (200, 232, 238))
    govde("post-05-sifir-faiz", True, "night-gate.webp", (0.5, 1.0, 0.45),
          560, c)


def p06():
    def c(dr, im, g):
        b(dr, 300, "İZMİT MİA BÖLGESİ", "Black", 72, M)
        b(dr, 380, "şehrin yeni değer merkezi", "SemiBold", 36, GRI)
        satirlar = [("İzmit sahiline", "2 dk"),
                    ("Sakarya'ya", "35 dk"),
                    ("İstanbul Anadolu Yakası'na", "1,5 saat")]
        y = 470
        for a, bdeg in satirlar:
            dr.rounded_rectangle([150, y, W - 150, y + 74], radius=14,
                                 fill=(255, 255, 255, 255),
                                 outline=TURKUAZ_K + (255,), width=2)
            dr.text((180, y + 37), a, font=mont("SemiBold", 30), fill=M,
                    anchor="lm")
            dr.text((W - 180, y + 37), bdeg, font=mont("ExtraBold", 34),
                    fill=TURKUAZ_K, anchor="rm")
            y += 92
    govde("post-06-konum", False, "ic-mekan/21-balkondan-deniz.webp",
          (0.5, 1.0, 0.3), 520, c)


def p07():
    def c(dr, im, g):
        b(dr, 320, "EV SAHİBİ", "Black", 92, M)
        cip(dr, W / 2, 420, "OLMA ZAMANI", mont("Black", 64),
            dolgu=(255, 209, 74), yazi=M, pad_x=26, pad_y=10, r=14)
        st.yok_izgara(dr, W / 2, 520, 29)
    govde("post-07-olma-zamani", False, "street-corner.webp",
          (0.42, 1.0, 0.35), 560, c, ["FAİZSİZ!"], (930, 100))


def p08():
    def c(dr, im, g):
        b(dr, 300, "TASARRUFA DAYALI", "Black", 62, M)
        b(dr, 372, "FİNANSMAN", "Black", 62, TURKUAZ_K)
        b(dr, 452, "Banka kredisi yok, faiz yok —", "SemiBold", 34, GRI)
        b(dr, 500, "60 ay boyunca sabit taksitle ödersiniz.", "SemiBold", 34,
          GRI)
        cip(dr, W / 2, 590, "60 AY SABİT TAKSİT", mont("ExtraBold", 36),
            dolgu=TURKUAZ_K, pad_x=22, pad_y=12, r=12)
    govde("post-08-tasarruf", False, "entrance-gate.webp", (0.35, 1.2, 0.45),
          520, c)


def p09():
    def c(dr, im, g):
        b(dr, 330, "SATIŞ OFİSİMİZE", "Black", 74, BEYAZ)
        b(dr, 410, "BEKLERİZ", "Black", 74, BEYAZ)
        st.yok_izgara(dr, W / 2, 510, 29)
        b(dr, 610, "Size özel ödeme planını birlikte çıkaralım", "SemiBold", 32,
          (200, 232, 238))
    govde("post-09-satis-ofisi", True, "hero-courtyard-dusk.webp",
          (0.5, 1.0, 0.5), 540, c)


def p10():
    def c(dr, im, g):
        b(dr, 300, "SİTE İÇİNDE YAŞAM", "Black", 64, M)
        maddeler = ["Yeşil avlular ve su aksları",
                    "Yürüyüş yolları", "Çocuk oyun alanları"]
        y = 400
        for t in maddeler:
            dr.ellipse([W / 2 - 290, y - 7, W / 2 - 276, y + 7],
                       fill=TURKUAZ + (255,))
            dr.text((W / 2 - 250, y), t, font=mont("SemiBold", 36), fill=M,
                    anchor="lm")
            y += 72
    govde("post-10-yasam", False, "courtyard-pools.webp", (0.5, 1.0, 0.45),
          620, c)


def p11():
    def c(dr, im, g):
        b(dr, 320, "ARA ÖDEME", "Black", 92, M)
        cip(dr, W / 2, 424, "YOK!", mont("Black", 84), pad_x=34, pad_y=8, r=16)
        b(dr, 540, "Balon ödeme yok · Kredi yok · Kefil yok", "SemiBold", 33,
          GRI)
    govde("post-11-ara-odeme", False, "aerial-pools.webp", (0.5, 1.0, 0.5),
          560, c)


def p12():
    def c(dr, im, g):
        b(dr, 320, "HAYALİNİZDEKİ EVE", "Black", 62, M)
        b(dr, 392, "KAVUŞUN", "Black", 84, TURKUAZ_K)
        st.yok_izgara(dr, W / 2, 500, 29)
    govde("post-12-hayal", False, "balcony-dusk.webp", (0.55, 1.0, 0.3),
          580, c, ["60 AY", "SABİT", "TAKSİT!"], (920, 105))


def p13():
    def c(dr, im, g):
        b(dr, 290, "RAKAMLARLA", "Black", 64, M)
        veriler = [("60 AY", "sabit taksit"), ("%0", "faiz"),
                   ("1+0 · 1+1", "daire tipleri")]
        y = 400
        for a, alt in veriler:
            dr.rounded_rectangle([180, y, W - 180, y + 96], radius=14,
                                 fill=(255, 255, 255, 255),
                                 outline=TURKUAZ_K + (255,), width=2)
            dr.text((220, y + 48), a, font=mont("ExtraBold", 44),
                    fill=TURKUAZ_K, anchor="lm")
            dr.text((W - 220, y + 48), alt, font=mont("SemiBold", 32), fill=M,
                    anchor="rm")
            y += 116
    govde("post-13-rakamlar", False, "entrance-gate.webp", (0.6, 1.25, 0.5),
          480, c)


def p14():
    def c(dr, im, g):
        b(dr, 330, "AKŞAM IŞIKLARI", "Black", 68, BEYAZ)
        b(dr, 406, "EVİNİZDEN YANSISIN", "Black", 54, BEYAZ)
        b(dr, 500, "İzmit MİA Bölgesi'nde yeni yaşam", "SemiBold", 34,
          (200, 232, 238))
    govde("post-14-aksam", True, "balcony-dusk.webp", (0.5, 1.0, 0.35),
          620, c, ["FAİZSİZ!"], (900, 96))


def p15():
    """Marka postu — köşe logoları yok; merkezde büyük MİA + sağda Ocean."""
    im, U, A = taban(False)
    foto_alt2(im, "entrance-gate.webp", 540, (0.5, 1.05, 0.45), U, A)
    og = Image.open(os.path.join(ROOT, "sunum", "kaynak", "sekil",
                                 "ocean-logo-renkli2.png")).convert("RGBA")
    og = og.resize((235, int(og.height * 235 / og.width)), Image.LANCZOS)
    im.alpha_composite(og, (W - 44 - 235, 46))
    lg = Image.open(os.path.join(ROOT, "public", "brand",
                                 "logo-mia-2026.png")).convert("RGBA")
    lg = lg.resize((560, int(lg.height * 560 / lg.width)), Image.LANCZOS)
    im.alpha_composite(lg, ((W - lg.width) // 2, 170))
    dr = ImageDraw.Draw(im)
    b(dr, 660, "İzmit MİA Bölgesi'nde yeni yaşam", "SemiBold", 40, M)
    st.iletisim(dr, W, H - 44, W - 70, acik=False)
    kaydet(im, "post-15-marka")


def kontak():
    fs = sorted(f for f in os.listdir(OUT)
                if f.startswith("post-") and f.endswith(".jpg"))
    tw = 380
    th = int(tw * H / W)
    ara = 10
    cols = 5
    rows = (len(fs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * ara,
                              rows * th + (rows + 1) * ara), (16, 20, 26))
    for i, f in enumerate(fs):
        im = Image.open(os.path.join(OUT, f)).resize((tw, th), Image.LANCZOS)
        sheet.paste(im, (ara + (i % cols) * (tw + ara),
                         ara + (i // cols) * (th + ara)))
    sheet.save(os.path.join(OUT, "kontak-postlar.jpg"), quality=88)
    print("   kontak-postlar.jpg")


if __name__ == "__main__":
    for p in [p01, p02, p03, p04, p05, p06, p07, p08, p09, p10,
              p11, p12, p13, p14, p15]:
        p()
    kontak()
    print("tamam ->", OUT)
