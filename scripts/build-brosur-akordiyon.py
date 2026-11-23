#!/usr/bin/env python3
"""
Akordiyon (Z) kırımlı broşür — açık 30×20 cm, 2 kırım, 3 panel (kapalı 10×20 cm), çift yüz.

Baskı PDF'i: 306×206 mm (her kenarda 3 mm taşma), 2 sayfa. Kırım çizgileri taşmalı sayfada
x = 103 mm ve x = 203 mm. Metinler vektör; görseller RGB (matbaa CMYK'ye çevirir).

Panel yerleşimi (Z kırım):
  DIŞ YÜZ (sayfa 1)  soldan sağa:  Daire Tipleri | Sosyal Yaşam + Konum | ÖN KAPAK
  İÇ YÜZ  (sayfa 2)  soldan sağa:  Proje         | Ödeme Planı          | ARKA KAPAK
Kapak açılınca Proje + Ödeme Planı karşılıklı görünür; arka kapak iletişim panelidir.

Çıktı: baski/brosur-akordiyon/
  mia-brosur-akordiyon-30x20-baski.pdf   matbaaya gidecek dosya (taşmalı)
  onizleme-dis-yuz.jpg / onizleme-ic-yuz.jpg   kırım çizgili önizleme

    python3.13 scripts/build-brosur-akordiyon.py
"""

import json
import os
import subprocess
import tempfile

import segno
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "baski", "brosur-akordiyon")
FONT = os.path.join(ROOT, "brand-source", "fonts", "Montserrat-var.ttf")
F = lambda *p: "file://" + os.path.join(ROOT, *p)
V = lambda ad: F("public", "brand", "vektor", ad)
IC = lambda ad: F("public", "images", "ic-mekan", ad)

LACI, LACI2, ALTIN, KIRMIZI, BUZ = "#14306b", "#0d2250", "#c9a24a", "#e1262f", "#f1f5fb"
TASMA, PANEL, BOY = 3, 100, 200  # mm

IKON = {
    "dalga": '<path d="M2 6c.6.5 1.2 1 2.5 1C7 7 7 5 9.5 5c2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/><path d="M2 12c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/><path d="M2 18c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/>',
    "damla": '<path d="M12 2.7l5.7 5.6a8 8 0 1 1-11.3 0z"/>',
    "spor": '<path d="M6.5 6.5l11 11"/><path d="M21 21l-1-1"/><path d="M3 3l1 1"/><path d="M18 22l4-4"/><path d="M2 6l4-4"/><path d="M3 10l7-7"/><path d="M14 21l7-7"/>',
    "alev": '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"/>',
    "agac": '<path d="M12 22v-7"/><path d="M8 22h8"/><circle cx="12" cy="8" r="6"/>',
    "yol": '<circle cx="6" cy="19" r="3"/><path d="M9 19h8.5a3.5 3.5 0 0 0 0-7h-11a3.5 3.5 0 0 1 0-7H15"/><circle cx="18" cy="5" r="3"/>',
    "araba": '<path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2"/><circle cx="7" cy="17" r="2"/><path d="M9 17h6"/><circle cx="17" cy="17" r="2"/>',
    "kalkan": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    "tel": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
    "kure": '<circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 0 20 15.3 15.3 0 0 1 0-20z"/>',
    "insta": '<rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".6"/>',
}
WA = ('<svg viewBox="0 0 24 24" style="width:{s}mm;height:{s}mm;fill:#25d366;flex:none">'
      '<path d="M17.5 14.4c-.3-.2-1.7-.8-2-.9-.3-.1-.5-.2-.7.2-.2.3-.7.9-.9 1.1-.2.2-.3.2-.6.1-.3-.2-1.2-.5-2.3-1.4-.9-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6.1-.1.3-.3.4-.5.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5 0-.1-.7-1.6-.9-2.2-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.4s1.1 2.8 1.2 3c.2.2 2.1 3.2 5 4.5.7.3 1.2.5 1.7.6.7.2 1.3.2 1.8.1.6-.1 1.7-.7 1.9-1.3.2-.7.2-1.2.2-1.3-.1-.2-.3-.3-.6-.4z"/>'
      '<path d="M12 2C6.5 2 2 6.5 2 12c0 1.8.5 3.5 1.3 5L2 22l5.1-1.3c1.4.8 3.1 1.2 4.9 1.2 5.5 0 10-4.5 10-10S17.5 2 12 2zm0 18.2c-1.6 0-3.1-.4-4.4-1.2l-.3-.2-3 .8.8-2.9-.2-.3C4 15 3.6 13.5 3.6 12 3.6 7.4 7.4 3.6 12 3.6S20.4 7.4 20.4 12 16.6 20.2 12 20.2z"/></svg>')


