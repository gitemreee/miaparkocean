#!/usr/bin/env python3
"""
MİA PARK OCEAN — 16,00 x 2,70 m TEK PARÇA branda/bilbord (10 tasarım).

Meta v5 kampanya dili, ultra geniş (5,93:1) kurgu:

    ┌───────────────────────────────────────────┬──────────────────┐
    │ dikey gradyan zemin: MİA logosu, dev      │ GİRİŞ KAPISI     │
    │ manşet, sarı çipler, telefon çipi         │ dış görseli tam  │
    │                                           │ boy; sol kenarı  │
    │                          yıldız rozet ────┤ zemine karışır   │
    └───────────────────────────────────────────┴──────────────────┘

GÖRSEL: yalnızca giriş kapısı dış cephesi (entrance-gate), tasarım
başına farklı kadraj. Kurallar (işveren): dipnot / koop adı /
"temsilidir" YOK, "%30" ve "peşinatsız" geçmez, bina üzerine yazı
binmez, onaylı örnek fiyatlar (1+0: 699.000/29.900 · 1+1: 999.000/39.900).

ÇIKTILAR (basım için):
  tabela/bilbord-16m/*.jpg      1:10 ölçek (1600 x 270 mm) @ 300 dpi
                                = 18898 x 3189 px, dpi gömülü
  tabela/bilbord-16m/psd/*.psd  1:10 ölçek @ 150 dpi = 9449 x 1594 px,
                                düzleştirilmiş TEK katman ("Background"
                                Photoshop'ta kilitli gelir), RLE sıkıştırma

    python3 scripts/build-bilbord-16m.py
"""

import math
import os
import struct
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "public", "images")
YAZI = os.path.join(ROOT, "sunum", "yazitipi")
OUT = os.path.join(ROOT, "tabela", "bilbord-16m")
PSD = os.path.join(OUT, "psd")
ONIZ = os.path.join(OUT, "onizleme")
for d in (OUT, PSD, ONIZ):
    os.makedirs(d, exist_ok=True)

# 16000 x 2700 mm — çalışma 1:10 ölçekte
W, H, DPI = 18898, 3189, 300         # 1600 x 270 mm @ 300 dpi
PSD_W, PSD_H, PSD_DPI = 9449, 1594, 150
PAD = 300
FOTO = "entrance-gate.webp"          # tek görsel: giriş kapısı

NAVY = (10, 42, 74)
SARI = (255, 209, 74)
KIRMIZI = (200, 32, 42)
MAVI_U = (12, 102, 150)
MAVI_A = (26, 146, 198)
YESIL_U = (8, 92, 70)
YESIL_A = (24, 146, 112)
BEYAZ = (255, 255, 255)

TEL = "0540 028 00 41"
SITE = "miaparkocean.com"


def mont(kes, boy):
    return ImageFont.truetype(os.path.join(YAZI, "Montserrat-%s.ttf" % kes), boy)


def sigdir(dr, t, kes, boy, maxw):
    f = mont(kes, boy)
    while boy > 60 and dr.textlength(t, font=f) > maxw:
        boy = int(boy * 0.96)
        f = mont(kes, boy)
    return f


def grad_zemin(ust, alt):
    t = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    g = (np.array(ust, np.float32) * (1 - t)
         + np.array(alt, np.float32) * t).astype(np.uint8)
    im = Image.new("RGBA", (W, H))
    im.paste(Image.fromarray(np.repeat(g, W, axis=1), "RGB"), (0, 0))
    return im


