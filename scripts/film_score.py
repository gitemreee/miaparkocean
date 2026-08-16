#!/usr/bin/env python3
"""
MİA PARK OCEAN tanıtım filmi — müzik yatağı.

Önceki yatak yavaş bir pad'di; sunumda cansız kalıyordu. Bu sürüm tempolu:
davul, yürüyen bas, akor vuruşları ve bölüm geçişlerinde yükselişler var.

YAPI (saniye)
─────────────
  0-14   giriş     · sadece pad + süzülen davul, gerilim
 14-22   yükseliş  · riser, tempo hissi oturur
 22-58   ana bölüm · tam ritim, bas, akor vuruşları
 58-76   ara       · davul seyrelir, melodi öne çıkar
 76-100  ikinci    · tam ritim geri döner, daha parlak
100-116  final     · en yoğun, kapanış vuruşu
116-122  bitiş     · yankı, sönüm

Ayrı dosya, çünkü müziği görüntüden bağımsız test edip değiştirebilelim:
    python3 scripts/film_score.py --dinle 20   → ilk 20 saniyeyi yazar
"""

from __future__ import annotations

import math
import sys
import wave

import numpy as np

SR = 44100
BPM = 100.0
BEAT = 60.0 / BPM          # 0.6 s
BAR = BEAT * 4             # 2.4 s


# ---------------------------------------------------------------- yardımcı
def hz(midi: float) -> float:
    return 440.0 * 2 ** ((midi - 69) / 12.0)


def env_ad(n: int, attack: float, decay: float, curve: float = 2.2) -> np.ndarray:
    """Vuruş zarfı: hızlı çıkış, üstel iniş."""
    a = max(int(SR * attack), 1)
    e = np.zeros(n, np.float32)
    e[:a] = np.linspace(0, 1, a, dtype=np.float32)
    rest = n - a
    if rest > 0:
        e[a:] = np.exp(-np.linspace(0, curve * 6, rest, dtype=np.float32))
    d = int(SR * decay)
    if d < n:
        e[d:] *= np.linspace(1, 0, n - d, dtype=np.float32)
    return e


def place(buf: np.ndarray, sig: np.ndarray, t: float) -> None:
    i = int(SR * t)
    if i >= len(buf) or i < 0:
        return
    k = min(len(sig), len(buf) - i)
    buf[i:i + k] += sig[:k]


# ---------------------------------------------------------------- enstrüman
def kick(dur: float = 0.42) -> np.ndarray:
    n = int(SR * dur)
    t = np.arange(n, dtype=np.float32) / SR
    # frekans süpürmesi: 110 Hz → 45 Hz
    f = 45 + 70 * np.exp(-t * 26)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-t * 7.5)
    click = np.exp(-t * 260) * 0.5
    return (body + click).astype(np.float32) * 0.95


def snare(dur: float = 0.30) -> np.ndarray:
    n = int(SR * dur)
    rng = np.random.default_rng(5)
    noise = rng.normal(0, 1, n).astype(np.float32)
    # bant geçiren yaklaşımı: fark alarak tizleştir, sonra biraz yumuşat
    noise = np.diff(np.concatenate([[0], noise]))
    noise = np.convolve(noise, np.ones(3, np.float32) / 3, mode="same")
    t = np.arange(n, dtype=np.float32) / SR
    tone = np.sin(2 * np.pi * 185 * t) * np.exp(-t * 34) * 0.5
    return (noise * np.exp(-t * 19) * 0.55 + tone).astype(np.float32) * 0.62


def hat(dur: float = 0.075, open_: bool = False) -> np.ndarray:
    n = int(SR * (0.24 if open_ else dur))
    rng = np.random.default_rng(9 if open_ else 3)
    x = rng.normal(0, 1, n).astype(np.float32)
    x = np.diff(np.concatenate([[0], x]))          # tiz
    t = np.arange(n, dtype=np.float32) / SR
    return (x * np.exp(-t * (11 if open_ else 58))).astype(np.float32) * 0.26


def bass(midi: float, dur: float) -> np.ndarray:
    n = int(SR * dur)
    t = np.arange(n, dtype=np.float32) / SR
    f = hz(midi - 12)
    x = np.sin(2 * np.pi * f * t)
    x += 0.35 * np.sin(4 * np.pi * f * t)
    x += 0.18 * np.sign(np.sin(2 * np.pi * f * t))  # gövde
    e = np.minimum(np.linspace(0, 1, n) * 60, 1.0) * np.exp(-t * 2.4)
    return (x * e).astype(np.float32) * 0.34


