const HOOKEV=wt('law');
// ================= SCENES (look A Newsroom Red: near-black #0D0D0F, white, one red #E63B2E; Inter 900 caps, Plex Mono kickers) =================
const BG='#0D0D0F';const KC='#FFD2CC';
const L15=x=>Math.max(1.55,x); // D41: no text before 1.5 s
const panel=(sc,src,y,h,pos,ox,oy)=>{const b=frm(sc,src,y,h,pos,ox,oy);mk(sc,'sh',`background:linear-gradient(180deg,${BG} ${y-2}px,rgba(13,13,15,0) ${y+140}px,rgba(13,13,15,0) ${y+h-220}px,${BG} ${y+h}px)`);return b};
const num=(p,css)=>mk(p,'H ts',css+';opacity:0','');
const cnt=(e,t,a,du,f)=>{e.style.opacity=cl((t-a+.1)/.15);const p=eo((t-a)/du);e.innerHTML=f(p);return p};
// recurring device: a thin red "refuge" bracket that locks onto the open floor
const heroBox=(sc,ox,oy,pos)=>box(sc,'h1',ox||540,oy||800,pos||'50% 50%');
// 1. HOOK: bright white tower, open empty floor with sky through it; slow tilt up toward the gap from frame 0; line spoken from 0 s; text from 1.55 s
add(0,sc=>{const b=heroBox(sc,540,760);b.im.style.filter='brightness(1.06) saturate(1.06) contrast(1.03)';mk(sc,'sh','background:linear-gradient(180deg,rgba(13,13,15,.88) 0%,rgba(13,13,15,.6) 8%,rgba(13,13,15,0) 17%)');const g=mk(sc,'sh','background:'+GB(48)+';opacity:0');
 const k=T(sc,'K ts','left:72px;top:1236px;color:'+KC,[['●',1.55,'c'],['Why',1.55],['India',1.55],['looks',1.55],['like',1.55],['this',1.55],['#4',1.55]]);
 const h=T(sc,'H ts','left:70px;top:1284px;width:940px;font-size:112px',[['An',L15(wt('an'))],['empty',L15(wt('empty'))],['floor.',L15(wt('floor'))],['\n'],['By',wt('by')],['law.',wt('law'),'hl',1]]);
 const br=corners(sc,110,650,970,1150,60,7);
 return t=>{const sk=shake(t,HOOKEV,6);const p=eio(t/3.4);b.style.transform=`translate(${sk}px,0) scale(${1.2+.05*p}) translateY(${-150+40*p}px)`;g.style.opacity=cl((t-1.3)/.3);rv(k,t);rv(h,t);crn(br,t,HOOKEV+.05)}});
// 2. Hero close on the gap, push-in. "No flats. No walls."
add(wt('no')-.1,sc=>{const b=heroBox(sc,540,820);b.im.style.filter='brightness(1.06) saturate(1.06) contrast(1.03)';mk(sc,'sh','background:'+GB(56));
 const b0=wt('no')-.1;
 const h=T(sc,'H ts','left:70px;top:1270px;width:940px;font-size:126px',[['No',wt('no')],['flats.',wt('flats'),'hl'],['\n'],['No',wt('no',2)],['walls.',wt('walls'),'hl']]);
 return t=>{b.style.transform=`scale(${1.9+.16*eio(t/2.6)}) translateY(${20-30*eio(t/2.6)}px)`;rv(h,t)}},true);
// 3. Inside the open floor (AI), framed panel, slow push. "Just columns and air."
add(wt('just')-.1,sc=>{const b=panel(sc,'r2',260,980,'50% 50%',540,490);
 const k=T(sc,'K ts','left:72px;top:1250px;color:'+KC,[['●',wt('just'),'c'],['Inside',wt('just')],['the',wt('just')],['empty',wt('just')],['floor',wt('just')]]);
 const h=T(sc,'H ts','left:70px;top:1300px;width:940px;font-size:112px',[['Just',wt('just')],['columns',wt('columns')],['\n'],['and',wt('and')],['air.',wt('air'),'hl',1]]);
 return t=>{b.im.style.transform=`scale(${1.04+.1*eio(t/3)}) translateX(${-20+30*eio(t/3)}px)`;rv(k,t);rv(h,t)}},true);
