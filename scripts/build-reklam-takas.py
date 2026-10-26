#!/usr/bin/env python3
"""
Story / reel reklam görselleri (1080x1920, çıktı 2160x3840): bitmiş proje fotoğrafları üzerine balon metinler.

Metin (müşteri talebi):
  1 MİLYON TL PEŞİNATLA YENİ EVİNİZE TAŞININ!
  60 AY SABİT TAKSİT · ARA ÖDEME YOK · FAİZ YOK · BANKA YOK · KREDİ YOK · KEFİL YOK
  EV & ARAÇ TAKASINA AÇIKTIR
  444 10 58 · miaparkocean.com · Tilda / MİA / Ocean logoları

    python3.13 scripts/build-reklam-takas.py
"""

import json
import os
import subprocess
import tempfile

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "sosyal-medya", "reklam-takas")
FOTO = os.path.join(ROOT, "sosyal-medya", "bitmis-fotograflar")
FONT = os.path.join(ROOT, "brand-source", "fonts", "Montserrat-var.ttf")
W, H = 1080, 1920
LAC, LAC2, ALTIN, ALTIN2, KIR, SIY = "#0f2a5a", "#17407f", "#c9a24a", "#e8c877", "#e3262e", "#141414"
F = lambda *p: "file://" + os.path.join(ROOT, *p)

# ad: (fotoğraf, fotoğrafı yukarı kaydırma px, üst koyulaştırma gücü, takas rozeti y)
KARELER = [
    ("1-uzaktan", "22-uzaktan-teleobjektif.jpg", 230, 0.00, 860),
    ("2-yoldan", "21-yoldan-gunesli.jpg", 0, 0.18, 1330),
    ("3-balkon-manzara", "15-balkondan-gunesli.jpg", 0, 0.22, 1330),
    ("4-balkonda-cay", "19-balkon-cay-gunduz.jpg", 0, 0.30, 1360),
    ("5-giris-gun-batimi", "23-giris-avlu-gun-batimi.jpg", 0, 0.30, 1330),
]

YOKLAR = [("ARA ÖDEME YOK!", SIY), ("FAİZ YOK!", KIR), ("BANKA YOK!", KIR),
          ("KREDİ YOK!", SIY), ("KEFİL YOK!", SIY)]


def pill(metin, renk, fs=34):
    return (f'<div class="pill" style="background:{renk};font-size:{fs}px">'
            f'<span class="tik">✕</span>{metin}</div>')


def sayfa(foto, kaydir, koyu, takas_y):
    yoklar = "".join(pill(m, r) for m, r in YOKLAR)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: Mont; src: url("file://{FONT}"); font-weight: 100 900; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:{W}px; height:{H}px; overflow:hidden; position:relative; font-family:Mont,sans-serif;
       -webkit-font-smoothing:antialiased; background:#000; }}
.a {{ position:absolute; }}
.tek {{ white-space:nowrap; line-height:1; }}
.golge {{ box-shadow:0 18px 40px rgba(0,0,0,.35), 0 4px 10px rgba(0,0,0,.25); }}
.pill {{ display:inline-flex; align-items:center; gap:14px; color:#fff; font-weight:800; letter-spacing:.03em;
        height:80px; padding:0 28px 0 14px; border-radius:40px; white-space:nowrap;
        box-shadow:0 12px 26px rgba(0,0,0,.30); border:3px solid rgba(255,255,255,.85); }}
