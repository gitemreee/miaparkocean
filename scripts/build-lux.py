#!/usr/bin/env python3
"""
MİA PARK OCEAN — roll-up serisi (4 tasarım x 2 renk düzeni = 8 dosya).

TASARIM İLKELERİ
────────────────
Önceki kurguda dört tasarımın da iskeleti aynıydı: logo ortada, başlık
ortada, ikon sırası, altta dekor fotoğraf. Aynı şablonun dört hali gibi
duruyordu. Bu sürümde her roll-up'ın YAPISI farklı:

    1 · CEPHE      tam sayfa mimari fotoğraf, altta tek cümle
    2 · ALTMIŞ     dev rakam; fotoğraf yalnızca alt bant
    3 · ÖDEME      üstte sert kenarlı fotoğraf, altta editoryal fiyat tablosu
    4 · DAİRELER   2x2 fotoğraf ızgarası, yazı görsellerin içinde

Ortak üç kural:

· TEK SOL PAY. Her şey 62 mm'den başlar. Ortalama yok — ortalanmış
  yığın şablon hissi veriyordu.
· ÖLÇEK FARKI. Manşet ~90 mm, ara başlık ~16 mm, künye ~9 mm. On kata
  varan fark; hepsi orta boy olunca hiyerarşi okunmuyordu.
· ALTIN AZ KULLANILIR. Saç teli çizgi, küçük etiket ve tek bir rakam.
  Manşet sıcak beyaz. Her yere altın sürülünce lüks değil ucuz duruyor.

ÖLÇÜ
─────
800 x 2000 mm, 1:1 ölçekte 100 dpi. Tasarım milimetre cinsinden yazılı;
piksele çeviren tek yer Board.p(). Kaset alt 40 mm'yi yutar, kritik yazı
1950 mm'yi geçmez.

RAKAMLAR
────────
Daire adetleri ve m² src/data/units.ts'ten. Fiyatlar depoda YOK; aşağıdaki
PRICES bloğu referans afişten alındı, bastırmadan önce doğrulatın.

Kullanım:
    python scripts/build-lux.py            # sekizi birden
    python scripts/build-lux.py cephe      # yalnız bir tasarım
    python scripts/build-lux.py --katman   # zemin + yazı katmanları
"""

from __future__ import annotations

import importlib.util
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_spec = importlib.util.spec_from_file_location(
    "bs", os.path.join(ROOT, "scripts", "build-signage.py"))
bs = importlib.util.module_from_spec(_spec)
sys.modules["bs"] = bs
_spec.loader.exec_module(bs)

Board = bs.Board
gradient, cover, scrim, overlay = bs.gradient, bs.cover, bs.scrim, bs.overlay
track, fit, fit_track, wrap = bs.track, bs.fit, bs.fit_track, bs.wrap
qr_image, lockup = bs.qr_image, bs.lockup

OUT = os.path.join(ROOT, "tabela", "lux")
PREVIEW = os.path.join(OUT, "onizleme")
SRC_OUT = os.path.join(OUT, "kaynak")

WHITE = (255, 255, 255)
SITE, PHONES = bs.SITE, bs.PHONES
SELLER, SELLER_ROLE = bs.SELLER, bs.SELLER_ROLE
QR_URL = "https://miaparkocean.com/?utm_source=rollup"

RU_W, RU_H, RU_DPI = 800, 2000, 100
M = 62                                   # tek sol pay
FOOT = 1876                              # künye satırının temel çizgisi

UNITS = bs.UNITS
TOTAL = bs.TOTAL_UNITS

# Referans afişten; depoda fiyat kaydı yok. TEK DEĞİŞTİRME NOKTASI.
PRICES = [
    ("1+0", "28 m²", "699.000", "29.900"),
    ("1+1", "50 m²", "999.000", "39.900"),
]


# ================================================================ renk düzeni
class Theme:
    def __init__(self, key, label, base, ink, accent, metal, muted, deep):
        self.key, self.label = key, label
        self.base = base          # zemin gradyanı
        self.ink = ink            # manşet — sıcak beyaz / beyaz
        self.accent = accent      # saç teli çizgi, etiket
        self.metal = metal        # tek dev rakamın gradyanı
        self.muted = muted        # ikincil yazı
        self.deep = deep          # fotoğraf üstü perde rengi


