#!/usr/bin/env python3
"""
180 m dev pano — 2. tur, 10 tasarım önizlemesi (karar için; baskı sonra).

Grup geri bildirimi:
  · taşan bina maketi ve soldaki büyük Tilda kalsın
  · 1+0 çıkar → 1+1 ve 2+1 aylık taksit
  · üstte kocaman başlık: MİA PARK OCEAN'DA YAŞAM BAŞLIYOR! /
    60 AY SABİT TAKSİTLE EV SAHİBİ OLMANIN TAM ZAMANI!
  · tek fotoğraf yetmez → gerçek render'lardan galeri
  · sağda büyük MİA PARK OCEAN; Ocean Gayrimenkul küçük
  · altta şerit: web siteleri, telefon, Instagram, Facebook

Geometri, kahraman görsel, logolar ve yardımcılar 1. turdan
(build-mega-bilbord.py) alınır.

    python3.13 scripts/build-mega-bilbord-v2.py            # 10 sunum sayfası
    python3.13 scripts/build-mega-bilbord-v2.py --sadece 1,4
"""

import importlib.util as _il
import json
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont

Image.MAX_IMAGE_PIXELS = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_spec = _il.spec_from_file_location("mb1", os.path.join(ROOT, "scripts", "build-mega-bilbord.py"))
mb = _il.module_from_spec(_spec)
_spec.loader.exec_module(mb)

OUT = os.path.join(ROOT, "tabela", "mega-bilbord-180m-v2")
TW, TH, EXT, PH = mb.TW, mb.TH, mb.EXT, mb.PH
HX, HW = mb.HX, mb.HW
SERIT = 132                       # alt şerit yüksekliği (1,32 m)
ICERIK = PH - SERIT               # şeridin üstündeki alan

B1 = "MİA PARK OCEAN'DA YAŞAM BAŞLIYOR!"
B2 = "60 AY SABİT TAKSİTLE EV SAHİBİ OLMANIN TAM ZAMANI!"

FOTO = {
    "gece": "signage-source/night-gate-temiz.jpg",
    "avlu": "signage-source/courtyard-pools.jpg",
    "deniz": "signage-source/balkondan-deniz.jpg",
    "teras": "public/images/terrace-pergola.webp",
    "ic": "public/images/interior-bedroom.webp",
    "aksam": "public/images/hero-courtyard-dusk.webp",
}
ETIKET = {"gece": "GECE AYDINLATMASI", "avlu": "HAVUZLU AVLU", "deniz": "DENİZ MANZARASI",
          "teras": "BAHÇE TERASI", "ic": "İÇ MEKÂN", "aksam": "AKŞAM AVLUSU"}

CSS_EK = """
.serit { position: absolute; left: 0; bottom: 0; width: 18000px; height: 132px;
  display: flex; align-items: center; justify-content: space-evenly; }
.serit .oge { display: flex; align-items: center; gap: 22px; white-space: nowrap;
  font-weight: 700; font-size: 62px; letter-spacing: .01em; }
.serit .oge svg { width: 70px; height: 70px; flex: none; }
.serit .ayr { width: 3px; height: 76px; opacity: .35; background: currentColor; }
.serit .etk { font-weight: 600; font-size: 40px; letter-spacing: .22em; opacity: .8; }
.foto-k { position: absolute; background-size: cover; background-repeat: no-repeat;
  overflow: hidden; }
.foto-k .lbl { position: absolute; left: 0; right: 0; bottom: 0; padding: 18px 26px 16px;
  font-weight: 700; font-size: 38px; letter-spacing: .2em; color: #fff;
  background: linear-gradient(0deg, rgba(0,0,0,.6), rgba(0,0,0,0)); white-space: nowrap; }
.fiyat2 { position: absolute; border-radius: 40px; overflow: hidden; }
.fiyat2 .bas { text-align: center; font-weight: 800; font-size: 60px; letter-spacing: .05em;
  padding: 26px 0 22px; white-space: nowrap; }
.fiyat2 .sat { display: flex; align-items: baseline; justify-content: space-between;
  padding: 26px 46px 22px; white-space: nowrap; }
.fiyat2 .sat + .sat { border-top: 3px solid var(--cizgi); }
.fiyat2 .tip { font-weight: 800; font-size: 92px; }
.fiyat2 .tut { font-weight: 800; font-size: 120px; letter-spacing: -.03em; line-height: 1; }
.fiyat2 .tut small { font-size: .45em; letter-spacing: 0; margin-left: .08em; }
.fiyat2 .tut em { font-style: normal; font-size: .3em; letter-spacing: .12em; margin-left: .3em; opacity: .8; }
"""

