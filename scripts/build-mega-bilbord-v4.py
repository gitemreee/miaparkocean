#!/usr/bin/env python3
"""
180 m dev pano — 4. tur: 5 bağımsız reklam konsepti.

Ödeme bilgisi hepsinde aynı (60 ay = ÖDEME VADESİ, teslim süresi değil):
  60 ay sabit taksit · 1+1 aylık 39.900 ₺ · 2+1 aylık 49.900 ₺
  faiz yok · banka yok · kredi yok · ara ödeme yok · son daireler

Bina (taşan kesik render) her konseptte farklı yerde: bina_cx ile.

  K1  Kiraya değil, kendi evinize ödeyin   (gri → renk geçişi)
  K2  Fotoğrafla dolu dev "60"             (bina solda)
  K3  60 ay boyunca her ay aynı taksit      (takvim duvarı)
  K4  Lüks sade — krem, serif, altın        (bina solda, kemerli iç mekân)
  K5  Yol tabelası dili                     (hız levhası 60, çıkış tabelası)

    python3.13 scripts/build-mega-bilbord-v4.py [--sadece 1,3]
"""

import importlib.util as _il
import json
import os
import subprocess
import sys
import tempfile

from PIL import Image

Image.MAX_IMAGE_PIXELS = None
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _yukle(ad, dosya):
    spec = _il.spec_from_file_location(ad, os.path.join(ROOT, "scripts", dosya))
    m = _il.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


v2 = _yukle("mb_v2", "build-mega-bilbord-v2.py")
mb = v2.mb
OUT = os.path.join(ROOT, "tabela", "mega-bilbord-180m-konseptler")
ICERIK, HW, HH, EXT = v2.ICERIK, mb.HW, mb.HH, mb.EXT
FRAUNCES = os.path.join(ROOT, "brand-source", "fonts", "Fraunces-600.ttf")

CSS_EK = f"""
@font-face {{ font-family: Fr; src: url("file://{FRAUNCES}"); }}
.fr {{ font-family: Fr, serif; }}
.cizik {{ text-decoration: line-through; text-decoration-color: #e30613;
         text-decoration-thickness: .1em; }}
"""

IMG = lambda yol: "file://" + os.path.join(ROOT, yol)


# ---------------------------------------------------------------- ortak
def bina(cx):
    """Taşan bina: (taşma katmanı, pano katmanı) — cx tuval x'i."""
    hx = cx - HW // 2
    hy = EXT - round(mb.UST_FR * HH)
    src = f"file://{mb.HERO}"
    dur = []
    for a, b in mb.SUTUNLAR:
        dur += [f"transparent {a * 100:.2f}%", f"#000 {a * 100:.2f}%",
                f"#000 {b * 100:.2f}%", f"transparent {b * 100:.2f}%"]
    maske = "linear-gradient(90deg," + ",".join(dur) + ")"
    tas = (f'<img class="a" src="{src}" style="left:{hx}px;top:{hy}px;width:{HW}px;height:{HH}px;'
           f'-webkit-mask-image:{maske}">')
    ic = (f'<img class="a" src="{src}" style="left:{hx}px;top:{hy - EXT}px;width:{HW}px;height:{HH}px">')
    return tas, ic


def pano(r, arka, icerik, bina_cx):
    tas, ic = bina(bina_cx)
    return f"""
<div class="tasma">{tas}</div>
<div class="pano" style="background:{r['zemin']}">
  {arka}
  {ic}
  {icerik}
  {v2.serit(r)}
</div>"""


def y(x, y_, metin, fs, w=800, renk="#fff", **k):
    return mb.yazi(x, y_, metin, fs, w, renk, **k)


def kutu(x, y_, w, h, ic, stil=""):
    return (f'<div class="a" style="left:{x}px;top:{y_}px;width:{w}px;height:{h}px;{stil}">{ic}</div>')


def satir(metin, fs, w=800, renk="#fff", ek=""):
    return f'<div class="tek" style="font-size:{fs}px;font-weight:{w};color:{renk};{ek}">{metin}</div>'


