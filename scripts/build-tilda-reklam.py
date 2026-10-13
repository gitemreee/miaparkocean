#!/usr/bin/env python3
"""
MİA PARK OCEAN × TİLDA İNŞAAT — Emlak Konut (Avrasya Cadde) tarzı reklam.

Görsel GERÇEK proje render'ı: signage-source/night-gate.jpg (4K, gün
batımı, 4 blok + MİA PARK OCEAN kapısı). Yapay zekâ görüntüsü kullanılmaz.

Düzen (referansla aynı):
  · üst: kraliyet mavisi degrade gök, render'ın kendi gün batımı göğüne
    yumuşakça bağlanır
  · beyaz Montserrat Bold: HAYALİNİ KURDUĞUNUZ YAŞAM
  · turuncu degrade Montserrat ExtraBold: İZMİT / MİA PARK OCEAN'DA!
  · ince beyaz konturlu haplar: 1+0 peşinat · 60 AY VADE · aylık taksit
  · render, altı siyaha kararır; logo satırı Tilda · MİA · Ocean

Çıktı: tilda-reklam-story.jpg (1080x1920), tilda-reklam-kare.jpg (1080x1080)

    python3.13 scripts/build-tilda-reklam.py
"""

import importlib.util as _il
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "brand-source", "fonts")
OUT = os.path.join(ROOT, "sosyal-medya", "turkuaz-kampanya")
RENDER = os.path.join(ROOT, "signage-source", "night-gate-temiz.jpg")
if not os.path.exists(RENDER):
    RENDER = os.path.join(ROOT, "signage-source", "night-gate.jpg")

_spec = _il.spec_from_file_location(
    "build_film", os.path.join(ROOT, "scripts", "build-film.py"))
bf = _il.module_from_spec(_spec)
sys.modules["build_film"] = bf
_spec.loader.exec_module(bf)

BEYAZ = (255, 255, 255)
MAVI_UST = (6, 18, 92)        # gök tepesi — kraliyet mavisi
MAVI_ALT = (30, 64, 168)      # render göğüne bağlanan açık mavi
TURUNCU_SOL = (242, 78, 52)   # kırmızımsı turuncu
TURUNCU_SAG = (246, 186, 48)  # altın sarısı


def mont(s, agirlik=700):
    f = ImageFont.truetype(os.path.join(FONTS, "Montserrat-var.ttf"), s)
    f.set_variation_by_axes([agirlik])
    return f


def harf_aralikli(dr, xy, metin, f, fill, sp, anchor="ma"):
    gen = [dr.textlength(c, font=f) for c in metin]
    top = sum(gen) + sp * (len(metin) - 1)
    x, y = xy
    if anchor[0] == "m":
        x -= top / 2
    for c, w in zip(metin, gen):
        dr.text((x, y), c, font=f, fill=fill, anchor="la")
        x += w + sp
    return top


def degrade_yazi(im, xy, metin, f, sol=TURUNCU_SOL, sag=TURUNCU_SAG, sp=0):
    """Soldan sağa turuncu→altın degrade yazı (referanstaki başlık)."""
    W, H = im.size
    maske = Image.new("L", (W, H), 0)
    harf_aralikli(ImageDraw.Draw(maske), xy, metin, f, 255, sp)
    kutu = maske.getbbox()
    if not kutu:
        return
    x0, x1 = kutu[0], kutu[2]
    xs = np.clip((np.arange(W) - x0) / max(x1 - x0, 1), 0, 1)[None, :, None]
    s, g = np.array(sol, np.float32), np.array(sag, np.float32)
    renk = (s + (g - s) * xs) * np.ones((H, 1, 1), np.float32)
    kat = Image.fromarray(renk.astype(np.uint8), "RGB").convert("RGBA")
    kat.putalpha(maske)
    golge_bas(im, kat, blur=10, op=1.0, dy=4)


def golge_bas(im, kat, blur=12, op=1.2, dy=4):
    g = kat.filter(ImageFilter.GaussianBlur(blur))
    a = g.split()[3].point(lambda v: min(255, int(v * op)))
    koyu = Image.new("RGBA", im.size, (2, 6, 34, 0))
    koyu.putalpha(a)
    im.alpha_composite(koyu, (0, dy))
    im.alpha_composite(kat)


def zemin(W, H, render_y, render_w):
    """Mavi degrade gök + gerçek render bandı + siyaha kararan alt."""
    gok = np.zeros((H, 1, 3), np.float32)
    for y in range(H):
        k = min(y / max(render_y + 120, 1), 1.0) ** 1.1
        gok[y, 0] = np.array(MAVI_UST) + (np.array(MAVI_ALT) - MAVI_UST) * k
    im = Image.fromarray(np.repeat(gok, W, axis=1).astype(np.uint8),
                         "RGB").convert("RGBA")

    r = Image.open(RENDER).convert("RGB")
    rh = round(r.height * render_w / r.width)
    r = r.resize((render_w, rh), Image.LANCZOS)
    x = (render_w - W) // 2
    r = r.crop((x, 0, x + W, rh)).convert("RGBA")

    # render'ın üst kenarı (göğü) mavi zemine eriyerek bağlansın
    erime = round(rh * 0.30)
    a = np.full((rh, W), 255, np.float32)
    for y in range(erime):
        a[y, :] = 255 * (y / erime) ** 1.6
    r.putalpha(Image.fromarray(a.astype(np.uint8), "L"))
    im.alpha_composite(r, (0, render_y))

    # alt: render'ın altından siyaha
    alt0 = render_y + round(rh * 0.64)
    alt1 = min(render_y + rh, H)          # render bitmeden tam siyah
    karart = np.zeros((H, W), np.float32)
    for y in range(alt0, H):
        karart[y, :] = min(1.0, (y - alt0) / max(alt1 - alt0, 1)) ** 1.15
    siyah = Image.new("RGBA", (W, H), (2, 3, 10, 0))
    siyah.putalpha(Image.fromarray((karart * 255).astype(np.uint8), "L"))
    im.alpha_composite(siyah)
    return im


