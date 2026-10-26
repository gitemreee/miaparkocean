#!/usr/bin/env python3
"""
Render → "çekilmiş fotoğraf" işleme (yapay zekâ servisi kullanmadan, yalnızca PIL/numpy).

Her kare: 8K render'dan 9:16 dikey kadraj → kamera karakteri:
  ton eğrisi (hafif kalkık siyahlar, yumuşak tepe), beyaz dengesi, render yeşillerini bastırma,
  ışık taşması (halation), hafif lens yumuşaklığı + kamera keskinleştirmesi, kromatik sapma,
  vinyet, luminans greni.

    python3.13 scripts/foto-isleme.py
"""

import os

import numpy as np
from PIL import Image, ImageFilter

Image.MAX_IMAGE_PIXELS = None
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "sosyal-medya", "bitmis-fotograflar")
CW, CH = 1536, 2752                          # setin diğer kareleriyle aynı ölçü

# ad: (kaynak, kadraj merkezi x (0-1), kadraj yüksekliği oranı (0-1), dikey merkez (0-1), ayarlar)
KARELER = {
    "22-uzaktan-teleobjektif": ("signage-source/4k/orta-giris-genis-8k.png", "UZAK", (0.05, 0.66), None,
                                dict(sicak=0.010, doygunluk=0.92, gren=0.020, vinyet=0.18, ca=1.2, pus=0.04)),
    "23-giris-avlu-gun-batimi": ("signage-source/4k/sag-giris-havuz-aksam-8k.png", 0.36, 1.0, 0.5,
                                 dict(sicak=0.006, doygunluk=0.92, gren=0.024, vinyet=0.26, ca=1.6, pus=0.0)),
}


