#!/usr/bin/env python3
"""
Vurucu satış reklamları — dev rakam, rozet, net çağrı (1080x1920 story, 2x çizim).

Dört konsept:
  1-dev-rakam   "1 MİLYON TL peşinatla ev sahibi olun"       (20-giris-gunesli)
  2-yok-yok     "BANKA YOK. FAİZ YOK. KEFİL YOK."             (22-uzaktan-teleobjektif)
  3-kira        "Kiraya değil, kendi evinize ödeyin."         (19-balkon-cay-gunduz)
  4-takas       "Arabanız peşinatınız olsun."                 (21-yoldan-gunesli)

Hepsinde: MİA PARK OCEAN + Tilda İnşaat (müteahhit) logoları, 444 10 58 ve
WhatsApp 0540 028 00 41.

    python3.13 scripts/build-reklam-vurucu.py
"""

import json
import os
import subprocess
import tempfile

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "sosyal-medya", "reklam-vurucu")
FONTS = os.path.join(ROOT, "brand-source", "fonts")
W, H = 1080, 1920
FOTO_H = round(W * 2752 / 1536)
F = lambda *p: "file://" + os.path.join(ROOT, *p)
FOTO = lambda ad: F("sosyal-medya", "bitmis-fotograflar", ad)

LACI, LACI2 = "#061a33", "#0b2a4f"
TURK = "#17a7b9"
SARI, SARI2 = "#f6c344", "#ffd86b"

WA = ('<svg viewBox="0 0 24 24" style="width:{s}px;height:{s}px;fill:{c};flex:none">'
      '<path d="M17.5 14.4c-.3-.2-1.7-.8-2-.9-.3-.1-.5-.2-.7.2-.2.3-.7.9-.9 1.1-.2.2-.3.2-.6.1-.3-.2-1.2-.5-2.3-1.4-.9-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6.1-.1.3-.3.4-.5.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5 0-.1-.7-1.6-.9-2.2-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.4s1.1 2.8 1.2 3c.2.2 2.1 3.2 5 4.5.7.3 1.2.5 1.7.6.7.2 1.3.2 1.8.1.6-.1 1.7-.7 1.9-1.3.2-.7.2-1.2.2-1.3-.1-.2-.3-.3-.6-.4z"/>'
      '<path d="M12 2C6.5 2 2 6.5 2 12c0 1.8.5 3.5 1.3 5L2 22l5.1-1.3c1.4.8 3.1 1.2 4.9 1.2 5.5 0 10-4.5 10-10S17.5 2 12 2zm0 18.2c-1.6 0-3.1-.4-4.4-1.2l-.3-.2-3 .8.8-2.9-.2-.3C4 15 3.6 13.5 3.6 12 3.6 7.4 7.4 3.6 12 3.6S20.4 7.4 20.4 12 16.6 20.2 12 20.2z"/></svg>')
TEL = ('<svg viewBox="0 0 24 24" style="width:{s}px;height:{s}px;flex:none" fill="none" stroke="{c}" stroke-width="2.4" '
       'stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>')
TIK = ('<svg viewBox="0 0 24 24" style="width:{s}px;height:{s}px;flex:none"><circle cx="12" cy="12" r="12" fill="{c}"/>'
       '<path d="M6.5 12.5l3.6 3.6L17.5 8.7" fill="none" stroke="{k}" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/></svg>')
TAKAS = ('<svg viewBox="0 0 24 24" style="width:{s}px;height:{s}px;flex:none" fill="none" stroke="{c}" stroke-width="2.4" '
         'stroke-linecap="round" stroke-linejoin="round"><path d="M17 3l4 4-4 4"/><path d="M3 7h18"/><path d="M7 21l-4-4 4-4"/><path d="M21 17H3"/></svg>')

