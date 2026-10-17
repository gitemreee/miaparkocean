#!/usr/bin/env python3
"""
180 m dev pano — 6. tur: üç yeni slogan, ferah kompozisyonlar.

  A  EV SAHİBİ OLMANIN ANAHTARI      — 65 m'lik dev altın anahtar, etiketinde fiyatlar
  M  BU MANZARA SİZİN OLABİLİR.      — 50 m'lik pencereden deniz manzarası
  Z  60 AY. SIFIR FAİZ. SIFIR SÜRPRİZ. — üç vuruşluk tipografi

Ödeme: 60 ay sabit taksit (vade) · 1+1 aylık 39.900 ₺ · 2+1 aylık 49.900 ₺ ·
faiz/banka/kredi/ara ödeme yok · son daireler.

    python3.13 scripts/build-mega-bilbord-v6.py [--sadece 1,3]
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


v5 = _yukle("mb_v5", "build-mega-bilbord-v5.py")
v4, v2, mb = v5.v4, v5.v2, v5.mb
OUT = os.path.join(ROOT, "tabela", "mega-bilbord-180m-tur6")
ICERIK = v2.ICERIK
satir, kutu, y, damga, pano = v4.satir, v4.kutu, v4.y, v4.damga, v4.pano
YOKLAR = v4.YOKLAR


def fiyat_satiri(renk="#fff", fs=150, et_renk=None, cizgi="rgba(255,255,255,.3)"):
    et_renk = et_renk or renk
    kol = [f'<div style="padding:0 50px">'
           f'{satir(t + " · AYLIK", round(fs * .36), 800, et_renk, "letter-spacing:.14em")}'
           f'{satir(v + "<span style=font-size:.45em>₺</span>", fs, 800, renk, "letter-spacing:-.03em;margin-top:4px")}</div>'
           for t, v in (("1+1", "39.900"), ("2+1", "49.900"))]
    return (f'<div style="display:flex;align-items:center">{kol[0]}'
            f'<div style="width:4px;align-self:stretch;background:{cizgi}"></div>{kol[1]}</div>')


# ================================================================ A — anahtar
def A():
    r = dict(v4.SERIT_KOYU, zemin="radial-gradient(ellipse 80% 160% at 40% 50%,#0d4a5e 0%,#08303f 55%,#041c26 100%)")
    altin = ('<linearGradient id="ag" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff1c2"/>'
             '<stop offset=".35" stop-color="#e9bd67"/><stop offset=".7" stop-color="#c38b3b"/>'
             '<stop offset="1" stop-color="#8d5d22"/></linearGradient>')
    cx, cy, R, r_ic = 5150, 330, 330, 215
    x_bit, x_son = cx + R - 30, 11900
    sy0, sy1 = 270, 400
    b0 = 10850
    bit = (f'<path d="M{b0} {sy1 - 4} H{x_son} V{sy1 + 200} H{x_son - 180} V{sy1 + 120} H{x_son - 330} '
           f'V{sy1 + 230} H{x_son - 520} V{sy1 + 110} H{x_son - 700} V{sy1 + 180} H{b0} Z" fill="url(#ag)"/>')
    anahtar = (f'<svg class="a" style="left:0;top:0;filter:drop-shadow(0 26px 40px rgba(0,0,0,.5))" '
               f'width="18000" height="{ICERIK}"><defs>{altin}</defs>'
               f'<circle cx="{cx}" cy="{cy}" r="{(R + r_ic) / 2}" fill="none" stroke="url(#ag)" stroke-width="{R - r_ic}"/>'
               f'<rect x="{x_bit}" y="{sy0}" width="{x_son - x_bit}" height="{sy1 - sy0}" rx="26" fill="url(#ag)"/>'
               f'{bit}</svg>')
    govde_yazi = (f'<div class="a tek" style="left:{x_bit + 300}px;top:{sy0 + 22}px;font-size:84px;font-weight:800;'
                  f'color:#5a3a12;letter-spacing:.34em">60 AY SABİT TAKSİT</div>')
    mia_ic = mb.mia(cx - round(300 * mb.MIA_ORAN) // 2, cy - 150, 300, True)
    ex = 8300
    etiket = (f'<div class="a" style="left:{ex - 3}px;top:{sy1}px;width:6px;height:60px;background:#e9bd67"></div>'
              f'<div class="a" style="left:{ex - 300}px;top:{sy1 + 50}px;'
              f'transform:rotate(-2deg);transform-origin:0 0;border-radius:24px 130px 130px 24px;'
              f'background:#fff8ea;box-shadow:0 22px 50px rgba(0,0,0,.45);padding:22px 150px 26px 20px;'
              f'display:flex;align-items:center">'
              f'<div style="position:absolute;right:56px;top:50%;width:56px;height:56px;margin-top:-28px;'
              f'border-radius:50%;background:#08303f"></div>{fiyat_satiri("#0b2545", 150, "#a8712a", "rgba(11,37,69,.18)")}</div>')
    icerik = f"""
  {mb.tilda(300, 200, 290, True)}
  {y(1960, 80, "EV SAHİBİ OLMANIN", 140, 800, "#ffffff", maxw=2700)}
  {y(1950, 230, "ANAHTARI", 300, 800, "", sinif="altin", maxw=2700)}
  {y(1962, 580, "FAİZ YOK · BANKA YOK", 60, 700, "#bfe3ec", sinif="kas", maxw=2700)}\n  {y(1962, 650, "KREDİ YOK · ARA ÖDEME YOK", 60, 700, "#bfe3ec", sinif="kas", maxw=2700)}
  {anahtar}{govde_yazi}{mia_ic}{etiket}
  {damga(16950, 360, 520, "SON", "DAİRELER", "KAÇIRMAYIN!", zemin="#e30613", yazi="#fff")}"""
    return pano(r, "", icerik, 14000)


# ================================================================ M — manzara
def M():
    r = dict(v4.SERIT_ACIK, zemin="linear-gradient(90deg,#f8f3ea 0%,#f3ecdf 50%,#e8f1f8 100%)")
    lac, bronz = "#0b2545", "#6b4a2b"
    deniz = "file://" + os.path.join(ROOT, "signage-source", "balkondan-deniz.jpg")
    x0, x1, y0, y1 = 5150, 10950, 50, 668
    pencere = (f'<div class="a" style="left:{x0}px;top:{y0}px;width:{x1 - x0}px;height:{y1 - y0}px;'
               f'background:url({deniz}) 60% 30%/cover;border:30px solid {bronz};border-radius:10px;'
               f'box-shadow:0 30px 70px rgba(60,40,20,.35),inset 0 0 0 4px rgba(255,255,255,.35)"></div>'
               f'<div class="a" style="left:{x0}px;top:{y0}px;width:{x1 - x0}px;height:{y1 - y0}px;border-radius:10px;'
               f'background:linear-gradient(115deg,rgba(255,255,255,.22) 0%,rgba(255,255,255,0) 30%,'
               f'rgba(255,255,255,0) 60%,rgba(255,255,255,.12) 75%,rgba(255,255,255,0) 90%)"></div>'
               + "".join(f'<div class="a" style="left:{round(x0 + (x1 - x0) * k) - 12}px;top:{y0}px;width:24px;'
                         f'height:{y1 - y0}px;background:{bronz}"></div>' for k in (1 / 3, 2 / 3)))
    kart = (f'<div class="a" style="left:{x1 - 2050}px;top:{y1 - 330}px;border-radius:30px;'
            f'background:#fff;box-shadow:0 24px 60px rgba(11,37,69,.35);padding:26px 10px 30px">'
            f'<div style="padding:0 50px">{satir("60 AY SABİT TAKSİT", 54, 800, "#c40d18", "letter-spacing:.12em;margin-bottom:8px")}</div>'
            f'{fiyat_satiri(lac, 120, "#a8712a", "rgba(11,37,69,.15)")}</div>')
    icerik = f"""
  {mb.tilda(300, 200, 290, False)}
  {y(1950, 60, "BU MANZARA", 260, 800, lac, maxw=3550)}
  {y(1950, 320, "SİZİN OLABİLİR.", 200, 800, "#0f6ea8", maxw=3550)}
  {y(1962, 590, "60 AY SABİT TAKSİTLE EV SAHİBİ OLUN", 70, 800, "#a8712a", maxw=3550)}
  {pencere}{kart}
  {damga(x0 + 240, 150, 360, "SON", "DAİRELER", "KAÇIRMAYIN!", zemin="#e30613", yazi="#fff", don=-12)}
  {kutu(16300, 120, 1550, 480, "".join(
        f'<div class="tek" style="font-size:76px;font-weight:800;color:{lac};margin:4px 0">'
        f'<span style="color:#e30613">✕</span> {t}</div>' for t in ("FAİZ YOK", "BANKA YOK", "KREDİ YOK", "ARA ÖDEME YOK")))}
  {mb.mia(11250, 170, 380, False)}"""
    return pano(r, "", icerik, 14000)


# ================================================================ Z — sıfır sürpriz
def Z():
    r = dict(v4.SERIT_KOYU, zemin="linear-gradient(90deg,#063a7a 0%,#0a56b0 45%,#0b62c4 60%,#08468f 100%)")
    sari = "#ffd21f"
    blok = [("60 AY.", sari, "sabit taksit", 1950),
            ("SIFIR FAİZ.", "#ffffff", "banka yok · kredi yok", 4096),
            ("SIFIR SÜRPRİZ.", "#ffffff", "ara ödeme yok", 7215)]
    s = []
    for metin, renk, alt, x in blok:
        s.append(y(x, 60, metin, 400, 800, renk))
        s.append(y(x + 10, 510, alt.upper(), 84, 700, "#bfdcff", sinif="kas"))
    icerik = f"""
  {mb.tilda(300, 200, 290, True)}
  {"".join(s)}
  {kutu(14050, 70, 2850, 470, f'<div style="padding:0 50px">{satir("60 AY SABİT TAKSİT", 64, 800, sari, "letter-spacing:.1em;margin-bottom:14px")}</div>{fiyat_satiri("#fff", 160, "#bfdcff")}')}
  <div class="a tek" style="left:14100px;top:575px;background:{sari};color:#0b2545;font-size:64px;font-weight:800;
       padding:16px 40px;border-radius:16px;transform:rotate(-2deg)">SON DAİRELER İÇİN FIRSATI KAÇIRMAYIN!</div>
  {mb.mia(17000, 170, 380, True)}"""
    return pano(r, "", icerik, 12150)


TASARIMLAR = [(A, "ev-sahibi-olmanin-anahtari"), (M, "bu-manzara-sizin-olabilir"),
              (Z, "60-ay-sifir-faiz-sifir-surpriz")]


def sayfa(govde):
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>'
            f'{mb.CSS.replace("__FONT__", mb.FONT)}{v2.CSS_EK}{v4.CSS_EK}{v5.CSS_EK}</style></head>'
            f'<body>{govde}{mb.JS}</body></html>')


def main():
    sec = None
    if "--sadece" in sys.argv:
        sec = {int(v) for v in sys.argv[sys.argv.index("--sadece") + 1].split(",")}
    gecici = tempfile.mkdtemp(prefix="mega6-")
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
