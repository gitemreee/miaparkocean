#!/usr/bin/env python3
"""
Reklam filmi — "Kira öder gibi ev sahibi olun" (1080x1920, ~50 sn, 24 fps, seslendirmeli + müzikli).

Kurgu (sahne süreleri seslendirme kayıtlarının uzunluğundan türetilir):
    uydu     Uzaydan İzmit Körfezi'ne iniş
    yakin    A: raylı sistem hatları (planlanan Güney Metro + Körfezray) · B: yaklaşırken beliren yakın yerler
    sokak    Kaldırımda yürüyen çift projeyi işaret eder
    yapim    Yapım aşaması (hızlandırılmış çekim)
    drone    Karşıdan yaklaşıp sola yönelen drone
    iceri    Drone balkondan daireye girer
    d10/d11/d21  Daire içleri + fiyat kartları
    balkon   Balkonda çay · 60 ay sabit taksit
    avlu     Avlu · dört "YOK" damgası
    kapanis  Akşam: 444 10 58, WhatsApp, slogan

Higgsfield ile üretilenler:
    film-source/higgsfield-kare/   dikey kareler (gpt_image_2_6; müşterinin render'ları referans)
    film-source/higgsfield-klip/   bu karelerden çekimler (seedance_2_0, 1080p)
    film-source/ses/yeni/vo-1..10.wav  seslendirme (aşağıdaki SESLENDIRME)
    film-source/muzik/reel-muzik.mp3   müzik (elevenlabs_music_v2_5)

Diğer kaynaklar:
  • Uydu görüntüsü: Sentinel-2 cloudless 2016, EOX IT Services GmbH — CC BY 4.0
    ("Contains modified Copernicus Sentinel data 2016"). Videoda künye yazılıdır.
  • Proje konumu: Google Maps koordinatı (src/data/location.ts).
  • Metro güzergâhları: müşterinin gönderdiği haritadan gözle sayısallaştırıldı — YAKLAŞIK.
    Güney Metro (Gölcük–Başiskele–İzmit) planlanan, Körfezray (Kuzey) yapım aşamasında.
  • Yakın yerlerin koordinatları OpenStreetMap'ten (Photon); süreler müşteriden / src/data/location.ts.

Yazılar Meta'nın Reels güvenli alanında tutulur (üst %14 ve alt %35 önemli yazıdan arındırılır).

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
from PIL import Image, ImageEnhance, ImageFilter

KOK = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("yy", os.path.join(KOK, "build-reklam-yeni-yuzler.py"))
yy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(yy)

ROOT, F, KIRMIZI = yy.ROOT, yy.F, yy.KIRMIZI
OUT = os.path.join(ROOT, "sosyal-medya", "instagram-reel")
ONBELLEK = os.path.join(ROOT, "film-source", ".kare-onbellek", "uydu")
HF = os.path.join(ROOT, "film-source", "higgsfield-klip")
SES_KLASOR = os.path.join(ROOT, "film-source", "ses", "yeni")
MUZIK = os.path.join(ROOT, "film-source", "muzik", "reel-muzik.mp3")
VEK = lambda ad: F("public", "brand", "vektor", ad)
KLIP = lambda ad: os.path.join(HF, ad + ".mp4")
W, H, FPS, SR = 1080, 1920, 24, 44100
KOYU, VURGU = yy.LACI
GUNEY, KUZEY = "#e0218a", "#2fbf71"
GECIS = 0.25
VO_HIZ = 1.04

# ---------------------------------------------------------------- seslendirme ve zaman çizelgesi
# Sayılar yazıyla, marka "Mia Park Oşın" okunacak biçimde yazılır. Her satır ayrı kayıttır.
SESLENDIRME = [
    "Kocaeli'de, İzmit Körfezi'nin kıyısında yeni bir hayat başlıyor.",
    "Planlanan Güney Metro hattının güzergâhında.",
    "Kira öder gibi ev sahibi olmak artık mümkün.",
    "Mia Park Oşın, Tilda İnşaat ile adım adım yükseliyor.",
    "Buyurun, yeni evinize.",
    "Bir artı sıfır, altı yüz doksan dokuz bin lira peşinatla.",
    "Bir artı bir, dokuz yüz doksan dokuz bin lira peşinatla.",
    "İki artı bir, iki milyon lira peşinatla.",
    "Ayda yirmi dokuz bin dokuz yüz liradan başlayan, altmış ay sabit taksit.",
    "Banka yok! Faiz yok! Kefil yok! Ara ödeme yok!",
    "Hemen arayın: dört yüz kırk dört, on, elli sekiz.",
]
# (sahne, en az süre, seslendirme no, seslendirmeden sonraki pay, seslendirmenin sahne içindeki gecikmesi)
# pay None ise sahne seslendirmeye göre uzamaz (satır sonraki sahneye taşabilir).
SAHNE = [
    ("uydu", 3.6, 1, None, 1.1), ("yakin", 7.2, 2, None, 2.3), ("sokak", 3.2, 3, .3, .25), ("yapim", 7.0, 4, None, .5),
    ("drone", 3.0, None, None, 0), ("iceri", 2.7, 5, None, .6), ("d10", 3.9, 6, .2, .15), ("d11", 3.9, 7, .2, .15),
    ("d21", 3.5, 8, .2, .15), ("balkon", 3.4, 9, .2, .15), ("avlu", 4.6, 10, .5, .2), ("kapanis", 5.6, 11, 1.3, .2),
]
# "Banka yok! Faiz yok! Kefil yok! Ara ödeme yok!" satırında her "yok"un başladığı an (satır süresine oran)
DAMGA_ORAN = (0.0, .22, .485, .735)


def vo_yol(i):
    return os.path.join(SES_KLASOR, f"vo-{i}.wav")


def vo_sure(i):
    if not i or not os.path.exists(vo_yol(i)):
        return 0.0
    with wave.open(vo_yol(i)) as w:
        return w.getnframes() / w.getframerate() / VO_HIZ


SESLI = all(os.path.exists(vo_yol(i)) for i in range(1, len(SESLENDIRME) + 1))
SURE, T, VO_BAS = {}, {}, {}
_t = 0.0
for _ad, _en_az, _vo, _pay, _gec in SAHNE:
    _uz = round((_gec + vo_sure(_vo) + _pay) * FPS) / FPS if SESLI and _vo and _pay is not None else 0
    SURE[_ad] = max(_en_az, _uz)
    T[_ad] = _t
    if _vo:
        VO_BAS[_vo] = _t + _gec
    _t += SURE[_ad]
TOPLAM = _t

# ---------------------------------------------------------------- harita (zamanlar harita sahnesinin başına göre)
LAT, LON = 40.736667, 29.944889          # proje (Google Maps koordinatı)
SX, SY = 500, 1040                        # projenin ekrandaki yeri
Z0, Z1 = 7.2, 12.0                        # yaklaşmanın başı ve sonu (harita yakınlığı)
ZB = 0.85                                 # yakın yerler için ek yakınlaşma (2^ZB kat)
M0 = T["uydu"]
T_ZOOM = SURE["uydu"] - .1                # iniş biter, hatlar çizilir
T_A = T_ZOOM + 3.2                        # yakın yerlere yaklaşma başlar
T_B = T_A + .8
T_HARITA = SURE["uydu"] + SURE["yakin"]
T_DALIS = T_HARITA - .5
LW, LH, LMIN, LMAX = 3584, 5120, 8, 14
UYDU = "https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless_3857/default/g/{z}/{y}/{x}.jpg"

# (ad, süre, enlem, boylam, etiketin tarafı, etiketin dikey kayması, yaklaşma başladıktan kaç sn sonra belirir)
YAKIN = [
    ("Sahil", "2 dk", 40.7367, 29.9395, "sol", 0, .0),
    ("41 Burda AVM", "2 dk", 40.75675, 29.94756, "sol", 0, .25),
    ("İzmit Outlet Center", "2 dk", 40.75548, 29.94690, "sag", -64, .5),
    ("Symbol AVM", "7 dk", 40.75787, 29.97956, "sag", 60, .85),
    ("Şehir Merkezi", "5 dk", 40.77211, 29.95056, "sol", 0, 1.1),
    ("Şehir Hastanesi", "5 dk", 40.78309, 29.96064, "sag", 0, 1.35),
    ("Kocaeli Üniversitesi", "10 dk", 40.81874, 29.92291, "sag", 0, 1.6),
]
# Yaklaşırken görünen coğrafi adlar: (ad, enlem, boylam, göründüğü yakınlık aralığı, punto)
COGRAFYA = [
    ("KARADENİZ", 42.25, 30.6, 7.2, 8.6, 40),
    ("İSTANBUL", 41.02, 28.97, 7.2, 10.0, 34),
    ("MARMARA DENİZİ", 40.68, 28.2, 7.4, 9.6, 30),
    ("BURSA", 40.19, 29.06, 7.6, 9.8, 30),
    ("KOCAELİ", 40.93, 29.92, 8.6, 10.6, 44),
    ("SAPANCA GÖLÜ", 40.715, 30.26, 9.8, 11.5, 26),
    ("İZMİT KÖRFEZİ", 40.735, 29.74, 10.0, 11.6, 30),
]


def _harita_pikseli(x, y):
    """Müşterinin gönderdiği metro haritasındaki pikseli enlem/boylama çevirir (proje 940,340; ~60 px/km)."""
    return LAT - (y - 340) / 60 / 111.2, LON + (x - 940) / 60 / 84.39


HAT_GUNEY = [_harita_pikseli(*p) for p in [
    (260, 525), (320, 520), (360, 522), (405, 524), (455, 523), (535, 578), (580, 612), (672, 608), (718, 601), (770, 580),
    (835, 563), (883, 540), (920, 507), (938, 420), (940, 340), (945, 300), (938, 218), (903, 153)]]
HAT_KUZEY = [_harita_pikseli(*p) for p in [
    (85, 75), (128, 88), (172, 97), (243, 126), (322, 182), (373, 210), (422, 196), (490, 214), (577, 182), (662, 178),
    (740, 178), (800, 174), (855, 152), (903, 153), (940, 96), (1015, 80), (1045, 120), (1035, 160), (1047, 200),
    (1108, 212), (1207, 246), (1275, 270), (1362, 298), (1428, 330), (1480, 355)]]
# (ad, harita pikseli, yazının noktaya göre kayması)
YER_ADI = [("GÖLCÜK", (260, 525), (0, 44)), ("BAŞİSKELE", (835, 563), (70, 46)), ("İZMİT", (903, 153), (-10, -46)),
           ("KARTEPE", (1480, 355), (-20, -46))]


def mpx(lat, lon, z):
    n = 256 * 2 ** z
    return (lon + 180) / 360 * n, (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n


def ekran(lat, lon, z):
    px, py = mpx(lat, lon, z)
    sx, sy = mpx(LAT, LON, z)
    return SX + px - sx, SY + py - sy


def olcek(t):
    """İniş bittikten sonraki büyüme (haritayla çizgiler aynı fonksiyonu kullanır)."""
    if t <= T_ZOOM:
        return 1.0
    if t <= T_A:
        return 1 + .04 * (t - T_ZOOM) / (T_A - T_ZOOM)
    if t <= T_B:
        p = (t - T_A) / (T_B - T_A)
        return 1.04 * 2 ** (ZB * p * p * (3 - 2 * p))
    b = 1.04 * 2 ** ZB
    if t <= T_DALIS:
        return b
    q = (t - T_DALIS) / (T_HARITA - T_DALIS)
    return b * (1 + 1.6 * q ** 3)


def kamera(t):
    """(harita yakınlığı, dönüş açısı). İniş yumuşak başlar, yumuşak konar."""
    if t < T_ZOOM:
        p = t / T_ZOOM
        e = p * p * p * (p * (p * 6 - 15) + 10)
        return Z0 + (Z1 - Z0) * e, -14 * (1 - e)
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
    n = 2 ** z
    tx0, ty0, tx1, ty1 = int(x0 // 256), max(0, int(y0 // 256)), int((x0 + LW) // 256), min(n - 1, int((y0 + LH) // 256))
    os.makedirs(ONBELLEK, exist_ok=True)
    isler = [(UYDU.format(z=z, x=x % n, y=y), os.path.join(ONBELLEK, f"{z}-{x % n}-{y}.jpg"))
             for x in range(tx0, tx1 + 1) for y in range(ty0, ty1 + 1)]
    with ThreadPoolExecutor(12) as havuz:
        list(havuz.map(lambda a: _indir(*a), isler))
    im = Image.new("RGB", (LW, LH), (6, 14, 30))
    for x in range(tx0, tx1 + 1):
        for y in range(ty0, ty1 + 1):
            im.paste(Image.open(os.path.join(ONBELLEK, f"{z}-{x % n}-{y}.jpg")).convert("RGB"), (round(x * 256 - x0), round(y * 256 - y0)))
    im = ImageEnhance.Brightness(im).enhance(1.16)
    im = ImageEnhance.Contrast(im).enhance(1.1)
    return ImageEnhance.Color(im).enhance(1.3)


def bulut_dokusu():
    """İnişin başında içinden geçilen ince bulut tabakası (fraktal gürültü)."""
    rng = np.random.default_rng(11)
    bw, bh = 2160, 3840
    top = np.zeros((bh, bw), np.float32)
    for o in range(6):
        g = (rng.random((8 * 2 ** o, 5 * 2 ** o)) * 255).astype(np.uint8)
        top += np.asarray(Image.fromarray(g).resize((bw, bh), Image.BICUBIC), np.float32) / 255 / 1.85 ** o
    top = (top - top.min()) / (top.max() - top.min())
    a = np.clip((top - .5) / .26, 0, 1)
    a = a * a * (3 - 2 * a)
    return Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(5))


def bulut(t, doku):
    p = (t - .05) / (T_ZOOM * .55)
    if not 0 < p < 1:
        return None
    s = 1 + 7 * p ** 1.7
    bw, bh = doku.size
    w, h = bw / s, bh / s
    cx, cy = bw * (.5 + .06 * p), bh * (.52 - .05 * p)
    cx, cy = min(max(cx, w / 2), bw - w / 2), min(max(cy, h / 2), bh - h / 2)
    a = doku.resize((W, H), Image.BILINEAR, box=(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2))
    return a.point(lambda v, k=.9 * (1 - p) ** 1.3 * min(1, p * 10): int(v * k))


def harita_karesi(t, sev, doku):
    z, aci = kamera(t)
    lv = min(max(math.ceil(z), LMIN), LMAX)
    f = 2 ** (lv - z)
    mw, mh = 1700, 2560
    kutu = (LW / 2 - mw / 2 * f, LH / 2 - mh / 2 * f, LW / 2 + mw / 2 * f, LH / 2 + mh / 2 * f)
    m = sev[lv].resize((mw, mh), Image.LANCZOS, box=kutu)
    if aci:
        m = m.rotate(aci, Image.BICUBIC)
    m = m.crop((mw // 2 - SX, mh // 2 - SY, mw // 2 - SX + W, mh // 2 - SY + H))
    b = bulut(t, doku)
    if b:
        m.paste(Image.new("RGB", (W, H), (246, 250, 255)), (0, 0), b)
    return m


def harita_videosu(yol, sure):
    sev = {z: seviye(z) for z in range(LMIN, LMAX + 1)}
    doku = bulut_dokusu()
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "fast", "-crf", "12", "-pix_fmt", "yuv420p", yol], stdin=subprocess.PIPE)
    for k in range(round(sure * FPS)):
        p.stdin.write(harita_karesi(k / FPS, sev, doku).tobytes())
    p.stdin.close()
    p.wait()


# ---------------------------------------------------------------- yazı katmanı (HTML)
GOLGE = "text-shadow:0 3px 18px rgba(4,12,30,.75),0 1px 3px rgba(4,12,30,.6)"


def blok(bas, sure, icerik, sinif="sahne"):
    return f'<div class="{sinif}" style="--s:{bas:.3f};--d:{sure:.3f}">{icerik}</div>'


def baslik(y, ust, ana, g, ana_boy=92):
    """Sinema dili: ince üst satır, altın çizgi, büyük beyaz başlık."""
    return f"""<div class="a" style="left:0;top:{y}px;width:{W}px;text-align:center">
      <div class="tek gir" style="--g:{g};font-size:30px;font-weight:700;letter-spacing:.42em;color:#fff;{GOLGE}">{ust}</div>
      <div class="cizgi" style="--g:{g + .12};width:150px;height:5px;margin:22px auto 20px;background:{VURGU}"></div>
      <div class="k gir" style="--g:{g + .2};font-size:{ana_boy}px;line-height:1.08;color:#fff;{GOLGE}">{ana}</div></div>"""


def ikili(y, ust, alt, g, ust_boy=84, alt_boy=50):
    """Onaylı fiyat kartının dili: koyu katman + altın şerit."""
    return f"""<div class="a" style="left:0;top:{y}px;width:{W}px;text-align:center">
      <div class="pat" style="--g:{g};display:inline-block;border-radius:26px;overflow:hidden;box-shadow:0 18px 40px rgba(8,20,45,.4)">
        <div class="k tek" style="background:{KOYU};color:#fff;font-size:{ust_boy}px;padding:{round(ust_boy * .34)}px {round(ust_boy * .62)}px {round(ust_boy * .3)}px">{ust}</div>
        <div class="k tek" style="background:{VURGU};color:{KOYU};font-size:{alt_boy}px;padding:{round(alt_boy * .42)}px {round(alt_boy * .6)}px {round(alt_boy * .38)}px">{alt}</div>
      </div></div>"""


def hap(x, y, gen, metin, boy, g, renk=KIRMIZI, yazi="#fff", sinif="pat"):
    return (f'<div class="a tek {sinif}" style="--g:{g:.2f};left:{x}px;top:{y}px;width:{gen}px;padding:{round(boy * .62)}px 0;'
            f'border-radius:{round(boy * .72)}px;background:{renk};color:{yazi};text-align:center;font-size:{boy}px;font-weight:800;'
            f'letter-spacing:.02em;box-shadow:0 14px 30px rgba(8,20,45,.34)">{metin}</div>')


def fiyat_karti(tip, pesin, ayda, sure):
    """Seslendirmeyle sırayla açılan fiyat kartı: tip → peşinat → aylık → 60 ay."""
    x, gen = 200, 680
    g = (.12, .12 * sure, .38 * sure, .56 * sure)
    return (hap(x + 150, 768, gen - 300, tip, 34, g[0], "#fff", KOYU)
            + f"""<div class="a pat" style="--g:{g[1]:.2f};left:{x}px;top:852px;width:{gen}px;height:196px;border-radius:26px 26px 0 0;background:{KOYU};
                   text-align:center;color:#fff;box-shadow:0 18px 40px rgba(8,20,45,.4);display:flex;flex-direction:column;justify-content:center">
                <div class="k tek" style="font-size:{108 if len(pesin) < 8 else 94}px">{pesin}<span style="font-size:40px;letter-spacing:0;margin-left:10px">TL</span></div>
                <div class="tek" style="margin-top:8px;font-size:32px;font-weight:800;letter-spacing:.14em">PEŞİNAT</div></div>
              <div class="a pat" style="--g:{g[2]:.2f};left:{x}px;top:1048px;width:{gen}px;padding:22px 0 20px;border-radius:0 0 26px 26px;background:{VURGU};
                   text-align:center;color:{KOYU};box-shadow:0 18px 40px rgba(8,20,45,.4)">
                <div class="k tek" style="font-size:64px"><span style="font-size:32px;letter-spacing:.08em;margin-right:14px">AYDA</span>{ayda}<span style="font-size:30px;letter-spacing:0;margin-left:9px">TL</span></div></div>"""
            + hap(x + 90, 1176, gen - 180, "60 AY SABİT TAKSİT", 36, g[3]))


def damgalar(bas_gecikme, satir_sure):
    """Dört 'YOK' — her biri seslendirmedeki sözle aynı anda, büyük ve tok biçimde iner."""
    govde = ""
    for i, m in enumerate(["BANKA YOK", "FAİZ YOK", "KEFİL YOK", "ARA ÖDEME YOK"]):
        g = bas_gecikme + DAMGA_ORAN[i] * satir_sure
        govde += (f'<div class="a k tek damga" style="--g:{g:.2f};left:110px;top:{470 + i * 172}px;width:860px;height:146px;border-radius:26px;background:{KIRMIZI};'
                  f'color:#fff;font-size:{84 if len(m) < 12 else 76}px;display:flex;align-items:center;justify-content:center;'
                  f'box-shadow:0 20px 44px rgba(120,10,20,.45)">{m}</div>')
    return govde


def cografya():
    """İnerken yer adları haritaya sabitlenmiş gibi akar: her kare için konum hesaplanır."""
    stil, govde = "", ""
    n = round(T_ZOOM * FPS)
    for i, (ad, lat, lon, z_in, z_out, boy) in enumerate(COGRAFYA):
        kare = ""
        for k in range(n + 1):
            z, aci = kamera(k / FPS)
            px, py = mpx(lat, lon, z)
            sx, sy = mpx(LAT, LON, z)
            dx, dy, r = px - sx, py - sy, math.radians(aci)
            x = SX + dx * math.cos(r) + dy * math.sin(r)
            y = SY - dx * math.sin(r) + dy * math.cos(r)
            o = max(0.0, min(1.0, (z - z_in) / .35, (z_out - z) / .35))
            kare += f"{100 * k / n:.3f}%{{transform:translate({x:.1f}px,{y:.1f}px);opacity:{o:.3f}}}"
        stil += f"@keyframes cog{i}{{{kare}}}\n"
        govde += (f'<div class="a tek" style="left:0;top:0;animation:cog{i} {T_ZOOM:.3f}s linear {M0:.3f}s both">'
                  f'<div style="transform:translate(-50%,-50%);font-size:{boy}px;font-weight:700;letter-spacing:.3em;color:#fff;{GOLGE}">{ad}</div></div>')
    return stil, govde


def hatlar():
    """Haritayla birlikte büyüyen katman: iki raylı sistem hattı, duraklar ve A bölümünün yazıları."""
    def yol(noktalar, renk, g):
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in (ekran(la, lo, Z1) for la, lo in noktalar))
        ort = (f'<polyline points="{p}" fill="none" stroke="#fff" stroke-width="13" stroke-linecap="round" stroke-linejoin="round" pathLength="1" '
               f'stroke-dasharray="1" stroke-dashoffset="1" class="hat" style="--g:{g:.2f}" opacity=".95"/>'
               f'<polyline points="{p}" fill="none" stroke="{renk}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" pathLength="1" '
               f'stroke-dasharray="1" stroke-dashoffset="1" class="hat" style="--g:{g:.2f}"/>')
        durak = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6.5" fill="#fff" stroke="{renk}" stroke-width="3" class="belir" style="--g:{g + .9 + i * .03:.2f}"/>'
                        for i, (x, y) in enumerate(ekran(la, lo, Z1) for la, lo in noktalar[1:-1]))
        return ort + durak
    g0 = M0 + T_ZOOM
    svg = yol(HAT_KUZEY, KUZEY, g0 + .05) + yol(HAT_GUNEY, GUNEY, g0 + .35)
    adlar = ""
    for ad, piksel, (dx, dy) in YER_ADI:
        x, y = ekran(*_harita_pikseli(*piksel), Z1)
        adlar += (f'<div class="a tek gir" style="--g:.45;left:{x + dx:.0f}px;top:{y + dy:.0f}px;transform:translate(-50%,-50%)">'
                  f'<div style="transform:translate(-50%,-50%);font-size:27px;font-weight:800;letter-spacing:.22em;color:#fff;{GOLGE}">{ad}</div></div>')
    cip = lambda x, y, renk, ust, alt, g: (
        f'<div class="a pat" style="--g:{g};left:{x}px;top:{y}px;border-radius:16px;overflow:hidden;box-shadow:0 12px 26px rgba(8,20,45,.5);display:flex;transform-origin:0 50%">'
        f'<span class="k tek" style="background:{renk};color:#fff;font-size:27px;padding:15px 18px 13px">{ust}</span>'
        f'<span class="tek" style="background:#fff;color:{KOYU};font-size:25px;font-weight:800;padding:16px 16px 13px">{alt}</span></div>')
    yazilar = (adlar + cip(54, 740, KUZEY, "KÖRFEZRAY", "YAPIM AŞAMASINDA", .5)
               + cip(54, 1290, GUNEY, "GÜNEY METRO HATTI", "PLANLANAN", .8))
    adim = 0.04
    n = round((T_HARITA + .3 - T_ZOOM) / adim)
    kare = "".join(f"{100 * k / n:.3f}%{{transform:scale({olcek(T_ZOOM + k * adim):.5f})}}" for k in range(n + 1))
    stil = (f"@keyframes harita{{{kare}}}\n.harita{{position:absolute;left:0;top:0;width:{W}px;height:{H}px;transform-origin:{SX}px {SY}px;"
            f"animation:harita {n * adim:.3f}s linear {M0 + T_ZOOM:.3f}s both}}")
    govde = (f'<div class="harita"><svg class="a" style="left:0;top:0;overflow:visible" width="{W}" height="{H}">{svg}</svg>'
             + blok(M0 + T_ZOOM - .1, T_A - T_ZOOM + .15, yazilar) + '</div>')
    return stil, govde


def yakin_yerler():
    """Yakın yerler: harita yaklaşırken birer birer belirir ve haritaya sabitlenmiş gibi onunla birlikte kayar."""
    stil, govde = "", ""
    t0 = T_A - .1
    n = round((T_HARITA - t0) * FPS)
    for i, (ad, sure, lat, lon, taraf, dy, belirme) in enumerate(YAKIN):
        kare = ""
        for k in range(n + 1):
            t = t0 + k / FPS
            x, y = ekran(lat, lon, kamera(t)[0])
            o = max(0.0, min(1.0, (T_DALIS + .2 - t) / .2))
            kare += f"{100 * k / n:.3f}%{{transform:translate({x:.1f}px,{y:.1f}px);opacity:{o:.2f}}}"
        stil += f"@keyframes poi{i}{{{kare}}}\n"
        g = M0 + T_A + belirme
        yer = "right:26px;transform-origin:100% 50%" if taraf == "sol" else "left:26px;transform-origin:0 50%"
        govde += f"""<div class="a" style="left:0;top:0;width:0;height:0;--s:0;animation:poi{i} {n / FPS:.3f}s linear {M0 + t0:.3f}s both">
            <div class="a pat" style="--g:{g:.2f};left:-13px;top:-13px;width:26px;height:26px;border-radius:50%;background:#fff;border:6px solid {KIRMIZI}"></div>
            <div class="a pat" style="--g:{g + .08:.2f};top:{dy - 31}px;{yer};display:flex;border-radius:16px;overflow:hidden;box-shadow:0 12px 26px rgba(8,20,45,.45)">
              <span class="tek" style="background:#fff;color:{KOYU};font-size:29px;font-weight:800;padding:14px 16px 13px">{ad}</span>
              <span class="k tek" style="background:{VURGU};color:{KOYU};font-size:29px;padding:15px 14px 12px">{sure}</span></div></div>"""
    return stil, govde


def html():
    hat_stil, hat = hatlar()
    poi_stil, poi = yakin_yerler()
    cog_stil, cog = cografya()
    r, g, b = (int(KOYU[j:j + 2], 16) for j in (1, 3, 5))
    g0 = T_ZOOM - .9
    igne = f"""<svg class="a dus" style="--g:{g0:.2f};left:{SX - 44}px;top:{SY - 112}px;width:88px;height:114px" viewBox="0 0 88 114">
        <path d="M44 112C44 112 6 66 6 42a38 38 0 1 1 76 0c0 24-38 70-38 70z" fill="{KIRMIZI}" stroke="#fff" stroke-width="5"/><circle cx="44" cy="42" r="15" fill="#fff"/></svg>"""
    igne += hap(SX - 215, SY + 24, 430, "MİA PARK OCEAN", 38, g0 + .3, "#fff", KOYU)
    kapanis = f"""
      <div class="a gir" style="--g:.05;left:0;top:0;width:{W}px;height:{H}px;background:linear-gradient(180deg,rgba({r},{g},{b},0) 0,rgba({r},{g},{b},0) 54%,
           rgba({r},{g},{b},.92) 61%,{KOYU} 65%)"></div>
      <div class="a k tek pat" style="--g:.5;left:0;top:1150px;width:{W}px;text-align:center;font-size:158px;color:#fff">444 10 58</div>
      <div class="a pat" style="--g:1.1;left:0;top:1334px;width:{W}px;display:flex;align-items:center;justify-content:center;gap:18px">{yy.WA.format(s=56)}
        <span class="k tek" style="font-size:54px;color:#fff">0540 028 00 41</span></div>
      <div class="a tek gir" style="--g:1.7;left:0;top:1420px;width:{W}px;text-align:center;font-size:31px;font-weight:700;color:{VURGU}">60 ay sabit taksitle ev sahibi olmanın tam zamanı!</div>
      <div class="a gir" style="--g:2.1;left:0;top:1484px;width:{W}px;display:flex;align-items:center;justify-content:center;gap:24px">
        <span class="tek" style="font-size:21px;font-weight:700;letter-spacing:.2em;color:rgba(255,255,255,.85)">TEK YETKİLİ SATIŞ</span>
        <img src="{VEK('ocean-beyaz.svg')}" style="height:60px"></div>"""
    sahneler = (
        blok(M0 + .15, T_ZOOM - 1.1, baslik(450, "KOCAELİ · İZMİT", "YENİ BİR HAYAT<br>BAŞLIYOR", .15, 88))
        + blok(T["sokak"] + .1, SURE["sokak"] - .1, baslik(450, "İZMİT · MİA BÖLGESİ", "KİRA ÖDER GİBİ<br>EV SAHİBİ OLUN", .2, 88))
        + blok(M0, T_ZOOM, cog)
        + blok(M0, T_HARITA - .1, hat)
        + blok(M0, T_HARITA - .1, igne)
        + poi
        + blok(M0 + T_HARITA - .12, .9, f'<div class="a" style="left:0;top:0;width:{W}px;height:{H}px;background:#fff"></div>', "flas")
        + blok(T["yapim"] + .2, SURE["yapim"] - .2, baslik(450, "TİLDA İNŞAAT İLE", "ADIM ADIM<br>YÜKSELİYOR", .2, 88))
        + blok(T["drone"] + .1, SURE["drone"] - .1, baslik(450, "İZMİT MİA BÖLGESİ", "MİA PARK OCEAN", .15, 88))
        + blok(T["d10"], SURE["d10"], fiyat_karti("1+0 DAİRELER", "699.000", "29.900", SURE["d10"]))
        + blok(T["d11"], SURE["d11"], fiyat_karti("1+1 DAİRELER", "999.000", "39.900", SURE["d11"]))
        + blok(T["d21"], SURE["d21"], fiyat_karti("2+1 DAİRELER", "2.000.000", "50.000", SURE["d21"]))
        + blok(T["balkon"], SURE["balkon"], ikili(880, "AYDA 29.900 TL'DEN", "60 AY SABİT TAKSİT", .25, 64, 70))
        + blok(T["avlu"], SURE["avlu"], damgalar(VO_BAS.get(10, T["avlu"] + .2) - T["avlu"], vo_sure(10) or 3.6))
        + blok(T["kapanis"], SURE["kapanis"], kapanis, "sahne son")
    )
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{yy.css(H)}
body {{ background:transparent; }}
.sahne, .flas {{ position:absolute; left:0; top:0; width:{W}px; height:{H}px; animation:sahne calc(var(--d)*1s) linear calc(var(--s)*1s) both; }}
.sahne .sahne {{ animation-name:sahne; }}
.sahne.son {{ animation-name:sahne-son; }}
.flas {{ animation-name:flas; }}
@keyframes sahne {{ 0%{{opacity:0}} .1%{{opacity:1}} 93%{{opacity:1}} 100%{{opacity:0}} }}
@keyframes sahne-son {{ 0%{{opacity:0}} .1%{{opacity:1}} 100%{{opacity:1}} }}
@keyframes flas {{ 0%{{opacity:0}} 22%{{opacity:.92}} 100%{{opacity:0}} }}
.gir {{ animation:gir .6s cubic-bezier(.2,.9,.25,1) calc((var(--s) + var(--g))*1s) both; }}
.pat {{ animation:pat .55s cubic-bezier(.2,.9,.25,1) calc((var(--s) + var(--g))*1s) both; }}
.dus {{ animation:dus .6s cubic-bezier(.3,1.4,.5,1) calc((var(--s) + var(--g))*1s) both; }}
.ciz {{ animation:ciz .45s ease-out calc((var(--s) + var(--g))*1s) both; }}
.hat {{ animation:ciz 1.5s cubic-bezier(.4,0,.2,1) calc(var(--g)*1s) both; }}
.belir {{ animation:belir .3s ease-out calc(var(--g)*1s) both; }}
.cizgi {{ animation:cizgi .5s cubic-bezier(.2,.9,.25,1) calc((var(--s) + var(--g))*1s) both; }}
.damga {{ animation:damga .32s cubic-bezier(.2,1.2,.3,1) calc((var(--s) + var(--g))*1s) both; }}
@keyframes gir {{ from{{opacity:0;transform:translateY(46px)}} to{{opacity:1;transform:none}} }}
@keyframes pat {{ 0%{{opacity:0;transform:scale(.55)}} 60%{{opacity:1;transform:scale(1.07)}} 100%{{opacity:1;transform:scale(1)}} }}
@keyframes dus {{ from{{opacity:0;transform:translateY(-260px)}} to{{opacity:1;transform:none}} }}
@keyframes ciz {{ from{{stroke-dashoffset:1}} to{{stroke-dashoffset:0}} }}
@keyframes belir {{ from{{opacity:0}} to{{opacity:1}} }}
@keyframes cizgi {{ from{{opacity:0;transform:scaleX(0)}} to{{opacity:1;transform:none}} }}
@keyframes damga {{ 0%{{opacity:0;transform:scale(2.3)}} 55%{{opacity:1;transform:scale(.96)}} 100%{{opacity:1;transform:scale(1)}} }}
{hat_stil}
{poi_stil}
{cog_stil}
</style></head><body>
  {blok(M0, T_HARITA, f'''<div class="a" style="left:0;top:0;width:{W}px;height:{H}px;background:radial-gradient(ellipse 75% 62% at 50% 54%,rgba(4,12,30,0) 55%,rgba(4,12,30,.5) 100%)"></div>
    <div class="a tek" style="left:0;top:1590px;width:{W}px;text-align:center;font-size:19px;font-weight:600;letter-spacing:.04em;
    color:rgba(255,255,255,.82)">Uydu görüntüsü: Copernicus Sentinel-2 (2016) · EOX, CC BY 4.0 · Metro güzergâhları yaklaşıktır</div>''')}
  <div class="a" style="left:0;top:0;width:{W}px;height:470px;background:linear-gradient(180deg,rgba({r},{g},{b},.66),rgba({r},{g},{b},0))"></div>
  <img class="a" src="{VEK('mia-beyaz.svg')}" style="left:64px;top:270px;width:156px">
  <img class="a" src="{VEK('tilda-beyaz.svg')}" style="left:{W - 64 - 250}px;top:304px;width:250px">
  {sahneler}
</body></html>"""


