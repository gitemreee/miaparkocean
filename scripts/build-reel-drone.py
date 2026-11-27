#!/usr/bin/env python3
"""
Reklam Reels'i — "Uydudan eve" (1080x1920, ~46 sn, 24 fps).

Kurgu (sahne süreleri seslendirme kayıtlarının uzunluğundan türetilir):
    uydu     Uzaydan yaklaşma: Karadeniz/Marmara → İzmit Körfezi → projenin tam konumu
    yakin    Yakın yerler: gerçek koordinatlarla çizgiler ve dakika etiketleri
    giris    Projeye dalış: girişe inen drone çekimi
    d10      1+0 daire içi + fiyat kartı
    d11      1+1 daire içi + fiyat kartı
    d21      2+1 daire içi + fiyat kartı
    balkon   Balkondan bakış + 60 ay sabit taksit
    avlu     Avlu + dört "YOK" etiketi
    kapanis  Akşam girişi: logo, 444 10 58, WhatsApp, tek yetkili satış

SES — Higgsfield ile üretilir, dosyalar buraya konur (yoksa video sessiz TASLAK çıkar):
    film-source/ses/yeni/vo-1.wav … vo-9.wav   seslendirme satırları (aşağıdaki SESLENDIRME)
    film-source/muzik/reel-muzik.mp3           müzik (aşağıdaki MUZIK_KOMUTU)

Kaynaklar:
  • Uydu görüntüsü: Sentinel-2 cloudless 2016, EOX IT Services GmbH — CC BY 4.0
    ("Contains modified Copernicus Sentinel data 2016"). Videoda künye yazılıdır.
    Konum: Google Maps'ten alınan proje koordinatı (src/data/location.ts).
  • Yakın yerlerin koordinatları OpenStreetMap'ten (Photon), süreler src/data/location.ts'ten.
  • Çekimler film-source/clips (projenin kendi render'larından), fotoğraf sosyal-medya/bitmis-fotograflar.

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
KLIP = lambda ad: os.path.join(ROOT, "film-source", "clips", ad + ".mp4")
SES_KLASOR = os.path.join(ROOT, "film-source", "ses", "yeni")
MUZIK = os.path.join(ROOT, "film-source", "muzik", "reel-muzik.mp3")
VEK = lambda ad: F("public", "brand", "vektor", ad)
W, H, FPS, SR = 1080, 1920, 24, 44100
KOYU, VURGU = yy.LACI
GECIS = 0.35
VO_GIRIS = 0.35

# ---------------------------------------------------------------- Higgsfield komutları
# Seslendirme: ElevenLabs (elevenlabs_v4), erkek, tok ve sakin sinema fragmanı anlatıcısı; her satır ayrı kayıt.
# Sayılar yazıyla, marka "Mia Park Oşın" okunacak biçimde yazılır.
SESLENDIRME = [
    "Kocaeli'de, İzmit Körfezi'nin kıyısında yeni bir hayat başlıyor.",
    "Sahile iki, şehir merkezine beş dakika. Her şey bir adım ötenizde.",
    "Mia Park Oşın.",
    "Bir artı sıfır daireler: altı yüz doksan dokuz bin lira peşinat, ayda yirmi dokuz bin dokuz yüz lira.",
    "Bir artı bir daireler: dokuz yüz doksan dokuz bin lira peşinat, ayda otuz dokuz bin dokuz yüz lira.",
    "İki artı bir daireler: iki milyon lira peşinat, ayda elli bin lira.",
    "Üstelik tam altmış ay sabit taksit.",
    "Banka yok. Faiz yok. Kefil yok. Ara ödeme yok.",
    "Mia Park Oşın. Hemen arayın: dört yüz kırk dört, on, elli sekiz.",
]
MUZIK_KOMUTU = ("Powerful cinematic trailer music for a premium real estate launch commercial. Starts with a deep sub boom and a rising "
                "whoosh, then driving modern percussion, punchy hybrid orchestral hits, bold brass and staccato strings, confident and "
                "uplifting, 112 bpm, big impact every four bars, strong build from 30 seconds and a final hit with a clean tail at the "
                "end. Instrumental, no vocals.")
# Çekim (seedance_2_0, 9:16): start_image = uydu karesi, end_image = projenin havadan görseli.
CEKIM_KOMUTU = ("Cinematic continuous drone descent in one take: the camera dives from high altitude straight down over the bay and the "
                "city, pushes through thin clouds, tilts forward and glides toward the modern residential complex with pools in the "
                "courtyard, golden hour light, photorealistic, smooth stabilized motion, no text.")

# ---------------------------------------------------------------- zaman çizelgesi
# (sahne, en az süre, seslendirme no, seslendirmeden sonraki pay)
SAHNE = [("uydu", 6.0, 1, 1.1), ("yakin", 5.6, 2, .9), ("giris", 2.6, 3, .9), ("d10", 6.2, 4, .6), ("d11", 6.2, 5, .6),
         ("d21", 5.0, 6, .6), ("balkon", 3.2, 7, .5), ("avlu", 4.6, 8, .6), ("kapanis", 6.0, 9, 1.8)]


def vo_yol(i):
    return os.path.join(SES_KLASOR, f"vo-{i}.wav")


def vo_sure(i):
    if not os.path.exists(vo_yol(i)):
        return 0.0
    with wave.open(vo_yol(i)) as w:
        return w.getnframes() / w.getframerate()


SESLI = all(os.path.exists(vo_yol(i)) for i in range(1, len(SESLENDIRME) + 1))
SURE, T = {}, {}
_t = 0.0
for _ad, _en_az, _vo, _pay in SAHNE:
    SURE[_ad] = max(_en_az, round((VO_GIRIS + vo_sure(_vo) + _pay) * FPS) / FPS if SESLI else 0)
    T[_ad] = _t
    _t += SURE[_ad]
TOPLAM = _t

# ---------------------------------------------------------------- harita
LAT, LON = 40.736667, 29.944889          # proje (Google Maps koordinatı)
SX, SY = 500, 1080                        # projenin ekrandaki yeri
Z0, Z1 = 6.6, 12.9                        # yaklaşmanın başı ve sonu (harita yakınlığı)
T_ZOOM, T_DALIS, T_HARITA = SURE["uydu"] - .5, T["giris"] - .7, T["giris"]
LW, LH, LMIN, LMAX = 3584, 5120, 7, 14
UYDU = "https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless_3857/default/g/{z}/{y}/{x}.jpg"

# (ad, süre, enlem, boylam, etiketin tarafı)
YAKIN = [
    ("41 Burda AVM", "3 dk", 40.75675, 29.94756, "sol"),
    ("Symbol AVM", "7 dk", 40.75787, 29.97956, "sag"),
    ("Şehir Merkezi", "5 dk", 40.77211, 29.95056, "sol"),
    ("Şehir Hastanesi", "5 dk", 40.78309, 29.96064, "sag"),
    ("Kocaeli Üniversitesi", "10 dk", 40.81874, 29.92291, "sag"),
]
# Yaklaşırken görünen coğrafi adlar: (ad, enlem, boylam, göründüğü yakınlık aralığı, punto)
COGRAFYA = [
    ("KARADENİZ", 42.25, 30.6, 6.6, 8.6, 40),
    ("İSTANBUL", 41.02, 28.97, 6.9, 10.2, 34),
    ("MARMARA DENİZİ", 40.68, 28.2, 7.4, 9.9, 30),
    ("BURSA", 40.19, 29.06, 7.6, 10.0, 30),
    ("KOCAELİ", 40.93, 29.92, 8.6, 10.9, 44),
    ("SAPANCA GÖLÜ", 40.715, 30.26, 10.0, 12.2, 26),
    ("İZMİT KÖRFEZİ", 40.735, 29.74, 10.3, 12.3, 30),
    ("İZMİT", 40.775, 29.94, 10.6, 12.4, 38),
]


def mpx(lat, lon, z):
    n = 256 * 2 ** z
    return (lon + 180) / 360 * n, (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n


def olcek(t):
    """Yaklaşma bittikten sonraki büyüme (haritayla etiketler aynı fonksiyonu kullanır)."""
    if t <= T_ZOOM:
        return 1.0
    if t <= T_DALIS:
        return 1 + .06 * (t - T_ZOOM) / (T_DALIS - T_ZOOM)
    q = (t - T_DALIS) / (T_HARITA - T_DALIS)
    return 1.06 * (1 + 2.2 * q ** 3)


def kamera(t):
    """(harita yakınlığı, dönüş açısı). Yaklaşma yumuşak başlar, yumuşak konar."""
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
    """Yaklaşmanın başında içinden geçilen ince bulut tabakası (fraktal gürültü)."""
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
    p = (t - .05) / 2.6
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


def baslik(y, ust, ana, g, ana_boy=96, alt=None):
    """Sinema dili: ince üst satır, altın çizgi, büyük beyaz başlık."""
    alt_satir = (f'<div class="tek gir" style="--g:{g + .5};margin-top:22px;font-size:32px;font-weight:700;letter-spacing:.3em;color:#fff;{GOLGE}">{alt}</div>'
                 if alt else "")
    return f"""<div class="a" style="left:0;top:{y}px;width:{W}px;text-align:center">
      <div class="tek gir" style="--g:{g};font-size:32px;font-weight:700;letter-spacing:.42em;color:#fff;{GOLGE}">{ust}</div>
      <div class="cizgi" style="--g:{g + .15};width:150px;height:5px;margin:24px auto 22px;background:{VURGU}"></div>
      <div class="k gir" style="--g:{g + .25};font-size:{ana_boy}px;line-height:1.08;color:#fff;{GOLGE}">{ana}</div>{alt_satir}</div>"""


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
    g = (.3, .22 * sure, .56 * sure, .78 * sure)
    return (hap(x + 150, 1010, gen - 300, tip, 34, g[0], "#fff", KOYU)
            + f"""<div class="a pat" style="--g:{g[1]:.2f};left:{x}px;top:1098px;width:{gen}px;height:202px;border-radius:26px 26px 0 0;background:{KOYU};
                   text-align:center;color:#fff;box-shadow:0 18px 40px rgba(8,20,45,.4);display:flex;flex-direction:column;justify-content:center">
                <div class="k tek" style="font-size:{112 if len(pesin) < 8 else 96}px">{pesin}<span style="font-size:40px;letter-spacing:0;margin-left:10px">TL</span></div>
                <div class="tek" style="margin-top:8px;font-size:34px;font-weight:800;letter-spacing:.14em">PEŞİNAT</div></div>
              <div class="a pat" style="--g:{g[2]:.2f};left:{x}px;top:1300px;width:{gen}px;padding:24px 0 22px;border-radius:0 0 26px 26px;background:{VURGU};
                   text-align:center;color:{KOYU};box-shadow:0 18px 40px rgba(8,20,45,.4)">
                <div class="k tek" style="font-size:66px"><span style="font-size:34px;letter-spacing:.08em;margin-right:14px">AYDA</span>{ayda}<span style="font-size:32px;letter-spacing:0;margin-left:9px">TL</span></div></div>"""
            + hap(x + 90, 1434, gen - 180, "60 AY SABİT TAKSİT", 38, g[3]))


def cografya():
    """Yaklaşırken yer adları haritaya sabitlenmiş gibi akar: her kare için konum hesaplanır."""
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
        govde += (f'<div class="a tek" style="left:0;top:0;animation:cog{i} {T_ZOOM:.3f}s linear 0s both">'
                  f'<div style="transform:translate(-50%,-50%);font-size:{boy}px;font-weight:700;letter-spacing:.3em;color:#fff;{GOLGE}">{ad}</div></div>')
    return stil, govde


def yakin_yerler():
    """Harita üstü: proje iğnesi, gerçek konumlara çizgiler, dakika etiketleri."""
    sx, sy = mpx(LAT, LON, Z1)
    cizgi, nokta, etiket = "", "", ""
    for i, (ad, sure, lat, lon, taraf) in enumerate(YAKIN):
        px, py = mpx(lat, lon, Z1)
        x, y = SX + px - sx, SY + py - sy
        g = T["yakin"] + .8 + i * .5
        cizgi += (f'<line class="ciz" style="--g:{g:.2f}" x1="{SX}" y1="{SY}" x2="{x:.1f}" y2="{y:.1f}" pathLength="1" stroke="#fff" stroke-width="4" '
                  f'stroke-linecap="round" stroke-dasharray="1" stroke-dashoffset="1"/>')
        nokta += (f'<div class="a pat" style="--g:{g + .35:.2f};left:{x - 13:.1f}px;top:{y - 13:.1f}px;width:26px;height:26px;border-radius:50%;'
                  f'background:#fff;border:6px solid {KIRMIZI}"></div>')
        yer = f"right:{W - x + 26:.1f}px;transform-origin:100% 50%" if taraf == "sol" else f"left:{x + 26:.1f}px;transform-origin:0 50%"
        etiket += f"""<div class="a pat" style="--g:{g + .4:.2f};top:{y - 31:.1f}px;{yer};display:flex;border-radius:16px;overflow:hidden;box-shadow:0 12px 26px rgba(8,20,45,.45)">
            <span class="tek" style="background:#fff;color:{KOYU};font-size:30px;font-weight:800;padding:14px 18px 13px">{ad}</span>
            <span class="k tek" style="background:{VURGU};color:{KOYU};font-size:30px;padding:15px 16px 12px">{sure}</span></div>"""
    g0 = T_ZOOM - 1.0
    igne = f"""<svg class="a dus" style="--g:{g0:.2f};left:{SX - 44}px;top:{SY - 112}px;width:88px;height:114px" viewBox="0 0 88 114">
        <path d="M44 112C44 112 6 66 6 42a38 38 0 1 1 76 0c0 24-38 70-38 70z" fill="{KIRMIZI}" stroke="#fff" stroke-width="5"/><circle cx="44" cy="42" r="15" fill="#fff"/></svg>"""
    ad = hap(SX - 215, SY + 24, 430, "MİA PARK OCEAN", 38, g0 + .35, "#fff", KOYU)
    alt = hap(SX - 250, SY + 118, 500, "SAHİLE 2 DK · D-100'E 1 DK", 30, T["yakin"] + .5)
    adim = 0.05
    n = round((T_HARITA + .3 - T_ZOOM) / adim)
    kare = "".join(f"{100 * k / n:.3f}%{{transform:scale({olcek(T_ZOOM + k * adim):.5f})}}" for k in range(n + 1))
    stil = (f"@keyframes harita{{{kare}}}\n.harita{{position:absolute;left:0;top:0;width:{W}px;height:{H}px;transform-origin:{SX}px {SY}px;"
            f"animation:harita {n * adim:.3f}s linear {T_ZOOM:.3f}s both}}")
    govde = (f'<div class="harita"><svg class="a" style="left:0;top:0" width="{W}" height="{H}">{cizgi}</svg>{nokta}{etiket}{igne}{ad}{alt}</div>')
    return stil, govde


def html():
    harita_stil, harita = yakin_yerler()
    cog_stil, cog = cografya()
    r, g, b = (int(KOYU[j:j + 2], 16) for j in (1, 3, 5))
    adim = (max(vo_sure(8), 3.6) - .3) / 4
    yoklar = "".join(hap(70 + (i % 2) * 484, 1110 + (i // 2) * 150, 456, m, 46, VO_GIRIS + .1 + i * adim)
                     for i, m in enumerate(["BANKA YOK", "FAİZ YOK", "KEFİL YOK", "ARA ÖDEME YOK"]))
    kapanis = f"""
      <div class="a gir" style="--g:.05;left:0;top:0;width:{W}px;height:{H}px;background:linear-gradient(180deg,rgba({r},{g},{b},.72) 0,rgba({r},{g},{b},.12) 24%,
           rgba({r},{g},{b},.06) 44%,rgba({r},{g},{b},.9) 55%,{KOYU} 62%)"></div>
      <img class="a gir" src="{VEK('mia-beyaz.svg')}" style="--g:.3;left:{W // 2 - 190}px;top:300px;width:380px">
      <div class="a tek gir" style="--g:1.3;left:0;top:1056px;width:{W}px;text-align:center;font-size:32px;font-weight:700;letter-spacing:.42em;color:#fff">HEMEN ARAYIN</div>
      <div class="a cizgi" style="--g:1.4;left:{W // 2 - 75}px;top:1116px;width:150px;height:5px;background:{VURGU}"></div>
      <div class="a k tek pat" style="--g:1.6;left:0;top:1140px;width:{W}px;text-align:center;font-size:164px;color:#fff">444 10 58</div>
      <div class="a pat" style="--g:2.3;left:0;top:1342px;width:{W}px;display:flex;align-items:center;justify-content:center;gap:18px">{yy.WA.format(s=58)}
        <span class="k tek" style="font-size:56px;color:#fff">0540 028 00 41</span></div>
      <div class="a gir" style="--g:3.0;left:0;top:1462px;width:{W}px;display:flex;align-items:center;justify-content:center;gap:30px">
        <div class="tek" style="font-size:22px;font-weight:700;letter-spacing:.2em;color:rgba(255,255,255,.85);line-height:1.5;text-align:right">TEK YETKİLİ<br>SATIŞ</div>
        <img src="{VEK('ocean-beyaz.svg')}" style="height:78px"><span style="width:2px;height:70px;background:rgba(255,255,255,.5)"></span>
        <img src="{VEK('tilda-beyaz.svg')}" style="height:46px"></div>"""
    sahneler = (
        blok(0, T_ZOOM, cog)
        + blok(.2, T_ZOOM - 1.9, baslik(330, "KOCAELİ · İZMİT", "YENİ BİR HAYAT<br>BAŞLIYOR", .2, 92))
        + blok(0, T_HARITA - .1, harita)
        + blok(T["yakin"] + .1, SURE["yakin"] - .2, ikili(1340, "HER YERE YAKIN", "İZMİT MİA BÖLGESİ", .1, 72, 46))
        + blok(T_HARITA - .12, .95, f'<div class="a" style="left:0;top:0;width:{W}px;height:{H}px;background:#fff"></div>', "flas")
        + blok(T["giris"] + .15, SURE["giris"] - .15, baslik(1130, "İZMİT MİA BÖLGESİ", "MİA PARK OCEAN", .2, 88))
        + blok(T["d10"], SURE["d10"], fiyat_karti("1+0 DAİRELER", "699.000", "29.900", SURE["d10"]))
        + blok(T["d11"], SURE["d11"], fiyat_karti("1+1 DAİRELER", "999.000", "39.900", SURE["d11"]))
        + blok(T["d21"], SURE["d21"], fiyat_karti("2+1 DAİRELER", "2.000.000", "50.000", SURE["d21"]))
        + blok(T["balkon"], SURE["balkon"], ikili(1130, "ÜSTELİK TAM", "60 AY SABİT TAKSİT", .3, 76, 70))
        + blok(T["avlu"], SURE["avlu"], ikili(320, "MİA PARK OCEAN'DA", "BANKASIZ EV SAHİBİ OLUN", .2, 70, 46) + yoklar)
        + blok(T["kapanis"], SURE["kapanis"], kapanis, "sahne son")
    )
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{yy.css(H)}
body {{ background:transparent; }}
.sahne, .flas {{ position:absolute; left:0; top:0; width:{W}px; height:{H}px; animation:sahne calc(var(--d)*1s) linear calc(var(--s)*1s) both; }}
.sahne.son {{ animation-name:sahne-son; }}
.flas {{ animation-name:flas; }}
@keyframes sahne {{ 0%{{opacity:0}} .1%{{opacity:1}} 93%{{opacity:1}} 100%{{opacity:0}} }}
@keyframes sahne-son {{ 0%{{opacity:0}} .1%{{opacity:1}} 100%{{opacity:1}} }}
@keyframes flas {{ 0%{{opacity:0}} 22%{{opacity:.92}} 100%{{opacity:0}} }}
.gir {{ animation:gir .6s cubic-bezier(.2,.9,.25,1) calc((var(--s) + var(--g))*1s) both; }}
.pat {{ animation:pat .55s cubic-bezier(.2,.9,.25,1) calc((var(--s) + var(--g))*1s) both; }}
.dus {{ animation:dus .6s cubic-bezier(.3,1.4,.5,1) calc((var(--s) + var(--g))*1s) both; }}
.ciz {{ animation:ciz .45s ease-out calc((var(--s) + var(--g))*1s) both; }}
.cizgi {{ animation:cizgi .5s cubic-bezier(.2,.9,.25,1) calc((var(--s) + var(--g))*1s) both; }}
@keyframes gir {{ from{{opacity:0;transform:translateY(46px)}} to{{opacity:1;transform:none}} }}
@keyframes pat {{ 0%{{opacity:0;transform:scale(.55)}} 60%{{opacity:1;transform:scale(1.07)}} 100%{{opacity:1;transform:scale(1)}} }}
@keyframes dus {{ from{{opacity:0;transform:translateY(-260px)}} to{{opacity:1;transform:none}} }}
@keyframes ciz {{ from{{stroke-dashoffset:1}} to{{stroke-dashoffset:0}} }}
@keyframes cizgi {{ from{{opacity:0;transform:scaleX(0)}} to{{opacity:1;transform:none}} }}
{harita_stil}
{cog_stil}
</style></head><body>
  {blok(0, T_HARITA, f'''<div class="a" style="left:0;top:0;width:{W}px;height:{H}px;background:radial-gradient(ellipse 75% 62% at 50% 54%,rgba(4,12,30,0) 55%,rgba(4,12,30,.5) 100%)"></div>
    <div class="a tek" style="left:0;top:1590px;width:{W}px;text-align:center;font-size:19px;font-weight:600;letter-spacing:.04em;
    color:rgba(255,255,255,.82)">Uydu görüntüsü: Copernicus Sentinel-2 (2016) · EOX, CC BY 4.0</div>''')}
  {blok(0, T["kapanis"] + .1, f'''<div class="a" style="left:0;top:0;width:{W}px;height:420px;background:linear-gradient(180deg,rgba({r},{g},{b},.62),rgba({r},{g},{b},0))"></div>
    <img class="a" src="{VEK('mia-beyaz.svg')}" style="left:{W // 2 - 84}px;top:150px;width:168px">''')}
  {sahneler}
</body></html>"""


