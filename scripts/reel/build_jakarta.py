# one-off: cut "So why is it sinking?" from take 2, speed 1.15x, write vo.wav + words.json for reels/2026-11-18-jakarta-sinking
import json, sys, subprocess, numpy as np, soundfile as sf
SP, D, SPEED = sys.argv[1], sys.argv[2], 1.15
W = json.load(open(SP+'/words.json')); v, sr = sf.read(SP+'/vo.wav')
a = next(i for i,x in enumerate(W) if x[0]=='So' and W[i+1][0]=='why'); b = a+5  # words a..a+4 = So why is it sinking?
c0, c1 = W[a][1]-.02, W[b][1]-.02; n0, n1 = int(c0*sr), int(c1*sr); d = c1-c0
v2 = np.concatenate([v[:n0], v[n1:]]); f=int(.008*sr); v2[n0-f:n0]*=np.linspace(1,.0,f); v2[n0:n0+f]*=np.linspace(0,1,f)
sf.write(SP+'/vo_cut.wav', v2, sr)
subprocess.run(['ffmpeg','-y','-v','error','-i',SP+'/vo_cut.wav','-filter:a',f'atempo={SPEED}','-ar','44100',D+'/vo.wav'],check=True)
out = [[x[0], x[1]/SPEED, x[2]/SPEED] for x in W[:a]] + [[x[0], (x[1]-d)/SPEED, (x[2]-d)/SPEED] for x in W[b:]]
json.dump([[x[0],round(x[1],3),round(x[2],3)] for x in out], open(D+'/words.json','w'))
print('words', len(out), 'end', round(out[-1][2],2))
for i,x in enumerate(out): print(i, x[0], round(x[1],2))
