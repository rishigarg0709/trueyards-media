const { chromium } = require('/opt/npm-tools/node_modules/playwright');const path=require('path');const {spawn}=require('child_process');const fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
const cfg=JSON.parse(fs.readFileSync(path.join(__dirname,process.argv[4]),'utf8'));await p.addInitScript(c=>{window.CFG=c},cfg);await p.goto('file://'+path.join(__dirname,'ov3.html'));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(800);
const a=parseInt(process.argv[2]),e=parseInt(process.argv[3]);const out=path.join(__dirname,`ov-${process.argv[5]}-${a}.mov`);const tmp=out.replace('.mov','.tmp.mov');
const ff=spawn('ffmpeg',['-y','-loglevel','error','-f','image2pipe','-framerate','30','-c:v','png','-i','-','-c:v','qtrle','-pix_fmt','argb','-r','30',tmp]);
const done=new Promise(r=>ff.on('close',r));ff.stderr.on('data',d=>process.stderr.write(d));
for(let i=a;i<e;i++){await p.evaluate(f=>window.__seek(f),i);const buf=await p.screenshot({omitBackground:true,type:'png'});if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));}
ff.stdin.end();const code=await done;if(code===0)fs.renameSync(tmp,out);console.log(a,e,code);await b.close();})();
