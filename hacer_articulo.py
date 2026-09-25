import re
# Plantilla
tpl=open('blog/ahorrar-seguro-coche.html',encoding='utf-8').read()
nuevo=open('contenido_articulo1.html',encoding='utf-8').read().strip()

slug='que-cubre-un-seguro-de-vida'
TITLE='Qué cubre un seguro de vida y por qué te conviene tenerlo'
DESC='Descubre qué cubre un seguro de vida, quién debería contratarlo y qué tener en cuenta para elegir el tuyo. Asesoramiento en CFG Seguros.'

def replace_title_desc(html,title,desc):
    # title
    html=re.sub(r'<title>.*?</title>','<title>'+title+'</title>',html,count=1,flags=re.S)
    # meta description (primera)
    html=re.sub(r'(<meta\s+name="description"\s+content=")[^"]*(")', r'\g<1>'+desc+r'\g<2>', html, count=1, flags=re.I)
    return html

def replace_content(tpl, nuevo, TITLE):
    # localizar el h1 en el body y el <footer>
    mb=re.search(r'<h1\b', tpl)
    # encontrar cierre del bloque de contenido: buscar el <footer> más cercano tras el h1
    # si no hay footer, usar </body>
    fi=re.search(r'\s*<footer\b', tpl)
    fin=fi.start() if fi else tpl.rfind('</body>')
    h1i=mb.start()
    # antes del h1: cabecera/contenido inicial (ej. nav, banner, breadcrumb)
    pre=tpl[:h1i]
    # despues del contenido: footer+
    post=tpl[fin:]
    # titulo en h1: reemplazar el h1 actual por el nuevo (para que el title del h1 coincida)
    nuevo2=re.sub(r'<h1[^>]*>[^<]*</h1>','<h1>'+TITLE+'</h1>',nuevo,count=1)
    return pre+nuevo2+post

html2=replace_title_desc(tpl,TITLE,DESC)
out=replace_content(html2,nuevo,TITLE)
open('blog/'+slug+'.html','w',encoding='utf-8').write(out)
print('CREADO blog/'+slug+'.html')