def damga(cx, cy, d, ust, orta, alt, zemin="#ffd21f", yazi="#14110a", don=-10):
    return (f'<div class="a" style="left:{cx - d // 2}px;top:{cy - d // 2}px;width:{d}px;height:{d}px;'
            f'border-radius:50%;background:{zemin};color:{yazi};transform:rotate({don}deg);'
            f'box-shadow:0 0 0 10px rgba(255,255,255,.9),0 20px 50px rgba(0,0,0,.4);display:flex;'
            f'flex-direction:column;align-items:center;justify-content:center;text-align:center;line-height:1">'
            f'<div class="tek" style="font-size:{round(d * .085)}px;font-weight:800;letter-spacing:.1em">{ust}</div>'
            f'<div class="tek" style="font-size:{round(d * .155)}px;font-weight:800;margin:.08em 0">{orta}</div>'
            f'<div class="tek" style="font-size:{round(d * .075)}px;font-weight:800;letter-spacing:.06em">{alt}</div></div>')


SERIT_KOYU = dict(serit="#ffffff", serit_yazi="#0b1f3a", serit_logo="#0f4c9b", serit_su="#2f7fd6")
SERIT_ACIK = dict(serit="#0b2545", serit_yazi="#ffffff", serit_logo="#ffffff", serit_su="#5fb3ff")
YOKLAR = "FAİZ YOK · BANKA YOK · KREDİ YOK · ARA ÖDEME YOK"


# ---------------------------------------------------------------- K1
def K1():
    r = dict(SERIT_KOYU, zemin="linear-gradient(90deg,#2a2e33 0%,#3d434a 18%,#2c3a4c 26%,"
                                "#0d3366 36%,#0b2f5e 70%,#0a2a55 100%)")
    yok = "".join(
        f'<div style="display:flex;align-items:center;gap:30px;height:150px">'
        f'<div style="width:110px;height:110px;border-radius:50%;background:#e30613;color:#fff;'
        f'display:flex;align-items:center;justify-content:center;font-size:84px;font-weight:800">✕</div>'
        f'<span class="tek" style="font-size:106px;font-weight:800;color:#fff">{t}</span></div>'
        for t in ("FAİZ YOK", "BANKA YOK", "KREDİ YOK", "ARA ÖDEME YOK"))
    kart = (satir("60 AY SABİT TAKSİT", 92, 800, "#ffd21f", "letter-spacing:.04em")
            + '<div style="height:4px;background:rgba(255,255,255,.35);margin:26px 0 18px"></div>'
            + f'<div style="display:flex;align-items:baseline;justify-content:space-between">'
              f'{satir("1+1", 110)}{satir("39.900₺<span style=font-size:.34em>/AY</span>", 190, ek="letter-spacing:-.03em")}</div>'
            + f'<div style="display:flex;align-items:baseline;justify-content:space-between;margin-top:6px">'
              f'{satir("2+1", 110)}{satir("49.900₺<span style=font-size:.34em>/AY</span>", 190, ek="letter-spacing:-.03em")}</div>')
    icerik = f"""
  {mb.tilda(320, 209, 300, True)}
  {y(1960, 48, '<span class="cizik" style="color:#9aa3ab">KİRAYA</span> <span style="color:#9aa3ab">DEĞİL,</span>', 250)}
  {y(1960, 310, "KENDİ EVİNİZE ÖDEYİN.", 250, maxw=4800)}
  {y(1972, 592, "60 AY SABİT TAKSİTLE EV SAHİBİ OLUN!", 80, 800, "#ffd21f", maxw=4900)}
  {kutu(7000, 60, 2600, 600, yok)}
  {kutu(9750, 46, 3050, 626, kart, "border-radius:44px;background:linear-gradient(160deg,#ff2a33,#c40d18);"
        "padding:44px 60px;box-shadow:0 24px 60px rgba(0,0,0,.45)")}
  {damga(12780, 120, 330, "SON", "DAİRELER", "KAÇIRMAYIN!")}
  {mb.mia(16820, 140, 440, True)}"""
    return pano(r, "", icerik, 14900)


