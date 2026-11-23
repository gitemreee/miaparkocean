#!/usr/bin/env python3
"""
Çeşitlendirilmiş satış kreatifleri — altı farklı düzen, altı farklı renk dünyası (2x çizilir).

  1-ev-cercevesi   kum + koyu yeşil + turuncu · ev biçimli çerçeve, aile
  2-gece-altin     gece lacivert + altın · eğik başlık bantları, iki rakam kutusu
  3-anahtar        kırmızı · anahtarlı aile, yuvarlak proje görseli
  4-konum-pini     açık mavi + petrol + mercan · konum pini içinde proje, mesafe etiketleri
  5-yasam          zümrüt yeşili · eğik fotoğraf kartları, "bir evden fazlası"
  6-bes-neden      turkuaz + sarı · numaralı 5 neden listesi, aile

Her biri 4x5 (1080x1350, akış) ve 9x16 (1080x1920, story/reels) çıkar.
Logoların yeri ve rengi her tasarımda farklıdır. Metin: 699.000 TL'den başlayan peşinat,
60 ay sabit taksit; 444 10 58 · WhatsApp 0540 028 00 41.

    python3.13 scripts/build-reklam-cesit.py
"""

import json
import os
import re
import subprocess
import tempfile

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "sosyal-medya", "reklam-cesit")
FONTS = os.path.join(ROOT, "brand-source", "fonts")
F = lambda *p: "file://" + os.path.join(ROOT, *p)
SRC = lambda ad: F("signage-source", ad)
FOTO = lambda ad: F("sosyal-medya", "bitmis-fotograflar", ad)
IC = lambda ad: F("public", "images", "ic-mekan", ad)
AILE_ANAHTAR = SRC("aile/aile2-kesik.png")   # 1654x1694
AILE_SEVINC = SRC("aile/aile-kesik.png")     # 2243x1695
W = 1080

_SVG = {}


def logo(ad, yukseklik, renk, renk2=None):
    """Vektör logoyu istenen renkte satır içi SVG olarak verir (ad: mia | tilda | ocean)."""
    dosya = {"mia": "mia-beyaz.svg", "tilda": "tilda-beyaz.svg", "ocean": "ocean-beyaz.svg"}[ad]
    if dosya not in _SVG:
        _SVG[dosya] = open(os.path.join(ROOT, "public", "brand", "vektor", dosya), encoding="utf-8").read()
    s = _SVG[dosya]
    vb = re.search(r'viewBox="0 0 (\d+) (\d+)"', s)
    en = round(yukseklik * int(vb.group(1)) / int(vb.group(2)))
    s = re.sub(r'<svg [^>]*>', f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb.group(0)[9:-1]}" '
                               f'style="width:{en}px;height:{yukseklik}px;flex:none;display:block">', s, count=1)
    renkler = iter([renk, renk2 or renk, renk, renk])
    return re.sub(r'fill="#[0-9a-fA-F]{6}"', lambda m: f'fill="{next(renkler)}"', s)


def wa(s, c="#25d366"):
    return (f'<svg viewBox="0 0 24 24" style="width:{s}px;height:{s}px;fill:{c};flex:none">'
            '<path d="M17.5 14.4c-.3-.2-1.7-.8-2-.9-.3-.1-.5-.2-.7.2-.2.3-.7.9-.9 1.1-.2.2-.3.2-.6.1-.3-.2-1.2-.5-2.3-1.4-.9-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6.1-.1.3-.3.4-.5.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5 0-.1-.7-1.6-.9-2.2-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.4s1.1 2.8 1.2 3c.2.2 2.1 3.2 5 4.5.7.3 1.2.5 1.7.6.7.2 1.3.2 1.8.1.6-.1 1.7-.7 1.9-1.3.2-.7.2-1.2.2-1.3-.1-.2-.3-.3-.6-.4z"/>'
            '<path d="M12 2C6.5 2 2 6.5 2 12c0 1.8.5 3.5 1.3 5L2 22l5.1-1.3c1.4.8 3.1 1.2 4.9 1.2 5.5 0 10-4.5 10-10S17.5 2 12 2zm0 18.2c-1.6 0-3.1-.4-4.4-1.2l-.3-.2-3 .8.8-2.9-.2-.3C4 15 3.6 13.5 3.6 12 3.6 7.4 7.4 3.6 12 3.6S20.4 7.4 20.4 12 16.6 20.2 12 20.2z"/></svg>')


