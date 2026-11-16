"""Beat-align a music track. usage: python3 beats.py <music.mp3> <anchor_seconds> <out beats.json>
Finds beats + downbeats and an offset (seconds to skip at the start of the track) so that a downbeat
lands exactly on anchor_seconds of the reel (e.g. the hook's key word). Writes {offset, beats, down, tempo}."""
import json, sys, numpy as np, librosa
mus, anchor, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
y, sr = librosa.load(mus, sr=22050)
tempo, b = librosa.beat.beat_track(y=y, sr=sr, units='time')
oe = librosa.onset.onset_strength(y=y, sr=sr); ft = librosa.times_like(oe, sr=sr)
stv = np.array([oe[np.argmin(abs(ft - x))] for x in b]); ph = [stv[k::4].mean() for k in range(4)]; k = int(np.argmax(ph))
down = b[k::4]; c = [d for d in down if 0 <= d - anchor <= 4] or [d for d in down if d >= anchor] or [anchor]
o = float(c[0] - anchor)
json.dump({'offset': o, 'tempo': float(np.atleast_1d(tempo)[0]), 'beats': [round(float(x - o), 3) for x in b if x - o >= 0],
           'down': [round(float(d - o), 3) for d in down if d - o >= 0]}, open(out, 'w'))
print('tempo', np.round(tempo, 1), 'offset', round(o, 3), 'beats', len(b))
