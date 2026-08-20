#!/usr/bin/env python3
"""
MİA PARK OCEAN — emlakçı sunumu görsel hazırlığı (elmas dili).

Referans şablonun görsel dili: elmas (45° döndürülmüş kare) içine
kırpılmış fotoğraflar, ince elmas çerçeveler, kesik çizgiyle bağlanan
adım diyagramları. Elmas ve çizgilerin kendisi PowerPoint'te vektör
şekil olarak duruyor (build-sunum.js); burada yalnızca vektörle
yapılamayanlar üretiliyor:

1. FOTOĞRAF KIRPMA — dikdörtgen: her render, yerleşeceği kutunun tam
   pikseline en-boy oranı korunarak kırpılır. Gerdirme yok.
2. ELMAS FOTOĞRAF — fotoğrafın 45° kare içine maskelenmiş, şeffaf
   zeminli hâli (pptxgenjs görseli şekle maskeleyemiyor).
3. PERDE — tam kanama fotoğrafların üstüne gelen lacivert gradyan.
4. İKON — ince çizgi piktogramlar (altın ve beyaz). Yazı tipi glifine
   güvenmemek için elle çiziliyor.
5. MATERYAL — tabela önizlemeleri, oran KORUNARAK kutuya (contain).

    python3 scripts/build-sunum-gorsel.py
"""

import os
import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "public", "images")
OUT = os.path.join(ROOT, "sunum", "kaynak")
FOTO = os.path.join(OUT, "foto")
SEKIL = os.path.join(OUT, "sekil")
os.makedirs(FOTO, exist_ok=True)
os.makedirs(SEKIL, exist_ok=True)

DPI = 150                       # slayt 13.333 x 7.5 inç -> 2000 x 1125
def px(inch): return int(round(inch * DPI))

# ------------------------------------------------------------ palet
GECE = (6, 25, 43)              # #06192B
LACI = (14, 46, 70)             # #0E2E46
KREM = (243, 237, 227)          # #F3EDE3
ALTIN = (201, 169, 97)          # #C9A961
BEYAZ = (255, 255, 255)


# =============================================================== FOTOĞRAF
def kirp(ad, kaynak, w_in, h_in, focus=0.5, zoom=1.0, kalite=88):
    """Kaynağı w_in x h_in kutunun tam pikseline kırpar (cover)."""
    w, h = px(w_in), px(h_in)
    im = Image.open(os.path.join(SRC, kaynak)).convert("RGB")
    iw, ih = im.size
    s = max(w / iw, h / ih) * max(1.0, zoom)
    nw, nh = max(w, int(round(iw * s))), max(h, int(round(ih * s)))
    im = im.resize((nw, nh), Image.LANCZOS)
    ox, oy = int((nw - w) * focus), int((nh - h) * focus)
    im.crop((ox, oy, ox + w, oy + h)).save(
        os.path.join(FOTO, ad + ".jpg"), quality=kalite, optimize=True)


