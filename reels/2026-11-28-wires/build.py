import json,re
t=open('reel.tpl.html').read()
# look E Blueprint palette
for a,b in [('#0D0D0F','#0C2340'),('rgba(13,13,15','rgba(12,35,64'),('#E63B2E','#4FD1FF'),('rgba(230,59,46','rgba(79,209,255'),('#FFD2CC','#4FD1FF'),('#FFF4F2','#F2FBFF'),('rgba(4,4,6,.38)','rgba(4,12,24,.30)')]:
    t=t.replace(a,b)
t=t.replace('.hl{background:#4FD1FF;color:#fff;','.hl{background:#4FD1FF;color:#0C2340;')
t=t.replace('.dg{background:#4FD1FF;color:#fff;','.dg{background:#4FD1FF;color:#0C2340;')
t=t.replace('.stamp{border:6px solid #4FD1FF;color:#4FD1FF;','.stamp{border:6px solid #4FD1FF;color:#fff;').replace('background:rgba(79,209,255,.18);white-space','background:rgba(12,35,64,.62);white-space')
t=t.replace('.H{font:900 100px/1.0 IN;letter-spacing:-.02em;text-transform:uppercase}','.H{font:800 100px/1.02 IN;letter-spacing:-.035em}\n.HK{font:900 100px/1.0 IN;letter-spacing:-.035em;color:#fff;text-shadow:0 6px 34px rgba(0,0,0,.85),0 2px 6px rgba(0,0,0,.7)}\n.HK .hl{padding:0 .1em;border-radius:12px;text-shadow:none}')
a=t.index("const HOOKEV=");b=t.index("const scenes=SC.map")
head=t[:a];tail=t[b:]
sc=open('_scenes.js').read()
W=open('words.json').read().strip();B=json.load(open('beats.json'))['beats']
head=re.sub(r"const WS=.*?;\n","const WS="+W+";\n",head,count=1,flags=re.S)
head=re.sub(r"const BEATS=.*?;\n","const BEATS="+json.dumps(B)+";\n",head,count=1,flags=re.S)
AIL="AI visualisation."
REAL="Real photo: Unsplash."
B1="BESCOM via PTI, 6 Jul 2024."
B2="BESCOM survey, Deccan Herald, 19 Jul 2024."
fine=("const AIL='"+AIL+"';const REAL='"+REAL+"';const FINE=[[0,AIL],[SC[1].t0,REAL],[SC[2].t0,AIL+' Power lines usually on top; not every pole.'],[SC[3].t0,AIL],[SC[4].t0,AIL],[SC[5].t0,REAL+' "+B1+"'],[SC[6].t0,AIL+' "+B1+"'],[SC[7].t0,AIL+' "+B2+"'],[SC[8].t0,REAL+' "+B2+"'],[SC[9].t0,AIL],[SC[10].t0,REAL+' Deccan Herald, Jul 2024.'],[SC[11].t0,AIL],[SC[12].t0,AIL+' Not a real street.'],[SC[13].t0,AIL+' Education only, not advice.'],[END-1.8,'']];")
tail=re.sub(r"const AIL=.*?const FINE=\[.*?\];",lambda m:fine,tail,count=1,flags=re.S)
tail=tail.replace(" floors(t);\n","\n")
tail=re.sub(r"\[HOOKEV,wt\('thirty-four'\).*?\]\.forEach","[HOOKEV,wt('two'),wt('or'),wt('back'),wt('wi-fi')].forEach",tail,count=1)
open('reel.html','w').write(head+sc+tail);print('ok')