// 4. Real Mumbai supertall, tilt up. "It's not unfinished."
add(wt("it's")-.1,sc=>{const b=box(sc,'sup',540,700,'50% 40%');b.im.style.filter='brightness(1.08) saturate(1.04)';mk(sc,'sh','background:'+GB(54));
 const b0=wt("it's")-.1;
 const h=mk(sc,'H ts','left:70px;top:1270px;width:940px;font-size:118px;opacity:0','Not');
 const u=mk(sc,'H ts','left:70px;top:1390px;font-size:118px;opacity:0;background:linear-gradient(#E63B2E,#E63B2E) left 54%/0% 14px no-repeat','unfinished.');
 return t=>{b.style.transform=`scale(${1.1+.04*eio(t/2.4)}) translateY(${70-90*eio(t/2.4)}px)`;fade(h,t,wt('not')-b0,.2,20);fade(u,t,wt('unfinished')-b0,.2,20);u.style.backgroundSize=`${eo((t-(wt('unfinished')-b0+.35))/.28)*100}% 14px`}},true);
// 5. Real Mumbai towers (framed). "In Maharashtra, once a tower passes twenty-four metres,"
add(wt('in')-.1,sc=>{const b=box(sc,'byc',540,600,'50% 30%');b.im.style.filter='brightness(1.06) saturate(1.04)';mk(sc,'sh','background:'+GB(52));
 const b0=wt('in')-.1;
 const tg=mk(sc,'tag','left:72px;top:1160px;opacity:0','Maharashtra rule');
 const k=T(sc,'K ts','left:72px;top:1240px;color:'+KC,[['Once',wt('once')],['a',wt('once')],['tower',wt('tower',2)],['passes',wt('passes')]]);
 const n=num(sc,'left:62px;top:1290px;font-size:250px;letter-spacing:-.04em');
 const tn=wt('twenty-four')-b0;
 return t=>{b.style.transform=`scale(${1.12+.08*eio(t/3.4)})`;fade(tg,t,.05,.2,10);rv(k,t);cnt(n,t,tn,.55,p=>`${Math.round(24*p)}<span style="font-size:.5em"> m</span>`);n.style.color=t>tn+.6?'#E63B2E':'#fff'}},true);
// 6. Cutaway: every 7th floor lit red (AI), full section, push. "a refuge area comes on every seventh floor you live on."
add(wt('a',2)-.1,sc=>{const b=box(sc,'c4',540,700,'50% 30%');b.im.style.filter='brightness(1.12) saturate(1.05)';mk(sc,'sh','background:'+GB(58));
 const b0=wt('a',2)-.1;
 const k=T(sc,'K ts','left:72px;top:1300px;color:'+KC,[['●',wt('refuge'),'c'],['A',wt('refuge')],['refuge',wt('refuge')],['area',wt('area')]]);
 const h=T(sc,'H ts','left:70px;top:1350px;width:940px;font-size:112px',[['Every',wt('every')],['7th',wt('seventh'),'hl',1],['\n'],['floor',wt('floor',2)]]);
 return t=>{b.style.transform=`scale(${1.02+.1*eio(t/3.6)}) translateY(${-10*eio(t/3.6)}px)`;rv(k,t);rv(h,t)}},true);
// 7. Stairwell filling with smoke (AI), wide, push. "Here's why. In a fire, the stairs fill with smoke"
add(wt("here's")-.1,sc=>{const b=box(sc,'s3',540,900,'50% 50%');b.im.style.filter='brightness(1.22) saturate(1.02) contrast(1.02)';mk(sc,'sh','background:'+GB(54));
 const b0=wt("here's")-.1;
 const k=T(sc,'K ts','left:72px;top:1250px;color:'+KC,[['●',wt('fire'),'c'],['In',wt('in',2)],['a',wt('a',3)],['fire',wt('fire')]]);
 const h=T(sc,'H ts','left:70px;top:1300px;width:940px;font-size:108px',[['Smoke',wt('smoke'),'hl',1],['\n'],['fills',wt('fill')],['the',wt('stairs')],['stairs',wt('stairs')]]);
 const q=mk(sc,'H ts','left:70px;top:1300px;width:940px;font-size:140px;opacity:0','Why?');
 return t=>{b.style.transform=`scale(${1.1+.12*eio(t/4)})`;const tf=wt('in',2)-b0-.05;q.style.opacity=t<tf?cl((t-.05)/.15):0;rv(k,t);rv(h,t)}},true);