# --- şerit ikonları (sade çizgi)
IK_WEB = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9">'
          '<circle cx="12" cy="12" r="9.5"/><path d="M2.5 12h19M12 2.5c3 3.2 3 15.8 0 19'
          'M12 2.5c-3 3.2-3 15.8 0 19"/></svg>')
IK_TEL = ('<svg viewBox="0 0 24 24" fill="currentColor"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 '
          '6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 '
          '17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/></svg>')
IK_IG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
         '<rect x="2.5" y="2.5" width="19" height="19" rx="5.5"/><circle cx="12" cy="12" r="4.4"/>'
         '<circle cx="17.6" cy="6.4" r="1.2" fill="currentColor" stroke="none"/></svg>')
IK_FB = ('<svg viewBox="0 0 24 24" fill="currentColor"><path d="M13.5 21.5v-8h2.7l.4-3.2h-3.1V8.3'
         'c0-.9.3-1.6 1.6-1.6h1.7V3.9c-.3 0-1.3-.1-2.5-.1-2.5 0-4.2 1.5-4.2 4.3v2.3H7.4v3.2h2.7v8z"/></svg>')


def serit(p):
    a = '<div class="ayr"></div>'
    ogeler = [
        f'<div class="oge"><span class="etk">TİLDA İNŞAAT</span>{IK_WEB}tildainsaat.com</div>',
        f'<div class="oge">{IK_IG}{IK_FB}@tildainsaat</div>',
        f'<div class="oge"><span class="etk">MİA PARK OCEAN</span>{IK_WEB}miaparkocean.com</div>',
        f'<div class="oge">{IK_WEB}miapark.com</div>',
        f'<div class="oge">{IK_IG}{IK_FB}@miaparkocean</div>',
        f'<div class="oge">{IK_TEL}0540 028 00 41</div>',
        f'<div class="oge"><span class="etk">TEK YETKİLİ SATIŞ</span>'
        f'{mb.ocean(74, p["serit_logo"], p["serit_su"])}</div>',
    ]
    return (f'<div class="serit" style="background:{p["serit"]};color:{p["serit_yazi"]}">'
            + a.join(ogeler) + '</div>')


def fiyat2(x, y, w, p):
    return f"""
<div class="fiyat2" style="left:{x}px;top:{y}px;width:{w}px;background:{p['panel']};
     color:{p['panel_yazi']};--cizgi:{p['panel_cizgi']};border:4px solid {p['panel_kenar']}">
  <div class="bas" style="background:{p['panel_bas']};color:{p['panel_bas_yazi']}">60 AY SABİT TAKSİT</div>
  <div class="sat"><span class="tip">1+1</span><span class="tut">39.900<small>₺</small><em>/ AY</em></span></div>
  <div class="sat"><span class="tip">2+1</span><span class="tut">49.900<small>₺</small><em>/ AY</em></span></div>
</div>"""


def foto(x, y, w, h, ad, pos="50% 50%", radius="28px", ek="", etiket=True):
    yol = os.path.join(ROOT, FOTO[ad])
    lbl = f'<div class="lbl">{ETIKET[ad]}</div>' if etiket else ""
    return (f'<div class="foto-k" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
            f'background-image:url(file://{yol});background-position:{pos};'
            f'border-radius:{radius};{ek}">{lbl}</div>')


