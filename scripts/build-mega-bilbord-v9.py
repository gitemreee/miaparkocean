#!/usr/bin/env python3
"""
180 m dev pano — 9. tur: müşterinin gün batımı render'ı, örnek panodaki gibi geçişli.

Sol: krem eğik panel (Tilda logosu + slogan) · orta: gerçek gün batımı render'ı, gökyüzü
maskeli, binalar panonun üstünden taşar, kenarları altın gökyüzüne erir · sağ: altın çerçeveli
fiyat kartları, "yok" ikon sırası, MİA PARK OCEAN logosu, son daireler damgası.

Kaynak: signage-source/render-gunbatimi.jpg (müşteri) · gök maskesi Higgsfield macenta
düzenlemesinden (scripts/gok-maskesi.py) → render-gunbatimi-maske.png.

Ödeme: 60 ay sabit taksit (vade) · 1+1 aylık 39.900 ₺ · 2+1 aylık 49.900 ₺ ·
faiz/banka/kredi/ara ödeme yok · son daireler.

    python3.13 scripts/build-mega-bilbord-v9.py [--pdf]
"""

import importlib.util as _il
import json
import os
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _yukle(ad, dosya):
    spec = _il.spec_from_file_location(ad, os.path.join(ROOT, "scripts", dosya))
    m = _il.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


v7 = _yukle("mb_v7", "build-mega-bilbord-v7.py")
v4, v2, mb = v7.v4, v7.v2, v7.mb
OUT = os.path.join(ROOT, "tabela", "mega-bilbord-180m-tur9")
ICERIK, TW, EXT, PH = v2.ICERIK, mb.TW, mb.EXT, mb.PH
y, kutu, satir, damga = v4.y, v4.kutu, v4.satir, v4.damga

HERO = os.path.join(ROOT, "signage-source", "render-gunbatimi.jpg")
MASKE = os.path.join(ROOT, "signage-source", "render-gunbatimi-maske.png")
KESIK = os.path.join(ROOT, "signage-source", "render-gunbatimi-kesik.png")

LAC, ALTIN, KREM = "#1c2742", "#c9973f", "#f7efe3"


# ---------------------------------------------------------------- kahraman: gök maskeli, kenarları erimiş
def kesik():
    o = Image.open(HERO).convert("RGB")
    m = Image.open(MASKE).convert("L").resize(o.size, Image.LANCZOS)
    m = np.asarray(m).astype(np.float32) / 255
    W, H = o.size
    xs, ys = np.arange(W) / W, np.arange(H) / H
    sol = np.clip(xs / 0.09, 0, 1) ** 1.5
    sag = np.clip((1 - xs) / 0.03, 0, 1) ** 1.5
    alt = np.clip((0.90 - ys) / 0.10, 0, 1) ** 1.2          # yol, şeridin altında erir
    a = m * (sol * sag)[None, :] * alt[:, None]
    Image.fromarray(np.dstack([np.asarray(o), (a * 255).astype(np.uint8)]), "RGBA").save(KESIK, optimize=True)
    return KESIK


HH = 1600                       # kahraman yüksekliği (css px); alt kenar 1450 → şeridin altına taşar
HW = round(HH * 16 / 9)
HY = 1450 - HH
SUTUNLAR = [(0.055, 0.465), (0.56, 1.0)]   # taşma katmanında yalnızca bloklar (ağaç tepeleri değil)


def bina(cx):
    src = "file://" + (KESIK if os.path.exists(KESIK) else kesik())
    hx = round(cx - HW / 2)
    dur = []
    for a, b in SUTUNLAR:
        dur += [f"transparent {a * 100:.2f}%", f"#000 {a * 100:.2f}%", f"#000 {b * 100:.2f}%", f"transparent {b * 100:.2f}%"]
    maske = "linear-gradient(90deg," + ",".join(dur) + ")"
    tas = (f'<img class="a" src="{src}" style="left:{hx}px;top:{HY}px;width:{HW}px;height:{HH}px;'
           f'-webkit-mask-image:{maske}">')
    ic = f'<img class="a" src="{src}" style="left:{hx}px;top:{HY - EXT}px;width:{HW}px;height:{HH}px">'
    gunes_x = hx + round(0.48 * HW)
    return tas, ic, gunes_x


# ---------------------------------------------------------------- parçalar
def kart(x, tip, tutar):
    return f'''
<div class="a" style="left:{x}px;top:60px;width:1500px;height:600px;border-radius:44px;
     background:linear-gradient(180deg,#223052 0%,{LAC} 100%);border:7px solid {ALTIN};
     box-shadow:0 26px 60px rgba(60,35,10,.35);display:flex;flex-direction:column;align-items:center;
     justify-content:center;text-align:center;color:#fff">
  <div class="tek altin" style="font-size:230px;font-weight:800;letter-spacing:-.03em;line-height:.95">{tip}</div>
  <div class="tek kas" style="font-size:52px;color:#e9dcc4;margin-top:22px">AYLIK SADECE</div>
  <div class="tek" style="font-size:168px;font-weight:800;letter-spacing:-.03em;margin-top:6px">{tutar}<span style="font-size:.45em">₺</span></div>
  <div style="width:1100px;height:4px;background:rgba(201,151,63,.6);margin:26px 0 18px"></div>
  <div class="tek kas" style="font-size:50px;color:{ALTIN}">60 AY SABİT TAKSİT</div>
</div>'''


