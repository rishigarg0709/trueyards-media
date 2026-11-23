"""FIT batch 2: new search-bar hooks spliced onto the winning P10 reel (same footage, facts and voice).
Usage: python render_hook.py <slug> "<search text>" <hook_voice.mp3> <out.mp4>"""
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SRC = "/home/claude/trueyards-media/ads/creatives/fit-reel-03-vo-hg-hq.mp4"
BEAT = "/home/claude/trueyards-media/library/media/fit-r3-beat.mp3"
BG = sorted(Path("/tmp/p10").glob("bg_*.png"))  # 63 frames = 0 to 2.1 s of P10
CUT = 2.1  # P10 cuts to "FOUND IT." here
FPS = 30
FONT = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-Medium.otf", 56)

slug, query, vo, out = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
work = Path(f"/tmp/fitb2/{slug}")
work.mkdir(parents=True, exist_ok=True)

vo_len = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", vo]).decode())
H = max(2.1, vo_len + 0.45)          # hook length: voice plus a beat for the tap
n = int(round(H * FPS))
type_end = min(H - 0.55, max(1.0, vo_len - 0.1))   # finish typing as the question ends
tap_at = H - 0.35


def frame(i):
    t = i / FPS
    bg = Image.open(BG[min(int(i * len(BG) / n), len(BG) - 1)]).convert("RGB")
    d = ImageDraw.Draw(bg)
    d.rounded_rectangle((90, 860, 989, 1023), radius=81, fill=(255, 255, 255))
    # search icon
    d.ellipse((140, 916, 176, 952), outline=(60, 60, 60), width=5)
    d.line((171, 947, 186, 962), fill=(60, 60, 60), width=6)
    k = max(0, min(len(query), int(len(query) * (t - 0.25) / max(type_end - 0.25, 0.1)))) if t >= 0.25 else 0
    txt = query[:k]
    d.text((214, 941), txt, font=FONT, fill=(25, 25, 25), anchor="lm")
    w = d.textlength(txt, font=FONT)
    if (t % 0.8) < 0.5 or k < len(query):
        d.line((218 + w, 912, 218 + w, 970), fill=(226, 35, 26), width=4)
    # red button with arrow
    cx, cy, r = 907, 941, 52
    pressed = tap_at <= t < tap_at + 0.15
    rr = r - 4 if pressed else r
    d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=(226, 35, 26))
    d.line((cx - 16, cy, cx + 14, cy), fill="white", width=6)
    d.line((cx + 2, cy - 13, cx + 15, cy), fill="white", width=6)
    d.line((cx + 2, cy + 13, cx + 15, cy), fill="white", width=6)
    if t >= tap_at - 0.25:  # tap ring
        a = min(1, (t - (tap_at - 0.25)) / 0.25)
        R = int(70 + 20 * a)
        d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=(235, 235, 235), width=4)
    bg.save(work / f"h_{i:03d}.png")


for i in range(n):
    frame(i)

hook = work / "hook.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", str(work / "h_%03d.png"),
                "-i", BEAT, "-i", vo, "-filter_complex",
                f"[1:a]atrim=0:{H},volume=0.55,afade=t=out:st={H-0.2}:d=0.2[b];[2:a]adelay=150|150[v];[b][v]amix=inputs=2:normalize=0,atrim=0:{H}[a]",
                "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2", "-t", str(H), str(hook)], check=True)
body = work / "body.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(CUT), "-i", SRC, "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2", "-r", str(FPS), str(body)], check=True)
lst = work / "list.txt"
lst.write_text(f"file '{hook}'\nfile '{body}'\n")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", out], check=True)
print(json.dumps({"slug": slug, "hook_s": round(H, 2), "vo_s": round(vo_len, 2), "out": out}))
