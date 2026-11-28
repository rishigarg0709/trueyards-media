import json,re
h=open('_head.part').read(); sc=open('_scenes.part').read(); o=open('_outro.part').read(); tl=open('_tail.part').read()
W=open('words.json').read().strip(); B=json.load(open('beats.json'))['beats']
h=re.sub(r"const WS=/\*WS\*/.*?;\n","const WS=/*WS*/"+W+";\n",h,flags=re.S)
h=re.sub(r"const BEATS=/\*BEATS\*/.*?;\n","const BEATS=/*BEATS*/"+json.dumps(B)+";\n",h,flags=re.S)
AIL="AI visualisation, representational, not a real project."
REAL="Real photo / Unsplash."
A1="Anarock via PTI (Jun 2022): stuck or delayed, projects launched 2014 or earlier."
fine=("const AIL='"+AIL+"';const REAL='"+REAL+"';const FINE=[[0,AIL],[SC[1].t0,AIL+' '+'"+A1+"'],[SC[2].t0,REAL+' '+'"+A1+"'],"
 "[SC[3].t0,AIL],[SC[4].t0,AIL+' Anarock: 220 fully stalled projects, 1.74 lakh homes, about 66% sold.'],[SC[5].t0,REAL+' Liases Foras via Business Standard (Sep 2022). Builder not named.'],"
 "[SC[6].t0,AIL+' Business Standard, Sep 2022: lenders fund 3 to 4 years, projects take 7 to 8.'],[SC[7].t0,AIL],[SC[8].t0,AIL],"
 "[SC[9].t0,AIL+' SWAMIH fund, Nov 2019.'],[SC[10].t0,AIL+' Ministry of Finance, Jan 2026: about 61,000 homes by 15 Dec 2025.'],[SC[11].t0,REAL],[SC[12].t0,AIL+' Education only, not advice.'],[OST,'']];")
tl=re.sub(r"const AIL='AI visualisation.';","",tl)
tl=re.sub(r"const FINE=\[.*?\];",lambda m:fine,tl,flags=re.S)
tl=re.sub(r"const FLASH=\[.*?\];","const FLASH=[HOOKEV,wt('bik'),wt('fund'),wt('kisi')];",tl)
open('reel.html','w').write(h+sc+o+tl); print('ok')
