#!/usr/bin/env python3
"""
Sesli reklam reel'i (1080x1920, 30 fps): seslendirme + fotoğraflar (yavaş yakınlaşma) + sesle eş zamanlı balonlar.

Seslendirme: Piper (açık kaynak, çevrimdışı) tr_TR-dfki-medium; cümle cümle wav (scratch/ses/c{i}.wav).
Fotoğraflar: sosyal-medya/bitmis-fotograflar. Balon katmanları Chromium ile şeffaf PNG olarak çizilir.

    python3.13 scripts/build-reel-sesli.py <ses_klasoru>
"""

import json
import os
import subprocess
import sys
import tempfile
import wave

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "sosyal-medya", "reel-sesli")
FOTO = os.path.join(ROOT, "sosyal-medya", "bitmis-fotograflar")
FONT = os.path.join(ROOT, "brand-source", "fonts", "Montserrat-var.ttf")
W, H, FPS = 1080, 1920, 30
LAC, LAC2, ALTIN, ALTIN2, KIR, SIY = "#0f2a5a", "#17407f", "#c9a24a", "#e8c877", "#e3262e", "#141414"
F = lambda *p: "file://" + os.path.join(ROOT, *p)
GIRIS = 0.30          # sahne başından seslendirmeye kadar
KUYRUK = 0.55         # seslendirme bitişinden sahne sonuna kadar

CSS = f"""
@font-face {{ font-family: Mont; src: url("file://{FONT}"); font-weight: 100 900; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:transparent; font-family:Mont,sans-serif;
             -webkit-font-smoothing:antialiased; }}
.a {{ position:absolute; }}
.tek {{ white-space:nowrap; line-height:1; }}
.golge {{ box-shadow:0 18px 40px rgba(0,0,0,.35), 0 4px 10px rgba(0,0,0,.25); }}
.yazi-golge {{ text-shadow:0 4px 18px rgba(0,0,0,.55), 0 2px 4px rgba(0,0,0,.45); }}
.altin {{ background:linear-gradient(180deg,#fff1c4 0%,{ALTIN2} 35%,{ALTIN} 70%,#a87b2c 100%);
         -webkit-background-clip:text; background-clip:text; color:transparent; }}
.pill {{ display:inline-flex; align-items:center; gap:18px; color:#fff; font-weight:900; letter-spacing:.03em;
        height:118px; padding:0 46px 0 20px; border-radius:59px; white-space:nowrap; font-size:52px;
        box-shadow:0 14px 30px rgba(0,0,0,.35); border:4px solid rgba(255,255,255,.9); }}
.tik {{ display:inline-flex; align-items:center; justify-content:center; width:74px; height:74px; border-radius:50%;
       background:#fff; color:{KIR}; font-size:40px; font-weight:900; }}
"""

ALT_BANT = f"""
<div class="a" style="left:0;bottom:0;width:{W}px;height:260px;background:linear-gradient(0deg,rgba(9,24,52,.92) 0%,rgba(9,24,52,.6) 55%,rgba(9,24,52,0) 100%)"></div>
<div class="a" style="left:0;bottom:70px;width:{W}px;display:flex;align-items:center;justify-content:center;gap:34px">
  <img src="{F('public','brand','logo-mia-2026.png')}" style="height:84px;filter:brightness(0) invert(1)">
  <div style="width:3px;height:64px;background:rgba(255,255,255,.5)"></div>
  <div class="tek" style="font-size:58px;font-weight:900;color:#fff;letter-spacing:.04em"><span style="color:{ALTIN2}">☎</span> 444 10 58</div>
</div>"""


def pill(m, r):
    return f'<div class="pill" style="background:{r}"><span class="tik">✕</span>{m}</div>'


def katman(govde, bant=True):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{govde}{ALT_BANT if bant else ""}</body></html>'


YOKLAR = [("ARA ÖDEME YOK!", SIY), ("FAİZ YOK!", KIR), ("BANKA YOK!", SIY), ("KREDİ YOK!", KIR), ("KEFİL YOK!", SIY)]

