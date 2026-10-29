#!/usr/bin/env python3
"""
Referans tarzı satış reklamları (story 1080x1920, 2x çizilir).

Üç şablon:
  · sunucu  — beyaz üst, büyük başlık, lacivert/altın fiyat kartı, kırmızı "yok" etiketi,
              kesilmiş sunucu/aile fotoğrafı + proje render'ı, lacivert alt bant
  · ic      — krem zemin, iç mekân görseli, iki parçalı fiyat hapı, üç özellik
  · gece    — gece render'ı, küçük harfli başlık, cam üç sütunlu fiyat bandı

Metin: 1 Milyon TL peşinat · 60 ay sabit taksit · banka/faiz/ara ödeme yok.
İletişim: 444 10 58 · WhatsApp 0540 028 00 41. Logolar: Tilda İnşaat + MİA PARK OCEAN.

    python3.13 scripts/build-reklam-referans.py
"""

import json
import os
import subprocess
import tempfile

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "sosyal-medya", "reklam-referans")
FONT = os.path.join(ROOT, "brand-source", "fonts", "Montserrat-var.ttf")
W, H = 1080, 1920
F = lambda *p: "file://" + os.path.join(ROOT, *p)

LACI, ALTIN, KIRMIZI = "#14306b", "#c9a24a", "#e1262f"
TEAL, KREM, KAHVE = "#0c4658", "#efe5d6", "#7a5a43"

WA = ('<svg viewBox="0 0 24 24" style="width:{s}px;height:{s}px;fill:{c};flex:none">'
      '<path d="M17.5 14.4c-.3-.2-1.7-.8-2-.9-.3-.1-.5-.2-.7.2-.2.3-.7.9-.9 1.1-.2.2-.3.2-.6.1-.3-.2-1.2-.5-2.3-1.4-.9-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6.1-.1.3-.3.4-.5.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5 0-.1-.7-1.6-.9-2.2-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.4s1.1 2.8 1.2 3c.2.2 2.1 3.2 5 4.5.7.3 1.2.5 1.7.6.7.2 1.3.2 1.8.1.6-.1 1.7-.7 1.9-1.3.2-.7.2-1.2.2-1.3-.1-.2-.3-.3-.6-.4z"/>'
      '<path d="M12 2C6.5 2 2 6.5 2 12c0 1.8.5 3.5 1.3 5L2 22l5.1-1.3c1.4.8 3.1 1.2 4.9 1.2 5.5 0 10-4.5 10-10S17.5 2 12 2zm0 18.2c-1.6 0-3.1-.4-4.4-1.2l-.3-.2-3 .8.8-2.9-.2-.3C4 15 3.6 13.5 3.6 12 3.6 7.4 7.4 3.6 12 3.6S20.4 7.4 20.4 12 16.6 20.2 12 20.2z"/></svg>')

IKON = {
    "havuz": '<path d="M2 18c2 0 2-1.5 4-1.5S8 18 10 18s2-1.5 4-1.5 2 1.5 4 1.5 2-1.5 4-1.5"/><path d="M2 22c2 0 2-1.5 4-1.5S8 22 10 22s2-1.5 4-1.5 2 1.5 4 1.5 2-1.5 4-1.5"/><path d="M8 15V5a2 2 0 0 1 4 0"/><path d="M16 15V5a2 2 0 0 0-4 0"/><path d="M8 9h8"/>',
    "otopark": '<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M9 17V7h4a3 3 0 0 1 0 6H9"/>',
    "park": '<path d="M12 22v-7"/><path d="M8 22h8"/><circle cx="12" cy="8" r="6"/>',
    "bahce": '<path d="M7 20h10"/><path d="M12 20V10"/><path d="M12 10c0-4 3-6 7-6 0 4-3 6-7 6z"/><path d="M12 13c0-3-2-5-6-5 0 3 2 5 6 5z"/>',
}

