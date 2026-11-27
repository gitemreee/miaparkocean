#!/usr/bin/env python3
"""
Instagram akış gönderileri (4:5, 1080x1350) — onaylı "Yeni Bir Yuva" reklam düzeninin
dili (beyaz üstte üç satır başlık · koyu/altın kart · kırmızı etiket · altta koyu bant),
ama reklam değil bilgi gönderisi: ödeme planı, daire tipleri, konum, sosyal yaşam.

Fiyatlar (Kasım 2026, 60 ay vade farksız):
    1+0  699.000 TL peşinat · ayda 29.900 TL
    1+1  999.000 TL peşinat · ayda 39.900 TL
    2+1  2.000.000 TL peşinat · ayda 50.000 TL

    python3 scripts/build-instagram-post.py
"""

import importlib.util
import json
import os
import subprocess
import sys
import tempfile

from PIL import Image

KOK = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("yy", os.path.join(KOK, "build-reklam-yeni-yuzler.py"))
yy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(yy)

ROOT, F, W, KIRMIZI = yy.ROOT, yy.F, yy.W, yy.KIRMIZI
LACI, PETROL, YESIL = yy.LACI, yy.PETROL, yy.YESIL
OUT = os.path.join(ROOT, "sosyal-medya", "instagram-post")
H = 1350
IMG = lambda ad: F("public", "images", ad)

