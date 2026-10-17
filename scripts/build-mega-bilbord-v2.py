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




# ---------------------------------------------------------------- 3. tur: blok ritmi
# Referans: Imtiaz / Westwood Grande pano dili — tam yükseklikte, yan yana
# fotoğraf blokları ile düz renk marka blokları; bina gökyüzü bloğunda.
def blok_foto(x0, x1, ad, pos="50% 50%"):
    yol = os.path.join(ROOT, FOTO[ad])
    return (f'<div class="a" style="left:{x0}px;top:0;width:{x1 - x0}px;height:{ICERIK}px;'
            f'background:url(file://{yol}) {pos}/cover no-repeat"></div>')


def blok_renk(x0, x1, renk, ic=""):
    return (f'<div class="a" style="left:{x0}px;top:0;width:{x1 - x0}px;height:{ICERIK}px;'
            f'background:{renk};display:flex;flex-direction:column;align-items:center;'
            f'justify-content:center;text-align:center">{ic}</div>')


def satir(metin, fs, w=800, renk="#fff", sinif="", ls="0", mt=0, maxw=None):
    m = f' data-maxw="{maxw}"' if maxw else ""
    rc = "" if sinif in ("altin", "turuncu") else f"color:{renk};"
    return (f'<div class="tek {sinif}"{m} style="font-size:{fs}px;font-weight:{w};{rc}'
            f'letter-spacing:{ls};margin-top:{mt}px">{metin}</div>')


def L5(r, fotolar=("ic", "deniz", "gece"), konum=("50% 50%", "45% 50%", "50% 45%")):
    """r: ana, ikinci, yazi, vurgu, vurgu_sinif, gok, tilda_beyaz, mia_beyaz, serit..."""
    vs = r.get("vurgu_sinif", "")
    tw = round(380 * mb.TILDA_ORAN)
    by = r.get("baslik_yazi", r["yazi"])
    baslik_ic = (satir("MİA PARK OCEAN'DA", 205, 800, by, maxw=2850)
                 + satir("YAŞAM BAŞLIYOR!", 205, 800, by, mt=4, maxw=2850)
                 + f'<div style="width:220px;height:6px;background:{r["vurgu"]};margin:26px 0 24px"></div>'
                 + satir("60 AY SABİT TAKSİTLE EV SAHİBİ", 76, 800, r["vurgu"], vs, maxw=2850)
                 + satir("OLMANIN TAM ZAMANI!", 76, 800, r["vurgu"], vs, mt=8, maxw=2850))
    fiyat_ic = (satir("60 AY SABİT TAKSİT", 58, 700, r["vurgu"], vs, ls=".08em")
                + f'<div style="width:1450px;height:4px;background:{r["yazi"]};opacity:.25;margin:22px 0 18px"></div>'
                + satir("1+1", 66, 700, r["yazi"], ls=".04em")
                + satir("39.900₺ <span style='font-size:.36em;letter-spacing:.14em'>/ AY</span>", 138, 800, r["yazi"], ls="-.03em", mt=4)
                + f'<div style="width:1450px;height:4px;background:{r["yazi"]};opacity:.25;margin:20px 0 16px"></div>'
                + satir("2+1", 66, 700, r["yazi"], ls=".04em")
                + satir("49.900₺ <span style='font-size:.36em;letter-spacing:.14em'>/ AY</span>", 138, 800, r["yazi"], ls="-.03em", mt=4))
    mia_h = 520
    return pano(r, f"""
  {blok_renk(0, 2300, r['ana'])}
  {mb.tilda((2300 - tw) // 2, (ICERIK - 380) // 2, 380, r['tilda_beyaz'])}
  {blok_foto(2300, 3700, fotolar[0], konum[0])}
  {blok_renk(3700, 6800, r['ikinci'], baslik_ic)}
  <div class="a" style="left:6800px;top:0;width:4400px;height:{ICERIK}px;background:{r['gok']}"></div>
  {blok_renk(11200, 13200, r['ana'], fiyat_ic)}
  {blok_foto(13200, 14800, fotolar[1], konum[1])}
  {blok_renk(14800, 16600, r['ikinci'])}
  {mb.mia(15700 - round(mia_h * mb.MIA_ORAN) // 2, (ICERIK - mia_h) // 2, mia_h, r['mia_beyaz'])}
  {blok_foto(16600, 18000, fotolar[2], konum[2])}""")


def r_(**k):
    taban = dict(zemin="#000", yazi="#fff", tilda_beyaz=True, mia_beyaz=True,
                 gok="linear-gradient(180deg,#7db8e8 0%,#b9dcf5 60%,#e8f3fb 100%)",
                 serit="#0b1f3a", serit_yazi="#ffffff", serit_logo="#ffffff", serit_su="#5fb3ff")
    taban.update(k)
    return taban


