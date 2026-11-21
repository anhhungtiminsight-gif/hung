import json, copy, uuid, time, os, sys
NAME=sys.argv[1]; MV=sys.argv[2]; VV='v1'
T=json.load(open('/mnt/user-data/uploads/com.lveditor.draft/1118_v2/draft_content.json',encoding='utf-8'))
SRC=json.load(open('/home/claude/w/draft_src.json',encoding='utf-8'))
P=json.load(open('plan_base.json')); O=json.load(open('overlays.json')); P3=json.load(open('plan3.json'))
VT=json.load(open('/home/claude/w/voice_timeline.json'))
EDIT='C:/Users/hung/Videos/1121_edit/'
US=lambda s:int(round(s*1e6))
def nid(): return str(uuid.uuid4()).upper()
def index(d):
    ix={}
    for k,v in d['materials'].items():
        if isinstance(v,list):
            for x in v:
                if isinstance(x,dict) and 'id' in x: ix[x['id']]=(k,x)
    return ix
IX=index(T)
D=copy.deepcopy(T)
for k,v in D['materials'].items():
    if isinstance(v,list): D['materials'][k]=[]
D['tracks']=[]; MAT=D['materials']
def add_mat(kind,m): MAT.setdefault(kind,[]).append(m); return m
def new_track(kind,flag=0):
    t={'id':nid(),'type':kind,'flag':flag,'attribute':0,'name':'','is_default_name':True,'segments':[]}; D['tracks'].append(t); return t
def tr(a,d): return {'start':US(a),'duration':US(d)}
TV=[t for t in T['tracks'] if t['type']=='video']
vseg_t=TV[0]['segments'][0]; ovseg_t=TV[1]['segments'][0]
vmat_t=IX[vseg_t['material_id']][1]; ovmat_t=IX[ovseg_t['material_id']][1]
TA=[t for t in T['tracks'] if t['type']=='audio']
allaud=[s for t in TA for s in t['segments']]
voice_seg_t=[s for s in allaud if IX[s['material_id']][1]['type']=='extract_music'][0]
music_seg_t=[s for s in allaud if IX[s['material_id']][1]['type']=='music'][0]
sound_seg_t=[s for s in allaud if IX[s['material_id']][1]['type']=='sound'][0]
def clone_refs(seg,skip=('audio_fades','realtime_denoises','beats')):
    out=[]
    for r in seg['extra_material_refs']:
        if r not in IX: continue
        k,m=IX[r]
        if k in skip: continue
        mm=copy.deepcopy(m); mm['id']=nid(); add_mat(k,mm); out.append((k,mm))
    return out
# ---- video materials from 1121 draft
SIX=index(SRC); vm={}
def vmat(path,w,h,dur,tmpl=vmat_t,name=None):
    if path in vm: return vm[path]
    m=copy.deepcopy(tmpl); m['id']=nid(); m['path']=path; m['material_name']=name or os.path.basename(path)
    m['width'],m['height']=w,h; m['duration']=US(dur)
    for k in ('local_material_id','local_id'):
        if k in m: m[k]=''
    add_mat('videos',m); vm[path]=m; return m
for m in SRC['materials']['videos']:
    vmat(m['path'],m['width'],m['height'],m['duration']/1e6)
trans={m['name']:m for m in T['materials']['transitions']}
src1110=json.load(open('/mnt/user-data/uploads/com.lveditor.draft/1110_v3/draft_content.json',encoding='utf-8'))
for m in src1110['materials']['transitions']: trans.setdefault(m['name'],m)
def vseg(track,tmpl,mat,src_in,src_dur,start,dur,speed,vol,render,scale=1.0,tx=0,ty=0):
    s=copy.deepcopy(tmpl); s['id']=nid(); s['material_id']=mat['id']
    refs=clone_refs(tmpl)
    for k,m in refs:
        if k=='speeds': m['speed']=speed
    s['extra_material_refs']=[m['id'] for _,m in refs]
    s['source_timerange']=tr(src_in,src_dur); s['target_timerange']=tr(start,dur); s['render_timerange']={'start':0,'duration':0}
    s['speed']=speed; s['volume']=vol; s['last_nonzero_volume']=vol if vol>0 else 1.0
    s['clip']={'scale':{'x':scale,'y':scale},'rotation':0.0,'rotation3d':[],'transform':{'x':tx,'y':ty},'flip':{'vertical':False,'horizontal':False},'alpha':1.0}
    s['render_index']=render; s['common_keyframes']=[]; s['keyframe_refs']=[]
    track['segments'].append(s); return s
