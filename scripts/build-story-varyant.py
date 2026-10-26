#!/usr/bin/env python3
"""
"İlk evine 1 milyon TL peşinat" story'sinin sürümleri (1080x1920 → 2160x3840).
Arka plan fotoğrafı: bitmiş proje, yol tarafından (sosyal-medya/bitmis-fotograflar/21-yoldan-gunesli.jpg).

  1-klasik      : beyaz-mavi üst alan, altta fotoğraf (orijinal düzen)
  2-tam-foto    : tüm arka plan fotoğraf, üstte beyaz perde
  3-lacivert    : lacivert üst alan, beyaz-altın yazılar, altta fotoğraf
  4-cerceveli   : tam fotoğraf, ince çerçeve, buzlu cam paneller (kurumsal reklam setiyle aynı dil)

    python3.13 scripts/build-story-varyant.py
"""

import json
import os
import subprocess
import tempfile

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "sosyal-medya", "story-pesinat")
FONT = os.path.join(ROOT, "brand-source", "fonts", "Montserrat-var.ttf")
W, H = 1080, 1920
LAC, LAC2, ALTIN, ALTIN2, KIR = "#0f2a5a", "#17407f", "#c9a24a", "#e3c27a", "#e3262e"
F = lambda *p: "file://" + os.path.join(ROOT, *p)
FOTO = F("sosyal-medya", "bitmis-fotograflar", "21-yoldan-gunesli.jpg")
SUNUCU = F("signage-source", "aile", "sunucu2-kesik.png")
S_H = 1150
S_W = round(S_H * 1051 / 2205)

CSS = f"""
@font-face {{ font-family: Mont; src: url("file://{FONT}"); font-weight: 100 900; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:{W}px; height:{H}px; overflow:hidden; position:relative; font-family:Mont,sans-serif;
       -webkit-font-smoothing:antialiased; background:#fff; }}
.a {{ position:absolute; }}
.tek {{ white-space:nowrap; line-height:1; }}
.orta {{ left:0; width:{W}px; text-align:center; }}
.rozet {{ left:61%; transform:translateX(-50%); text-align:center; font-weight:800; color:#fff; box-shadow:0 16px 34px rgba(0,0,0,.22); }}
.cam {{ background:rgba(10,26,56,.58); -webkit-backdrop-filter:blur(14px); backdrop-filter:blur(14px);
       border:1px solid rgba(227,194,122,.6); border-radius:6px; }}
"""


def sunucu(top=620, golge=True):
    return (f'<img class="a" src="{SUNUCU}" style="left:-70px;top:{top}px;width:{S_W}px;height:{S_H}px;'
            f'{"filter:drop-shadow(0 24px 34px rgba(0,0,0,.35));" if golge else ""}'
            f'-webkit-mask-image:linear-gradient(180deg,#000 82%,transparent 100%)">')


def rozetler(ust=600, ust_renk=(LAC2, LAC), ust_yazi="#fff", alt_yazi=None):
    alt_yazi = alt_yazi or LAC
    return f"""
  <div class="a rozet" style="top:{ust}px;width:540px;background:linear-gradient(180deg,{ust_renk[0]},{ust_renk[1]});color:{ust_yazi};border-radius:34px 34px 0 0;padding:26px 0 22px">
    <div class="tek" style="font-size:72px;letter-spacing:-.02em">1 MİLYON<span style="font-size:.5em;margin-left:10px">TL</span></div>
    <div class="tek" style="font-size:30px;margin-top:10px;letter-spacing:.06em">PEŞİNATLA</div>
  </div>
  <div class="a rozet" style="top:{ust + 166}px;width:540px;background:{ALTIN};color:{LAC};border-radius:0 0 34px 34px;padding:22px 0 24px">
    <div class="tek" style="font-size:62px;letter-spacing:.01em">60 AY VADE</div>
  </div>
  <div class="a rozet" style="top:{ust + 300}px;width:420px;background:{KIR};border-radius:30px;padding:20px 0">
    <div class="tek" style="font-size:30px;letter-spacing:.06em">BANKA YOK</div>
    <div class="tek" style="font-size:30px;margin-top:8px;letter-spacing:.06em">ARA ÖDEME YOK</div>
  </div>
  <div class="a tek" style="left:61%;transform:translateX(-50%);top:{ust + 435}px;font-size:30px;font-weight:700;color:{alt_yazi};letter-spacing:.06em">EV &amp; ARAÇ TAKASINA AÇIK</div>"""