def tel_ikon(s, c):
    return (f'<svg viewBox="0 0 24 24" style="width:{s}px;height:{s}px;flex:none" fill="none" stroke="{c}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>')


def css(h):
    return f"""
@font-face {{ font-family: Mont; src: url("file://{FONTS}/Montserrat-var.ttf"); font-weight: 100 900; }}
@font-face {{ font-family: Jost; src: url("file://{FONTS}/Jost-var.ttf"); font-weight: 100 900; }}
@font-face {{ font-family: Osw; src: url("file://{FONTS}/Oswald-var.ttf"); font-weight: 200 700; }}
@font-face {{ font-family: Play; src: url("file://{FONTS}/Playfair-var.ttf"); font-weight: 400 900; }}
@font-face {{ font-family: Fr; src: url("file://{FONTS}/Fraunces-600.ttf"); font-weight: 600; }}
@font-face {{ font-family: Fr; src: url("file://{FONTS}/Fraunces-700.ttf"); font-weight: 700; }}
@font-face {{ font-family: Dans; src: url("file://{FONTS}/Dancing-var.ttf"); font-weight: 400 700; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:{W}px; height:{h}px; overflow:hidden; position:relative; font-family:Mont,sans-serif;
       -webkit-font-smoothing:antialiased; display:flex; flex-direction:column; }}
.a {{ position:absolute; }}
.tek {{ white-space:nowrap; }}
.orta {{ flex:1; position:relative; min-height:0; }}
.sat {{ display:flex; align-items:center; }}
"""


# Story'de üst/alt güvenli alan için ek boşluk
def pay(h):
    return (130, 150) if h > 1500 else (0, 0)


# ------------------------------------------------------------- 1 · ev çerçevesi

def d1(h):
    ust, alt = pay(h)
    KUM, YESIL, TURUNCU = "#f6ead7", "#14453d", "#f08a24"
    ev = "polygon(50% 0, 100% 31%, 100% 100%, 0 100%, 0 31%)"
    return f"""<body style="background:{KUM};padding:{56 + ust}px 0 0">
  <div class="sat" style="justify-content:space-between;padding:0 64px">
    {logo('mia', 104, YESIL)}
    <div style="text-align:right"><div class="tek" style="font-size:14px;font-weight:700;letter-spacing:.3em;color:{TURUNCU}">MÜTEAHHİT</div>
      <div style="margin-top:10px">{logo('tilda', 44, YESIL)}</div></div>
  </div>
  <div style="padding:34px 64px 0">
    <div class="tek" style="font-family:Fr;font-weight:600;font-style:italic;font-size:60px;color:{YESIL};line-height:1">Bir evden fazlası,</div>
    <div class="tek" style="margin-top:8px;font-size:112px;font-weight:900;letter-spacing:-.03em;line-height:1;color:{YESIL}">YENİ BİR <span style="color:{TURUNCU}">HAYAT</span></div>
  </div>
  <div class="orta" style="margin-top:26px">
    <div class="a" style="right:44px;bottom:0;top:0;width:{760 if h < 1500 else 860}px;background:{TURUNCU};clip-path:{ev}"></div>
    <div class="a" style="right:60px;bottom:0;top:20px;width:{728 if h < 1500 else 828}px;clip-path:{ev};background:#ddd">
      <img src="{SRC('courtyard-pools.jpg')}" style="width:100%;height:100%;object-fit:cover;object-position:52% 50%"></div>
    <img class="a" src="{AILE_ANAHTAR}" style="left:-36px;bottom:0;height:{'74%' if h < 1500 else '62%'};filter:drop-shadow(0 18px 26px rgba(20,40,30,.3))">
    <div class="a" style="right:26px;bottom:{'7%' if h < 1500 else '9%'};width:300px;height:300px;border-radius:50%;background:{YESIL};color:#fff;display:flex;flex-direction:column;
         align-items:center;justify-content:center;text-align:center;box-shadow:0 18px 40px rgba(20,69,61,.45);border:6px solid {KUM};transform:rotate(-6deg)">
      <div class="tek" style="font-size:66px;font-weight:900;letter-spacing:-.02em;line-height:1">699.000</div>
      <div class="tek" style="margin-top:6px;font-size:25px;font-weight:800;color:{TURUNCU}">TL'DEN BAŞLAYAN</div>
      <div class="tek" style="font-size:38px;font-weight:900;line-height:1.1">PEŞİNAT</div>
    </div>
  </div>
  <div class="sat" style="background:{YESIL};color:#fff;justify-content:space-between;padding:30px 64px {34 + alt}px">
    <div><div class="tek" style="font-size:44px;font-weight:900;color:{TURUNCU};line-height:1">60 AY SABİT TAKSİT</div>
      <div class="tek" style="margin-top:12px;font-size:25px;font-weight:600;letter-spacing:.02em">Banka yok · Faiz yok · Kefil yok</div></div>
    <div style="text-align:right"><div class="tek" style="font-size:62px;font-weight:900;line-height:1">444 10 58</div>
      <div class="sat tek" style="margin-top:10px;gap:10px;justify-content:flex-end;font-size:27px;font-weight:700">{wa(30)}0540 028 00 41</div></div>
  </div>
</body>"""


