#!/usr/bin/env python3
"""
180 m dev pano — 12. tur: 11/3 (turkuaz → beyaz, kiraya değil) düzeninin sıkılaştırılmış üç varyantı.

  1  Aile solda      — Tilda · aile · slogan · finans kartı · bina · detay + 3 yuvarlak · MİA · damga
  2  Detaylar solda  — Tilda · slogan · 3 yuvarlak sütun · finans kartı · bina · detay + 3 yuvarlak · aile · MİA
  3  Aile solda, 6 yuvarlak sağda — Tilda · aile · slogan · finans kartı · bina · 2×3 yuvarlak · MİA · damga

    python3.13 scripts/build-mega-bilbord-v12.py [--sadece 1,3] [--pdf]
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


v11 = _yukle("mb_v11", "build-mega-bilbord-v11.py")
v10, v7, v6, v4, v2, mb = v11.v10, v11.v7, v11.v6, v11.v4, v11.v2, v11.mb
OUT = os.path.join(ROOT, "tabela", "mega-bilbord-180m-tur12")
TW = mb.TW
y, kutu, damga, pill, pano = v4.y, v4.kutu, v4.damga, v11.pill, v11.pano
sok, daire_foto, detay, aile, YOK4 = v11.sok, v11.daire_foto, v11.detay, v11.aile, v11.YOK4

KOYU, TURK, KIR = "#06343f", "#0e8a98", "#e3262e"
ZEMIN = "linear-gradient(90deg,#0b7f8d 0%,#15a0ae 20%,#6cc6d1 38%,#d9eff2 50%,#ffffff 60%,#ffffff 100%)"
SERIT = dict(v4.SERIT_ACIK, serit=KOYU, serit_su="#5fd3e0")


def slogan(x, renk="#fff"):
    return (y(x, 55, "KİRAYA DEĞİL,", 190, 800, renk, maxw=2250) + y(x, 262, "KENDİ EVİNİZE", 190, 800, renk, maxw=2250)
            + y(x, 470, "ÖDEYİN.", 190, 800, "#dff8fb" if renk == "#fff" else renk, maxw=2250))


def finans_karti(x, w=4050):
    """Beyaz kart: 60 ay rozeti + kırmızı fiyatlar + dört yıldız rozet."""
    kart = (f'<div class="a" style="left:{x}px;top:60px;width:{w}px;height:640px;border-radius:56px;background:#fff;'
            'box-shadow:0 30px 70px rgba(6,52,63,.28)"></div>')
    bx = x + w - 700
    yoklar = "".join(sok(cx, cy, 310, t.rsplit(" ", 1)[0], "YOK", don=d)
                     for (cx, cy, d), t in zip(((bx, 215, -10), (bx + 390, 215, 7), (bx, 540, 5), (bx + 390, 540, -8)), YOK4))
    return (kart + pill(x + 300, 130, "60 AY SABİT TAKSİT", KOYU, "#fff", 64, 130, "letter-spacing:.08em")
            + kutu(x + 250, 300, 3000, 300, v6.fiyat_satiri(KIR, 170, KOYU, "rgba(6,52,63,.25)")) + yoklar)


def detay_blogu(x):
    """Avlu render'ı + altında üç yuvarlak detay (1700 px genişlik)."""
    return (detay(x, 60, 1700, 400, "signage-source/avlu-havuz-teras.jpg", "50% 62%", 40)
            + daire_foto(x + 140, 600, 236, "salon") + daire_foto(x + 850, 600, 236, "mutfak") + daire_foto(x + 1560, 600, 236, "park"))


# ================================================================ 1 — aile solda
def B1():
    tas, ic = v4.bina(11500)
    icerik = f"""
  {mb.tilda(300, 70, 300, True)}
  {aile(1700, 950, -15)}
  {slogan(3100)}
  {finans_karti(5150)}
  {detay_blogu(13550)}
  {mb.mia(15700, 80, 420, False)}
  {damga(17200, 400, 360, "SON", "DAİRELER", "KAÇIRMAYIN!", zemin=KIR, yazi="#fff")}"""
    return pano(SERIT, ZEMIN, "", icerik, tas, ic)


# ================================================================ 2 — detaylar solda sütun, aile sağda
def B2():
    tas, ic = v4.bina(10700)
    sutun = (daire_foto(4330, 165, 205, "yatak") + daire_foto(4330, 385, 205, "teras") + daire_foto(4330, 605, 205, "deniz"))
    icerik = f"""
  {mb.tilda(300, 70, 300, True)}
  {slogan(1950)}
  {sutun}
  {finans_karti(4600)}
  {detay_blogu(12750)}
  {aile(14600, 950, -15)}
  {mb.mia(16000, 70, 400, False)}
  {damga(17480, 530, 330, "SON", "DAİRELER", "KAÇIRMAYIN!", zemin=KIR, yazi="#fff")}"""
    return pano(SERIT, ZEMIN, "", icerik, tas, ic)


# ================================================================ 3 — aile solda, sağda 2×3 yuvarlak
def B3():
    tas, ic = v4.bina(11300)
    adlar = ("salon", "mutfak", "yatak", "teras", "park", "deniz")
    izgara = "".join(daire_foto(13500 + (i % 3) * 330, 200 + (i // 3) * 330, 290, ad) for i, ad in enumerate(adlar))
    icerik = f"""
  {mb.tilda(300, 70, 300, True)}
  {aile(1700, 950, -15)}
  {slogan(3100)}
  {finans_karti(5150)}
  {izgara}
  {detay(14700, 60, 1500, 640, "signage-source/avlu-havuz-teras.jpg", "50% 62%", 40) if False else ""}
  {mb.mia(15000, 80, 420, False)}
  {detay(15900, 60, 1300, 640, "signage-source/avlu-havuz-teras.jpg", "42% 60%", 40)}
  {damga(17550, 530, 300, "SON", "DAİRELER", "KAÇIRMAYIN!", zemin=KIR, yazi="#fff")}"""
    return pano(SERIT, ZEMIN, "", icerik, tas, ic)


TASARIMLAR = [(B1, "aile-solda"), (B2, "detaylar-solda"), (B3, "aile-solda-alti-yuvarlak")]


def main():
    sec = None
    if "--sadece" in sys.argv:
        sec = {int(v) for v in sys.argv[sys.argv.index("--sadece") + 1].split(",")}
    gecici = tempfile.mkdtemp(prefix="mega12-")
    isler = []
    for i, (fn, ad) in enumerate(TASARIMLAR, 1):
        if sec and i not in sec:
            continue
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
