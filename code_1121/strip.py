import sys, json, numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0,'.')
from sheet import frame, cam, act
def strips(cands,out,n=7,scale=0.55):
    W=int(160*scale); H=int(284*scale); LW=70
    img=Image.new('RGB',(LW+n*W,len(cands)*(H+2)),'black'); d=ImageDraw.Draw(img); f=ImageFont.load_default()
    for r,(lab,a,b) in enumerate(cands):
        y=r*(H+2)
        i0=int(a*6); i1=int(b*6)
        c=np.percentile(cam[i0:i1],80); ac=act[i0:i1].mean()
        d.text((2,y+2),f'{lab}',fill='white',font=f); d.text((2,y+16),f'{a:.1f}-{b:.1f}',fill='white',font=f)
        d.text((2,y+30),f'c{c:.2f}',fill='yellow' if c<0.35 else 'red',font=f); d.text((2,y+44),f'a{ac:.2f}',fill='cyan',font=f)
        for k,t in enumerate(np.linspace(a,b-0.1,n)):
            img.paste(Image.fromarray(frame(t)).resize((W,H)),(LW+k*W,y))
    img.save(out,quality=80)
if __name__=='__main__':
    cands=json.loads(open(sys.argv[1]).read()); strips(cands,sys.argv[2])
