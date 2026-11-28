#!/usr/bin/env python3
"""
Akordiyon (zikzak) kırımlı satış broşürü — 4 panel × 20×30 cm, açık 80×30 cm, çift yüz.

Baskı PDF'i: 806×306 mm (her kenarda 3 mm taşma), 2 sayfa. Kırımlar taşmalı sayfada x = 203, 403, 603 mm.
Metinler vektör; görseller RGB (matbaa CMYK'ye çevirir).

Kırım: 1-2 arası vadi, 2-3 arası dağ, 3-4 arası vadi (iç yüze göre). Kapalıyken dışta kalan iki yüz
dış yüzün iki uç panelidir: sağ uç ÖN KAPAK, sol uç ARKA KAPAK.

  İÇ YÜZ (sayfa 1) — açılınca tek kompozisyon (müşterinin gönderdiği örnek, ref/brosur-80x30/referans.jpg):
      Daire Tipleri 1+0 · 1+1  |  proje görseli (iki panel boyunca) + olanaklar + yakınlıklar  |  2+1 Bahçe Dubleks
  DIŞ YÜZ (sayfa 2) soldan sağa:
      ARKA KAPAK (iletişim)  |  Fiyat ve ödeme planı  |  Konum haritası  |  ÖN KAPAK
      (ortadaki iki panelin zemini tek harita)

Kaynaklar (baski/brosur-akordiyon-80x30/kaynak/): ana-gorsel.png (örnekteki açıyla yeniden üretildi; mimari
projenin kendi render'ından), plan-*.png (kat planları), palmiye.png. Harita: Sentinel-2 cloudless 2016, EOX — CC BY 4.0.

    SSL_CERT_FILE=/root/.ccr/ca-bundle.crt python3.13 scripts/build-brosur-akordiyon-80x30.py
"""

import importlib.util
import json
import math
import os
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import segno
from PIL import Image, ImageFilter

KOK = os.path.dirname(os.path.abspath(__file__))


def _modul(ad, dosya):
    spec = importlib.util.spec_from_file_location(ad, os.path.join(KOK, dosya))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


eski = _modul("eski", "build-brosur-akordiyon.py")      # ikonlar, WhatsApp işareti, PDF çizici
rd = _modul("rd", "build-reel-drone.py")                # uydu karoları, metro güzergâhları

ROOT = eski.ROOT
OUT = os.path.join(ROOT, "baski", "brosur-akordiyon-80x30")
KAYNAK = os.path.join(OUT, "kaynak")
F, V = eski.F, eski.V
# Marka renkleri: brand-source/mia-brand.css ve sitenin globals.css'i. Düz turkuaz, altın, pembe yok.
DERIN, PETROL, OKYANUS, AQUA, BUZ = "#04283a", "#095678", "#1a7496", "#92d1df", "#ddf7fa"
LACI, LACI2, ALTIN, KREM = PETROL, DERIN, AQUA, "#f2f9fb"
METAL = ("linear-gradient(110deg,#075878 0%,#1a7496 10%,#48abc5 20%,#b8e4ec 31%,#f1fcfd 38%,#6ebdd0 49%,"
         "#2c94b4 58%,#095678 68%,#48abc5 79%,#ddf7fa 90%,#2c94b4 100%)")
DERIN_G = "linear-gradient(178deg,#12688c 0%,#0d5b7d 18%,#095678 40%,#06455f 70%,#04283a 100%)"
YUZEY_G = "linear-gradient(145deg,#04283a 0%,#06405a 26%,#095678 54%,#12688c 80%,#1a7496 100%)"
LOGO_ORAN = 0.7
LOGO = "file://" + os.path.join(ROOT, "baski", "brosur-akordiyon-80x30", "kaynak", "logo-mia.png")      # asıl metalik logo
DALGA = "file://" + os.path.join(ROOT, "public", "brand", "wave.png")                                   # marka dalgası
TASMA, PANEL, BOY, N = 3, 200, 300, 4
GEN = N * PANEL + 2 * TASMA          # 806
YUK = BOY + 2 * TASMA                # 306
KIRIM = [TASMA + i * PANEL for i in (1, 2, 3)]

# Fiyatlar (kampanya): tip, ad, peşinat, aylık taksit
FIYAT = [("1+0", "Stüdyo", "699.000", "29.900"), ("1+1", "Daire", "999.000", "39.900"), ("2+1", "Bahçe Dubleks", "2.000.000", "50.000")]
# Metrekareler müşterinin örnek görselinden; baskıdan önce teyit edilmeli (sitede 1+1 brüt 50, 2+1 brüt 100 yazıyor).
M2 = {"1+0": ("28", "23"), "1+1": ("100", "72"), "2+1": ("150", "110")}
YAKIN = [  # (ad, süre, enlem, boylam, etiketin tarafı, dikey kaydırma mm)
    ("Sahil", "2 dk", 40.7367, 29.9395, "sol", 0),
    ("41 Burda AVM", "2 dk", 40.75675, 29.94756, "sol", 0),
    ("İzmit Outlet Center", "2 dk", 40.75548, 29.94690, "sol", 8.6),
    ("Symbol AVM", "7 dk", 40.75787, 29.97956, "sol", 0),
    ("Şehir Merkezi", "5 dk", 40.77211, 29.95056, "sol", 0),
    ("Şehir Hastanesi", "5 dk", 40.78309, 29.96064, "sag", 0),
    ("Kocaeli Üniversitesi", "10 dk", 40.81874, 29.92291, "sag", 0),
]

IKON = dict(eski.IKON)
IKON.update({
    "katman": '<path d="M12 2 2 7l10 5 10-5-10-5z"/><path d="m2 12 10 5 10-5"/><path d="m2 17 10 5 10-5"/>',
    "yaprak": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.5 19 2c1 2 2 4.2 2 8 0 5.5-4.8 10-10 10z"/><path d="M2 21c0-3 1.9-5.4 5.1-6 2.4-.5 4.9-2 5.9-3"/>',
    "gunes": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M6.3 17.7l-1.4 1.4M19.1 4.9l-1.4 1.4"/>',
    "kahve": '<path d="M17 8h1a4 4 0 1 1 0 8h-1"/><path d="M3 8h14v9a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4z"/><path d="M6 2v2M10 2v2M14 2v2"/>',
    "koltuk": '<path d="M20 9V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v3"/><path d="M2 11v5a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-5a2 2 0 0 0-4 0v2H6v-2a2 2 0 0 0-4 0z"/><path d="M4 18v2M20 18v2"/>',
    "mutfak": '<path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3zm0 0v7"/>',
    "banyo": '<path d="M9 6 6.5 3.5a1.5 1.5 0 0 0-1-.5C4.7 3 4 3.7 4 4.5V17a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-5"/><path d="M2 12h20"/><path d="M7 19v2M17 19v2"/>',
    "balkon": '<path d="M4 4v17M20 4v17M4 12h16M4 21h16"/><path d="M8 12v9M12 12v9M16 12v9"/><path d="M7 4h10v8"/>',
    "yatak": '<path d="M2 4v16"/><path d="M2 8h18a2 2 0 0 1 2 2v10"/><path d="M2 17h20"/><path d="M6 8v9"/>',
    "asansor": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M12 3v18"/><path d="m6 10.5 1.8-2.2 1.8 2.2M14.4 13.5l1.8 2.2 1.8-2.2"/>',
    "otopark": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M9 17V7h4a3 3 0 0 1 0 6H9"/>',
    "filiz": '<path d="M7 20h10"/><path d="M10 20c5.5-2.5.8-6.4 3-10"/><path d="M9.5 9.4c1.1.8 1.8 2.2 2.3 3.7-2 .4-3.5.4-4.8-.3-1.2-.6-2.3-1.9-3-4.2 2.8-.5 4.4 0 5.5.8z"/><path d="M14.1 6a7 7 0 0 0-1.1 4c1.9-.1 3.3-.6 4.3-1.4 1-1 1.6-2.3 1.7-4.6-2.7.1-4 1-4.9 2z"/>',
    "merdiven": '<path d="M3 20h4v-4h4v-4h4V8h4V4h2"/><path d="m17 12 3-3 0 3"/>',
    "kure2": IKON["kure"],
})


