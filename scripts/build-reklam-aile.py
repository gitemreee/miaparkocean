#!/usr/bin/env python3
"""
Aile temalı satış kreatifleri — "Ailenize Yeni Bir Yuva" düzeninin çeşitlemeleri (2x çizilir).

Her kreatif üç oranda çıkar: 9x16 (Story/Reels), 4x5 (akış), 1x1 (kare).
Düzen: beyaz üstte başlık · sağda lacivert/altın fiyat kartı + kırmızı etiket · solda kesilmiş
aile fotoğrafı (signage-source/aile) · arkada proje görseli · lacivert alt bant
(Tilda İnşaat + MİA PARK OCEAN, 444 10 58, WhatsApp 0540 028 00 41).

    python3.13 scripts/build-reklam-aile.py
"""

import json
import os
import subprocess
import tempfile

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "sosyal-medya", "reklam-aile")
FONT = os.path.join(ROOT, "brand-source", "fonts", "Montserrat-var.ttf")
F = lambda *p: "file://" + os.path.join(ROOT, *p)
TILDA, MIA = F("public", "brand", "vektor", "tilda-beyaz.svg"), F("public", "brand", "vektor", "mia-beyaz.svg")
FOTO = lambda ad: F("sosyal-medya", "bitmis-fotograflar", ad)

LACI, ALTIN, KIRMIZI = "#14306b", "#c9a24a", "#e1262f"

WA = ('<svg viewBox="0 0 24 24" style="width:{s}px;height:{s}px;fill:#25d366;flex:none">'
      '<path d="M17.5 14.4c-.3-.2-1.7-.8-2-.9-.3-.1-.5-.2-.7.2-.2.3-.7.9-.9 1.1-.2.2-.3.2-.6.1-.3-.2-1.2-.5-2.3-1.4-.9-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6.1-.1.3-.3.4-.5.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5 0-.1-.7-1.6-.9-2.2-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.4s1.1 2.8 1.2 3c.2.2 2.1 3.2 5 4.5.7.3 1.2.5 1.7.6.7.2 1.3.2 1.8.1.6-.1 1.7-.7 1.9-1.3.2-.7.2-1.2.2-1.3-.1-.2-.3-.3-.6-.4z"/>'
      '<path d="M12 2C6.5 2 2 6.5 2 12c0 1.8.5 3.5 1.3 5L2 22l5.1-1.3c1.4.8 3.1 1.2 4.9 1.2 5.5 0 10-4.5 10-10S17.5 2 12 2zm0 18.2c-1.6 0-3.1-.4-4.4-1.2l-.3-.2-3 .8.8-2.9-.2-.3C4 15 3.6 13.5 3.6 12 3.6 7.4 7.4 3.6 12 3.6S20.4 7.4 20.4 12 16.6 20.2 12 20.2z"/></svg>')

# Kesilmiş aile fotoğrafları: (dosya, en/boy oranı)
AILELER = {
    "anahtar": (F("signage-source", "aile", "aile2-kesik.png"), 1654 / 1694),   # anne-baba-kız, anahtar
    "sevinc": (F("signage-source", "aile", "aile-kesik.png"), 2243 / 1695),     # dört kişi, kollar havada
}

# Oran başına sabit düzen. aile: {tip: (yükseklik, sol, alt kenar y)}
BICIMLER = {
    "9x16": dict(w=1080, h=1920, r_top=420, beyaz=900, b_top=132, b=(76, 128, 76, 29), bant=1470,
                 k_x=470, k_y=610, k_w=560, k_b=80, k_kay=70, i_y=1622, i=(70, 84, 30),
                 aile={"anahtar": (720, -30, 1720), "sevinc": (570, -16, 1722)}),
    "4x5": dict(w=1080, h=1350, r_top=300, beyaz=640, b_top=64, b=(58, 100, 58, 23), bant=960,
                k_x=520, k_y=420, k_w=510, k_b=66, k_kay=56, i_y=1070, i=(52, 66, 25),
                aile={"anahtar": (560, -24, 1150), "sevinc": (410, -24, 1150)}),
    "1x1": dict(w=1080, h=1080, r_top=250, beyaz=520, b_top=46, b=(46, 84, 46, 19), bant=760,
                k_x=570, k_y=330, k_w=460, k_b=56, k_kay=50, i_y=852, i=(42, 56, 22),
                aile={"anahtar": (490, -10, 920), "sevinc": (366, -20, 920)}),
}