# ---------------------------------------------------------------- 2 · gece altın

def d2(h):
    ust, alt = pay(h)
    GECE, ALTIN = "#071a3a", "#f6b93b"
    kutu = lambda b, k: (f'<div style="flex:1;border:3px solid {ALTIN};border-radius:18px;padding:18px 0 16px;text-align:center;background:rgba(7,26,58,.55)">'
                         f'<div class="tek" style="font-family:Osw;font-weight:700;font-size:92px;line-height:1;color:{ALTIN}">{b}</div>'
                         f'<div class="tek" style="margin-top:8px;font-family:Osw;font-weight:500;font-size:34px;letter-spacing:.14em;color:#fff">{k}</div></div>')
    return f"""<body style="background:{GECE};color:#fff;padding:{52 + ust}px 0 0">
  <img class="a" src="{SRC('night-gate-temiz.jpg')}" style="left:0;bottom:{120 + alt}px;width:{W}px;height:{round(h * .62)}px;object-fit:cover;object-position:50% 60%;
       -webkit-mask-image:linear-gradient(180deg,transparent 0%,#000 34%)">
  <div style="position:relative;display:flex;flex-direction:column;align-items:center">
    {logo('mia', 96, '#fff')}
    <div style="margin-top:34px;transform:rotate(-3deg);display:flex;flex-direction:column;align-items:center">
      <div class="tek" style="font-family:Osw;font-weight:700;font-size:112px;line-height:1;background:{ALTIN};color:{GECE};padding:6px 34px 12px">EV SAHİBİ OLMAK</div>
      <div class="tek" style="margin-top:-4px;font-family:Osw;font-weight:700;font-size:92px;line-height:1;background:#fff;color:{GECE};padding:6px 30px 12px">ARTIK ÇOK KOLAY!</div>
    </div>
    <div style="margin-top:44px;display:flex;gap:26px;width:{W - 150}px">{kutu('699.000 TL', "'DEN BAŞLAYAN PEŞİNAT")}{kutu('60 AY', 'SABİT TAKSİT')}</div>
    <div class="tek" style="margin-top:22px;font-family:Osw;font-weight:500;font-size:31px;letter-spacing:.1em;background:rgba(7,26,58,.82);border-radius:999px;padding:10px 30px 12px">BANKA YOK &nbsp;·&nbsp; FAİZ YOK &nbsp;·&nbsp; KEFİL YOK &nbsp;·&nbsp; ARA ÖDEME YOK</div>
  </div>
  <div class="orta"></div>
  <div class="sat" style="position:relative;background:{ALTIN};color:{GECE};justify-content:space-between;padding:22px 60px {24 + alt}px">
    <div class="sat" style="gap:22px">{logo('tilda', 46, GECE)}<span style="width:2px;height:54px;background:{GECE};opacity:.35"></span>{logo('ocean', 50, GECE)}</div>
    <div class="sat" style="gap:16px">{tel_ikon(46, GECE)}<span class="tek" style="font-family:Osw;font-weight:700;font-size:74px;line-height:1">444 10 58</span></div>
  </div>
</body>"""


