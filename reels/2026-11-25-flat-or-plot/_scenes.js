const HOOKEV=ws('every');
const box2=(p,src,ox,oy,pos)=>{const b=box(p,src,ox,oy,pos);return b};
const gridSVG=(op)=>{let s='';const x0=191,x1=887,y0=393,y1=1062,nc=10,nr=20;for(let c=1;c<nc;c++){const x=x0+(x1-x0)*c/nc;s+=`<line x1="${x}" y1="${y0}" x2="${x}" y2="${y1}"/>`}for(let r=1;r<nr;r++){const y=y0+(y1-y0)*r/nr;s+=`<line x1="${x0}" y1="${y}" x2="${x1}" y2="${y}"/>`}
 const cx=x0+(x1-x0)*6/nc,cy=y0+(y1-y0)*13/nr;return `<g stroke="rgba(255,255,255,.85)" stroke-width="2.2">${s}</g><rect x="${x0}" y="${y0}" width="${x1-x0}" height="${y1-y0}" fill="none" stroke="#fff" stroke-width="4"/><rect id="cc" x="${cx}" y="${cy}" width="${(x1-x0)/nc}" height="${(y1-y0)/nr}" fill="#FF6B57" stroke="#fff" stroke-width="3"/>`};
const SQ=[488,1142,605,1183];
// 1. HOOK: bright impossible-real tower lifted off its plot, push-in from frame 0, line spoken from 0 s; no text until 1.5 s
add(0,sc=>{const b=box(sc,'hero',546,760);b.im.style.filter='brightness(1.06) saturate(1.08) contrast(1.04)';
 const gl=mk(b,'',`position:absolute;left:${SQ[0]}px;top:${SQ[1]}px;width:${SQ[2]-SQ[0]}px;height:${SQ[3]-SQ[1]}px;background:#FF6B57;mix-blend-mode:screen;opacity:0`);
 const gd=mk(sc,'sh','opacity:0;background:'+GL(52));
 const tA=Math.max(1.5,HOOKEV||1.5);
 const h=T(sc,'H ts','left:70px;top:1290px;width:960px;font-size:140px',[['Flat',tA],['or',tA+.1,'c'],['plot?',tA+.2]]);
 const k=T(sc,'K ts','left:72px;top:1236px;color:#fff',[['●',tA,'c'],['Every',tA],['Indian',ws('indian')],['family',ws('family')],['has',ws('has')],['this',ws('this')],['fight',ws('fight')]]);
 return t=>{b.style.transform=`scale(${1.04+.13*eio(t/3.6)})`;gd.style.opacity=cl((t-tA+.35)/.4);gl.style.opacity=.25+.25*Math.sin(t*4);rv(h,t);rv(k,t)}});
LIGHT.push([0,0]);
// 2. Tilt down to the plot grid. "So here's what you actually own."
add(ws('so')-.08,sc=>{const b=box(sc,'hero',546,1162);b.im.style.filter='brightness(1.06) saturate(1.08)';
 const br=cab(corners(b,SQ[0]-14,SQ[1]-14,SQ[2]+14,SQ[3]+14,30,5));
 mk(sc,'sh','background:'+GL(50));
 const k=T(sc,'K ts','left:72px;top:1226px;color:#fff',[['●',ws('so'),'c'],['So',ws('so')],["here's",ws("here's")]]);
 const h=T(sc,'H ts','left:70px;top:1272px;width:960px;font-size:116px',[['What',ws('what')],['you',ws('you')],['\n'],['actually',ws('actually')],['own',ws('own'),'hl',1]]);
 return t=>{b.style.transform=`translateY(-120px) scale(${1.3+.12*eio(t/2.6)})`;crn(br,t,.3);rv(k,t);rv(h,t)}},true);
