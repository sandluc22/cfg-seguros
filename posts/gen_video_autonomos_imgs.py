#!/usr/bin/env python3
# Video SEGURO DE AUTONOMOS con imagenes reales + narracion (16:9 horizontal para redes)
import subprocess, os
from PIL import Image, ImageDraw, ImageFont

IMGS="/home/node/workspace/cfg-seguros/posts/imgs_autonomos"
BASE="/home/node/workspace/cfg-seguros/posts"
AUDIO=f"{BASE}/autonomos_audio.mp3"
OUT=f"{BASE}/video_autonomos_imagenes.mp4"
W,H=1280,720
FPS=24

escenas=[
 ("autonomo_trabajo.jpg",  "SER AUTÓNOMO ES CONSTRUIR LO TUYO"),
 ("emprendedor.jpg",       "PERO ¿QUÉ PASA SI TE PONES ENFERMO?"),
 ("planificar.jpg",        "SI TU NEGOCIO SE PARA, LOS GASTOS SIGUEN"),
 ("portatil_trabajo.jpg",  "POR ESO EXISTE EL SEGURO DE AUTÓNOMO"),
 ("oficina.jpg",           "CUBRE TU BAJA Y PROTEGE TU ACTIVIDAD"),
 ("dinero_negocio.jpg",    "TU RED DE SEGURIDAD ANTE IMPREVISTOS"),
 ("confianza.jpg",         "CUESTA MENOS DE LO QUE IMAGINAS"),
 ("cafe_negocio.jpg",      "CFG SEGUROS: PRESUPUESTO SIN COMPROMISO"),
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
    ip=f"{IMGS}/{img}"
    im=Image.open(ip).convert("RGB")
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
    # caja oscura arriba para legibilidad
    d.rectangle([(0,10),(W,10+th)],fill=(0,0,0,120))
    yy=20
    for ln in lineas:
        d.text(((W-d.textlength(ln,font=fs))//2+3,yy+3),ln,font=fs,fill=(0,0,0,255))
        d.text(((W-d.textlength(ln,font=fs))//2,yy),ln,font=fs,fill=(255,255,255,255))
        yy+=fs.size+8
    wm=ff(26); wtxt="CFG Seguros"
    d.text((W-d.textlength(wtxt,font=wm)-20,H-40),wtxt,font=wm,fill=(255,255,255,200))
    slide=f"/tmp/auto_slide_{i}.png"; im.save(slide)
    seg_i=seg+(0.6 if i==len(escenas)-1 else 0)
    v=f"/tmp/auto_v{i}.mp4"
    zf=f"zoompan=z='min(zoom+0.0015,1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={int(seg_i*FPS)}:s={W}x{H}:fps={FPS}"
    subprocess.run(["ffmpeg","-y","-loop","1","-i",slide,"-vf",zf,"-t",f"{seg_i:.2f}","-r",str(FPS),"-c:v","libx264","-pix_fmt","yuv420p",v],check=True,capture_output=True)
    vlist.append(v)

clist="/tmp/auto_lista.txt"
open(clist,"w").write("".join(f"file '{v}'\n" for v in vlist))
subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",clist,"-c:v","libx264","-pix_fmt","yuv420p","/tmp/auto_visual.mp4"],check=True,capture_output=True)
subprocess.run(["ffmpeg","-y","-i","/tmp/auto_visual.mp4","-i",AUDIO,"-c:v","copy","-c:a","aac","-shortest",OUT],check=True,capture_output=True)
for v in vlist: os.remove(v)
for i in range(len(escenas)): os.remove(f"/tmp/auto_slide_{i}.png")
print("VIDEO OK", round(os.path.getsize(OUT)/1024/1024,1), "MB,", round(dur(OUT),1),"s")
