#!/usr/bin/env python3
"""
MİA PARK OCEAN — SESLİ kampanya reeli (1080x1920, ~42 sn).

Instagram'daki emlak kampanya reelleri gibi: sinematik çekimler üzerine
Türkçe seslendirme, seslendirmeyle senkron büyük yazılar, kampanya
çipleri ve müzik. Çekimler filmle ortak (film-source/clips), tipografi
Instagram kimliği (Fraunces + Manrope), motor build-reels ile ortak.

Seslendirme: film-source/ses/vo-1..7.wav (ElevenLabs, önceden üretildi).
Sahne süreleri seslendirme satırlarının ölçülen uzunluğundan türetilir;
her satır sahnenin VO_GIRIS'inci saniyesinde başlar.

    python3 scripts/build-reklam-reel.py            # tam üretim
    python3 scripts/build-reklam-reel.py --onizle   # sahne başı 1 kare JPEG
"""

from __future__ import annotations

import math
import os
import subprocess
import sys
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import importlib.util as _il

_KOK = os.path.dirname(os.path.abspath(__file__))


def _yukle(ad: str, dosya: str):
    spec = _il.spec_from_file_location(ad, os.path.join(_KOK, dosya))
    m = _il.module_from_spec(spec)
    sys.modules[ad] = m
    spec.loader.exec_module(m)
    return m


bf = _yukle("build_film", "build-film.py")
br = _yukle("build_reels", "build-reels.py")

ROOT = bf.ROOT
SES = os.path.join(ROOT, "film-source", "ses")
OUT = os.path.join(ROOT, "sosyal-medya", "turkuaz-kampanya")

W, H = br.W, br.H
FPS = bf.FPS
SR = 44100
XFADE = br.XFADE
SAFE_X = br.SAFE_X
WORD_Y = br.WORD_Y
CAP_Y = br.CAP_Y

WHITE = (255, 255, 255)
MIA_ICE = br.MIA_ICE
KIRMIZI = (204, 32, 44)

VO_GIRIS = 0.45          # seslendirme sahne başladıktan bu kadar sonra girer


def vo_sure(i: int) -> float:
    with wave.open(os.path.join(SES, f"vo-{i}.wav")) as w:
        return w.getnframes() / w.getframerate()


# ---------------------------------------------------------------- overlay
def _cip(dr, cx, cy, metin, f, dolgu=KIRMIZI, yazi=WHITE, pad_x=30, pad_y=16, r=18):
    tw = dr.textlength(metin, font=f)
    th = f.size
    dr.rounded_rectangle([cx - tw / 2 - pad_x, cy - th / 2 - pad_y,
                          cx + tw / 2 + pad_x, cy + th / 2 + pad_y],
                         radius=r, fill=dolgu)
    dr.text((cx, cy - th * 0.06), metin, font=f, fill=yazi, anchor="mm")
    return tw + 2 * pad_x


def sahne_soz(klip, soz, cap, pan=(0.5, 0.5), zoom=(1.0, 1.06),
              offset=0.0, speed=1.0):
    """build-reels.vshot ile aynı dil — kelime + tracked alt başlık."""
    return br.vshot(klip, soz, cap, pan=pan, zoom=zoom, offset=offset, speed=speed)


def sahne_yoklar(klip, pan=(0.40, 0.60), speed=1.0):
    """Dört kırmızı YOK çipi sırayla düşer."""
    CIPLER = ["BANKA YOK", "FAİZ YOK", "KREDİ YOK", "ARA ÖDEME YOK"]

    def scene(t, d):
        k = min(max(t / d, 0.0), 1.0)
        im = br.clip_frame_smooth(klip, t, speed, 0.0)
        im = br.vcrop(im, pan[0] + (pan[1] - pan[0]) * k, 1.0 + 0.06 * k)
        im = br.grade(im)
        im = Image.alpha_composite(im.convert("RGBA"), br.scrim()).convert("RGB")

        o = bf.fade(t, d, 0.4, 0.45)

        def boya(dr):
            f = br.sans(56, "700")
            y0 = WORD_Y - 3 * 118
            for i, c in enumerate(CIPLER):
                ct = (t - (0.55 + i * 0.30)) / 0.45      # çipin kendi zamanı
                if ct <= 0:
                    continue
                e = bf.ease_out(min(ct, 1.0))
                dus = round((1 - e) * 42)
                _cip(dr, W / 2, y0 + i * 118 + dus, c, f)
            br.track(dr, (W / 2, CAP_Y + 66), "TASARRUFA DAYALI FİNANSMAN",
                     br.sans(33, "600"), (*MIA_ICE, 246), 9, "ma")

        im = br.with_shadow(im, br.text_layer(boya), opacity=o)
        return br.brandmark(im)
    return scene


