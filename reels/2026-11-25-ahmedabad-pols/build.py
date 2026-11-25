import json,re
h=open('_head.part').read(); sc=open('_scenes.part').read(); o=open('_outro.part').read(); tl=open('_tail.part').read()
W=open('words.json').read().strip(); B=json.load(open('beats.json'))['beats']
h=re.sub(r"const WS=/\*WS\*/.*?;\n","const WS=/*WS*/"+W+";\n",h,flags=re.S)
h=re.sub(r"const BEATS=/\*BEATS\*/.*?;\n","const BEATS=/*BEATS*/"+json.dumps(B)+";\n",h,flags=re.S)
o=o.replace("url(img/m1.jpg)","url(img/m1.jpg)")
AIL="AI visualisation."
fine=("const FINE=[[0,AIL+' Not a real street.'],[SC[1].t0,AIL+' UNESCO World Heritage Centre: a pol has 50 to 100 houses.'],"
 "[SC[2].t0,'Photo: Kalpit Visavadiya / Unsplash. Old Ahmedabad.'],[SC[3].t0,AIL],"
 "[SC[4].t0,'Photo: Kalpit Visavadiya / Unsplash. Ashtapad Derasar, old Ahmedabad. Pols took shape 1738 to 1753 (Wikipedia; Deccan Herald, 2022).'],"
 "[SC[5].t0,AIL+' Live History India, 2020; Wikipedia.'],[SC[6].t0,AIL+' Guard room above the gate (Live History India, 2020).'],"
 "[SC[7].t0,'Photo: Rishi Popat / Unsplash.'],[SC[8].t0,AIL+' Passages disguised as house fronts (Live History India, 2020; Deccan Herald, 2022).'],"
 "[SC[9].t0,AIL+' Joined terraces (Deccan Herald, 2022).'],[SC[10].t0,'Photo: Kalpit Visavadiya / Unsplash. UNESCO inscription, 2017.'],"
 "[SC[11].t0,'Photo: Kalpit Visavadiya / Unsplash.'],[SC[12].t0,AIL+' Education only.'],[OST,'']];")
tl=re.sub(r"const FINE=\[.*?\];",fine,tl,flags=re.S)
tl=re.sub(r"const FLASH=\[.*?\];","const FLASH=[HOOKEV,wt('gate'),wt('fortress'),wt('disguised'),wt('2017')];",tl)
open('reel.html','w').write(h+sc+o+tl); print('ok')
