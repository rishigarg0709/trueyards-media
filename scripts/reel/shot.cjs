// Renders at 2x by default: 1080x1920 layout -> 2160x3840 (4K UHD vertical) frames. SCALE=1 for quick drafts.
// usage: node shot.cjs <reel_dir> stills t1 t2 ...   |   node shot.cjs <reel_dir> <start> <end>
const path=require('path');const {chromium}=require(process.env.PW||'/opt/npm-tools/node_modules/playwright');
(async()=>{const [dir,...a]=process.argv.slice(2);const D=path.resolve(dir);
const b=await chromium.launch({args:['--allow-file-access-from-files','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:Number(process.env.SCALE||2)});p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto('file://'+D+'/reel.html');await p.evaluate(()=>window.ready);
if(a[0]=='stills'){for(const t of a.slice(1)){await p.evaluate(t=>window.setT(t),parseFloat(t));await p.screenshot({path:`${D}/still_${t}.jpg`,type:'jpeg',quality:88})}}
else{const fps=30,st=parseFloat(a[0]),end=parseFloat(a[1]);for(let i=Math.round(st*fps);i<Math.round(end*fps);i++){await p.evaluate(t=>window.setT(t),i/fps);await p.screenshot({path:`${D}/frames/f${String(i).padStart(5,'0')}.jpg`,type:'jpeg',quality:95})}}
await b.close()})();
