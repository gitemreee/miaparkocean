#!/usr/bin/env python3
"""
180 m dev pano — 13. tur: 12/3 üzerinden baştan kurgu, müşterinin sıralamasıyla.

Soldan sağa:
  Tilda logosu · vade + ödeme seçenekleri (60 AY SABİT TAKSİT, dört yıldız rozet) · detay görsel (avlu)
  · fiyat kartı · ana görsel (gündüz render, panodan taşar) · logolar (MİA PARK OCEAN, Ocean Gayrimenkul)
  · detay görsel (salon) · Tilda logosu

Zemin turkuaz → beyaz geçişli. Aile bu kurguda yok (müşteri listesinde geçmedi).

    python3.13 scripts/build-mega-bilbord-v13.py [--pdf]
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


v12 = _yukle("mb_v12", "build-mega-bilbord-v12.py")
v11, v10, v7, v4, v2, mb = v12.v11, v12.v10, v12.v7, v12.v4, v12.v2, v12.mb
OUT = os.path.join(ROOT, "tabela", "mega-bilbord-180m-tur13")
TW = mb.TW
y, kutu, damga, pill, pano = v4.y, v4.kutu, v4.damga, v11.pill, v11.pano
sok, detay, YOK4 = v11.sok, v11.detay, v11.YOK4
KOYU, TURK, KIR, ZEMIN, SERIT = v12.KOYU, v12.TURK, v12.KIR, v12.ZEMIN, v12.SERIT


def fiyat_karti(x, w=2700):
    """Beyaz kart: iki satır fiyat, kırmızı."""
    def sat(tip, tutar):
        return (f'<div style="display:flex;align-items:baseline;gap:40px">'
                f'<div class="tek" style="font-size:96px;font-weight:800;color:{KOYU}">{tip}</div>'
                f'<div class="tek kas" style="font-size:40px;color:#5a7b84">AYLIK</div>'
                f'<div class="tek" style="font-size:168px;font-weight:800;color:{KIR};letter-spacing:-.03em;margin-left:auto">'
                f'{tutar}<span style="font-size:.45em">₺</span></div></div>')
    return (f'<div class="a" style="left:{x}px;top:60px;width:{w}px;height:640px;border-radius:56px;background:#fff;'
            f'box-shadow:0 30px 70px rgba(6,52,63,.28);padding:40px 110px;display:flex;flex-direction:column;justify-content:center;gap:18px">'
            f'{sat("1+1", "39.900")}<div style="height:4px;background:rgba(6,52,63,.18)"></div>{sat("2+1", "49.900")}</div>')


def T():
    tas, ic = v4.bina(11900)
    rozetler = "".join(sok(cx, cy, 310, t.rsplit(" ", 1)[0], "YOK", don=d)
                       for (cx, cy, d), t in zip(((4350, 215, -10), (4740, 215, 7), (4350, 540, 5), (4740, 540, -8)), YOK4))
    ocean = (f'<div class="a" style="left:14700px;top:200px;display:flex;flex-direction:column;align-items:center;gap:26px">'
             f'<div class="tek kas" style="font-size:40px;color:{KOYU}">TEK YETKİLİ SATIŞ</div>{mb.ocean(130, "#0f4c9b", "#2f7fd6")}</div>')
    icerik = f"""
  {mb.tilda(300, 80, 300, True)}
  {y(1900, 30, "60 AY", 340, 800, "#fff", ls="-.03em")}
  {y(1905, 385, "SABİT TAKSİT", 150, 800, "#fff", maxw=2200)}
  {y(1910, 575, "KİRAYA DEĞİL, KENDİ EVİNİZE ÖDEYİN.", 50, 700, "#dff8fb", sinif="kas", maxw=2200)}
  {rozetler}
  {detay(5150, 60, 1700, 640, "signage-source/avlu-havuz-teras.jpg", "50% 62%", 44)}
  {fiyat_karti(7050)}
  {mb.mia(13950, 90, 380, False)}
  {ocean}
  {detay(15650, 60, 1250, 640, "public/images/ic-mekan/05-1plus1-salon.webp", "50% 50%", 44)}
  {mb.tilda(17000, 260, 205, False)}
  {damga(17650, 590, 230, "SON", "DAİRELER", "KAÇIRMAYIN!", zemin=KIR, yazi="#fff")}"""
    return pano(SERIT, ZEMIN, "", icerik, tas, ic)


TASARIMLAR = [(T, "iki-ucta-tilda")]


def main():
    gecici = tempfile.mkdtemp(prefix="mega13-")
    isler = []
    for i, (fn, ad) in enumerate(TASARIMLAR, 1):
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
