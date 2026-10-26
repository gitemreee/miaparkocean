#!/usr/bin/env python3
"""
Kurumsal reklam görselleri (1080x1920 → 2160x3840): ince dış çerçeve, içinde buzlu cam paneller.

Metin:
  1 Milyon TL peşinatla yeni evinize taşının.
  60 ay sabit taksit · Ara ödeme yok · Faiz yok · Banka yok · Kredi yok · Kefil yok
  Ev ve araç takasına açıktır.
  444 10 58 · miaparkocean.com · tildainsaat.com

    python3.13 scripts/build-reklam-kurumsal.py
"""

import json
import os
import subprocess
import tempfile

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "sosyal-medya", "reklam-kurumsal")
FONT = os.path.join(ROOT, "brand-source", "fonts", "Montserrat-var.ttf")
W, H = 1080, 1920
ALTIN, ALTIN2 = "#c9a24a", "#e3c27a"
F = lambda *p: "file://" + os.path.join(ROOT, *p)
FOTO_H = round(W * 2752 / 1536)

# ad: (fotoğraf, yukarı kaydırma px, koşullar paneli y)
KARELER = [
    ("1-uzaktan", "22-uzaktan-teleobjektif.jpg", 300, 545),
    ("2-yoldan", "21-yoldan-gunesli.jpg", 0, 1190),
    ("3-drone", "17-drone-yalniz-site.jpg", 0, 1190),
    ("4-balkonda-aile", "19-balkon-cay-gunduz.jpg", 110, 1200),
    ("5-giris-gun-batimi", "23-giris-avlu-gun-batimi.jpg", 0, 1190),
]

MADDELER = ["60 ay sabit taksit", "Ara ödeme yok", "Faiz yok", "Banka yok", "Kredi yok", "Kefil yok"]