CSS = f"""
@font-face {{ font-family: Jost; src: url("file://{os.path.join(ROOT, "brand-source", "fonts", "Jost-var.ttf")}"); font-weight: 100 900; }}
@font-face {{ font-family: Mont; src: url("file://{FONT}"); font-weight: 100 900; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:{W}px; height:{H}px; overflow:hidden; position:relative; font-family:Mont,sans-serif;
       -webkit-font-smoothing:antialiased; background:#fff; }}
.a {{ position:absolute; }}
.tek {{ white-space:nowrap; }}
.m {{ left:0; width:{W}px; text-align:center; }}
.k {{ font-weight:800; letter-spacing:-.02em; line-height:1; }}
"""


def alt_bant(top=1470):
    """Lacivert alt bant: logolar + 444 10 58 + WhatsApp."""
    return f"""
  <div class="a" style="left:0;top:{top}px;width:{W}px;height:{H - top}px;background:linear-gradient(180deg,rgba(20,48,107,0) 0%,rgba(20,48,107,.88) 34%,{LACI} 62%)"></div>
  <div class="a m" style="top:1626px;display:flex;align-items:center;justify-content:center;gap:38px">
    <img src="{F('public','brand','vektor','tilda-beyaz.svg')}" style="height:72px">
    <span style="width:2px;height:96px;background:rgba(255,255,255,.55)"></span>
    <img src="{F('public','brand','vektor','mia-beyaz.svg')}" style="height:104px">
  </div>
  <div class="a m k tek" style="top:1756px;font-size:86px;color:#fff;letter-spacing:.01em">444 10 58</div>
  <div class="a m" style="top:1858px;display:flex;align-items:center;justify-content:center;gap:12px;color:#fff">
    {WA.format(s=34, c="#25d366")}<span class="tek" style="font-size:32px;font-weight:700;letter-spacing:.04em">0540 028 00 41</span>
  </div>"""


def sunucu(render, pos, insan, insan_stil, b1, b2, b3, kart1, kart1k, kart2, hap1, hap2, kart_left=395):
    """Referans 2: üstte başlık, ortada render + insan, sağda kart."""
    return f"""
  <img class="a" src="{render}" style="left:0;top:420px;width:{W}px;height:1300px;object-fit:cover;object-position:{pos};
       -webkit-mask-image:linear-gradient(180deg,transparent 0%,#000 30%)">
  <div class="a" style="left:0;top:1700px;width:{W}px;height:220px;background:{LACI}"></div>
  <div class="a" style="left:0;top:0;width:{W}px;height:900px;background:linear-gradient(180deg,#fff 52%,rgba(255,255,255,0))"></div>

  <div class="a m k tek" style="top:132px;font-size:76px;color:{LACI}">{b1}</div>
  <div class="a m k tek" style="top:226px;font-size:128px;color:{ALTIN}">{b2}</div>
  <div class="a m k tek" style="top:370px;font-size:76px;color:{LACI}">{b3}</div>
  <div class="a m tek" style="top:478px;font-size:29px;font-weight:600;letter-spacing:.2em;color:#4a5878">MİA PARK OCEAN · İZMİT</div>

  <img class="a" src="{insan}" style="{insan_stil};filter:drop-shadow(0 20px 30px rgba(10,30,60,.25))">

  <div class="a" style="left:{kart_left}px;top:610px;width:560px;border-radius:26px;overflow:hidden;box-shadow:0 24px 50px rgba(10,30,70,.35)">
    <div style="background:{LACI};padding:30px 0 24px;text-align:center;color:#fff">
      <div class="k tek" style="font-size:80px">{kart1}</div>
      <div class="tek" style="margin-top:10px;font-size:32px;font-weight:800;letter-spacing:.04em">{kart1k}</div>
    </div>
    <div style="height:6px;background:#fff"></div>
    <div class="k tek" style="background:{ALTIN};padding:26px 0 24px;text-align:center;font-size:52px;color:{LACI}">{kart2}</div>
  </div>
  <div class="a" style="left:{kart_left + 70}px;top:942px;width:420px;padding:22px 0;border-radius:24px;background:{KIRMIZI};
       color:#fff;text-align:center;font-size:33px;font-weight:800;line-height:1.25;box-shadow:0 16px 34px rgba(225,38,47,.35)">{hap1}<br>{hap2}</div>
  {alt_bant()}
"""


