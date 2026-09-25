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

def center_text(d, text, y, fnt, fill=(255,255,255), wrap=False, maxw=600):
    if wrap:
        words = text.split()
        lines = []
        cur = ""
        for w in words:
            t = (cur+" "+w).strip()
            if d.textlength(t, font=fnt) <= maxw:
                cur = t
            else:
                if cur: lines.append(cur)
                cur = w
        if cur: lines.append(cur)
    else:
        lines = [text]
    for ln in lines:
        b = d.textbbox((0,0), ln, font=fnt)
        x = (W-(b[2]-b[0]))//2
        d.text((x+4,y+4), ln, font=fnt, fill=(0,0,0))
        d.text((x,y), ln, font=fnt, fill=fill)
        y += (b[3]-b[1]) + 20
    return y

def build_frame(png, lines, style='center'):
    im = Image.open(png).convert("RGB")
    iw,ih = im.size
    tr = W/H
    if iw/ih > tr:
        nw=int(ih*tr); x0=(iw-nw)//2; im=im.crop((x0,0,x0+nw,ih))
    else:
        nh=int(iw/tr); y0=(ih-nh)//2; im=im.crop((0,y0,iw,y0+nh))
    im = im.resize((W,H), Image.LANCZOS)
    im = Image.blend(im, Image.new("RGB",(W,H),(0,0,0)), 0.30)
    d = ImageDraw.Draw(im)
    # top gold band
    d.rectangle([0,90,W,130], fill=GOLD)
    # text block -> ABOVE CENTER (Regla Nº7: nunca abajo)
    y = 180
    for t,sz,col in lines:
        f = font(sz)
        y = center_text(d, t, y, f, col if col else (255,255,255), wrap=(sz<=46))
        y += 12
    # bottom navy band
    d.rectangle([0,H-110,W,H], fill=NAVY)
    f=font(30)
    center_text(d,"cfg-seguros.com  ·  te ayudamos a asegurarte", H-80, f, (255,255,255))
    im.save("/tmp/frame.png")
    return "/tmp/frame.png"

def make_short(name, slides, slide_dur=4.2):
    parts=[]
    tmp=f"/tmp/{name}"; os.makedirs(tmp, exist_ok=True)
    for i,sl in enumerate(slides):
        fr = build_frame(sl['img'], sl['lines'], sl.get('style','center'))
        seg = f"{tmp}/seg{i}.mp4"
        dur = sl.get('dur', slide_dur)
        vf = f"zoompan=z='min(zoom+0.0010,1.14)':d={int(dur*FPS)}:x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':s={W}x{H}:fps={FPS}"
        subprocess.run(["ffmpeg","-y","-framerate",str(FPS),"-loop","1","-i",fr,"-vf",vf,
            "-t",str(dur),"-c:v","libx264","-pix_fmt","yuv420p",seg],
            check=True, capture_output=True)
        parts.append(f"file '{seg}'")
    lst = f"{tmp}/list.txt"
    open(lst,"w").write("\n".join(parts)+"\n")
    out = f"{OUT}/{name}.mp4"
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",lst,"-c","copy",out],
        check=True, capture_output=True)
    print("OK:", out)

IMGS = "imgs_autonomos"

MOTIVA = [
 dict(img=f"{IMGS}/emprendedor.jpg",
      lines=[("AUTÓNOMO",54,GOLD),("no estás solo",46,(255,255,255)),
             ("construyes tu negocio cada día",40,(255,255,255))]),
 dict(img=f"{IMGS}/cafe_negocio.jpg",
      lines=[("pero un imprevisto",46,(255,255,255)),
             ("una baja, un accidente",44,GOLD),
             ("no debe tirar todo por la borda",38,(255,255,255))]),
 dict(img=f"{IMGS}/dinero_negocio.jpg",
      lines=[("protege lo que tanto",42,(255,255,255)),
             ("te ha costado construir",46,GOLD)]),
 dict(img=f"{IMGS}/confianza.jpg",
      lines=[("asegurar tu trabajo",44,(255,255,255)),
             ("es invertir en tu tranquilidad",40,GOLD),
             ("no es un gasto, es protegerte",38,(255,255,255))]),
 dict(img=f"{IMGS}/portatil_trabajo.jpg",
      lines=[("te ayudamos a hacerlo",46,GOLD),
             ("te conseguimos el seguro",42,(255,255,255)),
             ("que tu negocio necesita",40,(255,255,255))]),
]

make_short("short_autonomo_motivacion", MOTIVA, slide_dur=4.2)