# -------------------------------------------------------------------- 3 · anahtar

def d3(h):
    ust, alt = pay(h)
    K1, K2, KREM = "#d4142f", "#8f0b1f", "#fff3e2"
    cap = 640 if h < 1500 else 820
    return f"""<body style="background:radial-gradient(120% 80% at 80% 20%,{K1} 0%,{K2} 100%);color:#fff;padding:{54 + ust}px 0 0">
  <div class="sat" style="justify-content:space-between;padding:0 60px">
    {logo('tilda', 46, '#fff')}{logo('mia', 92, '#fff')}
  </div>
  <div style="padding:{30 if h < 1500 else 60}px 60px 0">
    <div class="tek" style="font-family:Jost;font-weight:300;font-size:70px;line-height:1.02">Yeni bir başlangıcın</div>
    <div class="tek" style="font-family:Jost;font-weight:800;font-size:96px;line-height:1.05;letter-spacing:-.02em">ANAHTARI <span style="color:#ffd65a">BURADA</span></div>
  </div>
  <div class="orta">
    <div class="a" style="right:-90px;bottom:{-60 if h < 1500 else 40}px;width:{cap}px;height:{cap}px;border-radius:50%;border:12px solid {KREM};overflow:hidden;box-shadow:0 30px 60px rgba(0,0,0,.35)">
      <img src="{SRC('entrance-gate.jpg')}" style="width:100%;height:100%;object-fit:cover;object-position:34% 50%"></div>
    <img class="a" src="{AILE_ANAHTAR}" style="left:-30px;bottom:0;height:{'92%' if h < 1500 else '70%'};filter:drop-shadow(0 20px 30px rgba(60,0,10,.45))">
    <div class="a" style="right:40px;top:{26 if h < 1500 else 70}px;background:{KREM};color:{K2};border-radius:26px;padding:20px 34px 22px;text-align:center;box-shadow:0 18px 40px rgba(0,0,0,.3);transform:rotate(4deg)">
      <div class="tek" style="font-family:Jost;font-weight:800;font-size:84px;line-height:1">699.000 <span style="font-size:44px">TL</span></div>
      <div class="tek" style="margin-top:4px;font-family:Jost;font-weight:600;font-size:30px;letter-spacing:.04em">'den başlayan peşinat</div>
      <div class="tek" style="margin-top:12px;background:{K1};color:#fff;border-radius:999px;padding:8px 0;font-family:Jost;font-weight:700;font-size:30px;letter-spacing:.04em">60 AY SABİT TAKSİT</div>
    </div>
  </div>
  <div class="sat" style="position:relative;z-index:3;background:{KREM};color:{K2};justify-content:space-between;padding:24px 60px {26 + alt}px">
    <div class="tek" style="font-family:Jost;font-weight:700;font-size:31px;line-height:1.2">Banka yok · Faiz yok<br>Kefil yok · Ara ödeme yok</div>
    <div style="text-align:right"><div class="tek" style="font-family:Jost;font-weight:800;font-size:72px;line-height:1">444 10 58</div>
      <div class="sat tek" style="margin-top:6px;gap:10px;justify-content:flex-end;font-family:Jost;font-weight:700;font-size:28px">{wa(30)}0540 028 00 41</div></div>
  </div>
</body>"""


# ------------------------------------------------------------------ 4 · konum pini