def ic(foto, b1, b2, a1, a2, sol_ust, sol_buyuk, sol_alt, sag1, sag2, ozellikler):
    """Referans 1: krem zemin, iç mekân, iki parçalı fiyat hapı."""
    oz = "".join(
        f'<div style="width:300px;text-align:center"><svg viewBox="0 0 24 24" style="width:58px;height:58px" fill="none" '
        f'stroke="{TEAL}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{IKON[i]}</svg>'
        f'<div style="margin-top:12px;font-size:30px;font-weight:600;color:#2b3a40;line-height:1.2">{t}</div></div>'
        for i, t in ozellikler)
    return f"""
  <div class="a" style="left:0;top:0;width:{W}px;height:{H}px;background:#f7f3ed"></div>
  <img class="a" src="{foto}" style="left:0;top:470px;width:{W}px;height:880px;object-fit:cover;
       -webkit-mask-image:linear-gradient(180deg,transparent 0%,#000 22%,#000 78%,transparent 100%)">

  <div class="a k tek" style="left:76px;top:118px;font-size:98px;color:{TEAL}">{b1}</div>
  <div class="a k tek" style="left:76px;top:222px;font-size:98px;color:{TEAL}">{b2}</div>
  <div class="a tek" style="left:80px;top:344px;font-size:56px;font-weight:600;color:{KAHVE};line-height:1.12">{a1}<br>{a2}</div>

  <div class="a" style="left:70px;top:1196px;width:940px;height:200px;display:flex;align-items:stretch">
    <div style="flex:1;background:linear-gradient(135deg,#0f5a6f,{TEAL});border-radius:100px 0 0 100px;color:#fff;padding:26px 0 0 70px;
         box-shadow:0 22px 40px rgba(12,70,88,.3)">
      <div class="tek" style="font-size:28px;font-weight:700;letter-spacing:.14em">{sol_ust}</div>
      <div class="k tek" style="margin-top:8px;font-size:84px">{sol_buyuk}</div>
      <div class="tek" style="margin-top:6px;font-size:30px;font-weight:800;letter-spacing:.08em;padding-left:250px">{sol_alt}</div>
    </div>
    <div style="width:300px;margin-left:-40px;background:{KREM};border-radius:100px;display:flex;flex-direction:column;align-items:center;
         justify-content:center;box-shadow:0 22px 40px rgba(60,40,20,.22);border:4px solid #fff">
      <div class="k tek" style="font-size:60px;color:#1e2a2e">{sag1}</div>
      <div style="width:150px;height:2px;background:rgba(30,42,46,.35);margin:10px 0"></div>
      <div class="k tek" style="font-size:44px;color:#1e2a2e">{sag2}</div>
    </div>
  </div>

  <div class="a" style="left:90px;top:1446px;width:900px;display:flex;justify-content:space-between">{oz}</div>

  <div class="a m" style="top:1636px;display:flex;align-items:center;justify-content:center;gap:34px">
    <img src="{F('public','brand','vektor','tilda.svg')}" style="height:58px">
    <span style="width:2px;height:80px;background:rgba(12,70,88,.3)"></span>
    <img src="{F('public','brand','vektor','mia-lacivert.svg')}" style="height:92px">
  </div>
  <div class="a m" style="top:1758px;display:flex;align-items:center;justify-content:center;gap:28px">
    <span class="k tek" style="font-size:70px;color:{TEAL}">444 10 58</span>
    <span style="width:2px;height:54px;background:rgba(12,70,88,.3)"></span>
    <span class="tek" style="display:flex;align-items:center;gap:10px;font-size:34px;font-weight:700;color:#2b3a40">{WA.format(s=38, c="#25d366")}0540 028 00 41</span>
  </div>
"""