// 3. Real Indian tower, tilt up. "Buy a 1,000 sq ft flat in a tower..."
add(ws('buy')-.1,sc=>{const b=box(sc,'tower1',540,800,'50% 40%');b.im.style.filter='brightness(1.05)';
 mk(sc,'sh','background:'+GL(42));
 const k=T(sc,'K ts','left:72px;top:1150px;color:#fff',[['●',ws('buy'),'c'],['Buy',ws('buy')],['a',ws('a')]]);
 const h=T(sc,'H ts','left:70px;top:1196px;width:960px;font-size:150px',[['1,000',ws('thousand'),'hl',1],['\n'],['sq',ws('square')],['ft',ws('foot')],['flat',ws('flat',2)]]);
 return t=>{b.style.transform=`scale(1.1) translateY(${-70+110*eio(t/3.2)}px)`;rv(k,t);rv(h,t)}},true);
LIGHT.push([ws('buy')-.1,0]);
// 4. Back on the plot, the coral square: your share of the land ~228 sq ft
add(ws('your')-.12,sc=>{const b=box(sc,'hero',546,1162);b.im.style.filter='brightness(1.06) saturate(1.08)';
 const fq=mk(b,'',`position:absolute;left:${SQ[0]}px;top:${SQ[1]}px;width:${SQ[2]-SQ[0]}px;height:${SQ[3]-SQ[1]}px;background:#FF6B57;opacity:0`);
 const br=cab(corners(b,SQ[0]-14,SQ[1]-14,SQ[2]+14,SQ[3]+14,30,5));
 mk(sc,'sh','background:'+GL(48));
 const k=T(sc,'K ts','left:72px;top:1196px;color:#fff',[['●',ws('your'),'c'],['Your',ws('your')],['share',ws('share')],['of',ws('of')],['the',ws('the')],['land',ws('land')]]);
 const n=mk(sc,'ts','left:58px;top:1240px;font:600 200px/1 IN;letter-spacing:-.045em;color:#fff;opacity:0','≈0');
 const u=T(sc,'M ts','left:70px;top:1452px;font-size:62px',[['sq',ws('square',2)],['ft',ws('feet')],['of',ws('feet')+.06],['land',ws('feet')+.12,'hl',1]]);
 const b0=ws('your')-.12,t0=ws('twenty-eight')-b0-.25;
 return t=>{b.style.transform=`translateY(-260px) scale(${1.36+.06*eio(t/4)})`;crn(br,t,.15);fq.style.opacity=.45*cl((t-t0)/.5);const p=cnt(n,t,t0,.6,p=>'≈'+Math.round(228*p));n.style.color=p>=1?'#FF6B57':'#fff';rv(k,t);rv(u,t)}},true);
// 5. Aerial of the compound: the land split into slices, one is yours. "That's your undivided share of land."
add(ws("that's")-.08,sc=>{sc.style.background='#CEC6BB';const b=box(sc,'compound',540,728);
 const g=svg(b,'opacity:0',gridSVG());g.style.position='absolute';mk(b,'','position:absolute;left:0;top:1066px;width:1080px;height:1000px;background:#CEC6BB');
 mk(sc,'sh','background:'+LF(54));
 const k=T(sc,'K ink2','left:72px;top:1200px',[['●',ws("that's"),'c'],["That's",ws("that's")],['your',ws('your',2)]]);
 const h=T(sc,'H ink','left:70px;top:1246px;width:960px;font-size:100px',[['Undivided',ws('undivided')],['\n'],['share',ws('share',2),'hl',1],['of',ws('of',2)],['land',ws('land',2)]]);
 const tg=mk(sc,'tag','left:72px;top:1112px;opacity:0','UDS');
 const b0=ws("that's")-.08,tu=ws('undivided')-b0;
 return t=>{b.style.transform=`scale(${1.16-.1*eio(t/3.4)}) translateY(110px)`;g.style.opacity=cl((t-tu+.1)/.4);rv(k,t);rv(h,t);fade(tg,t,ws('land',2)-b0,.2,10)}},true);
