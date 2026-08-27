#!/usr/bin/env python3
"""
MİA PARK OCEAN — 15 bağımsız gönderi, INSTAGRAM KİMLİĞİNDE (tek kare).

social-media/instagram ızgara setinin dili birebir: Fraunces serif
başlıklar, Manrope harf aralıklı KÜÇÜK ETİKETLER, koyu okyanus
gradyanları, yalnızca yazının oturduğu yerde perdelenen tam kanama
render'lar, sol üstte beyaz MİA kilidi, sağ altta OCEAN imzası,
camgöbeği ince ayraç çizgileri, yumuşak metin gölgeleri.

Farkı: ızgara/karusel değil — her kare 1080x1350, TEK BAŞINA paylaşılır.

Kurallar: onaylı örnek fiyatlar (1+0: 699.000/29.900 · 1+1:
999.000/39.900), "peşinatsız"/"%30" yok, yalnız projenin render'ları.

    python3 scripts/build-post-serisi-ig.py
"""

import importlib.util
import os
import sys

from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_spec = importlib.util.spec_from_file_location(
    "ig", os.path.join(ROOT, "scripts", "build-instagram-grid.py"))
ig = importlib.util.module_from_spec(_spec)
sys.modules["ig"] = ig
_spec.loader.exec_module(ig)

W, H = 1080, 1350
SAFE = 74
OUT = os.path.join(ROOT, "sosyal-medya", "turkuaz-kampanya", "postlar")
os.makedirs(OUT, exist_ok=True)

NAVY, WHITE = ig.NAVY, ig.WHITE
AQUA, PALE, ICE, LIGHT = ig.MIA_AQUA, ig.MIA_PALE, ig.MIA_ICE, ig.MIA_LIGHT
DEEP = ig.DEEP_STOPS
serif, sans, sans_sb, sans_b = ig.serif, ig.sans, ig.sans_sb, ig.sans_b
track = ig.track

TEL = "0540 028 00 41"
SITE = "MIAPARKOCEAN.COM"


def zemin():
    return ig.gradient((W, H), DEEP, angle=0.55)


def foto(ad, focus=0.5, ust=110, alt=210, alt_bas=0.46):
    p = ig.cover(ad, (W, H), focus)
    p.alpha_composite(ig.scrim((W, H), [
        (0.0, (*NAVY, ust)), (0.22, (*NAVY, 0)), (alt_bas, (*NAVY, 0)),
        (max(alt_bas + 0.16, 0.66), (*NAVY, int(alt * 0.45))),
        (1.0, (*NAVY, alt)),
    ]))
    return p


def marka(p):
    lg = ig.lockup(240, True)
    ig.paste_soft(p, lg, (SAFE, 58))
    pm = ig.partner(150, True)
    pm.putalpha(pm.split()[3].point(lambda v: int(v * 0.9)))
    ig.paste_soft(p, pm, (W - SAFE - pm.width, H - 56 - pm.height), blur=16,
                  boost=1.4)


def golge(p, fn):
    ig.soft_shadow(p, fn)
    fn(ImageDraw.Draw(p))


def fit_serif(dr, t, start, maxw=W - 2 * SAFE, w="500"):
    s = start
    while s > 40 and dr.textlength(t, font=serif(s, w)) > maxw:
        s -= 4
    return serif(s, w)


def caps(dr, y, t, boy=34, sp=12, renk=(*ICE, 246), maxw=W - 2 * SAFE):
    f = sans_sb(boy)
    while boy > 16 and (sum(dr.textlength(c, font=f) for c in t)
                        + sp * (len(t) - 1)) > maxw:
        boy -= 1
        f = sans_sb(boy)
    track(dr, (W / 2, y), t, f, renk, sp, "ma")


def cizgi(dr, y, yarim=90):
    dr.line([W / 2 - yarim, y, W / 2 + yarim, y], fill=(*AQUA, 210), width=4)


