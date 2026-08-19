#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FİYAT AVANTAJI roll-up — Higgsfield çıktısını baskıya hazırlar.

Tasarımın kendisi Higgsfield (nano_banana_pro) ile üretiliyor; istemler
tabela/fiyat-rollup/PROMPT.md dosyasında, kaynak PNG'ler signage-source/hf/
altında duruyor (~80 MB, git'e girmiyor).

Betiğin üç işi var:

1.  ORAN.  Üretim 3072x5504 (9:16) geliyor, roll-up 100x200 cm yani 1:2.
    Eksik 640 px üstteki gradyanı ekstrapole ederek (440) ve alttaki düz
    künye bandını uzatarak (200) kapanıyor. Hiçbir tasarım öğesi
    esnetilmiyor, kırpılmıyor.
2.  MARKA.  Logo üretimi yapay zekâya bırakılmıyor — istemde "hiçbir logo
    çizme" denip künyenin köşeleri boş bırakıldı. Gerçek MİA PARK OCEAN
    kilidi üstteki yeni banda, OCEAN GAYRİMENKUL imzası alttakine
    basılıyor; üretimin bıraktığı yer tutucu bloklar kendi bant rengiyle
    kapatılıyor. Böylece üretilen tipografiyle hiç çakışmıyoruz.
3.  ÖLÇEK.  Depodaki diğer roll-up'larla aynı: 100 dpi, 3937x7874 px.
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "signage-source", "hf")
BRAND = os.path.join(ROOT, "public", "brand")
FONTS = os.path.join(ROOT, "brand-source", "fonts")
OUT = os.path.join(ROOT, "tabela", "fiyat-rollup")
PREVIEW = os.path.join(OUT, "onizleme")

W_MM, H_MM, DPI = 1000, 2000, 100
W_PX, H_PX = round(W_MM / 25.4 * DPI), round(H_MM / 25.4 * DPI)

ADD_TOP, ADD_BOT = 440, 200          # 3072x5504 -> 3072x6144 (1:2)
SELLER, SELLER_ROLE = "OCEAN GAYRİMENKUL", "TEK YETKİLİ SATICI"

# Her sanat yönü iki kez üretiliyor: rakamlı ve rakamsız. Fiyatsız sürüm
# rakam yerine m² ve vade gösterip aramaya yönlendiriyor.
DESIGNS = [
    ("hf-0-gunduz-a",           "fiyat-rollup-gunduz-1"),
    ("hf-1-gunduz-b",           "fiyat-rollup-gunduz-2"),
    ("hf-2-gece-a",             "fiyat-rollup-gece-1"),
    ("hf-3-gece-b",             "fiyat-rollup-gece-2"),
    ("hf-10-gunduz-a-fiyatsiz", "fiyat-rollup-gunduz-1-fiyatsiz"),
    ("hf-11-gunduz-b-fiyatsiz", "fiyat-rollup-gunduz-2-fiyatsiz"),
    ("hf-12-gece-a-fiyatsiz",   "fiyat-rollup-gece-1-fiyatsiz"),
    ("hf-13-gece-b-fiyatsiz",   "fiyat-rollup-gece-2-fiyatsiz"),
]


# ------------------------------------------------------------------ ölçüm
def bar_top(a: np.ndarray, bar: np.ndarray, tol: float = 10.0) -> int:
    """Künye bandının üst kenarı.

    Ölçüt satır ortalaması ya da medyanı değil, BANT RENGİNDEKİ PİKSEL
    ORANI. Ortalamayı künyedeki beyaz yazı 60 birim kaydırıyordu; medyanı
    ise bazı üretimlerin künyeye koyduğu iki büyük açık panel satırın tam
    yarısını kaplayıp bir aşağı bir yukarı zıplatıyordu. Oran ikisinden de
    etkilenmiyor: bandın içinde her satırda bol miktarda bant rengi var,
    fotoğrafta hiç yok.

    İki geçiş: önce %10 eşiğiyle bandın kaba sınırı bulunuyor (panellerin
    ve yazının seyrelttiği satırlar da içeride kalsın diye gevşek), sonra
    aşağı yürüyüp ilk tam dolu satıra oturuluyor — üstteki ince altın
    çizgi ya da yumuşak geçiş bandın dışında bırakılıyor.
    """
    frac = (np.abs(a - bar).max(axis=2) < tol).mean(axis=1)
    y = a.shape[0] - 1
    while y > 0 and frac[y - 1] > 0.10:                # bandın kaba sınırı
        y -= 1
    while y < a.shape[0] - 1 and frac[y] < 0.85:       # ilk tam dolu satır
        y += 1
    return y


