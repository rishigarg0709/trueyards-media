"""Assemble upscaled frames into a seamless loop and encode 4K master plus web sizes."""
import json, glob, subprocess, numpy as np, os
from PIL import Image
j = json.load(open('upscale/job.json'))
fs = sorted(glob.glob('up/u*.png')); L = len(fs); F = j['loop_frames']
x0, y0, x1, y1 = [v * 4 for v in j['crop']]
OW = j['out_width']; OH = round(OW * (y1 - y0) / (x1 - x0) / 2) * 2
def load(i): return np.asarray(Image.open(fs[i]).convert('RGB').crop((x0, y0, x1, y1)).resize((OW, OH), Image.LANCZOS)).astype(np.float32)
os.makedirs('out', exist_ok=True)
outs = {'4k': (OW, OH)}
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{OW}x{OH}', '-r', '24', '-i', '-',
                      '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', f"out/{j['name']}-4k.mp4"], stdin=subprocess.PIPE)
for i in range(L - F):
    fr = load(i)
    if i < F:
        w = i / F; w = w * w * (3 - 2 * w); fr = load(L - F + i) * (1 - w) + fr * w
    p.stdin.write(np.clip(fr, 0, 255).astype(np.uint8).tobytes())
    if i == 0: Image.fromarray(np.clip(fr, 0, 255).astype(np.uint8)).save(f"out/{j['name']}-poster.jpg", quality=90)
p.stdin.close(); p.wait()
n = j['name']
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'out/{n}-4k.mp4', '-vf', 'scale=2560:-2:flags=lanczos', '-c:v', 'libx264', '-preset', 'slow', '-crf', '21', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', f'out/{n}-2560.mp4'], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'out/{n}-4k.mp4', '-vf', 'scale=2560:-2:flags=lanczos', '-c:v', 'libvpx-vp9', '-b:v', '0', '-crf', '31', '-row-mt', '1', '-deadline', 'good', '-cpu-used', '2', f'out/{n}-2560.webm'], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'out/{n}-4k.mp4', '-vf', 'scale=1280:-2:flags=lanczos', '-c:v', 'libx264', '-preset', 'slow', '-crf', '22', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', f'out/{n}-1280.mp4'], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'out/{n}-poster.jpg', '-vf', 'scale=2560:-2', f'out/{n}-poster-2560.jpg'], check=True)
print(os.listdir('out'))