def ikon(ad, s=6, renk=LACI, kalinlik=1.6):
    return (f'<svg viewBox="0 0 24 24" style="width:{s}mm;height:{s}mm;flex:none" fill="none" stroke="{renk}" '
            f'stroke-width="{kalinlik}" stroke-linecap="round" stroke-linejoin="round">{IKON[ad]}</svg>')


FONT = lambda ad: os.path.join(ROOT, "brand-source", "fonts", ad)
CSS = f"""
@font-face {{ font-family: Mn; src: url("file://{FONT('Manrope-400.ttf')}"); font-weight: 400; }}
@font-face {{ font-family: Mn; src: url("file://{FONT('Manrope-600.ttf')}"); font-weight: 600; }}
@font-face {{ font-family: Mn; src: url("file://{FONT('Manrope-700.ttf')}"); font-weight: 700; }}
@font-face {{ font-family: Fr; src: url("file://{FONT('Fraunces-500.ttf')}"); font-weight: 500; }}
@font-face {{ font-family: Fr; src: url("file://{FONT('Fraunces-600.ttf')}"); font-weight: 600; }}
@font-face {{ font-family: Fr; src: url("file://{FONT('Fraunces-700.ttf')}"); font-weight: 700; }}
@page {{ size: {GEN}mm {YUK}mm; margin: 0; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ font-family:Mn,sans-serif; -webkit-font-smoothing:antialiased; color:{LACI};
              -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
.sayfa {{ position:relative; width:{GEN}mm; height:{YUK}mm; overflow:hidden; page-break-after:always; background:#fff; }}
.sayfa:last-child {{ page-break-after:auto; }}
.a {{ position:absolute; }}
.tek {{ white-space:nowrap; }}
.fr {{ font-family:Fr,serif; font-weight:700; letter-spacing:-.01em; }}
.ust {{ font-weight:700; letter-spacing:.3em; text-transform:uppercase; }}
.kilavuz {{ position:absolute; top:0; bottom:0; width:0; border-left:.4mm dashed #e1262f; z-index:50; }}
.kilavuz-kirp {{ position:absolute; left:{TASMA}mm; top:{TASMA}mm; width:{N * PANEL}mm; height:{BOY}mm; outline:.35mm solid #18a558; z-index:50; }}
.etiket {{ position:absolute; top:{TASMA + 1.5}mm; z-index:51; background:#e1262f; color:#fff; font-size:7pt; font-weight:700; padding:.8mm 2mm; border-radius:1mm; }}
"""

X = lambda panel, x=0.0: TASMA + panel * PANEL + x          # panel içi mm → sayfa mm


# ---------------------------------------------------------------- İÇ YÜZ ----
def baslik_daire(panel):
    return (f'<div class="a" style="left:{X(panel, 14)}mm;top:17mm;width:{PANEL - 28}mm;display:flex;align-items:center;gap:5mm">'
            f'<span style="flex:1;height:.3mm;background:{ALTIN}"></span>'
            f'<span class="tek" style="font-size:14pt;font-weight:600;letter-spacing:.34em;color:{LACI}">DAİRE TİPLERİ</span>'
            f'<span style="flex:1;height:.3mm;background:{ALTIN}"></span></div>')


def tip_kutusu(panel, y, tip, ad):
    brut, net = M2[tip]
    return (f'<div class="a" style="left:{X(panel, 14)}mm;top:{y}mm;width:{PANEL - 28}mm;height:19mm;border:.3mm solid {ALTIN};border-radius:3mm;background:#fff;'
            f'display:flex;align-items:center;padding:0 6mm 0 5mm">'
            f'<span class="fr tek" style="font-size:33pt;line-height:1;color:{LACI}">{tip}</span>'
            f'<span class="tek" style="margin-left:4.5mm;font-size:{17 if len(ad) < 9 else 15}pt;font-weight:600;color:{LACI}">{ad}</span>'
            f'<span style="flex:1"></span><span style="width:.3mm;height:11mm;background:{ALTIN};margin-right:5mm"></span>'
            f'<span style="font-size:9pt;font-weight:500;line-height:1.5;color:{LACI}"><span class="tek">Brüt <b style="font-size:11pt">{brut} m²</b></span><br>'
            f'<span class="tek">Net&nbsp; <b style="font-size:11pt">{net} m²</b></span></span></div>')


def fiyat_seridi(panel, y, pesin, ayda):
    hucre = lambda et, deger, ek="": (f'<div style="flex:1;padding-left:6mm"><div class="tek" style="font-size:6.6pt;font-weight:700;letter-spacing:.24em;color:{ALTIN}">{et}</div>'
                                      f'<div class="tek" style="margin-top:.9mm;font-size:16pt;font-weight:800;line-height:1;color:#fff">{deger}<span style="font-size:9pt;font-weight:700;margin-left:1.2mm">TL</span>{ek}</div></div>')
    return (f'<div class="a" style="left:{X(panel, 14)}mm;top:{y}mm;width:{PANEL - 28}mm;height:17mm;border-radius:3mm;background:{YUZEY_G};display:flex;align-items:center;'
            f'box-shadow:0 1.4mm 3.6mm rgba(4,40,58,.25)">'
            + hucre("PEŞİNAT", pesin) + f'<span style="width:.3mm;height:10mm;background:rgba(146,209,223,.6)"></span>' + hucre("AYLIK TAKSİT", ayda)
            + f'<div class="tek" style="margin-right:5mm;padding:2.2mm 3.6mm 2mm;border-radius:99mm;background:{BUZ};color:{DERIN};font-size:9pt;font-weight:800;letter-spacing:.06em">60 AY</div></div>')


