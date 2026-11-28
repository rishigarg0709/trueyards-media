const HOOKEV=wt('electricity');
// ================= SCENES (look E Blueprint: ink #0C2340, white line work, one cyan #4FD1FF; Inter 800/900, Plex Mono labels) =================
const BG='#0C2340';const KC='#BFEFFF';
const panel=(sc,src,y,h,pos,ox,oy)=>{const b=frm(sc,src,y,h,pos,ox,oy);mk(sc,'sh',`background:linear-gradient(180deg,${BG} ${y-2}px,rgba(12,35,64,0) ${y+140}px,rgba(12,35,64,0) ${y+h-220}px,${BG} ${y+h}px)`);return b};
const num=(p,css)=>mk(p,'H ts',css+';opacity:0','');
const cnt=(e,t,a,du,f)=>{e.style.opacity=cl((t-a+.1)/.15);const p=eo((t-a)/du);e.innerHTML=f(p);return p};
// cyan leader label: a dot, a thin line and a mono tag that draws on at time a (scene-local)
const lab=(sc,x,y,len,txt,dir)=>{const l=mk(sc,'',`left:${dir<0?x-len:x}px;top:${y}px;width:0px;height:4px;background:#4FD1FF;box-shadow:0 0 12px rgba(79,209,255,.8)`);const d=mk(sc,'',`left:${x-11}px;top:${y-9}px;width:22px;height:22px;border-radius:50%;background:#4FD1FF;box-shadow:0 0 16px #4FD1FF;opacity:0`);const g=mk(sc,'tag',`top:${y-26}px;opacity:0;font-size:30px;${dir<0?'right:'+(1080-(x-len)+12)+'px':'left:'+(x+len+12)+'px'}`,txt);
 return (t,a)=>{const p=eo((t-a)/.3);d.style.opacity=cl((t-a)/.08);l.style.width=(len*p)+'px';if(dir<0)l.style.left=(x-len*p)+'px';g.style.opacity=cl((t-a-.2)/.15)}};
const heroBox=(sc,ox,oy,pos)=>box(sc,'h1',ox||540,oy||700,pos||'50% 50%');
// 1. HOOK: bright pole buried in cables, blue sky, slow tilt up from frame 0; BIG hook text already on screen at frame 0 (D73), question spoken from 0 s
add(0,sc=>{const b=heroBox(sc,540,560);b.im.style.filter='brightness(1.08) saturate(1.08) contrast(1.03)';
 mk(sc,'sh','background:linear-gradient(180deg,rgba(12,35,64,.35) 0%,rgba(12,35,64,0) 30%)');
 const h=mk(sc,'HK ts','left:64px;top:262px;width:960px','<div style="font-size:90px;line-height:1.05;white-space:nowrap">Why are Indian poles</div><div style="font-size:190px;line-height:1.0;margin-top:22px"><span class="hl">buried</span></div><div style="font-size:190px;line-height:1.0;margin-top:22px;white-space:nowrap">in&nbsp;<span class="hl">wires?</span></div>');
 const t1=wt("here's")-.15;
 return t=>{const p=eio(t/3.2);b.style.transform=`scale(${1.16+.06*p}) translateY(${70-110*p}px)`;const q=eo(t/.16);h.style.transform=`scale(${1.06-.06*q})`;h.style.transformOrigin='0 50%';h.style.opacity=1-cl((t-t1)/.15)}});
// 2. Real pole tangle (photo), push-in on the knot. "Here's the twist. A lot of these wires... don't carry electricity at all."
add(wt("here's")-.1,sc=>{const b=panel(sc,'pt',200,1180,'50% 45%',540,560);b.im.style.filter='brightness(1.08) saturate(1.05)';
 const b0=wt("here's")-.1;
 const k=T(sc,'K ts','left:72px;top:1250px;color:'+KC,[['●',wt("here's"),'c'],["Here's",wt("here's")],['the',wt('the',1)],['twist',wt('twist')]]);
 const h=T(sc,'H ts','left:70px;top:1300px;width:960px;font-size:118px',[['Not',wt("don't")],['\n'],['electricity.',wt('electricity'),'hl',1]]);
 return t=>{b.im.style.transform=`scale(${1.05+.16*eio(t/3.4)})`;rv(k,t);rv(h,t)}},true);
