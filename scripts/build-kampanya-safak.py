#!/usr/bin/env python3
"""
MİA PARK OCEAN — "Şafak" kampanya görseli (Zeray tarzı kompozisyon).

Yapı (1080x1350):
  · üstte gökyüzüne oturan KIRMIZI kondanse manşet:
        FAİZ YOK, SIRA YOK / ARA ÖDEME YOK
  · altında lacivert soru cümlesi ("faiz indirimini" kırmızı)
  · AI ile yeniden kadrajlanan dev bina görseli (aile + kırmızı %0)
  · sağda eğik beyaz kampanya yazısı: MİA PARK OCEAN'DA /
        KOCAELİ EV SAHİBİ OLUYOR!
  · altta beyaz zeminli eğik kırmızı etiket:
        29.900 TL'DEN BAŞLAYAN / SABİT TAKSİTLERLE
  · en altta beyaz marka bandı: MİA logo · Ocean logo · telefon

    python3 scripts/build-kampanya-safak.py
"""

import math
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "brand-source", "fonts")
GORSEL = os.path.join(ROOT, "sosyal-medya", "turkuaz-kampanya",
                      "kaynak-safak-hero.jpg")
OUT = os.path.join(ROOT, "sosyal-medya", "turkuaz-kampanya")

W, H = 1080, 1350
BAR_H = 150                     # beyaz marka bandı
GOR_H = H - BAR_H               # görsel alanı 1080x1200