def ozellik_listesi(x, y, maddeler, ara=11.0):
    return "".join(f'<div class="a" style="left:{x}mm;top:{y + i * ara}mm;display:flex;align-items:center;gap:3.4mm">{ikon(ik, 7.2, LACI, 1.5)}'
                   f'<span class="tek" style="font-size:11.5pt;font-weight:600;color:{LACI}">{t}</span></div>' for i, (ik, t) in enumerate(maddeler))


def ic_sol():
    k = lambda ad: "file://" + os.path.join(KAYNAK, ad)
    return (baslik_daire(0)
            + tip_kutusu(0, 31, "1+0", "Stüdyo")
            + f'<img class="a" src="{k("plan-1-0-m.png")}" style="left:{X(0, 8)}mm;top:55mm;width:112mm;height:66mm;object-fit:contain">'
            + ozellik_listesi(X(0, 126), 64, [("koltuk", "Yaşam Alanı"), ("mutfak", "Amerikan Mutfak"), ("banyo", "Banyo"), ("balkon", "Balkon")])
            + fiyat_seridi(0, 124, FIYAT[0][2], FIYAT[0][3])
            + tip_kutusu(0, 150, "1+1", "Daire")
            + f'<img class="a" src="{k("plan-1-1-m.png")}" style="left:{X(0, 8)}mm;top:173mm;width:112mm;height:66mm;object-fit:contain">'
            + ozellik_listesi(X(0, 126), 178, [("koltuk", "Salon"), ("mutfak", "Amerikan Mutfak"), ("yatak", "Yatak Odası"), ("banyo", "Banyo"), ("balkon", "Balkon")], 10.4)
            + fiyat_seridi(0, 241, FIYAT[1][2], FIYAT[1][3]))


def ic_sag():
    k = lambda ad: "file://" + os.path.join(KAYNAK, ad)
    plan = lambda x, ad, et: (f'<img class="a" src="{k(ad)}" style="left:{X(3, x)}mm;top:54mm;width:92mm;height:92mm;object-fit:contain">'
                              f'<div class="a tek" style="left:{X(3, x)}mm;top:147mm;width:92mm;text-align:center;font-size:8.6pt;font-weight:700;letter-spacing:.2em;color:{LACI}">{et}</div>')
    maddeler = [("filiz", "Özel<br>Bahçe"), ("koltuk", "Geniş<br>Yaşam Alanı"), ("yatak", "2 Yatak<br>Odası"), ("banyo", "2 Banyo"), ("merdiven", "Dubleks<br>Konforu")]
    ikonlar = "".join(f'<div style="flex:1;text-align:center"><div style="display:flex;justify-content:center">{ikon(ik, 9.6, LACI, 1.35)}</div>'
                      f'<div style="margin-top:2mm;font-size:9.2pt;font-weight:600;line-height:1.3;color:{LACI}">{t}</div></div>' for ik, t in maddeler)
    yok = "".join(f'<span class="tek" style="display:flex;align-items:center;gap:1.8mm">{eski.tik(4.2, PETROL, "#fff")}{t}</span>' for t in ("Banka yok", "Faiz yok", "Kefil yok", "Ara ödeme yok"))
    return (baslik_daire(3)
            + tip_kutusu(3, 31, "2+1", "Bahçe Dubleks")
            + plan(6, "plan-2-1-alt-m.png", "ALT KAT") + plan(102, "plan-2-1-ust-m.png", "ÜST KAT")
            + f'<div class="a" style="left:{X(3, 12)}mm;top:158mm;width:{PANEL - 24}mm;display:flex;align-items:flex-start">{ikonlar}</div>'
            + fiyat_seridi(3, 184, FIYAT[2][2], FIYAT[2][3])
            + f'<div class="a" style="left:{X(3, 14)}mm;top:209mm;width:{PANEL - 28}mm;text-align:center;font-size:11pt;font-weight:600;letter-spacing:.34em;line-height:1.75;color:{LACI}">'
              f'BAHÇELİ LOFT<br>YAŞAMIN AYRICALIĞI</div>'
            + f'<div class="a" style="left:{X(3, 14)}mm;top:231mm;width:{PANEL - 28}mm;border-radius:3mm;border:.3mm solid {ALTIN};background:#fff;padding:3.6mm 5mm 3.4mm;text-align:center">'
              f'<div class="tek" style="font-size:12pt;font-weight:800;letter-spacing:.08em;color:{LACI}">60 AY SABİT TAKSİT</div>'
              f'<div style="margin-top:2.4mm;display:flex;justify-content:space-between;font-size:8.4pt;font-weight:700;color:{LACI}">{yok}</div></div>')


def ic_orta():
    sol, orta = X(1), X(2)                                   # 203, 403 (kırım)
    lw = 88
    lh = lw * LOGO_ORAN
    baslik = (f'<img class="a" src="{LOGO}" style="left:{orta - lw / 2}mm;top:9mm;width:{lw}mm">'
              f'<div class="a tek" style="right:{GEN - orta + 5.5}mm;top:{13 + lh}mm;font-size:11pt;font-weight:600;letter-spacing:.36em;color:{PETROL}">MODERN YAŞAM</div>'
              f'<div class="a" style="left:{orta - 1.1}mm;top:{15.3 + lh}mm;width:2.2mm;height:2.2mm;border-radius:50%;background:{OKYANUS}"></div>'
              f'<div class="a tek" style="left:{orta + 7}mm;top:{13 + lh}mm;font-size:11pt;font-weight:600;letter-spacing:.36em;color:{PETROL}">DOĞRU YATIRIM</div>')
    kose = lambda x, yon: (f'<svg class="a" style="left:{x}mm;top:12mm;width:28mm;height:44mm" viewBox="0 0 28 44"><path d="{"M28 1H1v42" if yon == "sol" else "M0 1h27v42"}" '
                           f'fill="none" stroke="{OKYANUS}" stroke-width=".6"/></svg>')
    baslik += kose(orta - 150, "sol") + kose(orta + 122, "sag")
    # Görseldeki olanaklar: (x, ikon, iki satır yazı, çizginin indiği y)
    isaret = [(250, "katman", "Modern<br>Cephe Tasarımı", 176), (312, "balkon", "Geniş<br>Balkonlar", 186), (366, "gunes", "Mimari<br>LED Aydınlatma", 152),
              (440, "dalga", "Süs<br>Havuzları", 209), (494, "agac", "Peyzaj ve<br>Yeşil Alanlar", 131), (556, "kahve", "Kafe ve<br>Ticari Alanlar", 228)]
    cagri = ""
    y0 = 20 + lh
    for x, ik, yazi, y2 in isaret:
        cagri += (f'<div class="a" style="left:{x - 24}mm;top:{y0}mm;width:48mm;display:flex;flex-direction:column;align-items:center">'
                  f'<div style="width:12.5mm;height:12.5mm;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;'
                  f'box-shadow:0 1mm 3mm rgba(4,40,58,.25);border:.3mm solid {AQUA}">{ikon(ik, 7.2, PETROL, 1.5)}</div>'
                  f'<div style="margin-top:1.6mm;padding:1.3mm 2.8mm 1.1mm;border-radius:2mm;background:rgba(255,255,255,.94);text-align:center;'
                  f'font-size:9.4pt;font-weight:700;line-height:1.24;color:{PETROL};box-shadow:0 1mm 3mm rgba(4,40,58,.2)">{yazi}</div></div>'
                  f'<div class="a" style="left:{x - .15}mm;top:{y0 + 26}mm;width:.3mm;height:{y2 - y0 - 26}mm;background:rgba(255,255,255,.95);box-shadow:0 0 .6mm rgba(4,40,58,.5)"></div>'
                  f'<div class="a" style="left:{x - 1.3}mm;top:{y2 - 1.3}mm;width:2.6mm;height:2.6mm;border-radius:50%;background:#fff;border:.5mm solid {PETROL}"></div>')
    return (f'<div class="a" style="left:{sol}mm;top:0;width:{2 * PANEL}mm;height:{YUK}mm;overflow:hidden">'
            f'<img src="file://{os.path.join(KAYNAK, "ana-gorsel.jpg")}" style="position:absolute;left:-2%;top:0;width:104%;height:100%;object-fit:cover;object-position:50% 40%">'
            f'<div style="position:absolute;inset:0;background:linear-gradient(180deg,{KREM} 0,rgba(242,249,251,.97) 19%,rgba(242,249,251,.55) 27%,rgba(242,249,251,0) 37%)"></div></div>'
            + baslik + cagri)