def gece():
    """Referans 3: gece render'ı, küçük harfli başlık, cam üç sütunlu fiyat bandı."""
    sutun = lambda ust, alt: (f'<div style="flex:1;text-align:center"><div class="tek" style="font-family:Jost;font-size:58px;font-weight:700;'
                              f'line-height:1;letter-spacing:-.01em">{ust}</div><div class="tek" style="margin-top:10px;font-family:Jost;'
                              f'font-size:30px;font-weight:400;letter-spacing:.04em">{alt}</div></div>')
    cizgi = '<span style="width:2px;height:96px;background:rgba(255,255,255,.4);align-self:center"></span>'
    return f"""
  <div class="a" style="left:0;top:0;width:{W}px;height:{H}px;background:#050b1a"></div>
  <img class="a" src="file://{os.path.join(S4K, 'night-gate-temiz.jpg')}" style="left:0;top:300px;width:{W}px;height:1620px;object-fit:cover;object-position:50% 50%;
       -webkit-mask-image:linear-gradient(180deg,transparent 0%,#000 14%)">
  <div class="a" style="left:0;top:0;width:{W}px;height:{H}px;background:radial-gradient(1.6px 1.6px at 12% 9%,#fff8,transparent),radial-gradient(1.4px 1.4px at 78% 6%,#fff8,transparent),radial-gradient(1.2px 1.2px at 55% 14%,#fff6,transparent),radial-gradient(1.6px 1.6px at 30% 19%,#fff6,transparent),radial-gradient(1.2px 1.2px at 90% 21%,#fff7,transparent),radial-gradient(1.4px 1.4px at 6% 27%,#fff5,transparent)"></div>
  <div class="a" style="left:0;top:1420px;width:{W}px;height:500px;background:linear-gradient(180deg,rgba(5,11,26,0),rgba(5,11,26,.92) 45%,#050b1a)"></div>

  <img class="a" src="{F('public','brand','vektor','mia-beyaz.svg')}" style="left:64px;top:62px;height:104px">
  <div class="a" style="right:64px;top:78px;text-align:right">
    <div class="tek" style="font-size:13px;font-weight:600;letter-spacing:.3em;color:rgba(255,255,255,.7)">MÜTEAHHİT</div>
    <img src="{F('public','brand','vektor','tilda-beyaz.svg')}" style="margin-top:10px;height:46px"></div>

  <div class="a tek" style="left:76px;top:262px;font-family:Jost;font-size:88px;font-weight:400;color:#fff;line-height:1.05;letter-spacing:-.01em">
    bankasız ve faizsiz<br><b style="font-weight:700">ev sahibi <span style="color:#ffd43b">olun</span></b></div>

  <div class="a" style="left:56px;top:510px;width:968px;padding:26px 30px 30px;border-radius:70px;border:3px solid rgba(255,255,255,.55);
       background:linear-gradient(180deg,rgba(255,255,255,.14),rgba(255,255,255,.04));-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);
       box-shadow:0 20px 50px rgba(0,0,0,.45), inset 0 1px 0 rgba(255,255,255,.35);color:#fff">
    <div class="tek" style="text-align:center;font-family:Jost;font-size:26px;font-weight:400;color:rgba(255,255,255,.85)">MİA PARK OCEAN · İzmit MİA Bölgesi</div>
    <div style="margin-top:16px;display:flex">{sutun('₺1.000.000', 'PEŞİNAT')}{cizgi}{sutun('60 AY', 'SABİT TAKSİT')}{cizgi}{sutun('%0', 'FAİZ')}</div>
  </div>

  <div class="a m tek" style="top:1660px;font-family:Jost;font-size:30px;font-weight:500;letter-spacing:.2em;color:rgba(255,255,255,.8)">HEMEN ARAYIN</div>
  <div class="a m tek" style="top:1706px;font-family:Jost;font-size:110px;font-weight:700;color:#fff;line-height:1">444 10 58</div>
  <div class="a m" style="top:1838px;display:flex;align-items:center;justify-content:center;gap:12px;color:#fff">
    {WA.format(s=36, c="#25d366")}<span class="tek" style="font-family:Jost;font-size:36px;font-weight:600;letter-spacing:.03em">0540 028 00 41</span></div>
"""