LIGHT.push([ws("that's")-.08,1]);
// 6. Zoom into the coral slice. "In one worked example, 200 flats split 40,000 sq ft of land."
add(ws('worked')-.45,sc=>{sc.style.background='#CEC6BB';const b=box(sc,'compound',540,728);
 const g=svg(b,'',gridSVG());g.style.position='absolute';mk(b,'','position:absolute;left:0;top:1066px;width:1080px;height:1000px;background:#CEC6BB');
 mk(sc,'sh','background:'+LF(52));
 const k=T(sc,'K ink2','left:72px;top:1190px',[['●',ws('worked'),'c'],['One',ws('one',2)],['worked',ws('worked')],['example',ws('example')]]);
 const a=mk(sc,'H ink','left:70px;top:1236px;font-size:104px;opacity:0','0 flats');
 const c=mk(sc,'H ink','left:70px;top:1352px;font-size:104px;opacity:0','0 sq ft');
 const cc=g.querySelector('#cc');
 const b0=ws('worked')-.45,tA=ws('hundred',2)-b0-.2,tB=ws('forty')-b0-.1;
 return t=>{b.style.transform=`scale(${1.0+.2*eio(t/4.5)}) translateY(110px)`;rv(k,t);cnt(a,t,tA,.6,p=>Math.round(200*p)+' flats');cnt(c,t,tB,.7,p=>inr(Math.round(40000*p/100)*100)+' sq ft');
  cc.setAttribute('opacity',.75+.25*Math.sin(t*5))}},true);
// 7. Empty fenced plot, pan right. TEAM PLOT: the whole land is yours
add(ws('team')-.1,sc=>{const b=box(sc,'plot',540,900);b.im.style.filter='brightness(1.04) saturate(1.06)';
 mk(sc,'sh','background:'+GL(46));
 const tg=mk(sc,'tag','left:72px;top:1150px;opacity:0','Team plot');
 const h=T(sc,'H ts','left:70px;top:1222px;width:960px;font-size:112px',[['All',ws('whole')],['the',ws('whole')+.08],['land',ws('land',4),'hl',1],['\n'],['is',ws('is')],['yours.',ws('yours')]]);
 return t=>{b.style.transform=`scale(1.14) translateX(${50-100*eio(t/3.2)}px)`;fade(tg,t,.05,.2,10);rv(h,t)}},true);
LIGHT.push([ws('team')-.1,0]);
// 8. Plot corner close. "...it's the land that tends to gain value while buildings age."
add(ws("it's")-.1,sc=>{const b=box(sc,'plot',300,1060);b.im.style.filter='brightness(1.04) saturate(1.06)';
 mk(sc,'sh','background:'+GL(46));
 const tg=mk(sc,'tag','left:72px;top:1150px','Team plot');
 const h=T(sc,'H ts','left:70px;top:1222px;width:960px;font-size:100px',[['Land',ws('land',5)],['tends',ws('tends')],['to',ws('to')],['\n'],['gain',ws('gain'),'hl',1],['value.',ws('value')],['\n'],['Buildings',ws('buildings')],['age.',ws('age')]]);
 return t=>{b.style.transform=`scale(${1.3+.12*eio(t/3.5)})`;rv(h,t)}},true);
// 9. Real tower facade with trees, push-in. TEAM FLAT
add(ws('team',2)-.1,sc=>{const b=box(sc,'tower2',540,700,'50% 40%');b.im.style.filter='brightness(1.05)';
 mk(sc,'sh','background:'+GL(42));
 const tg=mk(sc,'tag','left:72px;top:1130px;opacity:0','Team flat');
 const h=T(sc,'H ts','left:70px;top:1202px;width:960px;font-size:112px',[['Security.',ws('security'),'hl',1],['\n'],['Lifts.',ws('lifts')],['\n'],['Ready',ws('ready')],['now.',ws('now')]]);
 return t=>{b.style.transform=`scale(${1.08+.1*eio(t/3.6)})`;fade(tg,t,.05,.2,10);rv(h,t)}},true);
LIGHT.push([ws('team',2)-.1,0]);
// 10. The flat key on the family table. "...and no building to manage."
add(ws('no')-.12,sc=>{const b=box(sc,'table',430,960);
 mk(sc,'sh','background:'+GL(48));
 const tg=mk(sc,'tag','left:72px;top:1180px','Team flat');
 const h=T(sc,'H ts','left:70px;top:1252px;width:960px;font-size:112px',[['No',ws('no')],['building',ws('building'),'hl',1],['\n'],['to',ws('to',2)],['manage.',ws('manage')]]);
 return t=>{b.style.transform=`scale(${1.42-.08*eio(t/3)}) translate(${-20+30*eio(t/3)}px,0px)`;rv(h,t)}},true);
