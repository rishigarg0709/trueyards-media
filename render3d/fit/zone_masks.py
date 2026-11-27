import json
from PIL import Image, ImageDraw, ImageFilter
L=json.load(open('/home/claude/trueyards-media/render3d/fit/layout.json'))
S=4096; SC=1400.0; CX,CY=-68.0,40.0
def px(x,y): return ((x-(CX-SC/2))/SC*S, ((CY+SC/2)-y)/SC*S)
Z={'industrial':('shed','office'),'residential':('res',),'commercial':('sco',)}
out={}
for z,ks in Z.items():
    m=Image.new('L',(S,S),0); d=ImageDraw.Draw(m)
    for b in L['buildings']:
        if b['k'] not in ks: continue
        x0,y0=px(b['x']-b['w']/2,b['y']+b['d']/2); x1,y1=px(b['x']+b['w']/2,b['y']-b['d']/2)
        d.rectangle([x0,y0,x1,y1],fill=255)
    m.save(f'{z}-4k.png'); out[z]=m
holes=Image.new('L',(S,S),0); d=ImageDraw.Draw(holes)
for poly in L['holes']:
    d.polygon([px(*p) for p in poly[0]],fill=255)
holes.save('holes-4k.png')
B=Image.open('/home/claude/trueyards-media/library/media/fitweb-plan-exact-b.png').convert('RGB')
vis=B.copy()
cols={'industrial':(255,60,0),'residential':(0,200,255),'commercial':(255,0,200)}
for z,m in out.items():
    vis.paste(Image.new('RGB',(S,S),cols[z]),(0,0),m.point(lambda v: 110 if v else 0))
vis.paste(Image.new('RGB',(S,S),(255,255,0)),(0,0),holes.point(lambda v:120 if v else 0))
vis.resize((1400,1400)).save('/tmp/align.jpg',quality=82)
vis.crop((2200,2600,3400,3600)).save('/tmp/align-crop.jpg',quality=82)