def uzak_kadraj(im, x_aralik):
    """Tüm siteyi genişlikte sığdır, üstte doğal gökyüzünü uzat (reklam yazısı için boşluk)."""
    W, H = im.size
    x0, x1 = int(x_aralik[0] * W), int(x_aralik[1] * W)
    kenar = int(H * 0.012)                                               # render'ın üst kenar satırlarını at
    parca = im.crop((x0, kenar, x1, H))
    yh = int(CW * (H - kenar) / (x1 - x0))
    parca = parca.resize((CW, yh), Image.LANCZOS)
    a = np.asarray(parca).astype(np.float32)
    # üst 60 satırın sütun ortalaması → yatayda çok yumuşat (düz gökyüzü rengi)
    ust = a[10:70].mean(axis=0)
    ust_img = Image.fromarray(np.clip(ust[None].repeat(8, 0), 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(80))
    ust = np.asarray(ust_img).astype(np.float32)[4]
    gok_h = CH - yh
    t = np.linspace(1, 0, gok_h, dtype=np.float32)[:, None, None]       # 1 = en üst
    hedef = np.array([92, 140, 204], np.float32)                         # zenit mavisi
    gok = ust[None] * (1 - t ** 1.4) + (ust[None] * 0.45 + hedef * 0.55) * t ** 1.4
    # dikiş: render'ın üst 220 satırını düz gökyüzü rengiyle harmanla (çizgi kalmasın)
    n = 220
    w = (np.linspace(0, 1, n, dtype=np.float32) ** 1.5)[:, None, None]
    a[:n] = a[:n] * w + ust[None] * (1 - w)
    tam = np.concatenate([gok, a], axis=0)
    return Image.fromarray(np.clip(tam, 0, 255).astype(np.uint8))


def kadraj(im, cx, h_oran, cy):
    W, H = im.size
    ch = int(H * h_oran)
    cw = int(ch * CW / CH)
    if cw > W:
        cw = W
        ch = int(cw * CH / CW)
    x0 = int(min(max(cx * W - cw / 2, 0), W - cw))
    y0 = int(min(max(cy * H - ch / 2, 0), H - ch))
    return im.crop((x0, y0, x0 + cw, y0 + ch)).resize((CW, CH), Image.LANCZOS)


def fotograf(im, sicak, doygunluk, gren, vinyet, ca, pus, tohum=7):
    rng = np.random.default_rng(tohum)
    a = np.asarray(im.convert("RGB")).astype(np.float32) / 255.0
    h, w, _ = a.shape

    # 1) render yeşil/camgöbeği doygunluğunu bastır, genel doygunluk
    lum = (0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2])[..., None]
    yesil = np.clip((a[..., 1] - np.maximum(a[..., 0], a[..., 2])) * 4, 0, 1)[..., None]
    d = doygunluk - 0.10 * yesil
    a = lum + (a - lum) * d

    # 2) beyaz dengesi (sıcak), hafif pus (uzak kadrajda atmosfer)
    a[..., 0] *= 1 + sicak
    a[..., 2] *= 1 - sicak
    if pus:
        yy = np.linspace(1, 0, h, dtype=np.float32)[:, None, None]   # üst kısım daha puslu
        a = a * (1 - pus * yy) + np.array([0.80, 0.84, 0.90], np.float32) * pus * yy

    # 3) ton eğrisi: siyahları çok hafif kaldır, hafif S, tepeyi yumuşat (film omzu)
    a = 0.012 + 0.985 * a
    a = a + 0.06 * np.sin((a - 0.5) * np.pi) * (1 - np.abs(2 * a - 1))
    a = np.where(a > 0.88, 0.88 + (a - 0.88) * 0.75, a)

    # 4) halation / ışık taşması
    img = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))
    parlak = np.clip((a - 0.86) / 0.14, 0, 1)
    p_img = Image.fromarray((parlak * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(18))
    p = np.asarray(p_img).astype(np.float32) / 255.0
    a = np.clip(a + p * np.array([0.06, 0.04, 0.02], np.float32), 0, 1)

    # 5) lens yumuşaklığı + kamera keskinleştirmesi (render'ın aşırı keskin kenarlarını kır)
    img = Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7))
    img = img.filter(ImageFilter.UnsharpMask(radius=1.6, percent=55, threshold=2))
    a = np.asarray(img).astype(np.float32) / 255.0

    # 6) kromatik sapma: kenarlara doğru R dışarı, B içeri
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    cx, cy = w / 2, h / 2
    rx, ry = (xx - cx) / cx, (yy - cy) / cy
    def kaydir(kanal, s):
        sx = np.clip(xx + rx * s, 0, w - 1).astype(np.int32)
        sy = np.clip(yy + ry * s, 0, h - 1).astype(np.int32)
        return kanal[sy, sx]
    a[..., 0] = kaydir(a[..., 0], ca)
    a[..., 2] = kaydir(a[..., 2], -ca)

    # 7) vinyet (yumuşak, oval)
    r2 = (rx ** 2) * 0.85 + (ry ** 2) * 0.6
    a *= (1 - vinyet * np.clip(r2, 0, 1.4) ** 1.6)[..., None]

    # 8) gren: luminans ağırlıklı, gölgede biraz daha fazla
    g = rng.normal(0, 1, (h, w)).astype(np.float32)
    g = np.asarray(Image.fromarray(((g * 0.25 + 0.5).clip(0, 1) * 255).astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(0.6))).astype(np.float32) / 255.0 - 0.5
    lum = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    a += (g * gren * 4 * (1.2 - 0.6 * lum))[..., None]

    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))


def main():
    os.makedirs(OUT, exist_ok=True)
    for ad, (src, cx, h_oran, cy, ayar) in KARELER.items():
        im = Image.open(os.path.join(ROOT, src)).convert("RGB")
        k = uzak_kadraj(im, h_oran) if cx == "UZAK" else kadraj(im, cx, h_oran, cy)
        f = fotograf(k, **ayar)
        yol = os.path.join(OUT, ad + ".jpg")
        f.save(yol, quality=92, subsampling=0)
        print("  →", os.path.relpath(yol, ROOT), f.size)


if __name__ == "__main__":
    main()
