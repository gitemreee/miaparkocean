#!/usr/bin/env python3
"""
Çeşitlendirilmiş kreatifler, 2. seri — beğenilen üç tasarımın (ev çerçevesi, anahtar, konum pini)
tarzında altı yeni düzen: düz canlı zemin, biçimli çerçevede proje görseli, önde aile, tek vurgu
kelimeli iri başlık, yuvarlak fiyat etiketi, altta iletişim bandı.

   7-anahtar-deligi   hardal sarısı + lacivert · anahtar deliği çerçeve
   8-kemer            turkuaz + krem + turuncu · kemerli kapı çerçeve
   9-altmis-ay        kraliyet mavisi + sarı · içi fotoğraflı dev "60"
  10-kalp             mor + pembe · kalp çerçeve
  11-pencere          canlı yeşil · dört gözlü pencere, sunucu
  12-yorunge          turuncu + lacivert · yuvarlak görsel, çevresinde mesafe etiketleri

Her biri 4x5 (1080x1350) ve 9x16 (1080x1920) çıkar. Yardımcılar build-reklam-cesit.py'den gelir.

    python3.13 scripts/build-reklam-cesit-2.py
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
logo, wa, tel_ikon, css, pay, SRC, FOTO, W = c.logo, c.wa, c.tel_ikon, c.css, c.pay, c.SRC, c.FOTO, c.W
AILE_ANAHTAR, AILE_SEVINC = c.AILE_ANAHTAR, c.AILE_SEVINC
SUNUCU = SRC("aile/sunucu2-kesik.png")
OUT = os.path.join(ROOT, "sosyal-medya", "reklam-cesit-2")

_n = [0]


def sekil(src, w, h, sekiller, kontur_renk, kontur=14, hizala="xMidYMid", stil=""):
    """Görseli verilen SVG biçim(ler)iyle kırpar; aynı biçimin kalın konturunu arkasına çizer."""
    _n[0] += 1
    k = f"k{_n[0]}"
    return (f'<svg class="a" style="{stil};overflow:visible" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<defs><clipPath id="{k}">{sekiller}</clipPath></defs>'
            f'<g fill="{kontur_renk}" stroke="{kontur_renk}" stroke-width="{2 * kontur}" stroke-linejoin="round">{sekiller}</g>'
            f'<image href="{src}" width="{w}" height="{h}" preserveAspectRatio="{hizala} slice" clip-path="url(#{k})"/></svg>')


def etiket(ust, orta, alt, zemin, yazi, vurgu, cap=290, stil="", kenar="#fff", aci=-6):
    """Yuvarlak fiyat etiketi."""
    return (f'<div class="a" style="{stil};width:{cap}px;height:{cap}px;border-radius:50%;background:{zemin};color:{yazi};display:flex;flex-direction:column;'
            f'align-items:center;justify-content:center;text-align:center;box-shadow:0 18px 40px rgba(0,0,0,.3);border:6px solid {kenar};transform:rotate({aci}deg);z-index:2">'
            f'<div class="tek" style="font-size:{round(cap * .22)}px;font-weight:900;letter-spacing:-.02em;line-height:1">{ust}</div>'
            f'<div class="tek" style="margin-top:{round(cap * .02)}px;font-size:{round(cap * .083)}px;font-weight:800;color:{vurgu}">{orta}</div>'
            f'<div class="tek" style="font-size:{round(cap * .127)}px;font-weight:900;line-height:1.1">{alt}</div></div>')


FIYAT = ("699.000", "TL'DEN BAŞLAYAN", "PEŞİNAT")


def alt_bant(zemin, yazi, vurgu, alt, sol1="60 AY SABİT TAKSİT", sol2="Banka yok · Faiz yok · Kefil yok"):
    return f"""
  <div class="sat" style="position:relative;z-index:3;background:{zemin};color:{yazi};justify-content:space-between;padding:30px 64px {34 + alt}px">
    <div><div class="tek" style="font-size:44px;font-weight:900;color:{vurgu};line-height:1">{sol1}</div>
      <div class="tek" style="margin-top:12px;font-size:25px;font-weight:600;letter-spacing:.02em">{sol2}</div></div>
    <div style="text-align:right"><div class="tek" style="font-size:62px;font-weight:900;line-height:1">444 10 58</div>
      <div class="sat tek" style="margin-top:10px;gap:10px;justify-content:flex-end;font-size:27px;font-weight:700">{wa(30)}0540 028 00 41</div></div>
  </div>"""


def ust_logolar(sol, sag, renk, vurgu, muteahhit_sagda=True):
    """sol/sag: 'mia' | 'tilda'. Tilda'nın üstüne küçük MÜTEAHHİT etiketi konur."""
    def parca(ad, hiza):
        if ad == "mia":
            return logo("mia", 100, renk)
        return (f'<div style="text-align:{hiza}"><div class="tek" style="font-size:14px;font-weight:700;letter-spacing:.3em;color:{vurgu}">MÜTEAHHİT</div>'
                f'<div style="margin-top:10px">{logo("tilda", 44, renk)}</div></div>')
    return f'<div class="sat" style="position:relative;justify-content:space-between;padding:0 64px">{parca(sol, "left")}{parca(sag, "right")}</div>'


