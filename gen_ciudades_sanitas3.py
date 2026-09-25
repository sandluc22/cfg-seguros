#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LOTE 3 SEO/GEO Sanitas — resto de capitales. Reutiliza head de salud.html.
Usa terminologia Sanitas Students / Sanitas Residents."""
import re, os

BASE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(BASE, "seguros", "salud.html"), encoding="utf-8").read()
head = src[:src.index("<!-- HERO -->")]
tail = src[src.index("<footer>"):]

CIUDADES = {
 "santander": ("Santander","ES-CB","43.462306;-3.809980","43.462306, -3.809980"),
 "vigo": ("Vigo","ES-GA","42.240599;-8.720727","42.240599, -8.720727"),
 "gijon": ("Gijón","ES-AS","43.532201;-5.661119","43.532201, -5.661119"),
 "salamanca": ("Salamanca","ES-CL","40.970104;-5.663540","40.970104, -5.663540"),
 "logrono": ("Logroño","ES-RI","42.462719;-2.444985","42.462719, -2.444985"),
 "badajoz": ("Badajoz","ES-EX","38.879449;-6.970654","38.879449, -6.970654"),
 "cadiz": ("Cádiz","ES-AN","36.527061;-6.288596","36.527061, -6.288596"),
 "almeria": ("Almería","ES-AN","36.838125;-2.459740","36.838125, -2.459740"),
 "pamplona": ("Pamplona","ES-NC","42.812526;-1.645774","42.812526, -1.645774"),
 "san-sebastian": ("San Sebastián","ES-PV","43.318334;-1.981231","43.318334, -1.981231"),
 "burgos": ("Burgos","ES-CL","42.343993;-3.696906","42.343993, -3.696906"),
 "tarragona": ("Tarragona","ES-CT","41.118882;1.244490","41.118882, 1.244490"),
 "lleida": ("Lleida","ES-CT","41.617313;0.620015","41.617313, 0.620015"),
 "girona": ("Girona","ES-CT","41.979301;2.821426","41.979301, 2.821426"),
 "castellon": ("Castellón","ES-VC","39.986014;-0.037637","39.986014, -0.037637"),
 "huelva": ("Huelva","ES-AN","37.261421;-6.944722","37.261421, -6.944722"),
 "jaen": ("Jaén","ES-AN","37.779594;-3.784906","37.779594, -3.784906"),
 "albacete": ("Albacete","ES-CM","38.994349;-1.858542","38.994349, -1.858542"),
 "leon": ("León","ES-CL","42.598726;-5.567096","42.598726, -5.567096"),
 "oviedo": ("Oviedo","ES-AS","43.361914;-5.849389","43.361914, -5.849389"),
 "ourense": ("Ourense","ES-GA","42.335789;-7.863880","42.335789, -7.863880"),
 "lugo": ("Lugo","ES-GA","43.012089;-7.555851","43.012089, -7.555851"),
 "santiago": ("Santiago de Compostela","ES-GA","42.878213;-8.544844","42.878213, -8.544844"),
 "ceuta": ("Ceuta","ES-CE","35.889387;-5.321346","35.889387, -5.321346"),
 "melilla": ("Melilla","ES-ML","35.293660;-2.938206","35.293660, -2.938206"),
}

TITULOS = {
 "santander": "Cantabria", "vigo": "Vigo y Galicia", "gijon": "Asturias",
 "salamanca": "Castilla y León", "logrono": "La Rioja", "badajoz": "Extremadura",
 "cadiz": "Cádiz y la Bahía", "almeria": "Almería", "pamplona": "Navarra",
 "san-sebastian": "el País Vasco", "burgos": "Burgos", "tarragona": "Tarragona",
 "lleida": "Lleida", "girona": "Girona", "castellon": "Castellón",
 "huelva": "Huelva", "jaen": "Jaén", "albacete": "Castilla-La Mancha",
 "leon": "León", "oviedo": "Oviedo y Asturias", "ourense": "Ourense",
 "lugo": "Lugo", "santiago": "Santiago", "ceuta": "Ceuta", "melilla": "Melilla",
}
PERFIL = {
 "santander": "la Universidad de Cantabria y un entorno residencial atractivo",
 "vigo": "la Universidade de Vigo y su potente sector industrial y portuario",
 "gijon": "la Universidad de Oviedo y su creciente comunidad internacional",
 "salamanca": "la Universidad de Salamanca, referente para estudiantes internacionales",
 "logrono": "la Universidad de La Rioja y una comunidad extranjera en crecimiento",
 "badajoz": "la Universidad de Extremadura y su cercanía a Portugal",
 "cadiz": "la Universidad de Cádiz y una gran comunidad latinoamericana",
 "almeria": "la Universidad de Almería y su dinámico sector agrícola y tecnológico",
 "pamplona": "la Universidad de Navarra y la UPNA, con mucho alumnado internacional",
 "san-sebastian": "la UPV/EHU y la Universidad de Deusto, con alta presencia internacional",
 "burgos": "la Universidad de Burgos y su tejido industrial",
 "tarragona": "la Universitat Rovira i Virgili y su comunidad internacional",
 "lleida": "la Universitat de Lleida y su creciente alumnado extranjero",
 "girona": "la Universitat de Girona y su entorno internacional",
 "castellon": "la Universitat Jaume I y su comunidad estudiantil internacional",
 "huelva": "la Universidad de Huelva y su comunidad latinoamericana",
 "jaen": "la Universidad de Jaén y su alumnado internacional",
 "albacete": "la Universidad de Castilla-La Mancha y su comunidad extranjera",
 "leon": "la Universidad de León y su alumnado internacional",
 "oviedo": "la Universidad de Oviedo y su comunidad internacional",
 "ourense": "la Universidade de Vigo y su creciente alumnado extranjero",
 "lugo": "la Universidade de Santiago y su entorno internacional",
 "santiago": "la Universidade de Santiago de Compostela, muy atractiva para estudiantes extranjeros",
 "ceuta": "la Universidad de Granada en Ceuta y su situación fronteriza única",
 "melilla": "la Universidad de Granada en Melilla y su posición estratégica",
}

def faq(c, zona):
    return [
        ("¿Qué seguro de salud necesito para el visado en %s?" % c,
         "Un seguro sin copagos ni carencias, con repatriación y válido para todo el periodo. Gestiono el seguro Sanitas que cumple los requisitos del consulado, tanto en la modalidad Sanitas Students como Sanitas Residents."),
        ("¿Sanitas Students o Sanitas Residents: cuál elijo para mi visado en %s?" % c,
         "Sanitas Students está pensado para estudiantes y Sanitas Residents para quienes tramitan residencia o nómada digital. Te oriento según tu caso y el trámite que vayas a presentar."),
        ("¿Puedo contratar el seguro Sanitas desde mi país antes de venir a %s?" % c,
         "Sí. Se contrata a distancia, se paga con tarjeta o transferencia y recibes el certificado válido para el visado antes de viajar."),
        ("¿Cuánto cuesta el seguro Sanitas para el visado en %s?" % c,
         "Depende del tramo de edad y del producto contratado. Te preparo un presupuesto personalizado y sin compromiso."),
    ]

def build(slug, datos):
    c, region, coord, icbm = datos
    zona = TITULOS[slug]; perfil = PERFIL[slug]
    titulo = "Seguro de salud Sanitas para visado en %s (Students y Residents) | CFG Seguros" % c
    desc = "Seguro de salud Sanitas para el visado en %s: Sanitas Students y Sanitas Residents. Sin copagos ni carencias. Agente exclusiva Sanitas." % c
    h = head
    h = re.sub(r'<title>.*?</title>', '<title>%s</title>' % titulo, h, count=1)
    h = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % desc, h, count=1)
    h = re.sub(r'<meta name="geo\.region" content="[^"]*">', '<meta name="geo.region" content="%s">' % region, h)
    h = re.sub(r'<meta name="geo\.placename" content="[^"]*">', '<meta name="geo.placename" content="%s">' % c, h)
    h = re.sub(r'<meta name="geo\.position" content="[^"]*">', '<meta name="geo.position" content="%s">' % coord, h)
    h = re.sub(r'<meta name="ICBM" content="[^"]*">', '<meta name="ICBM" content="%s">' % icbm, h)
    url = "https://cfg-seguros.com/seguros/salud-%s" % slug
    h = re.sub(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="%s">' % url, h)
    h = re.sub(r'<meta property="og:url" content="[^"]*">', '<meta property="og:url" content="%s">' % url, h)
    h = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="Seguro de salud Sanitas para visado en %s">' % c, h, count=1)
    h = re.sub(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="%s">' % desc, h, count=1)
    # quitar TODOS los json-ld y dejar el FAQ propio
    h = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', '', h, flags=re.S)
    faq_data = faq(c, zona)
    ent = ",\n".join('    {"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}' % (q,a) for q,a in faq_data)
    schema = '<script type="application/ld+json">\n{\n  "@context":"https://schema.org",\n  "@type":"FAQPage",\n  "mainEntity":[\n%s\n  ]\n}\n</script>' % ent
    h = h.replace("</head>", schema + "\n</head>", 1)

    hero = '''<!-- HERO -->
<header class="hero">
  <div class="container">
    <span class="badge">Agente exclusiva Sanitas</span>
    <h1>Seguro de salud <span>Sanitas</span> para el visado en %s</h1>
    <p class="sub">Sanitas <strong>Students</strong> y Sanitas <strong>Residents</strong>. Si tramitas tu visado en <strong>%s</strong>, te gestiono el seguro que cumple los requisitos, sin copagos ni carencias.</p>
    <a href="#contacto" class="cta">Solicitar información →</a>
    <p class="contacto">📱 <a href="tel:+34641754490">+34 641 754 490</a> · ✉️ <a href="mailto:slcaicedo.agenteexclusivo@sanitas.es">slcaicedo.agenteexclusivo@sanitas.es</a></p>
  </div>
</header>''' % (c, c)

    cuerpo = '''<section class="bloque">
  <div class="container">
    <h2>Seguro médico para visado en %(c)s</h2>
    <p style="max-width:820px;margin:0 auto 1rem;color:#334155;line-height:1.7">%(c)s cuenta con %(perfil)s. Por eso la demanda de <strong>seguro médico para visado en %(c)s</strong> es constante durante todo el curso.</p>
    <p style="max-width:820px;margin:0 auto;color:#334155;line-height:1.7">Trabajo con <strong>Sanitas</strong>, la aseguradora líder en sanidad privada en España. Te gestiono la póliza y el <strong>certificado válido para tu visado</strong>, escogiendo entre <strong>Sanitas Students</strong> y <strong>Sanitas Residents</strong> según tu trámite, con trato directo y sin intermediarios.</p>
  </div>
</section>
<section class="bloque aparte">
  <div class="container">
    <h2>¿Para quién es el seguro Sanitas en %(c)s?</h2>
    <p class="lead">Según tu trámite necesitas Sanitas Students o Sanitas Residents. Te oriento según tu caso.</p>
    <div class="grid">
      <div class="card"><div class="emoji">🎓</div><h3>Sanitas Students en %(c)s</h3><p>Para el visado de estudios: sin copagos ni carencias, válido para todo el curso y con el NIE.</p></div>
      <div class="card"><div class="emoji">🌍</div><h3>Sanitas Residents en %(c)s</h3><p>Para residencia, reagrupación familiar o nómada digital. Cubre toda la estancia sin carencias.</p></div>
      <div class="card"><div class="emoji">💻</div><h3>Nómada digital en %(c)s</h3><p>Te gestiono el seguro Sanitas válido para la residencia de teletrabajadores internacionales.</p></div>
    </div>
  </div>
</section>
<section class="bloque">
  <div class="container">
    <h2>Preguntas frecuentes · seguro Sanitas en %(c)s</h2>
    <div class="grid">
      <div class="card"><h3>%(q1)s</h3><p>%(a1)s</p></div>
      <div class="card"><h3>%(q2)s</h3><p>%(a2)s</p></div>
      <div class="card"><h3>%(q3)s</h3><p>%(a3)s</p></div>
      <div class="card"><h3>%(q4)s</h3><p>%(a4)s</p></div>
    </div>
  </div>
</section>''' % {"c": c, "perfil": perfil, "q1": faq_data[0][0], "a1": faq_data[0][1], "q2": faq_data[1][0], "a2": faq_data[1][1], "q3": faq_data[2][0], "a3": faq_data[2][1], "q4": faq_data[3][0], "a4": faq_data[3][1]}

    cta = '''<!-- CTA FINAL -->
<section class="ctafinal" id="contacto">
  <div class="container">
    <h2>Solicita tu seguro Sanitas para %s</h2>
    <p>Sanitas Students y Residents · Sin copagos ni carencias · Emisión rápida</p>
    <div class="btns">
      <a class="wa" href="https://api.whatsapp.com/send?phone=34641754490&text=Hola!%%20Quiero%%20informaci%%C3%%B3n%%20sobre%%20el%%20seguro%%20Sanitas%%20para%%20%s" target="_blank" rel="noopener">💬 WhatsApp</a>
      <a class="mail" href="mailto:slcaicedo.agenteexclusivo@sanitas.es">✉️ Escribir correo</a>
    </div>
  </div>
</section>''' % (c, c.replace(" ", "%20"))

    out = h + "\n" + hero + "\n" + cuerpo + "\n" + cta + "\n" + tail
    path = os.path.join(BASE, "seguros", "salud-%s.html" % slug)
    open(path, "w", encoding="utf-8").write(out)
    return path

if __name__ == "__main__":
    for slug, datos in CIUDADES.items():
        p = build(slug, datos)
        print("creado:", os.path.relpath(p, BASE), os.path.getsize(p))
