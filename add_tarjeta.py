import re
idx=open('blog/index.html',encoding='utf-8').read()
slug='que-cubre-un-seguro-de-vida'
TITLE='Qué cubre un seguro de vida y por qué te conviene tenerlo'
# extracto: primer parrafo del articulo nuevo
contenido=open('blog/'+slug+'.html',encoding='utf-8').read()
mp=re.search(r'<p>(.*?)</p>',contenido,re.S)
extracto=re.sub(r'<[^>]+>','',mp.group(1)).strip()
if len(extracto)>110: extracto=extracto[:107].rstrip()+'...'
FECHA='6 agosto 2026'
tarjeta='<a href="'+slug+'.html"><h3>'+TITLE+'</h3><p>'+extracto+'</p><span class="date">'+FECHA+'</span></a>'
# insertar antes del cierre del bloque o tras la primera tarjeta
# detectar el bloque de articulos: buscar la primera aparicion de '<a href="'+primer html
refs=list(re.finditer(r'<a\b[^>]*href=\"([^\"]+\.html)\"[^>]*>',idx))
if refs:
    pos=refs[0].start()
    idx=idx[:pos]+tarjeta+chr(10)+idx[pos:]
    open('blog/index.html','w',encoding='utf-8').write(idx)
    print('INSERTADA_TARJETA')
else:
    print('SIN_REFERENCIA')
