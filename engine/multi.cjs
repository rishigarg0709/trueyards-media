const { chromium } = require('/opt/npm-tools/node_modules/playwright');const path=require('path');
(async()=>{const file=process.argv[2],n=Number(process.argv[3]),scale=Number(process.argv[4]||1);const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080*n,height:1350},deviceScaleFactor:scale});
p.on('pageerror',e=>console.log('ERR',e.message));p.on('requestfailed',r=>console.log('FAIL',r.url().split('/').pop()));
await p.goto('file://'+path.resolve(file));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(900);
const over=await p.evaluate(()=>{const out=[];document.querySelectorAll('#c .t').forEach(e=>{const r=e.getBoundingClientRect();const a=Math.floor((r.left+1)/1080),z=Math.floor((r.right-1)/1080);const m=Math.min(r.left-a*1080,(z+1)*1080-r.right);if(a!=z||m<56||r.bottom>1330||e.scrollWidth>e.clientWidth+2)out.push('EDGE s'+(a+1)+' '+Math.round(r.left-a*1080)+'-'+Math.round(r.right-a*1080)+' b'+Math.round(r.bottom)+' '+e.textContent.trim().slice(0,34))});return out});
console.log(over.join('\n')||'no edge issues');
await p.screenshot({path:path.resolve(file.replace('.html','.png')),type:'png'});
await b.close();})();