KIRMIZI = (222, 12, 24)
KOYU_KIRMIZI = (186, 8, 20)
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
    s = max(W / hero.width, GOR_H / hero.height)
    hero = hero.resize((round(hero.width * s), round(hero.height * s)),
                       Image.LANCZOS)
    x = (hero.width - W) // 2
    # dikeyde ne kadar yukarıdan kesileceği: aile ve anahtarlar kalsın,
    # üstte manşete yetecek kadar gök kalsın diye elle dengelendi
    KIRP_Y = min(140, hero.height - GOR_H)
    hero = hero.crop((x, KIRP_Y, x + W, KIRP_Y + GOR_H))

    im = Image.new("RGBA", (W, H), (*BEYAZ, 255))
    im.paste(hero, (0, 0))

    dr = ImageDraw.Draw(im)

    # ---- manşet: gökyüzünde iki satır kırmızı kondanse
    def manset(d):
        f1 = barlow(108)
        d.text((W / 2, 62), "FAİZ YOK, SIRA YOK", font=f1, fill=KIRMIZI,
               anchor="ma")
        d.text((W / 2, 174), "ARA ÖDEME YOK", font=f1, fill=KIRMIZI,
               anchor="ma")

    golge_yaz(im, manset, blur=14, op=70, dy=4)

    # ---- alt metin: lacivert, "faiz indirimini" kırmızı
    f2 = manrope(30, "700")
    sat1a, sat1b = "Sahip olmak istediğiniz o yuva için ", "faiz indirimini"
    sat2 = "beklemek istediğinize emin misiniz?"

    def altmetin(d):
        w1 = d.textlength(sat1a, font=f2) + d.textlength(sat1b, font=f2)
        x0 = (W - w1) / 2
        d.text((x0, 306), sat1a, font=f2, fill=BEYAZ, anchor="la")
        d.text((x0 + d.textlength(sat1a, font=f2), 306), sat1b, font=f2,
               fill=(255, 96, 96), anchor="la")
        d.text((W / 2, 348), sat2, font=f2, fill=BEYAZ, anchor="ma")

    golge_yaz(im, altmetin, blur=9, op=255, dy=3)

    # ---- sağ blok: eğik beyaz kampanya yazısı
    def kampanya(d):
        pass

    kat = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(kat)
    fk1 = barlow(54)
    fk2 = barlow(88)
    fk3 = barlow(62)
    cx = 700
    kd.text((cx, 742), "MİA PARK OCEAN'DA", font=fk1, fill=BEYAZ, anchor="ms")
    kd.text((cx, 828), "KOCAELİ", font=fk2, fill=BEYAZ, anchor="ms")
    kd.text((cx, 898), "EV SAHİBİ OLUYOR!", font=fk3, fill=BEYAZ, anchor="ms")
    # hafif italik: yatay kaydırma (shear)
    kat = kat.transform((W, H), Image.AFFINE, (1, -0.12, 0, 0, 1, 0),
                        resample=Image.BICUBIC)

    g = kat.filter(ImageFilter.GaussianBlur(10))
    golge = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    golge.paste(g, (2, 6))
    r, gg, b, a = golge.split()
    golge = Image.merge("RGBA", (r.point(lambda v: 6), gg.point(lambda v: 10),
                                 b.point(lambda v: 26), a))
    im.alpha_composite(golge)
    im.alpha_composite(kat)

    # ---- eğik etiket: beyaz taban + kırmızı üst, iki satır
    et1 = "29.900 TL'DEN BAŞLAYAN"
    et2 = "SABİT TAKSİTLERLE"
    fe = barlow(56)
    pad_x, pad_y, ara = 34, 10, 4
    w_et = max(dr.textlength(et1, font=fe), dr.textlength(et2, font=fe))
    kw = int(w_et + pad_x * 2)
    kh = int(56 * 2 + pad_y * 2 + ara + 14)
    etiket = Image.new("RGBA", (kw + 40, kh + 40), (0, 0, 0, 0))
    ed = ImageDraw.Draw(etiket)
    ed.rounded_rectangle([12, 12, kw + 28, kh + 28], radius=10, fill=BEYAZ)
    ed.rounded_rectangle([20, 20, kw + 20, kh + 20], radius=8, fill=KIRMIZI)
    ed.text(((kw + 40) / 2, 20 + pad_y + 2), et1, font=fe, fill=BEYAZ,
            anchor="ma")
    ed.text(((kw + 40) / 2, 20 + pad_y + 56 + ara + 2), et2, font=fe,
            fill=BEYAZ, anchor="ma")
    etiket = etiket.rotate(3.2, resample=Image.BICUBIC, expand=True)

    ex = (W - etiket.width) // 2 + 70
    ey = GOR_H - etiket.height + 44
    g = etiket.filter(ImageFilter.GaussianBlur(12))
    r, gg, b, a = g.split()
    golge = Image.merge("RGBA", (r.point(lambda v: 8), gg.point(lambda v: 8),
                                 b.point(lambda v: 20),
                                 a.point(lambda v: int(v * 0.55))))
    im.alpha_composite(golge, (ex + 2, ey + 8))
    im.alpha_composite(etiket, (ex, ey))

    # ---- beyaz marka bandı
    dr.rectangle([0, GOR_H, W, H], fill=BEYAZ)

    mia = Image.open(os.path.join(ROOT, "public", "brand",
                                  "logo-mia-2026.png")).convert("RGBA")
    mh = 108
    mia = mia.resize((round(mia.width * mh / mia.height), mh), Image.LANCZOS)
    im.alpha_composite(mia, (54, GOR_H + (BAR_H - mh) // 2))

    ocean = Image.open(os.path.join(ROOT, "sunum", "kaynak", "sekil",
                                    "ocean-logo-renkli2.png")).convert("RGBA")
    oh = 72
    ocean = ocean.resize((round(ocean.width * oh / ocean.height), oh),
                         Image.LANCZOS)
    im.alpha_composite(ocean, ((W - ocean.width) // 2 - 80,
                               GOR_H + (BAR_H - oh) // 2))

    ft = manrope(46, "700")
    tel = "0540 028 00 41"
    tx = W - 54 - dr.textlength(tel, font=ft)
    dr.text((tx, GOR_H + BAR_H / 2), tel, font=ft, fill=NAVY, anchor="lm")
    # ahize simgesi: kalın yay + iki uç
    ik = 44
    ax, ay = tx - ik - 20, GOR_H + BAR_H / 2 + 4
    ah = Image.new("RGBA", (ik * 2, ik * 2), (0, 0, 0, 0))
    hd = ImageDraw.Draw(ah)
    hd.arc([8, 14, ik * 2 - 8, ik * 2 + 20], start=200, end=340,
           fill=NAVY, width=13)
    hd.ellipse([2, 24, 26, 48], fill=NAVY)
    hd.ellipse([ik * 2 - 26, 24, ik * 2 - 2, 48], fill=NAVY)
    ah = ah.rotate(0, resample=Image.BICUBIC)
    im.alpha_composite(ah, (int(ax - ik * 0.5), int(ay - ik)))

    yol = os.path.join(OUT, "kampanya-safak-45.jpg")
    im.convert("RGB").save(yol, quality=93, optimize=True)
    print(f"  → {yol}")


if __name__ == "__main__":
    main()
