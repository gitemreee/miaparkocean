#!/usr/bin/env python3
"""
"Ailenize Yeni Bir Yuva" düzeninde, YENİ fotoğraflarla altı kreatif (2x çizilir).

Düzen (müşterinin en çok beğendiği): beyaz üstte üç satır başlık · koyu/altın fiyat kartı +
kırmızı etiket · önde kesilmiş insan fotoğrafı · arkada proje görseli · altta koyu bant
(Tilda İnşaat + MİA PARK OCEAN, 444 10 58, WhatsApp 0540 028 00 41).

Fotoğraflar signage-source/insanlar/ altındadır (Canva ile üretildi, arka planı temizlendi):
  cift-koli · aile-dort · genc-kadin · olgun-cift · genc-aile · sirtta-cift
Her kreatifte fotoğraf, arka plan, renk ve kartın tarafı değişir.

Her biri 4x5 (1080x1350) ve 9x16 (1080x1920) çıkar.

    python3.13 scripts/build-reklam-yeni-yuzler.py
"""

import json
import os
import subprocess
import tempfile

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "sosyal-medya", "reklam-yeni-yuzler")
FONT = os.path.join(ROOT, "brand-source", "fonts", "Montserrat-var.ttf")
F = lambda *p: "file://" + os.path.join(ROOT, *p)
TILDA, MIA = F("public", "brand", "vektor", "tilda-beyaz.svg"), F("public", "brand", "vektor", "mia-beyaz.svg")
FOTO = lambda ad: F("sosyal-medya", "bitmis-fotograflar", ad)
SRC = lambda ad: F("signage-source", ad)
W = 1080
KIRMIZI = "#e1262f"

WA = ('<svg viewBox="0 0 24 24" style="width:{s}px;height:{s}px;fill:#25d366;flex:none">'
      '<path d="M17.5 14.4c-.3-.2-1.7-.8-2-.9-.3-.1-.5-.2-.7.2-.2.3-.7.9-.9 1.1-.2.2-.3.2-.6.1-.3-.2-1.2-.5-2.3-1.4-.9-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6.1-.1.3-.3.4-.5.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5 0-.1-.7-1.6-.9-2.2-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.4s1.1 2.8 1.2 3c.2.2 2.1 3.2 5 4.5.7.3 1.2.5 1.7.6.7.2 1.3.2 1.8.1.6-.1 1.7-.7 1.9-1.3.2-.7.2-1.2.2-1.3-.1-.2-.3-.3-.6-.4z"/>'
      '<path d="M12 2C6.5 2 2 6.5 2 12c0 1.8.5 3.5 1.3 5L2 22l5.1-1.3c1.4.8 3.1 1.2 4.9 1.2 5.5 0 10-4.5 10-10S17.5 2 12 2zm0 18.2c-1.6 0-3.1-.4-4.4-1.2l-.3-.2-3 .8.8-2.9-.2-.3C4 15 3.6 13.5 3.6 12 3.6 7.4 7.4 3.6 12 3.6S20.4 7.4 20.4 12 16.6 20.2 12 20.2z"/></svg>')

# Renk takımları: (koyu, vurgu)
LACI = ("#14306b", "#c9a24a")
PETROL = ("#0b4a5a", "#f29a2e")
YESIL = ("#124a3a", "#d4a94a")

# İnsan fotoğrafları: en/boy oranı (kırpılmış PNG)
INSAN = {"cift-koli": .77, "aile-dort": .962, "genc-kadin": .528, "olgun-cift": .787, "genc-aile": .634, "sirtta-cift": .576}

# Biçim sabitleri. b: (giriş, ana satır, üçüncü satır, etiket) yazı boyutları.
BICIM = {
    "4x5": dict(h=1350, r_top=300, beyaz=640, b_top=62, b=(58, 100, 58, 23), bant=960, k_y=424, k_w=488, k_b=64,
                i_y=1070, i=(52, 66, 25), alt=1160),
    "9x16": dict(h=1920, r_top=430, beyaz=920, b_top=150, b=(74, 124, 74, 28), bant=1440, k_y=640, k_w=520, k_b=70,
                 i_y=1590, i=(64, 80, 29), alt=1700),
}

