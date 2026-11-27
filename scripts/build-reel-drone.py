#!/usr/bin/env python3
"""
Reklam Reels'i — "Uydudan eve" (1080x1920, ~48 sn, 24 fps, seslendirmeli + müzikli).

Kurgu:
    0,0   Uydudan yaklaşma: Marmara → İzmit Körfezi → projenin tam konumu   [vo-1]
    5,6   Yakın yerler: gerçek koordinatlarla çizgiler ve dakika etiketleri [vo-6]
    11,6  Projeye dalış: girişe inen drone çekimi
    14,0  1+0 daire içi + fiyat kartı                                       [vo-3]
    22,0  1+1 daire içi + fiyat kartı                                       [vo-4]
    29,8  Balkondan bakış + 60 ay sabit taksit + üç tipin tablosu           [vo-5]
    34,2  Avlu + dört "YOK" etiketi (seslendirmeyle eş zamanlı)             [vo-2]
    40,4  Kapanış: tek yetkili satış, 444 10 58, WhatsApp                   [vo-7]

Kaynaklar:
  • Uydu görüntüsü: Sentinel-2 cloudless 2016, EOX IT Services GmbH — CC BY 4.0
    ("Contains modified Copernicus Sentinel data 2016"). Videoda künye yazılıdır.
    Konum: Google Maps'ten alınan proje koordinatı (src/data/location.ts).
  • Yakın yerlerin koordinatları OpenStreetMap'ten (Photon), süreler src/data/location.ts'ten.
  • Seslendirme: film-source/ses/vo-1..7.wav (ElevenLabs, önceden üretildi), %7 hızlandırılır.
  • Müzik: "Inspired" — Kevin MacLeod (incompetech.com), CC BY 4.0. Yayınlarken açıklamaya
    künye yazılmalı: Müzik: "Inspired" Kevin MacLeod (incompetech.com), CC BY 4.0.
  • Çekimler film-source/clips (projenin kendi render'larından), fotoğraflar sosyal-medya/bitmis-fotograflar.

    python3 scripts/build-reel-drone.py
"""

import importlib.util
import math
import os
import shutil
import ssl
import subprocess
import tempfile
import urllib.request
import wave
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from PIL import Image, ImageEnhance

KOK = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("yy", os.path.join(KOK, "build-reklam-yeni-yuzler.py"))
yy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(yy)

ROOT, F, KIRMIZI = yy.ROOT, yy.F, yy.KIRMIZI
OUT = os.path.join(ROOT, "sosyal-medya", "instagram-reel")
ONBELLEK = os.path.join(ROOT, "film-source", ".kare-onbellek", "uydu")
KLIP = lambda ad: os.path.join(ROOT, "film-source", "clips", ad + ".mp4")
SES = lambda i: os.path.join(ROOT, "film-source", "ses", f"vo-{i}.wav")
MUZIK = os.path.join(ROOT, "film-source", "muzik", "inspired-kevin-macleod.mp3")
VEK = lambda ad: F("public", "brand", "vektor", ad)
W, H, FPS, SR = 1080, 1920, 24, 44100
KOYU, VURGU = yy.LACI
TOPLAM = 47.8
GECIS = 0.35
VO_HIZ = 1.07

# ---------------------------------------------------------------- harita
LAT, LON = 40.736667, 29.944889          # proje (Google Maps koordinatı)
SX, SY = 500, 1080                        # projenin ekrandaki yeri
Z0, Z1 = 8.2, 12.9                        # yaklaşmanın başı ve sonu (harita yakınlığı)
T_ZOOM, T_DALIS, T_HARITA = 5.2, 10.9, 11.6
LW, LH, LMIN, LMAX = 3072, 5120, 9, 13
UYDU = "https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless_3857/default/g/{z}/{y}/{x}.jpg"

