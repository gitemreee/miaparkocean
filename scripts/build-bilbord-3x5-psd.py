#!/usr/bin/env python3
"""
MİA PARK OCEAN — 3x5 panoların KATMANLI (düzenlenebilir) PSD'leri.

build-bilbord-3x5-turkuaz.py'deki üç tasarımın her öğesi AYRI KATMAN
olarak yazılır: zemin, foto, köşe ışıkları, mia-logo, ocean-logo,
manşet, yok-çipleri, iletişim, burgu... Photoshop'ta katmanlar tek tek
taşınabilir/silinebilir/değiştirilebilir.

NOT: Metin katmanları rasterdir (gerçek yazı katmanı değil) — yazıyı
değiştirmek için katmanı silip Montserrat ile yeniden yazın; fontlar
sunum/yazitipi/ klasöründe ve teslim zip'lerinde birlikte verilir.

ÇIKTI: tabela/bilbord-16m-turkuaz/psd-katmanli/*.psd
1:10 ölçek (500 x 300 mm) @ 200 dpi = 3937 x 2362 px, RLE sıkıştırma.

    python3 scripts/build-bilbord-3x5-psd.py
"""

import importlib.util
import os
import struct
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
b35 = _yukle("b35", "build-bilbord-3x5-turkuaz.py")

W, H = b35.W, b35.H
PAD = b35.PAD
PSD_W, PSD_H, PSD_DPI = 3937, 2362, 200
OUT = os.path.join(ROOT, "tabela", "bilbord-16m-turkuaz", "psd-katmanli")
os.makedirs(OUT, exist_ok=True)


# ═══════════════════════════════════════════ katmanlı PSD yazıcı
def _rle_satir(satir):
    n = len(satir)
    if n and satir.min() == satir.max():
        dolu, kalan, v = [], n, int(satir[0])
        while kalan:
            L = min(128, kalan)
            dolu.append(bytes((257 - L, v)))
            kalan -= L
        return b"".join(dolu)
    parca, b = [], satir.tobytes()
    for i in range(0, n, 128):
        blok = b[i:i + 128]
        parca.append(bytes((len(blok) - 1,)) + blok)
    return b"".join(parca)


def _kanal_rle(arr2d):
    satirlar = [_rle_satir(arr2d[y]) for y in range(arr2d.shape[0])]
    tablo = b"".join(struct.pack(">H", len(s)) for s in satirlar)
    return struct.pack(">H", 1) + tablo + b"".join(satirlar)


def _ad_pascal(ad):
    b = ad.encode("ascii", "replace")[:255]
    p = bytes((len(b),)) + b
    while len(p) % 4:
        p += b"\x00"
    return p


def psd_katmanli(yol, katmanlar, dpi):
    """katmanlar: [(ad, PIL RGBA tam kanvas)] ALTTAN ÜSTE sırayla."""
    kayit = []
    for ad, im in katmanlar:
        bbox = im.getbbox()
        if bbox is None:
            continue
        arr = np.asarray(im.crop(bbox))
        kayit.append((ad, bbox, arr))

    birlesik = Image.new("RGBA", (PSD_W, PSD_H), (255, 255, 255, 255))
    for _, im in katmanlar:
        birlesik = Image.alpha_composite(birlesik, im)
    komp = np.asarray(birlesik.convert("RGB"))

    govdeler = []
    kayitlar = []
    for ad, (x0, y0, x1, y1), arr in kayit:
        kanallar = []
        for cid, idx in [(0, 0), (1, 1), (2, 2), (-1, 3)]:
            veri = _kanal_rle(np.ascontiguousarray(arr[..., idx]))
            kanallar.append((cid, veri))
        r = struct.pack(">iiii", y0, x0, y1, x1)
        r += struct.pack(">H", 4)
        for cid, veri in kanallar:
            r += struct.pack(">hI", cid, len(veri))
        r += b"8BIM" + b"norm"
        r += bytes((255, 0, 0, 0))          # opaklık, kırpma, bayrak, dolgu
        ekstra = struct.pack(">I", 0) + struct.pack(">I", 0) + _ad_pascal(ad)
        r += struct.pack(">I", len(ekstra)) + ekstra
        kayitlar.append(r)
        govdeler.append(b"".join(v for _, v in kanallar))

    katman_bilgi = struct.pack(">h", len(kayit))
    katman_bilgi += b"".join(kayitlar) + b"".join(govdeler)
    if len(katman_bilgi) % 2:
        katman_bilgi += b"\x00"
    bolum = struct.pack(">I", len(katman_bilgi)) + katman_bilgi \
        + struct.pack(">I", 0)              # global maske yok

    with open(yol, "wb") as f:
        f.write(b"8BPS")
        f.write(struct.pack(">H6xHIIHH", 1, 3, PSD_H, PSD_W, 8, 3))
        f.write(struct.pack(">I", 0))
        coz = struct.pack(">IHHIHH", dpi << 16, 1, 2, dpi << 16, 1, 2)
        blok = b"8BIM" + struct.pack(">H", 1005) + b"\x00\x00" \
            + struct.pack(">I", len(coz)) + coz
        f.write(struct.pack(">I", len(blok)))
        f.write(blok)
        f.write(struct.pack(">I", len(bolum)))
        f.write(bolum)
        f.write(struct.pack(">H", 1))
        kanallar = [[_rle_satir(np.ascontiguousarray(komp[y, :, c]))
                     for y in range(PSD_H)] for c in range(3)]
        for kanal in kanallar:
            f.write(b"".join(struct.pack(">H", len(s)) for s in kanal))
        for kanal in kanallar:
            f.write(b"".join(kanal))


