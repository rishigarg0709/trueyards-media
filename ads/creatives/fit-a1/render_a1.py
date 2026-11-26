"""FIT A1 'Apni factory ka address' reel: Gemini stills, Tara Hinglish VO, punchy big text, beat."""
import math, subprocess, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

M = "/home/claude/trueyards-media/library/media/"
OUT = "/home/claude/a1/"
W, H, FPS = 1080, 1920, 30
FB = "/root/.fonts/BarlowCondensed-ExtraBold.ttf"
FS = "/root/.fonts/BarlowCondensed-SemiBold.ttf"
INTER = "/usr/share/fonts/opentype/inter/"
def F(p, s): return ImageFont.truetype(p, s)
YEL = (255, 197, 49); WHITE = (255, 255, 255); GREEN = (37, 211, 102)
HRERA = ["HRERA-PKL-ROH-653-2025", "HRERA-PKL-ROH-795-2025"]

# --- audio: tighten the two pauses in take 1 ---
VO = M + "a1-vo-tara-1.mp3"
SEG = [(0.0, 1.60), (3.15, 17.20), (18.30, 25.90)]
SH = [0.0, 1.60 - 3.15, 1.60 + 14.05 - 18.30]  # time shifts
def nt(t_old):
    for (a, b), s in zip(SEG, SH):
        if a <= t_old <= b + 0.01: return t_old + s
    return t_old
DUR = 25.0

def ease(x): x = max(0, min(1, x)); return 1 - (1 - x) ** 3

IM = {}
def still(name):
    if name not in IM:
        IM[name] = Image.open(M + f"{name}-4k.jpg").convert("RGB")
    return IM[name]

def kb(name, t, t0, t1, z0=1.0, z1=1.12, dx=0.0, dy=0.0, shake=0.0):
    """Ken Burns crop from the 4K still. dx, dy in fraction of width/height over the shot."""
    im = still(name); iw, ih = im.size
    p = (t - t0) / max(1e-6, (t1 - t0)); p = max(0, min(1, p))
    z = z0 + (z1 - z0) * (p * p * (3 - 2 * p))
    cw, ch = iw / z, iw / z * H / W
    if ch > ih: ch = ih; cw = ih * W / H / 1
    cx = iw / 2 + dx * iw * (p - 0.5); cy = ih / 2 + dy * ih * (p - 0.5)
    if shake:
        cx += shake * math.sin(t * 53) * iw * 0.004; cy += shake * math.cos(t * 47) * ih * 0.004
    cx = min(max(cx, cw / 2), iw - cw / 2); cy = min(max(cy, ch / 2), ih - ch / 2)
    box = (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)
    return im.resize((W, H), Image.BILINEAR, box=box)

# shots on the new timeline: (start, end, still, z0, z1, dx, dy)
SHOTS = [
    (0.00, 1.65, "a1-01-board", 1.18, 1.05, 0, 0.00),
    (1.65, 4.30, "a1-02-reveal", 1.35, 1.00, 0, 0.04),
    (4.30, 6.25, "a1-03-road", 1.00, 1.22, 0, -0.03),
    (6.25, 8.85, "a1-04-topdown", 1.25, 1.05, 0.03, 0.0),
    (8.85, 10.65, "a1-06-highway", 1.05, 1.25, 0, -0.04),
    (10.65, 12.50, "a1-05-truck", 1.00, 1.20, 0, 0.02),
    (12.50, 13.62, "a1-07-gate", 1.10, 1.22, 0, 0),
    (13.62, 14.32, "a1-01-board", 1.20, 1.32, 0, 0),
    (14.32, 15.65, "a1-07-gate", 1.25, 1.45, 0, -0.02),
    (15.65, DUR, "a1-08-endcard", 1.00, 1.10, 0, 0),
]

# captions: (start, end, lines, highlight words)  big punchy text
CAPS = [
    (0.05, 1.62, ["APNI FACTORY", "KA ADDRESS", "CHAHIYE?"], {"ADDRESS"}),
    (1.68, 2.70, ["TOH YEH", "DEKHIYE!"], {"DEKHIYE!"}),
    (2.72, 3.55, ["ROHTAK"], {"ROHTAK"}),
    (3.55, 6.20, ["138 ACRE", "INDUSTRIAL", "PARK"], {"138", "ACRE"}),
    (6.30, 8.82, ["PLOTS", "500 SE", "4,000 GAJ"], {"500", "4,000"}),
    (8.86, 10.62, ["HIGHWAY", "SIRF", "10 MIN"], {"10", "MIN"}),
    (10.66, 11.95, ["MAAL AANA", "JAANA..."], set()),
    (11.95, 12.50, ["FAST!"], {"FAST!"}),
    (12.52, 13.62, ["APNA", "GATE."], {"GATE."}),
    (13.64, 14.32, ["APNA", "BOARD."], {"BOARD."}),
    (14.34, 15.62, ["APNA", "ADDRESS."], {"ADDRESS."}),
]
SUBTAGS = {3.55: "NH-152D  ·  10 MIN"}