// 8. Smoke close (AI crop), slow drift up. "faster than people can get down."
add(wt('faster')-.1,sc=>{const b=box(sc,'s3',560,1180,'50% 50%');b.im.style.filter='brightness(1.2) saturate(1.02)';mk(sc,'sh','background:'+GB(54));
 const h=T(sc,'H ts','left:70px;top:1300px;width:960px;font-size:92px',[['Faster',wt('faster'),'hl'],['than',wt('than')],['\n'],['people',wt('people')],['can',wt('can')],['get',wt('get')],['down.',wt('down')]]);
 return t=>{b.style.transform=`scale(${2.0+.14*eio(t/2.6)}) translateY(${30-40*eio(t/2.6)}px)`;rv(h,t)}},false);
// 9. Cutaway again, close on two lit floors: the escape. "So you don't run thirty floors. You go down a few,"
add(wt('so')-.1,sc=>{const b=box(sc,'c4',540,1000,'50% 30%');b.im.style.filter='brightness(1.14) saturate(1.05)';mk(sc,'sh','background:'+GB(58));
 const b0=wt('so')-.1;
 const h=mk(sc,'H ts','left:70px;top:1190px;width:940px;font-size:100px;opacity:0',"Don't run <span style=\"background:linear-gradient(#E63B2E,#E63B2E) left 54%/0% 14px no-repeat\" id=\"r30\">30</span> floors.");
 const u=mk(sc,'H ts','left:70px;top:1410px;width:940px;font-size:100px;opacity:0','Go down <span class="hl">a few.</span>');
 const ar=svg(sc,'opacity:0','<path d="M960 420 L960 900 M920 860 L960 905 L1000 860" stroke="#E63B2E" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round"/>');
 return t=>{const tg=wt('go')-b0;b.style.transform=`scale(${1.7+.12*eio(t/4)}) translateY(${-60+60*eio(t/4)}px)`;fade(h,t,wt('run')-b0-.05,.2,20);const s=h.querySelector('span');s.style.backgroundSize=`${eo((t-(wt('thirty')-b0+.2))/.25)*100}% 14px`;fade(u,t,tg,.2,20);ar.style.opacity=cl((t-tg)/.2);ar.style.transform=`translateY(${(t>tg?eio((t-tg)/1.2):0)*80}px)`}},true);
// 10. Inside the refuge floor, push to the railing and the city: "step into open air... and wait for rescue." (tell-a-friend core)
add(wt('step')-.1,sc=>{const b=panel(sc,'r2',260,980,'85% 50%',800,490);
 const b0=wt('step')-.1;
 const k=T(sc,'K ts','left:72px;top:1250px;color:'+KC,[['●',wt('step'),'c'],['Step',wt('step')],['into',wt('into')],['open',wt('open')],['air',wt('air',2)]]);
 const st=mk(sc,'stamp','left:70px;top:1300px;opacity:0;font-size:118px;color:#fff;background:rgba(230,59,46,.22)','WAIT.');
 const u=T(sc,'M ts','left:70px;top:1470px;width:940px',[['for',wt('for')],['rescue',wt('rescue'),'hl']]);
 return t=>{b.im.style.transform=`scale(${1.3+.22*eio(t/3.6)})`;rv(k,t);const tw=wt('wait')-b0;if(t>=tw)slam(st,t,tw,1.7,-3);else st.style.opacity=0;rv(u,t)}},true);