def placeholder_cols(band: np.ndarray, bar: np.ndarray) -> tuple[int, int]:
    """Künyedeki yer tutucu blokların bittiği sütunlar (sol, sağ).

    Ayırt edici ölçü DOLULUK: yer tutucu bant boyunca uzanan dolu bir
    kutu, yazı ise sütun başına bandın küçük bir dilimi. Doluluğu 0,5'i
    aşan en dıştaki sütunu bulup kenara kadar temizliyoruz — böylece
    ince köşe çerçevelerinin yatay kolları da içeride kalıyor.
    """
    w = band.shape[1]
    cov = (np.abs(band - bar).max(axis=2) > 24).mean(axis=0)
    lim = round(w * 0.25)
    left = np.where(cov[:lim] > 0.5)[0]
    right = np.where(cov[w - lim:] > 0.5)[0]
    pad = round(w * 0.012)
    # İnce köşe çerçeveleri doluluk eşiğini geçmiyor; künye yazısı hiçbir
    # tasarımda dış %13'e girmediği için (en genişi %15'te başlıyor) o
    # şerit her hâlükârda siliniyor.
    base = round(w * 0.13)
    return (max(base, int(left.max()) + pad if left.size else 0),
            min(w - base, w - lim + int(right.min()) - pad if right.size else w))


