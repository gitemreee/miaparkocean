#!/usr/bin/env python3
"""
MİA PARK OCEAN — Meta / Instagram reklam görselleri (10 çeşit).

1080 x 1350 (4:5) — Meta'nın akış reklamları için önerdiği tek format;
aynı dosya Facebook ve Instagram akışında kırpılmadan çıkar.

Vurgu (işveren talebi): BANKA YOK · FAİZ YOK · KEFİL YOK · 60 AY SABİT
TAKSİT · KOMİSYON YOK · ARA ÖDEME YOK · BALON ÖDEME YOK.
Fiyat YOK. Her görselde yasal satır + "Görseller temsilidir."

On görselin onu da farklı kurgu: tam kanama tipografi, elmas fotoğraf,
onay listesi, soru-cevap, X/✓ karşılaştırma, dev rakam, yok-listesi…
Marka dili sunumla aynı: okyanus paleti + elmas motifi + Montserrat.

    python3 scripts/build-meta-reklam.py
Çıktı: sosyal-medya/meta-reklam/meta-01…10.jpg (+ kontak.jpg)
"""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "public", "images")
YAZI = os.path.join(ROOT, "sunum", "yazitipi")
OUT = os.path.join(ROOT, "sosyal-medya", "meta-reklam")
os.makedirs(OUT, exist_ok=True)

W, H = 1080, 1350

# ------------------------------------------------- palet (marka: okyanus)
GECE = (4, 40, 58)
LACI = (10, 58, 85)
KAGIT = (245, 250, 252)
AYRAC = (217, 231, 238)
VURGU = (26, 116, 150)
CAM = (72, 171, 197)
KURSUN = (71, 96, 110)
SIS = (169, 201, 216)
BEYAZ = (255, 255, 255)

YASAL = "S.S. Yahya Kaptan Birlik Yapı Kooperatifi · Ocean Gayrimenkul, Tek Yetkili Satıcı · Görseller temsilidir."
CTA = "miaparkocean.com   ·   0540 028 00 41"


def mont(kalinlik, boy):
    return ImageFont.truetype(os.path.join(YAZI, "Montserrat-%s.ttf" % kalinlik), boy)


def foto(ad, w, h, focus=0.5, zoom=1.0):
    im = Image.open(os.path.join(SRC, ad)).convert("RGB")
    iw, ih = im.size
    s = max(w / iw, h / ih) * max(1.0, zoom)
    nw, nh = max(w, int(iw * s)), max(h, int(ih * s))
    im = im.resize((nw, nh), Image.LANCZOS)
    ox, oy = int((nw - w) * focus), int((nh - h) * focus)
    return im.crop((ox, oy, ox + w, oy + h))


def perde(im, duraklar, renk=GECE):
    """Alta doğru koyulaşan gradyan bindirir."""
    t = np.linspace(0, 1, im.height, dtype=np.float32)
    a = (np.interp(t, [d[0] for d in duraklar], [d[1] for d in duraklar]) * 255).astype(np.uint8)
    alpha = np.repeat(a[:, None], im.width, axis=1)
    kat = np.zeros((im.height, im.width, 4), np.uint8)
    kat[..., 0], kat[..., 1], kat[..., 2] = renk
    kat[..., 3] = alpha
    im = im.convert("RGBA")
    im.alpha_composite(Image.fromarray(kat, "RGBA"))
    return im.convert("RGB")


def elmas_foto(ad, boy, focus=0.5, zoom=1.0):
    """Elmas (45° kare) maskeli fotoğraf, şeffaf zemin."""
    ss = 4
    kare = foto(ad, boy, boy, focus, zoom)
    m = Image.new("L", (boy * ss, boy * ss), 0)
    d = ImageDraw.Draw(m)
    B = boy * ss
    d.polygon([(B // 2, 0), (B, B // 2), (B // 2, B), (0, B // 2)], fill=255)
    m = m.resize((boy, boy), Image.LANCZOS)
    out = Image.new("RGBA", (boy, boy), (0, 0, 0, 0))
    out.paste(kare, (0, 0), m)
    return out


def elmas_cizgi(dr, cx, cy, boy, renk, kalin=3):
    r = boy / 2
    dr.line([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy), (cx, cy - r)],
            fill=renk, width=kalin, joint="curve")


def elmas_dolu(dr, cx, cy, boy, renk):
    r = boy / 2
    dr.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], fill=renk)


def metin_gen(dr, t, f):
    return dr.textlength(t, font=f)