def ikon(ad, s=4.4, renk=LACI, kalinlik=1.7):
    return (f'<svg viewBox="0 0 24 24" style="width:{s}mm;height:{s}mm;flex:none" fill="none" stroke="{renk}" '
            f'stroke-width="{kalinlik}" stroke-linecap="round" stroke-linejoin="round">{IKON[ad]}</svg>')


def tik(s=3.6, zemin=ALTIN, cizgi="#fff"):
    return (f'<svg viewBox="0 0 24 24" style="width:{s}mm;height:{s}mm;flex:none"><circle cx="12" cy="12" r="12" fill="{zemin}"/>'
            f'<path d="M6.5 12.5l3.6 3.6L17.5 8.7" fill="none" stroke="{cizgi}" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/></svg>')


CSS = f"""
@font-face {{ font-family: Mont; src: url("file://{FONT}"); font-weight: 100 900; }}
@page {{ size: {3 * PANEL + 2 * TASMA}mm {BOY + 2 * TASMA}mm; margin: 0; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ font-family:Mont,sans-serif; -webkit-font-smoothing:antialiased; color:#1f2a44;
              -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
.sayfa {{ position:relative; width:{3 * PANEL + 2 * TASMA}mm; height:{BOY + 2 * TASMA}mm; overflow:hidden; page-break-after:always; background:#fff; }}
.sayfa:last-child {{ page-break-after:auto; }}
/* Panel: kırpma alanı 100×200 mm; zemin (.z) taşma payına kadar uzar. */
.panel {{ position:absolute; top:{TASMA}mm; width:{PANEL}mm; height:{BOY}mm; }}
.z {{ position:absolute; top:-{TASMA}mm; bottom:-{TASMA}mm; left:0; right:0; overflow:hidden; }}
.sol .z {{ left:-{TASMA}mm; }}
.sag .z {{ right:-{TASMA}mm; }}
.a {{ position:absolute; }}
.tek {{ white-space:nowrap; }}
.k {{ font-weight:800; letter-spacing:-.015em; line-height:1.02; }}
.ust {{ font-size:6.6pt; font-weight:700; letter-spacing:.26em; color:{ALTIN}; text-transform:uppercase; }}
.baslik {{ font-size:14.5pt; font-weight:800; line-height:1.12; letter-spacing:-.01em; color:{LACI}; }}
.metin {{ font-size:7.7pt; line-height:1.5; font-weight:500; color:#34405c; }}
.kilavuz {{ position:absolute; top:0; bottom:0; width:0; border-left:.35mm dashed #e1262f; z-index:50; }}
.kilavuz-kirp {{ position:absolute; left:{TASMA}mm; top:{TASMA}mm; width:{3 * PANEL}mm; height:{BOY}mm; outline:.3mm solid #18a558; z-index:50; }}
.etiket {{ position:absolute; top:{TASMA + 1.5}mm; z-index:51; background:#e1262f; color:#fff; font-size:6pt; font-weight:700; padding:.6mm 1.6mm; border-radius:1mm; }}
"""


# ---------------------------------------------------------------- DIŞ YÜZ ----