IKON = {
    "faiz": '<circle cx="30" cy="30" r="9"/><circle cx="70" cy="70" r="9"/><path d="M26 76 74 24"/>',
    "banka": '<path d="M12 40 50 20l38 20Z"/><path d="M20 44v30M38 44v30M62 44v30M80 44v30M12 80h76"/>',
    "kredi": '<rect x="10" y="26" width="80" height="50" rx="7"/><path d="M10 42h80M22 62h20"/>',
    "ara": '<ellipse cx="50" cy="32" rx="30" ry="11"/><path d="M20 32v18c0 6 13 11 30 11s30-5 30-11V32M20 50v18c0 6 13 11 30 11s30-5 30-11V50"/>',
}


def yok(x, ikon, etiket):
    return f'''
<div class="a" style="left:{x}px;top:170px;width:620px;display:flex;flex-direction:column;align-items:center;text-align:center">
  <div style="width:190px;height:190px;border-radius:50%;border:6px solid {ALTIN};display:flex;align-items:center;justify-content:center;background:rgba(255,250,240,.55)">
    <svg width="120" height="120" viewBox="0 0 100 100" fill="none" stroke="{LAC}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round">
      {IKON[ikon]}<path d="M14 86 86 14" stroke="#c8482f" stroke-width="8"/>
    </svg>
  </div>
  <div class="tek" style="font-size:60px;font-weight:800;color:{LAC};margin-top:26px;letter-spacing:.04em">{etiket}</div>
  <div class="tek" style="font-size:72px;font-weight:800;color:#c8482f;margin-top:4px">YOK</div>
</div>'''


def T():
    r = dict(v4.SERIT_ACIK, serit=LAC, serit_su=ALTIN, serit_logo="#ffffff")
    tas, ic, gx = bina(7500)
    zemin = (f"radial-gradient(ellipse 1500px 1100px at {gx}px 0px,rgba(255,247,214,.95) 0%,rgba(253,230,190,.6) 40%,rgba(253,230,190,0) 100%),"
             "linear-gradient(90deg,#efd9c0 0%,#f4dcc0 30%,#f6dfc4 45%,#f1d4b6 70%,#ead0b4 100%)")
    # taşma bölgesinde gökyüzü yok (fiziksel kesim) — yalnızca bloklar; panoda altın gök
    panel = (f'<div class="a" style="left:0;top:0;width:6100px;height:850px;background:linear-gradient(90deg,#fbf6ee 0%,{KREM} 100%);'
             'clip-path:polygon(0 0,100% 0,92% 100%,0 100%);box-shadow:30px 0 80px rgba(80,50,20,.18)"></div>'
             f'<div class="a" style="left:5560px;top:0;width:560px;height:850px;background:{ALTIN};'
             'clip-path:polygon(calc(100% - 26px) 0,100% 0,52px 100%,26px 100%)"></div>')
    icerik = f"""
  {mb.tilda(330, 220, 300, False)}
  {y(2050, 95, "MİA PARK OCEAN'DA", 150, 800, LAC, maxw=3350)}
  {y(2035, 260, "YAŞAM BAŞLIYOR.", 280, 800, "#a8742a", maxw=3350, ls="-.02em")}
  {y(2055, 585, "60 AY SABİT TAKSİTLE EV SAHİBİ OLMANIN TAM ZAMANI", 56, 700, LAC, sinif="kas", maxw=3300)}
  {kart(8750, "1+1", "39.900")}
  {kart(10450, "2+1", "49.900")}
  {yok(12450, "faiz", "FAİZ")}
  {yok(13200, "banka", "BANKA")}
  {yok(13950, "kredi", "KREDİ")}
  {yok(14700, "ara", "ARA ÖDEME")}
  {mb.mia(16280, 130, 440, False)}
  {damga(17520, 370, 380, "SON", "DAİRELER", "KAÇIRMAYIN!", zemin="#c8482f", yazi="#fff")}"""
    return f"""
<div class="tasma">{tas}</div>
<div class="pano" style="background:{zemin}">
  {panel}
  {ic}
  {icerik}
  {v2.serit(r)}
</div>"""


TASARIMLAR = [(T, "gun-batimi-gecisli")]


def main():
    gecici = tempfile.mkdtemp(prefix="mega9-")
    isler = []
    for i, (fn, ad) in enumerate(TASARIMLAR, 1):
        hp = os.path.join(gecici, f"{i}.html")
        open(hp, "w", encoding="utf-8").write(v7.sayfa(fn()))
        isler.append(dict(html=hp, w=TW, h=mb.TH, dsf=0.5, dilim=TW, cikti=os.path.join(gecici, f"{i}"), no=i, ad=ad))
    npm = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    env = {**os.environ, "NODE_PATH": npm}
    if "--pdf" in sys.argv:
        hedef = os.path.join(OUT, "duzenlenebilir-pdf")
        os.makedirs(hedef, exist_ok=True)
        for is_ in isler:
            is_["pdf"] = os.path.join(hedef, f"{is_['no']:02d}-{is_['ad']}.pdf")
        jp = os.path.join(gecici, "pdf.json")
        json.dump(isler, open(jp, "w"))
        subprocess.run(["node", os.path.join(ROOT, "scripts", "mega-bilbord", "pdf.cjs"), jp], check=True, env=env)
        return
    jp = os.path.join(gecici, "isler.json")
    json.dump(isler, open(jp, "w"))
    subprocess.run(["node", os.path.join(ROOT, "scripts", "mega-bilbord", "render.cjs"), jp], check=True, env=env)
    os.makedirs(OUT, exist_ok=True)
    for is_ in isler:
        tam = Image.open(json.load(open(is_["cikti"] + ".json"))[0]).convert("RGBA")
        yol = os.path.join(OUT, f"{is_['no']:02d}-{is_['ad']}.jpg")
        v2.sunum(tam, is_["no"], is_["ad"], yol)
        print("  →", os.path.relpath(yol, ROOT))


if __name__ == "__main__":
    main()
