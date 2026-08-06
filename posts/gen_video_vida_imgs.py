#!/usr/bin/env python3
# Video de SEGURO DE VIDA con IMAGENES reales + narracion (formato 16:9 horizontal para redes)
import subprocess, os, sys
from PIL import Image, ImageDraw, ImageFont

IMGS="/home/node/workspace/cfg-seguros/posts/imgs_vida"
BASE="/home/node/workspace/cfg-seguros/posts"
AUDIO=f"{BASE}/video_vida_audio.mp3"
OUT=f"{BASE}/video_vida_imagenes.mp4"
W,H=1280,720
FPS=24

# Escenas: (imagen, texto)
escenas=[
 ("familia.jpg",        "PROTEGE A TU FAMILIA"),
 ("madre_hijo.jpg",     "SI TÚ FALTAS, LA DEUDA SIGUE"),
 ("casa.jpg",           "ELLOS NO DEBERÍAN CARGAR SOLOS"),
 ("familia_campo.jpg",  "POR ESO EXISTE EL SEGURO DE VIDA"),
 ("padres_hijos.jpg",   "NO ES PARA TI: ES PARA ELLOS"),
 ("dinero.jpg",         "CUESTA MENOS DE LO QUE PIENSAS"),
]

def dur(p):
    return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p]).decode().strip())

def ff(tam,bold=True):
    cands=(['/usr/share/fonts/truetype/open-sans/OpenSans-Bold.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'] if bold else ['/usr/share/fonts/truetype/open-sans/OpenSans-Regular.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'])
    for p in cands:
        if os.path.exists(p): return ImageFont.truetype(p,tam)
    return ImageFont.load_default()

def wrap(d,text,font,mw):
    palabras=text.split();lineas=[];linea=""
    for p in palabras:
        t=(linea+" "+p).strip()
        if d.textlength(t,font=font)<=mw and linea: linea=t
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
    # precrop a 16:9 (relacion de aspecto correcta)
    im=Image.open(ip).convert("RGB")
    iw,ih=im.size
    tr=W/H
    if iw/ih > tr:
        nw=int(ih*tr); x=(iw-nw)//2; im=im.crop((x,0,x+nw,ih))
    else:
        nh=int(iw/tr); y=(ih-nh)//2; im=im.crop((0,y,iw,y+nh))
    im=im.resize((W,H),Image.LANCZOS)

    # texto central
    d=ImageDraw.Draw(im)
    fs=ff(64,True)
    lineas=wrap(d,txt,fs,W-140)
    # caja trasera
    th=len(lineas)*fs.size+20
    y0=H-180-th
    d.rectangle([(0,y0),(W,y0+th+20)],fill=(0,0,0,110))
    yy=y0+10
    for ln in lineas:
        d.text(((W-d.textlength(ln,font=fs))//2+3,yy+3),ln,font=fs,fill=(0,0,0,255))
        d.text(((W-d.textlength(ln,font=fs))//2,yy),ln,font=fs,fill=(255,255,255,255))
        yy+=fs.size+10
    # marca CFG Seguros
    wm=ff(26,True)
    wtxt="CFG Seguros"
    wl=d.textlength(wtxt,font=wm)
    d.text((W-wl-20,H-40),wtxt,font=wm,fill=(255,255,255,200))

    slide=f"/tmp/vida_slide_{i}.png"
    im.save(slide)
    seg_i=seg + (0.6 if i==len(escenas)-1 else 0)
    v=f"/tmp/vida_v{i}.mp4"
    # zoompan lento sobre la imagen
    zf=f"zoompan=z='min(zoom+0.0015,1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={int(seg_i*FPS)}:s={W}x{H}:fps={FPS}"
    subprocess.run(["ffmpeg","-y","-loop","1","-i",slide,"-vf",zf,"-t",f"{seg_i:.2f}","-r",str(FPS),"-c:v","libx264","-pix_fmt","yuv420p",v],check=True,capture_output=True)
    vlist.append(v)

# concat
clist="/tmp/vida_lista.txt"
open(clist,"w").write("".join(f"file '{v}'\n" for v in vlist))
subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",clist,"-c:v","libx264","-pix_fmt","yuv420p","/tmp/vida_visual.mp4"],check=True,capture_output=True)
# juntar con audio
subprocess.run(["ffmpeg","-y","-i","/tmp/vida_visual.mp4","-i",AUDIO,"-c:v","copy","-c:a","aac","-shortest",OUT],check=True,capture_output=True)

# limpiar
for v in vlist:
    os.remove(v)
for i in range(len(escenas)):
    os.remove(f"/tmp/vida_slide_{i}.png")

print("VIDEO OK", round(os.path.getsize(OUT)/1024/1024,1), "MB,", round(dur(OUT),1),"s,", W,"x",H)
