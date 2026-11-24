#!/usr/bin/env python3
"""
MİA PARK OCEAN — "pro" reklam seti, 2. yarı (tasarım spec v3, yerleşim A4–A6).

  4-cok-kolay      Kum + koyu yeşil + turuncu · kontursuz kemer render, sunucu 1
  5-her-yere-yakin Gök mavisi + lacivert + mercan · ince çizgili mesafe listesi + render kartı, sunucu 2
  6-yeni-bir-yuva  Turkuaz + sarı · üç bant, kahraman havuzlu avlu, dört kişilik aile

Her biri 4x5 (1080x1350) ve 9x16 (1080x1920, içerik y 250–1580) olarak ayrı dizilir; 2x çizilir (2160 px).
Kurallar: kenar 72, tek sol hat, Montserrat 500/800 + Manrope, düz karo, kontur/glow/altın yok,
gölge yalnız fotoğraf kartında. Yardımcılar (logo, wa) build-reklam-cesit.py'den gelir.

    python3.13 scripts/build-reklam-pro-2.py            # hepsi
    python3.13 scripts/build-reklam-pro-2.py 5 9x16     # süzgeç (ad ya da oran içinde geçen)
"""

import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_s = importlib.util.spec_from_file_location("cesit", os.path.join(ROOT, "scripts", "build-reklam-cesit.py"))
c = importlib.util.module_from_spec(_s)
_s.loader.exec_module(c)
logo, wa, SRC, FOTO, FONTS = c.logo, c.wa, c.SRC, c.FOTO, c.FONTS

OUT = os.path.join(ROOT, "sosyal-medya", "reklam-pro")
GRAFIK = os.path.join(ROOT, "scripts", "reklam-grafik")
W, K = 1080, 72                      # tuval eni, kenar boşluğu

GECICI = tempfile.mkdtemp(prefix="pro2-")


def temiz_kesim(ad):
    """Yeşil perde kesiminin kenarındaki yeşil haleyi giderir (asıl dosyaya dokunmaz, geçici kopya üretir).
    Kenar bandında yeşil kanal (R+B)/2'ye indirilir, alfa 1 px içeri çekilir."""
    im = Image.open(os.path.join(ROOT, "signage-source", "aile", ad)).convert("RGBA")
    alfa = im.getchannel("A")
    ic = alfa.filter(ImageFilter.MinFilter(25)).filter(ImageFilter.GaussianBlur(4))     # kenardan ~12 px içerisi
    d = np.asarray(im).astype(np.float32)
    a = d[..., 3]
    bant = np.clip((255 - np.asarray(ic, dtype=np.float32)) / 255, 0, 1) * (a > 0)
    r, g, b = d[..., 0], d[..., 1], d[..., 2]
    sinir = (r + b) / 2
    fazla = np.clip(g - sinir, 0, None)
    d[..., 1] = g - fazla * bant
    dar = np.asarray(alfa.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(.6)), dtype=np.float32)
    d[..., 3] = np.minimum(a, dar) * (1 - np.clip(fazla / 60, 0, 1) * bant * .6)
    yol = os.path.join(GECICI, ad)
    Image.fromarray(np.clip(d, 0, 255).astype(np.uint8), "RGBA").save(yol)
    return "file://" + yol


SUNUCU1 = temiz_kesim("sunucu-kesik.png")    # 1122x2235
SUNUCU2 = temiz_kesim("sunucu2-kesik.png")   # 1051x2205
AILE = temiz_kesim("aile-kesik.png")         # 2243x1695

AVANTAJ = "Banka yok · Faiz yok · Kefil yok"


def css(h):
    return f"""
@font-face {{ font-family: Mont; src: url("file://{FONTS}/Montserrat-var.ttf"); font-weight: 100 900; }}
@font-face {{ font-family: Manr; src: url("file://{FONTS}/Manrope-400.ttf"); font-weight: 400; }}
@font-face {{ font-family: Manr; src: url("file://{FONTS}/Manrope-600.ttf"); font-weight: 600; }}
@font-face {{ font-family: Manr; src: url("file://{FONTS}/Manrope-700.ttf"); font-weight: 700; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:{W}px; height:{h}px; overflow:hidden; position:relative; font-family:Mont,sans-serif;
       -webkit-font-smoothing:antialiased; text-rendering:geometricPrecision; }}
.a {{ position:absolute; }}
.tek {{ white-space:nowrap; }}
.sat {{ display:flex; align-items:center; }}
img {{ display:block; }}
.etk {{ font-weight:700; letter-spacing:.14em; line-height:1; white-space:nowrap; }}
.giris {{ font-weight:500; letter-spacing:-.01em; line-height:1.1; white-space:nowrap; }}
.baslik {{ font-weight:800; letter-spacing:-.025em; line-height:.95; white-space:nowrap; }}
.rakam {{ font-weight:800; letter-spacing:-.03em; line-height:.95; font-variant-numeric:tabular-nums; white-space:nowrap; }}
.govde {{ font-family:Manr,sans-serif; font-weight:600; line-height:1.3; white-space:nowrap; }}
.tel {{ font-weight:800; letter-spacing:-.01em; line-height:1; white-space:nowrap; font-variant-numeric:tabular-nums; }}
"""


