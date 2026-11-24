#!/usr/bin/env python3
"""
Profesyonel reklam seti, 1. bölüm — tasarım spec v3'teki A1, A2, A3 yerleşimleri (2x çizilir).

  mia-pro-1-kiradan-kurtulun     A1 · lila · dört kişilik aile, bina zemin sahnesi, pembe karo, iletişim hapı
  mia-pro-2-anahtari-hazir       A2 · taze yeşil · anahtarlı aile, sağa taşan render kartı, beyaz karo
  mia-pro-3-60-ay-sabit-taksit   A3 · kırmızı · anahtarlı aile, arkada dev "60", sarı karo

Her biri 4x5 (1080x1350, akış) ve 9x16 (1080x1920, story; içerik y 250–1580) olarak ayrı dizilir.
Izgara: kenar 72 px, tek sol hat. Tipografi: Montserrat 500/800 (+ A1 girişinde Fraunces,
A3 dev rakamında Barlow Condensed). Gölge yalnız fotoğraf kartında; kontur, glow, altın yok.

    python3.13 scripts/build-reklam-pro-1.py
"""

import importlib.util
import json
import os
import subprocess
import sys
import tempfile

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_s = importlib.util.spec_from_file_location("cesit", os.path.join(ROOT, "scripts", "build-reklam-cesit.py"))
c = importlib.util.module_from_spec(_s)
_s.loader.exec_module(c)
logo, wa, SRC, FOTO = c.logo, c.wa, c.SRC, c.FOTO

OUT = os.path.join(ROOT, "sosyal-medya", "reklam-pro")
FONTS = os.path.join(ROOT, "brand-source", "fonts")
GRAFIK = os.path.join(ROOT, "scripts", "reklam-grafik")
W, K = 1080, 72                      # tuval genişliği, kenar boşluğu
AILE4 = SRC("aile/aile-kesik.png")   # 2243x1695 · dört kişi, kollar havada
AILE3 = SRC("aile/aile2-kesik.png")  # 1654x1694 · anahtarlı baba, anne, kız
ORAN4, ORAN3 = 2243 / 1695, 1654 / 1694
GIRIS = FOTO("20-giris-gunesli.jpg")  # 1536x2752 · güneşli giriş takı + bloklar
KESIK = SRC("entrance-gate-genis-kesik.png")  # 3168x1344 · gökyüzü saydam


def css(h):
    return f"""
@font-face {{ font-family: Mont; src: url("file://{FONTS}/Montserrat-var.ttf"); font-weight: 100 900; }}
@font-face {{ font-family: Manr; src: url("file://{FONTS}/Manrope-400.ttf"); font-weight: 400; }}
@font-face {{ font-family: Manr; src: url("file://{FONTS}/Manrope-600.ttf"); font-weight: 600; }}
@font-face {{ font-family: Manr; src: url("file://{FONTS}/Manrope-700.ttf"); font-weight: 700; }}
@font-face {{ font-family: Barlow; src: url("file://{FONTS}/BarlowCond-700.ttf"); font-weight: 700; }}
@font-face {{ font-family: Fr; src: url("file://{FONTS}/Fraunces-600.ttf"); font-weight: 600; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:{W}px; height:{h}px; overflow:hidden; position:relative; font-family:Mont,sans-serif;
       -webkit-font-smoothing:antialiased; text-rendering:geometricPrecision; }}
.a {{ position:absolute; }}
.tek {{ white-space:nowrap; }}
.sat {{ display:flex; align-items:center; }}
.rakam {{ font-variant-numeric:tabular-nums; font-feature-settings:"tnum" 1; }}
"""


def grafik(ad, stil):
    """Vektör aksan setinden bir SVG'yi satır içi verir (currentColor çalışsın diye)."""
    s = open(os.path.join(GRAFIK, ad + ".svg"), encoding="utf-8").read()
    return s.replace("<svg ", f'<svg class="a" style="{stil}" ', 1)


