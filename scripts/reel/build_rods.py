# one-off builder for reels/2026-11-18-roof-rods: injects words/beats into reel.tpl.html (main) and builds the trial twin dir
import json, sys, os, subprocess, numpy as np, soundfile as sf, shutil
D='reels/2026-11-18-roof-rods'; TD=D+'-trial'; SP=sys.argv[1]; SPEED=1.05; BODY=10
tpl=open(D+'/reel.tpl.html').read(); W=json.load(open(D+'/words.json')); B=json.load(open(D+'/beats.json'))['beats']
r=lambda ws: json.dumps([[w[0],round(w[1],3),round(w[2],3)] for w in ws])
def make(ws,trial): return tpl.replace('/*TRIAL*/false','true' if trial else 'false').replace('/*WS*/[]',r(ws)).replace('/*BEATS*/[]',json.dumps(B))
open(D+'/reel.html','w').write(make(W,False))
subprocess.run(['ffmpeg','-y','-v','error','-i',SP+'/trial/vo.wav','-filter:a',f'atempo={SPEED}','-ar','44100',SP+'/trial/vo_f.wav'],check=True)
TW=[[a,b/SPEED,c/SPEED] for a,b,c in json.load(open(SP+'/trial/words.json'))][:BODY]
os.makedirs(TD,exist_ok=True); WT=TW+W[BODY:]
open(TD+'/reel.html','w').write(make(WT,True)); json.dump(WT,open(TD+'/words.json','w'))
for f in ('beats.json','hits.json'): shutil.copy(D+'/'+f,TD+'/'+f)
if not os.path.exists(TD+'/img'): os.symlink(os.path.abspath(D+'/img'),TD+'/img')
v,sr=sf.read(D+'/vo.wav'); tv,_=sf.read(SP+'/trial/vo_f.wav'); cut=int((W[BODY][1]-.06)*sr); tcut=int((TW[-1][2]+.05)*sr)
out=np.zeros(len(v)); n=min(tcut,cut); f=int(.01*sr); seg=tv[:n].copy(); seg[-f:]*=np.linspace(1,0,f); out[:n]=seg; out[cut:]=v[cut:]; sf.write(TD+'/vo.wav',out,sr)
print('ok trial hook end', round(TW[-1][2],2), 'main body', W[BODY][1])