ALTIN = Theme(
    "ALTIN", "altın · gece lacivert",
    base=[(0.0, (8, 15, 28)), (0.45, (16, 27, 48)), (1.0, (7, 13, 26))],
    ink=(247, 243, 234),
    accent=(206, 166, 92),
    metal=[(0.0, (150, 106, 38)), (0.24, (232, 200, 126)), (0.46, (250, 236, 190)),
           (0.70, (200, 154, 70)), (1.0, (140, 98, 32))],
    muted=(176, 186, 204),
    deep=(6, 11, 22),
)

MIA = Theme(
    "MIA", "okyanus · buz",
    base=[(0.0, (3, 26, 39)), (0.45, (5, 52, 76)), (1.0, (3, 30, 45))],
    ink=WHITE,
    accent=bs.MIA_AQUA,
    metal=[(0.0, (86, 168, 192)), (0.26, (196, 234, 243)), (0.48, WHITE),
           (0.72, (150, 210, 226)), (1.0, (74, 152, 178))],
    muted=(178, 208, 220),
    deep=(2, 22, 34),
)


# ================================================================ yardımcılar
def board() -> Board:
    return Board(RU_W, RU_H, RU_DPI)


def col(b: Board) -> int:
    """Sol paydan sağ paya kalan sütun genişliği."""
    return b.p(RU_W - M * 2)


def cap_h(f) -> float:
    bb = f.getbbox("H")
    return bb[3] - bb[1]


def cap_top(f, cy: float) -> float:
    """track() metni TEPESİNDEN basar; görsel ortası cy olsun istiyorsak."""
    bb = f.getbbox("H")
    return cy - (bb[1] + bb[3]) / 2


def metal(b: Board, xy, text: str, font, stops, anchor="ls") -> None:
    """Gradyanla dolu yazı. Yalnızca dev rakamlarda kullanılır."""
    mask = Image.new("L", b.im.size, 0)
    ImageDraw.Draw(mask).text(xy, text, font=font, fill=255, anchor=anchor)
    box = mask.getbbox()
    if not box:
        return
    x0, y0, x1, y1 = box
    g = gradient((x1 - x0, y1 - y0), stops, angle=0.0)
    layer = Image.new("RGBA", b.im.size, (0, 0, 0, 0))
    layer.paste(g, (x0, y0), mask.crop(box))
    b.im.alpha_composite(layer)


def hair(b: Board, y: float, x0: float = M, x1: float = RU_W - M,
         color=(255, 255, 255), a: int = 90, w: float = 0.5) -> None:
    """Saç teli çizgi — bölümleri ayıran tek süs."""
    def paint(d):
        d.line([b.p(x0), b.p(y), b.p(x1), b.p(y)], fill=(*color, a),
               width=max(1, b.p(w)))
    overlay(b, paint)


def label(b: Board, y: float, text: str, th: Theme, size: float = 9.5,
          x: float = M, color=None, anchor="la") -> None:
    """Harf aralıklı küçük etiket — bölüm başlıkları hep bu."""
    f, sp = fit_track(b, b.draw, [text], col(b), size, 0.30,
                      lambda s: b.sans(s, "700"))

    def paint(d):
        track(b, d, (b.p(x), b.p(y)), text, f, (*(color or th.accent), 255), sp, anchor)
    overlay(b, paint)


def hero(b: Board, y: float, lines, th: Theme, size: float = 88,
         lead: float = 1.30, x: float = M, weight: str = "600") -> float:
    """Sola dayalı manşet, sıkı satır aralığı. Temel çizgi y'den başlar.

    Satır adımı puntonun oranı değil, BÜYÜK HARF YÜKSEKLİĞİNİN katı:
    Fraunces'te punto ile görünen boy arasındaki fark satırları
    gereğinden fazla açıyordu.
    """
    f = fit(b, b.draw, lines, col(b), size, lambda s: b.serif(s, weight))
    step = cap_h(f) * lead

    def paint(d):
        for i, ln in enumerate(lines):
            d.text((b.p(x), b.p(y) + i * step), ln, font=f, fill=th.ink, anchor="ls")
    overlay(b, paint)
    return (b.p(y) + (len(lines) - 1) * step) * 25.4 / b.dpi