def p_daire_tipleri():
    tipler = [
        ("1+0", "Brüt 28 m²", "Akıllı tasarım, maksimum konfor", "01-1plus0-salon.webp"),
        ("1+1", "Brüt 50 m²", "Ferah, konforlu ve fonksiyonel", "05-1plus1-salon.webp"),
        ("1+1 Bahçe Loft", "Brüt 50 m²", "Zemin katta kendi bahçeniz", "09-loft-salon.webp"),
        ("2+1 Bahçe Dubleks", "Brüt 100 m²", "Bahçeniz, evinizin devamı", "11-dubleks-salon.webp"),
    ]
    kartlar = "".join(f"""
    <div style="position:relative;height:35.2mm;border-radius:2.6mm;overflow:hidden;box-shadow:0 1.2mm 3mm rgba(10,30,70,.16)">
      <img src="{IC(g)}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">
      <div style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(13,34,80,.9) 0%,rgba(13,34,80,.62) 46%,rgba(13,34,80,0) 78%)"></div>
      <div style="position:absolute;left:4.2mm;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center;color:#fff">
        <div class="k tek" style="font-size:{'17' if len(t) < 5 else '11.5'}pt">{t}</div>
        <div class="tek" style="margin-top:1.4mm;display:inline-block;align-self:flex-start;background:{ALTIN};color:{LACI2};font-size:6.8pt;font-weight:800;padding:.7mm 2mm;border-radius:1mm">{m2}</div>
        <div style="margin-top:1.6mm;width:36mm;font-size:6.6pt;font-weight:500;line-height:1.35;opacity:.95">{slogan}</div>
      </div>
    </div>""" for t, m2, slogan, g in tipler)
    return f"""
  <div class="panel sol" style="left:{TASMA}mm">
    <div class="z" style="background:#fff"></div>
    <div class="a" style="left:7mm;right:7mm;top:9mm">
      <div class="ust">Daire Tipleri</div>
      <div class="baslik" style="margin-top:2mm">Her ihtiyaca uygun<br>4 farklı yaşam tipi</div>
    </div>
    <div class="a" style="left:7mm;right:7mm;top:34mm;display:flex;flex-direction:column;gap:3.2mm">{kartlar}</div>
    <div class="a tek" style="left:7mm;right:7mm;top:190.5mm;font-size:6pt;font-weight:500;color:#6a748c">İç mekân görselleri örnek tasarımdır.</div>
  </div>"""


def p_sosyal_konum():
    donatilar = [("dalga", "Süs havuzları"), ("damla", "Kapalı yüzme havuzu"), ("spor", "Fitness salonu"),
                 ("alev", "Sauna ve Türk hamamı"), ("agac", "Çocuk oyun parkı"), ("yol", "Yürüyüş yolları"),
                 ("araba", "Kapalı otopark"), ("kalkan", "7/24 güvenlik")]
    konum = [("D-100 Karayolu", "1 dk"), ("41 Burada AVM", "3 dk"), ("Şehir Merkezi", "5 dk"),
             ("Şehir Hastanesi", "5 dk"), ("TEM Otoyolu", "5 dk"), ("Kocaeli Üniversitesi", "10 dk")]
    d = "".join(f'<div style="display:flex;align-items:center;gap:2mm;font-size:7.3pt;font-weight:600;color:{LACI2}">'
                f'<span style="width:7.4mm;height:7.4mm;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;'
                f'box-shadow:0 .5mm 1.5mm rgba(10,30,70,.14);flex:none">{ikon(i, 4)}</span>{t}</div>' for i, t in donatilar)
    k = "".join(f'<div style="display:flex;justify-content:space-between;align-items:baseline;padding:1.25mm 0;border-bottom:.2mm solid rgba(255,255,255,.18);'
                f'font-size:7.4pt;font-weight:500"><span>{y}</span><b style="font-weight:800;color:{ALTIN}">{s}</b></div>' for y, s in konum)
    return f"""
  <div class="panel" style="left:{TASMA + PANEL}mm">
    <div class="z" style="background:{BUZ}"></div>
    <div class="a" style="left:7mm;right:7mm;top:9mm">
      <div class="ust">Sosyal Yaşam</div>
      <div class="baslik" style="margin-top:2mm">Aradığınız her şey<br>sitenin içinde</div>
    </div>
    <img class="a" src="{IC('17-sus-havuzu.webp')}" style="left:7mm;top:34mm;width:86mm;height:44mm;object-fit:cover;border-radius:2.6mm">
    <div class="a" style="left:7mm;right:7mm;top:84mm;display:grid;grid-template-columns:1fr 1fr;gap:2.8mm 2mm">{d}</div>
    <div class="a" style="left:7mm;right:7mm;top:128.5mm;height:63.5mm;border-radius:2.6mm;background:{LACI};color:#fff;padding:4.6mm 5.5mm">
      <div class="ust">Konum · İzmit MİA Bölgesi</div>
      <div style="margin-top:1.6mm;font-size:11pt;font-weight:800;line-height:1.15">Şehrin her noktasına<br>dakikalar içinde</div>
      <div style="margin-top:2.4mm">{k}</div>
    </div>
  </div>"""


