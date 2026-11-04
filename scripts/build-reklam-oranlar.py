#!/usr/bin/env python3
"""
Lacivert/altın kartlı sunucu kreatifleri — farklı en-boy oranları (2x çizilir).

  ilk-evine            yeni kitle (soğuk): "İlk Evine 1 Milyon TL Peşinat ile Sahip Ol" — 5 oran
  hatirlatma-*         daha önce reklamı görenler (yeniden pazarlama) — 9x16, 4x5, 1x1

  9x16   1080x1920  Story / Reels / TikTok
  4x5    1080x1350  Instagram / Facebook akış
  1x1    1080x1080  Kare gönderi, Google Display
  191x1  1200x628   Meta / Google bağlantı reklamı
  16x9   1920x1080  YouTube, ekran, yatay pano

Öğeler: başlık · sunucu (signage-source/aile/sunucu2-kesik.png) · lacivert/altın fiyat kartı ·
kırmızı "Banka yok / Ara ödeme yok" · proje render'ı (signage-source/entrance-gate.jpg) ·
lacivert alt bant (Tilda İnşaat + MİA PARK OCEAN, 444 10 58, WhatsApp 0540 028 00 41).

    python3.13 scripts/build-reklam-oranlar.py
"""

import json
import os
import subprocess
import tempfile

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "sosyal-medya", "reklam-oranlar")
FONT = os.path.join(ROOT, "brand-source", "fonts", "Montserrat-var.ttf")
F = lambda *p: "file://" + os.path.join(ROOT, *p)
RENDER = F("signage-source", "entrance-gate.jpg")
SUNUCU = F("signage-source", "aile", "sunucu2-kesik.png")
TILDA, MIA = F("public", "brand", "vektor", "tilda-beyaz.svg"), F("public", "brand", "vektor", "mia-beyaz.svg")

LACI, ALTIN, KIRMIZI = "#14306b", "#c9a24a", "#e1262f"

WA = ('<svg viewBox="0 0 24 24" style="width:{s}px;height:{s}px;fill:#25d366;flex:none">'
      '<path d="M17.5 14.4c-.3-.2-1.7-.8-2-.9-.3-.1-.5-.2-.7.2-.2.3-.7.9-.9 1.1-.2.2-.3.2-.6.1-.3-.2-1.2-.5-2.3-1.4-.9-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6.1-.1.3-.3.4-.5.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5 0-.1-.7-1.6-.9-2.2-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.4s1.1 2.8 1.2 3c.2.2 2.1 3.2 5 4.5.7.3 1.2.5 1.7.6.7.2 1.3.2 1.8.1.6-.1 1.7-.7 1.9-1.3.2-.7.2-1.2.2-1.3-.1-.2-.3-.3-.6-.4z"/>'
      '<path d="M12 2C6.5 2 2 6.5 2 12c0 1.8.5 3.5 1.3 5L2 22l5.1-1.3c1.4.8 3.1 1.2 4.9 1.2 5.5 0 10-4.5 10-10S17.5 2 12 2zm0 18.2c-1.6 0-3.1-.4-4.4-1.2l-.3-.2-3 .8.8-2.9-.2-.3C4 15 3.6 13.5 3.6 12 3.6 7.4 7.4 3.6 12 3.6S20.4 7.4 20.4 12 16.6 20.2 12 20.2z"/></svg>')


def css(w, h):
    return f"""
@font-face {{ font-family: Mont; src: url("file://{FONT}"); font-weight: 100 900; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:{w}px; height:{h}px; overflow:hidden; position:relative; font-family:Mont,sans-serif;
       -webkit-font-smoothing:antialiased; background:#fff; }}
.a {{ position:absolute; }}
.tek {{ white-space:nowrap; }}
.k {{ font-weight:800; letter-spacing:-.02em; line-height:1; }}
"""


