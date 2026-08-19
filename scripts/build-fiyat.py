#!/usr/bin/env python3
"""
MİA PARK OCEAN — fiyat roll-up'ı (PIL sürümü).

ARTIK BİRİNCİL DEĞİL. Onaylanan fiyat roll-up'ı Higgsfield ile üretiliyor:
tabela/fiyat-rollup/ altında, istemleri PROMPT.md'de, bitirme betiği
scripts/finish-fiyat-rollup.py. Bu betik tümüyle depo içinde kaldığı için
duruyor — rakam ya da metin değişince yapay zekâ kuyruğuna girmeden pano
üretmek gerekirse hâlâ çalışıyor.

DÖRT DOSYA: gündüz/gece x rakamlı/rakamsız.

    fiyat-gunduz.jpg           gündüz render, Montserrat, logo mavisi
    fiyat-gunduz-fiyatsiz.jpg
    fiyat-gece.jpg             gece render, Playfair, şampanya vurgu
    fiyat-gece-fiyatsiz.jpg

Gündüz ve gece yalnızca fotoğrafla değil RENK VE YAZI TİPİYLE de ayrışır;
aynı panonun iki hali gibi değil, iki ayrı pano gibi dursun diye.

KART RENGİ markanın kendi mavisi (#095678 → #2C94B4), gece laciverti
değil: kartlar neredeyse siyaha kaçınca logo ile pano konuşmuyordu.

Yapı referans afişten: kartlar solda, dört özellik hapı sağda dikey
sütun, altta render, mühür ve konum hapı binanın üstünde, en altta
faizsiz finansman şeridi.

Ölçü: 800 x 2000 mm, 1:1 ölçekte 100 dpi.

    python scripts/build-fiyat.py
"""

from __future__ import annotations

import importlib.util
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_spec = importlib.util.spec_from_file_location(
    "ru", os.path.join(ROOT, "scripts", "build-rollup.py"))
ru = importlib.util.module_from_spec(_spec)
sys.modules["ru"] = ru
_spec.loader.exec_module(ru)

bs = ru.bs
gradient, cover, scrim, overlay = ru.gradient, ru.cover, ru.scrim, ru.overlay
track, fit, fit_track = ru.track, ru.fit, ru.fit_track
qr_image, lockup = ru.qr_image, ru.lockup
cap_h, cap_top, soft_shadow = ru.cap_h, ru.cap_top, ru.soft_shadow
PRICES, SIZES = ru.PRICES, ru.SIZES
SITE, PHONES = ru.SITE, ru.PHONES
SELLER, SELLER_ROLE = ru.SELLER, ru.SELLER_ROLE

OUT = os.path.join(ROOT, "tabela", "fiyat")
PREVIEW = os.path.join(OUT, "onizleme")
W_MM, H_MM, DPI = 800, 2000, 100
M = 58
QR_URL = "https://miaparkocean.com/?utm_source=fiyat"

WHITE = (255, 255, 255)
# Marka mavileri — kartlar bunlardan kuruluyor.
DEEP = bs.MIA_DEEP          # 09 56 78
DARK = bs.MIA_DARK          # 1A 74 96
OCEAN = bs.MIA_OCEAN        # 2C 94 B4
LIGHT = bs.MIA_LIGHT
PALE = bs.MIA_PALE
ICE = bs.MIA_ICE
NIGHT = (5, 18, 30)
SAND = (223, 199, 154)
SAND_HI = (240, 224, 190)
SAND_DIM = (176, 150, 106)
INK = (18, 32, 44)
GREY = (118, 130, 142)


class Theme:
    def __init__(self, key, render, focus, light, ground, card, card_edge,
                 badge_fill, badge_ink, accent, head_a, head_b, ink, sub,
                 label, pill_icon, bar, foot_ink, head_font, body_font,
                 card_angle=0.30, card_alpha=196, name=""):
        self.__dict__.update(locals())
        del self.__dict__["self"]


COPPER = (196, 142, 96)
COPPER_HI = (226, 184, 146)
SLATE = (38, 50, 60)
CHAR = (26, 30, 36)


def _T(**kw):
    base = dict(ink=INK, sub=GREY, pill_icon=DEEP, foot_ink=INK,
                body_font="mont", card_angle=0.30)
    base.update(kw)
    return Theme(**base)