TIK = ('<svg viewBox="0 0 24 24" style="width:{s}px;height:{s}px;flex:none"><circle cx="12" cy="12" r="12" fill="{c}"/>'
       '<path d="M6.5 12.4l3.6 3.6 7.4-7.6" fill="none" stroke="{k}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def iskelet(m, orta, g_h=None, bant=960):
    """Zemin fotoğrafı + beyaz üst + başlık + (orta) + koyu alt bant."""
    koyu, vurgu = m["renk"]
    r_top = 300
    g_h = g_h or H - r_top
    b1, b2, b3, et = 58, 100, 58, 23
    logo, tel, wa = 52, 66, 25
    y = 1070
    r, g, bl = (int(koyu[j:j + 2], 16) for j in (1, 3, 5))
    return f"""
  <div class="a" style="left:0;top:{r_top + g_h - 60}px;width:{W}px;height:{H - r_top - g_h + 60}px;background:{koyu}"></div>
  <img class="a" src="{m['zemin']}" style="left:0;top:{r_top}px;width:{W}px;height:{g_h}px;object-fit:cover;object-position:{m['pos']};
       -webkit-mask-image:linear-gradient(180deg,transparent 0%,#000 30%)">
  <div class="a" style="left:0;top:0;width:{W}px;height:640px;background:linear-gradient(180deg,#fff 55%,rgba(255,255,255,0))"></div>

  <div class="a" style="left:0;top:62px;width:{W}px;text-align:center">
    <div class="k tek" style="font-size:{b1}px;color:{koyu}">{m['b1']}</div>
    <div class="k tek" style="margin-top:{round(b2 * .14)}px;font-size:{round(b2 * m.get('olcek', 1))}px;color:{vurgu}">{m['b2']}</div>
    <div class="k tek" style="margin-top:{round(b2 * .1)}px;font-size:{round(b3 * m.get('b3_olcek', 1))}px;color:{koyu}">{m['b3']}</div>
    <div class="tek" style="margin-top:{round(et * .9)}px;font-size:{et}px;font-weight:600;letter-spacing:.2em;color:#4a5878">MİA PARK OCEAN · İZMİT</div>
  </div>

  {orta}
  <div class="a" style="left:0;top:{bant}px;width:{W}px;height:{H - bant}px;
       background:linear-gradient(180deg,rgba({r},{g},{bl},0) 0%,rgba({r},{g},{bl},.92) 36%,{koyu} 60%)"></div>

  <div class="a" style="left:0;top:{y}px;width:{W}px;display:flex;align-items:center;justify-content:center;gap:{round(logo * .5)}px">
    <img src="{yy.TILDA}" style="height:{logo}px"><span style="width:2px;height:{round(logo * 1.3)}px;background:rgba(255,255,255,.55)"></span>
    <img src="{yy.MIA}" style="height:{round(logo * 1.45)}px"></div>
  <div class="a k tek" style="left:0;top:{y + round(logo * 1.75)}px;width:{W}px;text-align:center;font-size:{tel}px;color:#fff;letter-spacing:.01em">444 10 58</div>
  <div class="a" style="left:0;top:{y + round(logo * 1.75) + round(tel * 1.18)}px;width:{W}px;display:flex;align-items:center;justify-content:center;gap:{round(wa * .4)}px;color:#fff">
    {yy.WA.format(s=round(wa * 1.1))}<span class="tek" style="font-size:{wa}px;font-weight:700;letter-spacing:.04em">0540 028 00 41</span>
    <span style="width:1px;height:{wa}px;background:rgba(255,255,255,.5);margin:0 {round(wa * .3)}px"></span>
    <span class="tek" style="font-size:{round(wa * .9)}px;font-weight:600;letter-spacing:.06em;opacity:.9">miaparkocean.com</span></div>
"""


def hap(x, y, gen, metin, boy=27):
    return (f'<div class="a tek" style="left:{x}px;top:{y}px;width:{gen}px;padding:{round(boy * .62)}px 0;border-radius:{round(boy * .7)}px;'
            f'background:{KIRMIZI};color:#fff;text-align:center;font-size:{boy}px;font-weight:800;letter-spacing:.02em;'
            f'box-shadow:0 12px 26px rgba(225,38,47,.35)">{metin}</div>')


# ---------------------------------------------------------------- gönderi tipleri
def daire(m):
    """Daire tipi gönderisi: bir yanda fiyat kartı, diğer yanda dairenin iç mekânı."""
    x = 44 if m["taraf"] == "sol" else W - 488 - 44
    return iskelet(m, yy.kart(x, 424, 488, 64, m), g_h=760, bant=900)


def plan(m):
    """Ödeme planı: üç daire tipi tek tabloda."""
    koyu, vurgu = m["renk"]
    satir = ""
    for i, (tip, pesin, ayda) in enumerate(m["satirlar"]):
        satir += f"""
    <div class="a" style="left:54px;top:{424 + i * 142}px;width:{W - 108}px;height:124px;display:flex;border-radius:22px;overflow:hidden;
         box-shadow:0 18px 36px rgba(10,30,50,.32)">
      <div class="k" style="width:200px;background:{koyu};color:{vurgu};font-size:68px;display:flex;align-items:center;justify-content:center">{tip}</div>
      <div style="flex:1;background:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center">
        <div class="k tek" style="font-size:50px;color:{koyu}">{pesin}<span style="font-size:24px;letter-spacing:0;margin-left:7px">TL</span></div>
        <div class="tek" style="margin-top:7px;font-size:19px;font-weight:800;letter-spacing:.2em;color:#4a5878">PEŞİNAT</div></div>
      <div style="width:330px;background:{vurgu};display:flex;flex-direction:column;align-items:center;justify-content:center">
        <div class="tek" style="font-size:19px;font-weight:800;letter-spacing:.2em;color:{koyu}">AYDA</div>
        <div class="k tek" style="margin-top:5px;font-size:50px;color:{koyu}">{ayda}<span style="font-size:24px;letter-spacing:0;margin-left:7px">TL</span></div></div>
    </div>"""
    return iskelet(m, satir + hap(120, 862, W - 240, m["hap"], 26), bant=930)


def liste(m):
    """Bir yanda başlıklı liste kartı, diğer yanda fotoğraf."""
    koyu, vurgu = m["renk"]
    gen = 520
    x = 44 if m["taraf"] == "sol" else W - gen - 44
    sat = ""
    for i, (on, ad) in enumerate(m["satirlar"]):
        sol = (f'<span class="k tek" style="width:112px;font-size:33px;color:{vurgu}">{on}</span>' if on
               else TIK.format(s=34, c=vurgu, k=koyu) + '<span style="width:20px"></span>')
        cizgi = "border-top:1px solid rgba(255,255,255,.16);" if i else ""
        sat += (f'<div style="display:flex;align-items:center;height:67px;padding:0 30px;{cizgi}">{sol}'
                f'<span class="tek" style="font-size:26px;font-weight:700;color:#fff">{ad}</span></div>')
    kart = f"""
    <div class="a" style="left:{x}px;top:424px;width:{gen}px;border-radius:22px;overflow:hidden;box-shadow:0 20px 40px rgba(10,30,50,.36)">
      <div class="k tek" style="background:{vurgu};color:{koyu};text-align:center;font-size:33px;padding:20px 0 18px">{m['kart_baslik']}</div>
      <div style="background:{koyu};padding:4px 0 6px">{sat}</div>
    </div>"""
    return iskelet(m, kart + hap(x + 50, 928, gen - 100, m["hap"], 25), bant=980)


GONDERILER = [
    dict(ad="1-odeme-plani", tip=plan, renk=LACI, zemin=yy.SRC("avlu-havuz-ustten.jpg"), pos="50% 60%",
         b1="60 Ay Vade Farksız", b2="ÖDEME PLANI", b3="Size Uygun Daireyi Seçin",
         satirlar=[("1+0", "699.000", "29.900"), ("1+1", "999.000", "39.900"), ("2+1", "2.000.000", "50.000")],
         hap="BANKA YOK · FAİZ YOK · KEFİL YOK · ARA ÖDEME YOK"),
    dict(ad="2-daire-1-0", tip=daire, renk=PETROL, taraf="sol", zemin=IMG("unit-1plus0-a.webp"), pos="88% 50%",
         b1="1+0 Daireler", b2="699.000 TL", b3="Peşinatla Sizin",
         ust=("AYDA", "29.900", "TL", "SABİT TAKSİT"), serit="60 AY VADE FARKSIZ", hap="BANKA YOK<br>ARA ÖDEME YOK", alt="1+0 · BRÜT 28 m²"),
    dict(ad="3-daire-1-1", tip=daire, renk=LACI, taraf="sag", zemin=IMG("ic-mekan/05-1plus1-salon.webp"), pos="12% 50%",
         b1="1+1 Daireler", b2="999.000 TL", b3="Peşinatla Sizin",
         ust=("AYDA", "39.900", "TL", "SABİT TAKSİT"), serit="60 AY VADE FARKSIZ", hap="FAİZ YOK<br>KEFİL YOK", alt="1+1 · BRÜT 50 m²"),
    dict(ad="4-daire-2-1", tip=daire, renk=YESIL, taraf="sol", zemin=IMG("unit-2plus1-a.webp"), pos="80% 50%",
         b1="2+1 Daireler", b2="2.000.000 TL", olcek=.9, b3="Peşinatla Sizin",
         ust=("AYDA", "50.000", "TL", "SABİT TAKSİT"), serit="60 AY VADE FARKSIZ", hap="BANKA YOK<br>ARA ZAM YOK", alt="2+1 · BRÜT 100 m²"),
    dict(ad="5-konum", tip=liste, renk=PETROL, taraf="sol", zemin=yy.FOTO("4-tepeden-capraz.jpg"), pos="50% 62%",
         b1="Yeni Eviniz", b2="HER YERE YAKIN", olcek=.88, b3="İzmit MİA Bölgesi'nde",
         kart_baslik="DAKİKALAR İÇİNDE",
         satirlar=[("1 dk", "D-100 Karayolu"), ("3 dk", "41 Burada AVM"), ("5 dk", "Şehir Merkezi"),
                   ("5 dk", "Şehir Hastanesi"), ("5 dk", "TEM Otoyolu"), ("10 dk", "Kocaeli Üniversitesi")],
         hap="MERKEZİ KONUM"),
    dict(ad="6-sosyal-yasam", tip=liste, renk=YESIL, taraf="sag", zemin=yy.SRC("cocuk-parki.jpg"), pos="30% 50%",
         b1="Sitenin İçinde", b2="HER ŞEY HAZIR", olcek=.92, b3="Ailece Keyifli Bir Yaşam",
         kart_baslik="SOSYAL YAŞAM",
         satirlar=[("", "Kapalı Yüzme Havuzu"), ("", "Fitness Salonu"), ("", "Sauna ve Türk Hamamı"),
                   ("", "Çocuk Oyun Parkı"), ("", "Kapalı Otopark"), ("", "7/24 Güvenlik")],
         hap="HEPSİ SİTENİN İÇİNDE"),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    gecici = tempfile.mkdtemp(prefix="igpost-")
    isler = []
    for m in GONDERILER:
        hp = os.path.join(gecici, m["ad"] + ".html")
        open(hp, "w", encoding="utf-8").write(
            f'<!doctype html><html><head><meta charset="utf-8"><style>{yy.css(H)}</style></head><body>{m["tip"](m)}</body></html>')
        isler.append(dict(html=hp, w=W, h=H, dsf=2, dilim=W, cikti=os.path.join(gecici, m["ad"]), ad=m["ad"]))
    jp = os.path.join(gecici, "isler.json")
    json.dump(isler, open(jp, "w"))
    npm = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    subprocess.run(["node", os.path.join(ROOT, "scripts", "mega-bilbord", "render.cjs"), jp], check=True,
                   env={**os.environ, "NODE_PATH": npm}, stdout=subprocess.DEVNULL)
    kareler = []
    for is_ in isler:
        im = Image.open(json.load(open(is_["cikti"] + ".json"))[0]).convert("RGB")
        yol = os.path.join(OUT, f"mia-post-{is_['ad']}.jpg")
        im.save(yol, quality=92)
        kareler.append(im)
        print("  →", os.path.relpath(yol, ROOT), im.size)
    kw, kh = 540, 675
    sayfa = Image.new("RGB", (3 * kw + 4 * 20, 2 * kh + 3 * 20), "#e9edf2")
    for i, im in enumerate(kareler):
        sayfa.paste(im.resize((kw, kh), Image.LANCZOS), (20 + (i % 3) * (kw + 20), 20 + (i // 3) * (kh + 20)))
    sayfa.save(os.path.join(OUT, "onizleme.jpg"), quality=88)


if __name__ == "__main__":
    sys.exit(main())