// 3. Cutaway (AI): power layer on top. "The power lines usually run at the top."
add(wt('the',2)-.1,sc=>{const b=box(sc,'cut',540,520,'50% 20%');b.im.style.filter='brightness(1.15) saturate(1.05)';mk(sc,'sh','background:'+GB(56));
 const b0=wt('the',2)-.1;
 const L1=lab(sc,640,560,170,'POWER',1);
 const h=T(sc,'H ts','left:70px;top:1290px;width:960px;font-size:112px',[['Power',wt('power',1)],['\n'],['on',wt('top')-.2],['top.',wt('top'),'hl',1]]);
 const k=T(sc,'K ts','left:72px;top:1240px;color:'+KC,[['usually',wt('usually')]]);
 return t=>{b.style.transform=`scale(${1.9+.12*eio(t/2.6)}) translateY(${120}px)`;L1(t,wt('power',1)-b0);rv(h,t);rv(k,t)}},true);
// 4. Cutaway, the bundles below, with labels. "The tangle below? Cable TV. Internet. Optical fibre."
add(wt('the',4)-.1,sc=>{const b=box(sc,'cut',540,900,'50% 30%');b.im.style.filter='brightness(1.18) saturate(1.05)';mk(sc,'sh','background:'+GB(60));
 const b0=wt('the',4)-.1;
 const a=lab(sc,440,520,150,'CABLE TV',-1),c=lab(sc,640,690,150,'INTERNET',1);
 const h=T(sc,'H ts','left:70px;top:1330px;width:960px;font-size:112px',[['The',wt('the',4)],['tangle',wt('tangle'),'hl',1],['\n'],['below?',wt('below')]]);
 return t=>{b.style.transform=`scale(${1.45+.1*eio(t/4)}) translateY(${-40*eio(t/4)}px)`;rv(h,t);a(t,wt('cable')-b0);c(t,wt('internet')-b0)}},true);
// 5. Macro: optical fibre strands (AI), framed panel. "Optical fibre." then "Hung on electricity poles."
add(wt('optical')-.12,sc=>{const b=panel(sc,'fib',380,860,'50% 50%',600,430);b.im.style.filter='brightness(1.15) saturate(1.05)';
 const b0=wt('optical')-.12;
 const k=T(sc,'K ts','left:72px;top:1250px;color:'+KC,[['●',wt('optical'),'c'],['Optical',wt('optical')],['fibre',wt('fibre')]]);
 const h=T(sc,'H ts','left:70px;top:1300px;width:960px;font-size:108px',[['Hung',wt('hung')],['on',wt('on',1)],['\n'],['power',wt('electricity',2)],['poles.',wt('poles',2),'hl',1]]);
 return t=>{b.im.style.transform=`scale(${1.08+.14*eio(t/2.6)}) rotate(${-2+3*eio(t/2.6)}deg)`;rv(k,t);rv(h,t)}},true);
// 6. Real old facade with wires (photo), tilt down. "In July 2024, Bengaluru's power company told operators:"
add(wt('in',2)-.1,sc=>{const b=panel(sc,'hw',200,1180,'50% 30%',540,590);b.im.style.filter='brightness(1.06) saturate(1.04)';
 const b0=wt('in',2)-.1;
 const tg=mk(sc,'tag','left:72px;top:1180px;opacity:0','Bengaluru · July 2024');
 const h=T(sc,'H ts','left:70px;top:1260px;width:960px;font-size:100px',[['Power',wt('power',2)],['company',wt('company')],['\n'],['to',wt('told')],['operators:',wt('operators'),'hl',1]]);
 return t=>{b.im.style.transform=`scale(${1.1+.06*eio(t/3.4)}) translateY(${-60+80*eio(t/3.4)}px)`;fade(tg,t,.05,.2,10);rv(h,t)}},true);