CSS = f"""
@font-face {{ font-family: Bar; src: url("file://{FONTS}/BarlowCond-700.ttf"); font-weight: 700; }}
@font-face {{ font-family: Bar; src: url("file://{FONTS}/BarlowCond-500.ttf"); font-weight: 500; }}
@font-face {{ font-family: Mont; src: url("file://{FONTS}/Montserrat-var.ttf"); font-weight: 100 900; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:{W}px; height:{H}px; overflow:hidden; position:relative; font-family:Mont,sans-serif;
       -webkit-font-smoothing:antialiased; background:{LACI}; color:#fff; }}
.a {{ position:absolute; }}
.bar {{ font-family:Bar,sans-serif; font-weight:700; text-transform:uppercase; line-height:.88; letter-spacing:.005em; }}
.tek {{ white-space:nowrap; }}
.foto {{ position:absolute; left:0; width:{W}px; height:{FOTO_H}px; object-fit:cover; }}
.etiket {{ font-size:15px; font-weight:600; letter-spacing:.3em; color:rgba(255,255,255,.8); }}
.cta {{ display:flex; align-items:center; justify-content:center; gap:22px; background:linear-gradient(180deg,{SARI2},{SARI});
       color:{LACI}; border-radius:999px; box-shadow:0 14px 40px rgba(0,0,0,.35), inset 0 -4px 0 rgba(0,0,0,.12); }}
"""


def ust_logolar(top=58):
    """Sol: MİA PARK OCEAN · Sağ: Müteahhit Tilda İnşaat."""
    return f"""
  <img class="a" src="{F('public','brand','vektor','mia-beyaz.svg')}" style="left:64px;top:{top}px;height:118px;filter:drop-shadow(0 3px 10px rgba(0,0,0,.4))">
  <div class="a" style="right:64px;top:{top + 18}px;text-align:right">
    <div class="etiket tek" style="font-size:14px">MÜTEAHHİT</div>
    <img src="{F('public','brand','vektor','tilda-beyaz.svg')}" style="margin-top:12px;height:50px;filter:drop-shadow(0 3px 10px rgba(0,0,0,.4))">
  </div>"""


def iletisim(top, alt_renk="rgba(255,255,255,.92)"):
    """Sarı ARA butonu + WhatsApp satırı + satıcı."""
    return f"""
  <div class="a cta" style="left:70px;top:{top}px;width:{W - 140}px;height:128px">
    {TEL.format(s=50, c=LACI)}
    <span class="bar tek" style="font-size:44px;letter-spacing:.04em;line-height:1">HEMEN ARA</span>
    <span style="width:3px;height:56px;background:{LACI};opacity:.35"></span>
    <span class="bar tek" style="font-size:82px;line-height:1;letter-spacing:.02em">444 10 58</span>
  </div>
  <div class="a" style="left:0;top:{top + 150}px;width:{W}px;display:flex;align-items:center;justify-content:center;gap:16px;color:{alt_renk}">
    {WA.format(s=44, c="#25d366")}
    <span class="tek" style="font-size:38px;font-weight:700;letter-spacing:.04em">0540 028 00 41</span>
    <span class="tek" style="font-size:22px;font-weight:500;opacity:.75;margin-left:6px">WhatsApp</span>
  </div>
  <div class="a" style="left:0;top:{top + 220}px;width:{W}px;display:flex;align-items:center;justify-content:center;gap:18px;color:rgba(255,255,255,.7)">
    <span class="tek" style="font-size:19px;font-weight:600;letter-spacing:.2em">MIAPARKOCEAN.COM</span>
    <span style="width:1px;height:26px;background:rgba(255,255,255,.4)"></span>
    <span class="tek" style="font-size:15px;font-weight:600;letter-spacing:.2em">TEK YETKİLİ SATICI</span>
    <img src="{F('public','brand','vektor','ocean-beyaz.svg')}" style="height:30px">
  </div>"""


