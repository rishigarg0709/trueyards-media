const { chromium } = require('/opt/npm-tools/node_modules/playwright');const path=require('path');const fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
const cfg=JSON.parse(fs.readFileSync(path.join(__dirname,process.argv[2]),'utf8'));await p.addInitScript(c=>{window.CFG=c},cfg);
await p.goto('file://'+path.join(__dirname,'ov3.html'));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(600);
for(const t of process.argv.slice(4)){await p.evaluate(f=>window.__seek(f),Math.round(parseFloat(t)*30));await p.screenshot({path:`${process.argv[3]}-${t}.png`,omitBackground:true});}
await b.close();})();