def baslik(top=170, ana=LAC, vurgu=ALTIN, alt="#5a6b85", golge=""):
    return f"""
  <div class="a tek orta" style="top:{top}px;font-size:70px;font-weight:800;color:{ana};letter-spacing:-.01em;{golge}">İlk Evine</div>
  <div class="a tek orta" style="top:{top + 88}px;font-size:112px;font-weight:800;color:{vurgu};letter-spacing:-.02em;{golge}">1 MİLYON TL</div>
  <div class="a tek orta" style="top:{top + 218}px;font-size:70px;font-weight:800;color:{ana};letter-spacing:-.01em;{golge}">Peşinat ile Sahip Ol</div>
  <div class="a tek orta" style="top:{top + 308}px;font-size:30px;font-weight:600;color:{alt};letter-spacing:.2em;{golge}">MİA PARK OCEAN · İZMİT</div>"""


def alt_bant(siteler=False):
    s = ("444 10 58 &nbsp;·&nbsp; miaparkocean.com" if not siteler else
         "444 10 58")
    ek = ("" if not siteler else
          f'<div class="a tek orta" style="top:1868px;font-size:24px;font-weight:600;color:rgba(255,255,255,.9);letter-spacing:.12em">miaparkocean.com &nbsp;|&nbsp; tildainsaat.com</div>')
    return f"""
  <div class="a" style="left:0;top:{1710 if not siteler else 1680}px;width:{W}px;display:flex;align-items:center;justify-content:center;gap:46px">
    <img src="{F('public','brand','vektor','tilda-beyaz.svg')}" style="height:84px">
    <div style="width:3px;height:90px;background:rgba(255,255,255,.45)"></div>
    <img src="{F('public','brand','logo-mia-2026.png')}" style="height:112px;filter:brightness(0) invert(1)">
  </div>
  <div class="a tek orta" style="top:{1840 if not siteler else 1800}px;font-size:{40 if not siteler else 54}px;font-weight:800;color:#fff;letter-spacing:.04em">{s}</div>{ek}"""


def foto_alt(top, h, pos="50% 38%", ust_renk="207,227,244"):
    return f"""
  <div class="a" style="left:0;top:{top}px;width:{W}px;height:{h}px;overflow:hidden">
    <img src="{FOTO}" style="width:{W}px;height:{h}px;object-fit:cover;object-position:{pos}">
    <div class="a" style="left:0;top:0;width:{W}px;height:240px;background:linear-gradient(180deg,rgb({ust_renk}),rgba({ust_renk},0))"></div>
    <div class="a" style="left:0;bottom:0;width:{W}px;height:300px;background:linear-gradient(0deg,rgba(15,42,90,.94) 0%,rgba(15,42,90,.6) 55%,rgba(15,42,90,0) 100%)"></div>
  </div>"""


def v1():
    return f"""
  <div class="a" style="inset:0;background:linear-gradient(180deg,#ffffff 0%,#f4f7fb 30%,#e6eef8 50%,#d7e7f6 62%,#cfe3f4 66%)"></div>
  {foto_alt(1000, 920)}
  {baslik()}
  {rozetler()}
  {sunucu()}
  {alt_bant(siteler=True)}"""


def v2():
    return f"""
  <div class="a" style="inset:0;background:linear-gradient(180deg,#ffffff 0%,#eef4fb 40%,#cfe3f4 70%)"></div>
  <img class="a" src="{FOTO}" style="left:0;top:470px;width:{W}px;height:{round(W * 2752 / 1536)}px;-webkit-mask-image:linear-gradient(180deg,transparent 0,#000 22%)">
  <div class="a" style="left:0;top:0;width:{W}px;height:1000px;background:linear-gradient(180deg,rgba(255,255,255,.96) 0%,rgba(255,255,255,.88) 45%,rgba(255,255,255,0) 100%)"></div>
  <div class="a" style="left:0;bottom:0;width:{W}px;height:420px;background:linear-gradient(0deg,rgba(15,42,90,.95) 0%,rgba(15,42,90,.7) 50%,rgba(15,42,90,0) 100%)"></div>
  {baslik()}
  {rozetler(alt_yazi=LAC)}
  {sunucu()}
  {alt_bant(siteler=True)}"""


def v3():
    return f"""
  <div class="a" style="inset:0;background:radial-gradient(120% 70% at 50% 0%,#1d4f95 0%,{LAC} 55%,#0a1c3d 100%)"></div>
  {foto_alt(980, 940, ust_renk="15,42,90")}
  {baslik(ana="#fff", vurgu=ALTIN2, alt="rgba(255,255,255,.75)")}
  {rozetler(ust_renk=("#ffffff", "#eef3fa"), ust_yazi=LAC, alt_yazi="#fff")}
  {sunucu()}
  {alt_bant(siteler=True)}"""