// 7. Cut cables and a coil on the kerb (AI). "remove your unauthorised cables from our poles by July eighth. Or we will."
add(wt('remove')-.1,sc=>{const b=box(sc,'coil',600,1100,'50% 60%');b.im.style.filter='brightness(1.1) saturate(1.04)';mk(sc,'sh','background:'+GB(54));
 const b0=wt('remove')-.1;
 const h=T(sc,'H ts','left:70px;top:1250px;width:960px;font-size:112px',[['Remove',wt('remove')],['by',wt('by')],['\n'],['8',wt('eighth')],['July.',wt('eighth'),'hl',1]]);
 const st=mk(sc,'stamp','left:330px;top:960px;opacity:0;font-size:80px','OR WE WILL.');
 return t=>{b.style.transform=`scale(${1.08+.1*eio(t/4)})`;rv(h,t);const ts=wt('or')-b0;if(t>=ts)slam(st,t,ts,1.7,-4);else st.style.opacity=0}},true);
// 8. Counter over the blurred hero street, a cyan cable line draws on. "Its survey counted about 2,335 kilometres of illegal wires."
add(wt('its')-.1,sc=>{const b=box(sc,'h1',540,960,'50% 50%');b.im.style.filter='brightness(.95) saturate(1.0) blur(10px)';mk(sc,'sh','background:rgba(12,35,64,.45)');
 const b0=wt('its')-.1;
 const ln=svg(sc,'','<path id="cw" d="M-40 760 C 200 640, 330 900, 540 780 S 880 640, 1120 820" stroke="#4FD1FF" stroke-width="9" fill="none" stroke-linecap="round" style="filter:drop-shadow(0 0 14px #4FD1FF)"/>');const P=ln.querySelector('path');const PL=P.getTotalLength();P.style.strokeDasharray=PL;
 const k=T(sc,'K ts','left:72px;top:880px;color:'+KC,[['●',wt('survey'),'c'],['BESCOM',wt('survey')],['survey',wt('survey')]]);
 const n=num(sc,'left:62px;top:930px;font-size:230px;letter-spacing:-.04em;white-space:nowrap');
 const u=T(sc,'H ts','left:70px;top:1180px;width:960px;font-size:104px',[['km',wt('kilometres')],['of',wt('of',2)],['\n'],['illegal',wt('illegal'),'hl',1],['wires',wt('wires',3)]]);
 const tn=wt('two')-b0;
 return t=>{b.style.transform=`scale(${1.25+.08*eio(t/4)})`;P.style.strokeDashoffset=PL*(1-eo((t-tn)/2.2));rv(k,t);cnt(n,t,tn,1.6,p=>Math.round(2335*p).toLocaleString('en-IN'));n.style.color=t>tn+1.6?'#4FD1FF':'#fff';rv(u,t)}},true);
// 9. Real street of wires (photo, cropped to the sky band, no people). "In one city."
add(wt('in',3)-.1,sc=>{const b=panel(sc,'sw',200,1100,'50% 8%',540,300);b.im.style.filter='brightness(1.18) saturate(1.04) contrast(1.04)';
 const h=T(sc,'H ts','left:70px;top:1260px;width:960px;font-size:170px',[['In',wt('in',3)],['one',wt('one',1),'hl',1],['\n'],['city.',wt('city')]]);
 return t=>{b.im.style.transform=`scale(${1.12+.08*eio(t/2)}) translateX(${30-60*eio(t/2)}px)`;rv(h,t)}},true);
// 10. Cut ends close (AI). "Some came down."
add(wt('some')-.1,sc=>{const b=box(sc,'coil',600,1300,'50% 60%');b.im.style.filter='brightness(1.1) saturate(1.04)';mk(sc,'sh','background:'+GB(54));
 const h=T(sc,'H ts','left:70px;top:1280px;width:960px;font-size:118px',[['Some',wt('some')],['came',wt('came')],['\n'],['down.',wt('down'),'hl',1]]);
 return t=>{b.style.transform=`scale(${1.9+.12*eio(t/1.6)}) translateY(${-40}px)`;rv(h,t)}},true);
