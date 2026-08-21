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
    hap(dr, W / 2, 1110, "İZMİT MİA BÖLGESİ", mont("Bold", 30), CAM, GECE)
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



# ═══════════════════════════ V2 — KAZANAN KALIP GRAMERİ ═══════════════════
# TR faizsiz-konut kategorisinin tutan dili: üçlü YOK kısaltması/mührü,
# dev tek rakam, tam genişlik iddia bantları, ✗/✓ karşıtlığı, WhatsApp
# yeşili buton + büyük numara, dürüst aciliyet şeridi (lansman gerçek).
WA_YESIL = (37, 211, 102)
TEL = "0540 028 00 41"


def wa_buton(im, dr, cy, t="WHATSAPP'TAN YAZIN", gen=560, yuk=92, tel=True):
    """WhatsApp yeşili hap buton + ahize-balon ikonu + numara altta."""
    x0 = (W - gen) / 2
    dr.rounded_rectangle([x0, cy, x0 + gen, cy + yuk], radius=yuk / 2, fill=WA_YESIL)
    # ikon: beyaz konuşma balonu + ahize
    ic = cy + yuk / 2
    bx = x0 + 62
    dr.ellipse([bx - 26, ic - 26, bx + 26, ic + 26], fill=BEYAZ)
    dr.polygon([(bx - 18, ic + 14), (bx - 8, ic + 26), (bx - 4, ic + 12)], fill=BEYAZ)
    dr.arc([bx - 14, ic - 14, bx + 14, ic + 14], 200, 40, fill=WA_YESIL, width=7)
    f = mont("Bold", 34)
    dr.text((x0 + gen / 2 + 28, ic), t, font=f, fill=BEYAZ, anchor="mm")
    if tel:
        py = min(H - 60, cy + yuk + 44)
        koyu = im.getpixel((int(W / 2), int(py)))[0] < 128
        dr.text((W / 2, py), TEL, font=mont("Bold", 40),
                fill=BEYAZ if koyu else GECE, anchor="mm")


def yasal(dr, koyu=True, y=None):
    y = y or H - 34
    dr.text((W / 2, y), YASAL, font=mont("Regular", 18),
            fill=SIS if koyu else KURSUN, anchor="mm")


def serit_kurdele(im, dr, t="LANSMANA ÖZEL DÖNEM"):
    """Sol üst çapraz kurdele — köşegeni tam kaplar, metin köşede okunur."""
    B = 860
    kat = Image.new("RGBA", (B, B), (0, 0, 0, 0))
    kd = ImageDraw.Draw(kat)
    bant = Image.new("RGBA", (int(B * 1.5), 96), (72, 171, 197, 255))
    bd = ImageDraw.Draw(bant)
    bd.text((bant.width / 2, 48), t, font=mont("Bold", 34), fill=(4, 40, 58, 255), anchor="mm")
    bant = bant.rotate(-45, expand=True, resample=Image.BICUBIC)
    # bandın merkezi köşegen üstünde (k, k) noktasına gelsin
    k = 235
    kat.alpha_composite(bant, (int(k - bant.width / 2), int(k - bant.height / 2)))
    im.alpha_composite(kat, (0, 0))


def v01():
    """Üç tam genişlik iddia bandı — kategori klasiği, dev punto."""
    im = perde(foto("night-gate.webp", W, H, 0.5, 1.05),
               [(0, 0.10), (0.55, 0.16), (0.72, 0.62), (1, 0.94)]).convert("RGBA")
    dr = ImageDraw.Draw(im)
    logo(im, "mia-beyaz", (W - 320) // 2, 56, 320)
    bantlar = [("BANKA", "YOK"), ("FAİZ", "YOK"), ("KEFİL", "YOK")]
    y = 360
    fA = mont("Bold", 96)
    for i, (a, b) in enumerate(bantlar):
        renk = (10, 58, 85, 235) if i % 2 == 0 else (26, 116, 150, 235)
        kat = Image.new("RGBA", (W, 150), renk)
        im.alpha_composite(kat, (0, y))
        dr.text((W / 2 - 90, y + 75), a, font=fA, fill=BEYAZ, anchor="rm")
        dr.text((W / 2 - 50, y + 75), "YOK", font=fA, fill=(72, 171, 197) if i % 2 == 0 else GECE, anchor="lm")
        y += 172
    dr.text((W / 2, y + 60), "60 AY SABİT TAKSİT · %30 PEŞİNAT",
            font=mont("Bold", 44), fill=BEYAZ, anchor="mm")
    wa_buton(im, dr, y + 130)
    yasal(dr)
    kaydet(im, "meta-v2-01-uc-bant")


def v02():
    """%0 FAİZ mührü — damga estetiği."""
    im = perde(foto("hero-courtyard-dusk.webp", W, H, 0.5, 1.05),
               [(0, 0.12), (0.55, 0.20), (0.72, 0.60), (1, 0.94)]).convert("RGBA")
    dr = ImageDraw.Draw(im)
    logo(im, "mia-beyaz", (W - 300) // 2, 54, 300)
    cx, cy, R = W / 2, 560, 300
    # mühür içi lokal koyuluk — rakam okunur, çevrede proje görünür
    sc = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sc)
    sd.ellipse([cx - R + 14, cy - R + 14, cx + R - 14, cy + R - 14], fill=(4, 40, 58, 150))
    im.alpha_composite(sc)
    for r, wdt in [(R, 10), (R - 26, 4)]:
        dr.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(72, 171, 197), width=wdt)
    dr.text((cx, cy - 78), "%0", font=mont("Bold", 210), fill=BEYAZ, anchor="mm")
    dr.text((cx, cy + 92), "FAİZ", font=mont("Bold", 96), fill=(72, 171, 197), anchor="mm")
    dr.text((cx, cy + 180), "VADE FARKI YOK · KOMİSYON YOK", font=mont("SemiBold", 30),
            fill=SIS, anchor="mm")
    # kurdele bant
    ky = 950
    dr.rectangle([0, ky, W, ky + 96], fill=(26, 116, 150))
    dr.text((W / 2, ky + 48), "60 AY SABİT TAKSİT", font=mont("Bold", 52), fill=BEYAZ, anchor="mm")
    wa_buton(im, dr, 1105)
    yasal(dr)
    kaydet(im, "meta-v2-02-muhur")


