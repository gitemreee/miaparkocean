#!/usr/bin/env python3
"""
Instagram reel (1080x1920): "Bir proje önce hayal edilir" — arsa → inşaat → bitmiş proje → yaşam → teklif.

Girdi: Higgsfield (Kling 3.0) ile üretilmiş 6 dikey klip (sosyal-medya/reel-hikaye/klip/*.mp4) + bu betiğin
çizdiği kapanış kartı. Çıktı: sosyal-medya/reel-hikaye/mia-reel-hikaye.mp4 (sessiz; müzik Instagram'da eklenir)
ve her klibin altyazılı tekil hali.

    python3.13 scripts/build-reel-hikaye.py
"""

import json
import os
import subprocess
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "sosyal-medya", "reel-hikaye")
KLIP = os.path.join(OUT, "klip")
FONT = os.path.join(ROOT, "brand-source", "fonts", "Montserrat-var.ttf")
FONT_K = os.path.join(ROOT, "sunum", "yazitipi", "Montserrat-Black.ttf")
FONT_O = os.path.join(ROOT, "sunum", "yazitipi", "Montserrat-Medium.ttf")
W, H, FPS = 1080, 1920, 30
XF = 0.6          # geçiş süresi (sn)
LAC, ALTIN = "#0f2a5a", "#c9a24a"

# (dosya, üst satır, alt satır, sahne süresi)
SAHNELER = [
    ("0-arsa.mp4",   "BİR PROJE",            "önce hayal edilir.",            4.8),
    ("1-insaat.mp4", "SONRA",                "kat kat yükselir.",             4.8),
    ("2-giris.mp4",  "MİA PARK OCEAN",       "İzmit'in yeni yaşam alanı",     4.8),
    ("4-havuz.mp4",  "60 AY VADE",           "vade farksız",                  4.8),
    ("5-aile.mp4",   "BANKA YOK · KREDİ YOK", "faiz yok, ara ödeme yok",       4.8),
    ("3-gece.mp4",   "699.000 TL PEŞİNAT",   "ayda sadece 29.900 TL",         4.8),
]


_TMP = tempfile.mkdtemp(prefix="reeltxt-")


def _tf(s, ad):
    """Metni dosyaya yaz (drawtext kaçış sorunlarından kaçınmak için textfile= kullanılır)."""
    p = os.path.join(_TMP, ad + ".txt")
    open(p, "w", encoding="utf-8").write(s)
    return p


def altyazi(ust, alt, i):
    """Alt üçte birlik alanda iki satırlık yazı: üst satır kalın, alt satır ince."""
    return (
        f"drawtext=fontfile={FONT_K}:textfile={_tf(ust, f'{i}u')}:fontsize=78:fontcolor=white:"
        f"shadowcolor=black@0.55:shadowx=0:shadowy=6:x=(w-text_w)/2:y=h-470:"
        f"alpha='if(lt(t,0.4),t/0.4,1)',"
        f"drawtext=fontfile={FONT_O}:textfile={_tf(alt, f'{i}a')}:fontsize=54:fontcolor=white@0.97:"
        f"shadowcolor=black@0.55:shadowx=0:shadowy=5:x=(w-text_w)/2:y=h-380:"
        f"alpha='if(lt(t,0.7),max(0,(t-0.3)/0.4),1)'"
    )


