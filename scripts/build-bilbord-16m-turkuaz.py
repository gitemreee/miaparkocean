#!/usr/bin/env python3
"""
MİA PARK OCEAN — 16,00 x 2,70 m TURKUAZ seri (10 tasarım, v2).

İlk 16 m serisinden TAMAMEN FARKLI ikinci set. Kurallar (işveren):
- Turkuaz-beyaz odaklı paletler; 8 tasarım GÜNDÜZ, 2 tasarım GECE karesi.
- Fotoğraf çerçevesiz/kartsız: sağda tam boy, sol kenarı zemine karışır.
- HER tasarımda 1+0 ve 1+1 ödeme kartları BİRLİKTE:
    1+0: 699.000 TL peşinat · 29.900 TL taksit
    1+1: 999.000 TL peşinat · 39.900 TL taksit
- HER tasarımda vurgulu: BANKA YOK · FAİZ YOK · KREDİ YOK · ARA ÖDEME YOK
  ve 60 AY SABİT TAKSİT.
- Logolar KENDİ RENKLERİNDE (beyaza çevrilmez): MİA solda, OCEAN sağda;
  koyu foto üstünde okunması için yumuşak beyaz ışıltı.
- Alt bant her tasarımda aynı: SOLDA telefon · ORTADA miaparkocean.com ·
  SAĞDA Instagram + Facebook ikonları ve miaparkocean.
- Dipnot / koop adı / "temsilidir" YOK; "%30" ve "peşinatsız" geçmez.

ÇIKTILAR (basım): JPEG 1:10 ölçek (1600x270 mm) @ 300 dpi = 18898x3189;
kilitli PSD (düz tek katman) 1:10 @ 150 dpi = 9449x1594.

    python3 scripts/build-bilbord-16m-turkuaz.py
"""

import importlib.util
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_spec = importlib.util.spec_from_file_location(
    "b16", os.path.join(ROOT, "scripts", "build-bilbord-16m.py"))
b16 = importlib.util.module_from_spec(_spec)
sys.modules["b16"] = b16
_spec.loader.exec_module(b16)

mont, sigdir, psd_yaz = b16.mont, b16.sigdir, b16.psd_yaz
cip, cip_sol, yildiz = b16.cip, b16.cip_sol, b16.yildiz
grad_zemin = b16.grad_zemin

W, H, DPI = b16.W, b16.H, b16.DPI
PSD_W, PSD_H, PSD_DPI = b16.PSD_W, b16.PSD_H, b16.PSD_DPI
PAD = b16.PAD
SRC = b16.SRC
TEL, SITE = b16.TEL, b16.SITE

OUT = os.path.join(ROOT, "tabela", "bilbord-16m-turkuaz")
PSD = os.path.join(OUT, "psd")
ONIZ = os.path.join(OUT, "onizleme")
for d in (OUT, PSD, ONIZ):
    os.makedirs(d, exist_ok=True)

# ------------------------------------------------------------ turkuaz palet
KIRMIZI = b16.KIRMIZI            # vurgu çipleri ve burgu rozetler
TURKUAZ = (0, 154, 168)
TURKUAZ_K = (0, 106, 118)        # koyu turkuaz / petrol
TURKUAZ_A = (72, 189, 200)
PETROL = (4, 66, 76)             # koyu metin ve alt bant
BUZ = (224, 246, 248)
BEYAZ = (255, 255, 255)
GRI = (66, 108, 116)

BAR_H = 300                      # alt iletişim bandı


def foto_sag(im, ust, alt, ad, gen=7600, focus=0.5, zoom=1.0, focus_y=0.45,
             bl=520):
    """Fotoğraf sağda TAM BOY, çerçevesiz; sol kenarı zeminin o satırdaki
    gradyan rengine yumuşak karışır."""
    kay = Image.open(os.path.join(SRC, ad)).convert("RGB")
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
    return x0


