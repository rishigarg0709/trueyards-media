"""Reel N1: Earth zoom + map pins (Google Maps style UI over real footage)."""
import shutil
from engine import *

WORK = Path("/tmp/fitn1"); shutil.rmtree(WORK, ignore_errors=True); WORK.mkdir()
vo = VO("fitn1", at=0.2)
T = {k: vo.t(p) for k, p in dict(india="India", har="Haryana", roh="Rohtak.", aur="Aur yahaan", fit="Forteasia", acre="Ek sau",
                                   nh="NH", bhi="Rohtak-Bhiwani", plots="Industrial plots", loc="Location").items()}
END_AT = vo.end + 0.25; END_LEN = 3.4; TOTAL = END_AT + END_LEN
sp_earth = (15.2 - 7.4) / max(T["roh"] + 0.2, 1)
S = lambda **k: k
shots = [
    S(at=0.0, src=SRC / "walk_earth_wide.mp4", t=7.4, kind="wide", speed=sp_earth, z0=1.0, z1=1.06, grade="clean"),
    S(at=T["aur"], src=SRC / "walk_ge2.mp4", t=0.6, kind="wide", speed=0.85, z0=1.0, z1=1.25, grade="warm"),
    S(at=T["fit"], src=SRC / "upd_v1.mp4", t=13.2, kind="upd", speed=0.6, z0=1.0, z1=1.1, grade="warm"),
    S(at=T["acre"], src=SRC / "july_v.mp4", t=10.6, kind="v", speed=0.9, z0=1.05, z1=1.16, grade="warm"),
    S(at=T["nh"], src=SRC / "upd_v2.mp4", t=43.3, kind="upd", speed=0.8, z0=1.0, z1=1.1, grade="warm"),
    S(at=T["bhi"], src=SRC / "upd_v2.mp4", t=29.5, kind="upd", speed=0.9, z0=1.02, z1=1.12, grade="warm"),
    S(at=T["plots"], src=SRC / "upd_v2.mp4", t=4.0, kind="upd", speed=0.8, z0=1.0, z1=1.12, grade="warm"),
    S(at=T["loc"], src=SRC / "upd_v2.mp4", t=0.2, kind="upd", speed=0.8, z0=1.05, z1=1.15, grade="warm"),
]
seq = build_frames(WORK, shots, END_AT)

BLUE = (26, 115, 232); GREEN = (24, 128, 56); RED = (234, 67, 53); INK = (32, 33, 36)

def pin(d, x, y, s=1.0, col=RED):
    r = int(34 * s); d.ellipse((x - r, y - 2.6 * r, x + r, y - 0.6 * r), fill=col)
    d.polygon([(x - r * 0.86, y - 1.25 * r), (x + r * 0.86, y - 1.25 * r), (x, y)], fill=col)
    d.ellipse((x - r * 0.38, y - 2.0 * r, x + r * 0.38, y - 1.24 * r), fill=(255, 255, 255))

def big_word(fr, s, p, y=1460, size=170):
    d = ImageDraw.Draw(fr); q = back(p / 0.35); f = F("bk", int(size * (0.7 + 0.3 * q)))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).text((W / 2, y + 8), s, font=f, fill=(0, 0, 0, 150), anchor="mm")
    fr.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    d.text((W / 2, y), s, font=f, fill=(255, 255, 255, int(255 * min(1, p / 0.15))), anchor="mm")

