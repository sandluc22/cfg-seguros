#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera articulos de blog CFG Seguros enfocados en Sanitas Students/Residents.
Usa la misma plantilla/estilo que blog/seguro-visado-estudiante-espana.html."""
import os, re

BASE = os.path.dirname(os.path.abspath(__file__))
BLOG = os.path.join(BASE, "blog")

HEAD = '''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://cfg-seguros.com/blog/{slug}">
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-ZSXBB84TL3"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-ZSXBB84TL3');
</script>
<style>
  * {{margin:0;padding:0;box-sizing:border-box;}}
  body {{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:#1f2937;line-height:1.7;background:#f9fafb;}}
  .container {{max-width:860px;margin:0 auto;padding:0 20px;}}
  .header-secundario {{background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.08);position:sticky;top:0;z-index:10;}}
  .header-secundario .container {{display:flex;align-items:center;height:64px;font-size:18px;font-weight:700;letter-spacing:.3px;}}
  .post-content {{max-width:760px;margin:40px auto 30px;padding:0 20px;}}
  .post-content h1 {{font-size:32px;line-height:1.3;color:#0a1f44;margin-bottom:8px;}}
  .post-content .meta {{color:#6b7280;font-size:14px;display:block;margin-bottom:24px;}}
  .post-content h2 {{font-size:24px;color:#0a1f44;margin:36px 0 14px;}}
  .post-content h3 {{font-size:19px;color:#0a1f44;margin:24px 0 10px;}}
  .post-content p {{margin-bottom:16px;font-size:17px;}}
  .post-content ul, .post-content ol {{margin:0 0 20px 24px;font-size:17px;}}
  .post-content li {{margin-bottom:8px;}}
  .post-content a {{color:#0a6cd6;}}
  .tabla {{width:100%;border-collapse:collapse;margin:10px 0 24px;font-size:16px;}}
  .tabla th, .tabla td {{border:1px solid #e5e7eb;padding:10px 12px;text-align:left;}}
  .tabla th {{background:#0a1f44;color:#fff;}}
  .tabla tr:nth-child(even) {{background:#f3f6fb;}}
  .cta {{background:linear-gradient(135deg,#0a1f44,#123a73);color:#fff;border-radius:14px;padding:40px 32px;text-align:center;margin:40px 0 0;}}
  .cta h2 {{color:#fff;font-size:26px;margin-bottom:12px;}}
  .cta p {{font-size:16px;opacity:.9;margin-bottom:20px;}}
  .cta a {{display:inline-block;background:#ffd700;color:#0a1f44;padding:14px 32px;border-radius:8px;text-decoration:none;font-weight:700;font-size:16px;}}
  footer {{background:#0a1f44;color:#fff;padding:30px 20px;text-align:center;font-size:13px;margin-top:40px;}}
  footer a {{color:#ffd700;text-decoration:none;}}
  .cookie-banner {{position:fixed;bottom:0;left:0;right:0;background:#0a1f44;color:#fff;padding:14px 20px;font-size:14px;display:flex;justify-content:space-between;align-items:center;gap:16px;z-index:99;}}
  .cookie-banner a {{color:#ffd700;}}
  .cookie-banner button {{background:#ffd700;border:none;color:#0a1f44;padding:8px 18px;border-radius:6px;font-weight:700;cursor:pointer;}}
  .cookie-banner.hidden {{display:none;}}
</style>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{title}",
  "author": {{"@type":"Person","name":"Sandra Caicedo"}},
  "publisher": {{"@type":"Person","name":"CFG Seguros"}}
}}
</script>
<script type="application/ld+json">
{faq_schema}
</script>
</head>
<body>
<header class="header-secundario">
  <div class="container">
    <a href="/"><img src="/logo.png?v=20260629" alt="CFG" style="height:38px;vertical-align:middle"> <span style="color:#0a1f44">Crecimiento</span> <span style="color:#f0c040">Financiero Global</span></a>
  </div>
</header>
<main class="post-content">
  <h1>{h1}</h1>
  <span class="meta">Por Sandra Caicedo · 25 de septiembre de 2026</span>
'''

FOOT = '''  <section class="cta">
    <h2>¿Te ayudamos con tu seguro Sanitas?</h2>
    <p>Sanitas Students y Sanitas Residents · Sin copagos ni carencias · Presupuesto sin compromiso.</p>
    <a href="https://cfg-seguros.com/#contactForm">📝 Solicitar presupuesto</a>
  </section>
</main>
<footer>
  <div>
    <a href="/">CFG Seguros</a> · Agente exclusiva Sanitas · Protege lo que importa<br>
    <span style="font-size:12px;">&copy; 2026 CFG Seguros</span>
  </div>
</footer>
<div id="cookie-banner" class="cookie-banner"><span>Usamos cookies propias y de terceros (Google Analytics) para mejorar tu experiencia. <a href="/cookies.html">Más información</a></span><button onclick="aceptarCookies()">Aceptar</button></div>
<script>
function aceptarCookies() {document.getElementById('cookie-banner').classList.add('hidden');localStorage.setItem('cookies_aceptadas','true');}
if (localStorage.getItem('cookies_aceptadas') === 'true') {document.getElementById('cookie-banner').classList.add('hidden');}
</script>
</body>
</html>'''

def faq_schema(items):
    ent = ",\n".join(
      '    {"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}' % (q, a) for q, a in items)
    return ('{\n  "@context":"https://schema.org",\n  "@type":"FAQPage",\n  "mainEntity":[\n%s\n  ]\n}' % ent)

ARTICULOS = {
 "sanitas-students-vs-residents-visado": {
   "title": "Sanitas Students vs Sanitas Residents: cuál elegir para tu visado en España | CFG Seguros",
   "desc": "¿Sanitas Students o Sanitas Residents? Te explico la diferencia, para qué visado sirve cada uno y cómo elegir el seguro de salud Sanitas correcto para tu trámite.",
   "h1": "Sanitas Students vs Sanitas Residents: cuál elegir para tu visado",
   "body": '''
<p>Si vas a solicitar un <strong>visado para España</strong> y te han hablado del seguro <strong>Sanitas</strong>, es normal que dudes entre sus dos modalidades para extranjeros: <strong>Sanitas Students</strong> y <strong>Sanitas Residents</strong>. No son lo mismo, y elegir mal puede costarte un rechazo o un visado retrasado. Aquí te lo explico claro.</p>

<h2>¿Qué es Sanitas Students?</h2>
<p><strong>Sanitas Students</strong> es la modalidad pensada para <strong>estudiantes internacionales</strong> que vienen a España con un visado de estudios. Cumple los requisitos que piden los consulados para el visado de estudiante (tipo D): cobertura médica completa, <strong>sin copagos ni carencias</strong>, válida durante todo el periodo de estudios y con asistencia en España.</p>
<p>Es la opción natural si vienes a un curso, una carrera, un máster o una estancia académica.</p>

<h2>¿Qué es Sanitas Residents?</h2>
<p><strong>Sanitas Residents</strong> está diseñado para quienes se establecen en España de forma más estable: <strong>residencia no lucrativa, residencia por reagrupación familiar, nómada digital</strong> o cualquier trámite de residencia que exija seguro médico privado. Ofrece una cobertura sanitaria amplia, sin copagos ni carencias, y válida para el periodo que dure tu autorización.</p>

<h2>Diferencias clave entre Students y Residents</h2>
<table class="tabla">
<tr><th></th><th>Sanitas Students</th><th>Sanitas Residents</th></tr>
<tr><td><strong>Para quién</strong></td><td>Estudiantes con visado de estudios</td><td>Residencia, reagrupación, nómada digital</td></tr>
<tr><td><strong>Trámite</strong></td><td>Visado de estudiante (tipo D)</td><td>Residencia y asimilados</td></tr>
<tr><td><strong>Sin copagos</strong></td><td>Sí</td><td>Sí</td></tr>
<tr><td><strong>Sin carencias</strong></td><td>Sí</td><td>Sí</td></tr>
<tr><td><strong>Vigencia</strong></td><td>Duración de los estudios</td><td>Duración de la residencia</td></tr>
</table>

<h2>¿Y si dudo? Te oriento según tu caso</h2>
<p>Cada trámite tiene sus matices y cada consulado aplica sus requisitos. Por eso, antes de contratar, conviene revisar <strong>qué visado vas a presentar y qué exige exactamente</strong>. Te ayudo a decidir entre Sanitas Students y Sanitas Residents para que la póliza encaje a la primera.</p>

<h2>¿Se puede contratar desde mi país?</h2>
<p>Sí. Tanto Sanitas Students como Sanitas Residents se pueden contratar <strong>a distancia antes de venir a España</strong>, pagando por tarjeta o transferencia. Recibes el certificado válido para presentar en tu solicitud de visado.</p>

<h2>Conclusión</h2>
<p>Si vienes a estudiar, probablemente tu opción es <strong>Sanitas Students</strong>. Si vas a residir, reagrupar a tu familia o venir como nómada digital, lo más habitual es <strong>Sanitas Residents</strong>. Ante la duda, pregúntame: te oriento gratis y sin compromiso.</p>
''',
   "faq": [
     ("¿Cuál es la diferencia entre Sanitas Students y Sanitas Residents?","Sanitas Students está pensado para estudiantes con visado de estudios y Sanitas Residents para residencia, reagrupación familiar o nómada digital. Ambos son sin copagos ni carencias."),
     ("¿Qué seguro Sanitas necesito para el visado de estudiante?","Sanitas Students: cobertura completa, sin copagos ni carencias y válido para todo el periodo de estudios."),
     ("¿Sanitas Residents sirve para la residencia no lucrativa?","Sí, es una de sus modalidades habituales. Te oriento según tu trámite y consulado."),
   ],
 },
 "seguro-sanitas-nomada-digital-espana": {
   "title": "Seguro Sanitas para nómada digital en España: requisitos y cómo contratarlo | CFG Seguros",
   "desc": "Qué seguro de salud Sanitas necesita un nómada digital para su residencia en España: requisitos, modalidad Residents y cómo contratarlo desde tu país.",
   "h1": "Seguro Sanitas para nómada digital en España: lo que necesitas",
   "body": '''
<p>España es uno de los destinos favoritos de los <strong>nómadas digitales</strong>. Si vas a solicitar la residencia como teletrabajador internacional, uno de los documentos obligatorios es el <strong>seguro médico privado</strong>. Aquí te explico qué pide el trámite y por qué <strong>Sanitas Residents</strong> es la modalidad que suele encajar.</p>

<h2>¿Qué seguro exige la residencia de nómada digital?</h2>
<p>La autorización de residencia para teletrabajadores exige, entre otros requisitos, un <strong>seguro de enfermedad con cobertura en España</strong> durante todo el periodo autorizado. Los consulados y la Oficina de Extranjería suelen pedir:</p>
<ul>
<li>Cobertura médica completa en España.</li>
<li><strong>Sin copagos ni carencias.</strong></li>
<li>Vigente durante toda la autorización.</li>
<li>Emitido por una aseguradora con solvencia.</li>
</ul>

<h2>Sanitas Residents: la modalidad adecuada</h2>
<p>Para el nómada digital, la modalidad que suele encajar es <strong>Sanitas Residents</strong>. Ofrece atención médica amplia en España, sin copagos ni carencias, y se adapta a la duración de tu autorización de residencia.</p>

<h2>¿Y si vengo con familia?</h2>
<p>Si tu autorización incluye a tu cónyuge o hijos, todos necesitan su propio seguro. Te gestiono las pólizas de toda la unidad familiar para que el expediente quede completo.</p>

<h2>¿Se puede contratar antes de llegar a España?</h2>
<p>Sí, y es lo recomendable. Contratas <strong>desde tu país</strong>, pagas por tarjeta o transferencia y recibes el certificado para presentar con tu solicitud. Así no tienes que hacer trámites a contrarreloj desde aquí.</p>

<h2>Ciudades con más demanda</h2>
<p>Los nómadas digitales se concentran sobre todo en <strong>Madrid, Barcelona, Valencia, Málaga, Alicante, Palma de Mallorca y las Islas Canarias</strong>. Da igual dónde te instales: la cobertura Sanitas es válida en toda España.</p>

<h2>Resumiendo</h2>
<p>Si eres nómada digital, apunta a <strong>Sanitas Residents</strong>, sin copagos ni carencias y válido para tu residencia. Si tienes dudas, te ayudo a elegir el producto exacto según tu caso.</p>
''',
   "faq": [
     ("¿Qué seguro necesita un nómada digital para residir en España?","Un seguro de salud con cobertura en España, sin copagos ni carencias y válido durante toda la autorización. Sanitas Residents es la modalidad habitual."),
     ("¿Puedo contratar el seguro Sanitas antes de llegar a España?","Sí, se contrata a distancia y recibes el certificado válido para tu solicitud de residencia antes de viajar."),
     ("¿Cubre a mi familia?","Cada miembro de la familia necesita su póliza. Te gestiono todas las de la unidad familiar."),
   ],
 },
 "seguro-salud-sanitas-visado-residencia-espana": {
   "title": "Seguro de salud Sanitas para el visado y la residencia en España | CFG Seguros",
   "desc": "Guía del seguro de salud Sanitas para el visado y la residencia en España: qué exige el consulado, qué es Sanitas Students y Sanitas Residents y cómo contratarlo.",
   "h1": "Seguro de salud Sanitas para el visado y la residencia en España",
   "body": '''
<p>Uno de los documentos que más problemas da en los trámites de <strong>visado y residencia en España</strong> es el <strong>seguro médico</strong>. Las autoridades exigen una póliza con cobertura completa, y si no cumple, tu expediente puede retrasarse o ser denegado. Aquí te explico qué pide y cómo resolverlo con <strong>Sanitas</strong>.</p>

<h2>¿Qué exige el consulado?</h2>
<p>Con carácter general, los consulados y la Oficina de Extranjería piden un seguro que reúna:</p>
<ul>
<li><strong>Cobertura médica completa</strong> (enfermedad y accidente).</li>
<li><strong>Sin copagos ni carencias.</strong></li>
<li><strong>Válido durante todo el periodo</strong> autorizado.</li>
<li><strong>Repatriación</strong> en algunos casos.</li>
<li>Emitido por una aseguradora con solvencia.</li>
</ul>

<h2>Las dos modalidades de Sanitas para extranjeros</h2>
<p>Según tu trámite, eliges una:</p>
<ul>
<li><strong>Sanitas Students</strong> → para el <strong>visado de estudios</strong> (estudiantes internacionales).</li>
<li><strong>Sanitas Residents</strong> → para <strong>residencia</strong>, reagrupación familiar y nómada digital.</li>
</ul>
<p>Ambas cumplen los requisitos habituales: cobertura completa, sin copagos ni carencias y válidas durante toda la estancia.</p>

<h2>El error que debes evitar</h2>
<p>Contratar un simple <strong>seguro de viaje</strong> pensando que vale. No ofrece la cobertura que exige el trámite y suele ser motivo de rechazo. Lo correcto es contratar un seguro <strong>específico para el visado</strong> y confirmar que cumple antes de presentar.</p>

<h2>¿Cómo lo gestiono yo por ti?</h2>
<p>Como <strong>agente exclusiva de Sanitas</strong>, te preparo el presupuesto, elijo contigo la modalidad correcta (Students o Residents) y te emito el <strong>certificado válido para tu visado</strong>, listo para presentar. Todo a distancia y con trato directo.</p>

<h2>¿Cuánto cuesta?</h2>
<p>Depende de tu edad, la duración y la modalidad. Es una inversión asumible comparada con el riesgo de quedarte sin cobertura o de que te devuelvan el expediente. Te doy presupuesto sin compromiso.</p>

<h2>Da el paso</h2>
<p>El trámite ya es bastante engorroso como para encima fallar con el seguro. Si necesitas la póliza correcta, lista antes de tu cita, <strong>te ayudo a conseguirla</strong> sin vueltas.</p>
''',
   "faq": [
     ("¿Qué seguro de salud piden para el visado y la residencia en España?","Un seguro con cobertura completa, sin copagos ni carencias y válido durante todo el periodo. Sanitas Students (estudios) y Sanitas Residents (residencia) cumplen estos requisitos."),
     ("¿Sirve un seguro de viaje para el visado?","No. Los seguros de viaje suelen no cumplir la cobertura exigida y son causa habitual de rechazo. Hay que usar un seguro específico para el visado."),
     ("¿Puedo contratarlo desde mi país?","Sí, se contrata a distancia y recibes el certificado antes de presentar tu solicitud."),
   ],
 },
}

if __name__ == "__main__":
    for slug, a in ARTICULOS.items():
        html = HEAD.format(title=a["title"], desc=a["desc"], slug=slug, h1=a["h1"], faq_schema=faq_schema(a["faq"]))
        html += a["body"] + "\n" + FOOT
        p = os.path.join(BLOG, slug + ".html")
        open(p, "w", encoding="utf-8").write(html)
        print("creado:", os.path.relpath(p, BASE), os.path.getsize(p), "bytes")
