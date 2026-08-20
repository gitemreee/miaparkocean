#!/usr/bin/env python3
"""
MİA PARK OCEAN — emlakçı sunumu görsel hazırlığı.

Üç iş yapar:

1. FOTOĞRAF KIRPMA. Her render, yerleşeceği kutunun tam pikseline
   en-boy oranı korunarak kırpılır. PowerPoint'e hiçbir görsel
   gerdirilerek verilmez; kutu ile dosya birebir aynı orandadır.
2. PERDE. Tam kanama fotoğrafların üstüne gelen lacivert gradyanlar
   (pptxgenjs gradyan dolgu desteklemiyor).
3. İNFOGRAFİK GEOMETRİSİ. Konum diyagramı ve ulaşım aksının çizgi/nokta
   geometrisi. YAZILAR BURADA ÇİZİLMEZ — etiket çapaları JSON olarak
   dışa verilir, metni build-sunum.js gerçek metin kutusu olarak koyar.
   Böylece sunum açıldığında yazılar düzenlenebilir ve keskin kalır.

    python3 scripts/build-sunum-gorsel.py
"""

import os
import json
import math
import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "public", "images")
OUT = os.path.join(ROOT, "sunum", "kaynak")
FOTO = os.path.join(OUT, "foto")
os.makedirs(FOTO, exist_ok=True)

DPI = 150                      # slayt 13.333 x 7.5 inç -> 2000 x 1125
def px(inch): return int(round(inch * DPI))

# ------------------------------------------------------------ palet
GECE = (6, 25, 43)          # #06192B  en koyu gece mavisi
LACI = (14, 46, 70)         # #0E2E46
KREM = (243, 237, 227)      # #F3EDE3  sıcak kırık beyaz
KREM_K = (230, 220, 203)    # #E6DCCB
ALTIN = (201, 169, 97)      # #C9A961  champagne gold
ALTIN_A = (224, 203, 156)   # #E0CB9C
SU = (111, 168, 190)        # #6FA8BE  çok sınırlı açık mavi
BEYAZ = (255, 255, 255)


# =============================================================== FOTOĞRAF
def kirp(ad, kaynak, w_in, h_in, focus=0.5, zoom=1.0, kalite=88):
    """
    Kaynağı w_in x h_in inçlik kutunun tam pikseline kırpar (cover).
    focus 0..1 kırpma penceresinin konumu; zoom>1 önce büyütür.
    Mimari okunabilir kalsın diye zoom bilerek düşük tutuluyor.
    """
    w, h = px(w_in), px(h_in)
    im = Image.open(os.path.join(SRC, kaynak)).convert("RGB")
    iw, ih = im.size
    s = max(w / iw, h / ih) * max(1.0, zoom)
    nw, nh = max(w, int(round(iw * s))), max(h, int(round(ih * s)))
    im = im.resize((nw, nh), Image.LANCZOS)
    ox, oy = int((nw - w) * focus), int((nh - h) * focus)
    im.crop((ox, oy, ox + w, oy + h)).save(
        os.path.join(FOTO, ad + ".jpg"), quality=kalite, optimize=True)
    return w, h


# ================================================================= PERDE
def perde(ad, w_in, h_in, duraklar, yon="alt", renk=GECE):
    """
    Tek yönlü lacivert gradyan. duraklar = [(konum 0..1, opaklık 0..1), ...]
    yon: alt | ust | sol | sag
    """
    w, h = px(w_in), px(h_in)
    t = np.linspace(0, 1, h if yon in ("alt", "ust") else w, dtype=np.float32)
    if yon in ("ust", "sol"):
        t = 1.0 - t
    a = np.interp(t, [d[0] for d in duraklar], [d[1] for d in duraklar])
    a = (a * 255).astype(np.uint8)
    if yon in ("alt", "ust"):
        alpha = np.repeat(a[:, None], w, axis=1)
    else:
        alpha = np.repeat(a[None, :], h, axis=0)
    rgba = np.zeros((h, w, 4), np.uint8)
    rgba[..., 0], rgba[..., 1], rgba[..., 2] = renk
    rgba[..., 3] = alpha
    Image.fromarray(rgba, "RGBA").save(os.path.join(OUT, ad + ".png"), optimize=True)


