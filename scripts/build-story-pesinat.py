#!/usr/bin/env python3
"""
Instagram story / reel kapak görseli (1080x1920): "İlk evine 1 milyon TL peşinat ile sahip ol".

Referans (Egeyapı): mor → mavi geçişli üst alan, ortada üç kademeli rozet (sarı peşinat / yeşil
60 ay vade / mor banka-kefil yok), solda işaret eden sunucu kadın, altta tam genişlik proje render'ı.
Bizde aynı kurgu: sunucu kesiği (Higgsfield), gerçek giriş render'ı (altın saat, 8K), Tilda + MİA
logoları ve 444 10 58.

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

SUNUCU = os.path.join(ROOT, "signage-source", "aile", "sunucu2-kesik.png")
HERO = os.path.join(ROOT, "signage-source", "4k", "sol-avlu-havuz-teras-8k.png")

LAC, LAC2, ALTIN, KIR = "#0f2a5a", "#17407f", "#c9a24a", "#e3262e"


def sayfa():
    sw, sh = Image.open(SUNUCU).size
    s_h = 1150
    s_w = round(s_h * sw / sh)
    hw, hh = Image.open(HERO).size
    r_h = 900
    r_w = round(r_h * hw / hh)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
{mb.CSS.replace("__FONT__", mb.FONT)}
body {{ margin:0; width:{W}px; height:{H}px; overflow:hidden; position:relative; background:#fff; }}
.a {{ position:absolute; }}
.tek {{ white-space:nowrap; line-height:1; }}
.orta {{ left:0; width:{W}px; text-align:center; }}
.rozet {{ left:61%; transform:translateX(-50%); text-align:center; font-weight:800; color:#fff;
          box-shadow:0 16px 34px rgba(0,0,0,.22); }}
</style></head><body>
  <div class="a" style="left:0;top:0;width:{W}px;height:{H}px;
       background:linear-gradient(180deg,#ffffff 0%,#f4f7fb 30%,#e6eef8 50%,#d7e7f6 62%,#cfe3f4 66%)"></div>

  <div class="a" style="left:0;top:{H - r_h}px;width:{W}px;height:{r_h}px;overflow:hidden">
    <img src="{F('signage-source','4k','sol-avlu-havuz-teras-8k.png')}" style="position:absolute;left:{-round((r_w - W) / 2)}px;top:0;width:{r_w}px;height:{r_h}px">
    <div class="a" style="left:0;top:0;width:{W}px;height:220px;background:linear-gradient(180deg,#cfe3f4,rgba(207,227,244,0))"></div>
    <div class="a" style="left:0;bottom:0;width:{W}px;height:240px;background:linear-gradient(0deg,rgba(15,42,90,.92) 0%,rgba(15,42,90,.55) 55%,rgba(15,42,90,0) 100%)"></div>
  </div>

  <div class="a tek orta" style="top:170px;font-size:70px;font-weight:800;color:{LAC};letter-spacing:-.01em">İlk Evine</div>
  <div class="a tek orta" style="top:258px;font-size:112px;font-weight:800;color:{ALTIN};letter-spacing:-.02em">1 MİLYON TL</div>
  <div class="a tek orta" style="top:388px;font-size:70px;font-weight:800;color:{LAC};letter-spacing:-.01em">Peşinat ile Sahip Ol</div>
  <div class="a tek orta" style="top:478px;font-size:30px;font-weight:600;color:#5a6b85;letter-spacing:.2em">MİA PARK OCEAN · İZMİT</div>

  <div class="a rozet" style="top:600px;width:540px;background:linear-gradient(180deg,{LAC2},{LAC});border-radius:34px 34px 0 0;padding:26px 0 22px">
    <div class="tek" style="font-size:72px;letter-spacing:-.02em">1 MİLYON<span style="font-size:.5em;margin-left:10px">TL</span></div>
    <div class="tek" style="font-size:30px;margin-top:10px;letter-spacing:.06em">PEŞİNATLA</div>
  </div>
  <div class="a rozet" style="top:766px;width:540px;background:{ALTIN};color:{LAC};border-radius:0 0 34px 34px;padding:22px 0 24px">
    <div class="tek" style="font-size:62px;letter-spacing:.01em">60 AY VADE</div>
  </div>
  <div class="a rozet" style="top:900px;width:420px;background:{KIR};border-radius:30px;padding:20px 0">
    <div class="tek" style="font-size:30px;letter-spacing:.06em">BANKA YOK</div>
    <div class="tek" style="font-size:30px;margin-top:8px;letter-spacing:.06em">ARA ÖDEME YOK</div>
  </div>
  <div class="a tek" style="left:61%;transform:translateX(-50%);top:1035px;font-size:30px;font-weight:700;color:{LAC};letter-spacing:.06em">EV &amp; ARAÇ TAKASINA AÇIK</div>

  <img class="a" src="{F('signage-source','aile','sunucu2-kesik.png')}" style="left:-70px;top:620px;width:{s_w}px;height:{s_h}px;filter:drop-shadow(0 24px 34px rgba(0,0,0,.35));-webkit-mask-image:linear-gradient(180deg,#000 82%,transparent 100%);mask-image:linear-gradient(180deg,#000 82%,transparent 100%)">

  <div class="a" style="left:0;top:1730px;width:{W}px;display:flex;align-items:center;justify-content:center;gap:46px">
    <img src="{F('public','brand','vektor','tilda-beyaz.svg')}" style="height:84px">
    <div style="width:3px;height:90px;background:rgba(255,255,255,.45)"></div>
    <img src="{F('public','brand','logo-mia-2026.png')}" style="height:112px;filter:brightness(0) invert(1)">
  </div>
  <div class="a tek orta" style="top:1850px;font-size:40px;font-weight:800;color:#fff;letter-spacing:.04em">444 10 58 &nbsp;·&nbsp; miaparkocean.com</div>
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