def p_on_kapak():
    return f"""
  <div class="panel sag" style="left:{TASMA + 2 * PANEL}mm">
    <div class="z" style="background:#fff">
      <img src="{F('signage-source', 'courtyard-pools.jpg')}" style="position:absolute;left:0;top:{TASMA + 60}mm;width:100%;height:{BOY + TASMA - 60}mm;object-fit:cover;object-position:50% 50%;
           -webkit-mask-image:linear-gradient(180deg,transparent 0%,#000 26%)">
      <img src="{F('signage-source', 'aile', 'aile2-kesik.png')}" style="position:absolute;left:-1mm;top:{TASMA + 106}mm;height:72mm;filter:drop-shadow(0 2mm 3mm rgba(10,30,60,.28))">
      <div style="position:absolute;left:0;right:0;top:{TASMA + 148}mm;bottom:0;background:linear-gradient(180deg,rgba(20,48,107,0) 0%,rgba(20,48,107,.92) 38%,{LACI} 62%)"></div>
    </div>
    <img class="a" src="{V('mia-lacivert.svg')}" style="left:36mm;top:8mm;width:28mm">
    <div class="a" style="left:0;right:0;top:32mm;text-align:center">
      <div class="k tek" style="font-size:15pt;color:{LACI}">Ailenize</div>
      <div class="k tek" style="margin-top:1.4mm;font-size:24pt;color:{ALTIN}">YENİ BİR YUVA</div>
      <div class="tek" style="margin-top:2.6mm;font-size:6.4pt;font-weight:600;letter-spacing:.24em;color:#4a5878">İZMİT · MİA BÖLGESİ</div>
    </div>
    <div class="a" style="left:45mm;top:65mm;width:49mm">
      <div style="border-radius:2.4mm;overflow:hidden;box-shadow:0 2mm 4.5mm rgba(10,30,70,.35)">
        <div style="background:{LACI};padding:2.8mm 0 2.3mm;text-align:center;color:#fff">
          <div class="k tek" style="font-size:19pt">699.000<span style="font-size:7pt;letter-spacing:0;margin-left:.8mm">TL'DEN</span></div>
          <div class="tek" style="margin-top:.9mm;font-size:7.4pt;font-weight:800;letter-spacing:.06em">BAŞLAYAN PEŞİNAT</div>
        </div>
        <div style="height:.5mm;background:#fff"></div>
        <div class="k tek" style="background:{ALTIN};padding:2.3mm 0 2.1mm;text-align:center;font-size:11.4pt;color:{LACI}">60 AY SABİT TAKSİT</div>
      </div>
      <div class="tek" style="margin:2.8mm 1.5mm 0;padding:1.9mm 0;border-radius:2.2mm;background:{KIRMIZI};color:#fff;text-align:center;font-size:7pt;font-weight:800;line-height:1.25;
           box-shadow:0 1.4mm 3mm rgba(225,38,47,.35)">BANKA YOK · FAİZ YOK<br>KEFİL YOK · ARA ÖDEME YOK</div>
    </div>
    <div class="a" style="left:0;right:0;top:170mm;display:flex;align-items:center;justify-content:center;gap:3.4mm">
      <img src="{V('tilda-beyaz.svg')}" style="height:6.4mm"><span style="width:.25mm;height:8.4mm;background:rgba(255,255,255,.55)"></span>
      <img src="{V('ocean-beyaz.svg')}" style="height:6.8mm"></div>
    <div class="a k tek" style="left:0;right:0;top:181mm;text-align:center;font-size:21pt;color:#fff;letter-spacing:.01em">444 10 58</div>
  </div>"""


