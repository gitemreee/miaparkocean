#!/usr/bin/env python3
"""
MİA PARK OCEAN × TİLDA İNŞAAT — Emlak Konut tarzı reklam görseli.

Referans düzen (Avrasya Cadde reklamı):
  · üstte beyaz aralıklı slogan: HAYALİNİ KURDUĞUNUZ YAŞAM
  · altında turuncu İZMİT + büyük turuncu degrade MİA PARK OCEAN'DA!
  · beyaz konturlu haplar: peşinat · 60 AY SABİT VADE · 29.900₺ AYLIK TAKSİT
  · altta gün batımı avlu render'ı (tam kanvas) ve logo satırı:
    TİLDA İNŞAAT · MİA PARK OCEAN · OCEAN GAYRİMENKUL + iletişim

Çıktılar: tilda-reklam-story.jpg (1080x1920) + tilda-reklam-kare.jpg (1080x1080)

    python3.13 scripts/build-tilda-reklam.py
"""

import importlib.util as _il
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "brand-source", "fonts")
OUT = os.path.join(ROOT, "sosyal-medya", "turkuaz-kampanya")
HERO = os.path.join(OUT, "kaynak-tilda-dusk.jpg")

_spec = _il.spec_from_file_location(
    "build_film", os.path.join(ROOT, "scripts", "build-film.py"))
bf = _il.module_from_spec(_spec)
sys.modules["build_film"] = bf
_spec.loader.exec_module(bf)

BEYAZ = (255, 255, 255)
SARI = (255, 196, 84)
TURUNCU = (243, 112, 42)
BUZ = (226, 236, 248)


def manrope(s, w="700"):
    return ImageFont.truetype(os.path.join(FONTS, f"Manrope-{w}.ttf"), s)


def track(dr, xy, text, f, fill, sp, anchor="ma"):
    widths = [dr.textlength(c, font=f) for c in text]
    total = sum(widths) + sp * max(len(text) - 1, 0)
    x, y = xy
    if anchor[0] == "m":
        x -= total / 2
    for c, w in zip(text, widths):
        dr.text((x, y), c, font=f, fill=fill)
        x += w + sp
    return total


def degrade_yazi(im, metin, f, cy, ust=SARI, alt=TURUNCU, sp=2):
    """Sarıdan turuncuya dikey degradeli büyük başlık."""
    W = im.width
    kat = Image.new("L", (W, f.size * 2), 0)
    kd = ImageDraw.Draw(kat)
    track(kd, (W / 2, f.size * 0.2), metin, f, 255, sp)
    bbox = kat.getbbox()
    if not bbox:
        return
    grad = Image.new("RGB", (W, f.size * 2))
    gd = ImageDraw.Draw(grad)
    y0, y1 = bbox[1], bbox[3]
    for yy in range(grad.height):
        k = min(max((yy - y0) / max(y1 - y0, 1), 0), 1)
        gd.line([(0, yy), (W, yy)],
                fill=tuple(round(u + (a - u) * k) for u, a in zip(ust, alt)))
    grad.putalpha(kat)
    im.alpha_composite(grad, (0, round(cy - f.size * 0.2)))


def hap(dr, box, r=30):
    dr.rounded_rectangle(box, radius=r, outline=(255, 255, 255, 235),
                         width=4, fill=(8, 14, 54, 96))


def golge(im, kat, blur=12, op=1.4, dy=4):
    g = kat.filter(ImageFilter.GaussianBlur(blur))
    rr, gg, b, a = g.split()
    go = Image.merge("RGBA", (rr.point(lambda v: 4), gg.point(lambda v: 8),
                              b.point(lambda v: 26),
                              a.point(lambda v: min(255, int(v * op)))))
    im.alpha_composite(go, (0, dy))
    im.alpha_composite(kat)


def hero_kirp(W, H, y_oran=0.5):
    hero = Image.open(HERO).convert("RGB")
    s = max(W / hero.width, H / hero.height)
    hero = hero.resize((round(hero.width * s), round(hero.height * s)),
                       Image.LANCZOS)
    x = (hero.width - W) // 2
    y = round((hero.height - H) * y_oran)
    return hero.crop((x, y, x + W, y + H))