def baslik(x, y, hiza, b1, b2, b3, etiket, genislik=None, m=None):
    """Üç satır başlık + MİA PARK OCEAN · İZMİT etiketi. b*: (yazı boyutu, satır arası üst boşluk)."""
    g = f"width:{genislik}px;" if genislik else ""
    return f"""
  <div class="a" style="left:{x}px;top:{y}px;{g}text-align:{hiza}">
    <div class="k tek" style="font-size:{b1}px;color:{LACI}">{m['b1']}</div>
    <div class="k tek" style="margin-top:{round(b2 * .14)}px;font-size:{round(b2 * m.get('b2_olcek', 1))}px;color:{ALTIN}">{m['b2']}</div>
    <div class="k tek" style="margin-top:{round(b2 * .1)}px;font-size:{b3}px;color:{LACI}">{m['b3']}</div>
    <div class="tek" style="margin-top:{round(etiket * .9)}px;font-size:{etiket}px;font-weight:600;letter-spacing:.2em;color:#4a5878">MİA PARK OCEAN · İZMİT</div>
  </div>"""


def kart(x, y, gen, b, kirmizi_kaydir, m):
    """Lacivert/altın fiyat kartı + kırmızı hap + 'faiz yok · kefil yok'. b: ana yazı boyutu."""
    return f"""
  <div class="a" style="left:{x}px;top:{y}px;width:{gen}px">
    <div style="border-radius:{round(b * .33)}px;overflow:hidden;box-shadow:0 {round(b * .3)}px {round(b * .6)}px rgba(10,30,70,.35)">
      <div style="background:{LACI};padding:{round(b * .38)}px 0 {round(b * .3)}px;text-align:center;color:#fff">
        <div class="k tek" style="font-size:{b}px">1 MİLYON TL</div>
        <div class="tek" style="margin-top:{round(b * .12)}px;font-size:{round(b * .4)}px;font-weight:800;letter-spacing:.06em">PEŞİNAT</div>
      </div>
      <div style="height:{max(3, round(b * .07))}px;background:#fff"></div>
      <div class="k tek" style="background:{ALTIN};padding:{round(b * .32)}px 0 {round(b * .3)}px;text-align:center;font-size:{round(b * .62)}px;color:{LACI}">60 AY SABİT TAKSİT</div>
    </div>
    <div style="margin:{round(b * .4)}px 0 0 {kirmizi_kaydir}px;width:{gen - 2 * kirmizi_kaydir}px;padding:{round(b * .27)}px 0;border-radius:{round(b * .3)}px;
         background:{KIRMIZI};color:#fff;text-align:center;font-size:{round(b * .41)}px;font-weight:800;line-height:1.25;
         box-shadow:0 {round(b * .2)}px {round(b * .42)}px rgba(225,38,47,.35)">{m["hap"]}</div>
    <div style="margin-top:{round(b * .26)}px;text-align:center"><span class="tek" style="display:inline-block;padding:{round(b * .16)}px {round(b * .4)}px;
         border-radius:999px;background:#fff;font-size:{round(b * .36)}px;font-weight:800;letter-spacing:.06em;color:{LACI};
         box-shadow:0 {round(b * .12)}px {round(b * .3)}px rgba(10,30,70,.25)">{m["alt"]}</span></div>
  </div>"""


def iletisim_dikey(w, y, logo, tel, wa):
    return f"""
  <div class="a" style="left:0;top:{y}px;width:{w}px;display:flex;align-items:center;justify-content:center;gap:{round(logo * .5)}px">
    <img src="{TILDA}" style="height:{logo}px"><span style="width:2px;height:{round(logo * 1.3)}px;background:rgba(255,255,255,.55)"></span>
    <img src="{MIA}" style="height:{round(logo * 1.45)}px"></div>
  <div class="a k tek" style="left:0;top:{y + round(logo * 1.75)}px;width:{w}px;text-align:center;font-size:{tel}px;color:#fff;letter-spacing:.01em">444 10 58</div>
  <div class="a" style="left:0;top:{y + round(logo * 1.75) + round(tel * 1.18)}px;width:{w}px;display:flex;align-items:center;justify-content:center;gap:{round(wa * .4)}px;color:#fff">
    {WA.format(s=round(wa * 1.1))}<span class="tek" style="font-size:{wa}px;font-weight:700;letter-spacing:.04em">0540 028 00 41</span>
    <span style="width:1px;height:{wa}px;background:rgba(255,255,255,.5);margin:0 {round(wa * .3)}px"></span>
    <span class="tek" style="font-size:{round(wa * .9)}px;font-weight:600;letter-spacing:.06em;opacity:.9">miaparkocean.com</span></div>"""