TIK = (f'<svg viewBox="0 0 24 24" style="width:30px;height:30px;flex:none"><circle cx="12" cy="12" r="11" '
       f'fill="none" stroke="{ALTIN2}" stroke-width="1.6"/><path d="M7 12.5l3.2 3.2L17 9" fill="none" '
       f'stroke="{ALTIN2}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def sayfa(foto, kaydir, panel_y):
    maddeler = "".join(
        f'<div style="display:flex;align-items:center;gap:16px">{TIK}<span>{m}</span></div>' for m in MADDELER)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: Mont; src: url("file://{FONT}"); font-weight: 100 900; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:{W}px; height:{H}px; overflow:hidden; position:relative; font-family:Mont,sans-serif;
       -webkit-font-smoothing:antialiased; background:#0b1a36; color:#fff; }}
.a {{ position:absolute; }}
.tek {{ white-space:nowrap; line-height:1; }}
.cam {{ background:rgba(10,26,56,.58); -webkit-backdrop-filter:blur(14px) saturate(1.1); backdrop-filter:blur(14px) saturate(1.1);
       border:1px solid rgba(227,194,122,.55); border-radius:6px; }}
.ust-yazi {{ font-size:22px; font-weight:600; letter-spacing:.32em; color:{ALTIN2}; }}
</style></head><body>
  <img class="a" src="{F('sosyal-medya','bitmis-fotograflar',foto)}" style="left:0;top:{-kaydir}px;width:{W}px;height:{FOTO_H}px;object-fit:cover;-webkit-mask-image:linear-gradient(180deg,#000 {'86%' if kaydir else '100%'},transparent 100%)">
  <div class="a" style="left:0;top:0;width:{W}px;height:520px;background:linear-gradient(180deg,rgba(6,16,36,.55),rgba(6,16,36,0))"></div>
  <div class="a" style="left:0;bottom:0;width:{W}px;height:760px;background:linear-gradient(0deg,rgba(6,16,36,.80),rgba(6,16,36,0))"></div>

  <!-- ince dış çerçeve + köşe vurguları -->
  <div class="a" style="left:34px;top:34px;width:{W - 68}px;height:{H - 68}px;border:1.5px solid rgba(255,255,255,.82)"></div>
  {''.join(f'<div class="a" style="{p};width:44px;height:44px;border-color:{ALTIN2};border-style:solid;border-width:{b}"></div>'
           for p, b in [("left:26px;top:26px", "3px 0 0 3px"), ("right:26px;top:26px", "3px 3px 0 0"),
                        ("left:26px;bottom:26px", "0 0 3px 3px"), ("right:26px;bottom:26px", "0 3px 3px 0")])}

  <!-- üst: logo + başlık -->
  <img class="a" src="{F('public','brand','logo-mia-2026.png')}" style="left:430px;top:78px;width:220px;filter:brightness(0) invert(1) drop-shadow(0 2px 8px rgba(0,0,0,.35))">
  <div class="a cam" style="left:96px;top:290px;width:888px;padding:34px 40px 38px;text-align:center">
    <div class="tek ust-yazi">İZMİT · MİA BÖLGESİ</div>
    <div class="tek" style="margin-top:22px;font-size:50px;font-weight:300;letter-spacing:.01em">1 Milyon TL peşinatla</div>
    <div class="tek" style="margin-top:12px;font-size:54px;font-weight:700;letter-spacing:.005em">yeni evinize taşının.</div>
  </div>

  <!-- alt panel: koşullar + takas -->
  <div class="a cam" style="left:96px;top:{panel_y}px;width:888px;padding:34px 46px 30px">
    <div class="tek ust-yazi" style="text-align:center">ÖDEME KOŞULLARI</div>
    <div style="margin-top:26px;display:grid;grid-template-columns:1fr 1fr;gap:20px 30px;font-size:31px;font-weight:500;line-height:1">
      {maddeler}
    </div>
    <div style="margin:28px auto 0;width:120px;height:1px;background:{ALTIN2}"></div>
    <div class="tek" style="margin-top:22px;text-align:center;font-size:31px;font-weight:600;color:{ALTIN2};letter-spacing:.02em">
      Ev ve araç takasına açıktır.</div>
  </div>

  <!-- iletişim -->
  <div class="a tek" style="left:0;width:{W}px;top:1636px;text-align:center;font-size:52px;font-weight:700;letter-spacing:.08em">444 10 58</div>
  <div class="a tek" style="left:0;width:{W}px;top:1708px;text-align:center;font-size:24px;font-weight:500;letter-spacing:.14em;color:rgba(255,255,255,.9)">
    miaparkocean.com &nbsp;<span style="color:{ALTIN2}">|</span>&nbsp; tildainsaat.com</div>
  <div class="a" style="left:0;top:1768px;width:{W}px;display:flex;align-items:center;justify-content:center;gap:30px">
    <img src="{F('public','brand','vektor','tilda-beyaz.svg')}" style="height:34px">
    <div style="width:1px;height:38px;background:rgba(255,255,255,.55)"></div>
    <img src="{F('public','brand','vektor','ocean-beyaz.svg')}" style="height:32px">
  </div>
</body></html>"""


def main():
    os.makedirs(OUT, exist_ok=True)
    gecici = tempfile.mkdtemp(prefix="kurumsal-")
    isler = []
    for ad, foto, kaydir, panel_y in KARELER:
        hp = os.path.join(gecici, ad + ".html")
        open(hp, "w", encoding="utf-8").write(sayfa(foto, kaydir, panel_y))
        isler.append(dict(html=hp, w=W, h=H, dsf=2, dilim=W, cikti=os.path.join(gecici, ad), ad=ad))
    jp = os.path.join(gecici, "isler.json")
    json.dump(isler, open(jp, "w"))
    npm = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    subprocess.run(["node", os.path.join(ROOT, "scripts", "mega-bilbord", "render.cjs"), jp], check=True,
                   env={**os.environ, "NODE_PATH": npm}, stdout=subprocess.DEVNULL)
    for is_ in isler:
        im = Image.open(json.load(open(is_["cikti"] + ".json"))[0]).convert("RGB")
        yol = os.path.join(OUT, f"mia-reklam-{is_['ad']}.jpg")
        im.save(yol, quality=93)
        print("  →", os.path.relpath(yol, ROOT), im.size)


if __name__ == "__main__":
    main()