_G = {}


def grafik(ad, stil):
    """reklam-grafik/ad.svg'yi satır içi verir (currentColor çalışsın diye)."""
    if ad not in _G:
        _G[ad] = open(os.path.join(GRAFIK, ad + ".svg"), encoding="utf-8").read().strip()
    return re.sub(r"<svg ", f'<svg style="{stil}" preserveAspectRatio="none" ', _G[ad], count=1)


def logolar(renk, y, mia_h=72, tilda_h=30):
    """Sol üst MİA PARK OCEAN, sağ üst Tilda (üstünde minik MÜTEAHHİT); ikisi tek renk."""
    et = round(tilda_h * .43)
    blok = et + 9 + tilda_h
    return (f'<div class="a" style="left:{K}px;top:{y}px">{logo("mia", mia_h, renk)}</div>'
            f'<div class="a" style="right:{K}px;top:{y + (mia_h - blok) // 2}px;display:flex;flex-direction:column;align-items:flex-end;color:{renk}">'
            f'<div class="etk" style="font-size:{et}px;letter-spacing:.3em;margin-right:-.3em;opacity:.7">MÜTEAHHİT</div>'
            f'<div style="margin-top:9px">{logo("tilda", tilda_h, renk)}</div></div>')


def vurgu(kelime, renk, cizgi=None):
    """Başlıktaki tek vurgu kelimesi; cizgi renk verilirse altında el çizimi alt çizgi."""
    alt = (grafik("alt-cizgi", f"position:absolute;left:-3%;bottom:-.13em;width:106%;height:.2em;z-index:-1;color:{cizgi}")
           if cizgi else "")
    return f'<span style="position:relative;display:inline-block;color:{renk};z-index:0">{kelime}{alt}</span>'


def baslik_blok(y, giris, satirlar, renk, story, avantaj_renk=None, boy=None):
    """Giriş satırı + sıkı başlık (+ sessiz avantaj satırı); hepsi sol hatta."""
    g, b, v = (52, 120, 30) if story else (46, 104, 28)
    b = boy or b
    av = (f'<div class="govde" style="margin-top:{round(b * .26)}px;font-size:{v}px;color:{avantaj_renk}">{AVANTAJ}</div>'
          if avantaj_renk else "")
    return (f'<div class="a" style="left:{K}px;top:{y}px;color:{renk};z-index:3">'
            f'<div class="giris" style="font-size:{g}px">{giris}</div>'
            f'<div class="baslik" style="margin-top:{round(b * .1)}px;font-size:{b}px">{"<br>".join(satirlar)}</div>{av}</div>')


def fiyat_karo(x, y_alt, en, zemin, yazi, story, h_tuval, z=4, rakam=None):
    """Dik, düz fiyat karosu: etiket → 699.000 → açıklama → ince çizgi → 60 ay sabit taksit."""
    e, r, a, i, py, px = (24, 120, 30, 44, 32, 40) if story else (22, 104, 26, 38, 28, 36)
    r = rakam or r
    return (f'<div class="a" style="left:{x}px;bottom:{h_tuval - y_alt}px;width:{en}px;padding:{py}px {px}px {py - 2}px;background:{zemin};color:{yazi};border-radius:20px;z-index:{z}">'
            f'<div class="etk" style="font-size:{e}px">PEŞİNAT</div>'
            f'<div class="rakam" style="margin-top:{round(r * .09)}px;font-size:{r}px">699.000</div>'
            f'<div class="tek" style="margin-top:{round(r * .07)}px;font-size:{a}px;font-weight:600;line-height:1.15">TL\'den başlayan peşinat</div>'
            f'<div style="margin:{round(a * .65)}px 0 {round(a * .55)}px;height:2px;background:{yazi};opacity:.2"></div>'
            f'<div class="tek" style="font-size:{i}px;font-weight:700;letter-spacing:-.01em;line-height:1.1">60 ay sabit taksit</div></div>')


