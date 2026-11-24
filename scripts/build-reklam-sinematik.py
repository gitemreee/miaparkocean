#!/usr/bin/env python3
"""
Sinematik kreatifler — tam ekran fotoğraf, fotoğrafın içine yerleşen tipografi (2x çizilir).

Düz renk zemin ve çerçeveli fotoğraf yok: her tasarım tek bir gerçekçi görselin üzerine kurulur;
yazı gökyüzüne/ışığa oturur, cam (buzlu) bantlar ve ince çizgiler kullanılır, üstte film greni ve
kenar karartması vardır.

  1-her-yere-yakin   drone görüntüsü · siteden çıkan ışıklı rotalar ve mesafe etiketleri
  2-altmis-ay        gün batımı gökyüzü · binaların ARKASINDA duran dev "60"
  3-kiradan-kurtulun balkonda oturan aile fotoğrafı
  4-anahtari-hazir   bulanık gün batımı girişinin önünde anahtarlı aile
  5-sabit-taksit     gece girişi · ışıklı altın başlık, cam rakam bandı
  6-cok-kolay        akşam avlusu · dev altın "699.000 TL"

Her biri 4x5 (1080x1350) ve 9x16 (1080x1920) çıkar.

    python3.13 scripts/build-reklam-sinematik.py
"""

import importlib.util
import json
import os
import subprocess
import tempfile

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_s = importlib.util.spec_from_file_location("cesit", os.path.join(ROOT, "scripts", "build-reklam-cesit.py"))
c = importlib.util.module_from_spec(_s)
_s.loader.exec_module(c)
logo, wa, css, SRC, FOTO, W = c.logo, c.wa, c.css, c.SRC, c.FOTO, c.W
GERCEK = lambda ad: c.F("sosyal-medya", "gercekci-gorseller", ad)
OUT = os.path.join(ROOT, "sosyal-medya", "reklam-sinematik")

ALTIN = "linear-gradient(180deg,#fff1c2 0%,#f2cd72 45%,#d9a441 100%)"
GOLGE = "text-shadow:0 4px 26px rgba(0,0,0,.55),0 1px 3px rgba(0,0,0,.4)"

GREN = ('<svg class="a" style="left:0;top:0;width:100%;height:100%;opacity:.16;mix-blend-mode:overlay;pointer-events:none;z-index:8">'
        '<filter id="gr"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="7"/><feColorMatrix type="saturate" values="0"/></filter>'
        '<rect width="100%" height="100%" filter="url(#gr)"/></svg>'
        '<div class="a" style="left:0;top:0;width:100%;height:100%;background:radial-gradient(120% 90% at 50% 45%,transparent 55%,rgba(0,0,0,.42) 100%);pointer-events:none;z-index:8"></div>')

EK_CSS = """
.altin { background:%s; -webkit-background-clip:text; background-clip:text; color:transparent; text-shadow:none; filter:drop-shadow(0 4px 14px rgba(0,0,0,.5)); }
.cam { background:linear-gradient(180deg,rgba(255,255,255,.2),rgba(255,255,255,.07)); -webkit-backdrop-filter:blur(16px) saturate(1.2);
       backdrop-filter:blur(16px) saturate(1.2); border:1.5px solid rgba(255,255,255,.5); box-shadow:0 20px 50px rgba(0,0,0,.4), inset 0 1px 0 rgba(255,255,255,.4); }
.kucuk { font-size:15px; font-weight:700; letter-spacing:.34em; text-transform:uppercase; }
.z { z-index:5; }
body { display:block; color:#fff; background:#05101c; }
""" % ALTIN


def K(h):
    """Biçime göre değer seçici: K(h)(akış, story)."""
    return lambda a, b: a if h < 1500 else b