# ============================================================ İNFOGRAFİK
def _tuval(w_in, h_in, ss=3):
    w, h = px(w_in) * ss, px(h_in) * ss
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im), ss


def _kaydet(im, ad, w_in, h_in):
    im = im.resize((px(w_in), px(h_in)), Image.LANCZOS)
    im.save(os.path.join(OUT, ad + ".png"), optimize=True)


def konum_diyagram(ad, w_in, h_in, hedefler):
    """
    Merkezde proje, çevresinde hedefler. Sadece GEOMETRİ: halkalar, ince
    altın ışınlar, uç noktalar. Etiketler JSON çapalarıyla dışarıda.
    Işın uzunluğu süreyle orantılı — diyagram bilgi taşıyor, süs değil.
    """
    im, d, ss = _tuval(w_in, h_in)
    W, H = im.size
    cx, cy = W * 0.50, H * 0.52
    rmin, rmax = min(W, H) * 0.145, min(W, H) * 0.400
    ofset = 0.34 * DPI * ss          # etiket bloğu doku bu kadar dışında
    dk_max = max(x["dk"] for x in hedefler)

    # zemin halkaları (dakika ızgarası)
    for k in (0.25, 0.5, 0.75, 1.0):
        r = rmin + (rmax - rmin) * k
        d.ellipse([cx - r, cy - r, cx + r, cy + r],
                  outline=ALTIN + (46,), width=max(1, ss))

    capalar = []
    n = len(hedefler)
    for i, hd in enumerate(hedefler):
        # üstten başla, saat yönünde
        a = -math.pi / 2 + 2 * math.pi * i / n
        r = rmin + (rmax - rmin) * (hd["dk"] / dk_max)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        d.line([cx + rmin * 0.62 * math.cos(a), cy + rmin * 0.62 * math.sin(a), x, y],
               fill=ALTIN + (150,), width=max(1, ss))
        rr = 7 * ss
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=ALTIN + (255,))
        # etiket çapası: ışının biraz dışında
        lx, ly = cx + (r + ofset) * math.cos(a), cy + (r + ofset) * math.sin(a)
        capalar.append({
            "ad": hd["ad"], "dk": hd["dk"],
            "x": lx / W * w_in, "y": ly / H * h_in,
            "hiza": "left" if math.cos(a) > 0.20 else ("right" if math.cos(a) < -0.20 else "center"),
        })

    # merkez: dolu altın disk + halka
    d.ellipse([cx - rmin * 0.60, cy - rmin * 0.60, cx + rmin * 0.60, cy + rmin * 0.60],
              fill=ALTIN + (255,))
    d.ellipse([cx - rmin * 0.80, cy - rmin * 0.80, cx + rmin * 0.80, cy + rmin * 0.80],
              outline=ALTIN + (120,), width=max(1, ss))
    _kaydet(im, ad, w_in, h_in)
    return {"merkez": {"x": cx / W * w_in, "y": cy / H * h_in}, "capalar": capalar}


def aks_diyagram(ad, w_in, h_in, duraklar):
    """İstanbul — MİA PARK OCEAN — Sakarya ulaşım aksı; yatay çizgi."""
    im, d, ss = _tuval(w_in, h_in)
    W, H = im.size
    y = H * 0.50
    x0, x1 = W * 0.07, W * 0.93
    d.line([x0, y, x1, y], fill=ALTIN + (110,), width=max(1, ss))
    capalar = []
    for i, dur in enumerate(duraklar):
        x = x0 + (x1 - x0) * dur["t"]
        r = (13 if dur.get("ana") else 7) * ss
        if dur.get("ana"):
            d.ellipse([x - r * 1.9, y - r * 1.9, x + r * 1.9, y + r * 1.9],
                      outline=ALTIN + (130,), width=max(1, ss))
        d.ellipse([x - r, y - r, x + r, y + r], fill=ALTIN + (255,))
        capalar.append({"ad": dur["ad"], "x": x / W * w_in, "y": y / H * h_in,
                        "ana": bool(dur.get("ana"))})
    _kaydet(im, ad, w_in, h_in)
    return {"capalar": capalar}


