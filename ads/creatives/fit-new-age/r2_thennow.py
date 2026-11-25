"""Reel N2: Then vs Now. Faded 'PEHLE' farmland, glitch hit on the beat, vivid 'AB' with lime check tags."""
import shutil, random
import numpy as np
from engine import *

WORK = Path("/tmp/fitn2"); shutil.rmtree(WORK, ignore_errors=True); WORK.mkdir()
vo = VO("fitn2", at=0.15)
T = {k: vo.t(p) for k, p in dict(pehle="Pehle", ab="Ab dekhiye", gate="Gate", off="Site office", roads="Roads",
                                   fit="Forteasia", visit="Ek baar").items()}
END_AT = vo.end + 0.3; END_LEN = 3.2; TOTAL = END_AT + END_LEN
LIME = (205, 255, 40); INK = (12, 12, 12)
S = lambda **k: k
mid_roads = T["roads"] + (T["fit"] - T["roads"]) / 2
shots = [
    S(at=0.0, src=SRC / "walk_ge2.mp4", t=0.6, kind="wide", speed=0.75, z0=1.12, z1=1.3, grade="faded"),
    S(at=T["ab"], src=SRC / "upd_v2.mp4", t=4.2, kind="upd", speed=0.9, z0=1.0, z1=1.12, grade="vivid"),
    S(at=T["gate"], src=SRC / "upd_v1.mp4", t=13.2, kind="upd", speed=0.5, z0=1.0, z1=1.1, grade="vivid"),
    S(at=T["off"], src=SRC / "july_v.mp4", t=31.6, kind="v", speed=0.8, z0=1.04, z1=1.14, grade="vivid"),
    S(at=T["roads"], src=SRC / "upd_v2.mp4", t=22.6, kind="upd", speed=1.1, z0=1.0, z1=1.1, grade="vivid"),
    S(at=mid_roads, src=SRC / "upd_v2.mp4", t=8.4, kind="upd", speed=1.0, z0=1.05, z1=1.15, grade="vivid"),
    S(at=T["fit"], src=SRC / "upd_v2.mp4", t=36.2, kind="upd", speed=0.8, z0=1.0, z1=1.12, grade="vivid"),
    S(at=T["visit"], src=SRC / "upd_v1.mp4", t=28.4, kind="upd", speed=0.8, z0=1.05, z1=1.15, grade="vivid"),
]
seq = build_frames(WORK, shots, END_AT)
rng = np.random.default_rng(7)

def grain(fr, amt=26):
    a = np.asarray(fr.convert("RGB")).astype(np.int16)
    n = rng.integers(-amt, amt, a.shape[:2], dtype=np.int16)[..., None]
    return Image.fromarray(np.clip(a + n, 0, 255).astype(np.uint8)).convert("RGBA")

def glitch(fr, s):
    a = np.asarray(fr.convert("RGB")).copy(); off = int(40 * s)
    out = a.copy(); out[..., 0] = np.roll(a[..., 0], off, axis=1); out[..., 2] = np.roll(a[..., 2], -off, axis=1)
    for _ in range(int(10 * s)):
        y = int(rng.integers(0, H - 80)); h = int(rng.integers(20, 90)); dx = int(rng.integers(-120, 120))
        out[y:y + h] = np.roll(out[y:y + h], dx, axis=1)
    return Image.fromarray(out).convert("RGBA")

def mega(fr, s, p, y, size=330, col=(255, 255, 255), outline=False):
    d = ImageDraw.Draw(fr); q = back(min(1, p / 0.3)); f = F("bc", int(size * (1.25 - 0.25 * q)))
    o = int(255 * min(1, p / 0.12))
    if outline: d.text((W / 2, y), s, font=f, fill=(0, 0, 0, 0), stroke_width=6, stroke_fill=col + (o,), anchor="mm")
    else: d.text((W / 2, y), s, font=f, fill=col + (o,), anchor="mm")