def ust(h, orta=False):
    """Üst logolar: MİA + müteahhit Tilda."""
    y = 54 if h < 1500 else 150
    if orta:
        return (f'<div class="a z sat" style="left:0;width:{W}px;top:{y}px;justify-content:center;gap:26px;filter:drop-shadow(0 3px 10px rgba(0,0,0,.5))">'
                f'{logo("mia", 92, "#fff")}<span style="width:1.5px;height:70px;background:rgba(255,255,255,.5)"></span>{logo("tilda", 38, "#fff")}</div>')
    return (f'<div class="a z sat" style="left:60px;right:60px;top:{y}px;justify-content:space-between;filter:drop-shadow(0 3px 10px rgba(0,0,0,.5))">'
            f'{logo("mia", 92, "#fff")}<div style="text-align:right"><div class="tek kucuk" style="font-size:12px;opacity:.85">Müteahhit</div>'
            f'<div style="margin-top:9px">{logo("tilda", 38, "#fff")}</div></div></div>')


def iletisim(h, cizgi=True):
    """Alt iletişim satırı: 444 10 58 · WhatsApp · site."""
    alt = 44 if h < 1500 else 190
    return (f'<div class="a z" style="left:60px;right:60px;bottom:{alt}px">'
            + ('<div style="height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.6),transparent)"></div>' if cizgi else '')
            + f'<div class="sat" style="margin-top:20px;justify-content:space-between">'
              f'<div class="tek" style="font-family:Jost;font-weight:700;font-size:66px;line-height:1;letter-spacing:.02em;{GOLGE}">444 10 58</div>'
              f'<div style="text-align:right"><div class="sat tek" style="gap:10px;justify-content:flex-end;font-size:28px;font-weight:700;{GOLGE}">{wa(30)}0540 028 00 41</div>'
              f'<div class="tek" style="margin-top:6px;font-size:19px;font-weight:600;letter-spacing:.16em;opacity:.85">MIAPARKOCEAN.COM</div></div></div></div>')


def zemin(src, pos, ek=""):
    return f'<img class="a" src="{src}" style="left:0;top:0;width:100%;height:100%;object-fit:cover;object-position:{pos};{ek}">'


def karart(ust_y, alt_y, renk="5,16,28"):
    """Üstte ve altta yumuşak karartma (px yükseklikleri)."""
    return (f'<div class="a" style="left:0;top:0;width:100%;height:{ust_y}px;background:linear-gradient(180deg,rgba({renk},.86),rgba({renk},.5) 55%,rgba({renk},0))"></div>'
            f'<div class="a" style="left:0;bottom:0;width:100%;height:{alt_y}px;background:linear-gradient(0deg,rgba({renk},.96) 30%,rgba({renk},.6) 62%,rgba({renk},0))"></div>')


# ------------------------------------------------------------ 1 · her yere yakın

