#!/usr/bin/env python3
"""
MİA PARK OCEAN — turkuaz-01 "KOCAELİ EV SAHİBİ OLUYOR!" tasarımının
3 x 5 metre TEK PANO sürümü (5000 x 3000 mm).

16 m sürümüyle aynı dil, 5:3 oranına uyarlanmış:
- gök-buz gradyan; giriş kapısı fotoğrafı ALTTA çerçevesiz, zemine karışır
- beyazlaşan köşelerde kendi renklerinde MİA (solda) + OCEAN (sağda)
- KOCAELİ EV SAHİBİ OLUYOR! + kırmızı YOK çipleri + 1+0/1+1 kartları +
  kırmızı 60 AY SABİT TAKSİT! burgusu
- altta foto üzerinde beyaz "Satış Ofisi: numara | web | sosyal" satırı

ÇIKTI: JPEG 1:1 ölçekte 40 dpi = 7874 x 4724 px (dpi gömülü);
kilitli PSD 1:10 ölçek (500 x 300 mm) @ 200 dpi = 3937 x 2362 px.

    python3 scripts/build-bilbord-3x5-turkuaz.py
"""

import importlib.util
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _yukle(ad, dosya):
    spec = importlib.util.spec_from_file_location(
        ad, os.path.join(ROOT, "scripts", dosya))
    m = importlib.util.module_from_spec(spec)
    sys.modules[ad] = m
    spec.loader.exec_module(m)
    return m


b16 = _yukle("b16", "build-bilbord-16m.py")
tz = _yukle("tz", "build-bilbord-16m-turkuaz.py")

mont, sigdir, psd_yaz, yildiz = b16.mont, b16.sigdir, b16.psd_yaz, b16.yildiz
PETROL, BEYAZ, TURKUAZ_K = tz.PETROL, tz.BEYAZ, tz.TURKUAZ_K
TEL, SITE = tz.TEL, tz.SITE

W, H, DPI = 7874, 4724, 40           # 5000 x 3000 mm @ 40 dpi
PAD = 340
Z_UST, Z_ALT = (255, 255, 255), (224, 246, 248)
OUT = os.path.join(ROOT, "tabela", "bilbord-16m-turkuaz")


def zemin(ust=Z_UST, alt=Z_ALT):
    t = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    g = (np.array(ust, np.float32) * (1 - t)
         + np.array(alt, np.float32) * t).astype(np.uint8)
    im = Image.new("RGBA", (W, H))
    im.paste(Image.fromarray(np.repeat(g, W, axis=1), "RGB"), (0, 0))
    return im


def foto_alt(im, yuk, bl=280, ad="entrance-gate.webp", ust=Z_UST, alt=Z_ALT):
    from PIL import ImageFilter
    kay = Image.open(os.path.join(ROOT, "public", "images", ad)).convert("RGB")
    iw, ih = kay.size
    s = max(W / iw, yuk / ih) * 1.05
    sw, sh = W / s, yuk / s
    ox = (iw - sw) * 0.5
    oy = (ih - sh) * 0.45
    ft = kay.crop((int(ox), int(oy), int(ox + sw), int(oy + sh)))
    ft = ft.resize((W, yuk), Image.LANCZOS)
    if s > 1.6:
        ft = ft.filter(ImageFilter.UnsharpMask(radius=3, percent=52, threshold=3))
    im.paste(ft, (0, H - yuk))
    t = (H - yuk) / H
    zc = np.array([u * (1 - t) + a * t for u, a in zip(ust, alt)], np.float32)
    band = np.asarray(ft.crop((0, 0, W, bl)), np.float32)
    alfa = np.linspace(1, 0, bl, dtype=np.float32)[:, None, None]
    kar = (zc * alfa + band * (1 - alfa)).astype(np.uint8)
    im.paste(Image.fromarray(kar, "RGB"), (0, H - yuk))


def logolar(im):
    kat = tz._kose_kat()
    R = kat.width // 2
    im.alpha_composite(kat, (PAD + 480 - R, 280 - R))
    im.alpha_composite(kat, (W - PAD - 480 - R, 280 - R))
    lg = Image.open(os.path.join(ROOT, "public", "brand",
                                 "logo-mia-2026.png")).convert("RGBA")
    lg = lg.resize((950, int(lg.height * 950 / lg.width)), Image.LANCZOS)
    im.alpha_composite(lg, (PAD, 70))
    og = Image.open(os.path.join(ROOT, "sunum", "kaynak", "sekil",
                                 "ocean-logo-renkli2.png")).convert("RGBA")
    og = og.resize((880, int(og.height * 880 / og.width)), Image.LANCZOS)
    im.alpha_composite(og, (W - PAD - 880, 130))


