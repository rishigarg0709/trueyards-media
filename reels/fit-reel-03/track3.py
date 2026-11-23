import subprocess, os, sys, json
F=30; C=json.load(open(f"cfg-{sys.argv[1]}.json")); L=C["lang"]
lst=[]
for i,(a,b,src,off,sp,gr,z0) in enumerate(C["shots"]):
    n=round(b*F)-round(a*F); out=f'{L}seg{i:02d}.mp4'; lst.append(out)
    if src is None:
        cmd=['ffmpeg','-y','-loglevel','error','-f','lavfi','-i',f'color=c=black:s=1080x1920:r={F}','-frames:v',str(n)]
    else:
        vf=(f"setpts=PTS/{sp},fps={F},scale=2160:3840:flags=bicubic,{gr},"
            f"zoompan=z='{z0}*(1.02+0.07*exp(-on/3.5)+0.0007*on)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps={F},unsharp=5:5:0.6")
        cmd=['ffmpeg','-y','-loglevel','error','-stream_loop','-1','-ss',str(off),'-i',src+'.mp4','-an','-vf',vf,'-frames:v',str(n)]
    cmd+=['-c:v','libx264','-crf','14','-preset','fast','-pix_fmt','yuv420p','-r',str(F),out]
    r=subprocess.run(cmd); print(i,src,n,r.returncode,flush=True)
open(f'list-{L}.txt','w').write(''.join(f"file '{x}'\n" for x in lst))
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',f'list-{L}.txt','-c','copy',f'track-{L}.mp4'],check=True)
print("track ok")
