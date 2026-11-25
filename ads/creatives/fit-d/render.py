"""FIT Industry reel D (25 Nov 2026): "Ye render nahi hai, ye asli site hai".
Real site footage only, P10 look (black and white footage, FIT red, white Barlow captions), upbeat Jessa voice,
P10 beat, standard FIT end card. Rishi 25 Nov: no sad or pain-led reels; match the red and white reel with actual shots."""
import json, subprocess, shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

M = Path("/home/claude/trueyards-media/library/media")
SRC = Path("/home/claude/fitd/src")
P10 = "/home/claude/trueyards-media/ads/creatives/fit-reel-03-vo-hg-hq.mp4"
W, H, FPS = 1080, 1920, 30
RED = (232, 28, 36)
WORK = Path("/tmp/fitd"); shutil.rmtree(WORK, ignore_errors=True); WORK.mkdir(parents=True)
FD = "/home/claude/fitd/fonts/"
BX = lambda s: ImageFont.truetype(FD + "BarlowCondensed-ExtraBold.ttf", s)
BS = lambda s: ImageFont.truetype(FD + "BarlowCondensed-SemiBold.ttf", s)
MONO = lambda s: ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", s)

def dur(p): return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]))

parts = ["hook", "body", "cta"]; gap = {"hook": 0.25, "body": 0.3, "cta": 0.3}
start, t = {}, 0.2
for p in parts:
    start[p] = t; t += dur(M / f"fitd-{p}.mp3") + gap[p]
END_AT = t; END_LEN = 3.2; TOTAL = END_AT + END_LEN

def at(part, phrase, which="s"):
    a = json.load(open(M / f"fitd-{part}.align.json")); s = "".join(a["characters"]); i = s.find(phrase)
    assert i >= 0, phrase
    return start[part] + (a["character_start_times_seconds"][i] if which == "s" else a["character_end_times_seconds"][i + len(phrase) - 1])

T = dict(asli=at("hook", "asli"), fit=start["body"], acre=at("body", "Ek sau"), kaam=at("body", "Kaam"),
         plots=at("body", "Industrial plots"), trucks=at("body", "Trucks"), nh=at("body", "NH"),
         rera=at("body", "Aur project"), cta=start["cta"])

# (start, clip, clip offset, zoom from, zoom to, crop bottom ticker)
SHOTS = [
    (0.0, "real-aerial1", 0.0, 1.00, 1.12, False),
    (T["asli"] - 0.05, "real-sign", 0.0, 1.05, 1.18, False),
    (T["fit"], "real-gate", 0.9, 1.00, 1.10, False),
    (T["acre"], "real-aerial2", 1.0, 1.05, 1.15, False),
    (T["kaam"], "real-aerial3", 0.0, 1.00, 1.12, False),
    (T["plots"], "real-road", 0.0, 1.00, 1.10, False),
    (T["trucks"], "real-truck", 0.0, 1.10, 1.00, False),
    (T["nh"], "real-aerial1", 1.2, 1.15, 1.25, False),
    (T["rera"], "real-gate2", 0.0, 1.20, 1.30, True),
    (T["cta"], "real-office", 0.0, 1.00, 1.10, False),
]

# footage track: one graded clip per shot, slowed (never below 0.55x) or trimmed to fit
segs = []
for k, (s0, clip, off, z0, z1, tick) in enumerate(SHOTS):
    s1 = SHOTS[k + 1][0] if k + 1 < len(SHOTS) else END_AT
    need = s1 - s0; f = SRC / f"{clip}.mp4"; avail = dur(f) - off
    speed = min(1.0, max(0.55, avail / need))
    out = WORK / f"seg{k:02d}.mp4"
    crop = "crop=iw:ih*0.88:0:0," if tick else ""
    vf = (f"{crop}setpts=PTS/{speed},scale={int(W*1.3)}:-2,"
          f"zoompan=z='{z0}+({z1}-{z0})*on/({int(need*FPS)})':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS},"
          f"hue=s=0,eq=contrast=1.22:brightness=-0.02,tpad=stop_mode=clone:stop_duration=3")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(off), "-i", str(f), "-t", f"{need:.3f}", "-vf", vf,
                    "-t", f"{need:.3f}", "-an", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", str(out)], check=True)
    segs.append(out)