def foto_sag(im, ust, alt, gen, focus=0.5, zoom=1.0, focus_y=0.45, bl=420):
    """Giriş kapısı görseli sağda TAM BOY; sol kenarı, zeminin o satırdaki
    gradyan rengine yumuşak karışır (meta foto_alt dilinin yatayı)."""
    kay = Image.open(os.path.join(SRC, FOTO)).convert("RGB")
    iw, ih = kay.size
    s = max(gen / iw, H / ih) * max(1.0, zoom)
    sw, sh = gen / s, H / s
    ox = (iw - sw) * focus
    oy = (ih - sh) * focus_y
    ft = kay.crop((int(ox), int(oy), int(ox + sw), int(oy + sh)))
    ft = ft.resize((gen, H), Image.LANCZOS)
    if s > 1.6:
        ft = ft.filter(ImageFilter.UnsharpMask(radius=3, percent=52, threshold=3))
    x0 = W - gen
    im.paste(ft, (x0, 0))
    t = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    gr = (np.array(ust, np.float32) * (1 - t) + np.array(alt, np.float32) * t)
    band = np.asarray(ft.crop((0, 0, bl, H)), np.float32)
    alfa = np.linspace(1, 0, bl, dtype=np.float32)[None, :, None]
    kar = (gr * alfa + band * (1 - alfa)).astype(np.uint8)
    im.paste(Image.fromarray(kar, "RGB"), (x0, 0))
    # Sağ üstteki OCEAN logosu için fotoğrafın tepesine hafif lacivert
    # perde — logo binaya denk gelse de okunur, bina net kalır.
    ph = 620
    perde = np.zeros((ph, 1, 4), np.uint8)
    perde[:, 0, :3] = (6, 26, 44)
    perde[:, 0, 3] = (np.clip(1 - np.arange(ph) / ph, 0, 1) ** 1.2 * 150)
    im.alpha_composite(Image.fromarray(np.repeat(perde, gen, axis=1), "RGBA"),
                       (x0, 0))
    return x0


def logolar(im, koyu, foto_x0):
    """MİA solda zeminde; Ocean Gayrimenkul sağda fotoğrafın göğünde."""
    mia = os.path.join(ROOT, "public", "brand",
                       "logo-ocean-white.png" if koyu else "logo-ocean-trim.png")
    lg = Image.open(mia).convert("RGBA")
    lg = lg.resize((760, int(lg.height * 760 / lg.width)), Image.LANCZOS)  # h≈520
    im.alpha_composite(lg, (PAD, 110))
    oce = os.path.join(ROOT, "public", "ocean-logo-white.png")
    og = Image.open(oce).convert("RGBA")
    og = og.resize((760, int(og.height * 760 / og.width)), Image.LANCZOS)  # h≈320
    im.alpha_composite(og, (W - PAD - 760, 150))


def cip(dr, cx, cy, t, f, dolgu=SARI, yazi=NAVY, pad_x=120, pad_y=60, radius=60):
    tw = dr.textlength(t, font=f)
    h = f.size + 2 * pad_y
    dr.rounded_rectangle([cx - tw / 2 - pad_x, cy - h / 2,
                          cx + tw / 2 + pad_x, cy + h / 2], radius=radius, fill=dolgu)
    dr.text((cx, cy - f.size * 0.06), t, font=f, fill=yazi, anchor="mm")


def cip_sol(dr, x, cy, t, f, dolgu=SARI, yazi=NAVY, pad_x=100, pad_y=52, radius=52):
    tw = dr.textlength(t, font=f)
    h = f.size + 2 * pad_y
    dr.rounded_rectangle([x, cy - h / 2, x + tw + 2 * pad_x, cy + h / 2],
                         radius=radius, fill=dolgu)
    dr.text((x + pad_x + tw / 2, cy - f.size * 0.06), t, font=f, fill=yazi, anchor="mm")
    return x + tw + 2 * pad_x


def fiyat_satiri(dr, cx, cy, parcalar, boy=250, yazi=BEYAZ):
    f1, f2 = mont("ExtraBold", boy), mont("ExtraBold", int(boy * 0.85))
    genlik = [dr.textlength(b, font=f1) + 200 + 130 + dr.textlength(k, font=f2)
              for b, k in parcalar]
    x = cx - (sum(genlik) + (len(parcalar) - 1) * 360) / 2
    for (b, k), g in zip(parcalar, genlik):
        x2 = cip_sol(dr, x, cy, b, f1)
        dr.text((x2 + 130, cy - 15), k, font=f2, fill=yazi, anchor="lm")
        x += g + 360