# ----------------------------------------------------------------- İÇ YÜZ ----

def p_proje():
    rakamlar = [("600", "Daire"), ("4", "Blok"), ("10", "Dönüm Arazi"), ("4", "Daire Tipi")]
    r = "".join(f'<div style="background:{BUZ};border-radius:2.2mm;padding:2.6mm 0 2.3mm;text-align:center">'
                f'<div class="k" style="font-size:19pt;color:{LACI}">{s}</div>'
                f'<div style="margin-top:.8mm;font-size:6.6pt;font-weight:700;letter-spacing:.08em;color:{ALTIN};text-transform:uppercase">{e}</div></div>' for s, e in rakamlar)
    maddeler = ["Fore kazık temel sistemi", "Depreme dayanıklı yapı", "Merkezi avlu ve geniş peyzaj", "Bahçeli zemin kat daireleri"]
    m = "".join(f'<div style="display:flex;align-items:center;gap:2mm;font-size:7.7pt;font-weight:600;color:{LACI2}">{tik()}{t}</div>' for t in maddeler)
    return f"""
  <div class="panel sol" style="left:{TASMA}mm">
    <div class="z" style="background:#fff">
      <img src="{F('signage-source', 'entrance-gate.jpg')}" style="position:absolute;left:0;top:0;width:100%;height:{TASMA + 76}mm;object-fit:cover;object-position:42% 50%">
      <div style="position:absolute;left:0;right:0;top:{TASMA + 54}mm;height:22.2mm;background:linear-gradient(180deg,rgba(255,255,255,0),#fff)"></div>
    </div>
    <div class="a" style="left:7mm;right:7mm;top:78mm">
      <div class="ust">Proje</div>
      <div class="baslik" style="margin-top:2mm">Şehrin merkezinde,<br>modern ve güvenli<br>bir yaşam</div>
      <div class="metin" style="margin-top:3mm">MİA PARK OCEAN; İzmit MİA Bölgesi'nde, 10 dönüm arazi üzerinde yükselen 4 blok ve 600 daireden oluşuyor.
        Süs havuzlu avlusu, geniş peyzajı ve zengin sosyal alanlarıyla şehrin içinde ferah bir yaşam sunuyor.</div>
    </div>
    <div class="a" style="left:7mm;right:7mm;top:131mm;display:grid;grid-template-columns:1fr 1fr;gap:2.4mm">{r}</div>
    <div class="a" style="left:7mm;right:7mm;top:168.5mm;display:flex;flex-direction:column;gap:1.9mm">{m}</div>
  </div>"""