def tel(dr, y=None):
    """Sol altta — sağ alttaki OCEAN imzasıyla çakışmaz."""
    track(dr, (SAFE, (H - 118) if y is None else y),
          TEL + "  ·  " + SITE, sans_sb(26), (*LIGHT, 255), 7, "la")


def kaydet(p, ad):
    p.convert("RGB").save(os.path.join(OUT, ad + ".jpg"), quality=92,
                          optimize=True)
    print("   " + ad)


# ═══════════════════════════════════════════════ 15 GÖNDERİ
def p01():
    p = foto("entrance-gate.webp", 0.5, alt=225, alt_bas=0.40)
    def c(dr):
        dr.text((W / 2, 800), "Kocaeli", font=serif(150, "600"),
                fill=WHITE, anchor="ms")
        dr.text((W / 2, 930), "ev sahibi oluyor.", font=fit_serif(
            dr, "ev sahibi oluyor.", 96, w="500"), fill=WHITE, anchor="ms")
        caps(dr, 986, "BANKA YOK · FAİZ YOK · KREDİ YOK · ARA ÖDEME YOK")
        cizgi(dr, 1074)
        caps(dr, 1108, "60 AY SABİT TAKSİT", 40, 16, (*WHITE, 255))
    golge(p, c)
    tel(ImageDraw.Draw(p))
    marka(p)
    kaydet(p, "post-01-kocaeli")


def p02():
    p = zemin()
    def c(dr):
        dr.text((W / 2, 620), "60", font=serif(400, "600"), fill=WHITE,
                anchor="ms")
        caps(dr, 668, "AY SABİT TAKSİT", 52, 22, (*WHITE, 255))
        cizgi(dr, 790)
        caps(dr, 830, "BANKASIZ · FAİZSİZ · KREDİSİZ KONUT EDİNME MODELİ",
             30, 10)
        dr.text((W / 2, 1010), "Taksitiniz ilk gün ne ise,",
                font=serif(52), fill=(*PALE, 244), anchor="ms")
        dr.text((W / 2, 1076), "60. ay da o.", font=serif(52),
                fill=(*PALE, 244), anchor="ms")
    golge(p, c)
    tel(ImageDraw.Draw(p))
    marka(p)
    kaydet(p, "post-02-60ay")


def _fiyat(ad, foto_ad, focus, tip, pesin, taksit, satir):
    p = foto(foto_ad, focus, alt=230, alt_bas=0.36)
    def c(dr):
        dr.text((W / 2, 730), tip, font=serif(140, "600"), fill=WHITE,
                anchor="ms")
        caps(dr, 776, satir, 34, 13)
        cizgi(dr, 856)
        dr.text((W / 2, 966), pesin + " TL", font=serif(92, "600"),
                fill=WHITE, anchor="ms")
        caps(dr, 1000, "PEŞİNAT", 30, 14)
        dr.text((W / 2, 1116), taksit + " TL", font=serif(70, "600"),
                fill=(*ICE, 252), anchor="ms")
        caps(dr, 1150, "AYLIK SABİT TAKSİT", 28, 12)
    golge(p, c)
    marka(p)
    kaydet(p, ad)


def p03():
    _fiyat("post-03-studyo", "terrace-pergola.webp", 0.5, "1+0",
           "699.000", "29.900", "STÜDYO · AVANTAJLI YATIRIM")


def p04():
    _fiyat("post-04-birarti1", "facade-warm.webp", 0.5, "1+1",
           "999.000", "39.900", "AİLENİZE FERAH BİR BAŞLANGIÇ")


