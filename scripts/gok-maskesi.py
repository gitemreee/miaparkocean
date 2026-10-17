#!/usr/bin/env python3
"""
Render'ın gökyüzü maskesini çıkarır.

Yapay zekâ ile gökyüzü düz macentaya boyanmış bir kopya (aynı kadraj)
verilir; macenta bölgeden yalnızca ÜST KENARA BAĞLI olanlar gök sayılır
(penceredeki yansımalar karışmasın). Pikseller orijinal render'dan kalır,
yapay zekâ görüntüsünden yalnızca maske alınır.

    python3.13 scripts/gok-maskesi.py <orijinal.jpg> <macenta.png> <maske.png>
"""
import sys

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

o = Image.open(sys.argv[1]).convert("RGB")
m = Image.open(sys.argv[2]).convert("RGB").resize(o.size, Image.LANCZOS)
a = np.asarray(m).astype(np.int16)
gok = (a[..., 0] > 160) & (a[..., 2] > 160) & (a[..., 1] < 120)
etiket, _ = ndimage.label(gok)
ust = set(np.unique(etiket[0])) - {0}
bag = np.isin(etiket, list(ust))
maske = Image.fromarray(((~bag) * 255).astype(np.uint8), "L")
maske = maske.filter(ImageFilter.MedianFilter(5)).filter(ImageFilter.GaussianBlur(1.0))
maske.save(sys.argv[3])
print("gök oranı:", round(float(bag.mean()), 3))