// 11. Cutaway, single refuge floor close: "And the builder doesn't lose. Up to four percent ... is free of FSI."
add(wt('and',3)-.1,sc=>{const b=box(sc,'c4',540,820,'50% 30%');b.im.style.filter='brightness(1.14) saturate(1.05)';mk(sc,'sh','background:'+GB(52));
 const b0=wt('and',3)-.1;
 const k=T(sc,'K ts','left:72px;top:1130px;color:'+KC,[['The',wt('the',2)],['builder',wt('builder')],["doesn't",wt("doesn't")],['lose',wt('lose')]]);
 const k2=T(sc,'M ts','left:70px;top:1110px;color:#fff',[['Up',wt('up')],['to',wt('to')]]);
 const n=num(sc,'left:58px;top:1180px;font-size:250px;letter-spacing:-.04em');
 const u=T(sc,'H ts','left:70px;top:1430px;width:940px;font-size:92px',[['free',wt('free')],['of',wt('of',2)],['FSI',wt('fsi'),'hl',1]]);
 const tn=wt('four')-b0;
 return t=>{b.style.transform=`scale(${2.5+.18*eio(t/4)})`;rv(k,t,wt('up')-b0-.2);rv(k2,t);cnt(n,t,tn,.5,p=>`${Math.round(4*p)}%`);n.style.color=t>tn+.55?'#E63B2E':'#fff';rv(u,t)}},true);
// 12. Bricked-in refuge floor with a padlocked door (AI): "But it can never be sold."
add(wt('but')-.1,sc=>{const b=box(sc,'w5',600,900,'50% 50%');b.im.style.filter='brightness(1.18) saturate(1.02)';mk(sc,'sh','background:'+GB(54));
 const b0=wt('but')-.1;
 const tg=mk(sc,'tagw','left:72px;top:1220px;opacity:0','Not allowed');
 const h=T(sc,'H ts','left:70px;top:1290px;width:940px;font-size:120px',[['Never',wt('never')],['sold.',wt('sold'),'hl',1]]);
 return t=>{b.style.transform=`scale(${1.12+.1*eio(t/2.4)})`;fade(tg,t,.05,.2,10);rv(h,t)}},true);
// 13. Padlock close: "Never locked."
add(wt('never',2)-.1,sc=>{const b=box(sc,'w5',573,1170,'50% 50%');b.im.style.filter='brightness(1.2) saturate(1.02)';mk(sc,'sh','background:'+GB(54));
 const h=T(sc,'H ts','left:70px;top:1290px;width:940px;font-size:120px',[['Never',wt('never',2)],['locked.',wt('locked'),'hl',1]]);
 const br=corners(sc,466,480,756,770,50,6);
 return t=>{b.style.transform=`translateY(-150px) scale(${2.4+.2*eio(t/1.6)})`;rv(h,t);crn(br,t,.15)}},false);
// 14. Real tower facade (Mumbai), slow pan: "Never turned into a flat."
add(wt('never',3)-.1,sc=>{const b=panel(sc,'mnt',200,1160,'50% 50%',540,580);
 const h=T(sc,'H ts','left:70px;top:1290px;width:940px;font-size:112px',[['Never',wt('never',3)],['a',wt('a',5)],['flat.',wt('flat'),'hl',1]]);
 return t=>{b.im.style.transform=`scale(${1.06+.08*eio(t/2.4)}) translateX(${20-40*eio(t/2.4)}px)`;rv(h,t)}},true);
// 15. Loop: back to the frame-0 tower. "So that empty floor isn't missing. It's waiting."
add(wt('so',2)-.1,sc=>{const b=heroBox(sc,540,760);b.im.style.filter='brightness(1.06) saturate(1.06) contrast(1.03)';mk(sc,'sh','background:linear-gradient(180deg,rgba(13,13,15,.88) 0%,rgba(13,13,15,.6) 8%,rgba(13,13,15,0) 17%)');mk(sc,'sh','background:'+GB(46));/*loop*/
 const b0=wt('so',2)-.1;
 const k=T(sc,'M ts','left:70px;top:1140px;width:960px;font-size:66px;color:#fff',[['That',wt('that')],['empty',wt('empty',2)],['floor',wt('floor',4)],["isn't",wt("isn't")],['missing',wt('missing')]]);
 const h=T(sc,'H ts','left:70px;top:1300px;width:960px;font-size:124px',[["It's",wt("it's",2)],['waiting.',wt('waiting'),'hl',1]]);
 const tg=mk(sc,'tagw','left:72px;top:1462px;opacity:0','Why India looks like this · #5 next');
 const br=corners(sc,110,650,970,1150,60,7);
 return t=>{const p=eio(t/3);b.style.transform=`scale(${1.36-.11*p}) translateY(${-150+0*p}px)`;rv(k,t);rv(h,t);fade(tg,t,wt('waiting')-b0+.3,.25,14);crn(br,t,wt('waiting')-b0)}},true);