def logo(im, tur, x, y, gen):
    """tur: mia-beyaz | mia-renkli | ocean-beyaz | ocean-renkli"""
    yol = {
        "mia-beyaz": os.path.join(ROOT, "public", "brand", "logo-ocean-white.png"),
        "mia-renkli": os.path.join(ROOT, "public", "brand", "logo-ocean-trim.png"),
        "ocean-beyaz": os.path.join(ROOT, "public", "ocean-logo-white.png"),
        "ocean-renkli": os.path.join(ROOT, "sunum", "kaynak", "sekil", "ocean-logo-renkli.png"),
    }[tur]
    lg = Image.open(yol).convert("RGBA")
    o = gen / lg.width
    lg = lg.resize((gen, int(lg.height * o)), Image.LANCZOS)
    im.alpha_composite(lg, (x, y))
    return lg.height


def hap(dr, cx, y, t, f, dolgu, yazi, pad=26, hh=None):
    """Ortalanmış hap rozet; genişliğini metinden alır."""
    tw = dr.textlength(t, font=f)
    hh = hh or (f.size + 2 * 14)
    x0 = cx - tw / 2 - pad
    dr.rounded_rectangle([x0, y, cx + tw / 2 + pad, y + hh], radius=hh / 2, fill=dolgu)
    dr.text((cx, y + hh / 2), t, font=f, fill=yazi, anchor="mm")
    return hh


def alt_bant(im, dr, koyu=True):
    """Alt yasal satır + CTA."""
    f1 = mont("SemiBold", 26)
    f2 = mont("Regular", 19)
    renk1 = BEYAZ if koyu else GECE
    renk2 = SIS if koyu else KURSUN
    dr.text((W / 2, H - 92), CTA, font=f1, fill=renk1, anchor="mm")
    dr.text((W / 2, H - 46), YASAL, font=f2, fill=renk2, anchor="mm")


def yok_seridi(dr, y, maddeler, koyu=True, boy=30):
    """'BANKA YOK · FAİZ YOK …' tek satır şerit, elmas ayraçlı."""
    f = mont("Bold", boy)
    parca = [(m, dr.textlength(m, font=f)) for m in maddeler]
    ara = 46
    toplam = sum(p[1] for p in parca) + ara * (len(parca) - 1)
    x = (W - toplam) / 2
    renk = BEYAZ if koyu else GECE
    for i, (m, tw) in enumerate(parca):
        dr.text((x, y), m, font=f, fill=renk, anchor="lm")
        x += tw
        if i < len(parca) - 1:
            elmas_dolu(dr, x + ara / 2, y, 12, CAM if koyu else VURGU)
            x += ara


def kaydet(im, ad):
    im.convert("RGB").save(os.path.join(OUT, ad + ".jpg"), quality=92, optimize=True)
    print("  ", ad)


