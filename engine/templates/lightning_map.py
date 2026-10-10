import math, numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
W,H,FPS,DUR=1920,1080,30,11
e=Image.open('package/example/img/earth-night.jpg').convert('RGB')
EW,EH=e.size
earth=Image.new('RGB',(EW*2,EH)); earth.paste(e,(0,0)); earth.paste(e,(EW,0))
cl0=Image.open('package/example/clouds/clouds.png').convert('RGBA')
clouds=Image.new('RGBA',(EW*2,EH)); clouds.paste(cl0,(0,0)); clouds.paste(cl0,(EW,0))
def L(lon): return lon+360
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
    cx=340-50*k; cy=2+8*k; wd=300-160*k; hd=wd*H/W
    x0=(cx-wd/2+180)/360*EW; x1=(cx+wd/2+180)/360*EW; y0=(90-(cy+hd/2))/180*EH; y1=(90-(cy-hd/2))/180*EH
    bg=earth.transform((W,H),Image.EXTENT,(x0,y0,x1,y1),Image.BICUBIC)
    cl=clouds.transform((W,H),Image.EXTENT,(x0-30*t,y0,x1-30*t,y1),Image.BICUBIC)
    a=np.asarray(bg).astype(np.float32)/255
    a=np.clip(a**0.8*1.2,0,1)*np.array([0.85,0.95,1.15])
    c=np.asarray(cl).astype(np.float32)/255; a=a*(1-c[...,3:]*0.15)+c[...,:3]*c[...,3:]*0.08
    def S(lat,lon): X,Y=px(lat,lon); return ((X-x0)/(x1-x0)*W,(Y-y0)/(y1-y0)*H)
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    rr=np.random.default_rng(int(t*30))
    nfl=int(min(t,3)/3*44)
    for _ in range(nfl):
        la=rr.normal(0,22); lo=rr.uniform(-180,180)
        if rr.random()<0.25: la,lo=rr.normal(5,8),rr.normal(-60,25)
        if rr.random()<0.15: la,lo=rr.normal(0,8),rr.normal(20,15)
        q=S(la,lo); r=rr.uniform(3,9)
        d.ellipse([q[0]-r,q[1]-r,q[0]+r,q[1]+r],fill=(200,220,255,255))
    al=int(255*min(ease((t-1.0)/0.7),1))
    d.text((W/2,110),"LIGHTNING HITS EARTH",font=fbig,fill=(255,255,255,al),anchor='mm',stroke_width=3,stroke_fill=(0,20,60,al))
    d.text((W/2,180),"ABOUT 44 TIMES EVERY SECOND",font=fsm,fill=(170,210,255,al),anchor='mm',stroke_width=2,stroke_fill=(0,0,0,al))
    if t>6.5:
        A=int(255*ease((t-6.5)/0.5)); q=S(9.8,-71.6); R=22+6*math.sin(t*7)
        d.ellipse([q[0]-R,q[1]-R,q[0]+R,q[1]+R],outline=(255,230,80,A),width=5)
        txt="LAKE MARACAIBO · LIGHTNING CAPITAL"; bx,by=q[0]+40,q[1]-20
        bb=d.textbbox((bx,by),txt,font=flab)
        d.rounded_rectangle([bb[0]-14,bb[1]-10,bb[2]+14,bb[3]+10],radius=10,fill=(15,15,20,int(220*A/255)),outline=(255,230,80,A),width=3)
        d.text((bx,by),txt,font=flab,fill=(255,255,255,A))
    g=np.asarray(ov.filter(ImageFilter.GaussianBlur(16))).astype(np.float32)/255
    o=np.asarray(ov).astype(np.float32)/255
    a=a+g[...,:3]*g[...,3:]*2.2; a=a*(1-o[...,3:])+o[...,:3]*o[...,3:]
    a=a*vig+rng.normal(0,0.016,(H,W,1)); a=np.clip(a,0,1)*min(1,ease(t/0.5),ease((DUR-t)/0.4))
    Image.fromarray((a*255).astype(np.uint8)).save(f's/{i:04d}.jpg',quality=92)