.tik {{ display:inline-flex; align-items:center; justify-content:center; width:48px; height:48px; border-radius:50%;
       background:#fff; color:{KIR}; font-size:26px; font-weight:900; }}
.altin {{ background:linear-gradient(180deg,#fff1c4 0%,{ALTIN2} 35%,{ALTIN} 70%,#a87b2c 100%);
         -webkit-background-clip:text; background-clip:text; color:transparent; }}
</style></head><body>
  <img class="a" src="{F('sosyal-medya','bitmis-fotograflar',foto)}" style="left:0;top:{-kaydir}px;width:{W}px;height:{round(W * 2752 / 1536)}px;object-fit:cover">
  <div class="a" style="left:0;top:0;width:{W}px;height:1100px;
       background:linear-gradient(180deg,rgba(8,20,45,{koyu}) 0%,rgba(8,20,45,{koyu * .6}) 55%,rgba(8,20,45,0) 100%)"></div>
  <div class="a" style="left:0;bottom:0;width:{W}px;height:520px;
       background:linear-gradient(0deg,rgba(9,24,52,1) 0%,rgba(9,24,52,.9) 50%,rgba(9,24,52,0) 100%)"></div>

  <!-- ana balon: 1 milyon TL peşinat -->
  <div class="a golge" style="left:70px;top:70px;width:940px;padding:34px 30px 38px;border-radius:44px;text-align:center;
       background:linear-gradient(160deg,{LAC2} 0%,{LAC} 70%);border:5px solid {ALTIN}">
    <div class="tek altin" style="font-size:124px;font-weight:900;letter-spacing:-.02em">1 MİLYON TL</div>
    <div class="tek" style="margin-top:14px;font-size:52px;font-weight:800;color:#fff;letter-spacing:.06em">PEŞİNATLA</div>
    <div class="tek" style="margin-top:12px;font-size:58px;font-weight:900;color:#fff;letter-spacing:.01em">YENİ EVİNİZE TAŞININ!</div>
    <!-- balon kuyruğu -->
    <div class="a" style="left:120px;bottom:-46px;width:0;height:0;border-left:34px solid transparent;
         border-right:34px solid transparent;border-top:46px solid {ALTIN}"></div>
    <div class="a" style="left:126px;bottom:-36px;width:0;height:0;border-left:28px solid transparent;
         border-right:28px solid transparent;border-top:38px solid {LAC}"></div>
  </div>

  <!-- 60 ay rozeti -->
  <div class="a golge" style="left:150px;top:470px;width:780px;height:130px;border-radius:65px;background:{KIR};
       border:5px solid #fff;display:flex;align-items:center;justify-content:center;gap:22px;transform:rotate(-2deg)">
    <div class="tek" style="font-size:84px;font-weight:900;color:#fff">60 AY</div>
    <div style="line-height:1.02;color:#fff;font-weight:800">
      <div class="tek" style="font-size:38px;letter-spacing:.04em">SABİT</div>
      <div class="tek" style="font-size:38px;letter-spacing:.04em">TAKSİT</div>
    </div>
  </div>

  <!-- yok balonları -->
  <div class="a" style="left:20px;top:635px;width:1040px;display:flex;flex-wrap:wrap;justify-content:center;gap:16px 14px">
    {yoklar}
  </div>

  <!-- takas rozeti -->
  <div class="a golge" style="left:130px;top:{takas_y}px;width:820px;padding:20px 0;border-radius:30px;text-align:center;
       background:linear-gradient(180deg,#fff1c4 0%,{ALTIN2} 40%,{ALTIN} 100%);border:4px solid #fff;transform:rotate(1.5deg)">
    <div class="tek" style="font-size:28px;font-weight:800;color:{LAC};letter-spacing:.22em">EV &amp; ARAÇ</div>
    <div class="tek" style="margin-top:6px;font-size:56px;font-weight:900;color:{LAC};letter-spacing:.02em">TAKASINA AÇIKTIR</div>
  </div>

  <!-- alt bant: logolar + iletişim -->
  <div class="a" style="left:0;top:1560px;width:{W}px;display:flex;align-items:center;justify-content:center;gap:40px">
    <img src="{F('public','brand','vektor','tilda-beyaz.svg')}" style="height:62px">
    <div style="width:3px;height:84px;background:rgba(255,255,255,.5)"></div>
    <img src="{F('public','brand','logo-mia-2026.png')}" style="height:108px;filter:brightness(0) invert(1)">
    <div style="width:3px;height:84px;background:rgba(255,255,255,.5)"></div>
    <img src="{F('public','brand','vektor','ocean-beyaz.svg')}" style="height:58px">
  </div>
  <div class="a tek" style="left:0;width:{W}px;top:1712px;text-align:center;font-size:92px;font-weight:900;color:#fff;letter-spacing:.04em">
    <span style="color:{ALTIN2}">☎</span> 444 10 58</div>
  <div class="a tek" style="left:0;width:{W}px;top:1830px;text-align:center;font-size:38px;font-weight:700;color:{ALTIN2};letter-spacing:.12em">miaparkocean.com</div>
</body></html>"""


def main():
    os.makedirs(OUT, exist_ok=True)
    gecici = tempfile.mkdtemp(prefix="reklam-")
    isler = []
    for ad, foto, kaydir, koyu, takas_y in KARELER:
        hp = os.path.join(gecici, ad + ".html")
        open(hp, "w", encoding="utf-8").write(sayfa(foto, kaydir, koyu, takas_y))
        isler.append(dict(html=hp, w=W, h=H, dsf=2, dilim=W, cikti=os.path.join(gecici, ad), ad=ad))
    jp = os.path.join(gecici, "isler.json")
    json.dump(isler, open(jp, "w"))
    npm = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    subprocess.run(["node", os.path.join(ROOT, "scripts", "mega-bilbord", "render.cjs"), jp], check=True,
                   env={**os.environ, "NODE_PATH": npm})
    for is_ in isler:
        im = Image.open(json.load(open(is_["cikti"] + ".json"))[0]).convert("RGB")
        yol = os.path.join(OUT, f"mia-reklam-{is_['ad']}.jpg")
        im.save(yol, quality=93)
        print("  →", os.path.relpath(yol, ROOT), im.size)


if __name__ == "__main__":
    main()