(WORK / "l.txt").write_text("".join(f"file '{s}'\n" for s in segs))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(WORK / "l.txt"), "-t", f"{END_AT:.3f}",
                "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", str(WORK / "foot.mp4")], check=True)
(WORK / "fr").mkdir()
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(WORK / "foot.mp4"), "-vf", f"fps={FPS}", "-q:v", "2", str(WORK / "fr" / "f_%04d.jpg")], check=True)

# captions: (start, end, [(text, red box?)], small line)
CAPS = [
    (0.25, T["asli"] - 0.05, [("YE RENDER", False), ("NAHI HAI.", True)], None),
    (T["asli"] - 0.05, T["fit"], [("YE ASLI", False), ("SITE HAI.", True)], None),
    (T["fit"] + 0.05, T["acre"], [("FORTEASIA", False), ("INDUSTRIAL", False), ("TOWNSHIP", True)], "KALANAUR, ROHTAK"),
    (T["acre"] + 0.05, T["kaam"], [("138", True), ("ACRES", False)], None),
    (T["kaam"] + 0.05, T["plots"], [("KAAM", False), ("ZAMEEN PAR.", True)], "ON THE GROUND. NOW."),
    (T["plots"] + 0.05, T["trucks"], [("PLOTS", False), ("500 - 4,000", True), ("SQ YD", False)], None),
    (T["trucks"] + 0.05, T["nh"], [("18 M & 24 M", True), ("ROADS", False)], "BUILT FOR TRUCKS"),
    (T["nh"] + 0.05, T["rera"], [("NH-152D", True), ("10 MIN", False)], "ROHTAK-BHIWANI HIGHWAY 5 MIN"),
    (T["cta"] + 0.05, END_AT, [("SITE", False), ("DEKHNI HAI?", True)], "WHATSAPP KARIYE"),
]

def chips(fr):
    d = ImageDraw.Draw(fr)
    d.rectangle((48, 70, 48 + 20, 90), fill=RED)
    d.text((80, 64), "ACTUAL SITE FOOTAGE", font=MONO(26), fill="white")
    f = MONO(22)
    for i, s in enumerate(["HRERA-PKL-ROH-795-2025", "HRERA-PKL-ROH-653-2025"]):
        w = d.textlength(s, font=f); d.text((W - 48 - w, 66 + i * 30), s, font=f, fill=(230, 230, 230))

def shade(fr):
    g = Image.linear_gradient("L").resize((W, 1000))
    sh = Image.new("RGBA", (W, 1000), (0, 0, 0, 200)); sh.putalpha(g.point(lambda v: int(v * 0.85)))
    fr.alpha_composite(sh, (0, H - 1000))
    top = Image.linear_gradient("L").rotate(180).resize((W, 260))
    sh2 = Image.new("RGBA", (W, 260), (0, 0, 0, 150)); sh2.putalpha(top.point(lambda v: int(v * 0.8)))
    fr.alpha_composite(sh2, (0, 0))

def caption(fr, lines, small, p):
    d = ImageDraw.Draw(fr); size = 190 if len(lines) <= 2 else 160
    f = BX(size); lh = int(size * 0.98)
    y = H - 330 - len(lines) * lh - (70 if small else 0)
    for k, (s, red) in enumerate(lines):
        q = min(1, max(0, (p - k * 0.07) / 0.14))
        if q <= 0: y += lh; continue
        w = d.textlength(s, font=f); x = 64
        if red:
            d.rectangle((x - 14, y + 18, x + (w + 28) * q - 14, y + lh + 6), fill=RED)
        d.text((x, y + int((1 - q) * 30)), s, font=f, fill="white")
        y += lh
    if small and p > 0.2:
        d.rectangle((66, y + 30, 66 + 8, y + 82), fill=RED)
        d.text((92, y + 26), small, font=BS(54), fill="white")