def p05():
    p = zemin()
    def c(dr):
        dr.text((W / 2, 640), "%0", font=serif(380, "600"), fill=WHITE,
                anchor="ms")
        caps(dr, 700, "FAİZ · VADE FARKI · KOMİSYON", 40, 16, (*WHITE, 255))
        cizgi(dr, 810)
        caps(dr, 850, "TASARRUFA DAYALI KONUT FİNANSMANI", 30, 12)
        dr.text((W / 2, 1030), "60 ay sabit taksit, banka yok.",
                font=serif(54), fill=(*PALE, 244), anchor="ms")
    golge(p, c)
    tel(ImageDraw.Draw(p))
    marka(p)
    kaydet(p, "post-05-sifir-faiz")


def p06():
    p = foto("ic-mekan/21-balkondan-deniz.webp", 0.5, ust=130, alt=235,
             alt_bas=0.34)
    def c(dr):
        dr.text((W / 2, 680), "İzmit MİA Bölgesi", font=fit_serif(
            dr, "İzmit MİA Bölgesi", 104, w="600"), fill=WHITE, anchor="ms")
        caps(dr, 728, "ŞEHRİN YENİ DEĞER MERKEZİ", 32, 13)
        veriler = [("2 dk", "İZMİT SAHİLİ"), ("35 dk", "SAKARYA"),
                   ("1,5 saat", "İSTANBUL ANADOLU YAKASI")]
        y = 900
        for a, b in veriler:
            dr.text((W / 2, y), a, font=serif(62, "600"), fill=WHITE,
                    anchor="ms")
            caps(dr, y + 24, b, 26, 10)
            y += 152
    golge(p, c)
    marka(p)
    kaydet(p, "post-06-konum")


def p07():
    p = foto("street-corner.webp", 0.42, alt=225, alt_bas=0.42)
    def c(dr):
        dr.text((W / 2, 840), "Ev sahibi", font=serif(120, "600"),
                fill=WHITE, anchor="ms")
        dr.text((W / 2, 964), "olma zamanı.", font=serif(120, "600"),
                fill=WHITE, anchor="ms")
        cizgi(dr, 1044)
        caps(dr, 1082, "BANKA YOK · FAİZ YOK · KREDİ YOK · ARA ÖDEME YOK")
    golge(p, c)
    tel(ImageDraw.Draw(p))
    marka(p)
    kaydet(p, "post-07-olma-zamani")


def p08():
    p = zemin()
    def c(dr):
        caps(dr, 500, "TASARRUFA DAYALI FİNANSMAN", 34, 14)
        dr.text((W / 2, 640), "Banka yok.", font=serif(110, "600"),
                fill=WHITE, anchor="ms")
        dr.text((W / 2, 764), "Faiz yok.", font=serif(110, "600"),
                fill=WHITE, anchor="ms")
        cizgi(dr, 850)
        dr.text((W / 2, 950), "Kredi başvurusu ve masraf olmadan,",
                font=serif(48), fill=(*PALE, 244), anchor="ms")
        dr.text((W / 2, 1012), "60 ay sabit taksitle ödersiniz.",
                font=serif(48), fill=(*PALE, 244), anchor="ms")
    golge(p, c)
    tel(ImageDraw.Draw(p))
    marka(p)
    kaydet(p, "post-08-tasarruf")


def p09():
    p = foto("hero-courtyard-dusk.webp", 0.5, alt=230, alt_bas=0.42)
    def c(dr):
        dr.text((W / 2, 880), "Satış ofisimize", font=serif(104, "600"),
                fill=WHITE, anchor="ms")
        dr.text((W / 2, 990), "bekleriz.", font=serif(104, "600"),
                fill=WHITE, anchor="ms")
        cizgi(dr, 1064)
        caps(dr, 1100, "SİZE ÖZEL ÖDEME PLANINI BİRLİKTE ÇIKARALIM", 28, 10)
    golge(p, c)
    tel(ImageDraw.Draw(p))
    marka(p)
    kaydet(p, "post-09-satis-ofisi")


