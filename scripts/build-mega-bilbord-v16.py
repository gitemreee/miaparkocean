#!/usr/bin/env python3
"""
180 m dev pano — 16. tur: müşterinin maket kurgusu (15.jpg) ile baştan.

Kurgu (soldan sağa, beyaz zemin):
  Tilda logosu · [boşluk: slogan] · dikey fotoğraf paneli (avlu) · [boşluk: finans] · ana görsel (gündüz
  render, ortada, panodan taşar) · [boşluk: aile + rozetler] · fotoğraf paneli (avlu/teras) · [boşluk: MİA
  logosu + yuvarlak detaylar] · Tilda logosu

Fotoğraf panelleri maketteki gibi tam yükseklik, keskin kenarlı. Alt şerit korunur (iletişim).

    python3.13 scripts/build-mega-bilbord-v16.py [--pdf]
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


v15 = _yukle("mb_v15", "build-mega-bilbord-v15.py")
v14, v11, v7, v6, v4, v2, mb = v15.v14, v15.v11, v15.v7, v15.v6, v15.v4, v15.v2, v15.mb
OUT = os.path.join(ROOT, "tabela", "mega-bilbord-180m-tur16")
TW, EXT = mb.TW, mb.EXT
y, kutu, damga, pill, pano = v4.y, v4.kutu, v4.damga, v11.pill, v11.pano
aile, AILE1, onay_liste, F = v14.aile, v14.AILE1, v11.onay_liste, v14.F
serit_buyut, KIR = v15.serit_buyut, v15.KIR
v15.TEL2 = "444 1 058"          # şeritte de aynı yazım

YESIL, ACIK = "#14225a", "#1f6fb2"
F["avlu3"] = "file://" + os.path.join(ROOT, "signage-source", "avlu-havuz-ustten.jpg")
yumusak = v14.yumusak


def telefon(x, top, renk, fs=72, hizala="left"):
    simge = v2.IK_TEL.replace("<svg", f'<svg style="width:{round(fs * 1.1)}px;height:{round(fs * 1.1)}px;flex:none"', 1)
    return (f'<div class="a tek" style="left:{x}px;top:{top}px;display:flex;align-items:center;gap:22px;color:{renk};'
            f'font-size:{fs}px;font-weight:800;letter-spacing:.02em{";transform:translateX(-50%)" if hizala == "center" else ""}">{simge}444 1 058</div>')


def bina_olcekli(cx, s):
    """v4.bina ile aynı kahraman, s ölçeğinde (taşma üst kenara sığacak şekilde)."""
    HW, HH = round(v4.HW * s), round(v4.HH * s)
    hx, hy = round(cx - HW / 2), max(0, min(EXT - round(mb.UST_FR * HH), 1350 - HH))
    src = f"file://{mb.HERO}"
    dur = []
    for a, b in mb.SUTUNLAR:
        dur += [f"transparent {a * 100:.2f}%", f"#000 {a * 100:.2f}%", f"#000 {b * 100:.2f}%", f"transparent {b * 100:.2f}%"]
    maske = "linear-gradient(90deg," + ",".join(dur) + ")"
    tas = f'<img class="a" src="{src}" style="left:{hx}px;top:{hy}px;width:{HW}px;height:{HH}px;-webkit-mask-image:{maske}">'
    ic = f'<img class="a" src="{src}" style="left:{hx}px;top:{hy - EXT}px;width:{HW}px;height:{HH}px">'
    return tas, ic


def panel_foto(x, w, ad, pos="50% 50%"):
    """Maketteki gibi tam yükseklik, keskin kenarlı fotoğraf paneli."""
    return (f'<div class="a" style="left:{x}px;top:0;width:{w}px;height:718px;background:url({F[ad]}) {pos}/cover no-repeat;'
            f'box-shadow:0 0 60px rgba(0,0,0,.18)"></div>')


FIYATLAR = (("1+0", "29.900"), ("1+1", "39.900"))   # 1+0 tutarı [DOĞRULANACAK]


def fiyat_cift(x, top, renk, et, fs=136, cizgi="rgba(20,34,90,.25)"):
    """1+0 ve 1+1 yan yana."""
    kol = [f'<div style="padding:0 46px">{v4.satir(t + " · AYLIK", round(fs * .36), 800, et, "letter-spacing:.14em")}'
           f'{v4.satir(v + "<span style=font-size:.45em>₺</span>", fs, 800, renk, "letter-spacing:-.03em;margin-top:4px")}</div>'
           for t, v in FIYATLAR]
    return (f'<div class="a" style="left:{x}px;top:{top}px;display:flex;align-items:center;transform:translateX(-50%)">'
            f'{kol[0]}<div style="width:4px;align-self:stretch;background:{cizgi}"></div>{kol[1]}</div>')


def fiyat_dikey(x, top, renk, et, fs=130):
    """1+0 ve 1+1 alt alta (sağ blok)."""
    s_ = ""
    for i, (t, v) in enumerate(FIYATLAR):
        yy = top + i * round(fs * 1.75)
        s_ += (v4.y(x, yy, t + " · AYLIK", round(fs * .34), 800, et, sinif="kas")
               + v4.y(x, yy + round(fs * .5), v + "<span style=font-size:.45em>₺</span>", fs, 800, renk, ls="-.03em"))
    return s_


def site(x, top, renk, fs=48):
    return v4.y(x, top, "miaparkocean.com", fs, 700, renk, ek="transform:translateX(-50%);letter-spacing:.04em")


def finans(cx, top=70, fs=136, mia=False):
    """Ortalanmış finans bloğu: (MİA logosu) · 60 ay rozeti · 1+0 / 1+1 · onay listesi."""
    s_ = ""
    if mia:
        s_ += mb.mia(cx - 160, top, 220, False)
        top += 260
    s_ += pill(cx, top, "60 AY SABİT TAKSİT", ACIK, "#fff", 54, 106, "letter-spacing:.08em;transform:translateX(-50%)")
    s_ += fiyat_cift(cx, top + 140, YESIL, ACIK, fs)
    s_ += onay_liste(cx - 1120, top + 140 + round(fs * 1.55), YESIL, ACIK, "#fff", 42, 100, 1180)
    return s_


def M():
    zemin = ("repeating-linear-gradient(135deg,rgba(20,34,90,.05) 0 2px,transparent 2px 30px),"
             "repeating-linear-gradient(45deg,rgba(20,34,90,.05) 0 2px,transparent 2px 30px),"
             "linear-gradient(90deg,#eef3f8 0%,#f7f9fc 50%,#e9eff5 100%)")
    tas, ic = bina_olcekli(8750, 0.85)
    rozet = lambda yy, t, bg, ek="": pill(11950, yy, t, bg, "#fff", 46, 112, "transform:translateX(-50%);letter-spacing:.06em" + ek)
    icerik = f"""
  {mb.tilda(230, 200, 290, False)}
  {telefon(960, 540, YESIL, 72, "center")}
  {site(960, 640, ACIK)}
  {y(2520, 190, "KİRAYA DEĞİL,", 125, 800, ACIK, ek="transform:translateX(-50%)")}
  {y(2520, 330, "KENDİ EVİNİZE", 125, 800, YESIL, ek="transform:translateX(-50%)")}
  {y(2520, 470, "ÖDEYİN.", 125, 800, YESIL, ek="transform:translateX(-50%)")}
  {yumusak(3350, 0, 1500, 850, "avlu2", "38% 60%", (.14, .14), (0, .08))}
  {finans(6000, 110, 136)}
  {aile(10400, 1000, AILE1, -20)}
  {rozet(120, "VADE FARKI YOK", "#111")}
  {pill(11940, 256, "BANKA YOK", KIR, "#fff", 46, 112, "transform:translateX(-100%);letter-spacing:.06em")}
  {pill(11960, 256, "KREDİ YOK", KIR, "#fff", 46, 112, "letter-spacing:.06em")}
  {rozet(392, "ARA ÖDEME YOK", "#111")}
  {rozet(528, "60 AY SABİT TAKSİT", KIR)}
  {yumusak(12450, 0, 2000, 850, "avlu3", "50% 50%", (.13, .13), (0, .08))}
  {finans(15450, 40, 118, mia=True)}
  {mb.tilda(16700, 120, 230, False)}
  {y(17230, 400, "TEK YETKİLİ SATIŞ", 34, 600, YESIL, sinif="kas", ek="transform:translateX(-50%)")}
  {kutu(16930, 445, 600, 130, mb.ocean(88, "#0f4c9b", "#2f7fd6"), "display:flex;justify-content:center")}
  {telefon(17230, 600, YESIL, 64, "center")}
  {telefon(17230, 680, YESIL, 46, "center").replace("444 1 058", "0540 028 00 41")}
  {site(17230, 750, ACIK, 44)}"""
    return f"""
<div class="tasma">{tas}</div>
<div class="pano" style="background:{zemin}">
  {ic}
  {icerik}
</div>"""


TASARIMLAR = [(M, "maket-kurgusu")]


def main():
    gecici = tempfile.mkdtemp(prefix="mega16-")
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