def iletisim(dr, cy, acik=False, boy=200):
    while boy > 60:
        fe, f = mont("SemiBold", boy), mont("Bold", boy)
        ik = int(boy * 1.05)
        bosluk = int(boy * 1.15)
        w_l = dr.textlength("Satış Ofisi:", font=fe)
        w_t = dr.textlength(TEL, font=f)
        w_s = dr.textlength(SITE, font=f)
        w_h = dr.textlength("miaparkocean", font=f)
        w_sos = ik * 2 + int(boy * 0.5) + int(boy * 0.55) + w_h
        toplam = w_l + boy * 0.8 + w_t + (bosluk * 2 + 5) * 2 + w_s + w_sos
        if toplam <= W - 2 * PAD:
            break
        boy -= 4
    kal = max(3, int(boy * 0.09))
    r1 = (46, 96, 106) if acik else (214, 234, 238)
    r2 = PETROL if acik else BEYAZ
    r3 = (110, 150, 160) if acik else (200, 222, 228)
    x = W / 2 - toplam / 2
    dr.text((x, cy), "Satış Ofisi:", font=fe, fill=r1, anchor="lm")
    x += w_l + boy * 0.8
    dr.text((x, cy), TEL, font=f, fill=r2, anchor="lm")
    x += w_t + bosluk
    dr.line([(x, cy - boy * 0.62), (x, cy + boy * 0.62)], fill=r3, width=5)
    x += 5 + bosluk
    dr.text((x, cy), SITE, font=f, fill=r2, anchor="lm")
    x += w_s + bosluk
    dr.line([(x, cy - boy * 0.62), (x, cy + boy * 0.62)], fill=r3, width=5)
    x += 5 + bosluk
    dr.rounded_rectangle([x, cy - ik / 2, x + ik, cy + ik / 2],
                         radius=int(ik * 0.24), outline=r2, width=kal)
    dr.ellipse([x + ik * 0.26, cy - ik * 0.24, x + ik * 0.74, cy + ik * 0.24],
               outline=r2, width=kal)
    dr.ellipse([x + ik * 0.70, cy - ik * 0.40, x + ik * 0.87, cy - ik * 0.23],
               fill=r2)
    x += ik + int(boy * 0.5)
    dr.rounded_rectangle([x, cy - ik / 2, x + ik, cy + ik / 2],
                         radius=int(ik * 0.24), outline=r2, width=kal)
    dr.text((x + ik * 0.55, cy + 4), "f", font=mont("Bold", int(ik * 0.8)),
            fill=r2, anchor="mm")
    x += ik + int(boy * 0.55)
    dr.text((x, cy), "miaparkocean", font=f, fill=r2, anchor="lm")


def _ciktilar(im, ad):
    rgb = im.convert("RGB")
    p = os.path.join(OUT, ad + ".jpg")
    rgb.save(p, "JPEG", quality=92, optimize=True, dpi=(DPI, DPI))
    kucuk = rgb.copy()
    kucuk.thumbnail((1500, 1500), Image.LANCZOS)
    kucuk.save(os.path.join(OUT, "onizleme", ad + ".jpg"),
               quality=86, optimize=True)
    ps = rgb.resize((3937, 2362), Image.LANCZOS)
    pp = os.path.join(OUT, "psd", ad + ".psd")
    psd_yaz(ps, pp, 200)
    print("   %s  jpg %.1f MB · psd %.1f MB"
          % (ad, os.path.getsize(p) / 1e6, os.path.getsize(pp) / 1e6))


def proje_alani():
    """3x5 arsa panosu: logolar + PROJE ALANI + iletişim — başka öğe yok."""
    im = zemin()
    logolar(im)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 2160), "PROJE ALANI",
            font=sigdir(dr, "PROJE ALANI", "Black", 950, W - 2 * PAD),
            fill=PETROL, anchor="mm")
    dr.rounded_rectangle([W / 2 - 850, 2800, W / 2 + 850, 2842], radius=21,
                         fill=tz.TURKUAZ + (255,))
    iletisim(dr, H - 430, acik=True, boy=250)
    _ciktilar(im, "turkuaz-proje-alani-3x5")


def gece():
    """16 m'deki turkuaz-09'un 3x5 sürümü — FİYATSIZ marka panosu.
    İletişim satırı fotoğrafın değil, temiz petrol zeminin üzerinde."""
    U, A = (3, 48, 56), (0, 96, 108)
    im = zemin(U, A)
    foto_alt(im, 2300, bl=380, ad="night-gate.webp", ust=U, alt=A)
    logolar(im)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 1010), "KOCAELİ EV SAHİBİ OLUYOR!",
            font=sigdir(dr, "KOCAELİ EV SAHİBİ OLUYOR!", "Black", 470,
                        W - 2 * PAD), fill=BEYAZ, anchor="mm")
    tz.yok_satiri(dr, W / 2, 1520, boy=230, ara=190)
    iletisim(dr, 2080, boy=240)
    yildiz(im, W - 1150, 3100, 700, ["60 AY", "SABİT", "TAKSİT!"], don=10)
    _ciktilar(im, "turkuaz-09-gece-3x5")


def main():
    """Gündüz Kocaeli — gece ile aynı FİYATSIZ düzen, açık zemin."""
    im = zemin()
    foto_alt(im, 2300, bl=340)
    logolar(im)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 1010), "KOCAELİ EV SAHİBİ OLUYOR!",
            font=sigdir(dr, "KOCAELİ EV SAHİBİ OLUYOR!", "Black", 470,
                        W - 2 * PAD), fill=PETROL, anchor="mm")
    tz.yok_satiri(dr, W / 2, 1520, boy=230, ara=190)
    iletisim(dr, 2080, acik=True, boy=240)
    yildiz(im, W - 1150, 3100, 700, ["60 AY", "SABİT", "TAKSİT!"], don=10)
    _ciktilar(im, "turkuaz-01-kocaeli-3x5")


if __name__ == "__main__":
    main()
    proje_alani()
    gece()