# yuk: (4x5, 9x16) insan yüksekliği px · taraf: insanın durduğu taraf · kay: kenardan taşma (px, + içeri)
KREATIFLER = [
    dict(ad="1-kiradan-kurtulun", insan="cift-koli", yuk=(740, 980), taraf="sol", kay=(-24, -40), renk=LACI,
         zemin=SRC("entrance-gate.jpg"), pos="62% 50%",
         b1="Kiradan Kurtulun", b2="EV SAHİBİ OLUN", olcek=.9, b3="699.000 TL Peşinatla", hap="BANKA YOK<br>ARA ÖDEME YOK", serit="60 AY SABİT TAKSİT"),
    dict(ad="2-yeni-bir-yuva", insan="aile-dort", yuk=(610, 760), taraf="sag", kay=(-40, -110), renk=PETROL,
         zemin=SRC("courtyard-pools.jpg"), pos="50% 50%",
         b1="Ailenize", b2="YENİ BİR YUVA", b3="699.000 TL Peşinatla", hap="BANKA YOK<br>FAİZ YOK", serit="60 AY SABİT TAKSİT"),
    dict(ad="3-ilk-evine", insan="genc-kadin", yuk=(790, 1060), taraf="sol", kay=(30, 10), renk=LACI,
         zemin=FOTO("20-giris-gunesli.jpg"), pos="50% 42%",
         b1="İlk Evine", b2="699.000 TL", b3="Peşinat ile Sahip Ol", hap="BANKA YOK<br>KEFİL YOK", serit="60 AY SABİT TAKSİT"),
    dict(ad="4-anahtari-hazir", insan="olgun-cift", yuk=(730, 960), taraf="sag", kay=(-20, -60), renk=YESIL,
         zemin=FOTO("16-avlu-gunesli-kahve.jpg"), pos="50% 68%",
         b1="Yeni Evinizin", b2="ANAHTARI HAZIR", olcek=.86, b3="MİA PARK OCEAN'da", hap="FAİZ YOK<br>KEFİL YOK", serit="60 AY SABİT TAKSİT"),
    dict(ad="5-her-yere-yakin", insan="genc-aile", yuk=(800, 1070), taraf="sol", kay=(-10, -30), renk=PETROL,
         zemin=FOTO("17-drone-yalniz-site.jpg"), pos="50% 46%",
         b1="Yeni Eviniz", b2="HER YERE YAKIN", olcek=.88, b3="D-100'e 1 dk · Merkeze 5 dk", b3_olcek=.8, hap="BANKA YOK<br>FAİZ YOK", serit="60 AY SABİT TAKSİT"),
    dict(ad="6-60-ay-sabit-taksit", insan="sirtta-cift", yuk=(790, 980), taraf="sag", kay=(-10, -90), renk=YESIL,
         zemin=FOTO("23-giris-avlu-gun-batimi.jpg"), pos="50% 40%",
         b1="Banka Yok, Faiz Yok", b2="60 AY SABİT TAKSİT", olcek=.74, b3="699.000 TL Peşinatla", hap="KEFİL YOK<br>ARA ÖDEME YOK", serit="BANKASIZ · FAİZSİZ"),
]


def css(h):
    return f"""
@font-face {{ font-family: Mont; src: url("file://{FONT}"); font-weight: 100 900; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:{W}px; height:{h}px; overflow:hidden; position:relative; font-family:Mont,sans-serif;
       -webkit-font-smoothing:antialiased; background:#fff; }}
.a {{ position:absolute; }}
.tek {{ white-space:nowrap; }}
.k {{ font-weight:800; letter-spacing:-.02em; line-height:1; }}
"""


def kart(x, y, gen, b, m):
    koyu, vurgu = m["renk"]
    return f"""
  <div class="a" style="left:{x}px;top:{y}px;width:{gen}px">
    <div style="border-radius:{round(b * .33)}px;overflow:hidden;box-shadow:0 {round(b * .3)}px {round(b * .6)}px rgba(10,30,50,.35)">
      <div style="background:{koyu};padding:{round(b * .38)}px 0 {round(b * .3)}px;text-align:center;color:#fff">
        <div class="k tek" style="font-size:{b}px">699.000<span style="font-size:{round(b * .36)}px;letter-spacing:0;margin-left:{round(b * .1)}px">TL'DEN</span></div>
        <div class="tek" style="margin-top:{round(b * .12)}px;font-size:{round(b * .4)}px;font-weight:800;letter-spacing:.06em">BAŞLAYAN PEŞİNAT</div>
      </div>
      <div style="height:{max(3, round(b * .07))}px;background:#fff"></div>
      <div class="k tek" style="background:{vurgu};padding:{round(b * .32)}px 0 {round(b * .3)}px;text-align:center;font-size:{round(b * .6)}px;color:{koyu}">{m['serit']}</div>
    </div>
    <div style="margin:{round(b * .4)}px {round(gen * .13)}px 0;padding:{round(b * .27)}px 0;border-radius:{round(b * .3)}px;
         background:{KIRMIZI};color:#fff;text-align:center;font-size:{round(b * .41)}px;font-weight:800;line-height:1.25;
         box-shadow:0 {round(b * .2)}px {round(b * .42)}px rgba(225,38,47,.35)">{m['hap']}</div>
  </div>"""


