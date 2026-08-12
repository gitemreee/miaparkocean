#!/usr/bin/env python3
"""MİA PARK OCEAN — lansman baskı/paylaşım varlıkları.

Üretilenler (public/etkinlik/):
    davetiye-karti.png        1080x1350  WhatsApp / Instagram davetiyesi
    davetiye-karti-story.png  1080x1920  Instagram story
    masa-qr-davetiye.png      A5 300dpi  masaya konulacak davetiye/RSVP etiketi
    masa-qr-basin.png         A5 300dpi  masaya konulacak basın açıklaması etiketi
    qr-davetiye.png / .svg    tekil QR
    qr-basin.png / .svg       tekil QR

Kimlik: beyaz zemin · Sapphire/Emerald gradyan · logodaki dalga.
Logo hiçbir yerde renklendirilmez, daima beyaz zemindedir.

Kullanım:
    pip install pillow numpy segno
    python scripts/build-event-assets.py
"""

from __future__ import annotations

import os

import numpy as np
import segno
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "brand-source", "fonts")
BRAND = os.path.join(ROOT, "public", "brand")
OUT = os.path.join(ROOT, "public", "etkinlik")

# --- Palet (globals.css ile birebir) ---
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
MIDNIGHT = (6, 64, 90)
SAPPHIRE = MIA_DEEP
LOGO_BLUE = MIA_DEEP
LOGO_MID = MIA_DARK
LOGO_BRIGHT = MIA_CYAN
LOGO_LIGHT = MIA_LIGHT
ICE = MIA_PALE
POWDER = MIA_LIGHT
WHITE = (255, 255, 255)
INK = (4, 40, 58)

# Metalik geçiş: koyu petrol → okyanus → buz mavisi
BRAND_STOPS = [(0.0, NAVY), (0.22, MIDNIGHT), (0.5, MIA_DEEP), (0.76, MIA_DARK), (1.0, MIA_OCEAN)]

# --- Etkinlik bilgisi (src/data/event.ts ile aynı) ---
EVENT = {
    "kicker": "DAVETLİSİNİZ",
    "name": "Lansman & Basın Toplantısı",
    "project": "MİA PARK OCEAN",
    "region": "İZMİT MİA BÖLGESİ",
    "date": "21 Ağustos 2026",
    "day": "Cuma",
    "time": "10:00",
    "venue": "Emex Otel",
    "city": "KOCAELİ",
    "host": "Gül Hanım",
    "phone": "0534 859 26 72",
    "site": "miaparkocean.com",
}
QR_DAVETIYE = "https://miaparkocean.com/davetiye/"
QR_BASIN = "https://miaparkocean.com/basin-aciklamasi/"

# Dalga: logodan birebir kesilmiş varlıklar (scripts/build-wave.py üretir).
# Baskı çıktıları da sitedeki dalganın AYNISINI kullanır.
WAVE_MASK_PNG = os.path.join(ROOT, "public", "brand", "wave-mask.png")
WAVE_PNG = os.path.join(ROOT, "public", "brand", "wave.png")


# --------------------------------------------------------------------------
# Yardımcılar
# --------------------------------------------------------------------------
def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(os.path.join(FONTS, name), size)


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


def wave_shape(width: int, height: int, flip: bool = False) -> Image.Image:
    """Logodaki dalganın dolgulu maskesi (L kanalı), istenen boyutta."""
    m = Image.open(WAVE_MASK_PNG).convert("RGBA").split()[3]
    m = m.resize((width, height), Image.LANCZOS)
    return m.transpose(Image.FLIP_TOP_BOTTOM) if flip else m


def wave_layer(width: int, height: int, color, opacity: float = 1.0, flip: bool = False) -> Image.Image:
    """Dalgayı düz bir renkle boyar."""
    img = Image.new("RGBA", (width, height), (*color, 255))
    mask = wave_shape(width, height, flip)
    img.putalpha(Image.eval(mask, lambda v: int(v * opacity)))
    return img


def wave_stack(width: int, height: int, colors=(ICE, (243, 248, 252), WHITE), flip: bool = False) -> Image.Image:
    """Aynı dalganın üç katmanı — logodaki kurdele derinliğini verir."""
    layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    offsets = (int(height * 0.22), int(height * 0.11), 0)
    for c, o, dy in zip(colors, (0.5, 0.85, 1.0), offsets):
        piece = wave_layer(width, height, c, o, flip)
        layer.alpha_composite(piece, (0, dy) if not flip else (0, 0))
    return layer


