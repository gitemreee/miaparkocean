#!/usr/bin/env python3
"""
MİA PARK OCEAN — "premium" sinematik reklam filmi (1080x1920, 24 fps) · 45, 30 ve 15 saniyelik üç kurgu.

Ana filmden (build-reel-drone.py) farkı:
  • Uzun harita girişi yerine çarpıcı bir açılış: altın saatte tarlanın üstünden projeye alçak uçuş.
  • Konum bölümü 3–4 saniye: hızlı uydu inişi, logo rozeti, iki raylı sistem hattı, dört yakın yer.
  • Fiyatlar kutu/etiket yerine sade tipografiyle: lacivert geçiş, şampanya altını çizgi, beyaz rakam.
  • Sosyal alanlar yazı listesi yerine çekimle: süs havuzu, yürüyüş yolu, oyun parkı, kapalı otopark
    (hepsi projenin kendi görsellerinden, public/images/ic-mekan). Referans görseli olmayan donatılar
    (kapalı yüzme havuzu, fitness, sauna, Türk hamamı) UYDURULMAZ — yalnızca yazıyla verilir.
  • Kapanış: gece çekiminde yavaş geri çekilme (kurguda yapılır; mimari bozulmaz), marka, telefon.
  • Özgün orkestral müzik, tek renk tonu, ince film greni, yumuşak geçişler.

Bütün yazılar kurguda eklenir; üretilen çekimlerde yazı yoktur. Mimari, fiyatlar, ödeme koşulları ve
iletişim bilgileri ana filmle aynıdır.

    python3 scripts/build-reel-premium.py 45      # veya 30, 15
"""

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import wave

import numpy as np

KOK = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("rd", os.path.join(KOK, "build-reel-drone.py"))
rd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rd)

W, H, FPS, SR = rd.W, rd.H, rd.FPS, rd.SR
ROOT, VEK, KLIP = rd.ROOT, rd.VEK, rd.KLIP
LACI, ALTIN = "#10254f", "#d9c08c"                 # lacivert, şampanya altını
LR, LG, LB = (int(LACI[i:i + 2], 16) for i in (1, 3, 5))
OUT = os.path.join(ROOT, "sosyal-medya", "instagram-reel", "premium")
SES = lambda ad: os.path.join(ROOT, "film-source", "ses", ad)
MUZ = lambda ad: os.path.join(ROOT, "film-source", "muzik", "premium", ad)
GECIS = 0.3