def vurgu(kelime, renk, cizgi=True):
    """Başlığın tek vurgu kelimesi; altında elle çizilmiş çizgi."""
    alt = grafik("alt-cizgi", "left:-3%;width:106%;top:86%;color:inherit") if cizgi else ""
    return f'<span style="position:relative;display:inline-block;color:{renk}">{kelime}{alt}</span>'


def logolar(y, renk, etiket, buyuk=False):
    """MİA PARK OCEAN sol üst, Tilda İnşaat (+ MÜTEAHHİT etiketi) sağ üst; ikisi tek renk."""
    mh, th, es = (84, 34, 13) if buyuk else (72, 30, 12)
    return (f'<div class="a" style="left:{K}px;top:{y}px">{logo("mia", mh, renk)}</div>'
            f'<div class="a" style="right:{K}px;top:{y}px;height:{mh}px;display:flex;flex-direction:column;align-items:flex-end;justify-content:center">'
            f'<div class="tek" style="font-size:{es}px;font-weight:700;letter-spacing:.3em;margin-right:-.3em;color:{etiket}">MÜTEAHHİT</div>'
            f'<div style="margin-top:9px">{logo("tilda", th, renk)}</div></div>')


def baslik(y, giris, ana, renk, gs, bs, giris_font="Mont", giris_agirlik=500, x=K, ara=6, z=4):
    """İnce giriş satırı + kalın ana satır(lar), cümle düzeni, tek sol hat."""
    return (f'<div class="a" style="left:{x}px;top:{y}px;color:{renk};z-index:{z}">'
            f'<div class="tek" style="font-family:{giris_font};font-weight:{giris_agirlik};font-size:{gs}px;line-height:1.1;letter-spacing:-.01em">{giris}</div>'
            f'<div class="tek" style="margin-top:{ara}px;font-weight:800;font-size:{bs}px;line-height:.95;letter-spacing:-.025em">{ana}</div></div>')


def sessiz(x, y, renk, boyut=28, metin="Banka yok · Faiz yok · Kefil yok", z=4):
    return (f'<div class="a tek" style="left:{x}px;top:{y}px;font-family:Manr;font-weight:600;font-size:{boyut}px;line-height:1.3;'
            f'color:{renk};z-index:{z}">{metin}</div>')


def karo(x, y, w, zemin, yazi, ikincil="60 ay sabit taksit", buyuk=False, rakam_renk=None, z=5, ikincil_boyut=None):
    """Dik, düz fiyat karosu: etiket → 699.000 → açıklama → ince çizgi → ikincil teklif."""
    e, r, a, i = (24, 120, 30, 44) if buyuk else (22, 104, 26, 38)
    py, px = (32, 40) if buyuk else (28, 36)
    i = ikincil_boyut or i
    return (f'<div class="a" style="left:{x}px;top:{y}px;width:{w}px;background:{zemin};color:{yazi};border-radius:20px;padding:{py}px {px}px {py - 2}px;z-index:{z}">'
            f'<div class="tek" style="font-size:{e}px;font-weight:700;letter-spacing:.14em;line-height:1">PEŞİNAT</div>'
            f'<div class="tek rakam" style="margin-top:{round(r * .1)}px;margin-left:-{round(r * .04)}px;font-size:{r}px;font-weight:800;letter-spacing:-.03em;line-height:.8;color:{rakam_renk or yazi}">699.000</div>'
            f'<div class="tek" style="margin-top:{round(r * .16)}px;font-size:{a}px;font-weight:600;line-height:1">TL\'den başlayan peşinat</div>'
            f'<div style="margin:{round(a * .7)}px 0 {round(a * .62)}px;height:2px;background:{yazi};opacity:.2"></div>'
            f'<div class="tek" style="font-size:{i}px;font-weight:700;letter-spacing:-.01em;line-height:1">{ikincil}</div></div>')