def tag(fr, s, p, y, check=True):
    q = back(min(1, p / 0.35)); d = ImageDraw.Draw(fr); f = F("bc", 92)
    tw = d.textlength(s, font=f); w = tw + (150 if check else 80); x0 = (W - w) / 2 - (1 - q) * 500
    d.rounded_rectangle((x0, y, x0 + w, y + 130), radius=24, fill=LIME)
    tx = x0 + 40
    if check:
        cx, cy = x0 + 62, y + 65; d.line([(cx - 24, cy), (cx - 6, cy + 20), (cx + 28, cy - 24)], fill=INK, width=14, joint="curve"); tx = x0 + 110
    d.text((tx, y + 66), s, font=f, fill=INK, anchor="lm")

first_frame = None; last_then = None
for i, (k, lt, need, src) in enumerate(seq):
    t = i / FPS; p = lt / need
    fr = Image.open(src).convert("RGBA")
    if k == 0:
        fr = grain(fr); last_then = fr.copy()
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 90)); fr.alpha_composite(sh)
        chip_footage(fr, "MAP VISUAL · PEHLE", dot=(200, 200, 200))
        mega(fr, "PEHLE", lt, 760, outline=False)
        if t > T["pehle"] + 0.6: mega(fr, "SIRF KHET", lt - 0.6, 1050, size=170, col=(235, 235, 235))
    else:
        g = Image.linear_gradient("L").resize((W, 700)); sh = Image.new("RGBA", (W, 700), (0, 0, 0, 150)); sh.putalpha(g.point(lambda v: int(v * 0.7)))
        fr.alpha_composite(sh, (0, H - 700))
        if k == 1:
            # split screen: top PEHLE (faded freeze), bottom AB (live)
            top = last_then.crop((0, 480, W, 480 + H // 2)); split = min(1, lt / 0.4)
            if lt < 2.2:
                fr.alpha_composite(top.crop((0, 0, int(W * split) if split < 1 else W, H // 2)), (0, 0))
                d = ImageDraw.Draw(fr); d.rectangle((0, H // 2 - 6, W, H // 2 + 6), fill=LIME)
                d.text((60, H // 2 - 40), "PEHLE", font=F("bc", 120), fill=(255, 255, 255), anchor="ls")
                d.rounded_rectangle((50, H // 2 + 30, 250, H // 2 + 170), radius=22, fill=LIME)
                d.text((150, H // 2 + 102), "AB", font=F("bc", 120), fill=INK, anchor="mm")
            else:
                mega(fr, "AB DEKHIYE", lt - 2.2, 1450, size=200, col=LIME)
        elif k == 2: tag(fr, "GATE READY", lt, 1420)
        elif k == 3: tag(fr, "SITE OFFICE LIVE", lt, 1420)
        elif k in (4, 5): tag(fr, "ROADS PE KAAM", lt if k == 4 else 1, 1420);
        elif k == 6:
            mega(fr, "FORTEASIA", lt, 1330, size=150); mega(fr, "INDUSTRIAL TOWNSHIP", lt - 0.15, 1470, size=110, col=LIME)
            mega(fr, "ROHTAK", lt - 0.3, 1590, size=90)
        elif k == 7: mega(fr, "EK BAAR", lt, 1340, size=190); mega(fr, "SITE DEKHIYE", lt - 0.15, 1530, size=170, col=LIME)
        chip_footage(fr, "ACTUAL SITE FOOTAGE · AB", dot=LIME)
        if k == 1 and lt < 0.35: fr = glitch(fr, 1 - lt / 0.35)
        elif lt < 0.12 and k > 1: fr = glitch(fr, 0.5 * (1 - lt / 0.12))
    fr.convert("RGB").save(WORK / f"o_{i:05d}.jpg", quality=92)
n0 = len(seq)
for j in range(int(END_LEN * FPS)):
    end_card(j / FPS, dark=(12, 12, 12), accent=(84, 160, 0), lines=["Pehle khet, ab industrial township"]).convert("RGB").save(WORK / f"o_{n0+j:05d}.jpg", quality=92)
mix_audio(WORK, TOTAL, "fitn2-beat.mp3", 0.5, [("fitn2", vo.at)], WORK / "a.m4a")
encode(WORK, n0, WORK / "a.m4a", "/home/claude/fitn/FIT-N2-then-now.mp4")
print("done", TOTAL, T)
