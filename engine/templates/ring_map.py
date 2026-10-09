import math, numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
W,H,FPS,DUR=1920,1080,30,11
e=Image.open('package/example/img/earth-blue-marble.jpg').convert('RGB')
EW,EH=e.size
earth=Image.new('RGB',(EW*2,EH)); earth.paste(e,(0,0)); earth.paste(e,(EW,0))
cl0=Image.open('package/example/clouds/clouds.png').convert('RGBA')
clouds=Image.new('RGBA',(EW*2,EH)); clouds.paste(cl0,(0,0)); clouds.paste(cl0,(EW,0))
def L(lon): return lon if lon>=0 else lon+360   # longitudes 0..360 (Pacific centred)
def px(lat,lon): return ((L(lon)+180)/360*EW, (90-lat)/180*EH)
F='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
fbig=ImageFont.truetype(F,64); fsm=ImageFont.truetype(F,30); flab=ImageFont.truetype(F,28)
ring=[(-46,168),(-39.3,175.6),(-20.5,-175.4),(-15,168),(-6,147),(-6.1,105.4),(1,125),(15.1,120.4),(24,122),(32.76,130.3),(35.4,138.7),(43,145),(52,158),(56,160.6),(53,-168),(55,-160),(60,-152),(58,-135),(46.2,-122.2),(40,-122),(19,-98.6),(14,-91),(12,-86),(4.9,-75.3),(-1.5,-78.4),(-16,-71.5),(-23,-67.7),(-39.4,-71.9),(-50,-73)]
named=[("UNZEN · 1991",32.76,130.3,(-260,-40)),("PINATUBO · 1991",15.1,120.4,(40,0)),("MT ST HELENS · 1980",46.2,-122.2,(30,-50))]
def ease(t): t=max(0,min(1,t)); return t*t*(3-2*t)
rng=np.random.default_rng(2)
yy,xx=np.mgrid[0:H,0:W]; vig=np.clip(1-0.6*(((xx-W/2)/(W/2))**2+((yy-H/2)/(H/2))**2)**1.2/2,0.3,1)[...,None]
for i in range(FPS*DUR):
    t=i/FPS; k=ease(t/DUR)
    cx=198-2*k; cy=5+1*k; wd=218-16*k; hd=wd*H/W
    x0=(cx-wd/2+180)/360*EW; x1=(cx+wd/2+180)/360*EW; y0=(90-(cy+hd/2))/180*EH; y1=(90-(cy-hd/2))/180*EH
    bg=earth.transform((W,H),Image.EXTENT,(x0,y0,x1,y1),Image.BICUBIC)
    cl=clouds.transform((W,H),Image.EXTENT,(x0-30*t,y0,x1-30*t,y1),Image.BICUBIC)
    a=np.asarray(bg).astype(np.float32)/255
    a=np.clip(a**0.7*0.95,0,1)*np.array([0.8,0.95,1.1])+np.array([0,0.02,0.05])
    c=np.asarray(cl).astype(np.float32)/255; a=a*(1-c[...,3:]*0.35)+c[...,:3]*c[...,3:]*0.35
    def S(lat,lon): X,Y=px(lat,lon); return ((X-x0)/(x1-x0)*W,(Y-y0)/(y1-y0)*H)
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    pts=[S(*p) for p in ring]
    p=ease((t-0.8)/5.5); n=(len(pts)-1)*p; m=int(n)
    seg=pts[:m+1]
    if m<len(pts)-1: f=n-m; seg=seg+[(pts[m][0]+(pts[m+1][0]-pts[m][0])*f,pts[m][1]+(pts[m+1][1]-pts[m][1])*f)]
    if len(seg)>1: d.line(seg,fill=(255,90,30,255),width=7,joint='curve')
    for j,q in enumerate(pts):
        if j<=n:
            ph=(t*1.1+j*0.37)%1; R=8+26*ph
            d.ellipse([q[0]-8,q[1]-8,q[0]+8,q[1]+8],fill=(255,60,30,255))
            d.ellipse([q[0]-R,q[1]-R,q[0]+R,q[1]+R],outline=(255,120,40,int(180*(1-ph))),width=3)
    if t>1.0:
        al=int(255*min(ease((t-1.0)/0.7),1))
        d.text((W/2,120),"THE RING OF FIRE",font=fbig,fill=(255,255,255,al),anchor='mm',stroke_width=3,stroke_fill=(60,10,0,al))
        d.text((W/2,190),"75% OF EARTH'S ACTIVE VOLCANOES",font=fsm,fill=(255,200,150,al),anchor='mm',stroke_width=2,stroke_fill=(0,0,0,al))
    for j,(nm,la,lo,(dx,dy)) in enumerate(named):
        al=ease((t-7.0-j*0.6)/0.5)
        if al>0:
            q=S(la,lo); A=int(255*al); R=18+6*math.sin(t*6)
            d.ellipse([q[0]-R,q[1]-R,q[0]+R,q[1]+R],outline=(255,230,80,A),width=5)
            bx,by=q[0]+dx,q[1]+dy
            bb=d.textbbox((bx,by),nm,font=flab)
            d.rounded_rectangle([bb[0]-14,bb[1]-10,bb[2]+14,bb[3]+10],radius=10,fill=(15,15,20,int(220*al)),outline=(255,230,80,A),width=3)
            d.text((bx,by),nm,font=flab,fill=(255,255,255,A))
    g=np.asarray(ov.filter(ImageFilter.GaussianBlur(16))).astype(np.float32)/255
    o=np.asarray(ov).astype(np.float32)/255
    a=a+g[...,:3]*g[...,3:]*1.5; a=a*(1-o[...,3:])+o[...,:3]*o[...,3:]
    a=a*vig+rng.normal(0,0.016,(H,W,1)); a=np.clip(a,0,1)*min(1,ease(t/0.5),ease((DUR-t)/0.4))
    Image.fromarray((a*255).astype(np.uint8)).save(f'r/{i:04d}.jpg',quality=92)