def yildiz(im, cx, cy, r, satirlar, dolgu=KIRMIZI, yazi=BEYAZ, don=-12, N=26):
    kat = Image.new("RGBA", (r * 3, r * 3), (0, 0, 0, 0))
    kd = ImageDraw.Draw(kat)
    c = r * 1.5
    pts = []
    for i in range(N * 2):
        rr = r if i % 2 == 0 else r * 0.84
        a = math.pi * i / N
        pts.append((c + rr * math.cos(a), c + rr * math.sin(a)))
    kd.polygon(pts, fill=dolgu + (255,))
    fb = mont("ExtraBold", int(r * (0.28 if len(satirlar) > 1 else 0.34)))
    y0 = c - (len(satirlar) - 1) * r * 0.19
    for i, t in enumerate(satirlar):
        kd.text((c, y0 + i * r * 0.38), t, font=fb, fill=yazi, anchor="mm")
    kat = kat.rotate(don, resample=Image.BICUBIC, expand=False)
    im.alpha_composite(kat, (int(cx - c), int(cy - c)))


def tel_cip(dr, cx, cy, dolgu=NAVY, yazi=BEYAZ, site=True, boy=230):
    t = TEL + ("   ·   " + SITE if site else "")
    f = mont("Bold", boy)
    gen = dr.textlength(t, font=f) + 400
    dr.rounded_rectangle([cx - gen / 2, cy - boy * 0.85, cx + gen / 2, cy + boy * 0.85],
                         radius=boy * 0.85, fill=dolgu)
    dr.text((cx, cy - boy * 0.05), t, font=f, fill=yazi, anchor="mm")


# ------------------------------------------------------- PSD (kilitli)
def _packbits_satir(satir):
    """PackBits: sabit satır -> koşu paketleri; değişken satır -> literal."""
    n = len(satir)
    if n and satir.min() == satir.max():
        dolu, kalan, v = [], n, int(satir[0])
        while kalan:
            L = min(128, kalan)
            dolu.append(bytes((257 - L, v)))
            kalan -= L
        return b"".join(dolu)
    parca = []
    b = satir.tobytes()
    for i in range(0, n, 128):
        blok = b[i:i + 128]
        parca.append(bytes((len(blok) - 1,)) + blok)
    return b"".join(parca)


def psd_yaz(im, yol, dpi):
    """Düzleştirilmiş, tek katmanlı PSD (Photoshop'ta kilitli Background).
    RGB 8 bit, RLE (PackBits) sıkıştırma, çözünürlük bilgisi gömülü."""
    im = im.convert("RGB")
    w, h = im.size
    arr = np.asarray(im)                       # h, w, 3
    with open(yol, "wb") as f:
        f.write(b"8BPS")
        f.write(struct.pack(">H6xHIIHH", 1, 3, h, w, 8, 3))
        f.write(struct.pack(">I", 0))          # renk modu verisi yok
        cozunurluk = struct.pack(">IHHIHH", dpi << 16, 1, 2, dpi << 16, 1, 2)
        blok = b"8BIM" + struct.pack(">H", 1005) + b"\x00\x00" \
            + struct.pack(">I", len(cozunurluk)) + cozunurluk
        f.write(struct.pack(">I", len(blok)))
        f.write(blok)
        f.write(struct.pack(">I", 0))          # katman bölümü yok = düz dosya
        f.write(struct.pack(">H", 1))          # RLE
        kanallar = [[_packbits_satir(arr[y, :, c]) for y in range(h)]
                    for c in range(3)]
        for kanal in kanallar:
            f.write(b"".join(struct.pack(">H", len(s)) for s in kanal))
        for kanal in kanallar:
            f.write(b"".join(kanal))