def iletisim(renk, boy=52, wa_renk="#25D366"):
    """Tek satır iletişim: solda 444 10 58, sağda WhatsApp ikonu + numara (aynı boy, aynı ağırlık)."""
    tel = f"font-size:{boy}px;font-weight:800;letter-spacing:-.01em;line-height:1;color:{renk}"
    return (f'<span class="tek rakam" style="{tel}">444 10 58</span>'
            f'<span class="sat" style="gap:{round(boy * .3)}px">{wa(round(boy * .92), wa_renk)}'
            f'<span class="tek rakam" style="{tel}">0540 028 00 41</span></span>')


def serit(h, zemin, renk, ust, buyuk=False):
    """Alt iletişim şeridi: tek satır. Story'de şerit aşağı doğru yalnız zemin olarak uzar."""
    return (f'<div class="a" style="left:0;top:{ust}px;width:{W}px;height:{h - ust}px;background:{zemin};z-index:6">'
            f'<div class="a sat" style="left:{K}px;right:{K}px;top:0;height:132px;justify-content:space-between">{iletisim(renk, 56 if buyuk else 52)}</div></div>')


def hap(y, zemin, renk, yuk=96, buyuk=False):
    """Fotoğraf üstü iletişim hapı, x 72–1008."""
    return (f'<div class="a sat" style="left:{K}px;top:{y}px;width:{W - 2 * K}px;height:{yuk}px;border-radius:999px;background:{zemin};'
            f'justify-content:space-between;padding:0 {48 if buyuk else 44}px;z-index:7">{iletisim(renk, 50 if buyuk else 46)}</div>')


def kisi(src, oran, yuk, sol, alt_y, z=3, ek=""):
    """Kişi kesimi: alt kenarı alt_y'ye (şerit üstü / tuval altı) oturur."""
    return f'<img class="a" src="{src}" style="left:{sol}px;top:{alt_y - yuk}px;height:{yuk}px;width:{round(yuk * oran)}px;z-index:{z};{ek}">'


# ------------------------------------------------------ A1 · lila · zemin sahnesi

def a1(h):
    MOR, KOYU, PEMBE, ACIK = "#5B2BC4", "#2A1466", "#FF5CA8", "#EFE7FF"

    def sahne(ust, foto_y, erime, yikama):
        """Güneşli giriş fotoğrafı tam genişlik; üstü mora erir, gökyüzü mor tona çekilir."""
        m = f"linear-gradient(180deg,transparent 0,rgba(0,0,0,.5) {round(erime * .45)}px,#000 {erime}px)"
        return (f'<div class="a" style="left:0;top:{ust}px;width:{W}px;height:{h - ust}px;overflow:hidden;isolation:isolate;'
                f'-webkit-mask-image:{m};mask-image:{m}">'
                f'<img class="a" src="{GIRIS}" style="left:0;top:{foto_y - ust}px;width:{W}px">'
                f'<div class="a" style="left:0;top:0;width:{W}px;height:{yikama}px;background:linear-gradient(180deg,{MOR} 0,{MOR} 35%,rgba(91,43,196,0) 100%);mix-blend-mode:color"></div>'
                f'<div class="a" style="left:0;top:0;width:{W}px;height:{yikama}px;background:linear-gradient(180deg,#C4ADFF 0,#C4ADFF 45%,rgba(196,173,255,0) 100%);mix-blend-mode:multiply"></div>'
                f'<div class="a" style="inset:0;background:{MOR};mix-blend-mode:soft-light;opacity:.2"></div></div>')

    ana = 'ev sahibi ' + vurgu('olun', PEMBE)
    if h < 1500:
        return f"""<body style="background:{MOR}">
  {sahne(380, 232, 230, 560)}
  {logolar(K, '#fff', ACIK)}
  {baslik(176, 'Kiradan kurtulun,', ana, '#fff', 48, 104, 'Fr', 600, ara=4)}
  {sessiz(K, 352, ACIK)}
  {karo(K, 416, 536, PEMBE, KOYU)}
  {kisi(AILE4, ORAN4, 680, 158, 716 + 680)}
  {hap(1182, KOYU, '#fff')}
</body>"""
    # story: aynı sahne daha uzun; aile altta mora erir, hap güvenli alanın alt sınırında
    return f"""<body style="background:{MOR}">
  {sahne(540, 300, 300, 760)}
  {logolar(250, '#fff', ACIK, True)}
  {baslik(364, 'Kiradan kurtulun,', ana, '#fff', 56, 120, 'Fr', 600, ara=6)}
  {sessiz(K, 572, ACIK, 30)}
  {karo(K, 642, 600, PEMBE, KOYU, buyuk=True)}
  {kisi(AILE4, ORAN4, 790, 17, 990 + 790)}
  <div class="a" style="left:0;top:1440px;width:{W}px;height:{h - 1440}px;z-index:4;background:linear-gradient(180deg,rgba(91,43,196,0) 0,{MOR} 284px)"></div>
  {hap(1476, KOYU, '#fff', 104, True)}
</body>"""