def s1(h):
    k = K(h)
    sx, sy = 540, k(760, 1010)          # sitenin kadrajdaki merkezi
    noktalar = k([("1 dk", "D-100 Karayolu", 60, -330), ("5 dk", "Şehir Merkezi", 650, -380),
                  ("3 dk", "41 Burada AVM", 40, -170), ("5 dk", "Şehir Hastanesi", 690, -200)],
                 [("1 dk", "D-100 Karayolu", 60, -360), ("5 dk", "Şehir Merkezi", 660, -410),
                  ("3 dk", "41 Burada AVM", 40, -160), ("5 dk", "Şehir Hastanesi", 690, -200), ("5 dk", "TEM Otoyolu", 340, -490)])
    yollar, etiketler = "", ""
    for dk, yer, x, dy in noktalar:
        ex, ey = x + 150, sy + dy + 30
        cx, cy = (sx + ex) / 2 + (ex - sx) * .15, min(sy, ey) - 90
        yollar += (f'<path d="M{sx},{sy} Q{cx:.0f},{cy:.0f} {ex:.0f},{ey:.0f}" fill="none" stroke="#fff" stroke-width="3" stroke-dasharray="2 11" stroke-linecap="round"/>'
                   f'<circle cx="{ex:.0f}" cy="{ey:.0f}" r="7" fill="#ffd978"/>')
        etiketler += (f'<div class="a cam sat z" style="left:{x}px;top:{sy + dy - 30:.0f}px;gap:12px;border-radius:999px;padding:9px 22px 9px 9px">'
                      f'<span class="tek" style="background:#ffd978;color:#0a2233;border-radius:999px;padding:9px 15px;font-size:26px;font-weight:800;line-height:1">{dk}</span>'
                      f'<span class="tek" style="font-size:25px;font-weight:700;{GOLGE}">{yer}</span></div>')
    return f"""<body>
  {zemin(FOTO('17-drone-yalniz-site.jpg'), k('50% 42%', '50% 50%'), 'filter:saturate(1.08) contrast(1.04)')}
  {karart(k(470, 700), k(520, 800), '6,26,38')}
  <svg class="a" style="left:0;top:0;width:{W}px;height:{h}px;filter:drop-shadow(0 0 8px rgba(255,217,120,.9))" viewBox="0 0 {W} {h}">{yollar}
    <circle cx="{sx}" cy="{sy}" r="26" fill="none" stroke="#ffd978" stroke-width="3" opacity=".9"/><circle cx="{sx}" cy="{sy}" r="52" fill="none" stroke="#ffd978" stroke-width="2" opacity=".5"/>
    <circle cx="{sx}" cy="{sy}" r="11" fill="#ffd978"/></svg>
  {etiketler}
  {ust(h)}
  <div class="a z" style="left:60px;right:60px;top:{k(168, 300)}px">
    <div class="tek" style="font-family:Fr;font-weight:600;font-style:italic;font-size:{k(60, 68)}px;line-height:1;{GOLGE}">Yeni eviniz</div>
    <div class="tek" style="margin-top:6px;font-size:{k(104, 112)}px;font-weight:900;letter-spacing:-.03em;line-height:1;{GOLGE}">HER YERE <span class="altin">YAKIN</span></div>
  </div>
  <div class="a z" style="left:60px;right:60px;bottom:{k(176, 330)}px">
    <div class="tek kucuk" style="color:#ffd978">İzmit · MİA Bölgesi</div>
    <div class="tek" style="margin-top:10px;font-size:46px;font-weight:800;line-height:1.1;{GOLGE}"><span class="altin">699.000 TL</span>'den başlayan peşinat</div>
    <div class="tek" style="margin-top:6px;font-size:30px;font-weight:500;{GOLGE}">60 ay sabit taksit · banka yok · faiz yok</div>
  </div>
  {iletisim(h)}{GREN}
</body>"""


# ---------------------------------------------------------------- 2 · altmış ay

def s2(h):
    k = K(h)
    bina_h = k(700, 880)
    bina_w = round(bina_h * 3168 / 1344)
    bina_top = k(470, 760)
    return f"""<body style="background:#0a1626">
  <div class="a" style="left:0;top:0;width:{W}px;height:{bina_top + 420}px;overflow:hidden">
    <img src="{GERCEK('mia-2-giris-gunbatimi.jpg')}" style="position:absolute;left:-420px;top:-40px;width:1900px;filter:blur(1.5px) saturate(1.15)">
    <div class="a" style="left:0;top:0;width:100%;height:100%;background:linear-gradient(180deg,rgba(10,22,38,.55) 0%,rgba(10,22,38,0) 40%,rgba(10,22,38,0) 70%,#0a1626 100%)"></div>
  </div>
  <div class="a" style="left:-140px;top:{bina_top - 120}px;width:700px;height:700px;background:radial-gradient(closest-side,rgba(255,196,110,.75),rgba(255,160,80,.25) 55%,transparent)"></div>

  <div class="a tek" style="left:0;width:{W}px;top:{bina_top - k(235, 320)}px;text-align:center;font-family:Osw;font-weight:700;font-size:{k(680, 840)}px;line-height:.9;letter-spacing:-.02em;
       background:linear-gradient(180deg,#fff6d6 0%,#ffd978 40%,#e0a23c 100%);-webkit-background-clip:text;background-clip:text;color:transparent;
       filter:drop-shadow(0 12px 40px rgba(120,60,0,.55))">60</div>

  <img class="a" src="{SRC('entrance-gate-genis-kesik.png')}" style="left:{-(bina_w - W) * .58:.0f}px;top:{bina_top}px;width:{bina_w}px;height:{bina_h}px;filter:saturate(1.05) contrast(1.05) brightness(.96)">
  <div class="a" style="left:0;top:{bina_top}px;width:{W}px;height:{bina_h}px;background:linear-gradient(180deg,rgba(255,150,70,.16),rgba(10,22,38,0) 45%);mix-blend-mode:soft-light"></div>
  <div class="a" style="left:0;bottom:0;width:{W}px;height:{h - bina_top - bina_h + 300}px;background:linear-gradient(0deg,#0a1626 52%,rgba(10,22,38,.8) 76%,rgba(10,22,38,0))"></div>
  <div class="a" style="left:0;top:0;width:{W}px;height:{k(330, 520)}px;background:linear-gradient(180deg,rgba(10,22,38,.8),rgba(10,22,38,0))"></div>

  {ust(h)}
  <div class="a z" style="left:0;width:{W}px;top:{k(178, 320)}px;text-align:center">
    <div class="tek" style="font-family:Fr;font-weight:600;font-style:italic;font-size:{k(54, 64)}px;line-height:1;{GOLGE}">Banka yok, faiz yok;</div>
  </div>
  <div class="a z" style="left:0;width:{W}px;bottom:{k(196, 372)}px;text-align:center">
    <div class="tek" style="font-size:{k(96, 108)}px;font-weight:900;letter-spacing:-.02em;line-height:1;{GOLGE}">AY <span class="altin">SABİT TAKSİT</span></div>
    <div class="tek" style="margin-top:16px;font-size:34px;font-weight:600;{GOLGE}"><b style="font-weight:900">699.000 TL</b>'den başlayan peşinat · kefil yok · ara ödeme yok</div>
  </div>
  {iletisim(h)}{GREN}
</body>"""