def body(b: Board, y: float, text: str, th: Theme, size: float = 15,
         width: float = None, x: float = M, lead: float = 1.55) -> float:
    f = b.sans(size, "400")
    w = b.p(width) if width else col(b)
    lines = wrap(b.draw, text, f, w)
    step = b.p(size * lead)

    def paint(d):
        for i, ln in enumerate(lines):
            d.text((b.p(x), b.p(y) + i * step), ln, font=f, fill=(*th.muted, 248),
                   anchor="ls")
    overlay(b, paint)
    return (b.p(y) + (len(lines) - 1) * step) * 25.4 / b.dpi


def brand(b: Board, th: Theme, y: float = 74, w: float = 178,
          x: float = M) -> None:
    """Logo SOL ÜSTTE ve küçük. Ortalanmış dev kilit afiş hissi veriyordu."""
    lg = lockup(b.p(w), white=True)
    if th.key == "ALTIN":
        g = gradient(lg.size, th.metal, angle=0.2)
        g.putalpha(lg.split()[3])
        lg = g
    b.im.alpha_composite(lg, (b.p(x), b.p(y)))


def footer(b: Board, th: Theme, on_photo: bool = True) -> None:
    """Künye: solda web+telefon, sağda karekod. Bant yok, saç teli var."""
    hair(b, FOOT - 34, color=th.accent, a=130, w=0.6)

    qs = b.p(46)
    qx, qy = b.W - b.p(M) - qs, b.p(FOOT - 20)

    def plate(d):
        d.rounded_rectangle([qx - b.p(4), qy - b.p(4), qx + qs + b.p(4), qy + qs + b.p(4)],
                            radius=b.p(3), fill=(255, 255, 255, 250))
    overlay(b, plate)
    b.im.alpha_composite(qr_image(QR_URL, qs, th.deep), (qx, qy))

    dr = b.draw
    fi, spi = fit_track(b, dr, ["@MIAPARKOCEAN"], b.p(240), 8.4, 0.20,
                        lambda s: b.sans(s, "600"))
    fs, sps = fit_track(b, dr, [f"{SELLER} · {SELLER_ROLE}"], b.p(360), 7.4, 0.16,
                        lambda s: b.sans(s, "700"))

    def paint(d):
        d.text((b.p(M), b.p(FOOT)), SITE, font=b.serif(24, "600"),
               fill=th.ink, anchor="ls")
        track(b, d, (b.p(M), b.p(FOOT + 10)), "@MIAPARKOCEAN", fi, (*th.accent, 250), spi)
        d.text((b.p(M), b.p(FOOT + 40)), "  ·  ".join(PHONES), font=b.sans(13, "700"),
               fill=th.ink, anchor="ls")
        track(b, d, (b.p(M), b.p(FOOT + 50)), f"{SELLER} · {SELLER_ROLE}", fs,
              (*th.muted, 225), sps)
    overlay(b, paint)


def veil_up(b: Board, y0: float, y1: float, th: Theme, a0: int = 0,
            a1: int = 250) -> None:
    """Fotoğrafın altını yukarıdan aşağı koyulaştırır — yazı zemini."""
    h = b.p(y1) - b.p(y0)
    b.im.alpha_composite(scrim((b.W, h), [
        (0.0, (*th.deep, a0)), (0.55, (*th.deep, int(a1 * 0.82))),
        (1.0, (*th.deep, a1)),
    ]), (0, b.p(y0)))


# ============================================================ 1 · CEPHE
def ru_cephe(th: Theme) -> Image.Image:
    """Sert kenarlı mimari blok üstte, yazı altta karanlık alanda.

    facade-warm 1460x1600 — elimizdeki tek dikeye yakın render, cephenin
    ritmi dikey panoya birebir oturuyor. Tam sayfa denendi ama 1460 px
    kaynağı 4,9 kat büyütmek gerekiyor, baskıda dağılıyordu; 1180 mm'lik
    blokta büyütme 2,9 kat ve kare yanlardan yalnızca dörtte bir kırpılıyor.
    """
    b = board()
    b.im = gradient((b.W, b.H), th.base, angle=0.3)

    ph = 1180
    im = cover("facade-warm", (b.W, b.p(ph)), 0.40)
    im.alpha_composite(scrim((b.W, b.p(ph)), [
        (0.0, (*th.deep, 248)), (0.16, (*th.deep, 150)), (0.30, (*th.deep, 45)),
        (1.0, (*th.deep, 45)),
    ]))
    b.im.alpha_composite(im, (0, 0))
    hair(b, ph, x0=0, x1=RU_W, color=th.accent, a=255, w=1.6)

    brand(b, th, 74, 178)

    label(b, 1300, "İZMİT MİA BÖLGESİ", th, 10)
    last = hero(b, 1432, ["Lüks artık", "ulaşılabilir."], th, 96, 1.22)
    body(b, last + 64, "600 daire · dört yaşam tipi · dört blok, sekiz kat",
         th, 16, 660)
    hair(b, last + 104, x1=M + 190, color=th.accent, a=180, w=0.8)
    label(b, last + 146, "AVANTAJLI PEŞİNAT · VADE FARKSIZ 60 AY · %0 FAİZ", th, 11)

    footer(b, th)
    return b.im.convert("RGB")


