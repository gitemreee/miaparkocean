#!/usr/bin/env python3
"""
İnşaat timelapse reel'i (1080x1920): sabit kameradan boş arsa → temel → iskelet → cephe → bitmiş proje.

Girdi: Higgsfield'da (nano_banana_pro) bitmiş render'ın açısından üretilen aşama kareleri ve her aşama çifti
için Kling 3.0 start/end-image klipleri (sosyal-medya/reel-timelapse/klip/*.mp4, sırayla). Çıktı:
sosyal-medya/reel-timelapse/mia-reel-timelapse.mp4 (sessiz; müzik Instagram'da eklenir).

    python3.13 scripts/build-reel-timelapse.py
"""

import importlib.util as _il
import os
import subprocess
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "sosyal-medya", "reel-timelapse")
KLIP = os.path.join(OUT, "klip")
W, H, FPS = 1080, 1920, 30
XF = 0.35                     # aşamalar arası kısa geçiş (kareler zaten eşleşiyor)
FONT_K = os.path.join(ROOT, "sunum", "yazitipi", "Montserrat-Black.ttf")
FONT_O = os.path.join(ROOT, "sunum", "yazitipi", "Montserrat-Medium.ttf")

_spec = _il.spec_from_file_location("rh", os.path.join(ROOT, "scripts", "build-reel-hikaye.py"))
rh = _il.module_from_spec(_spec)
_spec.loader.exec_module(rh)

KLIPLER = ["1-arsa-temel.mp4", "2-temel-iskelet.mp4", "3-iskelet-cephe.mp4", "4-cephe-bitmis.mp4"]
_TMP = tempfile.mkdtemp(prefix="tltxt-")


def _tf(s, ad):
    p = os.path.join(_TMP, ad + ".txt")
    open(p, "w", encoding="utf-8").write(s)
    return p


def ust_yazi(ust, alt, ad):
    """Üstte küçük başlık + alt satır (ilk klipte giriş, son klipte proje adı)."""
    return (
        f",drawbox=x=0:y=0:w=iw:h=420:color=black@0.30:t=fill,"
        f"drawtext=fontfile={FONT_K}:textfile={_tf(ust, ad + 'u')}:fontsize=64:fontcolor=white:"
        f"shadowcolor=black@0.5:shadowx=0:shadowy=5:x=(w-text_w)/2:y=150,"
        f"drawtext=fontfile={FONT_O}:textfile={_tf(alt, ad + 'a')}:fontsize=44:fontcolor=white@0.95:"
        f"shadowcolor=black@0.5:shadowx=0:shadowy=4:x=(w-text_w)/2:y=240"
    )


def main():
    os.makedirs(OUT, exist_ok=True)
    tekil = os.path.join(OUT, "tekil")
    os.makedirs(tekil, exist_ok=True)
    kart = os.path.join(OUT, "kapanis-karti.png")
    if not os.path.exists(kart):
        rh.kapanis_karti(kart)

    parcalar = []
    for i, dosya in enumerate(KLIPLER):
        src = os.path.join(KLIP, dosya)
        dst = os.path.join(tekil, dosya)
        vf = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}"
        if i == 0:
            vf += ust_yazi("BİR PROJE", "önce hayal edilir, sonra yükselir.", "ilk")
        if i == len(KLIPLER) - 1:
            vf += ust_yazi("MİA PARK OCEAN", "İzmit MİA Bölgesi'nde yaşam başlıyor", "son")
        sure = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src],
                                    capture_output=True, text=True).stdout.strip())
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", vf, "-an", "-r", str(FPS),
                        "-video_track_timescale", "15360", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                        "-pix_fmt", "yuv420p", dst], check=True)
        parcalar.append((dst, sure))

    kart_mp4 = os.path.join(tekil, "9-kapanis.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", kart, "-t", "4", "-vf",
                    f"scale={W}:{H},zoompan=z='1+0.0008*in':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS},fps={FPS}",
                    "-r", str(FPS), "-video_track_timescale", "15360",
                    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", kart_mp4], check=True)
    parcalar.append((kart_mp4, 4.0))

    girdiler = []
    for p, _ in parcalar:
        girdiler += ["-i", p]
    fc, prev, ofs = [], "[0:v]", 0.0
    for i in range(1, len(parcalar)):
        xf = 0.8 if i == len(parcalar) - 1 else XF
        ofs += parcalar[i - 1][1] - xf
        cikis = f"[v{i}]" if i < len(parcalar) - 1 else "[v]"
        fc.append(f"{prev}[{i}:v]xfade=transition=fade:duration={xf}:offset={ofs:.3f}{cikis}")
        prev = cikis
    son = os.path.join(OUT, "mia-reel-timelapse.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *girdiler, "-filter_complex", ";".join(fc), "-map", "[v]",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", son], check=True)
    print("  →", os.path.relpath(son, ROOT))


if __name__ == "__main__":
    main()
