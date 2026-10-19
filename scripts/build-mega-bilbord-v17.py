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
B = (1500, 3400, 4600, 7100, 10900, 13400, 14600, 16500)  # panel sınırları (9 panel)
FIYAT = (("1+0", "699.000", "29.900"), ("1+1", "999.000", "39.900"))

RENKLER = {
    "lacivert": dict(koyu="#0f2a5a", koyu2="#17407f", altin="#c9a24a", metin="#0f2a5a", vurgu="#c9a24a"),
    "yesil": dict(koyu="#0f3d2a", koyu2="#1a5c40", altin="#c9a24a", metin="#0f3d2a", vurgu="#c9a24a"),
    "siyah": dict(koyu="#141414", koyu2="#2a2a2a", altin="#d4af37", metin="#141414", vurgu="#d4af37"),
    "bordo": dict(koyu="#6b1020", koyu2="#8c1a2e", altin="#d9b35a", metin="#4a0b16", vurgu="#d9b35a"),
}


D = (-1, 1, -1, 1, -1, 1, -1, 1)   # sınır eğimi: +1 → "/" (üst sağda), -1 → "\\" (üst solda) — beyazlar Λ, fotolar V


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
    ic_w = x1 - x0 - 2 * SK
    return f"""
  <div class="a" style="left:{x0 + SK}px;top:95px;width:{ic_w}px;display:flex;align-items:center;justify-content:center;gap:70px">
    <div style="width:470px;height:260px;border-radius:30px;border:8px solid {p['altin']};flex:none;
         background:linear-gradient(180deg,{p['koyu2']},{p['koyu']});display:flex;align-items:center;justify-content:center;
         box-shadow:0 18px 40px rgba(0,0,0,.25)"><div class="tek" style="font-size:160px;font-weight:800;color:#fff;letter-spacing:-.03em">{tip}</div></div>
    <div><div class="tek kas" style="font-size:46px;font-weight:800;color:{p['metin']}">PEŞİNAT</div>
      <div class="tek" style="font-size:160px;font-weight:800;color:{p['metin']};letter-spacing:-.03em;margin-top:6px">{pesinat}<span style="font-size:.5em;font-weight:700;margin-left:20px">TL</span></div></div>
  </div>
  <div class="a" style="left:{x0 + SK}px;top:415px;width:{ic_w}px;display:flex;align-items:center;justify-content:center;gap:34px">
    <div class="tek" style="font-size:46px;font-weight:800;color:{p['metin']};letter-spacing:.03em">AYDA SADECE
      <span style="font-size:96px;letter-spacing:-.03em;margin-left:12px">{aylik}</span><span style="font-size:50px;font-weight:700;margin-left:14px">TL</span></div>
    <div style="width:4px;height:100px;background:{p['altin']}"></div>
    <div class="tek" style="font-size:46px;font-weight:800;color:{p['metin']};letter-spacing:.03em">60 AY VADE FARKSIZ</div>
  </div>
  <div class="a" style="left:{x0 + SK}px;top:575px;width:{ic_w}px;display:flex;justify-content:center;gap:18px">
    {"".join(f'<div class="tek" style="height:80px;padding:0 30px;border-radius:40px;background:{bg};color:#fff;font-size:36px;font-weight:800;letter-spacing:.04em;display:flex;align-items:center">{t}</div>' for t, bg in zip(("FAİZ YOK!", "BANKA YOK!", "KREDİ YOK!", "ARA ÖDEME YOK!"), ("#111111", "#e3262e", "#111111", "#e3262e")))}
  </div>
  {telefon(cx, 690, p['metin'], 76)}"""


def bilgi_paneli(cx, p, ocean=False):
    """Bilgi paneli: MİA PARK OCEAN logosu · slogan · telefon · siteler (+ Ocean)."""
    s_ = mb.mia(cx - 145, 60, 200, False)
    s_ += y(cx, 300, "MİA PARK OCEAN'DA", 58, 800, p["vurgu"], ek="transform:translateX(-50%);letter-spacing:.04em")
    s_ += y(cx, 366, "YAŞAM BAŞLIYOR.", 70, 800, p["metin"], ek="transform:translateX(-50%);letter-spacing:.02em")
    s_ += telefon(cx, 470, p["metin"], 80)
    s_ += y(cx, 575, "tildainsaat.com &nbsp;·&nbsp; miaparkocean.com", 40, 800, p["vurgu"], ek="transform:translateX(-50%);letter-spacing:.03em")
    if ocean:
        s_ += (f'<div class="a" style="left:{cx}px;top:645px;transform:translateX(-50%);display:flex;align-items:center;gap:30px">'
               f'<div class="tek kas" style="font-size:28px;color:{p["metin"]}">TEK YETKİLİ SATIŞ</div>{mb.ocean(74, "#0f4c9b", "#2f7fd6")}</div>')
    return s_


def tasarim(ad):
    p = RENKLER[ad]
    b1, b2, b3, b4, b5, b6, b7, b8 = B
    d = D
    cx_h = (b4 + b5) / 2
    olcek = (b5 - b4 + 2 * SK) / v4.HW
    tas, _ = v16.bina_olcekli(cx_h, olcek)
    HW, HH = round(v4.HW * olcek), round(v4.HH * olcek)
    hx = round(cx_h - HW / 2)
    orijinal = os.path.join(ROOT, "signage-source", "entrance-gate-genis.png")
    hero = (f'<div class="a" style="left:0;top:0;width:18000px;height:850px;clip-path:{kesik(b4, b5, d[3], d[4])}">'
            f'<img class="a" src="file://{orijinal}" style="left:{hx}px;top:{-mb.EXT}px;width:{HW}px;height:{HH}px"></div>')
    tint = "linear-gradient(180deg,#f4f7fb,#e9eef6)"
    paneller = (beyaz(-SK - 10, b1, 0, d[0]) + beyaz(b1, b2, d[0], d[1], tint) + foto_panel(b2, b3, d[1], d[2], "avlu2")
                + beyaz(b3, b4, d[2], d[3]) + hero + beyaz(b5, b6, d[4], d[5]) + foto_panel(b6, b7, d[5], d[6], "avlu3")
                + beyaz(b7, b8, d[6], d[7], tint) + beyaz(b8, 18000 + SK + 10, d[7], 0))
    cizgiler = "".join(cizgi(b_, d_, p["altin"]) for b_, d_ in zip(B, D))
    icerik = f"""
  {mb.tilda(b1 / 2 - 460, 325, 200, False)}
  {bilgi_paneli((b1 + b2) / 2, p)}
  {fiyat_paneli(b3, b4, *FIYAT[0], p)}
  {fiyat_paneli(b5, b6, *FIYAT[1], p)}
  {bilgi_paneli((b7 + b8) / 2, p, ocean=True)}
  {mb.tilda((b8 + 18000) / 2 - 460, 325, 200, False)}"""
    return f"""
<div class="tasma">{tas}</div>
<div class="pano" style="background:#f1f1f1">
  {paneller}
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