def draw_caption(fr, t, c):
    t0, t1, lines, hl = c
    age = t - t0
    pop = 1 + 0.28 * (1 - ease(age / 0.16))  # pop in
    alpha = 255 if t < t1 - 0.06 else int(255 * max(0, (t1 - t) / 0.06))
    size = 190 if max(len(l) for l in lines) <= 9 else (165 if max(len(l) for l in lines) <= 11 else 140)
    f = F(FB, int(size * pop))
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    lh = int(size * 0.98 * pop); total = lh * len(lines)
    yc = 0.72 if t0 < 1.65 or t0 >= 12.5 else 0.47
    y = int(H * yc - total / 2)
    for i, line in enumerate(lines):
        words = line.split(" ")
        widths = [d.textlength(w + (" " if j < len(words) - 1 else ""), font=f) for j, w in enumerate(words)]
        x = (W - sum(widths)) / 2
        for w, ww in zip(words, widths):
            col = YEL if w in hl else WHITE
            d.text((x, y + i * lh), w, font=f, fill=col + (alpha,), stroke_width=max(6, int(size * 0.05)), stroke_fill=(0, 0, 0, int(alpha * 0.9)))
            x += ww
    # soft shadow
    sh = layer.split()[3].filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * 0.55))
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); shadow.putalpha(sh)
    fr.alpha_composite(shadow, (0, 12)); fr.alpha_composite(layer)

LOGO = None
def logo(width):
    global LOGO
    if LOGO is None:
        lg = Image.open("/home/claude/trueyards-media/ads/creatives/fit-c/logo_crop.png").convert("RGB")
        a = np.asarray(lg).astype(float).max(axis=2)
        LOGO = lg.copy(); LOGO.putalpha(Image.fromarray(np.clip((a - 40) * 1.6, 0, 255).astype("uint8")))
    return LOGO.resize((width, int(width * LOGO.height / LOGO.width)), Image.LANCZOS)

def chrome(fr, t, end=False):
    d = ImageDraw.Draw(fr)
    # top gradient for legibility
    if not end:
        g = Image.new("L", (1, 260)); g.putdata([int(150 * (1 - i / 260)) for i in range(260)])
        top = Image.new("RGBA", (W, 260), (0, 0, 0, 255)); top.putalpha(g.resize((W, 260)))
        fr.alpha_composite(top)
    f = F(INTER + "Inter-SemiBold.otf", 24)
    lab = "AI VISUALS  ·  ARTIST'S IMPRESSION"
    w = d.textlength(lab, font=f) + 44
    d.rounded_rectangle((36, 52, 36 + w, 96), radius=22, fill=(0, 0, 0, 140))
    d.text((58, 74), lab, font=f, fill=WHITE, anchor="lm")
    f2 = F(INTER + "Inter-Medium.otf", 22)
    for i, s in enumerate(HRERA + ["haryanarera.gov.in"]):
        d.text((W - 40, 52 + i * 28), s, font=f2, fill=(255, 255, 255, 230), anchor="ra",
               stroke_width=2, stroke_fill=(0, 0, 0, 160))