# ============================================================ 2 · ALTMIŞ
def ru_altmis(th: Theme) -> Image.Image:
    """Dev rakam. Ölçek farkı bu panoda en uçta: 300 mm'ye karşı 9 mm."""
    b = board()
    b.im = gradient((b.W, b.H), th.base, angle=0.28)

    # Alt bant: fotoğraf doğal en-boyunda, kırpılmadan.
    bh = round(RU_W * 2294 / 4096)          # 800 mm → 448 mm
    top = 1330
    im = cover("courtyard-pools", (b.W, b.p(bh)), 0.5)
    im.alpha_composite(scrim((b.W, b.p(bh)), [
        (0.0, (*th.deep, 120)), (0.30, (*th.deep, 55)), (1.0, (*th.deep, 210)),
    ]))
    b.im.alpha_composite(im, (0, b.p(top)))

    brand(b, th, 78, 178)

    label(b, 300, "TASARRUFA DAYALI FAİZSİZ FİNANSMAN", th, 10)

    # 300 mm'lik rakam — panonun grafiği bu.
    f60 = b.serif(300, "700")
    metal(b, (b.p(M - 14), b.p(660)), "60", f60, th.metal, "ls")

    dr = b.draw
    w60 = dr.textlength("60", font=f60)
    fx = b.p(M - 14) + w60 + b.p(22)
    fay, spay = fit_track(b, dr, ["AY VADE", "%0 FAİZ"], b.p(300), 20, 0.14,
                          lambda s: b.sans(s, "700"))

    def side(d):
        track(b, d, (fx, b.p(548)), "AY VADE", fay, th.ink, spay)
        track(b, d, (fx, b.p(590)), "%0 FAİZ", fay, (*th.accent, 255), spay)
    overlay(b, side)

    hair(b, 736)

    # Dört ret — sola dayalı liste, aralarında saç teli.
    nos = ["BANKA YOK", "KEFİL YOK", "ARA ÖDEME YOK", "SÜRPRİZ YOK"]
    fn = fit(b, dr, nos, col(b), 44, lambda s: b.serif(s, "600"))
    y = 800
    for i, t in enumerate(nos):
        def one(d, t=t, y=y):
            d.text((b.p(M), b.p(y)), t, font=fn, fill=th.ink, anchor="ls")
        overlay(b, one)
        if i < len(nos) - 1:
            hair(b, y + 22)
        y += 78

    body(b, 1160, "Peşinatın ardından ödemeniz 60 aya kadar sabit taksitlere "
                  "bölünür. Ara ödeme çıkmaz, taksitiniz baştan sona değişmez.",
         th, 15, 660)

    label(b, 1256, "T.C. TİCARET BAKANLIĞI · KOOPBİS KAYITLI KOOPERATİF", th, 10)

    footer(b, th)
    return b.im.convert("RGB")