def kosul_chip(ust, alt, genis=300):
    return (f'<div style="width:{genis}px;padding:20px 0 18px;border:2px solid rgba(255,255,255,.85);border-radius:14px;text-align:center">'
            f'<div class="bar tek" style="font-size:62px;color:{SARI}">{ust}</div>'
            f'<div class="bar tek" style="margin-top:8px;font-size:28px;font-weight:500;letter-spacing:.06em">{alt}</div></div>')


def rozet(cap, ic, renk=TURK, aci=-10):
    """Tırtıklı yuvarlak rozet (starburst)."""
    import math
    n, r1, r2 = 28, 50, 46
    pts = " ".join(f"{50 + (r1 if i % 2 == 0 else r2) * math.cos(math.pi * i / n):.2f},"
                   f"{50 + (r1 if i % 2 == 0 else r2) * math.sin(math.pi * i / n):.2f}" for i in range(2 * n))
    return (f'<div style="position:relative;width:{cap}px;height:{cap}px;transform:rotate({aci}deg);filter:drop-shadow(0 16px 30px rgba(0,0,0,.4))">'
            f'<svg viewBox="0 0 100 100" style="position:absolute;inset:0;width:100%;height:100%"><polygon points="{pts}" fill="{renk}"/>'
            f'<circle cx="50" cy="50" r="40" fill="none" stroke="rgba(255,255,255,.7)" stroke-width=".6" stroke-dasharray="1.6 1.2"/></svg>'
            f'<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center">{ic}</div></div>')


def k1_dev_rakam():
    return f"""
  <img class="foto" src="{FOTO('20-giris-gunesli.jpg')}" style="top:-120px">
  <div class="a" style="left:0;top:0;width:{W}px;height:420px;background:linear-gradient(180deg,rgba(4,14,30,.7),rgba(4,14,30,0))"></div>
  {ust_logolar()}
  <div class="a" style="left:54px;top:300px">{rozet(250, f'<div class="bar tek" style="font-size:30px;font-weight:500;letter-spacing:.08em">YÜZDE</div><div class="bar tek" style="font-size:96px;line-height:.85">0</div><div class="bar tek" style="font-size:44px">FAİZ</div>')}</div>

  <div class="a" style="left:0;top:1010px;width:{W}px;height:{H - 1010}px;background:linear-gradient(180deg,{LACI2},{LACI});clip-path:polygon(0 70px,100% 0,100% 100%,0 100%)"></div>
  <div class="a" style="left:0;top:1010px;width:{W}px;height:12px;background:{SARI};clip-path:polygon(0 70px,100% 0,100% 6px,0 76px)"></div>

  <div class="a tek" style="left:70px;top:1112px;font-size:22px;font-weight:700;letter-spacing:.3em;color:{TURK}">İZMİT · MİA BÖLGESİ</div>
  <div class="a bar tek" style="left:64px;top:1150px;font-size:236px;color:{SARI};letter-spacing:-.01em">1 MİLYON TL</div>
  <div class="a bar tek" style="left:68px;top:1362px;font-size:72px">PEŞİNATLA EV SAHİBİ OLUN!</div>
  <div class="a" style="left:70px;top:1446px;width:{W - 140}px;display:flex;justify-content:space-between">
    {kosul_chip('60 AY', 'SABİT TAKSİT', 300)}{kosul_chip('BANKASIZ', 'KREDİSİZ', 300)}{kosul_chip('KEFİLSİZ', 'ARA ÖDEMESİZ', 300)}
  </div>
  <div class="a" style="left:0;top:1588px;width:{W}px;display:flex;align-items:center;justify-content:center;gap:14px">
    {TAKAS.format(s=34, c=TURK)}<span class="bar tek" style="font-size:38px;color:#fff;letter-spacing:.04em">EV &amp; ARAÇ TAKASI KABUL EDİLİR</span>
  </div>
  {iletisim(1650)}
"""