def end_overlay(fr, t):
    p = ease((t - 15.65) / 0.5)
    dark = Image.new("RGBA", (W, H), (0, 0, 0, int(120 * p))); fr.alpha_composite(dark)
    d = ImageDraw.Draw(fr)
    lg = logo(400); fr.alpha_composite(lg, ((W - lg.width) // 2, int(300 - 40 * (1 - p))))
    f = F(FB, 150)
    for i, (s, col) in enumerate([("APNI FACTORY", WHITE), ("KA ADDRESS", YEL)]):
        d.text((W / 2, 720 + i * 145), s, font=f, fill=col + (int(255 * p),), anchor="mm", stroke_width=7, stroke_fill=(0, 0, 0, int(200 * p)))
    d.text((W / 2, 1000), "FORTEASIA INDUSTRIAL TOWNSHIP", font=F(FB, 64), fill=(255, 255, 255, int(255 * p)), anchor="mm", stroke_width=3, stroke_fill=(0, 0, 0, 160))
    d.text((W / 2, 1068), "ROHTAK  ·  HARYANA", font=F(FS, 46), fill=(255, 255, 255, int(235 * p)), anchor="mm", stroke_width=2, stroke_fill=(0, 0, 0, 160))
    q = ease((t - 16.2) / 0.4); pulse = 1 + 0.04 * math.sin(t * 7)
    bw, bh = int(780 * pulse), int(150 * pulse); bx, by = (W - bw) // 2, 1210
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).rounded_rectangle((bx - 12, by - 12, bx + bw + 12, by + bh + 12), radius=88, fill=GREEN + (int(160 * q),))
    fr.alpha_composite(glow.filter(ImageFilter.GaussianBlur(28)))
    d.rounded_rectangle((bx, by, bx + bw, by + bh), radius=75, fill=GREEN + (int(255 * q),))
    d.text((W / 2, by + bh / 2), "NEECHE BUTTON DABAIYE", font=F(FB, 70), fill=(255, 255, 255, int(255 * q)), anchor="mm")
    for i in range(3):
        a = (math.sin(t * 6 - i * 0.9) + 1) / 2; y = 1410 + i * 46
        d.line((W / 2 - 36, y, W / 2, y + 32, W / 2 + 36, y), fill=GREEN + (int(255 * a * q),), width=11, joint="curve")
    f3 = F(INTER + "Inter-SemiBold.otf", 30)
    for i, s in enumerate(HRERA):
        d.text((W / 2, 1610 + i * 42), s, font=f3, fill=(255, 255, 255, int(240 * p)), anchor="mm", stroke_width=2, stroke_fill=(0, 0, 0, 150))
    d.text((W / 2, 1700), "Verify at haryanarera.gov.in", font=F(INTER + "Inter-Medium.otf", 26), fill=(255, 255, 255, int(220 * p)), anchor="mm")

def frame(t):
    for s in SHOTS:
        if s[0] <= t < s[1] or (s is SHOTS[-1] and t >= s[0]):
            t0, t1, name, z0, z1, dx, dy = s
            break
    img = kb(name, t, t0, t1, z0, z1, 0, dy, shake=1.0 if t0 in (1.65, 10.65) and t - t0 < 0.35 else 0)
    fr = img.convert("RGBA")
    # flash on cuts
    age = t - t0
    if age < 0.08 and t0 > 0:
        fr.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(170 * (1 - age / 0.08)))))
    end = t >= 15.65
    if not end:
        for c in CAPS:
            if c[0] <= t < c[1]: draw_caption(fr, t, c)
        if 3.55 <= t < 6.2:
            d = ImageDraw.Draw(fr)
    chrome(fr, t, end)
    if end: end_overlay(fr, t)
    return fr.convert("RGB")

def main(preview=None):
    os.makedirs(OUT, exist_ok=True)
    if preview:
        for t in preview: frame(t).save(OUT + f"prev_{t:05.2f}.jpg", quality=88)
        return
    # audio
    parts = []; fc = []
    for i, (a, b) in enumerate(SEG):
        fc.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS[v{i}]")
    fc.append("[v0][v1][v2]concat=n=3:v=0:a=1,volume=1.6,apad=whole_dur=25,asplit=2[vo][vo2]")
    fc.append(f"[1:a]atrim=1.9:{1.9 + DUR},asetpts=PTS-STARTPTS,volume=0.32,afade=t=out:st={DUR - 1.2}:d=1.2[mu]")
    fc.append("[mu][vo]sidechaincompress=threshold=0.05:ratio=6:attack=20:release=300[duck]")
    fc.append("[duck][vo2]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", VO, "-i", M + "a1-beat.mp3", "-filter_complex", ";".join(fc),
                    "-map", "[a]", "-t", str(DUR), "-ar", "48000", OUT + "a1_audio.wav"], check=True)
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-i", OUT + "a1_audio.wav", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
                          "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-t", str(DUR), "-movflags", "+faststart",
                          OUT + "FIT-A1-apni-factory-ka-address.mp4"], stdin=subprocess.PIPE)
    n = int(DUR * FPS)
    for i in range(n):
        try: p.stdin.write(frame(i / FPS).tobytes())
        except BrokenPipeError: break
    p.stdin.close(); p.wait()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1: main([float(x) for x in sys.argv[1:]])
    else: main()