def d4(h):
    ust, alt = pay(h)
    ZEMIN, PETROL, MERCAN = "#e8f3f6", "#0b5468", "#ff6b4a"
    pin = 600 if h < 1500 else 760
    etiket = lambda yer, dk, stil: (f'<div class="a sat" style="{stil};gap:14px;background:#fff;border-radius:999px;padding:10px 24px 10px 10px;box-shadow:0 10px 26px rgba(11,84,104,.2)">'
                                    f'<span class="tek" style="background:{MERCAN};color:#fff;border-radius:999px;padding:10px 16px;font-size:28px;font-weight:800;line-height:1">{dk}</span>'
                                    f'<span class="tek" style="font-size:27px;font-weight:700;color:{PETROL}">{yer}</span></div>')
    return f"""<body style="background:{ZEMIN};padding:{50 + ust}px 0 0">
  <div style="display:flex;flex-direction:column;align-items:center">
    {logo('mia', 100, PETROL)}
    <div class="tek" style="margin-top:26px;font-family:Play;font-weight:500;font-style:italic;font-size:66px;color:{PETROL};line-height:1">Doğru lokasyon,</div>
    <div class="tek" style="margin-top:8px;font-size:106px;font-weight:900;letter-spacing:-.03em;color:{PETROL};line-height:1">GÜÇLÜ <span style="color:{MERCAN}">YATIRIM</span></div>
    <div class="tek" style="margin-top:16px;font-size:26px;font-weight:600;letter-spacing:.22em;color:{PETROL};opacity:.75">İZMİT · MİA BÖLGESİ</div>
  </div>
  <div class="orta" style="margin-top:20px">
    <div class="a" style="left:50%;top:50%;width:{pin}px;height:{pin}px;margin:{-pin // 2 - 34}px 0 0 {-pin // 2}px;transform:rotate(45deg);border-radius:50% 50% 0 50%;background:{PETROL};
         box-shadow:0 24px 50px rgba(11,84,104,.35)"></div>
    <div class="a" style="left:50%;top:50%;width:{pin - 36}px;height:{pin - 36}px;margin:{-(pin - 36) // 2 - 34}px 0 0 {-(pin - 36) // 2}px;transform:rotate(45deg);border-radius:50% 50% 0 50%;overflow:hidden">
      <img src="{SRC('entrance-gate.jpg')}" style="width:142%;height:142%;margin:-21%;object-fit:cover;object-position:50% 50%;transform:rotate(-45deg)"></div>
    {etiket('D-100 Karayolu', '1 dk', 'left:34px;top:9%')}
    {etiket('Şehir Merkezi', '5 dk', 'right:34px;top:20%')}
    {etiket('41 Burada AVM', '3 dk', 'left:34px;bottom:27%')}
    {etiket('Şehir Hastanesi', '5 dk', 'right:34px;bottom:15%')}
  </div>
  <div class="sat" style="position:relative;z-index:3;background:{MERCAN};color:#fff;justify-content:center;gap:22px;padding:18px 0">
    <span class="tek" style="font-size:33px;font-weight:900">699.000 TL'den başlayan peşinat</span>
    <span style="width:3px;height:32px;background:#fff;opacity:.6"></span>
    <span class="tek" style="font-size:33px;font-weight:900">60 ay sabit taksit</span>
  </div>
  <div class="sat" style="position:relative;z-index:3;background:#fff;justify-content:space-between;padding:22px 60px {24 + alt}px">
    <div><div class="tek" style="font-size:13px;font-weight:700;letter-spacing:.3em;color:{MERCAN}">MÜTEAHHİT</div><div style="margin-top:8px">{logo('tilda', 42, PETROL)}</div></div>
    <div class="sat" style="gap:26px;color:{PETROL}">
      <span class="sat tek" style="gap:10px;font-size:29px;font-weight:700">{wa(32)}0540 028 00 41</span>
      <span class="tek" style="font-size:62px;font-weight:900;line-height:1">444 10 58</span></div>
  </div>
</body>"""


# ----------------------------------------------------------------------- 5 · yaşam

