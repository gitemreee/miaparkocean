#!/usr/bin/env python3
"""
180 m dev pano — 8. tur: Higgsfield'da üretilmiş sinematik sahneler üzerine gerçek proje görselleri.

Sahne (signage-source/hf-bilbord8/*.png, Higgsfield / nano banana) panonun ortasına yerleşir,
kenarlarına doğru satır renklerinden türetilmiş kesintisiz geçişe erir; böylece 80 + 20 + 80 m
parçalar tek bir manzara gibi okunur. Bina her zaman gerçek render (yapay zekâ binası yok).

  1  GÜNÜN EN GÜZEL SAATİ: EVE DÖNÜŞ.   — gün batımında körfez, şeftali & lacivert
  2  IŞIKLARI SİZİN İÇİN YAKTIK.          — mavi saat, gece render'ı, lacivert & altın
  3  NEFES ALAN BİR YAŞAM.               — güneşli park, gök mavisi & orman yeşili

Ödeme: 60 ay sabit taksit (vade) · 1+1 aylık 39.900 ₺ · 2+1 aylık 49.900 ₺ ·
faiz/banka/kredi/ara ödeme yok · son daireler.

    python3.13 scripts/build-mega-bilbord-v8.py [--sadece 1,3] [--pdf]
"""

import importlib.util as _il
import json
import os
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

Image.MAX_IMAGE_PIXELS = None
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _yukle(ad, dosya):
    spec = _il.spec_from_file_location(ad, os.path.join(ROOT, "scripts", dosya))
    m = _il.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


v7 = _yukle("mb_v7", "build-mega-bilbord-v7.py")
v6, v5, v4, v2, mb = v7.v6, v7.v5, v7.v4, v7.v2, v7.mb
OUT = os.path.join(ROOT, "tabela", "mega-bilbord-180m-tur8")
SAHNE = os.path.join(ROOT, "signage-source", "hf-bilbord8")
ICERIK, TW, EXT, PH = v2.ICERIK, mb.TW, mb.EXT, mb.PH
satir, kutu, y, damga = v4.satir, v4.kutu, v4.y, v4.damga
fiyat_satiri = v6.fiyat_satiri
OLCEK = 0.5          # zemin görselinin css px başına pikseli (önizleme)


# ---------------------------------------------------------------- zemin: sahne + kesintisiz geçiş
def zemin(ad, ufuk, hedef_ufuk, merkez, genislik, yumusak=1400):
    """Sahneyi `merkez` etrafında `genislik` css px'e yerleştirir; dışı satır ortalamalarıyla uzar.

    ufuk: sahnede ufkun yükseklik oranı · hedef_ufuk: panoda ufkun oranı (0 = üst kenar).
    """
    W, H = round(TW * OLCEK), round(PH * OLCEK)
    src = Image.open(os.path.join(SAHNE, f"{ad}.png")).convert("RGB")
    s = genislik * OLCEK / src.width
    bh = H / s                                        # sahneden alınacak bant yüksekliği (kaynak px)
    y0 = ufuk * src.height - hedef_ufuk * bh
    y0 = max(0, min(src.height - bh, y0))
    bant = src.crop((0, round(y0), src.width, round(y0 + bh))).resize((round(genislik * OLCEK), H), Image.LANCZOS)
    b = np.asarray(bant).astype(np.float32)
    bw, bx = b.shape[1], round((merkez - genislik / 2) * OLCEK)
    # sahneyi aynalayarak tüm genişliğe döşe (dikiş yok), dışını yatayda çok yumuşat
    sutun = np.arange(W) - bx
    k, m = np.divmod(sutun, bw)
    idx = np.where(k % 2 == 0, m, bw - 1 - m)
    dose = b[:, idx]
    R = round(900 * OLCEK)
    pad = np.pad(dose, ((0, 0), (R, R), (0, 0)), mode="reflect")
    cs = np.cumsum(pad, axis=1)
    cs = np.concatenate([np.zeros_like(cs[:, :1]), cs], axis=1)
    uzak = (cs[:, 2 * R:2 * R + W] - cs[:, :W]) / (2 * R)
    uzak = np.asarray(Image.fromarray(uzak.clip(0, 255).astype(np.uint8))
                      .filter(ImageFilter.GaussianBlur(5))).astype(np.float32)
    a = np.zeros(W, np.float32)
    a[max(0, bx):min(W, bx + bw)] = 1
    f = round(yumusak * OLCEK)
    rampa = np.linspace(0, 1, f) ** 1.5
    a[bx:bx + f] = rampa[:max(0, min(f, W - bx))]
    a[bx + bw - f:bx + bw] = rampa[::-1][:max(0, min(f, W - (bx + bw - f)))]
    a = a[None, :, None]
    son = dose * a + uzak * (1 - a)
    yol = os.path.join(SAHNE, f"zemin-{ad}.jpg")
    Image.fromarray(son.clip(0, 255).astype(np.uint8)).save(yol, quality=92)
    return yol