def p10():
    p = foto("courtyard-pools.webp", 0.5, alt=235, alt_bas=0.40)
    def c(dr):
        dr.text((W / 2, 860), "Site içinde yaşam", font=fit_serif(
            dr, "Site içinde yaşam", 100, w="600"), fill=WHITE, anchor="ms")
        cizgi(dr, 934)
        caps(dr, 976, "YEŞİL AVLULAR · SU AKSLARI · YÜRÜYÜŞ YOLLARI", 29, 11)
        caps(dr, 1030, "ÇOCUK OYUN ALANLARI", 29, 11)
    golge(p, c)
    tel(ImageDraw.Draw(p))
    marka(p)
    kaydet(p, "post-10-yasam")


def p11():
    p = zemin()
    def c(dr):
        dr.text((W / 2, 660), "Yok.", font=serif(300, "600"), fill=WHITE,
                anchor="ms")
        cizgi(dr, 760)
        caps(dr, 806, "ARA ÖDEME · BALON ÖDEME · KEFİL", 36, 15,
             (*WHITE, 255))
        dr.text((W / 2, 990), "Bütçenizi zorlamayan tek plan:",
                font=serif(50), fill=(*PALE, 244), anchor="ms")
        dr.text((W / 2, 1054), "60 ay sabit taksit.", font=serif(50),
                fill=(*PALE, 244), anchor="ms")
    golge(p, c)
    tel(ImageDraw.Draw(p))
    marka(p)
    kaydet(p, "post-11-ara-odeme")


def p12():
    p = foto("balcony-dusk.webp", 0.55, alt=225, alt_bas=0.40)
    def c(dr):
        dr.text((W / 2, 860), "Hayalinizdeki eve", font=fit_serif(
            dr, "Hayalinizdeki eve", 96, w="600"), fill=WHITE, anchor="ms")
        dr.text((W / 2, 966), "kavuşun.", font=serif(96, "600"), fill=WHITE,
                anchor="ms")
        cizgi(dr, 1042)
        caps(dr, 1080, "60 AY SABİT TAKSİT · FAİZSİZ", 32, 13)
    golge(p, c)
    tel(ImageDraw.Draw(p))
    marka(p)
    kaydet(p, "post-12-hayal")


def p13():
    p = zemin()
    def c(dr):
        caps(dr, 470, "RAKAMLARLA MİA PARK OCEAN", 34, 14)
        veriler = [("60", "AY SABİT TAKSİT"), ("%0", "FAİZ · VADE FARKI"),
                   ("1+0 · 1+1", "DAİRE TİPLERİ")]
        y = 640
        for a, b in veriler:
            dr.text((W / 2, y), a, font=serif(120, "600"), fill=WHITE,
                    anchor="ms")
            caps(dr, y + 44, b, 30, 12)
            y += 218
    golge(p, c)
    tel(ImageDraw.Draw(p))
    marka(p)
    kaydet(p, "post-13-rakamlar")


def p14():
    p = foto("night-gate.webp", 0.5, ust=140, alt=225, alt_bas=0.44)
    def c(dr):
        dr.text((W / 2, 880), "Akşam ışıkları", font=serif(104, "600"),
                fill=WHITE, anchor="ms")
        dr.text((W / 2, 990), "evinizden yansısın.", font=fit_serif(
            dr, "evinizden yansısın.", 88, w="600"), fill=WHITE, anchor="ms")
        cizgi(dr, 1064)
        caps(dr, 1100, "İZMİT MİA BÖLGESİ'NDE YENİ YAŞAM", 30, 12)
    golge(p, c)
    marka(p)
    kaydet(p, "post-14-aksam")