def kaydet(ad, im):
    rgb = im.convert("RGB")
    p = os.path.join(OUT, ad + ".jpg")
    rgb.save(p, "JPEG", quality=92, optimize=True, dpi=(DPI, DPI))
    kucuk = rgb.copy()
    kucuk.thumbnail((1800, 1800), Image.LANCZOS)
    kucuk.save(os.path.join(ONIZ, ad + ".jpg"), quality=86, optimize=True)
    ps = rgb.resize((PSD_W, PSD_H), Image.LANCZOS)
    pp = os.path.join(PSD, ad + ".psd")
    psd_yaz(ps, pp, PSD_DPI)
    print("   %-26s jpg %.1f MB · psd %.1f MB"
          % (ad, os.path.getsize(p) / 1e6, os.path.getsize(pp) / 1e6))


# ═══════════════════════════════════════════════════════════ 10 TASARIM
def b01():
    G_U, G_A = (88, 118, 132), (150, 202, 226)
    im = grad_zemin(G_U, G_A)
    x0 = foto_sag(im, G_U, G_A, 7600, 0.5, 1.1, 0.48)
    logolar(im, True, x0)
    dr = ImageDraw.Draw(im)
    cx = x0 / 2
    dr.text((cx, 900), "İZMİT EV SAHİBİ OLUYOR", font=mont("Black", 540),
            fill=BEYAZ, anchor="mm")
    fiyat_satiri(dr, cx, 1560, [("699.000 TL", "PEŞİNATLA"),
                                ("29.900 TL", "TAKSİTLE KAVUŞUN!")], 250)
    dr.text((cx, 2110), "1+0 dairelerde · Banka yok · Faiz yok · Kefil yok",
            font=mont("SemiBold", 190), fill=(20, 52, 80), anchor="mm")
    yildiz(im, x0 + 350, 2350, 640, ["ÜSTELİK", "FAİZSİZ!"])
    dr = ImageDraw.Draw(im)
    tel_cip(dr, cx, H - 330)
    kaydet("bilbord-16m-01-izmit", im)


def b02():
    A_U, A_A = (240, 246, 251), (252, 253, 255)
    im = grad_zemin(A_U, A_A)
    x0 = foto_sag(im, A_U, A_A, 7600, 0.42, 1.0, 0.40, bl=360)
    logolar(im, False, x0)
    dr = ImageDraw.Draw(im)
    cx = x0 / 2
    dr.text((cx, 800), "EV SAHİBİ OLMAK İÇİN", font=mont("ExtraBold", 280),
            fill=NAVY, anchor="mm")
    f1 = mont("Black", 300)
    grup = []
    for a in ["BANKA", "FAİZ", "KEFİL"]:
        aw = dr.textlength(a + " ", font=f1)
        bw = dr.textlength("YOK", font=f1) + 180
        grup.append((a, aw, bw))
    top = sum(aw + 50 + bw for _, aw, bw in grup) + 340 * 2
    x = cx - top / 2
    for a, aw, bw in grup:
        dr.text((x, 1360), a, font=f1, fill=NAVY, anchor="lm")
        cip(dr, x + aw + 50 + bw / 2, 1360, "YOK", f1, pad_x=90, pad_y=30)
        x += aw + 50 + bw + 340
    cip(dr, cx, 1950, "60 AY SABİT TAKSİT", mont("ExtraBold", 280),
        dolgu=NAVY, yazi=BEYAZ, pad_x=170, pad_y=95)
    yildiz(im, x0 + 350, 2300, 640, ["KOMİSYON", "YOK!"], don=10)
    dr = ImageDraw.Draw(im)
    tel_cip(dr, cx, H - 330)
    kaydet("bilbord-16m-02-yok-duvari", im)