# ------------------------------------------------------ A2 · taze yeşil · taşan kart

def a2(h):
    YESIL, KOYU, SARI, ACIK = "#2FBF71", "#0E5A3A", "#FFD84D", "#E6F8EE"
    golge = "box-shadow:0 16px 40px rgba(14,90,58,.14)"

    def kart(sol, ust, alt, r, foto_sol, foto_ust, foto_en):
        """Sağ kenardan taşan, şeride oturan render kartı (yalnız sol üst köşe yuvarlak)."""
        return (f'<div class="a" style="left:{sol}px;top:{ust}px;width:{W - sol}px;height:{alt - ust}px;border-radius:{r}px 0 0 0;overflow:hidden;{golge};z-index:1">'
                f'<img class="a" src="{GIRIS}" style="left:{foto_sol}px;top:{foto_ust}px;width:{foto_en}px"></div>')

    ana = 'anahtarı ' + vurgu('hazır', SARI)
    if h < 1500:
        ust = h - 132
        return f"""<body style="background:{YESIL}">
  {grafik('nokta-deseni', 'left:-14px;top:500px;width:240px;color:#fff;opacity:.26')}
  {kart(500, 500, ust, 28, -150, -250, 800)}
  {logolar(K, '#fff', ACIK)}
  {baslik(176, 'Yeni evinizin', ana, '#fff', 46, 104)}
  {sessiz(K, 350, ACIK)}
  {kisi(AILE3, ORAN3, 652, -24, ust)}
  {karo(472, 396, 536, '#fff', KOYU)}
  {serit(h, KOYU, '#fff', ust)}
</body>"""
    # story: aile büyür, karo güvenli alanın hemen üstünde kartın alt köşesine iner
    ust = 1448
    return f"""<body style="background:{YESIL}">
  {grafik('nokta-deseni', 'left:-14px;top:700px;width:280px;color:#fff;opacity:.26')}
  {kart(340, 720, ust, 32, 0, -324, 740)}
  {logolar(250, '#fff', ACIK, True)}
  {baslik(364, 'Yeni evinizin', ana, '#fff', 52, 120)}
  {sessiz(K, 572, ACIK, 30)}
  {kisi(AILE3, ORAN3, 800, -10, ust)}
  {karo(408, 1096, 600, '#fff', KOYU, buyuk=True)}
  {serit(h, KOYU, '#fff', ust, True)}
</body>"""


# ------------------------------------------------------ A3 · kırmızı · dev rakam

