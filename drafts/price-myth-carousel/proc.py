# Flat-field each image to the bone field #EFE9DF (robust 2D background fit) and feather edges.
import numpy as np
from PIL import Image, ImageFilter
Image.MAX_IMAGE_PIXELS=None
M='/home/claude/trueyards-media/library/media/2026-11-19-carousel-%d-4k.jpg'
O='/home/claude/trueyards-media/drafts/price-myth-carousel/img/'
BONE=np.array([244,247,245],float)
def bgfit(a,deg=3,it=5):
    h,w,_=a.shape; s=np.asarray(Image.fromarray(a.astype('uint8')).resize((96,max(8,int(96*h/w))),Image.BOX)).astype(float)
    sh,sw,_=s.shape; yy,xx=np.mgrid[0:sh,0:sw]; X=(xx/(sw-1)).ravel(); Y=(yy/(sh-1)).ravel()
    A=np.stack([X**i*Y**j for i in range(deg+1) for j in range(deg+1-i)],1)
    keep=np.ones(len(X),bool); P=s.reshape(-1,3)
    for _ in range(it):
        c,*_=np.linalg.lstsq(A[keep],P[keep],rcond=None); r=np.abs(P-A@c).sum(1)
        keep=r<max(12,np.percentile(r[keep],60)*1.5)
    yy,xx=np.mgrid[0:h,0:w]; X=xx/(w-1); Y=yy/(h-1)
    out=np.zeros((h,w,3))
    for n,(i,j) in enumerate([(i,j) for i in range(deg+1) for j in range(deg+1-i)]): out+= (X**i*Y**j)[...,None]*c[n]
    return out
def ramp(n,f,ends=(1,1)):
    t=np.ones(n); m=int(n*f); x=np.linspace(0,1,m); s=x*x*(3-2*x)
    if ends[0]: t[:m]=s
    if ends[1]: t[-m:]=np.minimum(t[-m:],s[::-1])
    return t
def proc(k,box,out,maxw,fe=(.1,.1,.1,.1),cut=False,CUT=30):
    im=Image.open(M%k).convert('RGB'); W,H=im.size
    im=im.crop((int(box[0]*W),int(box[1]*H),int(box[2]*W),int(box[3]*H)))
    if im.width>maxw: im=im.resize((maxw,int(im.height*maxw/im.width)),Image.LANCZOS)
    a=np.asarray(im).astype(float); bg=bgfit(a)
    o=(a*BONE/np.clip(bg,1,None)).clip(0,255); h,w,_=o.shape
    dd=np.abs(o-BONE).sum(2,keepdims=True); k=np.clip((dd-6)/14,0,1); o=o*k+BONE*(1-k)
    l,t,r,b=fe
    al=np.outer(np.minimum(ramp(h,t,(1,0)) if t else 1,ramp(h,b,(0,1)) if b else 1)*np.ones(h),1) if False else None
    ry=np.ones(h); rx=np.ones(w)
    if t: ry=np.minimum(ry,ramp(h,t,(1,0)))
    if b: ry=np.minimum(ry,ramp(h,b,(0,1)))
    if l: rx=np.minimum(rx,ramp(w,l,(1,0)))
    if r: rx=np.minimum(rx,ramp(w,r,(0,1)))
    al=np.outer(ry,rx)
    if cut:  # object cutout: alpha from difference to the field, soft
        from scipy import ndimage as nd
        d=np.abs(o-BONE).sum(2); hard=nd.binary_closing(d>CUT,iterations=6)
        hard=nd.binary_fill_holes(hard); hard=nd.binary_opening(hard,iterations=3)
        lab,n=nd.label(hard); sz=nd.sum(hard,lab,range(1,n+1)); keep=np.isin(lab,1+np.where(sz>0.002*hard.size)[0])
        m=keep*1.0
        mi=Image.fromarray((m*255).astype('uint8')).filter(ImageFilter.GaussianBlur(5))
        al=al*np.asarray(mi)/255
    Image.fromarray(np.dstack([o,al*255]).astype('uint8'),'RGBA').save(O+out)
    print(out,o.shape[1],o.shape[0])
for k,b,n,w in [(1,(0,.22,1,1),'cover',3000),(3,(.08,.18,.92,.92),'towers',2600),(4,(.05,.12,.95,.92),'apt',2600),(5,(.1,.15,.9,.92),'scale',2600)]:
    proc(k,b,n+'.png',w,(.16,.16,.16,.12))
proc(2,(0,.36,.755,.97),'pano.png',4784,(.05,.12,.07,.06))