def b03():
    im = grad_zemin((20, 138, 104), (8, 86, 66))
    x0 = foto_sag(im, (20, 138, 104), (8, 86, 66), 7600, 0.55, 1.2, 0.45)
    logolar(im, True, x0)
    dr = ImageDraw.Draw(im)
    cx = x0 / 2
    dr.text((cx - 2350, 1350), "%0", font=mont("Black", 1250), fill=SARI, anchor="mm")
    dr.text((cx + 850, 1080), "FAİZ · VADE FARKI", font=mont("ExtraBold", 330),
            fill=BEYAZ, anchor="mm")
    dr.text((cx + 850, 1540), "KOMİSYON", font=mont("ExtraBold", 330),
            fill=BEYAZ, anchor="mm")
    cip(dr, cx + 850, 2050, "İZMİT MİA BÖLGESİ", mont("ExtraBold", 240),
        dolgu=SARI, yazi=YESIL_U, pad_x=150, pad_y=75)
    dr = ImageDraw.Draw(im)
    tel_cip(dr, cx, H - 330, dolgu=BEYAZ, yazi=YESIL_U)
    kaydet("bilbord-16m-03-sifir", im)


def b04():
    A_U, A_A = (253, 251, 249), (244, 238, 232)
    im = grad_zemin(A_U, A_A)
    x0 = foto_sag(im, A_U, A_A, 7600, 0.5, 1.25, 0.42, bl=360)
    logolar(im, False, x0)
    dr = ImageDraw.Draw(im)
    cx = x0 / 2
    dr.text((cx - 2500, 1300), "60 AY", font=mont("Black", 900), fill=KIRMIZI,
            anchor="mm")
    cip(dr, cx + 1250, 1000, "VADE FARKSIZ · SABİT TAKSİT", mont("ExtraBold", 260),
        pad_x=170, pad_y=95)
    dr.text((cx + 1250, 1560), "Banka yok · Faiz yok · Kefil yok · Komisyon yok",
            font=mont("SemiBold", 210), fill=(96, 74, 70), anchor="mm")
    dr = ImageDraw.Draw(im)
    tel_cip(dr, cx, H - 330, dolgu=KIRMIZI, site=False)
    kaydet("bilbord-16m-04-60ay", im)


def b05():
    im = grad_zemin(MAVI_U, MAVI_A)
    x0 = foto_sag(im, MAVI_U, MAVI_A, 7600, 0.65, 1.25, 0.35)
    logolar(im, True, x0)
    dr = ImageDraw.Draw(im)
    cx = x0 / 2
    dr.text((cx, 760), "İzmit MİA'da", font=mont("SemiBold", 240),
            fill=(206, 234, 248), anchor="mm")
    f = sigdir(dr, "Aylık 29.900 TL'ye ev sahibi olun.", "ExtraBold", 420, x0 - 900)
    dr.text((cx, 1300), "Aylık 29.900 TL'ye ev sahibi olun.", font=f,
            fill=BEYAZ, anchor="mm")
    dr.text((cx, 1850), "Üstelik 60 aya varan vade ve 0 faizle!",
            font=mont("SemiBold", 220), fill=(206, 234, 248), anchor="mm")
    yildiz(im, x0 + 350, 2300, 640, ["FAİZ", "YOK!"], don=10)
    dr = ImageDraw.Draw(im)
    tel_cip(dr, cx, H - 330, dolgu=BEYAZ, yazi=MAVI_U)
    kaydet("bilbord-16m-05-aylik", im)