def galeri(x0, x1, y, h, adlar, p, bicim="kose", etiket=True):
    n = len(adlar)
    ara = 70
    w = (x1 - x0 - ara * (n - 1)) / n
    s = []
    for i, ad in enumerate(adlar):
        x = round(x0 + i * (w + ara))
        if bicim == "kemer":
            r = f"{round(w / 2)}px {round(w / 2)}px 18px 18px"
            s.append(foto(x, y, round(w), h, ad, radius=r,
                          ek=f"box-shadow:0 0 0 6px {p['cerceve']}"))
        elif bicim == "egik":
            s.append(foto(x, y, round(w), h, ad, radius="0",
                          ek="clip-path:polygon(9% 0,100% 0,91% 100%,0 100%)"))
        elif bicim == "daire":
            d = min(round(w), h)
            s.append(foto(x + (round(w) - d) // 2, y + (h - d) // 2, d, d, ad, radius="50%",
                          ek=f"box-shadow:0 0 0 8px {p['cerceve']}", etiket=False))
        else:
            s.append(foto(x, y, round(w), h, ad, etiket=etiket,
                          ek=f"box-shadow:0 0 0 5px {p['cerceve']}"))
    return "".join(s)


def baslik(x, y, p, maxw, fs1=230, fs2=118, ara=290):
    v = p["vurgu"] or ""
    renk2 = p.get("vurgu_renk", p["yazi"])
    return (mb.yazi(x, y, B1, fs1, 800, p["yazi"], maxw=maxw)
            + mb.yazi(x + 6, y + ara, B2, fs2, 800, renk2, v, maxw=maxw))


def pano(p, icerik):
    return f"""
<div class="tasma">{mb.kahraman(False)}</div>
<div class="pano" style="background:{p['zemin']}">
  {icerik}
  {mb.kahraman(True)}
  {serit(p)}
</div>"""


# ---------------------------------------------------------------- paletler
def palet(taban, **ek):
    d = dict(taban)
    d.update(ek)
    return d


LAC = palet(mb.LACIVERT, cerceve="rgba(255,255,255,.85)", serit="#ffffff",
            serit_yazi="#0f2a4d", serit_logo="#0f4c9b", serit_su="#2f7fd6")
GOK = palet(mb.GOKYUZU, cerceve="#ffffff", serit="#0b2545", serit_yazi="#ffffff",
            serit_logo="#ffffff", serit_su="#5fb3ff")
KRM = palet(mb.KREM, cerceve="#ffffff", serit="#13212c", serit_yazi="#f3e6d2",
            serit_logo="#ffffff", serit_su="#5fb3ff")
TRK = palet(mb.TURKUAZ, cerceve="#ffffff", serit="#ffffff", serit_yazi="#05505b",
            serit_logo="#0f4c9b", serit_su="#2f7fd6")
GEC = palet(mb.LACIVERT, zemin="linear-gradient(180deg,#071225 0%,#0d2242 60%,#173a66 100%)",
            vurgu="turuncu", cerceve="rgba(255,255,255,.8)", serit="#ff7a2e",
            serit_yazi="#1a0d02", serit_logo="#1a0d02", serit_su="#ffffff",
            panel_bas="linear-gradient(90deg,#ff5a33,#ffb43a)", panel_bas_yazi="#1a0d02")
GUN = palet(mb.LACIVERT, zemin="linear-gradient(180deg,#2b2a63 0%,#8a3f6d 38%,#e0704a 72%,#f7b25a 100%)",
            vurgu=None, vurgu_renk="#ffe2a6", kas="#ffe2a6", cerceve="rgba(255,255,255,.9)",
            serit="#1b1838", serit_yazi="#ffe7c2", serit_logo="#ffffff", serit_su="#ffb36b",
            panel="rgba(27,24,56,.9)", panel_kenar="rgba(255,226,166,.7)")
BYZ = palet(mb.GOKYUZU, zemin="linear-gradient(180deg,#ffffff 0%,#f1f5f9 100%)",
            vurgu=None, vurgu_renk="#b07a2c", yazi="#0b2545", cerceve="#ffffff",
            serit="#0b2545", serit_yazi="#ffffff", serit_logo="#ffffff", serit_su="#5fb3ff",
            panel="#0b2545", panel_yazi="#fff", panel_cizgi="rgba(255,255,255,.25)",
            panel_kenar="#0b2545", panel_bas="linear-gradient(90deg,#c9963f,#f0cf86,#c9963f)",
            panel_bas_yazi="#2b1905")