def kapanis_karti(yol):
    """Kapanış kartı PNG'si (Chromium): logolar, teklif, telefon."""
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:M;src:url(file://{FONT});}}
body{{margin:0;width:{W}px;height:{H}px;font-family:M,sans-serif;color:#fff;position:relative;overflow:hidden;
 background:radial-gradient(120% 80% at 50% 0%,#1b4a8a 0%,{LAC} 55%,#08182f 100%);}}
.a{{position:absolute;left:0;width:{W}px;text-align:center}}
.cizgi{{position:absolute;left:290px;width:500px;height:3px;background:{ALTIN}}}
</style></head><body>
 <img src="file://{ROOT}/public/brand/vektor/tilda-beyaz.svg" style="position:absolute;left:390px;top:230px;width:300px">
 <img src="file://{ROOT}/public/brand/logo-mia-2026.png" style="position:absolute;left:240px;top:430px;width:600px;filter:brightness(0) invert(1)">
 <div class="cizgi" style="top:900px"></div>
 <div class="a" style="top:960px;font-size:44px;font-weight:600;letter-spacing:.18em;color:{ALTIN}">PEŞİNAT</div>
 <div class="a" style="top:1020px;font-size:130px;font-weight:800;letter-spacing:-.02em">699.000 TL</div>
 <div class="a" style="top:1190px;font-size:52px;font-weight:600">AYDA SADECE <b style="color:{ALTIN}">29.900 TL</b></div>
 <div class="a" style="top:1290px;font-size:34px;font-weight:600;letter-spacing:.06em;opacity:.9;white-space:nowrap">60 AY VADE FARKSIZ · BANKA YOK · KREDİ YOK</div>
 <div class="cizgi" style="top:1400px"></div>
 <div class="a" style="top:1470px;font-size:96px;font-weight:800;letter-spacing:.04em">444 10 58</div>
 <div class="a" style="top:1600px;font-size:46px;font-weight:600;letter-spacing:.08em;color:{ALTIN}">miaparkocean.com</div>
 <img src="file://{ROOT}/public/brand/vektor/ocean-beyaz.svg" style="position:absolute;left:440px;top:1720px;width:200px;opacity:.9">
</body></html>"""
    gecici = tempfile.mkdtemp(prefix="reelkart-")
    hp = os.path.join(gecici, "k.html")
    open(hp, "w", encoding="utf-8").write(html)
    js = os.path.join(gecici, "k.cjs")
    open(js, "w").write(f"""
const {{chromium}} = require('playwright');
(async () => {{ const b = await chromium.launch(); const p = await b.newPage({{viewport:{{width:{W},height:{H}}}}});
  await p.goto('file://{hp}'); await p.waitForTimeout(400);
  await p.screenshot({{path:{json.dumps(yol)}}}); await b.close(); }})();""")
    npm = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    subprocess.run(["node", js], check=True, env={**os.environ, "NODE_PATH": npm})


def main():
    os.makedirs(OUT, exist_ok=True)
    kart = os.path.join(OUT, "kapanis-karti.png")
    kapanis_karti(kart)
    tekil = os.path.join(OUT, "tekil")
    os.makedirs(tekil, exist_ok=True)

    # 1) her klibi 1080x1920/30fps'e normalize et + altyazı
    parcalar = []
    for i, (dosya, ust, alt, sure) in enumerate(SAHNELER):
        src = os.path.join(KLIP, dosya)
        dst = os.path.join(tekil, f"{i + 1}-{dosya}")
        vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},"
              f"drawbox=x=0:y=ih-640:w=iw:h=640:color=black@0.40:t=fill," + altyazi(ust, alt, i))
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-t", str(sure), "-vf", vf, "-an",
                        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", dst], check=True)
        parcalar.append((dst, sure))
    # kapanış kartı 4 sn
    kart_mp4 = os.path.join(tekil, "7-kapanis.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", kart, "-t", "4", "-vf",
                    f"scale={W}:{H},zoompan=z='1+0.0008*in':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS},fps={FPS}",
                    "-r", str(FPS), "-video_track_timescale", "15360",
                    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", kart_mp4], check=True)
    parcalar.append((kart_mp4, 4.0))

    # 2) xfade zinciri
    girdiler = []
    for p, _ in parcalar:
        girdiler += ["-i", p]
    fc, prev, ofs = [], "[0:v]", 0.0
    for i in range(1, len(parcalar)):
        ofs += parcalar[i - 1][1] - XF
        cikis = f"[v{i}]" if i < len(parcalar) - 1 else "[v]"
        fc.append(f"{prev}[{i}:v]xfade=transition=fade:duration={XF}:offset={ofs:.3f}{cikis}")
        prev = cikis
    son = os.path.join(OUT, "mia-reel-hikaye.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *girdiler, "-filter_complex", ";".join(fc), "-map", "[v]",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", son], check=True)
    print("  →", os.path.relpath(son, ROOT))


if __name__ == "__main__":
    main()
