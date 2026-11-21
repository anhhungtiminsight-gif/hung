import json, copy, subprocess, sys, numpy as np, soundfile as sf
from mk_draft_util import *
V=sys.argv[1]
info=json.load(open('voice_timeline.json')); sr=48000
parts=[]; marks=[]
for b in info:
    y,_=sf.read(f'voice/voice_{b}.wav'); marks.append((b,round(sum(len(p) for p in parts)/sr,2)))
    parts+= [y, np.zeros(sr)]
sf.write(f'voice/kiemtra_voice_{V}.wav',np.concatenate(parts),sr)
dur=sum(len(p) for p in parts)/sr; print(marks,dur)
D=json.load(open(SRC))
at=copy.deepcopy([t for t in D['tracks'] if t['type']=='audio'][0])
a=copy.deepcopy(D['materials']['audios'][0])
a['id']=nid(); a['type']='extract_music'; a['name']=f'kiemtra_voice_{V}'
a['path']=f'C:/Users/hung/Videos/1121_edit/voice_{V}/kiemtra_voice_{V}.wav'; a['duration']=US(dur)
D['materials']['audios']=[a]
s=at['segments'][0]; s['id']=nid(); s['material_id']=a['id']
s['source_timerange']={'start':0,'duration':US(dur)}; s['target_timerange']={'start':0,'duration':US(dur)}
at['segments']=[s]; at['id']=nid()
D['tracks']=[at]; D['materials']['texts']=[]
name=f'1121_kiemtra_voice_{V}'
write_draft(D,name,f'out/{name}',dur)
json.dump(marks,open(f'voice/marks_{V}.json','w'))