KREATIFLER = [
    dict(ad="1-yeni-yuva", aile="anahtar", zemin=F("signage-source", "courtyard-pools.jpg"), pos="50% 50%",
         b1="Ailenize", b2="YENİ BİR YUVA", b3="699.000 TL Peşinatla", hap="BANKA YOK<br>FAİZ YOK", alt="KEFİL YOK · ARA ÖDEME YOK"),
    dict(ad="2-kiradan-kurtulun", aile="sevinc", zemin=F("signage-source", "entrance-gate.jpg"), pos="30% 50%",
         b1="Kiradan Kurtulun", b2="EV SAHİBİ OLUN", olcek=.9, b3="699.000 TL Peşinatla", hap="BANKA YOK<br>ARA ÖDEME YOK", alt=None),
    dict(ad="3-anahtariniz", aile="anahtar", zemin=FOTO("20-giris-gunesli.jpg"), pos="50% 45%",
         b1="Anahtarınız", b2="SİZİ BEKLİYOR", b3="MİA PARK OCEAN'da", hap="FAİZ YOK<br>KEFİL YOK", alt="BANKA YOK · ARA ÖDEME YOK"),
    dict(ad="4-cocuklariniza", aile="sevinc", zemin=FOTO("16-avlu-gunesli-kahve.jpg"), pos="50% 70%",
         b1="Çocuklarınıza", b2="GÜVENLİ BİR YUVA", olcek=.78, b3="Parklı, Bahçeli Site", hap="BANKA YOK<br>FAİZ YOK", alt=None),
    dict(ad="5-hayalinizdeki-ev", aile="anahtar", zemin=FOTO("23-giris-avlu-gun-batimi.jpg"), pos="50% 40%",
         b1="Hayalinizdeki Ev", b2="ARTIK ÇOK YAKIN", olcek=.84, b3="60 Ay Sabit Taksitle", hap="BANKA YOK<br>ARA ÖDEME YOK", alt="FAİZ YOK · KEFİL YOK"),
]


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


def kart(x, y, gen, b, kay, m):
    alt = (f'<div style="margin-top:{round(b * .26)}px;text-align:center"><span class="tek" style="display:inline-block;'
           f'padding:{round(b * .16)}px {round(b * .34)}px;border-radius:999px;background:#fff;font-size:{round(b * .31)}px;font-weight:800;'
           f'letter-spacing:.05em;color:{LACI};box-shadow:0 {round(b * .12)}px {round(b * .3)}px rgba(10,30,70,.25)">{m["alt"]}</span></div>'
           ) if m.get("alt") else ""
    return f"""
  <div class="a" style="left:{x}px;top:{y}px;width:{gen}px">
    <div style="border-radius:{round(b * .33)}px;overflow:hidden;box-shadow:0 {round(b * .3)}px {round(b * .6)}px rgba(10,30,70,.35)">
      <div style="background:{LACI};padding:{round(b * .38)}px 0 {round(b * .3)}px;text-align:center;color:#fff">
        <div class="k tek" style="font-size:{b}px">699.000<span style="font-size:{round(b * .36)}px;letter-spacing:0;margin-left:{round(b * .1)}px">TL'DEN</span></div>
        <div class="tek" style="margin-top:{round(b * .12)}px;font-size:{round(b * .4)}px;font-weight:800;letter-spacing:.06em">BAŞLAYAN PEŞİNAT</div>
      </div>
      <div style="height:{max(3, round(b * .07))}px;background:#fff"></div>
      <div class="k tek" style="background:{ALTIN};padding:{round(b * .32)}px 0 {round(b * .3)}px;text-align:center;font-size:{round(b * .62)}px;color:{LACI}">60 AY SABİT TAKSİT</div>
    </div>
    <div style="margin:{round(b * .4)}px 0 0 {kay}px;width:{gen - 2 * kay}px;padding:{round(b * .27)}px 0;border-radius:{round(b * .3)}px;
         background:{KIRMIZI};color:#fff;text-align:center;font-size:{round(b * .41)}px;font-weight:800;line-height:1.25;
         box-shadow:0 {round(b * .2)}px {round(b * .42)}px rgba(225,38,47,.35)">{m["hap"]}</div>
    {alt}
  </div>"""