def k2_yok_yok():
    satir = lambda s, t: (f'<div class="tek" style="display:flex;align-items:baseline;gap:22px"><span class="bar" style="font-size:150px">{s}</span>'
                          f'<span class="bar" style="font-size:150px;color:{SARI}">YOK.</span></div>')
    return f"""
  <img class="foto" src="{FOTO('22-uzaktan-teleobjektif.jpg')}" style="top:-30px">
  <div class="a" style="left:0;top:0;width:{W}px;height:1300px;background:linear-gradient(180deg,rgba(6,26,51,.9) 0%,rgba(6,26,51,.6) 55%,rgba(6,26,51,0) 100%)"></div>
  <div class="a" style="left:0;bottom:0;width:{W}px;height:470px;background:linear-gradient(0deg,rgba(6,26,51,.96) 45%,rgba(6,26,51,0))"></div>
  {ust_logolar()}
  <div class="a" style="left:70px;top:270px">
    {satir('BANKA', 0)}{satir('FAİZ', 0)}{satir('KEFİL', 0)}
    <div class="tek" style="margin-top:26px;font-size:40px;font-weight:600;line-height:1.25">Ara ödeme de yok.<br><span style="font-weight:300">Sadece <b style="font-weight:800;color:{SARI}">60 ay sabit taksit.</b></span></div>
  </div>
  <div class="a" style="right:52px;top:740px">{rozet(380, f'<div class="bar tek" style="font-size:40px;font-weight:500;letter-spacing:.06em">SADECE</div><div class="bar tek" style="font-size:110px;line-height:.86">1 MİLYON</div><div class="bar tek" style="font-size:64px">TL PEŞİNAT</div>', renk=TURK, aci=8)}</div>
  <div class="a" style="left:70px;top:1540px;display:flex;align-items:center;gap:14px;background:rgba(23,167,185,.18);border:2px solid {TURK};border-radius:999px;padding:12px 26px">
    {TAKAS.format(s=32, c="#fff")}<span class="bar tek" style="font-size:34px;letter-spacing:.04em">EVİNİZİ / ARACINIZI TAKASA VERİN</span>
  </div>
  {iletisim(1650)}
"""


def k3_kira():
    return f"""
  <img class="foto" src="{FOTO('19-balkon-cay-gunduz.jpg')}" style="top:-40px">
  <div class="a" style="left:0;top:0;width:{W}px;height:760px;background:linear-gradient(180deg,rgba(6,26,51,.88) 0%,rgba(6,26,51,.55) 65%,rgba(6,26,51,0))"></div>
  {ust_logolar()}
  <div class="a" style="left:70px;top:258px">
    <div class="bar tek" style="font-size:118px">KİRAYA DEĞİL,</div>
    <div class="tek" style="margin-top:10px;display:inline-block;background:{SARI};color:{LACI};padding:14px 22px 6px">
      <span class="bar" style="font-size:118px">KENDİ EVİNİZE</span></div>
    <div class="bar tek" style="margin-top:12px;font-size:118px">ÖDEYİN.</div>
  </div>

  <div class="a" style="left:0;top:1360px;width:{W}px;height:{H - 1360}px;background:linear-gradient(180deg,rgba(6,26,51,0),rgba(6,26,51,.9) 22%,{LACI})"></div>
  <div class="a" style="left:70px;top:1392px;width:{W - 140}px;display:flex;align-items:flex-end;justify-content:space-between">
    <div>
      <div class="bar tek" style="font-size:118px;color:{SARI};line-height:.85">1 MİLYON TL</div>
      <div class="bar tek" style="margin-top:6px;font-size:46px">PEŞİNAT + 60 AY SABİT TAKSİT</div>
    </div>
  </div>
  <div class="a" style="left:70px;top:1590px;width:{W - 140}px;display:flex;justify-content:space-between;font-size:27px;font-weight:700">
    {''.join(f'<span class="tek" style="display:flex;align-items:center;gap:9px">{TIK.format(s=30, c=TURK, k="#fff")}{m}</span>' for m in ["Faizsiz", "Bankasız", "Kefilsiz", "Ev & araç takası"])}
  </div>
  {iletisim(1650)}
"""