# =================================================================== ÜRET
def main():
    veri = {}

    # ---- tam kanama fotoğraflar (16:9 slayt)
    kirp("tam-kapak", "hero-courtyard-dusk.webp", 13.333, 7.5, 0.50)
    kirp("tam-kapanis", "night-gate.webp", 13.333, 7.5, 0.50)
    kirp("tam-mimari", "facade-warm.webp", 13.333, 7.5, 0.50)

    # ---- yarım / sütun fotoğraflar
    kirp("yar-ozet", "entrance-gate.webp", 5.35, 7.5, 0.42, zoom=1.25)
    kirp("yar-mia", "street-corner.webp", 5.10, 7.5, 0.38, zoom=1.30)
    kirp("yar-urun", "ic-mekan/01-1plus0-salon.webp", 4.60, 7.5, 0.50, zoom=1.45)
    kirp("yar-odeme", "balcony-dusk.webp", 4.35, 7.5, 0.55, zoom=1.30)
    kirp("yar-guven", "ic-mekan/16-giris-holu.webp", 4.35, 7.5, 0.50, zoom=1.10)
    kirp("yar-profil", "ic-mekan/05-1plus1-salon.webp", 4.10, 7.5, 0.50, zoom=1.50)
    kirp("ser-arguman", "courtyard-pools.webp", 13.333, 2.10, 0.55)

    # ---- galeri (dergi ızgarası): gündüz/gece dengeli
    kirp("gal-1", "entrance-gate.webp", 7.07, 3.42, 0.45)
    kirp("gal-2", "hero-courtyard-dusk.webp", 3.05, 3.42, 0.50, zoom=1.55)
    kirp("gal-3", "ic-mekan/17-sus-havuzu.webp", 3.05, 3.42, 0.50, zoom=1.15)
    kirp("gal-4", "terrace-pergola.webp", 3.05, 3.42, 0.50, zoom=1.35)
    kirp("gal-5", "balcony-dusk.webp", 3.05, 3.42, 0.50, zoom=1.35)
    kirp("gal-6", "facade-warm.webp", 7.07, 3.42, 0.50)

    # ---- ürün dağılımı görselleri
    kirp("urun-1plus0", "ic-mekan/02-1plus0-mutfak.webp", 5.30, 2.55, 0.50)
    kirp("urun-1plus1", "ic-mekan/06-1plus1-yatak-odasi.webp", 5.30, 2.55, 0.50)

    # ---- perdeler
    perde("perde-kapak", 13.333, 7.5, [(0, 0.30), (0.35, 0.46), (1, 0.86)], "alt")
    perde("perde-kapanis", 13.333, 7.5, [(0, 0.34), (0.30, 0.52), (1, 0.90)], "alt")
    perde("perde-serit", 13.333, 2.10, [(0, 0.86), (1, 0.62)], "sol")
    perde("perde-mimari", 13.333, 7.5, [(0, 0.06), (0.40, 0.22), (0.58, 0.72), (1, 0.94)], "alt")

    # ---- infografikler
    veri["konum"] = konum_diyagram("info-konum", 6.30, 5.30, [
        {"ad": "D100 Karayolu", "dk": 1},
        {"ad": "İzmit Sahili", "dk": 2},
        {"ad": "41 Burada AVM", "dk": 3},
        {"ad": "Şehir Merkezi", "dk": 5},
        {"ad": "Şehir Hastanesi", "dk": 5},
        {"ad": "TEM Otoyolu", "dk": 5},
        {"ad": "Symbol AVM", "dk": 7},
        {"ad": "Kocaeli Üniversitesi", "dk": 10},
    ])
    veri["aks"] = aks_diyagram("info-aks", 11.60, 1.30, [
        {"ad": "İstanbul Anadolu Yakası", "t": 0.00},
        {"ad": "MİA PARK OCEAN · İzmit", "t": 0.55, "ana": True},
        {"ad": "Sakarya", "t": 1.00},
    ])

    with open(os.path.join(OUT, "info.json"), "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, indent=2)
    print("hazir ->", FOTO, "+ perde/infografik ->", OUT)


if __name__ == "__main__":
    main()