def wave_band(width: int, wave_h: int, band_h: int) -> Image.Image:
    """Üst kenarı logodaki dalga olan gradyan bant (sayfanın altına oturur)."""
    total = wave_h + band_h
    out = Image.new("RGBA", (width, total), (0, 0, 0, 0))
    grad = gradient((width, total))

    for opacity, offset in ((0.45, 0), (0.7, int(wave_h * 0.12)), (1.0, int(wave_h * 0.26))):
        mask = Image.new("L", (width, total), 0)
        mask.paste(wave_shape(width, wave_h), (0, offset))
        ImageDraw.Draw(mask).rectangle([0, wave_h + offset, width, total], fill=255)
        layer = grad.copy()
        layer.putalpha(Image.eval(mask, lambda v: int(v * opacity)))
        out.alpha_composite(layer)
    return out


def rounded_mask(size, radius: int) -> Image.Image:
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], radius=radius, fill=255)
    return m


def paste_rounded(base: Image.Image, img: Image.Image, xy, radius: int) -> None:
    img = img.copy()
    img.putalpha(rounded_mask(img.size, radius))
    base.alpha_composite(img, xy)


def text(draw, xy, s, f, fill, anchor="mm", spacing: float = 0.0):
    """Harf aralıklı metin (PIL'de tracking yok, elle uygulanır)."""
    if spacing == 0:
        draw.text(xy, s, font=f, fill=fill, anchor=anchor)
        return
    widths = [draw.textlength(ch, font=f) for ch in s]
    total = sum(widths) + spacing * (len(s) - 1)
    x = xy[0] - total / 2 if anchor[0] == "m" else xy[0]
    for ch, w in zip(s, widths):
        draw.text((x, xy[1]), ch, font=f, fill=fill, anchor="l" + anchor[1])
        x += w + spacing


def logo(width: int) -> Image.Image:
    im = Image.open(os.path.join(BRAND, "logo-ocean-trim.png")).convert("RGBA")
    h = round(im.height * width / im.width)
    return im.resize((width, h), Image.LANCZOS)


def ocean_logo(width: int) -> Image.Image | None:
    p = os.path.join(ROOT, "public", "ocean-logo.webp")
    if not os.path.exists(p):
        return None
    im = Image.open(p).convert("RGBA")
    # Beyaz zeminli logo: beyaz plakete oturacağı için olduğu gibi kullanılır
    h = round(im.height * width / im.width)
    return im.resize((width, h), Image.LANCZOS)