# (ad, süre, enlem, boylam, etiketin tarafı)
YAKIN = [
    ("41 Burda AVM", "3 dk", 40.75675, 29.94756, "sol"),
    ("Symbol AVM", "7 dk", 40.75787, 29.97956, "sag"),
    ("Şehir Merkezi", "5 dk", 40.77211, 29.95056, "sol"),
    ("Şehir Hastanesi", "5 dk", 40.78309, 29.96064, "sag"),
    ("Kocaeli Üniversitesi", "10 dk", 40.81874, 29.92291, "sag"),
]


def mpx(lat, lon, z):
    n = 256 * 2 ** z
    return (lon + 180) / 360 * n, (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n


def olcek(t):
    """Yaklaşma bittikten sonraki büyüme (haritayla etiketler aynı fonksiyonu kullanır)."""
    if t <= T_ZOOM:
        return 1.0
    if t <= T_DALIS:
        return 1 + .05 * (t - T_ZOOM) / (T_DALIS - T_ZOOM)
    q = (t - T_DALIS) / (T_HARITA - T_DALIS)
    return 1.05 * (1 + 1.7 * q ** 3)


def kamera(t):
    if t < T_ZOOM:
        p = t / T_ZOOM
        e = p * p * (3 - 2 * p)
        return Z0 + (Z1 - Z0) * e, -10 * (1 - e)
    return Z1 + math.log2(olcek(t)), 0.0


def _indir(url, yol):
    if os.path.exists(yol) and os.path.getsize(yol) > 300:
        return
    ctx = ssl.create_default_context(cafile=os.environ.get("SSL_CERT_FILE") or None)
    for _ in range(5):
        try:
            veri = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), context=ctx, timeout=30).read()
            open(yol, "wb").write(veri)
            return
        except Exception as hata:  # noqa: BLE001
            son = hata
    raise SystemExit(f"uydu karosu alınamadı: {url} · {son}")


