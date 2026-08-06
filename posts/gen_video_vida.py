#!/usr/bin/env python3
# Video corto seguro de vida CFG Seguros (vertical 720x1280, 41s)
import subprocess, os
from PIL import Image, ImageDraw, ImageFont

W,H=720,1280
FPS=24
BASE="/home/node/workspace/cfg-seguros/posts"

def ff(tam,bold=True):
    for p in (["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf","/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"] if bold else ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf","/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"]):
        if os.path.exists(p): return ImageFont.truetype(p,tam)
    return ImageFont.load_default()

def wrap(d,text,font,mw):
    pal=text.split();ls=[];l=""
    for p in pal:
        t=(l+" "+p).strip()
        if d.textlength(t,font=font)<=mw and l:l=t
        else:
            if l:ls.append(l)
            l=p
    if l:ls.append(l)
    return ls

# fondo gradiente azul (confianza/proteccion)
img=Image.new("RGB",(W,H),(10,28,52))
d=ImageDraw.Draw(img)
for y in range(H):
    t=y/H
    r=int(10+(0-10)*t); g=int(28+(60-28)*t); b=int(52+(120-52)*t)
    d.line([(0,y),(W,y)],fill=(r,g,b))
# circulo decorativo suave
for cx,cy,rad,col in [(W-60,120,140,(255,255,255,8)),(60,H-140,180,(120,180,255,6))]:
    d.ellipse([cx-rad,cy-rad,cx+rad,cy+rad],fill=col)
# marca superior
d.text((30,60),"CFG SEGUROS",font=ff(42,True),fill=(255,255,255,235))
d.text((30,115),"Seguro de Vida",font=ff(34,False),fill=(140,200,255,235))

# texto central
frag=[("PROTEGE A TU FAMILIA",ff(70,True),(255,255,255,255)),
      ("SI TÚ FALTAS, LA DEUDA SIGUE",ff(40,True),(120,190,255,255)),
      ("ELLOS NO DEBERÍAN CARGAR SOLOS",ff(34,False),(230,240,255,210))]
yy=300
for txt,ft,col in frag:
    d.rectangle([(0,yy+6),(W,yy+70+6)],fill=(0,0,0,90)) if col[0]==255 and col[1]==255 else None
    for ln in wrap(d,txt,ft,W-90):
        d.text(((W-d.textlength(ln,font=ft))//2+3,yy+3),ln,font=ft,fill=(0,0,0,255))
        d.text(((W-d.textlength(ln,font=ft))//2,yy),ln,font=ft,fill=col); yy+=ft.size+14
    yy+=20

# CTA
yy=H-340
cta="SEGURO DE VIDA = TRANQUILIDAD"
for ln in wrap(d,cta,ff(46,True),W-80):
    d.text(((W-d.textlength(ln,font=ff(46,True)))//2+3,yy+3),ln,font=ff(46,True),fill=(0,0,0,255))
    d.text(((W-d.textlength(ln,font=ff(46,True)))//2,yy),ln,font=ff(46,True),fill=(255,209,102,255)); yy+=56

slide=f"{BASE}/_vida_slide.png"; img.save(slide)

# montar video con audio
tl=41
z=f"[0:v]zoompan=z='min(zoom+0.0004,1.08)':d={int(tl*FPS)}:s={W}x{H}:fps={FPS}[vout]"
cmd=["ffmpeg","-y","-loop","1","-t",str(tl),"-i",slide,"-i",f"{BASE}/video_vida_audio.mp3",
     "-filter_complex",z,"-map","[vout]","-map","1:a",
     "-c:v","libx264","-pix_fmt","yuv420p","-crf","26","-preset","medium","-c:a","aac","-b:a","128k","-shortest",
     f"{BASE}/video_vida.mp4"]
r=subprocess.run(cmd,capture_output=True)
if r.returncode!=0:
    print("ERR",r.stderr.decode()[-150:]); sys.exit(1)
os.remove(slide)
au=subprocess.run(["ffprobe","-v","error","-show_streams",f"{BASE}/video_vida.mp4"],capture_output=True).stdout.count(b"audio")>0
print("VIDEO OK",round(os.path.getsize(f"{BASE}/video_vida.mp4")/1024/1024,1),"MB audio=",au)
