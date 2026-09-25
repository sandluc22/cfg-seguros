#!/usr/bin/env python3
# Corregir SOLO el enlace del CTA de presupuesto -> /#contactForm en todos los articulos del blog
# SIN banners, SIN cambios de diseño. Solo el href del boton de presupuesto que apunta a la home.
import re, glob, os, shutil

BLOG = "/home/node/workspace/cfg-seguros/blog"
FORM = "https://cfg-seguros.com/#contactForm"

# backup
bak="/home/node/workspace/cfg-seguros/backup_cambio_enlace"
os.makedirs(bak, exist_ok=True)

def procesar(archivo):
    html=open(archivo,encoding='utf-8',errors='ignore').read()
    original=html

    # Backup si no existe
    bn=os.path.basename(archivo)
    if not os.path.exists(os.path.join(bak,bn)):
        shutil.copy(archivo, os.path.join(bak,bn))

    # --- CORRECCION A: el enlace del CTA/boton de presupuesto que apunta a la home ---
    # Busca <a href="/"> o href="https://cfg-seguros.com/"> donde el texto/contexto sea presupuesto/contacta/solicita/cotiza
    def fix_link(m):
        ctx = html[max(0,m.start()-150):m.end()+150]
        if re.search(r'presupuesto|contrata|solicita|contact|cotiz', ctx, re.I):
            return 'href="'+FORM+'"'
        return m.group(0)

    # patrones de href a la home (relativo "/" o absoluto)
    html = re.sub(r'''href=["']/(?:index\.html)?["'#]''', lambda m: 'href="'+FORM+'"' if re.search(r'presupuesto|contrata|solicita|contact|cotiz', html[max(0,m.start()-150):m.end()+150], re.I) else m.group(0), html, flags=re.I)
    # absoluto https://cfg-seguros.com/ y https://cfg-seguros.com
    html = re.sub(r'''href=["']https://cfg-seguros\.com/?["']''', lambda m: 'href="'+FORM+'"' if re.search(r'presupuesto|contrata|solicita|contact|cotiz', html[max(0,m.start()-150):m.end()+150], re.I) else m.group(0), html, flags=re.I)

    # --- Si el articulo NO tenia ningun enlace a #contactForm, y tenia un CTA a la home, ya se corrigio arriba.
    # Verificacion: cuenta si hay al menos 1 enlace al form
    tiene_form = '#contactForm' in html

    if html!=original or True:
        open(archivo,'w',encoding='utf-8').write(html)
        return (tiene_form, html.count('#contactForm'), html.count('<div')-html.count('</div>'))
    return (tiene_form, 0, 0)

resultados=[]
for f in sorted(glob.glob(BLOG+"/*.html")):
    bn=os.path.basename(f)
    t,cnt,divs = procesar(f)
    resultados.append((bn, str(cnt), str(divs)))

print("PROCESADOS="+str(len(resultados)))
for bn,cnt,divs in resultados:
    flag='OK' if divs=='0' else 'DIV_ROTO'
    print(bn[:45]+" form="+cnt+" divs="+divs+" "+flag)
