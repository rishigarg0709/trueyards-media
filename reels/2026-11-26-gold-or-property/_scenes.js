const HOOKEV=ws('property');
const AMB='#F2B33D';
const num=(p,css)=>mk(p,'N ts',css+';opacity:0','');
// 1. HOOK: bright impossible-real tower with one floor of solid gold, push-in from frame 0, line spoken from 0 s; no text until 1.5 s
add(0,sc=>{const b=box(sc,'hero',540,760);b.im.style.filter='brightness(1.14) saturate(1.1) contrast(1.03)';
 const gd=mk(sc,'sh','opacity:0;background:'+GL(50));
 const tA=1.55;
 const k=T(sc,'K ts','left:72px;top:1196px;color:#F7F1E3',[['●',tA,'c'],['Uncle',tA],['vs',tA+.08],['aunt',ws('aunt')]]);
 const h=T(sc,'H ts','left:70px;top:1244px;width:960px;font-size:132px',[['Property',tA],['\n'],['or',ws('just')],['gold?',ws('gold'),'hl',1]]);
 return t=>{b.style.transform=`scale(${1.24+.12*eio(t/4.2)})`;gd.style.opacity=cl((t-tA+.35)/.4);rv(k,t);rv(h,t)}});
LIGHT.push([0,0]);
// 2. Close on the gold floor, pull-out. "Who's right? Let's check the numbers."
add(ws("who's")-.1,sc=>{const b=box(sc,'hero',520,770);b.im.style.filter='brightness(1.1) saturate(1.1)';
 const br=cab(corners(b,90,650,1000,905,40,5));
 mk(sc,'sh','background:'+GL(50));
 const k=T(sc,'K ts','left:72px;top:1196px;color:#F7F1E3',[['●',ws("let's"),'c'],["Let's",ws("let's")],['check',ws('check')]]);
 const h=T(sc,'H ts','left:70px;top:1244px;width:960px;font-size:128px',[["Who's",ws("who's")],['right?',ws('right'),'hl',1]]);
 return t=>{b.style.transform=`scale(${1.75-.25*eio(t/1.8)})`;crn(br,t,.2);rv(k,t);rv(h,t)}},true);
// 3. Real gold jewellery shop, pan. "Gold first."
add(ws('gold',2)-.1,sc=>{const b=box(sc,'shop',540,700,'50% 50%');b.im.style.filter='brightness(1.05)';
 mk(sc,'sh','background:'+GL(46));
 const tg=mk(sc,'tag','left:72px;top:1150px;opacity:0','Gold · 24K · per 10 g');
 const h=T(sc,'H ts','left:70px;top:1222px;width:960px;font-size:140px',[['Gold',ws('gold',2),'hl',1],['first.',ws('first')]]);
 return t=>{b.style.transform=`scale(1.12) translateX(${60-120*eio(t/1.4)}px)`;fade(tg,t,.1,.2,10);rv(h,t)}},true);
LIGHT.push([ws('gold',2)-.1,0]);
// 4. Coins, bar and house key on navy velvet. "In 2010, ten grams cost about 18,500 rupees."
add(ws('in')-.08,sc=>{const b=box(sc,'coinkey',540,900);b.im.style.filter='brightness(1.12) saturate(1.05)';
 mk(sc,'sh','background:'+GL(50));
 const k=T(sc,'K ts','left:72px;top:1180px;color:#F7F1E3',[['●',ws('2010'),'c'],['2010',ws('2010')],['·',ws('ten')],['10',ws('ten')],['g',ws('grams')]]);
 const n=num(sc,'left:56px;top:1226px;color:#F7F1E3');
 const b0=ws('in')-.08,tn=ws('eighteen')-b0-.05;
 return t=>{b.style.transform=`scale(${1.12+.1*eio(t/4)}) translateY(-80px)`;rv(k,t);const p=cnt(n,t,tn,.7,p=>'₹'+inr(Math.round(18500*p/100)*100));n.style.color=p>=1?AMB:'#F7F1E3'}},true);
