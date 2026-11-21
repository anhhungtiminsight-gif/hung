import cv2, numpy as np, json, sys
from PIL import Image, ImageDraw, ImageFont
cap=cv2.VideoCapture('p6.mp4')
M=json.load(open('motion.json')); cam=np.array(M['cam']); act=np.array(M['act'])
clips=json.load(open('clips.json'))
def clip_at(t):
    for c in clips:
        if c['s']<=t<c['s']+c['d']: return c['name'][-4:]
    return ''
def frame(t):
    cap.set(cv2.CAP_PROP_POS_FRAMES,int(t*6)); ok,f=cap.read()
    return cv2.cvtColor(f,cv2.COLOR_BGR2RGB) if ok else np.zeros((284,160,3),np.uint8)
def sheet(a,b,step,out,cols=10,scale=1.0):
    ts=list(np.arange(a,b,step)); rows=(len(ts)+cols-1)//cols
    W=int(160*scale); H=int(284*scale)
    img=Image.new('RGB',(cols*W,rows*(H+14)),'black'); d=ImageDraw.Draw(img)
    f=ImageFont.load_default()
    for k,t in enumerate(ts):
        im=Image.fromarray(frame(t)).resize((W,H)); x=(k%cols)*W; y=(k//cols)*(H+14)
        img.paste(im,(x,y+14))
        i=int(t*6); c=cam[i:i+6].mean() if i<len(cam) else 0
        d.text((x+2,y+1),f'{t:.1f} {clip_at(t)} c{c:.1f}',fill='yellow' if c<0.35 else 'red',font=f)
    img.save(out,quality=80)
if __name__=='__main__':
    a,b,s,o=float(sys.argv[1]),float(sys.argv[2]),float(sys.argv[3]),sys.argv[4]
    sheet(a,b,s,o,int(sys.argv[5]) if len(sys.argv)>5 else 10, float(sys.argv[6]) if len(sys.argv)>6 else 1.0)