// 11. Real pole tangle again, other crop. "On one street, they were back the very next day."
add(wt('on',2)-.1,sc=>{const b=panel(sc,'pt',200,1180,'70% 30%',760,400);b.im.style.filter='brightness(1.1) saturate(1.05)';
 const b0=wt('on',2)-.1;
 const tg=mk(sc,'tagw','left:72px;top:1180px;opacity:0','One street');
 const h=T(sc,'H ts','left:70px;top:1250px;width:960px;font-size:112px',[['Back',wt('back')],['the',wt('the',5)],['\n'],['next',wt('next',1)],['day.',wt('day'),'hl',1]]);
 return t=>{b.im.style.transform=`scale(${1.3+.12*eio(t/3)})`;fade(tg,t,.05,.2,10);rv(h,t)}},true);
// 12. Hero mid crop, one new cyan cable draws on. "Every new connection can mean one more wire."
add(wt('every')-.1,sc=>{const b=heroBox(sc,540,820);b.im.style.filter='brightness(1.08) saturate(1.06)';mk(sc,'sh','background:'+GB(56));
 const b0=wt('every')-.1;
 const ln=svg(sc,'','<path d="M1120 360 C 860 420, 700 520, 600 760 C 560 860, 640 980, 520 1060" stroke="#4FD1FF" stroke-width="10" fill="none" stroke-linecap="round" style="filter:drop-shadow(0 0 16px #4FD1FF)"/>');const P=ln.querySelector('path');const PL=P.getTotalLength();P.style.strokeDasharray=PL;
 const h=T(sc,'H ts','left:70px;top:1270px;width:960px;font-size:104px',[['+1',wt('new'),'hl'],['connection',wt('connection')],['\n'],['=',wt('mean')],['+1',wt('one',3),'hl'],['wire.',wt('wire')]]);
 return t=>{b.style.transform=`scale(${1.75+.1*eio(t/3)})`;P.style.strokeDashoffset=PL*(1-eo((t-(wt('new')-b0))/1.6));rv(h,t)}},true);
// 13. Impossible-real: the street with every wire gone (AI). "So next time you look up..."
add(wt('so')-.1,sc=>{const b=box(sc,'clean',540,500,'50% 40%');b.im.style.filter='brightness(1.06) saturate(1.06)';mk(sc,'sh','background:'+GB(60));
 const k=T(sc,'K ts','left:72px;top:1300px;color:'+KC,[['●',wt('so'),'c'],['Without',wt('so')],['them',wt('so')]]);
 const h=T(sc,'H ts','left:70px;top:1350px;width:960px;font-size:120px',[['Look',wt('look')],['up.',wt('up'),'hl',1]]);
 return t=>{const p=eio(t/2.4);b.style.transform=`scale(${1.12+.04*p}) translateY(${60-80*p}px)`;rv(k,t);rv(h,t)}},true);
// 14. Loop: back to the frame-0 tangle. "you're not looking at power. You're looking at your Wi-Fi."
add(wt("you're")-.1,sc=>{const b=heroBox(sc,540,560);b.im.style.filter='brightness(1.08) saturate(1.08) contrast(1.03)';mk(sc,'sh','background:'+GB(54));
 const b0=wt("you're")-.1;
 const k=T(sc,'M ts','left:70px;top:1160px;width:960px;font-size:72px;color:#fff',[['Not',wt('not')],['power.',wt('power',3)]]);
 const h=T(sc,'H ts','left:70px;top:1260px;width:960px;font-size:140px',[['Your',wt('your',2)],['\n'],['Wi-Fi.',wt('wi-fi'),'hl',1]]);
 const tg=mk(sc,'tagw','left:72px;top:1075px;opacity:0','Why India looks like this · #7');
 return t=>{const p=eio(t/3.4);b.style.transform=`scale(${1.3-.14*p}) translateY(${-40+110*p}px)`;rv(k,t);rv(h,t);fade(tg,t,wt('wi-fi')-b0+.3,.25,14)}},true);
