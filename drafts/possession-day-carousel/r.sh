node ../../engine/multi.cjs pd.html 7 2 && python3 ../../engine/slice.py pd.png 7 pd out && python3 -c "
from PIL import Image;Image.MAX_IMAGE_PIXELS=None
im=Image.open('pd.png');im.resize((2520,450)).save('/tmp/claude-0/s/strip.jpg',quality=88)
for k in [1,2,5,7]: Image.open(f'out/pd-slide-{k}.jpg').resize((720,900)).save(f'/tmp/claude-0/s/s{k}.jpg',quality=88)"