def k4_takas():
    return f"""
  <img class="foto" src="{FOTO('21-yoldan-gunesli.jpg')}" style="top:0">
  <div class="a" style="left:0;top:0;width:{W}px;height:900px;background:linear-gradient(180deg,rgba(6,26,51,.9) 0%,rgba(6,26,51,.7) 60%,rgba(6,26,51,0))"></div>
  {ust_logolar()}
  <div class="a" style="left:70px;top:262px">
    <div class="bar tek" style="font-size:140px">ARABANIZ</div>
    <div class="bar tek" style="font-size:140px;color:{SARI}">PEŞİNATINIZ</div>
    <div class="bar tek" style="font-size:140px">OLSUN!</div>
    <div class="tek" style="margin-top:28px;font-size:36px;font-weight:500;line-height:1.3">Ev ve araç takasıyla<br><b style="font-weight:800">MİA PARK OCEAN'da ev sahibi olun.</b></div>
  </div>
  <div class="a" style="right:56px;top:700px">{rozet(300, f'<div class="bar tek" style="font-size:72px;line-height:.85">TAKAS</div><div class="bar tek" style="font-size:40px;font-weight:500;letter-spacing:.04em">KABUL</div><div class="bar tek" style="font-size:40px;font-weight:500;letter-spacing:.04em">EDİLİR</div>', renk=TURK, aci=-8)}</div>

  <div class="a" style="left:0;top:1380px;width:{W}px;height:{H - 1380}px;background:linear-gradient(180deg,rgba(6,26,51,0),rgba(6,26,51,.92) 20%,{LACI})"></div>
  <div class="a" style="left:70px;top:1470px;width:{W - 140}px;display:flex;align-items:center;justify-content:space-between">
    <div class="bar tek" style="font-size:96px;color:{SARI};line-height:.85">1 MİLYON TL<span style="font-size:52px;color:#fff;font-weight:500"> PEŞİNAT</span></div>
  </div>
  <div class="a" style="left:70px;top:1574px;width:{W - 140}px;display:flex;justify-content:space-between;font-size:27px;font-weight:700">
    {''.join(f'<span class="tek" style="display:flex;align-items:center;gap:9px">{TIK.format(s=30, c=TURK, k="#fff")}{m}</span>' for m in ["60 ay sabit taksit", "Faizsiz", "Bankasız", "Kefilsiz"])}
  </div>
  {iletisim(1650)}
"""


KONSEPTLER = [("1-dev-rakam", k1_dev_rakam), ("2-yok-yok", k2_yok_yok), ("3-kira", k3_kira), ("4-takas", k4_takas)]


def main():
    os.makedirs(OUT, exist_ok=True)
    gecici = tempfile.mkdtemp(prefix="vurucu-")
    isler = []
    for ad, fn in KONSEPTLER:
        hp = os.path.join(gecici, ad + ".html")
        open(hp, "w", encoding="utf-8").write(
            f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{fn()}</body></html>')
        isler.append(dict(html=hp, w=W, h=H, dsf=2, dilim=W, cikti=os.path.join(gecici, ad), ad=ad))
    jp = os.path.join(gecici, "isler.json")
    json.dump(isler, open(jp, "w"))
    npm = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    subprocess.run(["node", os.path.join(ROOT, "scripts", "mega-bilbord", "render.cjs"), jp], check=True,
                   env={**os.environ, "NODE_PATH": npm}, stdout=subprocess.DEVNULL)
    for is_ in isler:
        im = Image.open(json.load(open(is_["cikti"] + ".json"))[0]).convert("RGB")
        yol = os.path.join(OUT, f"mia-story-{is_['ad']}.jpg")
        im.save(yol, quality=93)
        print("  →", os.path.relpath(yol, ROOT), im.size)


if __name__ == "__main__":
    main()