def sahne_fiyat(klip, tip, ayda, altsatir, pan, speed=0.85):
    """Fiyat sahnesi — 'Ayda X TL' kahraman, üstte tip, altta koşullar."""
    def scene(t, d):
        k = min(max(t / d, 0.0), 1.0)
        im = br.clip_frame_smooth(klip, t, speed, 0.0)
        im = br.vcrop(im, pan[0] + (pan[1] - pan[0]) * k, 1.0 + 0.06 * k)
        im = br.grade(im)
        im = Image.alpha_composite(im.convert("RGBA"), br.scrim()).convert("RGB")

        o = bf.fade(t, d, 0.55, 0.45)
        rise = round((1 - bf.ease_out(min(t / 0.7, 1.0))) * 26)

        def boya(dr):
            br.track(dr, (SAFE_X, WORD_Y - 236 + rise), tip,
                     br.sans(37, "700"), (*MIA_ICE, 250), 10)
            f = br.serif(124, "600")
            while dr.textlength(ayda, font=f) > W - SAFE_X * 2 - 60:
                f = br.serif(f.size - 4, "600")
            dr.text((SAFE_X, WORD_Y + rise), ayda, font=f, fill=WHITE, anchor="ls")
            fa = br.sans(37, "600")
            while dr.textlength(altsatir, font=fa) > W - SAFE_X * 2 - 40:
                fa = br.sans(fa.size - 2, "600")
            dr.text((SAFE_X, CAP_Y + 10 + rise), altsatir, font=fa,
                    fill=(*MIA_ICE, 248), anchor="la")

        im = br.with_shadow(im, br.text_layer(boya), opacity=o)
        return br.brandmark(im)
    return scene


def sahne_60ay(klip, pan=(0.42, 0.58), speed=1.0):
    """Dev kırmızı '60 AY SABİT TAKSİT!' çipi — vuruşla büyüyerek gelir."""
    def scene(t, d):
        k = min(max(t / d, 0.0), 1.0)
        im = br.clip_frame_smooth(klip, t, speed, 0.0)
        im = br.vcrop(im, pan[0] + (pan[1] - pan[0]) * k, 1.0 + 0.06 * k)
        im = br.grade(im)
        im = Image.alpha_composite(im.convert("RGBA"), br.scrim()).convert("RGB")

        o = bf.fade(t, d, 0.35, 0.4)
        e = bf.ease_out(min(t / 0.55, 1.0))
        olcek = 0.78 + 0.22 * e

        kat = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        kd = ImageDraw.Draw(kat)
        fs = br.serif(int(168 * olcek), "600")
        kd.text((W / 2, 1210), "60 ay", font=fs, fill=WHITE, anchor="ms")
        _cip(kd, W / 2, 1300, "SABİT TAKSİT!", br.sans(int(64 * olcek), "700"),
             pad_x=36, pad_y=20, r=22)
        br.track(kd, (W / 2, CAP_Y + 66), "KUR FARKI YOK · SÜRPRİZ YOK",
                 br.sans(33, "600"), (*MIA_ICE, 246), 9, "ma")

        im = br.with_shadow(im, kat, opacity=o)
        return br.brandmark(im)
    return scene