# (sahne, süre, kaynak çekim, çekimde başlangıç, hız | "sigdir")
KURGU = {
    "45": dict(
        sahne=[("acilis", 3.0, "24-acilis-drone", 0.1, "sigdir"), ("cift", 1.9, "20-sokak-cift", 1.0, 1.0), ("harita", 3.6, None, 0, 1),
               ("yapim", 4.8, "17-yapim-asamasi", 0.0, "sigdir"), ("drone", 2.3, "22-drone-sola", 0.3, 1.15),
               ("d10", 3.95, "07-1-0-salon", 0.2, 1.1), ("d11", 3.95, "09-1-1-salon", 0.2, 1.1), ("d21", 3.3, "11-2-1-salon", 0.2, 1.2),
               ("s1", 2.0, "25-sus-havuzu", 0.4, 1.2), ("s2", 2.0, "26-yuruyus-yolu", 0.4, 1.2), ("s3", 2.0, "27-oyun-parki", 0.4, 1.2),
               ("s4", 1.9, "28-kapali-otopark", 0.4, 1.2), ("s5", 2.5, "23-tepeden-suzulme", 0.0, 1.0),
               ("final", 7.7, "06-aksam", 0.0, "sigdir")],
        ses=[("yeni/vo-1.wav", "acilis", .55), ("yeni/vo-4.wav", "yapim", .3), ("yeni/vo-5.wav", "d10", .08), ("yeni/vo-6.wav", "d11", .08),
             ("yeni/vo-7.wav", "d21", .12), ("yeni/vo-11.wav", "final", .4)],
        muzik=("muzik-45.mp3", 0.0)),
    "30": dict(
        sahne=[("acilis", 2.6, "24-acilis-drone", 0.3, "sigdir"), ("harita", 3.1, None, 0, 1),
               ("yapim", 2.8, "17-yapim-asamasi", 0.0, "sigdir"),
               ("d10", 2.6, "07-1-0-salon", 0.3, 1.3), ("d11", 2.6, "09-1-1-salon", 0.3, 1.3), ("d21", 2.6, "11-2-1-salon", 0.3, 1.3),
               ("s1", 1.45, "25-sus-havuzu", 0.6, 1.3), ("s2", 1.45, "26-yuruyus-yolu", 0.6, 1.3), ("s3", 1.45, "27-oyun-parki", 0.6, 1.3),
               ("s5", 1.9, "23-tepeden-suzulme", 0.2, 1.1),
               ("final", 7.8, "06-aksam", 0.0, "sigdir")],
        ses=[("yeni/vo-1.wav", "acilis", .35), ("premium/vo-fiyat-ozet.wav", "d10", .35), ("yeni/vo-11.wav", "final", .4)],
        muzik=("muzik-30.mp3", 0.0)),
    "15": dict(
        sahne=[("acilis", 2.3, "24-acilis-drone", 1.0, 1.5),
               ("d10", 2.1, "07-1-0-salon", 0.4, 1.4), ("d11", 2.1, "09-1-1-salon", 0.4, 1.4), ("d21", 2.1, "11-2-1-salon", 0.4, 1.4),
               ("final", 6.4, "06-aksam", 0.0, "sigdir")],
        ses=[("premium/vo-arayin.wav", "final", 1.5)],
        muzik=("muzik-30.mp3", 16.9)),                 # 30'luk parçanın doruk + kapanış bölümü
}
FIYAT = {"d10": ("1+0 DAİRELER", "699.000", "29.900"), "d11": ("1+1 DAİRELER", "999.000", "39.900"), "d21": ("2+1 DAİRELER", "2.000.000", "50.000")}
SOSYAL = {
    "s1": ["DEKORATİF SÜS HAVUZLARI"],
    "s2": ["GENİŞ PEYZAJ ALANLARI", "YÜRÜYÜŞ VE DİNLENME YOLLARI"],
    "s3": ["ÇOCUK OYUN PARKI"],
    "s4": ["KAPALI OTOPARK", "7/24 GÜVENLİK"],
    "s5": ["YARI OLİMPİK KAPALI YÜZME HAVUZU", "FITNESS SALONU · SAUNA · TÜRK HAMAMI"],
}
SOSYAL_KISA = {"s5": ["KAPALI YÜZME HAVUZU · FITNESS · SAUNA", "TÜRK HAMAMI · KAPALI OTOPARK · 7/24 GÜVENLİK"]}   # 30 sn: otopark çekimi yok
YAKIN = [  # (ad, süre, enlem, boylam, etiketin tarafı)
    ("Sahil", "2 dk", 40.7367, 29.9395, "sol"),
    ("41 Burda · İzmit Outlet", "2 dk", 40.7561, 29.9472, "sag"),
    ("Şehir Merkezi", "5 dk", 40.77211, 29.95056, "sol"),
    ("Şehir Hastanesi", "5 dk", 40.78309, 29.96064, "sag"),
]


def zaman(surum):
    T, SURE, t = {}, {}, 0.0
    for ad, sure, *_ in KURGU[surum]["sahne"]:
        T[ad], SURE[ad] = t, sure
        t += sure
    return T, SURE, t


# ---------------------------------------------------------------- yazı katmanı
GOLGE = "text-shadow:0 2px 22px rgba(4,10,26,.7),0 1px 3px rgba(4,10,26,.55)"


def el(t, sinif, stil, ic=""):
    return f'<div class="a {sinif}" style="--t:{t:.3f}s;{stil}">{ic}</div>'


def gecis_perdesi(t, ust, yukseklik, koyuluk=.62):
    """Yazının arkasında yumuşak kenarlı lacivert bant: görüntünün geri kalanı açık kalır."""
    return el(t, "sol", f"left:0;top:{ust}px;width:{W}px;height:{yukseklik}px;background:rgba({LR},{LG},{LB},{koyuluk});"
                        f"-webkit-mask-image:linear-gradient(180deg,transparent 0,#000 20%,#000 78%,transparent 100%)")


