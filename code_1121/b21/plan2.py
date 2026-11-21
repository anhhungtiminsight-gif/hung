import json
P=json.load(open('plan_base.json')); VT=json.load(open('/home/claude/w/voice_timeline.json')); VW=json.load(open('/home/claude/w/vwords.json'))
V=P['voice']; ON=P['screen_on']; TOTAL=P['total']; SEC=P['secs']
def w(b,word,n=1,dt=0.0):
    k=0
    for x in VW[b]:
        if x[0]==word.lower():
            k+=1
            if k==n: return round(V[b]+x[1]+dt,3)
    raise Exception((b,word,n))
S=P['shots']; hs=[s for s in S if s['sec']=='HK']
def hk(src):
    for s in hs:
        if s['a']-0.01<=src<=s['b']+0.01: return round(s['start']+(src-s['a'])/s['sp'],3)
    raise Exception(src)
O=[]
def title(lines,y=1330,size=118): return dict(kind='title',x=500,y=y,size=size,maxw=760,lines=lines)
def job(name,start,end,els): O.append(dict(name=name,start=round(start,3),dur=round(end-start,3),els=els))
def T(name,start,end,lines,times,keys=(),pill=None,pill_at=None,sticker=None,emoji=None,y=1330):
    ln=[];k=0
    for line in lines:
        row=[]
        for x in line: row.append(dict(t=x,k=1 if x in keys else 0,at=round(times[min(k,len(times)-1)]-start,3))); k+=1
        ln.append(row)
    els=[title(ln,y=y)]
    if pill: els.append(dict(kind='pill',maxw=740,x=500,y=y-190 if len(lines)>1 else y-130,size=40,text=pill,at=round((pill_at if pill_at is not None else start)-start,3)))
    if sticker: els.append(dict(kind='sticker',maxw=600,x=sticker.get('x',640),y=sticker.get('y',y+200),size=60,text=sticker['text'],at=round(sticker['at']-start,3),rot=-6))
    if emoji: els.append(dict(kind='emoji',x=emoji.get('x',850),y=emoji.get('y',y-150),size=emoji.get('size',130),text=emoji['e'],at=round(emoji['at']-start,3),rot=8))
    job(name,start,end,els)
def ST(name,start,end,text,x=560,y=1420,size=66): job(name,start,end,[dict(kind='sticker',maxw=600,x=x,y=y,size=size,text=text,at=0.0,rot=-6)])
def PL(name,start,end,text,y=1330): job(name,start,end,[dict(kind='pill',maxw=740,x=500,y=y,size=44,text=text,at=0.0)])
# -------- HOOK (dày hiệu ứng, mỗi câu 1 emoji)
t=[hk(4.65),hk(4.85),hk(5.09),hk(5.33)]
T('hk_kiem_tra',0.25,hk(6.80),[['KIỂM','TRA'],['GIÚP','CHÚ!']],t,keys=('KIỂM','TRA'),pill='Khách mang máy tới',pill_at=0.25,emoji=dict(e='📱',at=t[1]+0.1))
t=[hk(7.15),hk(7.35),hk(7.95),hk(8.23)]
T('hk_bi_xanh',hk(6.85),hk(8.58),[['ĐANG','DÙNG'],['BỊ','XANH!']],t,keys=('BỊ','XANH!'),emoji=dict(e='😱',at=t[3]))
t=[hk(11.55),hk(11.67),hk(12.15),hk(12.31)]
T('hk_binh_thuong',hk(11.0),hk(13.1),[['GIỜ','LẠI'],['BÌNH','THƯỜNG?']],t,keys=('BÌNH','THƯỜNG?'),emoji=dict(e='🤔',at=t[2]))
t=[hk(17.29),hk(17.53),hk(17.97),hk(18.09)]
T('hk_thao_may',hk(15.55),hk(18.88),[['THÁO','MÁY'],['KIỂM','TRA!']],t,keys=('THÁO','MÁY'),emoji=dict(e='🔧',at=t[1]))
t=[hk(20.37),hk(20.93),hk(21.17)]
T('hk_thao_luon',hk(19.15),SEC['HK'][1]+0.05,[['ĐƯỢC,'],['THÁO','LUÔN!']],[hk(19.4),hk(20.93),hk(21.17)],keys=('THÁO','LUÔN!'),emoji=dict(e='👌',at=hk(21.2)))
# -------- A
PL('a_loi_nhan',V['A']+0.1,w('A','nóng')-0.15,'Lời nhắn của bạn khách')
T('a_xanh_le',w('A','nóng')-0.1,w('A','gửi')+0.3,[['NÓNG','LÊN'],['LÀ','XANH','LÈ']],
  [w('A','nóng'),w('A','lên'),w('A','là'),w('A','sành'),w('A','le')],keys=('XANH','LÈ'))