def hrera(fr, p):
    d = ImageDraw.Draw(fr)
    bw, bh = 960, 560; x0, y0 = (W - bw) // 2, 640
    q = min(1, p / 0.12)
    card = Image.new("RGBA", (bw, bh), (255, 255, 255, int(245 * q))); cd = ImageDraw.Draw(card)
    cd.rectangle((0, 0, bw, 18), fill=RED)
    cd.text((50, 50), "HRERA REGISTERED", font=BX(110), fill=(15, 15, 15))
    for i, s in enumerate(["HRERA-PKL-ROH-795-2025", "HRERA-PKL-ROH-653-2025"]):
        cd.rectangle((52, 205 + i * 92, 74, 227 + i * 92), fill=RED)
        cd.text((96, 182 + i * 92), s, font=BX(76), fill=(15, 15, 15))
    cd.text((52, 390), "DTCP LICENCES 86/2024, 84/2025, 185/2025", font=BS(44), fill=(60, 60, 60))
    cd.text((52, 450), "VERIFY AT HARYANARERA.GOV.IN", font=BS(44), fill=(60, 60, 60))
    fr.alpha_composite(card, (x0, y0 + int((1 - q) * 60)))

N = int(round(END_AT * FPS))
for i in range(N):
    t = i / FPS
    src = WORK / "fr" / f"f_{min(i + 1, len(list((WORK / 'fr').glob('*.jpg')))) :04d}.jpg"
    fr = Image.open(src).convert("RGBA")
    if fr.size != (W, H): fr = fr.resize((W, H))
    shade(fr); chips(fr)
    for c0, c1, lines, small in CAPS:
        if c0 <= t < c1: caption(fr, lines, small, (t - c0) / 0.5)
    if T["rera"] <= t < T["cta"]: hrera(fr, (t - T["rera"]) / max(T["cta"] - T["rera"], 0.1))
    # beat flash on the two big cuts
    for cut in (T["asli"] - 0.05, T["fit"]):
        if 0 <= t - cut < 0.08:
            fr = Image.blend(fr, Image.new("RGBA", (W, H), (255, 255, 255, 255)), 0.5 * (1 - (t - cut) / 0.08))
    fr.convert("RGB").save(WORK / f"o_{i:04d}.jpg", quality=92)

subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", str(WORK / "o_%04d.jpg"),
                "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", str(WORK / "body.mp4")], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "33.0", "-t", str(END_LEN), "-i", P10, "-an", "-vf", "fps=30",
                "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", str(WORK / "end.mp4")], check=True)
(WORK / "c.txt").write_text(f"file '{WORK/'body.mp4'}'\nfile '{WORK/'end.mp4'}'\n")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(WORK / "c.txt"), "-c", "copy", str(WORK / "v.mp4")], check=True)

inputs = ["-i", str(M / "fit-r3-beat.mp3")]; flt = [f"[0:a]atrim=0:{TOTAL},afade=t=out:st={TOTAL-1.0}:d=1.0,volume=0.38[m]"]; mix = ["[m]"]
for k, p in enumerate(parts):
    inputs += ["-i", str(M / f"fitd-{p}.mp3")]; ms = int(start[p] * 1000)
    flt.append(f"[{k+1}:a]adelay={ms}|{ms},volume=1.7[v{k}]"); mix.append(f"[v{k}]")
flt.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(flt), "-map", "[a]", "-t", str(TOTAL),
                "-c:a", "aac", "-b:a", "192k", str(WORK / "a.m4a")], check=True)
OUT = "/home/claude/fitd/FIT-d-asli-site.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(WORK / "v.mp4"), "-i", str(WORK / "a.m4a"), "-map", "0:v", "-map", "1:a",
                "-c:v", "libx264", "-crf", "20", "-maxrate", "10M", "-bufsize", "20M", "-pix_fmt", "yuv420p", "-c:a", "copy",
                "-shortest", "-movflags", "+faststart", OUT], check=True)
print(json.dumps({"out": OUT, "total": round(TOTAL, 2), "T": {k: round(v, 2) for k, v in T.items()}}))