# ---------------------------------------------------------------- K2
def K2():
    r = dict(SERIT_KOYU, zemin="linear-gradient(90deg,#04252d 0%,#0a3f4c 45%,#06303a 100%)")
    foto = IMG("signage-source/courtyard-pools.jpg")
    gece = IMG("signage-source/night-gate-temiz.jpg")
    altmis = (f'<div class="a tek" style="left:3950px;top:-170px;font-size:1000px;font-weight:800;'
              f'letter-spacing:-.06em;line-height:1;background:url({foto}) 50% 55%/1600px auto;'
              f'-webkit-background-clip:text;background-clip:text;color:transparent;'
              f'-webkit-text-stroke:10px #f3d39c">60</div>')
    fiyat = "".join(
        f'<div style="text-align:left">'
        f'{satir(t + " · AYLIK", 66, 700, "#f3d39c", "letter-spacing:.14em")}'
        f'{satir(v + "<span style=font-size:.42em>₺</span>", 260, 800, "#fff", "letter-spacing:-.035em;margin-top:6px")}</div>'
        for t, v in (("1+1", "39.900"), ("2+1", "49.900")))
    icerik = f"""
  {altmis}
  {y(5560, 30, "AY SABİT", 260, maxw=3000)}
  {y(5560, 300, "TAKSİT!", 260, 800, "", sinif="altin", maxw=3000)}
  {y(5570, 600, YOKLAR, 60, 700, "#cfe9ee", sinif="kas", maxw=3000)}
  {kutu(8850, 50, 4200, 440, fiyat, "display:flex;justify-content:space-between")}
  {kutu(8850, 520, 4200, 140, satir("SON DAİRELER İÇİN FIRSATI KAÇIRMAYIN!", 76, 800, "#14110a"),
        "border-radius:24px;background:#ffd21f;display:flex;align-items:center;justify-content:center")}
  {mb.tilda(13300, 200, 320, True)}
  <div class="a" style="left:14980px;top:120px;width:4px;height:480px;background:#f3d39c;opacity:.6"></div>
  {mb.mia(15250, 140, 440, True)}
  <div class="a" style="left:16200px;top:0;width:1800px;height:{ICERIK}px;background:url({gece}) 70% 60%/cover;
       clip-path:polygon(18% 0,100% 0,100% 100%,0 100%)"></div>"""
    return pano(r, "", icerik, 2050)


