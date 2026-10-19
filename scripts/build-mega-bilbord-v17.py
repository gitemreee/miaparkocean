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
B = (1500, 3050, 4850, 7200, 10800, 13150, 14950, 16500)  # panel sınırları (9 panel)
MIA_PNG = os.path.join(ROOT, "public", "brand", "logo-mia-2026.png")   # orijinal logo (1024×712)
MIA_RENK = "#1d7f9c"
FIYAT = (("1+0", "699.000", "29.900"), ("1+1", "999.000", "39.900"))

RENKLER = {
    "lacivert": dict(koyu="#0f2a5a", koyu2="#17407f", altin="#c9a24a", metin="#0f2a5a", vurgu="#c9a24a"),
    "yesil": dict(koyu="#0f3d2a", koyu2="#1a5c40", altin="#c9a24a", metin="#0f3d2a", vurgu="#c9a24a"),
    "siyah": dict(koyu="#141414", koyu2="#2a2a2a", altin="#d4af37", metin="#141414", vurgu="#d4af37"),
    "bordo": dict(koyu="#6b1020", koyu2="#8c1a2e", altin="#d9b35a", metin="#4a0b16", vurgu="#d9b35a"),
}


D = (1, -1, 1, -1, 1, -1, 1, -1)   # fotoğraflar ve bina V (üstü geniş), beyazlar Λ — sınır eğimi: +1 → "/" (üst sağda), -1 → "\\" (üst solda) — beyazlar Λ, fotolar V


