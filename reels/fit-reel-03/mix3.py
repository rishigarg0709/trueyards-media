import numpy as np, json, sys, subprocess, librosa
from scipy import signal
from scipy.io import wavfile
L=sys.argv[1]; C=json.load(open(f"cfg-{L}.json")); SR=44100; D=C["D"]; N=int(SR*D); rng=np.random.default_rng(7)
DROP=C["DROP"]; O=C["O"]
y,_=librosa.load("music3.mp3",sr=SR,mono=True)
tempo,beats=librosa.beat.beat_track(y=y,sr=SR,units="time")
on=librosa.onset.onset_strength(y=y,sr=SR); 
b=[x for x in beats if x>=DROP][0]; start=b-DROP   # a beat lands exactly on the drop
subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',f'{start:.3f}','-i','music3.mp3','-ar',str(SR),'-ac','2',f'm-{L}.wav'],check=True)
_,m=wavfile.read(f'm-{L}.wav'); m=m.astype(np.float64)/32768; m=np.pad(m,((0,max(0,N-len(m))),(0,0)))[:N]
_,v=wavfile.read(C["vo"]); v=v.astype(np.float64); v=v/np.max(np.abs(v)); vo=np.zeros(N); i0=int(O*SR); n=min(len(v),N-i0); vo[i0:i0+n]=v[:n]
sfx=np.zeros((N,2))
def add(x,t,g=1.0,pan=0.0):
    i=int(t*SR); n=min(len(x),N-i)
    if n<=0 or i<0:return
    sfx[i:i+n,0]+=x[:n]*g*(1-pan*.5); sfx[i:i+n,1]+=x[:n]*g*(1+pan*.5)
def bpf(x,lo,hi): return signal.sosfilt(signal.butter(2,[lo,hi],btype='band',fs=SR,output='sos'),x)
def whoosh(dur=.4,up=True,lo=400,hi=6000):
    n=int(dur*SR); x=rng.standard_normal(n); out=np.zeros(n); blk=256
    for i in range(0,n,blk):
        p=i/n; p=p if up else 1-p; fc=lo*(hi/lo)**p
        seg=x[max(0,i-512):i+blk]; yy=bpf(seg,fc*.7,min(fc*1.4,SR/2-200)); k=min(blk,n-i); out[i:i+k]=yy[-blk:][:k] if len(yy)>=blk else yy[:k]
    t=np.linspace(0,1,n); e=t**2.2 if up else (1-t)**1.6
    return out*e
def impact(g=1.0):
    n=int(.9*SR); t=np.arange(n)/SR; f=36+80*np.exp(-t*20)
    x=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*4.5); c=signal.sosfilt(signal.butter(2,2500,btype='low',fs=SR,output='sos'),rng.standard_normal(n))*np.exp(-t*28)*.5
    return np.tanh((x+c)*1.5)*g
def riser(dur):
    n=int(dur*SR); t=np.arange(n)/SR; f=180*2**(t/dur*2.5)
    return (np.sin(2*np.pi*np.cumsum(f)/SR)*.22+whoosh(dur,True,300,9000))*(t/dur)**2.4
def tick():
    n=int(.03*SR); t=np.arange(n)/SR; return bpf(rng.standard_normal(n),1800,6000)*np.exp(-t*220)
TXT=C["hook"]; t0,t1=.25,DROP-.8
for k in range(len(TXT)): add(tick(),t0+k*(t1-t0)/len(TXT),.4,rng.uniform(-.3,.3))
add(tick(),DROP-.2,.9); add(impact(.5),DROP-.2,.25); add(riser(.9),DROP-.9,.45)
add(impact(1.2),DROP,.7); add(whoosh(.5,False,300,5000),DROP,.3)
for c in C["cuts"]:
    if c>DROP+.1: add(whoosh(.24,True,800,7000),c-.24,.16,rng.uniform(-.6,.6))
for c in C["wipes"]: add(whoosh(.34,True,300,6000),c-.3,.3,-.5)
add(impact(.9),C["RERA"],.45); add(impact(1.0),C["END"],.5)
# music: low in the hook, ducked under the voice, full in gaps
env_v=np.abs(vo); k=int(.12*SR); env_v=np.convolve(env_v,np.ones(k)/k,'same'); env_v=np.clip(env_v/(np.percentile(env_v[env_v>0],90)+1e-9),0,1)
duck=1-.62*env_v; duck[:int(DROP*SR)]*=.55
fade=np.ones(N); f0=int((D-1.4)*SR); fade[f0:]=np.linspace(1,0,N-f0)**1.4
mm=m/np.max(np.abs(m))*.62
mix=mm*duck[:,None]+sfx*.7+np.stack([vo,vo],1)*.95
mix*=fade[:,None]
mix=np.tanh(mix*1.1)/np.tanh(1.1); mix=mix/np.max(np.abs(mix))*.89
wavfile.write(f'mix-{L}.wav',SR,(mix*32767).astype(np.int16)); print(L,'mix ok, music start',round(start,2),'tempo',tempo)