def ortali_baslik(t, y, ust, satirlar, boy=78):
    ana = "".join(f'<div class="tek">{s}</div>' for s in satirlar)
    return (el(t, "yuk", f"left:0;top:{y}px;width:{W}px;text-align:center;font-size:27px;font-weight:600;letter-spacing:.62em;padding-left:.62em;color:{ALTIN};{GOLGE}", ust)
            + el(t + .12, "yuk", f"left:0;top:{y + 62}px;width:{W}px;text-align:center;font-size:{boy}px;font-weight:400;letter-spacing:.13em;padding-left:.13em;"
                                 f"line-height:1.24;color:#fff;{GOLGE}", ana)
            + el(t + .35, "cizgi-o", f"left:{W // 2 - 48}px;top:{y + 62 + round(boy * 1.24 * len(satirlar)) + 30}px;width:96px;height:2px;background:{ALTIN}"))


def alt_yazi(t, kicker, satirlar, boy=38, ara=.14):
    """Sol altta sade açıklama: küçük altın üst satır, ince çizgi, beyaz büyük harf satırlar."""
    n = len(satirlar)
    y0 = 1206 - n * round(boy * 1.55)
    h = gecis_perdesi(t - .1, y0 - 190, 1206 - y0 + 330, .55)
    h += el(t, "yuk", f"left:84px;top:{y0 - 70}px;font-size:24px;font-weight:600;letter-spacing:.44em;color:{ALTIN}", f'<span class="tek">{kicker}</span>')
    h += el(t + .1, "cizgi", f"left:84px;top:{y0 - 24}px;width:112px;height:2px;background:{ALTIN}")
    for i, s in enumerate(satirlar):
        h += el(t + .18 + i * ara, "yuk", f"left:84px;top:{y0 + i * round(boy * 1.55)}px;font-size:{boy}px;font-weight:500;letter-spacing:.13em;color:#fff", f'<span class="tek">{s}</span>')
    return h


def fiyat(t, d, tip, pesin, ayda):
    """Fiyat: kutu yok. Lacivert geçiş üstünde altın üst satır, büyük beyaz rakam, altında aylık taksit."""
    k = min(1.0, d / 3.6)
    g = lambda i: t + (.16 + i * .14) * k
    x = 84
    return (gecis_perdesi(t, 730, 640)
            + el(g(0), "yuk", f"left:{x}px;top:872px;font-size:29px;font-weight:600;letter-spacing:.36em;color:{ALTIN}", f'<span class="tek">{tip}</span>')
            + el(g(1), "cizgi", f"left:{x}px;top:928px;width:132px;height:2px;background:{ALTIN}")
            + el(g(1), "ac", f"left:{x - 6}px;top:944px;padding:0 6px", f'<span class="tek" style="font-size:136px;font-weight:500;letter-spacing:-.01em;line-height:1;color:#fff">{pesin}'
                             f'<span style="font-size:46px;font-weight:500;margin-left:16px;letter-spacing:.04em">TL</span></span>')
            + el(g(2), "yuk", f"left:{x + 4}px;top:1092px;font-size:25px;font-weight:500;letter-spacing:.46em;color:rgba(255,255,255,.84)", '<span class="tek">PEŞİNAT</span>')
            + el(g(3), "cizgi", f"left:{x}px;top:1148px;width:{W - 2 * x}px;height:1px;background:rgba(255,255,255,.28)")
            + el(g(3), "yuk", f"left:{x}px;top:1170px;width:{W - 2 * x}px;display:flex;align-items:baseline;justify-content:space-between",
                 f'<span class="tek" style="color:#fff"><span style="font-size:29px;font-weight:400;letter-spacing:.08em;color:rgba(255,255,255,.84)">AYDA</span>'
                 f'<span style="font-size:58px;font-weight:600;margin-left:16px">{ayda}</span><span style="font-size:29px;font-weight:500;margin-left:10px">TL</span></span>'
                 f'<span class="tek" style="font-size:25px;font-weight:600;letter-spacing:.2em;color:{ALTIN}">60 AY SABİT TAKSİT</span>'))