LIGHT.push([ws('in')-.08,0]);
// 5. Push-in on the gold stack. "This month? About 1,37,000. Roughly seven times."
add(ws('this')-.1,sc=>{const b=box(sc,'coinkey',330,820);b.im.style.filter='brightness(1.12) saturate(1.05)';
 mk(sc,'sh','background:'+GL(50));
 const k=T(sc,'K ts','left:72px;top:1180px;color:#F7F1E3',[['●',ws('this'),'c'],['November',ws('month')],['2026',ws('month')+.1]]);
 const n=num(sc,'left:56px;top:1226px;color:#F7F1E3');
 const tg=mk(sc,'tag','left:72px;top:1440px;opacity:0;font-size:34px','≈ 7x since 2010');
 const b0=ws('this')-.1,tn=ws('one')-b0-.05,ts7=ws('seven')-b0;
 return t=>{b.style.transform=`scale(${1.5+.14*eio(t/4.2)}) translate(60px,-40px)`;rv(k,t);const p=cnt(n,t,tn,.8,p=>'₹'+inr(Math.round(136950*p/50)*50));n.style.color=p>=1?AMB:'#F7F1E3';slam(tg,t,ts7,1.6,0)}},true);
// 6. The gold floor again, pull-out. "But this month gold also fell 1,600 rupees in a single weekend."
add(ws('but')-.1,sc=>{const b=box(sc,'hero',540,770);b.im.style.filter='brightness(1.1) saturate(1.1)';
 mk(sc,'sh','background:'+GL(50));
 const k=T(sc,'K ts','left:72px;top:1180px;color:#F7F1E3',[['●',ws('but'),'c'],['Gold',ws('gold',3)],['also',ws('also')],['fell',ws('fell')]]);
 const n=mk(sc,'N ts','left:56px;top:1226px;color:'+AMB+';opacity:0','−₹1,690');
 const u=T(sc,'M ts','left:70px;top:1430px;font-size:64px',[['in',ws('in',2)],['one',ws('single')],['weekend',ws('weekend'),'hl',1]]);
 const b0=ws('but')-.1,tf=ws('sixteen')-b0;
 return t=>{b.style.transform=`scale(${1.62-.3*eio(t/4.4)})`;rv(k,t);slam(n,t,tf,1.5,0);rv(u,t);b.style.marginLeft=shake(t,tf,8)+'px'}},true);
// 7. Real Indian apartment balconies, tilt up. "Now property. The RBI tracks home prices in 18 cities."
add(ws('now')-.1,sc=>{const b=box(sc,'balc',540,700,'50% 60%');b.im.style.filter='brightness(1.05)';
 mk(sc,'sh','background:'+GL(44));
 const tg=mk(sc,'tag','left:72px;top:1130px;opacity:0','Now: property');
 const h=T(sc,'H ts','left:70px;top:1202px;width:960px;font-size:104px',[['RBI',ws('rbi'),'hl',1],['house',ws('tracks')],['price',ws('home')],['\n'],['index',ws('prices')],['·',ws('eighteen',2)],['18',ws('eighteen',2)],['cities',ws('cities')]]);
 return t=>{b.style.transform=`scale(1.1) translateY(${-90+150*eio(t/4.4)}px)`;fade(tg,t,.05,.2,10);rv(h,t)}},true);