# her sahne: fotoğraf, ses no, katmanlar [(html, sahne içi görünme zamanı)], yakınlaşma yönü
def sahneler():
    s = []
    s.append(dict(foto="22-uzaktan-teleobjektif.jpg", ses=0, zoom="in", katman=[(katman(f"""
      <div class="a tek yazi-golge" style="left:0;width:{W}px;top:330px;text-align:center;font-size:58px;font-weight:700;color:#fff;letter-spacing:.24em">İZMİT'TE</div>
      <div class="a tek yazi-golge" style="left:0;width:{W}px;top:420px;text-align:center;font-size:92px;font-weight:900;color:#fff">YENİ BİR YAŞAM</div>
      <div class="a tek yazi-golge altin" style="left:0;width:{W}px;top:530px;text-align:center;font-size:110px;font-weight:900">BAŞLIYOR</div>
    """), 0.15)]))
    s.append(dict(foto="23-giris-avlu-gun-batimi.jpg", ses=1, zoom="out", katman=[(katman(f"""
      <div class="a" style="left:0;top:0;width:{W}px;height:{H}px;background:radial-gradient(60% 40% at 50% 42%,rgba(9,24,52,.72) 0%,rgba(9,24,52,.25) 70%,rgba(9,24,52,0) 100%)"></div>
      <img class="a" src="{F('public','brand','logo-mia-2026.png')}" style="left:190px;top:520px;width:700px;filter:brightness(0) invert(1) drop-shadow(0 10px 30px rgba(0,0,0,.5))">
    """, bant=False), 0.10)]))
    s.append(dict(foto="15-balkondan-gunesli.jpg", ses=2, zoom="in", katman=[(katman(f"""
      <div class="a golge" style="left:70px;top:240px;width:940px;padding:40px 30px 44px;border-radius:44px;text-align:center;
           background:linear-gradient(160deg,{LAC2} 0%,{LAC} 70%);border:5px solid {ALTIN}">
        <div class="tek altin" style="font-size:132px;font-weight:900;letter-spacing:-.02em">1 MİLYON TL</div>
        <div class="tek" style="margin-top:16px;font-size:56px;font-weight:800;color:#fff;letter-spacing:.06em">PEŞİNATLA</div>
        <div class="tek" style="margin-top:14px;font-size:60px;font-weight:900;color:#fff">YENİ EVİNİZE TAŞININ!</div>
        <div class="a" style="left:120px;bottom:-46px;border-left:34px solid transparent;border-right:34px solid transparent;border-top:46px solid {ALTIN}"></div>
        <div class="a" style="left:126px;bottom:-36px;border-left:28px solid transparent;border-right:28px solid transparent;border-top:38px solid {LAC}"></div>
      </div>"""), 0.15)]))
    s.append(dict(foto="21-yoldan-gunesli.jpg", ses=3, zoom="out", katman=[(katman(f"""
      <div class="a golge" style="left:90px;top:420px;width:900px;height:220px;border-radius:110px;background:{KIR};border:6px solid #fff;
           display:flex;align-items:center;justify-content:center;gap:30px;transform:rotate(-3deg)">
        <div class="tek" style="font-size:140px;font-weight:900;color:#fff">60 AY</div>
        <div style="line-height:1.02;color:#fff;font-weight:900">
          <div class="tek" style="font-size:62px">SABİT</div><div class="tek" style="font-size:62px">TAKSİT</div></div>
      </div>"""), 0.15)]))
    # yoklar: her biri sırayla, seslendirmedeki "… yok" anlarına yakın
    yok_k = []
    for i, (m, r) in enumerate(YOKLAR):
        x = 140 if i % 2 == 0 else 300
        yok_k.append((katman(f'<div class="a" style="left:{x}px;top:{250 + i * 150}px">{pill(m, r)}</div>', bant=(i == 0)), None))
    s.append(dict(foto="19-balkon-cay-gunduz.jpg", ses=4, zoom="in", katman=yok_k, yok=True))
    s.append(dict(foto="18-arka-bahce-gunduz.jpg", ses=5, zoom="out", katman=[(katman(f"""
      <div class="a golge" style="left:110px;top:420px;width:860px;padding:34px 0;border-radius:36px;text-align:center;
           background:linear-gradient(180deg,#fff1c4 0%,{ALTIN2} 40%,{ALTIN} 100%);border:5px solid #fff;transform:rotate(2deg)">
        <div class="tek" style="font-size:40px;font-weight:800;color:{LAC};letter-spacing:.24em">EV &amp; ARAÇ</div>
        <div class="tek" style="margin-top:10px;font-size:76px;font-weight:900;color:{LAC}">TAKASINA</div>
        <div class="tek" style="margin-top:6px;font-size:76px;font-weight:900;color:{KIR}">AÇIKTIR!</div>
      </div>"""), 0.15)]))
    s.append(dict(foto="22-uzaktan-teleobjektif.jpg", ses=6, zoom="none", son=True, katman=[(katman(f"""
      <div class="a" style="left:0;top:0;width:{W}px;height:{H}px;background:linear-gradient(180deg,rgba(9,24,52,.86) 0%,rgba(9,24,52,.80) 60%,rgba(9,24,52,.95) 100%)"></div>
      <img class="a" src="{F('public','brand','vektor','tilda-beyaz.svg')}" style="left:390px;top:200px;width:300px">
      <img class="a" src="{F('public','brand','logo-mia-2026.png')}" style="left:240px;top:380px;width:600px;filter:brightness(0) invert(1)">
      <div class="a" style="left:290px;top:860px;width:500px;height:3px;background:{ALTIN}"></div>
      <div class="a tek altin" style="left:0;width:{W}px;top:925px;text-align:center;font-size:80px;font-weight:900">1 MİLYON TL PEŞİNAT</div>
      <div class="a tek" style="left:0;width:{W}px;top:1050px;text-align:center;font-size:46px;font-weight:800;color:#fff;letter-spacing:.04em">60 AY SABİT TAKSİT · TAKAS İMKÂNI</div>
      <div class="a" style="left:290px;top:1150px;width:500px;height:3px;background:{ALTIN}"></div>
      <div class="a tek" style="left:0;width:{W}px;top:1230px;text-align:center;font-size:130px;font-weight:900;color:#fff;letter-spacing:.03em">444 10 58</div>
      <div class="a tek" style="left:0;width:{W}px;top:1400px;text-align:center;font-size:52px;font-weight:700;color:{ALTIN2};letter-spacing:.1em">miaparkocean.com</div>
      <img class="a" src="{F('public','brand','vektor','ocean-beyaz.svg')}" style="left:430px;top:1570px;width:220px;opacity:.9">
    """, bant=False), 0.0)]))
    return s


