#!/usr/bin/env python3
import subprocess, os, math
from PIL import Image, ImageDraw, ImageFont

BASE="/home/node/workspace/cfg-seguros/posts"
W,H=720,1280
FPS=24

def ff(tam,bold=True):
    cands=["/usr/share/fonts/truetype/open-sans/OpenSans-Bold.ttf",
           "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
           "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"]
    for p in cands:
        if os.path.exists(p): return ImageFont.truetype(p,tam)
    return ImageFont.load_default()

def wrap(d,text,font,mw):
    pal=text.split();lines=[];line=""
    for p in pal:
        t=(line+" "+p).strip()
        if d.textlength(t,font=font)<=mw and line: line=t
        else:
            if line: lines.append(line)
            line=p
    if line: lines.append(line)
    return lines

def make_frame(img_path, lines, font, out):
    im=Image.open(img_path).convert("RGB")
    # relleno vertical (crop a 720x1280) manteniendo centro
    im.thumbnail((2000,2000))
    iw,ih=im.size
    scale=max(W/iw,H/ih)
    im=im.resize((int(iw*scale),int(ih*scale)),Image.LANCZOS)
    iw,ih=im.size
    x=(iw-W)//2; y=(ih-H)//2
    im=im.crop((x,y,x+W,y+H))
    im=im.convert("RGBA")
    # overlay oscuro para legibilidad
    ov=Image.new("RGBA",(W,H),(0,0,0,120)); im=Image.alpha_composite(im,ov)
    d=ImageDraw.Draw(im)
    # subtitulo de marca arriba
    top=ImageFont.truetype("/usr/share/fonts/truetype/open-sans/OpenSans-Bold.ttf" if os.path.exists("/usr/share/fonts/truetype/open-sans/OpenSans-Bold.ttf") else "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",56)
    marca="CFG SEGUROS"
    tw=d.textlength(marca,font=top); d.text(((W-tw)/2,90),marca,font=top,fill=(240,196,60,255))
    # lineas centrales
    total_h=sum(d.textlength(l,font=font)//1*0 + 0 for l in []) # placeholder
    # dibujar lineas centradas
    lh=font.size+24
    start=H/2 - (len(lines)*lh)/2
    ycur=start
    for l in lines:
        lw=d.textlength(l,font=font)
        # caja negra detras
        d.rectangle([(W-lw)/2-20,ycur-12, (W+lw)/2+20, ycur+font.size+16],fill=(0,0,0,160))
        d.text(((W-lw)/2,ycur),l,font=font,fill=(255,255,255,255))
        ycur+=lh
    # sin CTA inferior
    im.convert("RGB").save(out)

def gen(name, imgs, frases, audio, out):
    adur=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",audio]).decode().strip())
    nframes=int(adur*FPS)
    frames_dir=f"{BASE}/_frames_{name}"
    os.makedirs(frames_dir,exist_ok=True)
    nseg=len(frases)
    segdur=nframes/nseg
    idx=0
    for s in range(nseg):
        img=imgs[s%len(imgs)]
        lines=wrap(ImageDraw.Draw(Image.new("RGB",(10,10))),frases[s],ff(72),W-80)
        # asegurar max 4 lineas
        if len(lines)>4: lines=lines[:4]
        for k in range(int(segdur)):
            make_frame(img,lines,ff(72),f"{frames_dir}/f{idx:05d}.png"); idx+=1
    # completar si sobra
    while idx<nframes:
        make_frame(imgs[(idx//int(segdur))%len(imgs)],wrap(ImageDraw.Draw(Image.new("RGB",(10,10))),frases[-1],ff(72),W-80),ff(72),f"{frames_dir}/f{idx:05d}.png"); idx+=1
    # video sin audio
    vraw=f"{BASE}/_raw_{name}.mp4"
    subprocess.run(["ffmpeg","-y","-framerate",str(FPS),"-i",f"{frames_dir}/f%05d.png","-c:v","libx264","-pix_fmt","yuv420p","-vf","scale=720:1280",vraw],check=True,stderr=subprocess.DEVNULL)
    # mux audio
    subprocess.run(["ffmpeg","-y","-i",vraw,"-i",audio,"-c:v","copy","-c:a","aac","-shortest",out],check=True,stderr=subprocess.DEVNULL)
    # limpiar
    subprocess.run(["rm","-rf",frames_dir,vraw])
    print(f"OK {out} ({adur:.0f}s)")
    return os.path.getsize(out)

aut=gen("autonomos",
        [f"{BASE}/imgs_autonomos/{f}" for f in ["emprendedor.jpg","oficina.jpg","autonomo_trabajo.jpg","portatil_trabajo.jpg","cafe_negocio.jpg"]],
        ["SI ENFERMAS,", "TU NEGOCIO SIGUE GASTANDO.", "PERO NADIE LO CUENTA.", "EL SEGURO DE AUTÓNOMO TE CUBRE.", "CUESTA MENOS DE LO QUE CREES."],
        f"{BASE}/audio_autonomos_NUEVO.mp3",
        f"{BASE}/short_autonomos_NUEVO.mp4")

vid=gen("vida",
        [f"{BASE}/imgs_vida/{f}" for f in ["familia.jpg","madre_hijo.jpg","casa.jpg","familia_campo.jpg","padres_hijos.jpg"]],
        ["MÁS DEL 70% NO TIENE SEGURO DE VIDA.", "PERO LA MAYORÍA TIENE HIPOTECA.", "SI TÚ FALTAS,", "¿QUIÉN PAGA LA CASA?", "NO ES PARA TI: ES PARA ELLOS."],
        f"{BASE}/audio_vida_NUEVO.mp3",
        f"{BASE}/short_vida_NUEVO.mp4")

print("TOTAL:",aut,vid)