# --- GÜNDÜZ: üç renk düzeni --------------------------------------------
G1 = _T(key="gunduz-okyanus", name="gündüz · okyanus", render="entrance-gate",
        focus=0.46, light=True,
        ground=[(0.0, WHITE), (0.34, (243, 250, 252)), (1.0, PALE)],
        card=[(0.0, DEEP), (0.55, DARK), (1.0, OCEAN)], card_edge=(255, 255, 255, 120),
        badge_fill=WHITE, badge_ink=DEEP, accent=OCEAN,
        head_a=DEEP, head_b=OCEAN, label=ICE, bar=DEEP, head_font="mont")

G2 = _T(key="gunduz-buz", name="gündüz · buz", render="entrance-gate",
        focus=0.46, light=True,
        ground=[(0.0, WHITE), (0.40, (238, 248, 251)), (1.0, (205, 232, 240))],
        card=[(0.0, DARK), (0.5, OCEAN), (1.0, bs.MIA_CYAN)],
        card_edge=(255, 255, 255, 150),
        badge_fill=DEEP, badge_ink=WHITE, accent=DEEP,
        head_a=INK, head_b=DEEP, label=(232, 248, 252), bar=DARK,
        head_font="mont", card_angle=0.62)

# Cephe yakın planı duvar gibi okunuyordu; gündüzün üçü de dış görünüm.
G3 = _T(key="gunduz-antrasit", name="gündüz · antrasit", render="entrance-gate",
        focus=0.46, light=True,
        ground=[(0.0, (252, 251, 248)), (0.45, (245, 243, 238)), (1.0, (226, 224, 218))],
        card=[(0.0, CHAR), (0.6, SLATE), (1.0, (54, 68, 78))],
        card_edge=(255, 255, 255, 110),
        badge_fill=COPPER, badge_ink=CHAR, accent=COPPER,
        head_a=CHAR, head_b=COPPER, label=(226, 220, 210), bar=CHAR,
        pill_icon=CHAR, head_font="marcellus", body_font="cormorant")

# --- GECE: üç renk düzeni ----------------------------------------------
N1 = _T(key="gece-sampanya", name="gece · şampanya", render="night-gate",
        focus=0.5, light=False,
        ground=[(0.0, NIGHT), (0.30, (8, 30, 46)), (0.62, (10, 42, 62)), (1.0, NIGHT)],
        card=[(0.0, (7, 44, 62)), (0.6, DEEP), (1.0, (10, 66, 90))],
        card_edge=(*SAND_DIM, 190),
        badge_fill=SAND, badge_ink=NIGHT, accent=SAND,
        head_a=WHITE, head_b=SAND, ink=WHITE, sub=ICE, label=PALE, bar=DEEP,
        foot_ink=WHITE, head_font="playfair", body_font="cormorant")

N2 = _T(key="gece-okyanus", name="gece · okyanus", render="aerial-pools",
        focus=0.5, light=False,
        ground=[(0.0, (3, 20, 32)), (0.34, (6, 40, 60)), (0.66, (8, 52, 76)),
                (1.0, (3, 18, 30))],
        card=[(0.0, (6, 52, 74)), (0.55, DARK), (1.0, (44, 148, 180))],
        card_edge=(*LIGHT, 170),
        badge_fill=LIGHT, badge_ink=(4, 34, 50), accent=LIGHT,
        head_a=WHITE, head_b=LIGHT, ink=WHITE, sub=ICE, label=(224, 246, 252),
        bar=(6, 46, 68), foot_ink=WHITE, head_font="oswald", card_angle=0.55)

N3 = _T(key="gece-bakir", name="gece · bakır", render="night-gate",
        focus=0.5, light=False,
        ground=[(0.0, (12, 12, 14)), (0.34, (24, 26, 30)), (0.68, (32, 34, 40)),
                (1.0, (10, 10, 12))],
        card=[(0.0, (24, 26, 32)), (0.6, (40, 44, 52)), (1.0, (56, 62, 72))],
        card_edge=(*COPPER, 190),
        badge_fill=COPPER, badge_ink=(16, 16, 18), accent=COPPER,
        head_a=WHITE, head_b=COPPER_HI, ink=WHITE, sub=(196, 190, 182),
        label=(226, 214, 202), pill_icon=CHAR, bar=(26, 28, 34), foot_ink=WHITE,
        head_font="cormorant", body_font="cormorant")


def board() -> ru.B:
    ru.W_MM, ru.H_MM, ru.M = W_MM, H_MM, M
    return ru.B(W_MM, H_MM, DPI)


