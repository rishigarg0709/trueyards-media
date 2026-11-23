"""FIT Industry, new theme (23 Nov 2026): "Kiraye se apne address tak" (from rented shed to your own plot).
Full colour AI visuals, landlord-message hook, Hinglish male voice, new music. Ends on the standard FIT end card.
Usage: python render.py <voice prefix r|j> <out.mp4>"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

V = sys.argv[1] if len(sys.argv) > 1 else "r"
OUT = sys.argv[2] if len(sys.argv) > 2 else f"/home/claude/fitc/FIT-c-{V}.mp4"
M = Path("/home/claude/trueyards-media/library/media")
P10 = "/home/claude/trueyards-media/ads/creatives/fit-reel-03-vo-hg-hq.mp4"
W, H, FPS = 1080, 1920, 30
RED = (232, 28, 36)
WORK = Path(f"/tmp/fitc/{V}"); WORK.mkdir(parents=True, exist_ok=True)
F = "/usr/share/fonts/opentype/inter/"
fXB = lambda s: ImageFont.truetype(F + "Inter-ExtraBold.otf", s)
fB = lambda s: ImageFont.truetype(F + "Inter-Bold.otf", s)
fM = lambda s: ImageFont.truetype(F + "Inter-Medium.otf", s)
fSB = lambda s: ImageFont.truetype(F + "Inter-SemiBold.otf", s)

def dur(p): return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]))

# ---------- voice timeline ----------
parts = ["hook", "pain", "turn", "facts", "cta"]
gaps = {"hook": 0.35, "pain": 0.45, "turn": 0.3, "facts": 0.45, "cta": 0.25}
start, t = {}, 0.35
for p in parts:
    start[p] = t
    t += dur(M / f"fitc-{V}-{p}.mp3") + gaps[p]
END_AT = t                      # end card starts
END_LEN = 3.2
TOTAL = END_AT + END_LEN

def at(part, phrase, which="start"):
    a = json.load(open(M / f"fitc-{V}-{part}.align.json"))
    s = "".join(a["characters"]); i = s.find(phrase)
    if i < 0: raise SystemExit(f"phrase not found {part}: {phrase}")
    if which == "start": return start[part] + a["character_start_times_seconds"][i]
    return start[part] + a["character_end_times_seconds"][i + len(phrase) - 1]

T = dict(
    pain1=at("pain", "हर"), pain2=at("pain", "गली"), pain3=at("pain", "और factory"),
    turn1=start["turn"] - 0.05, turn2=at("turn", "अपनी"),
    f1=start["facts"], f2=at("facts", "Industrial plots"), f3=at("facts", "Trucks"),
    f4=at("facts", "NH"), f5=at("facts", "और project"), cta=start["cta"] - 0.1,
)

# ---------- images ----------
cache = {}
def img(n):
    if n not in cache:
        im = Image.open(M / f"fitc-{n}-4k.jpg").convert("RGB")
        r = 1.18 * W / im.width
        cache[n] = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
    return cache[n]

def kb(n, p, z0=1.0, z1=1.08, cx=0.5, cy=0.5, dx=0.0, dy=0.0):
    """Ken Burns: p in 0..1. zoom relative to a frame that just covers the canvas."""
    im = img(n)
    base = max(W / im.width, H / im.height)
    z = base * (z0 + (z1 - z0) * p)
    cw, ch = W / z, H / z
    x = (cx + dx * p) * im.width - cw / 2; y = (cy + dy * p) * im.height - ch / 2
    x = min(max(0, x), im.width - cw); y = min(max(0, y), im.height - ch)
    return im.crop((int(x), int(y), int(x + cw), int(y + ch))).resize((W, H), Image.BILINEAR)

# shot list: (start, image, kb args, ai label)
AI = "AI visualisation"
AIS = "AI visualisation, not the actual site"
SHOTS = [
    (0.0, "1", dict(z0=1.0, z1=1.10, cx=0.55, cy=0.5), AI),
    (T["pain1"], "3", dict(z0=1.05, z1=1.18, cx=0.5, cy=0.72), AI),
    (T["pain2"], "2", dict(z0=1.12, z1=1.0, cx=0.5, cy=0.6), AI),
    (T["pain3"], "1", dict(z0=1.35, z1=1.45, cx=0.3, cy=0.62), AI),
    (T["turn1"], "4", dict(z0=1.0, z1=1.14, cx=0.5, cy=0.55), AIS),
    (T["f1"], "6", dict(z0=1.0, z1=1.12, cx=0.5, cy=0.5, dy=-0.04), AIS),
    (T["f2"], "6", dict(z0=1.35, z1=1.5, cx=0.62, cy=0.55), AIS),
    (T["f3"], "4", dict(z0=1.25, z1=1.12, cx=0.5, cy=0.68), AIS),
    (T["f4"], "5", dict(z0=1.0, z1=1.1, cx=0.5, cy=0.5), AIS),
    (T["f5"], None, {}, None),            # HRERA card
    (T["cta"], "5", dict(z0=1.2, z1=1.32, cx=0.55, cy=0.45), AIS),
]

# captions: (start, end, lines[(text, red?)], small)
CAPS = [
    (T["pain1"] + 0.1, T["pain2"], [("RENT BADHA.", True), ("HAR SAAL.", False)], None),
    (T["pain2"] + 0.1, T["pain3"], [("TRUCK", False), ("GALI MEIN FASA.", True)], None),
    (T["pain3"] + 0.1, T["turn1"], [("FACTORY?", False), ("PHIR BHI", False), ("KIRAYE KI.", True)], None),
    (T["turn1"] + 0.05, T["turn2"], [("AB KIRAYA", False), ("NAHI.", True)], None),
    (T["turn2"], T["f1"], [("APNI", False), ("ZAMEEN.", True)], None),
    (T["f1"] + 0.1, T["f2"], [("FORTEASIA", False), ("INDUSTRIAL", False), ("TOWNSHIP", True)], "Kalanaur, Rohtak, Haryana"),
    (T["f2"] + 0.1, T["f3"], [("PLOTS", False), ("500 TO 4,000", True), ("SQ YD", False)], "Industrial plots"),
    (T["f3"] + 0.1, T["f4"], [("18 M & 24 M", True), ("ROADS", False)], "Wide enough for trucks"),
    (T["f4"] + 0.1, T["f5"], [("NH-152D", True), ("10 MIN", False)], "Rohtak-Bhiwani highway, 5 min"),
    (T["cta"] + 0.05, END_AT, [("KIRAYE SE", False), ("APNE ADDRESS", True), ("TAK.", False)], "Message us on WhatsApp"),
]

# ---------- static elements ----------
lg = Image.open("/home/claude/trueyards-media/ads/creatives/fit-c/logo_crop.png").convert("RGB")
a = np.asarray(lg).astype(float).max(axis=2)
alpha = Image.fromarray(np.clip((a - 40) * 1.6, 0, 255).astype("uint8"))
logo = lg.copy(); logo.putalpha(alpha); logo = logo.resize((170, 117), Image.LANCZOS)

def chip(d, box, fill=(0, 0, 0, 150), r=14):
    d.rounded_rectangle(box, radius=r, fill=fill)

def top_bar(fr):
    o = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(o)
    g = Image.linear_gradient("L").rotate(180).resize((W, 300))
    o.paste(Image.new("RGBA", (W, 300), (0, 0, 0, 120)), (0, 0), g.point(lambda v: v * 0.9))
    chip(d, (40, 48, 250, 196), (10, 10, 10, 170))
    o.alpha_composite(logo, (60, 63))
    f = ImageFont.truetype(F + "Inter-SemiBold.otf", 23)
    lines = ["HRERA-PKL-ROH-795-2025", "HRERA-PKL-ROH-653-2025", "www.haryanarera.gov.in"]
    chip(d, (690, 58, 1040, 168), (10, 10, 10, 170))
    d.rectangle((1032, 66, 1036, 160), fill=RED)
    for k, s in enumerate(lines):
        d.text((708, 72 + k * 31), s, font=f, fill=(235, 235, 235))
    fr.alpha_composite(o)

def ai_label(fr, text):
    d = ImageDraw.Draw(fr); f = fM(26)
    w = d.textlength(text, font=f)
    chip(d, (40, H - 112, 40 + w + 64, H - 62), (10, 10, 10, 160), 25)
    d.ellipse((58, H - 95, 74, H - 79), fill=RED)
    d.text((86, H - 87), text, font=f, fill=(240, 240, 240), anchor="lm")

def bottom_shade(fr):
    g = Image.linear_gradient("L").resize((W, 900))
    fr.alpha_composite(Image.new("RGBA", (W, 900), (0, 0, 0, 0)), (0, H - 900))
    sh = Image.new("RGBA", (W, 900), (0, 0, 0, 185)); sh.putalpha(g.point(lambda v: int(v * 0.8)))
    fr.alpha_composite(sh, (0, H - 900))

def caption(fr, lines, small, p):
    d = ImageDraw.Draw(fr)
    size = 118
    f = fXB(size)
    y = H - 260 - len(lines) * (size + 18) - (60 if small else 0)
    for k, (s, red) in enumerate(lines):
        pk = min(1, max(0, (p - k * 0.06) / 0.18))  # staggered pop
        if pk <= 0: continue
        off = int((1 - pk) * 40)
        w = d.textlength(s, font=f)
        x = 70
        if red:
            d.rectangle((x - 18, y + off - 4, x + w * pk + 18, y + off + size + 8), fill=RED)
        else:
            d.text((x + 3, y + off + 4), s, font=f, fill=(0, 0, 0, 120))
        d.text((x, y + off), s, font=f, fill=(255, 255, 255))
        y += size + 18
    if small and p > 0.15:
        d.text((74, y + 16), small, font=fSB(42), fill=(255, 255, 255))

def hrera_card(p):
    fr = Image.new("RGBA", (W, H), (246, 244, 239, 255)); d = ImageDraw.Draw(fr)
    d.rectangle((0, 0, 22, H), fill=RED)
    d.text((90, 600), "REGISTERED", font=fSB(40), fill=RED)
    d.text((86, 660), "HRERA", font=fXB(210), fill=(18, 18, 18))
    for k, s in enumerate(["HRERA-PKL-ROH-795-2025", "HRERA-PKL-ROH-653-2025"]):
        if p > 0.15 + 0.15 * k:
            yy = 940 + k * 92
            d.rectangle((92, yy + 14, 118, yy + 40), fill=RED)
            d.text((146, yy), s, font=fB(56), fill=(18, 18, 18))
    if p > 0.45:
        d.text((92, 1170), "DTCP Haryana licence 86 and 164 of 2026", font=fM(36), fill=(70, 70, 70))
        d.text((92, 1220), "Verify at www.haryanarera.gov.in", font=fM(36), fill=(70, 70, 70))
    lg2 = logo.resize((230, 158))
    dark = Image.new("RGBA", (290, 200), (18, 18, 18, 255))
    fr.alpha_composite(dark, (90, 300)); fr.alpha_composite(lg2, (120, 321))
    return fr

def notif(fr, t):
    if t < 0.15: return
    p = min(1, (t - 0.15) / 0.28); p = 1 - (1 - p) ** 3
    y0 = int(-260 + p * (300 + 260))
    o = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(o)
    d.rounded_rectangle((50, y0 + 8, 1030, y0 + 238), radius=44, fill=(0, 0, 0, 70))
    d.rounded_rectangle((50, y0, 1030, y0 + 230), radius=44, fill=(250, 250, 250, 245))
    d.rounded_rectangle((86, y0 + 40, 176, y0 + 130), radius=22, fill=(37, 180, 90))
    d.rounded_rectangle((108, y0 + 64, 154, y0 + 98), radius=10, fill="white")
    d.polygon([(116, y0 + 96), (112, y0 + 112), (130, y0 + 98)], fill="white")
    d.text((206, y0 + 48), "Landlord", font=fB(44), fill=(20, 20, 20))
    d.text((990, y0 + 52), "now", font=fM(34), fill=(130, 130, 130), anchor="ra")
    d.text((206, y0 + 112), "Next month se rent badh raha hai.", font=fM(40), fill=(40, 40, 40))
    d.text((206, y0 + 164), "Aur agreement bhi renew karna hai.", font=fM(40), fill=(40, 40, 40))
    fr.alpha_composite(o)
    # second ping on the phone screen
    if t > 1.0:
        d = ImageDraw.Draw(fr)

# ---------- render ----------
N = int(round(END_AT * FPS))
for i in range(N):
    t = i / FPS
    k = max(j for j, s in enumerate(SHOTS) if s[0] <= t + 1e-6)
    s0, name, args, lab = SHOTS[k]
    s1 = SHOTS[k + 1][0] if k + 1 < len(SHOTS) else END_AT
    p = (t - s0) / max(s1 - s0, 0.01)
    if name is None:
        fr = hrera_card(p)
    else:
        fr = kb(name, p, **args).convert("RGBA")
        bottom_shade(fr)
    if name is not None:
        top_bar(fr)
        ai_label(fr, lab)
    if t < T["pain1"]:
        notif(fr, t)
        if t > start["hook"]:
            pass
    for c0, c1, lines, small in CAPS:
        if c0 <= t < c1:
            caption(fr, lines, small, (t - c0) / 0.6)
    # hard-cut flash on the turn
    if 0 <= t - T["turn1"] < 0.1:
        fr = Image.blend(fr, Image.new("RGBA", (W, H), (255, 255, 255, 255)), 0.55 * (1 - (t - T["turn1"]) / 0.1))
    fr.convert("RGB").save(WORK / f"f_{i:04d}.jpg", quality=92)

body = WORK / "body.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", str(WORK / "f_%04d.jpg"),
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", str(body)], check=True)
endc = WORK / "end.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "33.0", "-t", str(END_LEN), "-i", P10, "-an",
                "-vf", "fps=30", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", str(endc)], check=True)

# ---------- audio ----------
beat = M / "fitc-beat.mp3"
inputs = ["-i", str(beat)]; flt = []; mix = ["[m]"]
flt.append(f"[0:a]atrim=0:{TOTAL},afade=t=out:st={TOTAL-1.2}:d=1.2,volume=0.30[m]")
for k, p_ in enumerate(parts):
    inputs += ["-i", str(M / f"fitc-{V}-{p_}.mp3")]
    ms = int(start[p_] * 1000)
    flt.append(f"[{k+1}:a]adelay={ms}|{ms},volume=1.6[v{k}]"); mix.append(f"[v{k}]")
flt.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0,loudnorm=I=-15:TP=-1.5:LRA=11[a]")
aud = WORK / "mix.m4a"
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(flt), "-map", "[a]",
                "-t", str(TOTAL), "-c:a", "aac", "-b:a", "192k", str(aud)], check=True)
cat = WORK / "list.txt"; cat.write_text(f"file '{body}'\nfile '{endc}'\n")
vid = WORK / "video.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(cat), "-c", "copy", str(vid)], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(vid), "-i", str(aud), "-map", "0:v", "-map", "1:a",
                "-c:v", "libx264", "-crf", "21", "-maxrate", "9M", "-bufsize", "18M", "-pix_fmt", "yuv420p",
                "-c:a", "copy", "-shortest", "-movflags", "+faststart", OUT], check=True)
print(json.dumps({"out": OUT, "total": round(TOTAL, 2), "times": {k: round(v, 2) for k, v in T.items()}}))