def sayfa(oran, m):
    p = BICIM[oran]
    h = p["h"]
    i = 0 if oran == "4x5" else 1
    koyu, vurgu = m["renk"]
    b1, b2, b3, et = p["b"]
    logo, tel, wa = p["i"]
    a_h = m["yuk"][i]
    a_w = round(a_h * INSAN[m["insan"]])
    kay = m["kay"][i]
    sol = m["taraf"] == "sol"
    a_x = kay if sol else W - a_w - kay
    k_x = W - p["k_w"] - 44 if sol else 44
    y = p["i_y"]
    r, g, bl = (int(koyu[j:j + 2], 16) for j in (1, 3, 5))
    return f"""
  <img class="a" src="{m['zemin']}" style="left:0;top:{p['r_top']}px;width:{W}px;height:{h - p['r_top']}px;object-fit:cover;object-position:{m['pos']};
       -webkit-mask-image:linear-gradient(180deg,transparent 0%,#000 30%)">
  <div class="a" style="left:0;top:0;width:{W}px;height:{p['beyaz']}px;background:linear-gradient(180deg,#fff 55%,rgba(255,255,255,0))"></div>

  <div class="a" style="left:0;top:{p['b_top']}px;width:{W}px;text-align:center">
    <div class="k tek" style="font-size:{b1}px;color:{koyu}">{m['b1']}</div>
    <div class="k tek" style="margin-top:{round(b2 * .14)}px;font-size:{round(b2 * m.get('olcek', 1))}px;color:{vurgu}">{m['b2']}</div>
    <div class="k tek" style="margin-top:{round(b2 * .1)}px;font-size:{round(b3 * m.get('b3_olcek', 1))}px;color:{koyu}">{m['b3']}</div>
    <div class="tek" style="margin-top:{round(et * .9)}px;font-size:{et}px;font-weight:600;letter-spacing:.2em;color:#4a5878">MİA PARK OCEAN · İZMİT</div>
  </div>

  {kart(k_x, p['k_y'], p['k_w'], p['k_b'], m)}
  <img class="a" src="{F('signage-source', 'insanlar', m['insan'] + '.png')}" style="left:{a_x}px;top:{p['alt'] - a_h}px;height:{a_h}px;
       filter:drop-shadow(0 20px 30px rgba(10,30,50,.3))">
  <div class="a" style="left:0;top:{p['bant']}px;width:{W}px;height:{h - p['bant']}px;
       background:linear-gradient(180deg,rgba({r},{g},{bl},0) 0%,rgba({r},{g},{bl},.92) 36%,{koyu} 60%)"></div>

  <div class="a" style="left:0;top:{y}px;width:{W}px;display:flex;align-items:center;justify-content:center;gap:{round(logo * .5)}px">
    <img src="{TILDA}" style="height:{logo}px"><span style="width:2px;height:{round(logo * 1.3)}px;background:rgba(255,255,255,.55)"></span>
    <img src="{MIA}" style="height:{round(logo * 1.45)}px"></div>
  <div class="a k tek" style="left:0;top:{y + round(logo * 1.75)}px;width:{W}px;text-align:center;font-size:{tel}px;color:#fff;letter-spacing:.01em">444 10 58</div>
  <div class="a" style="left:0;top:{y + round(logo * 1.75) + round(tel * 1.18)}px;width:{W}px;display:flex;align-items:center;justify-content:center;gap:{round(wa * .4)}px;color:#fff">
    {WA.format(s=round(wa * 1.1))}<span class="tek" style="font-size:{wa}px;font-weight:700;letter-spacing:.04em">0540 028 00 41</span>
    <span style="width:1px;height:{wa}px;background:rgba(255,255,255,.5);margin:0 {round(wa * .3)}px"></span>
    <span class="tek" style="font-size:{round(wa * .9)}px;font-weight:600;letter-spacing:.06em;opacity:.9">miaparkocean.com</span></div>
"""


def main():
    os.makedirs(OUT, exist_ok=True)
    gecici = tempfile.mkdtemp(prefix="yuzler-")
    isler = []
    for m in KREATIFLER:
        for oran in BICIM:
            h = BICIM[oran]["h"]
            ad = f"{m['ad']}-{oran}"
            hp = os.path.join(gecici, ad + ".html")
            open(hp, "w", encoding="utf-8").write(
                f'<!doctype html><html><head><meta charset="utf-8"><style>{css(h)}</style></head><body>{sayfa(oran, m)}</body></html>')
            isler.append(dict(html=hp, w=W, h=h, dsf=2, dilim=W, cikti=os.path.join(gecici, ad), ad=ad))
    jp = os.path.join(gecici, "isler.json")
    json.dump(isler, open(jp, "w"))
    npm = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    subprocess.run(["node", os.path.join(ROOT, "scripts", "mega-bilbord", "render.cjs"), jp], check=True,
                   env={**os.environ, "NODE_PATH": npm}, stdout=subprocess.DEVNULL)
    for is_ in isler:
        im = Image.open(json.load(open(is_["cikti"] + ".json"))[0]).convert("RGB")
        yol = os.path.join(OUT, f"mia-yeni-{is_['ad']}.jpg")
        im.save(yol, quality=92)
        print("  →", os.path.relpath(yol, ROOT), im.size)


if __name__ == "__main__":
    main()