def logo_glow(im, logo, x, y, blur=45, kat=6):
    """Gece zeminlerinde logonun biçimini izleyen beyaz parlama;
    alfa eğriltilir ki artık yarı saydam zemin plakalaşmasın."""
    a = np.asarray(logo.split()[3], np.float32) / 255.0
    a = (a ** 1.6 * 255).astype(np.uint8)
    sil = Image.new("RGBA", logo.size, (255, 255, 255, 255))
    sil.putalpha(Image.fromarray(a, "L"))
    sil = sil.filter(ImageFilter.GaussianBlur(blur))
    for _ in range(kat):
        im.alpha_composite(sil, (x, y))


def logolar(im, gece=False):
    """İkisi de KENDİ renklerinde, plakasız şeffaf PNG: MİA (2026 kurumsal
    çizim) solda, OCEAN sağda; koyu zeminde biçimi izleyen beyaz parlama."""
    lg = Image.open(os.path.join(ROOT, "public", "brand",
                                 "logo-mia-2026.png")).convert("RGBA")
    lg = lg.resize((1040, int(lg.height * 1040 / lg.width)), Image.LANCZOS)
    if gece:
        logo_glow(im, lg, PAD, 60)
    im.alpha_composite(lg, (PAD, 60))
    og = Image.open(os.path.join(ROOT, "sunum", "kaynak", "sekil",
                                 "ocean-logo-renkli2.png")).convert("RGBA")
    og = og.resize((980, int(og.height * 980 / og.width)), Image.LANCZOS)
    if gece:
        logo_glow(im, og, W - PAD - 980, 110)
    im.alpha_composite(og, (W - PAD - 980, 110))


def alt_bar(im):
    """Solda telefon · ortada site · sağda Instagram+Facebook ikonları."""
    dr = ImageDraw.Draw(im)
    y0 = H - BAR_H
    dr.rectangle([0, y0, W, H], fill=PETROL + (255,))
    cy = y0 + BAR_H / 2
    f = mont("Bold", 190)
    dr.text((PAD, cy), TEL, font=f, fill=BEYAZ, anchor="lm")
    dr.text((W / 2, cy), SITE, font=f, fill=BEYAZ, anchor="mm")
    t = "miaparkocean"
    tw = dr.textlength(t, font=f)
    tx = W - PAD - tw
    dr.text((tx, cy), t, font=f, fill=BEYAZ, anchor="lm")
    ik, kal = 185, 15
    fx = tx - 80 - ik                       # facebook
    ix = fx - 60 - ik                       # instagram
    dr.rounded_rectangle([ix, cy - ik / 2, ix + ik, cy + ik / 2], radius=42,
                         outline=BEYAZ, width=kal)
    dr.ellipse([ix + ik * 0.26, cy - ik * 0.24, ix + ik * 0.74, cy + ik * 0.24],
               outline=BEYAZ, width=kal)
    dr.ellipse([ix + ik * 0.72, cy - ik * 0.40, ix + ik * 0.86, cy - ik * 0.26],
               fill=BEYAZ)
    dr.rounded_rectangle([fx, cy - ik / 2, fx + ik, cy + ik / 2], radius=42,
                         outline=BEYAZ, width=kal)
    dr.text((fx + ik * 0.55, cy + 6), "f", font=mont("Bold", 152), fill=BEYAZ,
            anchor="mm")


def yok_satiri(dr, cx, y, boy=195, dolgu=KIRMIZI, yazi=BEYAZ, ara=190):
    ts = ["BANKA YOK", "FAİZ YOK", "KREDİ YOK", "ARA ÖDEME YOK"]
    f = mont("ExtraBold", boy)
    gs = [dr.textlength(t, font=f) + 2 * 140 for t in ts]
    x = cx - (sum(gs) + (len(ts) - 1) * ara) / 2
    for t, g in zip(ts, gs):
        cip(dr, x + g / 2, y, t, f, dolgu=dolgu, yazi=yazi, pad_x=140, pad_y=62)
        x += g + ara


def sabit_taksit(dr, cx, y, boy=300, dolgu=TURKUAZ_K, yazi=BEYAZ):
    cip(dr, cx, y, "60 AY SABİT TAKSİT", mont("Black", boy),
        dolgu=dolgu, yazi=yazi, pad_x=210, pad_y=90)


