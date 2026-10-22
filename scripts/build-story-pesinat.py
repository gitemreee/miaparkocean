#!/usr/bin/env python3
"""
Instagram story / reel kapak görseli (1080x1920): "İlk evine 699.000 TL peşinat ile sahip ol".

Referans: Egeyapı'nın mor zeminli, sunucu kadınlı kampanya görseli. Bizde MİA turkuazından
laciverte geçişli üst alan, üç kademeli rozet (peşinat / 60 ay vade / banka-kredi-ara ödeme yok),
solda sunucu kesiği, altta projenin gerçek render'ı, en altta Tilda + MİA logoları ve 444 10 58.

    python3.13 scripts/build-story-pesinat.py          # sosyal-medya/story-pesinat/story-pesinat.jpg (2160x3840)
"""

import importlib.util as _il
import json
import os
import subprocess
import tempfile

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _yukle(ad, dosya):
    spec = _il.spec_from_file_location(ad, os.path.join(ROOT, "scripts", dosya))
    m = _il.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


mb = _yukle("mb", "build-mega-bilbord.py")
OUT = os.path.join(ROOT, "sosyal-medya", "story-pesinat")
W, H = 1080, 1920
F = lambda *p: "file://" + os.path.join(ROOT, *p)

SUNUCU = os.path.join(ROOT, "signage-source", "aile", "sunucu-kesik.png")
HERO = os.path.join(ROOT, "signage-source", "4k", "orta-giris-genis-8k.png")
TILDA = os.path.join(ROOT, "public", "brand", "vektor", "tilda-beyaz.svg")
MIA = os.path.join(ROOT, "public", "brand", "logo-mia-2026.png")

TURK, LAC, SARI, YESIL, KIR = "#1d7f9c", "#14225a", "#f5c542", "#3fae5a", "#e3262e"


def sayfa():
    sw, sh = Image.open(SUNUCU).size
    s_h = 920
    s_w = round(s_h * sw / sh)
    hw, hh = Image.open(HERO).size
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
{mb.CSS.replace("__FONT__", mb.FONT)}
body {{ margin:0; width:{W}px; height:{H}px; overflow:hidden; position:relative; background:#fff; }}
.a {{ position:absolute; }}
.tek {{ white-space:nowrap; line-height:1; }}
.orta {{ left:0; width:{W}px; text-align:center; }}
.rozet {{ left:50%; transform:translateX(-50%); border-radius:26px; padding:18px 44px; text-align:center;
          font-weight:800; color:#fff; box-shadow:0 14px 30px rgba(0,0,0,.25); }}
</style></head><body>
  <div class="a" style="left:0;top:0;width:{W}px;height:{H}px;
       background:linear-gradient(180deg,{LAC} 0%,#163a73 28%,{TURK} 52%,#8fd6e6 60%,#ffffff 64%)"></div>
  <div class="a" style="left:0;top:1120px;width:{W}px;height:800px;overflow:hidden">
    <img src="{F('signage-source','4k','orta-giris-genis-8k.png')}" style="position:absolute;left:{-round((1000 * hw / hh - W) / 2)}px;top:-40px;width:{round(1000 * hw / hh)}px;height:1000px;filter:brightness(1.12) saturate(1.08)">
    <div class="a" style="left:0;top:0;width:{W}px;height:260px;background:linear-gradient(180deg,#8fd6e6,rgba(143,214,230,0))"></div>
    <div class="a" style="left:0;bottom:0;width:{W}px;height:330px;background:linear-gradient(0deg,rgba(20,34,90,.96) 0%,rgba(20,34,90,.8) 50%,rgba(20,34,90,0) 100%)"></div>
  </div>
  <div class="a tek orta" style="top:120px;font-size:84px;font-weight:800;color:#fff;letter-spacing:-.01em">İlk Evine</div>
  <div class="a tek orta" style="top:218px;font-size:112px;font-weight:800;color:{SARI};letter-spacing:-.02em">699.000 TL</div>
  <div class="a tek orta" style="top:348px;font-size:84px;font-weight:800;color:#fff;letter-spacing:-.01em">Peşinat ile Sahip Ol</div>
  <div class="a tek orta" style="top:455px;font-size:36px;font-weight:600;color:#cfe8f0;letter-spacing:.18em">MİA PARK OCEAN · İZMİT</div>

  <img class="a" src="{F('signage-source','aile','sunucu-kesik.png')}" style="left:-40px;top:{1560 - s_h}px;width:{s_w}px;height:{s_h}px;filter:drop-shadow(0 20px 30px rgba(0,0,0,.35))">

  <div class="a rozet" style="left:67%;top:600px;width:440px;background:{SARI};color:{LAC};border-radius:26px 26px 0 0">
    <div class="tek" style="font-size:66px;letter-spacing:-.02em">699.000<span style="font-size:.4em;margin-left:8px">TL'DEN</span></div>
    <div class="tek" style="font-size:30px;margin-top:8px;letter-spacing:.06em">BAŞLAYAN PEŞİNAT</div>
  </div>
  <div class="a rozet" style="left:67%;top:755px;width:440px;background:{YESIL};border-radius:0">
    <div class="tek" style="font-size:62px;letter-spacing:-.01em">60 AY VADE</div>
  </div>
  <div class="a rozet" style="left:67%;top:862px;width:440px;background:{KIR};border-radius:0 0 26px 26px">
    <div class="tek" style="font-size:30px;letter-spacing:.06em">BANKA YOK · KREDİ YOK</div>
    <div class="tek" style="font-size:30px;margin-top:6px;letter-spacing:.06em">ARA ÖDEME YOK</div>
  </div>
  <div class="a tek" style="left:67%;transform:translateX(-50%);top:1000px;font-size:30px;font-weight:700;color:#fff;letter-spacing:.04em;text-align:center">AYDA SADECE 29.900 TL</div>

  <div class="a" style="left:0;top:1655px;width:{W}px;display:flex;align-items:center;justify-content:center;gap:60px">
    <img src="{F('public','brand','vektor','tilda-beyaz.svg')}" style="height:100px">
    <div style="width:3px;height:120px;background:rgba(255,255,255,.4)"></div>
    <img src="{F('public','brand','logo-mia-2026.png')}" style="height:130px;filter:brightness(0) invert(1)">
  </div>
  <div class="a tek orta" style="top:1812px;font-size:50px;font-weight:800;color:#fff;letter-spacing:.04em">444 10 58 &nbsp;·&nbsp; miaparkocean.com</div>
</body></html>"""


def main():
    os.makedirs(OUT, exist_ok=True)
    gecici = tempfile.mkdtemp(prefix="story-")
    hp = os.path.join(gecici, "s.html")
    open(hp, "w", encoding="utf-8").write(sayfa())
    isler = [dict(html=hp, w=W, h=H, dsf=2, dilim=W, cikti=os.path.join(gecici, "s"))]
    jp = os.path.join(gecici, "isler.json")
    json.dump(isler, open(jp, "w"))
    npm = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    subprocess.run(["node", os.path.join(ROOT, "scripts", "mega-bilbord", "render.cjs"), jp], check=True, env={**os.environ, "NODE_PATH": npm})
    im = Image.open(json.load(open(os.path.join(gecici, "s.json")))[0]).convert("RGB")
    yol = os.path.join(OUT, "story-pesinat.jpg")
    im.save(yol, quality=94)
    im.resize((1080, 1920), Image.LANCZOS).save(os.path.join(OUT, "story-pesinat-1080.jpg"), quality=92)
    print("  →", os.path.relpath(yol, ROOT), im.size)


if __name__ == "__main__":
    main()
