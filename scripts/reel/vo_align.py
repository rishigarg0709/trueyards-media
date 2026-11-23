"""Trim an ElevenLabs narration and export word timings.
usage: python3 vo_align.py <voice.mp3> <voice.align.json> <out_dir> [max_gap=0.3]
writes <out_dir>/vo.wav (44.1k mono) and <out_dir>/words.json ([[word,start,end],...] on the trimmed audio)
[pause]-style tags are ignored; pauses longer than max_gap are cut down to max_gap."""
import json, subprocess, sys, numpy as np, soundfile as sf
mp3, al, out = sys.argv[1:4]; MAXG = float(sys.argv[4]) if len(sys.argv) > 4 else .3
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', mp3, '-ar', '44100', '-ac', '1', f'{out}/_vo_raw.wav'], check=True)
a = json.load(open(al)); ch, st, en = a['characters'], a['character_start_times_seconds'], a['character_end_times_seconds']
words = []; cur = None; inb = False
for c, s, e in zip(ch, st, en):
    if c == '[': inb = True; continue
    if c == ']': inb = False; continue
    if inb: continue
    if c.isspace():
        if cur: words.append(cur); cur = None
        continue
    if cur is None: cur = [c, s, e]
    else: cur[0] += c; cur[2] = e
if cur: words.append(cur)
h, sr = sf.read(f'{out}/_vo_raw.wav'); fr = int(.01 * sr)
def eend(s, e):
    seg = h[int(s * sr):int(e * sr)]
    if len(seg) < fr * 3: return e
    r = [np.sqrt((seg[i:i + fr] ** 2).mean()) for i in range(0, len(seg) - fr, fr)]; pk = max(r); idx = [i for i, x in enumerate(r) if x > pk * .08]
    return min(e, s + (idx[-1] + 2) * .01) if idx else e
pe = max(0, words[0][1] - .02); outw = []; nw = []
for i, (w, s, e) in enumerate(words):
    gap = s - pe; keep = min(gap, MAXG) if i else 0
    if gap > keep: hk = keep / 2; outw += [h[int(pe * sr):int((pe + hk) * sr)], h[int((s - hk) * sr):int(s * sr)]]
    else: outw.append(h[int(pe * sr):int(s * sr)])
    t = sum(len(x) for x in outw) / sr
    e2 = eend(s, e) if (i + 1 == len(words) or words[i + 1][1] - e > .25 or w.endswith(('.', ',', '...', '?', '!'))) else e
    outw.append(h[int(s * sr):int(e2 * sr)]); nw.append([w, round(t, 3), round(t + e2 - s, 3)]); pe = e2
outw.append(h[int(pe * sr):int((pe + .12) * sr)]); vo = np.concatenate(outw); f = int(.015 * sr); vo[-f:] *= np.linspace(1, 0, f)
sf.write(f'{out}/vo.wav', vo, sr); json.dump(nw, open(f'{out}/words.json', 'w'))
print('words', len(nw), 'duration', round(len(vo) / sr, 2))