# ============================================================ 3 · ÖDEME
def ru_odeme(th: Theme) -> Image.Image:
    """Editoryal fiyat tablosu üstte, fotoğraf tam boy alt blok.

    Fiyatlar kutulu kart yerine tabloya alındı: çerçeve, dolgu ve hap üst
    üste binince ilan panosu gibi duruyordu. Rakamı büyütüp etiketi
    küçültmek aynı bilgiyi daha sakin veriyor.
    """
    b = board()
    b.im = gradient((b.W, b.H), th.base, angle=0.28)

    brand(b, th, 74, 178)

    label(b, 290, "ÖDEME PLANI", th, 11)
    hero(b, 424, ["Peşinatı ödeyin,", "60 ay oturun."], th, 70, 1.24)

    dr = b.draw
    ftyp = fit(b, dr, [p[0] for p in PRICES], b.p(190), 52, lambda s: b.serif(s, "700"))
    fnum = fit(b, dr, [p[2] for p in PRICES], b.p(330), 56, lambda s: b.serif(s, "700"))
    fay = fit(b, dr, [f"aylık {p[3]} ₺ · 60 ay taksit" for p in PRICES], b.p(430), 24,
              lambda s: b.serif(s, "500"))
    fl, spl = fit_track(b, dr, [f"{p[1]} · {p[0] and ''}" for p in PRICES] +
                        ["PEŞİNAT"], b.p(230), 9, 0.20, lambda s: b.sans(s, "700"))

    top = 648
    for i, (typ, area, pesin, aylik) in enumerate(PRICES):
        yy = top + i * 208

        def row(d, yy=yy, typ=typ, area=area, pesin=pesin, aylik=aylik):
            d.text((b.p(M), b.p(yy)), typ, font=ftyp, fill=th.ink, anchor="ls")
            track(b, d, (b.p(M), b.p(yy + 14)), area, fl, (*th.muted, 240), spl)
            wn = d.textlength(pesin, font=fnum)
            d.text((b.p(RU_W - M) - b.p(14), b.p(yy)), pesin, font=fnum,
                   fill=th.ink, anchor="rs")
            d.text((b.p(RU_W - M), b.p(yy)), "₺", font=b.sans(20, "700"),
                   fill=(*th.accent, 255), anchor="rs")
            track(b, d, (b.p(RU_W - M), b.p(yy + 14)), "PEŞİNAT", fl,
                  (*th.muted, 240), spl, "ra")
            d.text((b.p(RU_W - M), b.p(yy + 82)),
                   f"aylık {aylik} ₺ · 60 ay taksit", font=fay,
                   fill=(*th.accent, 255), anchor="rs")
        overlay(b, row)
        hair(b, yy + 108, a=80)

    label(b, top + 366, "BANKA YOK · FAİZ YOK · KEFİL YOK · ARA ÖDEME YOK", th, 12)

    # Alt blok: fotoğraf doğal en-boyunda, tam genişlik.
    bh = round(RU_W * 1118 / 1600)          # 559 mm
    ty = 1168
    im = cover("balcony-dusk", (b.W, b.p(bh)), 0.5)
    im.alpha_composite(scrim((b.W, b.p(bh)), [
        (0.0, (*th.deep, 90)), (0.35, (*th.deep, 25)), (1.0, (*th.deep, 120)),
    ]))
    b.im.alpha_composite(im, (0, b.p(ty)))
    hair(b, ty, x0=0, x1=RU_W, color=th.accent, a=255, w=1.6)

    footer(b, th, on_photo=False)
    return b.im.convert("RGB")


# ============================================================ 4 · DAİRELER
SHOTS = ["ic-mekan/01-1plus0-salon", "ic-mekan/05-1plus1-salon",
         "ic-mekan/09-loft-salon", "ic-mekan/14-dubleks-bahcesi"]


