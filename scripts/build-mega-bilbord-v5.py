#!/usr/bin/env python3
"""
180 m dev pano — 5. tur: seçilen üç fikrin baştan tasarımı.

  Y  Yol tabelası (beğenilen 5. konsept, gerçek levha diliyle)
  S  60 ay boyunca her ay aynı taksit — dümdüz iki altın çizgi
  K  Kiraya değil, kendi evinize ödeyin — yırtık kâğıt geçişi

Ödeme: 60 ay sabit taksit (vade) · 1+1 aylık 39.900 ₺ · 2+1 aylık 49.900 ₺ ·
faiz/banka/kredi/ara ödeme yok · son daireler.

    python3.13 scripts/build-mega-bilbord-v5.py [--sadece 1,3]
"""

import importlib.util as _il
import json
import os
import random
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


v4 = _yukle("mb_v4", "build-mega-bilbord-v4.py")
v2, mb = v4.v2, v4.mb
OUT = os.path.join(ROOT, "tabela", "mega-bilbord-180m-tur5")
ICERIK = v2.ICERIK
BARLOW = os.path.join(ROOT, "brand-source", "fonts", "BarlowCond-700.ttf")

CSS_EK = f"""
@font-face {{ font-family: Yol; src: url("file://{BARLOW}"); }}
.yol {{ font-family: Yol, sans-serif; font-weight: 700; letter-spacing: .01em; }}
"""

satir, kutu, y, damga, pano = v4.satir, v4.kutu, v4.y, v4.damga, v4.pano


# ================================================================ Y — yol tabelası
def direk(x, ust, w=44):
    return (f'<div class="a" style="left:{x - w // 2}px;top:{ust}px;width:{w}px;height:{ICERIK - ust}px;'
            f'background:linear-gradient(90deg,#5d6670,#c9d0d6 45%,#6b747d);border-radius:6px 6px 0 0"></div>')