def d5(h):
    ust, alt = pay(h)
    Y1, Y2, ALTIN = "#0c4a3a", "#062c22", "#e9c46a"
    kartlar = [("17-sus-havuzu.webp", "Süs Havuzları", -5), ("18-yuruyus-yolu.webp", "Yürüyüş Yolları", 3),
               ("19-cocuk-oyun-parki.webp", "Çocuk Parkı", -3), ("20-kapali-otopark.webp", "Kapalı Otopark", 5)]
    kh = 250 if h < 1500 else 300
    k = "".join(f'<div style="width:226px;background:#fff;padding:9px 9px 12px;border-radius:10px;transform:rotate({a}deg);box-shadow:0 16px 34px rgba(0,0,0,.4)">'
                f'<img src="{IC(g)}" style="width:100%;height:{kh - 62}px;object-fit:cover;border-radius:5px;display:block">'
                f'<div class="tek" style="margin-top:9px;text-align:center;font-size:22px;font-weight:800;color:{Y1}">{t}</div></div>' for g, t, a in kartlar)
    return f"""<body style="background:linear-gradient(180deg,{Y1} 0%,{Y2} 100%);color:#fff;padding:{50 + ust}px 0 0">
  <img class="a" src="{FOTO('20-giris-gunesli.jpg') if h > 1500 else SRC('entrance-gate.jpg')}" style="left:0;bottom:0;width:{W}px;height:{round(h * .52)}px;object-fit:cover;object-position:{'50% 40%' if h > 1500 else '40% 50%'};
       -webkit-mask-image:linear-gradient(180deg,transparent 0%,#000 30%)">
  <div style="position:relative;display:flex;flex-direction:column;align-items:center">
    <div class="tek" style="font-family:Dans;font-weight:700;font-size:78px;color:{ALTIN};line-height:1">Bir evden fazlası</div>
    <div class="tek" style="margin-top:10px;font-family:Play;font-weight:800;font-size:92px;line-height:1;letter-spacing:-.01em">EKSİKSİZ BİR YAŞAM</div>
    <div class="tek" style="margin-top:16px;font-size:24px;font-weight:600;letter-spacing:.24em;opacity:.85">MİA PARK OCEAN · İZMİT MİA BÖLGESİ</div>
    <div style="margin-top:{34 if h < 1500 else 54}px;display:flex;gap:18px">{k}</div>
  </div>
  <div class="orta"></div>
  <div style="position:relative;background:linear-gradient(180deg,rgba(6,44,34,0),rgba(6,44,34,.92) 40%);padding:{90 if h < 1500 else 120}px 56px {30 + alt}px">
    <div class="sat" style="justify-content:center;gap:20px;background:{ALTIN};color:{Y2};border-radius:999px;padding:16px 0;box-shadow:0 14px 34px rgba(0,0,0,.35)">
      <span class="tek" style="font-size:32px;font-weight:900">699.000 TL'den başlayan peşinat</span>
      <span style="width:3px;height:30px;background:{Y2};opacity:.4"></span>
      <span class="tek" style="font-size:32px;font-weight:900">60 ay sabit taksit</span></div>
    <div class="sat" style="margin-top:24px;justify-content:space-between">
      <div class="sat" style="gap:22px">{logo('mia', 84, '#fff')}<span style="width:2px;height:70px;background:rgba(255,255,255,.4)"></span>{logo('tilda', 40, '#fff')}</div>
      <div style="text-align:right"><div class="tek" style="font-size:60px;font-weight:900;line-height:1">444 10 58</div>
        <div class="sat tek" style="margin-top:8px;gap:10px;justify-content:flex-end;font-size:26px;font-weight:700">{wa(28)}0540 028 00 41</div></div>
    </div>
  </div>
</body>"""


# ------------------------------------------------------------------- 6 · beş neden

