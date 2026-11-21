# HK tiny homes reel: trim silent word onsets and tails, cap gaps, speed up; write vo.wav + words.json
import json, sys, subprocess, numpy as np, soundfile as sf
SP, D, SPEED, GAP = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
W = json.load(open(SP+'/words.json')); v, sr = sf.read(SP+'/vo.wav')
if v.ndim>1: v=v.mean(1)
fr = int(.01*sr)
def env(s,e):
    seg=v[int(s*sr):int(e*sr)]
    return np.array([np.sqrt((seg[i:i+fr]**2).mean()) for i in range(0,max(1,len(seg)-fr),fr)])
def trim(s,e):
    r=env(s,e)
    if not len(r) or r.max()==0: return s,e
    on=r>r.max()*.08; a=np.argmax(on); b=len(on)-np.argmax(on[::-1])
    s2=s+max(0,a-2)*.01 if e-s>.4 else s
    e2=min(e,s+(b+4)*.01) if e-s>.4 else e
    return s2,e2
parts=[]; out=[]; t=0
for i,(w,s,e) in enumerate(W):
    s2,e2=trim(s,e)
    if i:
        pe=out_e
        g=v[int(pe*sr):int((pe+min(max(s2-pe,0),GAP))*sr)]; parts.append(g); t+=len(g)/sr
    seg=v[int(s2*sr):int(e2*sr)].copy(); f=int(.006*sr)
    if len(seg)>2*f: seg[:f]*=np.linspace(0,1,f); seg[-f:]*=np.linspace(1,0,f)
    parts.append(seg); out.append([w,t,t+len(seg)/sr]); t+=len(seg)/sr; out_e=e2
parts.append(np.zeros(int(.15*sr)))
sf.write(SP+'/vo_cut.wav', np.concatenate(parts), sr)
subprocess.run(['ffmpeg','-y','-v','error','-i',SP+'/vo_cut.wav','-filter:a',f'atempo={SPEED}','-ar','44100',D+'/vo.wav'],check=True)
json.dump([[x[0],round(x[1]/SPEED,3),round(x[2]/SPEED,3)] for x in out], open(D+'/words.json','w'))
o=json.load(open(D+'/words.json')); print('words',len(o),'end',o[-1][2])