def dikey(w, h, p, m):
    """9x16 · 4x5 · 1x1: ortalı başlık, solda sunucu, sağda kart, altta lacivert bant."""
    return f"""
  <img class="a" src="{RENDER}" style="left:0;top:{p['r_top']}px;width:{w}px;height:{h - p['r_top']}px;object-fit:cover;object-position:{p['r_pos']};
       -webkit-mask-image:linear-gradient(180deg,transparent 0%,#000 30%)">
  <div class="a" style="left:0;top:0;width:{w}px;height:{p['beyaz']}px;background:linear-gradient(180deg,#fff 55%,rgba(255,255,255,0))"></div>
  {baslik(0, p['b_top'], 'center', *p['b'], genislik=w, m=m)}
  <div class="a" style="left:0;top:{p['bant']}px;width:{w}px;height:{h - p['bant']}px;background:linear-gradient(180deg,rgba(20,48,107,0) 0%,rgba(20,48,107,.9) 36%,{LACI} 62%)"></div>
  <img class="a" src="{m['sunucu']}" style="left:{p['s_x']}px;top:{p['s_y']}px;height:{p['s_h']}px;filter:drop-shadow(0 20px 30px rgba(10,30,60,.25))">
  {kart(p['k_x'], p['k_y'], p['k_w'], p['k_b'], p['k_kay'], m)}
  {iletisim_dikey(w, p['i_y'], *p['i'])}
"""


def yatay(w, h, p, m):
    """1.91x1 · 16x9: solda başlık, ortada sunucu, sağda kart; altta lacivert şerit."""
    bh = p['bant_h']
    return f"""
  <img class="a" src="{RENDER}" style="left:0;top:0;width:{w}px;height:{h}px;object-fit:cover;object-position:{p['r_pos']}">
  <div class="a" style="left:0;top:0;width:{round(w * .62)}px;height:{round(h * p['beyaz'])}px;
       background:linear-gradient(90deg,#fff 0%,#fff 58%,rgba(255,255,255,0) 100%);
       -webkit-mask-image:linear-gradient(180deg,#000 62%,transparent 100%)"></div>
  {baslik(p['b_x'], p['b_y'], 'left', *p['b'], m=m)}
  <div class="a" style="left:0;top:{h - bh}px;width:{w}px;height:{bh}px;background:{LACI}"></div>
  <div class="a" style="left:0;top:{h - bh - round(bh * .6)}px;width:{w}px;height:{round(bh * .6)}px;background:linear-gradient(180deg,rgba(20,48,107,0),rgba(20,48,107,.55))"></div>
  <img class="a" src="{m['sunucu']}" style="left:{p['s_x']}px;top:{p['s_y']}px;height:{p['s_h']}px;filter:drop-shadow(0 20px 30px rgba(10,30,60,.25))">
  {kart(p['k_x'], p['k_y'], p['k_w'], p['k_b'], p['k_kay'], m)}
  <div class="a" style="left:{p['b_x']}px;top:{h - bh}px;height:{bh}px;display:flex;align-items:center;gap:{round(p['logo'] * .5)}px">
    <img src="{TILDA}" style="height:{p['logo']}px"><span style="width:2px;height:{round(p['logo'] * 1.3)}px;background:rgba(255,255,255,.55)"></span>
    <img src="{MIA}" style="height:{round(p['logo'] * 1.45)}px"></div>
  <div class="a" style="right:{p['b_x']}px;top:{h - bh}px;height:{bh}px;display:flex;flex-direction:column;align-items:flex-end;justify-content:center;color:#fff">
    <div class="k tek" style="font-size:{p['tel']}px;letter-spacing:.01em">444 10 58</div>
    <div style="margin-top:{round(p['wa'] * .35)}px;display:flex;align-items:center;gap:{round(p['wa'] * .4)}px">
      {WA.format(s=round(p['wa'] * 1.1))}<span class="tek" style="font-size:{p['wa']}px;font-weight:700;letter-spacing:.04em">0540 028 00 41</span></div>
  </div>
"""


