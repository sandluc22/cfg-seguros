#!/usr/bin/env python3
# Videito corto SEGURO DE VIDA para LINKEDIN (vertical 9:16, 720x1280)
import subprocess, os
from PIL import Image, ImageDraw, ImageFont

IMGS="/home/node/workspace/cfg-seguros/posts/imgs_vida"
BASE="/home/node/workspace/cfg-seguros/posts"
AUDIO=f"{BASE}/linkedin_vida_audio.mp3"
OUT=f"{BASE}/linkedin_vida_video.mp4"
W,H=720,1280
FPS=24

escenas=[
 ("familia.jpg",       "¿QUIÉN DEPENDE DE TI?"),
 ("madre_hijo.jpg",    "SI TÚ FALTAS, ¿QUIÉN PAGA LA HIPOTECA?"),
 ("casa.jpg",          "EL SEGURO DE VIDA ES PARA ELLOS"),
 ("familia_campo.jpg", "CUESTA MENOS DE LO QUE IMAGINAS"),
 ("padres_hijos.jpg",  "HABLEMOS: SIMULACIÓN SIN COMPROMISO"),
]

def dur(p):
    return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p]).decode().strip())

# font
try:
    f_big=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 54)
    f_med=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
    f_water=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
except:
    f_big=ImageFont.load_default(); f_med=f_big; f_water=f_big

def wrapper(draw,text,font,maxw):
    words=text.split(); lines=[]; cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if draw.textlength(t,font=font)<=maxw: cur=t
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    return lines

adt=dur(AUDIO)
seg=adt/len(escenas)
print(f"audio {adt:.1f}s, {seg:.1f}s/escena")

# overlay transparente
ov=Image.new("RGBA",(W,H),(0,0,0,0))
od=ImageDraw.Draw(ov)
od.rectangle([0,int(H*0.62),W,H],fill=(0,0,0,170))

vlist=[]
for i,(img,txt) in enumerate(escenas):
    ip=f"{IMGS}/{img}"
    im=Image.open(ip).convert("RGB")
    iw,ih=im.size
    tr=W/H
    if iw/ih>tr:
        nw=int(ih*tr); x=(iw-nw)//2; im=im.crop((x,0,x+nw,ih))
    else:
        nh=int(iw/tr); y=(ih-nh)//2; im=im.crop((0,y,iw,y+nh))
    im=im.resize((W,H),Image.LANCZOS)
    # overlay
    im=Image.alpha_composite(im.convert("RGBA"),ov).convert("RGB")
    d=ImageDraw.Draw(im)
    lines=wrapper(d,txt.upper(),f_big,W-80)
    y=int(H*0.66)
    for ln in lines:
        wl=d.textlength(ln,font=f_big)
        d.text(((W-wl)/2,y),ln,font=f_big,fill=(255,255,255))
        y+=60
    # marca de agua
    wt="CFG SEGUROS"
    ww=d.textlength(wt,font=f_water)
    d.text((W-ww-20,H-50),wt,font=f_water,fill=(255,215,0))
    fp=f"/tmp/vida_lk_{i}.png"
    im.save(fp)
    vlist.append((fp,seg))

# montar
with open("/tmp/vida_lk.txt","w") as f:
    for fp,s in vlist:
        f.write(f"file '{fp}'\nduration {s:.3f}\n")
    f.write(f"file '{vlist[-1][0]}'\nduration 0.5\n")
cmd=["ffmpeg","-y","-f","concat","-safe","0","-i","/tmp/vida_lk.txt","-i",AUDIO,
     "-vf","fps=24","-pix_fmt","yuv420p","-c:v","libx264","-crf","23","-preset","fast",
     "-c:a","aac","-shortest",OUT]
subprocess.run(cmd,check=True,capture_output=True)
print("OUT",OUT, round(os.path.getsize(OUT)/1e6,1),"MB")