def sayfa(p, m):
    w, h = p["w"], p["h"]
    b1, b2, b3, et = p["b"]
    logo, tel, wa = p["i"]
    aile_src, oran = AILELER[m["aile"]]
    a_h, a_x, a_alt = p["aile"][m["aile"]]
    y = p["i_y"]
    return f"""
  <img class="a" src="{m['zemin']}" style="left:0;top:{p['r_top']}px;width:{w}px;height:{h - p['r_top']}px;object-fit:cover;object-position:{m['pos']};
       -webkit-mask-image:linear-gradient(180deg,transparent 0%,#000 30%)">
  <div class="a" style="left:0;top:0;width:{w}px;height:{p['beyaz']}px;background:linear-gradient(180deg,#fff 55%,rgba(255,255,255,0))"></div>

  <div class="a" style="left:0;top:{p['b_top']}px;width:{w}px;text-align:center">
    <div class="k tek" style="font-size:{b1}px;color:{LACI}">{m['b1']}</div>
    <div class="k tek" style="margin-top:{round(b2 * .14)}px;font-size:{round(b2 * m.get('olcek', 1))}px;color:{ALTIN}">{m['b2']}</div>
    <div class="k tek" style="margin-top:{round(b2 * .1)}px;font-size:{b3}px;color:{LACI}">{m['b3']}</div>
    <div class="tek" style="margin-top:{round(et * .9)}px;font-size:{et}px;font-weight:600;letter-spacing:.2em;color:#4a5878">MİA PARK OCEAN · İZMİT</div>
  </div>

  <img class="a" src="{aile_src}" style="left:{a_x}px;top:{a_alt - a_h}px;height:{a_h}px;filter:drop-shadow(0 20px 30px rgba(10,30,60,.28))">
  <div class="a" style="left:0;top:{p['bant']}px;width:{w}px;height:{h - p['bant']}px;background:linear-gradient(180deg,rgba(20,48,107,0) 0%,rgba(20,48,107,.9) 36%,{LACI} 62%)"></div>
  {kart(p['k_x'], p['k_y'], p['k_w'], p['k_b'], p['k_kay'], m)}

  <div class="a" style="left:0;top:{y}px;width:{w}px;display:flex;align-items:center;justify-content:center;gap:{round(logo * .5)}px">
    <img src="{TILDA}" style="height:{logo}px"><span style="width:2px;height:{round(logo * 1.3)}px;background:rgba(255,255,255,.55)"></span>
    <img src="{MIA}" style="height:{round(logo * 1.45)}px"></div>
  <div class="a k tek" style="left:0;top:{y + round(logo * 1.75)}px;width:{w}px;text-align:center;font-size:{tel}px;color:#fff;letter-spacing:.01em">444 10 58</div>
  <div class="a" style="left:0;top:{y + round(logo * 1.75) + round(tel * 1.18)}px;width:{w}px;display:flex;align-items:center;justify-content:center;gap:{round(wa * .4)}px;color:#fff">
    {WA.format(s=round(wa * 1.1))}<span class="tek" style="font-size:{wa}px;font-weight:700;letter-spacing:.04em">0540 028 00 41</span>
    <span style="width:1px;height:{wa}px;background:rgba(255,255,255,.5);margin:0 {round(wa * .3)}px"></span>
    <span class="tek" style="font-size:{round(wa * .9)}px;font-weight:600;letter-spacing:.06em;opacity:.9">miaparkocean.com</span></div>
"""


def main():
    os.makedirs(OUT, exist_ok=True)
    gecici = tempfile.mkdtemp(prefix="aile-")
    isler = []
    for m in KREATIFLER:
        for oran, p in BICIMLER.items():
            ad = f"{m['ad']}-{oran}"
            hp = os.path.join(gecici, ad + ".html")
            open(hp, "w", encoding="utf-8").write(
                f'<!doctype html><html><head><meta charset="utf-8"><style>{css(p["w"], p["h"])}</style></head><body>{sayfa(p, m)}</body></html>')
            isler.append(dict(html=hp, w=p["w"], h=p["h"], dsf=2, dilim=p["w"], cikti=os.path.join(gecici, ad), ad=ad))
    jp = os.path.join(gecici, "isler.json")
    json.dump(isler, open(jp, "w"))
    npm = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    subprocess.run(["node", os.path.join(ROOT, "scripts", "mega-bilbord", "render.cjs"), jp], check=True,
                   env={**os.environ, "NODE_PATH": npm}, stdout=subprocess.DEVNULL)
    for is_ in isler:
        im = Image.open(json.load(open(is_["cikti"] + ".json"))[0]).convert("RGB")
        yol = os.path.join(OUT, f"mia-aile-{is_['ad']}.jpg")
        im.save(yol, quality=93)
        print("  →", os.path.relpath(yol, ROOT), im.size)


if __name__ == "__main__":
    main()