def p_odeme():
    yoklar = ["Faiz yok", "Banka yok", "Kredi yok", "Kefil yok", "Ara ödeme yok", "Sabit taksit"]
    y = "".join(f'<div style="display:flex;align-items:center;gap:1.8mm;font-size:8pt;font-weight:700">{tik(3.6)}{t}</div>' for t in yoklar)
    adimlar = [("1", "Dairenizi seçin", "Satış ofisinde size uygun tipi belirleyin."),
               ("2", "Peşinatınızı ödeyin", "699.000 TL'den başlayan peşinatla yerinizi ayırtın."),
               ("3", "60 ayda tamamlayın", "Kalan tutarı sabit taksitlerle ödeyin.")]
    a = "".join(f'<div style="display:flex;gap:2.6mm;align-items:flex-start"><span class="k" style="width:7mm;height:7mm;border-radius:50%;background:{ALTIN};'
                f'color:{LACI2};font-size:10pt;display:flex;align-items:center;justify-content:center;flex:none">{n}</span>'
                f'<div><div style="font-size:8.4pt;font-weight:800">{b}</div><div style="margin-top:.5mm;font-size:6.8pt;font-weight:500;line-height:1.4;opacity:.85">{t}</div></div></div>'
                for n, b, t in adimlar)
    return f"""
  <div class="panel" style="left:{TASMA + PANEL}mm;color:#fff">
    <div class="z" style="background:linear-gradient(180deg,{LACI} 0%,{LACI2} 100%)"></div>
    <div class="a" style="left:7mm;right:7mm;top:9mm">
      <div class="ust">Ödeme Planı</div>
      <div class="k" style="margin-top:2.4mm;font-size:19pt;line-height:1.08">BANKA <span style="color:{ALTIN}">YOK.</span><br>FAİZ <span style="color:{ALTIN}">YOK.</span><br>KEFİL <span style="color:{ALTIN}">YOK.</span></div>
    </div>
    <div class="a" style="left:7mm;right:7mm;top:47mm;border-radius:2.6mm;overflow:hidden;box-shadow:0 2mm 5mm rgba(0,0,0,.3)">
      <div style="background:#fff;padding:3.6mm 0 3mm;text-align:center;color:{LACI}">
        <div class="k tek" style="font-size:27pt">699.000<span style="font-size:10pt;letter-spacing:0;margin-left:1mm">TL'DEN</span></div>
        <div class="tek" style="margin-top:1.1mm;font-size:8.6pt;font-weight:800;letter-spacing:.08em">BAŞLAYAN PEŞİNAT</div>
      </div>
      <div class="k tek" style="background:{ALTIN};padding:2.9mm 0 2.6mm;text-align:center;font-size:14pt;color:{LACI2}">60 AY SABİT TAKSİT</div>
    </div>
    <div class="a" style="left:7mm;right:7mm;top:86.5mm;display:grid;grid-template-columns:1fr 1fr;gap:2.4mm 2mm">{y}</div>
    <div class="a" style="left:7mm;right:7mm;top:112mm;height:.25mm;background:rgba(255,255,255,.22)"></div>
    <div class="a" style="left:7mm;right:7mm;top:118mm">
      <div class="ust">3 Adımda Ev Sahibi Olun</div>
      <div style="margin-top:3.6mm;display:flex;flex-direction:column;gap:3.8mm">{a}</div>
    </div>
    <div class="a" style="left:7mm;right:7mm;top:171mm;border-radius:2.4mm;background:rgba(255,255,255,.08);border:.25mm solid rgba(201,162,74,.6);padding:3.2mm 3.6mm;display:flex;gap:2.6mm;align-items:flex-start">
      {ikon('kalkan', 6.4, ALTIN, 1.6)}
      <div><div style="font-size:7.8pt;font-weight:800;color:{ALTIN}">Kooperatif Güvencesi</div>
      <div style="margin-top:.8mm;font-size:6.5pt;font-weight:500;line-height:1.42;opacity:.92">S.S. Yahya Kaptan Birlik Yapı Kooperatifi, T.C. Ticaret Bakanlığı bünyesindeki KOOPBİS'e kayıtlıdır.</div></div>
    </div>
  </div>"""


