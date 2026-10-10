import math, numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
W,H,FPS,DUR=1920,1080,30,14
F='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
fbig=ImageFont.truetype(F,58); fsm=ImageFont.truetype(F,30); flab=ImageFont.truetype(F,28)
rng=np.random.default_rng(3)
# fond étoilé
sky=np.zeros((H,W,3),np.float32)
for _ in range(1400):
    x,y=rng.integers(0,W),rng.integers(0,H); b=rng.uniform(.2,1)**2; sky[y,x]=b
sky=np.asarray(Image.fromarray((sky*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))).astype(np.float32)/255*1.6
em=Image.open('package/example/img/earth-blue-marble.jpg').convert('RGB')
def disc(img,r):
    s=img.resize((r*2,r*2)); m=Image.new('L',(r*2,r*2),0); ImageDraw.Draw(m).ellipse([0,0,r*2-1,r*2-1],fill=255)
    # ombrage
    yy,xx=np.mgrid[0:r*2,0:r*2]; sh=np.clip(1.15-((xx-r*0.6)**2+(yy-r*0.7)**2)**0.5/(r*1.6),0.15,1)[...,None]
    a=(np.asarray(s).astype(np.float32)*sh).clip(0,255).astype(np.uint8); return Image.fromarray(a),m
ew,eh=em.size
earth_img,earth_m=disc(em.crop((int(ew*0.15),int(eh*0.15),int(ew*0.15)+eh//1,int(eh*0.85))),150)
mn=np.full((400,400,3),150,np.float32)+rng.normal(0,18,(400,400,1))
for _ in range(90):
    cx,cy,rr=rng.integers(0,400),rng.integers(0,400),rng.integers(4,30)
    yy,xx=np.mgrid[0:400,0:400]; mn[((xx-cx)**2+(yy-cy)**2)<rr*rr]-=rng.uniform(15,40)
moon_img,moon_m=disc(Image.fromarray(np.clip(mn,0,255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2)),70)
E=(380,560); M=(1560,500)
# trajectoire de retour libre : aller (haut), contour de la Lune, retour (bas)
pts=[]
for k in range(200):
    u=k/199; x=E[0]+190+(M[0]-43-E[0]-190)*u; y=E[1]-170*math.sin(math.pi*u)+(M[1]-117-E[1])*u; pts.append((x,y))
for k in range(1,80):
    a=math.pi*0.55-k/79*math.pi*1.1*-1; a=math.radians(110+k/79*(-220)); pts.append((M[0]+125*math.cos(a), M[1]-125*math.sin(a)))
last=pts[-1]
for k in range(1,200):
    u=k/199; x=last[0]+(E[0]+150-last[0])*u; y=last[1]+(E[1]+120-last[1])*u+150*math.sin(math.pi*u); pts.append((x,y))
L=[0]+list(np.cumsum([math.dist(pts[i],pts[i+1]) for i in range(len(pts)-1)])); T=L[-1]
def at(f):
    d=f*T; i=max(0,min(len(pts)-2,int(np.searchsorted(L,d))-1)); s=(d-L[i])/max(1e-6,L[i+1]-L[i]); return (pts[i][0]+(pts[i+1][0]-pts[i][0])*s,pts[i][1]+(pts[i+1][1]-pts[i][1])*s)
def ease(t): t=max(0,min(1,t)); return t*t*(3-2*t)
yy,xx=np.mgrid[0:H,0:W]; vig=np.clip(1-0.55*(((xx-W/2)/(W/2))**2+((yy-H/2)/(H/2))**2),0.35,1)[...,None]
ev=[(0.30,"EXPLOSION","55 h 54 min",(255,80,60)),(0.50,"AROUND THE MOON","no power to land",(255,210,90)),(0.985,"SPLASHDOWN","142 h 54 min",(120,230,140))]
for i in range(FPS*DUR):
    t=i/FPS; p=ease((t-0.8)/11.0)
    base=Image.fromarray((np.clip(sky,0,1)*255).astype(np.uint8))
    base.paste(earth_img,(E[0]-150,E[1]-150),earth_m); base.paste(moon_img,(M[0]-70,M[1]-70),moon_m)
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    n=int(np.searchsorted(L,p*T))
    if n>1:
        seg=pts[:n]+[at(p)]
        for j in range(0,len(seg)-1,3): d.line([seg[j],seg[min(j+2,len(seg)-1)]],fill=(140,200,255,230),width=5)
    q=at(p); R=10+3*math.sin(t*8); d.ellipse([q[0]-R,q[1]-R,q[0]+R,q[1]+R],fill=(255,255,255,255))
    for (f,a,b,col) in ev:
        if p>=f-0.002:
            A=int(255*ease((p-f+0.002)/0.04)); x,y=at(f); r=16
            d.ellipse([x-r,y-r,x+r,y+r],outline=col+(A,),width=5)
            bx,by={0.30:(x-140,y+30),0.50:(x-250,y-150)}.get(f,(x+30,y+20))
            bb=d.textbbox((bx,by),a,font=flab); bb2=d.textbbox((bx,by+38),b,font=fsm)
            d.rounded_rectangle([bb[0]-14,bb[1]-10,max(bb[2],bb2[2])+14,bb2[3]+10],radius=10,fill=(10,12,20,int(220*A/255)),outline=col+(A,),width=3)
            d.text((bx,by),a,font=flab,fill=col+(A,)); d.text((bx,by+38),b,font=fsm,fill=(235,235,240,A))
    al=int(255*ease((t-0.3)/0.6))
    d.text((W/2,90),"APOLLO 13 · APRIL 1970",font=fbig,fill=(255,255,255,al),anchor='mm',stroke_width=3,stroke_fill=(0,0,0,al))
    d.text((W/2,150),"THE FREE-RETURN PATH HOME",font=fsm,fill=(170,210,255,al),anchor='mm',stroke_width=2,stroke_fill=(0,0,0,al))
    hrs=int(142.9*p); d.text((W-60,H-60),f"T + {hrs:03d} h",font=fbig,fill=(255,255,255,al),anchor='rs',stroke_width=2,stroke_fill=(0,0,0,al))
    g=np.asarray(ov.filter(ImageFilter.GaussianBlur(12))).astype(np.float32)/255; o=np.asarray(ov).astype(np.float32)/255
    a=np.asarray(base).astype(np.float32)/255; a=a+g[...,:3]*g[...,3:]*1.4; a=a*(1-o[...,3:])+o[...,:3]*o[...,3:]
    a=a*vig+rng.normal(0,0.012,(H,W,1)); a=np.clip(a,0,1)*min(1,ease(t/0.5),ease((DUR-t)/0.4))
    Image.fromarray((a*255).astype(np.uint8)).save(f'ap/{i:04d}.jpg',quality=92)
