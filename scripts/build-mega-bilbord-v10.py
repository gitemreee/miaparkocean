#!/usr/bin/env python3
"""
180 m dev pano — 10. tur: müşterinin gönderdiği beş şablon düzeni, gerçek proje görselleriyle.

Her tasarımda: gün batımı render'ı (gök maskeli, panonun üstünden taşar), iç/dış mekândan
2-3 detay fotoğrafı, Tilda + MİA PARK OCEAN logoları, alt şerit. 5'te mutlu aile.

  1  Ferah / zeytin yeşili  — YENİ EVİNİZE HOŞ GELDİNİZ          (Borcelle şablonu)
  2  Simetrik / serif       — YAŞAM BAŞLIYOR, iki yanda bina      (Thynk Property)
  3  Arduvaz panel / turuncu çerçeve — HAYALİNİZDEKİ EV SİZİ BEKLİYOR (Dream Home)
  4  Beyaz / asılı fiyat etiketi — YENİ YAŞAM BURADA BAŞLIYOR     (Smart Living)
  5  Turuncu eğik panel / mutlu aile — HAYALİNİZDEKİ EVE BUGÜN ADIM ATIN (Find Your Home)

Ödeme: 60 ay sabit taksit (vade) · 1+1 aylık 39.900 ₺ · 2+1 aylık 49.900 ₺ ·
faiz/banka/kredi/ara ödeme yok · son daireler.

    python3.13 scripts/build-mega-bilbord-v10.py [--sadece 1,3] [--pdf]
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


v9 = _yukle("mb_v9", "build-mega-bilbord-v9.py")
v8 = _yukle("mb_v8", "build-mega-bilbord-v8.py")
v7, v6, v4, v2, mb = v9.v7, v9.v7.v6, v9.v4, v9.v2, v9.mb
OUT = os.path.join(ROOT, "tabela", "mega-bilbord-180m-tur10")
EXT, TW = mb.EXT, mb.TW
y, kutu, satir, damga = v4.y, v4.kutu, v4.satir, v4.damga
YOKLAR = v4.YOKLAR

IMG = lambda *p: "file://" + os.path.join(ROOT, *p)
F = {
    "salon": IMG("public", "images", "ic-mekan", "05-1plus1-salon.webp"),
    "yatak": IMG("public", "images", "ic-mekan", "06-1plus1-yatak-odasi.webp"),
    "mutfak": IMG("public", "images", "ic-mekan", "07-1plus1-mutfak.webp"),
    "dubleks": IMG("public", "images", "ic-mekan", "11-dubleks-salon.webp"),
    "teras": IMG("public", "images", "ic-mekan", "13-bahceli-daire-terasi.webp"),
    "avlu": IMG("public", "images", "ic-mekan", "15-balkondan-avlu.webp"),
    "park": IMG("public", "images", "ic-mekan", "19-cocuk-oyun-parki.webp"),
    "deniz": IMG("public", "images", "ic-mekan", "21-balkondan-deniz.webp"),
    "pergola": IMG("public", "images", "terrace-pergola.webp"),
    "balkon": IMG("public", "images", "balcony-dusk.webp"),
}
AILE = IMG("signage-source", "aile", "aile-kesik.png")
AILE_ORAN = Image.open(os.path.join(ROOT, "signage-source", "aile", "aile-kesik.png")).size
AILE_ORAN = AILE_ORAN[0] / AILE_ORAN[1]


def foto(x, y_, w, h, ad, r=44, ek="", pos="50% 50%", golge=True):
    g = "box-shadow:0 22px 50px rgba(0,0,0,.22);" if golge else ""
    return (f'<div class="a" style="left:{x}px;top:{y_}px;width:{w}px;height:{h}px;border-radius:{r}px;'
            f'background:url({F[ad]}) {pos}/cover no-repeat;{g}{ek}"></div>')


def pill(x, y_, metin, bg, renk, fs=60, h=130, ek=""):
    return (f'<div class="a tek" style="left:{x}px;top:{y_}px;height:{h}px;padding:0 {round(h * .45)}px;border-radius:{h}px;'
            f'background:{bg};color:{renk};font-size:{fs}px;font-weight:800;display:flex;align-items:center;'
            f'letter-spacing:.04em;{ek}">{metin}</div>')


def fiyatlar(renk, fs=150, et="", cizgi="rgba(0,0,0,.2)"):
    return v6.fiyat_satiri(renk, fs, et or renk, cizgi)


def kart_bina(cx, kenar_renk, kenar=24, top=60, h=640, r=60, golge="0 30px 70px rgba(0,0,0,.28)"):
    """Yuvarlatılmış çerçeveli fotoğraf kartı; binalar kartın üstünden ve panodan taşar.

    Kart içinde orijinal render (gökyüzüyle), üstünde aynı geometride gök maskeli kopya →
    bina çerçeveden dışarı çıkar."""
    tas, ic, _ = v9.bina(cx)
    hx = round(cx - v9.HW / 2)
    ic_img = (f'<img class="a" src="file://{v9.HERO}" style="left:{kenar}px;top:{v9.HY - EXT - top - kenar}px;'
              f'width:{v9.HW}px;height:{v9.HH}px">')
    kart = (f'<div class="a" style="left:{hx - kenar}px;top:{top}px;width:{v9.HW + 2 * kenar}px;height:{h}px;'
            f'border-radius:{r}px;overflow:hidden;background:{kenar_renk};box-shadow:{golge}">'
            f'<div class="a" style="left:{kenar}px;top:{kenar}px;right:{kenar}px;bottom:{kenar}px;'
            f'border-radius:{r - kenar}px;overflow:hidden;background:#dfe6ee">'
            f'<img class="a" src="file://{v9.HERO}" style="left:0;top:{v9.HY - EXT - top - kenar}px;'
            f'width:{v9.HW}px;height:{v9.HH}px"></div></div>')
    return tas, kart + ic


def pano(r, zemin, arka, icerik, tas, ic):
    return f"""