# ----------------------------------------------------------- 7 · anahtar deliği

def d7(h):
    ust, alt = pay(h)
    SARI, LACI, KIRMIZI = "#ffc93c", "#132a5e", "#e63946"
    w, hh = (540, 770) if h < 1500 else (680, 1000)
    r, cx = w * .46, w / 2
    delik = (f'<circle cx="{cx}" cy="{r}" r="{r}"/>'
             f'<polygon points="{cx - w * .16},{r * 1.55} {cx + w * .16},{r * 1.55} {cx + w * .37},{hh} {cx - w * .37},{hh}"/>')
    return f"""<body style="background:{SARI};padding:{56 + ust}px 0 0">
  {ust_logolar('tilda', 'mia', LACI, KIRMIZI)}
  <div style="padding:34px 64px 0">
    <div class="tek" style="font-family:Fr;font-weight:600;font-style:italic;font-size:60px;color:{LACI};line-height:1">Yeni evinizin</div>
    <div class="tek" style="margin-top:8px;font-size:108px;font-weight:900;letter-spacing:-.03em;line-height:1;color:{LACI}">ANAHTARI <span style="color:{KIRMIZI}">HAZIR</span></div>
  </div>
  <div class="orta" style="margin-top:30px">
    {sekil(SRC('entrance-gate.jpg'), w, hh, delik, LACI, 14, 'xMidYMid', f'right:70px;bottom:-4px')}
    <img class="a" src="{AILE_ANAHTAR}" style="left:-36px;bottom:0;height:{'76%' if h < 1500 else '60%'};filter:drop-shadow(0 18px 26px rgba(19,42,94,.32))">
    {etiket(*FIYAT, KIRMIZI, '#fff', SARI, 290, f"right:22px;top:{'2%' if h < 1500 else '4%'}", SARI, 7)}
  </div>
  {alt_bant(LACI, '#fff', SARI, alt)}
</body>"""


# --------------------------------------------------------------------- 8 · kemer