def iletisim(renk, wa_renk, boy=52):
    return (f'<span class="tel" style="font-size:{boy}px;color:{renk}">444 10 58</span>'
            f'<span class="sat" style="gap:{round(boy * .3)}px">{wa(round(boy * .92), wa_renk)}'
            f'<span class="tel" style="font-size:{boy}px;color:{renk}">0540 028 00 41</span></span>')


def serit(zemin, renk, wa_renk="#25D366", h=132):
    """4:5 iletişim şeridi: altta 132 px, tek satır."""
    return (f'<div class="a sat" style="left:0;right:0;bottom:0;height:{h}px;padding:0 {K}px;justify-content:space-between;background:{zemin};z-index:6">'
            f'{iletisim(renk, wa_renk)}</div>')


def hap(y, zemin, renk, wa_renk="#25D366", h=108):
    """Story iletişim hapı: x 72–1008, güvenli alanın (y 1580) hemen üstünde biter."""
    return (f'<div class="a sat" style="left:{K}px;right:{K}px;top:{y}px;height:{h}px;padding:0 48px;justify-content:space-between;background:{zemin};border-radius:999px;z-index:6">'
            f'{iletisim(renk, wa_renk, 50)}</div>')


def kisi(src, h, stil, ayna=False, z=3, kirp=0):
    """Kesilmiş insan görseli. kirp: alttan gizlenecek px (kesim bir karonun/şeridin arkasında bitsin diye)."""
    return (f'<img class="a" src="{src}" style="height:{h}px;{stil};z-index:{z};'
            f'{"transform:scaleX(-1);" if ayna else ""}{f"clip-path:inset(0 0 {kirp}px 0);" if kirp else ""}">')


def nokta(stil, renk, opak=.16):
    return grafik("nokta-deseni", f"position:absolute;{stil};color:{renk};opacity:{opak}")


# ------------------------------------------------------------ A4 · kemer (Kum)

def a4(story):
    ZEMIN, KOYU, AKSAN = "#F6EAD7", "#134B3F", "#F28C1B"
    foto = FOTO("20-giris-gunesli.jpg")          # 1536x2752, güneşli giriş
    if not story:
        h = 1350
        return f"""<body style="background:{ZEMIN}">
  {logolar(KOYU, 72)}
  {baslik_blok(176, "Ev sahibi olmak", [f"artık çok {vurgu('kolay', AKSAN, AKSAN)}"], KOYU, False, KOYU, boy=112)}
  <div class="a" style="left:432px;top:424px;width:576px;height:794px;border-radius:288px 288px 0 0;overflow:hidden;z-index:1">
    <img src="{foto}" style="width:100%;height:100%;object-fit:cover;object-position:50% 56%"></div>
  {kisi(SUNUCU1, 770, "left:104px;bottom:132px")}
  {fiyat_karo(452, 1198, 536, AKSAN, KOYU, False, h)}
  {serit(KOYU, "#FFFFFF")}
</body>"""
    h = 1920
    # Story: kemer solda (başlığın sol hattında), sunucu sağda aynalı; karo sağ altta sunucunun önünde, kesim karonun arkasında biter.
    return f"""<body style="background:{ZEMIN}">
  {logolar(KOYU, 250, 84, 34)}
  {baslik_blok(374, "Ev sahibi olmak", [f"artık çok {vurgu('kolay', AKSAN, AKSAN)}"], KOYU, True, KOYU)}
  <div class="a" style="left:72px;top:696px;width:528px;height:824px;border-radius:264px 264px 0 0;overflow:hidden;z-index:1;
       clip-path:polygon(0 0,100% 0,100% 734px,376px 734px,376px 100%,0 100%)">
    <img class="a" src="{foto}" style="left:0;top:-114px;width:528px"></div>
  {kisi(SUNUCU1, 1000, "left:504px;top:640px", ayna=True, kirp=640 + 1000 - 1400)}
  {fiyat_karo(448, 1440, 560, AKSAN, KOYU, True, h, rakam=114)}
  {hap(1466, KOYU, "#FFFFFF", h=110)}
  {nokta("right:72px;top:1640px;width:200px;height:200px", KOYU, .14)}
</body>"""


# ------------------------------------------------- A5 · liste + kart (Gök mavisi)

