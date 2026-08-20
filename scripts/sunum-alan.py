#!/usr/bin/env python3
"""
Zemin PNG'lerinde yazının güvenle oturabileceği alanları ÖLÇER.

Organik dalga zeminlerde "sol yarı beyazdır" varsayımı tutmuyor; sınır her
y'de farklı yerden geçiyor. Bu yüzden yerleşimi gözle değil bu raporla
kuruyoruz.

Her zemin için:
  ACIK  = koyu yazının okunacağı alan (luminans yüksek)
  KOYU  = beyaz yazının okunacağı alan (luminans düşük)
her satır bandı (0.5 inç'lik dilimler) için sol/sağ sınırıyla birlikte.

    python3 scripts/sunum-alan.py [zemin-adi ...]
"""

import os
import sys
import glob
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEK = os.path.join(ROOT, "sunum", "kaynak", "sekil")
W_IN, H_IN = 13.333, 7.5
BANT = 0.5          # inç
ACIK_ESIK = 186     # bunun üstü koyu yazıyı taşır
KOYU_ESIK = 96      # bunun altı beyaz yazıyı taşır


def lum(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def rapor(path):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im, np.float32)
    h, w = a.shape[:2]
    L = lum(a)
    px_in = w / W_IN
    nb = int(round(H_IN / BANT))
    print("\n" + os.path.basename(path))
    print(f"  {'bant(inç)':>12} {'AÇIK sol→sağ':>22} {'KOYU sol→sağ':>22}")
    for b in range(nb):
        y0 = int(b * BANT / H_IN * h)
        y1 = int((b + 1) * BANT / H_IN * h)
        blok = L[y0:y1]
        acik = (blok > ACIK_ESIK).all(axis=0)     # sütunun TAMAMI açık
        koyu = (blok < KOYU_ESIK).all(axis=0)

        def araligi(m):
            if not m.any():
                return None
            # en uzun kesintisiz koşuyu bul
            d = np.diff(np.concatenate([[0], m.view(np.int8), [0]]))
            bas, son = np.where(d == 1)[0], np.where(d == -1)[0]
            i = int(np.argmax(son - bas))
            return bas[i] / px_in, son[i] / px_in

        ra, rk = araligi(acik), araligi(koyu)
        fa = f"{ra[0]:5.2f} → {ra[1]:5.2f}" if ra else "          —"
        fk = f"{rk[0]:5.2f} → {rk[1]:5.2f}" if rk else "          —"
        print(f"  {b*BANT:5.2f}-{(b+1)*BANT:4.2f} {fa:>22} {fk:>22}")


def main(argv):
    if argv:
        fs = [os.path.join(SEK, a if a.endswith(".png") else a + ".png") for a in argv]
    else:
        fs = sorted(glob.glob(os.path.join(SEK, "bg-*.png")))
    for f in fs:
        rapor(f)


if __name__ == "__main__":
    main(sys.argv[1:])