# ---------------------------------------------------------------- yerleşimler
def L1(p, bicim="kose", fotolar=("gece", "avlu", "deniz")):
    """Sol: Tilda + başlık · orta: bina · sağ: galeri + fiyat + büyük MİA."""
    return pano(p, f"""
  {mb.tilda(300, 150, 360, p['tilda_beyaz'])}
  <div class="a" style="left:2000px;top:90px;width:4px;height:520px;background:{p['kas']};opacity:.55"></div>
  {baslik(2180, 110, p, 4750)}
  {mb.yazi(2186, 575, "İZMİT · MİA BÖLGESİ", 60, 600, p['kas'], "kas")}
  {galeri(11150, 14850, 70, 560, fotolar, p, bicim)}
  {fiyat2(15050, 70, 1720, p)}
  {mb.mia(16980, 80, 560, p['mia_beyaz'])}""")


def L2(p, fotolar=("gece", "avlu", "deniz", "teras")):
    """Başlık binanın iki yanına bölünür: sol 'MİA PARK OCEAN'DA', sağ 'YAŞAM BAŞLIYOR!'."""
    v = p["vurgu"] or ""
    renk2 = p.get("vurgu_renk", p["yazi"])
    return pano(p, f"""
  {mb.tilda(300, 120, 330, p['tilda_beyaz'])}
  {mb.yazi(2100, 70, "MİA PARK OCEAN'DA", 300, 800, p['yazi'], maxw=4800)}
  {mb.yazi(2108, 405, "60 AY SABİT TAKSİTLE EV SAHİBİ", 118, 800, renk2, v, maxw=4800)}
  {mb.yazi(2108, 545, "OLMANIN TAM ZAMANI!", 118, 800, renk2, v, maxw=4800)}
  {mb.yazi(306, 492, "1+1 · 39.900₺ / AY", 86, 800, p['kas'], maxw=1650)}
  {mb.yazi(306, 596, "2+1 · 49.900₺ / AY", 86, 800, p['kas'], maxw=1650)}
  {mb.yazi(11150, 70, "YAŞAM BAŞLIYOR!", 300, 800, p['yazi'], maxw=4700)}
  {galeri(11158, 15850, 405, 290, fotolar, p, "kose", etiket=False)}
  {mb.mia(16150, 80, 560, p['mia_beyaz'])}""")


def L3(p, fotolar=("gece", "avlu", "deniz", "teras", "ic")):
    """Eğik film şeridi galeri — sağ bölge boyunca beş kare."""
    return pano(p, f"""
  {mb.tilda(300, 150, 360, p['tilda_beyaz'])}
  <div class="a" style="left:2000px;top:90px;width:4px;height:520px;background:{p['kas']};opacity:.55"></div>
  {baslik(2180, 110, p, 4750)}
  {mb.yazi(2186, 552, "1+1 · 39.900₺ / AY   ·   2+1 · 49.900₺ / AY", 96, 800, p['kas'], maxw=4700)}
  {galeri(11050, 16250, 70, 560, fotolar, p, "egik")}
  {mb.mia(16500, 80, 560, p['mia_beyaz'])}""")


def L4(p, fotolar=("avlu", "deniz", "gece")):
    """Dev 60 — başlığın 60'ı kocaman, galeri daire pencereler."""
    v = p["vurgu"] or ""
    return pano(p, f"""
  {mb.tilda(300, 150, 360, p['tilda_beyaz'])}
  {mb.yazi(2100, 70, "MİA PARK OCEAN'DA YAŞAM BAŞLIYOR!", 170, 800, p['yazi'], maxw=4850)}
  {mb.yazi(2060, 165, "60", 630, 800, "", "altin", ls="-.06em")}
  {mb.yazi(2960, 300, "AY SABİT TAKSİTLE", 170, 800, p['yazi'], maxw=3950)}
  {mb.yazi(2966, 500, "EV SAHİBİ OLMANIN TAM ZAMANI!", 112, 800, p.get('vurgu_renk', p['yazi']), v, maxw=3950)}
  {galeri(11200, 14500, 60, 600, fotolar, p, "daire")}
  {fiyat2(14700, 70, 1720, p)}
  {mb.mia(16650, 80, 560, p['mia_beyaz'])}""")


