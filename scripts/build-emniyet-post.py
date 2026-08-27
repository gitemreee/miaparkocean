#!/usr/bin/env python3
"""
MİA PARK OCEAN — Kocaeli Emniyet personeline %5 peşinat indirimi kartı.

Onaylı açık şablonun (sosyal-turkuaz / sarı çipli YOK kalıbı) aynısı:
gök-buz gradyan, beyazlaşan köşelerde renkli logolar, navy başlık,
SARI çipli satırlar, kırmızı burgu, giriş kapısı fotoğrafı altta,
lacivert iletişim hapı (tel · web · Instagram/Facebook · miaparkocean).

Kampanya fiyatları (işveren):
    1+0 :   664.000 TL peşinat · 29.900 TL x 60 ay taksit
    1+1 :   950.000 TL peşinat · 39.900 TL x 60 ay taksit
    2+1 : 1.900.000 TL peşinat · 49.900 TL x 60 ay taksit

    python3 scripts/build-emniyet-post.py
"""

import importlib.util
import math
import os
import sys

from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_spec = importlib.util.spec_from_file_location(
    "st", os.path.join(ROOT, "scripts", "build-sosyal-turkuaz.py"))
st = importlib.util.module_from_spec(_spec)
sys.modules["st"] = st
_spec.loader.exec_module(st)

W, H = 1080, 1350
OUT = os.path.join(ROOT, "sosyal-medya", "turkuaz-kampanya", "postlar")

NAVY = (10, 42, 74)
SARI = (255, 209, 74)
KIRMIZI = (200, 32, 42)
BEYAZ = (255, 255, 255)
mont = st.mont


def yildiz(im, metinler, cx, cy, r, don=10):
    kat = Image.new("RGBA", (r * 3, r * 3), (0, 0, 0, 0))
    kd = ImageDraw.Draw(kat)
    c = r * 1.5
    pts = []
    for i in range(52):
        rr = r if i % 2 == 0 else r * 0.84
        a = math.pi * i / 26
        pts.append((c + rr * math.cos(a), c + rr * math.sin(a)))
    kd.polygon(pts, fill=KIRMIZI + (255,))
    fb = mont("ExtraBold", int(r * (0.30 if len(metinler) > 1 else 0.34)))
    y0 = c - (len(metinler) - 1) * r * 0.20
    for i, t in enumerate(metinler):
        kd.text((c, y0 + i * r * 0.40), t, font=fb, fill=BEYAZ, anchor="mm")
    kat = kat.rotate(don, resample=Image.BICUBIC, expand=False)
    im.alpha_composite(kat, (int(cx - c), int(cy - c)))


def main():
    im = st.zemin(W, H)
    st.foto_alt(im, 500, 0.5, 1.05, 0.45)
    st.logolar(im, 260, 235, 44, 28, 46, 600)
    dr = ImageDraw.Draw(im)

    dr.text((W / 2, 236), "KOCAELİ EMNİYET", font=mont("ExtraBold", 54),
            fill=NAVY, anchor="mm")
    dr.text((W / 2, 296), "PERSONELİNE ÖZEL", font=mont("ExtraBold", 54),
            fill=NAVY, anchor="mm")
    fb = mont("Black", 46)
    tw1 = dr.textlength("PEŞİNATTA ", font=fb)
    tw2 = dr.textlength("%5 İNDİRİM", font=fb) + 2 * 22
    x = (W - tw1 - 14 - tw2) / 2
    dr.text((x, 378), "PEŞİNATTA", font=fb, fill=NAVY, anchor="lm")
    st.cip(dr, x + tw1 + 14 + tw2 / 2, 378, "%5 İNDİRİM", fb,
           dolgu=SARI, yazi=NAVY, pad_x=22, pad_y=8, r=12)

    satirlar = [("1+0", "664.000 TL PEŞİNAT", "29.900 TL x 60 ay taksit"),
                ("1+1", "950.000 TL PEŞİNAT", "39.900 TL x 60 ay taksit"),
                ("2+1", "1.900.000 TL PEŞİNAT", "49.900 TL x 60 ay taksit")]
    ft = mont("Black", 48)
    fc = mont("ExtraBold", 33)
    fk = mont("SemiBold", 26)
    y = 476
    for tip, pesin, taksit in satirlar:
        wt = dr.textlength(tip, font=ft)
        wc = dr.textlength(pesin, font=fc) + 2 * 18
        wk = dr.textlength(taksit, font=fk)
        x = (W - wt - 16 - wc - 18 - wk) / 2
        dr.text((x, y), tip, font=ft, fill=NAVY, anchor="lm")
        st.cip(dr, x + wt + 16 + wc / 2, y, pesin, fc, dolgu=SARI,
               yazi=NAVY, pad_x=18, pad_y=10, r=11)
        dr.text((x + wt + 16 + wc + 18, y + 2), taksit, font=fk,
                fill=(36, 74, 108), anchor="lm")
        y += 90
    dr.text((W / 2, y + 8), "Banka yok · Faiz yok · Kefil yok · Komisyon yok",
            font=mont("SemiBold", 29), fill=(36, 74, 108), anchor="mm")

    st.cip(dr, W / 2, y + 82, "60 AY SABİT TAKSİT", mont("ExtraBold", 38),
           dolgu=NAVY, yazi=BEYAZ, pad_x=28, pad_y=12, r=14)

    yildiz(im, ["BANKA", "YOK!"], 915, 985, 100)
    dr = ImageDraw.Draw(im)

    # Lacivert iletişim hapı: tel · web · ikonlar · miaparkocean
    f1 = mont("Bold", 27)
    f2 = mont("Bold", 24)
    t1 = "0540 028 00 41  ·  miaparkocean.com"
    ik, kal = 32, 3
    w1 = dr.textlength(t1, font=f1)
    wh = dr.textlength("miaparkocean", font=f2)
    icerik = w1 + 26 + ik + 12 + ik + 14 + wh
    gen = icerik + 2 * 40
    cy = H - 88
    dr.rounded_rectangle([(W - gen) / 2, cy - 34, (W + gen) / 2, cy + 34],
                         radius=34, fill=NAVY)
    x = (W - icerik) / 2
    dr.text((x, cy), t1, font=f1, fill=BEYAZ, anchor="lm")
    x += w1 + 26
    dr.rounded_rectangle([x, cy - ik / 2, x + ik, cy + ik / 2], radius=9,
                         outline=BEYAZ, width=kal)
    dr.ellipse([x + ik * 0.26, cy - ik * 0.24, x + ik * 0.74, cy + ik * 0.24],
               outline=BEYAZ, width=kal)
    dr.ellipse([x + ik * 0.70, cy - ik * 0.42, x + ik * 0.88, cy - ik * 0.24],
               fill=BEYAZ)
    x += ik + 12
    dr.rounded_rectangle([x, cy - ik / 2, x + ik, cy + ik / 2], radius=9,
                         outline=BEYAZ, width=kal)
    dr.text((x + ik * 0.55, cy + 1), "f", font=mont("Bold", 24), fill=BEYAZ,
            anchor="mm")
    x += ik + 14
    dr.text((x, cy), "miaparkocean", font=f2, fill=BEYAZ, anchor="lm")

    p = os.path.join(OUT, "post-16-emniyet-kampanya.jpg")
    im.convert("RGB").save(p, quality=92, optimize=True)
    print("   post-16-emniyet-kampanya  1080x1350")


if __name__ == "__main__":
    main()