def p_arka_kapak(qr, ykb):
    satir = lambda i, t: f'<div style="display:flex;align-items:flex-start;gap:2.4mm;font-size:7.8pt;font-weight:600;color:{LACI2};line-height:1.4">{i}<span>{t}</span></div>'
    logo = lambda etiket, img: (f'<div style="flex:1;text-align:center"><div style="font-size:5pt;font-weight:700;letter-spacing:.14em;color:#6a748c">{etiket}</div>'
                                f'<div style="height:14mm;display:flex;align-items:center;justify-content:center;margin-top:1mm">{img}</div></div>')
    return f"""
  <div class="panel sag" style="left:{TASMA + 2 * PANEL}mm">
    <div class="z" style="background:#fff">
      <div style="position:absolute;left:0;right:0;top:0;height:{TASMA + 63}mm;background:linear-gradient(180deg,{LACI} 0%,{LACI2} 100%)"></div>
    </div>
    <img class="a" src="{V('mia-beyaz.svg')}" style="left:38mm;top:7.5mm;width:24mm">
    <div class="a" style="left:0;right:0;top:30mm;text-align:center;color:#fff">
      <div class="tek" style="font-size:7pt;font-weight:600;letter-spacing:.22em;color:{ALTIN}">BİLGİ VE SATIŞ</div>
      <div class="k tek" style="margin-top:1.8mm;font-size:30pt;letter-spacing:.01em">444 10 58</div>
      <div style="margin-top:2.4mm;display:flex;align-items:center;justify-content:center;gap:1.6mm">{WA.format(s=4.4)}
        <span class="tek" style="font-size:10.5pt;font-weight:700;letter-spacing:.03em">0540 028 00 41</span></div>
    </div>

    <div class="a" style="left:7mm;right:7mm;top:70mm">
      <div class="ust">Satış Ofisi</div>
      <div style="margin-top:2.6mm;display:flex;flex-direction:column;gap:2.2mm">
        {satir(ikon('pin', 4.2), 'Ömerağa Mah. Abdurrahman Yüksel Cad.<br>Bana Bak Ap. No:15/4 İzmit / Kocaeli')}
        {satir(ikon('tel', 4.2), '0541 128 40 41')}
        {satir(ikon('kure', 4.2), 'miaparkocean.com')}
        {satir(ikon('insta', 4.2), '@miaparkocean')}
      </div>
    </div>

    <div class="a" style="left:7mm;right:7mm;top:113mm;border-radius:2.6mm;background:{BUZ};padding:4mm;display:flex;align-items:center;gap:4mm">
      <img src="file://{qr}" style="width:27mm;height:27mm;flex:none">
      <div><div style="font-size:9pt;font-weight:800;color:{LACI};line-height:1.2">Projeyi telefonunuzdan inceleyin</div>
        <div style="margin-top:1.4mm;font-size:6.6pt;font-weight:500;line-height:1.42;color:#34405c">Kamerayı kodun üzerine tutun; daire tipleri, kat planları ve galeri karşınızda.</div></div>
    </div>

    <div class="a" style="left:6mm;right:6mm;top:154mm;display:flex;align-items:flex-start;gap:1mm">
      {logo('YAPIMCI', f'<img src="file://{ykb}" style="height:14mm">')}
      {logo('MÜTEAHHİT', f'<img src="{V("tilda.svg")}" style="width:25mm">')}
      {logo('TEK YETKİLİ SATICI', f'<img src="{V("ocean-lacivert.svg")}" style="width:21mm">')}
    </div>
    <div class="a" style="left:7mm;right:7mm;top:178.5mm;font-size:5pt;font-weight:500;line-height:1.45;color:#7a849b;text-align:center">
      Yapımcı: S.S. Yahya Kaptan Birlik Yapı Kooperatifi · Müteahhit: Tilda İnşaat · Tek Yetkili Satıcı: Ocean Gayrimenkul.
      Görseller tanıtım amaçlıdır; uygulamada değişiklik olabilir. Güncel ödeme planı ve kampanya koşulları için satış ofisimizle görüşünüz.</div>
  </div>"""


