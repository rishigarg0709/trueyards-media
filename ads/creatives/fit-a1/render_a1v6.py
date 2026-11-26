"""FIT A1 real-footage cut: 'Apni factory ke liye address chahiye?' Premium edit on actual site footage."""
import math, subprocess, os, json, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SRC = "/home/claude/fitn/src/"
M = "/home/claude/trueyards-media/library/media/"
OUT = "/home/claude/a1/"
W, H, FPS = 1080, 1920, 30
ID = "/usr/share/fonts/opentype/inter/"
FB = ID + "InterDisplay-Black.otf"; FXB = ID + "InterDisplay-ExtraBold.otf"; FSB = ID + "Inter-SemiBold.otf"; FM = ID + "Inter-Medium.otf"
def F(p, s): return ImageFont.truetype(p, int(s))
RED = (225, 37, 27); HIL = (255, 64, 52); WHITE = (255, 255, 255); GREEN = (37, 211, 102)
HRERA = ["HRERA-PKL-ROH-653-2025", "HRERA-PKL-ROH-795-2025"]
MUSIC = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].endswith(".mp3") else M + "a1r-beat-1.mp3"

# voice take 1, one long pause tightened
VO = M + "a1v6-vo-tara-2.mp3"
SPD = 1.15
CUT = (999, 999)
def nt(t): return t / SPD
DUR = round(43.31 / SPD + 1.6, 2)
END = nt(36.50)

# crop boxes (fraction of source) to drop letterbox and burned-in subtitle band of the update films
UPD = (0.0, 0.112, 1.0, 0.884)
FULL = (0.0, 0.0, 1.0, 1.0)
# shots: (start, end, file, src_start, speed, crop, zoom0, zoom1)
SHOTS = [
    (0.00, nt(2.03), "upd_v1.mp4", 12.95, 0.60, UPD, 1.00, 1.08),
    (nt(2.03), nt(4.16), "upd_v1.mp4", 28.00, 1.20, UPD, 1.04, 1.00),
    (nt(4.16), nt(7.01), "july_v.mp4", 10.50, 1.00, FULL, 1.00, 1.10),
    (nt(7.01), nt(10.32), "upd_v2.mp4", 3.90, 1.00, UPD, 1.10, 1.00),
    (nt(10.32), nt(13.33), "upd_v2.mp4", 30.50, 1.00, UPD, 1.00, 1.08),
    (nt(13.33), nt(15.25), "upd_v1.mp4", 34.50, 1.00, UPD, 1.00, 1.10),
    (nt(15.25), nt(18.35), "upd_v2.mp4", 22.50, 1.00, UPD, 1.06, 1.00),
    (nt(18.35), nt(22.12), "upd_v2.mp4", 41.80, 1.00, UPD, 1.00, 1.08),
    (nt(22.12), nt(24.40), "july_v.mp4", 31.50, 1.00, FULL, 1.00, 1.08),
    (nt(24.40), nt(26.68), "upd_v2.mp4", 0.40, 1.00, UPD, 1.00, 1.10),
    (nt(26.68), nt(29.48), "upd_v2.mp4", 8.00, 1.30, UPD, 1.00, 1.12),
    (nt(29.48), nt(32.69), "upd_v1.mp4", 40.50, 1.00, UPD, 1.08, 1.00),
    (nt(32.69), nt(34.03), "july_v.mp4", 4.00, 1.00, FULL, 1.06, 1.14),
    (nt(34.03), nt(35.44), "upd_v2.mp4", 36.00, 1.00, UPD, 1.00, 1.08),
    (nt(35.44), END, "upd_v1.mp4", 45.20, 1.00, UPD, 1.00, 1.08),
    (END, DUR, "upd_v1.mp4", 30.00, 0.50, UPD, 1.02, 1.10),
]
GRADE = ("eq=contrast=0.96:saturation=0.98:gamma=1.03:brightness=-0.035,"
         "curves=all='0/0.035 0.25/0.23 0.5/0.47 0.75/0.70 1/0.90',"
         "colorbalance=rs=-0.02:gs=0.0:bs=0.03:rm=-0.01:bm=0.01:rh=0.015:bh=-0.01")

