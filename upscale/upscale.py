"""Real-ESRGAN x4 on CPU with tiling. Usage: python upscale.py <in_dir> <out_dir> <frame numbers comma separated>"""
import sys, os, torch, numpy as np
from PIL import Image
from spandrel import ModelLoader
torch.set_num_threads(os.cpu_count())
m = ModelLoader().load_from_file('RealESRGAN_x4plus.pth').eval()
src, dst, ids = sys.argv[1], sys.argv[2], [int(x) for x in sys.argv[3].split(',') if x]
os.makedirs(dst, exist_ok=True)
T, O = 320, 16
for i in ids:
    im = np.asarray(Image.open(f'{src}/f{i:04d}.png').convert('RGB')).astype(np.float32) / 255
    H, W, _ = im.shape
    out = np.zeros((H * 4, W * 4, 3), np.float32)
    x = torch.from_numpy(im).permute(2, 0, 1)[None]
    with torch.inference_mode():
        for y0 in range(0, H, T):
            for x0 in range(0, W, T):
                ya, yb = max(0, y0 - O), min(H, y0 + T + O); xa, xb = max(0, x0 - O), min(W, x0 + T + O)
                r = m(x[:, :, ya:yb, xa:xb])[0].permute(1, 2, 0).clamp(0, 1).numpy()
                cy, cx = (y0 - ya) * 4, (x0 - xa) * 4
                h, w = min(T, H - y0) * 4, min(T, W - x0) * 4
                out[y0 * 4:y0 * 4 + h, x0 * 4:x0 * 4 + w] = r[cy:cy + h, cx:cx + w]
    Image.fromarray((out * 255 + 0.5).astype(np.uint8)).save(f'{dst}/u{i:04d}.png', compress_level=3)
    print('done', i, flush=True)
