# one-off: from take 2 (vo_align output), cut words, trim silent word onsets, speed up; write vo.wav + words.json
import json, sys, subprocess, numpy as np, soundfile as sf
SP, D, SPEED = sys.argv[1], sys.argv[2], 1.1
W = json.load(open(SP+'/words.json')); v, sr = sf.read(SP+'/vo.wav')
CUT = set(range(21,26)) | set(range(98,104)) | {127}
fr = int(.01*sr)
def onset(s, e):  # first 10 ms frame above 10% of the word's peak
    seg = v[int(s*sr):int(e*sr)]
    r = np.array([np.sqrt((seg[i:i+fr]**2).mean()) for i in range(0, max(1,len(seg)-fr), fr)])
    if not len(r): return s
    k = np.argmax(r > r.max()*.10); return s + max(0, k-3)*.01
parts=[]; out=[]; t=0; prev_end=None
for i,(w,s,e) in enumerate(W):
    if i in CUT: continue
    s2 = onset(s,e) if e-s > .45 else s
    if prev_end is not None:
        gap = s - prev_end  # natural gap before the original start, keep it (max .3)
        g = v[int(prev_end*sr):int((prev_end+min(gap,.3))*sr)]; parts.append(g); t += len(g)/sr
    seg = v[int(s2*sr):int(e*sr)]; f=int(.006*sr)
    if len(seg)>2*f: seg=seg.copy(); seg[:f]*=np.linspace(0,1,f)
    parts.append(seg); out.append([w, t, t+len(seg)/sr]); t += len(seg)/sr; prev_end = e
parts.append(v[int(prev_end*sr):int((prev_end+.12)*sr)])
sf.write(SP+'/vo_cut.wav', np.concatenate(parts), sr)
subprocess.run(['ffmpeg','-y','-v','error','-i',SP+'/vo_cut.wav','-filter:a',f'atempo={SPEED}','-ar','44100',D+'/vo.wav'],check=True)
json.dump([[x[0],round(x[1]/SPEED,3),round(x[2]/SPEED,3)] for x in out], open(D+'/words.json','w'))
o=json.load(open(D+'/words.json')); print('words',len(o),'end',o[-1][2])
for i,x in enumerate(o): print(i,x[0],x[1],end=' | ')