def belge(qr, ykb, kilavuz=False):
    k1 = k2 = ""
    if kilavuz:
        cizgi = "".join(f'<div class="kilavuz" style="left:{TASMA + i * PANEL}mm"></div>' for i in (1, 2)) + '<div class="kilavuz-kirp"></div>'
        et = lambda adlar: "".join(f'<div class="etiket" style="left:{TASMA + i * PANEL + 1.5}mm">{a}</div>' for i, a in enumerate(adlar))
        k1 = cizgi + et(["DIŞ YÜZ · sol panel", "DIŞ YÜZ · orta panel", "ÖN KAPAK"])
        k2 = cizgi + et(["İÇ YÜZ · kapak arkası", "İÇ YÜZ · orta panel", "ARKA KAPAK"])
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>'
            f'<div class="sayfa" id="dis">{p_daire_tipleri()}{p_sosyal_konum()}{p_on_kapak()}{k1}</div>'
            f'<div class="sayfa" id="ic">{p_proje()}{p_odeme()}{p_arka_kapak(qr, ykb)}{k2}</div></body></html>')


RENDER_JS = r"""
const fs = require("fs");
const { chromium } = require("playwright");
(async () => {
  const is = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
  const t = await chromium.launch();
  const hazir = async (s) => { await s.evaluate(() => document.fonts.ready);
    await s.waitForFunction(() => [...document.images].every((i) => i.complete && i.naturalWidth > 0)); };
  const s = await t.newPage();
  await s.goto("file://" + is.html); await hazir(s);
  await s.pdf({ path: is.pdf, preferCSSPageSize: true, printBackground: true });
  const c = await t.newContext({ viewport: { width: 1200, height: 800 }, deviceScaleFactor: 3 });
  const o = await c.newPage();
  await o.goto("file://" + is.kilavuzHtml); await hazir(o);
  for (const id of ["dis", "ic"]) await o.locator("#" + id).screenshot({ path: is.png[id] });
  await t.close();
})();
"""


def main():
    os.makedirs(OUT, exist_ok=True)
    g = tempfile.mkdtemp(prefix="brosur-")
    qr = os.path.join(g, "qr.svg")
    segno.make("https://miaparkocean.com/", error="q").save(qr, scale=10, border=1, dark=LACI2, light=None)
    ykb = os.path.join(g, "ykb.png")
    y = Image.open(os.path.join(ROOT, "public", "ykb-logo.png")).convert("RGBA")
    y = y.crop(y.getchannel("A").getbbox())
    y.resize((round(y.width * 900 / y.height), 900), Image.LANCZOS).save(ykb)

    html, kil = os.path.join(g, "brosur.html"), os.path.join(g, "kilavuz.html")
    open(html, "w", encoding="utf-8").write(belge(qr, ykb))
    open(kil, "w", encoding="utf-8").write(belge(qr, ykb, kilavuz=True))
    pdf = os.path.join(OUT, "mia-brosur-akordiyon-30x20-baski.pdf")
    png = {k: os.path.join(g, k + ".png") for k in ("dis", "ic")}
    js, jp = os.path.join(g, "render.cjs"), os.path.join(g, "is.json")
    open(js, "w").write(RENDER_JS)
    json.dump(dict(html=html, kilavuzHtml=kil, pdf=pdf, png=png), open(jp, "w"))
    npm = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    subprocess.run(["node", js, jp], check=True, env={**os.environ, "NODE_PATH": npm})
    print("  →", os.path.relpath(pdf, ROOT))
    for k, ad in (("dis", "onizleme-dis-yuz.jpg"), ("ic", "onizleme-ic-yuz.jpg")):
        im = Image.open(png[k]).convert("RGB")
        im.save(os.path.join(OUT, ad), quality=90)
        print("  →", os.path.relpath(os.path.join(OUT, ad), ROOT), im.size)


if __name__ == "__main__":
    main()
