#!/usr/bin/env python3
"""
Instagram Reels — 699.000 TL kampanyası (1080x1920, 24 sn, 24 fps, müzikli).

Onaylı "Yeni Bir Yuva" reklam düzeninin hareketli hâli: beyaz üstte üç satır başlık,
ortada proje çekimi (film-source/clips), üstünde koyu/altın kart ve kırmızı etiketler,
altta Tilda + MİA logoları ve telefonlar. Yazılar HTML/CSS animasyonuyla saydam kare
dizisi olarak çizilir (scripts/reel-kare.cjs), ffmpeg çekimlerin üstüne bindirir.

Önemli her şey 4:5 akış kırpımının (y 285–1635) içinde kalır; Reels arayüzünün
kapattığı alt bölüm düz koyu renktir.

Sahneler (müziğin vuruşlarına oturur, vuruş = 0,6 sn):
    0,0   Kira Öder Gibi EV SAHİBİ OLUN
    3,6   Ayda 29.900 TL ile NE ALABİLİRSİNİZ?      → fiyat kartı
    7,8   Banka Yok, Faiz Yok · 60 AY SABİT TAKSİT  → dört kırmızı etiket
    12,0  ÖDEME PLANI                               → 1+0 / 1+1 / 2+1 tablosu
    18,0  Hemen Arayın 444 10 58                    → WhatsApp kartı

    python3 scripts/build-reel-699.py            # tam üretim
    python3 scripts/build-reel-699.py --onizle   # yalnızca sahne başına bir kare
"""

import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import wave

import numpy as np

KOK = os.path.dirname(os.path.abspath(__file__))


def _yukle(ad, dosya):
    spec = importlib.util.spec_from_file_location(ad, os.path.join(KOK, dosya))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


yy = _yukle("yy", "build-reklam-yeni-yuzler.py")
skor = _yukle("film_score", "film_score.py")

ROOT, F, KIRMIZI = yy.ROOT, yy.F, yy.KIRMIZI
OUT = os.path.join(ROOT, "sosyal-medya", "instagram-reel")
KLIP = lambda ad: os.path.join(ROOT, "film-source", "clips", ad + ".mp4")
W, H, FPS = 1080, 1920, 24
KOYU, VURGU = yy.LACI
MIA_LACI = F("public", "brand", "vektor", "mia-lacivert.svg")

G_TOP, G_H = 520, 1040          # çekimin durduğu şerit
GECIS = 0.4                     # çekimler arası çapraz geçiş
MUZIK_BAS = 24.0                # film müziğinin tam ritimli bölümünden kesit

# (başlangıç sn, klip, klipte başlangıç sn, kaydırma başı, kaydırma sonu)
SAHNELER = [
    (0.0, "13-giris-drone", 0.3, .46, .54),
    (3.6, "04-avlu-suzulme", 3.2, .52, .78),
    (7.8, "03-havadan-yorunge", 0.4, .42, .58),
    (12.0, "10-daire-1plus1", 0.3, .30, .62),
    (18.0, "02-sokak-drone", 1.0, .52, .40),
]
TOPLAM = 24.0


# ---------------------------------------------------------------- HTML
def baslik(b1, b2, b3, olcek=1.0):
    s1, s2, s3, et = 74, 124, 74, 28
    return f"""
  <div class="a" style="left:0;top:300px;width:{W}px;text-align:center">
    <div class="k tek gir" style="--g:.05;font-size:{s1}px;color:{KOYU}">{b1}</div>
    <div class="k tek pat" style="--g:.22;margin-top:{round(s2 * .14)}px;font-size:{round(s2 * olcek)}px;color:{VURGU}">{b2}</div>
    <div class="k tek gir" style="--g:.42;margin-top:{round(s2 * .1)}px;font-size:{s3}px;color:{KOYU}">{b3}</div>
    <div class="tek gir" style="--g:.55;margin-top:{round(et * .9)}px;font-size:{et}px;font-weight:600;letter-spacing:.2em;color:#4a5878">MİA PARK OCEAN · İZMİT</div>
  </div>"""


