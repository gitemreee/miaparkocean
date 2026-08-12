#!/usr/bin/env python3
"""MİA PARK OCEAN — online katalog / broşür üreticisi.

Sitedeki kimlikle birebir aynı 10 sayfalık A4 katalog üretir:
  public/mia-park-ocean-katalog.pdf   indirilebilir PDF
  public/images/catalog-1..10.webp    online katalog sayfaları (+ -sm srcset)

Renkler, tipografi ve dalga silueti siteden alınır; daire adetleri tek
kaynaktan (aşağıdaki UNITS) gelir, elle rakam yazılmaz.

Kullanım:
    pip install pillow numpy
    python scripts/build-catalog.py
"""

from __future__ import annotations

import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "brand-source", "fonts")
IMG = os.path.join(ROOT, "public", "images")
BRAND = os.path.join(ROOT, "public", "brand")

# --- A4 @ 200 dpi ---
W, H = 1654, 2339
M = 118  # kenar boşluğu

# --- Palet (globals.css ile aynı) ---
# Marka renk ailesi (marka paketi · mia-brand.css)
MIA_DEEP = (9, 86, 120)      # #095678
MIA_DARK = (26, 116, 150)    # #1A7496
MIA_OCEAN = (44, 148, 180)   # #2C94B4
MIA_CYAN = (72, 171, 197)    # #48ABC5
MIA_AQUA = (110, 189, 208)   # #6EBDD0
MIA_LIGHT = (146, 209, 223)  # #92D1DF
MIA_PALE = (184, 228, 236)   # #B8E4EC
MIA_ICE = (221, 247, 250)    # #DDF7FA

NAVY = (4, 40, 58)
MIDNIGHT = MIA_DEEP
SAPPHIRE = MIA_DEEP
LOGO_BLUE = MIA_DEEP
LOGO_MID = MIA_DARK
LOGO_BRIGHT = MIA_CYAN
LOGO_LIGHT = MIA_LIGHT
ICE = MIA_PALE
MIST = (240, 250, 252)
INK = (4, 40, 58)
INK_SOFT = (82, 113, 126)
WHITE = (255, 255, 255)
FOREST = (11, 110, 79)

# Metalik geçiş: koyu petrol → okyanus → buz mavisi
BRAND_STOPS = [(0.0, NAVY), (0.22, MIA_DEEP), (0.48, MIA_DARK), (0.74, MIA_OCEAN), (1.0, MIA_CYAN)]

# Dalga: logodan birebir kesilmiş maske (scripts/build-wave.py üretir).
# Katalog da sitedeki dalganın AYNISINI kullanır.
WAVE_MASK_PNG = os.path.join(ROOT, "public", "brand", "wave-mask.png")

# ---------------------------------------------------------------- veri
PROJECT = {
    "name": "MİA PARK OCEAN",
    "region": "İZMİT MİA BÖLGESİ",
    "tagline": "Lüks artık ulaşılabilir.",
    "developer": "S.S. Yahya Kaptan Birlik Yapı Kooperatifi",
    "seller": "Ocean Gayrimenkul",
    "site": "miaparkocean.com",
    "phones": "0540 028 00 41 · 0541 128 40 41",
    "address": "Ömerağa Mah. Abdurrahman Yüksel Cad. Bana Bak Ap. No:15/4 · İzmit / Kocaeli",
}