def kartlar(dr, cx, y, kw=2560, kh=880, gap=360, cerceve=True):
    """1+0 ve 1+1 ödeme kartları — her tasarımda aynı içerik."""
    veriler = [("1+0", "699.000 TL", "29.900 TL"),
               ("1+1", "999.000 TL", "39.900 TL")]
    for i, (tip, pesin, taksit) in enumerate(veriler):
        bx = cx + (i - 0.5) * (kw + gap)
        if cerceve:
            dr.rounded_rectangle([bx - kw / 2, y, bx + kw / 2, y + kh],
                                 radius=90, fill=(255, 255, 255, 255),
                                 outline=TURKUAZ_K + (255,), width=13)
        else:
            dr.rounded_rectangle([bx - kw / 2, y, bx + kw / 2, y + kh],
                                 radius=90, fill=(255, 255, 255, 255))
        cip(dr, bx, y, tip, mont("ExtraBold", 165), dolgu=TURKUAZ, yazi=BEYAZ,
            pad_x=115, pad_y=48)
        dr.text((bx, y + 300), pesin, font=mont("ExtraBold", 245),
                fill=PETROL, anchor="mm")
        dr.text((bx, y + 460), "peşinat", font=mont("SemiBold", 140),
                fill=GRI, anchor="mm")
        cip(dr, bx, y + 668, taksit + " TAKSİT", mont("ExtraBold", 160),
            dolgu=TURKUAZ_K, yazi=BEYAZ, pad_x=120, pad_y=58)


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
    print("   %-30s jpg %.1f MB · psd %.1f MB"
          % (ad, os.path.getsize(p) / 1e6, os.path.getsize(pp) / 1e6))


def govde_a(im, dr, cx, baslik, boy, koyu_metin=True):
    """Düzen A: manşet / (aralık) / YOK satırı / ortalı kartlar.
    60 AY SABİT TAKSİT vurgusu fotodaki kırmızı burguda."""
    renk = PETROL if koyu_metin else BEYAZ
    dr.text((cx, 770), baslik, font=sigdir(dr, baslik, "Black", boy, 10400),
            fill=renk, anchor="mm")
    yok_satiri(dr, cx, 1340)
    kartlar(dr, cx + 300, 1700)


def govde_b(im, dr, cx, baslik, boy, koyu_metin=True):
    """Düzen B: manşet / kartlar / YOK + 60 AY alt alta."""
    renk = PETROL if koyu_metin else BEYAZ
    dr.text((cx, 780), baslik, font=sigdir(dr, baslik, "Black", boy, 10400),
            fill=renk, anchor="mm")
    kartlar(dr, cx, 1180)
    yok_satiri(dr, cx, 2300, 185)
    sabit_taksit(dr, cx, 2660, 215)


# ═══════════════════════════════════ 10 TASARIM (8 gündüz · 2 gece)
def t01():
    """Gündüz · giriş kapısı · beyaz-buz zemin."""
    Z = (BEYAZ, BUZ)
    im = grad_zemin(*Z)
    x0 = foto_sag(im, *Z, "entrance-gate.webp", 7600, 0.5, 1.05, 0.45)
    logolar(im)
    dr = ImageDraw.Draw(im)
    govde_a(im, dr, x0 / 2, "KOCAELİ EV SAHİBİ OLUYOR", 430)
    yildiz(im, x0 + 500, 850, 620, ["60 AY", "SABİT", "TAKSİT!"], don=10)
    alt_bar(im)
    kaydet("turkuaz-01-kocaeli", im)


def t02():
    """Gündüz · havadan havuzlar · buz-turkuaz zemin."""
    Z = (BUZ, (168, 224, 230))
    im = grad_zemin(*Z)
    x0 = foto_sag(im, *Z, "aerial-pools.webp", 7600, 0.5, 1.0, 0.5)
    logolar(im)
    dr = ImageDraw.Draw(im)
    govde_b(im, dr, x0 / 2, "İZMİT MİA'DA YENİ YAŞAM", 420)
    yildiz(im, x0 + 500, 850, 600, ["FAİZSİZ!"], don=10)
    alt_bar(im)
    kaydet("turkuaz-02-yeni-yasam", im)