BICIMLER = [
    ("9x16", 1080, 1920, dikey, dict(
        r_top=420, r_pos="13% 50%", beyaz=900, b_top=132, b=(76, 128, 76, 29), bant=1470,
        s_x=-70, s_y=600, s_h=1320, k_x=395, k_y=610, k_w=560, k_b=80, k_kay=70,
        i_y=1622, i=(70, 84, 30))),
    ("4x5", 1080, 1350, dikey, dict(
        r_top=300, r_pos="13% 50%", beyaz=640, b_top=64, b=(58, 100, 58, 23), bant=960,
        s_x=-40, s_y=410, s_h=1000, k_x=410, k_y=420, k_w=520, k_b=68, k_kay=60,
        i_y=1070, i=(52, 66, 25))),
    ("1x1", 1080, 1080, dikey, dict(
        r_top=250, r_pos="13% 60%", beyaz=520, b_top=46, b=(46, 84, 46, 19), bant=760,
        s_x=-10, s_y=318, s_h=820, k_x=440, k_y=330, k_w=460, k_b=56, k_kay=50,
        i_y=852, i=(42, 56, 22))),
    ("191x1", 1200, 628, yatay, dict(
        beyaz=.62, r_pos="20% 62%", b_x=56, b_y=58, b=(34, 62, 32, 13), bant_h=120,
        s_x=478, s_y=96, s_h=640, k_x=790, k_y=44, k_w=360, k_b=44, k_kay=36,
        logo=40, tel=46, wa=19)),
    ("16x9", 1920, 1080, yatay, dict(
        beyaz=.6, r_pos="20% 62%", b_x=100, b_y=150, b=(58, 104, 56, 22), bant_h=200,
        s_x=860, s_y=170, s_h=1100, k_x=1360, k_y=110, k_w=480, k_b=64, k_kay=50,
        logo=66, tel=80, wa=30)),
]


# Kreatifler: "yeni" = soğuk kitle (ilk kez görenler), "hatirlatma" = daha önce reklamı görenler / etkileşenler.
KREATIFLER = [
    ("ilk-evine", dict(b1="İlk Evine", b2="1 MİLYON TL", b3="Peşinat ile Sahip Ol", hap="BANKA YOK<br>ARA ÖDEME YOK",
                       alt="FAİZ YOK · KEFİL YOK", sunucu=SUNUCU), None),
    ("hatirlatma-akliniz", dict(b1="Aklınız Hâlâ", b2="MİA PARK OCEAN'DA", b2_olcek=.68, b3="mı?",
                                hap="ÖDEME PLANINIZ İÇİN<br>HEMEN ARAYIN", alt="FAİZ YOK · BANKA YOK",
                                sunucu=F("signage-source", "aile", "sunucu-kesik.png")), ("9x16", "4x5", "1x1")),
    ("hatirlatma-daireniz", dict(b1="Yeni Daireniz", b2="SİZİ BEKLİYOR", b2_olcek=.92, b3="1 Milyon TL Peşinatla",
                                 hap="DAİRENİZİ SEÇİN<br>YERİNİZİ AYIRTIN", alt="60 AY · ARA ÖDEME YOK",
                                 sunucu=SUNUCU), ("9x16", "4x5", "1x1")),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    gecici = tempfile.mkdtemp(prefix="oranlar-")
    isler = []
    for kad, m, oranlar in KREATIFLER:
        for ad, w, h, fn, p in BICIMLER:
            if oranlar and ad not in oranlar:
                continue
            ad = f"{kad}-{ad}"
            hp = os.path.join(gecici, ad + ".html")
            open(hp, "w", encoding="utf-8").write(
                f'<!doctype html><html><head><meta charset="utf-8"><style>{css(w, h)}</style></head><body>{fn(w, h, p, m)}</body></html>')
            isler.append(dict(html=hp, w=w, h=h, dsf=2, dilim=w, cikti=os.path.join(gecici, ad), ad=ad))
    jp = os.path.join(gecici, "isler.json")
    json.dump(isler, open(jp, "w"))
    npm = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    subprocess.run(["node", os.path.join(ROOT, "scripts", "mega-bilbord", "render.cjs"), jp], check=True,
                   env={**os.environ, "NODE_PATH": npm}, stdout=subprocess.DEVNULL)
    for is_ in isler:
        im = Image.open(json.load(open(is_["cikti"] + ".json"))[0]).convert("RGB")
        yol = os.path.join(OUT, f"mia-{is_['ad']}.jpg")
        im.save(yol, quality=93)
        print("  →", os.path.relpath(yol, ROOT), im.size)


if __name__ == "__main__":
    main()