def harita_katmani(t0, d, t_inis):
    """Konum: logo rozeti, iki hat, dört yakın yer. İnişten sonra haritayla birlikte çok hafif büyür."""
    SX, SY, Z1 = rd.SX, rd.SY, rd.Z1
    nokta = lambda la, lo: rd.ekran(la, lo, Z1)
    yol = lambda nk: " ".join(f"{x:.1f},{y:.1f}" for x, y in (nokta(la, lo) for la, lo in nk))
    g = t0 + t_inis
    cizgi = lambda nk, renk, kal, gg: (f'<polyline points="{yol(nk)}" fill="none" stroke="rgba(6,14,34,.55)" stroke-width="{kal + 5}" stroke-linecap="round" stroke-linejoin="round" '
                                       f'pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" class="hat" style="--t:{gg:.2f}s"/>'
                                       f'<polyline points="{yol(nk)}" fill="none" stroke="{renk}" stroke-width="{kal}" stroke-linecap="round" stroke-linejoin="round" '
                                       f'pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" class="hat" style="--t:{gg:.2f}s"/>')
    ic = f'<svg class="a" style="left:0;top:0;overflow:visible" width="{W}" height="{H}">{cizgi(rd.HAT_KUZEY, "rgba(255,255,255,.9)", 4, g - .15)}{cizgi(rd.HAT_GUNEY, "#f0c66a", 7, g)}</svg>'
    for i, (ad, sure, la, lo, taraf) in enumerate(YAKIN):
        x, y = nokta(la, lo)
        gg = g + .1 + i * .17
        yer = f"right:{W - x + 24:.0f}px;transform-origin:100% 50%" if taraf == "sol" else f"left:{x + 24:.0f}px;transform-origin:0 50%"
        ic += el(gg, "sol", f"left:{x - 9:.0f}px;top:{y - 9:.0f}px;width:18px;height:18px;border-radius:50%;background:#fff;box-shadow:0 0 0 5px rgba(217,192,140,.55)")
        ic += el(gg + .06, "yuk", f"top:{y - 27:.0f}px;{yer};display:flex;align-items:baseline;gap:14px;padding:11px 20px 10px;border-radius:30px;"
                                  f"background:rgba({LR},{LG},{LB},.74);border:1px solid rgba(217,192,140,.5)",
                 f'<span class="tek" style="font-size:28px;font-weight:500;letter-spacing:.03em;color:#fff">{ad}</span>'
                 f'<span class="tek" style="font-size:25px;font-weight:700;letter-spacing:.04em;color:{ALTIN}">{sure}</span>')
    lg, pay = 176, 16
    lh = round(lg * 3288 / 4764)
    ic += el(g - .45, "pat", f"left:{SX - 17}px;top:{SY - 17}px;width:34px;height:34px;border-radius:50%;background:{LACI};border:6px solid {ALTIN};box-shadow:0 0 0 4px rgba(255,255,255,.9)")
    ic += el(g - .3, "pat", f"left:{SX - lg // 2 - pay}px;top:{SY + 38}px;transform-origin:50% 0",
             f'<div style="position:absolute;left:{lg // 2 + pay - 13}px;top:-11px;width:26px;height:26px;background:{LACI};border-left:3px solid {ALTIN};border-top:3px solid {ALTIN};transform:rotate(45deg)"></div>'
             f'<div style="position:relative;padding:{pay}px {pay}px {pay - 4}px;border-radius:20px;background:{LACI};border:3px solid {ALTIN};box-shadow:0 18px 40px rgba(0,0,0,.55)">'
             f'<img src="{VEK("mia-beyaz.svg")}" style="display:block;width:{lg}px;height:{lh}px"></div>')
    buyume = rd.olcek(d)
    stil = (f"@keyframes haritab{{from{{transform:scale(1)}}to{{transform:scale({buyume:.5f})}}}}\n"
            f".haritab{{position:absolute;left:0;top:0;width:{W}px;height:{H}px;transform-origin:{SX}px {SY}px;animation:haritab {d - t_inis:.3f}s linear {g:.3f}s both}}")
    gosterge = lambda y, renk, ad, durum, gg: el(gg, "yuk", f"left:84px;top:{y}px;display:flex;align-items:center;gap:16px;{GOLGE}",
                                                 f'<span style="width:54px;height:5px;border-radius:3px;background:{renk}"></span>'
                                                 f'<span class="tek" style="font-size:24px;font-weight:600;letter-spacing:.2em;color:#fff">{ad}</span>'
                                                 f'<span class="tek" style="font-size:22px;font-weight:500;letter-spacing:.16em;color:{renk}">{durum}</span>')
    sabit = (gosterge(1338, "#f0c66a", "GÜNEY METRO HATTI", "PLANLANAN", g + .3) + gosterge(1386, "#ffffff", "KÖRFEZRAY", "YAPIM AŞAMASINDA", g + .42)
             + f'<div class="a tek" style="left:0;top:1600px;width:{W}px;text-align:center;font-size:17px;font-weight:500;letter-spacing:.04em;color:rgba(255,255,255,.7)">'
               f'Uydu görüntüsü: Copernicus Sentinel-2 (2016) · EOX, CC BY 4.0 · Metro güzergâhları yaklaşıktır</div>'
             )
    return stil, f'<div class="haritab">{ic}</div>' + sabit


