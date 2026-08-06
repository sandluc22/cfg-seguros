#!/usr/bin/env python3
import subprocess, os
from PIL import Image, ImageDraw, ImageFont

W,H,FPS = 720,1280,30
OUT = "/home/node/workspace/cfg-seguros/posts"
GOLD = (184,134,11)
NAVY = (15,40,68)

def font(size):
    for fp in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
               "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"]:
        if os.path.exists(fp):
            return ImageFont.truetype(fp, size)
    return ImageFont.load_default()

def center_text(d, text, y, fnt, fill=(255,255,255)):
    b = d.textbbox((0,0), text, font=fnt)
    x = (W-(b[2]-b[0]))//2
    d.text((x+4,y+4), text, font=fnt, fill=(0,0,0))
    d.text((x,y), text, font=fnt, fill=fill)

def build_frame(png, lines, style):
    """lines: list of (text,size,color); style: layout"""
    im = Image.open(png).convert("RGB")
    iw,ih = im.size
    tr = W/H
    if iw/ih > tr:
        nw=int(ih*tr); x0=(iw-nw)//2; im=im.crop((x0,0,x0+nw,ih))
    else:
        nh=int(iw/tr); y0=(ih-nh)//2; im=im.crop((0,y0,iw,y0+nh))
    im = im.resize((W,H), Image.LANCZOS)
    # light dark for legibility (mild)
    im = Image.blend(im, Image.new("RGB",(W,H),(0,0,0)), 0.22)
    d = ImageDraw.Draw(im)
    # top gold band
    d.rectangle([0,90,W,130], fill=GOLD)
    # text block
    y = 170 if style=='top' else (H-420 if style=='bottom' else (H-450)//2)
    for t,sz,col in lines:
        f=font(sz)
        center_text(d,t,y,f,col if col else (255,255,255))
        y += sz+26
    # bottom navy band
    d.rectangle([0,H-120,W,H], fill=NAVY)
    f=font(30)
    center_text(d,"cfg-seguros.com", H-88, f, (255,255,255))
    im.save("/tmp/frame.png")
    return "/tmp/frame.png"

def make_short(name, slides, slide_dur=4.2):
    # slides: list of dict {img, lines, style}
    parts=[]
    tmp=f"/tmp/{name}"; os.makedirs(tmp, exist_ok=True)
    for i,sl in enumerate(slides):
        fr=build_frame(sl['img'], sl['lines'], sl['style'])
        dur=slide_dur
        mp4=f"{tmp}/m{i}.mp4"
        vf=f"zoompan=z='min(zoom+0.0010,1.14)':d={int(dur*FPS)}:x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':s={W}x{H}:fps={FPS}"
        subprocess.run(["ffmpeg","-y","-framerate",str(FPS),"-loop","1","-i",fr,"-vf",vf,
                        "-t",str(dur),"-c:v","libx264","-pix_fmt","yuv420p","-r",str(FPS),mp4],
                       check=True, capture_output=True)
        parts.append(mp4)
    lst=f"{tmp}/list.txt"
    with open(lst,"w") as fh:
        for p in parts: fh.write(f"file '{p}'\n")
    out=f"{OUT}/{name}.mp4"
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",lst,"-c","copy",out],
                   check=True, capture_output=True)
    print("OK", out, round(os.path.getsize(out)/1e6,1),"MB")

BAJA = [
 dict(img="imgs_autonomos/autonomo_trabajo.jpg", style='top',
      lines=[("AUTÓNOMO",44,GOLD),("trabajas 12 horas",44,(255,255,255)),("para no perderlo todo",40,(255,255,255))]),
 dict(img="imgs_autonomos/oficina.jpg", style='center',
      lines=[("¿Y SI MAÑANA",52,(255,255,255)),("NO PUEDES TRABAJAR?",54,(255,255,255)),("Sin sueldo desde el día 1",34,GOLD)]),
 dict(img="imgs_autonomos/portatil_trabajo.jpg", style='center',
      lines=[("El seguro de baja",46,(255,255,255)),("te cubre el sueldo",46,(255,255,255)),("que no quieres perder",40,GOLD)]),
 dict(img="imgs_autonomos/dinero_negocio.jpg", style='center',
      lines=[("PROTEGE TU NEGOCIO",46,GOLD),("PROTEGE TUS INGRESOS",46,(255,255,255))]),
]
COCHE = [
 dict(img="imgs_coche/coche_moderno.jpg", style='top',
      lines=[("AUTÓNOMO",44,GOLD),("tu coche NO es un lujo",42,(255,255,255)),("es tu herramienta de trabajo",40,(255,255,255))]),
 dict(img="imgs_coche/carretera.jpg", style='center',
      lines=[("¿VIAJAS PARA TRABAJAR?",52,(255,255,255)),("Tu coche es tu negocio",40,GOLD)]),
 dict(img="imgs_coche/volante.jpg", style='center',
      lines=[("AUTÓNOMO + COCHE",50,GOLD),("asegura tu herramienta",46,(255,255,255)),("protección total",40,(255,255,255))]),
 dict(img="imgs_coche/coche_carretera.jpg", style='center',
      lines=[("SEGURO DE AUTÓNOMO",44,GOLD),("que cubre tu trabajo",46,(255,255,255))]),
]

make_short("short_autonomo_baja_laboral", BAJA)
make_short("short_autonomo_coche_trabajo", COCHE)
