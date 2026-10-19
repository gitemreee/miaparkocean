#!/usr/bin/env python3
"""
180 m dev pano — 17. tur: müşterinin "cool" referansı (17.webp) — eğik altın kenarlı paneller.

Soldan sağa: Tilda · dikey foto · 1+0 fiyat paneli · ana görsel (gündüz render, panodan taşar) ·
1+1 fiyat paneli · dikey foto · Tilda. Paneller paralelkenar, aralarında ince altın çizgi.
444 1 058 Tilda logolarının ve fiyatların altında. Dört renk seçeneği.

Peşinat tutarları (699.000 / 999.000 TL) referans görselden alındı [DOĞRULANACAK].

    python3.13 scripts/build-mega-bilbord-v17.py [--sadece 1,3] [--pdf]
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


v16 = _yukle("mb_v16", "build-mega-bilbord-v16.py")
v14, v11, v7, v4, v2, mb = v16.v14, v16.v11, v16.v7, v16.v4, v16.v2, v16.mb
OUT = os.path.join(ROOT, "tabela", "mega-bilbord-180m-tur17")
TW = mb.TW
y, kutu, satir = v4.y, v4.kutu, v4.satir
F = v14.F

SK = 110                                   # panel kenarı eğimi (px, üstte sağa / altta sola)
B = (2430, 3960, 7080, 11080, 14040, 15570)  # panel sınırları
FIYAT = (("1+0", "699.000", "29.900"), ("1+1", "999.000", "39.900"))

RENKLER = {
    "lacivert": dict(koyu="#0f2a5a", koyu2="#17407f", altin="#c9a24a", metin="#0f2a5a", vurgu="#c9a24a"),
    "yesil": dict(koyu="#0f3d2a", koyu2="#1a5c40", altin="#c9a24a", metin="#0f3d2a", vurgu="#c9a24a"),
    "siyah": dict(koyu="#141414", koyu2="#2a2a2a", altin="#d4af37", metin="#141414", vurgu="#d4af37"),
    "bordo": dict(koyu="#6b1020", koyu2="#8c1a2e", altin="#d9b35a", metin="#4a0b16", vurgu="#d9b35a"),
}


def kesik(x0, x1):
    """x0–x1 arası paralelkenar (üst kenar sağa kaymış)."""
    return f"polygon({x0 + SK}px 0,{x1 + SK}px 0,{x1 - SK}px 100%,{x0 - SK}px 100%)"


def beyaz(x0, x1, bg="#ffffff"):
    return f'<div class="a" style="left:0;top:0;width:18000px;height:850px;background:{bg};clip-path:{kesik(x0, x1)}"></div>'


def foto_panel(x0, x1, ad, pos="50% 50%"):
    w = x1 - x0 + 2 * SK
    return (f'<div class="a" style="left:{x0 - SK}px;top:0;width:{w}px;height:850px;'
            f'clip-path:polygon({2 * SK}px 0,100% 0,{w - 2 * SK}px 100%,0 100%);'
            f'background:url({F[ad]}) {pos}/cover no-repeat"></div>')


def cizgi(b, altin):
    w = 16
    return (f'<div class="a" style="left:{b - SK - w // 2}px;top:0;width:{2 * SK + w}px;height:850px;'
            f'background:linear-gradient(180deg,{altin},#fff5d6 50%,{altin});'
            f'clip-path:polygon({2 * SK}px 0,{2 * SK + w}px 0,{w}px 100%,0 100%)"></div>')


def telefon(cx, top, renk, fs=64):
    simge = v2.IK_TEL.replace("<svg", f'<svg style="width:{round(fs * 1.05)}px;height:{round(fs * 1.05)}px;flex:none"', 1)
    return (f'<div class="a tek" style="left:{cx}px;top:{top}px;display:flex;align-items:center;gap:18px;color:{renk};'
            f'font-size:{fs}px;font-weight:800;letter-spacing:.02em;transform:translateX(-50%)">{simge}444 1 058</div>')


def fiyat_paneli(x0, x1, tip, pesinat, aylik, p):
    cx = (x0 + x1) / 2
    return f"""
  <div class="a" style="left:{x0 + SK}px;top:105px;width:{x1 - x0 - 2 * SK}px;display:flex;align-items:center;justify-content:center;gap:90px">
    <div style="width:560px;height:300px;border-radius:34px;border:8px solid {p['altin']};flex:none;
         background:linear-gradient(180deg,{p['koyu2']},{p['koyu']});display:flex;align-items:center;justify-content:center;
         box-shadow:0 18px 40px rgba(0,0,0,.25)"><div class="tek" style="font-size:190px;font-weight:800;color:#fff;letter-spacing:-.03em">{tip}</div></div>
    <div><div class="tek kas" style="font-size:52px;font-weight:800;color:{p['metin']}">PEŞİNAT</div>
      <div class="tek" style="font-size:190px;font-weight:800;color:{p['metin']};letter-spacing:-.03em;margin-top:6px">{pesinat}<span style="font-size:.5em;font-weight:700"> TL</span></div></div>
  </div>
  <div class="a" style="left:{x0 + SK}px;top:465px;width:{x1 - x0 - 2 * SK}px;display:flex;align-items:center;justify-content:center;gap:40px">
    <div class="tek" style="font-size:54px;font-weight:800;color:{p['metin']};letter-spacing:.04em">AYDA SADECE
      <span style="font-size:110px;letter-spacing:-.03em;margin-left:14px">{aylik}</span><span style="font-size:58px;font-weight:700">TL</span></div>
    <div style="width:4px;height:120px;background:{p['altin']}"></div>
    <div class="tek" style="font-size:54px;font-weight:800;color:{p['metin']};letter-spacing:.04em">60 AY VADE FARKSIZ</div>
  </div>
  {y(cx, 640, "FAİZ YOK · BANKA YOK · KREDİ YOK · ARA ÖDEME YOK", 36, 700, p['vurgu'], sinif="kas", ek="transform:translateX(-50%)")}
  {telefon(cx, 715, p['metin'], 56)}"""


def tasarim(ad):
    p = RENKLER[ad]
    b1, b2, b3, b4, b5, b6 = B
    tas, ic = v4.bina((b3 + b4) / 2)
    gok = (f'<div class="a" style="left:0;top:0;width:18000px;height:850px;clip-path:{kesik(b3, b4)};'
           f'background:linear-gradient(180deg,#cfe3f3 0%,#eef6fb 60%,#f6f9fc 100%)"></div>')
    paneller = (beyaz(-SK - 10, b1) + foto_panel(b1, b2, "avlu2") + beyaz(b2, b3) + gok + beyaz(b4, b5)
                + foto_panel(b5, b6, "avlu3") + beyaz(b6, 18000 + SK + 10))
    cizgiler = "".join(cizgi(b, p["altin"]) for b in B)
    icerik = f"""
  {mb.tilda(1215 - 585, 170, 255, False)}
  {telefon(1215, 500, p['metin'], 66)}
  {y(1215, 600, "miaparkocean.com", 46, 700, p['vurgu'], ek="transform:translateX(-50%);letter-spacing:.04em")}
  {fiyat_paneli(b2, b3, *FIYAT[0], p)}
  {fiyat_paneli(b4, b5, *FIYAT[1], p)}
  {mb.tilda(16785 - 585, 110, 255, False)}
  {telefon(16785, 430, p['metin'], 66)}
  {mb.mia(16785 - 560, 560, 230, False)}
  {y(16785 + 110, 585, "TEK YETKİLİ SATIŞ", 30, 600, p['metin'], sinif="kas")}
  {kutu(16785 + 90, 630, 520, 120, mb.ocean(76, "#0f4c9b", "#2f7fd6"))}"""
    return f"""
<div class="tasma">{tas}</div>
<div class="pano" style="background:#f1f1f1">
  {paneller}
  {ic}
  {cizgiler}
  {icerik}
</div>"""


TASARIMLAR = [(lambda: tasarim("lacivert"), "lacivert-altin"), (lambda: tasarim("yesil"), "yesil-altin"),
              (lambda: tasarim("siyah"), "siyah-altin"), (lambda: tasarim("bordo"), "bordo-altin")]


def main():
    sec = None
    if "--sadece" in sys.argv:
        sec = {int(v) for v in sys.argv[sys.argv.index("--sadece") + 1].split(",")}
    gecici = tempfile.mkdtemp(prefix="mega17-")
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
