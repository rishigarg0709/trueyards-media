import numpy as np
from PIL import Image, ImageOps
Image.MAX_IMAGE_PIXELS=None
exec(open('proc.py').read().split("M='/home/claude/trueyards-media/library/media/2026-11-25-carousel-%s-4k.jpg'")[0].split('def proc')[0])
M='/home/claude/trueyards-media/library/media/2026-11-25-carousel-%s-4k.jpg'
def white(k,box,out,maxw):
    im=Image.open(M%k).convert('RGB'); W,H=im.size
    im=im.crop((int(box[0]*W),int(box[1]*H),int(box[2]*W),int(box[3]*H)))
    im=im.resize((maxw,int(im.height*maxw/im.width)),Image.LANCZOS)
    a=np.asarray(im).astype(float); bg=bgfit(a)
    o=(a*255/np.clip(bg,1,None)).clip(0,255)
    d=(255-o).sum(2,keepdims=True); k2=np.clip((d-8)/18,0,1); o=o*k2+255*(1-k2)
    h,w,_=o.shape; ry=np.minimum(ramp(h,.08,(1,0)),ramp(h,.08,(0,1))); rx=np.minimum(ramp(w,.08,(1,0)),ramp(w,.08,(0,1)))
    al=np.outer(ry,rx)[...,None]; o=o*al+255*(1-al)
    Image.fromarray(o.astype('uint8')).save(O+out,quality=94); print(out,w,h)
white('3',(.12,.12,.98,.92),'tools.jpg',1400)
white('5',(.05,.25,.95,.93),'clip.jpg',1400)
im=Image.open(O+'pano1.png'); ImageOps.mirror(im).save(O+'pano1f.png')
