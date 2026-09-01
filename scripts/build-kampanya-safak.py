#!/usr/bin/env python3
"""
MİA PARK OCEAN — "Şafak" kampanya görseli (Zeray tarzı, STORY 1080x1920).

Yapı:
  · en üstte BEYAZ satır: KOCAELİ EV SAHİBİ OLUYOR!
  · altında KIRMIZI kondanse manşet: FAİZ YOK, SIRA YOK / ARA ÖDEME YOK
  · AI ile kadrajlanan dev bina görseli: aile havuzsuz yoldan MİA PARK
    OCEAN kapısına yürüyor, solda kırmızı %0 + altın anahtarlar
  · eğik kırmızı etiket: 29.900 TL'DEN BAŞLAYAN / SABİT TAKSİTLERLE
  · en altta bantsız, doğrudan fotoğraf üstünde: MİA logo · Ocean logo ·
    telefon (gölgeyle)

    python3 scripts/build-kampanya-safak.py
"""

import importlib.util as _il
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "brand-source", "fonts")
GORSEL = os.path.join(ROOT, "sosyal-medya", "turkuaz-kampanya",
                      "kaynak-safak-hero-story.jpg")
OUT = os.path.join(ROOT, "sosyal-medya", "turkuaz-kampanya")

_spec = _il.spec_from_file_location(
    "build_film", os.path.join(ROOT, "scripts", "build-film.py"))
bf = _il.module_from_spec(_spec)
sys.modules["build_film"] = bf
_spec.loader.exec_module(bf)

W, H = 1080, 1920

KIRMIZI = (222, 12, 24)
NAVY = (28, 26, 84)
BEYAZ = (255, 255, 255)


def barlow(s):
    return ImageFont.truetype(os.path.join(FONTS, "BarlowCond-700.ttf"), s)


def manrope(s, w="700"):
    return ImageFont.truetype(os.path.join(FONTS, f"Manrope-{w}.ttf"), s)


def golge_yaz(im, kat_ciz, blur=10, op=160, dx=0, dy=5):
    """Yazı katmanını gölgesiyle bindirir."""
    kat = Image.new("RGBA", im.size, (0, 0, 0, 0))
    kat_ciz(ImageDraw.Draw(kat))
    g = Image.new("RGBA", im.size, (0, 0, 0, 0))
    g.paste(kat.filter(ImageFilter.GaussianBlur(blur)), (dx, dy))
    r, gg, b, a = g.split()
    golge = Image.merge("RGBA", (r.point(lambda v: 8), gg.point(lambda v: 8),
                                 b.point(lambda v: 24),
                                 a.point(lambda v: min(255, int(v * op / 160)))))
    im.alpha_composite(golge)
    im.alpha_composite(kat)


def main():
    hero = Image.open(GORSEL).convert("RGB")
    s = max(W / hero.width, H / hero.height)
    hero = hero.resize((round(hero.width * s), round(hero.height * s)),
                       Image.LANCZOS)
    x = (hero.width - W) // 2
    y = (hero.height - H) // 2
    hero = hero.crop((x, y, x + W, y + H))

    im = hero.convert("RGBA")
    dr = ImageDraw.Draw(im)

    # ---- üst blok: beyaz slogan + kırmızı manşet (story üst güvenli
    # alanının altından başlar)
    def manset(d):
        f0 = barlow(66)
        d.text((W / 2, 168), "KOCAELİ EV SAHİBİ OLUYOR!", font=f0,
               fill=BEYAZ, anchor="ma")
        f1 = barlow(112)
        d.text((W / 2, 252), "FAİZ YOK, SIRA YOK", font=f1, fill=KIRMIZI,
               anchor="ma")
        d.text((W / 2, 368), "ARA ÖDEME YOK", font=f1, fill=KIRMIZI,
               anchor="ma")

    golge_yaz(im, manset, blur=14, op=110, dy=4)

    # ---- eğik etiket: beyaz taban + kırmızı üst, iki satır
    et1 = "29.900 TL'DEN BAŞLAYAN"
    et2 = "SABİT TAKSİTLERLE"
    fe = barlow(58)
    pad_x, pad_y, ara = 36, 10, 4
    w_et = max(dr.textlength(et1, font=fe), dr.textlength(et2, font=fe))
    kw = int(w_et + pad_x * 2)
    kh = int(58 * 2 + pad_y * 2 + ara + 14)
    etiket = Image.new("RGBA", (kw + 40, kh + 40), (0, 0, 0, 0))
    ed = ImageDraw.Draw(etiket)
    ed.rounded_rectangle([12, 12, kw + 28, kh + 28], radius=10, fill=BEYAZ)
    ed.rounded_rectangle([20, 20, kw + 20, kh + 20], radius=8, fill=KIRMIZI)
    ed.text(((kw + 40) / 2, 20 + pad_y + 2), et1, font=fe, fill=BEYAZ,
            anchor="ma")
    ed.text(((kw + 40) / 2, 20 + pad_y + 58 + ara + 2), et2, font=fe,
            fill=BEYAZ, anchor="ma")
    etiket = etiket.rotate(3.2, resample=Image.BICUBIC, expand=True)

    ex = (W - etiket.width) // 2 + 30
    ey = 525
    g = etiket.filter(ImageFilter.GaussianBlur(12))
    r, gg, b, a = g.split()
    golge = Image.merge("RGBA", (r.point(lambda v: 8), gg.point(lambda v: 8),
                                 b.point(lambda v: 20),
                                 a.point(lambda v: int(v * 0.55))))
    im.alpha_composite(golge, (ex + 2, ey + 8))
    im.alpha_composite(etiket, (ex, ey))

    # ---- alt satır: bantsız — BEYAZ logolar + BEYAZ numara, koyu gölge
    alt = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cy = 1826

    mia = bf.logo_white(270)
    alt.alpha_composite(mia, (56, cy - mia.height // 2))

    oc = bf.partner_white(225)
    alt.alpha_composite(oc, ((W - oc.width) // 2 - 70, cy - oc.height // 2))

    ad = ImageDraw.Draw(alt)
    ft = manrope(46, "700")
    tel = "0540 028 00 41"
    tx = W - 52 - ad.textlength(tel, font=ft)
    ad.text((tx, cy), tel, font=ft, fill=BEYAZ, anchor="lm")
    fg = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 52)
    ad.text((tx - 18, cy + 2), "☎", font=fg, fill=BEYAZ, anchor="rm")

    # koyu, yumuşak gölge — beyaz öğeler her zeminde okunsun
    g = alt.filter(ImageFilter.GaussianBlur(16))
    r, gg, b, a = g.split()
    golge = Image.merge("RGBA", (r.point(lambda v: 6), gg.point(lambda v: 12),
                                 b.point(lambda v: 28),
                                 a.point(lambda v: min(255, int(v * 2.0)))))
    im.alpha_composite(golge, (0, 6))
    im.alpha_composite(alt)

    yol = os.path.join(OUT, "kampanya-safak-story.jpg")
    im.convert("RGB").save(yol, quality=93, optimize=True)
    print(f"  → {yol}")


if __name__ == "__main__":
    main()