AILE = os.path.join(ROOT, "signage-source", "aile")
S4K = os.path.join(ROOT, "signage-source")
IC = lambda ad: F("public", "images", "ic-mekan", ad)

GORSELLER = [
    ("1-sunucu-ilk-evine", sunucu(
        "file://" + os.path.join(S4K, "entrance-gate.jpg"), "13% 50%",
        "file://" + os.path.join(AILE, "sunucu2-kesik.png"), "left:-70px;top:600px;height:1320px",
        "İlk Evine", "1 MİLYON TL", "Peşinat ile Sahip Ol",
        "1 MİLYON TL", "PEŞİNAT", "60 AY SABİT TAKSİT", "BANKA YOK", "ARA ÖDEME YOK")),
    ("2-sunucu-kiraciliga-son", sunucu(
        "file://" + os.path.join(S4K, "4k", "orta-giris-genis-8k.png"), "11% 50%",
        "file://" + os.path.join(AILE, "sunucu-kesik.png"), "left:-40px;top:590px;height:1330px",
        "Kiracılığa Son!", "EV SAHİBİ OL", "1 Milyon TL Peşinatla",
        "%0 FAİZ", "BANKASIZ · KEFİLSİZ", "60 AY SABİT TAKSİT", "ARA ÖDEME YOK", "KREDİ YOK")),
    ("3-aile-yeni-yuva", sunucu(
        "file://" + os.path.join(S4K, "courtyard-pools.jpg"), "50% 50%",
        "file://" + os.path.join(AILE, "aile2-kesik.png"), "left:-30px;top:1010px;height:700px",
        "Ailenize", "YENİ BİR YUVA", "1 Milyon TL Peşinatla",
        "1 MİLYON TL", "PEŞİNAT", "60 AY SABİT TAKSİT", "BANKA YOK", "FAİZ YOK", kart_left=470)),
    ("4-ic-yeni-nesil-1-1", ic(
        IC("05-1plus1-salon.webp"), "İZMİT", "MİA PARK OCEAN", "YENİ NESİL 1+1", "MODERN YAŞAM",
        "SADECE", "1 MİLYON TL", "PEŞİNAT", "60 AY", "0 FAİZ",
        [("havuz", "Süs<br>Havuzları"), ("otopark", "Kapalı<br>Otopark"), ("park", "Çocuk<br>Parkı")])),
    ("5-ic-bahce-loft", ic(
        IC("09-loft-salon.webp"), "İZMİT", "MİA PARK OCEAN", "BAHÇELİ 1+1 LOFT", "AYRICALIKLI YAŞAM",
        "SADECE", "1 MİLYON TL", "PEŞİNAT", "60 AY", "SABİT",
        [("bahce", "Özel<br>Bahçe"), ("havuz", "Süs<br>Havuzları"), ("otopark", "Kapalı<br>Otopark")])),
    ("6-gece-cam-bant", gece()),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    gecici = tempfile.mkdtemp(prefix="referans-")
    isler = []
    for ad, govde in GORSELLER:
        hp = os.path.join(gecici, ad + ".html")
        open(hp, "w", encoding="utf-8").write(
            f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{govde}</body></html>')
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