def kapanis(t, d):
    hiz = min(1.0, d / 7.0)
    g = lambda s: t + s * hiz
    return (el(t, "sol", f"left:0;top:0;width:{W}px;height:{H}px;background:linear-gradient(180deg,rgba({LR},{LG},{LB},.5) 0,rgba({LR},{LG},{LB},0) 26%,rgba({LR},{LG},{LB},0) 52%,"
                         f"rgba({LR},{LG},{LB},.93) 60%,{LACI} 64%)")
            + el(g(.35), "yuk2", f"left:{W // 2 - 150}px;top:286px;width:300px", f'<img src="{VEK("mia-beyaz.svg")}" style="display:block;width:300px">')
            + el(g(.9), "cizgi-o", f"left:{W // 2 - 60}px;top:{286 + 207 + 26}px;width:120px;height:2px;background:{ALTIN}")
            + el(g(1.0), "yuk", f"left:0;top:1158px;width:{W}px;text-align:center;font-size:31px;font-weight:500;letter-spacing:.03em;color:{ALTIN}",
                 '<span class="tek">60 ay sabit taksitle ev sahibi olmak için hemen arayın</span>')
            + el(g(1.3), "ac", f"left:0;top:1208px;width:{W}px;text-align:center", '<span class="tek" style="font-size:150px;font-weight:600;letter-spacing:.01em;line-height:1;color:#fff">444 10 58</span>')
            + el(g(1.9), "yuk", f"left:0;top:1384px;width:{W}px;display:flex;align-items:center;justify-content:center;gap:18px",
                 rd.yy.WA.format(s=50) + '<span class="tek" style="font-size:50px;font-weight:500;letter-spacing:.03em;color:#fff">0540 028 00 41</span>')
            + el(g(2.4), "yuk", f"left:0;top:1474px;width:{W}px;display:flex;align-items:center;justify-content:center;gap:30px",
                 f'<img src="{VEK("tilda-beyaz.svg")}" style="height:34px"><span style="width:1px;height:46px;background:rgba(255,255,255,.4)"></span>'
                 f'<span class="tek" style="font-size:19px;font-weight:600;letter-spacing:.24em;color:rgba(255,255,255,.85)">TEK YETKİLİ SATIŞ</span>'
                 f'<img src="{VEK("ocean-beyaz.svg")}" style="height:54px">'))


