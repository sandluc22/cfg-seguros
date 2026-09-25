#!/usr/bin/env python3
import os, re, shutil, glob

ROOT = "/home/node/workspace/cfg-seguros"
BACK = os.path.join(ROOT, ".seo_backup_20260811")
os.makedirs(BACK, exist_ok=True)

# Páginas con canonical .html (24 + 3 artículos de hoy)
html_files = []
for pattern in ["*.html", "seguros/*.html", "blog/*.html"]:
    html_files += glob.glob(os.path.join(ROOT, pattern))

# El canonical que apunta a .html -> pasarlo a sin .html
# Ej: https://cfg-seguros.com/blog/seguro-vida.html -> https://cfg-seguros.com/blog/seguro-vida
pat = re.compile(r'(rel="canonical" href="https://cfg-seguros\.com/[^"]*)\.html(")')

cambios = []
for f in html_files:
    if "gen_articulos" in f:
        continue
    with open(f, encoding="utf-8") as fh:
        orig = fh.read()
    nuevo, n = pat.subn(r'\1\2', orig)
    if n:
        # backup solo si no existe
        bf = os.path.join(BACK, os.path.basename(f))
        if not os.path.exists(bf):
            shutil.copy2(f, bf)
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(nuevo)
        cambios.append((os.path.relpath(f, ROOT), n))

print(f"Archivos modificados: {len(cambios)}")
for r, n in cambios:
    print(f"  {r}: {n} canonical corregido")