def ru_daireler(th: Theme) -> Image.Image:
    """2x2 fotoğraf ızgarası; yazı görsellerin İÇİNDE, altında değil."""
    b = board()
    b.im = gradient((b.W, b.H), th.base, angle=0.28)

    brand(b, th, 78, 178)

    label(b, 296, "DÖRT YAŞAM TİPİ, TEK PROJEDE", th, 10)
    hero(b, 396, ["Hangisi", "size göre?"], th, 84, 1.22)

    gx, gy = M, 560
    tw = (RU_W - M * 2 - 16) / 2
    tht = 480
    dr = b.draw
    ftyp = fit(b, dr, [u[0] for u in UNITS], b.p(tw - 30), 38,
               lambda s: b.serif(s, "700"))
    fn, spn = fit_track(b, dr, [u[1].upper() for u in UNITS], b.p(tw - 26), 8.6, 0.16,
                        lambda s: b.sans(s, "700"))

    for i, ((typ, name, area, count), shot) in enumerate(zip(UNITS, SHOTS)):
        cx = gx + (i % 2) * (tw + 16)
        cy = gy + (i // 2) * (tht + 16)
        pw, phh = b.p(tw), b.p(tht)
        im = cover(shot, (pw, phh), 0.5)
        im.alpha_composite(scrim((pw, phh), [
            (0.0, (*th.deep, 30)), (0.44, (*th.deep, 70)), (1.0, (*th.deep, 232)),
        ]))
        mask = Image.new("L", (pw, phh), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, pw - 1, phh - 1],
                                               radius=b.p(4), fill=255)
        im.putalpha(Image.fromarray(
            (np.asarray(im.split()[3], np.float32) *
             (np.asarray(mask, np.float32) / 255.0)).astype(np.uint8), "L"))
        b.im.alpha_composite(im, (b.p(cx), b.p(cy)))

        def tile(d, cx=cx, cy=cy, typ=typ, name=name, area=area, count=count):
            d.text((b.p(cx + 18), b.p(cy + tht - 54)), typ, font=ftyp,
                   fill=th.ink, anchor="ls")
            d.text((b.p(cx + tw - 18), b.p(cy + tht - 54)), area,
                   font=b.serif(20, "600"), fill=(*th.accent, 255), anchor="rs")
            track(b, d, (b.p(cx + 18), b.p(cy + tht - 38)), name.upper(), fn,
                  (*th.muted, 246), spn)
            track(b, d, (b.p(cx + tw - 18), b.p(cy + tht - 38)), f"{count} DAİRE", fn,
                  (*th.accent, 250), spn, "ra")
        overlay(b, tile)

    hair(b, 1596, color=th.accent, a=150, w=0.7)
    label(b, 1636, f"TOPLAM {TOTAL} DAİRE · DÖRT BLOK · SEKİZ KAT", th, 12)
    body(b, 1712, "Kat planları ve daire seçenekleri için karekodu okutun.",
         th, 14, 620)

    footer(b, th, on_photo=False)
    return b.im.convert("RGB")


DESIGNS = [
    ("rollup-1-cephe", ru_cephe, "cephe"),
    ("rollup-2-altmis", ru_altmis, "altmış"),
    ("rollup-3-odeme", ru_odeme, "ödeme"),
    ("rollup-4-daireler", ru_daireler, "daireler"),
]
THEMES = [ALTIN, MIA]


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(PREVIEW, exist_ok=True)
    only = [a for a in sys.argv[1:] if not a.startswith("--")]
    for th in THEMES:
        print(f"\n  {th.label}")
        for name, fn, label_ in DESIGNS:
            if only and not any(o in name for o in only):
                continue
            im = fn(th)
            full = f"{name}-{th.key}"
            p = os.path.join(OUT, f"{full}.jpg")
            im.save(p, "JPEG", quality=94, subsampling=0, optimize=True,
                    dpi=(RU_DPI, RU_DPI))
            small = im.copy()
            small.thumbnail((1400, 1400), Image.LANCZOS)
            small.save(os.path.join(PREVIEW, f"{full}.jpg"), "JPEG", quality=88,
                       optimize=True)
            print(f"    {full:<30} {im.width}x{im.height} px  "
                  f"{os.path.getsize(p)/1e6:.1f} MB")
    print(f"\n  → {OUT}")


def build_layers() -> None:
    os.makedirs(SRC_OUT, exist_ok=True)
    for th in THEMES:
        for name, fn, label_ in DESIGNS:
            full = f"{name}-{th.key}"
            bs._NO_TEXT = True
            bg = fn(th).convert("RGB")
            bs._NO_TEXT = False
            bp = os.path.join(SRC_OUT, f"{full}-zemin.jpg")
            bg.save(bp, "JPEG", quality=94, subsampling=0, optimize=True,
                    dpi=(RU_DPI, RU_DPI))
            bg = Image.open(bp).convert("RGB")
            tam = Image.open(os.path.join(OUT, f"{full}.jpg")).convert("RGB")
            tp = os.path.join(SRC_OUT, f"{full}-yazi.png")
            bs._split(tam, bg).save(tp, optimize=True)
            print(f"  {full:<30} zemin {os.path.getsize(bp)/1e6:5.1f} MB · "
                  f"yazı {os.path.getsize(tp)/1e6:5.1f} MB")
    print(f"\n  → {SRC_OUT}")


if __name__ == "__main__":
    if "--katman" in sys.argv:
        build_layers()
    else:
        main()
