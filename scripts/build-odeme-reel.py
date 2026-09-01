#!/usr/bin/env python3
"""
MİA PARK OCEAN — Taksit ve ödeme planı reeli (1080x1920, ~37 sn, sesli).

Kurgu:
  1. Kampanya görseli (şafak hero) + KOCAELİ EV SAHİBİ OLUYOR!   [vo-1]
  2. 1+0 ödeme kartı — peşinat / aylık taksit / vade, satırlar
     sırayla düşer                                               [vo-3]
  3. 1+1 ödeme kartı                                             [vo-4]
  4. YOK çipleri + dev 60 AY SABİT TAKSİT!                       [vo-2, vo-5]
  5. Kapanış kartı: logolar, telefon, web                        [vo-7]

Seslendirmeler film-source/ses/vo-*.wav'dan (kampanya reeliyle ortak),
müzik film skorundan; seslendirme girince müzik kısılır.

    python3 scripts/build-odeme-reel.py            # tam üretim
    python3 scripts/build-odeme-reel.py --onizle   # sahne başı kare
"""

from __future__ import annotations

import os
import subprocess
import sys
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import importlib.util as _il

_KOK = os.path.dirname(os.path.abspath(__file__))


def _yukle(ad, dosya):
    spec = _il.spec_from_file_location(ad, os.path.join(_KOK, dosya))
    m = _il.module_from_spec(spec)
    sys.modules[ad] = m
    spec.loader.exec_module(m)
    return m


bf = _yukle("build_film", "build-film.py")
br = _yukle("build_reels", "build-reels.py")
rr = _yukle("build_reklam_reel", "build-reklam-reel.py")

ROOT = bf.ROOT
SES = os.path.join(ROOT, "film-source", "ses")
OUT = os.path.join(ROOT, "sosyal-medya", "turkuaz-kampanya")
HERO = os.path.join(OUT, "kaynak-safak-hero-story.jpg")

W, H = br.W, br.H
FPS = bf.FPS
SR = 44100

WHITE = (255, 255, 255)
NAVY = (7, 44, 66)
GRI = (86, 118, 138)
MIA_ICE = br.MIA_ICE
KIRMIZI = rr.KIRMIZI
VO_GIRIS = rr.VO_GIRIS


def vo_sure(i):
    with wave.open(os.path.join(SES, f"vo-{i}.wav")) as w:
        return w.getnframes() / w.getframerate()


# ---------------------------------------------------------------- sahneler
_HERO: Image.Image | None = None


def sahne_giris():
    """Şafak kampanya görseli üzerinde yavaş zoom + slogan."""
    def scene(t, d):
        global _HERO
        if _HERO is None:
            _HERO = Image.open(HERO).convert("RGB")
        k = min(max(t / d, 0.0), 1.0)
        z = 1.0 + 0.09 * k
        sw, sh = _HERO.size
        s = max(W / sw, H / sh) * z
        im = _HERO.resize((round(sw * s), round(sh * s)), Image.BILINEAR)
        x = (im.width - W) // 2
        y = int((im.height - H) * 0.42)
        im = im.crop((x, y, x + W, y + H))
        im = Image.alpha_composite(im.convert("RGBA"), br.scrim()).convert("RGB")

        o = bf.fade(t, d, 0.4, 0.45)
        rise = round((1 - bf.ease_out(min(t / 0.7, 1.0))) * 26)

        def boya(dr):
            f, lines = br.fit_lines(dr, "Kocaeli ev sahibi oluyor!", 116,
                                    W - br.SAFE_X * 2 - 60)
            lh = round(f.size * 1.16)
            top = br.WORD_Y - lh * (len(lines) - 1)
            for i, ln in enumerate(lines):
                dr.text((br.SAFE_X, top + i * lh + rise), ln, font=f,
                        fill=WHITE, anchor="ls")
            br.track(dr, (br.SAFE_X, br.CAP_Y + rise), "MİA PARK OCEAN ÖDEME PLANI",
                     br.sans(34, "600"), (*MIA_ICE, 246), 9)

        im = br.with_shadow(im, br.text_layer(boya), opacity=o)
        return br.brandmark(im)
    return scene