def v4():
    koseler = "".join(
        f'<div class="a" style="{p};width:44px;height:44px;border-color:{ALTIN2};border-style:solid;border-width:{b}"></div>'
        for p, b in [("left:26px;top:26px", "3px 0 0 3px"), ("right:26px;top:26px", "3px 3px 0 0"),
                     ("left:26px;bottom:26px", "0 0 3px 3px"), ("right:26px;bottom:26px", "0 3px 3px 0")])
    tik = (f'<svg viewBox="0 0 24 24" style="width:28px;height:28px;flex:none"><circle cx="12" cy="12" r="11" fill="none" '
           f'stroke="{ALTIN2}" stroke-width="1.6"/><path d="M7 12.5l3.2 3.2L17 9" fill="none" stroke="{ALTIN2}" '
           f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>')
    madde = lambda m: f'<div style="display:flex;align-items:center;gap:14px">{tik}<span>{m}</span></div>'
    return f"""
  <div class="a" style="inset:0;background:linear-gradient(180deg,#5d86b8 0%,#9cbfe0 45%,#cfe1f1 75%)"></div>
  <img class="a" src="{FOTO}" style="left:0;top:430px;width:{W}px;height:{round(W * 2752 / 1536)}px;-webkit-mask-image:linear-gradient(180deg,transparent 0,#000 20%)">
  <div class="a" style="left:0;top:0;width:{W}px;height:700px;background:linear-gradient(180deg,rgba(6,16,36,.6),rgba(6,16,36,0))"></div>
  <div class="a" style="left:0;bottom:0;width:{W}px;height:820px;background:linear-gradient(0deg,rgba(6,16,36,.88),rgba(6,16,36,0))"></div>
  <div class="a" style="left:34px;top:34px;width:{W - 68}px;height:{H - 68}px;border:1.5px solid rgba(255,255,255,.82)"></div>
  {koseler}
  <div class="a cam" style="left:96px;top:110px;width:888px;padding:34px 40px 36px;text-align:center;color:#fff">
    <div class="tek" style="font-size:22px;font-weight:600;letter-spacing:.32em;color:{ALTIN2}">MİA PARK OCEAN · İZMİT</div>
    <div class="tek" style="margin-top:22px;font-size:48px;font-weight:300">İlk evinize</div>
    <div class="tek" style="margin-top:10px;font-size:92px;font-weight:800;color:{ALTIN2};letter-spacing:-.01em">1 MİLYON TL</div>
    <div class="tek" style="margin-top:12px;font-size:48px;font-weight:700">peşinat ile sahip olun.</div>
  </div>
  <img class="a" src="{SUNUCU}" style="left:-60px;top:640px;width:{round(1000 * 1051 / 2205)}px;height:1000px;filter:drop-shadow(0 24px 34px rgba(0,0,0,.4));-webkit-mask-image:linear-gradient(180deg,#000 80%,transparent 100%)">
  <div class="a cam" style="left:480px;top:700px;width:504px;padding:30px 34px 28px;color:#fff">
    <div class="tek" style="font-size:20px;font-weight:600;letter-spacing:.3em;color:{ALTIN2}">ÖDEME KOŞULLARI</div>
    <div style="margin-top:22px;display:flex;flex-direction:column;gap:18px;font-size:30px;font-weight:500;line-height:1">
      {madde("60 ay vade")}{madde("Banka yok")}{madde("Kefil yok")}{madde("Ara ödeme yok")}
    </div>
    <div style="margin:24px 0 0;width:90px;height:1px;background:{ALTIN2}"></div>
    <div class="tek" style="margin-top:20px;font-size:22px;font-weight:600;letter-spacing:.12em;color:rgba(255,255,255,.85)">TAKAS İMKÂNI</div>
    <div class="tek" style="margin-top:10px;font-size:34px;font-weight:700;color:{ALTIN2};line-height:1.15">Ev &amp; araç<br>takasına açıktır.</div>
  </div>
  {alt_bant(siteler=True)}"""


VARYANTLAR = [("1-klasik", v1), ("2-tam-foto", v2), ("3-lacivert", v3), ("4-cerceveli", v4)]


def main():
    os.makedirs(OUT, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="storyv-")
    isler = []
    for ad, fn in VARYANTLAR:
        hp = os.path.join(tmp, ad + ".html")
        open(hp, "w", encoding="utf-8").write(
            f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{fn()}</body></html>')
        isler.append(dict(html=hp, w=W, h=H, dsf=2, dilim=W, cikti=os.path.join(tmp, ad), ad=ad))
    jp = os.path.join(tmp, "isler.json")
    json.dump(isler, open(jp, "w"))
    npm = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    subprocess.run(["node", os.path.join(ROOT, "scripts", "mega-bilbord", "render.cjs"), jp], check=True,
                   env={**os.environ, "NODE_PATH": npm}, stdout=subprocess.DEVNULL)
    for is_ in isler:
        im = Image.open(json.load(open(is_["cikti"] + ".json"))[0]).convert("RGB")
        yol = os.path.join(OUT, f"story-pesinat-{is_['ad']}.jpg")
        im.save(yol, quality=93)
        print("  →", os.path.relpath(yol, ROOT), im.size)


if __name__ == "__main__":
    main()