# ---------------------------------------------------------------- K3
def K3():
    r = dict(SERIT_KOYU, zemin="linear-gradient(90deg,#071a36 0%,#0b2545 50%,#0d2d55 100%)")
    x0, x1, sut, sat = 5150, 10950, 12, 5
    cw = (x1 - x0) / sut
    ch = ICERIK / sat
    kare = []
    for i in range(60):
        cx, cy = x0 + (i % sut) * cw, (i // sut) * ch
        son = i == 59
        kare.append(
            f'<div class="a" style="left:{cx + 9:.0f}px;top:{cy + 9:.0f}px;width:{cw - 18:.0f}px;height:{ch - 18:.0f}px;'
            f'border-radius:16px;background:{"#ffd21f" if son else "#ffffff"};display:flex;align-items:center;'
            f'justify-content:space-between;padding:0 26px;color:#0b2545">'
            f'<span class="tek" style="font-size:34px;font-weight:700;opacity:.7">{i + 1}. AY</span>'
            f'<span class="tek" style="font-size:62px;font-weight:800;letter-spacing:-.02em">39.900₺</span></div>')
    serit_kurdele = (f'<div class="a tek" style="left:{(x0 + x1) // 2}px;top:{ICERIK // 2}px;'
                     f'transform:translate(-50%,-50%) rotate(-3deg);background:#e30613;color:#fff;'
                     f'font-size:96px;font-weight:800;padding:26px 70px;border-radius:20px;'
                     f'box-shadow:0 20px 50px rgba(0,0,0,.5)">1+1 · HER AY 39.900₺ · 60 AY DEĞİŞMEZ</div>')
    kart = (satir("AYLIK SABİT TAKSİT", 58, 800, "#c40d18", "letter-spacing:.1em")
            + '<div style="height:4px;background:rgba(11,37,69,.15);margin:20px 0 10px"></div>'
            + satir("1+1", 70, 800, "#0b2545") + satir("39.900₺", 170, 800, "#0b2545", "letter-spacing:-.03em")
            + '<div style="height:4px;background:rgba(11,37,69,.15);margin:10px 0"></div>'
            + satir("2+1", 70, 800, "#0b2545") + satir("49.900₺", 170, 800, "#0b2545", "letter-spacing:-.03em"))
    icerik = f"""
  {mb.tilda(300, 209, 300, True)}
  {y(1950, 50, "60 AY BOYUNCA", 210, maxw=3000)}
  {y(1950, 300, "HER AY AYNI TAKSİT!", 210, 800, "#ffd21f", maxw=3000)}
  {y(1960, 590, YOKLAR, 58, 700, "#cfe1f5", sinif="kas", maxw=3000)}
  {"".join(kare)}
  {serit_kurdele}
  {kutu(11150, 30, 1850, 660, kart, "border-radius:36px;background:#fff;padding:34px 50px;"
        "box-shadow:0 20px 50px rgba(0,0,0,.35)")}
  {damga(12930, 110, 300, "SON", "DAİRELER", "KAÇIRMAYIN!", zemin="#e30613", yazi="#fff")}
  {mb.mia(16800, 140, 440, True)}"""
    return pano(r, "", icerik, 14850)


# ---------------------------------------------------------------- K4
def K4():
    r = dict(SERIT_ACIK, zemin="linear-gradient(90deg,#f7f2e9 0%,#f1e8d8 100%)")
    lac, alt = "#13284a", "#a8783f"
    ic_foto = IMG("public/images/interior-living.webp")
    fiyat = "".join(
        f'<div>{satir(t + " · AYLIK", 58, 700, alt, "letter-spacing:.2em")}'
        f'<div class="tek fr" style="font-size:230px;color:{lac};line-height:1;margin-top:10px">{v}'
        f'<span style="font-size:.4em"> ₺</span></div></div>'
        for t, v in (("1+1", "39.900"), ("2+1", "49.900")))
    arka = (f'<div class="a" style="left:60px;top:40px;width:17880px;height:{ICERIK - 80}px;'
            f'border:3px solid {alt};opacity:.45;border-radius:6px"></div>')
    icerik = f"""
  <div class="a tek fr" style="left:4100px;top:10px;font-size:260px;color:{lac};line-height:1.05">Mia Park Ocean'da</div>
  <div class="a tek fr" style="left:4100px;top:285px;font-size:260px;color:{alt};line-height:1.05">yaşam başlıyor.</div>
  {y(4110, 610, YOKLAR, 56, 700, lac, sinif="kas", maxw=4200)}
  <div class="a" style="left:8650px;top:110px;width:3px;height:500px;background:{alt}"></div>
  <div class="a tek fr" style="left:8950px;top:20px;font-size:150px;color:{lac}">60 ay sabit taksit</div>
  {kutu(8950, 210, 3900, 380, fiyat, "display:flex;justify-content:space-between")}
  <div class="a tek fr" style="left:8950px;top:600px;font-size:76px;color:{alt}">Son daireler için fırsatı kaçırmayın.</div>
  <div class="a" style="left:13150px;top:110px;width:3px;height:500px;background:{alt}"></div>
  {mb.tilda(13450, 200, 320, False)}
  {mb.mia(15250, 150, 420, False)}
  <div class="a" style="left:16300px;top:70px;width:1460px;height:{ICERIK - 70}px;
       border-radius:730px 730px 0 0;background:url({ic_foto}) 50% 50%/cover;
       box-shadow:0 0 0 12px #f7f2e9,0 0 0 15px {alt}"></div>"""
    return pano(r, arka, icerik, 2050)


# ---------------------------------------------------------------- K5
def K5():
    r = dict(SERIT_KOYU, zemin="linear-gradient(180deg,#0e1d3d 0%,#1d3566 60%,#2f4f86 100%)")
    hiz = (f'<div class="a" style="left:1950px;top:39px;width:640px;height:640px;border-radius:50%;'
           f'background:#fff;box-shadow:inset 0 0 0 80px #e30613,0 20px 50px rgba(0,0,0,.45);display:flex;'
           f'flex-direction:column;align-items:center;justify-content:center;line-height:.9;color:#111">'
           f'<div class="tek" style="font-size:330px;font-weight:800;letter-spacing:-.05em">60</div>'
           f'<div class="tek" style="font-size:80px;font-weight:800;letter-spacing:.1em">AY</div></div>')
    ok = ('<svg viewBox="0 0 100 100" width="300" height="300"><path d="M20 80 L70 30 M70 30 H34 M70 30 V66" '
          'stroke="#fff" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>')
    cikis = (f'<div class="a" style="left:6150px;top:40px;width:3000px;height:640px;border-radius:34px;'
             f'background:#00704a;box-shadow:inset 0 0 0 12px #fff,0 20px 50px rgba(0,0,0,.45);'
             f'display:flex;align-items:center;justify-content:space-between;padding:0 80px">'
             f'<div>{satir("SON ÇIKIŞ", 76, 800, "#14110a", "background:#ffd21f;display:inline-block;padding:10px 30px;border-radius:12px")}'
             f'{satir("EV SAHİBİ", 200, 800, "#fff", "margin-top:30px")}{satir("OLMAK", 200, 800, "#fff")}</div>{ok}</div>')
    turistik = "".join(
        f'<div style="display:flex;align-items:baseline;justify-content:space-between;margin-top:8px">'
        f'{satir(t, 96)}{satir(v + "₺<span style=font-size:.36em>/AY</span>", 170, ek="letter-spacing:-.03em")}</div>'
        for t, v in (("1+1", "39.900"), ("2+1", "49.900")))
    tabela = (f'<div class="a" style="left:12950px;top:40px;width:3500px;height:640px;border-radius:34px;'
              f'background:#7a3f1d;box-shadow:inset 0 0 0 12px #fff,0 20px 50px rgba(0,0,0,.45);padding:56px 80px">'
              f'{satir("MİA PARK OCEAN · 60 AY SABİT TAKSİT", 74, 800, "#ffe2a6", "letter-spacing:.04em")}'
              f'{turistik}</div>')
    icerik = f"""
  {mb.tilda(300, 209, 300, True)}
  {hiz}
  {y(2780, 50, "SABİT TAKSİT!", 220, maxw=3250)}
  {y(2790, 310, "Bu 60 hız sınırı değil, fırsat!", 96, 800, "#ffd21f", maxw=3250)}
  {y(2790, 460, "FAİZ YOK · BANKA YOK", 76, 800, "#fff", sinif="kas", maxw=3250)}
  {y(2790, 570, "KREDİ YOK · ARA ÖDEME YOK", 76, 800, "#fff", sinif="kas", maxw=3250)}
  {cikis}
  {tabela}
  {mb.mia(16900, 150, 420, True)}"""
    return pano(r, "", icerik, 11050)


KONSEPTLER = [(K1, "kiraya-degil-evinize"), (K2, "fotografli-dev-60"), (K3, "her-ay-ayni-takvim"),
              (K4, "luks-sade-krem"), (K5, "yol-tabelasi")]


def sayfa(govde):
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>'
            f'{mb.CSS.replace("__FONT__", mb.FONT)}{v2.CSS_EK}{CSS_EK}</style></head>'
            f'<body>{govde}{mb.JS}</body></html>')


def main():
    sec = None
    if "--sadece" in sys.argv:
        sec = {int(v) for v in sys.argv[sys.argv.index("--sadece") + 1].split(",")}
    gecici = tempfile.mkdtemp(prefix="mega4-")
    isler = []
    for i, (fn, ad) in enumerate(KONSEPTLER, 1):
        if sec and i not in sec:
            continue
        hp = os.path.join(gecici, f"{i}.html")
        open(hp, "w", encoding="utf-8").write(sayfa(fn()))
        isler.append(dict(html=hp, w=mb.TW, h=mb.TH, dsf=0.5, dilim=mb.TW,
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
        v2.sunum(tam, is_["no"], is_["ad"], yol)
        print("  →", os.path.relpath(yol, ROOT))


if __name__ == "__main__":
    main()