# src/data/units.ts ile aynı
UNITS = [
    {"type": "1+0", "name": "1+0 Daireler", "count": 472, "area": 28,
     "tagline": "Akıllı tasarım, maksimum konfor",
     "text": "Yaşam alanı, mutfak ve balkonun tek bir ferah düzende buluştuğu 1+0 daireler; ilk evini alanlar ve yatırım yapmak isteyenler için pratik bir seçenek.",
     "features": ["Açık plan ferah yaşam alanı", "Geniş balkon", "Modern mutfak tasarımı", "Yatırım için ideal ölçek"],
     "img": "unit-1plus0-a.webp", "img2": "unit-1plus0-b.webp", "plan": "unit-1plus0-plan.webp", "wide": "facade-warm.webp"},
    {"type": "1+1", "name": "1+1 Daireler", "count": 96, "area": 50,
     "tagline": "Ferah, konforlu ve fonksiyonel",
     "text": "Yatak odasının yaşam alanından ayrıldığı 1+1 daireler, hem yalnız hem çift yaşayanlar için rahat bir düzen kuruyor. Geniş balkonu ve açık mutfağıyla gün boyu ferah kalıyor.",
     "features": ["Ayrı yatak odası", "Geniş balkon", "Açık mutfak", "Yüksek kaliteli iç mekân"],
     "img": "unit-1plus1-a.webp", "img2": "unit-1plus1-c.webp", "plan": "unit-1plus1-plan.webp", "wide": "balcony-dusk.webp"},
    {"type": "1+1", "name": "1+1 Bahçe Loft", "count": 16, "area": 50,
     "tagline": "Zemin katta kendi bahçeniz",
     "text": "1+1 dairenin aynı ferah planı, bu kez zemin katta ve kendine ait özel bahçesiyle. Loft kurgusu yaşam alanını yükselterek genişletiyor; bahçeye açılan camlar sabah kahvesini dışarı taşıyor.",
     "features": ["Özel kullanım bahçesi", "Loft kurgulu yüksek tavan", "Bahçeye direkt çıkış", "Ayrı yatak odası"],
     "img": "unit-2plus1-c.webp", "img2": "unit-1plus1-b.webp", "plan": "unit-1plus1-plan.webp", "wide": "terrace-pergola.webp"},
    {"type": "2+1", "name": "2+1 Bahçe Dubleks", "count": 16, "area": 100,
     "tagline": "Bahçeniz, evinizin devamı",
     "text": "İki katlı kurgusu ve zemindeki özel bahçesiyle 2+1 dubleks, apartman içinde müstakil ev keyfi veriyor. Geniş sürme camlar ve bahçeye açılan yaşam alanı aileler düşünülerek planlandı.",
     "features": ["Özel kullanım bahçesi", "İki katlı dubleks yaşam", "Geniş sürme camlar", "Pergolalı oturma alanı"],
     "img": "unit-2plus1-a.webp", "img2": "unit-2plus1-d.webp", "plan": "unit-2plus1-cutaway.webp", "wide": "duplex-cutaway.webp"},
]
TOTAL = sum(u["count"] for u in UNITS)

AMENITIES = [
    "Kapalı yüzme havuzu", "Fitness salonu", "Sauna ve Türk hamamı",
    "Çocuk oyun parkı", "Kapalı otopark", "7/24 güvenlik",
    "Merkezi avlu", "Dekoratif süs havuzları", "Geniş peyzaj alanları",
    "Yürüyüş ve dinlenme yolları", "Özel gece aydınlatması", "Bahçeli zemin daireler",
]

DISTANCES = [
    ("D-100 Karayolu", "1 dk"), ("İzmit Sahili", "2 dk"), ("41 Burada AVM", "3 dk"),
    ("Şehir Merkezi", "5 dk"), ("Şehir Hastanesi", "5 dk"), ("TEM Otoyolu", "5 dk"),
    ("Symbol AVM", "7 dk"), ("Kocaeli Üniversitesi", "10 dk"),
]


