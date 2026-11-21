import json, subprocess, numpy as np, soundfile as sf, os, sys
MV=sys.argv[1]; OUT=sys.argv[2]
P=json.load(open('plan_base.json')); O=json.load(open('overlays.json')); P3=json.load(open('plan3.json')); VT=json.load(open('/home/claude/w/voice_timeline.json'))
FULL='/home/claude/w/ana/full.mp4'; W,H=480,854; SR=48000
os.makedirs('pv',exist_ok=True)
segs=[]
for i,s in enumerate(P['shots']):
    z=s.get('zoom',1.0); cx,cy=s.get('c',(0.5,0.5))
    vf=f"setpts=(PTS-STARTPTS)/{s['sp']}"
    if z>1:
        cw,ch=W/z,H/z; x0=min(max(cx*W-cw/2,0),W-cw); y0=min(max(cy*H-ch/2,0),H-ch)
        vf+=f",crop={cw:.0f}:{ch:.0f}:{x0:.0f}:{y0:.0f},scale={W}:{H}"
    vf+=f",fps=30,trim=duration={s['dur']:.3f}"
    o=f'pv/s{i:02d}.mp4'
    subprocess.run(['ffmpeg','-v','error','-y','-ss',f"{s['a']:.3f}",'-t',f"{s['b']-s['a']+0.1:.3f}",'-i',FULL,'-vf',vf,'-an','-c:v','libx264','-preset','veryfast','-crf','26',o],check=True)
    segs.append(o)
open('pv/list.txt','w').write(''.join(f"file '{os.path.abspath(x)}'\n" for x in segs))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','pv/list.txt','-c','copy','pv/base.mp4'],check=True)
# overlays
inputs=['-i','pv/base.mp4']; fc=[]; last='0:v'
for k,o in enumerate(O):
    inputs+=['-itsoffset',f"{o['start']:.3f}",'-i',f'motion_{MV}/{k+1:02d}-{o["name"]}.mov']
    fc.append(f"[{k+1}:v]scale={W}:{H},format=rgba[o{k}]")
    fc.append(f"[{last}][o{k}]overlay=0:0:eof_action=pass:enable='between(t,{o['start']:.3f},{o['start']+o['dur']:.3f})'[v{k}]"); last=f'v{k}'
subprocess.run(['ffmpeg','-v','error','-y']+inputs+['-filter_complex',';'.join(fc),'-map',f'[{last}]','-c:v','libx264','-preset','veryfast','-crf','27','pv/vid.mp4'],check=True)
# audio mix
N=int((P['total']+0.5)*SR); mix=np.zeros(N,np.float32)
def load(path,ss=0,t=None,tempo=None):
    cmd=['ffmpeg','-v','error','-ss',f'{ss:.3f}']+(['-t',f'{t:.3f}'] if t else [])+['-i',path]+(['-af',f'atempo={tempo}'] if tempo else [])+['-ac','1','-ar',str(SR),'-f','f32le','-']
    return np.frombuffer(subprocess.check_output(cmd),np.float32).copy()
def put(y,t0,vol,fi=0,fo=0):
    y=y*vol; n1=int(fi*SR); n2=int(fo*SR)
    if n1 and len(y)>n1: y[:n1]*=np.linspace(0,1,n1)
    if n2 and len(y)>n2: y[-n2:]*=np.linspace(1,0,n2)
    i=int(t0*SR); j=min(N,i+len(y)); mix[i:j]+=y[:j-i]
for s in P['shots']:
    if s['vol']>0: put(load(FULL,s['a'],s['b']-s['a'],s['sp'])[:int(s['dur']*SR)],s['start'],s['vol'],0.07,0.08)
for b,t0 in P['voice'].items(): put(load(f'/home/claude/w/voice/voice_{b}.wav'),t0,1.15)
for m in P3['music']: put(load('/mnt/user-data/uploads/music/'+os.path.basename(m['path']),m['src'],m['dur']),m['start'],m['vol'],m['fi'],m['fo'])
D=json.load(open('out/1121_v2/draft_content.json'))
sp={a['name']:a['path'] for a in D['materials']['audios'] if a['type']=='sound'}
for x in P3['sfx']:
    p=sp.get(x['name']) or [v for k,v in sp.items() if k.startswith(x['name'])][0]
    put(load('/mnt/user-data/uploads/music/'+os.path.basename(p)),x['start'],x['vol'])
mix=np.clip(mix,-1,1); sf.write('pv/mix.wav',mix,SR)
subprocess.run(['ffmpeg','-v','error','-y','-i','pv/vid.mp4','-i','pv/mix.wav','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','128k','-shortest',OUT],check=True)
print('ok',OUT)