def wav_sure(p):
    with wave.open(p) as w:
        return w.getnframes() / w.getframerate()


def main():
    ses_dir = sys.argv[1]
    os.makedirs(OUT, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="reelses-")
    S = sahneler()

    # 1) katmanları çiz
    isler, idx = [], 0
    for si, sc in enumerate(S):
        for ki, (html, _) in enumerate(sc["katman"]):
            hp = os.path.join(tmp, f"k{si}_{ki}.html")
            open(hp, "w", encoding="utf-8").write(html)
            isler.append(dict(html=hp, w=W, h=H, dsf=1, dilim=W, cikti=os.path.join(tmp, f"k{si}_{ki}")))
    jp = os.path.join(tmp, "isler.json")
    json.dump(isler, open(jp, "w"))
    npm = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    subprocess.run(["node", os.path.join(ROOT, "scripts", "mega-bilbord", "render.cjs"), jp], check=True,
                   env={**os.environ, "NODE_PATH": npm}, stdout=subprocess.DEVNULL)

    # 2) sahne videoları
    parcalar, zaman, ses_yer = [], 0.0, []
    for si, sc in enumerate(S):
        sw = os.path.join(ses_dir, f"c{sc['ses']}.wav")
        sd = wav_sure(sw)
        sure = GIRIS + sd + (1.4 if sc.get("son") else KUYRUK)
        ses_yer.append((sw, zaman + GIRIS))
        n = int(round(sure * FPS))
        z = {"in": "1+0.10*on/{n}", "out": "1.10-0.10*on/{n}", "none": "1+0.03*on/{n}"}[sc["zoom"]].format(n=n)
        foto = os.path.join(FOTO, sc["foto"])
        girdiler = ["-loop", "1", "-framerate", str(FPS), "-t", f"{sure:.3f}", "-i", foto]
        fc = [f"[0:v]scale={W * 3}:{H * 3}:force_original_aspect_ratio=increase,crop={W * 3}:{H * 3},"
              f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS},setsar=1[b0]"]
        prev = "b0"
        katmanlar = sc["katman"]
        if sc.get("yok"):
            # 5 "yok" seslendirme süresine eşit dağıtılır
            adim = sd / len(katmanlar)
            zamanlar = [GIRIS + i * adim for i in range(len(katmanlar))]
        else:
            zamanlar = [t for _, t in katmanlar]
        for ki, t in enumerate(zamanlar):
            png = json.load(open(os.path.join(tmp, f"k{si}_{ki}.json")))[0]
            girdiler += ["-loop", "1", "-framerate", str(FPS), "-t", f"{sure:.3f}", "-i", png]
            fc.append(f"[{ki + 1}:v]format=rgba,fade=t=in:st={t:.3f}:d=0.22:alpha=1[o{ki}]")
            fc.append(f"[{prev}][o{ki}]overlay=0:0:format=auto[b{ki + 1}]")
            prev = f"b{ki + 1}"
        if si == 0:
            fc.append(f"[{prev}]fade=t=in:st=0:d=0.35[bx]"); prev = "bx"
        if sc.get("son"):
            fc.append(f"[{prev}]fade=t=out:st={sure - 0.5:.3f}:d=0.5[bx]"); prev = "bx"
        mp4 = os.path.join(tmp, f"s{si}.mp4")
        subprocess.run(["ffmpeg", "-v", "error", "-y", *girdiler, "-filter_complex", ";".join(fc), "-map", f"[{prev}]",
                        "-frames:v", str(n), "-r", str(FPS), "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                        "-pix_fmt", "yuv420p", mp4], check=True)
        parcalar.append(mp4)
        zaman += n / FPS

    liste = os.path.join(tmp, "liste.txt")
    open(liste, "w").write("".join(f"file '{p}'\n" for p in parcalar))
    video = os.path.join(tmp, "video.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", liste, "-c", "copy", video], check=True)

    # 3) ses: cümleleri yerine koy, temizle, yükseklik normalize
    girdiler, fc = [], []
    for i, (p, t) in enumerate(ses_yer):
        girdiler += ["-i", p]
        ms = int(t * 1000)
        fc.append(f"[{i}:a]aresample=48000,adelay={ms}|{ms},apad[a{i}]")
    fc.append("".join(f"[a{i}]" for i in range(len(ses_yer))) +
              f"amix=inputs={len(ses_yer)}:normalize=0,atrim=0:{zaman:.3f},"
              "highpass=f=80,equalizer=f=3000:t=q:w=1.2:g=2.5,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,"
              "loudnorm=I=-15:TP=-1.5:LRA=7[a]")
    ses = os.path.join(tmp, "ses.m4a")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *girdiler, "-filter_complex", ";".join(fc), "-map", "[a]",
                    "-c:a", "aac", "-b:a", "192k", ses], check=True)

    son = os.path.join(OUT, "mia-reel-sesli.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-i", ses, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "copy", "-shortest", "-movflags", "+faststart", son], check=True)
    print("  →", os.path.relpath(son, ROOT), f"{zaman:.1f} sn")


if __name__ == "__main__":
    main()
