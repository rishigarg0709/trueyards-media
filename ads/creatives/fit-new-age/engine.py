"""Shared engine for the four new-age FIT Industry reels (25 Nov 2026)."""
import json, subprocess, shutil, math, random
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops, ImageEnhance

W, H, FPS = 1080, 1920, 30
SRC = Path("/home/claude/fitn/src")
R02 = Path("/home/claude/fitd/src")
M = Path("/home/claude/trueyards-media/library/media")
INTER = "/usr/share/fonts/opentype/inter/"
FD = "/home/claude/fitd/fonts/"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
def F(name, s):
    p = {"xb": INTER + "Inter-ExtraBold.otf", "bk": INTER + "Inter-Black.otf", "b": INTER + "Inter-Bold.otf",
         "sb": INTER + "Inter-SemiBold.otf", "m": INTER + "Inter-Medium.otf", "bc": FD + "BarlowCondensed-ExtraBold.ttf",
         "bcs": FD + "BarlowCondensed-SemiBold.ttf", "mono": MONO}[name]
    return ImageFont.truetype(p, s)

def dur(p): return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]))

class VO:
    def __init__(self, name, at=0.3):
        self.name, self.at = name, at
        self.a = json.load(open(M / f"{name}.align.json")); self.s = "".join(self.a["characters"])
        self.len = dur(M / f"{name}.mp3")
    def t(self, phrase, end=False):
        i = self.s.find(phrase); assert i >= 0, phrase
        k = i + len(phrase) - 1 if end else i
        return self.at + (self.a["character_end_times_seconds"] if end else self.a["character_start_times_seconds"])[k]
    @property
    def end(self): return self.at + self.len

GRADES = {
    "warm": "eq=contrast=1.08:saturation=1.18:brightness=0.01,colorbalance=rs=0.04:bs=-0.04",
    "vivid": "eq=contrast=1.15:saturation=1.45:brightness=0.02",
    "faded": "hue=s=0.25,eq=contrast=0.92:brightness=-0.03,colorbalance=rs=0.08:gs=0.03:bs=-0.06",
    "neon": "eq=contrast=1.25:saturation=0.55:brightness=-0.2:gamma=0.85,colorbalance=rs=-0.12:gs=0.02:bs=0.22:rm=-0.08:bm=0.18",
    "clean": "eq=contrast=1.05:saturation=1.1",
}
# source framings: letterboxed 4K update (bars and burnt-in subtitles), wide walkthrough, full vertical
FRAMING = {"upd": "crop=855:1520:112:200,scale=1080:1920", "wide": "crop=ih*9/16:ih,scale=1080:1920", "v": "scale=1080:1920"}

def build_video_shot(work, k, s, need):
    """s: dict(src, t, kind in FRAMING, speed, z0, z1, ax, ay, grade, ramp)"""
    f = s["src"]; kind = s.get("kind", "v"); sp = s.get("speed", 1.0)
    avail = dur(f) - s["t"]
    if avail / sp < need: sp = max(0.5, avail / need)
    out = work / f"seg{k:02d}.mp4"
    z0, z1 = s.get("z0", 1.0), s.get("z1", 1.08); ax, ay = s.get("ax", 0.5), s.get("ay", 0.5)
    n = max(1, int(need * FPS))
    vf = (f"{FRAMING[kind]},setpts=PTS/{sp},fps={FPS},"
          f"scale={int(W*1.25)}:-2,zoompan=z='{z0}+({z1}-{z0})*on/{n}':x='(iw-iw/zoom)*{ax}':y='(ih-ih/zoom)*{ay}':d=1:s={W}x{H}:fps={FPS},"
          f"{GRADES[s.get('grade','warm')]},tpad=stop_mode=clone:stop_duration=4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(s["t"]), "-i", str(f), "-vf", vf, "-t", f"{need:.3f}", "-an",
                    "-c:v", "libx264", "-crf", "15", "-pix_fmt", "yuv420p", str(out)], check=True)
    d = work / f"seg{k:02d}"; d.mkdir()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(out), "-q:v", "2", str(d / "f_%04d.jpg")], check=True)
    return sorted(d.glob("*.jpg"))

def build_frames(work, shots, end_at):
    """returns list of (shot_index, local_time, frame_source) per output frame. A still shot has 'still': PIL image fn."""
    seq = []
    for k, s in enumerate(shots):
        s0 = s["at"]; s1 = shots[k + 1]["at"] if k + 1 < len(shots) else end_at
        need = s1 - s0
        frames = None if s.get("still") else build_video_shot(work, k, s, need)
        n = int(round(s1 * FPS)) - int(round(s0 * FPS))
        for i in range(n):
            seq.append((k, i / FPS, need, frames[min(i, len(frames) - 1)] if frames else None))
    return seq

def kb(im, p, z0=1.0, z1=1.08, ax=0.5, ay=0.5):
    z = z0 + (z1 - z0) * p; cw, ch = im.width / z, im.height / z
    x = (im.width - cw) * ax; y = (im.height - ch) * ay
    return im.crop((int(x), int(y), int(x + cw), int(y + ch))).resize((W, H), Image.BILINEAR)

def ease(x): x = min(1, max(0, x)); return 1 - (1 - x) ** 3
def back(x):
    x = min(1, max(0, x)); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2

LOGO = None
def logo(width=300, color=None):
    global LOGO
    if LOGO is None:
        lg = Image.open("/home/claude/trueyards-media/ads/creatives/fit-c/logo_crop.png").convert("RGB")
        a = np.asarray(lg).astype(float).max(axis=2)
        LOGO = lg.copy(); LOGO.putalpha(Image.fromarray(np.clip((a - 40) * 1.6, 0, 255).astype("uint8")))
    im = LOGO.resize((width, int(width * LOGO.height / LOGO.width)), Image.LANCZOS)
    if color:
        solid = Image.new("RGBA", im.size, color + (255,)); solid.putalpha(im.split()[3]); return solid
    return im