# ---------------------------------------------------------------- binalar (gerçek render)
def gunduz_bina(cx, filtre=""):
    """Gündüz kahraman render'ı (gökyüzü maskeli) — v4.bina ile aynı geometri, renk filtresi ile."""
    tas, ic = v4.bina(cx)
    if filtre:
        tas = tas.replace('style="', f'style="filter:{filtre};', 1)
        ic = ic.replace('style="', f'style="filter:{filtre};', 1)
    return tas, ic


GECE_KAYNAK = "gece-genis-ham.png"   # night-gate-temiz.jpg, Higgsfield ile 21:9'a genişletildi
GECE_SINIR = 700     # pano üst kenarına denk gelen satır
GECE_CATILAR = [     # (x0, x1, üst) — dört bloğun çatı döşemesi + çatı üstü kütlesi, 3168 px kaynakta
    (380, 1110, 468), (540, 980, 440), (1005, 1407, 444), (1005, 1335, 423),
    (1765, 2185, 448), (1855, 2185, 427), (2060, 2788, 470), (2185, 2648, 440),
]


def gece_maskeli():
    yol = os.path.join(SAHNE, "gece-maskeli.png")
    im = Image.open(os.path.join(SAHNE, GECE_KAYNAK)).convert("RGB")
    m = Image.new("L", im.size, 0)
    d = ImageDraw.Draw(m)
    d.rectangle((0, GECE_SINIR, im.width, im.height), fill=255)
    for x0, x1, ust in GECE_CATILAR:
        d.rectangle((x0, ust, x1, GECE_SINIR), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(1.2))
    a = np.asarray(m).astype(np.float32) / 255
    f = 380                                           # yan kenarlar zemine erisin
    r = np.linspace(0, 1, f) ** 1.4
    a[:, :f] *= r
    a[:, -f:] *= r[::-1]
    im.putalpha(Image.fromarray((a * 255).astype(np.uint8)))
    im.save(yol)
    return yol


def gece_bina(cx, olcek=1.8):
    src = gece_maskeli()
    W0, H0 = Image.open(src).size
    w, h = round(W0 * olcek), round(H0 * olcek)
    x, ust = round(cx - w / 2), round(EXT - GECE_SINIR * olcek)
    stil = f'left:{x}px;top:{{t}}px;width:{w}px;height:{h}px'
    tas = f'<img class="a" src="file://{src}" style="{stil.format(t=ust)}">'
    ic = f'<img class="a" src="file://{src}" style="{stil.format(t=ust - EXT)}">'
    return tas, ic


def pano(r, zemin_yol, arka, icerik, bina):
    tas, ic = bina
    return f"""
<div class="tasma">{tas}</div>
<div class="pano" style="background:url(file://{zemin_yol}) 0 0/100% 100% no-repeat">
  {arka}
  {ic}
  {icerik}
  {v2.serit(r)}
</div>"""


def fiyat_blok(x, y_, renk, et, cizgi, baslik_renk, fs=160, w=3300, stil=""):
    ic = (f'<div style="padding:0 50px">{satir("60 AY SABİT TAKSİT", round(fs * .42), 800, baslik_renk, "letter-spacing:.1em;margin-bottom:12px")}</div>'
          + fiyat_satiri(renk, fs, et, cizgi))
    return kutu(x, y_, w, 500, ic, stil)


# ================================================================ 1 — eve dönüş (gün batımı)
def G():
    zy = zemin("gun-batimi", ufuk=.69, hedef_ufuk=.66, merkez=7700, genislik=9000)
    lac, mercan = "#1c2742", "#b9452e"
    r = dict(v4.SERIT_ACIK, serit=lac, serit_su="#ff9b73")
    # sol: metin okunurluğu için çok hafif açık perde, sağ: lacivert-şeftali perde
    arka = ('<div class="a" style="left:0;top:0;width:6400px;height:850px;'
            'background:linear-gradient(90deg,rgba(255,236,220,.35) 0%,rgba(255,236,220,.2) 70%,rgba(255,236,220,0) 100%)"></div>')
    kart = ("width:fit-content;border-radius:44px;background:rgba(28,39,66,.82);padding:44px 0 36px;"
            "box-shadow:0 24px 60px rgba(28,39,66,.35)")
    icerik = f"""
  {mb.tilda(300, 200, 290, False)}
  {y(1950, 80, "GÜNÜN EN GÜZEL SAATİ:", 150, 800, lac, maxw=4800)}
  {y(1935, 245, "EVE DÖNÜŞ.", 320, 800, mercan, maxw=4800, ls="-.02em")}
  {y(1955, 600, "60 AY SABİT TAKSİTLE EV SAHİBİ OLUN", 68, 700, lac, sinif="kas", maxw=4600)}
  {fiyat_blok(13150, 50, "#fff", "#ffd2bd", "rgba(255,255,255,.35)", "#ffb08f", fs=150, stil=kart)}
  {y(13200, 600, v4.YOKLAR, 60, 700, lac, sinif="kas", maxw=3000)}
  {mb.mia(16350, 140, 420, False)}
  {damga(17500, 370, 380, "SON", "DAİRELER", "KAÇIRMAYIN!", zemin="#c8482f", yazi="#fff")}"""
    return pano(r, zy, arka, icerik, gunduz_bina(11050, "sepia(.2) saturate(1.1) brightness(1.02)"))