main=new_track('video')
for i,sh in enumerate(P['shots']):
    m=vm[sh['path']]; sd=sh['out']-sh['in']; dur=round(sd/sh['sp'],6)
    z=sh.get('zoom',1.0); cx,cy=sh.get('c',(0.5,0.5))
    tx=max(-(z-1),min(z-1,(0.5-cx)*2*z)); ty=max(-(z-1),min(z-1,(cy-0.5)*2*z))
    s=vseg(main,vseg_t,m,sh['in'],sd,sh['start'],dur,sh['sp'],sh['vol'],0,z,round(tx,4),round(ty,4)); s['track_render_index']=0
    if sh['vol']>0:
        f={'id':nid(),'type':'audio_fade','fade_type':0,'fade_in_duration':70000,'fade_out_duration':80000}; add_mat('audio_fades',f); s['extra_material_refs'].append(f['id'])
    tn=P3['trans'].get(str(i))
    if tn:
        tm=copy.deepcopy(trans[tn]); tm['id']=nid(); add_mat('transitions',tm); s['extra_material_refs'].insert(2,tm['id'])
# ---- overlays
lanes=[]
for i,o in enumerate(O):
    path=EDIT+f'motion_{MV}/{i+1:02d}-{o["name"]}.mov'
    m=vmat(path,1080,1920,o['dur'],ovmat_t)
    lane=next((L for L in lanes if L['end']<=o['start']-0.01),None)
    if lane is None: lane={'t':new_track('video',2),'end':0,'k':len(lanes)}; lanes.append(lane)
    s=vseg(lane['t'],ovseg_t,m,0,o['dur'],o['start'],o['dur'],1.0,0.0,1+lane['k']); s['track_render_index']=1+lane['k']
    lane['end']=o['start']+o['dur']
# ---- stickers
stk={m['name']:m for m in T['materials']['stickers']}
for m in src1110['materials']['stickers']: stk.setdefault(m['name'],m)
stseg_t=[t for t in T['tracks'] if t['type']=='sticker'][0]['segments'][0]
st=new_track('sticker')
for x in P3['stickers']:
    sm=copy.deepcopy(stk[x['name']]); sm['id']=nid(); add_mat('stickers',sm)
    s=copy.deepcopy(stseg_t); s['id']=nid(); s['material_id']=sm['id']; s['extra_material_refs']=[]
    s['target_timerange']=tr(x['start'],x['dur'])
    s['clip']={'scale':{'x':x['scale'],'y':x['scale']},'rotation':0.0,'rotation3d':[],'transform':{'x':x['x'],'y':x['y']},'flip':{'vertical':False,'horizontal':False},'alpha':1.0}
    st['segments'].append(s)
# ---- effects
fx={m['name']:m for m in T['materials']['video_effects']}
efseg_t=[t for t in T['tracks'] if t['type']=='effect'][0]['segments'][0]
ef=new_track('effect')
for e in sorted(P3['effects'],key=lambda e:e['start']):
    fm=copy.deepcopy(fx[e['name']]); fm['id']=nid(); add_mat('video_effects',fm)
    s=copy.deepcopy(efseg_t); s['id']=nid(); s['material_id']=fm['id']; s['extra_material_refs']=[]; s['target_timerange']=tr(e['start'],e['dur'])
    ef['segments'].append(s)
# ---- filter (look quen dùng của 1118)
ft=[t for t in T['tracks'] if t['type']=='filter'][0]; fseg=copy.deepcopy(ft['segments'][0])
fm=copy.deepcopy(IX[fseg['material_id']][1]); fm['id']=nid(); add_mat('effects',fm)
fseg['id']=nid(); fseg['material_id']=fm['id']; fseg['extra_material_refs']=[]; fseg['target_timerange']=tr(0,P['total'])
nt=new_track('filter'); nt['segments'].append(fseg)
# ---- audio
def amat(seg_t,kind,path,name,dur,src_mat=None):
    m=copy.deepcopy(src_mat if src_mat else IX[seg_t['material_id']][1]); m['id']=nid()
    if not src_mat:
        m['type']=kind; m['path']=path; m['name']=name; m['duration']=US(dur)
        if kind=='extract_music': m['unique_id']=uuid.uuid4().hex; m['music_id']=''; m['effect_id']=''
    add_mat('audios',m); return m