def levha(x, ust, w, h, zemin, ic, direkler=None):
    perc = "".join(
        f'<div style="position:absolute;{a}:26px;{b}:26px;width:20px;height:20px;border-radius:50%;'
        f'background:radial-gradient(circle at 35% 35%,#fff,#9aa3ab)"></div>'
        for a in ("top", "bottom") for b in ("left", "right"))
    d = "".join(direk(x + px, ust + h - 10) for px in (direkler or (w // 4, 3 * w // 4)))
    return (d + f'<div class="a" style="left:{x}px;top:{ust}px;width:{w}px;height:{h}px;border-radius:34px;'
                f'background:linear-gradient(170deg,rgba(255,255,255,.14),rgba(255,255,255,0) 40%),{zemin};'
                f'box-shadow:inset 0 0 0 12px #fff,inset 0 0 0 16px rgba(0,0,0,.18),0 26px 60px rgba(0,0,0,.5)">'
                f'{perc}{ic}</div>')


def hiz_levhasi(cx, cy, d):
    return (direk(cx, cy + d // 2 - 10)
            + f'<div class="a" style="left:{cx - d // 2}px;top:{cy - d // 2}px;width:{d}px;height:{d}px;'
              f'border-radius:50%;background:radial-gradient(circle at 40% 35%,#ffffff,#eceff1);'
              f'box-shadow:inset 0 0 0 {round(d * .12)}px #d7141e,inset 0 0 0 {round(d * .135)}px #fff,'
              f'0 0 0 8px #fff,0 26px 60px rgba(0,0,0,.5);display:flex;flex-direction:column;'
              f'align-items:center;justify-content:center;line-height:.86;color:#111">'
              f'<div class="tek yol" style="font-size:{round(d * .52)}px">60</div>'
              f'<div class="tek yol" style="font-size:{round(d * .15)}px;letter-spacing:.12em">AY</div></div>')


def uyari_levhasi(cx, ust):
    w = 520
    ucgen = (f'<svg viewBox="0 0 100 88" width="{w}" height="{round(w * .88)}">'
             f'<path d="M50 4 L96 84 H4 Z" fill="#fff" stroke="#d7141e" stroke-width="9" stroke-linejoin="round"/>'
             f'<rect x="45" y="30" width="10" height="30" rx="4" fill="#111"/><circle cx="50" cy="70" r="5.5" fill="#111"/></svg>')
    plaka_y = ust + round(w * .88) + 18
    return (direk(cx, ust + 200)
            + f'<div class="a" style="left:{cx - w // 2}px;top:{ust}px;filter:drop-shadow(0 22px 40px rgba(0,0,0,.5))">{ucgen}</div>'
            + f'<div class="a tek yol" style="left:{cx - 330}px;top:{plaka_y}px;width:660px;height:120px;'
              f'background:#fff;border:8px solid #111;border-radius:14px;color:#111;font-size:84px;'
              f'display:flex;align-items:center;justify-content:center;box-shadow:0 18px 40px rgba(0,0,0,.45)">'
              f'SON DAİRELER</div>')


def piktogram(ikon):
    return (f'<div style="width:104px;height:104px;border-radius:14px;background:#fff;flex:none;'
            f'display:flex;align-items:center;justify-content:center">'
            f'<svg viewBox="0 0 24 24" width="84" height="84" fill="none" stroke="#0a4fa3" '
            f'stroke-linecap="round" stroke-linejoin="round">{ikon}'
            f'<path d="M4 4l16 16" stroke="#d7141e" stroke-width="2.6"/></svg></div>')


def Y():
    r = dict(v4.SERIT_KOYU,
             zemin="linear-gradient(180deg,#0b1834 0%,#172d5c 55%,#2c4c86 100%)")
    sehir = "".join(
        f'<circle cx="{random.Random(i).uniform(0, 18000):.0f}" cy="{random.Random(i * 7).uniform(560, 710):.0f}" '
        f'r="{random.Random(i * 3).choice([3, 4, 6])}" fill="#ffd98a" opacity=".35"/>' for i in range(500))
    arka = f'<svg class="a" style="left:0;top:0" width="18000" height="{ICERIK}">{sehir}</svg>'

    yesil_ic = (f'<div style="position:absolute;left:60px;top:46px" class="tek yol">'
                f'<span style="background:#ffd21f;color:#111;font-size:84px;padding:6px 34px 8px;border-radius:12px">ÇIKIŞ 60</span></div>'
                f'<div class="tek yol" style="position:absolute;left:60px;top:170px;font-size:190px;color:#fff;line-height:.95">'
                f'SON ÇIKIŞ:<br>EV SAHİBİ OLMAK</div>'
                f'<svg viewBox="0 0 100 100" width="330" height="330" style="position:absolute;right:50px;top:110px">'
                f'<path d="M22 82 L74 30 M74 30 H38 M74 30 V66" stroke="#fff" stroke-width="13" fill="none" '
                f'stroke-linecap="round" stroke-linejoin="round"/></svg>')
    mavi_ic = "".join(
        f'<div style="display:flex;align-items:center;gap:30px;height:112px;margin-bottom:{4 if i < 3 else 0}px">'
        f'{piktogram(ik)}<span class="tek yol" style="font-size:104px;color:#fff">{t}</span></div>'
        for i, (t, ik) in enumerate((("FAİZ YOK", v2.IK_YUZDE), ("BANKA YOK", v2.IK_BANKA),
                                     ("KREDİ YOK", v2.IK_KART), ("ARA ÖDEME YOK",
                                      '<path d="M4 7h16M4 12h16M4 17h10" stroke-width="2"/>'))))
    kahve_ic = (f'<div class="tek yol" style="font-size:96px;color:#ffe2a6;display:flex;align-items:center;gap:24px">'
                f'<svg viewBox="0 0 24 24" width="96" height="96"><path d="M12 2a7.5 7.5 0 0 0-7.5 7.5c0 5.6 7.5 12.5 7.5 12.5'
                f's7.5-6.9 7.5-12.5A7.5 7.5 0 0 0 12 2z" fill="#ffe2a6"/><circle cx="12" cy="9.5" r="2.9" fill="#7a3e1c"/></svg>'
                f'MİA PARK OCEAN · 60 AY SABİT TAKSİT</div>'
                + "".join(
                    f'<div style="display:flex;align-items:baseline;justify-content:space-between;margin-top:14px;'
                    f'border-top:5px solid rgba(255,255,255,.35);padding-top:10px">'
                    f'<span class="tek yol" style="font-size:120px;color:#fff">{t}</span>'
                    f'<span class="tek yol" style="font-size:160px;color:#fff">{v}₺'
                    f'<span style="font-size:.38em;letter-spacing:.06em"> / AY</span></span></div>'
                    for t, v in (("1+1", "39.900"), ("2+1", "49.900"))))
    icerik = f"""
  {mb.tilda(280, 200, 290, True)}
  {hiz_levhasi(2160, 310, 560)}
  {y(2560, 60, "SABİT TAKSİT!", 230, maxw=2750)}
  {y(2570, 330, "Bu 60 hız sınırı değil,", 100, 800, "#ffd21f", maxw=2750)}
  {y(2570, 450, "fırsat!", 100, 800, "#ffd21f", maxw=2750)}
  {uyari_levhasi(5800, 50)}
  {levha(6420, 40, 3050, 560, "#00703c", yesil_ic)}
  {levha(12850, 40, 2700, 560, "#7a3e1c", f'<div style="padding:52px 80px">{kahve_ic}</div>')}
  {levha(15700, 40, 1520, 560, "#0a4fa3", f'<div style="padding:46px 56px">{mavi_ic}</div>', (380, 1140))}
  {mb.mia(17300, 190, 330, True)}"""
    return pano(r, arka, icerik, 11100)


# ================================================================ S — her ay aynı
def S():
    r = dict(v4.SERIT_KOYU, zemin="radial-gradient(ellipse 70% 140% at 45% 100%,#123a6e 0%,#0b2545 50%,#061631 100%)")
    x0, x1 = 5350, 12350
    grid = (f'<div class="a" style="left:{x0}px;top:40px;width:{x1 - x0}px;height:600px;opacity:.12;'
            f'background:repeating-linear-gradient(90deg,#9fc3ea 0 2px,transparent 2px {(x1 - x0) / 59:.2f}px),'
            f'repeating-linear-gradient(180deg,#9fc3ea 0 2px,transparent 2px 100px)"></div>')

    def mx(m):
        return x0 + (m - 1) * (x1 - x0) / 59

    s = [grid]
    for yy, renk, tip, val in ((200, "#ffffff", "2+1", "49.900"), (460, "#f2c46b", "1+1", "39.900")):
        s.append(f'<div class="a" style="left:{x0}px;top:{yy - 11}px;width:{x1 - x0}px;height:22px;border-radius:11px;'
                 f'background:{renk};box-shadow:0 0 40px {renk}"></div>')
        s.append(f'<div class="a tek" style="left:{x0 - 40}px;top:{yy}px;transform:translate(-100%,-50%);'
                 f'background:{renk};color:#0b2545;font-size:84px;font-weight:800;padding:14px 34px;border-radius:999px">{tip}</div>')
        for m in (1, 12, 24, 36, 48, 60):
            x = mx(m)
            s.append(f'<div class="a" style="left:{x - 30:.0f}px;top:{yy - 30}px;width:60px;height:60px;border-radius:50%;'
                     f'background:#0b2545;border:12px solid {renk}"></div>')
            s.append(f'<div class="a tek" style="left:{x:.0f}px;top:{yy - 140}px;transform:translateX(-50%);'
                     f'font-size:{110 if m == 60 else 86}px;font-weight:800;color:{renk};letter-spacing:-.02em">'
                     f'{val}₺</div>')
    s.append(f'<div class="a" style="left:{x0}px;top:600px;width:{x1 - x0}px;height:4px;background:rgba(159,195,234,.6)"></div>')
    for m in (1, 12, 24, 36, 48, 60):
        s.append(f'<div class="a tek" style="left:{mx(m):.0f}px;top:620px;transform:translateX(-50%);font-size:58px;'
                 f'font-weight:800;color:#9fc3ea;letter-spacing:.06em">{m}. AY</div>')
    yok = "".join(f'<div class="tek" style="font-size:78px;font-weight:800;color:#fff;margin:8px 0">'
                  f'<span style="color:#ff4d4d">✕</span> {t}</div>'
                  for t in ("FAİZ YOK", "BANKA YOK", "KREDİ YOK", "ARA ÖDEME YOK"))
    icerik = f"""
  {mb.tilda(280, 200, 290, True)}
  {y(1850, 26, "60 AY BOYUNCA", 196, maxw=2900)}
  {y(1850, 248, "HER AY AYNI", 196, 800, "#f2c46b", maxw=2900)}
  {y(1850, 470, "TAKSİT!", 196, maxw=2900)}
  {"".join(s)}
  {damga(12780, 560, 260, "SON", "DAİRELER", "KAÇIRMAYIN!", zemin="#e30613", yazi="#fff")}
  {kutu(16000, 70, 1200, 560, yok)}
  {mb.mia(17250, 190, 330, True)}"""
    return pano(r, "", icerik, 14350)


# ================================================================ K — kiraya değil
def yirtik(x_kenar, sapma=110, tohum=4):
    rnd = random.Random(tohum)
    pts = ["0px 0px"]
    yy = 0.0
    while yy < ICERIK:
        pts.append(f"{x_kenar + rnd.uniform(-sapma, sapma):.0f}px {yy:.0f}px")
        yy += rnd.uniform(18, 46)
    pts += [f"{x_kenar}px {ICERIK}px", f"0px {ICERIK}px"]
    return "polygon(" + ",".join(pts) + ")"


def K():
    r = dict(v4.SERIT_ACIK, zemin="linear-gradient(90deg,#fff6e6 0%,#fdf3e4 35%,#e9f3fb 75%,#dcecf8 100%)")
    sol = (f'<div class="a" style="left:0;top:0;width:5600px;height:{ICERIK}px;filter:drop-shadow(18px 0 18px rgba(0,0,0,.35))">'
           f'<div style="width:100%;height:100%;clip-path:{yirtik(5420)};'
           f'background:radial-gradient(ellipse 60% 90% at 40% 50%,#4a5058,#2b2f35 70%,#1f2226)"></div></div>')
    kira = (f'<div class="a tek" style="left:1880px;top:40px;font-size:380px;font-weight:800;letter-spacing:-.02em;'
            f'color:#6f7780">KİRAYA</div>'
            f'<div class="a" style="left:1800px;top:230px;width:3000px;height:70px;background:#e30613;'
            f'transform:rotate(-6deg);border-radius:10px;box-shadow:0 10px 30px rgba(0,0,0,.4)"></div>'
            f'<div class="a tek" style="left:1900px;top:480px;font-size:170px;font-weight:800;color:#9aa3ab">DEĞİL,</div>')
    anahtar = (f'<div class="a" style="left:8000px;top:70px;width:520px;height:226px;'
               f'filter:drop-shadow(0 16px 30px rgba(168,113,42,.45))">{v2.ANAHTAR if hasattr(v2, "ANAHTAR") else ""}</div>')
    yok = "".join(f'<div class="tek" style="font-size:90px;font-weight:800;color:#0b2545;margin:0">'
                  f'<span style="color:#e30613">✕</span> {t}</div>'
                  for t in ("FAİZ YOK", "BANKA YOK", "KREDİ YOK", "ARA ÖDEME YOK"))
    kart = (satir("60 AY SABİT TAKSİT", 80, 800, "#ffd21f", "letter-spacing:.06em")
            + "".join(
                f'<div style="display:flex;align-items:baseline;justify-content:space-between;'
                f'border-top:4px solid rgba(255,255,255,.25);margin-top:16px;padding-top:10px">'
                f'{satir(t, 100)}{satir(v + "₺<span style=font-size:.34em> /AY</span>", 170, ek="letter-spacing:-.03em")}</div>'
                for t, v in (("1+1", "39.900"), ("2+1", "49.900"))))
    icerik = f"""
  {sol}
  {mb.tilda(280, 200, 290, True)}
  {kira}
  {y(5750, 40, "KENDİ EVİNİZE", 250, 800, "#0b2545", maxw=4200)}
  {y(5750, 300, "ÖDEYİN.", 250, 800, "#e30613", maxw=4200)}
  {y(5762, 600, "60 AY SABİT TAKSİTLE EV SAHİBİ OLUN!", 76, 800, "#a8712a", maxw=4300)}
  {kutu(8550, 300, 2200, 400, yok)}
  {kutu(14250, 60, 2550, 600, kart, "border-radius:40px;background:linear-gradient(160deg,#123a6e,#0b2545);"
        "padding:48px 60px;box-shadow:0 24px 60px rgba(11,37,69,.35)")}
  {damga(16760, 110, 300, "SON", "DAİRELER", "KAÇIRMAYIN!", zemin="#e30613", yazi="#fff")}
  {mb.mia(17050, 260, 300, False)}"""
    return pano(r, "", icerik, 12300)


TASARIMLAR = [(Y, "yol-tabelasi-v2"), (S, "her-ay-ayni-duz-cizgi"), (K, "kiraya-degil-yirtik")]


def sayfa(govde):
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>'
            f'{mb.CSS.replace("__FONT__", mb.FONT)}{v2.CSS_EK}{v4.CSS_EK}{CSS_EK}</style></head>'
            f'<body>{govde}{mb.JS}</body></html>')


def main():
    sec = None
    if "--sadece" in sys.argv:
        sec = {int(v) for v in sys.argv[sys.argv.index("--sadece") + 1].split(",")}
    gecici = tempfile.mkdtemp(prefix="mega5-")
    isler = []
    for i, (fn, ad) in enumerate(TASARIMLAR, 1):
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