R_LACIVERT = r_(ana="#0f2a4d", ikinci="#13365f", vurgu="#e6bd6e")
R_TILDA = r_(ana="#13212c", ikinci="#a87a55", vurgu="#f3dcb8", serit="#13212c")
R_TURKUAZ = r_(ana="#05707d", ikinci="#079aa9", vurgu="#ffffff", serit="#044e57")
R_BORDO = r_(ana="#7a1424", ikinci="#a51d33", vurgu="#ffd9a0", serit="#4a0b15")
R_BEYAZ = r_(ana="#ffffff", ikinci="#0f2a4d", yazi="#0f2a4d", baslik_yazi="#ffffff", vurgu="#d9a95b",
             tilda_beyaz=False, serit="#0f2a4d")



# ---------------------------------------------------------------- 4. tur: konsept
# "Geceden sabaha, kiradan ev sahipliğine — 60 adım."
# 180 m arabadan soldan sağa okunur: sol uçta yıldızlı gece, binanın
# arkasında gün doğumu, sağ uçta gündüz. 60 altın basamak (her biri bir ay)
# gece tarafından binaya tırmanır; 60. basamakta anahtar.
import random as _rnd

ANAHTAR = ('<svg viewBox="0 0 120 52" xmlns="http://www.w3.org/2000/svg">'
           '<defs><linearGradient id="ak" x1="0" y1="0" x2="0" y2="1">'
           '<stop offset="0" stop-color="#fff1c2"/><stop offset=".5" stop-color="#e7b75e"/>'
           '<stop offset="1" stop-color="#a8712a"/></linearGradient></defs>'
           '<circle cx="26" cy="26" r="21" fill="none" stroke="url(#ak)" stroke-width="9"/>'
           '<rect x="44" y="21" width="72" height="10" rx="3" fill="url(#ak)"/>'
           '<rect x="92" y="29" width="9" height="15" rx="2" fill="url(#ak)"/>'
           '<rect x="106" y="29" width="9" height="11" rx="2" fill="url(#ak)"/></svg>')


def yildizlar(x0, x1, y0, y1, n, tohum=7):
    r = _rnd.Random(tohum)
    noktalar = []
    for _ in range(n):
        x = r.uniform(x0, x1)
        k = (x - x0) / (x1 - x0)                 # sağa doğru sönükleşir
        if r.random() < k * 1.1:
            continue
        rr = r.choice([2.2, 2.6, 3.2, 4.2, 5.5])
        a = round(r.uniform(.35, .95) * (1 - k * .8), 2)
        noktalar.append(f'<circle cx="{x:.0f}" cy="{r.uniform(y0, y1):.0f}" r="{rr}" fill="#fff" opacity="{a}"/>')
    return (f'<svg class="a" style="left:0;top:0" width="18000" height="{ICERIK}" '
            f'viewBox="0 0 18000 {ICERIK}">' + "".join(noktalar) + '</svg>')


def basamaklar(x0, x1, hmin, hmax):
    n = 60
    adim = (x1 - x0) / n
    s = []
    for i in range(n):
        k = i / (n - 1)
        h = round(hmin + (hmax - hmin) * k ** 1.15)
        x = x0 + i * adim
        s.append(f'<div class="a" style="left:{x:.1f}px;top:{ICERIK - h}px;width:{adim - 14:.1f}px;'
                 f'height:{h}px;border-radius:10px 10px 0 0;'
                 f'background:linear-gradient(180deg,#ffe7a8 0,#e2b45c 8px,#c99343 40%,#8f6127 100%);'
                 f'box-shadow:0 0 {round(10 + 30 * k)}px rgba(255,196,96,{.15 + .35 * k:.2f})"></div>')
        ay = i + 1
        if ay in (1, 12, 24, 36, 48, 60):
            et = "60. AY · ANAHTAR SİZDE" if ay == 60 else f"{ay}. AY"
            s.append(f'<div class="a tek" style="left:{x + (adim - 14) / 2:.0f}px;top:{ICERIK - h - 82}px;'
                     f'transform:translateX(-50%);font-size:52px;font-weight:800;color:#ffe2a6;'
                     f'letter-spacing:.06em">{et}</div>')
    return "".join(s)