# ---------------------------------------------------------------- zemin görüntüsü
# (sahne, kaynak, kaynakta başlangıç sn, hız[, (büyütme, kaynakta üst kenar)])
# hız: 1.2 = %20 hızlı. "sigdir" = çekimin tamamı sahneye sığacak biçimde hızlanır/yavaşlar.
ZEMIN = [
    ("uydu", None, 0, 1),
    ("sokak", "20-sokak-cift", 0.2, 1.15),
    ("yapim", "17-yapim-asamasi", 0.0, "sigdir"),
    ("drone", "22-drone-sola", 0.3, 1.15),
    ("iceri", "21-balkondan-iceri", 0.2, "sigdir"),
    ("d10", "07-1-0-salon", 0.2, 1.15),
    ("d11", "09-1-1-salon", 0.2, 1.15),
    ("d21", "11-2-1-salon", 0.2, 1.15),
    ("balkon", "08-1-0-balkon", 0.3, 1.1),
    ("avlu", "04-avlu", 0.2, 1.0),
    ("kapanis", "06-aksam", 0.0, 1.0, (1.5, 640)),
]


def klip_sure(yol):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", yol],
                                capture_output=True, text=True).stdout)


def zemin(gecici):
    harita = os.path.join(gecici, "harita.mp4")
    harita_videosu(harita, T_HARITA + GECIS)
    girdi, f, bas_list = [], [], []
    for i, (ad, kaynak, kbas, hiz, *kirp) in enumerate(ZEMIN):
        bas = T[ad]
        son = T[ZEMIN[i + 1][0]] if i + 1 < len(ZEMIN) else TOPLAM
        sure = son - bas + (GECIS / 2 if i else 0) + (GECIS / 2 if i + 1 < len(ZEMIN) else 0)
        bas_list.append(bas)
        son_ek = f"trim=duration={sure:.3f},setpts=PTS-STARTPTS,fps={FPS},settb=1/{FPS},setsar=1,format=yuv420p[v{i}]"
        if kaynak is None:
            girdi += ["-i", harita]
            f.append(f"[{i}:v]{son_ek}")
            continue
        yol = KLIP(kaynak)
        var = klip_sure(yol) - kbas - .08
        carpan = (sure + .06) / var if hiz == "sigdir" else max(1 / hiz, (sure + .06) / var)
        z, ust = kirp[0] if kirp else (1.0, 0)
        girdi += ["-ss", f"{kbas:.3f}", "-i", yol]
        f.append(f"[{i}:v]setpts={carpan:.4f}*PTS,fps={FPS},scale={round(W * z / 2) * 2}:{round(H * z / 2) * 2}:flags=lanczos,"
                 f"crop={W}:{H}:(iw-{W})/2:{round(ust * z)},{son_ek}")
    onceki = "v0"
    for i in range(1, len(ZEMIN)):
        f.append(f"[{onceki}][v{i}]xfade=transition=fade:duration={GECIS}:offset={bas_list[i] - GECIS / 2:.3f}[x{i}]")
        onceki = f"x{i}"
    # tek renk tonu + hafif film greni: çekimleri birbirine bağlar, yapay parlaklığı kırar
    f.append(f"[{onceki}]eq=contrast=1.04:saturation=.93:gamma=.98,noise=alls=4:allf=t,format=yuv420p[zemin]")
    return girdi, f, "zemin"