# ------------------------------------------------------------------ uzatma
def smooth1d(m: np.ndarray, k: int, passes: int = 3) -> np.ndarray:
    """Sütun ekseninde kutu filtresi — üç geçiş Gauss'a yeterince yakın.

    PIL'in Gauss'u tek satırlık "F" görüntüde çalışmıyor, katsayıları
    numpy ile yumuşatıyoruz. Kenarlar 'edge' ile doldurularak sol/sağ uçta
    renk kaymıyor.
    """
    for _ in range(passes):
        pad = np.pad(m, ((k // 2, k // 2), (0, 0)), mode="edge")
        c = np.cumsum(pad, axis=0)
        m = (c[k:] - c[:-k]) / k
    return m


def extend_top(im: Image.Image, n: int, fit: int = 300, damp: float = 0.6) -> Image.Image:
    """Üstteki gradyanı sütun sütun doğrusal uzat.

    Düz kopyalama gradyanı durdurup görünür bir kuşak bırakıyor. Ham
    en-küçük-kareler ise sütun gürültüsünü de eğim sanıp dikey çizgiler
    üretiyordu; katsayıları yatayda güçlü bulanıklaştırıp (geniş ışık
    dağılımı korunur, piksel gürültüsü gider) eğimi 0,6 ile sönümlüyoruz
    ki gece sürümünde ek bant siyaha koşmasın.
    """
    a = np.asarray(im, np.float32)
    head = a[:fit]
    y = np.arange(fit, dtype=np.float32)
    ym, xm = y.mean(), head.mean(axis=0)
    s = ((y - ym)[:, None, None] * (head - xm)).sum(axis=0) / ((y - ym) ** 2).sum()
    c0 = xm - s * ym

    s = smooth1d(s, 81) * damp
    c0 = smooth1d(c0, 81)

    j = np.arange(-n, 0, dtype=np.float32)[:, None, None]
    ext = np.clip(c0 + s * j, 0, 255)

    # Üretimde ince bir gren var; ek bant pürüzsüz kalırsa dikişte doku
    # farkı okunuyor. Kaynaktaki grenin şiddetini ölçüp aynısını veriyoruz.
    sigma = float(np.median(np.abs(head - head.mean(axis=0))))
    ext += np.random.default_rng(7).normal(0, max(sigma, 0.6), ext.shape)

    top = Image.fromarray(np.clip(ext, 0, 255).astype(np.uint8), "RGB")
    out = Image.new("RGB", (im.width, im.height + n))
    out.paste(top, (0, 0))
    out.paste(im, (0, n))
    return out


# ------------------------------------------------------------------- marka
def lockup(width: int, white: bool) -> Image.Image:
    """MİA PARK OCEAN kilidi — alttaki 'İZMİT MİA BÖLGESİ' satırı olmadan.

    Konumu zaten künyede ve tekrarı istenmedi. Alfa satır toplamındaki son
    uzun boşluktan, yani şeridin hemen üstünden kesiyoruz.
    """
    name = "logo-ocean-white.png" if white else "logo-ocean-trim.png"
    im = Image.open(os.path.join(BRAND, name)).convert("RGBA")
    im = im.crop(im.getbbox())
    a = np.asarray(im.split()[3], np.float32).sum(axis=1)
    rows = np.where(a > a.max() * 0.02)[0]
    gaps = [(p, r) for p, r in zip(rows[:-1], rows[1:]) if r - p > 6]
    if gaps:
        im = im.crop((0, 0, im.width, gaps[-1][0] + 1))
    return im.resize((width, round(width * im.height / im.width)), Image.LANCZOS)


def font(name: str, px: int, w=None):
    f = ImageFont.truetype(os.path.join(FONTS, name), px)
    if w is not None:
        try:
            f.set_variation_by_axes([w])
        except Exception:
            pass
    return f


def track(dr, xy, text: str, f, fill, sp: int, anchor: str = "la") -> None:
    ws = [dr.textlength(c, font=f) for c in text]
    x, y = xy
    total = sum(ws) + sp * max(len(text) - 1, 0)
    x -= total / 2 if anchor[0] == "m" else (total if anchor[0] == "r" else 0)
    for c, w in zip(text, ws):
        dr.text((x, y), c, font=f, fill=fill)
        x += w + sp


def cap_top(f, cy: float) -> float:
    """Metni ORTASINDAN hizala. PIL üst kenardan yazıyor; büyük harf
    yüksekliğini ölçüp yarısını düşmezsek satır aşağı kayıyor."""
    t, b = f.getbbox("H")[1], f.getbbox("H")[3]
    return cy - (t + b) / 2


# -------------------------------------------------------------------- akış
def build(src: str, name: str) -> None:
    im = Image.open(os.path.join(SRC, src + ".png")).convert("RGB")
    W = im.width
    a = np.asarray(im, np.float32)
    bar = np.median(a[im.height - 8:, round(W * 0.42):round(W * 0.58)], axis=(0, 1))
    top = bar_top(a, bar)
    l, r = placeholder_cols(a[top:], bar)

    im = extend_top(im, ADD_TOP)
    top += ADD_TOP
    ext = Image.new("RGB", (W, im.height + ADD_BOT))
    ext.paste(im, (0, 0))
    ext.paste(im.crop((0, im.height - 1, W, im.height)).resize((W, ADD_BOT)),
              (0, im.height))
    im = ext
    H = im.height

    dr = ImageDraw.Draw(im)
    fill = tuple(int(v) for v in bar)
    # Bandın ilk pikselleri silinmiyor: gece sürümlerinde künyenin üstünde
    # ince bir altın çizgi var, köşeleri tam üstten temizleyince o çizgi
    # iki ucundan kırpılıyordu.
    keep = top + round(W * 0.004)
    dr.rectangle([0, keep, l, H], fill=fill)
    dr.rectangle([r, keep, W, H], fill=fill)

    # Üst bant: proje kilidi. Beyaz mı renkli mi, bandın parlaklığı seçiyor.
    head = np.asarray(im.crop((0, 0, W, ADD_TOP)), np.float32)
    lg = lockup(round(W * 0.185), white=head.mean() < 140)
    im.paste(lg, ((W - lg.width) // 2, (ADD_TOP - lg.height) // 2), lg)

    # Alt bant: satıcı imzası. Üretilen künyeye hiç dokunmuyoruz.
    s = round(ADD_BOT * 0.30)
    f1, f2 = font("Montserrat-var.ttf", s, 700), font("Montserrat-var.ttf",
                                                      round(s * 0.72), 600)
    cy = H - ADD_BOT / 2
    gap = round(W * 0.020)
    w1 = sum(dr.textlength(c, font=f1) for c in SELLER) + round(s * 0.14) * (len(SELLER) - 1)
    w2 = sum(dr.textlength(c, font=f2) for c in SELLER_ROLE) + round(s * 0.22) * (len(SELLER_ROLE) - 1)
    x = (W - (w1 + gap * 2 + w2)) / 2
    track(dr, (x, cap_top(f1, cy)), SELLER, f1, (255, 255, 255, 255), round(s * 0.14))
    dr.rectangle([x + w1 + gap - round(W * 0.001), cy - s * 0.42,
                  x + w1 + gap + round(W * 0.001), cy + s * 0.42],
                 fill=(255, 255, 255, 120))
    track(dr, (x + w1 + gap * 2, cap_top(f2, cy)), SELLER_ROLE, f2,
          (255, 255, 255, 200), round(s * 0.22))

    print(f"  {src}: künye %{(top - ADD_TOP) / (H - ADD_TOP - ADD_BOT) * 100:.1f}, "
          f"yer tutucu sol {l} sağ {W - r}")

    im = im.resize((W_PX, H_PX), Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.4, percent=52, threshold=3))
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(PREVIEW, exist_ok=True)
    im.save(os.path.join(OUT, name + ".jpg"), quality=92, subsampling=0,
            optimize=True, dpi=(DPI, DPI))
    im.resize((im.width // 6, im.height // 6), Image.LANCZOS).save(
        os.path.join(PREVIEW, name + ".jpg"), quality=88, optimize=True)


def main() -> None:
    print(f"FİYAT AVANTAJI roll-up — {W_MM}x{H_MM} mm @ {DPI} dpi ({W_PX}x{H_PX} px)")
    for src, name in DESIGNS:
        build(src, name)
        print(f"  -> {name}.jpg")


if __name__ == "__main__":
    main()
