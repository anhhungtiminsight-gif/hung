import json, uuid, time, copy, os
SRC='/home/claude/w/draft_src.json'
META='/mnt/user-data/uploads/com.lveditor.draft/1121/draft_meta_info.json'
ROOT='C:/Users/hung/AppData/Local/CapCut/User Data/Projects/com.lveditor.draft'
def nid(): return str(uuid.uuid4()).upper()
def US(t): return int(round(t*1e6))
def write_draft(D,name,outdir,dur):
    os.makedirs(outdir,exist_ok=True)
    D['id']=nid(); D['duration']=US(dur)
    json.dump(D,open(f'{outdir}/draft_content.json','w',encoding='utf-8'),ensure_ascii=False)
    m=json.load(open(META,encoding='utf-8'))
    m['draft_id']=nid(); m['draft_name']=name; m['draft_cover']=''
    m['draft_fold_path']=f'{ROOT}/{name}'; m['tm_duration']=US(dur)
    now=int(time.time()*1e6); m['tm_draft_create']=now; m['tm_draft_modified']=now
    for g in m.get('draft_materials',[]):
        if isinstance(g,dict) and 'value' in g: g['value']=[]
    json.dump(m,open(f'{outdir}/draft_meta_info.json','w',encoding='utf-8'),ensure_ascii=False)
