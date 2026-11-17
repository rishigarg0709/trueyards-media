import json
s=open('reel.tpl.html').read();w=json.load(open('words.json'));b=json.load(open('beats.json'))
open('reel.html','w').write(s.replace('/*WS*/[]',json.dumps(w)).replace('/*BEATS*/[]',json.dumps(b['beats'])))
