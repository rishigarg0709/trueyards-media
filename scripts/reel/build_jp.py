# one-off builder for reels/2026-11-17-japan-houses: injects words/beats into reel.tpl.html (main) and builds the trial twin dir
import json, sys, os, numpy as np, soundfile as sf, shutil
D='reels/2026-11-17-japan-houses'; TD=D+'-trial'; SP=sys.argv[1]
tpl=open(D+'/reel.tpl.html').read(); W=json.load(open(D+'/words.json')); B=json.load(open(D+'/beats.json'))['beats']
r=lambda ws: json.dumps([[w[0],round(w[1],3),round(w[2],3)] for w in ws])
def make(ws,body,trial): return tpl.replace('/*TRIAL*/false','true' if trial else 'false').replace('/*WS*/[]',r(ws)).replace('/*BODY*/15',str(body)).replace('/*BEATS*/[]',json.dumps(B))
open(D+'/reel.html','w').write(make(W,15,False))
TW=json.load(open(SP+'/trial/words.json')); os.makedirs(TD,exist_ok=True)
open(TD+'/reel.html','w').write(make(TW+W[15:],len(TW),True))
json.dump(TW+W[15:],open(TD+'/words.json','w'))
for f in ('beats.json','hits.json'): shutil.copy(D+'/'+f,TD+'/'+f)
if not os.path.exists(TD+'/img'): os.symlink(os.path.abspath(D+'/img'),TD+'/img')
v,sr=sf.read(D+'/vo.wav'); tv,_=sf.read(SP+'/trial/vo.wav'); cut=int((W[15][1]-.06)*sr)
out=np.zeros(len(v)); n=min(len(tv),cut); out[:n]=tv[:n]; out[cut:]=v[cut:]; sf.write(TD+'/vo.wav',out,sr)
h=json.load(open(D+'/hits.json')); 
print('ok', len(TW), 'trial vo', round(len(tv)/sr,2), 'cut', W[15][1])
