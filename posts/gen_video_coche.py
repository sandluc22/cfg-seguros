#!/usr/bin/env python3
# Video SEGURO DE COCHE con imagenes reales + narracion (16:9 horizontal para redes)
import subprocess, os
from PIL import Image, ImageDraw, ImageFont

IMGS="/home/node/workspace/cfg-seguros/posts/imgs_coche"
BASE="/home/node/workspace/cfg-seguros/posts"
AUDIO=f"{BASE}/coche_audio.mp3"
OUT=f"{BASE}/video_coche_imagenes.mp4"
W,H=1280,720
FPS=24

escenas=[
 ("coche_moderno.jpg",    "TU COCHE ES TU LIBERTAD"),
 ("carretera.jpg",        "LA CARRETERA ES IMPREVISIBLE"),
 ("volante.jpg",          "CONDUCE TRANQUILO, PROTEGIDO"),
 ("coche_aparcado.jpg",   "ELIGE LA COBERTURA QUE NECESITAS"),
 ("coche_carretera.jpg",  "ACTUAMOS RÁPIDO ANTE IMPREVISTOS"),
 ("coche_moderno.jpg",    "LA MEJOR TARIFA PARA TU HISTORIAL"),
 ("carretera.jpg",        "CFG SEGUROS: PROTEGE TU COCHE HOY"),
]

def dur(p):
    return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p]).decode().strip())

def ff(tam):
    for p in ['/usr/share/fonts/truetype/open-sans/OpenSans-Bold.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf']:
        if os.path.exists(p): return ImageFont.truetype(p,tam)
    return ImageFont.load_default()

def wrap(d,text,font,mw):
    palabras=text.split();lineas=[];linea=""
    for p in palabras:
        t=(linea+" "+p).strip()
        if linea and d.textlength(t,font=font)<=mw: linea=t
        else:
            if linea: lineas.append(linea)
            linea=p
    if linea: lineas.append(linea)
    return lineas

total=dur(AUDIO)
seg=total/len(escenas)
print(f"Audio {total:.1f}s, {len(escenas)} escenas de {seg:.1f}s")

vlist=[]
for i,(img,txt) in enumerate(escenas):
    im=Image.open(f"{IMGS}/{img}").convert("RGB")
    iw,ih=im.size; tr=W/H
    if iw/ih>tr:
        nw=int(ih*tr); x=(iw-nw)//2; im=im.crop((x,0,x+nw,ih))
    else:
        nh=int(iw/tr); y=(ih-nh)//2; im=im.crop((0,y,iw,y+nh))
    im=im.resize((W,H),Image.LANCZOS)
    d=ImageDraw.Draw(im)
    fs=ff(60)
    lineas=wrap(d,txt,fs,W-140)
    th=len(lineas)*fs.size+20
    d.rectangle([(0,10),(W,10+th)],fill=(0,0,0,120))
    yy=20
    for ln in lineas:
        d.text(((W-d.textlength(ln,font=fs))//2+3,yy+3),ln,font=fs,fill=(0,0,0,255))
        d.text(((W-d.textlength(ln,font=fs))//2,yy),ln,font=fs,fill=(255,255,255,255))
        yy+=fs.size+8
    wm=ff(26); wtxt="CFG Seguros"
    d.text((W-d.textlength(wtxt,font=wm)-20,H-40),wtxt,font=wm,fill=(255,255,255,200))
    slide=f"/tmp/coche_s{i}.png"; im.save(slide)
    seg_i=seg+(0.6 if i==len(escenas)-1 else 0)
    v=f"/tmp/coche_v{i}.mp4"
    zf=f"zoompan=z='min(zoom+0.0015,1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={int(seg_i*FPS)}:s={W}x{H}:fps={FPS}"
    subprocess.run(["ffmpeg","-y","-loop","1","-i",slide,"-vf",zf,"-t",f"{seg_i:.2f}","-r",str(FPS),"-c:v","libx264","-pix_fmt","yuv420p",v],check=True,capture_output=True)
    vlist.append(v)

clist="/tmp/coche_lista.txt"
open(clist,"w").write("".join(f"file '{v}'\n" for v in vlist))
subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",clist,"-c:v","libx264","-pix_fmt","yuv420p","/tmp/coche_visual.mp4"],check=True,capture_output=True)
subprocess.run(["ffmpeg","-y","-i","/tmp/coche_visual.mp4","-i",AUDIO,"-c:v","copy","-c:a","aac","-shortest",OUT],check=True,capture_output=True)
for v in vlist: os.remove(v)
for i in range(len(escenas)): os.remove(f"/tmp/coche_s{i}.png")
print("VIDEO OK", round(os.path.getsize(OUT)/1024/1024,1), "MB,", round(dur(OUT),1),"s")