# ---------------------------------------------------------- 3 · kiradan kurtulun

def s3(h):
    k = K(h)
    return f"""<body>
  {zemin(FOTO('19-balkon-cay-gunduz.jpg'), k('50% 62%', '50% 50%'), 'filter:saturate(1.06) contrast(1.03)')}
  {karart(k(560, 800), k(560, 820), '8,24,44')}
  {ust(h)}
  <div class="a z" style="left:60px;right:60px;top:{k(170, 310)}px">
    <div class="tek" style="font-family:Fr;font-weight:600;font-style:italic;font-size:{k(66, 76)}px;line-height:1;{GOLGE}">Kiradan kurtulun,</div>
    <div class="tek" style="margin-top:8px;font-size:{k(104, 114)}px;font-weight:900;letter-spacing:-.03em;line-height:1;{GOLGE}">KENDİ EVİNİZDE</div>
    <div class="tek" style="font-size:{k(104, 114)}px;font-weight:900;letter-spacing:-.03em;line-height:1.05"><span class="altin" style="filter:drop-shadow(0 4px 18px rgba(0,0,0,.5))">OTURUN</span></div>
  </div>
  <div class="a cam z sat" style="left:60px;right:60px;bottom:{k(182, 340)}px;border-radius:28px;padding:22px 34px;justify-content:space-between">
    <div><div class="tek kucuk" style="font-size:14px;color:#ffe08a">Peşinat</div>
      <div class="tek" style="margin-top:4px;font-family:Jost;font-weight:800;font-size:66px;line-height:1">699.000 <span style="font-size:36px">TL'den</span></div></div>
    <span style="width:1.5px;height:84px;background:rgba(255,255,255,.5)"></span>
    <div><div class="tek kucuk" style="font-size:14px;color:#ffe08a">Sabit taksit</div>
      <div class="tek" style="margin-top:4px;font-family:Jost;font-weight:800;font-size:66px;line-height:1">60 <span style="font-size:36px">AY</span></div></div>
    <span style="width:1.5px;height:84px;background:rgba(255,255,255,.5)"></span>
    <div><div class="tek kucuk" style="font-size:14px;color:#ffe08a">Faiz</div>
      <div class="tek" style="margin-top:4px;font-family:Jost;font-weight:800;font-size:66px;line-height:1">%0</div></div>
  </div>
  {iletisim(h, False)}{GREN}
</body>"""