# ═══════════════════════════════════════════════════════════ GÖRSELLER
def g01():
    """Tam kanama gece render + üç büyük YOK — manifesto."""
    im = perde(foto("night-gate.webp", W, H, 0.5, 1.05),
               [(0, 0.30), (0.45, 0.55), (1, 0.92)]).convert("RGBA")
    dr = ImageDraw.Draw(im)
    logo(im, "mia-beyaz", (W - 340) // 2, 70, 340)
    fB = mont("Bold", 108)
    for i, t in enumerate(["BANKA YOK.", "FAİZ YOK.", "KEFİL YOK."]):
        dr.text((W / 2, 560 + i * 128), t, font=fB, fill=BEYAZ, anchor="mm")
    elmas_dolu(dr, W / 2, 980, 18, CAM)
    dr.text((W / 2, 1052), "60 AY SABİT TAKSİTLE EV SAHİBİ OLUN",
            font=mont("SemiBold", 40), fill=SIS, anchor="mm")
    hap(dr, W / 2, 1110, "İZMİT MİA BÖLGESİ · 600 KONUT", mont("Bold", 30), CAM, GECE)
    alt_bant(im, dr)
    kaydet(im, "meta-01-banka-faiz-kefil")


def g02():
    """Dev 60 — açık zemin, elmas fotoğraf."""
    im = Image.new("RGBA", (W, H), KAGIT + (255,))
    dr = ImageDraw.Draw(im)
    logo(im, "mia-renkli", (W - 300) // 2, 64, 300)
    dr.text((W / 2, 420), "60 AY", font=mont("Bold", 230), fill=GECE, anchor="mm")
    dr.text((W / 2, 585), "SABİT TAKSİT", font=mont("Bold", 64), fill=VURGU, anchor="mm")
    ef = elmas_foto("hero-courtyard-dusk.webp", 520, 0.5, 1.1)
    im.alpha_composite(ef, (W // 2 - 260, 660))
    elmas_cizgi(dr, W / 2, 920, 590, VURGU, 3)
    elmas_dolu(dr, 150, 700, 34, VURGU)
    elmas_cizgi(dr, 940, 1140, 60, VURGU, 3)
    yok_seridi(dr, 1225, ["BANKA YOK", "FAİZ YOK", "KEFİL YOK"], koyu=False, boy=32)
    dr.text((W / 2, H - 92), CTA, font=mont("SemiBold", 26), fill=GECE, anchor="mm")
    dr.text((W / 2, H - 46), YASAL, font=mont("Regular", 19), fill=KURSUN, anchor="mm")
    kaydet(im, "meta-02-60-ay")


def g03():
    """Onay listesi kartı — koyu zemin."""
    im = Image.new("RGBA", (W, H), GECE + (255,))
    dr = ImageDraw.Draw(im)
    ust = foto("balcony-dusk.webp", W, 430, 0.55, 1.1)
    im.paste(ust, (0, 0))
    im2 = perde(im.convert("RGB"), [(0, 0), (0.24, 0.10), (0.32, 0.95), (1, 1.0)]).convert("RGBA")
    dr = ImageDraw.Draw(im2)
    logo(im2, "mia-beyaz", 60, 56, 250)
    dr.text((W / 2, 520), "ÖDEME PLANINDA", font=mont("SemiBold", 40), fill=SIS, anchor="mm")
    dr.text((W / 2, 588), "SÜRPRİZ YOK", font=mont("Bold", 84), fill=BEYAZ, anchor="mm")
    maddeler = ["Banka yok, kredi dosyası yok", "Faiz yok, vade farkı yok",
                "Ara ödeme yok, balon ödeme yok", "Komisyon yok",
                "60 ay sabit taksit"]
    fM = mont("SemiBold", 38)
    y = 700
    for m in maddeler:
        elmas_dolu(dr, 150, y, 26, CAM)
        dr.line([(141, y), (149, y + 9), (163, y - 9)], fill=GECE, width=5, joint="curve")
        dr.text((200, y), m, font=fM, fill=BEYAZ, anchor="lm")
        y += 86
    alt_bant(im2, dr)
    kaydet(im2, "meta-03-surpriz-yok")


def g04():
    """KOMİSYON YOK odaklı — açık, büyük tipografi + küçük elmas foto."""
    im = Image.new("RGBA", (W, H), KAGIT + (255,))
    dr = ImageDraw.Draw(im)
    logo(im, "mia-renkli", 60, 60, 270)
    logo(im, "ocean-renkli", W - 260, 78, 200)
    dr.text((90, 360), "KOMİSYON", font=mont("Bold", 118), fill=GECE, anchor="lm")
    dr.text((90, 490), "YOK.", font=mont("Bold", 118), fill=VURGU, anchor="lm")
    dr.text((90, 610), "Kooperatiften doğrudan ortaklık;", font=mont("Regular", 40), fill=KURSUN, anchor="lm")
    dr.text((90, 664), "aracı maliyeti ödemezsiniz.", font=mont("Regular", 40), fill=KURSUN, anchor="lm")
    ef = elmas_foto("entrance-gate.webp", 460, 0.45, 1.2)
    im.alpha_composite(ef, (560, 700))
    elmas_cizgi(dr, 790, 930, 520, VURGU, 3)
    elmas_dolu(dr, 250, 860, 30, VURGU)
    elmas_cizgi(dr, 180, 1000, 70, VURGU, 3)
    yok_seridi(dr, 1222, ["BANKA YOK", "FAİZ YOK", "60 AY SABİT TAKSİT"], koyu=False, boy=30)
    dr.text((W / 2, H - 92), CTA, font=mont("SemiBold", 26), fill=GECE, anchor="mm")
    dr.text((W / 2, H - 46), YASAL, font=mont("Regular", 19), fill=KURSUN, anchor="mm")
    kaydet(im, "meta-04-komisyon-yok")


def g05():
    """%0 dev rakam — koyu, tam kanama."""
    im = perde(foto("hero-courtyard-dusk.webp", W, H, 0.5, 1.05),
               [(0, 0.55), (0.5, 0.72), (1, 0.94)]).convert("RGBA")
    dr = ImageDraw.Draw(im)
    logo(im, "mia-beyaz", (W - 320) // 2, 66, 320)
    dr.text((W / 2, 540), "%0", font=mont("Bold", 330), fill=(72, 171, 197), anchor="mm")
    dr.text((W / 2, 780), "FAİZ · VADE FARKI · KOMİSYON", font=mont("Bold", 46), fill=BEYAZ, anchor="mm")
    dr.text((W / 2, 860), "Tasarrufa dayalı faizsiz finansman", font=mont("Regular", 36), fill=SIS, anchor="mm")
    hap(dr, W / 2, 950, "60 AY SABİT TAKSİT", mont("Bold", 40), CAM, GECE, pad=40)
    dr.text((W / 2, 1120), "İzmit MİA Bölgesi'nde 600 konut", font=mont("SemiBold", 34), fill=BEYAZ, anchor="mm")
    alt_bant(im, dr)
    kaydet(im, "meta-05-yuzde-sifir")


def g06():
    """X / ✓ karşılaştırma: kredi vs kooperatif."""
    im = Image.new("RGBA", (W, H), KAGIT + (255,))
    dr = ImageDraw.Draw(im)
    logo(im, "mia-renkli", (W - 280) // 2, 56, 280)
    dr.text((W / 2, 330), "EV ALMANIN İKİ YOLU", font=mont("Bold", 56), fill=GECE, anchor="mm")
    # sol: banka — sağ: mia
    kx, ky, kw, kh = 60, 420, 460, 620
    dr.rounded_rectangle([kx, ky, kx + kw, ky + kh], radius=18, fill=AYRAC)
    dr.rounded_rectangle([kx + 500, ky, kx + 500 + kw, ky + kh], radius=18, fill=GECE)
    dr.text((kx + kw / 2, ky + 70), "BANKA KREDİSİ", font=mont("Bold", 36), fill=KURSUN, anchor="mm")
    dr.text((kx + 500 + kw / 2, ky + 70), "MİA PARK OCEAN", font=mont("Bold", 36), fill=CAM, anchor="mm")
    sol = ["Faiz yükü", "Kredi dosyası", "Kefil şartı", "Komisyonlar", "Değişken taksit"]
    sag = ["Faiz yok", "Banka yok", "Kefil yok", "Komisyon yok", "60 ay sabit taksit"]
    fL = mont("SemiBold", 33)
    for i in range(5):
        y = ky + 150 + i * 92
        dr.line([(kx + 52, y - 12), (kx + 76, y + 12)], fill=(160, 80, 80), width=7)
        dr.line([(kx + 76, y - 12), (kx + 52, y + 12)], fill=(160, 80, 80), width=7)
        dr.text((kx + 105, y), sol[i], font=fL, fill=KURSUN, anchor="lm")
        elmas_dolu(dr, kx + 500 + 64, y, 24, CAM)
        dr.line([(kx + 500 + 56, y), (kx + 500 + 63, y + 8), (kx + 500 + 76, y - 8)],
                fill=GECE, width=4, joint="curve")
        dr.text((kx + 500 + 100, y), sag[i], font=fL, fill=BEYAZ, anchor="lm")
    dr.text((W / 2, 1130), "Tercih sizin.", font=mont("Bold", 48), fill=VURGU, anchor="mm")
    dr.text((W / 2, H - 92), CTA, font=mont("SemiBold", 26), fill=GECE, anchor="mm")
    dr.text((W / 2, H - 46), YASAL, font=mont("Regular", 19), fill=KURSUN, anchor="mm")
    kaydet(im, "meta-06-karsilastirma")


def g07():
    """Soru-cevap: 'Kredim çıkmazsa?'"""
    im = perde(foto("street-corner.webp", W, H, 0.40, 1.15),
               [(0, 0.62), (0.45, 0.80), (1, 0.95)]).convert("RGBA")
    dr = ImageDraw.Draw(im)
    logo(im, "mia-beyaz", (W - 300) // 2, 64, 300)
    dr.text((W / 2, 430), "— Kredim çıkmazsa?", font=mont("SemiBold", 62), fill=SIS, anchor="mm")
    dr.text((W / 2, 585), "ÇIKMASIN.", font=mont("Bold", 130), fill=BEYAZ, anchor="mm")
    dr.text((W / 2, 720), "BANKA ZATEN YOK.", font=mont("Bold", 66), fill=(72, 171, 197), anchor="mm")
    dr.text((W / 2, 850), "Faizsiz, kefilsiz, komisyonsuz —", font=mont("Regular", 38), fill=BEYAZ, anchor="mm")
    dr.text((W / 2, 904), "60 ay sabit taksitle.", font=mont("Regular", 38), fill=BEYAZ, anchor="mm")
    hap(dr, W / 2, 1010, "İZMİT MİA BÖLGESİ", mont("Bold", 32), CAM, GECE, pad=34)
    alt_bant(im, dr)
    kaydet(im, "meta-07-kredim-cikmazsa")


def g08():
    """Konum + rozetler — açık, yatay foto bandı."""
    im = Image.new("RGBA", (W, H), KAGIT + (255,))
    dr = ImageDraw.Draw(im)
    bant = foto("ic-mekan/21-balkondan-deniz.webp", W - 120, 540, 0.5, 1.0)
    im.paste(bant, (60, 210))
    elmas_cizgi(dr, 60 + 40, 210 + 40, 90, BEYAZ, 4)
    logo(im, "mia-renkli", (W - 280) // 2, 48, 280)
    dr.text((W / 2, 850), "İZMİT MİA BÖLGESİ", font=mont("Bold", 76), fill=GECE, anchor="mm")
    dr.text((W / 2, 928), "D100'e 1 dk · Sahile 2 dk · Merkeze 5 dk",
            font=mont("SemiBold", 36), fill=VURGU, anchor="mm")
    y = 1035
    for t in ["600 KONUT", "60 AY SABİT TAKSİT", "BANKA · FAİZ · KEFİL YOK"]:
        hap(dr, W / 2, y, t, mont("Bold", 30), GECE, CAM, pad=34)
        y += 88
    dr.text((W / 2, H - 46), YASAL, font=mont("Regular", 19), fill=KURSUN, anchor="mm")
    kaydet(im, "meta-08-konum")


def g09():
    """'Kiracıya değil, kendi evinize' — duygusal + rozet."""
    im = perde(foto("terrace-pergola.webp", W, H, 0.5, 1.1),
               [(0, 0.20), (0.40, 0.42), (1, 0.93)]).convert("RGBA")
    dr = ImageDraw.Draw(im)
    logo(im, "mia-beyaz", 60, 56, 260)
    dr.text((90, 700), "HER TAKSİT,", font=mont("Bold", 88), fill=BEYAZ, anchor="lm")
    dr.text((90, 800), "KENDİ EVİNİZE.", font=mont("Bold", 88), fill=(72, 171, 197), anchor="lm")
    dr.text((90, 906), "Faizsiz ve sabit taksitli kooperatif modeli:", font=mont("Regular", 36), fill=SIS, anchor="lm")
    dr.text((90, 956), "ödediğiniz her kuruş konutunuza yazılır.", font=mont("Regular", 36), fill=SIS, anchor="lm")
    yok_seridi(dr, 1080, ["BANKA YOK", "FAİZ YOK", "ARA ÖDEME YOK"], koyu=True, boy=30)
    alt_bant(im, dr)
    kaydet(im, "meta-09-kendi-evinize")


def g10():
    """YOK listesi — saf tipografik poster."""
    im = Image.new("RGBA", (W, H), GECE + (255,))
    dr = ImageDraw.Draw(im)
    logo(im, "mia-beyaz", (W - 300) // 2, 70, 300)
    maddeler = ["BANKA", "FAİZ", "KEFİL", "KOMİSYON", "ARA ÖDEME", "BALON ÖDEME"]
    fY = mont("Bold", 76)
    fyok = mont("Bold", 76)
    y = 400
    for m in maddeler:
        tw = dr.textlength(m + "  ", font=fY) + dr.textlength("YOK", font=fyok)
        x = (W - tw) / 2
        dr.text((x, y), m, font=fY, fill=BEYAZ, anchor="lm")
        dr.text((x + dr.textlength(m + "  ", font=fY), y), "YOK",
                font=fyok, fill=(72, 171, 197), anchor="lm")
        y += 108
    elmas_cizgi(dr, 120, 330, 70, CAM, 3)
    elmas_dolu(dr, 960, 1060, 26, CAM)
    hap(dr, W / 2, 1105, "VAR OLAN TEK ŞEY: 60 AY SABİT TAKSİT",
        mont("Bold", 31), CAM, GECE, pad=36)
    alt_bant(im, dr)
    kaydet(im, "meta-10-yok-listesi")


def kontak():
    fs = sorted(f for f in os.listdir(OUT) if f.startswith("meta-") and f.endswith(".jpg"))
    tw = 360
    th = int(tw * H / W)
    cols, rows = 5, 2
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * 8, rows * th + (rows + 1) * 8), (16, 20, 26))
    for i, f in enumerate(fs[:10]):
        im = Image.open(os.path.join(OUT, f)).resize((tw, th), Image.LANCZOS)
        sheet.paste(im, (8 + (i % cols) * (tw + 8), 8 + (i // cols) * (th + 8)))
    sheet.save(os.path.join(OUT, "kontak.jpg"), quality=88)
    print("   kontak.jpg")


if __name__ == "__main__":
    for g in [g01, g02, g03, g04, g05, g06, g07, g08, g09, g10]:
        g()
    kontak()
    print("tamam ->", OUT)