def html(surum, T, SURE, TOPLAM, t_inis):
    stil, govde = "", ""

    def sahne(ad, ic, son=False):
        nonlocal stil, govde
        if ad not in T:
            return
        d = SURE[ad]
        p = 100 if son else 100 * (1 - .26 / d)
        i = len(stil)
        stil += f"@keyframes sc{i}{{0%{{opacity:0}}.01%{{opacity:1}}{p:.2f}%{{opacity:1}}100%{{opacity:{1 if son else 0}}}}}\n"
        govde += f'<div class="a" style="left:0;top:0;width:{W}px;height:{H}px;animation:sc{i} {d:.3f}s linear {T[ad]:.3f}s both">{ic}</div>'

    b = lambda ad, g=0.0: T.get(ad, 0) + g
    sahne("acilis", ortali_baslik(b("acilis", .4), 392, "İZMİT'TE" if surum != "15" else "İZMİT · MİA BÖLGESİ",
                                  ["YENİ BİR YAŞAM", "YÜKSELİYOR"] if surum != "15" else ["MİA PARK", "OCEAN"], 70))
    if "harita" in T:
        hs, hg = harita_katmani(T["harita"], SURE["harita"], t_inis)
        stil += hs + "\n"
        sahne("harita", hg)
    sahne("yapim", alt_yazi(b("yapim", .3), "TİLDA İNŞAAT İLE", ["ADIM ADIM YÜKSELİYOR"], 44))
    sahne("drone", ortali_baslik(b("drone", .25), 470, "İZMİT · MİA BÖLGESİ", ["MİA PARK OCEAN"], 66))
    for ad, (tip, pesin, ayda) in FIYAT.items():
        if ad in T:
            sahne(ad, fiyat(T[ad] + .05, SURE[ad], tip, pesin, ayda))
    sosyal = {**SOSYAL, **(SOSYAL_KISA if "s4" not in T else {})}
    for ad, satirlar in sosyal.items():
        if ad in T:
            uzun = max(len(s) for s in satirlar)
            sahne(ad, alt_yazi(T[ad] + .12, "SOSYAL YAŞAM", satirlar, 38 if uzun < 28 else 31 if uzun < 39 else 27, .1))
    sahne("final", kapanis(T["final"] + .1, SURE["final"]), son=True)
    tf = T["final"]
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{rd.yy.css(H)}
body {{ background:transparent; }}
.yuk {{ animation:yuk .95s cubic-bezier(.16,1,.3,1) var(--t) both; }}
.yuk2 {{ animation:yuk2 1.5s cubic-bezier(.16,1,.3,1) var(--t) both; }}
.sol {{ animation:sol .7s ease-out var(--t) both; }}
.ac {{ animation:ac 1.05s cubic-bezier(.16,1,.3,1) var(--t) both; }}
.pat {{ animation:pat .6s cubic-bezier(.2,.9,.25,1) var(--t) both; }}
.cizgi {{ transform-origin:0 50%; animation:cizgi .8s cubic-bezier(.16,1,.3,1) var(--t) both; }}
.cizgi-o {{ transform-origin:50% 50%; animation:cizgi .9s cubic-bezier(.16,1,.3,1) var(--t) both; }}
.hat {{ animation:ciz 1.1s cubic-bezier(.4,0,.2,1) var(--t) both; }}
@keyframes yuk {{ from{{opacity:0;transform:translateY(30px);filter:blur(7px)}} to{{opacity:1;transform:none;filter:blur(0)}} }}
@keyframes yuk2 {{ from{{opacity:0;transform:scale(1.12);filter:blur(10px)}} to{{opacity:1;transform:none;filter:blur(0)}} }}
@keyframes sol {{ from{{opacity:0}} to{{opacity:1}} }}
@keyframes ac {{ from{{opacity:0;clip-path:inset(0 100% 0 0);transform:translateX(-18px)}} to{{opacity:1;clip-path:inset(0 0 0 0);transform:none}} }}
@keyframes pat {{ 0%{{opacity:0;transform:scale(.6)}} 100%{{opacity:1;transform:scale(1)}} }}
@keyframes cizgi {{ from{{opacity:0;transform:scaleX(0)}} to{{opacity:1;transform:none}} }}
@keyframes ciz {{ from{{stroke-dashoffset:1}} to{{stroke-dashoffset:0}} }}
@keyframes ust {{ 0%{{opacity:0}} {100 * .5 / TOPLAM:.2f}%{{opacity:1}} {100 * (tf - .1) / TOPLAM:.2f}%{{opacity:1}} {100 * (tf + .35) / TOPLAM:.2f}%{{opacity:0}} 100%{{opacity:0}} }}
{stil}
</style></head><body>
  <div class="a" style="left:0;top:0;width:{W}px;height:{H}px;animation:ust {TOPLAM:.3f}s linear 0s both">
    <div class="a" style="left:0;top:0;width:{W}px;height:430px;background:linear-gradient(180deg,rgba({LR},{LG},{LB},.5),rgba({LR},{LG},{LB},0))"></div>
    <img class="a" src="{VEK('mia-beyaz.svg')}" style="left:72px;top:276px;width:136px">
    <img class="a" src="{VEK('tilda-beyaz.svg')}" style="left:{W - 72 - 210}px;top:306px;width:210px">
  </div>
  {govde}