def d6(h):
    ust, alt = pay(h)
    T1, T2, SARI, KOYU = "#12a0b4", "#0a6a80", "#ffd447", "#06303b"
    nedenler = [("Bankasız, faizsiz ödeme", "699.000 TL'den başlayan peşinat, 60 ay sabit taksit"),
                ("Merkezi konum", "D-100'e 1 dk, şehir merkezine 5 dk"),
                ("Depreme dayanıklı yapı", "Fore kazık temel sistemi"),
                ("Zengin sosyal yaşam", "Kapalı havuz, fitness, sauna, çocuk parkı"),
                ("Kooperatif güvencesi", "Bakanlık KOOPBİS sistemine kayıtlı")]
    bosluk, cap, f1, f2 = (20, 78, 39, 24) if h < 1500 else (50, 96, 46, 28)
    n = "".join(f'<div class="sat" style="gap:22px"><span style="width:{cap}px;height:{cap}px;border-radius:50%;background:{SARI};color:{KOYU};display:flex;align-items:center;justify-content:center;'
                f'font-family:Osw;font-weight:700;font-size:{round(cap * .64)}px;flex:none;box-shadow:0 8px 18px rgba(0,0,0,.2)">{i}</span>'
                f'<div><div class="tek" style="font-size:{f1}px;font-weight:800;line-height:1.05">{b}</div>'
                f'<div class="tek" style="margin-top:5px;font-size:{f2}px;font-weight:500;opacity:.92">{t}</div></div></div>' for i, (b, t) in enumerate(nedenler, 1))
    return f"""<body style="background:linear-gradient(160deg,{T1} 0%,{T2} 100%);color:#fff;padding:{52 + ust}px 0 0">
  <div class="a" style="right:-170px;top:{-150 + ust}px;width:520px;height:520px;border-radius:50%;border:60px solid rgba(255,255,255,.08)"></div>
  <div class="sat" style="position:relative;justify-content:space-between;padding:0 60px">
    <div class="sat" style="gap:20px">{logo('mia', 92, '#fff')}</div>
    <div style="text-align:right"><div class="tek" style="font-size:13px;font-weight:700;letter-spacing:.3em;color:{SARI}">MÜTEAHHİT</div><div style="margin-top:9px">{logo('tilda', 40, '#fff')}</div></div>
  </div>
  <div style="position:relative;padding:{32 if h < 1500 else 56}px 60px 0">
    <div class="tek" style="font-size:44px;font-weight:600;line-height:1">MİA PARK OCEAN'ı seçmeniz için</div>
    <div class="tek" style="margin-top:6px;font-family:Osw;font-weight:700;font-size:170px;line-height:1;letter-spacing:-.01em"><span style="color:{SARI}">5</span> NEDEN</div>
  </div>
  <div class="orta" style="margin-top:{14 if h < 1500 else 40}px">
    <img class="a" src="{AILE_SEVINC}" style="right:-150px;bottom:0;height:{'56%' if h < 1500 else '40%'};filter:drop-shadow(0 20px 30px rgba(0,40,50,.4))">
    <div style="position:relative;padding:0 60px;display:flex;flex-direction:column;gap:{bosluk}px">{n}</div>
  </div>
  <div class="sat" style="position:relative;background:#fff;color:{KOYU};justify-content:space-between;padding:22px 60px {24 + alt}px">
    <div class="sat" style="gap:18px">{tel_ikon(50, T2)}<span class="tek" style="font-family:Osw;font-weight:700;font-size:80px;line-height:1;color:{T2}">444 10 58</span></div>
    <div style="text-align:right"><div class="sat tek" style="gap:10px;justify-content:flex-end;font-size:30px;font-weight:800">{wa(32)}0540 028 00 41</div>
      <div class="tek" style="margin-top:6px;font-size:22px;font-weight:600;letter-spacing:.06em;opacity:.75">miaparkocean.com</div></div>
  </div>
</body>"""


TASARIMLAR = [("1-ev-cercevesi", d1), ("2-gece-altin", d2), ("3-anahtar", d3), ("4-konum-pini", d4), ("5-yasam", d5), ("6-bes-neden", d6)]
BICIMLER = [("4x5", 1350), ("9x16", 1920)]


def main():
    os.makedirs(OUT, exist_ok=True)
    gecici = tempfile.mkdtemp(prefix="cesit-")
    isler = []
    for ad, fn in TASARIMLAR:
        for oran, h in BICIMLER:
            tam = f"{ad}-{oran}"
            hp = os.path.join(gecici, tam + ".html")
            open(hp, "w", encoding="utf-8").write(
                f'<!doctype html><html><head><meta charset="utf-8"><style>{css(h)}</style></head>{fn(h)}</html>')
            isler.append(dict(html=hp, w=W, h=h, dsf=2, dilim=W, cikti=os.path.join(gecici, tam), ad=tam))
    jp = os.path.join(gecici, "isler.json")
    json.dump(isler, open(jp, "w"))
    npm = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    subprocess.run(["node", os.path.join(ROOT, "scripts", "mega-bilbord", "render.cjs"), jp], check=True,
                   env={**os.environ, "NODE_PATH": npm}, stdout=subprocess.DEVNULL)
    for is_ in isler:
        im = Image.open(json.load(open(is_["cikti"] + ".json"))[0]).convert("RGB")
        yol = os.path.join(OUT, f"mia-{is_['ad']}.jpg")
        im.save(yol, quality=93)
        print("  →", os.path.relpath(yol, ROOT), im.size)


if __name__ == "__main__":
    main()
