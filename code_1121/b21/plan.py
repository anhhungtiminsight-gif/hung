import json
SRC=json.load(open('/home/claude/w/draft_src.json',encoding='utf-8'))
mats={m['id']:m for m in SRC['materials']['videos']}
CLIPS=[]
for s in [t for t in SRC['tracks'] if t['type']=='video'][0]['segments']:
    m=mats[s['material_id']]
    CLIPS.append(dict(path=m['path'],start=s['target_timerange']['start']/1e6,dur=m['duration']/1e6,w=m['width'],h=m['height'],mid=m['id']))
def loc(a,b):
    for c in CLIPS:
        if c['start']-1e-6<=a<c['start']+c['dur']:
            assert b<=c['start']+c['dur']+1e-6,(a,b)
            return c['path'],round(a-c['start'],3),round(b-c['start'],3)
    raise Exception(a)
VT=json.load(open('/home/claude/w/voice_timeline.json')); VW=json.load(open('/home/claude/w/vwords.json'))
S=[]
def add(sec,a,b,sp,vol=0.0,**kw): S.append(dict(sec=sec,a=a,b=b,sp=sp,vol=vol,**kw))
# HOOK: thoại trực tiếp
for a,b in [(3.55,8.60),(10.95,13.15),(15.50,18.90),(19.08,21.55)]: add('HK',a,b,1.05,1.6)
# A: từ đầu → tách màn khỏi khung
for a,b,sp in [(26.0,30.3,1.5),(32.4,35.6,1.3),(38.0,42.6,1.2),(62.6,65.8,1.0),(85.0,88.5,1.2),(159.5,165.0,1.5),
               (195.5,200.5,1.5),(304.0,306.9,1.0),(335.5,340.0,1.4),(361.5,367.5,1.6),(708.5,713.5,1.4)]: add('A',a,b,sp)
add('A',810.8,815.0,1.0,tag='tach_man')
# B: bóc keo đen, mỗi cảnh 2-3s
for a,b in [(827.0,830.0),(830.5,833.5),(837.5,840.5),(841.0,844.0)]: add('B',a,b,1.2)
# C: bóc seal + lên kính hiển vi
add('C',956.0,962.0,1.5); add('C',981.0,986.5,1.5); add('C',1032.1,1035.8,1.0,tag='kinh')
# D: vết chập cháy trên màn (màn hình kính hiển vi)
Z=dict(zoom=1.2,c=(0.52,0.55))
add('D',1037.6,1045.5,1.0,**Z)
# E: vết cháy đen trên cáp
add('E',1046.5,1052.0,1.0,**Z); add('E',1052.0,1058.0,1.2,**Z); add('E',1058.0,1064.5,1.2,**Z)
# F: cắt cáp cũ → dán keo trắng cáp mới
for a,b,sp in [(1108.0,1112.0,1.0),(1170.5,1175.5,1.5),(1188.0,1193.5,1.5),(1228.0,1234.0,1.6),(1414.0,1419.0,1.6),
               (1756.0,1761.0,1.5),(1768.0,1773.0,1.5),(1832.0,1837.0,1.5),(1838.0,1843.0,1.5)]: add('F',a,b,sp)
# G: ép cáp
add('G',2046.5,2050.5,1.0,zoom=1.5,c=(0.3,0.42)); add('G',2120.5,2126.5,2.0)
# T: dán băng cách nhiệt sau ép + chờ
add('T',2160.5,2166.0,1.4); add('T',2172.0,2178.0,1.6)
# H: lên màn + test → kết
add('H',2226.6,2238.5,1.0,tag='screen_on'); add('H',2247.0,2253.0,1.7)
add('H',2266.0,2274.0,3.0); add('H',2284.0,2294.0,3.1); add('H',2300.0,2304.8,1.0,tag='like')
t=0.0
for s in S:
    s['path'],s['in'],s['out']=loc(s['a'],s['b'])
    s['start']=round(t,3); s['dur']=round((s['b']-s['a'])/s['sp'],3); t+=s['dur']
TOTAL=round(t,3)
def ss(sec): return min(s['start'] for s in S if s['sec']==sec)
def se(sec): return max(s['start']+s['dur'] for s in S if s['sec']==sec)
def at(tag,src):
    s=[x for x in S if x.get('tag')==tag][0]; return round(s['start']+(src-s['a'])/s['sp'],3)
V={}
V['A']=round(ss('A')+0.9,3); V['B']=round(ss('B')+0.3,3); V['C']=round(ss('C')+2.6,3); V['D']=round(ss('D')+0.3,3)
V['E']=round(ss('E')+0.3,3); V['F']=round(ss('F')+0.3,3); V['G1']=round(ss('G')+0.4,3)
ON=at('screen_on',2231.1)
V['G2']=round(ss('H')+0.4,3)
V['H1']=round(ON+0.35,3)
like=at('like',2300.0)
V['H2']=round(V['H1']+VT['H1']['dur']+1.3,3)
P=dict(shots=S,total=TOTAL,voice=V,screen_on=ON,like=like,secs={k:(round(ss(k),3),round(se(k),3)) for k in dict.fromkeys(s['sec'] for s in S)})
json.dump(P,open('plan_base.json','w'),ensure_ascii=False,indent=1)
print('TOTAL',TOTAL); print(P['secs'])
for b,t0 in V.items(): print(b,t0,'->',round(t0+VT[b]['dur'],2))
print('ON',ON,'like',like)