<div class="tasma">{tas}</div>
<div class="pano" style="background:{zemin}">
  {arka}
  {ic}
  {icerik}
  {v2.serit(r)}
</div>"""


# ================================================================ 1 — ferah, zeytin yeşili
def D1():
    zeytin, acik = "#3f4a1f", "#6f8a2a"
    r = dict(v4.SERIT_ACIK, serit=zeytin, serit_su="#c9dd8a")
    zemin = "linear-gradient(90deg,#dbe7f2 0%,#f6f8fa 22%,#ffffff 50%,#f4f8ee 80%,#dfeccb 100%)"
    tas, ic, _ = v9.bina(3300)
    perde = ('<div class="a" style="left:3300px;top:0;width:1800px;height:850px;'
             'background:linear-gradient(90deg,rgba(255,255,255,0),rgba(255,255,255,.85) 70%,#fff)"></div>')
    icerik = f"""
  {mb.tilda(300, 90, 260, False)}
  {y(5200, 40, "YENİ EVİNİZE", 340, 700, zeytin, sinif="yol", maxw=4000)}
  {y(5200, 390, "HOŞ GELDİNİZ.", 340, 700, zeytin, sinif="yol", maxw=4000)}
  {pill(9500, 80, "60 AY SABİT TAKSİT", acik, "#fff", 58, 120)}
  {kutu(9450, 240, 3600, 300, fiyatlar(zeytin, 150, "#5a6630", "rgba(63,74,31,.25)"))}
  {y(9500, 600, YOKLAR, 56, 700, "#5a6630", sinif="kas", maxw=3500)}
  {foto(13350, 60, 1500, 640, "salon")}
  {foto(15000, 60, 1500, 640, "teras")}
  {mb.mia(16700, 180, 370, False)}"""
    return pano(r, zemin, "", icerik, tas, perde + ic)


# ================================================================ 2 — simetrik, serif
def D2():
    r = dict(v4.SERIT_ACIK, serit="#1c2742", serit_su="#e2b45c")
    zemin = "linear-gradient(90deg,#d9e4ef 0%,#edf3f9 28%,#f3f7fb 50%,#edf3f9 72%,#d9e4ef 100%)"
    tas1, ic1 = v4.bina(2500)
    tas2, ic2 = v8.gece_bina(15700, 1.8)
    icerik = f"""
  {mb.tilda(4750, 300, 230, False)}
  {mb.mia(8815, 30, 250, False)}
  {y(9000, 305, "YAŞAM BAŞLIYOR", 290, 600, "#2b2f3a", sinif="fr", ek="transform:translateX(-50%)")}
  {pill(9000, 625, "60 AY SABİT TAKSİT &nbsp;·&nbsp; 1+1 AYLIK 39.900₺ &nbsp;·&nbsp; 2+1 AYLIK 49.900₺", "#c9973f", "#1c2742", 54, 90, "transform:translateX(-50%);letter-spacing:.06em")}
  {foto(11600, 60, 1400, 300, "yatak", 36)}
  {foto(11600, 400, 1400, 300, "avlu", 36)}"""
    return pano(r, zemin, "", icerik, tas1 + tas2, ic1 + ic2)


# ================================================================ 3 — arduvaz panel, turuncu çerçeve
def D3():
    ard, tur = "#3e4f5c", "#f28c1a"
    r = dict(v4.SERIT_ACIK, serit=ard, serit_su=tur)
    zemin = "linear-gradient(90deg,#e4e9ee 0%,#f3f5f8 50%,#e9edf1 100%)"
    tas, ic = kart_bina(13200, tur, 24)
    panel = (f'<div class="a" style="left:1750px;top:60px;width:9550px;height:640px;border-radius:64px;background:{ard};'
             'box-shadow:0 26px 60px rgba(40,55,70,.3)"></div>')
    etiket = (f'<div class="a tek" style="left:13250px;top:500px;height:180px;padding:0 70px;background:{tur};color:#fff;'
              f'font-size:70px;font-weight:800;display:flex;align-items:center;gap:40px;transform:skewX(-10deg);'
              f'box-shadow:0 20px 40px rgba(0,0,0,.3)"><span style="font-weight:600;font-size:.7em;letter-spacing:.08em">AYLIK</span>'
              f'1+1 &nbsp;39.900₺ <span style="opacity:.6">|</span> 2+1 &nbsp;49.900₺</div>')
    icerik = f"""
  {mb.tilda(300, 290, 240, False)}
  {panel}
  {y(2080, 130, f'HAYALİNİZDEKİ <span style="color:{tur}">EV</span>', 215, 800, "#fff", maxw=5400)}
  {y(2080, 360, "SİZİ BEKLİYOR.", 215, 800, "#fff", maxw=5400)}
  {y(2090, 600, YOKLAR + " · 60 AY SABİT TAKSİT", 46, 700, "#cfd9e2", sinif="kas", maxw=5400)}
  {foto(7750, 140, 1600, 480, "salon", 40, golge=False)}
  {foto(9500, 140, 1600, 480, "pergola", 40, golge=False)}
  {etiket}
  {mb.mia(15450, 110, 420, False)}
  {damga(17200, 370, 380, "SON", "DAİRELER", "KAÇIRMAYIN!", zemin=tur, yazi="#fff")}"""
    return pano(r, zemin, "", icerik, tas, ic)


# ================================================================ 4 — beyaz, asılı fiyat etiketi
def D4():
    lac, mercan = "#1d3b5a", "#e8694a"
    r = dict(v4.SERIT_ACIK, serit=lac, serit_su=mercan)
    zemin = "#ffffff"
    tas, ic = kart_bina(10900, "#ffffff", 22, golge="0 30px 70px rgba(29,59,90,.25)")
    dalga = ('<svg class="a" style="left:0;top:0" width="7600" height="850" fill="none" stroke="#e9dfd0" stroke-width="3">'
             + "".join(f'<path d="M-200 {120 + i * 95} C 1800 {-200 + i * 95}, 3200 {900 + i * 60}, 5200 {200 + i * 95} S 7800 {700 + i * 40}, 8200 {300 + i * 95}"/>'
                       for i in range(9)) + '</svg>')
    nokta = lambda x, yy: ('<div class="a" style="left:%dpx;top:%dpx;display:flex;gap:34px">' % (x, yy)
                           + ''.join(f'<div style="width:46px;height:46px;border-radius:50%;border:7px solid {mercan}"></div>' for _ in range(4)) + '</div>')
    etiket = (f'<div class="a" style="left:7050px;top:-120px;width:820px;height:980px;transform:rotate(-14deg);transform-origin:50% 0;'
              f'filter:drop-shadow(0 24px 40px rgba(0,0,0,.25))">'
              f'<div class="a" style="left:400px;top:0;width:18px;height:220px;background:#d9c7a8;border-radius:9px;transform:translateX(-50%)"></div>'
              f'<div class="a" style="left:0;top:160px;width:820px;height:820px;background:{mercan};'
              f'clip-path:polygon(50% 0,100% 22%,100% 100%,0 100%,0 22%);display:flex;flex-direction:column;align-items:center;justify-content:center;color:#fff;text-align:center;padding-top:140px">'
              f'<div style="position:absolute;top:140px;left:50%;width:70px;height:70px;border-radius:50%;background:#fff;transform:translateX(-50%);box-shadow:inset 0 0 0 12px #c9d6e0"></div>'
              f'<div class="tek" style="font-size:54px;font-weight:600;letter-spacing:.14em">1+1 AYLIK</div>'
              f'<div class="tek" style="font-size:190px;font-weight:800;letter-spacing:-.03em;margin:8px 0 18px">39.900<span style="font-size:.45em">₺</span></div>'
              f'<div class="tek" style="font-size:52px;font-weight:700;letter-spacing:.08em;opacity:.95">2+1 AYLIK 49.900₺</div>'
              f'</div></div>')
    icerik = f"""
  {mb.tilda(300, 290, 240, False)}
  {nokta(6250, 70)}
  {y(1800, 45, "YENİ YAŞAM", 340, 700, lac, sinif="yol", maxw=4300)}
  {y(1800, 395, "BURADA BAŞLIYOR", 340, 700, lac, sinif="yol", maxw=4300)}
  {etiket}
  {pill(9250, 575, "60 AY SABİT TAKSİT &nbsp;·&nbsp; " + YOKLAR, "#c8482f", "#fff", 54, 130, "letter-spacing:.06em;box-shadow:0 20px 40px rgba(0,0,0,.25)")}
  {foto(13000, 60, 1500, 640, "mutfak")}
  {foto(14650, 60, 1500, 640, "balkon")}
  {mb.mia(16500, 170, 380, False)}
  {nokta(17150, 640)}"""
    return pano(r, zemin, dalga, icerik, tas, ic)


# ================================================================ 5 — turuncu eğik panel, mutlu aile
def D5():
    lac = "#14225a"
    r = dict(v4.SERIT_ACIK, serit=lac, serit_su="#ff9b4a")
    zemin = "linear-gradient(90deg,#e6ecf3 0%,#f3f6f9 50%,#e9eef4 100%)"
    tas, ic, _ = v9.bina(11500)
    panel = ('<div class="a" style="left:0;top:0;width:7700px;height:850px;clip-path:polygon(0 0,100% 0,86% 100%,0 100%);'
             'background:radial-gradient(circle at 20% 80%,rgba(255,255,255,.18) 0,rgba(255,255,255,0) 35%),'
             'linear-gradient(135deg,#ff9a3c 0%,#f5701d 60%,#e85d10 100%)"></div>'
             '<div class="a" style="left:0;top:0;width:7700px;height:850px;clip-path:polygon(0 0,100% 0,86% 100%,0 100%);'
             'background-image:radial-gradient(rgba(255,255,255,.22) 7px,transparent 8px);background-size:60px 60px;opacity:.5;'
             'mask-image:linear-gradient(90deg,transparent 55%,#000 100%);-webkit-mask-image:linear-gradient(90deg,transparent 55%,#000 100%)"></div>')
    ah = 900
    aile = (f'<img class="a" src="{AILE}" style="left:6450px;top:{850 + 60 - ah}px;height:{ah}px;width:{round(ah * AILE_ORAN)}px;'
            f'filter:drop-shadow(0 30px 40px rgba(0,0,0,.3))">')
    mia_pill = (f'<div class="a" style="left:13700px;top:80px;width:1900px;height:300px;border-radius:150px;background:#fff;'
                f'box-shadow:0 20px 50px rgba(0,0,0,.18)"></div>{mb.mia(14480, 120, 220, False)}')
    icerik = f"""
  {mb.tilda(300, 70, 230, True)}
  {y(1600, 60, "HAYALİNİZDEKİ EVE", 230, 800, "#fff", maxw=4700)}
  {y(1600, 300, "BUGÜN ADIM ATIN.", 230, 800, "#fff", maxw=4700)}
  {y(1610, 505, "60 ay sabit taksit · faiz yok · banka yok · kredi yok · ara ödeme yok", 54, 600, "#fff3e8", maxw=4600)}
  {pill(300, 580, "<span>1+1 AYLIK <b>39.900₺</b> &nbsp;·&nbsp; 2+1 AYLIK <b>49.900₺</b></span>", "#fff", lac, 54, 130)}
  {foto(8050, 60, 1400, 300, "park", 36)}
  {foto(8050, 400, 1400, 300, "yatak", 36)}
  {mia_pill}
  {foto(15800, 60, 1300, 640, "deniz")}
  {damga(17450, 370, 380, "SON", "DAİRELER", "KAÇIRMAYIN!", zemin="#f5701d", yazi="#fff")}"""
    return pano(r, zemin, panel, icerik, tas, ic + aile)


TASARIMLAR = [(D1, "hos-geldiniz"), (D2, "yasam-basliyor-simetrik"), (D3, "hayalinizdeki-ev"),
              (D4, "yeni-yasam-etiket"), (D5, "mutlu-aile")]


def main():
    sec = None
    if "--sadece" in sys.argv:
        sec = {int(v) for v in sys.argv[sys.argv.index("--sadece") + 1].split(",")}
    gecici = tempfile.mkdtemp(prefix="mega10-")
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
