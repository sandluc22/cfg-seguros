#!/usr/bin/env python3
"""Add CTA + footer to cfg-seguros blog pages"""
import sys, os

files = [
    'blog/seguro-vida-mitos-realidades.html',
    'blog/seguro-salud-guia-completa.html',
    'blog/ahorro-inversion-primeros-pasos.html',
    'blog/proteccion-empresas-autonomos.html',
]

os.chdir('/home/node/workspace/cfg-seguros')

cta = '''
<section style="background:linear-gradient(135deg,#0a1f44,#1a3a6a);padding:50px 20px;text-align:center;color:white;">
  <div style="max-width:600px;margin:0 auto;">
    <div style="font-size:40px;margin-bottom:12px;">\U0001f6e1\ufe0f</div>
    <h2 style="font-size:22px;font-weight:700;margin-bottom:10px;">\u00bfTe ayudamos a elegir?</h2>
    <p style="opacity:.9;margin-bottom:20px;font-size:15px;">No todas las polizas son iguales. Solicita un presupuesto personalizado y te asesoramos sin compromiso.</p>
    <a href="/#contacto" style="display:inline-block;background:#ffd700;color:#0a1f44;padding:14px 32px;border-radius:8px;text-decoration:none;font-weight:700;font-size:16px;">\U0001f4dd Quiero mi presupuesto</a>
  </div>
</section>
<footer style="background:#0a1f44;color:#94a3b8;padding:30px 20px;text-align:center;font-size:13px;">
  <div>
    <a href="/" style="color:#ffd700;text-decoration:none;">CFG Seguros</a> \u00b7 Protege lo que importa<br>
    <span style="font-size:12px;">&copy; 2026 CFG Seguros</span>
  </div>
</footer>
'''

for f in files:
    with open(f) as fh:
        content = fh.read()
    
    if 'presupuesto personalizado' not in content:
        content = content.replace('</body>', cta + '</body>')
        print(f'✅ CTA + footer añadido en {f}')
    
    with open(f, 'w') as fh:
        fh.write(content)

print('✅ Blog CTA y footer completados')
