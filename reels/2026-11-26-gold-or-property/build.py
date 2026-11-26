import json,sys
D='.'
head=open('_head.html').read(); mid=open('_mid.html').read()
sc=open('_scenes.js').read(); tl=open('_tail.js').read()
draw='''const draw=t=>{window.GT=t;
 scenes.forEach((s,i)=>{const on=t>=s.t0&&t<s.t1;s.sc.style.display=on?'block':'none';
  if(on){const lt=t-s.t0;const n=8;if(i>0&&s.wipe&&lt<.32){const p=lt/.32;const prev=scenes[i-1];prev.sc.style.display='block';prev.u(t-prev.raw);
    s.sc.style.clipPath=`polygon(${(()=>{let a=[];for(let c=0;c<n;c++){const q=eo(cl(p*1.6-c*.07));const x0=c*1080/n,x1=(c+1)*1080/n+1;a.push(`${x0}px 0px`,`${x1}px 0px`,`${x1}px ${1920*q}px`,`${x0}px ${1920*q}px`,`${x0}px 0px`)}return a.join(',')})()})`}
   else s.sc.style.clipPath='none';
   s.u(t-s.raw)}});
 let ft='';FINE.forEach(([tt,s])=>{if(t>=tt)ft=s});const fe=document.getElementById('fine');fe.textContent=ft;let lg=0;LIGHT.forEach(([tt,v])=>{if(t>=tt)lg=v});fe.style.color=lg?'rgba(20,20,22,.62)':'rgba(255,255,255,.72)';fe.style.textShadow=lg?'none':'0 1px 6px rgba(0,0,0,.6)';
 let fl=0;scenes.forEach((s,i)=>{if(i&&t>=s.t0&&!s.wipe)fl=Math.max(fl,.14*Math.exp(-(t-s.t0)/.06))});
 [ws('seven'),ws('fell',2),ws('locker')].forEach((e,j)=>{if(e!=null&&t>=e)fl=Math.max(fl,.22*Math.exp(-(t-e)/.08))});document.getElementById('flash').style.opacity=fl;
 const fo=cl((t-(END-1.75))/.2)*(1-cl((t-(END-.42))/.25));document.getElementById('fol').style.opacity=fo;
};
if(MISS.length)console.log('ERR missing words',MISS.join(','));
</script></body></html>'''
mid=mid.replace("const AIL='AI visualisation.';\nconst FINE=","//FINEX\nconst _F0=")
# drop old FINE line from mid
import re
mid=re.sub(r"//FINEX\nconst _F0=.*?\n","",mid,flags=re.S)
tpl=head+sc+"\n"+mid.replace("window.DUR=END;","window.DUR=END;\n"+tl)+draw
# remove tape divs
tpl=tpl.replace('<div id="tp"><div id="tpf"></div></div><div id="tpl"></div>','')
open('reel.tpl.html','w').write(tpl)
W=open('words.json').read(); B=json.load(open('beats.json'))
out=tpl.replace('%%WS%%','const WS='+W+';').replace('%%BEATS%%','const BEATS='+json.dumps(B['beats'])+';')
open('reel.html','w').write(out); print('built',len(out))
