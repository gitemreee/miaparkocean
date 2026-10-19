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
B = (2430, 3960, 7110, 11050, 14200, 15730)  # panel sınırları
FIYAT = (("1+0", "699.000", "29.900"), ("1+1", "999.000", "39.900"))

RENKLER = {
    "lacivert": dict(koyu="#0f2a5a", koyu2="#17407f", altin="#c9a24a", metin="#0f2a5a", vurgu="#c9a24a"),
    "yesil": dict(koyu="#0f3d2a", koyu2="#1a5c40", altin="#c9a24a", metin="#0f3d2a", vurgu="#c9a24a"),
    "siyah": dict(koyu="#141414", koyu2="#2a2a2a", altin="#d4af37", metin="#141414", vurgu="#d4af37"),
    "bordo": dict(koyu="#6b1020", koyu2="#8c1a2e", altin="#d9b35a", metin="#4a0b16", vurgu="#d9b35a"),
}


D = (-1, 1, -1, 1, -1, 1)   # sınır eğimi: +1 → "/" (üst sağda), -1 → "\\" (üst solda) — beyazlar Λ, fotolar V


def kesik(x0, x1, dL, dR):
    """x0–x1 arası yamuk: sol kenar dL, sağ kenar dR eğimli."""
    return (f"polygon({x0 + dL * SK}px 0,{x1 + dR * SK}px 0,{x1 - dR * SK}px 100%,{x0 - dL * SK}px 100%)")


def beyaz(x0, x1, dL, dR, bg="#ffffff"):
    return f'<div class="a" style="left:0;top:0;width:18000px;height:850px;background:{bg};clip-path:{kesik(x0, x1, dL, dR)}"></div>'


def foto_panel(x0, x1, dL, dR, ad, pos="50% 50%"):
    """V biçimli fotoğraf paneli; fotoğraf çerçeveye tam oturur (keskin kenar)."""
    w = x1 - x0 + 2 * SK
    return (f'<div class="a" style="left:{x0 - SK}px;top:0;width:{w}px;height:850px;'
            f'clip-path:polygon({SK + dL * SK}px 0,{w - SK + dR * SK}px 0,{w - SK - dR * SK}px 100%,{SK - dL * SK}px 100%);'
            f'background:url({F[ad]}) {pos}/cover no-repeat"></div>')


def cizgi(b, d, altin):
    w = 16
    ust, alt = (2 * SK, 0) if d > 0 else (0, 2 * SK)
    return (f'<div class="a" style="left:{b - SK - w // 2}px;top:0;width:{2 * SK + w}px;height:850px;'
            f'background:linear-gradient(180deg,{altin},#fff5d6 50%,{altin});'
            f'clip-path:polygon({ust}px 0,{ust + w}px 0,{alt + w}px 100%,{alt}px 100%)"></div>')


def telefon(cx, top, renk, fs=64):
    simge = v2.IK_TEL.replace("<svg", f'<svg style="width:{round(fs * 1.05)}px;height:{round(fs * 1.05)}px;flex:none"', 1)
    return (f'<div class="a tek" style="left:{cx}px;top:{top}px;display:flex;align-items:center;gap:18px;color:{renk};'
            f'font-size:{fs}px;font-weight:800;letter-spacing:.02em;transform:translateX(-50%)">{simge}444 10 58</div>')