def t03():
    """Gündüz · avlu havuzları · turkuaz blok zemin."""
    Z = (TURKUAZ, TURKUAZ_K)
    im = grad_zemin(*Z)
    x0 = foto_sag(im, *Z, "courtyard-pools.webp", 7600, 0.5, 1.0, 0.45)
    logolar(im, gece=True)
    dr = ImageDraw.Draw(im)
    dr.text((x0 / 2, 770), "EV SAHİBİ OLMA ZAMANI",
            font=sigdir(dr, "EV SAHİBİ OLMA ZAMANI", "Black", 430, 10400),
            fill=BEYAZ, anchor="mm")
    yok_satiri(dr, x0 / 2, 1340)
    kartlar(dr, x0 / 2 + 300, 1700, cerceve=False)
    yildiz(im, x0 + 500, 850, 620, ["60 AY", "SABİT", "TAKSİT!"], don=10)
    alt_bar(im)
    kaydet("turkuaz-03-olma-zamani", im)


def t04():
    """Gündüz · sokak köşesi · beyaz zemin, sol hizalı manşet."""
    Z = ((252, 254, 255), (236, 248, 250))
    im = grad_zemin(*Z)
    x0 = foto_sag(im, *Z, "street-corner.webp", 7400, 0.42, 1.0, 0.35)
    logolar(im)
    dr = ImageDraw.Draw(im)
    cx = x0 / 2
    dr.text((PAD + 100, 940), "İZMİT MİA BÖLGESİ'NDE",
            font=mont("Black", 330), fill=TURKUAZ_K, anchor="lm")
    dr.text((PAD + 100, 1310), "EV SAHİBİ OLUYORSUNUZ",
            font=mont("Black", 330), fill=PETROL, anchor="lm")
    kartlar(dr, cx + 300, 1680)
    yok_satiri(dr, cx, 2680, 180)
    yildiz(im, x0 + 500, 850, 620, ["60 AY", "SABİT", "TAKSİT!"], don=10)
    alt_bar(im)
    kaydet("turkuaz-04-izmit-mia", im)


def t05():
    """Gündüz · giriş kapısı yakın · beyaz-turkuaz, dev 60 AY."""
    Z = (BEYAZ, (206, 240, 244))
    im = grad_zemin(*Z)
    x0 = foto_sag(im, *Z, "entrance-gate.webp", 7600, 0.72, 1.3, 0.5)
    logolar(im)
    dr = ImageDraw.Draw(im)
    cx = x0 / 2
    dr.text((cx - 2500, 1050), "60 AY", font=mont("Black", 780),
            fill=TURKUAZ_K, anchor="mm")
    dr.text((cx + 1500, 890), "SABİT TAKSİTLE", font=mont("Black", 330),
            fill=PETROL, anchor="mm")
    dr.text((cx + 1500, 1290), "EV SAHİBİ OLUN", font=mont("Black", 330),
            fill=PETROL, anchor="mm")
    kartlar(dr, cx, 1620)
    yok_satiri(dr, cx, 2680, 180)
    alt_bar(im)
    kaydet("turkuaz-05-60ay", im)


def t06():
    """Gündüz · pergola terası · buz zemin."""
    Z = ((240, 250, 252), (214, 240, 244))
    im = grad_zemin(*Z)
    x0 = foto_sag(im, *Z, "terrace-pergola.webp", 7600, 0.5, 1.0, 0.42)
    logolar(im)
    dr = ImageDraw.Draw(im)
    govde_a(im, dr, x0 / 2, "HAYALİNİZDEKİ EVE KAVUŞUN", 400)
    yildiz(im, x0 + 500, 850, 620, ["60 AY", "SABİT", "TAKSİT!"], don=10)
    alt_bar(im)
    kaydet("turkuaz-06-hayal", im)