def sahne_kapanis(klip, offset=0.0, speed=0.85):
    """Kapanış kartı: logo, gece bandı, TEK YETKİLİ SATIŞ + telefon + web."""
    BAND_H = round(W * 9 / 16)

    def scene(t, d):
        base = bf.brand_bg(t, d, drift=0.9).resize((W, H), Image.LANCZOS).convert("RGBA")
        base.alpha_composite(br.glow_v(W * 0.5, 620, 900, br.MIA_CYAN, 0.22))

        band = br.clip_frame_smooth(klip, t, speed, offset).resize((W, BAND_H), Image.LANCZOS)
        band = br.grade(band, teal=0.10, bloom=0.10)
        by = 640
        base.alpha_composite(band.convert("RGBA"), (0, by))
        d2 = ImageDraw.Draw(base)
        d2.rectangle([0, by - 3, W, by], fill=(*br.MIA_AQUA, 190))
        d2.rectangle([0, by + BAND_H, W, by + BAND_H + 3], fill=(*br.MIA_AQUA, 190))

        o = bf.fade(t, d, 0.6, 0.4)
        kat = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        lg = bf.logo_white(600)
        kat.alpha_composite(lg, ((W - lg.width) // 2, 180))
        dr = ImageDraw.Draw(kat)
        br.track(dr, (W / 2, 1284), "TEK YETKİLİ SATIŞ", br.sans(29, "700"),
                 (*MIA_ICE, 240), 11, "ma")
        pm = bf.partner_white(225)
        kat.alpha_composite(pm, ((W - pm.width) // 2, 1352))
        dr.text((W / 2, 1556), "0540 028 00 41", font=br.serif(92, "600"),
                fill=WHITE, anchor="ms")
        br.track(dr, (W / 2, 1614), "miaparkocean.com · @miaparkocean",
                 br.sans(33, "600"), (*MIA_ICE, 244), 6, "ma")
        if o < 1:
            kat.putalpha(kat.split()[3].point(lambda v: int(v * o)))
        return br.with_shadow(base.convert("RGB"), kat, blur=16, boost=1.2)
    return scene


# ---------------------------------------------------------------- kurgu
def kurgu():
    v = [vo_sure(i) for i in range(1, 8)]
    # sahne süresi: giriş payı + seslendirme + nefes payı
    dur = [VO_GIRIS + s + p for s, p in zip(
        v, [0.85, 0.55, 0.55, 0.45, 0.55, 0.45, 1.35])]

    sahneler = [
        (sahne_soz("13-giris-drone", "Kocaeli ev sahibi oluyor!",
                   "MİA PARK OCEAN · İZMİT MİA BÖLGESİ",
                   pan=(0.62, 0.42), zoom=(1.08, 1.0)), dur[0]),
        (sahne_yoklar("08-cephe-yukselis"), dur[1]),
        (sahne_fiyat("09-daire-1plus0", "1+0 STÜDYO DAİRELER",
                     "Ayda 29.900 TL", "699.000 TL PEŞİNAT · 60 AY SABİT TAKSİT",
                     pan=(0.44, 0.56)), dur[2]),
        (sahne_fiyat("10-daire-1plus1", "1+1 DAİRELER",
                     "Ayda 39.900 TL", "999.000 TL PEŞİNAT · 60 AY SABİT TAKSİT",
                     pan=(0.56, 0.44)), dur[3]),
        (sahne_60ay("06-teras-sosyal"), dur[4]),
        (sahne_soz("03-havadan-yorunge", "Sahile iki dakika",
                   "İZMİT MİA BÖLGESİ · D100'E 1 DAKİKA",
                   pan=(0.38, 0.62), zoom=(1.0, 1.08)), dur[5]),
        (sahne_kapanis("14-gece-yaklasim", offset=1.0), dur[6]),
    ]
    return sahneler, v


# ---------------------------------------------------------------- ses
def _oku(p):
    with wave.open(p) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
        if w.getnchannels() == 2:
            a = a.reshape(-1, 2).mean(axis=1)
        if w.getframerate() != SR:
            raise SystemExit(f"örnekleme {w.getframerate()} != {SR}: {p}")
    return a


def _kayan_ort(x, n):
    c = np.cumsum(np.concatenate([[0.0], x]))
    y = (c[n:] - c[:-n]) / n
    return np.concatenate([np.full(n // 2, y[0]), y,
                           np.full(len(x) - len(y) - n // 2, y[-1])])


def ses_miksi(yol, sahneler, starts, toplam):
    N = int(toplam * SR)
    voice = np.zeros(N, np.float32)
    for i, s in enumerate(starts):
        a = _oku(os.path.join(SES, f"vo-{i + 1}.wav"))
        j = int((s + VO_GIRIS) * SR)
        voice[j:j + len(a)] += a[:max(0, N - j)]
    voice *= 0.95 / max(np.abs(voice).max(), 1e-6)

    skor = os.path.join(SES, "_skor.wav")
    bf.write_score(skor, toplam)
    m = _oku(skor)
    m = m[:N] if len(m) >= N else np.concatenate([m, np.zeros(N - len(m), np.float32)])

    # ducking: seslendirme varken müzik kısılır
    zarf = _kayan_ort(np.abs(voice), int(0.16 * SR))
    zarf = np.clip(zarf * 9.0, 0.0, 1.0)
    zarf = _kayan_ort(zarf, int(0.10 * SR))
    muzik = m * (0.66 * (1.0 - 0.60 * zarf))

    mix = muzik + voice
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
    sahneler, v = kurgu()
    starts = br.starts_of(sahneler)
    toplam = br.duration_of(sahneler)
    print(f"  seslendirme: {sum(v):.1f} sn · video: {toplam:.1f} sn")

    if "--onizle" in sys.argv:
        oz = os.path.join(OUT, "reel-onizleme")
        os.makedirs(oz, exist_ok=True)
        for i, s in enumerate(starts):
            d = sahneler[i][1]
            br.frame_at(s + min(1.6, d * 0.55), sahneler, starts).save(
                os.path.join(oz, f"sahne-{i + 1}.jpg"), quality=88)
        print(f"  önizleme → {oz}")
        return

    mikswav = os.path.join(SES, "_miks.wav")
    ses_miksi(mikswav, sahneler, starts, toplam)

    yol = os.path.join(OUT, "reel-kampanya-sesli.mp4")
    cmd = [bf.FF, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-i", mikswav,
           "-c:v", "libx264", "-preset", "medium", "-crf", "21",
           "-pix_fmt", "yuv420p", "-profile:v", "high", "-movflags", "+faststart",
           "-c:a", "aac", "-b:a", "160k", "-shortest", yol]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
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