def load_shot(s):
    t0, t1, f, ss, sp, cr, z0, z1 = s
    n = int(round((t1 - t0) * FPS)) + 2
    need = (t1 - t0) * sp + 0.6
    x0, y0, x1, y1 = cr
    crop = f"crop=iw*{x1-x0}:ih*{y1-y0}:iw*{x0}:ih*{y0}"
    vf = f"{crop},scale=-2:1920:flags=lanczos,crop=1080:1920,setpts=PTS/{sp}"
    if sp < 0.8: vf += f",minterpolate=fps=30:mi_mode=blend"
    vf += f",fps=30,{GRADE}"
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(ss), "-t", str(need), "-i", SRC + f, "-vf", vf,
                          "-frames:v", str(n), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    return fr

def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def ease_io(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)

def hblur(a, k):
    if k < 2: return a
    k = int(k); c = np.cumsum(np.pad(a.astype(np.int32), ((0, 0), (k, 0), (0, 0)), mode="edge"), axis=1)
    return ((c[:, k:] - c[:, :-k]) // k).astype(np.uint8)

# --- grain and vignette, precomputed ---
rng = np.random.default_rng(7)
GRAIN = [rng.normal(0, 5.5, (H // 2, W // 2, 1)).repeat(2, 0).repeat(2, 1) for _ in range(6)]
yy, xx = np.mgrid[0:H, 0:W]
VIG = (1 - 0.24 * (((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.62)) ** 2)).clip(0.55, 1)[..., None]

# --- words: (text, start, end, line, highlight) on the new timeline ---
def P(words, lines):
    out = []
    for (w, s, e, hl), ln in zip(words, lines): out.append((w, nt(s), nt(e), ln, hl))
    return out
PHRASES = [
    (0.0, 2.70, P([("Apni", 0.0, .24, 0), ("factory", .29, .64, 0), ("ke", .68, .8, 0), ("liye", .84, .96, 0),
                   ("address", 1.01, 1.36, 1), ("chahiye?", 1.44, 2.28, 0)], [0, 0, 0, 0, 1, 1])),
    (2.77, 3.75, P([("Toh", 2.77, 2.8, 0), ("yeh", 2.86, 2.96, 0), ("dekhiye!", 3.0, 3.64, 1)], [0, 0, 0])),
    (3.78, 7.40, P([("Rohtak", 3.78, 4.24, 0), ("mein", 4.28, 4.48, 0), ("138 acre", 4.67, 6.08, 1), ("ka", 6.12, 6.24, 0),
                    ("industrial", 6.3, 6.88, 0), ("park", 6.95, 7.28, 0)], [0, 0, 1, 1, 2, 2])),
    (7.52, 10.10, P([("500", 7.52, 7.92, 0), ("se", 8.16, 8.4, 0), ("4,000 gaj", 8.44, 9.28, 1), ("tak", 9.31, 9.36, 0),
                     ("ke", 9.4, 9.52, 0), ("plots", 9.6, 10.08, 0)], [0, 0, 0, 1, 1, 1])),
    (10.17, 12.05, P([("Highway", 10.17, 10.8, 0), ("sirf", 10.88, 11.12, 0), ("10 minute", 11.2, 12.0, 1)], [0, 0, 1])),
    (12.12, 14.40, P([("Maal", 12.12, 12.4, 0), ("aana", 12.48, 12.72, 0), ("jaana...", 12.8, 13.2, 0), ("fast!", 13.35, 14.36, 1)], [0, 0, 0, 1])),
    (14.47, 15.55, P([("Apna", 14.47, 15.0, 0), ("gate.", 15.04, 15.52, 1)], [0, 1])),
    (15.60, 16.65, P([("Apna", 15.6, 16.04, 0), ("board.", 16.08, 16.6, 1)], [0, 1])),
    (16.69, 17.85, P([("Apna", 16.69, 17.28, 0), ("address.", 17.32, 17.68, 1)], [0, 1])),
]

FONT = F(FB, 104)
def draw_phrase(fr, t, ph):
    p0, p1, words = ph
    p1 = nt(p1) if p1 > CUT[0] else p1
    out_a = 1.0 if t < p1 - 0.10 else max(0.0, (p1 - t) / 0.10)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    lines = {}
    for w in words: lines.setdefault(w[3], []).append(w)
    gap = 22; size = 104
    while True:
        fnt = F(FB, size)
        wmax = max(sum(d.textlength(w[0], font=fnt) + (44 if w[4] else 0) for w in ws) + gap * (len(ws) - 1) for ws in lines.values())
        if wmax <= 900 or size <= 70: break
        size -= 4
    lh = int(size * 1.23); n = len(lines); y0 = int(H * 0.69 - n * lh / 2)
    for li, (ln, ws) in enumerate(sorted(lines.items())):
        widths = [d.textlength(w[0], font=fnt) + (44 if w[4] else 0) for w in ws]
        x = (W - (sum(widths) + gap * (len(ws) - 1))) / 2; y = y0 + li * lh
        for w, wd in zip(ws, widths):
            a = ease((t - w[1] + 0.06) / 0.14) * out_a
            if a <= 0: x += wd + gap; continue
            dy = int(18 * (1 - ease((t - w[1] + 0.06) / 0.18)))
            al = int(255 * a)
            if w[4]:
                d.rounded_rectangle((x, y - int(size*.06) + dy, x + wd, y + int(size*1.08) + dy), radius=18, fill=RED + (al,))
                d.text((x + 22, y + int(size*.5) + dy), w[0], font=fnt, fill=WHITE + (al,), anchor="lm")
            else:
                d.text((x, y + int(size*.5) + dy), w[0], font=fnt, fill=WHITE + (al,), anchor="lm")
            x += wd + gap
    sh = layer.split()[3].filter(ImageFilter.GaussianBlur(22)).point(lambda v: int(v * 0.6))
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); shadow.putalpha(sh)
    fr.alpha_composite(shadow, (0, 10)); fr.alpha_composite(layer)


# big full-screen captions: one chunk at a time (Rishi 26 Nov 22:53)
CHUNKS_RAW = [
 ("Apni",0.0,0),("factory",.29,0),("ke liye",.67,0),("address",.92,1),("chahiye?",1.23,0),(None,1.95,0),
 ("Toh yeh",2.03,0),("dekhiye!",2.38,1),(None,3.2,0),
 ("Rohtak",3.32,0),("mein",3.73,0),("138",4.16,1),("acre",5.09,1),("industrial",5.57,0),("park",6.16,0),(None,6.9,0),
 ("Plots",7.01,0),("400",7.84,1),("se",8.29,0),("4,000",8.56,1),("gaj tak",9.2,0),(None,10.2,0),
 ("24 metre",10.32,1),("wide",11.02,0),("roads",11.35,0),("trucks",11.97,0),("ke liye",12.29,0),(None,13.2,0),
 ("Apna",13.33,0),("electrical",13.57,0),("substation",14.16,1),("STP",15.25,1),("CCTV",15.98,1),("aur",16.94,0),("fire safety",17.18,1),(None,18.25,0),
 ("NH-152D",18.35,1),("se sirf",20.08,0),("10 minute",20.8,1),("door",21.32,0),(None,22.0,0),
 ("Haryana",22.12,0),("MSME",22.88,1),("policy",23.42,0),("mein...",23.81,0),("25%",24.4,1),("capital",25.26,0),("subsidy!",25.91,1),(None,26.6,0),
 ("Stamp duty",26.68,0),("pe",27.6,0),("75%",27.84,1),("subsidy",28.78,1),(None,29.4,0),
 ("SGST",29.97,0),("pe",30.61,0),("60%",30.88,1),("tak",31.72,0),("subsidy!",31.9,1),(None,32.6,0),
 ("Apna",32.69,0),("gate.",33.5,1),("Apna",34.03,0),("board.",34.61,1),("Apna",35.44,0),("address.",35.75,1),(None,36.5,0),
]
CHUNKS = []
for i,(w,s0,h) in enumerate(CHUNKS_RAW):
    if w is None: continue
    CHUNKS.append((w.upper(), nt(s0), nt(CHUNKS_RAW[i+1][1]), h))
FCACHE = {}
def bigfont(sz):
    if sz not in FCACHE: FCACHE[sz] = F(FB, sz)
    return FCACHE[sz]
def draw_big(fr, t):
    c = None
    for ch in CHUNKS:
        if ch[1] <= t < ch[2]: c = ch; break
    if c is None: return
    w, t0, t1, hl = c
    # gentle darken behind the word for legibility
    fr.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 85)))
    d = ImageDraw.Draw(fr)
    sz = 340
    while sz > 120 and d.textlength(w, font=bigfont(sz)) > 960: sz -= 10
    f = bigfont(sz)
    age = t - t0
    sc = 1 + 0.22 * (1 - ease(age / 0.14))
    f2 = bigfont(max(60, int(sz * sc)))
    tw = d.textlength(w, font=f2)
    cy = int(H * 0.52)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
    ld.text((W / 2, cy), w, font=f2, fill=(HIL if hl else WHITE) + (255,), anchor="mm")
    sh = layer.split()[3].filter(ImageFilter.GaussianBlur(26)).point(lambda v: int(min(255, v * 0.8)))
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); shadow.putalpha(sh)
    fr.alpha_composite(shadow, (0, 14)); fr.alpha_composite(layer)