def text_w(d, s, f): return d.textlength(s, font=f)

def stroke_text(d, xy, s, f, fill="white", stroke=8, sfill="black", anchor="la"):
    d.text(xy, s, font=f, fill=fill, stroke_width=stroke, stroke_fill=sfill, anchor=anchor)

def glow_layer(draw_fn, radius=14, strength=2):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); draw_fn(ImageDraw.Draw(lay))
    g = lay.filter(ImageFilter.GaussianBlur(radius))
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for _ in range(strength): out = Image.alpha_composite(out, g)
    return Image.alpha_composite(out, lay)

def mix_audio(work, total, beat, beat_vol, vos, out, music_start=0.0, duck=None):
    inputs = ["-ss", str(music_start), "-i", str(M / beat)]
    flt = [f"[0:a]atrim=0:{total},afade=t=out:st={total-1.2}:d=1.2,volume={beat_vol}[m]"]; mix = ["[m]"]
    for k, (name, at) in enumerate(vos):
        inputs += ["-i", str(M / f"{name}.mp3")]; ms = int(at * 1000)
        flt.append(f"[{k+1}:a]adelay={ms}|{ms},volume=1.7[v{k}]"); mix.append(f"[v{k}]")
    flt.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(flt), "-map", "[a]", "-t", str(total),
                    "-c:a", "aac", "-b:a", "192k", str(out)], check=True)

def encode(work, n, audio, out):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", str(work / "o_%05d.jpg"), "-i", str(audio),
                    "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-crf", "19", "-maxrate", "12M", "-bufsize", "24M",
                    "-pix_fmt", "yuv420p", "-c:a", "copy", "-shortest", "-movflags", "+faststart", str(out)], check=True)

HRERA = ["HRERA-PKL-ROH-795-2025", "HRERA-PKL-ROH-653-2025"]
PHONE = "+91 92206 07264"

def end_card(t, dark=(8, 10, 16), accent=(37, 211, 102), sub=(200, 200, 210), title_col=(255, 255, 255), lines=None):
    """Clean modern end card with the FIT logo, WhatsApp button and pulsing arrows."""
    fr = Image.new("RGBA", (W, H), dark + (255,)); d = ImageDraw.Draw(fr)
    g = Image.radial_gradient("L").resize((1600, 1600)).point(lambda v: int((255 - v) * 0.25))
    halo = Image.new("RGBA", (1600, 1600), accent + (0,)); halo.putalpha(g); fr.alpha_composite(halo, (-260, 300))
    p = ease(t / 0.5)
    lg = logo(520); fr.alpha_composite(lg, ((W - lg.width) // 2, int(430 - 40 * (1 - p))))
    f = F("xb", 58); s = "FORTEASIA INDUSTRIAL TOWNSHIP"
    d.text((W / 2, 880), s, font=F("b", 44), fill=title_col, anchor="mm")
    d.text((W / 2, 945), "KALANAUR  ·  ROHTAK  ·  HARYANA", font=F("m", 32), fill=sub, anchor="mm")
    if lines:
        for i, l in enumerate(lines): d.text((W / 2, 1010 + i * 46), l, font=F("sb", 34), fill=sub, anchor="mm")
    q = ease((t - 0.25) / 0.4); pulse = 1 + 0.035 * math.sin(t * 7)
    bw, bh = int(760 * pulse), int(150 * pulse); bx, by = (W - bw) // 2, 1150
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(glow).rounded_rectangle((bx - 10, by - 10, bx + bw + 10, by + bh + 10), radius=85, fill=accent + (int(150 * q),))
    fr.alpha_composite(glow.filter(ImageFilter.GaussianBlur(28)))
    d.rounded_rectangle((bx, by, bx + bw, by + bh), radius=75, fill=accent + (int(255 * q),))
    d.text((W / 2, by + bh / 2 - 18), "WHATSAPP KARIYE", font=F("bk", 54), fill=(255, 255, 255, int(255 * q)), anchor="mm")
    d.text((W / 2, by + bh / 2 + 34), PHONE, font=F("sb", 34), fill=(255, 255, 255, int(255 * q)), anchor="mm")
    for i in range(3):
        a = (math.sin(t * 6 - i * 0.9) + 1) / 2
        y = 1350 + i * 46; c = accent + (int(255 * a * q),)
        d.line((W / 2 - 34, y, W / 2, y + 30, W / 2 + 34, y), fill=c, width=10, joint="curve")
    for i, s in enumerate(HRERA):
        d.text((W / 2, 1600 + i * 36), s, font=F("m", 28), fill=sub, anchor="mm")
    d.text((W / 2, 1680), "Verify at haryanarera.gov.in", font=F("m", 26), fill=sub, anchor="mm")
    return fr

def chip_footage(fr, label="ACTUAL SITE FOOTAGE", y=78, col=(255, 255, 255), dot=(255, 60, 60), small=True):
    d = ImageDraw.Draw(fr); f = F("sb", 26)
    w = text_w(d, label, f) + 70
    d.rounded_rectangle((40, y - 6, 40 + w, y + 42), radius=24, fill=(0, 0, 0, 120))
    d.ellipse((58, y + 10, 74, y + 26), fill=dot); d.text((88, y + 18), label, font=f, fill=col, anchor="lm")
    f2 = F("m", 22)
    for i, s in enumerate(HRERA):
        d.text((W - 44, y + 4 + i * 28), s, font=f2, fill=(255, 255, 255, 220), anchor="ra")
