#!/usr/bin/env python3
"""
Dev pano kahraman görseli: gökyüzü maskeli + kenar geçişli RGBA.

    python3.13 scripts/kahraman-kesik.py <goruntu> <maske> <cikti.png>
"""
import sys

import numpy as np
from PIL import Image

o = Image.open(sys.argv[1]).convert("RGB")
m = Image.open(sys.argv[2]).convert("L").resize(o.size, Image.LANCZOS)
m = np.asarray(m).astype(np.float32) / 255
W, H = o.size
xs = np.arange(W) / W
ys = np.arange(H) / H
sol = np.clip(xs / 0.10, 0, 1) ** 1.5
sag = np.clip((1.0 - xs) / 0.045, 0, 1) ** 1.5
alt = np.clip((0.943 - ys) / 0.05, 0, 1) ** 1.2
alfa = m * (sol * sag)[None, :] * alt[:, None]
Image.fromarray(np.dstack([np.asarray(o), (alfa * 255).astype(np.uint8)]), "RGBA").save(
    sys.argv[3], optimize=True)
print("kesik:", o.size)