LOGO = None
def logo(width):
    global LOGO
    if LOGO is None:
        lg = Image.open("/home/claude/trueyards-media/ads/creatives/fit-c/logo_crop.png").convert("RGB")
        a = np.asarray(lg).astype(float).max(axis=2)
        LOGO = lg.copy(); LOGO.putalpha(Image.fromarray(np.clip((a - 40) * 1.6, 0, 255).astype("uint8")))
    return LOGO.resize((width, int(width * LOGO.height / LOGO.width)), Image.LANCZOS)

def glass(fr, box, r, alpha=110):
    x0, y0, x1, y1 = [int(v) for v in box]
    reg = fr.crop((x0, y0, x1, y1)).filter(ImageFilter.GaussianBlur(14))
    m = Image.new("L", reg.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, reg.width - 1, reg.height - 1), radius=r, fill=255)
    fr.paste(reg, (x0, y0), m)
    ov = Image.new("RGBA", fr.size, (0, 0, 0, 0))
    ImageDraw.Draw(ov).rounded_rectangle(box, radius=r, fill=(10, 12, 16, alpha), outline=(255, 255, 255, 60), width=2)
    fr.alpha_composite(ov)

def chrome(fr, t):
    d = ImageDraw.Draw(fr); f = F(FSB, 22)
    lab = "ACTUAL SITE FOOTAGE"; w = d.textlength(lab, font=f) + 64
    glass(fr, (36, 54, 36 + w, 98), 22, 90)
    d = ImageDraw.Draw(fr)
    a = 0.6 + 0.4 * (math.sin(t * 5) + 1) / 2
    d.ellipse((54, 68, 68, 82), fill=(255, 59, 48, int(255 * a)))
    d.text((80, 76), lab, font=f, fill=WHITE, anchor="lm")
    f2 = F(FM, 20)
    for i, s in enumerate(HRERA):
        d.text((W - 40, 58 + i * 26), s, font=f2, fill=(255, 255, 255, 225), anchor="ra")