def qr_image(data: str, px: int, dark=NAVY, light=WHITE, border: int = 2) -> Image.Image:
    """Yüksek hata düzeltmeli (H) QR — baskıda güvenli."""
    q = segno.make(data, error="h")
    scale = max(1, px // (q.symbol_size(border=border)[0]))
    buf = os.path.join(OUT, ".tmp-qr.png")
    q.save(buf, scale=scale, border=border, dark="#%02x%02x%02x" % dark, light="#%02x%02x%02x" % light)
    im = Image.open(buf).convert("RGBA").resize((px, px), Image.NEAREST)
    os.remove(buf)
    return im


# --------------------------------------------------------------------------
# 1. Davetiye kartı
# --------------------------------------------------------------------------
def invitation_card(size=(1080, 1350), with_qr: bool = True, name: str = "davetiye-karti") -> None:
    """Davetiye kartı — bloklar ölçülüp kalan boşluğa eşit dağıtılır, böylece
    aynı düzen hem 4:5 hem story oranında dengeli çıkar."""
    W, H = size
    s = W / 1080
    card = Image.new("RGBA", (W, H), WHITE)
    dr = ImageDraw.Draw(card)

    # --- Üst gradyan bant + dalga ---
    band_h = int(H * (0.30 if H / W < 1.5 else 0.26))
    card.alpha_composite(gradient((W, band_h)), (0, 0))
    wave_h = int(96 * s)
    card.alpha_composite(wave_stack(W, wave_h), (0, band_h - wave_h))

    f_kicker = font("Manrope-700.ttf", int(30 * s))
    f_event = font("Fraunces-500.ttf", int(58 * s))
    top_area = band_h - wave_h
    text(dr, (W / 2, top_area * 0.30), EVENT["kicker"], f_kicker, ICE, anchor="mm", spacing=int(11 * s))
    dr.text((W / 2, top_area * 0.52), EVENT["name"], font=f_event, fill=WHITE, anchor="ma")
    line = gradient((int(150 * s), int(5 * s)), [(0.0, LOGO_BRIGHT), (0.5, ICE), (1.0, LOGO_BRIGHT)], angle=1.0)
    paste_rounded(card, line, (int(W / 2 - 75 * s), int(top_area * 0.52 + 78 * s)), int(3 * s))

    # --- Ölçüler: içerik yüksekliği u ile doğrusal, kalan alana göre çözülür ---
    strip_h = int(16 * s)
    content_top = band_h - wave_h + int(26 * s)
    content_bottom = H - strip_h - int(30 * s)
    available = content_bottom - content_top
    min_gap = 20 * s

    logo_ratio = 822 / 1200
    ol_probe = ocean_logo(int(230 * s))
    ol_ratio = (ol_probe.height / ol_probe.width) if ol_probe else 0.22

    # u = 1 iken blokların toplam yüksekliği
    unit = (
        400 * s * logo_ratio           # logo
        + 292 * s                      # tarih kutusu
        + 96 * s                       # iletişim
        + ((196 + 36 + 46) * s if with_qr else 0)  # QR + açıklama
        + 34 * s + 230 * s * ol_ratio + 52 * s     # alt blok
    )
    n_blocks = 5 if with_qr else 4
    u = min(1.0, max(0.62, (available - min_gap * (n_blocks - 1)) / unit))
    k = s * u  # içerik ölçeği

    lg = logo(int(400 * k))
    box_w, box_h = int(W - 150 * s), int(292 * k)
    contact_h = int(96 * k)
    qr_px = int(196 * k)
    qr_block = (qr_px + int(36 * k) + int(46 * k)) if with_qr else 0
    ol = ocean_logo(int(230 * k))
    foot_h = int(34 * k) + (ol.height if ol else int(46 * k)) + int(52 * k)

    blocks = [lg.height, box_h, contact_h] + ([qr_block] if with_qr else []) + [foot_h]
    gap = max(int(min_gap), (available - sum(blocks)) // (len(blocks) - 1))

    y = content_top

    # --- Logo (beyaz zeminde) ---
    card.alpha_composite(lg, (int((W - lg.width) / 2), y))
    y += lg.height + gap

    # --- Tarih / saat kartı ---
    box_x = int(75 * s)
    box = Image.new("RGBA", (box_w, box_h), (243, 248, 252, 255))
    ImageDraw.Draw(box).rounded_rectangle(
        [0, 0, box_w - 1, box_h - 1], radius=int(28 * k), outline=(*POWDER, 150), width=max(2, int(2 * s))
    )
    card.alpha_composite(box, (box_x, y))

    f_date = font("Fraunces-500.ttf", int(64 * k))
    f_sub = font("Manrope-600.ttf", int(28 * k))
    f_venue = font("Fraunces-500.ttf", int(42 * k))
    f_city = font("Manrope-700.ttf", int(23 * k))

    dr.text((W / 2, y + int(44 * k)), EVENT["date"], font=f_date, fill=SAPPHIRE, anchor="ma")
    dr.text((W / 2, y + int(122 * k)), f"{EVENT['day']} · Saat {EVENT['time']}", font=f_sub, fill=(74, 91, 125), anchor="ma")
    dr.line(
        [box_x + int(90 * k), y + int(176 * k), box_x + box_w - int(90 * k), y + int(176 * k)],
        fill=(*POWDER, 160),
        width=max(2, int(2 * s)),
    )
    dr.text((W / 2, y + int(196 * k)), EVENT["venue"], font=f_venue, fill=INK, anchor="ma")
    text(dr, (W / 2, y + int(262 * k)), EVENT["city"], f_city, (74, 91, 125), anchor="mm", spacing=int(7 * k))
    y += box_h + gap

    # --- İletişim ---
    f_lbl = font("Manrope-700.ttf", int(22 * k))
    f_val = font("Manrope-600.ttf", int(32 * k))
    text(dr, (W / 2, y + int(12 * k)), "İLETİŞİM", f_lbl, LOGO_BLUE, anchor="mm", spacing=int(6 * k))
    dr.text((W / 2, y + int(38 * k)), f"{EVENT['host']} · {EVENT['phone']}", font=f_val, fill=INK, anchor="ma")
    y += contact_h + gap

    # --- QR ---
    if with_qr:
        plate_pad = int(18 * k)
        plate = Image.new("RGBA", (qr_px + plate_pad * 2, qr_px + plate_pad * 2), WHITE)
        plate.alpha_composite(qr_image(QR_DAVETIYE, qr_px, dark=NAVY), (plate_pad, plate_pad))
        ImageDraw.Draw(plate).rounded_rectangle(
            [0, 0, plate.width - 1, plate.height - 1], radius=int(20 * k), outline=(*POWDER, 170), width=max(2, int(2 * s))
        )
        card.alpha_composite(plate, (int((W - plate.width) / 2), y))
        f_qr = font("Manrope-600.ttf", int(22 * k))
        dr.text(
            (W / 2, y + plate.height + int(14 * k)),
            "Katılım bildirimi için kodu okutun",
            font=f_qr,
            fill=(74, 91, 125),
            anchor="ma",
        )
        y += qr_block + gap

    # --- Alt: Ocean Gayrimenkul + site ---
    text(dr, (W / 2, y + int(10 * k)), "TEK YETKİLİ SATICI", f_lbl, (74, 91, 125), anchor="mm", spacing=int(6 * k))
    y += int(34 * k)
    if ol:
        card.alpha_composite(ol, (int((W - ol.width) / 2), y))
        y += ol.height
    else:
        y += int(46 * k)
    f_site = font("Manrope-700.ttf", int(30 * k))
    dr.text((W / 2, y + int(14 * k)), EVENT["site"], font=f_site, fill=SAPPHIRE, anchor="ma")

    # --- Alt gradyan şerit ---
    card.alpha_composite(gradient((W, strip_h), angle=1.0), (0, H - strip_h))

    card.convert("RGB").save(os.path.join(OUT, f"{name}.png"), optimize=True)
    print(f"  {name}.png: {W}x{H}")


# --------------------------------------------------------------------------
# 2. Masa QR etiketi (A5, 300 dpi)
# --------------------------------------------------------------------------
def table_card(target: str, headline: str, caption: str, name: str, size=(1748, 2480)) -> None:
    W, H = size
    s = W / 1748
    card = Image.new("RGBA", (W, H), WHITE)

    # Üst gradyan bant + dalga
    band_h = int(H * 0.26)
    card.alpha_composite(gradient((W, band_h)), (0, 0))
    wave_h = int(150 * s)
    card.alpha_composite(wave_stack(W, wave_h), (0, band_h - wave_h))

    dr = ImageDraw.Draw(card)
    f_head = font("Fraunces-500.ttf", int(84 * s))
    f_kick = font("Manrope-700.ttf", int(34 * s))
    text(dr, (W / 2, int(120 * s)), EVENT["region"], f_kick, ICE, spacing=int(13 * s))
    dr.text((W / 2, int(200 * s)), headline, font=f_head, fill=WHITE, anchor="ma")

    # --- Ölçüler: bloklar ölçülür, kalan boşluk eşit dağıtılır ---
    base_h = int(230 * s)               # alt gradyan taban
    base_wave_h = int(120 * s)          # tabana geçiş dalgası
    content_top = band_h - wave_h + int(40 * s)
    # Alt dalga içeriğin üstünü örtmesin: taban + dalga yüksekliği düşülür
    content_bottom = H - base_h - base_wave_h - 20 * s
    available = content_bottom - content_top
    min_gap = 26 * s

    logo_ratio = 822 / 1200
    ol_probe = ocean_logo(int(360 * s))
    ol_ratio = (ol_probe.height / ol_probe.width) if ol_probe else 0.22

    # u = 1 iken toplam blok yüksekliği
    unit = (
        620 * s * logo_ratio                                  # logo
        + 44 * s + (360 * s * ol_ratio + 40 * s)              # satıcı etiketi + plaket
        + (760 + 56 * 2 + 14) * s                             # QR çerçevesi
        + 56 * s                                              # açıklama
        + 62 * s                                              # site adresi
    )
    u = min(1.0, max(0.6, (available - min_gap * 4) / unit))
    k = s * u

    # Logo
    lg = logo(int(620 * k))
    y = content_top
    card.alpha_composite(lg, (int((W - lg.width) / 2), y))
    blocks_h = lg.height

    f_lbl = font("Manrope-700.ttf", int(30 * k))
    ol = ocean_logo(int(360 * k))
    seller_h = int(44 * k) + (ol.height + int(40 * k) if ol else int(90 * k))

    qr_px = int(760 * k)
    pad = int(56 * k)
    frame_side = qr_px + pad * 2 + int(14 * k)

    f_cap = font("Manrope-600.ttf", int(38 * k))
    f_site = font("Manrope-700.ttf", int(48 * k))
    cap_h, site_h = int(56 * k), int(62 * k)

    blocks = [lg.height, seller_h, frame_side, cap_h, site_h]
    gap = max(int(min_gap), int((available - sum(blocks)) / (len(blocks) - 1)))

    y += lg.height + gap

    # Tek yetkili satıcı
    text(dr, (W / 2, y + int(10 * k)), "TEK YETKİLİ SATICI", f_lbl, (74, 91, 125), anchor="mm", spacing=int(9 * k))
    if ol:
        plate = Image.new("RGBA", (ol.width + int(56 * k), ol.height + int(40 * k)), WHITE)
        plate.alpha_composite(ol, (int(28 * k), int(20 * k)))
        ImageDraw.Draw(plate).rounded_rectangle(
            [0, 0, plate.width - 1, plate.height - 1], radius=int(18 * k), outline=(*POWDER, 150), width=max(2, int(2 * s))
        )
        card.alpha_composite(plate, (int((W - plate.width) / 2), y + int(44 * k)))
    y += seller_h + gap

    # QR — gradyan çerçeveli beyaz plaket
    frame = gradient((frame_side, frame_side))
    frame.putalpha(rounded_mask(frame.size, int(46 * k)))
    inner = Image.new("RGBA", (qr_px + pad * 2, qr_px + pad * 2), WHITE)
    inner.alpha_composite(qr_image(target, qr_px, dark=NAVY), (pad, pad))
    inner.putalpha(rounded_mask(inner.size, int(40 * k)))
    frame.alpha_composite(inner, (int(7 * k), int(7 * k)))
    card.alpha_composite(frame, (int((W - frame.width) / 2), y))
    y += frame_side + gap

    # Açıklama + site
    dr.text((W / 2, y), caption, font=f_cap, fill=(36, 54, 92), anchor="ma")
    y += cap_h + gap
    dr.text((W / 2, y), EVENT["site"], font=f_site, fill=SAPPHIRE, anchor="ma")

    # Alt taban: üst kenarı dalga olan gradyan bant
    card.alpha_composite(wave_band(W, base_wave_h, base_h), (0, H - base_h - base_wave_h))

    f_foot = font("Manrope-600.ttf", int(32 * s))
    dr.text(
        (W / 2, H - int(134 * s)),
        f"{EVENT['date']} · {EVENT['time']} · {EVENT['venue']}, Kocaeli",
        font=f_foot,
        fill=ICE,
        anchor="ma",
    )
    f_host = font("Manrope-600.ttf", int(30 * s))
    dr.text((W / 2, H - int(80 * s)), f"{EVENT['host']} · {EVENT['phone']}", font=f_host, fill=POWDER, anchor="ma")

    card.convert("RGB").save(os.path.join(OUT, f"{name}.png"), dpi=(300, 300), optimize=True)
    print(f"  {name}.png: {W}x{H} (A5 · 300 dpi)")


def main() -> None:
    os.makedirs(OUT, exist_ok=True)

    print("Tekil QR kodları…")
    for label, url in (("davetiye", QR_DAVETIYE), ("basin", QR_BASIN)):
        q = segno.make(url, error="h")
        q.save(os.path.join(OUT, f"qr-{label}.svg"), scale=10, border=2, dark="#000926", light="#ffffff")
        q.save(os.path.join(OUT, f"qr-{label}.png"), scale=20, border=2, dark="#000926", light="#ffffff")
        print(f"  qr-{label}.svg / .png")

    print("Davetiye kartları…")
    invitation_card((1080, 1350), with_qr=True, name="davetiye-karti")
    invitation_card((1080, 1920), with_qr=True, name="davetiye-karti-story")

    print("Masa QR etiketleri…")
    table_card(QR_DAVETIYE, "Davetiye", "Davetiye ve katılım bildirimi için kodu okutun", "masa-qr-davetiye")
    table_card(QR_BASIN, "Basın Açıklaması", "Basın açıklamasını okumak için kodu okutun", "masa-qr-basin")


if __name__ == "__main__":
    main()