def b06():
    G_U, G_A = (96, 138, 158), (168, 210, 230)
    im = grad_zemin(G_U, G_A)
    x0 = foto_sag(im, G_U, G_A, 7600, 0.5, 1.0, 0.25)
    logolar(im, True, x0)
    dr = ImageDraw.Draw(im)
    cx = x0 / 2
    dr.text((cx, 830), "KOCAELİ DENİZE YAKIN EV SAHİBİ OLUYOR",
            font=sigdir(dr, "KOCAELİ DENİZE YAKIN EV SAHİBİ OLUYOR", "Black", 380,
                        x0 - 800), fill=BEYAZ, anchor="mm")
    fiyat_satiri(dr, cx, 1480, [("999.000 TL", "PEŞİNATLA 1+1"),
                                ("39.900 TL", "TAKSİTLE!")], 250)
    dr.text((cx, 2030), "İzmit sahiline 2 dk · 60 ay vade farksız",
            font=mont("SemiBold", 190), fill=(16, 58, 92), anchor="mm")
    yildiz(im, x0 + 350, 2350, 640, ["BANKA", "YOK!"])
    dr = ImageDraw.Draw(im)
    tel_cip(dr, cx, H - 330)
    kaydet("bilbord-16m-06-kocaeli", im)


def b07():
    im = grad_zemin((12, 48, 92), (26, 80, 132))
    x0 = foto_sag(im, (12, 48, 92), (26, 80, 132), 7600, 0.5, 1.1, 0.48, bl=480)
    logolar(im, True, x0)
    dr = ImageDraw.Draw(im)
    cx = x0 / 2
    dr.text((cx, 760), "29.900 TL taksitle", font=mont("SemiBold", 250),
            fill=(150, 205, 228), anchor="mm")
    dr.text((cx - 1650, 1400), "EV SAHİBİ", font=mont("Black", 520), fill=BEYAZ,
            anchor="mm")
    cip(dr, cx + 1850, 1400, "OLMA ZAMANI", mont("Black", 420), pad_x=170, pad_y=60)
    dr.text((cx, 2050), "Banka yok · Faiz yok · Kefil yok · Ara ödeme yok",
            font=mont("SemiBold", 210), fill=(180, 208, 226), anchor="mm")
    yildiz(im, x0 + 350, 2300, 640, ["60 AY", "VADE", "FARKSIZ"], don=12)
    dr = ImageDraw.Draw(im)
    tel_cip(dr, cx, H - 330, dolgu=SARI, yazi=NAVY)
    kaydet("bilbord-16m-07-olma-zamani", im)


def b08():
    im = grad_zemin(YESIL_U, YESIL_A)
    x0 = foto_sag(im, YESIL_U, YESIL_A, 7600, 0.35, 1.15, 0.45)
    logolar(im, True, x0)
    dr = ImageDraw.Draw(im)
    cx = x0 / 2
    dr.text((cx, 780), "1+0 stüdyo dairelerde avantajlı yatırım fırsatı",
            font=sigdir(dr, "1+0 stüdyo dairelerde avantajlı yatırım fırsatı",
                        "ExtraBold", 300, x0 - 800), fill=BEYAZ, anchor="mm")
    f1, fk = mont("ExtraBold", 250), mont("SemiBold", 170)
    for i, (buyuk, kucuk) in enumerate([("699.000 TL", "peşinat"),
                                        ("29.900 TL", "taksit")]):
        bx = cx - 1420 + i * 2840
        dr.rounded_rectangle([bx - 1230, 1180, bx + 1230, 1900], radius=90,
                             outline=BEYAZ, width=16)
        dr.text((bx, 1450), buyuk, font=f1, fill=SARI, anchor="mm")
        dr.text((bx, 1740), kucuk, font=fk, fill=BEYAZ, anchor="mm")
    cip(dr, cx, 2270, "60 AY VADE FARKSIZ · BANKA YOK", mont("ExtraBold", 210),
        dolgu=SARI, yazi=YESIL_U, pad_x=150, pad_y=75)
    dr = ImageDraw.Draw(im)
    tel_cip(dr, cx, H - 330, dolgu=BEYAZ, yazi=YESIL_U)
    kaydet("bilbord-16m-08-studyo", im)