def sahne_kart(klip, baslik, pesinat, taksit, pan, speed=0.85):
    """Ödeme planı kartı: satırlar sırayla belirir."""
    def scene(t, d):
        k = min(max(t / d, 0.0), 1.0)
        im = br.clip_frame_smooth(klip, t, speed, 0.0)
        im = br.vcrop(im, pan[0] + (pan[1] - pan[0]) * k, 1.0 + 0.06 * k)
        im = br.grade(im)
        # kart pop
        e = bf.ease_out(min(t / 0.55, 1.0))
        o = bf.fade(t, d, 0.4, 0.45)

        KW, KH = 860, 810
        kart = Image.new("RGBA", (KW, KH), (0, 0, 0, 0))
        kd = ImageDraw.Draw(kart)
        kd.rounded_rectangle([0, 0, KW, KH], radius=36,
                             fill=(255, 255, 255, 246))
        kd.rounded_rectangle([0, 0, KW, 128], radius=36, fill=NAVY + (255,))
        kd.rectangle([0, 64, KW, 128], fill=NAVY + (255,))
        kd.text((KW / 2, 64), baslik, font=br.sans(46, "700"), fill=WHITE,
                anchor="mm")

        satirlar = [("PEŞİNAT", pesinat, 0.55),
                    ("AYLIK TAKSİT", taksit, 0.95),
                    ("VADE", "60 AY", 1.35)]
        y = 208
        for etiket, deger, gecikme in satirlar:
            ct = (t - gecikme) / 0.4
            if ct > 0:
                ce = bf.ease_out(min(ct, 1.0))
                dus = round((1 - ce) * 26)
                al = int(255 * min(ct * 1.6, 1.0))
                kd.text((KW / 2, y + dus - 26), etiket,
                        font=br.sans(31, "700"), fill=GRI + (al,), anchor="mm")
                kd.text((KW / 2, y + dus + 44), deger,
                        font=br.serif(96, "600"), fill=NAVY + (al,),
                        anchor="mm")
            y += 178
        ct = (t - 1.75) / 0.45
        if ct > 0:
            ce = bf.ease_out(min(ct, 1.0))
            al = int(255 * min(ct * 1.6, 1.0))
            f = br.sans(40, "700")
            tw = kd.textlength("60 AY SABİT TAKSİT!", font=f)
            cx, cy2 = KW / 2, KH - 92 + round((1 - ce) * 22)
            kd.rounded_rectangle([cx - tw / 2 - 30, cy2 - 40,
                                  cx + tw / 2 + 30, cy2 + 40], radius=18,
                                 fill=(*KIRMIZI, al))
            kd.text((cx, cy2 - 2), "60 AY SABİT TAKSİT!", font=f,
                    fill=(255, 255, 255, al), anchor="mm")

        olcek = 0.94 + 0.06 * e
        kw2, kh2 = round(KW * olcek), round(KH * olcek)
        kart = kart.resize((kw2, kh2), Image.LANCZOS)
        if o < 1:
            kart.putalpha(kart.split()[3].point(lambda v: int(v * o)))

        base = im.convert("RGBA")
        kx, ky = (W - kw2) // 2, round(560 - (kh2 - KH) / 2)
        g = kart.filter(ImageFilter.GaussianBlur(18))
        golge = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        r, gg, b, a = g.split()
        golge.paste(Image.merge("RGBA", (
            r.point(lambda v: 4), gg.point(lambda v: 20),
            b.point(lambda v: 32), a.point(lambda v: int(v * 0.6)))),
            (kx + 2, ky + 12))
        base.alpha_composite(golge)
        base.alpha_composite(kart, (kx, ky))
        return br.brandmark(base.convert("RGB"))
    return scene


def sahne_yok60(klip, pan=(0.42, 0.58), t5_bas=6.9):
    """Dört YOK çipi + t5_bas'tan sonra dev 60 AY SABİT TAKSİT!"""
    CIPLER = ["BANKA YOK", "FAİZ YOK", "KREDİ YOK", "ARA ÖDEME YOK"]

    def scene(t, d):
        k = min(max(t / d, 0.0), 1.0)
        im = br.clip_frame_smooth(klip, t, 0.85, 0.0)
        im = br.vcrop(im, pan[0] + (pan[1] - pan[0]) * k, 1.0 + 0.06 * k)
        im = br.grade(im)
        im = Image.alpha_composite(im.convert("RGBA"), br.scrim()).convert("RGB")

        o = bf.fade(t, d, 0.4, 0.45)
        kat = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        kd = ImageDraw.Draw(kat)
        if t < t5_bas:
            f = br.sans(56, "700")
            y0 = br.WORD_Y - 3 * 118
            for i, c in enumerate(CIPLER):
                ct = (t - (0.55 + i * 0.55)) / 0.45
                if ct <= 0:
                    continue
                ce = bf.ease_out(min(ct, 1.0))
                dus = round((1 - ce) * 42)
                rr._cip(kd, W / 2, y0 + i * 118 + dus, c, f)
        else:
            ct = (t - t5_bas) / 0.5
            ce = bf.ease_out(min(ct, 1.0))
            olcek = 0.8 + 0.2 * ce
            fs = br.serif(int(170 * olcek), "600")
            kd.text((W / 2, 1204), "60 ay", font=fs, fill=WHITE, anchor="ms")
            rr._cip(kd, W / 2, 1298, "SABİT TAKSİT!",
                    br.sans(int(64 * olcek), "700"), pad_x=36, pad_y=20, r=22)
        im = br.with_shadow(im, kat, opacity=o)
        return br.brandmark(im)
    return scene


