"""Mix narration + beat-aligned music + hits. usage: python3 mix.py <reel_dir> <music.mp3> [duration]
Reads <dir>/vo.wav, <dir>/beats.json (offset), optional <dir>/hits.json [{"t":2.08,"type":"boom"|"whoosh"|"riser"}].
Music is ducked ~9 dB under the voice. Writes <dir>/audio.wav."""
import json, subprocess, sys, os, numpy as np, soundfile as sf
d, mus = sys.argv[1], sys.argv[2]
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', mus, '-ar', '44100', '-ac', '1', f'{d}/_mus.wav'], check=True)
vo, sr = sf.read(f'{d}/vo.wav'); m, _ = sf.read(f'{d}/_mus.wav'); B = json.load(open(f'{d}/beats.json'))
m = m[int(B['offset'] * sr):]
W = json.load(open(f'{d}/words.json')); D = float(sys.argv[3]) if len(sys.argv) > 3 else W[-1][2] + 2.3
N = int(D * sr); v = np.zeros(N); v[:min(N, len(vo))] = vo[:N]; mu = np.zeros(N); k = min(N, len(m)); mu[:k] = m[:k]
fr = int(.04 * sr); env = np.array([np.sqrt((v[i:i + fr] ** 2).mean()) for i in range(0, N, fr)])
act = (env > env.max() * .04).astype(float); act = np.clip(np.convolve(act, np.ones(7) / 7, 'same') * 1.6, 0, 1)
g = np.repeat(1 - act * (1 - 10 ** (-9 / 20)), fr)[:N]
mv = np.sqrt((mu[mu != 0] ** 2).mean()) if mu.any() else 1; vv = np.sqrt((v[v != 0] ** 2).mean())
mix = v + mu * g * (vv / mv) * .42; R = np.random.default_rng(3)
def add(t, x):
    i = int(t * sr); j = min(N, i + len(x));
    if i < N: mix[i:j] += x[:j - i]
tt = lambda s: np.arange(int(s * sr)) / sr
hits = json.load(open(f'{d}/hits.json')) if os.path.exists(f'{d}/hits.json') else []
for h in hits:
    t = h['t']
    if h['type'] == 'boom': x = tt(.7); add(t, np.sin(2 * np.pi * (52 + 40 * np.exp(-x * 16)) * x) * .5 * np.exp(-x * 5))
    elif h['type'] == 'whoosh': x = tt(.45); add(t - .2, np.convolve(R.standard_normal(len(x)), np.ones(30) / 30, 'same') * np.sin(np.pi * x / .45) * .2)
    elif h['type'] == 'riser': x = tt(1.2); add(t - 1.2, np.convolve(R.standard_normal(len(x)), np.ones(40) / 40, 'same') * .22 * (x / 1.2) ** 2)
fo = int(1.0 * sr); mix[-fo:] *= np.linspace(1, 0, fo); mix /= max(1, np.abs(mix).max() / .95)
sf.write(f'{d}/audio.wav', mix, sr); print('audio', round(D, 2), 's')