T('a_chi_phi',w('A','không')-0.1,w('A','đó')+0.4,[['KHÔNG','ĐỦ'],['CHI','PHÍ','THAY','MÀN']],
  [w('A','không'),w('A','đủ'),w('A','chi'),w('A','phí'),w('A','thay'),w('A','màn',2)],keys=('CHI','PHÍ'))
T('a_bat_thuong',w('A','chưa')-0.1,w('A','sáng')+0.6,[['CHƯA','THẤY'],['BẤT','THƯỜNG']],
  [w('A','chưa'),w('A','thấy'),w('A','bất'),w('A','thường',2)],keys=('BẤT','THƯỜNG'))
T('a_mo_may',w('A','mở')-0.1,V['A']+VT['A']['dur']+0.8,[['MỞ','MÁY'],['KIỂM','TRA','KỸ']],
  [w('A','mở'),w('A','máy',4),w('A','kiểm',3),w('A','tra',3),w('A','kỹ')],keys=('KIỂM','TRA','KỸ'))
tm=[s for s in S if s.get('tag')=='tach_man'][0]
PL('a_tach_man',tm['start']+2.9,SEC['A'][1]+0.2,'Tách màn khỏi khung ✓')
# -------- B
T('b_keo',w('B','vệ')-0.1,SEC['B'][1]-0.3,[['VỆ','SINH'],['KEO','CŨ']],[w('B','vệ'),w('B','sinh'),w('B','keo'),w('B','keo')+0.15],keys=('KEO','CŨ'))
# -------- C
T('c_seal',w('C','bóc')-0.1,w('C','kính')-0.1,[['BÓC','LỚP','SEAL']],[w('C','bóc'),w('C','vỏ'),w('C','seal')],keys=('SEAL',))
T('c_kinh',w('C','kính')-0.05,SEC['C'][1]-0.1,[['SOI','KÍNH'],['HIỂN','VI']],[w('C','kính'),w('C','kính')+0.1,w('C','hiển'),w('C','vi')],keys=('HIỂN','VI'))
# -------- D
ST('d_khong_on',w('D','không')-0.05,w('D','khu')-0.1,'Không ổn rồi!',x=560,y=1420)
T('d_chay',w('D','mạch')-0.1,SEC['D'][1]-0.1,[['MẠCH'],['CHÁY','CHẬP!']],[w('D','mạch'),w('D','cháy'),w('D','chậm')],keys=('CHÁY','CHẬP!'))
# -------- E
T('e_vet_den',w('E','vết')-0.1,w('E','chính')+1.0,[['VẾT','ĐEN'],['TRÊN','CÁP']],[w('E','vết'),w('E','đen'),w('E','trên'),w('E','cáp')],keys=('VẾT','ĐEN'))
T('e_nguyen_nhan',w('E','nguyên')-0.1,w('E','các')-0.1,[['NGUYÊN','NHÂN'],['XANH','MÀN']],[w('E','nguyên'),w('E','nhân'),w('E','xanh'),w('E','xanh')+0.15],keys=('XANH','MÀN'))
T('e_nghiem_trong',w('E','tương')-0.1,SEC['E'][1]-0.2,[['KHÁ'],['NGHIÊM','TRỌNG']],[w('E','tương'),w('E','nghiêm'),w('E','trọng')],keys=('NGHIÊM','TRỌNG'))
# -------- F
PL('f_danh_gia',V['F']+0.1,w('F','hiện')-0.1,'Đánh giá ban đầu')
T('f_2_van_de',w('F','2')-0.1,w('F','vấn',2)-0.1,[['2','VẤN','ĐỀ'],['CẦN','LƯU','Ý']],[w('F','2'),w('F','vấn',1),w('F','đề',1),w('F','cần'),w('F','lưu'),w('F','ý')],keys=('2','VẤN','ĐỀ'))
T('f_xanh_man',w('F','vấn',2)-0.05,w('F','nhưng')-0.1,[['LỖI','XANH','MÀN'],['→','THAY','CÁP']],
  [w('F','lỗi'),w('F','xanh'),w('F','màn'),w('F','thay'),w('F','thay'),w('F','cap')],keys=('THAY','CÁP'),pill='Vấn đề 1',pill_at=w('F','vấn',2))
