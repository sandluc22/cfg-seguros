#!/usr/bin/env python3
# Insertar banner CTA arriba y corregir enlace presupuesto -> /#contactForm
# Primero se aplica a UN articulo de ejemplo (responsabilidad civil)
import re, sys

FORM_ANCHOR = "https://cfg-seguros.com/#contactForm"
BANNER = """
<!-- CTA PRESUPUESTO -->
<div style="background:#1F365C;border:3px solid #C9A227;border-radius:10px;padding:22px 24px;margin:24px 0;text-align:center;">
  <p style="color:#ffffff;font-size:22px;font-weight:bold;margin:0 0 10px 0;">¿Quieres saber cuánto cuesta tu seguro?</p>
  <p style="color:#E9EFF7;font-size:17px;margin:0 0 14px 0;">Solicita tu presupuesto gratis y sin compromiso. Te respondemos rápido.</p>
  <a href="__ANCHOR__" style="display:inline-block;background:#C9A227;color:#1F365C;font-weight:bold;font-size:19px;padding:14px 34px;border-radius:6px;text-decoration:none;">📞 Contáctanos · Solicita tu presupuesto</a>
</div>
"""

def insertar_banner(html):
    # punto de insercion: justo despues del <main> o despues del primer <h1> del articulo
    idx=None
    m=re.search(r'<main[^>]*>',html,re.I)
    if m:
        idx=m.end()
    else:
        h=re.search(r'<article[^>]*>',html,re.I) or re.search(r'<body[^>]*>',html,re.I)
        if h: idx=h.end()
    if idx is None:
        return html, False
    banner=BANNER.replace("__ANCHOR__", FORM_ANCHOR)
    return html[:idx]+banner+html[idx:], True

def corregir_enlaces(html):
    # Reemplazar enlaces a la home (href="/" o href="https://cfg-seguros.com/") por el ancla del form
    # SOLO dentro de contexto de CTA/boton, no romper links de logo/nav
    # Simplificamos: reemplazar href="/" y href="https://cfg-seguros.com/" -> /#contactForm
    # pero cuidado con el nav. Mejor: reemplazar el href si el texto del enlace contiene presupuesto/contacta/solicita
    def fix(m):
        texto_ctx=html[max(0,m.start()-200):m.end()+200]
        if re.search(r'presupuesto|contrata|solicita|contact',texto_ctx,re.I):
            return 'href="'+FORM_ANCHOR+'"'
        return m.group(0)
    html2=re.sub(r'''href=["'](?:/|https://cfg-seguros\.com/?)(?:#(?:contact|form)[^"']*)?["']''', fix, html, flags=re.I)
    return html2

def main():
    src=sys.argv[1]; out=sys.argv[2]
    html=open(src,encoding='utf-8',errors='ignore').read()
    html,c1=insertar_banner(html)
    html2=corregir_enlaces(html)
    c2 = html2!=html
    open(out,'w',encoding='utf-8').write(html2)
    print("banner="+str(c1))
    print("enlace_corregido="+str(c2))

if __name__=='__main__':
    main()