def hap(dr, kutu, r):
    dr.rounded_rectangle(kutu, radius=r, outline=(255, 255, 255, 240),
                         width=3, fill=(10, 24, 110, 70))


def basliklar(im, y0, o):
    W = im.width
    kat = Image.new("RGBA", im.size, (0, 0, 0, 0))
    harf_aralikli(ImageDraw.Draw(kat), (W / 2, y0),
                  "HAYALİNİ KURDUĞUNUZ YAŞAM", mont(o(40), 700), BEYAZ, o(2))
    golge_bas(im, kat, blur=8, op=1.0, dy=3)
    degrade_yazi(im, (W / 2, y0 + o(66)), "İZMİT", mont(o(64), 800),
                 sp=o(2))
    degrade_yazi(im, (W / 2, y0 + o(146)), "MİA PARK OCEAN'DA!",
                 mont(o(76), 800), sp=0)
    return y0 + o(146) + o(76)


def haplar(im, y0, o, tip, pesinat, taksit):
    W = im.width
    kat = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(kat)

    # geniş hap
    hw, hh = o(610), o(128)
    hx = (W - hw) // 2
    hap(d, [hx, y0, hx + hw, y0 + hh], o(34))
    fk = mont(o(22), 500)
    d.text((hx + o(184), y0 + o(30)), f"{tip} DAİRENİN", font=fk, fill=BEYAZ,
           anchor="ra")
    d.text((hx + o(184), y0 + o(58)), "FİYATI", font=fk, fill=BEYAZ,
           anchor="ra")
    d.text((hx + o(198), y0 + o(12)), pesinat, font=mont(o(66), 700),
           fill=BEYAZ, anchor="la")
    d.text((hx + o(210), y0 + o(88)), "'DEN BAŞLAYAN PEŞİNAT",
           font=mont(o(22), 500), fill=BEYAZ, anchor="la")

    # iki küçük hap
    y1 = y0 + hh + o(20)
    hh2 = o(122)
    w1, w2, ara = o(226), o(364), o(20)
    x1 = (W - w1 - w2 - ara) // 2
    x2 = x1 + w1 + ara
    hap(d, [x1, y1, x1 + w1, y1 + hh2], o(34))
    d.text((x1 + w1 / 2, y1 + o(16)), "60 AY", font=mont(o(58), 700),
           fill=BEYAZ, anchor="ma")
    d.text((x1 + w1 / 2, y1 + o(84)), "VADE", font=mont(o(22), 500),
           fill=BEYAZ, anchor="ma")
    hap(d, [x2, y1, x2 + w2, y1 + hh2], o(34))
    d.text((x2 + w2 / 2, y1 + o(16)), taksit, font=mont(o(58), 700),
           fill=BEYAZ, anchor="ma")
    d.text((x2 + w2 / 2, y1 + o(84)), "AYLIK TAKSİT", font=mont(o(22), 500),
           fill=BEYAZ, anchor="ma")
    golge_bas(im, kat, blur=10, op=0.9, dy=3)


def logolar(im, cy, o, iletisim_y=None):
    W = im.width
    kat = Image.new("RGBA", im.size, (0, 0, 0, 0))
    tilda = Image.open(os.path.join(ROOT, "public", "brand",
                                    "logo-tilda-beyaz.png")).convert("RGBA")
    th = o(58)
    tilda = tilda.resize((round(tilda.width * th / tilda.height), th),
                         Image.LANCZOS)
    kat.alpha_composite(tilda, (o(60), cy - th // 2))
    mia = bf.logo_white(o(210))
    kat.alpha_composite(mia, ((W - mia.width) // 2, cy - mia.height // 2))
    oc = bf.partner_white(o(190))
    kat.alpha_composite(oc, (W - o(60) - oc.width, cy - oc.height // 2))
    if iletisim_y is not None:
        harf_aralikli(ImageDraw.Draw(kat), (W / 2, iletisim_y),
                      "0540 028 00 41   ·   MIAPARKOCEAN.COM",
                      mont(o(26), 600), (220, 228, 245), o(2))
    golge_bas(im, kat, blur=8, op=0.8, dy=2)


def uret(W, H, olcek, baslik_y, render_y, render_w, logo_y, iletisim_y, ad,
         tip, pesinat, taksit):
    def o(v):
        return round(v * olcek)

    im = zemin(W, H, render_y, render_w)
    son = basliklar(im, baslik_y, o)
    haplar(im, son + o(36), o, tip, pesinat, taksit)
    logolar(im, logo_y, o, iletisim_y)
    yol = os.path.join(OUT, ad)
    im.convert("RGB").save(yol, quality=94, optimize=True)
    print(f"  → {yol}")


DAIRELER = [("1+0", "699.000₺", "29.900₺", "1plus0"),
            ("1+1", "999.000₺", "39.900₺", "1plus1")]

if __name__ == "__main__":
    for tip, pesinat, taksit, ek in DAIRELER:
        uret(1080, 1920, 1.0, baslik_y=230, render_y=600, render_w=1860,
             logo_y=1700, iletisim_y=1812, ad=f"tilda-reklam-{ek}-story.jpg",
             tip=tip, pesinat=pesinat, taksit=taksit)
        uret(1080, 1080, 0.80, baslik_y=54, render_y=330, render_w=1420,
             logo_y=930, iletisim_y=1010, ad=f"tilda-reklam-{ek}-kare.jpg",
             tip=tip, pesinat=pesinat, taksit=taksit)
