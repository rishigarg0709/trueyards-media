import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
NAVY=np.array([11,20,38],float)
crops={1:(0,650,3712,4500),2:(300,900,3700,4100),3:(900,2600,3712,4560),4:(300,1900,3400,4300),5:(100,2470,3450,4450)}
def ramp(n,f):
    t=np.ones(n); m=int(n*f); x=np.linspace(0,1,m); s=x*x*(3-2*x); t[:m]=s; t[-m:]=np.minimum(t[-m:],s[::-1]); return t
for k,(a,b,c,d) in crops.items():
    im=np.asarray(Image.open(f'/home/claude/trueyards-media/library/media/2026-11-17-carousel-{k}-4k.jpg').convert('RGB').crop((a,b,c,d))).astype(float)
    h,w,_=im.shape
    border=np.concatenate([im[:40].reshape(-1,3),im[-40:].reshape(-1,3),im[:,:40].reshape(-1,3),im[:,-40:].reshape(-1,3)])
    bg=np.median(border,0)
    off=np.clip(bg-NAVY,0,None)
    out=(im-off*0.95).clip(0,255)
    al=np.outer(ramp(h,.13),ramp(w,.13))*255
    o=np.dstack([out,al]).astype('uint8')
    I=Image.fromarray(o,'RGBA')
    if w>2600: I=I.resize((2600,int(h*2600/w)),Image.LANCZOS)
    I.save(f'/home/claude/trueyards-media/drafts/stamp-duty-carousel/img/s{k}.png',optimize=False)
    print(k,bg,I.size)