def hfont(b, th, size, w=800):
    return {"mont": lambda: b.mont(size, w),
            "playfair": lambda: b.playfair(size, w),
            "oswald": lambda: b.f("Oswald-var.ttf", size, 700),
            "marcellus": lambda: b.marcellus(size),
            "cormorant": lambda: b.cormorant(size, 700)}[th.head_font]()


# ------------------------------------------------------------------ ikonlar
def picto(d, kind, cx, cy, r, col):
    """Dolu ikonlar. Önceki sürümde ince çizgiyle çizilmişlerdi ve
    40 mm'lik karede dağılıyorlardı; dolu biçim küçükte de duruyor."""
    if kind == "onay":
        d.polygon([(cx - r * .62, cy - r * .04), (cx - r * .30, cy - r * .36),
                   (cx - r * .10, cy + r * .10), (cx + r * .46, cy - r * .62),
                   (cx + r * .70, cy - r * .28), (cx - r * .08, cy + r * .60)],
                  fill=col)
    elif kind == "grafik":
        for i, hh in enumerate((0.34, 0.62, 0.94)):
            x = cx - r * .52 + i * r * .52
            d.rounded_rectangle([x - r * .16, cy + r * .58 - r * hh,
                                 x + r * .16, cy + r * .58],
                                radius=r * .08, fill=col)
        d.polygon([(cx + r * .30, cy - r * .58), (cx + r * .78, cy - r * .58),
                   (cx + r * .78, cy - r * .12)], fill=col)
    elif kind == "pin":
        d.ellipse([cx - r * .58, cy - r * .82, cx + r * .58, cy + r * .34], fill=col)
        d.polygon([(cx - r * .30, cy + r * .10), (cx + r * .30, cy + r * .10),
                   (cx, cy + r * .84)], fill=col)
    elif kind == "takvim":
        d.rounded_rectangle([cx - r * .74, cy - r * .52, cx + r * .74, cy + r * .78],
                            radius=r * .16, fill=col)
        for s_ in (-.40, .40):
            d.rounded_rectangle([cx + r * s_ - r * .09, cy - r * .84,
                                 cx + r * s_ + r * .09, cy - r * .38],
                                radius=r * .09, fill=col)
    elif kind == "banka":
        d.polygon([(cx, cy - r * .80), (cx + r * .86, cy - r * .30),
                   (cx - r * .86, cy - r * .30)], fill=col)
        for i in range(3):
            x = cx - r * .46 + i * r * .46
            d.rounded_rectangle([x - r * .11, cy - r * .16, x + r * .11, cy + r * .46],
                                radius=r * .05, fill=col)
        d.rounded_rectangle([cx - r * .82, cy + r * .52, cx + r * .82, cy + r * .74],
                            radius=r * .08, fill=col)
    elif kind == "yuzde":
        w = max(2, int(r * .18))
        d.ellipse([cx - r * .58, cy - r * .76, cx - r * .06, cy - r * .24],
                  outline=col, width=w)
        d.ellipse([cx + r * .06, cy + r * .24, cx + r * .58, cy + r * .76],
                  outline=col, width=w)
        d.line([cx - r * .52, cy + r * .62, cx + r * .52, cy - r * .62],
               fill=col, width=w)
    elif kind == "bina":
        d.rounded_rectangle([cx - r * .70, cy - r * .52, cx - r * .06, cy + r * .78],
                            radius=r * .08, fill=col)
        d.rounded_rectangle([cx + r * .04, cy - r * .84, cx + r * .70, cy + r * .78],
                            radius=r * .08, fill=col)
    elif kind == "kisi":
        for s_ in (-1, 1):
            d.ellipse([cx + s_ * r * .40 - r * .24, cy - r * .70,
                       cx + s_ * r * .40 + r * .24, cy - r * .22], fill=col)
            d.pieslice([cx + s_ * r * .40 - r * .44, cy - r * .18,
                        cx + s_ * r * .40 + r * .44, cy + r * .78], 180, 360, fill=col)


