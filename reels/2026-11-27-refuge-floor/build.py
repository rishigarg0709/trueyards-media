import json,re
t=open('reel.tpl.html').read()
a=t.index("const HOOKEV=");b=t.index("const scenes=SC.map")
head=t[:a];tail=t[b:]
sc=open('_scenes.js').read()
W=open('words.json').read().strip();B=json.load(open('beats.json'))['beats']
head=re.sub(r"const WS=.*?;\n","const WS="+W+";\n",head,count=1,flags=re.S)
head=re.sub(r"const BEATS=.*?;\n","const BEATS="+json.dumps(B)+";\n",head,count=1,flags=re.S)
# drop the floor counter device of the template (it lives between the helpers and the scenes)
AIL="AI visualisation, not a real building."
REAL="Real photo: Mumbai / Unsplash."
RULE="Maharashtra rule, as summarised by Square Yards, Nov 2024."
fine=("const AIL='"+AIL+"';const REAL='"+REAL+"';const FINE=[[0,''],[1.4,AIL],[SC[3].t0,REAL],[SC[4].t0,REAL+' '+'"+RULE+"'],[SC[5].t0,AIL+' "+RULE+"'],[SC[6].t0,AIL+' No fire shown. Why: Piramal Realty, Jul 2025; NBC 2016 (Housing.com).'],"
 "[SC[8].t0,AIL],[SC[10].t0,AIL+' Up to 4% of the habitable floor area it serves (Piramal Realty, Jul 2025).'],[SC[11].t0,AIL+' Not allowed: sold, locked, walled in (Piramal Realty, Jul 2025).'],[SC[13].t0,REAL+' Building shown is not a refuge-floor case.'],[SC[14].t0,AIL+' Education only, not advice.'],[END-1.8,'']];")
tail=re.sub(r"const AIL=.*?const FINE=\[.*?\];",lambda m:fine,tail,count=1,flags=re.S)
tail=tail.replace(" floors(t);\n","\n")
tail=re.sub(r"\[HOOKEV,wt\('thirty-four'\).*?\]\.forEach","[HOOKEV,wt('twenty-four'),wt('seventh'),wt('wait'),wt('four'),wt('flat')].forEach",tail,count=1)
open('reel.html','w').write(head+sc+tail);print('ok')
