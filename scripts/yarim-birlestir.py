#!/usr/bin/env python3
"""4K yarımları (L/R, ov px bindirmeli) yumuşak geçişle tek görsele birleştirir.

    python3.13 scripts/yarim-birlestir.py <ad>   (signage-source/4k/<ad>-yarim-{L,R}-4k.png → <ad>-8k.png)
"""
import json, os, sys
import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "signage-source", "4k")
ad = sys.argv[1]
m = json.load(open(os.path.join(D, "yarim-meta.json")))[ad]
L = Image.open(os.path.join(D, f"{ad}-yarim-L-4k.png")).convert("RGB")
R = Image.open(os.path.join(D, f"{ad}-yarim-R-4k.png")).convert("RGB")
# iki yarım aynı yüksekliğe getirilir; ölçek = yeni yükseklik / eski yükseklik
H = min(L.height, R.height)
s = H / m["h"]
L = L.resize((round(m["L"][0] * s), H), Image.LANCZOS)
R = R.resize((round(m["R"][0] * s), H), Image.LANCZOS)
ov = round(2 * m["ov"] * s)                      # bindirme genişliği (yeni px)
W = L.width + R.width - ov
out = np.zeros((H, W, 3), np.float32)
a = np.asarray(L, np.float32); b = np.asarray(R, np.float32)
out[:, :L.width] = a
out[:, L.width - ov:] = np.maximum(out[:, L.width - ov:], 0)
out[:, L.width:] = b[:, ov:]
# bindirme bölgesi: doğrusal karışım
t = np.linspace(0, 1, ov, dtype=np.float32)[None, :, None]
out[:, L.width - ov:L.width] = a[:, L.width - ov:] * (1 - t) + b[:, :ov] * t
yol = os.path.join(D, f"{ad}-8k.png")
Image.fromarray(out.clip(0, 255).astype(np.uint8)).save(yol, optimize=True)
print(yol, (W, H))