def a5(story):
    ZEMIN, KOYU, AKSAN, VURGU = "#DFF1FB", "#0B4F82", "#FF6B4A", "#1C8FD6"
    foto = FOTO("4-tepeden-capraz.jpg")          # 1536x2752, yol ve şehirle havadan
    yerler = [("1", "D-100 Karayolu"), ("3", "41 Burada AVM"), ("5", "Şehir Merkezi"), ("5", "Şehir Hastanesi")]
    CIZGI = "2px solid rgba(11,79,130,.2)"

    def liste(x, y, en, sat_h, dk, birim, etiket, kol):
        s = "".join(
            f'<div class="sat" style="height:{sat_h}px;border-top:{CIZGI}">'
            f'<div class="tek" style="width:{kol}px;color:{VURGU};font-weight:800;letter-spacing:-.03em;font-size:{dk}px;line-height:1">{d}'
            f'<span style="font-size:{birim}px;font-weight:700;letter-spacing:0;margin-left:.2em">dk</span></div>'
            f'<div class="govde" style="font-size:{etiket}px;color:{KOYU}">{ad}</div></div>' for d, ad in yerler)
        return f'<div class="a" style="left:{x}px;top:{y}px;width:{en}px;border-bottom:{CIZGI};z-index:2">{s}</div>'

    def kart(x, y, boy, foto_ust, pin):
        en = W - x
        return (f'<div class="a" style="left:{x}px;top:{y}px;width:{en}px;height:{boy}px;border-radius:28px 0 0 28px;overflow:hidden;'
                f'box-shadow:0 16px 40px rgba(11,79,130,.14);z-index:1">'
                f'<img class="a" src="{foto}" style="left:0;top:{foto_ust}px;width:{en}px;filter:saturate(1.12) contrast(1.04) brightness(1.03)">'
                f'{grafik("konum-pini", f"position:absolute;left:{pin[0]}px;top:{pin[1]}px;width:{pin[2]}px;height:{pin[2]}px;color:{AKSAN}")}</div>')

    def yatay_karo(y, boy, e, r, a, i):
        return (f'<div class="a sat" style="left:{K}px;right:{K}px;top:{y}px;height:{boy}px;padding:0 40px;background:#FFFFFF;color:{KOYU};border-radius:20px;z-index:4">'
                f'<div><div class="etk" style="font-size:{e}px;color:{VURGU}">PEŞİNAT</div>'
                f'<div class="rakam" style="margin-top:8px;font-size:{r}px">699.000</div></div>'
                f'<div class="tek" style="margin-left:20px;align-self:flex-end;padding-bottom:{round((boy - e - 8 - r * .95) / 2 + r * .1)}px;font-size:{a}px;font-weight:600;line-height:1.18">TL\'den başlayan<br>peşinat</div>'
                f'<div style="margin:0 30px 0 auto;width:2px;height:{round(boy * .56)}px;background:{KOYU};opacity:.2;flex:none"></div>'
                f'<div class="tek" style="font-size:{i}px;font-weight:700;letter-spacing:-.01em;line-height:1.12">60 ay<br>sabit taksit</div></div>')

    if not story:
        return f"""<body style="background:{ZEMIN}">
  {logolar(KOYU, 72)}
  {baslik_blok(176, "Yeni eviniz", [f"her yere {vurgu('yakın', AKSAN)}"], KOYU, False, KOYU, boy=112)}
  {liste(72, 462, 400, 142, 62, 28, 28, 138)}
  {kart(512, 462, 570, -384, (190, 262, 76))}
  {kisi(SUNUCU2, 716, "left:686px;top:400px", ayna=True, kirp=400 + 716 - 1130)}
  {yatay_karo(1050, 144, 22, 84, 24, 34)}
  {serit(KOYU, "#FFFFFF")}
</body>"""
    return f"""<body style="background:{ZEMIN}">
  {logolar(KOYU, 250, 84, 34)}
  {baslik_blok(374, "Yeni eviniz", ["her yere", vurgu('yakın', AKSAN)], KOYU, True, KOYU)}
  {liste(72, 792, 368, 116, 66, 28, 30, 128)}
  {kart(480, 792, 504, -416, (176, 246, 80))}
  {kisi(SUNUCU2, 880, "left:632px;top:600px", ayna=True, kirp=600 + 880 - 1400)}
  {yatay_karo(1296, 156, 24, 88, 25, 36)}
  {hap(1472, KOYU, "#FFFFFF", h=104)}
  {nokta("left:72px;top:1640px;width:200px;height:200px", KOYU, .12)}
</body>"""


# ----------------------------------------------------- A6 · üç bant (Turkuaz)