LIGHT.push([ws('now')-.1,0]);
// 8. Coin staircase vs house models. "In one quarter last year, that index actually fell."
add(ws('in',4)-.1,sc=>{const b=box(sc,'stairs',600,860);b.im.style.filter='brightness(1.2) saturate(1.05)';
 mk(sc,'sh','background:'+GL(50));
 const k=T(sc,'K ts','left:72px;top:1180px;color:#F7F1E3',[['●',ws('quarter'),'c'],['Jul',ws('quarter')],['to',ws('quarter')+.05],['Sep',ws('quarter')+.1],['2025',ws('last')]]);
 const n=mk(sc,'N ts','left:56px;top:1226px;font-size:150px;color:#F7F1E3;opacity:0','113.4 → 112.7');
 const h=T(sc,'H ts','left:70px;top:1400px;width:960px;font-size:96px',[['It',ws('fell',2)],['fell.',ws('fell',2),'hl',1]]);
 const b0=ws('in',4)-.1,tn=ws('quarter')-b0+.25;
 return t=>{b.style.transform=`scale(${1.2+.06*eio(t/3.4)}) translateX(${40-90*eio(t/3.4)}px)`;rv(k,t);fade(n,t,tn,.3,20);rv(h,t)}},true);
// 9. Push on the houses. "So yes, property falls too. Quietly."
add(ws('so')-.1,sc=>{const b=box(sc,'stairs',780,860);b.im.style.filter='brightness(1.2) saturate(1.05)';
 mk(sc,'sh','background:'+GL(50));
 const h=T(sc,'H ts','left:70px;top:1220px;width:960px;font-size:116px',[['Property',ws('property',3)],['\n'],['falls',ws('falls',2),'hl',1],['too.',ws('too')]]);
 const k=T(sc,'K ts','left:72px;top:1470px;color:#F7F1E3',[['Quietly.',ws('quietly')]]);
 return t=>{b.style.transform=`scale(${1.5+.12*eio(t/2.6)})`;rv(h,t);rv(k,t)}},true);
// 10. Balconies again, upper floors, push-in. "Lately, it is up about 3.5% a year."
add(ws('lately')-.1,sc=>{const b=box(sc,'balc',540,420,'50% 30%');b.im.style.filter='brightness(1.05)';
 mk(sc,'sh','background:'+GL(44));
 const k=T(sc,'K ts','left:72px;top:1150px;color:#F7F1E3',[['●',ws('lately'),'c'],['Latest',ws('lately')],['RBI',ws('lately')+.1],['reading',ws('it')]]);
 const n=num(sc,'left:56px;top:1196px;color:#F7F1E3');
 const u=T(sc,'M ts','left:70px;top:1400px;font-size:64px',[['a',ws('a',4)],['year',ws('year',2),'hl',1]]);
 const b0=ws('lately')-.1,tn=ws('three')-b0-.05;
 return t=>{b.style.transform=`scale(${1.25+.1*eio(t/2.6)})`;rv(k,t);const p=cnt(n,t,tn,.6,p=>'+'+(3.6*p).toFixed(1)+'%');n.style.color=p>=1?AMB:'#F7F1E3';rv(u,t)}},true);
// 11. Open flat door, warm light. "A flat can pay you rent, or save yours."
add(ws("here's")-.1,sc=>{const b=box(sc,'door',80,820);b.im.style.filter='brightness(1.12)';
 mk(sc,'sh','background:'+GL(50));
 const k=T(sc,'K ts','left:72px;top:1150px;color:#F7F1E3',[['●',ws("here's"),'c'],['What',ws('what')],['the',ws('the',3)],['gold',ws('gold',4)],['chart',ws('chart')],['misses',ws('misses')]]);
 const h=T(sc,'H ts','left:70px;top:1198px;width:960px;font-size:104px',[['A',ws('a',5)],['flat',ws('flat')],['can',ws('can')],['\n'],['pay',ws('pay')],['rent,',ws('rent'),'hl',1],['\n'],['or',ws('or')],['save',ws('save')],['yours.',ws('yours')]]);
 return t=>{b.style.transform=`scale(${1.5+.1*eio(t/4.6)})`;rv(k,t);rv(h,t)}},true);