def kirik_desen():
    """Açık tonlu kırık (düşük poligon) desen — panel zemini. Bir kez üretilir."""
    yol = os.path.join(ROOT, "signage-source", "desen-kirik.svg")
    if os.path.exists(yol):
        return "file://" + yol
    import random
    from scipy.spatial import Delaunay
    random.seed(7)
    W, H = 18000, 850
    pts = [(random.uniform(-200, W + 200), random.uniform(-200, H + 200)) for _ in range(520)]
    pts += [(-300, -300), (W + 300, -300), (-300, H + 300), (W + 300, H + 300)]
    tri = Delaunay(pts)
    tonlar = ["#ffffff", "#f8fafc", "#f1f5f9", "#eaf0f6", "#e3eaf2", "#f5f7fa", "#edf2f7"]
    poly = []
    for a, b, c in tri.simplices:
        renk = random.choice(tonlar)
        poly.append(f'<polygon points="{pts[a][0]:.0f},{pts[a][1]:.0f} {pts[b][0]:.0f},{pts[b][1]:.0f} {pts[c][0]:.0f},{pts[c][1]:.0f}" fill="{renk}" stroke="#ffffff" stroke-width="3"/>')
    open(yol, "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{"".join(poly)}</svg>')
    return "file://" + yol


def kesik(x0, x1, dL, dR):
    """x0–x1 arası yamuk: sol kenar dL, sağ kenar dR eğimli."""
    return (f"polygon({x0 + dL * SK}px 0,{x1 + dR * SK}px 0,{x1 - dR * SK}px 100%,{x0 - dL * SK}px 100%)")


def beyaz(x0, x1, dL, dR, bg=None):
    bg = bg or f"url({kirik_desen()}) 0 0/18000px 850px no-repeat"
    return f'<div class="a" style="left:0;top:0;width:18000px;height:850px;background:{bg};clip-path:{kesik(x0, x1, dL, dR)}"></div>'


YAN_FOTO = {   # çerçeve fotoğrafı, gök maskeli kesik, taşmada gösterilecek sütunlar (bina blokları)
    "avlu2": ("signage-source/avlu-havuz-teras.jpg", "signage-source/avlu-havuz-teras-kesik.png", [(0.26, 0.445), (0.455, 0.70)]),
    "balkon_avlu": ("signage-source/balkondan-avlu.jpg", "signage-source/balkondan-avlu-kesik.png", [(0.0, 1.0)]),
    "avlu_aksam": ("signage-source/avlu-aksam.jpg", "signage-source/avlu-aksam-kesik.png", [(0.12, 0.33), (0.34, 0.42)]),
    "cocuk_parki": ("signage-source/cocuk-parki.jpg", "signage-source/cocuk-parki-kesik.png", [(0.50, 1.0)]),
    "gece": ("signage-source/hf-bilbord8/gece-genis-ham.png", "signage-source/hf-bilbord8/gece-maskeli.png", [(0.31, 0.45), (0.555, 0.70)], 1800),
}


def foto_panel(x0, x1, dL, dR, ad):
    """V çerçeve panoda kalır; fotoğraf alt kenara dayalı büyütülür, çerçeve üstünde yalnızca
    gök maskeli bina silüeti (seçili sütunlar) görünür → (tasma katmanı, pano katmanı)."""
    tam, kesik_png, sutunlar, *ek = YAN_FOTO[ad]
    H = ek[0] if ek else 850 + mb.EXT
    ust = 850 + mb.EXT - H                     # tuval koordinatında üst kenar (≤ 0)
    im_w, im_h = Image.open(os.path.join(ROOT, tam)).size
    w = round(H * im_w / im_h)
    cx = (x0 + x1) / 2
    left = round(cx - w / 2)
    dur = []
    for a_, b_ in sutunlar:
        dur += [f"transparent {a_ * 100:.1f}%", f"#000 {a_ * 100:.1f}%", f"#000 {b_ * 100:.1f}%", f"transparent {b_ * 100:.1f}%"]
    maske = "linear-gradient(90deg," + ",".join(dur) + ")"
    tasma = (f'<img class="a" src="file://{os.path.join(ROOT, kesik_png)}" style="left:{left}px;top:{ust}px;width:{w}px;height:{H}px;'
             f'-webkit-mask-image:{maske}">')
    pano_ = (f'<div class="a" style="left:0;top:0;width:18000px;height:850px;clip-path:{kesik(x0, x1, dL, dR)}">'
             f'<img class="a" src="file://{os.path.join(ROOT, tam)}" style="left:{left}px;top:{ust - mb.EXT}px;width:{w}px;height:{H}px"></div>')
    return tasma, pano_


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
    dL, dR = D[B.index(x0)], D[B.index(x1)]
    return f"""
  <div class="a" style="left:0;top:0;width:18000px;height:850px;background:rgba(255,255,255,.45);clip-path:{kesik(x0, x1, dL, dR)}"></div>
  <div class="a" style="left:{x0 + SK}px;top:95px;width:{ic_w}px;display:flex;align-items:center;justify-content:center;gap:70px">
    <div style="width:420px;height:234px;border-radius:28px;border:8px solid {p['altin']};flex:none;
         background:linear-gradient(180deg,{p['koyu2']},{p['koyu']});display:flex;align-items:center;justify-content:center;
         box-shadow:0 18px 40px rgba(0,0,0,.25)"><div class="tek" style="font-size:144px;font-weight:800;color:#fff;letter-spacing:-.03em">{tip}</div></div>
    <div><div class="tek kas" style="font-size:46px;font-weight:800;color:{p['metin']}">PEŞİNAT</div>
      <div class="tek" style="font-size:176px;font-weight:800;color:{p['metin']};letter-spacing:-.03em;margin-top:6px">{pesinat}<span style="font-size:.5em;font-weight:700;margin-left:20px">TL</span></div></div>
  </div>
  <div class="a" style="left:{x0 + SK}px;top:415px;width:{ic_w}px;display:flex;align-items:center;justify-content:center;gap:34px">
    <div class="tek" style="font-size:42px;font-weight:800;color:{p['metin']};letter-spacing:.02em">AYDA SADECE
      <span style="font-size:92px;letter-spacing:-.03em;margin-left:10px">{aylik}</span><span style="font-size:46px;font-weight:700;margin-left:12px">TL</span></div>
    <div style="width:4px;height:100px;background:{p['altin']}"></div>
    <div class="tek" style="font-size:42px;font-weight:800;color:{p['metin']};letter-spacing:.02em">60 AY VADE FARKSIZ</div>
  </div>
  <div class="a" style="left:{x0 + SK}px;top:575px;width:{ic_w}px;display:flex;justify-content:center;gap:18px">
    {"".join(f'<div class="tek" style="height:80px;padding:0 30px;border-radius:40px;background:{bg};color:#fff;font-size:36px;font-weight:800;letter-spacing:.04em;display:flex;align-items:center">{t}</div>' for t, bg in zip(("FAİZ YOK!", "BANKA YOK!", "KREDİ YOK!", "ARA ÖDEME YOK!"), ("#111111", "#e3262e", "#111111", "#e3262e")))}
  </div>
  {telefon(cx, 690, p['metin'], 76)}"""


def mia_orj(cx, top, h):
    w = round(h * 1024 / 712)
    return f'<img class="a" src="file://{MIA_PNG}" style="left:{cx - w // 2}px;top:{top}px;width:{w}px;height:{h}px">'


def bilgi_paneli(cx, p, ocean=False):
    """Bilgi paneli: orijinal MİA PARK OCEAN logosu · slogan (logo renginde) · site (+ Ocean logosu)."""
    s_ = mia_orj(cx, 40, 300)
    s_ += y(cx, 375, "MİA PARK OCEAN'DA", 70, 800, MIA_RENK, ek="transform:translateX(-50%);letter-spacing:.04em")
    s_ += y(cx, 455, "YERİNİZİ ALIN!", 104, 800, MIA_RENK, ek="transform:translateX(-50%);letter-spacing:.01em")
    s_ += y(cx, 590, "miaparkocean.com", 50, 800, p["vurgu"], ek="transform:translateX(-50%);letter-spacing:.04em")
    if ocean:
        s_ += kutu(cx - 300, 665, 600, 130, mb.ocean(78, "#0f4c9b", "#2f7fd6"), "display:flex;justify-content:center")
    return s_


def tilda_paneli(cx, p):
    return (mb.tilda(cx - 540, 170, 235, False)
            + telefon(cx, 490, p["metin"], 80)
            + y(cx, 600, "tildainsaat.com", 52, 800, p["vurgu"], ek="transform:translateX(-50%);letter-spacing:.04em"))


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
    tint = None
    f1t, f1 = foto_panel(b2, b3, d[1], d[2], "avlu2")
    f2t, f2 = foto_panel(b6, b7, d[5], d[6], "gece")
    paneller = (beyaz(-SK - 10, b1, 0, d[0]) + beyaz(b1, b2, d[0], d[1], tint) + f1
                + beyaz(b3, b4, d[2], d[3]) + hero + beyaz(b5, b6, d[4], d[5]) + f2
                + beyaz(b7, b8, d[6], d[7], tint) + beyaz(b8, 18000 + SK + 10, d[7], 0))
    cizgiler = "".join(cizgi(b_, d_, p["altin"]) for b_, d_ in zip(B, D))
    tas = f1t + f2t + tas
    icerik = f"""
  {tilda_paneli(b1 / 2, p)}
  {bilgi_paneli((b1 + b2) / 2, p)}
  {fiyat_paneli(b3, b4, *FIYAT[0], p)}
  {fiyat_paneli(b5, b6, *FIYAT[1], p)}
  {bilgi_paneli((b7 + b8) / 2, p, ocean=True)}
  {tilda_paneli((b8 + 18000) / 2, p)}"""
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
