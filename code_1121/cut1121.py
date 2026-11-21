import json, numpy as np, subprocess, soundfile as sf
W=json.load(open('words.json')); OFF=121.2667
x,sr=sf.read('v_48.wav'); x=x.astype(np.float32)
hop=sr//100
fr_db=np.array([20*np.log10(np.sqrt(np.mean(x[i*hop:(i+1)*hop]**2))+1e-9) for i in range(len(x)//hop)])
np.save('v_db.npy',fr_db)
ref=np.percentile(fr_db,95); TH=ref-34
print('p95',round(ref,1),'TH',round(TH,1))
def w(l,i): return W[l]['words'][i]
def T(t): return int(round((t-OFF)*100))
def start_at(t):
    i=T(t)+3; lo=T(t)-30
    while i>lo and not all(fr_db[i-j]<TH for j in range(1,5)): i-=1
    return max(0,(i-3))/100
def end_at(t):
    i=T(t)-3; hi=T(t)+45
    while i<hi and not all(fr_db[i+j]<TH for j in range(4)): i+=1
    return (i+6)/100
def gap_cut(a,b):
    lo=T(a)-6; hi=T(b)+6; best=None; i=lo
    while i<hi:
        if fr_db[i]<TH:
            j=i
            while j<hi and fr_db[j]<TH: j+=1
            if best is None or j-i>best[1]-best[0]: best=(i,j)
            i=j
        else: i+=1
    return best
SP={
'A':[((11,4),(11,5),.25),((12,0),(17,8),.12),((18,0),(19,5),.30),((22,0),(24,4),.12),((26,0),(29,10),0)],
'B':[((30,3),(31,10),0)],
'C':[((35,0),(36,11),0)],
'D':[((41,0),(42,11),0)],
'E':[((44,0),(45,8),.28),((47,0),(49,10),0)],
'F':[((54,0),(54,10),.12),((56,0),(59,7),.10),((60,0),(63,11),.30),((66,0),(69,0),0)],
'G':[((70,0),(71,11),.22),((72,1),(72,9),0)],
'H':[((73,0),(80,2),0)],
}
plan={}
for b,spans in SP.items():
    out=[]
    for (l0,i0),(l1,i1),gap in spans:
        # start
        if i0>0:
            g=gap_cut(w(l0,i0-1)['e'],w(l0,i0)['s'])
            s=(g[1]-4)/100 if g else start_at(w(l0,i0)['s'])
        else: s=start_at(w(l0,i0)['s'])
        last=len(W[l1]['words'])-1
        if i1<last:
            g=gap_cut(w(l1,i1)['e'],w(l1,i1+1)['s'])
            e=(g[0]+5)/100 if g else end_at(w(l1,i1)['e'])
            if not g: print('WARN tail',b,l1,i1)
        else: e=end_at(w(l1,i1)['e'])
        if i0>0 and not gap_cut(w(l0,i0-1)['e'],w(l0,i0)['s']): print('WARN head',b,l0,i0)
        txt=' '.join(x['w'] for l in range(l0,l1+1) for k,x in enumerate(W[l]['words']) if (l>l0 or k>=i0) and (l<l1 or k<=i1))
        out.append(dict(s=round(s,2),e=round(e,2),gap=gap,text=txt))
    plan[b]=out
json.dump(plan,open('voice_plan.json','w'),ensure_ascii=False,indent=1)
for b,o in plan.items():
    for c in o: print(b,c['s'],c['e'],c['gap'],c['text'])