def aseg(track,seg_t,mat,src_in,src_dur,start,vol,fi=0,fo=0,denoise=False):
    s=copy.deepcopy(seg_t); s['id']=nid(); s['material_id']=mat['id']
    refs=[m['id'] for k,m in clone_refs(seg_t)]
    for r in refs:
        pass
    if fi or fo:
        f={'id':nid(),'type':'audio_fade','fade_type':0,'fade_in_duration':US(fi),'fade_out_duration':US(fo)}; add_mat('audio_fades',f); refs.append(f['id'])
    if denoise:
        dn=copy.deepcopy(T['materials']['realtime_denoises'][0]); dn['id']=nid()
        dn['path']='C:/Users/hung/AppData/Local/CapCut/Apps/9.8.0.4213/Resources/audiosami/unet_denoise_44k_music_model_v1.0.model'
        add_mat('realtime_denoises',dn); refs.append(dn['id'])
    s['extra_material_refs']=refs
    s['source_timerange']=tr(src_in,src_dur); s['target_timerange']=tr(start,src_dur)
    s['speed']=1.0; s['volume']=vol; s['last_nonzero_volume']=vol
    track['segments'].append(s); return s
vt=new_track('audio')
for b,t0 in P['voice'].items():
    d=VT[b]['dur']; m=amat(voice_seg_t,'extract_music',EDIT+f'voice_{VV}/voice_{b}.wav','voice_'+b,d)
    aseg(vt,voice_seg_t,m,0,d,t0,1.15,denoise=True)
# music: reuse real material of template drafts by path
MUS={}
for dd in (T,src1110):
    for m in dd['materials']['audios']:
        if m['type']=='music': MUS.setdefault(m['path'],m)
mlanes=[]
for mu in sorted(P3['music'],key=lambda x:x['start']):
    lane=next((L for L in mlanes if L['end']<=mu['start']+0.001),None)
    if lane is None: lane={'t':new_track('audio'),'end':0}; mlanes.append(lane)
    m=amat(music_seg_t,'music',None,None,0,src_mat=MUS[mu['path']])
    aseg(lane['t'],music_seg_t,m,mu['src'],mu['dur'],mu['start'],mu['vol'],mu.get('fi',0.4),mu.get('fo',0.6))
    lane['end']=mu['start']+mu['dur']
SFX={}
for dd in (T,src1110):
    for m in dd['materials']['audios']:
        if m['type']=='sound': SFX.setdefault(m['name'],m)
sl=[]
for sx in sorted(P3['sfx'],key=lambda x:x['start']):
    lane=next((L for L in sl if L['end']<=sx['start']),None)
    if lane is None: lane={'t':new_track('audio'),'end':0}; sl.append(lane)
    src=SFX.get(sx['name']) or [v for k,v in SFX.items() if k.startswith(sx['name'])][0]; m=amat(sound_seg_t,'sound',None,None,0,src_mat=src)
    d=min(sx.get('dur',src['duration']/1e6),src['duration']/1e6)
    aseg(lane['t'],sound_seg_t,m,0,d,sx['start'],sx['vol'])
    lane['end']=sx['start']+d+0.01
D['duration']=US(P['total']); D['id']=nid()
os.makedirs(f'out/{NAME}',exist_ok=True)
json.dump(D,open(f'out/{NAME}/draft_content.json','w',encoding='utf-8'),ensure_ascii=False)
meta=json.load(open('/mnt/user-data/uploads/com.lveditor.draft/1121/draft_meta_info.json',encoding='utf-8'))
meta['draft_id']=nid(); meta['draft_name']=NAME; meta['draft_cover']=''
meta['draft_fold_path']=f'C:/Users/hung/AppData/Local/CapCut/User Data/Projects/com.lveditor.draft/{NAME}'
meta['tm_duration']=US(P['total']); now=int(time.time()*1e6); meta['tm_draft_create']=now; meta['tm_draft_modified']=now
for g in meta.get('draft_materials',[]):
    if isinstance(g,dict) and 'value' in g: g['value']=[]
json.dump(meta,open(f'out/{NAME}/draft_meta_info.json','w',encoding='utf-8'),ensure_ascii=False)
print('tracks',[(t['type'],len(t['segments'])) for t in D['tracks']],'dur',P['total'])