def d8(h):
    ust, alt = pay(h)
    T1, T2, KREM, TURUNCU = "#12a5ac", "#0a7c86", "#fff4e0", "#ff8c42"
    w, hh = (660, 720) if h < 1500 else (800, 1000)
    kemer = f'<path d="M0,{hh} L0,{w / 2} A{w / 2},{w / 2} 0 0 1 {w},{w / 2} L{w},{hh} Z"/>'
    return f"""<body style="background:linear-gradient(170deg,{T1},{T2});color:#fff;padding:{56 + ust}px 0 0">
  {ust_logolar('mia', 'tilda', '#fff', KREM)}
  <div style="padding:30px 0 0;text-align:center">
    <div class="tek" style="font-family:Jost;font-weight:300;font-size:70px;line-height:1">Kiradan kurtulun,</div>
    <div class="tek" style="margin-top:6px;font-family:Jost;font-weight:800;font-size:112px;line-height:1.02;letter-spacing:-.02em">EV SAHİBİ <span style="color:#ffd65a">OLUN</span></div>
  </div>
  <div class="orta" style="margin-top:30px">
    {sekil(SRC('courtyard-pools.jpg'), w, hh, kemer, KREM, 13, 'xMidYMid', f'left:{(W - w) // 2}px;bottom:-4px')}
    <img class="a" src="{AILE_SEVINC}" style="left:50%;bottom:0;height:{'58%' if h < 1500 else '46%'};transform:translateX(-50%);filter:drop-shadow(0 18px 26px rgba(4,60,66,.4))">
    {etiket(*FIYAT, TURUNCU, '#fff', '#fff3c4', 280, f"right:26px;top:{'6%' if h < 1500 else '8%'}", KREM, 7)}
  </div>
  {alt_bant(KREM, T2, TURUNCU, alt)}
</body>"""


# ------------------------------------------------------------------ 9 · altmış ay

def d9(h):
    ust, alt = pay(h)
    MAVI, MAVI2, SARI = "#1c4fd8", "#12348f", "#ffd23f"
    boy = 400 if h < 1500 else 460
    return f"""<body style="background:linear-gradient(160deg,{MAVI},{MAVI2});color:#fff;padding:{56 + ust}px 0 0">
  {ust_logolar('mia', 'tilda', '#fff', SARI)}
  <div style="padding:{26 if h < 1500 else 60}px 64px 0">
    <div class="tek" style="font-family:Fr;font-weight:600;font-style:italic;font-size:58px;line-height:1">Banka yok, faiz yok;</div>
    <div class="sat" style="margin-top:6px;gap:26px;align-items:center">
      <div style="position:relative;line-height:.84;font-size:{boy}px;font-weight:900;letter-spacing:-.05em">
        <div class="tek" style="position:absolute;left:10px;top:10px;color:{SARI}">60</div>
        <div class="tek" style="position:relative;background:url('{SRC('courtyard-pools.jpg')}') 50% 40%/cover;-webkit-background-clip:text;background-clip:text;color:transparent;
             -webkit-text-stroke:6px #fff">60</div>
      </div>
      <div class="tek" style="font-size:{round(boy * .45)}px;font-weight:900;line-height:.9;letter-spacing:-.03em;color:{SARI}">AY</div>
    </div>
    <div class="tek" style="margin-top:14px;font-size:{112 if h < 1500 else 124}px;font-weight:900;line-height:1;letter-spacing:-.03em">SABİT TAKSİT</div>
  </div>
  <div class="orta">
    <img class="a" src="{AILE_ANAHTAR}" style="left:-30px;bottom:0;height:{'108%' if h < 1500 else '92%'};filter:drop-shadow(0 18px 26px rgba(6,20,70,.45))">
    {etiket(*FIYAT, SARI, MAVI2, '#d6252e', 320 if h < 1500 else 380, f"right:44px;bottom:{'14%' if h < 1500 else '26%'}", '#fff', 6)}
  </div>
  {alt_bant('#fff', MAVI2, MAVI, alt, 'ARA ÖDEME YOK', 'Kefil yok · Kredi yok · Faiz yok')}
</body>"""


# --------------------------------------------------------------------- 10 · kalp

