# usage: python3 slice.py <panorama.png> <n_slides> <name> [out_dir]
# Panorama is rendered by multi.cjs at scale 2 (2160x2700 per slide). Writes:
#   <out>/master/<name>-slide-N.jpg  full-res 4K-class masters (2160x2700)
#   <out>/<name>-slide-N.jpg         1440x1800 Instagram/Facebook/Threads exports (Meta API max image width is 1440)
import sys,os
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
f,n,name=sys.argv[1],int(sys.argv[2]),sys.argv[3]
im=Image.open(f).convert('RGB'); w=im.width//n
if im.height<2700: print(f'WARN panorama is {im.height}px tall; render with multi.cjs scale 2 for 4K-class masters')
if len(sys.argv)>4:
    o=sys.argv[4]; os.makedirs(f'{o}/master',exist_ok=True)
    for i in range(n):
        s=im.crop((i*w,0,(i+1)*w,im.height))
        s.save(f'{o}/master/{name}-slide-{i+1}.jpg',quality=96,subsampling=0)
        s.resize((1440,1800),Image.LANCZOS).save(f'{o}/{name}-slide-{i+1}.jpg',quality=95,subsampling=0)
    im.resize((1440*n,1800),Image.LANCZOS).save(f'{o}/{name}-full-panorama.jpg',quality=90)
cols=4; rows=(n+cols-1)//cols
sh=Image.new('RGB',(cols*548,rows*685),(40,40,40))
for i in range(n): sh.paste(im.crop((i*w,0,(i+1)*w,im.height)).resize((540,675),Image.LANCZOS),((i%cols)*548+4,(i//cols)*685+5))
sh.save(f.replace('.png','-sheet.jpg'),quality=84)