def ic_bant():
    """Alt lacivert bant: olanaklar (kırımın iki yanında üçer tane) ve yakınlıklar."""
    sol, orta = X(1), X(2)
    olanak = [(236, "asansor", "Asansör", "Her blokta 2 adet"), (302, "kalkan", "Deprem", "Güvenliği"), (368, "otopark", "Kapalı", "Otopark"),
              (438, "kalkan", "7/24", "Güvenlik"), (504, "damla", "Kapalı Yüzme", "Havuzu"), (570, "spor", "Fitness · Sauna", "Türk Hamamı")]
    bant = ""
    for i, (x, ik, a, b) in enumerate(olanak):
        kucuk = "font-size:7.4pt;font-weight:500;opacity:.85" if i == 0 else "font-size:10.5pt;font-weight:600"
        bant += (f'<div class="a" style="left:{x - 32}mm;top:265mm;width:64mm;display:flex;align-items:center;justify-content:center;gap:3mm;color:#fff">{ikon(ik, 9.6, "#fff", 1.3)}'
                 f'<div style="line-height:1.22"><div class="tek" style="font-size:10.5pt;font-weight:600">{a}</div><div class="tek" style="{kucuk}">{b}</div></div></div>')
        if i not in (2, 5):
            bant += f'<div class="a" style="left:{x + 33}mm;top:268mm;width:.25mm;height:8mm;background:rgba(255,255,255,.35)"></div>'
    yakin = lambda maddeler: " <span style='color:rgba(255,255,255,.5)'>·</span> ".join(f'{a} <b style="color:{ALTIN}">{s}</b>' for a, s in maddeler)
    bant += (f'<div class="a tek" style="left:{sol}mm;top:282.6mm;width:{PANEL}mm;text-align:center;font-size:9.4pt;font-weight:500;letter-spacing:.02em;color:#fff">'
             + yakin([("D-100", "1 dk"), ("Sahil", "2 dk"), ("41 Burda AVM", "2 dk"), ("İzmit Outlet", "2 dk")]) + "</div>"
             + f'<div class="a tek" style="left:{orta}mm;top:282.6mm;width:{PANEL}mm;text-align:center;font-size:9.4pt;font-weight:500;letter-spacing:.02em;color:#fff">'
             + yakin([("Şehir Merkezi", "5 dk"), ("Şehir Hastanesi", "5 dk"), ("Symbol AVM", "7 dk"), ("Üniversite", "10 dk")]) + "</div>")
    return bant


def dalgalar():
    """Alt kenar: orta iki panelde koyu petrol bant; yan panellerde markanın kendi dalga görseli (yeniden çizilmez)."""
    dh = (KIRIM[0] + 14) * 446 / 2332
    return (f'<div class="a" style="left:{X(1)}mm;top:262mm;width:{2 * PANEL}mm;height:{YUK - 262}mm;background:{DERIN_G}"></div>'
            f'<img class="a" src="{DALGA}" style="left:-8mm;top:{YUK - dh + 4}mm;width:{KIRIM[0] + 14}mm">'
            f'<img class="a" src="{DALGA}" style="left:{KIRIM[2] - 6}mm;top:{YUK - dh + 4}mm;width:{GEN - KIRIM[2] + 14}mm;transform:scaleX(-1)">')


def ic_yuz():
    palmiye = "file://" + os.path.join(KAYNAK, "palmiye-saydam.png")
    return (f'<div class="a" style="left:0;top:0;width:{KIRIM[0]}mm;height:{YUK}mm;background:linear-gradient(180deg,#fff 0,{KREM} 100%)"></div>'
            f'<div class="a" style="left:{KIRIM[2]}mm;top:0;width:{GEN - KIRIM[2]}mm;height:{YUK}mm;background:linear-gradient(180deg,#fff 0,{KREM} 100%)"></div>'
            f'<img class="a" src="{palmiye}" style="left:-10mm;top:226mm;width:78mm">'
            f'<img class="a" src="{palmiye}" style="left:{GEN - 68}mm;top:226mm;width:78mm;transform:scaleX(-1)">'
            + ic_orta() + dalgalar() + ic_bant() + ic_sol() + ic_sag()
            # dalga, alt banttaki yazıların üstüne çıkmasın diye bant yazıları yeniden üstte
            )


# ---------------------------------------------------------------- DIŞ YÜZ ----
HARITA = dict(m_mm=56.0, proje=(322.0, 186.0))      # 1 mm = 52 m; proje, haritanın (iki panel, 400×306 mm) bu noktasında