LIGHT.push([ws("here's")-.1,0]);
// 12. Bank locker corridor. "Gold just sits in the locker."
add(ws('gold',5)-.1,sc=>{const b=box(sc,'locker',540,640);b.im.style.filter='brightness(1.15)';
 mk(sc,'sh','background:'+GL(48));
 const tg=mk(sc,'tag','left:72px;top:1150px;opacity:0','Gold');
 const h=T(sc,'H ts','left:70px;top:1222px;width:960px;font-size:118px',[['No',ws('sits')],['income.',ws('locker'),'hl',1]]);
 return t=>{b.style.transform=`scale(${1.12+.16*eio(t/1.8)})`;fade(tg,t,.05,.2,10);rv(h,t)}},true);
// 13. Open locker close. "And gold sells in minutes."
add(ws('and',3)-.1,sc=>{const b=box(sc,'locker',600,640);b.im.style.filter='brightness(1.15)';
 mk(sc,'sh','background:'+GL(48));
 const tg=mk(sc,'tag','left:72px;top:1150px','Gold');
 const h=T(sc,'H ts','left:70px;top:1222px;width:960px;font-size:118px',[['Sells',ws('sells')],['in',ws('in',6)],['\n'],['minutes.',ws('minutes'),'hl',1]]);
 return t=>{b.style.transform=`scale(${2.3+.15*eio(t/1.9)}) translateY(-40px)`;rv(h,t)}},true);
// 14. Keys in the flat door. "A flat takes months, and stamp duty in Delhi starts at 6%."
add(ws('a',6)-.1,sc=>{const b=box(sc,'door',470,620);b.im.style.filter='brightness(1.12)';
 mk(sc,'sh','background:'+GL(48));
 const tg=mk(sc,'tag','left:72px;top:1150px;opacity:0','Flat');
 const h=T(sc,'H ts','left:70px;top:1222px;width:960px;font-size:118px',[['Takes',ws('takes')],['months.',ws('months'),'hl',1]]);
 const u=T(sc,'M ts','left:70px;top:1380px;font-size:62px',[['+',ws('stamp')],['stamp',ws('stamp')],['duty',ws('duty')],['from',ws('starts')],['6%',ws('six'),'hl',1]]);
 const k=T(sc,'K ts','left:72px;top:1470px;color:#F7F1E3',[['Delhi',ws('delhi')]]);
 return t=>{b.style.transform=`scale(${1.9-.18*eio(t/4)})`;fade(tg,t,.05,.2,10);rv(h,t);rv(u,t);rv(k,t)}},true);
// 15. Send line over the hero, wide like frame 0
add(ws('send')-.1,sc=>{const b=box(sc,'hero',540,760);b.im.style.filter='brightness(1.14) saturate(1.1) contrast(1.03)';
 mk(sc,'sh','background:'+GL(48));
 const k=T(sc,'K ts','left:72px;top:1150px;color:#F7F1E3',[['●',ws('send'),'c'],['Send',ws('send')],['this',ws('this',3)],['to',ws('to')]]);
 const h=T(sc,'H ts','left:70px;top:1196px;width:960px;font-size:92px',[['the',ws('the',5)],['uncle',ws('uncle',2),'hl',1],['who',ws('who')],['says',ws('says',3)],['\n'],['property',ws('property',4)],['\n'],['never',ws('never',2)],['falls.',ws('falls',3)]]);
 return t=>{b.style.transform=`scale(${1.12+.08*eio(t/2.8)})`;rv(k,t);rv(h,t)}},true);
// 16. Loop: back to the frame-0 framing; silent follow card on top (X15: silent card this reel)
add(WS[WS.length-1][2]+.1,sc=>{const b=box(sc,'hero',540,760);b.im.style.filter='brightness(1.14) saturate(1.1) contrast(1.03)';
 return t=>{b.style.transform=`scale(${1.3-.06*eo(t/2.2)})`}},true);
LIGHT.push([WS[WS.length-1][2]+.1,0]);