# ---------------------------------------------------------------- zemin görüntüsü
# (sahne, tür, kaynak, kaynakta başlangıç sn, kaydırma başı, kaydırma sonu) — klip sahneye sığmazsa yavaşlatılır
FOTO = os.path.join(ROOT, "sosyal-medya", "bitmis-fotograflar", "15-balkondan-gunesli.jpg")
ZEMIN = [
    ("uydu", "harita", None, 0, 0, 0),
    ("giris", "klip", "13-giris-drone", 0.4, .50, .50),
    ("d10", "klip", "09-daire-1plus0", 0.0, .34, .60),
    ("d11", "klip", "10-daire-1plus1", 0.0, .28, .60),
    ("d21", "klip", "11-bahce-loft", 0.0, .30, .46),
    ("balkon", "foto", FOTO, 0, 0, 0),
    ("avlu", "klip", "04-avlu-suzulme", 1.4, .55, .86),
    ("kapanis", "klip", "01-gunduz-gece", 0.6, .50, .50),
]
KLIP_SURE = 8.0


def zemin(gecici):
    harita = os.path.join(gecici, "harita.mp4")
    harita_videosu(harita, T_HARITA + GECIS)
    girdi, f, bas_list = [], [], []
    for i, (ad, tur, kaynak, kbas, p0, p1) in enumerate(ZEMIN):
        bas = T[ad]
        son = T[ZEMIN[i + 1][0]] if i + 1 < len(ZEMIN) else TOPLAM
        sure = son - bas + (GECIS / 2 if i else 0) + (GECIS / 2 if i + 1 < len(ZEMIN) else 0)
        bas_list.append(bas)
        son_ek = f"trim=duration={sure:.3f},setpts=PTS-STARTPTS,fps={FPS},settb=1/{FPS},setsar=1,format=yuv420p[v{i}]"
        if tur == "harita":
            girdi += ["-i", harita]
            f.append(f"[{i}:v]{son_ek}")
        elif tur == "foto":
            n = round(sure * FPS)
            girdi += ["-loop", "1", "-framerate", str(FPS), "-t", f"{sure:.3f}", "-i", kaynak]
            f.append(f"[{i}:v]scale=2160:-2:flags=lanczos,crop=2160:3840:0:'(ih-3840)*.5',"
                     f"zoompan=z='1+.09*on/{n}':x='iw/2-(iw/zoom/2)':y='ih*.56-(ih/zoom)*.56':d=1:s={W}x{H}:fps={FPS},{son_ek}")
        else:
            yavas = max(1.0, (sure + .1) / (KLIP_SURE - kbas))
            girdi += ["-ss", f"{kbas:.3f}", "-i", KLIP(kaynak)]
            f.append(f"[{i}:v]setpts={yavas:.4f}*PTS,fps={FPS},scale=-2:{H}:flags=lanczos,"
                     f"crop={W}:{H}:'(iw-{W})*({p0}+({p1 - p0:.3f})*t/{sure:.3f})':0,unsharp=5:5:.55,eq=brightness=.02:saturation=1.08,{son_ek}")
    onceki = "v0"
    for i in range(1, len(ZEMIN)):
        f.append(f"[{onceki}][v{i}]xfade=transition=fade:duration={GECIS}:offset={bas_list[i] - GECIS / 2:.3f}[x{i}]")
        onceki = f"x{i}"
    return girdi, f, onceki


