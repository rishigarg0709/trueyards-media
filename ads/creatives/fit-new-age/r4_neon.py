"""Reel N4: Neon map overlay on drone. Dark teal grade, glowing cyan roads and magenta plot outlines traced live, HUD labels."""
import shutil
import numpy as np
from engine import *

WORK = Path("/tmp/fitn4"); shutil.rmtree(WORK, ignore_errors=True); WORK.mkdir()
vo = VO("fitn4", at=0.3)
T = {k: vo.t(p) for k, p in dict(grid="Ye hai", acre="Ek sau", roads="Trucks", util="Bijli", nh="NH", fit="Forteasia", fut="Future").items()}
END_AT = vo.end + 0.3; END_LEN = 3.4; TOTAL = END_AT + END_LEN
CY = (0, 240, 255); MG = (255, 40, 200); WH = (230, 250, 255)
S = lambda **k: k
shots = [
    S(at=0.0, still=True), S(at=T["acre"], src=SRC / "july_v.mp4", t=10.6, kind="v", speed=0.9, z0=1.05, z1=1.15, grade="neon"),
    S(at=T["roads"], still=True), S(at=T["util"], still=True),
    S(at=T["nh"], src=SRC / "upd_v2.mp4", t=43.2, kind="upd", speed=0.75, z0=1.0, z1=1.1, grade="neon"),
    S(at=T["fit"], src=SRC / "upd_v2.mp4", t=36.2, kind="upd", speed=0.8, z0=1.0, z1=1.1, grade="neon"),
    S(at=T["fut"], src=SRC / "upd_v2.mp4", t=0.2, kind="upd", speed=0.8, z0=1.05, z1=1.15, grade="neon"),
]
seq = build_frames(WORK, shots, END_AT)

def neon_grade(path):
    a = np.asarray(Image.open(path).convert("RGB")).astype(np.float32) / 255
    l = a.mean(axis=2, keepdims=True); a = l + (a - l) * 0.5
    a = np.clip((a - 0.5) * 1.25 + 0.5 - 0.18, 0, 1) ** 1.15
    a = a * np.array([0.78, 1.0, 1.18]); return Image.fromarray(np.clip(a * 255, 0, 255).astype(np.uint8)).convert("RGBA")
ST5 = neon_grade("st/u2_5_t.png"); ST0 = neon_grade("st/u2_0_t.png")
ROADS = [((600, 390), (40, 1280)), ((330, 920), (1080, 920)), ((1050, 480), (1050, 910)), ((0, 1680), (1080, 1680))]
PLOTS = [[(590, 470), (990, 470), (1000, 860), (470, 860)], [(240, 980), (820, 980), (820, 1590), (90, 1590)]]

def part(a, b, p):
    return (a[0] + (b[0] - a[0]) * p, a[1] + (b[1] - a[1]) * p)

def poly_part(pts, p):
    pts = pts + [pts[0]]; segs = list(zip(pts[:-1], pts[1:])); L = [np.hypot(b[0] - a[0], b[1] - a[1]) for a, b in segs]
    tot = sum(L) * min(1, max(0, p)); out = [pts[0]]
    for (a, b), l in zip(segs, L):
        if tot <= 0: break
        f = min(1, tot / l); out.append(part(a, b, f)); tot -= l
    return out

def hud(fr, t):
    d = ImageDraw.Draw(fr); c = CY + (200,)
    for (x, y, sx, sy) in ((50, 190, 1, 1), (W - 50, 190, -1, 1), (50, H - 170, 1, -1), (W - 50, H - 170, -1, -1)):
        d.line([(x, y + 70 * sy), (x, y), (x + 70 * sx, y)], fill=c, width=5)
    d.text((70, 230), f"REC  {t:05.2f}", font=F("mono", 28), fill=c)
    d.text((W - 70, 230), "KALANAUR // ROHTAK", font=F("mono", 28), fill=c, anchor="ra")
    if int(t * 2) % 2 == 0: d.ellipse((52 + 0, 236, 64, 248), fill=(255, 50, 80))

def scan(fr):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for y in range(0, H, 6): d.line([(0, y), (W, y)], fill=(0, 0, 0, 38))
    fr.alpha_composite(lay)

def label(fr, s, x, y, lt, col=CY, size=46, anchor="lm"):
    n = int(len(s) * min(1, lt / 0.5)); txt = s[:n] + ("_" if n < len(s) and int(lt * 10) % 2 == 0 else "")
    f = F("mono", size); d = ImageDraw.Draw(fr)
    if n == 0: return
    bb = d.textbbox((x, y), s[:n] or " ", font=f, anchor=anchor)
    d.rectangle((bb[0] - 18, bb[1] - 14, bb[2] + 18, bb[3] + 14), fill=(0, 10, 20, 190), outline=col + (255,), width=3)
    fr.alpha_composite(glow_layer(lambda dd: dd.text((x, y), txt, font=f, fill=col, anchor=anchor), radius=8, strength=1))

def big(fr, s, y, lt, col=WH, size=150):
    o = min(1, lt / 0.2); f = F("bc", size)
    fr.alpha_composite(glow_layer(lambda dd: dd.text((W / 2, y), s, font=f, fill=col + (int(255 * o),), anchor="mm"), radius=18, strength=2))