T('f_mach_ic',w('F','khu')-0.1,w('F','nếu')+0.2,[['MẠCH','IC'],['CHÁY','CHẬP']],[w('F','khu'),w('F','ic'),w('F','cháy'),w('F','chậm')],keys=('CHÁY','CHẬP'),pill='Vấn đề 2 · nghiêm trọng hơn',pill_at=w('F','nhưng'))
PL('f_soc',w('F','nguy')-0.1,w('F','sọc')+0.5,'Nguy cơ màn tự phát sinh sọc')
T('f_xu_ly',w('F','xử')-0.1,SEC['F'][1]-1.0,[['XỬ','LÝ'],['XANH','MÀN','TRƯỚC']],[w('F','xử'),w('F','lý'),w('F','xanh',2),w('F','màn',3),w('F','màn',3)+0.15],keys=('XANH','MÀN'))
# -------- G
PL('g_ep_cap',w('G1','máy')-0.2,SEC['G'][1]-0.3,'Ép cáp mới lên màn')
T('g2_ket_qua',w('G2','kết')-0.1,ON-0.05,[['KẾT','QUẢ'],['THẾ','NÀO?']],[w('G2','kết'),w('G2','quả'),w('G2','thế'),w('G2','nào')],keys=('THẾ','NÀO?'))
# -------- H
T('h_sang_dep',ON+0.12,w('H1','cảm')-0.1,[['SÁNG','ĐẸP'],['TRỞ','LẠI!']],[ON+0.15,ON+0.35,ON+0.6,ON+0.75],keys=('SÁNG','ĐẸP'),sticker=dict(text='Quá đã!',at=ON+1.0,x=660,y=1560))
T('h_cam_ung',w('H1','cảm')-0.1,w('H1','mà')+1.6,[['CẢM','ỨNG'],['MƯỢT','MÀ']],[w('H1','cảm'),w('H1','ứng'),w('H1','mượt'),w('H1','mà')],keys=('MƯỢT','MÀ'))
T('h_comment',w('H2','comment')-0.2,w('H2','mb')-0.15,[['COMMENT'],['BÊN','DƯỚI','NHÉ!']],[w('H2','comment'),w('H2','xuống'),w('H2','phía'),w('H2','dưới')],keys=('COMMENT',))
T('h_slogan',w('H2','mb')-0.05,TOTAL-0.05,[['TẬN','TÂM'],['BỀN','&','ĐẸP']],[w('H2','tận'),w('H2','tâm'),w('H2','bền'),w('H2','và'),w('H2','đẹp')],keys=('TẬN','TÂM','BỀN','ĐẸP'),pill='MBS Việt Trì',pill_at=w('H2','mb'))
O.sort(key=lambda o:o['start'])
for i in range(len(O)-1):
    if O[i]['start']+O[i]['dur']>O[i+1]['start']-0.03: O[i]['dur']=round(O[i+1]['start']-0.03-O[i]['start'],3)
for o in O:
    if o['name']!='h_slogan': o['dur']=min(o['dur'],4.5)
    assert o['dur']>0.4,o['name']
    for el in o['els']:
        if 'at' in el: el['at']=max(0,min(el['at'],o['dur']-0.3))
        for ln in el.get('lines',[]):
            for x in ln: x['at']=max(0,min(x['at'],o['dur']-0.3))
json.dump(O,open('overlays.json','w'),ensure_ascii=False,indent=1)
for o in O: print(f"{o['start']:7.2f} {o['dur']:5.2f} {o['name']}")
