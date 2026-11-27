import json,re
h=open('_head.part').read(); sc=open('_scenes.part').read(); o=open('_outro.part').read(); tl=open('_tail.part').read()
W=open('words.json').read().strip(); B=json.load(open('beats.json'))['beats']
h=re.sub(r"const WS=/\*WS\*/.*?;\n","const WS=/*WS*/"+W+";\n",h,flags=re.S)
h=re.sub(r"const BEATS=/\*BEATS\*/.*?;\n","const BEATS=/*BEATS*/"+json.dumps(B)+";\n",h,flags=re.S)
AIL="AI visualisation, representational, not a real building."
REAL="Real photo: Mumbai / Unsplash."
fine=("const AIL='"+AIL+"';const REAL='"+REAL+"';const FINE=[[0,AIL],[SC[1].t0,REAL+' Rain: IMD Santacruz normals 1991 to 2020, about 2,502 mm a year.'],[SC[2].t0,AIL+' About 95% of the yearly rain falls June to September (IMD normals 1991 to 2020).'],"
 "[SC[3].t0,AIL],[SC[4].t0,AIL+' Dark stains follow run-off under parapets and sills (LNEC facade study).'],[SC[5].t0,AIL],[SC[6].t0,AIL+' Magnified. Biofilm on wet facades (RIBuild; LNEC).'],[SC[7].t0,AIL+' Magnified.'],"
 "[SC[8].t0,REAL],[SC[9].t0,REAL],[SC[10].t0,AIL+' Order of work: Berger Paints guidance. No brand recommended.'],[SC[11].t0,AIL+' Education only, not advice.'],[SC[12].t0,AIL+' Soot and dirt can add to the stains.'],[OST,'']];")
tl=re.sub(r"const AIL='AI visualisation.';","",tl)
tl=re.sub(r"const FINE=\[.*?\];",lambda m:fine,tl,flags=re.S)
tl=re.sub(r"const FLASH=\[.*?\];","const FLASH=[HOOKEV,wt('zinda'),wt('repaint'),wt('zinda',2)];",tl)
open('reel.html','w').write(h+sc+o+tl); print('ok')