def stab(notes, dur: float) -> np.ndarray:
    """Akor vuruşu — kısa, parlak, ritmi taşır."""
    n = int(SR * dur)
    t = np.arange(n, dtype=np.float32) / SR
    out = np.zeros(n, np.float32)
    for i, m in enumerate(notes):
        f = hz(m)
        for h, a in ((1, 1.0), (2, 0.5), (3, 0.28), (4, 0.14), (6, 0.07)):
            out += a * np.sin(2 * np.pi * f * h * t + i * 0.6)
    out /= len(notes) * 2.0
    return (out * env_ad(n, 0.006, dur * 0.9, 1.6)).astype(np.float32) * 0.5


def pad(notes, dur: float, bright: float = 1.0) -> np.ndarray:
    n = int(SR * dur)
    t = np.arange(n, dtype=np.float32) / SR
    out = np.zeros(n, np.float32)
    for i, m in enumerate(notes):
        f = hz(m)
        det = 1 + 0.0022 * (i - len(notes) / 2)
        for h, a in ((1, 1.0), (2, 0.44), (3, 0.22 * bright), (4, 0.12 * bright),
                     (5, 0.06 * bright), (6, 0.035 * bright)):
            out += a * np.sin(2 * np.pi * f * h * det * t + h * 0.5 + i)
    out /= len(notes) * 2.3
    a = int(SR * 0.9)
    e = np.ones(n, np.float32)
    e[:a] = np.linspace(0, 1, a) ** 1.6
    r = int(SR * 1.3)
    if r < n:
        e[-r:] *= np.linspace(1, 0, r) ** 1.4
    return (out * e).astype(np.float32) * 0.30


def pluck(midi: float, dur: float) -> np.ndarray:
    """Melodi için kısa, çekilmiş bir ses — üst bölgeyi açık tutar."""
    n = int(SR * dur)
    t = np.arange(n, dtype=np.float32) / SR
    f = hz(midi)
    x = np.sin(2 * np.pi * f * t) + 0.4 * np.sin(4 * np.pi * f * t) \
        + 0.2 * np.sin(6 * np.pi * f * t)
    return (x * env_ad(n, 0.004, dur * 0.8, 2.6)).astype(np.float32) * 0.22


def riser(dur: float) -> np.ndarray:
    """Bölüm geçişi — gürültü süpürmesi + yükselen ton."""
    n = int(SR * dur)
    t = np.arange(n, dtype=np.float32) / SR
    k = t / dur
    rng = np.random.default_rng(21)
    x = rng.normal(0, 1, n).astype(np.float32)
    x = np.diff(np.concatenate([[0], x]))
    sweep = np.sin(2 * np.pi * np.cumsum(220 + 900 * k ** 2) / SR) * 0.35
    return ((x * 0.5 + sweep) * (k ** 2.2)).astype(np.float32) * 0.5


def impact(dur: float = 1.7) -> np.ndarray:
    n = int(SR * dur)
    t = np.arange(n, dtype=np.float32) / SR
    sub = np.sin(2 * np.pi * 42 * t) * np.exp(-t * 2.6)
    rng = np.random.default_rng(33)
    boom = rng.normal(0, 1, n).astype(np.float32) * np.exp(-t * 5.5) * 0.25
    return (sub + boom).astype(np.float32) * 0.75


def reverb(x: np.ndarray, mix: float = 0.26) -> np.ndarray:
    out = np.zeros_like(x)
    for ms, g in ((31.7, 0.72), (43.3, 0.68), (57.1, 0.64)):
        d = int(SR * ms / 1000)
        acc = np.zeros_like(x)
        acc[d:] = x[:-d]
        for _ in range(3):
            nxt = np.zeros_like(acc)
            nxt[d:] = acc[:-d] * g
            acc = nxt
            out += acc
    return x * (1 - mix) + (out / 7.0) * mix


# ---------------------------------------------------------------- beste
# Dm – Bb – F – C · her akor bir ölçü (2.4 sn). Türk kulağına da tanıdık,
# yükselen ve umutlu duran bir döngü.
PROG = [
    (50, [62, 65, 69, 74]),   # Dm
    (46, [58, 62, 65, 70]),   # Bb
    (41, [57, 60, 65, 69]),   # F
    (48, [60, 64, 67, 72]),   # C
]
MELODY = [74, 72, 69, 72, 74, 77, 76, 74, 72, 69, 65, 69, 72, 74, 72, 69]