TASARIMLAR = [
    (lambda: L1(LAC), "lacivert-galeri"),
    (lambda: L1(GOK), "gokyuzu-galeri"),
    (lambda: L2(LAC), "lacivert-bolunmus-baslik"),
    (lambda: L2(KRM), "krem-bolunmus-baslik"),
    (lambda: L3(TRK), "turkuaz-film-seridi"),
    (lambda: L3(GUN), "gunbatimi-film-seridi"),
    (lambda: L4(GOK), "gokyuzu-dev-60"),
    (lambda: L1(KRM, "kemer", ("gece", "teras", "deniz")), "krem-kemerler"),
    (lambda: L3(BYZ, ("aksam", "avlu", "deniz", "teras", "ic")), "beyaz-film-seridi"),
    (lambda: L2(GEC), "gece-turuncu-bolunmus"),
]


def sayfa(govde):
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>'
            f'{mb.CSS.replace("__FONT__", mb.FONT)}{CSS_EK}</style></head><body>{govde}{mb.JS}</body></html>')


# ---------------------------------------------------------------- sunum sayfası
def sunum(tam, no, ad, yol):
    """Üstte tam pano (gökyüzü + taşma), altta sol ve sağ yarı büyütülmüş."""
    gok = (166, 203, 236)
    W = 4500
    k = W / tam.width
    ust = tam.resize((W, round(tam.height * k)), Image.LANCZOS)
    pay = 70
    yar_h = tam.height
    f_b = ImageFont.truetype(mb.FONT, 64)
    f_b.set_variation_by_axes([800])
    f_k = ImageFont.truetype(mb.FONT, 34)
    f_k.set_variation_by_axes([600])
    bas_h = 150
    H = bas_h + ust.height + pay + 2 * (yar_h + 50) + 60
    s = Image.new("RGB", (W, H), (245, 247, 250))
    d = ImageDraw.Draw(s)
    d.text((70, 48), f"TASARIM {no:02d}", font=f_b, fill=(11, 37, 69))
    d.text((520, 64), ad.upper().replace("-", " · "), font=f_k, fill=(90, 105, 125))
    d.text((W - 70, 64), "180 m × 8,5 m · 80 m + 20 m + 80 m · bina 3,55 m taşar",
           font=f_k, fill=(90, 105, 125), anchor="ra")
    zem = Image.new("RGB", ust.size, gok)
    zem.paste(ust, (0, 0), ust)
    s.paste(zem, (0, bas_h))
    y = bas_h + ust.height + pay
    for i, (x0, x1, et) in enumerate(((0, tam.width // 2, "SOL YARI  ·  0–90 m"),
                                      (tam.width // 2, tam.width, "SAĞ YARI  ·  90–180 m"))):
        parca = tam.crop((x0, 0, x1, yar_h))
        zem = Image.new("RGB", parca.size, gok)
        zem.paste(parca, (0, 0), parca)
        s.paste(zem, (0, y))
        d.text((70, y + 20), et, font=f_k, fill=(11, 37, 69))
        y += yar_h + 50
    s.save(yol, quality=90)


def main():
    sec = None
    if "--sadece" in sys.argv:
        sec = {int(v) for v in sys.argv[sys.argv.index("--sadece") + 1].split(",")}
    gecici = tempfile.mkdtemp(prefix="mega2-")
    isler = []
    for i, (fn, ad) in enumerate(TASARIMLAR, 1):
        if sec and i not in sec:
            continue
        hp = os.path.join(gecici, f"{i}.html")
        open(hp, "w", encoding="utf-8").write(sayfa(fn()))
        isler.append(dict(html=hp, w=TW, h=TH, dsf=0.5, dilim=TW,
                          cikti=os.path.join(gecici, f"{i}"), no=i, ad=ad))
    jp = os.path.join(gecici, "isler.json")
    json.dump(isler, open(jp, "w"))
    npm = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    subprocess.run(["node", os.path.join(ROOT, "scripts", "mega-bilbord", "render.cjs"), jp],
                   check=True, env={**os.environ, "NODE_PATH": npm})
    os.makedirs(OUT, exist_ok=True)
    for is_ in isler:
        tam = Image.open(json.load(open(is_["cikti"] + ".json"))[0]).convert("RGBA")
        yol = os.path.join(OUT, f"{is_['no']:02d}-{is_['ad']}.jpg")
        sunum(tam, is_["no"], is_["ad"], yol)
        print("  →", os.path.relpath(yol, ROOT))


if __name__ == "__main__":
    main()