def b09():
    G_U, G_A = (140, 198, 224), (225, 242, 250)
    im = grad_zemin(G_U, G_A)
    x0 = foto_sag(im, G_U, G_A, 7600, 0.6, 1.15, 0.40, bl=460)
    logolar(im, False, x0)
    dr = ImageDraw.Draw(im)
    cx = x0 / 2
    dr.rounded_rectangle([cx - 2750, 620, cx + 2750, 1600], radius=150, fill=NAVY)
    dr.text((cx, 950), "Tasarrufa dayalı finansmanla", font=mont("SemiBold", 210),
            fill=(150, 205, 228), anchor="mm")
    dr.text((cx, 1320), "EV SAHİBİ OL!", font=mont("Black", 340), fill=BEYAZ,
            anchor="mm")
    f = mont("ExtraBold", 210)
    metins = ["BANKA YOK", "FAİZ YOK", "60 AY SABİT TAKSİT"]
    genlik = [dr.textlength(t, font=f) + 300 for t in metins]
    x = cx - (sum(genlik) + 2 * 260) / 2
    for t, g in zip(metins, genlik):
        cip(dr, x + g / 2, 1980, t, f, pad_x=150, pad_y=70)
        x += g + 260
    yildiz(im, x0 + 350, 2350, 640, ["ARA", "ÖDEME", "YOK!"], don=10)
    dr = ImageDraw.Draw(im)
    tel_cip(dr, cx, H - 330)
    kaydet("bilbord-16m-09-tasarruf", im)


def b10():
    im = grad_zemin(MAVI_A, MAVI_U)
    x0 = foto_sag(im, MAVI_A, MAVI_U, 7600, 0.4, 1.05, 0.55)
    logolar(im, True, x0)
    dr = ImageDraw.Draw(im)
    cx = x0 / 2
    dr.text((cx, 800), "60 AY VADEYLE EV SAHİBİ OLMAK İÇİN",
            font=sigdir(dr, "60 AY VADEYLE EV SAHİBİ OLMAK İÇİN", "Black", 340,
                        x0 - 800), fill=BEYAZ, anchor="mm")
    cip(dr, cx, 1330, "SATIŞ OFİSİMİZE BEKLERİZ", mont("ExtraBold", 250),
        pad_x=190, pad_y=95)
    fs1, fs2 = mont("ExtraBold", 200), mont("SemiBold", 145)
    for i, (a, b) in enumerate([("699.000 TL'den", "başlayan peşinat"),
                                ("%0", "faiz"), ("29.900 TL", "taksit")]):
        bx = cx + (i - 1) * 2100
        dr.rounded_rectangle([bx - 960, 1720, bx + 960, 2400], radius=90,
                             outline=BEYAZ, width=14)
        dr.text((bx, 1980), a, font=fs1, fill=SARI, anchor="mm")
        dr.text((bx, 2250), b, font=fs2, fill=BEYAZ, anchor="mm")
    dr = ImageDraw.Draw(im)
    tel_cip(dr, cx, H - 330, dolgu=BEYAZ, yazi=MAVI_U)
    kaydet("bilbord-16m-10-satis-ofisi", im)


def kontak():
    fs = sorted(f for f in os.listdir(ONIZ)
                if f.startswith("bilbord-16m-") and f.endswith(".jpg"))
    tw = 1320
    th = int(tw * H / W)
    ara = 18
    sheet = Image.new("RGB", (tw + 2 * ara, len(fs) * (th + ara) + ara), (16, 20, 26))
    for i, f in enumerate(fs[:10]):
        im = Image.open(os.path.join(ONIZ, f)).resize((tw, th), Image.LANCZOS)
        sheet.paste(im, (ara, ara + i * (th + ara)))
    sheet.save(os.path.join(OUT, "kontak-bilbord-16m.jpg"), quality=88)
    print("   kontak-bilbord-16m.jpg")


if __name__ == "__main__":
    for b in [b01, b02, b03, b04, b05, b06, b07, b08, b09, b10]:
        b()
    kontak()
    print("tamam ->", OUT)