# ------------------------------------------------------------ 4 · anahtarı hazır

def s4(h):
    k = K(h)
    return f"""<body>
  {zemin(GERCEK('mia-2-giris-gunbatimi.jpg'), k('30% 46%', '30% 50%'), 'filter:blur(7px) saturate(1.15) brightness(1.02);transform:scale(1.06)')}
  <div class="a" style="left:-260px;top:{k(120, 300)}px;width:900px;height:900px;background:radial-gradient(closest-side,rgba(255,214,150,.8),rgba(255,170,90,.28) 55%,transparent);mix-blend-mode:screen"></div>
  {karart(k(520, 760), k(620, 900), '30,16,10')}
  <img class="a" src="{c.AILE_ANAHTAR}" style="left:50%;bottom:{k(150, 300)}px;height:{k(880, 1130)}px;transform:translateX(-46%);
       filter:drop-shadow(0 30px 40px rgba(20,8,0,.55)) saturate(1.05) sepia(.12) brightness(1.02)">
  <div class="a" style="left:0;bottom:0;width:{W}px;height:{k(560, 820)}px;background:linear-gradient(0deg,rgba(24,12,8,.97) 34%,rgba(24,12,8,.7) 60%,rgba(24,12,8,0))"></div>
  {ust(h)}
  <div class="a z" style="left:0;width:{W}px;top:{k(166, 300)}px;text-align:center">
    <div class="tek" style="font-family:Fr;font-weight:600;font-style:italic;font-size:{k(62, 72)}px;line-height:1;{GOLGE}">Yeni evinizin</div>
    <div class="tek" style="margin-top:6px;font-size:{k(108, 116)}px;font-weight:900;letter-spacing:-.03em;line-height:1;{GOLGE}">ANAHTARI <span class="altin">HAZIR</span></div>
  </div>
  <div class="a z" style="left:0;width:{W}px;bottom:{k(178, 334)}px;text-align:center">
    <div class="tek" style="font-size:50px;font-weight:800;line-height:1.1;{GOLGE}"><span class="altin">699.000 TL</span>'den başlayan peşinat</div>
    <div class="tek" style="margin-top:8px;font-size:31px;font-weight:500;{GOLGE}">60 ay sabit taksit · banka yok · faiz yok · kefil yok</div>
  </div>
  {iletisim(h)}{GREN}
</body>"""


# -------------------------------------------------------------- 5 · sabit taksit

def s5(h):
    k = K(h)
    sutun = lambda ust_, alt_: (f'<div style="flex:1;text-align:center"><div class="tek" style="font-family:Jost;font-weight:800;font-size:64px;line-height:1">{ust_}</div>'
                                f'<div class="tek kucuk" style="margin-top:8px;font-size:15px;color:#ffe08a">{alt_}</div></div>')
    cizgi = '<span style="width:1.5px;height:84px;background:rgba(255,255,255,.45)"></span>'
    return f"""<body>
  {zemin(GERCEK('mia-7-gece-kapi.jpg'), k('50% 46%', '50% 50%'), 'filter:saturate(1.1) contrast(1.05)')}
  {karart(k(560, 780), k(500, 760), '6,10,30')}
  {ust(h, True)}
  <div class="a z" style="left:0;width:{W}px;top:{k(176, 312)}px;text-align:center">
    <div class="tek" style="font-family:Fr;font-weight:600;font-style:italic;font-size:{k(62, 72)}px;line-height:1.05;{GOLGE}">Taksitiniz sabit,</div>
    <div class="tek" style="margin-top:4px;font-size:{k(100, 110)}px;font-weight:900;letter-spacing:-.03em;line-height:1.02"><span class="altin" style="filter:drop-shadow(0 0 26px rgba(255,200,90,.55))">İÇİNİZ RAHAT</span></div>
    <div class="tek kucuk" style="margin-top:18px;font-size:17px;{GOLGE}">Banka yok &nbsp;·&nbsp; Faiz yok &nbsp;·&nbsp; Kefil yok &nbsp;·&nbsp; Ara ödeme yok</div>
  </div>
  <div class="a cam z sat" style="left:60px;right:60px;bottom:{k(182, 340)}px;border-radius:999px;padding:24px 20px">
    {sutun("699.000 TL", "'den başlayan peşinat")}{cizgi}{sutun('60 AY', 'sabit taksit')}{cizgi}{sutun('%0', 'faiz')}
  </div>
  {iletisim(h, False)}{GREN}
</body>"""