# ═══════════════════════════════════════════ katman üretimi
def _bos():
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def _kucult(im):
    return im.resize((PSD_W, PSD_H), Image.LANCZOS)


def _logolar_katman():
    kose = _bos()
    kat = tz._kose_kat()
    R = kat.width // 2
    kose.alpha_composite(kat, (PAD + 480 - R, 280 - R))
    kose.alpha_composite(kat, (W - PAD - 480 - R, 280 - R))
    mia = _bos()
    lg = Image.open(os.path.join(ROOT, "public", "brand",
                                 "logo-mia-2026.png")).convert("RGBA")
    lg = lg.resize((950, int(lg.height * 950 / lg.width)), Image.LANCZOS)
    mia.alpha_composite(lg, (PAD, 70))
    oce = _bos()
    og = Image.open(os.path.join(ROOT, "sunum", "kaynak", "sekil",
                                 "ocean-logo-renkli2.png")).convert("RGBA")
    og = og.resize((880, int(og.height * 880 / og.width)), Image.LANCZOS)
    oce.alpha_composite(og, (W - PAD - 880, 130))
    return [("kose-isik", kose), ("mia-logo", mia), ("ocean-logo", oce)]


def _kampanya(gece):
    if gece:
        U, A = (3, 48, 56), (0, 96, 108)
        foto_ad, metin = "night-gate.webp", b35.BEYAZ
    else:
        U, A = b35.Z_UST, b35.Z_ALT
        foto_ad, metin = "entrance-gate.webp", b35.PETROL
    zem = b35.zemin(U, A)
    fot = _bos()
    b35.foto_alt(fot, 2300, bl=380 if gece else 340, ad=foto_ad, ust=U, alt=A)
    katmanlar = [("zemin", zem), ("foto", fot)] + _logolar_katman()
    man = _bos()
    dr = ImageDraw.Draw(man)
    dr.text((W / 2, 1010), "KOCAELİ EV SAHİBİ OLUYOR!",
            font=b35.sigdir(dr, "KOCAELİ EV SAHİBİ OLUYOR!", "Black", 470,
                            W - 2 * PAD), fill=metin, anchor="mm")
    katmanlar.append(("manset", man))
    yok = _bos()
    tz.yok_satiri(ImageDraw.Draw(yok), W / 2, 1520, boy=230, ara=190)
    katmanlar.append(("yok-cipleri", yok))
    ilt = _bos()
    b35.iletisim(ImageDraw.Draw(ilt), 2080, acik=not gece, boy=240)
    katmanlar.append(("iletisim", ilt))
    brg = _bos()
    b16.yildiz(brg, W - 1150, 3100, 700, ["60 AY", "SABİT", "TAKSİT!"], don=10)
    katmanlar.append(("burgu", brg))
    return katmanlar


def _proje_alani():
    katmanlar = [("zemin", b35.zemin())] + _logolar_katman()
    man = _bos()
    dr = ImageDraw.Draw(man)
    dr.text((W / 2, 2160), "PROJE ALANI",
            font=b35.sigdir(dr, "PROJE ALANI", "Black", 950, W - 2 * PAD),
            fill=b35.PETROL, anchor="mm")
    dr.rounded_rectangle([W / 2 - 850, 2800, W / 2 + 850, 2842], radius=21,
                         fill=tz.TURKUAZ + (255,))
    katmanlar.append(("proje-alani", man))
    ilt = _bos()
    b35.iletisim(ImageDraw.Draw(ilt), b35.H - 430, acik=True, boy=250)
    katmanlar.append(("iletisim", ilt))
    return katmanlar


def uret(ad, katmanlar):
    kucuk = [(a, _kucult(im)) for a, im in katmanlar]
    p = os.path.join(OUT, ad + ".psd")
    psd_katmanli(p, kucuk, PSD_DPI)
    print("   %-28s %.1f MB · %d katman"
          % (ad, os.path.getsize(p) / 1e6, len(kucuk)))


if __name__ == "__main__":
    uret("turkuaz-01-kocaeli-3x5", _kampanya(gece=False))
    uret("turkuaz-09-gece-3x5", _kampanya(gece=True))
    uret("turkuaz-proje-alani-3x5", _proje_alani())
    print("tamam ->", OUT)
