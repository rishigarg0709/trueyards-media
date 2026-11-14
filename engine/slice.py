import sys,os
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
f,n,name=sys.argv[1],int(sys.argv[2]),sys.argv[3]
im=Image.open(f).convert('RGB'); s=im.height/1350; w=int(1080*s)
if len(sys.argv)>4:
    o=sys.argv[4]; os.makedirs(o,exist_ok=True)
    for i in range(n): im.crop((i*w,0,(i+1)*w,im.height)).save(f'{o}/{name}-slide-{i+1}.jpg',quality=93,subsampling=0)
    im.resize((1080*n,1350),Image.LANCZOS).save(f'{o}/{name}-full-panorama.jpg',quality=88)
cols=4; rows=(n+cols-1)//cols
sh=Image.new('RGB',(cols*548,rows*685),(40,40,40))
for i in range(n): sh.paste(im.crop((i*w,0,(i+1)*w,im.height)).resize((540,675),Image.LANCZOS),((i%cols)*548+4,(i//cols)*685+5))
sh.save(f.replace('.png','-sheet.jpg'),quality=84)