def a6(story):
    ZEMIN, KOYU, AKSAN, ACIK = "#12A5A0", "#0A4F52", "#FFC93C", "#E3F6F4"
    foto = SRC("courtyard-pools.jpg")            # 4096x2294, havuzlu avlu

    def bantlar(y1, y2, konum):
        return (f'<div class="a" style="left:0;top:0;width:{W}px;height:{y1}px;background:{ACIK}"></div>'
                f'<img class="a" src="{foto}" style="left:0;top:{y1}px;width:{W}px;height:{y2 - y1}px;object-fit:cover;object-position:{konum};'
                f'filter:saturate(1.1) brightness(1.04);z-index:1">'
                f'<div class="a" style="left:0;top:{y2}px;width:{W}px;bottom:0;background:{ZEMIN};z-index:4"></div>')

    def teklif(y, e, r, a, b, i, v=0):
        alt = (f'<div style="margin-top:22px;height:2px;background:#FFFFFF;opacity:.2"></div>'
               f'<div class="govde" style="margin-top:14px;font-size:{v}px;opacity:.92">{AVANTAJ}</div>') if v else ""
        return (f'<div class="a" style="left:{K}px;right:{K}px;top:{y}px;color:#FFFFFF;z-index:5"><div class="sat">'
                f'<div><div class="etk" style="font-size:{e}px;opacity:.85">PEŞİNAT</div>'
                f'<div class="rakam" style="margin-top:{round(r * .09)}px;font-size:{r}px;color:{AKSAN}">699.000</div>'
                f'<div class="tek" style="margin-top:{round(r * .07)}px;font-size:{a}px;font-weight:600;line-height:1.15">TL\'den başlayan peşinat</div></div>'
                f'<div style="margin:0 auto;width:2px;align-self:stretch;background:#FFFFFF;opacity:.2;flex:none"></div>'
                f'<div><div class="rakam" style="font-size:{b}px">60 ay</div>'
                f'<div class="tek" style="margin-top:{round(b * .1)}px;font-size:{i}px;font-weight:700;letter-spacing:-.01em;line-height:1.1">sabit taksit</div></div>'
                f'</div>{alt}</div>')

    if not story:
        return f"""<body style="background:{ZEMIN}">
  {bantlar(444, 916, "50% 78%")}
  {logolar(KOYU, 72)}
  {baslik_blok(176, "Ailenize", ["yeni bir", vurgu('yuva', ZEMIN, AKSAN)], KOYU, False)}
  {kisi(AILE, 544, "left:340px;top:372px", z=2)}
  {teklif(946, 22, 104, 26, 76, 38, 26)}
  {serit("#FFFFFF", KOYU)}
</body>"""
    return f"""<body style="background:{ZEMIN}">
  {bantlar(772, 1232, "50% 80%")}
  {logolar(KOYU, 250, 84, 34)}
  {baslik_blok(374, "Ailenize", ["yeni bir", vurgu('yuva', ZEMIN, AKSAN)], KOYU, True, KOYU)}
  {kisi(AILE, 540, "left:322px;top:692px", z=2)}
  {teklif(1264, 24, 112, 28, 84, 42)}
  {hap(1470, "#FFFFFF", KOYU, h=104)}
  {grafik("dalga", f"position:absolute;left:{K}px;top:1700px;width:936px;height:70px;color:#FFFFFF;opacity:.14;z-index:5")}
</body>"""


TASARIMLAR = [("4-cok-kolay", a4), ("5-her-yere-yakin", a5), ("6-yeni-bir-yuva", a6)]
BICIMLER = [("4x5", 1350), ("9x16", 1920)]


def main():
    suzgec = sys.argv[1:]
    os.makedirs(OUT, exist_ok=True)
    gecici = GECICI
    isler = []
    for ad, fn in TASARIMLAR:
        for oran, h in BICIMLER:
            tam = f"{ad}-{oran}"
            if suzgec and not all(s in tam for s in suzgec):
                continue
            hp = os.path.join(gecici, tam + ".html")
            open(hp, "w", encoding="utf-8").write(
                f'<!doctype html><html lang="tr"><head><meta charset="utf-8"><style>{css(h)}</style></head>{fn(h > 1500)}</html>')
            isler.append(dict(html=hp, w=W, h=h, dsf=2, dilim=W, cikti=os.path.join(gecici, tam), ad=tam))
    jp = os.path.join(gecici, "isler.json")
    json.dump(isler, open(jp, "w"))
    npm = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    subprocess.run(["node", os.path.join(ROOT, "scripts", "mega-bilbord", "render.cjs"), jp], check=True,
                   env={**os.environ, "NODE_PATH": npm}, stdout=subprocess.DEVNULL)
    for is_ in isler:
        im = Image.open(json.load(open(is_["cikti"] + ".json"))[0]).convert("RGB")
        yol = os.path.join(OUT, f"mia-pro-{is_['ad']}.jpg")
        im.save(yol, quality=92)
        print("  →", os.path.relpath(yol, ROOT), im.size)


if __name__ == "__main__":
    main()