def hap(x, y, gen, metin, boy, g, renk=KIRMIZI, yazi="#fff", sinif="pat"):
    golge = "rgba(225,38,47,.35)" if renk == KIRMIZI else "rgba(10,30,50,.28)"
    return (f'<div class="a tek {sinif}" style="--g:{g};left:{x}px;top:{y}px;width:{gen}px;padding:{round(boy * .62)}px 0;'
            f'border-radius:{round(boy * .72)}px;background:{renk};color:{yazi};text-align:center;font-size:{boy}px;font-weight:800;'
            f'letter-spacing:.02em;box-shadow:0 14px 30px {golge}">{metin}</div>')


def tablo():
    satir = ""
    for i, (tip, pesin, ayda) in enumerate([("1+0", "699.000", "29.900"), ("1+1", "999.000", "39.900"), ("2+1", "2.000.000", "50.000")]):
        satir += f"""
    <div class="a soldan" style="--g:{.7 + i * .55};left:54px;top:{720 + i * 162}px;width:{W - 108}px;height:140px;display:flex;border-radius:24px;overflow:hidden;
         box-shadow:0 18px 36px rgba(10,30,50,.34)">
      <div class="k" style="width:212px;background:{KOYU};color:{VURGU};font-size:76px;display:flex;align-items:center;justify-content:center">{tip}</div>
      <div style="flex:1;background:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center">
        <div class="k tek" style="font-size:56px;color:{KOYU}">{pesin}<span style="font-size:26px;letter-spacing:0;margin-left:7px">TL</span></div>
        <div class="tek" style="margin-top:8px;font-size:21px;font-weight:800;letter-spacing:.2em;color:#4a5878">PEŞİNAT</div></div>
      <div style="width:344px;background:{VURGU};display:flex;flex-direction:column;align-items:center;justify-content:center">
        <div class="tek" style="font-size:21px;font-weight:800;letter-spacing:.2em;color:{KOYU}">AYDA</div>
        <div class="k tek" style="margin-top:6px;font-size:56px;color:{KOYU}">{ayda}<span style="font-size:26px;letter-spacing:0;margin-left:7px">TL</span></div></div>
    </div>"""
    return satir