# ---------------------------------------------------------------- ses
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
    if SESLI:
        for ad, _, vo, _ in SAHNE:
            a = ses_oku(vo_yol(vo))
            a *= 0.9 / np.abs(a).max()
            j = int((T[ad] + VO_GIRIS) * SR)
            konusma[j:j + len(a)] += a[:n - j]
    m = np.zeros((n, 2), np.float32)
    if os.path.exists(MUZIK):
        ham = ses_oku(MUZIK)[:n]
        m[:len(ham)] = ham
        m *= 0.5 / np.sqrt((m ** 2).mean() + 1e-9) * (0.24 if SESLI else 0.5)
        zarf = np.clip(kayan(np.abs(konusma).max(axis=1), int(.25 * SR)) / 0.12, 0, 1)
        m *= (1.0 - 0.6 * kayan(zarf, int(.3 * SR)))[:, None]     # seslendirme varken müzik kısılır
        a, z = int(.15 * SR), int(2.4 * SR)
        m[:a] *= np.linspace(0, 1, a, dtype=np.float32)[:, None]
        m[-z:] *= (np.linspace(1, 0, z, dtype=np.float32) ** 1.4)[:, None]
    efekt = np.zeros((n, 2), np.float32)
    for bas, v, kazanc in [(0.0, vinlama(T_ZOOM + .5, T_ZOOM - .4, .35), .10), (T_DALIS - .3, vinlama(1.6, .95, .22, 400, 5000), .22)]:
        j = int(bas * SR)
        efekt[j:j + len(v)] += v * kazanc
    miks = np.tanh((konusma + m + efekt) * 1.1) * 0.9
    with wave.open(yol, "wb") as f:
        f.setnchannels(2), f.setsampwidth(2), f.setframerate(SR)
        f.writeframes((miks * 32767).astype(np.int16).tobytes())


# ---------------------------------------------------------------- üretim
def main():
    os.makedirs(OUT, exist_ok=True)
    print(f"  {'seslendirmeli' if SESLI else 'SESSİZ TASLAK (seslendirme dosyaları yok)'} · {TOPLAM:.1f} sn · "
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
    yol = os.path.join(OUT, "mia-reel-uydudan-eve.mp4" if SESLI else "mia-reel-uydudan-eve-sessiz-taslak.mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", *girdi, "-framerate", str(FPS), "-i", os.path.join(kare, "k-%04d.png"), "-i", wav,
                    "-filter_complex", ";".join(f), "-map", "[v]", "-map", f"{k + 1}:a", "-t", f"{TOPLAM}",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "21", "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", str(FPS),
                    "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k", yol], check=True)
    print(f"  → {os.path.relpath(yol, ROOT)} · {os.path.getsize(yol) / 1048576:.1f} MB")
    shutil.rmtree(gecici, ignore_errors=True)


if __name__ == "__main__":
    main()
