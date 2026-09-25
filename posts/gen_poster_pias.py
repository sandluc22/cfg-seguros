#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pósters motivacionales PIAS / ahorro / interés compuesto — CFG SEGUROS.
Reutiliza el enfoque de posters_cfg (render HTML con chromium headless),
adaptando marca a CFG SEGUROS (escudo+palomita, navy + dorado, cfg-seguros.com).
USO: gen_poster_pias.py --foto X.jpg --fondo-color "#0D2A4A"
        --tag "..."; --titulo1 ... --titulo2 ... --sub ... --cta ... --out out.png
"""
import argparse, subprocess, os, sys, base64

LOGO = "/home/node/workspace/cfg-seguros/logo-cfg-seguros.png"

def b64(p):
    with open(p, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--foto", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--tag", default="Ahorro e Inversión")
    ap.add_argument("--titulo1", default="", help="línea 1 (blanco o parte normal)")
    ap.add_argument("--titulo2", default="", help="línea 2 en DORADO/resaltado")
    ap.add_argument("--sub", default="")
    ap.add_argument("--cta", default="Pide información en CFG Seguros")
    ap.add_argument("--uso", default="cfg-seguros.com")
    o = ap.parse_args()

    logo_data = b64(LOGO)
    FOTO = os.path.abspath(o.foto)

    html = f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<style>
  html,body{{margin:0;padding:0;width:1600px;height:900px;overflow:hidden;background:#0D2440;font-family:'Montserrat','DejaVu Sans',sans-serif;}}
  .bg{{position:absolute;left:0;top:0;width:1600px;height:900px;}}
  .bg img{{position:absolute;width:1600px;height:900px;object-fit:cover;display:block;}}
  .overlay{{position:absolute;inset:0;background:linear-gradient(100deg, rgba(6,20,38,0.97) 0%, rgba(10,32,56,0.93) 28%, rgba(13,42,74,0.75) 48%, rgba(13,42,74,0.30) 75%, rgba(13,42,74,0.02) 100%);}}
  .shade{{position:absolute;inset:0;background:linear-gradient(to top, rgba(5,16,30,0.85), rgba(5,16,30,0) 30%);}}
  .content{{position:absolute;inset:0;z-index:5;box-sizing:border-box;padding:50px 62px 42px;display:flex;flex-direction:column;justify-content:space-between;}}
  .top{{display:flex;align-items:center;justify-content:space-between;width:100%;}}
  .brand{{display:flex;align-items:center;}}
  .brand img{{height:74px;}}
  .pill{{margin-top:18px;display:inline-block;width:max-content;max-width:100%;background:rgba(255,255,255,0.10);border:2px solid #FFD700;color:#FFD700;font-weight:800;font-size:24px;letter-spacing:3px;text-transform:uppercase;padding:11px 26px;border-radius:50px;font-family:'Montserrat','DejaVu Sans',sans-serif;}}
  .title{{color:#ffffff;font-family:'Anton','DejaVu Sans',sans-serif;font-weight:400;font-size:92px;line-height:1.03;margin:28px 0 0;max-width:1040px;text-shadow:0 4px 22px rgba(0,0,0,0.45);}}
  .title .hl{{color:#FFD700;}}
  .sub{{color:#f0f6fd;font-size:34px;font-weight:600;line-height:1.4;margin:30px 0 0;max-width:1050px;}}
  .sub b,.sub .g{{color:#FFE58A;}}
  .bottom{{display:flex;align-items:center;justify-content:space-between;margin-top:38px;width:100%;}}
  .cta{{background:linear-gradient(135deg,#FFD700,#f5a80b);color:#0D2440;font-weight:800;font-size:38px;padding:18px 44px;border-radius:16px;box-shadow:0 8px 30px rgba(245,168,11,0.5);font-family:'Montserrat','DejaVu Sans',sans-serif;}}
  .note{{color:#cfe0f2;font-size:24px;font-weight:700;}}
</style></head><body>
<div class="wrap">
 <div class="bg"><img src="file://{FOTO}"></div>
 <div class="overlay"></div><div class="shade"></div>
 <div class="content">
  <div>
   <div class="top">
     <div class="brand"><img src="{logo_data}"></div>
   </div>
   <div class="pill">{o.tag}</div>
   <div class="title">{o.titulo1}<br><span class="hl">{o.titulo2}</span></div>
   <div class="sub">{o.sub}</div>
  </div>
  <div class="bottom"><div class="cta">{o.cta}</div><div class="note">{o.uso}</div></div>
 </div>
</div>
</body></html>"""

    hpath = "/tmp/poster_pias_src.html"
    open(hpath, "w", encoding="utf-8").write(html)
    cmd = ["chromium", "--headless", "--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage",
           "--hide-scrollbars", "--window-size=1600,900", "--screenshot=" + os.path.abspath(o.out),
           "file://" + hpath]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if not os.path.exists(o.out) or os.path.getsize(o.out) == 0:
        print("FALLO:", r.stderr[-1000:]); sys.exit(1)
    from PIL import Image
    im = Image.open(o.out).convert("RGB")
    print("OK", o.out, im.size)

if __name__ == "__main__":
    main()
