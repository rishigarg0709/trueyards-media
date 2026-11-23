"""Free 4K upscale for generated images (no API cost).
Gemini makes images at 2K; this runs Real-ESRGAN (realesr-general-x4v3, CPU) on each new one and writes
library/media/<name>-4k.jpg: 2x for 2K Pro images, 4x for 1K Flash images (both end near 3072x5504).
usage: python3 scripts/upscale.py [files...]   (no args: new or changed PNGs in library/media below 3000 px)"""
import os, subprocess, sys, urllib.request
import numpy as np, torch
from PIL import Image
from spandrel import ModelLoader

Image.MAX_IMAGE_PIXELS = None
W = os.path.expanduser("~/.cache/realesr-general-x4v3.pth")
URL = "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-general-x4v3.pth"
TILE, PAD = 384, 16

def targets():
    if len(sys.argv) > 1: return sys.argv[1:]
    out = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all", "library/media"], capture_output=True, text=True).stdout
    fs = [l[3:].strip() for l in out.splitlines() if l[3:].strip().endswith(".png")]
    return [f for f in fs if os.path.exists(f) and not f.endswith("-4k.png") and max(Image.open(f).size) < 3000]

def run(model, img):
    x = torch.from_numpy(np.asarray(img, dtype=np.float32) / 255).permute(2, 0, 1)[None]
    _, _, h, w = x.shape; s = 4
    out = torch.zeros(1, 3, h * s, w * s)
    with torch.no_grad():
        for y in range(0, h, TILE):
            for x0 in range(0, w, TILE):
                y1, x1 = max(y - PAD, 0), max(x0 - PAD, 0)
                y2, x2 = min(y + TILE + PAD, h), min(x0 + TILE + PAD, w)
                o = model(x[:, :, y1:y2, x1:x2])
                ty, tx = (y - y1) * s, (x0 - x1) * s
                th, tw = (min(y + TILE, h) - y) * s, (min(x0 + TILE, w) - x0) * s
                out[:, :, y * s:y * s + th, x0 * s:x0 * s + tw] = o[:, :, ty:ty + th, tx:tx + tw]
    a = (out[0].clamp(0, 1).permute(1, 2, 0).numpy() * 255).round().astype(np.uint8)
    return Image.fromarray(a)

def main():
    fs = targets()
    if not fs: print("nothing to upscale"); return
    if not os.path.exists(W):
        os.makedirs(os.path.dirname(W), exist_ok=True); urllib.request.urlretrieve(URL, W)
    torch.set_num_threads(os.cpu_count() or 2)
    model = ModelLoader().load_from_file(W).eval().model
    for f in fs:
        im = Image.open(f).convert("RGB")
        k = 4 if max(im.size) < 2000 else 2  # 1K Flash images get the full 4x, 2K Pro images 2x: same output size
        big = run(model, im)
        if k != 4: big = big.resize((im.width * k, im.height * k), Image.LANCZOS)
        o = f[:-4] + "-4k.jpg"; big.save(o, quality=95, subsampling=0)
        print(f"{f} {im.size} -> {o} {big.size}")

if __name__ == "__main__":
    main()