# ================================================================ 2 — ışıklar (gece)
def I():
    zy = zemin("mavi-saat", ufuk=.665, hedef_ufuk=.72, merkez=9600, genislik=9000)
    r = dict(v4.SERIT_ACIK, serit="#0a1428", serit_su="#e2b45c", serit_logo="#e9c27a")
    arka = ('<div class="a" style="left:0;top:0;width:18000px;height:850px;'
            'background:linear-gradient(90deg,rgba(5,10,24,.55) 0%,rgba(5,10,24,.15) 30%,rgba(5,10,24,0) 45%,'
            'rgba(5,10,24,0) 62%,rgba(5,10,24,.25) 75%,rgba(5,10,24,.6) 100%)"></div>')
    icerik = f"""
  {mb.tilda(300, 200, 290, True)}
  {y(1950, 75, "IŞIKLARI", 170, 800, "#ffffff", maxw=4600)}
  {y(1935, 255, "SİZİN İÇİN YAKTIK.", 230, 800, "", sinif="altin", maxw=4600)}
  {y(1955, 560, "60 AY SABİT TAKSİTLE EV SAHİBİ OLUN", 68, 700, "#d9e2f2", sinif="kas", maxw=4600)}
  {fiyat_blok(13000, 70, "#ffe2a3", "#d9e2f2", "rgba(233,194,122,.45)", "#e9c27a")}
  {y(13060, 575, v4.YOKLAR, 62, 700, "#d9e2f2", sinif="kas", maxw=3200)}
  {mb.mia(16150, 120, 450, True)}
  {damga(17450, 380, 390, "SON", "DAİRELER", "KAÇIRMAYIN!", zemin="#e2b45c", yazi="#0a1428")}"""
    return pano(r, zy, arka, icerik, gece_bina(9300, 1.8))


# ================================================================ 3 — nefes alan yaşam (gündüz park)
def N():
    zy = zemin("sabah-gok", ufuk=.62, hedef_ufuk=.55, merkez=7600, genislik=6200)
    yesil = "#123d2a"
    r = dict(v4.SERIT_ACIK, serit=yesil, serit_su="#8fd1a6")
    arka = ('<div class="a" style="left:0;top:0;width:7000px;height:850px;'
            'background:linear-gradient(90deg,rgba(255,255,255,.62) 0%,rgba(255,255,255,.4) 75%,rgba(255,255,255,0) 100%)"></div>')
    kart = "border-radius:44px;background:rgba(18,61,42,.9);padding:44px 0;width:fit-content;box-shadow:0 24px 60px rgba(10,40,25,.35)"
    icerik = f"""
  {mb.tilda(300, 200, 290, False)}
  {y(1950, 80, "NEFES ALAN", 170, 800, yesil, maxw=4600)}
  {y(1935, 255, "BİR YAŞAM.", 300, 800, "#2f8a4e", maxw=4600, ls="-.02em")}
  {y(1955, 600, "60 AY SABİT TAKSİTLE EV SAHİBİ OLUN", 68, 700, yesil, sinif="kas", maxw=4600)}
  {fiyat_blok(13050, 60, "#fff", "#cfeedd", "rgba(255,255,255,.3)", "#9fe0b5", fs=150, stil=kart)}
  {y(13100, 610, v4.YOKLAR, 60, 700, yesil, sinif="kas", maxw=3000, ek="text-shadow:0 0 18px rgba(255,255,255,.9)")}
  {mb.mia(16300, 150, 410, False)}
  {damga(17500, 370, 380, "SON", "DAİRELER", "KAÇIRMAYIN!", zemin="#2f8a4e", yazi="#fff")}"""
    return pano(r, zy, arka, icerik, gunduz_bina(10800))


TASARIMLAR = [(G, "eve-donus"), (I, "isiklari-sizin-icin-yaktik"), (N, "nefes-alan-bir-yasam")]


def main():
    sec = None
    if "--sadece" in sys.argv:
        sec = {int(v) for v in sys.argv[sys.argv.index("--sadece") + 1].split(",")}
    gecici = tempfile.mkdtemp(prefix="mega8-")
    isler = []
    for i, (fn, ad) in enumerate(TASARIMLAR, 1):
        if sec and i not in sec:
            continue
        hp = os.path.join(gecici, f"{i}.html")
        open(hp, "w", encoding="utf-8").write(v7.sayfa(fn()))
        isler.append(dict(html=hp, w=TW, h=mb.TH, dsf=0.5, dilim=TW,
                          cikti=os.path.join(gecici, f"{i}"), no=i, ad=ad))
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