def p15():
    p = zemin()
    lg = ig.lockup(560, True)
    ig.paste_soft(p, lg, ((W - lg.width) // 2, 300))
    def c(dr):
        cizgi(dr, 820)
        dr.text((W / 2, 930), "İzmit MİA Bölgesi'nde", font=serif(64),
                fill=(*PALE, 248), anchor="ms")
        dr.text((W / 2, 1010), "yeni yaşam.", font=serif(64),
                fill=(*PALE, 248), anchor="ms")
    golge(p, c)
    tel(ImageDraw.Draw(p))
    pm = ig.partner(150, True)
    pm.putalpha(pm.split()[3].point(lambda v: int(v * 0.9)))
    ig.paste_soft(p, pm, (W - SAFE - pm.width, H - 56 - pm.height), blur=16,
                  boost=1.4)
    kaydet(p, "post-15-marka")


def p16():
    """Kocaeli Emniyet personeline %5 peşinat indirimi — kampanya kartı."""
    p = zemin()
    def c(dr):
        caps(dr, 400, "KOCAELİ EMNİYET PERSONELİNE ÖZEL", 34, 13,
             (*WHITE, 252))
        dr.text((W / 2, 540), "Peşinatta %5 indirim.", font=fit_serif(
            dr, "Peşinatta %5 indirim.", 96, w="600"), fill=WHITE,
            anchor="ms")
        cizgi(dr, 610)
        veriler = [("1+0", "664.000 TL", "29.900 TL x 60 AY SABİT TAKSİT"),
                   ("1+1", "950.000 TL", "39.900 TL x 60 AY SABİT TAKSİT"),
                   ("2+1", "1.900.000 TL", "49.900 TL x 60 AY SABİT TAKSİT")]
        y = 748
        for tip, pesin, taksit in veriler:
            caps(dr, y - 64, tip + " · PEŞİNAT", 26, 11)
            dr.text((W / 2, y), pesin, font=serif(64, "600"), fill=WHITE,
                    anchor="ms")
            caps(dr, y + 30, taksit, 25, 9)
            y += 186
    golge(p, c)
    dr = ImageDraw.Draw(p)
    track(dr, (SAFE, 1196), TEL + "  ·  " + SITE, sans_sb(26),
          (*LIGHT, 255), 7, "la")
    ik, kal = 34, 3
    x, cy = SAFE, 1254
    dr.rounded_rectangle([x, cy - ik / 2, x + ik, cy + ik / 2], radius=9,
                         outline=WHITE, width=kal)
    dr.ellipse([x + ik * 0.26, cy - ik * 0.24, x + ik * 0.74, cy + ik * 0.24],
               outline=WHITE, width=kal)
    dr.ellipse([x + ik * 0.70, cy - ik * 0.42, x + ik * 0.88, cy - ik * 0.24],
               fill=WHITE)
    x += ik + 14
    dr.rounded_rectangle([x, cy - ik / 2, x + ik, cy + ik / 2], radius=9,
                         outline=WHITE, width=kal)
    dr.text((x + ik * 0.55, cy + 1), "f", font=sans_b(26), fill=WHITE,
            anchor="mm")
    x += ik + 16
    track(dr, (x, cy + 10), "MIAPARKOCEAN", sans_sb(24), (*LIGHT, 255), 7,
          "la")
    marka(p)
    kaydet(p, "post-16-emniyet-kampanya")


def kontak():
    fs = sorted(f for f in os.listdir(OUT)
                if f.startswith("post-") and f.endswith(".jpg"))
    tw = 380
    th = int(tw * H / W)
    ara = 10
    cols = 5
    rows = (len(fs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * ara,
                              rows * th + (rows + 1) * ara), (16, 20, 26))
    for i, f in enumerate(fs):
        im = Image.open(os.path.join(OUT, f)).resize((tw, th), Image.LANCZOS)
        sheet.paste(im, (ara + (i % cols) * (tw + ara),
                         ara + (i // cols) * (th + ara)))
    sheet.save(os.path.join(OUT, "kontak-postlar.jpg"), quality=88)
    print("   kontak-postlar.jpg")


if __name__ == "__main__":
    for p in [p01, p02, p03, p04, p05, p06, p07, p08, p09, p10,
              p11, p12, p13, p14, p15]:
        p()
    kontak()
    print("tamam ->", OUT)
