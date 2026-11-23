const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const a=process.argv.slice(2);const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
await p.goto('file:///home/claude/reel3/reel.html');await p.evaluate(()=>window.ready);
if(a[0]=='stills'){for(const t of a.slice(1)){await p.evaluate(t=>window.setT(t),parseFloat(t));await p.screenshot({path:`/home/claude/reel3/still_${t}.jpg`,type:'jpeg',quality:88})}}
else{const fps=30,end=parseFloat(a[1]||'22.6'),st=parseFloat(a[0]||'0');for(let i=Math.round(st*fps);i<Math.round(end*fps);i++){await p.evaluate(t=>window.setT(t),i/fps);await p.screenshot({path:`/home/claude/reel3/frames/f${String(i).padStart(5,'0')}.jpg`,type:'jpeg',quality:92})}}
await b.close()})();