def fiyat_paneli(x0, x1, tip, pesinat, aylik, p):
    cx = (x0 + x1) / 2
    return f"""
  <div class="a" style="left:{x0 + SK}px;top:85px;width:{x1 - x0 - 2 * SK}px;display:flex;align-items:center;justify-content:center;gap:90px">
    <div style="width:560px;height:300px;border-radius:34px;border:8px solid {p['altin']};flex:none;
         background:linear-gradient(180deg,{p['koyu2']},{p['koyu']});display:flex;align-items:center;justify-content:center;
         box-shadow:0 18px 40px rgba(0,0,0,.25)"><div class="tek" style="font-size:190px;font-weight:800;color:#fff;letter-spacing:-.03em">{tip}</div></div>
    <div><div class="tek kas" style="font-size:52px;font-weight:800;color:{p['metin']}">PEŞİNAT</div>
      <div class="tek" style="font-size:190px;font-weight:800;color:{p['metin']};letter-spacing:-.03em;margin-top:6px">{pesinat}<span style="font-size:.5em;font-weight:700;margin-left:22px">TL</span></div></div>
  </div>
  <div class="a" style="left:{x0 + SK}px;top:445px;width:{x1 - x0 - 2 * SK}px;display:flex;align-items:center;justify-content:center;gap:40px">
    <div class="tek" style="font-size:54px;font-weight:800;color:{p['metin']};letter-spacing:.04em">AYDA SADECE
      <span style="font-size:110px;letter-spacing:-.03em;margin-left:14px">{aylik}</span><span style="font-size:58px;font-weight:700;margin-left:16px">TL</span></div>
    <div style="width:4px;height:120px;background:{p['altin']}"></div>
    <div class="tek" style="font-size:54px;font-weight:800;color:{p['metin']};letter-spacing:.04em">60 AY VADE FARKSIZ</div>
  </div>
  <div class="a" style="left:{x0 + SK}px;top:600px;width:{x1 - x0 - 2 * SK}px;display:flex;justify-content:center;gap:26px">
    {"".join(f'<div class="tek" style="height:86px;padding:0 36px;border-radius:43px;background:{bg};color:#fff;font-size:40px;font-weight:800;letter-spacing:.05em;display:flex;align-items:center">{t}</div>' for t, bg in zip(("FAİZ YOK!", "BANKA YOK!", "KREDİ YOK!", "ARA ÖDEME YOK!"), ("#111111", "#e3262e", "#111111", "#e3262e")))}
  </div>
  {telefon(cx, 715, p['metin'], 80)}"""


def uc_panel(cx, p, ocean=False):
    """Uç panel: Tilda · MİA PARK OCEAN (+ Ocean) · slogan · telefon · siteler."""
    s_ = mb.tilda(cx - 460, 55, 200, False)
    if ocean:
        s_ += mb.mia(cx - 420, 285, 170, False)
        s_ += (f'<div class="a" style="left:{cx + 30}px;top:300px;display:flex;flex-direction:column;align-items:center;gap:10px">'
               f'<div class="tek kas" style="font-size:28px;color:{p["metin"]}">TEK YETKİLİ SATIŞ</div>{mb.ocean(72, "#0f4c9b", "#2f7fd6")}</div>')
    else:
        s_ += mb.mia(cx - 123, 285, 170, False)
    s_ += y(cx, 478, "MİA PARK OCEAN'DA", 56, 800, p["vurgu"], ek="transform:translateX(-50%);letter-spacing:.04em")
    s_ += y(cx, 542, "YAŞAM BAŞLIYOR.", 64, 800, p["metin"], ek="transform:translateX(-50%);letter-spacing:.02em")
    s_ += telefon(cx, 628, p["metin"], 72)
    s_ += y(cx, 722, "tildainsaat.com &nbsp;·&nbsp; miaparkocean.com", 40, 800, p["vurgu"], ek="transform:translateX(-50%);letter-spacing:.03em")
    return s_


def tasarim(ad):
    p = RENKLER[ad]
    b1, b2, b3, b4, b5, b6 = B
    tas, ic = v16.bina_olcekli((b3 + b4) / 2, 1.12)
    HW, HH = round(v4.HW * 1.12), round(v4.HH * 1.12)
    hx = round((b3 + b4) / 2 - HW / 2)
    orijinal = os.path.join(ROOT, "signage-source", "entrance-gate-genis.png")
    gok = (f'<div class="a" style="left:0;top:0;width:18000px;height:850px;clip-path:{kesik(b3, b4, D[2], D[3])}">'
           f'<img class="a" src="file://{orijinal}" style="left:{hx}px;top:{-mb.EXT}px;width:{HW}px;height:{HH}px"></div>')
    ic = ""
    paneller = (beyaz(-SK - 10, b1, 0, D[0]) + foto_panel(b1, b2, D[0], D[1], "avlu2") + beyaz(b2, b3, D[1], D[2]) + gok
                + beyaz(b4, b5, D[3], D[4]) + foto_panel(b5, b6, D[4], D[5], "avlu3") + beyaz(b6, 18000 + SK + 10, D[5], 0))
    cizgiler = "".join(cizgi(b, d, p["altin"]) for b, d in zip(B, D))
    icerik = f"""
  {uc_panel(1215, p)}
  {fiyat_paneli(b2, b3, *FIYAT[0], p)}
  {fiyat_paneli(b4, b5, *FIYAT[1], p)}
  {uc_panel(16865, p, ocean=True)}"""
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