def build(duration: float) -> np.ndarray:
    n = int(SR * duration)
    drums = np.zeros(n, np.float32)
    lows = np.zeros(n, np.float32)
    mids = np.zeros(n, np.float32)
    highs = np.zeros(n, np.float32)
    fx = np.zeros(n, np.float32)

    # ── bölüm sınırları
    S_RISE, S_MAIN, S_BREAK, S_SECOND, S_FINAL, S_END = 14.0, 22.0, 58.0, 76.0, 100.0, 116.0

    bar_i = 0
    t = 0.0
    while t < duration:
        root, notes = PROG[bar_i % 4]
        full = S_MAIN <= t < S_BREAK or S_SECOND <= t < S_END
        light = S_BREAK <= t < S_SECOND
        intro = t < S_RISE

        # akor yatağı her zaman. Girişte tek başına kaldığı için daha yüksek:
        # ölçümde giriş -39 dBFS çıkıyordu, sunumda duyulmuyordu.
        place(mids, pad(notes, BAR * 1.05, bright=0.6 if intro else 1.0)
              * (2.1 if intro else 1.0), t)
        if intro:
            # girişe gövde veren alçak drone
            ln = int(SR * BAR)
            tt_ = np.arange(ln, dtype=np.float32) / SR
            dr = (np.sin(2 * math.pi * hz(root - 12) * tt_)
                  * (0.5 + 0.5 * np.sin(2 * math.pi * 0.25 * tt_))) * 0.16
            place(lows, dr.astype(np.float32), t)

        if not intro:
            for b in range(4):
                tb = t + b * BEAT
                if tb >= duration:
                    break
                # bas: 1 ve 3'te kök, aralarda sekizlik
                if b in (0, 2):
                    place(lows, bass(root, BEAT * 0.95), tb)
                else:
                    place(lows, bass(root + (0 if b == 1 else 7), BEAT * 0.5), tb)
                if full:
                    place(drums, kick(), tb)
                    if b in (1, 3):
                        place(drums, snare(), tb)
                    place(drums, hat(), tb)
                    place(drums, hat(open_=(b == 3)), tb + BEAT / 2)
                    place(mids, stab(notes, BEAT * 0.42), tb + BEAT / 2)
                elif light:
                    if b in (0, 2):
                        place(drums, kick(0.34), tb)
                    place(drums, hat(), tb + BEAT / 2)

        # melodi: ana ve ikinci bölümde
        if S_MAIN <= t < S_BREAK or S_SECOND <= t < S_END:
            for b in range(4):
                tb = t + b * BEAT
                m = MELODY[(bar_i * 4 + b) % len(MELODY)]
                place(highs, pluck(m, BEAT * 0.85), tb)
        elif light:
            place(highs, pluck(MELODY[bar_i % len(MELODY)], BEAT * 1.6), t)

        t += BAR
        bar_i += 1

    # ── geçişler
    place(fx, riser(3.2), S_RISE - 0.4)
    place(fx, impact(), S_MAIN)
    place(fx, riser(2.4), S_SECOND - 2.0)
    place(fx, impact(1.4), S_SECOND)
    place(fx, riser(2.6), S_FINAL - 2.2)
    place(fx, impact(2.2), S_FINAL)
    place(fx, impact(2.6), S_END)

    mix = drums * 0.82 + lows * 0.92 + mids * 1.05 + highs * 1.0 + fx * 0.8
    mix = reverb(mix, 0.22)

    # bölümlere göre genel seviye
    tt = np.arange(n, dtype=np.float32) / SR
    shape = np.interp(tt, [0, S_RISE, S_MAIN, S_BREAK, S_SECOND, S_FINAL,
                           S_END, duration - 1.5, duration],
                      [0.72, 0.80, 1.0, 0.84, 1.0, 1.0, 0.9, 0.55, 0.0]).astype(np.float32)
    mix *= shape
    mix = np.tanh(mix * 1.35) * 0.86

    # stereo genişlik
    d = 300
    right = np.zeros_like(mix)
    right[d:] = mix[:-d]
    right = right * 0.35 + mix * 0.65
    st = np.stack([mix, right], axis=1)
    a = int(SR * 0.35)
    st[:a] *= np.linspace(0, 1, a, dtype=np.float32)[:, None]
    return np.clip(st, -1, 1)


def write(path: str, duration: float) -> None:
    st = (build(duration) * 32767).astype(np.int16)
    with wave.open(path, "wb") as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes(st.tobytes())


if __name__ == "__main__":
    d = 122.0
    if "--dinle" in sys.argv:
        d = float(sys.argv[sys.argv.index("--dinle") + 1])
    out = sys.argv[sys.argv.index("--cikti") + 1] if "--cikti" in sys.argv else "muzik.wav"
    write(out, d)
    print(f"{out} · {d:.0f} s")
