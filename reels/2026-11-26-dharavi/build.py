import json,re
h=open('_head.part').read(); sc=open('_scenes.part').read(); o=open('_outro.part').read(); tl=open('_tail.part').read()
W=open('words.json').read().strip(); B=json.load(open('beats.json'))['beats']
h=re.sub(r"const WS=/\*WS\*/.*?;\n","const WS=/*WS*/"+W+";\n",h,flags=re.S)
h=re.sub(r"const BEATS=/\*BEATS\*/.*?;\n","const BEATS=/*BEATS*/"+json.dumps(B)+";\n",h,flags=re.S)
o=o.replace("url(img/m1.jpg)","url(img/tarps.jpg)")
fine="const FINE=[[0,REAL],[SC[1].t0,AIL+' Population estimates 3 to 10 lakh; area about 2.39 sq km (Oneindia, FPJ, May 2025).'],[SC[2].t0,AIL],[SC[3].t0,REAL+' Towers beside older low-rise.'],[SC[4].t0,AIL+' Model. Master plan approved May 2025 (Business Standard; Oneindia).'],[SC[5].t0,AIL+' 58,532 homes + 13,468 commercial and industrial units (Oneindia; Business Standard).'],[SC[6].t0,AIL],[SC[7].t0,AIL+' Eligible ground-floor structures built on or before 1 Jan 2000: 350 sq ft at no cost under the scheme (Business Standard; Business Today, Jul 2026).'],[SC[8].t0,REAL+' About 9.5 crore sq ft of rehab homes before about 13 crore sq ft of saleable space (Business Today, Jul 2026).'],[SC[9].t0,AIL+' Operator: joint venture of the Maharashtra government and a private developer.'],[SC[10].t0,AIL+' Phase 1 target, Chief Minister in the Assembly (Business Today, Jul 2026).'],[SC[11].t0,REAL+' Education only, not advice.'],[OST,'']];"
fine=fine.replace("const FINE=","const AIL='AI visualisation, representational, not actual photos of Dharavi.';const REAL='Photo: Mumbai, not Dharavi. Zoshua Colah, Kunal Kalra / Unsplash.';const FINE=")
tl=tl.replace("const AIL='AI visualisation.';","")
tl=re.sub(r"const FINE=\[.*?\];",fine,tl,flags=re.S)
tl=re.sub(r"const FLASH=\[.*?\];","const FLASH=[HOOKEV,wt('dharavi'),wt('may'),wt('free'),wt('sold')];",tl)
open('reel.html','w').write(h+sc+o+tl); print('ok')