def v03():
    """6 YOK + 1 VAR — pul ızgarası."""
    im = Image.new("RGBA", (W, H), GECE + (255,))
    dr = ImageDraw.Draw(im)
    logo(im, "mia-beyaz", (W - 300) // 2, 60, 300)
    dr.text((W / 2, 300), "BU PROJEDE", font=mont("SemiBold", 40), fill=SIS, anchor="mm")
    puls = ["BANKA", "FAİZ", "KEFİL", "KOMİSYON", "ARA ÖDEME", "BALON"]
    fP = mont("Bold", 40); fY = mont("Bold", 34)
    for i, t in enumerate(puls):
        r, c = divmod(i, 2)
        cx = W / 2 - 245 + c * 490
        cy = 430 + r * 170
        dr.rounded_rectangle([cx - 225, cy - 62, cx + 225, cy + 62], radius=28,
                             fill=(10, 58, 85), outline=(72, 171, 197), width=3)
        dr.text((cx, cy - 16), t, font=fP, fill=BEYAZ, anchor="mm")
        dr.text((cx, cy + 30), "YOK", font=fY, fill=(72, 171, 197), anchor="mm")
    dr.text((W / 2, 985), "VAR OLAN TEK ŞEY:", font=mont("SemiBold", 34), fill=SIS, anchor="mm")
    dr.text((W / 2, 1055), "60 AY SABİT TAKSİT", font=mont("Bold", 72), fill=BEYAZ, anchor="mm")
    wa_buton(im, dr, 1120)
    yasal(dr)
    kaydet(im, "meta-v2-03-pul-izgara")


def v04():
    """Dev 60 — sayfayı kaplayan rakam."""
    im = perde(foto("balcony-dusk.webp", W, H, 0.55, 1.1),
               [(0, 0.14), (0.48, 0.24), (0.66, 0.62), (1, 0.94)]).convert("RGBA")
    dr = ImageDraw.Draw(im)
    logo(im, "mia-beyaz", (W - 300) // 2, 50, 300)
    dr.text((W / 2 + 8, 528), "60", font=mont("Bold", 470), fill=(4, 40, 58), anchor="mm")
    dr.text((W / 2, 520), "60", font=mont("Bold", 470), fill=BEYAZ, anchor="mm")
    dr.text((W / 2, 810), "AY SABİT TAKSİT", font=mont("Bold", 76), fill=(72, 171, 197), anchor="mm")
    dr.text((W / 2, 895), "Bugün belirlenen taksit 60 ay değişmez.",
            font=mont("Regular", 34), fill=SIS, anchor="mm")
    yok_seridi(dr, 975, ["BANKA YOK", "FAİZ YOK", "KEFİL YOK"], koyu=True, boy=34)
    wa_buton(im, dr, 1050)
    yasal(dr)
    kaydet(im, "meta-v2-04-dev-60")


def v05():
    """✗ / ✓ dev karşıtlık."""
    im = Image.new("RGBA", (W, H), KAGIT + (255,))
    dr = ImageDraw.Draw(im)
    logo(im, "mia-renkli", (W - 280) // 2, 54, 280)
    ust = ["KREDİ", "FAİZ", "KEFİL"]
    fX = mont("Bold", 74)
    y = 350
    for t in ust:
        x0 = W / 2 - (dr.textlength("✗  " + t + "  DERDİ", font=fX)) / 2
        dr.line([(x0 + 6, y - 22), (x0 + 50, y + 22)], fill=(163, 74, 74), width=13)
        dr.line([(x0 + 50, y - 22), (x0 + 6, y + 22)], fill=(163, 74, 74), width=13)
        dr.text((x0 + 76, y), t + " DERDİ", font=fX, fill=KURSUN, anchor="lm")
        y += 118
    dr.text((W / 2, y + 30), "BURADA YOK.", font=mont("Bold", 110), fill=GECE, anchor="mm")
    y += 170
    dr.rectangle([0, y, W, y + 108], fill=GECE)
    elmas_dolu(dr, W / 2 - 400, y + 54, 30, (72, 171, 197))
    dr.line([(W / 2 - 410, y + 54), (W / 2 - 400, y + 66), (W / 2 - 384, y + 40)],
            fill=GECE, width=6, joint="curve")
    dr.text((W / 2 + 16, y + 54), "60 AY SABİT TAKSİT · %30 PEŞİNAT",
            font=mont("Bold", 42), fill=BEYAZ, anchor="mm")
    wa_buton(im, dr, y + 160)
    yasal(dr, koyu=False)
    kaydet(im, "meta-v2-05-carpi-tik")


def v06():
    """Lansman kurdelesi + yok pulları serpme."""
    im = perde(foto("entrance-gate.webp", W, H, 0.45, 1.15),
               [(0, 0.08), (0.42, 0.16), (0.60, 0.60), (1, 0.94)]).convert("RGBA")
    dr = ImageDraw.Draw(im)
    serit_kurdele(im, dr)
    logo(im, "mia-beyaz", W - 360, 56, 300)
    dr.text((W / 2, 628), "İZMİT MİA BÖLGESİ'NDE", font=mont("SemiBold", 40), fill=BEYAZ, anchor="mm")
    dr.text((W / 2, 706), "EV SAHİBİ OLUN", font=mont("Bold", 92), fill=BEYAZ, anchor="mm")
    puls = ["BANKA YOK", "FAİZ YOK", "KEFİL YOK", "KOMİSYON YOK", "ARA ÖDEME YOK"]
    fP = mont("Bold", 30)
    y = 830
    x = 90
    for t in puls:
        tw = dr.textlength(t, font=fP) + 56
        if x + tw > W - 90:
            x = 90; y += 96
        dr.rounded_rectangle([x, y, x + tw, y + 74], radius=37,
                             fill=(10, 58, 85, 220), outline=(72, 171, 197), width=3)
        dr.text((x + tw / 2, y + 37), t, font=fP, fill=BEYAZ, anchor="mm")
        x += tw + 26
    dr.text((W / 2, y + 150), "21 AĞUSTOS'TA LANSMAN · 60 AY SABİT TAKSİT",
            font=mont("Bold", 34), fill=(72, 171, 197), anchor="mm")
    wa_buton(im, dr, y + 196, tel=False)
    yasal(dr)
    kaydet(im, "meta-v2-06-lansman")


def v07():
    """WhatsApp sohbeti kalıbı — temsili yazışma."""
    im = Image.new("RGBA", (W, H), GECE + (255,))
    dr = ImageDraw.Draw(im)
    logo(im, "mia-beyaz", (W - 300) // 2, 56, 300)
    dr.text((W / 2, 300), "TEMSİLİ YAZIŞMA", font=mont("SemiBold", 22),
            fill=(126, 154, 171), anchor="mm")
    def balon(t1, t2, y, sag=False, renk=(10, 58, 85), yazi=BEYAZ):
        fB = mont("SemiBold", 34)
        wmax = max(dr.textlength(t1, font=fB), dr.textlength(t2, font=fB) if t2 else 0) + 66
        h = 136 if t2 else 92
        x0 = W - 90 - wmax if sag else 90
        dr.rounded_rectangle([x0, y, x0 + wmax, y + h], radius=28, fill=renk)
        dr.text((x0 + 33, y + 46), t1, font=fB, fill=yazi, anchor="lm")
        if t2:
            dr.text((x0 + 33, y + 96), t2, font=fB, fill=yazi, anchor="lm")
        return y + h + 26
    y = 340
    y = balon("Merhaba, ev bakıyorum ama", "bankadan kredim çıkmıyor…", y, sag=False,
              renk=(233, 240, 244), yazi=GECE)
    y = balon("Bizde banka YOK, faiz YOK,", "kefil YOK 🙂", y, sag=True,
              renk=WA_YESIL, yazi=GECE)
    y = balon("Taksitler artar mı?", None, y, sag=False, renk=(233, 240, 244), yazi=GECE)
    y = balon("60 ay SABİT. Ara ödeme ve", "balon ödeme de YOK.", y, sag=True,
              renk=WA_YESIL, yazi=GECE)
    y = balon("Nasıl başvuruyorum?", None, y, sag=False, renk=(233, 240, 244), yazi=GECE)
    dr.text((W / 2, y + 34), "CEVABI SİZ YAZIN:", font=mont("Bold", 30),
            fill=(72, 171, 197), anchor="mm")
    wa_buton(im, dr, y + 74, tel=False)
    yasal(dr)
    kaydet(im, "meta-v2-07-sohbet")


def v08():
    """Kilitli taksit — dev kilit + sabitlik vurgusu."""
    im = perde(foto("terrace-pergola.webp", W, H, 0.5, 1.1),
               [(0, 0.10), (0.42, 0.20), (0.60, 0.62), (1, 0.94)]).convert("RGBA")
    dr = ImageDraw.Draw(im)
    logo(im, "mia-beyaz", (W - 300) // 2, 52, 300)
    cx, cy = W / 2, 470
    dr.rounded_rectangle([cx - 130, cy - 20, cx + 130, cy + 170], radius=34,
                         fill=(72, 171, 197))
    dr.arc([cx - 88, cy - 150, cx + 88, cy + 30], 180, 360, fill=(72, 171, 197), width=34)
    dr.ellipse([cx - 26, cy + 34, cx + 26, cy + 86], fill=GECE)
    dr.rectangle([cx - 12, cy + 70, cx + 12, cy + 130], fill=GECE)
    dr.text((W / 2, 780), "TAKSİTİNİZ", font=mont("Bold", 76), fill=BEYAZ, anchor="mm")
    dr.text((W / 2, 872), "60 AY KİLİTLİ", font=mont("Bold", 100), fill=(72, 171, 197), anchor="mm")
    dr.text((W / 2, 968), "Zam yok, sürpriz yok: ara ödeme YOK, balon ödeme YOK.",
            font=mont("SemiBold", 32), fill=SIS, anchor="mm")
    yok_seridi(dr, 1030, ["BANKA YOK", "FAİZ YOK", "KEFİL YOK"], koyu=True, boy=30)
    wa_buton(im, dr, 1090)
    yasal(dr)
    kaydet(im, "meta-v2-08-kilitli-taksit")


def kontak_v2():
    fs = sorted(f for f in os.listdir(OUT) if f.startswith("meta-v2-") and f.endswith(".jpg"))
    tw = 430
    th = int(tw * H / W)
    cols, rows = 4, 2
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * 8, rows * th + (rows + 1) * 8), (16, 20, 26))
    for i, f in enumerate(fs[:8]):
        im = Image.open(os.path.join(OUT, f)).resize((tw, th), Image.LANCZOS)
        sheet.paste(im, (8 + (i % cols) * (tw + 8), 8 + (i // cols) * (th + 8)))
    sheet.save(os.path.join(OUT, "kontak-v2.jpg"), quality=88)
    print("   kontak-v2.jpg")



# ═══════════════════ V3 — PROJE KAHRAMAN (fotoğraf üstünde yazı YOK) ═══════
# Geri bildirim: "fotoğrafın üstüne yazmıştın, proje görünmüyor."
# Bu sette render'a hiçbir şey binmiyor — logo dahil. Bütün mesaj, fotoğrafın
# dışındaki düz panelde. Metinler copywriter prensibiyle kısaltıldı:
# fayda dili ("taksitin değişmez", "sürpriz yok"), tek aksiyon CTA'sı.

def panel_icerik(im, dr, y0, y1, baslik1, baslik2, altyazi, acik=False):
    """Panele: logo + başlık(lar) + yok satırı + buton + tel + yasal."""
    zem = KAGIT if acik else GECE
    dr.rectangle([0, y0, W, y1], fill=zem)
    dr.rectangle([0, y0, W, y0 + 8], fill=CAM)          # foto-panel ayracı
    logo(im, "mia-renkli" if acik else "mia-beyaz", (W - 190) // 2, y0 + 18, 190)
    ana = GECE if acik else BEYAZ
    dr.text((W / 2, y0 + 196), baslik1, font=mont("Bold", 58 if baslik2 else 66),
            fill=ana, anchor="mm")
    if baslik2:
        dr.text((W / 2, y0 + 258), baslik2, font=mont("Bold", 40),
                fill=VURGU if acik else CAM, anchor="mm")
    dr.text((W / 2, y0 + (306 if baslik2 else 258)), altyazi,
            font=mont("SemiBold", 28), fill=KURSUN if acik else SIS, anchor="mm")
    by = y0 + (344 if baslik2 else 296)
    x0 = (W - 500) / 2
    dr.rounded_rectangle([x0, by, x0 + 500, by + 72], radius=36, fill=WA_YESIL)
    ic = by + 36
    bx = x0 + 52
    dr.ellipse([bx - 21, ic - 21, bx + 21, ic + 21], fill=BEYAZ)
    dr.polygon([(bx - 14, ic + 11), (bx - 6, ic + 21), (bx - 2, ic + 9)], fill=BEYAZ)
    dr.arc([bx - 11, ic - 11, bx + 11, ic + 11], 200, 40, fill=WA_YESIL, width=6)
    dr.text((x0 + 500 / 2 + 22, ic), "WHATSAPP'TAN YAZIN", font=mont("Bold", 29),
            fill=BEYAZ, anchor="mm")
    dr.text((W / 2, by + 104), TEL, font=mont("Bold", 33), fill=ana, anchor="mm")
    dr.text((W / 2, y1 - 22), YASAL, font=mont("Regular", 17),
            fill=KURSUN if acik else (126, 154, 171), anchor="mm")


def u_split_alt(ad, kaynak, focus, zoom, b1, b2, alt):
    """Foto üstte TEMİZ (%60), panel altta."""
    im = Image.new("RGBA", (W, H))
    im.paste(foto(kaynak, W, 810, focus, zoom), (0, 0))
    dr = ImageDraw.Draw(im)
    panel_icerik(im, dr, 810, H, b1, b2, alt)
    kaydet(im, ad)


def u_split_ust(ad, kaynak, focus, zoom, b1, b2, alt):
    """Panel üstte, foto altta TEMİZ (%60) — akışta önce mesaj görünür."""
    im = Image.new("RGBA", (W, H))
    im.paste(foto(kaynak, W, 810, focus, zoom), (0, 540))
    dr = ImageDraw.Draw(im)
    panel_icerik(im, dr, 0, 540, b1, b2, alt)
    # ayracı alta çevir
    dr.rectangle([0, 532, W, 540], fill=CAM)
    kaydet(im, ad)


def u_cerceve(ad, kaynak, focus, zoom, b1, alt):
    """Açık zemin; foto ortada büyük ve çerçeveli, yazılar dışında."""
    im = Image.new("RGBA", (W, H), KAGIT + (255,))
    dr = ImageDraw.Draw(im)
    logo(im, "mia-renkli", (W - 250) // 2, 40, 250)
    dr.text((W / 2, 258), b1, font=mont("Bold", 66), fill=GECE, anchor="mm")
    fy0, fy1 = 330, 1030
    im.paste(foto(kaynak, W - 112, fy1 - fy0, focus, zoom), (56, fy0))
    dr.rectangle([56, fy0, W - 56, fy1], outline=VURGU, width=4)
    elmas_dolu(dr, 56, fy0, 26, VURGU)
    elmas_dolu(dr, W - 56, fy1, 26, VURGU)
    dr.text((W / 2, 1080), alt, font=mont("Bold", 34), fill=VURGU, anchor="mm")
    x0 = (W - 520) / 2
    by = 1128
    dr.rounded_rectangle([x0, by, x0 + 520, by + 78], radius=39, fill=WA_YESIL)
    ic = by + 39
    bx = x0 + 56
    dr.ellipse([bx - 22, ic - 22, bx + 22, ic + 22], fill=BEYAZ)
    dr.polygon([(bx - 15, ic + 12), (bx - 7, ic + 22), (bx - 3, ic + 10)], fill=BEYAZ)
    dr.arc([bx - 12, ic - 12, bx + 12, ic + 12], 200, 40, fill=WA_YESIL, width=6)
    dr.text((x0 + 520 / 2 + 24, ic), "WHATSAPP'TAN YAZIN", font=mont("Bold", 30),
            fill=BEYAZ, anchor="mm")
    dr.text((W / 2, by + 116), TEL, font=mont("Bold", 34), fill=GECE, anchor="mm")
    dr.text((W / 2, H - 26), YASAL, font=mont("Regular", 17), fill=KURSUN, anchor="mm")
    kaydet(im, ad)


def v3_hepsi():
    u_split_alt("meta-v3-01-gece", "night-gate.webp", 0.5, 1.02,
                "BANKA YOK. FAİZ YOK.", "KEFİL YOK.",
                "60 ay sabit taksit · %30 peşinat")
    u_split_alt("meta-v3-02-avlu", "hero-courtyard-dusk.webp", 0.5, 1.02,
                "60 AY SABİT TAKSİT", None,
                "Banka yok · Faiz yok · Kefil yok · Komisyon yok")
    u_split_alt("meta-v3-03-deniz", "ic-mekan/21-balkondan-deniz.webp", 0.5, 1.0,
                "TAKSİTİN 60 AY", "DEĞİŞMEZ.",
                "Ara ödeme yok · Balon ödeme yok")
    u_split_ust("meta-v3-04-balkon", "balcony-dusk.webp", 0.55, 1.05,
                "SÜRPRİZ ÖDEME YOK", None,
                "Ara ödeme yok · Balon yok · Komisyon yok")
    u_split_ust("meta-v3-05-teras", "terrace-pergola.webp", 0.5, 1.05,
                "KREDİSİZ", "EV SAHİPLİĞİ",
                "Banka yok · Faiz yok · 60 ay sabit taksit")
    u_cerceve("meta-v3-06-cephe", "street-corner.webp", 0.42, 1.05,
              "EVİNİZ İZMİT MİA'DA",
              "BANKA YOK · FAİZ YOK · 60 AY SABİT TAKSİT")


def kontak_v3():
    fs = sorted(f for f in os.listdir(OUT) if f.startswith("meta-v3-") and f.endswith(".jpg"))
    tw = 430
    th = int(tw * H / W)
    cols, rows = 3, 2
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * 8, rows * th + (rows + 1) * 8), (16, 20, 26))
    for i, f in enumerate(fs[:6]):
        im = Image.open(os.path.join(OUT, f)).resize((tw, th), Image.LANCZOS)
        sheet.paste(im, (8 + (i % cols) * (tw + 8), 8 + (i // cols) * (th + 8)))
    sheet.save(os.path.join(OUT, "kontak-v3.jpg"), quality=88)
    print("   kontak-v3.jpg")



# ═════════════ V4 — REFERANS GRAMERİ: YAZI GÖKYÜZÜNDE, PROJE ALTTA ═════════
# Kullanıcının verdiği 5 örneğin ortak dili: başlık fotoğrafın BOŞ göğünde
# ya da fotoğraf dışında; bina hiç kapatılmıyor. Karışık ağırlıklı başlık
# (beyaz satır + renkli vurgu satırı), yıldız rozet, ödeme tablosu, ışık
# hüzmeleri, altta logo + telefon. Fiyatlı olanlarda onaylı örnek rakamlar
# + dönemsellik dipnotu.

DONEMSEL = "Fiyatlar ve kampanya koşulları dönemsel olarak değişebilir. Güncel bilgi: satış ofisi."


def gok_uzat(kaynak, foto_h, focus=0.5, zoom=1.0, gok=(8, 34, 56)):
    """Foto altta; üstü fotoğrafın göğüyle harmanlanan lacivert gökyüzü."""
    im = Image.new("RGB", (W, H), gok)
    ust = np.linspace(0, 1, H - foto_h, dtype=np.float32)[:, None, None]
    g1 = np.array((4, 22, 40), np.float32)
    g2 = np.array(gok, np.float32)
    grad = (g1 * (1 - ust) + g2 * ust).astype(np.uint8)
    im.paste(Image.fromarray(np.repeat(grad, W, axis=1), "RGB"), (0, 0))
    ft = foto(kaynak, W, foto_h, focus, zoom)
    im.paste(ft, (0, H - foto_h))
    # dikiş: fotoğrafın üst 110 px'ine göğe doğru alfa geçişi
    bl = 110
    band = np.asarray(ft.crop((0, 0, W, bl)), np.float32)
    alfa = np.linspace(1, 0, bl, dtype=np.float32)[:, None, None]
    karisim = (np.array(gok, np.float32) * alfa + band * (1 - alfa)).astype(np.uint8)
    im.paste(Image.fromarray(karisim, "RGB"), (0, H - foto_h))
    return im.convert("RGBA")


def huzmeler(im, taban_y, n=5):
    """Projeden yükselen ışık hüzmeleri (Toprak Tan referansı)."""
    kat = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(kat)
    import random
    random.seed(7)
    for i in range(n):
        cx = 120 + i * (W - 240) / (n - 1) + random.randint(-30, 30)
        gen = random.randint(26, 44)
        kd.polygon([(cx - gen, taban_y), (cx + gen, taban_y),
                    (cx + gen * 2.2, taban_y - 640), (cx - gen * 2.2, taban_y - 640)],
                   fill=(120, 200, 230, 26))
        kd.polygon([(cx - gen * 0.4, taban_y), (cx + gen * 0.4, taban_y),
                    (cx + gen, taban_y - 640), (cx - gen, taban_y - 640)],
                   fill=(160, 220, 245, 30))
    kat = kat.filter(__import__("PIL.ImageFilter", fromlist=["GaussianBlur"]).GaussianBlur(6))
    im.alpha_composite(kat)


def yildiz_rozet(im, cx, cy, r, satirlar, dolgu=CAM, yazi=GECE, don=-12):
    """Yıldız patlaması rozet (referanslardaki kampanya damgası)."""
    import math
    kat = Image.new("RGBA", (r * 3, r * 3), (0, 0, 0, 0))
    kd = ImageDraw.Draw(kat)
    c = r * 1.5
    pts = []
    N = 24
    for i in range(N * 2):
        rr = r if i % 2 == 0 else r * 0.82
        a = math.pi * i / N
        pts.append((c + rr * math.cos(a), c + rr * math.sin(a)))
    kd.polygon(pts, fill=dolgu + (255,))
    fb = mont("Bold", int(r * (0.30 if len(satirlar) > 1 else 0.36)))
    y0 = c - (len(satirlar) - 1) * r * 0.19
    for i, t in enumerate(satirlar):
        kd.text((c, y0 + i * r * 0.38), t, font=fb, fill=yazi, anchor="mm")
    kat = kat.rotate(don, resample=Image.BICUBIC, expand=False)
    im.alpha_composite(kat, (int(cx - c), int(cy - c)))


def karma_baslik(dr, y, satirlar, aralik=1.16):
    """Karışık ağırlık/renk başlık: [(metin, boy, kalinlik, renk), ...]"""
    for t, boy, kes, renk in satirlar:
        dr.text((W / 2, y), t, font=mont(kes, boy), fill=renk, anchor="mm")
        y += boy * aralik
    return y


def alt_kimlik(im, dr, koyu=True):
    logo(im, "mia-beyaz" if koyu else "mia-renkli", 64, H - 158, 150)
    dr.text((W - 64, H - 122), TEL, font=mont("Bold", 34),
            fill=BEYAZ if koyu else GECE, anchor="rm")
    dr.text((W - 64, H - 84), "miaparkocean.com", font=mont("SemiBold", 22),
            fill=SIS if koyu else KURSUN, anchor="rm")
    dr.text((W / 2, H - 20), YASAL, font=mont("Regular", 15),
            fill=(150, 175, 190) if koyu else KURSUN, anchor="mm")


def w01():
    """Toprak Tan grameri: gece proje + hüzmeler + gök başlığı + rozet."""
    im = gok_uzat("night-gate.webp", 620, 0.5, 1.02)
    huzmeler(im, H - 560)
    dr = ImageDraw.Draw(im)
    karma_baslik(dr, 170, [
        ("KREDİYE TAKILMAYIN,", 46, "SemiBold", BEYAZ),
        ("BANKA YOK · FAİZ YOK", 62, "Bold", BEYAZ),
        ("60 AY SABİT TAKSİT!", 74, "Bold", CAM),
    ], aralik=1.28)
    yildiz_rozet(im, W - 190, 520, 118, ["KEFİL", "YOK"])
    dr = ImageDraw.Draw(im)
    alt_kimlik(im, dr)
    kaydet(im, "meta-v4-01-gece-huzme")


def w02():
    """arsaVev grameri: minimal, fiyat cümlesi gökte, proje dokunulmamış."""
    im = gok_uzat("entrance-gate.webp", 700, 0.45, 1.1, gok=(10, 44, 66))
    dr = ImageDraw.Draw(im)
    karma_baslik(dr, 168, [
        ("Aylık 29.900 TL'ye", 72, "SemiBold", BEYAZ),
        ("ev sahibi olmak var.", 72, "SemiBold", BEYAZ),
    ], aralik=1.18)
    dr.text((W / 2, 360), "1+0 dairelerde · 60 ay vade farksız · Banka yok, faiz yok",
            font=mont("Regular", 28), fill=SIS, anchor="mm")
    dr.text((W / 2, 428), "Fırsatı kaçırmayın…", font=mont("SemiBold", 26),
            fill=CAM, anchor="mm")
    logo(im, "mia-beyaz", (W - 250) // 2, 470, 250)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, H - 40), DONEMSEL + "  ·  " + YASAL,
            font=mont("Regular", 14), fill=(150, 175, 190), anchor="mm")
    dr.text((W / 2, H - 84), TEL + "   ·   miaparkocean.com",
            font=mont("Bold", 28), fill=BEYAZ, anchor="mm")
    kaydet(im, "meta-v4-02-aylik")


def w03():
    """Eminevim grameri: ödeme tablosu kahraman."""
    im = Image.new("RGBA", (W, H), KAGIT + (255,))
    alt = foto("ic-mekan/18-yuruyus-yolu.webp", W, 430, 0.5, 1.05)
    im.paste(alt, (0, H - 430))
    dr = ImageDraw.Draw(im)
    # foto-panel dikişi yumuşak
    bl = 90
    band = np.asarray(alt.crop((0, 0, W, bl)), np.float32)
    alfa = np.linspace(1, 0, bl, dtype=np.float32)[:, None, None]
    kar = (np.array(KAGIT, np.float32) * alfa + band * (1 - alfa)).astype(np.uint8)
    im.paste(Image.fromarray(kar, "RGB"), (0, H - 430))
    logo(im, "mia-renkli", (W - 240) // 2, 44, 240)
    dr = ImageDraw.Draw(im)
    karma_baslik(dr, 260, [
        ("Tasarrufa Şimdi Başlayın", 40, "SemiBold", VURGU),
        ("EVİNİZİ KOLAYCA ALIN", 66, "Bold", GECE),
    ], aralik=1.35)
    # tablo
    tx, ty, tw_, rh = 90, 420, W - 180, 92
    kols = [0.26, 0.40, 0.34]
    bas = ["DAİRE", "PEŞİNAT", "AYLIK TAKSİT"]
    dr.rounded_rectangle([tx, ty, tx + tw_, ty + rh * 3], radius=18, fill=BEYAZ,
                         outline=AYRAC, width=2)
    dr.rounded_rectangle([tx, ty, tx + tw_, ty + rh], radius=18, fill=GECE)
    dr.rectangle([tx, ty + rh * 0.5, tx + tw_, ty + rh], fill=GECE)
    x = tx
    for i, b in enumerate(bas):
        cw = tw_ * kols[i]
        dr.text((x + cw / 2, ty + rh / 2), b, font=mont("Bold", 26),
                fill=CAM if i == 2 else BEYAZ, anchor="mm")
        x += cw
    veriler = [("1+0", "699.000 TL", "29.900 TL"), ("1+1", "999.000 TL", "39.900 TL")]
    for r_i, satir in enumerate(veriler):
        y0 = ty + rh * (r_i + 1)
        if r_i == 0:
            dr.rectangle([tx + 2, y0, tx + tw_ - 2, y0 + rh], fill=(238, 246, 250))
        # aylık kolonu vurgulu
        dr.rectangle([tx + tw_ * (kols[0] + kols[1]), y0, tx + tw_ - 2, y0 + rh],
                     fill=(213, 238, 246) if r_i == 0 else (225, 243, 249))
        x = tx
        for c_i, hucre in enumerate(satir):
            cw = tw_ * kols[c_i]
            dr.text((x + cw / 2, y0 + rh / 2), hucre,
                    font=mont("Bold", 34 if c_i else 30),
                    fill=VURGU if c_i == 2 else GECE, anchor="mm")
            x += cw
        dr.line([(tx + 8, y0), (tx + tw_ - 8, y0)], fill=AYRAC, width=2)
    by = ty + rh * 3 + 34
    dr.rounded_rectangle([(W - 720) / 2, by, (W + 720) / 2, by + 66], radius=33, fill=VURGU)
    dr.text((W / 2, by + 33), "60 AY VADE FARKSIZ · BANKA YOK · FAİZ YOK",
            font=mont("Bold", 27), fill=BEYAZ, anchor="mm")
    dr.text((W / 2, by + 104), DONEMSEL, font=mont("Regular", 19), fill=KURSUN, anchor="mm")
    dr.text((W / 2, H - 34), YASAL, font=mont("Regular", 15), fill=BEYAZ, anchor="mm")
    dr.text((W / 2, H - 74), TEL + "   ·   miaparkocean.com",
            font=mont("Bold", 27), fill=BEYAZ, anchor="mm")
    kaydet(im, "meta-v4-03-odeme-tablosu")


def w04():
    """Fuzul grameri: açık gök, bulutlar, kartta proje."""
    im = Image.new("RGBA", (W, H))
    t = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    g1 = np.array((120, 190, 220), np.float32)
    g2 = np.array((225, 243, 250), np.float32)
    grad = (g1 * (1 - t) + g2 * t).astype(np.uint8)
    im.paste(Image.fromarray(np.repeat(grad, W, axis=1), "RGB"), (0, 0))
    dr = ImageDraw.Draw(im)
    # bulutlar
    for (bx, by_, r_) in [(140, 760, 90), (300, 800, 120), (860, 700, 100),
                          (1000, 760, 80), (560, 830, 130)]:
        for dx, dy, rr in [(-r_ * 0.7, 10, r_ * 0.62), (0, 0, r_), (r_ * 0.7, 12, r_ * 0.58)]:
            dr.ellipse([bx + dx - rr, by_ + dy - rr * 0.62, bx + dx + rr, by_ + dy + rr * 0.62],
                       fill=(255, 255, 255, 235))
    # üst afiş
    dr.rounded_rectangle([120, 96, W - 120, 300], radius=40, fill=GECE)
    karma_baslik(dr, 160, [
        ("Faizsiz Finansman ile", 38, "SemiBold", (140, 205, 228)),
        ("EV SAHİBİ OL!", 66, "Bold", BEYAZ),
    ], aralik=1.30)
    # çipler
    y = 360
    for t2 in ["BANKA YOK", "FAİZ YOK", "KEFİL YOK"]:
        hap(dr, W / 2, y, t2, mont("Bold", 27), BEYAZ, VURGU, pad=30)
        y += 78
    # kartta proje
    kx0, ky0, kx1, ky1 = 130, 640, W - 130, 1170
    dr.rounded_rectangle([kx0 - 10, ky0 - 10, kx1 + 10, ky1 + 10], radius=34, fill=BEYAZ)
    kf = foto("facade-warm.webp", kx1 - kx0, ky1 - ky0, 0.5, 1.0)
    maske = Image.new("L", kf.size, 0)
    ImageDraw.Draw(maske).rounded_rectangle([0, 0, kf.width, kf.height], radius=26, fill=255)
    im.paste(kf, (kx0, ky0), maske)
    dr = ImageDraw.Draw(im)
    yildiz_rozet(im, W - 185, 655, 105, ["60 AY", "SABİT"], dolgu=GECE, yazi=CAM, don=10)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 1226), TEL + "   ·   miaparkocean.com",
            font=mont("Bold", 30), fill=GECE, anchor="mm")
    dr.text((W / 2, H - 64), "MİA PARK OCEAN · İZMİT MİA BÖLGESİ",
            font=mont("Bold", 24), fill=VURGU, anchor="mm")
    dr.text((W / 2, H - 28), YASAL, font=mont("Regular", 15), fill=KURSUN, anchor="mm")
    kaydet(im, "meta-v4-04-acik-gok")


def w05():
    """Toprak Tan varyantı: alacakaranlık, farklı başlık."""
    im = gok_uzat("hero-courtyard-dusk.webp", 640, 0.5, 1.02, gok=(12, 38, 60))
    huzmeler(im, H - 580, n=4)
    dr = ImageDraw.Draw(im)
    karma_baslik(dr, 175, [
        ("DOĞRU PROJEYİ SEÇİN,", 46, "SemiBold", BEYAZ),
        ("İZMİT MİA'DA", 60, "Bold", CAM),
        ("EV SAHİBİ OLUN!", 76, "Bold", BEYAZ),
    ], aralik=1.28)
    yildiz_rozet(im, 178, 540, 118, ["BANKA", "FAİZ·KEFİL", "YOK"], don=-10)
    dr = ImageDraw.Draw(im)
    dr.text((W / 2, 640), "%30 peşinat · 60 ay sabit taksit",
            font=mont("SemiBold", 30), fill=SIS, anchor="mm")
    alt_kimlik(im, dr)
    kaydet(im, "meta-v4-05-dusk")


def w06():
    """Turyap grameri modern: taksit başlığı + yuvarlak foto + büyük telefon."""
    im = Image.new("RGBA", (W, H), KAGIT + (255,))
    dr = ImageDraw.Draw(im)
    logo(im, "mia-renkli", (W - 240) // 2, 40, 240)
    dr = ImageDraw.Draw(im)
    karma_baslik(dr, 250, [
        ("29.900 TL'den Başlayan", 52, "Bold", VURGU),
        ("Taksitlerle", 52, "Bold", VURGU),
        ("EV SAHİBİ OLMA", 72, "Bold", GECE),
        ("FIRSATI", 72, "Bold", GECE),
    ], aralik=1.16)
    dr.text((W / 2, 620), "Banka yok · Faiz yok · Kefil yok · Komisyon yok",
            font=mont("SemiBold", 28), fill=KURSUN, anchor="mm")
    ky0 = 680
    kf = foto("balcony-dusk.webp", W - 180, 430, 0.55, 1.05)
    maske = Image.new("L", kf.size, 0)
    ImageDraw.Draw(maske).rounded_rectangle([0, 0, kf.width, kf.height], radius=30, fill=255)
    im.paste(kf, (90, ky0), maske)
    dr = ImageDraw.Draw(im)
    yildiz_rozet(im, W - 175, ky0 + 30, 108, ["60 AY", "VADE", "FARKSIZ"], don=12)
    dr = ImageDraw.Draw(im)
    dr.rounded_rectangle([120, 1168, W - 120, 1252], radius=42, fill=GECE)
    dr.text((W / 2, 1210), TEL, font=mont("Bold", 46), fill=BEYAZ, anchor="mm")
    dr.text((W / 2, 1290), DONEMSEL, font=mont("Regular", 18), fill=KURSUN, anchor="mm")
    dr.text((W / 2, H - 26), YASAL, font=mont("Regular", 15), fill=KURSUN, anchor="mm")
    kaydet(im, "meta-v4-06-kampanya")


def kontak_v4():
    fs = sorted(f for f in os.listdir(OUT) if f.startswith("meta-v4-") and f.endswith(".jpg"))
    tw = 430
    th = int(tw * H / W)
    cols, rows = 3, 2
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * 8, rows * th + (rows + 1) * 8), (16, 20, 26))
    for i, f in enumerate(fs[:6]):
        im2 = Image.open(os.path.join(OUT, f)).resize((tw, th), Image.LANCZOS)
        sheet.paste(im2, (8 + (i % cols) * (tw + 8), 8 + (i // cols) * (th + 8)))
    sheet.save(os.path.join(OUT, "kontak-v4.jpg"), quality=88)
    print("   kontak-v4.jpg")


if __name__ == "__main__":
    for g in [g01, g02, g03, g04, g05, g06, g07, g08, g09, g10]:
        g()
    kontak()
    for v in [v01, v02, v03, v04, v05, v06, v07, v08]:
        v()
    kontak_v2()
    v3_hepsi()
    kontak_v3()
    for w in [w01, w02, w03, w04, w05, w06]:
        w()
    kontak_v4()
    print("tamam ->", OUT)