# ----------------------------------------------------------------- 6 · çok kolay

def s6(h):
    k = K(h)
    return f"""<body>
  {zemin(GERCEK('mia-4-giris-aksam.jpg'), k('50% 40%', '50% 50%'), 'filter:saturate(1.1) contrast(1.04)')}
  {karart(k(600, 860), k(620, 900), '8,16,40')}
  {ust(h)}
  <div class="a z" style="left:60px;right:60px;top:{k(170, 304)}px">
    <div class="tek" style="font-family:Fr;font-weight:600;font-style:italic;font-size:{k(62, 72)}px;line-height:1;{GOLGE}">Ev sahibi olmak</div>
    <div class="tek" style="margin-top:6px;font-size:{k(100, 98)}px;font-weight:900;letter-spacing:-.03em;line-height:1;{GOLGE}">ARTIK <span class="altin">ÇOK KOLAY</span></div>
  </div>
  <div class="a z" style="left:60px;right:60px;bottom:{k(170, 330)}px">
    <div class="tek kucuk" style="color:#ffe08a">Peşinat</div>
    <div class="tek" style="margin-top:2px;font-family:Jost;font-weight:800;font-size:{k(168, 164)}px;line-height:1;letter-spacing:-.02em"><span class="altin" style="filter:drop-shadow(0 8px 30px rgba(0,0,0,.55))">699.000</span><span style="font-size:.4em;font-weight:700;{GOLGE}"> TL'den</span></div>
    <div class="sat" style="margin-top:10px;gap:14px">
      <span class="tek cam" style="border-radius:999px;padding:10px 24px;font-size:28px;font-weight:800">60 AY SABİT TAKSİT</span>
      <span class="tek cam" style="border-radius:999px;padding:10px 24px;font-size:28px;font-weight:800">BANKA YOK</span>
      <span class="tek cam" style="border-radius:999px;padding:10px 24px;font-size:28px;font-weight:800">FAİZ YOK</span>
    </div>
  </div>
  {iletisim(h)}{GREN}
</body>"""


TASARIMLAR = [("1-her-yere-yakin", s1), ("2-altmis-ay", s2), ("3-kiradan-kurtulun", s3), ("4-anahtari-hazir", s4), ("5-sabit-taksit", s5), ("6-cok-kolay", s6)]
BICIMLER = [("4x5", 1350), ("9x16", 1920)]


def main():
    os.makedirs(OUT, exist_ok=True)
    gecici = tempfile.mkdtemp(prefix="sinematik-")
    isler = []
    for ad, fn in TASARIMLAR:
        for oran, h in BICIMLER:
            tam = f"{ad}-{oran}"
            hp = os.path.join(gecici, tam + ".html")
            open(hp, "w", encoding="utf-8").write(
                f'<!doctype html><html><head><meta charset="utf-8"><style>{css(h)}{EK_CSS}</style></head>{fn(h)}</html>')
            isler.append(dict(html=hp, w=W, h=h, dsf=2, dilim=W, cikti=os.path.join(gecici, tam), ad=tam))
    jp = os.path.join(gecici, "isler.json")
    json.dump(isler, open(jp, "w"))
    npm = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    subprocess.run(["node", os.path.join(ROOT, "scripts", "mega-bilbord", "render.cjs"), jp], check=True,
                   env={**os.environ, "NODE_PATH": npm}, stdout=subprocess.DEVNULL)
    for is_ in isler:
        im = Image.open(json.load(open(is_["cikti"] + ".json"))[0]).convert("RGB")
        yol = os.path.join(OUT, f"mia-{is_['ad']}.jpg")
        im.save(yol, quality=92)
        print("  →", os.path.relpath(yol, ROOT), im.size)


if __name__ == "__main__":
    main()