# ---------------------------------------------------------------- kurgu
def kurgu():
    v = {i: vo_sure(i) for i in (1, 2, 3, 4, 5, 7)}
    d1 = VO_GIRIS + v[1] + 0.85
    d2 = VO_GIRIS + v[3] + 0.55
    d3 = VO_GIRIS + v[4] + 0.45
    ara45 = 0.35
    d4 = VO_GIRIS + v[2] + ara45 + v[5] + 0.5
    d5 = VO_GIRIS + v[7] + 1.35
    t5_bas = VO_GIRIS + v[2] + ara45 - 0.15   # 60 ay vurgusunun başladığı an

    sahneler = [
        (sahne_giris(), d1),
        (sahne_kart("09-daire-1plus0", "1+0 STÜDYO DAİRELER",
                    "699.000 TL", "29.900 TL", pan=(0.44, 0.56)), d2),
        (sahne_kart("10-daire-1plus1", "1+1 DAİRELER",
                    "999.000 TL", "39.900 TL", pan=(0.56, 0.44)), d3),
        (sahne_yok60("08-cephe-yukselis", t5_bas=t5_bas), d4),
        (rr.sahne_kapanis("14-gece-yaklasim", offset=1.0), d5),
    ]
    # seslendirme yerleşimi: (dosya, sahne_indexi, sahne içi gecikme)
    yerlesim = [(1, 0, VO_GIRIS), (3, 1, VO_GIRIS), (4, 2, VO_GIRIS),
                (2, 3, VO_GIRIS), (5, 3, VO_GIRIS + v[2] + ara45),
                (7, 4, VO_GIRIS)]
    return sahneler, yerlesim


# ---------------------------------------------------------------- ses
def _oku(p):
    with wave.open(p) as w:
        a = np.frombuffer(w.readframes(w.getnframes()),
                          np.int16).astype(np.float32) / 32768
        if w.getnchannels() == 2:
            a = a.reshape(-1, 2).mean(axis=1)
    return a


def ses_miksi(yol, yerler, toplam):
    N = int(toplam * SR)
    voice = np.zeros(N, np.float32)
    for bas, dosya in yerler:
        a = _oku(dosya)
        j = int(bas * SR)
        n = min(len(a), N - j)
        if n > 0:
            voice[j:j + n] += a[:n]
    voice *= 0.95 / max(np.abs(voice).max(), 1e-6)

    skor = os.path.join(SES, "_skor2.wav")
    bf.write_score(skor, toplam)
    m = _oku(skor)
    m = m[:N] if len(m) >= N else np.concatenate(
        [m, np.zeros(N - len(m), np.float32)])

    zarf = rr._kayan_ort(np.abs(voice), int(0.16 * SR))
    zarf = np.clip(zarf * 9.0, 0.0, 1.0)
    zarf = rr._kayan_ort(zarf, int(0.10 * SR))
    mix = m * (0.66 * (1.0 - 0.60 * zarf)) + voice
    son = int(0.9 * SR)
    mix[-son:] *= np.linspace(1.0, 0.0, son)
    mix *= 0.97 / max(np.abs(mix).max(), 1e-6)

    st = np.stack([mix, mix], axis=1)
    with wave.open(yol, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((st * 32767).astype(np.int16).tobytes())
    os.remove(skor)


# ---------------------------------------------------------------- üretim
_SC = _ST = None


def _init(sc, st):
    global _SC, _ST
    _SC, _ST = sc, st


def _render(k):
    return br.frame_at(k / FPS, _SC, _ST).tobytes()


def main():
    os.makedirs(OUT, exist_ok=True)
    sahneler, yerlesim = kurgu()
    starts = br.starts_of(sahneler)
    toplam = br.duration_of(sahneler)
    print(f"  video: {toplam:.1f} sn")

    if "--onizle" in sys.argv:
        oz = os.path.join(OUT, "odeme-onizleme")
        os.makedirs(oz, exist_ok=True)
        for i, s in enumerate(starts):
            d = sahneler[i][1]
            br.frame_at(s + min(2.2, d * 0.6), sahneler, starts).save(
                os.path.join(oz, f"sahne-{i + 1}.jpg"), quality=88)
        print(f"  önizleme → {oz}")
        return

    yerler = [(starts[si] + gecikme, os.path.join(SES, f"vo-{vi}.wav"))
              for vi, si, gecikme in yerlesim]
    mikswav = os.path.join(SES, "_miks2.wav")
    ses_miksi(mikswav, yerler, toplam)

    yol = os.path.join(OUT, "reel-odeme-plani.mp4")
    cmd = [bf.FF, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", mikswav,
           "-c:v", "libx264", "-preset", "medium", "-crf", "21",
           "-pix_fmt", "yuv420p", "-profile:v", "high",
           "-movflags", "+faststart", "-c:a", "aac", "-b:a", "160k",
           "-shortest", yol]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
    total = int(toplam * FPS)
    import multiprocessing as mp
    with mp.Pool(max(1, min(4, os.cpu_count() or 2)),
                 initializer=_init, initargs=(sahneler, starts)) as pool:
        for k, buf in enumerate(pool.imap(_render, range(total), chunksize=6)):
            proc.stdin.write(buf)
            if k % 250 == 0:
                print(f"    kare {k}/{total}")
    proc.stdin.close()
    proc.wait()
    os.remove(mikswav)
    print(f"  → {yol} · {os.path.getsize(yol) / 1048576:.1f} MB")


if __name__ == "__main__":
    main()