def d10(h):
    ust, alt = pay(h)
    M1, M2, PEMBE, KREM = "#5a35a8", "#341b6b", "#ff7aa8", "#fff1e6"
    w, hh = (800, 730) if h < 1500 else (960, 880)
    sx, sy = w / 100, hh / 92
    P = lambda x, y: f"{x * sx:.1f},{y * sy:.1f}"
    kalp = (f'<path d="M{P(50, 92)} C{P(20, 66)} {P(0, 46)} {P(0, 26)} A{25 * sx:.1f},{25 * sy:.1f} 0 0 1 {P(50, 22)} '
            f'A{25 * sx:.1f},{25 * sy:.1f} 0 0 1 {P(100, 26)} C{P(100, 46)} {P(80, 66)} {P(50, 92)} Z"/>')
    return f"""<body style="background:radial-gradient(120% 80% at 20% 10%,{M1},{M2});color:#fff;padding:{56 + ust}px 0 0">
  {ust_logolar('tilda', 'mia', '#fff', PEMBE)}
  <div style="padding:26px 0 0;text-align:center">
    <div class="tek" style="font-family:Dans;font-weight:700;font-size:92px;color:{PEMBE};line-height:1">Ailenizin</div>
    <div class="tek" style="margin-top:4px;font-size:106px;font-weight:900;letter-spacing:-.03em;line-height:1">SEVECEĞİ <span style="color:#ffd65a">YUVA</span></div>
  </div>
  <div class="orta" style="margin-top:{34 if h < 1500 else 70}px">
    {sekil(SRC('courtyard-pools.jpg'), w, hh, kalp, PEMBE, 12, 'xMidYMid', f'left:{(W - w) // 2}px;top:0')}
    <img class="a" src="{AILE_SEVINC}" style="left:50%;bottom:0;height:{'56%' if h < 1500 else '46%'};transform:translateX(-50%);filter:drop-shadow(0 18px 26px rgba(20,6,50,.5))">
    {etiket(*FIYAT, KREM, M2, '#e0336d', 270, f"right:20px;top:{'30%' if h < 1500 else '36%'}", PEMBE, 8)}
  </div>
  {alt_bant(KREM, M2, '#e0336d', alt)}
</body>"""


# ------------------------------------------------------------------ 11 · pencere

def d11(h):
    ust, alt = pay(h)
    Y1, Y2, KOYU = "#35c27a", "#1f9a5a", "#0b3a24"
    w, hh = (600, 720) if h < 1500 else (700, 1000)
    g = 20
    gw, gh = (w - g) / 2, (hh - g) / 2
    pencere = "".join(f'<rect x="{x:.0f}" y="{y:.0f}" width="{gw:.0f}" height="{gh:.0f}" rx="34"/>' for x in (0, gw + g) for y in (0, gh + g))
    return f"""<body style="background:linear-gradient(165deg,{Y1},{Y2});color:#fff;padding:{56 + ust}px 0 0">
  {ust_logolar('mia', 'tilda', '#fff', KOYU)}
  <div style="padding:32px 64px 0">
    <div class="tek" style="font-family:Fr;font-weight:600;font-style:italic;font-size:60px;color:{KOYU};line-height:1">Pencerenizi açın,</div>
    <div class="tek" style="margin-top:8px;font-size:112px;font-weight:900;letter-spacing:-.03em;line-height:1">HUZURA <span style="color:{KOYU}">BAKIN</span></div>
  </div>
  <div class="orta" style="margin-top:34px">
    {sekil(SRC('courtyard-pools.jpg'), w, hh, pencere, '#fff', 12, 'xMidYMid', f'right:52px;top:0')}
    <img class="a" src="{SUNUCU}" style="left:-60px;bottom:0;height:{'104%' if h < 1500 else '86%'};filter:drop-shadow(0 18px 26px rgba(6,50,30,.4))">
    {etiket(*FIYAT, KOYU, '#fff', '#ffe066', 290, f"right:22px;bottom:{'6%' if h < 1500 else '5%'}", '#fff', -6)}
  </div>
  {alt_bant(KOYU, '#fff', '#ffe066', alt)}
</body>"""


# ------------------------------------------------------------------- 12 · yörünge

