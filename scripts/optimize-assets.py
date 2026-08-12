#!/usr/bin/env python3
"""
MİA PARK OCEAN — yayın varlıklarını gösterildikleri boyuta indirger.

Sorun: marka görselleri kaynak çözünürlükte yayınlanıyordu (başlıktaki 36px
işaret için 640px'lik dosya, 210px'lik footer logosu için 1200px'lik dosya
gibi). Hero videosu ise 960x960 / 10.4 Mbit-sn ile 12.7 MB idi ve sayfa
açılır açılmaz tamamı iniyordu.

ÖNEMLİ: `brand/*.png` dosyaları BASKI ustasıdır — katalog ve davetiye
betikleri 300 dpi çıktı için onları okur, bu yüzden hiç küçültülmez.
Site yalnızca `.webp` sürümlerini kullanır; küçültülen sadece onlardır.

Bu betik:
  1) Hero videosunu yeniden kodlar (H.264, CRF 30, sessiz, faststart)
  2) Site tarafındaki WebP kopyalarını 2x gösterim boyutuna indirir
  3) Ortak logolarının (YKB, KOOPBİS) web sürümlerini üretir

`scripts/build-brand-assets.py` ve `scripts/build-wave.py` çalıştırıldıktan
SONRA çalıştırılmalıdır — onlar tam çözünürlükte yeniden yazar.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
PUB = ROOT / "public"
BRAND = PUB / "brand"

# (kaynak png, hedef webp, genişlik) — hedef, en büyük gösterim boyutunun ~2 katı
WEB_TARGETS: list[tuple[Path, Path, int]] = [
    # Başlıktaki işaret 36px yükseklikte → 2x için 200px genişlik yeter
    (BRAND / "mark-ocean-trim.png", BRAND / "mark-ocean-trim.webp", 200),
    (BRAND / "mark-ocean-white.png", BRAND / "mark-ocean-white.webp", 200),
    (BRAND / "mark-ocean.png", BRAND / "mark-ocean.webp", 200),
    # Footer / davetiye logoları en fazla 230px genişlikte
    (BRAND / "logo-ocean-trim.png", BRAND / "logo-ocean-trim.webp", 520),
    (BRAND / "logo-ocean-white.png", BRAND / "logo-ocean-white.webp", 520),
    (BRAND / "logo-ocean.png", BRAND / "logo-ocean.webp", 520),
    # Dalga: en geniş kullanım masaüstünde ~%178 viewport → 2x için 1600px yeter
    (BRAND / "wave.png", BRAND / "wave.webp", 1600),
    # Ortak logoları rozet şeridinde 40px yükseklikte
    (PUB / "ykb-logo.png", PUB / "ykb-logo.webp", 360),
    (PUB / "koopbis-logo.png", PUB / "koopbis-logo.webp", 320),
    (PUB / "ocean-logo-white.png", PUB / "ocean-logo-white.webp", 400),
]

VIDEO_SRC = PUB / "videos" / "hero-tanitim.mp4"
VIDEO_CRF = 30  # görsel olarak kaynakla ayırt edilemiyor, ~7x küçük


def ffmpeg() -> str:
    import imageio_ffmpeg

    return imageio_ffmpeg.get_ffmpeg_exe()


def kb(p: Path) -> float:
    return p.stat().st_size / 1024 if p.exists() else 0.0


def make_web(src: Path, dst: Path, width: int) -> None:
    if not src.exists():
        print(f"  atlandı (yok): {src.name}")
        return
    before = kb(dst)
    im = Image.open(src)
    im = im.convert("RGBA") if im.mode in ("RGBA", "LA", "P") else im.convert("RGB")
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im.save(dst, quality=88, method=6)
    print(f"  {dst.name:<26} {before:6.0f} → {kb(dst):5.0f} KB   {im.width}x{im.height}")


def reencode_video() -> None:
    if not VIDEO_SRC.exists():
        print("  video yok, atlandı")
        return
    before = kb(VIDEO_SRC)
    tmp = VIDEO_SRC.with_suffix(".opt.mp4")
    subprocess.run(
        [
            ffmpeg(), "-y", "-v", "error",
            "-i", str(VIDEO_SRC),
            "-an",                       # ses yok (kaynak zaten sessiz)
            "-c:v", "libx264", "-preset", "slow", "-crf", str(VIDEO_CRF),
            "-pix_fmt", "yuv420p",
            "-g", "48",                  # sık keyframe: döngü başı takılmasın
            "-movflags", "+faststart",   # metadata başta: aşamalı oynatma
            str(tmp),
        ],
        check=True,
    )
    if kb(tmp) < before * 0.95:
        tmp.replace(VIDEO_SRC)
        print(f"  hero-tanitim.mp4          {before:6.0f} → {kb(VIDEO_SRC):5.0f} KB")
    else:
        tmp.unlink()
        print(f"  hero-tanitim.mp4          {before:6.0f} KB (zaten küçük)")


def main() -> None:
    print("Video…")
    reencode_video()
    print("\nSite görselleri (WebP) gösterim boyutuna indiriliyor…")
    for src, dst, width in WEB_TARGETS:
        make_web(src, dst, width)
    print("\nNot: brand/*.png baskı ustasıdır, küçültülmedi.")


if __name__ == "__main__":
    main()