def a3(h):
    KIRMIZI, KOYU, SARI, ACIK, TON = "#E0263C", "#8E0F22", "#FFD23F", "#FFF1E6", "#C81E33"

    def dev(boyut, sag, rakam_ust):
        """Zemin tonunda dev "60" (Barlow Condensed); rakam_ust = rakamın görünen üst kenarı."""
        return (f'<div class="a tek" style="right:{sag}px;top:{round(rakam_ust - boyut * .09)}px;font-family:Barlow;font-weight:700;font-size:{boyut}px;line-height:.8;'
                f'letter-spacing:-.02em;color:{TON};z-index:1">60</div>')

    def bina(sol, ust, en):
        """Proje render'ı (gökyüzü saydam) kırmızı tek ton baskı gibi: rakamın önünde, ailenin arkasında."""
        m = "linear-gradient(90deg,transparent 38%,#000 50%)"
        return (f'<img class="a" src="{KESIK}" style="left:{sol}px;top:{ust}px;width:{en}px;filter:grayscale(1) contrast(1.25) brightness(1.05);'
                f'mix-blend-mode:multiply;opacity:.5;z-index:2;-webkit-mask-image:{m};mask-image:{m}">')

    ana = '60 ay ' + vurgu('sabit', SARI) + ' taksit'
    ikincil = 'Kefil yok · ara ödeme yok'
    if h < 1500:
        ust = h - 132
        return f"""<body style="background:{KIRMIZI}">
  {dev(800, 36, 372)}
  {bina(-325, 603, 1500)}
  {logolar(K, '#fff', ACIK)}
  {baslik(176, 'Banka yok, faiz yok;', ana, '#fff', 46, 104, ara=8)}
  {kisi(AILE3, ORAN3, 700, -14, ust)}
  {karo(472, 912, 536, SARI, KOYU, ikincil, ikincil_boyut=34)}
  {serit(h, KOYU, '#fff', ust)}
</body>"""
    ust = 1448
    return f"""<body style="background:{KIRMIZI}">
  {dev(780, 36, 572)}
  {bina(-330, 756, 1650)}
  {logolar(250, '#fff', ACIK, True)}
  {baslik(364, 'Banka yok, faiz yok;', ana, '#fff', 52, 106, ara=8)}
  {kisi(AILE3, ORAN3, 790, -30, ust)}
  {karo(408, 1096, 600, SARI, KOYU, ikincil, buyuk=True, ikincil_boyut=38)}
  {serit(h, KOYU, '#fff', ust, True)}
</body>"""


TASARIMLAR = [("mia-pro-1-kiradan-kurtulun", a1), ("mia-pro-2-anahtari-hazir", a2), ("mia-pro-3-60-ay-sabit-taksit", a3)]
BICIMLER = [("4x5", 1350), ("9x16", 1920)]


def main():
    os.makedirs(OUT, exist_ok=True)
    gecici = tempfile.mkdtemp(prefix="pro1-")
    secim = sys.argv[1:]
    isler = []
    for ad, fn in TASARIMLAR:
        for oran, h in BICIMLER:
            tam = f"{ad}-{oran}"
            if secim and not any(k in tam for k in secim):
                continue
            hp = os.path.join(gecici, tam + ".html")
            open(hp, "w", encoding="utf-8").write(
                f'<!doctype html><html lang="tr"><head><meta charset="utf-8"><style>{css(h)}</style></head>{fn(h)}</html>')
            isler.append(dict(html=hp, w=W, h=h, dsf=2, dilim=W, cikti=os.path.join(gecici, tam), ad=tam))
    jp = os.path.join(gecici, "isler.json")
    json.dump(isler, open(jp, "w"))
    npm = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    subprocess.run(["node", os.path.join(ROOT, "scripts", "mega-bilbord", "render.cjs"), jp], check=True,
                   env={**os.environ, "NODE_PATH": npm}, stdout=subprocess.DEVNULL)
    for is_ in isler:
        im = Image.open(json.load(open(is_["cikti"] + ".json"))[0]).convert("RGB")
        yol = os.path.join(OUT, is_["ad"] + ".jpg")
        im.save(yol, quality=92)
        print("  →", os.path.relpath(yol, ROOT), im.size)


if __name__ == "__main__":
    main()