def d12(h):
    ust, alt = pay(h)
    T1, T2, LACI = "#ff8a2a", "#f25c05", "#1b2a49"
    cap = 520 if h < 1500 else 640
    yor = cap + 190
    hap = lambda yer, dk, stil: (f'<div class="a sat" style="{stil};gap:12px;background:#fff;border-radius:999px;padding:9px 22px 9px 9px;box-shadow:0 10px 24px rgba(120,40,0,.28);z-index:2">'
                                 f'<span class="tek" style="background:{LACI};color:#fff;border-radius:999px;padding:10px 15px;font-size:27px;font-weight:800;line-height:1">{dk}</span>'
                                 f'<span class="tek" style="font-size:26px;font-weight:700;color:{LACI}">{yer}</span></div>')
    return f"""<body style="background:linear-gradient(165deg,{T1},{T2});color:#fff;padding:{50 + ust}px 0 0">
  <div style="display:flex;flex-direction:column;align-items:center">
    {logo('mia', 100, '#fff')}
    <div class="tek" style="margin-top:24px;font-family:Play;font-weight:500;font-style:italic;font-size:64px;line-height:1">İzmit'in merkezinde,</div>
    <div class="tek" style="margin-top:8px;font-size:114px;font-weight:900;letter-spacing:-.03em;line-height:1">HER YERE <span style="color:{LACI}">YAKIN</span></div>
  </div>
  <div class="orta" style="margin-top:14px">
    <div class="a" style="left:50%;top:50%;width:{yor}px;height:{yor}px;margin:{-yor // 2}px 0 0 {-yor // 2}px;border-radius:50%;border:5px dashed rgba(255,255,255,.75)"></div>
    <div class="a" style="left:50%;top:50%;width:{cap}px;height:{cap}px;margin:{-cap // 2}px 0 0 {-cap // 2}px;border-radius:50%;border:12px solid #fff;overflow:hidden;box-shadow:0 26px 54px rgba(120,40,0,.4)">
      <img src="{SRC('entrance-gate.jpg')}" style="width:100%;height:100%;object-fit:cover;object-position:36% 55%"></div>
    {hap('D-100 Karayolu', '1 dk', 'left:30px;top:7%')}
    {hap('41 Burada AVM', '3 dk', 'right:30px;top:7%')}
    {hap('Şehir Merkezi', '5 dk', 'left:14px;top:46%')}
    {hap('Şehir Hastanesi', '5 dk', 'right:14px;top:46%')}
    {hap('TEM Otoyolu', '5 dk', 'left:30px;bottom:6%')}
    {hap('Kocaeli Üniv.', '10 dk', 'right:30px;bottom:6%')}
  </div>
  <div class="sat" style="position:relative;z-index:3;background:#fff;color:{T2};justify-content:center;gap:22px;padding:18px 0">
    <span class="tek" style="font-size:33px;font-weight:900">699.000 TL'den başlayan peşinat</span>
    <span style="width:3px;height:32px;background:{T2};opacity:.5"></span>
    <span class="tek" style="font-size:33px;font-weight:900">60 ay sabit taksit</span>
  </div>
  <div class="sat" style="position:relative;z-index:3;background:{LACI};justify-content:space-between;padding:22px 60px {24 + alt}px">
    <div><div class="tek" style="font-size:13px;font-weight:700;letter-spacing:.3em;color:{T1}">MÜTEAHHİT</div><div style="margin-top:8px">{logo('tilda', 42, '#fff')}</div></div>
    <div class="sat" style="gap:26px">
      <span class="sat tek" style="gap:10px;font-size:29px;font-weight:700">{wa(32)}0540 028 00 41</span>
      <span class="tek" style="font-size:62px;font-weight:900;line-height:1">444 10 58</span></div>
  </div>
</body>"""


TASARIMLAR = [("7-anahtar-deligi", d7), ("8-kemer", d8), ("9-altmis-ay", d9), ("10-kalp", d10), ("11-pencere", d11), ("12-yorunge", d12)]
BICIMLER = [("4x5", 1350), ("9x16", 1920)]


def main():
    os.makedirs(OUT, exist_ok=True)
    gecici = tempfile.mkdtemp(prefix="cesit2-")
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
