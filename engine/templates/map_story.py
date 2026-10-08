import math, numpy as np, subprocess
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops
W,H,FPS,DUR=1920,1080,30,10
earth=Image.open('package/example/img/earth-blue-marble.jpg').convert('RGB')
clouds=Image.open('package/example/clouds/clouds.png').convert('RGBA')
EW,EH=earth.size
def ll2px(lat,lon): return ((lon+180)/360*EW,(90-lat)/180*EH)
F='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
fbig=ImageFont.truetype(F,46); fsm=ImageFont.truetype(F,30); fbub=ImageFont.truetype(F,34)
MIA=(25.76,-80.19); BER=(32.30,-64.78); SJU=(18.47,-66.10); FLL=(26.12,-80.14)
path=[FLL,(26.0,-78.6),(26.2,-77.4),(27.3,-77.0),(28.4,-77.6),(29.3,-76.2),(29.9,-74.6),(30.6,-73.4)]
def ease(t): t=max(0,min(1,t)); return t*t*(3-2*t)
def cam(t):
    k=ease(t/DUR)
    cx=-74+(-73.5+74)*k; cy=26.5+0.5*k; wdeg=34-8*k
    return cx,cy,wdeg
grain=np.random.default_rng(1)
yy,xx=np.mgrid[0:H,0:W]; vig=1-0.55*(((xx-W/2)/(W/2))**2+((yy-H/2)/(H/2))**2)**1.2/2
vig=np.clip(vig,0.35,1)[...,None]
def plane(d,x,y,ang,s=26,col=(240,240,245)):
    pts=[(0,-1.2),(0.12,-0.9),(0.12,-0.3),(1.0,0.2),(1.0,0.35),(0.12,0.15),(0.1,0.8),(0.4,1.05),(0.4,1.15),(0,1.05),(-0.4,1.15),(-0.4,1.05),(-0.1,0.8),(-0.12,0.15),(-1.0,0.35),(-1.0,0.2),(-0.12,-0.3),(-0.12,-0.9)]
    c,sn=math.cos(ang),math.sin(ang)
    d.polygon([(x+s*(px*c-py*sn),y+s*(px*sn+py*c)) for px,py in pts],fill=col)
TXT='"WE CANNOT FIND WEST.\nEVERYTHING IS WRONG."'
for i in range(FPS*DUR):
    t=i/FPS; cx,cy,wd=cam(t); hd=wd*H/W
    x0,y0=ll2px(cy+hd/2,cx-wd/2); x1,y1=ll2px(cy-hd/2,cx+wd/2)
    box=(x0,y0,x1,y1)
    bg=earth.transform((W,H),Image.EXTENT,box,Image.BICUBIC)
    cl=clouds.transform((W,H),Image.EXTENT,(x0-20*t,y0,x1-20*t,y1),Image.BICUBIC)
    a=np.asarray(bg).astype(np.float32)/255
    # grade: teal shadows, contrast, darken
    a=np.clip(a**0.62*1.05,0,1); a=a*np.array([0.82,0.98,1.12])+np.array([0.0,0.03,0.07])
    cla=np.asarray(cl).astype(np.float32)/255; a=a*(1-cla[...,3:]*0.45)+cla[...,:3]*cla[...,3:]*0.45
    def S(lat,lon): return ((lon-(cx-wd/2))/wd*W,((cy+hd/2)-lat)/hd*H)
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    tri=[S(*MIA),S(*BER),S(*SJU)]
    # lines draw 1.2-3.2s
    for j in range(3):
        p=ease((t-1.2-j*0.6)/0.7)
        if p>0:
            A,B=tri[j],tri[(j+1)%3]
            d.line([A,(A[0]+(B[0]-A[0])*p,A[1]+(B[1]-A[1])*p)],fill=(90,220,255,255),width=6)
    if t>3.2:
        al=int(255*ease((t-3.2)/0.6)); gx=sum(p[0] for p in tri)/3; gy=sum(p[1] for p in tri)/3
        d.text((gx,gy),"BERMUDA\nTRIANGLE",font=fbig,fill=(255,255,255,al),anchor='mm',align='center',stroke_width=2,stroke_fill=(0,40,70,al))
    for j,(px,py) in enumerate(tri):
        p=ease((t-0.4-j*0.25)/0.35)
        if p>0:
            r=14*p; d.ellipse([px-r,py-r,px+r,py+r],fill=(255,50,50,255))
            ph=((t*1.2+j*0.3)%1); R=14+40*ph
            d.ellipse([px-R,py-R,px+R,py+R],outline=(255,70,70,int(200*(1-ph))),width=4)
    # flight 19 path 4.2-9.5s
    pts=[S(*q) for q in path]
    p=ease((t-4.2)/5.0)
    if p>0:
        seg=[]; L=[math.dist(pts[k],pts[k+1]) for k in range(len(pts)-1)]; tot=sum(L)*p; acc=0
        cur=pts[0]; ang=0
        for k in range(len(L)):
            if acc+L[k]>=tot:
                f=(tot-acc)/L[k]; cur=(pts[k][0]+(pts[k+1][0]-pts[k][0])*f,pts[k][1]+(pts[k+1][1]-pts[k][1])*f)
                ang=math.atan2(pts[k+1][1]-pts[k][1],pts[k+1][0]-pts[k][0])+math.pi/2; break
            acc+=L[k]
        # dotted trail
        n=int(tot/22)
        for m in range(n):
            dd=m*22; a2=0
            for k in range(len(L)):
                if a2+L[k]>=dd:
                    f=(dd-a2)/L[k]; qx=pts[k][0]+(pts[k+1][0]-pts[k][0])*f; qy=pts[k][1]+(pts[k+1][1]-pts[k][1])*f
                    d.ellipse([qx-4,qy-4,qx+4,qy+4],fill=(255,255,255,200)); break
                a2+=L[k]
        for o,(dx,dy) in enumerate([(0,0),(-46,34),(40,40),(-20,74),(30,86)]):
            plane(d,cur[0]+dx*1.4,cur[1]+dy*1.4,ang,s=34)
        if t>6.0:
            nch=int((t-6.0)*22); s=TXT[:nch]
            bx,by=cur[0]-60,cur[1]-250
            bb=d.multiline_textbbox((bx,by),TXT,font=fbub)
            d.rounded_rectangle([bb[0]-24,bb[1]-20,bb[2]+24,bb[3]+20],radius=22,fill=(255,255,255,240),outline=(20,20,20,255),width=4)
            d.polygon([(bx+40,bb[3]+18),(bx+90,bb[3]+18),(cur[0]+10,cur[1]-40)],fill=(255,255,255,240))
            d.multiline_text((bx,by),s,font=fbub,fill=(15,15,15,255))
    if t<3.0:
        al=int(255*min(ease(t/0.6),ease((3.0-t)/0.5)))
        d.text((90,H-130),"ATLANTIC OCEAN · 1945",font=fsm,fill=(230,240,255,al))
    glow=ov.filter(ImageFilter.GaussianBlur(14))
    o=np.asarray(ov).astype(np.float32)/255; g=np.asarray(glow).astype(np.float32)/255
    a=a+g[...,:3]*g[...,3:]*1.6
    a=a*(1-o[...,3:])+o[...,:3]*o[...,3:]
    a=a*vig+grain.normal(0,0.018,(H,W,1))
    a=np.clip(a,0,1)
    fade=min(1,ease(t/0.5),ease((DUR-t)/0.4)); a*=fade
    Image.fromarray((a*255).astype(np.uint8)).save(f'f/{i:04d}.jpg',quality=92)