def html():
    r, g, b = (int(KOYU[j:j + 2], 16) for j in (1, 3, 5))
    kart_m = dict(renk=yy.LACI, ust=("AYDA", "29.900", "TL'DEN", "BAŞLAYAN TAKSİT"), serit="60 AY SABİT TAKSİT",
                  hap="ARA ÖDEME YOK<br>FAİZ YOK", alt=None)
    etiketler = "".join(hap(70 + (i % 2) * 484, 730 + (i // 2) * 150, 456, m, 46, .7 + i * .32)
                        for i, m in enumerate(["BANKA YOK", "FAİZ YOK", "KEFİL YOK", "ARA ÖDEME YOK"]))
    icerik = [
        baslik("Kira Öder Gibi", "EV SAHİBİ OLUN", "MİA PARK OCEAN'da", .9)
        + hap(150, 1050, 780, "BANKA YOK · FAİZ YOK · KEFİL YOK", 36, 1.3),
        baslik("Ayda 29.900 TL ile", "NE ALABİLİRSİNİZ?", "MİA PARK OCEAN'da Ev!", .78)
        + f'<div class="a pat" style="--g:.75;left:0;top:0;width:{W}px;height:{H}px;transform-origin:540px 960px">{yy.kart(230, 716, 620, 84, kart_m)}</div>',
        baslik("Banka Yok, Faiz Yok", "60 AY SABİT TAKSİT", "Ara Ödeme Yok", .74) + etiketler
        + hap(170, 1056, 740, "ARA ZAM YOK · TAKSİT HEP AYNI", 31, 2.1, "#fff", KOYU),
        baslik("60 Ay Vade Farksız", "ÖDEME PLANI", "Size Uygun Daireyi Seçin") + tablo(),
        baslik("Hemen Arayın", "444 10 58", "Yeni Eviniz Sizi Bekliyor")
        + f"""<div class="a pat" style="--g:.8;left:130px;top:740px;width:820px;padding:34px 0 30px;border-radius:34px;background:#fff;text-align:center;
               box-shadow:0 20px 44px rgba(10,30,50,.34)">
            <div style="display:flex;align-items:center;justify-content:center;gap:20px">{yy.WA.format(s=74)}
              <span class="k tek" style="font-size:70px;color:{KOYU}">0540 028 00 41</span></div>
            <div class="tek" style="margin-top:14px;font-size:25px;font-weight:800;letter-spacing:.2em;color:#4a5878">WHATSAPP'TAN YAZIN</div></div>"""
        + hap(240, 960, 600, "HEMEN BİLGİ ALIN", 40, 1.4)
        + hap(300, 1084, 480, "miaparkocean.com", 30, 1.8, KOYU, "#fff"),
    ]
    sahne = ""
    for i, (bas, *_) in enumerate(SAHNELER):
        son = SAHNELER[i + 1][0] if i + 1 < len(SAHNELER) else TOPLAM
        sinif = "sahne" if i + 1 < len(SAHNELER) else "sahne son"
        sahne += f'<div class="{sinif}" style="--s:{bas};--d:{son - bas}">{icerik[i]}</div>'
    logo, tel, wa, y = 60, 80, 29, 1350
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{yy.css(H)}
body {{ background:transparent; }}
.sahne {{ position:absolute; left:0; top:0; width:{W}px; height:{H}px; animation:sahne calc(var(--d)*1s) linear calc(var(--s)*1s) both; }}
.sahne.son {{ animation-name:sahne-son; }}
@keyframes sahne {{ 0%{{opacity:0}} .1%{{opacity:1}} 93%{{opacity:1}} 100%{{opacity:0}} }}
@keyframes sahne-son {{ 0%{{opacity:0}} .1%{{opacity:1}} 100%{{opacity:1}} }}
.gir {{ animation:gir .5s cubic-bezier(.2,.9,.25,1) calc((var(--s) + var(--g))*1s) both; }}
.pat {{ animation:pat .55s cubic-bezier(.2,.9,.25,1) calc((var(--s) + var(--g))*1s) both; }}
.soldan {{ animation:soldan .55s cubic-bezier(.2,.9,.25,1) calc((var(--s) + var(--g))*1s) both; }}
@keyframes gir {{ from{{opacity:0;transform:translateY(46px)}} to{{opacity:1;transform:none}} }}
@keyframes pat {{ 0%{{opacity:0;transform:scale(.55)}} 60%{{opacity:1;transform:scale(1.07)}} 100%{{opacity:1;transform:scale(1)}} }}
@keyframes soldan {{ from{{opacity:0;transform:translateX(-160px)}} to{{opacity:1;transform:none}} }}
</style></head><body>
  <div class="a" style="left:0;top:0;width:{W}px;height:940px;background:linear-gradient(180deg,#fff 68%,rgba(255,255,255,0))"></div>
  <img class="a" src="{MIA_LACI}" style="left:{W // 2 - 80}px;top:118px;width:160px;height:150px;object-fit:contain">
  <div class="a" style="left:0;top:1190px;width:{W}px;height:{H - 1190}px;
       background:linear-gradient(180deg,rgba({r},{g},{b},0) 0,rgba({r},{g},{b},.92) 110px,{KOYU} 180px)"></div>
  <div class="a" style="left:0;top:{y}px;width:{W}px;display:flex;align-items:center;justify-content:center;gap:{round(logo * .5)}px">
    <img src="{yy.TILDA}" style="height:{logo}px"><span style="width:2px;height:{round(logo * 1.3)}px;background:rgba(255,255,255,.55)"></span>
    <img src="{yy.MIA}" style="height:{round(logo * 1.45)}px"></div>
  <div class="a k tek" style="left:0;top:{y + round(logo * 1.75)}px;width:{W}px;text-align:center;font-size:{tel}px;color:#fff;letter-spacing:.01em">444 10 58</div>
  <div class="a" style="left:0;top:{y + round(logo * 1.75) + round(tel * 1.18)}px;width:{W}px;display:flex;align-items:center;justify-content:center;gap:{round(wa * .4)}px;color:#fff">
    {yy.WA.format(s=round(wa * 1.1))}<span class="tek" style="font-size:{wa}px;font-weight:700;letter-spacing:.04em">0540 028 00 41</span>
    <span style="width:1px;height:{wa}px;background:rgba(255,255,255,.5);margin:0 {round(wa * .3)}px"></span>
    <span class="tek" style="font-size:{round(wa * .9)}px;font-weight:600;letter-spacing:.06em;opacity:.9">miaparkocean.com</span></div>
  {sahne}
</body></html>"""


# ---------------------------------------------------------------- ses ve görüntü
def muzik(yol):
    st = skor.build(MUZIK_BAS + TOPLAM + 0.5)[int(MUZIK_BAS * skor.SR):int((MUZIK_BAS + TOPLAM) * skor.SR)].copy()
    a, z = int(skor.SR * 0.04), int(skor.SR * 1.6)
    st[:a] *= np.linspace(0, 1, a, dtype=np.float32)[:, None]
    st[-z:] *= np.linspace(1, 0, z, dtype=np.float32)[:, None] ** 1.5
    with wave.open(yol, "wb") as f:
        f.setnchannels(2), f.setsampwidth(2), f.setframerate(skor.SR)
        f.writeframes((st * 0.8 * 32767).astype(np.int16).tobytes())


def zemin_filtresi():
    """Çekimleri şeride sığdırır, yatay kaydırır, çapraz geçişle birleştirir, beyaz tuvale oturtur."""
    girdi, f = [], []
    for i, (bas, klip, kbas, p0, p1) in enumerate(SAHNELER):
        son = SAHNELER[i + 1][0] if i + 1 < len(SAHNELER) else TOPLAM
        a = bas - (GECIS / 2 if i else 0)
        z = son + (GECIS / 2 if i + 1 < len(SAHNELER) else 0)
        sure = z - a
        girdi += ["-ss", f"{kbas:.3f}", "-t", f"{sure:.3f}", "-i", KLIP(klip)]
        f.append(f"[{i}:v]fps={FPS},scale=-2:{G_H}:flags=lanczos,crop={W}:{G_H}:'(iw-{W})*({p0}+({p1 - p0})*t/{sure:.3f})':0,"
                 f"eq=brightness=.02:saturation=1.08,setsar=1,format=yuv420p[v{i}]")
    onceki = "v0"
    for i in range(1, len(SAHNELER)):
        f.append(f"[{onceki}][v{i}]xfade=transition=fade:duration={GECIS}:offset={SAHNELER[i][0] - GECIS / 2:.3f}[x{i}]")
        onceki = f"x{i}"
    f.append(f"[{onceki}]pad={W}:{H}:0:{G_TOP}:white[zemin]")
    return girdi, f


def main():
    os.makedirs(OUT, exist_ok=True)
    gecici = tempfile.mkdtemp(prefix="reel699-")
    hp = os.path.join(gecici, "sayfa.html")
    open(hp, "w", encoding="utf-8").write(html())
    kare = os.path.join(gecici, "kare")
    os.makedirs(kare)
    n = round(TOPLAM * FPS)
    npm = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    subprocess.run(["node", os.path.join(KOK, "reel-kare.cjs"), hp, kare, str(n), str(FPS), str(W), str(H)],
                   check=True, env={**os.environ, "NODE_PATH": npm})
    wav = os.path.join(gecici, "muzik.wav")
    muzik(wav)
    girdi, f = zemin_filtresi()
    k = len(SAHNELER)
    f.append(f"[zemin][{k}:v]overlay=0:0:format=auto,format=yuv420p[v]")
    yol = os.path.join(OUT, "mia-reel-699-kira-oder-gibi.mp4")
    cmd = ["ffmpeg", "-y", "-v", "error", *girdi, "-framerate", str(FPS), "-i", os.path.join(kare, "k-%04d.png"), "-i", wav,
           "-filter_complex", ";".join(f), "-map", "[v]", "-map", f"{k + 1}:a", "-t", f"{TOPLAM}",
           "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", str(FPS),
           "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k", yol]
    if "--onizle" in sys.argv:
        for i, (bas, *_) in enumerate(SAHNELER):
            son = SAHNELER[i + 1][0] if i + 1 < len(SAHNELER) else TOPLAM
            t = son - 0.6
            subprocess.run(["ffmpeg", "-y", "-v", "error", *girdi, "-framerate", str(FPS), "-i", os.path.join(kare, "k-%04d.png"),
                            "-filter_complex", ";".join(f), "-map", "[v]", "-ss", f"{t}", "-frames:v", "1",
                            os.path.join(OUT, f"onizleme-sahne-{i + 1}.jpg")], check=True)
        return
    subprocess.run(cmd, check=True)
    print(f"  → {os.path.relpath(yol, ROOT)} · {os.path.getsize(yol) / 1048576:.1f} MB")
    shutil.rmtree(gecici, ignore_errors=True)


if __name__ == "__main__":
    main()
