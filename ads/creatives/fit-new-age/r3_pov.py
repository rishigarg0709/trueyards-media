"""Reel N3: POV meme caption style. No VO, beat-cut drone, word-by-word TikTok captions, punch zoom on every beat."""
import shutil
from engine import *

WORK = Path("/tmp/fitn3"); shutil.rmtree(WORK, ignore_errors=True); WORK.mkdir()
B = 60 / 110; INTRO = 4 * B; PER = 3 * B
S = lambda **k: k
plan = [
    (SRC / "upd_v1.mp4", 28.4, "upd", None),
    (SRC / "july_v.mp4", 10.6, "v", "138 acre ka township"),
    (SRC / "upd_v2.mp4", 4.2, "upd", "Plots 500 se 4,000 sq yd"),
    (SRC / "upd_v2.mp4", 22.6, "upd", "Chaudi roads, trucks ke liye"),
    (SRC / "july_v.mp4", 31.6, "v", "Site office already ready"),
    (SRC / "upd_v1.mp4", 13.1, "upd", "Gate bhi khada hai"),
    (SRC / "upd_v2.mp4", 8.4, "upd", "JCB on, kaam chalu"),
    (SRC / "upd_v2.mp4", 36.2, "upd", "HRERA registered"),
    (SRC / "upd_v2.mp4", 0.2, "upd", "Ab bas site visit baaki hai"),
]
shots = []; caps = []
at = 0.0
for n, (src, t0, kind, cap) in enumerate(plan):
    shots.append(S(at=at, src=src, t=t0, kind=kind, speed=0.5 if n == 5 else (1.25 if n % 2 else 0.8), z0=1.0, z1=1.08, grade="clean"))
    caps.append((at, cap)); at += INTRO if n == 0 else PER
END_AT = at; END_LEN = 3.8; TOTAL = END_AT + END_LEN
seq = build_frames(WORK, shots, END_AT)

def wrap(words, f, d, maxw):
    lines, cur = [], []
    for w in words:
        if cur and d.textlength(" ".join(cur + [w]), font=f) > maxw: lines.append(cur); cur = [w]
        else: cur.append(w)
    lines.append(cur); return lines

def caption(fr, text, lt, y, size=78, per_word=0.11, box=False):
    d = ImageDraw.Draw(fr); f = F("xb", size); words = text.split()
    shown = max(1, min(len(words), int(lt / per_word) + 1))
    lines = wrap(words, f, d, W - 160); idx = 0; lh = int(size * 1.22)
    yy = y - lh * len(lines) / 2
    for ln in lines:
        full = " ".join(ln); x = (W - d.textlength(full, font=f)) / 2
        for w in ln:
            if idx < shown:
                age = lt - idx * per_word; sc = 1 + 0.25 * max(0, 1 - age / 0.1)
                fw = F("xb", int(size * sc))
                d.text((x + d.textlength(w, font=f) / 2, yy + lh / 2), w, font=fw, fill="white", stroke_width=7, stroke_fill="black", anchor="mm")
            x += d.textlength(w + " ", font=f); idx += 1
        yy += lh

def punch(fr, t):
    ph = (t % B) / B; z = 1 + 0.045 * max(0, 1 - ph / 0.35)
    if z <= 1.001: return fr
    w, h = int(W / z), int(H / z)
    return fr.crop(((W - w) // 2, (H - h) // 2, (W - w) // 2 + w, (H - h) // 2 + h)).resize((W, H), Image.BILINEAR)

for i, (k, lt, need, src) in enumerate(seq):
    t = i / FPS
    fr = Image.open(src).convert("RGBA")
    if t >= 2.0: fr = punch(fr, t - 2.0)
    chip_footage(fr, "ACTUAL SITE FOOTAGE")
    if k == 0:
        caption(fr, "POV: aapko NH-152D se sirf 10 min par industrial plot mil gaya", lt, 520, size=74, per_word=0.13)
    else:
        caption(fr, caps[k][1], lt, 1380, size=92, per_word=0.09)
    if k > 0 and lt < 0.07:
        fr = Image.blend(fr, Image.new("RGBA", (W, H), (255, 255, 255, 255)), 0.5 * (1 - lt / 0.07))
    fr.convert("RGB").save(WORK / f"o_{i:05d}.jpg", quality=92)
n0 = len(seq)
for j in range(int(END_LEN * FPS)):
    fr = end_card(j / FPS, dark=(14, 14, 16), accent=(37, 180, 90), lines=["Comment nahi, WhatsApp karo"])
    fr.convert("RGB").save(WORK / f"o_{n0+j:05d}.jpg", quality=92)
mix_audio(WORK, TOTAL, "fitn3-beat.mp3", 0.9, [], WORK / "a.m4a")
encode(WORK, n0, WORK / "a.m4a", "/home/claude/fitn/FIT-N3-pov.mp4")
print("done", TOTAL)