def seviye(z):
    """Proje merkezli LW x LH mozaik (renk düzeltmeli)."""
    cx, cy = mpx(LAT, LON, z)
    x0, y0 = cx - LW / 2, cy - LH / 2
    tx0, ty0, tx1, ty1 = int(x0 // 256), int(y0 // 256), int((x0 + LW) // 256), int((y0 + LH) // 256)
    os.makedirs(ONBELLEK, exist_ok=True)
    isler = [(UYDU.format(z=z, x=x, y=y), os.path.join(ONBELLEK, f"{z}-{x}-{y}.jpg"))
             for x in range(tx0, tx1 + 1) for y in range(ty0, ty1 + 1)]
    with ThreadPoolExecutor(12) as havuz:
        list(havuz.map(lambda a: _indir(*a), isler))
    im = Image.new("RGB", (LW, LH))
    for x in range(tx0, tx1 + 1):
        for y in range(ty0, ty1 + 1):
            im.paste(Image.open(os.path.join(ONBELLEK, f"{z}-{x}-{y}.jpg")).convert("RGB"), (round(x * 256 - x0), round(y * 256 - y0)))
    im = ImageEnhance.Brightness(im).enhance(1.16)
    im = ImageEnhance.Contrast(im).enhance(1.08)
    return ImageEnhance.Color(im).enhance(1.28)


def harita_karesi(t, sev):
    z, aci = kamera(t)
    lv = min(max(math.ceil(z), LMIN), LMAX)
    f = 2 ** (lv - z)
    mw, mh = 1400, 2500
    kutu = (LW / 2 - mw / 2 * f, LH / 2 - mh / 2 * f, LW / 2 + mw / 2 * f, LH / 2 + mh / 2 * f)
    m = sev[lv].resize((mw, mh), Image.LANCZOS, box=kutu)
    if aci:
        m = m.rotate(aci, Image.BICUBIC)
    return m.crop((mw // 2 - SX, mh // 2 - SY, mw // 2 - SX + W, mh // 2 - SY + H))


def harita_videosu(yol, sure):
    sev = {z: seviye(z) for z in range(LMIN, LMAX + 1)}
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "fast", "-crf", "12", "-pix_fmt", "yuv420p", yol], stdin=subprocess.PIPE)
    for k in range(round(sure * FPS)):
        p.stdin.write(harita_karesi(k / FPS, sev).tobytes())
    p.stdin.close()
    p.wait()


# ---------------------------------------------------------------- yazı katmanı (HTML)
def blok(bas, sure, icerik, sinif="sahne"):
    return f'<div class="{sinif}" style="--s:{bas};--d:{sure}">{icerik}</div>'


def ikili(y, ust, alt, g, ust_boy=84, alt_boy=50):
    """Onaylı fiyat kartının dili: koyu katman + altın şerit."""
    return f"""<div class="a" style="left:0;top:{y}px;width:{W}px;text-align:center">
      <div class="pat" style="--g:{g};display:inline-block;border-radius:26px;overflow:hidden;box-shadow:0 18px 40px rgba(8,20,45,.4)">
        <div class="k tek" style="background:{KOYU};color:#fff;font-size:{ust_boy}px;padding:{round(ust_boy * .34)}px {round(ust_boy * .62)}px {round(ust_boy * .3)}px">{ust}</div>
        <div class="k tek" style="background:{VURGU};color:{KOYU};font-size:{alt_boy}px;padding:{round(alt_boy * .42)}px {round(alt_boy * .6)}px {round(alt_boy * .38)}px">{alt}</div>
      </div></div>"""


def hap(x, y, gen, metin, boy, g, renk=KIRMIZI, yazi="#fff", sinif="pat"):
    return (f'<div class="a tek {sinif}" style="--g:{g};left:{x}px;top:{y}px;width:{gen}px;padding:{round(boy * .62)}px 0;'
            f'border-radius:{round(boy * .72)}px;background:{renk};color:{yazi};text-align:center;font-size:{boy}px;font-weight:800;'
            f'letter-spacing:.02em;box-shadow:0 14px 30px rgba(8,20,45,.34)">{metin}</div>')


def fiyat_karti(tip, pesin, ayda, g):
    """Seslendirmeyle sırayla açılan fiyat kartı: tip → peşinat → aylık → 60 ay."""
    x, gen = 200, 680
    return (hap(x + 70, 1010, gen - 140, tip, 30, g[0], "#fff", KOYU)
            + f"""<div class="a pat" style="--g:{g[1]};left:{x}px;top:1094px;width:{gen}px;padding:30px 0 26px;border-radius:26px 26px 0 0;background:{KOYU};
                   text-align:center;color:#fff;box-shadow:0 18px 40px rgba(8,20,45,.4)">
                <div class="k tek" style="font-size:112px">{pesin}<span style="font-size:40px;letter-spacing:0;margin-left:10px">TL</span></div>
                <div class="tek" style="margin-top:8px;font-size:34px;font-weight:800;letter-spacing:.14em">PEŞİNAT</div></div>
              <div class="a pat" style="--g:{g[2]};left:{x}px;top:1296px;width:{gen}px;padding:24px 0 22px;border-radius:0 0 26px 26px;background:{VURGU};
                   text-align:center;color:{KOYU};box-shadow:0 18px 40px rgba(8,20,45,.4)">
                <div class="k tek" style="font-size:66px"><span style="font-size:34px;letter-spacing:.08em;margin-right:14px">AYDA</span>{ayda}<span style="font-size:32px;letter-spacing:0;margin-left:9px">TL</span></div></div>"""
            + hap(x + 90, 1430, gen - 180, "60 AY SABİT TAKSİT", 38, g[3]))


def tablo(y0, g0):
    satir = ""
    for i, (tip, pesin, ayda) in enumerate([("1+0", "699.000", "29.900"), ("1+1", "999.000", "39.900"), ("2+1", "2.000.000", "50.000")]):
        satir += f"""
    <div class="a soldan" style="--g:{g0 + i * .32};left:60px;top:{y0 + i * 146}px;width:{W - 120}px;height:128px;display:flex;border-radius:24px;overflow:hidden;
         box-shadow:0 18px 36px rgba(8,20,45,.4)">
      <div class="k" style="width:200px;background:{KOYU};color:{VURGU};font-size:70px;display:flex;align-items:center;justify-content:center">{tip}</div>
      <div style="flex:1;background:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center">
        <div class="k tek" style="font-size:52px;color:{KOYU}">{pesin}<span style="font-size:24px;letter-spacing:0;margin-left:7px">TL</span></div>
        <div class="tek" style="margin-top:7px;font-size:20px;font-weight:800;letter-spacing:.2em;color:#4a5878">PEŞİNAT</div></div>
      <div style="width:330px;background:{VURGU};display:flex;flex-direction:column;align-items:center;justify-content:center">
        <div class="tek" style="font-size:20px;font-weight:800;letter-spacing:.2em;color:{KOYU}">AYDA</div>
        <div class="k tek" style="margin-top:5px;font-size:52px;color:{KOYU}">{ayda}<span style="font-size:24px;letter-spacing:0;margin-left:7px">TL</span></div></div>
    </div>"""
    return satir


def yakin_yerler():
    """Harita üstü: proje iğnesi, gerçek konumlara çizgiler, dakika etiketleri."""
    sx, sy = mpx(LAT, LON, Z1)
    cizgi, nokta, etiket = "", "", ""
    for i, (ad, sure, lat, lon, taraf) in enumerate(YAKIN):
        px, py = mpx(lat, lon, Z1)
        x, y = SX + px - sx, SY + py - sy
        g = T_ZOOM + 1.2 + i * .5
        cizgi += (f'<line class="ciz" style="--g:{g}" x1="{SX}" y1="{SY}" x2="{x:.1f}" y2="{y:.1f}" pathLength="1" stroke="#fff" stroke-width="4" '
                  f'stroke-linecap="round" stroke-dasharray="1" stroke-dashoffset="1"/>')
        nokta += (f'<div class="a pat" style="--g:{g + .35};left:{x - 13:.1f}px;top:{y - 13:.1f}px;width:26px;height:26px;border-radius:50%;'
                  f'background:#fff;border:6px solid {KIRMIZI}"></div>')
        yer = f"right:{W - x + 26:.1f}px;transform-origin:100% 50%" if taraf == "sol" else f"left:{x + 26:.1f}px;transform-origin:0 50%"
        etiket += f"""<div class="a pat" style="--g:{g + .4};top:{y - 31:.1f}px;{yer};display:flex;border-radius:16px;overflow:hidden;box-shadow:0 12px 26px rgba(8,20,45,.45)">
            <span class="tek" style="background:#fff;color:{KOYU};font-size:30px;font-weight:800;padding:14px 18px 13px">{ad}</span>
            <span class="k tek" style="background:{VURGU};color:{KOYU};font-size:30px;padding:15px 16px 12px">{sure}</span></div>"""
    igne = f"""<svg class="a dus" style="--g:3.9;left:{SX - 44}px;top:{SY - 112}px;width:88px;height:114px" viewBox="0 0 88 114">
        <path d="M44 112C44 112 6 66 6 42a38 38 0 1 1 76 0c0 24-38 70-38 70z" fill="{KIRMIZI}" stroke="#fff" stroke-width="5"/><circle cx="44" cy="42" r="15" fill="#fff"/></svg>"""
    ad = hap(SX - 215, SY + 24, 430, "MİA PARK OCEAN", 38, 4.25, "#fff", KOYU)
    alt = hap(SX - 250, SY + 118, 500, "SAHİLE 2 DK · D-100'E 1 DK", 30, 7.1)
    adim = 0.05
    n = round((T_HARITA + .3 - T_ZOOM) / adim)
    kare = "".join(f"{100 * k / n:.3f}%{{transform:scale({olcek(T_ZOOM + k * adim):.5f})}}" for k in range(n + 1))
    stil = (f"@keyframes harita{{{kare}}}\n.harita{{position:absolute;left:0;top:0;width:{W}px;height:{H}px;transform-origin:{SX}px {SY}px;"
            f"animation:harita {n * adim:.3f}s linear {T_ZOOM}s both}}")
    govde = (f'<div class="harita"><svg class="a" style="left:0;top:0" width="{W}" height="{H}">{cizgi}</svg>{nokta}{etiket}{igne}{ad}{alt}</div>')
    return stil, govde


def html():
    harita_stil, harita = yakin_yerler()
    r, g, b = (int(KOYU[j:j + 2], 16) for j in (1, 3, 5))
    yoklar = "".join(hap(70 + (i % 2) * 484, 1110 + (i // 2) * 150, 456, m, 46, gk)
                     for i, (m, gk) in enumerate([("BANKA YOK", 1.5), ("FAİZ YOK", 2.5), ("KREDİ YOK", 3.7), ("ARA ÖDEME YOK", 4.8)]))
    kapanis = f"""
      <div class="a gir" style="--g:.1;left:0;top:0;width:{W}px;height:{H}px;background:rgba({r},{g},{b},.5)"></div>
      <div class="a pat" style="--g:.25;left:90px;top:330px;width:900px;height:1220px;border-radius:44px;background:#fff;box-shadow:0 30px 70px rgba(8,20,45,.5)"></div>
      <img class="a gir" src="{VEK('mia-lacivert.svg')}" style="--g:.5;left:{W // 2 - 150}px;top:384px;width:300px">
      <div class="a tek gir" style="--g:.8;left:0;top:626px;width:{W}px;text-align:center;font-size:27px;font-weight:800;letter-spacing:.22em;color:#4a5878">TEK YETKİLİ SATIŞ</div>
      <img class="a gir" src="{VEK('ocean-lacivert.svg')}" style="--g:1.0;left:{W // 2 - 170}px;top:676px;width:340px">
      <div class="a gir" style="--g:1.0;left:240px;top:836px;width:600px;height:3px;background:{VURGU}"></div>
      <div class="a tek gir" style="--g:2.5;left:0;top:880px;width:{W}px;text-align:center;font-size:30px;font-weight:800;letter-spacing:.2em;color:{KOYU}">HEMEN ARAYIN</div>
      <div class="a k tek pat" style="--g:2.7;left:0;top:928px;width:{W}px;text-align:center;font-size:150px;color:{KOYU}">444 10 58</div>
      <div class="a pat" style="--g:3.3;left:0;top:1120px;width:{W}px;display:flex;align-items:center;justify-content:center;gap:18px">{yy.WA.format(s=62)}
        <span class="k tek" style="font-size:60px;color:{KOYU}">0540 028 00 41</span></div>
      {hap(250, 1240, 580, "YERİNİZİ AYIRTIN", 42, 4.8)}
      <div class="a tek gir" style="--g:5.1;left:0;top:1376px;width:{W}px;text-align:center;font-size:32px;font-weight:700;letter-spacing:.08em;color:#4a5878">miaparkocean.com</div>
      <img class="a gir" src="{VEK('tilda.svg')}" style="--g:5.3;left:{W // 2 - 110}px;top:1452px;width:220px">"""
    sahneler = (
        blok(0.25, 3.45, ikili(330, "KOCAELİ", "EV SAHİBİ OLUYOR!", .15, 104, 58))
        + blok(0, T_HARITA - .1, harita)
        + blok(5.7, 5.5, ikili(1340, "HER YERE YAKIN", "İZMİT MİA BÖLGESİ", .1, 72, 46))
        + blok(11.5, .9, f'<div class="a" style="left:0;top:0;width:{W}px;height:{H}px;background:#fff"></div>', "flas")
        + blok(11.7, 2.3, ikili(1150, "MİA PARK OCEAN", "İZMİT'İN YENİ YAŞAM ALANI", .25, 80, 44))
        + blok(14.0, 8.0, fiyat_karti("1+0 DAİRELER · BRÜT 28 m²", "699.000", "29.900", (.3, 1.7, 4.5, 6.4)))
        + blok(22.0, 7.8, fiyat_karti("1+1 DAİRELER · BRÜT 50 m²", "999.000", "39.900", (.3, 1.8, 4.5, 6.3)))
        + blok(29.8, 4.4, ikili(320, "ÜSTELİK TAM", "60 AY SABİT TAKSİT", .3, 70, 62) + tablo(1090, 1.2))
        + blok(34.2, 6.2, ikili(320, "MİA PARK OCEAN'DA", "BANKASIZ EV SAHİBİ OLUN", .3, 70, 46) + yoklar)
        + blok(40.4, TOPLAM - 40.4, kapanis, "sahne son")
    )
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{yy.css(H)}
body {{ background:transparent; }}
.sahne, .flas {{ position:absolute; left:0; top:0; width:{W}px; height:{H}px; animation:sahne calc(var(--d)*1s) linear calc(var(--s)*1s) both; }}
.sahne.son {{ animation-name:sahne-son; }}
.flas {{ animation-name:flas; }}
@keyframes sahne {{ 0%{{opacity:0}} .1%{{opacity:1}} 94%{{opacity:1}} 100%{{opacity:0}} }}
@keyframes sahne-son {{ 0%{{opacity:0}} .1%{{opacity:1}} 100%{{opacity:1}} }}
@keyframes flas {{ 0%{{opacity:0}} 22%{{opacity:.92}} 100%{{opacity:0}} }}
.gir {{ animation:gir .5s cubic-bezier(.2,.9,.25,1) calc((var(--s) + var(--g))*1s) both; }}
.pat {{ animation:pat .55s cubic-bezier(.2,.9,.25,1) calc((var(--s) + var(--g))*1s) both; }}
.soldan {{ animation:soldan .55s cubic-bezier(.2,.9,.25,1) calc((var(--s) + var(--g))*1s) both; }}
.dus {{ animation:dus .6s cubic-bezier(.3,1.4,.5,1) calc((var(--s) + var(--g))*1s) both; }}
.ciz {{ animation:ciz .45s ease-out calc((var(--s) + var(--g))*1s) both; }}
@keyframes gir {{ from{{opacity:0;transform:translateY(46px)}} to{{opacity:1;transform:none}} }}
@keyframes pat {{ 0%{{opacity:0;transform:scale(.55)}} 60%{{opacity:1;transform:scale(1.07)}} 100%{{opacity:1;transform:scale(1)}} }}
@keyframes soldan {{ from{{opacity:0;transform:translateX(-160px)}} to{{opacity:1;transform:none}} }}
@keyframes dus {{ from{{opacity:0;transform:translateY(-260px)}} to{{opacity:1;transform:none}} }}
@keyframes ciz {{ from{{stroke-dashoffset:1}} to{{stroke-dashoffset:0}} }}
{harita_stil}
</style></head><body>
  {blok(0, 40.5, f'''<div class="a" style="left:0;top:0;width:{W}px;height:420px;background:linear-gradient(180deg,rgba({r},{g},{b},.62),rgba({r},{g},{b},0))"></div>
    <img class="a" src="{VEK('mia-beyaz.svg')}" style="left:{W // 2 - 84}px;top:150px;width:168px">''')}
  {blok(0, T_HARITA - .2, f'''<div class="a tek" style="left:0;top:1590px;width:{W}px;text-align:center;font-size:19px;font-weight:600;letter-spacing:.04em;
    color:rgba(255,255,255,.82)">Uydu görüntüsü: Copernicus Sentinel-2 (2016) · EOX, CC BY 4.0</div>''')}
  {sahneler}
</body></html>"""


# ---------------------------------------------------------------- zemin görüntüsü
# (başlangıç sn, tür, kaynak, kaynakta başlangıç sn, yavaşlatma, kaydırma başı, kaydırma sonu)
ZEMIN = [
    (0.0, "harita", None, 0, 1, 0, 0),
    (T_HARITA, "klip", "13-giris-drone", 0.4, 1.0, .50, .50),
    (14.0, "klip", "09-daire-1plus0", 0.0, 1.14, .34, .60),
    (22.0, "klip", "10-daire-1plus1", 0.0, 1.12, .28, .60),
    (29.8, "foto", os.path.join(ROOT, "sosyal-medya", "bitmis-fotograflar", "15-balkondan-gunesli.jpg"), 0, 1, 0, 0),
    (34.2, "klip", "04-avlu-suzulme", 1.4, 1.0, .55, .86),
    (40.4, "klip", "02-sokak-drone", 0.3, 1.0, .52, .42),
]


def zemin(gecici):
    harita = os.path.join(gecici, "harita.mp4")
    harita_videosu(harita, T_HARITA + GECIS)
    girdi, f = [], []
    for i, (bas, tur, kaynak, kbas, yavas, p0, p1) in enumerate(ZEMIN):
        son = ZEMIN[i + 1][0] if i + 1 < len(ZEMIN) else TOPLAM
        sure = son - bas + (GECIS / 2 if i else 0) + (GECIS / 2 if i + 1 < len(ZEMIN) else 0)
        if tur == "harita":
            girdi += ["-i", harita]
            f.append(f"[{i}:v]trim=duration={sure:.3f},setpts=PTS-STARTPTS,fps={FPS},settb=1/{FPS},setsar=1,format=yuv420p[v{i}]")
        elif tur == "foto":
            n = round(sure * FPS)
            girdi += ["-loop", "1", "-framerate", str(FPS), "-t", f"{sure:.3f}", "-i", kaynak]
            f.append(f"[{i}:v]scale=2160:-2:flags=lanczos,crop=2160:3840:0:'(ih-3840)*.5',"
                     f"zoompan=z='1+.09*on/{n}':x='iw/2-(iw/zoom/2)':y='ih*.56-(ih/zoom)*.56':d=1:s={W}x{H}:fps={FPS},"
                     f"trim=duration={sure:.3f},fps={FPS},settb=1/{FPS},setsar=1,format=yuv420p[v{i}]")
        else:
            girdi += ["-ss", f"{kbas:.3f}", "-i", KLIP(kaynak)]
            f.append(f"[{i}:v]setpts={yavas}*PTS,fps={FPS},scale=-2:{H}:flags=lanczos,"
                     f"crop={W}:{H}:'(iw-{W})*({p0}+({p1 - p0})*t/{sure:.3f})':0,unsharp=5:5:.55,eq=brightness=.02:saturation=1.08,"
                     f"trim=duration={sure:.3f},setpts=PTS-STARTPTS,fps={FPS},settb=1/{FPS},setsar=1,format=yuv420p[v{i}]")
    onceki = "v0"
    for i in range(1, len(ZEMIN)):
        f.append(f"[{onceki}][v{i}]xfade=transition=fade:duration={GECIS}:offset={ZEMIN[i][0] - GECIS / 2:.3f}[x{i}]")
        onceki = f"x{i}"
    return girdi, f, onceki


# ---------------------------------------------------------------- ses
VO = [(1, 0.4), (6, 5.9), (3, 14.3), (4, 22.3), (5, 30.1), (2, 34.5), (7, 40.7)]


def ses_oku(yol, filtre=None):
    cmd = ["ffmpeg", "-v", "error", "-i", yol] + (["-af", filtre] if filtre else []) + ["-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).reshape(-1, 2).copy()


def kayan(x, n):
    c = np.cumsum(np.concatenate([[0.0], x]))
    y = (c[n:] - c[:-n]) / n
    return np.concatenate([np.full(n // 2, y[0]), y, np.full(len(x) - len(y) - n // 2, y[-1])])


def vinlama(sure, tepe, dusus, alt=250, ust=3200):
    """Yaklaşma sesi: süzülmüş gürültü, yavaş yükselip çabuk söner."""
    n = int(sure * SR)
    g = np.fft.rfft(np.random.default_rng(7).standard_normal(n))
    fr = np.fft.rfftfreq(n, 1 / SR)
    g[(fr < alt) | (fr > ust)] = 0
    g = np.fft.irfft(g, n)
    t = np.arange(n) / SR
    zarf = np.where(t < tepe, (t / tepe) ** 2.4, np.exp(-(t - tepe) / dusus))
    g = g / np.abs(g).max() * zarf
    return np.stack([g, np.roll(g, 220)], axis=1).astype(np.float32)


def ses(yol):
    n = int(TOPLAM * SR)
    konusma = np.zeros((n, 2), np.float32)
    for i, bas in VO:
        a = ses_oku(SES(i), f"atempo={VO_HIZ}")
        a *= 0.9 / np.abs(a).max()
        j = int(bas * SR)
        konusma[j:j + len(a)] += a[:n - j]
    m = ses_oku(MUZIK)[:n]
    m *= 0.5 / np.sqrt((m ** 2).mean() + 1e-9) * 0.2          # müziği ortak bir düzeye çek
    zarf = kayan(np.abs(konusma).max(axis=1), int(.25 * SR))
    zarf = np.clip(zarf / 0.12, 0, 1)
    m *= (1.0 - 0.62 * kayan(zarf, int(.3 * SR)))[:, None]     # seslendirme varken müzik kısılır
    a, z = int(.3 * SR), int(2.2 * SR)
    m[:a] *= np.linspace(0, 1, a, dtype=np.float32)[:, None]
    m[-z:] *= (np.linspace(1, 0, z, dtype=np.float32) ** 1.4)[:, None]
    efekt = np.zeros((n, 2), np.float32)
    for bas, v, kazanc in [(0.0, vinlama(5.6, 4.7, .35), .10), (T_DALIS - .3, vinlama(1.6, .95, .22, 400, 5000), .22)]:
        j = int(bas * SR)
        efekt[j:j + len(v)] += v * kazanc
    miks = np.tanh((konusma + m + efekt) * 1.1) * 0.9
    with wave.open(yol, "wb") as f:
        f.setnchannels(2), f.setsampwidth(2), f.setframerate(SR)
        f.writeframes((miks * 32767).astype(np.int16).tobytes())


# ---------------------------------------------------------------- üretim
def main():
    os.makedirs(OUT, exist_ok=True)
    gecici = tempfile.mkdtemp(prefix="reeldrone-")
    hp = os.path.join(gecici, "sayfa.html")
    open(hp, "w", encoding="utf-8").write(html())
    kare = os.path.join(gecici, "kare")
    os.makedirs(kare)
    n = round(TOPLAM * FPS)
    npm = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    yazi = subprocess.Popen(["node", os.path.join(KOK, "reel-kare.cjs"), hp, kare, str(n), str(FPS), str(W), str(H)],
                            env={**os.environ, "NODE_PATH": npm})
    wav = os.path.join(gecici, "ses.wav")
    ses(wav)
    girdi, f, son = zemin(gecici)
    if yazi.wait():
        raise SystemExit("yazı kareleri çizilemedi")
    k = len(ZEMIN)
    f.append(f"[{son}][{k}:v]overlay=0:0:format=auto,format=yuv420p[v]")
    yol = os.path.join(OUT, "mia-reel-uydudan-eve.mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", *girdi, "-framerate", str(FPS), "-i", os.path.join(kare, "k-%04d.png"), "-i", wav,
                    "-filter_complex", ";".join(f), "-map", "[v]", "-map", f"{k + 1}:a", "-t", f"{TOPLAM}",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "21", "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", str(FPS),
                    "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k", yol], check=True)
    print(f"  → {os.path.relpath(yol, ROOT)} · {os.path.getsize(yol) / 1048576:.1f} MB")
    shutil.rmtree(gecici, ignore_errors=True)


if __name__ == "__main__":
    main()