LIGHT.push([ws('no')-.12,0]);
// 11. Old society block beside its new tower, pan old to new. "And if your tower is ever redeveloped..."
add(ws('if')-.3,sc=>{const b=box(sc,'redev',540,800);b.im.style.filter='brightness(1.04)';
 mk(sc,'sh','background:'+GL(44));
 const k=T(sc,'K ts','left:72px;top:1150px;color:#fff',[['●',ws('if'),'c'],['If',ws('if')],['your',ws('your',3)],['tower',ws('tower',2)],['is',ws('is',2)],['ever',ws('ever')]]);
 const h=T(sc,'H ts','left:70px;top:1196px;width:960px;font-size:120px',[['Redeveloped?',ws('redeveloped'),'hl',1]]);
 return t=>{b.style.transform=`scale(1.3) translateX(${110-200*eio(t/3.4)}px)`;rv(k,t);rv(h,t)}},true);
LIGHT.push([ws('if')-.3,0]);
// 12. The new tower top. "...that slice decides what you get."
add(ws('slice')-.3,sc=>{const b=box(sc,'redev',730,520);b.im.style.filter='brightness(1.04)';
 mk(sc,'sh','background:'+GL(44));
 const h=T(sc,'H ts','left:70px;top:1196px;width:960px;font-size:112px',[['Your',ws('slice')-.14],['slice',ws('slice'),'hl',1],['decides',ws('decides')],['\n'],['what',ws('what',2)],['you',ws('you',2)],['get.',ws('get')]]);
 return t=>{b.style.transform=`scale(${1.3+.12*eio(t/3)}) translateY(${50-40*eio(t/3)}px)`;rv(h,t)}},true);
// 13. Sale deed with magnifier. "Check it in your sale deed."
add(ws('check')-.1,sc=>{const b=box(sc,'deed',600,900);
 mk(sc,'sh','background:'+LF(50));
 const k=T(sc,'K ink2','left:72px;top:1190px',[['●',ws('check'),'c'],['Check',ws('check')],['it',ws('it',2)]]);
 const h=T(sc,'H ink','left:70px;top:1236px;width:960px;font-size:108px',[['Your',ws('in',3)],['UDS',ws('in',3)+.1,'hl',1],['\n'],['in',ws('sale')-.1],['the',ws('sale')-.05],['sale',ws('sale')],['deed.',ws('deed')]]);
 return t=>{b.style.transform=`scale(${1.12+.18*eio(t/3.2)})`;rv(k,t);rv(h,t)}},true);
LIGHT.push([ws('check')-.1,1]);
// 14. Family table: key and boundary pillar. Send line
add(ws('send')-.12,sc=>{const b=box(sc,'table',580,860);
 mk(sc,'sh','background:'+GL(46));
 const k=T(sc,'K ts','left:72px;top:1170px;color:#fff',[['●',ws('send'),'c'],['Send',ws('send')],['this',ws('this',2)],['to',ws('to',3)]]);
 const h=T(sc,'H ts','left:70px;top:1216px;width:960px;font-size:96px',[['the',ws('the',4)],['one',ws('person')],['in',ws('in',4)],['your',ws('your',5)],['\n'],['family',ws('family',2)],['who',ws('who')],['wants',ws('wants')],['\n'],['a',ws('a',4)],['plot.',ws('plot',3),'hl',1]]);
 return t=>{b.style.transform=`scale(${1.42-.2*eio(t/4)})`;rv(k,t);rv(h,t)}},true);
LIGHT.push([ws('send')-.12,0]);
// 15. Loop: hook frame, easing back to frame 0; silent follow card on top (X15: this reel uses the silent card)
add(WS[WS.length-1][2]+.1,sc=>{const b=box(sc,'hero',546,760);b.im.style.filter='brightness(1.06) saturate(1.08) contrast(1.04)';
 return t=>{b.style.transform=`scale(${1.06-.06*eo(t/2.2)})`}},true);
LIGHT.push([WS[WS.length-1][2]+.1,0]);