def L6():
    zemin = ("linear-gradient(90deg,#040a20 0%,#08153a 16%,#1b2a64 28%,#4b3a78 36%,"
             "#a8507a 42%,#f07a52 47%,#ffb768 51%,#ffd99a 55%,#bfe0f6 62%,#8cc4ee 75%,#6fb2e8 100%)")
    r = dict(zemin=zemin, serit="#071433", serit_yazi="#ffffff", serit_logo="#ffffff", serit_su="#5fb3ff")
    tw = round(330 * mb.TILDA_ORAN)
    ic = f"""
  <div class="a" style="left:6200px;top:0;width:5600px;height:{ICERIK}px;
       background:radial-gradient(ellipse 50% 90% at 50% 100%,rgba(255,214,140,.85) 0%,rgba(255,170,100,.35) 45%,rgba(255,170,100,0) 75%)"></div>
  {yildizlar(0, 7000, 20, 520, 900)}
  {basamaklar(560, 6980, 54, 372)}
  <div class="a" style="left:6700px;top:96px;width:340px;height:147px;
       filter:drop-shadow(0 0 34px rgba(255,210,120,.85))">{ANAHTAR}</div>
  {mb.tilda(520, 70, 330, True)}
  {mb.yazi(520 + tw + 170, 66, "EVİNİZE GİDEN 60 ADIM!", 216, 800, "#ffffff", maxw=6400 - (520 + tw + 170))}
  {mb.yazi(520 + tw + 178, 316, "BANKA YOK · FAİZ YOK · ARA ÖDEME YOK", 66, 700, "#ffe2a6", "kas",
           maxw=2900)}
  {mb.yazi(11280, 54, "MİA PARK OCEAN'DA", 236, 800, "#0b2545", maxw=3600)}
  {mb.yazi(11280, 290, "YAŞAM BAŞLIYOR!", 236, 800, "#0b2545", maxw=3600)}
  {mb.yazi(11290, 560, "60 AY SABİT TAKSİTLE EV SAHİBİ OLMANIN TAM ZAMANI!", 74, 800, "#0b2545", maxw=4500)}
  <div class="a" style="left:15000px;top:70px;width:1500px;height:470px;border-radius:40px;
       background:rgba(255,255,255,.92);box-shadow:0 20px 60px rgba(11,37,69,.18);
       display:flex;flex-direction:column;justify-content:center;padding:0 60px;color:#0b2545">
    <div class="tek" style="font-size:52px;font-weight:800;letter-spacing:.12em;color:#b07a2c">60 AY SABİT TAKSİT</div>
    <div style="display:flex;align-items:baseline;justify-content:space-between;margin-top:26px">
      <span class="tek" style="font-size:76px;font-weight:800">1+1</span>
      <span class="tek" style="font-size:118px;font-weight:800;letter-spacing:-.03em">39.900₺<span style="font-size:.36em;letter-spacing:.1em"> /AY</span></span></div>
    <div style="height:4px;background:rgba(11,37,69,.15);margin:14px 0"></div>
    <div style="display:flex;align-items:baseline;justify-content:space-between">
      <span class="tek" style="font-size:76px;font-weight:800">2+1</span>
      <span class="tek" style="font-size:118px;font-weight:800;letter-spacing:-.03em">49.900₺<span style="font-size:.36em;letter-spacing:.1em"> /AY</span></span></div>
  </div>
  {mb.mia(16720, 90, 500, False)}"""
    return pano(r, ic)

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
    """Tek görsel: tam pano (taşan bina dahil) açık gökyüzü önünde."""
    pay_x, pay_ust, pay_alt = 120, 60, 120
    W, H = tam.width + 2 * pay_x, tam.height + pay_ust + pay_alt
    s = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(s)
    for y in range(H):
        k = y / H
        d.line([(0, y), (W, y)], fill=(round(150 + 80 * k), round(190 + 50 * k), round(228 + 20 * k)))
    s.paste(tam, (pay_x, pay_ust), tam)
    s.save(yol, quality=92)


TASARIMLAR_BLOK = [
    (lambda: L5(R_LACIVERT), "blok-lacivert"),
    (lambda: L5(R_TILDA, ("teras", "ic", "aksam")), "blok-tilda-bronz"),
    (lambda: L5(R_TURKUAZ, ("ic", "avlu", "deniz")), "blok-turkuaz"),
    (lambda: L5(R_BORDO, ("teras", "deniz", "gece")), "blok-bordo"),
    (lambda: L5(R_BEYAZ, ("aksam", "deniz", "ic")), "blok-beyaz-lacivert"),
]


def main():
    global TASARIMLAR, OUT
    if "--konsept" in sys.argv:
        TASARIMLAR = [(L6, "gece-sabah-60-adim")]
        OUT = os.path.join(ROOT, "tabela", "mega-bilbord-180m-konsept")
    if "--blok" in sys.argv:
        TASARIMLAR = TASARIMLAR_BLOK
        OUT = os.path.join(ROOT, "tabela", "mega-bilbord-180m-v3")
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
