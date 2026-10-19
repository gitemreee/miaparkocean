#!/usr/bin/env python3
"""
180 m dev pano — 14. tur: beş serbest konsept; fotoğraflar kare kart değil, yumuşak geçişli.

Fotoğraflar kenarlarından zemine erir (CSS mask gradyanları), iki farklı aile kesiği kullanılır,
gerçek proje render'ları panonun üstünden taşar.

  1  Gece & altın     — IŞIKLARI SİZİN İÇİN YAKTIK.          (gece render, lacivert, altın finans)
  2  Krem editoryal   — Yeni bir hayata, sabit taksitle.     (serif, kiremit fiyatlar, foto kolajı)
  3  Turkuaz akış     — KİRAYA DEĞİL, KENDİ EVİNİZE ÖDEYİN.  (turkuaz → beyaz, erimiş fotoğraflar)
  4  Yeşil & çocuklar — ÇOCUKLARINIZ İÇİN GÜVENLİ BİR GELECEK (park fotoğrafı, onay listesi)
  5  Gün batımı       — GÜNÜN EN GÜZEL SAATİ: EVE DÖNÜŞ.     (gün batımı render, şeftali gök)

    python3.13 scripts/build-mega-bilbord-v14.py [--sadece 1,3] [--pdf]
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
v10, v9, v8 = v11.v10, _yukle("mb_v9", "build-mega-bilbord-v9.py"), _yukle("mb_v8", "build-mega-bilbord-v8.py")
v7, v6, v4, v2, mb = v11.v7, v11.v6, v11.v4, v11.v2, v11.mb
OUT = os.path.join(ROOT, "tabela", "mega-bilbord-180m-tur14")
TW = mb.TW
y, kutu, damga, pill, pano = v4.y, v4.kutu, v4.damga, v11.pill, v11.pano
sok, onay_liste, YOK4, YOKLAR = v11.sok, v11.onay_liste, v11.YOK4, v4.YOKLAR
F = v10.F
F["avlu2"] = "file://" + os.path.join(ROOT, "signage-source", "avlu-havuz-teras.jpg")
F["kapi"] = "file://" + os.path.join(ROOT, "signage-source", "entrance-gate.jpg")


def _aile_yolu(ad):
    p = os.path.join(ROOT, "signage-source", "aile", ad)
    im = Image.open(p).size
    return "file://" + p, im[0] / im[1]


AILE1 = _aile_yolu("aile-kesik.png")
AILE2 = _aile_yolu("aile2-kesik.png")


def aile(x, ah, kim=AILE1, top=None):
    src, oran = kim
    top = 910 - ah if top is None else top
    return (f'<img class="a" src="{src}" style="left:{x}px;top:{top}px;height:{ah}px;width:{round(ah * oran)}px;'
            f'filter:drop-shadow(0 30px 40px rgba(0,0,0,.3))">')


def yumusak(x, y_, w, h, ad, pos="50% 50%", yatay=(.14, .14), dikey=(0, 0), ek=""):
    """Kenarları zemine eriyen fotoğraf bandı (yatay ve dikey gradyan maske)."""
    mh = f"linear-gradient(90deg,transparent 0,#000 {yatay[0] * 100:.0f}%,#000 {100 - yatay[1] * 100:.0f}%,transparent 100%)"
    mv = f"linear-gradient(180deg,transparent 0,#000 {dikey[0] * 100:.0f}%,#000 {100 - dikey[1] * 100:.0f}%,transparent 100%)"
    return (f'<div class="a" style="left:{x}px;top:{y_}px;width:{w}px;height:{h}px;-webkit-mask-image:{mh};mask-image:{mh};{ek}">'
            f'<div style="position:absolute;inset:0;background:url({F[ad]}) {pos}/cover no-repeat;'
            f'-webkit-mask-image:{mv};mask-image:{mv}"></div></div>')


def fiyat_dikey(x, top, renk, et, fs=150):
    """İki satır fiyat: etiket solda, tutar sağda."""
    def sat(tip, tutar):
        return (f'<div style="display:flex;align-items:baseline;gap:34px"><div class="tek" style="font-size:{round(fs * .5)}px;font-weight:800;color:{et}">{tip}</div>'
                f'<div class="tek kas" style="font-size:{round(fs * .25)}px;color:{et};opacity:.8">AYLIK</div>'
                f'<div class="tek" style="font-size:{fs}px;font-weight:800;color:{renk};letter-spacing:-.03em;margin-left:auto">{tutar}<span style="font-size:.45em">₺</span></div></div>')
    return (f'<div class="a" style="left:{x}px;top:{top}px;display:flex;flex-direction:column;gap:14px;min-width:1500px">'
            f'{sat("1+1", "39.900")}{sat("2+1", "49.900")}</div>')


# ================================================================ 1 — gece & altın
def K1():
    lac, altin = "#0a1428", "#e2b45c"
    r = dict(v4.SERIT_ACIK, serit="#060c1c", serit_su=altin, serit_logo="#e9c27a")
    zemin = "linear-gradient(90deg,#0a1428 0%,#102044 35%,#15284f 50%,#102044 65%,#0a1428 100%)"
    tas, ic = v8.gece_bina(9000, 1.8)
    icerik = f"""
  {mb.tilda(300, 80, 300, True)}
  {y(1900, 70, "IŞIKLARI", 170, 800, "#fff", maxw=2500)}
  {y(1900, 255, "SİZİN İÇİN", 170, 800, "", sinif="altin", maxw=2500)}
  {y(1900, 440, "YAKTIK.", 170, 800, "", sinif="altin", maxw=2500)}
  {y(1905, 640, "60 AY SABİT TAKSİT · FAİZ YOK · BANKA YOK", 44, 700, "#cdd6ea", sinif="kas", maxw=2500)}
  {yumusak(4300, 0, 2400, 718, "balkon", "50% 40%", (.2, .25), (0, .15))}
  {pill(12050, 70, "60 AY SABİT TAKSİT", altin, lac, 60, 120, "letter-spacing:.08em")}
  {fiyat_dikey(12050, 230, "#ffe2a3", "#fff", 150)}
  {y(12060, 630, YOKLAR, 42, 700, "#cdd6ea", sinif="kas", maxw=3000)}
  {aile(15150, 900, AILE2)}
  {mb.mia(16700, 90, 360, True)}
  {damga(17600, 580, 230, "SON", "DAİRELER", "KAÇIRMAYIN!", zemin=altin, yazi=lac)}"""
    return pano(r, zemin, "", icerik, tas, ic)


# ================================================================ 2 — krem editoryal
def K2():
    lac, kir = "#1c2742", "#c8482f"
    r = dict(v4.SERIT_ACIK, serit=lac, serit_su="#ff9b73")
    zemin = "linear-gradient(90deg,#f7f1e7 0%,#fbf7f0 50%,#f5efe4 100%)"
    tas, ic = v4.bina(10000)
    icerik = f"""
  {mb.tilda(300, 80, 300, False)}
  {y(1900, 60, "Yeni bir hayata,", 200, 600, lac, sinif="fr", maxw=3400)}
  {y(1900, 290, "sabit taksitle.", 270, 600, kir, sinif="fr", maxw=3400)}
  {y(1910, 620, "60 AY · " + YOKLAR, 42, 700, "#6b5b4b", sinif="kas", maxw=3400)}
  {yumusak(5500, 0, 2700, 718, "avlu2", "50% 60%", (.18, .22), (0, .12))}
  {yumusak(11900, 0, 2300, 718, "salon", "50% 50%", (.22, .2), (0, .12))}
  {fiyat_dikey(14300, 110, kir, lac, 160)}
  {y(14310, 560, "SON DAİRELER · FIRSATI KAÇIRMAYIN", 44, 800, kir, sinif="kas", maxw=1800)}
  {aile(16050, 900, AILE1)}
  {mb.mia(17300, 100, 300, False)}"""
    return pano(r, zemin, "", icerik, tas, ic)


# ================================================================ 3 — turkuaz akış
def K3():
    koyu, kir = "#06343f", "#e3262e"
    r = dict(v4.SERIT_ACIK, serit=koyu, serit_su="#5fd3e0")
    zemin = "linear-gradient(90deg,#0b7f8d 0%,#15a0ae 18%,#6cc6d1 34%,#d9eff2 46%,#ffffff 58%,#ffffff 100%)"
    tas, ic = v4.bina(9400)
    rozetler = "".join(sok(12300 + i * 360, 620, 250, t.rsplit(" ", 1)[0], "YOK", don=d)
                       for i, (t, d) in enumerate(zip(YOK4, (-10, 7, 5, -8))))
    icerik = f"""
  {mb.tilda(300, 80, 300, True)}
  {y(1900, 55, "KİRAYA DEĞİL,", 190, 800, "#fff", maxw=2400)}
  {y(1900, 262, "KENDİ EVİNİZE", 190, 800, "#fff", maxw=2400)}
  {y(1900, 470, "ÖDEYİN.", 190, 800, "#dff8fb", maxw=2400)}
  {yumusak(4300, 0, 2800, 718, "avlu2", "50% 62%", (.2, .25), (0, .12))}
  {pill(12050, 60, "60 AY SABİT TAKSİT", koyu, "#fff", 60, 120, "letter-spacing:.08em")}
  {kutu(12000, 215, 3200, 300, v6.fiyat_satiri(kir, 160, koyu, "rgba(6,52,63,.25)"))}
  {rozetler}
  {aile(15350, 950, AILE1, -15)}
  {mb.mia(16750, 80, 380, False)}
  {damga(17600, 580, 230, "SON", "DAİRELER", "KAÇIRMAYIN!", zemin=kir, yazi="#fff")}"""
    return pano(r, zemin, "", icerik, tas, ic)


# ================================================================ 4 — yeşil & çocuklar
def K4():
    yesil, acik = "#123d2a", "#2f8a4e"
    r = dict(v4.SERIT_ACIK, serit=yesil, serit_su="#8fd1a6")
    zemin = "linear-gradient(90deg,#eef5ef 0%,#f8fbf8 45%,#e9f3eb 100%)"
    tas, ic = v4.bina(9900)
    icerik = f"""
  {mb.tilda(300, 80, 300, False)}
  {y(1900, 60, "ÇOCUKLARINIZ İÇİN", 165, 800, acik, maxw=2900)}
  {y(1900, 245, "GÜVENLİ BİR", 200, 800, yesil, maxw=2900)}
  {y(1900, 460, "GELECEK.", 200, 800, yesil, maxw=2900)}
  {yumusak(4800, 0, 2800, 718, "park", "50% 55%", (.2, .25), (0, .12))}
  {aile(11850, 950, AILE1, -15)}
  {pill(13300, 60, "60 AY SABİT TAKSİT", acik, "#fff", 60, 120, "letter-spacing:.08em")}
  {kutu(13250, 215, 3200, 300, v6.fiyat_satiri(yesil, 160, acik, "rgba(18,61,42,.25)"))}
  {onay_liste(13300, 540, yesil, acik, "#fff", 44, 90, 1500)}
  {mb.mia(16700, 80, 380, False)}
  {damga(17600, 580, 230, "SON", "DAİRELER", "KAÇIRMAYIN!", zemin=acik, yazi="#fff")}"""
    return pano(r, zemin, "", icerik, tas, ic)


# ================================================================ 5 — gün batımı
def K5():
    lac, mercan = "#1c2742", "#b9452e"
    r = dict(v4.SERIT_ACIK, serit=lac, serit_su="#ff9b73")
    tas, ic, gx = v9.bina(9000)
    zemin = (f"radial-gradient(ellipse 1500px 1100px at {gx}px 0px,rgba(255,247,214,.95) 0%,rgba(253,230,190,.6) 40%,rgba(253,230,190,0) 100%),"
             "linear-gradient(90deg,#f6e6d4 0%,#f4dcc0 30%,#f6dfc4 45%,#f1d4b6 70%,#ead0b4 100%)")
    icerik = f"""
  {mb.tilda(300, 80, 300, False)}
  {y(1900, 70, "GÜNÜN EN GÜZEL SAATİ:", 120, 800, lac, maxw=2500)}
  {y(1900, 215, "EVE", 260, 800, mercan)}
  {y(1900, 480, "DÖNÜŞ.", 200, 800, mercan)}
  {yumusak(4400, 0, 2400, 718, "balkon", "50% 45%", (.2, .25), (0, .12))}
  {yumusak(10700, 0, 2300, 718, "teras", "50% 50%", (.25, .2), (0, .12))}
  {pill(13150, 60, "60 AY SABİT TAKSİT", lac, "#fff", 60, 120, "letter-spacing:.08em")}
  {kutu(13100, 215, 3200, 300, v6.fiyat_satiri(mercan, 160, lac, "rgba(28,39,66,.25)"))}
  {y(13160, 560, YOKLAR, 46, 700, lac, sinif="kas", maxw=3100)}
  {aile(15900, 900, AILE2)}
  {mb.mia(17100, 90, 330, False)}
  {damga(17650, 590, 220, "SON", "DAİRELER", "KAÇIRMAYIN!", zemin=mercan, yazi="#fff")}"""
    return pano(r, zemin, "", icerik, tas, ic)


TASARIMLAR = [(K1, "gece-altin"), (K2, "krem-editoryal"), (K3, "turkuaz-akis"), (K4, "yesil-cocuklar"), (K5, "gun-batimi")]


def main():
    sec = None
    if "--sadece" in sys.argv:
        sec = {int(v) for v in sys.argv[sys.argv.index("--sadece") + 1].split(",")}
    gecici = tempfile.mkdtemp(prefix="mega14-")
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