def t07():
    """Gündüz · sıcak cephe · beyaz zemin, turkuaz manşet."""
    Z = (BEYAZ, BUZ)
    im = grad_zemin(*Z)
    x0 = foto_sag(im, *Z, "facade-warm.webp", 7000, 0.5, 1.0, 0.22, bl=460)
    logolar(im)
    dr = ImageDraw.Draw(im)
    govde_b(im, dr, x0 / 2, "TASARRUFA DAYALI FİNANSMAN", 380)
    alt_bar(im)
    kaydet("turkuaz-07-tasarruf", im)


def t08():
    """Gündüz · havuzlar yakın havadan · açık turkuaz zemin."""
    Z = ((190, 232, 238), (240, 250, 252))
    im = grad_zemin(*Z)
    x0 = foto_sag(im, *Z, "aerial-pools.webp", 7600, 0.75, 1.3, 0.45)
    logolar(im)
    dr = ImageDraw.Draw(im)
    govde_a(im, dr, x0 / 2, "SATIŞ OFİSİMİZE BEKLERİZ", 410)
    yildiz(im, x0 + 500, 850, 620, ["60 AY", "SABİT", "TAKSİT!"], don=10)
    alt_bar(im)
    kaydet("turkuaz-08-satis-ofisi", im)


def t09():
    """GECE · ışıklı giriş kapısı · petrol-turkuaz zemin."""
    Z = ((3, 48, 56), (0, 96, 108))
    im = grad_zemin(*Z)
    x0 = foto_sag(im, *Z, "night-gate.webp", 7600, 0.5, 1.0, 0.45, bl=600)
    logolar(im, gece=True)
    dr = ImageDraw.Draw(im)
    cx = x0 / 2
    dr.text((cx, 770), "KOCAELİ EV SAHİBİ OLUYOR",
            font=sigdir(dr, "KOCAELİ EV SAHİBİ OLUYOR", "Black", 420, 10400),
            fill=BEYAZ, anchor="mm")
    yok_satiri(dr, cx, 1340)
    kartlar(dr, cx + 300, 1700, cerceve=False)
    yildiz(im, x0 + 500, 850, 620, ["60 AY", "SABİT", "TAKSİT!"], don=10)
    alt_bar(im)
    kaydet("turkuaz-09-gece-kapi", im)


def t10():
    """GECE · avlu alacakaranlık havuzlar · koyu petrol zemin."""
    Z = ((2, 40, 48), (0, 84, 96))
    im = grad_zemin(*Z)
    x0 = foto_sag(im, *Z, "hero-courtyard-dusk.webp", 7600, 0.5, 1.0, 0.5, bl=600)
    logolar(im, gece=True)
    dr = ImageDraw.Draw(im)
    cx = x0 / 2
    dr.text((cx, 790), "AKŞAM IŞIKLARI EVİNİZDEN YANSISIN",
            font=sigdir(dr, "AKŞAM IŞIKLARI EVİNİZDEN YANSISIN", "Black", 340,
                        10400), fill=BEYAZ, anchor="mm")
    kartlar(dr, cx, 1180, cerceve=False)
    yok_satiri(dr, cx, 2300, 185)
    sabit_taksit(dr, cx, 2660, 215, dolgu=BEYAZ, yazi=PETROL)
    yildiz(im, x0 + 500, 850, 600, ["FAİZSİZ!"], don=10)
    alt_bar(im)
    kaydet("turkuaz-10-gece-avlu", im)


def kontak():
    fs = sorted(f for f in os.listdir(ONIZ)
                if f.startswith("turkuaz-") and f.endswith(".jpg"))
    tw = 1320
    th = int(tw * H / W)
    ara = 18
    sheet = Image.new("RGB", (tw + 2 * ara, len(fs) * (th + ara) + ara),
                      (16, 20, 26))
    for i, f in enumerate(fs[:10]):
        im = Image.open(os.path.join(ONIZ, f)).resize((tw, th), Image.LANCZOS)
        sheet.paste(im, (ara, ara + i * (th + ara)))
    sheet.save(os.path.join(OUT, "kontak-turkuaz.jpg"), quality=88)
    print("   kontak-turkuaz.jpg")


if __name__ == "__main__":
    for t in [t01, t02, t03, t04, t05, t06, t07, t08, t09, t10]:
        t()
    kontak()
    print("tamam ->", OUT)
