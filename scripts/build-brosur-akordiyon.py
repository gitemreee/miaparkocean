#!/usr/bin/env python3
"""
Akordiyon (Z) kırımlı broşür — açık 30×20 cm, 2 kırım, 3 panel (kapalı 10×20 cm), çift yüz.

Baskı PDF'i: 306×206 mm (her kenarda 3 mm taşma), 2 sayfa. Kırım çizgileri taşmalı sayfada
x = 103 mm ve x = 203 mm. Metinler vektör; görseller RGB (matbaa CMYK'ye çevirir).

Panel yerleşimi (Z kırım):
  DIŞ YÜZ (sayfa 1)  soldan sağa:  Daire Tipleri | Ödeme Planı | ÖN KAPAK
  İÇ YÜZ  (sayfa 2)  soldan sağa:  Neden MİA PARK OCEAN? (iki panel, 8 neden) | ARKA KAPAK
Kapak açılınca "Neden MİA PARK OCEAN?" iki panele yayılmış görünür; arka kapak iletişim panelidir.
Metinler web sitesindeki verilerden (konum, ödeme, sosyal alanlar, kooperatif) alınmıştır.

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

TEAL, TEAL2, TURK, KUM, MERCAN, SARI = "#0b4a5a", "#07333f", "#17a2b4", "#f6f0e6", "#ff6b4a", "#ffd166"
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
    "yuzde": '<line x1="19" y1="5" x2="5" y2="19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/>',
    "bina": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 22v-4h6v4"/><path d="M8 6h.01M12 6h.01M16 6h.01M8 10h.01M12 10h.01M16 10h.01M8 14h.01M12 14h.01M16 14h.01"/>',
    "banka": '<line x1="3" y1="22" x2="21" y2="22"/><line x1="6" y1="18" x2="6" y2="11"/><line x1="10" y1="18" x2="10" y2="11"/><line x1="14" y1="18" x2="14" y2="11"/><line x1="18" y1="18" x2="18" y2="11"/><polygon points="12 2 20 7 4 7"/>',
    "artis": '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>',
    "insta": '<rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".6"/>',
}
WA = ('<svg viewBox="0 0 24 24" style="width:{s}mm;height:{s}mm;fill:#25d366;flex:none">'
      '<path d="M17.5 14.4c-.3-.2-1.7-.8-2-.9-.3-.1-.5-.2-.7.2-.2.3-.7.9-.9 1.1-.2.2-.3.2-.6.1-.3-.2-1.2-.5-2.3-1.4-.9-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6.1-.1.3-.3.4-.5.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5 0-.1-.7-1.6-.9-2.2-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.4s1.1 2.8 1.2 3c.2.2 2.1 3.2 5 4.5.7.3 1.2.5 1.7.6.7.2 1.3.2 1.8.1.6-.1 1.7-.7 1.9-1.3.2-.7.2-1.2.2-1.3-.1-.2-.3-.3-.6-.4z"/>'
      '<path d="M12 2C6.5 2 2 6.5 2 12c0 1.8.5 3.5 1.3 5L2 22l5.1-1.3c1.4.8 3.1 1.2 4.9 1.2 5.5 0 10-4.5 10-10S17.5 2 12 2zm0 18.2c-1.6 0-3.1-.4-4.4-1.2l-.3-.2-3 .8.8-2.9-.2-.3C4 15 3.6 13.5 3.6 12 3.6 7.4 7.4 3.6 12 3.6S20.4 7.4 20.4 12 16.6 20.2 12 20.2z"/></svg>')


def ikon(ad, s=4.4, renk=TEAL, kalinlik=1.7):
    return (f'<svg viewBox="0 0 24 24" style="width:{s}mm;height:{s}mm;flex:none" fill="none" stroke="{renk}" '
            f'stroke-width="{kalinlik}" stroke-linecap="round" stroke-linejoin="round">{IKON[ad]}</svg>')


def tik(s=3.6, zemin=MERCAN, cizgi="#fff"):
    return (f'<svg viewBox="0 0 24 24" style="width:{s}mm;height:{s}mm;flex:none"><circle cx="12" cy="12" r="12" fill="{zemin}"/>'
            f'<path d="M6.5 12.5l3.6 3.6L17.5 8.7" fill="none" stroke="{cizgi}" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/></svg>')


CSS = f"""
@font-face {{ font-family: Mont; src: url("file://{FONT}"); font-weight: 100 900; }}
@font-face {{ font-family: Fr; src: url("file://{os.path.join(ROOT, "brand-source", "fonts", "Fraunces-600.ttf")}"); font-weight: 600; }}
@font-face {{ font-family: Fr; src: url("file://{os.path.join(ROOT, "brand-source", "fonts", "Fraunces-700.ttf")}"); font-weight: 700; }}
@page {{ size: {3 * PANEL + 2 * TASMA}mm {BOY + 2 * TASMA}mm; margin: 0; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ font-family:Mont,sans-serif; -webkit-font-smoothing:antialiased; color:#1f2f35;
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
.ust {{ font-size:6.6pt; font-weight:700; letter-spacing:.26em; color:{MERCAN}; text-transform:uppercase; }}
.fr {{ font-family:Fr,serif; font-weight:700; letter-spacing:-.01em; }}
.metin {{ font-size:7.7pt; line-height:1.5; font-weight:500; color:#34405c; }}
.kilavuz {{ position:absolute; top:0; bottom:0; width:0; border-left:.35mm dashed #e1262f; z-index:50; }}
.kilavuz-kirp {{ position:absolute; left:{TASMA}mm; top:{TASMA}mm; width:{3 * PANEL}mm; height:{BOY}mm; outline:.3mm solid #18a558; z-index:50; }}
.etiket {{ position:absolute; top:{TASMA + 1.5}mm; z-index:51; background:#e1262f; color:#fff; font-size:6pt; font-weight:700; padding:.6mm 1.6mm; border-radius:1mm; }}
"""


# ---------------------------------------------------------------- DIŞ YÜZ ----

def p_daire_tipleri():
    tipler = [
        ("1+0", "28 m²", "Akıllı tasarım, maksimum konfor", "01-1plus0-salon.webp"),
        ("1+1", "50 m²", "Ferah, konforlu ve fonksiyonel", "05-1plus1-salon.webp"),
        ("1+1 Bahçe Loft", "50 m²", "Zemin katta kendi bahçeniz", "09-loft-salon.webp"),
        ("2+1 Bahçe Dubleks", "100 m²", "Bahçeniz, evinizin devamı", "11-dubleks-salon.webp"),
    ]
    h = "".join(f"""
    <div>
      <div style="position:relative;height:53mm;border-radius:21mm 21mm 2.4mm 2.4mm;overflow:hidden;box-shadow:0 1.4mm 3.4mm rgba(7,51,63,.22)">
        <img src="{IC(g)}" style="width:100%;height:100%;object-fit:cover">
        <div class="tek" style="position:absolute;left:50%;bottom:2.4mm;transform:translateX(-50%);background:{MERCAN};color:#fff;font-size:6.6pt;font-weight:800;
             padding:.8mm 2.6mm;border-radius:99mm">Brüt {m2}</div>
      </div>
      <div class="fr tek" style="margin-top:2.4mm;text-align:center;font-size:{'13' if len(t) < 5 else '9.4'}pt;color:{TEAL};line-height:1.1">{t}</div>
      <div style="margin-top:.9mm;text-align:center;font-size:6.2pt;font-weight:500;line-height:1.35;color:#4b5d63">{slogan}</div>
    </div>""" for t, m2, slogan, g in tipler)
    return f"""
  <div class="panel sol" style="left:{TASMA}mm">
    <div class="z" style="background:{KUM}">
      <div style="position:absolute;right:-16mm;top:-14mm;width:46mm;height:46mm;border-radius:50%;border:7mm solid rgba(23,162,180,.14)"></div>
    </div>
    <div class="a" style="left:7mm;right:7mm;top:9mm">
      <div class="ust">Daire Tipleri</div>
      <div class="fr" style="margin-top:2mm;font-size:17pt;line-height:1.1;color:{TEAL}">Size uygun bir ev<br><span style="font-style:italic;color:{MERCAN}">mutlaka var</span></div>
    </div>
    <div class="a" style="left:7mm;right:7mm;top:36mm;display:grid;grid-template-columns:1fr 1fr;gap:5.6mm 3.4mm">{h}</div>
    <div class="a tek" style="left:7mm;right:7mm;top:181mm;text-align:center;background:{TEAL};color:#fff;border-radius:99mm;padding:1.9mm 0;font-size:7pt;font-weight:700">
      Zemin katlarda özel bahçeli daire seçenekleri</div>
    <div class="a tek" style="left:7mm;right:7mm;top:191.6mm;text-align:center;font-size:5.4pt;font-weight:500;color:#7b898d">İç mekân görselleri örnek tasarımdır.</div>
  </div>"""


def p_odeme():
    yoklar = ["Faiz yok", "Banka yok", "Kredi yok", "Kefil yok", "Ara ödeme yok", "Vade farkı yok"]
    y = "".join(f'<div style="display:flex;align-items:center;gap:1.8mm;font-size:7.8pt;font-weight:700">{tik(3.5, SARI, TEAL2)}{t}</div>' for t in yoklar)
    adimlar = [("1", "Dairenizi seçin", "Satış ofisinde size uygun tipi belirleyin."),
               ("2", "Peşinatınızı ödeyin", "699.000 TL'den başlayan peşinatla yerinizi ayırtın."),
               ("3", "60 ayda tamamlayın", "Kalanı sabit taksitlerle ödeyin; taksitiniz değişmez.")]
    a = "".join(f'<div style="display:flex;gap:2.6mm;align-items:flex-start"><span class="fr" style="width:7.4mm;height:7.4mm;border-radius:50%;background:#fff;'
                f'color:{TEAL};font-size:11pt;display:flex;align-items:center;justify-content:center;flex:none;line-height:1">{n}</span>'
                f'<div><div style="font-size:8.2pt;font-weight:800">{b}</div><div style="margin-top:.4mm;font-size:6.6pt;font-weight:500;line-height:1.38;opacity:.9">{t}</div></div></div>'
                for n, b, t in adimlar)
    return f"""
  <div class="panel" style="left:{TASMA + PANEL}mm;color:#fff">
    <div class="z" style="background:linear-gradient(165deg,{TURK} 0%,{TEAL} 62%,{TEAL2} 100%)">
      <div style="position:absolute;left:-22mm;top:{TASMA + 96}mm;width:60mm;height:60mm;border-radius:50%;border:8mm solid rgba(255,255,255,.07)"></div>
    </div>
    <div class="a" style="left:7mm;right:7mm;top:9mm">
      <div class="ust" style="color:{SARI}">Ödeme Planı</div>
      <div class="fr" style="margin-top:2.2mm;font-size:20pt;line-height:1.1">Banka <i style="color:{SARI}">yok.</i><br>Faiz <i style="color:{SARI}">yok.</i> Kefil <i style="color:{SARI}">yok.</i></div>
    </div>
    <div class="a" style="left:19mm;top:37mm;width:62mm;height:62mm;border-radius:50%;background:#fff;color:{TEAL};display:flex;flex-direction:column;align-items:center;justify-content:center;
         box-shadow:0 3mm 7mm rgba(4,35,44,.35)">
      <div class="tek" style="font-size:7pt;font-weight:700;letter-spacing:.2em;color:{MERCAN}">SADECE</div>
      <div class="k tek" style="margin-top:.6mm;font-size:27pt;font-weight:900">699.000</div>
      <div class="tek" style="margin-top:.6mm;font-size:7.6pt;font-weight:700">TL'den başlayan</div>
      <div class="k tek" style="margin-top:.5mm;font-size:13pt;font-weight:900;letter-spacing:.04em">PEŞİNAT</div>
      <div style="height:7mm"></div>
    </div>
    <div class="a k tek" style="left:14mm;right:14mm;top:89.5mm;background:{MERCAN};color:#fff;border-radius:99mm;padding:2.6mm 0 2.4mm;text-align:center;font-size:12.4pt;font-weight:900;
         box-shadow:0 2mm 4mm rgba(4,35,44,.35)">60 AY SABİT TAKSİT</div>
    <div class="a" style="left:9mm;right:7mm;top:108mm;display:grid;grid-template-columns:1fr 1fr;gap:2.3mm 2mm">{y}</div>
    <div class="a" style="left:7mm;right:7mm;top:130.5mm;height:.25mm;background:rgba(255,255,255,.28)"></div>
    <div class="a" style="left:7mm;right:7mm;top:135mm">
      <div class="ust" style="color:{SARI}">3 Adımda Ev Sahibi Olun</div>
      <div style="margin-top:3mm;display:flex;flex-direction:column;gap:3mm">{a}</div>
    </div>
    <div class="a" style="left:7mm;right:7mm;top:181.5mm;display:flex;gap:2.2mm;align-items:center;background:rgba(255,255,255,.1);border-radius:2mm;padding:2.2mm 2.8mm">
      {ikon('kalkan', 5.6, SARI, 1.7)}
      <div style="font-size:6.1pt;font-weight:500;line-height:1.4">S.S. Yahya Kaptan Birlik Yapı Kooperatifi, T.C. Ticaret Bakanlığı bünyesindeki <b>KOOPBİS</b>'e kayıtlıdır.</div>
    </div>
  </div>"""


def p_on_kapak():
    return f"""
  <div class="panel sag" style="left:{TASMA + 2 * PANEL}mm;color:#fff">
    <div class="z" style="background:linear-gradient(180deg,{TEAL} 0%,{TEAL2} 100%)">
      <div style="position:absolute;left:-20mm;top:-18mm;width:56mm;height:56mm;border-radius:50%;border:8mm solid rgba(23,162,180,.22)"></div>
      <div style="position:absolute;left:9mm;top:{TASMA + 64}mm;width:82mm;height:113mm;border-radius:41mm 41mm 0 0;background:{KUM}"></div>
      <div style="position:absolute;left:10.4mm;top:{TASMA + 65.4}mm;width:79.2mm;height:112mm;border-radius:39.6mm 39.6mm 0 0;overflow:hidden">
        <img src="{F('signage-source', 'courtyard-pools.jpg')}" style="width:100%;height:100%;object-fit:cover;object-position:50% 50%"></div>
      <img src="{F('signage-source', 'aile', 'aile2-kesik.png')}" style="position:absolute;left:1mm;top:{TASMA + 103}mm;height:73mm;filter:drop-shadow(0 2mm 3mm rgba(4,35,44,.4))">
      <div style="position:absolute;left:0;right:0;top:{TASMA + 174}mm;bottom:0;background:{TEAL2}"></div>
    </div>
    <div class="a" style="left:0;right:0;top:8mm;display:flex;justify-content:center"><img src="{V('mia-beyaz.svg')}" style="width:25mm"></div>
    <div class="a" style="left:0;right:0;top:31mm;text-align:center">
      <div class="fr tek" style="font-size:15pt;font-weight:600;font-style:italic;color:{SARI};line-height:1">Ailenize</div>
      <div class="fr tek" style="margin-top:1.2mm;font-size:27pt;line-height:1">yeni bir yuva</div>
      <div class="tek" style="margin-top:2.6mm;font-size:6.2pt;font-weight:600;letter-spacing:.26em;opacity:.8">İZMİT · MİA BÖLGESİ</div>
    </div>
    <div class="a" style="right:3mm;top:58mm;width:36mm;height:36mm;border-radius:50%;background:{MERCAN};display:flex;flex-direction:column;align-items:center;justify-content:center;
         transform:rotate(8deg);box-shadow:0 2mm 5mm rgba(4,35,44,.45);border:.8mm solid {KUM}">
      <div class="k tek" style="font-size:15.5pt;font-weight:900">699.000</div>
      <div class="tek" style="margin-top:.5mm;font-size:5.6pt;font-weight:800;letter-spacing:.04em">TL'DEN BAŞLAYAN</div>
      <div class="k tek" style="margin-top:.3mm;font-size:9.6pt;font-weight:900">PEŞİNAT</div>
    </div>
    <div class="a k tek" style="left:0;right:0;top:177.6mm;text-align:center;font-size:12pt;font-weight:900;color:{SARI}">60 AY SABİT TAKSİT</div>
    <div class="a tek" style="left:0;right:0;top:183.6mm;text-align:center;font-size:6.6pt;font-weight:600;letter-spacing:.04em">Banka yok · Faiz yok · Kefil yok · Ara ödeme yok</div>
    <div class="a" style="left:0;right:0;top:188.4mm;display:flex;align-items:center;justify-content:center;gap:1.8mm">{ikon('tel', 4.6, '#fff', 2.2)}
      <span class="k tek" style="font-size:15pt;font-weight:900">444 10 58</span></div>
  </div>"""


# ----------------------------------------------------------------- İÇ YÜZ ----

NEDENLER = [
    ("Merkezi konum", "D-100 Karayolu'na 1 dakika; şehir merkezine, şehir hastanesine ve TEM'e 5 dakika. AVM'ler ve üniversite hemen yakınınızda."),
    ("Bankasız, faizsiz ödeme", "699.000 TL'den başlayan peşinat, kalanı 60 ay sabit taksit. Ara ödeme, kefil ve vade farkı yok; taksitiniz baştan sona değişmez."),
    ("Depreme dayanıklı yapı", "Bloklar fore kazık temel sistemiyle, deprem güvenliği her şeyin üstünde tutularak inşa ediliyor."),
    ("Kooperatif güvencesi", "Kâr amacı gütmeyen kooperatif modeliyle maliyetine konut. Kooperatif, e-Devlet ve KOOPBİS üzerinden izlenebilir; devlet denetimine tabidir."),
    ("Zengin sosyal yaşam", "Kapalı yüzme havuzu, fitness salonu, sauna ve Türk hamamı, çocuk oyun parkı: hepsi sitenin içinde."),
    ("Yeşil ve ferah avlu", "Süs havuzları, geniş peyzaj alanları ve yürüyüş yollarıyla çevrili merkezi avlu; akşamları özel aydınlatma."),
    ("Güven ve konfor", "7/24 güvenlik ve kapalı otopark. Zemin katlarda bahçeli dairelerle apartmanda müstakil ev hissi."),
    ("Değerlenen bölge", "İzmit MİA Bölgesi şehrin yeni gelişim aksı; hem yaşamak hem yatırım yapmak isteyenlerin ilgi odağı."),
]


NEDEN_IKON = ["pin", "yuzde", "bina", "banka", "damla", "agac", "kalkan", "artis"]


def neden_satirlari(bas, top):
    """Dört neden kartı: mercan numara, başlık, açıklama, köşede ikon."""
    return "".join(f"""
    <div class="a" style="left:6mm;right:6mm;top:{top + i * 34}mm;height:31mm;background:#fff;border-radius:3mm;box-shadow:0 1.2mm 3.2mm rgba(7,51,63,.1);
         display:flex;gap:3mm;align-items:center;padding:0 3.4mm 0 3.6mm">
      <div class="fr" style="width:14.5mm;flex:none;font-size:29pt;line-height:1;color:{MERCAN}">{bas + i:02d}</div>
      <div style="flex:1"><div style="display:flex;align-items:center;justify-content:space-between;gap:2mm">
          <div style="font-size:10.4pt;font-weight:800;color:{TEAL};line-height:1.12">{b}</div>
          <span style="width:7.6mm;height:7.6mm;border-radius:50%;background:rgba(23,162,180,.14);display:flex;align-items:center;justify-content:center;flex:none">{ikon(NEDEN_IKON[bas + i - 1], 4.3, TEAL, 1.8)}</span></div>
        <div style="margin-top:1.2mm;font-size:7.2pt;font-weight:500;line-height:1.44;color:#3d4f55">{t}</div></div>
    </div>""" for i, (b, t) in enumerate(NEDENLER[bas - 1:bas + 3]))


def p_neden_sol():
    return f"""
  <div class="panel sol" style="left:{TASMA}mm">
    <div class="z" style="background:{KUM}">
      <div style="position:absolute;left:-20mm;top:-22mm;width:54mm;height:54mm;border-radius:50%;background:rgba(23,162,180,.12)"></div>
    </div>
    <div class="a" style="left:7mm;right:7mm;top:9mm">
      <div class="ust">8 Neden</div>
      <div class="fr tek" style="margin-top:1.6mm;font-size:22pt;font-weight:600;font-style:italic;color:{MERCAN};line-height:1">Neden</div>
      <div class="k tek" style="margin-top:1.4mm;font-size:18.5pt;font-weight:900;color:{TEAL}">MİA PARK OCEAN?</div>
      <div style="margin-top:3mm;font-size:7.4pt;font-weight:500;line-height:1.48;color:#3d4f55">İzmit'in gelişen MİA Bölgesi'nde; ulaşımı kolay, sosyal alanları zengin,
        ödemesi rahat bir yaşam. İşte burayı seçmeniz için sekiz neden.</div>
    </div>
    {neden_satirlari(1, 58.5)}
  </div>"""


def p_neden_sag():
    return f"""
  <div class="panel" style="left:{TASMA + PANEL}mm">
    <div class="z" style="background:{KUM}"></div>
    <div class="a" style="left:7mm;top:8mm;width:86mm;height:44mm;border-radius:43mm 43mm 2.4mm 2.4mm;overflow:hidden;box-shadow:0 1.6mm 4mm rgba(7,51,63,.22)">
      <img src="{F('signage-source', 'entrance-gate.jpg')}" style="width:100%;height:100%;object-fit:cover;object-position:40% 62%"></div>
    <div class="a" style="right:5mm;top:39mm;width:19mm;height:19mm;border-radius:50%;background:{MERCAN};color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;
         transform:rotate(-8deg);box-shadow:0 1.2mm 3mm rgba(7,51,63,.3);border:.6mm solid {KUM}">
      <div class="k" style="font-size:12pt;font-weight:900;line-height:1">600</div><div style="font-size:5.4pt;font-weight:800;letter-spacing:.08em">DAİRE</div></div>
    {neden_satirlari(5, 58.5)}
  </div>"""


def p_arka_kapak(qr, ykb):
    satir = lambda i, t: f'<div style="display:flex;align-items:flex-start;gap:2.4mm;font-size:7.6pt;font-weight:600;color:{TEAL2};line-height:1.4">{i}<span>{t}</span></div>'
    logo = lambda etiket, img: (f'<div style="flex:1;text-align:center"><div style="font-size:5pt;font-weight:700;letter-spacing:.14em;color:#7b898d">{etiket}</div>'
                                f'<div style="height:14mm;display:flex;align-items:center;justify-content:center;margin-top:1mm">{img}</div></div>')
    return f"""
  <div class="panel sag" style="left:{TASMA + 2 * PANEL}mm">
    <div class="z" style="background:#fff">
      <div style="position:absolute;left:-12%;right:-12%;top:-20mm;height:{TASMA + 88}mm;border-radius:0 0 50% 50%;overflow:hidden">
        <img src="{F('signage-source', 'night-gate-temiz.jpg')}" style="width:100%;height:100%;object-fit:cover;object-position:50% 70%">
        <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(7,51,63,.93) 30%,rgba(11,74,90,.8) 100%)"></div>
      </div>
    </div>
    <div class="a" style="left:0;right:0;top:7mm;display:flex;justify-content:center"><img src="{V('mia-beyaz.svg')}" style="width:22mm"></div>
    <div class="a" style="left:0;right:0;top:27mm;text-align:center;color:#fff">
      <div class="fr tek" style="font-size:12pt;font-weight:600;font-style:italic;color:{SARI}">Sizi bekliyoruz</div>
      <div class="k tek" style="margin-top:1.4mm;font-size:29pt;font-weight:900;letter-spacing:.01em">444 10 58</div>
      <div style="margin-top:2mm;display:flex;align-items:center;justify-content:center;gap:1.6mm">{WA.format(s=4.4)}
        <span class="tek" style="font-size:10.5pt;font-weight:700;letter-spacing:.03em">0540 028 00 41</span></div>
    </div>

    <div class="a" style="left:7mm;right:7mm;top:74mm">
      <div class="ust">Satış Ofisi</div>
      <div style="margin-top:2.4mm;display:flex;flex-direction:column;gap:2mm">
        {satir(ikon('pin', 4.2, TEAL), 'Ömerağa Mah. Abdurrahman Yüksel Cad.<br>Bana Bak Ap. No:15/4 İzmit / Kocaeli')}
        {satir(ikon('tel', 4.2, TEAL), '0541 128 40 41')}
        {satir(ikon('kure', 4.2, TEAL), 'miaparkocean.com')}
        {satir(ikon('insta', 4.2, TEAL), '@miaparkocean')}
      </div>
    </div>

    <div class="a" style="left:7mm;right:7mm;top:115mm;border-radius:2.6mm;background:{KUM};padding:3.6mm;display:flex;align-items:center;gap:3.6mm">
      <img src="file://{qr}" style="width:27mm;height:27mm;flex:none">
      <div><div class="fr" style="font-size:10pt;color:{TEAL};line-height:1.15">Projeyi telefonunuzdan inceleyin</div>
        <div style="margin-top:1.4mm;font-size:6.5pt;font-weight:500;line-height:1.42;color:#3d4f55">Kamerayı kodun üzerine tutun; daire tipleri, kat planları ve galeri karşınızda.</div></div>
    </div>

    <div class="a" style="left:6mm;right:6mm;top:155mm;display:flex;align-items:flex-start;gap:1mm">
      {logo('YAPIMCI', f'<img src="file://{ykb}" style="height:14mm">')}
      {logo('MÜTEAHHİT', f'<img src="{V("tilda.svg")}" style="width:25mm">')}
      {logo('TEK YETKİLİ SATICI', f'<img src="{V("ocean-lacivert.svg")}" style="width:21mm">')}
    </div>
    <div class="a" style="left:7mm;right:7mm;top:179.5mm;font-size:5pt;font-weight:500;line-height:1.45;color:#7b898d;text-align:center">
      Yapımcı: S.S. Yahya Kaptan Birlik Yapı Kooperatifi · Müteahhit: Tilda İnşaat · Tek Yetkili Satıcı: Ocean Gayrimenkul.
      Görseller tanıtım amaçlıdır; uygulamada değişiklik olabilir. Güncel ödeme planı ve kampanya koşulları için satış ofisimizle görüşünüz.</div>
  </div>"""


def belge(qr, ykb, kilavuz=False):
    k1 = k2 = ""
    if kilavuz:
        cizgi = "".join(f'<div class="kilavuz" style="left:{TASMA + i * PANEL}mm"></div>' for i in (1, 2)) + '<div class="kilavuz-kirp"></div>'
        et = lambda adlar: "".join(f'<div class="etiket" style="left:{TASMA + i * PANEL + 1.5}mm">{a}</div>' for i, a in enumerate(adlar))
        k1 = cizgi + et(["DIŞ YÜZ · sol panel", "DIŞ YÜZ · orta panel", "ÖN KAPAK"])
        k2 = cizgi + et(["İÇ YÜZ · neden 1-4", "İÇ YÜZ · neden 5-8", "ARKA KAPAK"])
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>'
            f'<div class="sayfa" id="dis">{p_daire_tipleri()}{p_odeme()}{p_on_kapak()}{k1}</div>'
            f'<div class="sayfa" id="ic">{p_neden_sol()}{p_neden_sag()}{p_arka_kapak(qr, ykb)}{k2}</div></body></html>')


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
    segno.make("https://miaparkocean.com/", error="q").save(qr, scale=10, border=1, dark=TEAL2, light=None)
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
