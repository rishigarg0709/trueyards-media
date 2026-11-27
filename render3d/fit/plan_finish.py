import numpy as np
from PIL import Image, ImageFilter, ImageChops
B=Image.open('/home/claude/trueyards-media/library/media/fitweb-plan-exact-b.png').convert('RGB')
H=Image.open('holes-4k.png')
out=B.copy()
# each Others Land parcel becomes plain farmland copied from the open fields at the top right (not part of FIT)
lab=np.array(H)>0
import cv2
n,cc,st,_=cv2.connectedComponentsWithStats(lab.astype(np.uint8))
donors=[(3150,40),(3150,520)]
for i in range(1,n):
    x,y,w,h,a=st[i]
    dx,dy=donors[(i-1)%len(donors)]
    patch=B.crop((dx,dy,dx+w,dy+h))
    m=Image.fromarray(((cc[y:y+h,x:x+w]==i)*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3))
    out.paste(patch,(x,y),m)
    print('hole',i,x,y,w,h)
out.save('/home/claude/zones/plan-exact-4k.png')
out.save('/home/claude/trueyards/public/fit/v2/plan-exact-4k.webp','WEBP',quality=84,method=6)
out.resize((2400,2400),Image.LANCZOS).save('/home/claude/trueyards/public/fit/v2/plan-exact.webp','WEBP',quality=86,method=6)
# zone masks at 2400: white with soft alpha, grown a little so the glow wraps each building
for z in ('industrial','residential','commercial'):
    m=Image.open(f'{z}-4k.png').filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(2)).resize((2400,2400),Image.LANCZOS)
    rgba=Image.new('RGBA',(2400,2400),(255,255,255,0)); rgba.putalpha(m)
    rgba.save(f'/home/claude/trueyards/public/fit/v2/zone-{z}.png',optimize=True)
out.crop((2100,2700,3500,3800)).resize((700,550)).save('/tmp/holefix.jpg',quality=82)