# ---------------------------------------------------------------- ses
def ses_oku(yol, filtre=None):
    cmd = ["ffmpeg", "-v", "error", "-i", yol] + (["-af", filtre] if filtre else []) + ["-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).reshape(-1, 2).copy()


def kayan(x, n):
    c = np.cumsum(np.concatenate([[0.0], x]))
    y = (c[n:] - c[:-n]) / n
    return np.concatenate([np.full(n // 2, y[0]), y, np.full(len(x) - len(y) - n // 2, y[-1])])


def vinlama(sure, tepe, dusus, alt=250, ust=3200):
    """Geçiş sesi: süzülmüş gürültü, yavaş yükselip çabuk söner."""
    n = int(sure * SR)
    g = np.fft.rfft(np.random.default_rng(7).standard_normal(n))
    fr = np.fft.rfftfreq(n, 1 / SR)
    g[(fr < alt) | (fr > ust)] = 0
    g = np.fft.irfft(g, n)
    t = np.arange(n) / SR
    zarf = np.where(t < tepe, (t / tepe) ** 2.4, np.exp(-(t - tepe) / dusus))
    g = g / np.abs(g).max() * zarf
    return np.stack([g, np.roll(g, 220)], axis=1).astype(np.float32)


def vurus(sure=.7):
    """Tok vuruş: alçalan sinüs + kısa tık. Damgalarda ve önemli kesmelerde kullanılır."""
    t = np.arange(int(sure * SR)) / SR
    faz = 2 * np.pi * (48 * t + (120 - 48) * .09 * (1 - np.exp(-t / .09)))
    g = np.sin(faz) * np.exp(-t / .22) + .25 * np.random.default_rng(3).standard_normal(len(t)) * np.exp(-t / .012)
    g = g / np.abs(g).max()
    return np.stack([g, g], axis=1).astype(np.float32)


def ses(yol):
    n = int(TOPLAM * SR)
    konusma = np.zeros((n, 2), np.float32)
    if SESLI:
        for vo, bas in VO_BAS.items():
            a = ses_oku(vo_yol(vo), f"atempo={VO_HIZ}" if VO_HIZ != 1 else None)
            a *= 0.80 / np.abs(a).max()
            j = int(bas * SR)
            konusma[j:j + len(a)] += a[:n - j]
    m = np.zeros((n, 2), np.float32)
    if os.path.exists(MUZIK):
        ham = ses_oku(MUZIK)[:n]
        m[:len(ham)] = ham
        m *= 0.5 / np.sqrt((m ** 2).mean() + 1e-9) * (0.28 if SESLI else 0.5)
        zarf = np.clip(kayan(np.abs(konusma).max(axis=1), int(.25 * SR)) / 0.12, 0, 1)
        m *= (1.0 - 0.47 * kayan(zarf, int(.3 * SR)))[:, None]     # seslendirme varken müzik kısılır
        a, z = int(.03 * SR), int(2.4 * SR)
        m[:a] *= np.linspace(0, 1, a, dtype=np.float32)[:, None]
        m[-z:] *= (np.linspace(1, 0, z, dtype=np.float32) ** 1.4)[:, None]
    efekt = np.zeros((n, 2), np.float32)

    def koy(bas, v, kazanc):
        j = max(0, int(bas * SR))
        v = v[:n - j]
        efekt[j:j + len(v)] += v * kazanc

    koy(M0, vinlama(T_ZOOM + .4, T_ZOOM - .3, .35), .08)                       # iniş
    koy(M0 + T_A - .1, vinlama(1.0, .7, .2, 400, 5000), .1)                    # yakın yerlere yaklaşma
    koy(M0 + T_DALIS - .3, vinlama(1.3, .8, .2, 400, 5000), .18)               # projeye dalış
    koy(T["iceri"] - .1, vinlama(SURE["iceri"] + .2, SURE["iceri"] - .5, .3, 300, 4000), .12)   # balkondan içeri
    for ad in ("yapim", "d10", "d11", "d21", "kapanis"):
        koy(T[ad] - .02, vurus(), .22)
    for i, oran in enumerate(DAMGA_ORAN):
        koy(VO_BAS.get(10, T["avlu"] + .2) + oran * (vo_sure(10) or 3.6) + .04, vurus(.8), .34)
    miks = np.tanh((konusma + m + efekt) * 1.1) * 0.9
    with wave.open(yol, "wb") as f:
        f.setnchannels(2), f.setsampwidth(2), f.setframerate(SR)
        f.writeframes((miks * 32767).astype(np.int16).tobytes())


# ---------------------------------------------------------------- üretim
def main():
    os.makedirs(OUT, exist_ok=True)
    print(f"  {'seslendirmeli' if SESLI else 'SESSİZ TASLAK (seslendirme dosyaları eksik)'} · {TOPLAM:.1f} sn · "
          + " ".join(f"{a}={T[a]:.1f}" for a in T))
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
    yol = os.path.join(OUT, "mia-reklam-filmi.mp4" if SESLI else "mia-reklam-filmi-sessiz-taslak.mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", *girdi, "-framerate", str(FPS), "-i", os.path.join(kare, "k-%04d.png"), "-i", wav,
                    "-filter_complex", ";".join(f), "-map", "[v]", "-map", f"{k + 1}:a", "-t", f"{TOPLAM}",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "22", "-maxrate", "9M", "-bufsize", "18M", "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", str(FPS),
                    "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k", yol], check=True)
    print(f"  → {os.path.relpath(yol, ROOT)} · {os.path.getsize(yol) / 1048576:.1f} MB")
    shutil.rmtree(gecici, ignore_errors=True)


if __name__ == "__main__":
    main()