def end_card(fr, t):
    p = ease((t - END) / 0.6)
    dark = Image.new("RGBA", (W, H), (6, 8, 12, int(150 * p))); fr.alpha_composite(dark)
    d = ImageDraw.Draw(fr)
    lg = logo(360); lgw = lg.copy(); lgw.putalpha(lg.split()[3].point(lambda v: int(v * p)))
    fr.alpha_composite(lgw, ((W - lg.width) // 2, int(330 - 30 * (1 - p))))
    q = ease((t - END - 0.25) / 0.5)
    f = F(FB, 112)
    for i, (s, hl) in enumerate([("Apni factory", False), ("ka address.", False)]):
        y = 720 + i * 135 + int(24 * (1 - q))
        if hl:
            wd = d.textlength(s, font=f) + 48
            d.rounded_rectangle(((W - wd) / 2, y - 64, (W + wd) / 2, y + 62), radius=20, fill=RED + (int(255 * q),))
        d.text((W / 2, y), s, font=f, fill=WHITE + (int(255 * q),), anchor="mm")
    r = ease((t - END - 0.6) / 0.5)
    d.text((W / 2, 1000), "Forteasia Industrial Township", font=F(FXB, 50), fill=WHITE + (int(255 * r),), anchor="mm")
    d.text((W / 2, 1060), "Kalanaur  ·  Rohtak  ·  Haryana", font=F(FM, 34), fill=(225, 228, 235, int(235 * r)), anchor="mm")
    c = ease((t - nt(39.68)) / 0.45); pulse = 1 + 0.03 * math.sin(t * 6)
    bw, bh = int(700 * pulse), int(128 * pulse); bx, by = (W - bw) // 2, 1190
    if c > 0:
        glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(glow).rounded_rectangle((bx - 10, by - 10, bx + bw + 10, by + bh + 10), radius=74, fill=GREEN + (int(120 * c),))
        fr.alpha_composite(glow.filter(ImageFilter.GaussianBlur(26)))
        d = ImageDraw.Draw(fr)
        d.rounded_rectangle((bx, by, bx + bw, by + bh), radius=64, fill=GREEN + (int(255 * c),))
        d.text((W / 2, by + bh / 2), "Is WhatsApp button pe click karein", font=F(FXB, 40), fill=WHITE + (int(255 * c),), anchor="mm")
        for i in range(3):
            a = (math.sin(t * 6 - i * 0.9) + 1) / 2; y = 1370 + i * 40
            d.line((W / 2 - 30, y, W / 2, y + 26, W / 2 + 30, y), fill=(255, 255, 255, int(220 * a * c)), width=8, joint="curve")
    f3 = F(FSB, 28)
    for i, s in enumerate(HRERA):
        d.text((W / 2, 1600 + i * 40), s, font=f3, fill=(255, 255, 255, int(235 * p)), anchor="mm")
    d.text((W / 2, 1685), "Verify at haryanarera.gov.in", font=F(FM, 24), fill=(220, 220, 228, int(220 * p)), anchor="mm")

CACHE = {}
def shot_at(t):
    for i, s in enumerate(SHOTS):
        if s[0] <= t < s[1] or (i == len(SHOTS) - 1 and t >= s[0]): return i, s

def base_frame(t, i, s):
    if i not in CACHE:
        for k in list(CACHE):
            if k < i - 1: del CACHE[k]
        CACHE[i] = load_shot(s)
    fr = CACHE[i]; k = min(len(fr) - 1, int((t - s[0]) * FPS))
    a = fr[k]
    # slow push
    p = ease_io((t - s[0]) / (s[1] - s[0])); z = s[6] + (s[7] - s[6]) * p
    if abs(z - 1) > 0.002:
        cw, ch = W / z, H / z
        im = Image.fromarray(a).resize((W, H), Image.BICUBIC, box=((W - cw) / 2, (H - ch) / 2, (W + cw) / 2, (H + ch) / 2))
        a = np.asarray(im)
    # whip transition: blur and shift at the start and end of shots (not the first, not into the end card)
    win = 0.16
    into = t - s[0]; outof = s[1] - t
    if i > 0 and into < win and s[0] != END:
        q = 1 - into / win; a = np.roll(hblur(a, 6 + 90 * q), int(-260 * q * q), axis=1)
    elif i < len(SHOTS) - 1 and outof < win and SHOTS[i + 1][0] != END:
        q = 1 - outof / win; a = np.roll(hblur(a, 6 + 90 * q), int(260 * q * q), axis=1)
    return a

def frame(t, fi):
    i, s = shot_at(t)
    a = base_frame(t, i, s).astype(np.float32)
    a = a * VIG + GRAIN[fi % 6]
    fr = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
    if t < END:
        draw_big(fr, t)
        if nt(22.12) <= t < nt(32.6):
            ImageDraw.Draw(fr).text((W / 2, 1500), "*Subject to eligibility, as per Haryana MSME Policy 2026", font=F(FM, 28), fill=(255, 255, 255, 230), anchor="mm")
    else:
        end_card(fr, t)
    chrome(fr, t)
    return fr.convert("RGB")

def audio():
    fc = [f"[0:a]atempo={SPD},volume=1.7,apad=whole_dur={DUR},asplit=2[vo][vo2]",
          "[1:a]atrim=0.23:29.9,asetpts=PTS-STARTPTS[m1]", "[2:a]atrim=2.9:24,asetpts=PTS-STARTPTS[m2]",
          f"[m1][m2]acrossfade=d=0.8:c1=tri:c2=tri,atrim=0:{DUR},volume=0.36,afade=t=out:st={DUR-1.5}:d=1.5[mu]",
          "[mu][vo]sidechaincompress=threshold=0.04:ratio=5:attack=15:release=280[duck]",
          "[duck][vo2]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]"]
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", VO, "-i", MUSIC, "-i", MUSIC, "-filter_complex", ";".join(fc), "-map", "[a]",
                    "-t", str(DUR), "-ar", "48000", OUT + "a1v6_audio.wav"], check=True)
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", OUT + "a1v6_audio.wav"]))
    assert d >= DUR - 0.05, f"audio too short: {d}"

def render(name):
    audio()
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", OUT + "a1v6_audio.wav", "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "192k", "-t", str(DUR), "-movflags", "+faststart", OUT + name], stdin=subprocess.PIPE)
    for fi in range(int(DUR * FPS)):
        try: p.stdin.write(frame(fi / FPS, fi).tobytes())
        except BrokenPipeError: break
    p.stdin.close(); p.wait()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "prev":
        for t in [float(x) for x in sys.argv[2:]]:
            frame(t, 0).save(OUT + f"r_{t:05.2f}.jpg", quality=90)
    else:
        render(sys.argv[2] if len(sys.argv) > 2 else "FIT-A1-real.mp4")
