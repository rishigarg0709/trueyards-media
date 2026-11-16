const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({args:['--allow-file-access-from-files']});const p=await b.newPage({viewport:{width:1080,height:1350}});
await p.goto('file://'+process.cwd()+'/slides.html');await p.evaluate(()=>document.fonts.ready);
for(let i=1;i<=9;i++){const e=await p.$('#s'+i);await e.screenshot({path:`slide-${i}.jpg`,type:'jpeg',quality:92});}
await b.close();})();