</body></html>"""


# ---------------------------------------------------------------- görüntü
def zemin(surum, T, TOPLAM, gecici, t_inis):
    sahneler = KURGU[surum]["sahne"]
    girdi, f, bas_list = [], [], []
    for i, (ad, _, kaynak, kbas, hiz) in enumerate(sahneler):
        bas = T[ad]
        son = T[sahneler[i + 1][0]] if i + 1 < len(sahneler) else TOPLAM
        sure = son - bas + (GECIS / 2 if i else 0) + (GECIS / 2 if i + 1 < len(sahneler) else 0)
        bas_list.append(bas)
        son_ek = f"trim=duration={sure:.3f},setpts=PTS-STARTPTS,fps={FPS},settb=1/{FPS},setsar=1,format=yuv420p[v{i}]"
        if kaynak is None:
            yol = os.path.join(gecici, "harita.mp4")
            rd.harita_videosu(yol, sure + .2)
            girdi += ["-i", yol]
            f.append(f"[{i}:v]{son_ek}")
            continue
        yol = KLIP(kaynak)
        var = rd.klip_sure(yol) - kbas - .08
        carpan = (sure + .06) / var if hiz == "sigdir" else 1 / hiz
        if hiz != "sigdir" and (sure + .06) * hiz > var:
            raise SystemExit(f"{ad}: çekim kısa ({var:.2f} sn var, {(sure + .06) * hiz:.2f} sn gerek)")
        kare = (f"minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1" if carpan > 1.02 else f"fps={FPS}")
        girdi += ["-ss", f"{kbas:.3f}", "-i", yol]
        if ad == "final":
            # Yavaş geri çekilme kurguda yapılır: kare 2 kat büyütülüp her karede biraz daha geniş kırpılır (mimari değişmez).
            n = round(sure * FPS)
            olcek = (f"scale={2 * W}:{2 * H}:flags=lanczos,zoompan=z='1.5+0.17*pow(1-on/{n},1.6)':x='(iw-iw/zoom)/2':y='1280+(2560-ih/zoom)*0.42':"
                     f"d=1:s={W}x{H}:fps={FPS}")
        else:
            olcek = f"scale={W}:{H}:flags=lanczos"
        f.append(f"[{i}:v]setpts={carpan:.4f}*PTS,{kare},{olcek},{son_ek}")
    onceki = "v0"
    for i in range(1, len(sahneler)):
        f.append(f"[{onceki}][v{i}]xfade=transition=fade:duration={GECIS}:offset={bas_list[i] - GECIS / 2:.3f}[x{i}]")
        onceki = f"x{i}"
    # Tek renk tonu: gölgeler hafif soğuk, ışıklar sıcak; yumuşak kenar kararması; ince gren; siyahtan açılış.
    f.append(f"[{onceki}]eq=contrast=1.05:saturation=.92:gamma=1.0,colorbalance=rs=-.035:bs=.05:rm=.01:rh=.045:bh=-.05,"
             f"vignette=angle=PI/7,noise=alls=5:allf=t,fade=t=in:st=0:d=0.35,format=yuv420p[zemin]")
    return girdi, f, "zemin"


# ---------------------------------------------------------------- ses
def ses(surum, T, TOPLAM, yol):
    n = int(TOPLAM * SR)
    konusma = np.zeros((n, 2), np.float32)
    for dosya, sahne, gec in KURGU[surum]["ses"]:
        a = rd.ses_oku(SES(dosya), "highpass=f=60,equalizer=f=3200:t=q:w=1.2:g=2.5")
        etkin = np.abs(a).max(axis=1) > 0.02
        a *= min(0.17 / np.sqrt((a[etkin] ** 2).mean()), 0.97 / np.abs(a).max())
        j = int((T[sahne] + gec) * SR)
        konusma[j:j + len(a)] += a[:n - j]
    ad, bas = KURGU[surum]["muzik"]
    ham = rd.ses_oku(MUZ(ad))[int(bas * SR):][:n]
    m = np.zeros((n, 2), np.float32)
    m[:len(ham)] = ham
    m *= 0.115 / np.sqrt((m ** 2).mean() + 1e-9)
    zarf = np.clip(rd.kayan(np.abs(konusma).max(axis=1), int(.25 * SR)) / 0.12, 0, 1)
    m *= (1.0 - 0.5 * rd.kayan(zarf, int(.35 * SR)))[:, None]              # seslendirme varken müzik geri çekilir
    a, z = int((.9 if bas == 0 else .35) * SR), int(2.2 * SR)
    m[:a] *= (np.linspace(0, 1, a, dtype=np.float32) ** 1.4)[:, None]
    m[-z:] *= (np.linspace(1, 0, z, dtype=np.float32) ** 1.3)[:, None]
    efekt = np.zeros((n, 2), np.float32)

    def koy(t, v, kazanc):
        j = max(0, int(t * SR))
        v = v[:n - j]
        efekt[j:j + len(v)] += v * kazanc

    koy(.4, rd.vurus(.9), .13)                                               # açılış başlığı
    if "drone" in T:
        koy(T["drone"] + .02, rd.vurus(.8), .11)                             # tamamlanmış proje
    koy(T["final"] - 1.0, rd.vinlama(1.2, 1.0, .25, 180, 2200), .045)        # kapanışa tek, hafif yükseliş
    koy(T["final"] + .02, rd.vurus(1.0), .15)
    miks = konusma + m + efekt
    gec = os.path.join(os.path.dirname(yol), "olcum.wav")
    with wave.open(gec, "wb") as w:
        w.setnchannels(2), w.setsampwidth(2), w.setframerate(SR)
        w.writeframes((np.clip(miks, -1, 1) * 32767).astype(np.int16).tobytes())
    r = subprocess.run(["ffmpeg", "-nostdin", "-i", gec, "-af", "loudnorm=print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
    olcum = json.loads(r[r.rindex("{"):r.rindex("}") + 1])
    kazanc = 10 ** ((-14.0 - float(olcum["input_i"])) / 20)                  # hedef: -14 LUFS
    miks = np.tanh(miks * kazanc * 1.05) * 0.93
    with wave.open(yol, "wb") as w:
        w.setnchannels(2), w.setsampwidth(2), w.setframerate(SR)
        w.writeframes((miks * 32767).astype(np.int16).tobytes())
    print(f"  ses: karışım {float(olcum['input_i']):.1f} LUFS → -14 LUFS")


# ---------------------------------------------------------------- üretim
def main():
    surum = sys.argv[1] if len(sys.argv) > 1 else "45"
    T, SURE, TOPLAM = zaman(surum)
    # Harita zamanlaması: hızlı iniş, ardından çok hafif yaklaşma (ana filmdeki ikinci yaklaşma ve dalış yok).
    t_inis = 0.0
    if "harita" in T:
        d = SURE["harita"]
        t_inis = round(d * .5, 2)
        rd.M0, rd.T_ZOOM, rd.Z1 = T["harita"], t_inis, 12.85
        rd.T_A = rd.T_B = rd.T_HARITA = rd.T_DALIS = d + 5
        rd.olcek = lambda t: 1.0 if t <= t_inis else 1 + .05 * (t - t_inis) / (d - t_inis)
    os.makedirs(OUT, exist_ok=True)
    print(f"  premium {surum} sn · {TOPLAM:.1f} sn · " + " ".join(f"{a}={T[a]:.1f}" for a in T))
    gecici = tempfile.mkdtemp(prefix="reelpremium-")
    hp = os.path.join(gecici, "sayfa.html")
    open(hp, "w", encoding="utf-8").write(html(surum, T, SURE, TOPLAM, t_inis))
    kare = os.path.join(gecici, "kare")
    os.makedirs(kare)
    n = round(TOPLAM * FPS)
    npm = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    yazi = subprocess.Popen(["node", os.path.join(KOK, "reel-kare.cjs"), hp, kare, str(n), str(FPS), str(W), str(H)], env={**os.environ, "NODE_PATH": npm})
    wav = os.path.join(gecici, "ses.wav")
    ses(surum, T, TOPLAM, wav)
    girdi, f, son = zemin(surum, T, TOPLAM, gecici, t_inis)
    if yazi.wait():
        raise SystemExit("yazı kareleri çizilemedi")
    k = len(KURGU[surum]["sahne"])
    f.append(f"[{son}][{k}:v]overlay=0:0:format=auto,format=yuv420p[v]")
    yol = os.path.join(OUT, f"mia-premium-{surum}sn.mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", *girdi, "-framerate", str(FPS), "-i", os.path.join(kare, "k-%04d.png"), "-i", wav,
                    "-filter_complex", ";".join(f), "-map", "[v]", "-map", f"{k + 1}:a", "-t", f"{TOPLAM}",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-maxrate", "10M", "-bufsize", "20M", "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", str(FPS),
                    "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k", yol], check=True)
    print(f"  → {os.path.relpath(yol, ROOT)} · {os.path.getsize(yol) / 1048576:.1f} MB")
    shutil.rmtree(gecici, ignore_errors=True)


if __name__ == "__main__":
    main()