# ------------------------------------------------------------------ parçalar
def ground(b, th) -> None:
    """Zemin + render. Bant kartların ARKASINDAN geçiyor ki buzlu cam
    kartların içinden bina görünsün.

    Doğal en-boyda bant 450 mm kalıyor ve kartların altında bitiyordu.
    640 mm'de kare yanlardan %30 kırpılıyor — ikiz blok kompozisyonu
    büyük ölçüde duruyor. 700 mm denendi, kırpma %36'ya çıkıp kadraj
    tek kuleye iniyordu.
    """
    b.im = gradient((b.W, b.H), th.ground, angle=0.22)
    bh = 640
    top = 620
    im = cover(th.render, (b.W, b.p(bh)), th.focus)
    a = np.asarray(im.split()[3], np.float32)
    fp = b.p(90)
    ramp = np.ones(b.p(bh), np.float32)
    ramp[:fp] = np.linspace(0, 1, fp) ** 1.3
    if th.light:
        # AÇIK temada render'ın altına uzatma yapılmıyor: yol ve çimin
        # rengi açık zemine doğru esnetilince çamurlu kahve bir bant
        # bırakıyor, künye de onun üstünde kayboluyordu. Bunun yerine
        # karenin alt kenarı doğrudan zemine eritiliyor.
        fb = b.p(170)
        ramp[b.p(bh) - fb:] *= np.linspace(1, 0, fb) ** 1.25
    im.putalpha(Image.fromarray((a * ramp[:, None]).astype(np.uint8), "L"))
    b.im.alpha_composite(im, (0, b.p(top)))

    if not th.light:
        src = np.asarray(im.convert("RGB"), np.float32)
        c_b = tuple(src[-round(b.p(bh) * 0.06):].mean(axis=(0, 1)))
        bot = b.H - b.p(top) - b.p(bh)
        if bot > 0:
            lay = gradient((b.W, bot), [(0.0, c_b),
                                        (0.5, tuple(c * 0.7 for c in c_b)),
                                        (1.0, NIGHT)], angle=0.0)
            tex = im.crop((0, b.p(bh) - round(b.p(bh) * .10), b.W, b.p(bh)))
            tex = tex.resize((b.W, bot), Image.LANCZOS).filter(
                ImageFilter.GaussianBlur(max(6, bot // 8)))
            tex.putalpha(96)
            lay.alpha_composite(tex)
            b.im.alpha_composite(lay, (0, b.p(top) + b.p(bh)))


def eyebrow(b, th, y, text) -> None:
    dr = b.draw
    f, sp = fit_track(b, dr, [text], b.p(640), 18, 0.24, lambda s: b.cond(s))
    w = sum(dr.textlength(c, font=f) for c in text) + sp * (len(text) - 1)

    def paint(d):
        cx = b.p(W_MM / 2)
        track(b, d, (cx, cap_top(f, b.p(y))), text, f, (*th.accent, 252), sp, "ma")
        for s_ in (-1, 1):
            d.line([cx + s_ * (w / 2 + b.p(20)), b.p(y),
                    cx + s_ * (w / 2 + b.p(70)), b.p(y)],
                   fill=(*th.accent, 200), width=max(2, b.p(1.0)))
    overlay(b, paint)


def headline(b, th, y, a, c) -> None:
    dr = b.draw
    f = fit(b, dr, [f"{a} {c}"], b.p(W_MM - M * 2), 96, lambda s: hfont(b, th, s))
    wa = dr.textlength(a + " ", font=f)
    tot = dr.textlength(f"{a} {c}", font=f)
    x0 = b.p(W_MM / 2) - tot / 2

    def paint(d):
        d.text((x0, b.p(y)), a, font=f, fill=th.head_a, anchor="ls")
        d.text((x0 + wa, b.p(y)), c, font=f, fill=th.head_b, anchor="ls")
    soft_shadow(b, paint, blur=6, alpha=100 if th.light else 130, dy=4)


def script_line(b, th, y, text) -> None:
    dr = b.draw
    f = fit(b, dr, [text], b.p(640), 49, lambda s: b.script(s, 700))
    w = dr.textlength(text, font=f)

    def paint(d):
        d.text((b.p(W_MM / 2), b.p(y)), text, font=f, fill=(*th.accent, 252),
               anchor="ms")
        d.arc([b.p(W_MM / 2) - w / 2, b.p(y) + b.p(3), b.p(W_MM / 2) + w / 2,
               b.p(y) + b.p(28)], 0, 180, fill=(*th.accent, 220), width=max(2, b.p(1.2)))
    overlay(b, paint)


def cards(b, th, y, h, rows, priced, x0=M, span=488) -> None:
    """Kart gövdesi markanın kendi mavisinden gradyan. Neredeyse siyah
    lacivert kart logo ile konuşmuyordu."""
    l1 = "PEŞİNAT" if priced else "DAİRE BÜYÜKLÜĞÜ"
    l2 = "AYLIK SADECE" if priced else "ÖDEME PLANI"
    l3 = "VADE FARKSIZ 60 AY" if priced else "VADE FARKSIZ · %0 FAİZ"
    gap = 10
    cw = (span - gap * (len(rows) - 1)) / len(rows)

    dr = b.draw
    ftyp = fit(b, dr, [r[0] for r in rows], b.p(94), 29, lambda s: b.mont(s, 700))
    fl, spl = fit_track(b, dr, [l1, l2], b.p(cw - 18), 12.5, 0.18, lambda s: b.cond(s))
    fnum = fit(b, dr, [r[1] for r in rows], b.p(cw - 34), 51, lambda s: b.mont(s, 700))
    fay = fit(b, dr, [r[2] for r in rows], b.p(cw - 50), 42, lambda s: b.mont(s, 700))
    ftl = b.mont(17, 700)
    fv, spv = fit_track(b, dr, [l3], b.p(cw - 22), 12, 0.10, lambda s: b.cond(s))

    for i, (typ, big, small) in enumerate(rows):
        x = x0 + i * (cw + gap)
        cwp, chp = b.p(cw), b.p(h)
        # Gölge: kart zeminden kalkmadan "yapıştırılmış" duruyordu.
        def shade(d, x=x):
            d.rounded_rectangle([b.p(x), b.p(y), b.p(x + cw), b.p(y + h)],
                                radius=b.p(10), fill=(0, 0, 0, 255))
        sh = Image.new("RGBA", b.im.size, (0, 0, 0, 0))
        shade(ImageDraw.Draw(sh))
        al = sh.split()[3].point(lambda v: min(255, round(v * 0.42)))
        al = al.filter(ImageFilter.GaussianBlur(b.p(7)))
        dk = Image.new("RGBA", b.im.size, (0, 0, 0, 0))
        dk.putalpha(al)
        b.im.alpha_composite(dk, (0, b.p(6)))

        # BUZLU CAM: kartın altındaki bölge bulanıklaştırılıp üstüne
        # yarı saydam tema gradyanı biniyor. Dolu renk kart "kapak" gibi
        # duruyordu, arkasındaki bina hiç görünmüyordu.
        reg = b.im.crop((b.p(x), b.p(y), b.p(x) + cwp, b.p(y) + chp))
        reg = reg.filter(ImageFilter.GaussianBlur(b.p(5)))
        tint = gradient((cwp, chp), th.card, angle=th.card_angle)
        tint.putalpha(th.card_alpha)
        body = reg.convert("RGBA")
        body.alpha_composite(tint)
        # Üst kenarda ince parlaklık — kart cam gibi kalkıyor.
        sheen = np.zeros((chp, 1, 4), np.float32)
        n = max(2, round(chp * 0.30))
        sheen[:n, 0, :3] = 255
        sheen[:n, 0, 3] = np.linspace(46, 0, n)
        body.alpha_composite(Image.fromarray(sheen.astype(np.uint8),
                                             "RGBA").resize((cwp, chp), Image.BILINEAR))
        mask = Image.new("L", (cwp, chp), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, cwp - 1, chp - 1],
                                               radius=b.p(10), fill=255)
        body.putalpha(mask)
        b.im.alpha_composite(body, (b.p(x), b.p(y)))

        def card(d, x=x, typ=typ, big=big, small=small):
            d.rounded_rectangle([b.p(x), b.p(y), b.p(x + cw), b.p(y + h)],
                                radius=b.p(10), outline=th.card_edge,
                                width=max(2, b.p(0.7)))
            bw, bh2 = b.p(cw * 0.56), b.p(34)
            bx = b.p(x + cw / 2) - bw // 2
            d.rounded_rectangle([bx, b.p(y) - bh2 // 2, bx + bw, b.p(y) + bh2 // 2],
                                radius=bh2 // 2, fill=th.badge_fill)
            d.text((bx + bw / 2, cap_top(ftyp, b.p(y))), typ, font=ftyp,
                   fill=th.badge_ink, anchor="ma")

            cx = b.p(x + cw / 2)
            track(b, d, (cx, b.p(y + 58)), l1, fl, (*th.label, 240), spl, "ma")
            wn = d.textlength(big, font=fnum)
            wt = d.textlength("TL", font=ftl) if priced else 0
            xa = cx - (wn + wt) / 2
            d.text((xa, b.p(y + 142)), big, font=fnum, fill=WHITE, anchor="ls")
            if priced:
                d.text((xa + wn, b.p(y + 142)), "TL", font=ftl, fill=(*ICE, 255),
                       anchor="ls")
            d.line([b.p(x + 20), b.p(y + 170), b.p(x + cw - 20), b.p(y + 170)],
                   fill=(255, 255, 255, 110), width=max(1, b.p(0.6)))
            track(b, d, (cx, b.p(y + 204)), l2, fl, (*th.label, 240), spl, "ma")

            pw, ph = b.p(cw - 26), b.p(74)
            px, py = b.p(x + 14), b.p(y + 238)
            d.rounded_rectangle([px, py, px + pw, py + ph], radius=b.p(6), fill=WHITE)
            wa2 = d.textlength(small, font=fay)
            wt2 = d.textlength("TL", font=ftl) if priced else 0
            ax = cx - (wa2 + wt2) / 2
            d.text((ax, py + ph - b.p(18)), small, font=fay, fill=DEEP, anchor="ls")
            if priced:
                d.text((ax + wa2, py + ph - b.p(18)), "TL", font=ftl, fill=OCEAN,
                       anchor="ls")

            vy = b.p(y + h) - b.p(52)
            d.rounded_rectangle([px, vy, px + pw, vy + b.p(38)], radius=b.p(5),
                                fill=th.badge_fill)
            track(b, d, (cx, cap_top(fv, vy + b.p(19))), l3, fv, th.badge_ink,
                  spv, "ma")
        overlay(b, card)


# Konum satırı çıkarıldı: üst satırda zaten "İzmit'in en değerli
# lokasyonunda" yazıyor, alttaki konum hapıyla üç kez tekrar ediyordu.
FEATS = [("EN UYGUN", "FİYATLAR", "onay"),
         ("YÜKSEK YATIRIM", "POTANSİYELİ", "grafik"),
         ("MODERN MİMARİ", "GENİŞ PEYZAJ", "bina"),
         ("VADE FARKSIZ", "60 AY TAKSİT", "takvim")]


def feat_pills(b, th, x, y0, pw, h, items, gapy=11) -> None:
    """Beyaz haplar, sağda dikey sütun — referansın yapısı."""
    dr = b.draw
    f, sp = fit_track(b, dr, [t for a in items for t in a[:2]], b.p(pw - h - 16),
                      12.5, 0.04, lambda s: b.mont(s, 600))

    for i, (l1, l2, kind) in enumerate(items):
        y = y0 + i * (h + gapy)

        def pill(d, y=y, l1=l1, l2=l2, kind=kind):
            d.rounded_rectangle([b.p(x), b.p(y), b.p(x + pw), b.p(y + h)],
                                radius=b.p(6), fill=WHITE)
            r = b.p(h * 0.30)
            cx, cy = b.p(x + h * 0.48), b.p(y + h / 2)
            d.rounded_rectangle([cx - r, cy - r, cx + r, cy + r], radius=b.p(5),
                                fill=th.pill_icon)
            picto(d, kind, cx, cy, r * 0.78, WHITE)
            tx = b.p(x + h * 0.92)
            track(b, d, (tx, b.p(y + h * 0.26)), l1, f, (*INK, 255), sp)
            track(b, d, (tx, b.p(y + h * 0.58)), l2, f, (*INK, 255), sp)
        overlay(b, pill)


def seal(b, th, cx, cy, r) -> None:
    dr = b.draw
    f1, sp1 = fit_track(b, dr, ["SINIRLI", "SAYIDA"], b.p(r * 1.5), 26, 0.04,
                        lambda s: b.mont(s, 800))
    f2, sp2 = fit_track(b, dr, ["BU FIRSAT", "KAÇMAZ!"], b.p(r * 1.9), 17, 0.04,
                        lambda s: b.mont(s, 800))
    fill = th.accent
    ink = th.badge_ink if th.key == "gece" else WHITE

    def paint(d):
        d.ellipse([b.p(cx - r), b.p(cy - r), b.p(cx + r), b.p(cy + r)], fill=fill)
        d.ellipse([b.p(cx - r * .88), b.p(cy - r * .88), b.p(cx + r * .88),
                   b.p(cy + r * .88)], outline=(*ink, 120), width=max(1, b.p(0.8)))
        for k in (-1, 0, 1):
            sx, sy, ss = b.p(cx + k * r * 0.26), b.p(cy - r * 0.44), b.p(r * 0.10)
            d.polygon([(sx, sy - ss), (sx + ss * .32, sy - ss * .28),
                       (sx + ss, sy - ss * .2), (sx + ss * .42, sy + ss * .24),
                       (sx + ss * .6, sy + ss), (sx, sy + ss * .46),
                       (sx - ss * .6, sy + ss), (sx - ss * .42, sy + ss * .24),
                       (sx - ss, sy - ss * .2), (sx - ss * .32, sy - ss * .28)],
                      fill=ink)
        track(b, d, (b.p(cx), b.p(cy - r * 0.20)), "SINIRLI", f1, ink, sp1, "ma")
        track(b, d, (b.p(cx), b.p(cy + r * 0.10)), "SAYIDA", f1, ink, sp1, "ma")
        rw, rh = b.p(r * 2.05), b.p(r * 0.56)
        rx, ry = b.p(cx) - rw // 2, b.p(cy + r * 0.42)
        d.polygon([(rx, ry), (rx + rw, ry), (rx + rw - b.p(r * .15), ry + rh // 2),
                   (rx + rw, ry + rh), (rx, ry + rh),
                   (rx + b.p(r * .15), ry + rh // 2)], fill=th.bar)
        track(b, d, (b.p(cx), ry + rh * 0.24), "BU FIRSAT", f2, WHITE, sp2, "ma")
        track(b, d, (b.p(cx), ry + rh * 0.58), "KAÇMAZ!", f2, WHITE, sp2, "ma")
    soft_shadow(b, paint, blur=7, alpha=130, dy=5)


def pin_pill(b, th, x, y, w, h, lines) -> None:
    dr = b.draw
    f, sp = fit_track(b, dr, lines, b.p(w - h - 14), 14, 0.06, lambda s: b.mont(s, 700))

    def paint(d):
        d.rounded_rectangle([b.p(x), b.p(y), b.p(x + w), b.p(y + h)], radius=b.p(6),
                            fill=DEEP)
        cx, cy, r = b.p(x + h * 0.48), b.p(y + h / 2), b.p(h * 0.24)
        picto(d, "pin", cx, cy, r, th.accent)
        tx = b.p(x + h * 0.90)
        for i, t in enumerate(lines):
            track(b, d, (tx, b.p(y + h * (0.24 + i * 0.34))), t, f, WHITE, sp)
    overlay(b, paint)


def bottom_bar(b, th, y, h) -> None:
    dr = b.draw
    fh = fit(b, dr, ["Tasarrufa Dayalı Faizsiz Finansman Sistemi ile"],
             b.p(W_MM - M * 2 - 50), 21,
             lambda s: b.mont(s, 600) if th.body_font == "mont" else b.cormorant(s, 600))
    items = [("banka", "BANKA YOK"), ("yuzde", "FAİZ YOK"), ("kisi", "KEFİL YOK")]
    fi, spi = fit_track(b, dr, [t for _, t in items], b.p((W_MM - M * 2) / 3 - 80), 18,
                        0.06, lambda s: b.mont(s, 700))

    def paint(d):
        d.rounded_rectangle([b.p(M), b.p(y), b.p(W_MM - M), b.p(y + h)],
                            radius=b.p(8), fill=th.bar,
                            outline=(*th.accent, 170), width=max(2, b.p(0.9)))
        a, bp, c = "Tasarrufa Dayalı ", "Faizsiz", " Finansman Sistemi ile"
        wa, wb, wc = (dr.textlength(t, font=fh) for t in (a, bp, c))
        x0 = b.p(W_MM / 2) - (wa + wb + wc) / 2
        d.text((x0, b.p(y + 36)), a, font=fh, fill=WHITE, anchor="ls")
        d.text((x0 + wa, b.p(y + 36)), bp, font=fh, fill=th.accent, anchor="ls")
        d.text((x0 + wa + wb, b.p(y + 36)), c, font=fh, fill=WHITE, anchor="ls")

        step = (W_MM - M * 2) / 3
        for i, (kind, t) in enumerate(items):
            cx = b.p(M + step * (i + 0.5))
            w = sum(d.textlength(ch, font=fi) for ch in t) + spi * (len(t) - 1)
            picto(d, kind, cx - w / 2 - b.p(24), b.p(y + 82), b.p(13), th.accent)
            track(b, d, (cx + b.p(14), cap_top(fi, b.p(y + 82))), t, fi, WHITE,
                  spi, "ma")
            if i:
                xv = b.p(M + step * i)
                d.line([xv, b.p(y + 58), xv, b.p(y + h - 14)],
                       fill=(255, 255, 255, 80), width=max(1, b.p(0.8)))
    overlay(b, paint)


def foot(b, th, y=1836) -> None:
    dr = b.draw

    def rule(d):
        d.line([b.p(M), b.p(y - 30), b.p(W_MM - M), b.p(y - 30)],
               fill=(*th.accent, 160), width=max(1, b.p(0.6)))
    overlay(b, rule)

    qs = b.p(54)
    qx, qy = b.p(W_MM - M) - qs, b.p(y - 10)

    def plate(d):
        d.rounded_rectangle([qx - b.p(5), qy - b.p(5), qx + qs + b.p(5),
                             qy + qs + b.p(5)], radius=b.p(4), fill=WHITE)
    overlay(b, plate)
    b.im.alpha_composite(qr_image(QR_URL, qs, DEEP), (qx, qy))

    fs, sps = fit_track(b, dr, [f"{SELLER} · {SELLER_ROLE}"], b.p(440), 10, 0.16,
                        lambda s: b.cond(s))
    sub = GREY if th.light else ICE

    def paint(d):
        d.text((b.p(M), b.p(y + 20)), SITE, font=b.marcellus(28), fill=th.foot_ink,
               anchor="ls")
        d.text((b.p(M), b.p(y + 50)), "  ·  ".join(PHONES), font=b.mont(17, 700),
               fill=th.foot_ink, anchor="ls")
        track(b, d, (b.p(M), b.p(y + 60)), f"{SELLER} · {SELLER_ROLE}", fs,
              (*sub, 230), sps)
    overlay(b, paint)


def afis(th, priced: bool) -> Image.Image:
    b = board()
    ground(b, th)

    lg = lockup(b.p(196), white=not th.light)
    b.im.alpha_composite(lg, ((b.W - lg.width) // 2, b.p(64)))

    eyebrow(b, th, 268, "İZMİT'İN EN DEĞERLİ LOKASYONUNDA")
    headline(b, th, 376, "FİYAT", "AVANTAJI")
    script_line(b, th, 452, "Kaçırılmayacak fırsat!")

    cards(b, th, 566, 392, PRICES if priced else SIZES, priced)
    feat_pills(b, th, 564, 566, 178, 90, FEATS)

    seal(b, th, 618, 1178, 102)
    bottom_bar(b, th, 1408, 130)

    if not priced:
        dr = b.draw
        fq, spq = fit_track(b, dr, ["FİYAT VE KAT PLANLARI İÇİN KAREKODU OKUTUN"],
                            b.p(600), 13, 0.16, lambda s: b.cond(s))

        def note(d):
            track(b, d, (b.p(W_MM / 2), b.p(1600)),
                  "FİYAT VE KAT PLANLARI İÇİN KAREKODU OKUTUN", fq,
                  (*th.accent, 250), spq, "ma")
        overlay(b, note)

    if not th.light:
        ru.vignette(b, 0.34, 2.3)
    foot(b, th)
    return b.im.convert("RGB")


THEMES = [G1, G2, G3, N1, N2, N3]
DESIGNS = [(f"fiyat-{t.key}" + ("" if pr else "-fiyatsiz"), t, pr)
           for t in THEMES for pr in (True, False)]


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(PREVIEW, exist_ok=True)
    for name, th, priced in DESIGNS:
        im = afis(th, priced)
        p = os.path.join(OUT, f"{name}.jpg")
        im.save(p, "JPEG", quality=94, subsampling=0, optimize=True, dpi=(DPI, DPI))
        sm = im.copy()
        sm.thumbnail((1400, 1400), Image.LANCZOS)
        sm.save(os.path.join(PREVIEW, f"{name}.jpg"), "JPEG", quality=88, optimize=True)
        print(f"  {name:<30} {th.name:<18} "
              f"{'rakamlı' if priced else 'rakamsız':<9} "
              f"{os.path.getsize(p)/1e6:.1f} MB")
    print(f"\n  → {OUT}")


if __name__ == "__main__":
    main()
