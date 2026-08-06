#!/usr/bin/env python3
import subprocess, os, math

W,H,FPS = 720,1280,30
OUT = "/home/node/workspace/cfg-seguros/posts"

def zoompan(img_in, out_png, dur, size, zoom_from=1.0, zoom_to=1.12, x='(iw-iw/zoom)/2', y='(ih-ih/zoom)/2'):
    f = dur*FPS
    s = f"{W}x{H}"
    vf = f"scale={size},zoompan=z='min(zoom+0.0008,{zoom_to})':d={f}:x={x}:y={y}:s={s}:fps={FPS}"
    cmd = ["ffmpeg","-y","-i",img_in,"-vf",vf,"-frames:v","1","-f","image2",out_png]
    subprocess.run(cmd, check=True, capture_output=True)

def make_short(name, shots, slide_dur=4.0, pad_dur=3.0, audio_placeholder=False):
    # shots: list of (png, overlay_text, align) ; align 'top'|'center'|'bottom'
    parts = []
    tmpdir = f"/tmp/{name}"
    os.makedirs(tmpdir, exist_ok=True)
    for i,(png,text,align) in enumerate(shots):
        # render frame with text via Pillow
        import PIL
        from PIL import Image, ImageDraw, ImageFont
        im = Image.open(png).convert("RGB")
        # resize/crop to 720x1280 center
        iw,ih = im.size
        tr = W/H
        if iw/ih > tr:
            nw = int(ih*tr); x0=(iw-nw)//2; im=im.crop((x0,0,x0+nw,ih))
        else:
            nh = int(iw/tr); y0=(ih-nh)//2; im=im.crop((0,y0,iw,y0+nh))
        im = im.resize((W,H), Image.LANCZOS)
        # dark overlay for legibility
        ov = Image.new("RGB",(W,H),(0,0,0))
        im = Image.blend(im, ov, 0.35)
        d = ImageDraw.Draw(im)
        # try fonts
        font_lines = None
        for fp in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf","/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"]:
            if os.path.exists(fp):
                font_lines = ImageFont.truetype(fp, 56); break
        else:
            font_lines = ImageFont.load_default()
        # wrap text
        lines = text.split("\n")
        line_h = 64
        total_h = len(lines)*line_h
        if align=='center':
            y = (H-total_h)//2
        elif align=='bottom':
            y = H-260-total_h
        else:
            y = 180
        for ln in lines:
            bw = d.textbbox((0,0),ln,font=font_lines)
            tx = (W-(bw[2]-bw[0]))//2
            # shadow
            d.text((tx+4,y+4),ln,font=font_lines,fill=(0,0,0))
            d.text((tx,y),ln,font=font_lines,fill=(255,255,255))
            y+=line_h
        fr = f"{tmpdir}/s{i}.png"
        im.save(fr)
        # motion: zoompan on the still frame
        with open(fr,'rb') as f:
            pass
        dur = slide_dur
        faded = f"{tmpdir}/m{i}.mp4"
        vf = f"zoompan=z='min(zoom+0.0010,1.15)':d={int(dur*FPS)}:x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':s={W}x{H}:fps={FPS}"
        subprocess.run(["ffmpeg","-y","-framerate",str(FPS),"-loop","1","-i",fr,"-vf",vf,
                        "-t",str(dur),"-c:v","libx264","-pix_fmt","yuv420p","-r",str(FPS),faded],
                       check=True, capture_output=True)
        parts.append(faded)
    # concatenate
    lst = f"{tmpdir}/list.txt"
    with open(lst,"w") as fh:
        for p in parts: fh.write(f"file '{p}'\n")
    out_mp4 = f"{OUT}/{name}.mp4"
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",lst,"-c","copy",out_mp4],
                   check=True, capture_output=True)
    print("OK", out_mp4, round(os.path.getsize(out_mp4)/1e6,1),"MB")

# ---- SHORT 1: BAJA LABORAL AUTÓNOMO ----
make_short("short_autonomo_baja_laboral", [
    ("imgs_autonomos/autonomo_trabajo.jpg","AUTÓNOMO:\nTRABAJAS 12 HORAS\nPARA NO PERDERLO TODO",'top'),
    ("imgs_autonomos/oficina.jpg","¿Y SI MAÑANA\nNO PUEDES TRABAJAR?\n\nSin sueldo desde el día 1",'center'),
    ("imgs_autonomos/portatil_trabajo.jpg","EL SEGURO DE BAJA\nTE CUBRE EL SUELDO\nQUE NO QUIERES PERDER",'center'),
    ("imgs_autonomos/dinero_negocio.jpg","PROTEGE TU NEGOCIO\nPROTEGE TUS INGRESOS",'bottom'),
])

# ---- SHORT 2: COCHE COMO HERRAMIENTA DE TRABAJO ----
make_short("short_autonomo_coche_trabajo", [
    ("imgs_coche/coche_moderno.jpg","TU COCHE\nNO ES UN LUJO\nES TU HERRAMIENTA",'top'),
    ("imgs_coche/carretera.jpg","¿ERES AUTÓNOMO\nY VIAJAS PARA TRABAJAR?",'center'),
    ("imgs_coche/volante.jpg","ASEGURA TU HERRAMIENTA\nAUTÓNOMO + COCHE\n= PROTECCIÓN TOTAL",'center'),
    ("imgs_coche/coche_carretera.jpg","SEGURO DE AUTÓNOMO\nQUE CUBRE TU TRABAJO",'bottom'),
])