# ---------------------------------------------------------------- yardımcılar
def f(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def serif(s): return f("Fraunces-500.ttf", s)
def sans(s): return f("Manrope-400.ttf", s)
def sans_sb(s): return f("Manrope-600.ttf", s)
def sans_b(s): return f("Manrope-700.ttf", s)


def gradient(size, stops=BRAND_STOPS, angle: float = 0.62) -> Image.Image:
    w, h = size
    yy, xx = np.mgrid[0:h, 0:w]
    t = np.clip((xx / max(w - 1, 1)) * angle + (yy / max(h - 1, 1)) * (1 - angle), 0, 1)
    arr = np.zeros((h, w, 3), np.float32)
    for i in range(len(stops) - 1):
        t0, c0 = stops[i]
        t1, c1 = stops[i + 1]
        m = (t >= t0) & (t <= t1)
        k = np.clip((t - t0) / max(t1 - t0, 1e-6), 0, 1)
        for c in range(3):
            arr[:, :, c] = np.where(m, c0[c] + (c1[c] - c0[c]) * k, arr[:, :, c])
    return Image.fromarray(arr.astype(np.uint8), "RGB").convert("RGBA")


def wave(width: int, height: int, color, opacity: float = 1.0, flip: bool = False) -> Image.Image:
    """Logodaki dalgayı istenen boyutta, istenen renkte çizer."""
    mask = Image.open(WAVE_MASK_PNG).convert("RGBA").split()[3].resize((width, height), Image.LANCZOS)
    if flip:
        mask = mask.transpose(Image.FLIP_TOP_BOTTOM)
    im = Image.new("RGBA", (width, height), (*color, 255))
    im.putalpha(Image.eval(mask, lambda v: int(v * opacity)))
    return im


def photo(name: str, box, radius: int = 0) -> Image.Image:
    """Görseli kutuya kırparak sığdırır."""
    im = Image.open(os.path.join(IMG, name)).convert("RGB")
    bw, bh = box
    s = max(bw / im.width, bh / im.height)
    im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
    im = im.crop(((im.width - bw) // 2, (im.height - bh) // 2, (im.width - bw) // 2 + bw, (im.height - bh) // 2 + bh))
    im = im.convert("RGBA")
    if radius:
        mask = Image.new("L", (bw, bh), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, bw - 1, bh - 1], radius=radius, fill=255)
        im.putalpha(mask)
    return im


def rounded(size, radius, fill) -> Image.Image:
    im = Image.new("RGBA", size, (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], radius=radius, fill=fill)
    return im


def track(dr, xy, s, font, fill, spacing, anchor="la"):
    """Harf aralıklı metin."""
    widths = [dr.textlength(c, font=font) for c in s]
    total = sum(widths) + spacing * (len(s) - 1)
    if anchor[0] == "m":
        x = xy[0] - total / 2
    elif anchor[0] == "r":
        x = xy[0] - total
    else:
        x = xy[0]
    for c, w in zip(s, widths):
        dr.text((x, xy[1]), c, font=font, fill=fill, anchor="l" + anchor[1])
        x += w + spacing
    return total


def wrap(dr, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = f"{cur} {w}".strip()
        if dr.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines


def para(dr, xy, text, font, fill, max_w, leading):
    x, y = xy
    for line in wrap(dr, text, font, max_w):
        dr.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def logo_img(width: int, on_dark: bool = False) -> Image.Image:
    """Logo. Koyu mavi zeminde beyaz sürüm kullanılır (plaket yok)."""
    name = "logo-ocean-white.png" if on_dark else "logo-ocean-trim.png"
    im = Image.open(os.path.join(BRAND, name)).convert("RGBA")
    return im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)


def mark_img(width: int) -> Image.Image:
    im = Image.open(os.path.join(BRAND, "mark-ocean-trim.png")).convert("RGBA")
    return im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)


# ---------------------------------------------------------------- sayfa iskeleti
def base_page(section: str, page_no: int, footer: str = "") -> tuple[Image.Image, ImageDraw.ImageDraw]:
    page = Image.new("RGBA", (W, H), WHITE)
    dr = ImageDraw.Draw(page)

    # Çok hafif turkuaz zemin yıkaması (sitedeki gibi)
    washer = gradient((W, H), [(0.0, WHITE), (0.45, (246, 252, 254)), (1.0, (228, 244, 249))], angle=0.15)
    page.alpha_composite(washer)

    # Üst bant
    m = mark_img(58)
    page.alpha_composite(m, (M, 78))
    dr.text((M + 78, 86), PROJECT["name"], font=serif(34), fill=INK)
    track(dr, (M + 79, 128), PROJECT["region"], sans_b(15), (120, 140, 165), 4)
    lab = section.upper()
    fs = 19 if len(lab) <= 18 else 15
    track(dr, (W - M, 104), lab, sans_b(fs), LOGO_BLUE, 4, anchor="ra")
    dr.line([M, 168, W - M, 168], fill=(*ICE, 255), width=2)

    # Alt bant
    dr.line([M, H - 118, W - M, H - 118], fill=(*ICE, 255), width=2)
    dr.text((M, H - 100), footer or "MİA PARK OCEAN · İzmit MİA Bölgesi", font=sans(20), fill=(140, 158, 180))
    dr.text((W - M, H - 100), f"{page_no:02d}", font=sans_b(22), fill=LOGO_BLUE, anchor="ra")
    return page, dr


def eyebrow(dr, y, text):
    dr.rounded_rectangle([M, y + 8, M + 46, y + 14], radius=3, fill=LOGO_BLUE)
    track(dr, (M + 64, y), text.upper(), sans_b(21), LOGO_BLUE, 5)
    return y + 46


def stat_row(page, dr, y, items, w=None):
    """Eşit genişlikte rakam şeridi."""
    w = w or (W - 2 * M)
    cw = w // len(items)
    for i, (val, label) in enumerate(items):
        x = M + i * cw
        dr.text((x, y), val, font=serif(62), fill=INK)
        dr.text((x, y + 82), label, font=sans_sb(21), fill=INK_SOFT)
        if i:
            dr.line([x - 34, y + 8, x - 34, y + 100], fill=(*ICE, 255), width=2)
    return y + 128


# ---------------------------------------------------------------- sayfalar
def page_cover():
    page = Image.new("RGBA", (W, H), WHITE)
    hero = photo("night-gate.webp", (W, H))
    page.alpha_composite(hero)
    # okyanus perdesi
    scrim = gradient((W, H), [(0.0, NAVY), (0.55, MIDNIGHT), (1.0, LOGO_BLUE)], angle=0.3)
    scrim.putalpha(190)
    page.alpha_composite(scrim)
    dr = ImageDraw.Draw(page)

    # Koyu zeminde logo beyaz durur — plaket yok
    lg = logo_img(600, on_dark=True)
    page.alpha_composite(lg, ((W - lg.width) // 2, 440))

    track(dr, (W / 2, 1180), PROJECT["tagline"].upper(), sans_b(30), LOGO_LIGHT, 9, anchor="ma")
    dr.text((W / 2, 1250), "Tasarrufa dayalı faizsiz finansmanla", font=sans(34), fill=(*ICE, 255), anchor="ma")
    dr.text((W / 2, 1300), "bankasız, faizsiz, kefilsiz ev sahibi olun.", font=sans(34), fill=(*ICE, 255), anchor="ma")

    # rozetler
    badges = ["Bankasız", "Faizsiz", "Kefilsiz", "60 Ay Vade"]
    fb = sans_sb(28)
    widths = [dr.textlength(b, font=fb) + 76 for b in badges]
    total = sum(widths) + 24 * (len(badges) - 1)
    x = (W - total) / 2
    for b, bw in zip(badges, widths):
        chip = rounded((int(bw), 78), 39, (255, 255, 255, 40))
        ImageDraw.Draw(chip).rounded_rectangle([0, 0, int(bw) - 1, 77], radius=39, outline=(*LOGO_LIGHT, 150), width=2)
        page.alpha_composite(chip, (int(x), 1420))
        dr.text((x + bw / 2, 1444), b, font=fb, fill=WHITE, anchor="ma")
        x += bw + 24

    # alt dalga + künye
    band_h = 300
    wv = wave(W, 150, WHITE, 1.0)
    page.alpha_composite(wv, (0, H - band_h - 150 + 4))
    dr.rectangle([0, H - band_h, W, H], fill=WHITE)
    y = H - band_h + 46
    stat_row(page, dr, y, [(str(TOTAL), "Toplam Daire"), (str(len(UNITS)), "Yaşam Tipi"), ("60", "Ay Vade"), ("28–100", "m² Aralığı")])
    dr.text((W / 2, H - 92), PROJECT["site"], font=sans_b(30), fill=LOGO_BLUE, anchor="ma")
    return page


def page_project():
    page, dr = base_page("Proje", 2)
    y = eyebrow(dr, 250, "Proje")
    dr.text((M, y), "Yaşamınızın", font=serif(92), fill=INK)
    dr.text((M, y + 104), "yeni merkezi", font=serif(92), fill=LOGO_BLUE)
    y += 240

    txt = ("İzmit MİA Bölgesi'nde, şehrin gelişen yaşam aksının tam merkezinde yükselen MİA PARK OCEAN; "
           f"4 blok ve {TOTAL} daireden oluşuyor. Doğayla iç içe ama şehrin her yerine dakikalar uzaklıkta "
           "bir yaşam kuruyoruz.")
    y = para(dr, (M, y), txt, sans(30), INK_SOFT, W - 2 * M - 640, 48) + 20

    bullets = [
        f"{TOTAL} daire · {len(UNITS)} farklı yaşam tipi",
        "4 blok · zemin + 7 kat",
        "Yaklaşık 10 dönüm arazi",
        "Temeller tamamen fore kazık sistemiyle",
        "Merkezi avlu, süs havuzları ve geniş peyzaj",
    ]
    for b in bullets:
        dr.ellipse([M + 4, y + 12, M + 20, y + 28], fill=LOGO_BRIGHT)
        dr.text((M + 44, y), b, font=sans_sb(28), fill=INK)
        y += 56

    page.alpha_composite(photo("hero-courtyard-dusk.webp", (560, 700), 28), (W - M - 560, 300))
    page.alpha_composite(photo("aerial-pools.webp", (560, 380), 28), (W - M - 560, 1030))
    page.alpha_composite(photo("facade-warm.webp", (W - 2 * M, 520), 28), (M, 1470))

    stat_row(page, dr, 2060, [(str(UNITS[0]["count"]), "1+0 Daire"), (str(UNITS[1]["count"]), "1+1 Daire"),
                              (str(UNITS[2]["count"] + UNITS[3]["count"]), "Bahçeli Daire"), (str(TOTAL), "Toplam")])
    return page


def page_finance():
    page, dr = base_page("Finansman", 3)
    y = eyebrow(dr, 250, "Tasarrufa Dayalı Faizsiz Finansman")
    dr.text((M, y), "Banka yok. Faiz yok.", font=serif(84), fill=INK)
    dr.text((M, y + 96), "Kefil yok.", font=serif(84), fill=LOGO_BLUE)
    y += 230

    y = para(dr, (M, y), "Avantajlı peşinatla başlarsınız, kalan tutarı 60 aya kadar sabit taksitlerle ödersiniz. "
                        "Ara ödeme yok, vade farkı yok, bankaya kâr payı yok.",
             sans(30), INK_SOFT, W - 2 * M, 48) + 40

    # büyük rakam kutuları
    boxes = [("%0", "Faiz"), ("60", "Ay Vade"), ("0", "Ara Ödeme")]
    bw = (W - 2 * M - 48) // 3
    for i, (big, lab) in enumerate(boxes):
        x = M + i * (bw + 24)
        card = rounded((bw, 230), 28, (*MIST, 255))
        ImageDraw.Draw(card).rounded_rectangle([0, 0, bw - 1, 229], radius=28, outline=(*ICE, 255), width=2)
        page.alpha_composite(card, (x, y))
        dr.text((x + bw / 2, y + 44), big, font=serif(96), fill=LOGO_BLUE, anchor="ma")
        dr.text((x + bw / 2, y + 168), lab, font=sans_sb(26), fill=INK_SOFT, anchor="ma")
    y += 300

    page.alpha_composite(photo("courtyard-pools.webp", (W - 2 * M, 560), 28), (M, y))
    y += 620

    items = [
        ("Sabit taksit, ara ödeme yok", "Ödeme planınız baştan bellidir; sürpriz maliyet çıkmaz."),
        ("Üye maliyetine konut", "Kooperatif kâr amacı gütmez; araya müteahhit kârı girmez."),
        ("Şeffaf ve devlet denetiminde", "KOOPBİS kaydı ve 1163 sayılı Kooperatifler Kanunu kapsamında."),
        ("Enflasyona karşı avantaj", "Bugünün fiyatıyla, bugünün koşullarında başlarsınız."),
    ]
    cw = (W - 2 * M - 40) // 2
    for i, (t, d) in enumerate(items):
        x = M + (i % 2) * (cw + 40)
        yy = y + (i // 2) * 170
        dr.rounded_rectangle([x, yy + 6, x + 6, yy + 120], radius=3, fill=LOGO_BRIGHT)
        dr.text((x + 30, yy), t, font=sans_b(28), fill=INK)
        para(dr, (x + 30, yy + 46), d, sans(24), INK_SOFT, cw - 40, 36)
    return page


def page_unit_overview():
    page, dr = base_page("Daire Tipleri", 4)
    y = eyebrow(dr, 250, "Daire Tipleri")
    dr.text((M, y), "Size uygun daireyi seçin", font=serif(84), fill=INK)
    y += 120
    y = para(dr, (M, y), f"1+0 stüdyodan bahçeli 2+1 dublekse kadar {len(UNITS)} farklı daire; "
                         "ihtiyacınıza ve bütçenize göre seçebileceğiniz dört yaşam biçimi.",
             sans(30), INK_SOFT, W - 2 * M, 48) + 40

    cw = (W - 2 * M - 3 * 26) // 4
    for i, u in enumerate(UNITS):
        x = M + i * (cw + 26)
        page.alpha_composite(photo(u["img"], (cw, 300), 22), (x, y))
        card_y = y + 320
        dr.text((x, card_y), u["type"], font=sans_b(26), fill=LOGO_BLUE)
        dr.text((x, card_y + 44), f"{u['area']}", font=serif(64), fill=INK)
        dr.text((x + dr.textlength(str(u["area"]), font=serif(64)) + 8, card_y + 78), "m²", font=sans_sb(24), fill=INK_SOFT)
        for li, line in enumerate(wrap(dr, u["name"], sans_b(27), cw)):
            dr.text((x, card_y + 128 + li * 36), line, font=sans_b(27), fill=INK)
        dr.text((x, card_y + 210), f"{u['count']} adet", font=sans(24), fill=INK_SOFT)
    y += 320 + 260

    # oran çubuğu
    dr.text((M, y), "Projedeki dağılım", font=sans_b(26), fill=INK)
    y += 46
    bar_w = W - 2 * M
    x = M
    seg_colors = [SAPPHIRE, LOGO_BLUE, LOGO_MID, LOGO_BRIGHT]
    for i, u in enumerate(UNITS):
        seg = round(bar_w * u["count"] / TOTAL)
        dr.rectangle([x, y, x + seg, y + 26], fill=seg_colors[i])
        x += seg
    y += 56
    for i, u in enumerate(UNITS):
        cx = M + (i % 4) * ((W - 2 * M) // 4)
        dr.ellipse([cx, y + 9, cx + 20, y + 29], fill=seg_colors[i])
        dr.text((cx + 34, y), f"{u['name']}", font=sans_sb(23), fill=INK)
        dr.text((cx + 34, y + 32), f"{u['count']} adet", font=sans(21), fill=INK_SOFT)
    y += 110

    note = rounded((W - 2 * M, 96), 24, (*MIST, 255))
    page.alpha_composite(note, (M, y))
    dr.text((W / 2, y + 30), "Tüm daireler 60 aya varan sıfır faiz ödeme imkânıyla. Kefil yok, banka yok, faiz yok.",
            font=sans_sb(26), fill=LOGO_BLUE, anchor="ma")
    y += 140

    rest = H - y - 150
    if rest > 200:
        page.alpha_composite(photo("entrance-gate.webp", (W - 2 * M, rest), 28), (M, y))
    return page


def page_unit(u, page_no):
    page, dr = base_page(u["name"], page_no)
    y = eyebrow(dr, 250, f"{u['name']} · {u['area']} m²")
    for li, line in enumerate(wrap(dr, u["tagline"], serif(76), W - 2 * M - 420)):
        dr.text((M, y + li * 88), line, font=serif(76), fill=INK)
        y_end = y + li * 88
    y = y_end + 130

    # m² rozeti
    chip_w = 330
    chip = rounded((chip_w, 108), 26, WHITE)
    ImageDraw.Draw(chip).rounded_rectangle([0, 0, chip_w - 1, 107], radius=26, outline=(*LOGO_BRIGHT, 200), width=3)
    page.alpha_composite(chip, (W - M - chip_w, 262))
    dr.text((W - M - chip_w / 2, 282), f"{u['area']},00 m²", font=sans_b(38), fill=LOGO_BLUE, anchor="ma")
    dr.text((W - M - chip_w / 2, 224), "BRÜT ALAN", font=sans_b(18), fill=INK_SOFT, anchor="ma")

    y = para(dr, (M, y), u["text"], sans(30), INK_SOFT, W - 2 * M, 48) + 30

    page.alpha_composite(photo(u["img"], (int((W - 2 * M) * 0.6), 620), 28), (M, y))
    right_x = M + int((W - 2 * M) * 0.6) + 26
    right_w = W - M - right_x
    page.alpha_composite(photo(u["img2"], (right_w, 300), 28), (right_x, y))
    page.alpha_composite(photo(u["plan"], (right_w, 294), 28), (right_x, y + 326))
    y += 690

    dr.text((M, y), "Öne çıkanlar", font=sans_b(30), fill=INK)
    y += 56
    cw = (W - 2 * M - 40) // 2
    for i, feat in enumerate(u["features"]):
        x = M + (i % 2) * (cw + 40)
        yy = y + (i // 2) * 86
        dr.ellipse([x, yy + 10, x + 20, yy + 30], fill=LOGO_BRIGHT)
        dr.text((x + 38, yy), feat, font=sans_sb(27), fill=INK)
    y += 200

    strip = rounded((W - 2 * M, 110), 26, (*MIST, 255))
    page.alpha_composite(strip, (M, y))
    dr.text((M + 40, y + 34), f"Projede {u['count']} adet", font=sans_b(28), fill=INK)
    dr.text((W - M - 40, y + 34), "60 ay vade · %0 faiz · kefilsiz", font=sans_sb(26), fill=LOGO_BLUE, anchor="ra")
    y += 150

    # Kalan alanı proje görseliyle kapat
    rest = H - y - 150
    if rest > 200:
        page.alpha_composite(photo(u.get("wide", "facade-warm.webp"), (W - 2 * M, rest), 28), (M, y))
    return page


def page_social():
    page, dr = base_page("Sosyal Yaşam", 9)
    y = eyebrow(dr, 250, "Sosyal Yaşam")
    dr.text((M, y), "Her gün tatil konforu", font=serif(84), fill=INK)
    y += 120
    y = para(dr, (M, y), "Kapalı yüzme havuzundan Türk hamamına, çocuk oyun parkından merkezi avluya; "
                         "MİA PARK OCEAN size her gün ayrıcalıklı bir deneyim sunar.",
             sans(30), INK_SOFT, W - 2 * M, 48) + 30

    page.alpha_composite(photo("courtyard-pools.webp", (W - 2 * M, 620), 28), (M, y))
    y += 680

    cw = (W - 2 * M - 2 * 26) // 3
    for i, a in enumerate(AMENITIES):
        x = M + (i % 3) * (cw + 26)
        yy = y + (i // 3) * 118
        card = rounded((cw, 100), 22, WHITE)
        ImageDraw.Draw(card).rounded_rectangle([0, 0, cw - 1, 99], radius=22, outline=(*ICE, 255), width=2)
        page.alpha_composite(card, (x, yy))
        dr.ellipse([x + 28, yy + 42, x + 44, yy + 58], fill=LOGO_BRIGHT)
        for li, line in enumerate(wrap(dr, a, sans_sb(24), cw - 90)[:2]):
            dr.text((x + 62, yy + (26 if len(wrap(dr, a, sans_sb(24), cw - 90)) > 1 else 36) + li * 32), line,
                    font=sans_sb(24), fill=INK)
    return page


def page_location():
    page, dr = base_page("Lokasyon & İletişim", 10)
    y = eyebrow(dr, 250, "Lokasyon")
    for li, line in enumerate(wrap(dr, "İzmit'in mükemmel konumu", serif(72), W - 2 * M - 660)):
        dr.text((M, y + li * 84), line, font=serif(72), fill=INK)
    y += 84 * len(wrap(dr, "İzmit'in mükemmel konumu", serif(72), W - 2 * M - 660)) + 24
    y = para(dr, (M, y), "MİA PARK OCEAN, İzmit'in en değerli gelişim aksı MİA Bölgesi'nde. Üniversite, "
                         "şehir hastanesi, AVM'ler ve ana yollar dakikalar içinde.",
             sans(30), INK_SOFT, W - 2 * M - 620, 48) + 20

    cw = (W - 2 * M - 620 - 26)
    for i, (place, t) in enumerate(DISTANCES):
        x = M + (i % 2) * ((cw + 26) // 2)
        yy = y + (i // 2) * 92
        dr.text((x, yy), t, font=serif(46), fill=LOGO_BLUE)
        dr.text((x, yy + 52), place, font=sans(24), fill=INK_SOFT)
    page.alpha_composite(photo("street-corner.webp", (600, 560), 28), (W - M - 600, 300))
    y += 4 * 92 + 40

    page.alpha_composite(photo("balcony-dusk.webp", (W - 2 * M, 420), 28), (M, y))
    y += 480

    # iletişim bandı
    band_h = H - y - 150
    band = gradient((W - 2 * M, band_h))
    band.putalpha(Image.new("L", (W - 2 * M, band_h), 255))
    mask = Image.new("L", (W - 2 * M, band_h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, W - 2 * M - 1, band_h - 1], radius=32, fill=255)
    band.putalpha(mask)
    page.alpha_composite(band, (M, y))

    tx = M + 56
    track(dr, (tx, y + 46), "İLETİŞİM", sans_b(20), LOGO_LIGHT, 5)
    dr.text((tx, y + 90), PROJECT["phones"], font=sans_b(36), fill=WHITE)
    dr.text((tx, y + 146), PROJECT["site"], font=sans_sb(30), fill=(*LOGO_LIGHT, 255))
    for li, line in enumerate(wrap(dr, PROJECT["address"], sans(23), W - 2 * M - 560)):
        dr.text((tx, y + 200 + li * 34), line, font=sans(23), fill=(*ICE, 255))

    # Koyu zeminde logo beyaz durur — plaket yok
    lg = logo_img(320, on_dark=True)
    page.alpha_composite(lg, (W - M - lg.width - 66, y + (band_h - lg.height) // 2))

    dr.text((tx, y + band_h - 60), f"Yapımcı: {PROJECT['developer']}", font=sans(21), fill=(*LOGO_LIGHT, 220))
    dr.text((tx, y + band_h - 30), f"Tek Yetkili Satıcı: {PROJECT['seller']}", font=sans(21), fill=(*LOGO_LIGHT, 220))
    return page


# ---------------------------------------------------------------- ana akış
def main() -> None:
    labels = ["Kapak", "Proje", "Finansman", "Daire Tipleri",
              UNITS[0]["name"], UNITS[1]["name"], UNITS[2]["name"], UNITS[3]["name"],
              "Sosyal Yaşam", "Lokasyon & İletişim"]

    print("Sayfalar üretiliyor…")
    pages = [
        page_cover(), page_project(), page_finance(), page_unit_overview(),
        page_unit(UNITS[0], 5), page_unit(UNITS[1], 6), page_unit(UNITS[2], 7), page_unit(UNITS[3], 8),
        page_social(), page_location(),
    ]

    rgb = [p.convert("RGB") for p in pages]
    pdf = os.path.join(ROOT, "public", "mia-park-ocean-katalog.pdf")
    rgb[0].save(pdf, save_all=True, append_images=rgb[1:], resolution=200.0)
    print(f"  PDF: {os.path.getsize(pdf)//1024} KB · {len(rgb)} sayfa")

    for i, im in enumerate(rgb, 1):
        big = im.resize((1600, round(1600 * im.height / im.width)), Image.LANCZOS)
        big.save(os.path.join(IMG, f"catalog-{i}.webp"), quality=86, method=6)
        big.resize((800, big.height // 2), Image.LANCZOS).save(
            os.path.join(IMG, f"catalog-{i}-sm.webp"), quality=84, method=6)
        print(f"  catalog-{i}.webp  {labels[i-1]}")


if __name__ == "__main__":
    main()
