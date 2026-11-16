// Reel cover in the house template. usage: node cover.cjs <spec.json> <out.jpg>
// spec: {"image": "/abs/path.jpg", "focus": "50% 40%", "kicker": "1 ACRE · GURGAON", "title": "₹50,000 to<br><mark>₹88 crore</mark>", "accent": "#ff3b30", "dark": true}
// Layout keeps everything inside the 3:4 grid crop (y 240 to 1680) so profile tiles look uniform.
const fs=require('fs'),path=require('path');const {chromium}=require(process.env.PW||'/opt/npm-tools/node_modules/playwright');
(async()=>{const [specF,out]=process.argv.slice(2);const S=JSON.parse(fs.readFileSync(specF));const R=path.resolve(__dirname,'../..');
const F=`${R}/engine/node_modules/@fontsource`,acc=S.accent||'#ff3b30';
const html=`<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:IN;font-weight:900;src:url(file://${F}/inter/files/inter-latin-900-normal.woff2)}
@font-face{font-family:IN;font-weight:800;src:url(file://${F}/inter/files/inter-latin-800-normal.woff2)}
@font-face{font-family:PM;font-weight:500;src:url(file://${F}/ibm-plex-mono/files/ibm-plex-mono-latin-500-normal.woff2)}
*{margin:0;padding:0}body{width:1080px;height:1920px;overflow:hidden;background:#0b0f14;font-family:IN}
.bg{position:absolute;inset:0;background:url('file://${S.image}') ${S.focus||'50% 50%'}/cover}
.sh{position:absolute;inset:0;background:linear-gradient(180deg,rgba(6,8,12,.55) 0%,rgba(6,8,12,0) 22%,rgba(6,8,12,0) 45%,rgba(6,8,12,.78) 66%,rgba(6,8,12,.92) 100%)}
.lg{position:absolute;left:84px;top:300px;display:flex;align-items:center;gap:14px;color:#fff;font:800 38px IN;letter-spacing:-.02em}.lg img{width:52px;height:52px;border-radius:12px}.lg b{color:#28c39d}
.k{position:absolute;left:86px;top:1188px;color:#fff;font:500 30px PM;letter-spacing:.18em;text-transform:uppercase}.k:before{content:'';display:inline-block;width:14px;height:14px;border-radius:50%;background:${acc};margin-right:14px;vertical-align:2px}
h1{position:absolute;left:80px;top:1240px;width:930px;color:#fff;font:900 108px/1.0 IN;letter-spacing:-.035em;text-shadow:0 4px 24px rgba(0,0,0,.35)}
mark{background:${acc};color:#fff;padding:0 .1em;border-radius:10px;-webkit-box-decoration-break:clone}
</style></head><body><div class="bg"></div><div class="sh"></div><div class="lg"><img src="file://${R}/library/brand/trueyards-icon.png"><span>True<b>Yards</b></span></div><div class="k">${S.kicker||''}</div><h1>${S.title}</h1></body></html>`;
const tmp=path.join(require('os').tmpdir(),'cover_'+Date.now()+'.html');fs.writeFileSync(tmp,html);
const b=await chromium.launch({args:['--allow-file-access-from-files']});const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+tmp);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
const h=await p.evaluate(()=>{const e=document.querySelector('h1');return e.getBoundingClientRect().bottom});
if(h>1640)console.log('WARN title bottom at',Math.round(h),'px, outside the 3:4 grid crop; shorten the title');
await p.screenshot({path:out,type:'jpeg',quality:92});await b.close();console.log('cover',out)})();