def elmas(ad, kaynak, boy_in, focus=0.5, zoom=1.0):
    """
    Fotoğrafı elmas (45° kare) içine maskeler; zemin şeffaf.
    Çerçeve elması build-sunum.js kendi vektör şekliyle çiziyor —
    burada yalnızca maskeli fotoğraf var, hizalama JS tarafında
    aynı merkeze oturtularak yapılıyor.
    """
    S = px(boy_in)
    ss = 4
    im = Image.open(os.path.join(SRC, kaynak)).convert("RGB")
    iw, ih = im.size
    k = max(S / iw, S / ih) * max(1.0, zoom)
    nw, nh = max(S, int(round(iw * k))), max(S, int(round(ih * k)))
    im = im.resize((nw, nh), Image.LANCZOS)
    ox, oy = int((nw - S) * focus), int((nh - S) * focus)
    im = im.crop((ox, oy, ox + S, oy + S))
    m = Image.new("L", (S * ss, S * ss), 0)
    d = ImageDraw.Draw(m)
    W = S * ss
    d.polygon([(W // 2, 0), (W, W // 2), (W // 2, W), (0, W // 2)], fill=255)
    m = m.resize((S, S), Image.LANCZOS)
    out = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    out.paste(im, (0, 0), m)
    out.save(os.path.join(SEKIL, ad + ".png"), optimize=True)


# ================================================================= PERDE
def perde(ad, w_in, h_in, duraklar, yon="alt", renk=GECE):
    """Tek yönlü lacivert gradyan. duraklar = [(konum, opaklık), ...]"""
    w, h = px(w_in), px(h_in)
    t = np.linspace(0, 1, h if yon in ("alt", "ust") else w, dtype=np.float32)
    if yon in ("ust", "sol"):
        t = 1.0 - t
    a = (np.interp(t, [d[0] for d in duraklar], [d[1] for d in duraklar]) * 255).astype(np.uint8)
    alpha = np.repeat(a[:, None], w, axis=1) if yon in ("alt", "ust") \
        else np.repeat(a[None, :], h, axis=0)
    rgba = np.zeros((h, w, 4), np.uint8)
    rgba[..., 0], rgba[..., 1], rgba[..., 2] = renk
    rgba[..., 3] = alpha
    Image.fromarray(rgba, "RGBA").save(os.path.join(OUT, ad + ".png"), optimize=True)


# ================================================================ MATERYAL
def malzeme(ad, yol, w_in, h_in):
    """Önizlemeyi oran KORUYARAK kutuya oturtur; beyaz zemin, altın kenar."""
    w, h = px(w_in), px(h_in)
    im = Image.open(os.path.join(ROOT, yol)).convert("RGB")
    iw, ih = im.size
    pad = int(min(w, h) * 0.04)
    s = min((w - 2 * pad) / iw, (h - 2 * pad) / ih)
    nw, nh = int(iw * s), int(ih * s)
    c = Image.new("RGB", (w, h), BEYAZ)
    c.paste(im.resize((nw, nh), Image.LANCZOS), ((w - nw) // 2, (h - nh) // 2))
    d = ImageDraw.Draw(c)
    d.rectangle([0, 0, w - 1, h - 1], outline=ALTIN, width=2)
    c.save(os.path.join(FOTO, ad + ".jpg"), quality=90, optimize=True)


# ================================================================== İKON
def _ikon_tuval(S):
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def ikon(ad, tur, renk):
    """İnce çizgi piktogram; 220px şeffaf PNG, 4x süper örnekleme."""
    S = 880
    im, d = _ikon_tuval(S)
    w = int(S * 0.048)
    c = S / 2
    r = S * 0.30
    R = renk + (255,)

    if tur == "pin":
        d.ellipse([c - r * 0.72, c - r, c + r * 0.72, c + r * 0.42], outline=R, width=w)
        d.polygon([(c - r * 0.30, c + r * 0.20), (c + r * 0.30, c + r * 0.20), (c, c + r)], fill=R)
        d.ellipse([c - r * 0.22, c - r * 0.50, c + r * 0.22, c - r * 0.06], fill=R)
    elif tur == "ev":
        d.polygon([(c - r, c - r * 0.05), (c, c - r * 0.85), (c + r, c - r * 0.05)],
                  outline=R, width=w)
        d.line([c - r * 0.72, c - r * 0.05, c - r * 0.72, c + r * 0.85], fill=R, width=w)
        d.line([c + r * 0.72, c - r * 0.05, c + r * 0.72, c + r * 0.85], fill=R, width=w)
        d.line([c - r * 0.72, c + r * 0.85, c + r * 0.72, c + r * 0.85], fill=R, width=w)
        d.rectangle([c - r * 0.18, c + r * 0.25, c + r * 0.18, c + r * 0.85], outline=R, width=w)
    elif tur == "takvim":
        d.rounded_rectangle([c - r, c - r * 0.72, c + r, c + r * 0.85], radius=r * 0.14,
                            outline=R, width=w)
        d.line([c - r, c - r * 0.25, c + r, c - r * 0.25], fill=R, width=w)
        d.line([c - r * 0.5, c - r, c - r * 0.5, c - r * 0.5], fill=R, width=w)
        d.line([c + r * 0.5, c - r, c + r * 0.5, c - r * 0.5], fill=R, width=w)
        for i in range(3):
            d.ellipse([c - r * 0.55 + i * r * 0.5, c + r * 0.1,
                       c - r * 0.35 + i * r * 0.5, c + r * 0.3], fill=R)
    elif tur == "grafik":
        d.line([c - r, c + r * 0.85, c + r, c + r * 0.85], fill=R, width=w)
        for i, hgt in enumerate((0.45, 0.85, 1.35)):
            x0 = c - r * 0.78 + i * r * 0.62
            d.rectangle([x0, c + r * 0.85 - r * hgt, x0 + r * 0.38, c + r * 0.85],
                        outline=R, width=w)
    elif tur == "banknot":
        d.rounded_rectangle([c - r, c - r * 0.58, c + r, c + r * 0.58], radius=r * 0.12,
                            outline=R, width=w)
        d.ellipse([c - r * 0.32, c - r * 0.32, c + r * 0.32, c + r * 0.32], outline=R, width=w)
        d.line([c - r * 0.68, c - r * 0.02, c - r * 0.52, c - r * 0.02], fill=R, width=w)
        d.line([c + r * 0.52, c - r * 0.02, c + r * 0.68, c - r * 0.02], fill=R, width=w)
    elif tur == "bina":
        d.rectangle([c - r, c - r * 0.55, c - r * 0.08, c + r * 0.85], outline=R, width=w)
        d.rectangle([c + r * 0.08, c - r, c + r, c + r * 0.85], outline=R, width=w)
        for yy in (0.35, 0.0, -0.35):
            d.ellipse([c - r * 0.62, c - yy * r - r * 0.06, c - r * 0.46, c - yy * r + r * 0.10], fill=R)
            d.ellipse([c + r * 0.46, c - yy * r - r * 0.28, c + r * 0.62, c - yy * r - r * 0.12], fill=R)
    elif tur == "anahtar":
        d.ellipse([c - r, c - r * 0.42, c - r * 0.18, c + r * 0.42], outline=R, width=w)
        d.line([c - r * 0.18, c, c + r, c], fill=R, width=w)
        d.line([c + r * 0.55, c, c + r * 0.55, c + r * 0.38], fill=R, width=w)
        d.line([c + r * 0.95, c, c + r * 0.95, c + r * 0.38], fill=R, width=w)
    elif tur == "mail":
        d.rectangle([c - r, c - r * 0.62, c + r, c + r * 0.62], outline=R, width=w)
        d.line([c - r, c - r * 0.62, c, c + r * 0.12], fill=R, width=w)
        d.line([c + r, c - r * 0.62, c, c + r * 0.12], fill=R, width=w)
    elif tur == "telefon":
        d.rounded_rectangle([c - r * 0.55, c - r, c + r * 0.55, c + r], radius=r * 0.22,
                            outline=R, width=w)
        d.line([c - r * 0.2, c + r * 0.68, c + r * 0.2, c + r * 0.68], fill=R, width=w)
    elif tur == "balon":
        d.rounded_rectangle([c - r, c - r * 0.78, c + r, c + r * 0.42], radius=r * 0.26,
                            outline=R, width=w)
        d.polygon([(c - r * 0.35, c + r * 0.42), (c + r * 0.05, c + r * 0.42),
                   (c - r * 0.35, c + r * 0.85)], fill=R)
        for i in range(3):
            d.ellipse([c - r * 0.5 + i * r * 0.5 - r * 0.09, c - r * 0.27,
                       c - r * 0.5 + i * r * 0.5 + r * 0.09, c - r * 0.09], fill=R)
    elif tur == "kalem":
        d.polygon([(c - r * 0.9, c + r * 0.9), (c - r * 0.62, c + r * 0.86),
                   (c + r * 0.72, c - r * 0.48), (c + r * 0.44, c - r * 0.76),
                   (c - r * 0.86, c + r * 0.62)], outline=R, width=w)
        d.line([c + r * 0.3, c - r * 0.62, c + r * 0.58, c - r * 0.34], fill=R, width=w)
    elif tur == "globe":
        d.ellipse([c - r, c - r, c + r, c + r], outline=R, width=w)
        d.ellipse([c - r * 0.45, c - r, c + r * 0.45, c + r], outline=R, width=w)
        d.line([c - r, c, c + r, c], fill=R, width=w)
    elif tur == "insta":
        d.rounded_rectangle([c - r, c - r, c + r, c + r], radius=r * 0.32, outline=R, width=w)
        d.ellipse([c - r * 0.42, c - r * 0.42, c + r * 0.42, c + r * 0.42], outline=R, width=w)
        d.ellipse([c + r * 0.44, c - r * 0.68, c + r * 0.68, c - r * 0.44], fill=R)
    elif tur == "belge":
        d.polygon([(c - r * 0.75, c - r), (c + r * 0.35, c - r), (c + r * 0.75, c - r * 0.6),
                   (c + r * 0.75, c + r), (c - r * 0.75, c + r)], outline=R, width=w)
        d.line([c + r * 0.35, c - r, c + r * 0.35, c - r * 0.6], fill=R, width=w)
        d.line([c + r * 0.35, c - r * 0.6, c + r * 0.75, c - r * 0.6], fill=R, width=w)
        for yy in (-0.2, 0.15, 0.5):
            d.line([c - r * 0.45, c + r * yy, c + r * 0.45, c + r * yy], fill=R, width=w)
    elif tur == "onay":
        d.line([c - r * 0.7, c + r * 0.05, c - r * 0.15, c + r * 0.55], fill=R, width=w)
        d.line([c - r * 0.15, c + r * 0.55, c + r * 0.75, c - r * 0.5], fill=R, width=w)
    elif tur == "kalkan":
        d.polygon([(c - r * 0.85, c - r * 0.7), (c + r * 0.85, c - r * 0.7),
                   (c + r * 0.85, c + r * 0.15), (c, c + r), (c - r * 0.85, c + r * 0.15)],
                  outline=R, width=w)

    im = im.resize((220, 220), Image.LANCZOS)
    im.save(os.path.join(SEKIL, ad + ".png"), optimize=True)


# =================================================================== ÜRET
def main():
    # ---- tam kanama
    kirp("tam-mimari", "facade-warm.webp", 13.333, 7.5, 0.50)
    perde("perde-mimari", 13.333, 7.5, [(0, 0.06), (0.40, 0.22), (0.58, 0.72), (1, 0.94)], "alt")

    # ---- yarım dikdörtgen fotoğraflar (F düzeni: yarı fotoğraf + elmas çerçeve)
    kirp("r-gundem", "entrance-gate.webp", 6.00, 7.5, 0.42, zoom=1.20)
    kirp("r-konum", "street-corner.webp", 5.00, 7.5, 0.38, zoom=1.30)
    kirp("r-1plus0", "ic-mekan/01-1plus0-salon.webp", 5.60, 7.5, 0.50, zoom=1.40)
    kirp("r-1plus1", "ic-mekan/06-1plus1-yatak-odasi.webp", 5.60, 7.5, 0.50, zoom=1.40)
    kirp("r-odeme", "balcony-dusk.webp", 4.60, 7.5, 0.55, zoom=1.30)
    kirp("r-guven", "ic-mekan/16-giris-holu.webp", 4.60, 7.5, 0.50, zoom=1.10)

    # ---- elmas fotoğraflar (şeffaf)
    elmas("e-kapak1", "hero-courtyard-dusk.webp", 3.80, 0.50, zoom=1.15)
    elmas("e-kapak2", "ic-mekan/13-bahceli-daire-terasi.webp", 2.55, 0.50, zoom=1.10)
    elmas("e-ozet", "balcony-dusk.webp", 4.00, 0.50, zoom=1.20)
    elmas("e-neden", "terrace-pergola.webp", 3.90, 0.50, zoom=1.15)
    elmas("e-mia", "ic-mekan/18-yuruyus-yolu.webp", 2.00, 0.50, zoom=1.10)
    elmas("e-profil", "ic-mekan/05-1plus1-salon.webp", 3.70, 0.50, zoom=1.15)
    elmas("e-guven", "ic-mekan/15-balkondan-avlu.webp", 2.00, 0.50, zoom=1.10)
    elmas("e-kapanis1", "night-gate.webp", 3.40, 0.50, zoom=1.15)
    elmas("e-kapanis2", "ic-mekan/21-balkondan-deniz.webp", 2.30, 0.50, zoom=1.10)

    # ---- yaşam / ürün fotoğrafları
    kirp("ya-1", "ic-mekan/17-sus-havuzu.webp", 3.55, 2.25, 0.50, zoom=1.05)
    kirp("ya-2", "ic-mekan/19-cocuk-oyun-parki.webp", 3.55, 2.25, 0.50, zoom=1.05)
    kirp("urun-1plus0", "ic-mekan/03-1plus0-balkon.webp", 5.30, 2.40, 0.50)
    kirp("urun-1plus1", "ic-mekan/05-1plus1-salon.webp", 5.30, 2.40, 0.50)

    # ---- galeri (dergi ızgarası)
    kirp("gal-1", "entrance-gate.webp", 7.07, 3.42, 0.45)
    kirp("gal-2", "ic-mekan/15-balkondan-avlu.webp", 3.05, 3.42, 0.50, zoom=1.15)
    kirp("gal-3", "ic-mekan/19-cocuk-oyun-parki.webp", 3.05, 3.42, 0.50, zoom=1.15)
    kirp("gal-4", "terrace-pergola.webp", 3.05, 3.42, 0.50, zoom=1.35)
    kirp("gal-5", "balcony-dusk.webp", 3.05, 3.42, 0.50, zoom=1.35)
    kirp("gal-6", "facade-warm.webp", 7.07, 3.42, 0.50)

    # ---- materyal önizlemeleri (oran korunarak)
    malzeme("m-bilbord", "tabela/bilbord-mia/onizleme/bilbord-2-kemer.jpg", 3.90, 2.34)
    malzeme("m-arsa", "tabela/arsa-mia/onizleme/arsa-5-duotone.jpg", 2.50, 1.67)
    malzeme("m-rollup", "tabela/fiyat-rollup/onizleme/fiyat-rollup-gunduz-2-fiyatsiz.jpg", 1.30, 2.60)

    # ---- ikonlar
    for t in ["pin", "ev", "takvim", "grafik", "banknot", "bina", "anahtar",
              "mail", "telefon", "balon", "kalem", "globe", "insta", "belge",
              "onay", "kalkan"]:
        ikon("i-" + t + "-altin", t, ALTIN)
        ikon("i-" + t + "-beyaz", t, BEYAZ)

    print("hazir:", FOTO, "+", SEKIL)


if __name__ == "__main__":
    main()
