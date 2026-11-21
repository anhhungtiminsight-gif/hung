import json, cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont
P=json.load(open('plan_base.json')); O=json.load(open('overlays.json')); VW=json.load(open('/home/claude/w/vwords.json'))
cap=cv2.VideoCapture('/home/claude/w/ana/full.mp4')
import glob
fp=glob.glob('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
F=ImageFont.truetype(fp[0],14) if fp else ImageFont.load_default()
def frame(t,z=1.0,c=(0.5,0.5)):
    cap.set(cv2.CAP_PROP_POS_MSEC,t*1000); ok,f=cap.read()
    im=Image.fromarray(cv2.cvtColor(f,cv2.COLOR_BGR2RGB)).resize((270,480))
    if z>1:
        w,h=im.size; cw,ch=w/z,h/z; x0=min(max(c[0]*w-cw/2,0),w-cw); y0=min(max(c[1]*h-ch/2,0),h-ch)
        im=im.crop((x0,y0,x0+cw,y0+ch)).resize((w,h))
    return im.convert('RGBA')
words=[]
for b,t0 in P['voice'].items():
    for x in VW[b]: words.append((t0+x[1],x[0]))
tiles=[]
for i,s in enumerate(P['shots']):
    mid=s['start']+s['dur']*0.5
    im=frame((s['a']+s['b'])/2,s.get('zoom',1.0),s.get('c',(0.5,0.5)))
    for k,o in enumerate(O):
        if o['start']<=mid<=o['start']+o['dur']:
            ov=Image.open(f'motion_v1/{k+1:02d}-{o["name"]}.png').convert('RGBA').resize((270,480)); im.alpha_composite(ov)
    t=Image.new('RGB',(270,560),'black'); t.paste(im.convert('RGB'),(0,0)); d=ImageDraw.Draw(t)
    d.text((4,484),f"#{i+1} {s['sec']}  {s['start']:.1f}-{s['start']+s['dur']:.1f}s  x{s['sp']}",fill='yellow',font=F)
    vt=' '.join(wd for tt,wd in words if s['start']<=tt<s['start']+s['dur'])
    import textwrap
    for j,l in enumerate(textwrap.wrap(vt,36)[:4]): d.text((4,502+j*14),l,fill='white',font=F)
    tiles.append(t)
cols=8
for p in range(0,len(tiles),24):
    ch=tiles[p:p+24]; rows=(len(ch)+cols-1)//cols
    sheet=Image.new('RGB',(cols*272,rows*562),'gray')
    for k,t in enumerate(ch): sheet.paste(t,((k%cols)*272,(k//cols)*562))
    sheet.save(f'/mnt/user-data/outputs/1121_storyboard_{p//24+1}.jpg',quality=82)
print(len(tiles))