def draw_roads(p, pulse=None):
    def fn(d):
        for k, (a, b) in enumerate(ROADS):
            q = min(1, max(0, p * 1.6 - k * 0.2))
            if q > 0: d.line([a, part(a, b, q)], fill=CY + (255,), width=10)
            if pulse is not None and q >= 1:
                c = part(a, b, (pulse + k * 0.27) % 1); d.ellipse((c[0] - 18, c[1] - 18, c[0] + 18, c[1] + 18), fill=WH + (255,))
    return glow_layer(fn, radius=16, strength=3)

def draw_plots(p):
    def fn(d):
        for k, pts in enumerate(PLOTS):
            q = min(1, max(0, p * 1.4 - k * 0.3)); pp = poly_part(pts, q)
            if len(pp) > 1: d.line(pp, fill=MG + (255,), width=9, joint="curve")
            if q >= 1: d.polygon(pts, fill=MG + (45,))
    return glow_layer(fn, radius=16, strength=3)

for i, (k, lt, need, src) in enumerate(seq):
    t = i / FPS; p = lt / need
    if k == 0:
        base = ST5.copy(); base.alpha_composite(draw_roads(p)); fr = kb(base, p, 1.0, 1.08)
        hud(fr, t); label(fr, "ROHTAK // NEW INDUSTRIAL GRID", 80, 1450, lt, size=42)
        big(fr, "YE HAI", 1300, lt, size=110)
    elif k == 2:
        base = ST5.copy(); base.alpha_composite(draw_roads(1, pulse=lt * 0.6)); base.alpha_composite(draw_plots(p)); fr = kb(base, p, 1.04, 1.12, 0.4, 0.5)
        hud(fr, t); label(fr, "INTERNAL ROADS // TRUCK READY", 80, 1760, lt, size=40)
    elif k == 3:
        base = ST0.copy()
        def fn(d, lt=lt):
            q = min(1, lt / 0.8); d.line([(0, 660), part((0, 660), (900, 350), q)], fill=CY + (255,), width=10)
            r = 26 + 10 * abs(np.sin(lt * 6)); d.ellipse((680 - r, 600 - r, 680 + r, 600 + r), outline=MG + (255,), width=7)
            d.ellipse((668, 588, 692, 612), fill=MG + (255,))
        base.alpha_composite(glow_layer(fn, radius=14, strength=3)); fr = kb(base, p, 1.0, 1.08, 0.6, 0.35)
        hud(fr, t); label(fr, "SITE OFFICE", 720, 600, lt, col=MG, size=36)
        for j, s in enumerate(("POWER", "WATER", "DRAINAGE")):
            label(fr, f"[{'#' if lt > 0.3 + j * 0.35 else ' '}] {s}", 80, 1300 + j * 110, lt - j * 0.3, size=44)
        if lt > 1.3: big(fr, "SAB PLANNED", 1700, lt - 1.3, col=CY, size=120)
    else:
        fr = Image.open(src).convert("RGBA"); hud(fr, t)
        if k == 1: big(fr, "138", 1180, lt, col=CY, size=330); big(fr, "ACRES", 1400, lt - 0.15, size=130)
        elif k == 4:
            label(fr, "NH-152D", 80, 1330, lt, size=56); w = int(900 * ease(lt / 1.2)); d = ImageDraw.Draw(fr)
            fr.alpha_composite(glow_layer(lambda dd: dd.line([(90, 1450), (90 + w, 1450)], fill=CY + (255,), width=8), radius=10))
            big(fr, "10 MIN", 1600, lt - 0.4, col=CY, size=180)
        elif k == 5: big(fr, "FORTEASIA", 1330, lt, size=150); big(fr, "INDUSTRIAL TOWNSHIP", 1470, lt - 0.15, col=CY, size=104)
        elif k == 6: big(fr, "FUTURE", 1330, lt, col=MG, size=200); big(fr, "YAHIN BAN RAHA HAI", 1500, lt - 0.2, size=104)
    chip_footage(fr, "ACTUAL SITE FOOTAGE · NEON OVERLAY", dot=CY)
    scan(fr)
    if lt < 0.1: fr = Image.blend(fr, Image.new("RGBA", (W, H), (0, 255, 255, 255)), 0.35 * (1 - lt / 0.1))
    fr.convert("RGB").save(WORK / f"o_{i:05d}.jpg", quality=92)
n0 = len(seq)
for j in range(int(END_LEN * FPS)):
    end_card(j / FPS, dark=(2, 10, 18), accent=(0, 170, 200), lines=["Rohtak ka naya industrial grid"]).convert("RGB").save(WORK / f"o_{n0+j:05d}.jpg", quality=92)
mix_audio(WORK, TOTAL, "fitn4-beat.mp3", 0.45, [("fitn4", vo.at)], WORK / "a.m4a")
encode(WORK, n0, WORK / "a.m4a", "/home/claude/fitn/FIT-N4-neon.mp4")
print("done", TOTAL, T)
