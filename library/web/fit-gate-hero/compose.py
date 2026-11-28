"""Composite Flow (Veo) 720p clips onto the 4K still they started from.
Static areas come from the sharp still (exact logos, crisp gate), moving areas (trucks, people, flags) from the clip."""
import sys, subprocess, numpy as np, cv2
still_path, out_prefix, clips = sys.argv[1], sys.argv[2], sys.argv[3:]
OW, OH = 2560, 1440
# boxes (fractions of the frame) that always show the sharp still: FIT logo+plaque, Forteasia logo, canopy letters
PROTECT = [(0.195, 0.41, 0.285, 0.55), (0.695, 0.52, 0.785, 0.635), (0.33, 0.345, 0.645, 0.43)]
S = cv2.imread(still_path)
H, W = S.shape[:2]

def align(f0):
    fh, fw = f0.shape[:2]
    sc = fw / W
    s_small = cv2.resize(S, (fw, int(round(H * sc))), interpolation=cv2.INTER_AREA)
    g1 = cv2.cvtColor(f0, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
    g2 = cv2.cvtColor(s_small, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
    M = np.eye(2, 3, dtype=np.float32); M[1, 2] = (g2.shape[0] - fh) / 2
    cc, M = cv2.findTransformECC(g1, g2, M, cv2.MOTION_AFFINE,
                                 (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 500, 1e-6), None, 5)
    k = OW / fw
    T = np.array([[M[0, 0] / k / sc, M[0, 1] / k / sc, M[0, 2] / sc],
                  [M[1, 0] / k / sc, M[1, 1] / k / sc, M[1, 2] / sc]], np.float32)
    return cc, cv2.warpAffine(S, T, (OW, OH), flags=cv2.INTER_AREA | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REPLICATE)

enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{OW}x{OH}', '-r', '24', '-i', '-',
                        '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', f'{out_prefix}-master.mp4'],
                       stdin=subprocess.PIPE)
for clip in clips:
    cap = cv2.VideoCapture(clip)
    ok, f0 = cap.read()
    cc, SH = align(f0)
    print(clip, 'align cc', round(cc, 4))
    up0 = cv2.resize(f0, (OW, OH), interpolation=cv2.INTER_CUBIC).astype(np.float32)
    shf = SH.astype(np.float32)
    # per-channel colour match of the clip to the still
    gain = []; 
    for c in range(3):
        a, b = np.polyfit(up0[..., c].ravel()[::97], shf[..., c].ravel()[::97], 1); gain.append((a, b))
    small = (640, 360)
    s_small = cv2.GaussianBlur(cv2.resize(SH, small, interpolation=cv2.INTER_AREA).astype(np.float32), (0, 0), 1.6)
    prev = None; f = f0; n = 0
    while ok:
        up = cv2.resize(f, (OW, OH), interpolation=cv2.INTER_LANCZOS4).astype(np.float32)
        for c in range(3):
            up[..., c] = up[..., c] * gain[c][0] + gain[c][1]
        fs = cv2.GaussianBlur(cv2.resize(np.clip(up, 0, 255).astype(np.uint8), small, interpolation=cv2.INTER_AREA).astype(np.float32), (0, 0), 1.6)
        d = np.abs(fs - s_small).max(axis=2)
        m = np.clip((d - 9) / 14, 0, 1)
        m = cv2.dilate(m, np.ones((7, 7), np.uint8))
        m = cv2.GaussianBlur(m, (0, 0), 3)
        m[:4, :] = 0; m[-4:, :] = 0; m[:, :4] = 0; m[:, -4:] = 0
        m[int(360*0.93):, int(640*0.92):] = 0   # Veo watermark corner
        for (x0, y0, x1, y1) in PROTECT:          # logos and canopy lettering always come from the still
            m[int(y0*360):int(y1*360), int(x0*640):int(x1*640)] = 0
        if prev is not None: m = np.maximum(m, prev * 0.6)
        prev = m
        M = cv2.resize(m, (OW, OH), interpolation=cv2.INTER_LINEAR)[..., None]
        out = up * M + shf * (1 - M)
        enc.stdin.write(np.clip(out, 0, 255).astype(np.uint8).tobytes())
        n += 1
        ok, f = cap.read()
    print(clip, 'frames', n)
enc.stdin.close(); enc.wait()