def harita_uret(yol):
    """İki orta panelin zemini: uydu görüntüsü, lacivert tek tona çekilmiş (yazılar ve hatlar öne çıksın diye)."""
    z = 14
    cx, cy = rd.mpx(rd.LAT, rd.LON, z)
    mpp = 156543.03392 * math.cos(math.radians(rd.LAT)) / 2 ** z
    k = HARITA["m_mm"] / mpp                                   # mm başına piksel
    w, h = round(2 * PANEL * k), round(YUK * k)
    x0, y0 = cx - HARITA["proje"][0] * k, cy - HARITA["proje"][1] * k
    tx0, ty0, tx1, ty1 = int(x0 // 256), int(y0 // 256), int((x0 + w) // 256), int((y0 + h) // 256)
    os.makedirs(rd.ONBELLEK, exist_ok=True)
    isler = [(rd.UYDU.format(z=z, x=x, y=y), os.path.join(rd.ONBELLEK, f"{z}-{x}-{y}.jpg")) for x in range(tx0, tx1 + 1) for y in range(ty0, ty1 + 1)]
    with ThreadPoolExecutor(12) as havuz:
        list(havuz.map(lambda a: rd._indir(*a), isler))
    im = Image.new("RGB", (w, h))
    for x in range(tx0, tx1 + 1):
        for y in range(ty0, ty1 + 1):
            im.paste(Image.open(os.path.join(rd.ONBELLEK, f"{z}-{x}-{y}.jpg")).convert("RGB"), (round(x * 256 - x0), round(y * 256 - y0)))
    g = np.asarray(im.convert("L"), np.float32) / 255
    g = np.clip((g - .06) / .62, 0, 1) ** .85
    duraklar = np.array([[4, 40, 58], [9, 86, 120], [44, 148, 180], [184, 228, 236]], np.float32)       # koyu deniz → açık yerleşim
    t = g * 3
    i = np.clip(t.astype(int), 0, 2)
    f = (t - i)[..., None]
    renk = duraklar[i] * (1 - f) + duraklar[i + 1] * f
    Image.fromarray(renk.astype(np.uint8)).save(yol, quality=90)
    return k


def konum(lat, lon):
    """Enlem/boylam → sayfa mm (dış yüz)."""
    z = 14
    mpp = 156543.03392 * math.cos(math.radians(rd.LAT)) / 2 ** z
    k = HARITA["m_mm"] / mpp
    px, py = rd.mpx(lat, lon, z)
    cx, cy = rd.mpx(rd.LAT, rd.LON, z)
    return KIRIM[0] + HARITA["proje"][0] + (px - cx) / k, HARITA["proje"][1] + (py - cy) / k


def dis_harita(harita_jpg):
    sol = KIRIM[0]
    px, py = konum(rd.LAT, rd.LON)
    cizgi = lambda nk, renk, kal, kesik="": (f'<polyline points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in (konum(la, lo) for la, lo in nk))}" fill="none" stroke="rgba(6,16,40,.55)" '
                                             f'stroke-width="{kal + 1}" stroke-linecap="round" stroke-linejoin="round"/>'
                                             f'<polyline points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in (konum(la, lo) for la, lo in nk))}" fill="none" stroke="{renk}" '
                                             f'stroke-width="{kal}" stroke-linecap="round" stroke-linejoin="round" {kesik}/>')
    h = (f'<div class="a" style="left:{sol}mm;top:0;width:{2 * PANEL}mm;height:{YUK}mm;overflow:hidden">'
         f'<img src="file://{harita_jpg}" style="position:absolute;left:0;top:0;width:100%;height:100%">'
         f'<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(4,40,58,.78) 0,rgba(4,40,58,0) 24%,rgba(4,40,58,0) 78%,rgba(4,40,58,.65) 100%)"></div></div>'
         f'<svg class="a" style="left:0;top:0;width:{GEN}mm;height:{YUK}mm;overflow:hidden" viewBox="0 0 {GEN} {YUK}">'
         f'<defs><clipPath id="hk"><rect x="{sol}" y="0" width="{2 * PANEL}" height="{YUK}"/></clipPath></defs><g clip-path="url(#hk)">'
         + cizgi(rd.HAT_KUZEY, AQUA, 1.2) + cizgi(rd.HAT_GUNEY, "#ffffff", 1.5, 'stroke-dasharray="3.2 2.2"') + '</g></svg>')
    for ad, sure, la, lo, taraf, dy in YAKIN:
        x, y = konum(la, lo)
        yer = f"right:{GEN - x + 3.4:.1f}mm" if taraf == "sol" else f"left:{x + 3.4:.1f}mm"
        h += (f'<div class="a" style="left:{x - 1.6:.1f}mm;top:{y - 1.6:.1f}mm;width:3.2mm;height:3.2mm;border-radius:50%;background:#fff;border:.8mm solid {PETROL}"></div>'
              f'<div class="a tek" style="top:{y + dy - 3.6:.1f}mm;{yer};display:flex;border-radius:1.8mm;overflow:hidden;box-shadow:0 1mm 2.6mm rgba(4,12,30,.5)">'
              f'<span style="background:#fff;color:{LACI};font-size:8.6pt;font-weight:700;padding:1.6mm 2.6mm 1.4mm">{ad}</span>'
              f'<span style="background:{PETROL};color:#fff;font-size:8.6pt;font-weight:700;padding:1.6mm 2.2mm 1.4mm">{sure}</span></div>')
    lg = 34
    h += (f'<div class="a" style="left:{px - 2.6:.1f}mm;top:{py - 2.6:.1f}mm;width:5.2mm;height:5.2mm;border-radius:50%;background:{PETROL};border:1mm solid #fff;box-shadow:0 0 0 .8mm rgba(4,40,58,.55)"></div>'
          f'<div class="a" style="left:{px - lg / 2 - 3.5:.1f}mm;top:{py + 6.4:.1f}mm">'
          f'<div style="position:absolute;left:{lg / 2 + 3.5 - 2.2:.1f}mm;top:-1.9mm;width:4.4mm;height:4.4mm;background:#fff;border-left:.4mm solid {AQUA};border-top:.4mm solid {AQUA};transform:rotate(45deg)"></div>'
          f'<div style="position:relative;padding:3mm 3.5mm 2.6mm;border-radius:3mm;background:#fff;border:.4mm solid {AQUA};box-shadow:0 2mm 5mm rgba(0,0,0,.45)">'
          f'<img src="{LOGO}" style="display:block;width:{lg}mm"></div></div>')
    # Konum paneli başlığı ve açıklamalar (sağdaki harita paneli)
    bx = X(2, 12)
    gosterge = lambda renk, ad, durum, kesik=False: (f'<div style="display:flex;align-items:center;gap:2.6mm"><span style="width:11mm;height:0;border-top:1mm {"dashed" if kesik else "solid"} {renk}"></span>'
                                                     f'<span class="tek" style="font-size:7.6pt;font-weight:700;letter-spacing:.12em;color:#fff">{ad}</span>'
                                                     f'<span class="tek" style="font-size:7pt;font-weight:600;letter-spacing:.08em;color:{renk}">{durum}</span></div>')
    h += (f'<div class="a" style="left:{bx}mm;top:13mm;color:#fff"><div class="ust tek" style="font-size:8pt;color:{ALTIN}">Konum</div>'
          f'<div class="fr tek" style="margin-top:1.8mm;font-size:23pt;line-height:1.08">Her yere<br>dakikalar içinde</div>'
          f'<div style="margin-top:2.6mm;font-size:8.4pt;font-weight:500;line-height:1.5;max-width:92mm;opacity:.92">İzmit MİA Bölgesi: sahile, alışveriş merkezlerine, hastaneye ve ana yollara dakikalar içinde.</div></div>'
          f'<div class="a" style="left:{X(2, 100)}mm;top:246mm;display:flex;flex-direction:column;gap:2.4mm;padding:4.4mm 5mm 4mm;border-radius:3mm;background:rgba(4,40,58,.86);border:.25mm solid rgba(146,209,223,.6)">'
          + gosterge("#ffffff", "GÜNEY METRO HATTI", "PLANLANAN", True) + gosterge(AQUA, "KÖRFEZRAY", "YAPIM AŞAMASINDA")
          + f'<div class="tek" style="margin-top:1mm;font-size:8.4pt;font-weight:600;color:#fff">D-100 Karayolu <b style="color:{ALTIN}">1 dk</b> &nbsp;·&nbsp; TEM Otoyolu <b style="color:{ALTIN}">5 dk</b></div></div>'
          f'<div class="a tek" style="left:{KIRIM[1] + 6}mm;top:{YUK - 9}mm;width:{PANEL - 12}mm;text-align:right;font-size:5pt;font-weight:500;color:rgba(255,255,255,.7)">'
          f'Uydu görüntüsü: Copernicus Sentinel-2 (2016) · EOX, CC BY 4.0. Metro güzergâhları yaklaşıktır.</div>')
    return h


def dis_fiyat():
    x, w = X(1, 13), PANEL - 26
    satir = ""
    for i, (tip, ad, pesin, ayda) in enumerate(FIYAT):
        hucre = lambda et, deger: (f'<div style="width:50mm"><div class="tek" style="font-size:7pt;font-weight:700;letter-spacing:.22em;color:{OKYANUS}">{et}</div>'
                                   f'<div class="tek" style="margin-top:1.4mm;font-size:19pt;font-weight:800;line-height:1;color:{LACI}">{deger}<span style="font-size:10pt;margin-left:1.2mm">TL</span></div></div>')
        satir += (f'<div style="display:flex;align-items:center;padding:11.5mm 0;{"border-top:.25mm solid rgba(146,209,223,.7);" if i else ""}">'
                  f'<div style="width:54mm"><div class="fr tek" style="font-size:31pt;line-height:1;color:{LACI}">{tip}</div>'
                  f'<div class="tek" style="margin-top:1.6mm;font-size:10.5pt;font-weight:600;color:{LACI}">{ad}</div></div>'
                  + hucre("PEŞİNAT", pesin) + hucre("AYLIK TAKSİT", ayda) + "</div>")
    yok = "".join(f'<div class="tek" style="display:flex;align-items:center;gap:2.2mm;font-size:9.4pt;font-weight:700;color:#fff">{eski.tik(4.6, ALTIN, LACI2)}{t}</div>'
                  for t in ("Banka yok", "Faiz yok", "Kefil yok", "Ara ödeme yok", "Ara zam yok", "Vade farkı yok"))
    return (f'<div class="a" style="left:{x}mm;top:15mm;width:{w}mm;height:276mm;border-radius:5mm;background:#fff;box-shadow:0 3mm 9mm rgba(4,12,30,.5);overflow:hidden">'
            f'<div style="padding:10mm 11mm 0"><div class="ust tek" style="font-size:8pt;color:{OKYANUS}">Fiyat ve Ödeme Planı</div>'
            f'<div class="fr" style="margin-top:2.2mm;font-size:23pt;line-height:1.1;color:{LACI}">60 ay sabit taksitle<br>ev sahibi olun</div>'
            f'<div style="margin-top:6mm">{satir}</div></div>'
            f'<div style="position:absolute;left:0;right:0;bottom:0;height:98mm;background:{YUZEY_G};padding:9mm 11mm 0">'
            f'<div class="tek" style="font-size:19pt;font-weight:800;letter-spacing:.04em;color:{ALTIN}">60 AY SABİT TAKSİT</div>'
            f'<div style="margin-top:1.6mm;font-size:8.8pt;font-weight:500;line-height:1.5;color:#fff;opacity:.92">Peşinatınızı ödeyin, kalanını 60 ay boyunca değişmeyen taksitlerle tamamlayın.</div>'
            f'<div style="margin-top:6mm;display:grid;grid-template-columns:1fr 1fr;gap:3.6mm 4mm">{yok}</div>'
            f'<div style="position:absolute;left:11mm;right:11mm;bottom:7mm;font-size:6.2pt;font-weight:500;line-height:1.5;color:rgba(255,255,255,.72)">'
            f'Başlangıç fiyatlarıdır (Kasım 2026). Güncel fiyat listesi ve ödeme planı için satış ofisimizle görüşünüz.</div></div></div>')


def dis_on_kapak():
    x = KIRIM[2]
    lw = 100
    return (f'<div class="a" style="left:{x}mm;top:0;width:{GEN - x}mm;height:{YUK}mm;overflow:hidden;background:{DERIN}">'
            f'<img src="file://{os.path.join(KAYNAK, "kapak.jpg")}" style="position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover;object-position:50% 50%">'
            f'<div style="position:absolute;inset:0;background:linear-gradient(180deg,{KREM} 0,rgba(242,249,251,.97) 26%,rgba(242,249,251,.5) 34%,rgba(242,249,251,0) 42%,'
            f'rgba(4,40,58,0) 58%,rgba(4,40,58,.8) 72%,rgba(4,40,58,.97) 84%,{DERIN} 100%)"></div></div>'
            f'<img class="a" src="{LOGO}" style="left:{x + (PANEL - lw) / 2}mm;top:20mm;width:{lw}mm">'
            f'<div class="a tek" style="left:{x}mm;top:{27 + lw * LOGO_ORAN}mm;width:{PANEL}mm;text-align:center;font-size:10pt;font-weight:600;letter-spacing:.36em;padding-left:.36em;color:{PETROL}">'
            f'MODERN YAŞAM <span style="color:{OKYANUS}">•</span> DOĞRU YATIRIM</div>'
            f'<div class="a" style="left:{x}mm;top:226mm;width:{PANEL}mm;text-align:center;color:#fff">'
            f'<div class="ust tek" style="font-size:8pt;color:{AQUA};padding-left:.3em">İzmit · MİA Bölgesi</div>'
            f'<div class="tek" style="margin-top:3mm;font-size:27pt;font-weight:700;letter-spacing:.02em;line-height:1">60 AY SABİT TAKSİT</div>'
            f'<div class="tek" style="margin-top:3mm;font-size:11pt;font-weight:600">699.000 TL\'den başlayan peşinat</div>'
            f'<div style="margin:5mm auto 0;width:24mm;height:.4mm;background:{METAL}"></div>'
            f'<div style="margin-top:4.6mm;display:flex;align-items:center;justify-content:center;gap:2.6mm">{eski.ikon("tel", 6.4, "#fff", 2)}'
            f'<span class="tek" style="font-size:20pt;font-weight:700;letter-spacing:.03em">444 10 58</span></div></div>')


def dis_arka_kapak(qr, ykb):
    satir = lambda i, t: f'<div style="display:flex;align-items:flex-start;gap:3.6mm;font-size:10pt;font-weight:600;color:{PETROL};line-height:1.45">{i}<span>{t}</span></div>'
    logo = lambda etiket, img: (f'<div style="flex:1;text-align:center"><div class="tek" style="font-size:6pt;font-weight:700;letter-spacing:.16em;color:#52717e">{etiket}</div>'
                                f'<div style="height:20mm;display:flex;align-items:center;justify-content:center;margin-top:1.6mm">{img}</div></div>')
    lw = 74
    return (f'<div class="a" style="left:0;top:0;width:{KIRIM[0]}mm;height:{YUK}mm;background:linear-gradient(180deg,#fff 0,{KREM} 100%)"></div>'
            f'<img class="a" src="{LOGO}" style="left:{X(0, (PANEL - lw) / 2)}mm;top:15mm;width:{lw}mm">'
            f'<div class="a" style="left:{X(0, 16)}mm;top:{24 + lw * LOGO_ORAN}mm;width:{PANEL - 32}mm;border-radius:5mm;background:{YUZEY_G};padding:7mm 0 6.4mm;text-align:center;color:#fff;'
            f'box-shadow:0 2.4mm 6mm rgba(4,40,58,.3)">'
            f'<div class="fr tek" style="font-size:15pt;font-weight:600;font-style:italic;color:{AQUA}">Sizi bekliyoruz</div>'
            f'<div class="tek" style="margin-top:2mm;font-size:40pt;font-weight:700;letter-spacing:.01em;line-height:1">444 10 58</div>'
            f'<div style="margin-top:3.4mm;display:flex;align-items:center;justify-content:center;gap:2.4mm">{eski.WA.format(s=6.4)}'
            f'<span class="tek" style="font-size:15pt;font-weight:700;letter-spacing:.03em">0540 028 00 41</span></div></div>'
            f'<div class="a" style="left:{X(0, 18)}mm;top:{82 + lw * LOGO_ORAN}mm;width:{PANEL - 36}mm">'
            f'<div class="ust tek" style="font-size:8pt;color:{OKYANUS}">Satış Ofisi</div>'
            f'<div style="margin-top:4mm;display:flex;flex-direction:column;gap:3.2mm">'
            + satir(ikon("pin", 6, PETROL), "Ömerağa Mah. Abdurrahman Yüksel Cad.<br>Bana Bak Ap. No:15/4 İzmit / Kocaeli")
            + satir(ikon("tel", 6, PETROL), "0541 128 40 41") + satir(ikon("kure", 6, PETROL), "miaparkocean.com") + satir(ikon("insta", 6, PETROL), "@miaparkocean")
            + f'</div></div>'
            f'<div class="a" style="left:{X(0, 18)}mm;top:196mm;width:{PANEL - 36}mm;border-radius:4mm;background:#fff;border:.3mm solid {AQUA};padding:5mm;display:flex;align-items:center;gap:6mm">'
            f'<img src="file://{qr}" style="width:34mm;height:34mm;flex:none">'
            f'<div><div class="fr" style="font-size:13pt;font-weight:600;color:{PETROL};line-height:1.15">Projeyi telefonunuzdan inceleyin</div>'
            f'<div style="margin-top:2mm;font-size:8pt;font-weight:400;line-height:1.45;color:#29505f">Kamerayı kodun üzerine tutun; daire tipleri, kat planları ve galeri karşınızda.</div></div></div>'
            f'<div class="a" style="left:{X(0, 14)}mm;top:249mm;width:{PANEL - 28}mm;display:flex;align-items:flex-start;gap:2mm">'
            + logo("YAPIMCI", f'<img src="file://{ykb}" style="height:19mm">') + logo("MÜTEAHHİT", f'<img src="{V("tilda.svg")}" style="width:36mm">')
            + logo("TEK YETKİLİ SATICI", f'<img src="{V("ocean-lacivert.svg")}" style="width:30mm">')
            + f'</div>'
            f'<div class="a" style="left:{X(0, 16)}mm;top:281mm;width:{PANEL - 32}mm;font-size:5.6pt;font-weight:400;line-height:1.5;color:#52717e;text-align:center">'
            f'Yapımcı: S.S. Yahya Kaptan Birlik Yapı Kooperatifi · Müteahhit: Tilda İnşaat · Tek Yetkili Satıcı: Ocean Gayrimenkul. '
            f'Görseller tanıtım amaçlıdır; uygulamada değişiklik olabilir.</div>')


def belge(qr, ykb, harita_jpg, kilavuz=False):
    k1 = k2 = ""
    if kilavuz:
        cizgi = "".join(f'<div class="kilavuz" style="left:{x}mm"></div>' for x in KIRIM) + '<div class="kilavuz-kirp"></div>'
        et = lambda adlar: "".join(f'<div class="etiket" style="left:{TASMA + i * PANEL + 2}mm">{a}</div>' for i, a in enumerate(adlar))
        k1 = cizgi + et(["İÇ YÜZ · 1", "İÇ YÜZ · 2", "İÇ YÜZ · 3", "İÇ YÜZ · 4"])
        k2 = cizgi + et(["ARKA KAPAK", "DIŞ YÜZ · fiyat", "DIŞ YÜZ · konum", "ÖN KAPAK"])
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>'
            f'<div class="sayfa" id="ic">{ic_yuz()}{k1}</div>'
            f'<div class="sayfa" id="dis">{dis_harita(harita_jpg)}{dis_fiyat()}{dis_on_kapak()}{dis_arka_kapak(qr, ykb)}{k2}</div></body></html>')


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
  for (const [html, ek] of [[is.html, ""], [is.kilavuzHtml, "-kilavuz"]]) {
    const c = await t.newContext({ viewport: { width: 3100, height: 1200 }, deviceScaleFactor: 1.5 });
    const o = await c.newPage();
    await o.goto("file://" + html); await hazir(o);
    for (const id of ["ic", "dis"]) await o.locator("#" + id).screenshot({ path: is.png[id + ek] });
    await c.close();
  }
  await t.close();
})();
"""


def rgb_hsv(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx, mn = a.max(-1), a.min(-1)
    d = mx - mn + 1e-9
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    return np.stack([h, np.where(mx > 0, (mx - mn) / (mx + 1e-9), 0), mx], -1)


def hsv_rgb(x):
    h, s, v = x[..., 0] / 60, x[..., 1], x[..., 2]
    c = v * s
    k = c * (1 - np.abs(h % 2 - 1))
    m = v - c
    i = np.floor(h).astype(int) % 6
    z = np.zeros_like(h)
    r = np.choose(i, [c, k, z, z, k, c]); g = np.choose(i, [k, c, c, k, z, z]); b = np.choose(i, [z, z, k, c, c, k])
    return np.stack([r + m, g + m, b + m], -1)


def markaya_cek(im, gok=True):
    """Pembe-lila-mor tonları (çiçekler, yastıklar) soluk beyaza çeker; gökyüzü mavisini marka petrol-mavisine yaklaştırır.
    Pembe ailesi: yeşil kanal en düşük, kırmızı ve mavi ondan yüksek (turuncu, ten ve ahşapta mavi en düşüktür, etkilenmez)."""
    a = np.asarray(im.convert("RGB"), np.float32) / 255
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    pembe = np.clip((np.minimum(r, b) - g + .004) / .03, 0, 1) * np.clip((r - .2) / .15, 0, 1) * np.clip((r - g) / .04, 0, 1)
    if gok:
        # Altın saat ışığı pembeyi somon/gül rengine kaydırır (mavi en düşük kanal olur); bunları tonla yakala:
        # 282°–372° (12°) arası tam, 22°'ye kadar söner. Turuncu, ahşap ve ten (25°+) etkilenmez.
        x0 = rgb_hsv(a)
        mesafe = np.abs(((x0[..., 0] - 327 + 180) % 360) - 180)
        pembe = np.maximum(pembe, np.clip((55 - mesafe) / 10, 0, 1) * np.clip((x0[..., 1] - .1) / .1, 0, 1))
    gri = (r * .3 + g * .59 + b * .11)[..., None]
    beyaz = np.clip(gri * 1.08 + .04, 0, 1) * np.array([.97, .99, 1.0], np.float32)       # hafif soğuk beyaz
    a = a * (1 - pembe[..., None]) + beyaz * pembe[..., None]
    if gok:
        x = rgb_hsv(a)
        h = x[..., 0]
        mavi = np.clip(1 - np.abs(h - 218) / 26, 0, 1)                                 # 192–244° gökyüzü
        x[..., 0] = h - (h - 200) * .55 * mavi
        x[..., 1] *= 1 - .14 * mavi
        a = hsv_rgb(x)
    return Image.fromarray((np.clip(a, 0, 1) * 255 + .5).astype(np.uint8))


def hazirla(g):
    """Kaynak görselleri baskıya hazırlar: ana görsel JPEG, palmiye beyazı saydam, kapak kırpılıp büyütülür."""
    global LOGO_ORAN
    ana = markaya_cek(Image.open(os.path.join(KAYNAK, "ana-gorsel.png")))
    ana.save(os.path.join(KAYNAK, "ana-gorsel.jpg"), quality=93, subsampling=0)
    for ad in ("plan-1-0", "plan-1-1", "plan-2-1-alt", "plan-2-1-ust"):                 # planlardaki pembe yastık/halılar
        p = Image.open(os.path.join(KAYNAK, ad + ".png")).convert("RGBA")
        m = markaya_cek(p, gok=False).convert("RGBA")
        m.putalpha(p.getchannel("A"))
        m.save(os.path.join(KAYNAK, ad + "-m.png"))
    lg = Image.open(os.path.join(ROOT, "public", "brand", "logo-mia-2026.png")).convert("RGBA")
    lg = lg.crop(lg.getchannel("A").point(lambda v: 255 if v > 12 else 0).getbbox())
    lg.save(os.path.join(KAYNAK, "logo-mia.png"))
    LOGO_ORAN = lg.height / lg.width
    p = np.asarray(Image.open(os.path.join(KAYNAK, "palmiye.png")).convert("RGB"), np.float32)
    alfa = np.clip((250 - p.min(axis=2)) * 5.0, 0, 255)
    Image.fromarray(np.dstack([p, alfa]).astype(np.uint8), "RGBA").save(os.path.join(KAYNAK, "palmiye-saydam.png"))
    k = ana                                                            # ön kapak: aynı gündüz görselinin orta kesiti (gün batımı yok)
    hedef = (GEN - KIRIM[2]) / YUK                                    # kapak paneli oranı (taşmalı)
    w = round(k.height * hedef)
    k = k.crop(((k.width - w) // 2, 0, (k.width - w) // 2 + w, k.height))
    k.save(os.path.join(KAYNAK, "kapak.jpg"), quality=92)
    qr = os.path.join(g, "qr.svg")
    segno.make("https://miaparkocean.com/", error="q").save(qr, scale=10, border=1, dark=LACI2, light=None)
    ykb = os.path.join(g, "ykb.png")
    y = Image.open(os.path.join(ROOT, "public", "ykb-logo.png")).convert("RGBA")
    y = y.crop(y.getchannel("A").getbbox())
    y.resize((round(y.width * 900 / y.height), 900), Image.LANCZOS).save(ykb)
    harita_jpg = os.path.join(KAYNAK, "harita.jpg")
    harita_uret(harita_jpg)
    return qr, ykb, harita_jpg


def main():
    os.makedirs(OUT, exist_ok=True)
    g = tempfile.mkdtemp(prefix="brosur80-")
    qr, ykb, harita_jpg = hazirla(g)
    html, kil = os.path.join(g, "brosur.html"), os.path.join(g, "kilavuz.html")
    open(html, "w", encoding="utf-8").write(belge(qr, ykb, harita_jpg))
    open(kil, "w", encoding="utf-8").write(belge(qr, ykb, harita_jpg, kilavuz=True))
    pdf = os.path.join(OUT, "mia-brosur-akordiyon-80x30-baski.pdf")
    png = {k: os.path.join(g, k + ".png") for k in ("ic", "dis", "ic-kilavuz", "dis-kilavuz")}
    js, jp = os.path.join(g, "render.cjs"), os.path.join(g, "is.json")
    open(js, "w").write(RENDER_JS)
    json.dump(dict(html=html, kilavuzHtml=kil, pdf=pdf, png=png), open(jp, "w"))
    npm = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    subprocess.run(["node", js, jp], check=True, env={**os.environ, "NODE_PATH": npm})
    print("  →", os.path.relpath(pdf, ROOT), f"{os.path.getsize(pdf) / 1048576:.1f} MB")
    for k, ad in (("ic", "onizleme-ic-yuz.jpg"), ("dis", "onizleme-dis-yuz.jpg"), ("ic-kilavuz", "onizleme-ic-yuz-kirimli.jpg"), ("dis-kilavuz", "onizleme-dis-yuz-kirimli.jpg")):
        im = Image.open(png[k]).convert("RGB")
        im.save(os.path.join(OUT, ad), quality=90)
        print("  →", os.path.relpath(os.path.join(OUT, ad), ROOT), im.size)


if __name__ == "__main__":
    main()
