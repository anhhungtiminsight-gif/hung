import json, numpy as np, subprocess, soundfile as sf, sys
TEMPO=float(sys.argv[1]) if len(sys.argv)>1 else 1.10
CAP=0.28
x,sr=sf.read('v_48.wav'); x=x.astype(np.float32)
db=np.load('v_db.npy'); TH=np.percentile(db,95)-34
plan=json.load(open('voice_plan.json'))
runs=[];st=None
for i,v in enumerate(db):
    if v<TH-6 and st is None: st=i
    if v>=TH-6 and st is not None: runs.append((i-st,st,i)); st=None
L,a,b=max(runs); room=x[int(a/100*sr)+2400:int(b/100*sr)-2400]
def tone(n): return np.tile(room,n//max(1,len(room))+2)[:n]*0.8
def fade(s,i,o):
    s=s.copy(); n1=int(sr*i/1000); n2=int(sr*o/1000)
    if n1: s[:n1]*=np.linspace(0,1,n1)
    if n2: s[-n2:]*=np.linspace(1,0,n2)
    return s
def pieces(s,e):
    a=int(s*100); b=int(e*100); out=[]; cur=a; i=a
    while i<b:
        if db[i]<TH:
            j=i
            while j<b and db[j]<TH: j+=1
            if (j-i)/100>CAP and i>a+3 and j<b-3:
                keep=CAP/2
                out.append((cur/100,i/100+keep)); cur=j-keep*100
            i=j
        else: i+=1
    out.append((cur/100,b/100)); return out
info={}; allparts=[]
for blk,sp in plan.items():
    parts=[tone(int(0.06*sr))]; lines=[]
    for c in sp:
        t0=sum(len(p) for p in parts)/sr
        for s,e in pieces(c['s'],c['e']):
            seg=x[int(s*sr):int(e*sr)]
            parts.append(fade(seg,10,25))
        lines.append((c['text'],round(t0/TEMPO,3),round(sum(len(p) for p in parts)/sr/TEMPO,3),c['s'],c['e']))
        if c['gap']>0: parts.append(tone(int(c['gap']*TEMPO*sr)))
    parts.append(tone(int(0.15*sr)))
    y=np.concatenate(parts)
    sf.write(f'voice/raw_{blk}.wav',y,sr)
    subprocess.run(['ffmpeg','-v','error','-y','-i',f'voice/raw_{blk}.wav','-af',f'atempo={TEMPO},loudnorm=I=-16:TP=-1.5:LRA=9','-ar','48000','-ac','1',f'voice/voice_{blk}.wav'],check=True)
    d=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'voice/voice_{blk}.wav']))
    info[blk]={'dur':round(d,3),'lines':lines}; print(blk,round(d,2))
json.dump(info,open('voice_timeline.json','w'),ensure_ascii=False,indent=1)
