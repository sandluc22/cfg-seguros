from PIL import Image, ImageDraw, ImageFilter
W,H=1080,1920
# fondo elegante: azul noche degradado con leve viñeta dorada
BASE="/home/node/workspace/cfg-seguros/brochure_video"
def fondo():
    img=Image.new("RGB",(W,H))
    px=img.load()
    for y in range(H):
        t=y/H
        r=int(10+14*t); g=int(14+12*t); b=int(28+18*t)
        for x in range(W):
            px[x,y]=(r,g,b)
    return img

def pagina(img, pag, zoom=1.0):
    # pagina A4 992x1404 -> escalar a ancho ~760
    pw=760; ph=int(pw*1404/992)
    p=Image.open(f"{BASE}/pag-{pag}.png").convert("RGB")
    p=p.resize((pw,ph),Image.LANCZOS)
    # sombra
    sh=Image.new("RGBA",(pw+80,ph+80),(0,0,0,0))
    d=ImageDraw.Draw(sh); d.rounded_rectangle([0,0,pw+79,ph+79],radius=18,fill=(0,0,0,180))
    sh=sh.filter(ImageFilter.GaussianBlur(20))
    # pegar sombra centrada
    img.paste(sh,(W-(pw+80)//2-(pw+80)//2, 80), sh)
    img.paste(p,((W-pw)//2,(H-ph)//2))
    return img

# escena con la pagina en posicion y zoom (se aplicara zoompan luego sobre el still)
for i,pag in enumerate(["01","02","03","04","05"] , start=0):
    pag_num=int(pag)
    img=fondo()
    pagina(img,pag_num)
    img.convert("RGB").save(f"{BASE}/escena_{pag}.png")
    print(f"escena {pag} ok", img.size)
# cierre: portada con marca
img=fondo()
pagina(img,1)
img.convert("RGB").save(f"{BASE}/escena_cierre.png")
print("escena cierre ok")
