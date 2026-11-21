import json
P=json.load(open('plan_base.json')); SEC=P['secs']; ON=P['screen_on']; TOT=P['total']; V=P['voice']
MP='C:/Users/hung/AppData/Local/CapCut/User Data/Cache/music/'
M=dict(clock='123fbdef84931e6a7b4d843ec502e0fe',drone='c13b20cfc3bd6986da7ee08b98d7730d',rain='b40834c2d4c3a6211297c175eae07ccd',
       b51='51b92a8bd98a9687e503ae19ddc07714',b7b='7b43d50bbc54560f0fa634e8272e8aa5',piano='ba62b1f3352aed58ff7792c35dfaa88d',
       c768='c768cf09c2ddcfb2e23484922dd44e9e',acou='24cc86e3df7fb4d089a1b1facab2b133')
mus=[]
def mu(k,start,end,src,vol,fi=0.4,fo=0.6): mus.append(dict(path=MP+M[k]+'.mp3',start=round(start,3),dur=round(end-start,3),src=src,vol=vol,fi=fi,fo=fo))
A0,A1=SEC['A']; vA_end=V['A']+31.5
mu('clock',0,A0+0.6,40,0.10,0,0.8); mu('drone',0,A0+0.4,0,0.20,0,0.8)
mu('rain',A0-0.2,vA_end+0.5,2,0.24,0.6,1.0)
mu('b51',vA_end+0.2,A1+0.5,10,0.45,0.8,0.6)
B0=SEC['B'][0]; mu('b7b',B0,V['B']+4.3,6,0.26,0.5,0.3); mu('b7b',V['B']+4.3,V['C']-0.1,6+V['B']+4.3-B0,0.55,0.3,0.4)
mu('b7b',V['C']-0.1,V['C']+4.2,6+V['C']-0.1-B0,0.26,0.3,0.3); mu('b7b',V['C']+4.2,SEC['C'][1]+0.1,6+V['C']+4.2-B0,0.5,0.3,0.6)
D0=SEC['D'][0]; mu('drone',D0-0.1,D0+4.8,0,0.30,0.1,1.0)
vE_end=V['E']+10.61; mu('rain',D0,vE_end+0.3,30,0.22,0.8,0.3); mu('rain',vE_end+0.3,SEC['E'][1]+0.2,30+vE_end+0.3-D0,0.5,0.3,0.6)
F0=SEC['F'][0]; vF_end=V['F']+23.19; mu('piano',F0,vF_end+0.3,0,0.14,0.6,0.3); mu('piano',vF_end+0.3,SEC['F'][1]+0.1,vF_end+0.3-F0,0.45,0.3,0.6)
G0=SEC['G'][0]; vG_end=V['G1']+5.75; mu('c768',G0,SEC['G'][1]+0.2,15,0.18,0.5,0.8)
T0=SEC['T'][0]; mu('clock',T0,V['G2']+2.6,3,0.35,0.6,0.2); mu('clock',V['G2']+2.6,ON+0.15,3+V['G2']+2.6-T0,0.9,0.2,0.3)
mu('acou',ON,V['H2']-0.2,12,0.30,0.1,0.3)
hE=V['H2']+10.5; mu('acou',V['H2']-0.2,hE,12+V['H2']-0.2-ON,0.14,0.4,0.2); mu('acou',hE,TOT,12+hE-ON,0.4,0.2,1.5)
sfx=[]
def sx(n,t,vol): sfx.append(dict(name=n,start=round(t,3),vol=vol))
POP='pop! (tapping the mouth with a hand)(912'; OH='"Oh?" "What !?" Piano sound effects(8857'
O={o['name']:o for o in json.load(open('overlays.json'))}
def o(n): return O[n]['start']
sx(POP,0.3,0.38); sx('MusicXylophone SME02_72.7',o('hk_bi_xanh')+0.9,0.36); sx(OH,o('hk_binh_thuong')+0.4,0.3)
sx(POP,o('hk_thao_may')+0.3,0.36); sx('叮 答题对了',o('hk_thao_luon')+1.0,0.3); sx('Woosh',A0-0.35,0.5)
sx('Mouse click sound',o('a_xanh_le')+0.1,0.24); sx('Mouse click sound',o('a_chi_phi')+0.1,0.2)
sx('Shine_04',o('a_tach_man'),0.24); sx('Mouse click sound',o('b_keo')+0.1,0.2); sx('叮 答题对了',o('c_kinh')+0.1,0.22)
sx(OH,V['D']-0.1,0.2); sx('Mouse click sound',o('e_vet_den')+0.1,0.22)
sx('Paper page turn sound 1 scene change swi',F0-0.1,0.2); sx('叮 答题对了',o('f_xanh_man')+0.1,0.2); sx('Mouse click sound',o('f_mach_ic')+0.1,0.22)
sx('Woosh',G0-0.2,0.3); sx('Glitter Lean Slow Rise (Telephone Style)',ON-2.3,0.16); sx('Bell ding',ON,0.28); sx('Ah~ (image of recovery)(1119332)',ON+0.9,0.24)
sx('叮 答题对了',o('h_cam_ung')+0.1,0.24); sx('Mouse click sound',o('h_comment')+0.1,0.24); sx(POP,o('h_slogan')+0.1,0.24); sx('MusicXylophone SME02_72.7',TOT-1.3,0.3)
SH=P['shots']; idx=lambda sec:[i for i,s in enumerate(SH) if s['sec']==sec]
trans={str(idx('HK')[-1]):'Nháy trắng',str(idx('C')[-1]):'Kết hợp',str(idx('F')[-1]):'Kết hợp',str(idx('T')[-1]):'Kết hợp'}
stickers=[dict(name='Monkey Emoji - Shocked Meme',start=V['D']-0.05,dur=1.6,scale=0.85,x=0.42,y=-0.05)]
effects=[dict(name='Pháo giấy sặc sỡ',start=ON,dur=3.2),dict(name='Lớp phủ lấp lánh',start=o('h_slogan'),dur=2.4)]
json.dump(dict(music=mus,sfx=sfx,trans=trans,stickers=stickers,effects=effects),open('plan3.json','w'),ensure_ascii=False,indent=1)
print(len(mus),len(sfx),trans)