def card(fr, title, sub, p, y=1380, right=None, icon="pin"):
    q = back(p / 0.45); o = int(255 * min(1, p / 0.2))
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    cw, ch = 900, 190; x0 = (W - cw) // 2; yy = y + int((1 - q) * 120)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((x0, yy + 14, x0 + cw, yy + ch + 14), radius=40, fill=(0, 0, 0, 110))
    lay.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16)))
    d.rounded_rectangle((x0, yy, x0 + cw, yy + ch), radius=40, fill=(255, 255, 255, 250))
    cx, cy = x0 + 100, yy + ch // 2
    if icon == "pin":
        pin(d, cx, cy + 46, 1.0)
    else:
        d.ellipse((cx - 56, cy - 56, cx + 56, cy + 56), fill=BLUE)
        d.rounded_rectangle((cx - 32, cy - 10, cx + 32, cy + 20), radius=8, fill="white")
        d.polygon([(cx - 24, cy - 10), (cx - 14, cy - 30), (cx + 14, cy - 30), (cx + 24, cy - 10)], fill="white")
        d.ellipse((cx - 26, cy + 14, cx - 12, cy + 28), fill=BLUE); d.ellipse((cx + 12, cy + 14, cx + 26, cy + 28), fill=BLUE)
    maxw = cw - 185 - (230 if right else 40); fs = 56
    while fs > 30 and d.textlength(title, font=F("xb", fs)) > maxw: fs -= 2
    d.text((x0 + 185, cy - 26), title, font=F("xb", fs), fill=INK, anchor="lm")
    d.text((x0 + 185, cy + 40), sub, font=F("m", 34), fill=(95, 99, 104), anchor="lm")
    if right:
        d.text((x0 + cw - 40, cy - 4), right, font=F("bk", 64), fill=GREEN, anchor="rm")
    a = lay.split()[3].point(lambda v: v * o // 255); lay.putalpha(a); fr.alpha_composite(lay)

def ge_pin(fr, p):
    d = ImageDraw.Draw(fr); q = back(p / 0.5)
    x, y = W // 2, int(960 - 300 * (1 - q))
    for i in range(3):
        r = int(60 + ((p * 1.6 + i / 3) % 1) * 260); a = int(160 * (1 - ((p * 1.6 + i / 3) % 1)))
        d.ellipse((W / 2 - r, 960 - r * 0.45, W / 2 + r, 960 + r * 0.45), outline=(255, 255, 255, a), width=5)
    pin(d, x, y, 2.2)

for i, (k, lt, need, src) in enumerate(seq):
    t = i / FPS; p = lt / need
    fr = Image.open(src).convert("RGBA")
    g = Image.linear_gradient("L").resize((W, 760)); sh = Image.new("RGBA", (W, 760), (0, 0, 0, 170)); sh.putalpha(g.point(lambda v: int(v * 0.75)))
    fr.alpha_composite(sh, (0, H - 760))
    if k <= 1: chip_footage(fr, "MAP VISUAL", dot=BLUE)
    else: chip_footage(fr, "ACTUAL SITE FOOTAGE", dot=(255, 70, 70))
    if k == 0:
        if t < T["india"] - 0.1: big_word(fr, "ZOOM KARKE", t + 0.3, y=1380, size=140); big_word(fr, "DEKHO", t + 0.1, y=1540, size=170)
    elif k == 1:
        ge_pin(fr, p);
        if p > 0.35: card(fr, "FORTEASIA INDUSTRIAL TOWNSHIP", "Kalanaur, Rohtak, Haryana", (p - 0.35) * need)
    elif k == 2: card(fr, "Forteasia Industrial Township", "Main gate  ·  Kalanaur, Rohtak", lt)
    elif k == 3: big_word(fr, "138 ACRES", lt, y=1300, size=190); card(fr, "Industrial township", "Industrial · Residential · Commercial", lt - 0.4, y=1480)
    elif k == 4: card(fr, "NH-152D", "From FIT, by road", lt, icon="car", right="10 min")
    elif k == 5: card(fr, "Rohtak-Bhiwani Hwy", "From FIT, by road", lt, icon="car", right="5 min")
    elif k == 6: big_word(fr, "500 - 4,000", lt, y=1250, size=170); card(fr, "Industrial plots", "Sizes in sq yd", lt - 0.3, y=1420)
    elif k == 7: big_word(fr, "LOCATION", lt, y=1260, size=160); big_word(fr, "PASAND AAYI?", lt - 0.2, y=1430, size=130)
    if k == 0 and t < 0.12:
        fr = Image.blend(fr, Image.new("RGBA", (W, H), (255, 255, 255, 255)), 0.6 * (1 - t / 0.12))
    fr.convert("RGB").save(WORK / f"o_{i:05d}.jpg", quality=92)
n0 = len(seq)
for j in range(int(END_LEN * FPS)):
    end_card(j / FPS, dark=(10, 14, 24), accent=(37, 211, 102), lines=["Industrial plots 500 to 4,000 sq yd"]).convert("RGB").save(WORK / f"o_{n0+j:05d}.jpg", quality=92)
mix_audio(WORK, TOTAL, "fitn1-beat.mp3", 0.42, [("fitn1", vo.at)], WORK / "a.m4a")
encode(WORK, n0, WORK / "a.m4a", "/home/claude/fitn/FIT-N1-earth-zoom.mp4")
print("done", TOTAL, T)