def ust_blok(im, y0, olcek=1.0):
    """Slogan + proje adı + üç hap. y0: blok başlangıcı."""
    W = im.width
    dr_ = ImageDraw.Draw(im)

    kat = Image.new("RGBA", im.size, (0, 0, 0, 0))
    kd = ImageDraw.Draw(kat)

    def o(v):
        return round(v * olcek)

    track(kd, (W / 2, y0), "HAYALİNİ KURDUĞUNUZ YAŞAM",
          manrope(o(44), "700"), BEYAZ, o(10))
    track(kd, (W / 2, y0 + o(74)), "İZMİT",
          manrope(o(58), "700"), SARI, o(16))
    golge(im, kat, blur=10, op=1.6, dy=3)

    f_ad = manrope(o(86), "700")
    degrade_yazi(im, "MİA PARK OCEAN'DA!", f_ad, y0 + o(158), sp=o(2))

    # --- haplar
    kat = Image.new("RGBA", im.size, (0, 0, 0, 0))
    kd = ImageDraw.Draw(kat)
    hy = y0 + o(320)

    # geniş hap: peşinat
    hw, hh = o(690), o(132)
    hx = (W - hw) // 2
    hap(kd, [hx, hy, hx + hw, hy + hh], r=o(30))
    fk = manrope(o(26), "700")
    fb = manrope(o(64), "700")
    fa = manrope(o(24), "700")
    sol_x = hx + o(44)
    kd.text((sol_x, hy + o(34)), "1+0", font=manrope(o(34), "700"),
            fill=BEYAZ, anchor="la")
    kd.text((sol_x, hy + o(74)), "DAİRELERDE", font=fk, fill=BEYAZ,
            anchor="la")
    kd.text((hx + hw - o(44), hy + o(22)), "699.000₺", font=fb, fill=BEYAZ,
            anchor="ra")
    kd.text((hx + hw - o(44), hy + o(92)), "'DEN BAŞLAYAN PEŞİNAT", font=fa,
            fill=BUZ, anchor="ra")

    # iki küçük hap
    hy2 = hy + hh + o(22)
    hw2, hh2 = o(332), o(124)
    bosluk = o(26)
    hx1 = (W - hw2 * 2 - bosluk) // 2
    hx2 = hx1 + hw2 + bosluk
    hap(kd, [hx1, hy2, hx1 + hw2, hy2 + hh2], r=o(28))
    kd.text((hx1 + hw2 / 2, hy2 + o(16)), "60 AY", font=manrope(o(52), "700"),
            fill=BEYAZ, anchor="ma")
    kd.text((hx1 + hw2 / 2, hy2 + o(82)), "SABİT VADE", font=fa, fill=BUZ,
            anchor="ma")
    hap(kd, [hx2, hy2, hx2 + hw2, hy2 + hh2], r=o(28))
    kd.text((hx2 + hw2 / 2, hy2 + o(16)), "29.900₺", font=manrope(o(52), "700"),
            fill=BEYAZ, anchor="ma")
    kd.text((hx2 + hw2 / 2, hy2 + o(82)), "AYLIK TAKSİT", font=fa, fill=BUZ,
            anchor="ma")
    golge(im, kat, blur=10, op=1.3, dy=4)
    return hy2 + hh2


def logo_satiri(im, cy, olcek=1.0):
    """Alt logo satırı: Tilda · MİA · Ocean + iletişim."""
    W = im.width

    def o(v):
        return round(v * olcek)

    kat = Image.new("RGBA", im.size, (0, 0, 0, 0))

    tilda = Image.open(os.path.join(ROOT, "public", "brand",
                                    "logo-tilda-beyaz.png")).convert("RGBA")
    th = o(74)
    tilda = tilda.resize((round(tilda.width * th / tilda.height), th),
                         Image.LANCZOS)
    kat.alpha_composite(tilda, (o(56), cy - th // 2))

    mia = bf.logo_white(o(236))
    kat.alpha_composite(mia, ((W - mia.width) // 2, cy - mia.height // 2))

    oc = bf.partner_white(o(206))
    kat.alpha_composite(oc, (W - o(56) - oc.width, cy - oc.height // 2))

    kd = ImageDraw.Draw(kat)
    kd.text((W / 2, cy + o(118)), "0540 028 00 41  ·  www.miaparkocean.com",
            font=manrope(o(31), "700"), fill=BEYAZ, anchor="mm")
    golge(im, kat, blur=14, op=1.8, dy=5)


def story():
    W, H = 1080, 1920
    im = hero_kirp(W, H, 0.5).convert("RGBA")

    # üstte koyu lacivert-mavi degrade perde (referanstaki mavi blok hissi)
    perde = Image.new("L", (1, H), 0)
    pd = ImageDraw.Draw(perde)
    for yy in range(900):
        pd.point((0, yy), fill=int(215 * (1 - yy / 900) ** 1.5))
    mavi = Image.new("RGBA", (W, H), (16, 22, 94, 0))
    mavi.putalpha(perde.resize((W, H)))
    im.alpha_composite(mavi)

    # altta koyu vinyet — logolar okunsun
    perde2 = Image.new("L", (1, H), 0)
    pd2 = ImageDraw.Draw(perde2)
    for yy in range(H - 420, H):
        k = (yy - (H - 420)) / 420
        pd2.point((0, yy), fill=int(180 * k ** 1.4))
    koyu = Image.new("RGBA", (W, H), (6, 10, 30, 0))
    koyu.putalpha(perde2.resize((W, H)))
    im.alpha_composite(koyu)

    ust_blok(im, 170, olcek=1.0)
    logo_satiri(im, 1742, olcek=1.0)

    yol = os.path.join(OUT, "tilda-reklam-story.jpg")
    im.convert("RGB").save(yol, quality=93, optimize=True)
    print(f"  → {yol}")


def kare():
    W, H = 1080, 1080
    im = hero_kirp(W, H, 0.44).convert("RGBA")

    perde = Image.new("L", (1, H), 0)
    pd = ImageDraw.Draw(perde)
    for yy in range(640):
        pd.point((0, yy), fill=int(225 * (1 - yy / 640) ** 1.4))
    mavi = Image.new("RGBA", (W, H), (16, 22, 94, 0))
    mavi.putalpha(perde.resize((W, H)))
    im.alpha_composite(mavi)

    perde2 = Image.new("L", (1, H), 0)
    pd2 = ImageDraw.Draw(perde2)
    for yy in range(H - 300, H):
        k = (yy - (H - 300)) / 300
        pd2.point((0, yy), fill=int(190 * k ** 1.4))
    koyu = Image.new("RGBA", (W, H), (6, 10, 30, 0))
    koyu.putalpha(perde2.resize((W, H)))
    im.alpha_composite(koyu)

    ust_blok(im, 64, olcek=0.86)
    logo_satiri(im, 952, olcek=0.82)

    yol = os.path.join(OUT, "tilda-reklam-kare.jpg")
    im.convert("RGB").save(yol, quality=93, optimize=True)
    print(f"  → {yol}")


if __name__ == "__main__":
    story()
    kare()
