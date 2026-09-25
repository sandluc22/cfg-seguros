#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera páginas SEO/GEO por ciudad para Sanitas (cfg-seguros.com).
Reutiliza head+style+footer de seguros/salud.html y cambia el contenido
con texto ÚNICO por ciudad (no duplicado)."""
import re, os

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "seguros", "salud.html")

src = open(SRC, encoding="utf-8").read()

# --- partir en 3 trozos: [0] hasta <body> , [1] contenido (HERO..CTA) , [2] footer+scripts
i_body = src.index("<body>")
i_hero = src.index("<!-- HERO -->")
i_cta_final_end = src.index("<footer>")
head = src[:i_hero]          # incluye head, style, <body>, <nav>
tail = src[i_cta_final_end:] # footer + wa + cookies + scripts

CIUDADES = {
    "madrid": {
        "ciudad": "Madrid", "region": "ES-MD", "coord": "40.416775;-3.703790", "icbm": "40.416775, -3.703790",
        "titulo": "Seguro de salud Sanitas para visado en Madrid | CFG Seguros",
        "desc": "Seguro de salud Sanitas para el visado en Madrid: estudiantes, residencia y nómada digital. Sin copagos ni carencias, contratación desde tu país. Agente exclusiva Sanitas.",
        "h1": "Seguro de salud <span>Sanitas</span> para el visado en Madrid",
        "sub": "Si tramitas tu visado de estudios, residencia o nómada digital en <strong>Madrid</strong>, necesitas un seguro médico que cumpla los requisitos. Sin copagos ni carencias y con gestión rápida desde tu país.",
        "intro": "Madrid es la ciudad de España que recibe más estudiantes internacionales, nómadas digitales y familias que llegan con visado de residencia. En la Comunidad de Madrid se concentran las principales universidades (Complutense, Politécnica, Carlos III, Autónoma) y la mayor oferta de consulados, lo que hace que la demanda de <strong>seguro médico para visado en Madrid</strong> sea constante durante todo el año.",
        "local": [
            ("🎓", "Estudiantes en Madrid", "Si vienes a estudiar a Madrid —Complutense, Politécnica, Carlos III o Autónoma— el seguro Sanitas cumple los requisitos del visado de estudios y del NIE."),
            ("🌍", "Residencia y reagrupación", "Para el visado de residencia no lucrativa o reagrupación familiar en Madrid, tu seguro debe cubrir toda la estancia sin carencias."),
            ("💻", "Nómada digital en Madrid", "Madrid es uno de los principales destinos de nómadas digitales en España. Te gestiono el seguro Sanitas válido para esa residencia."),
        ],
        "faq": [
            ("¿Qué seguro necesito para el visado de estudiante en Madrid?", "Un seguro sin copagos ni carencias, válido para todo el periodo de estudios y con repatriación. El seguro Sanitas que gestiono cumple los requisitos del consulado español y se contrata desde tu país antes de solicitar el visado."),
            ("¿Puedo contratarlo si aún no estoy en Madrid?", "Sí. Todo el proceso se hace a distancia: contratas desde tu país, pagas por tarjeta o transferencia y recibes el certificado válido para el visado antes de viajar a Madrid."),
            ("¿Cuánto tarda la emisión del certificado?", "Emito el presupuesto el mismo día y, una vez confirmado el pago, el certificado lo antes posible para no frenar tu expediente consular."),
        ],
    },
    "barcelona": {
        "ciudad": "Barcelona", "region": "ES-CT", "coord": "41.387400;2.168600", "icbm": "41.387400, 2.168600",
        "titulo": "Seguro de salud Sanitas para visado en Barcelona | CFG Seguros",
        "desc": "Seguro de salud Sanitas para el visado en Barcelona: estudiantes, residencia y nómada digital. Sin copagos ni carencias. Agente exclusiva Sanitas. Contratación desde tu país.",
        "h1": "Seguro de salud <span>Sanitas</span> para el visado en Barcelona",
        "sub": "Si tramitas tu visado de estudios, residencia o nómada digital en <strong>Barcelona</strong> o su área metropolitana, te gestiono el seguro Sanitas que cumple los requisitos, sin copagos ni carencias.",
        "intro": "Barcelona y su área metropolitana (L'Hospitalet, Badalona, Sabadell, Terrassa) son un destino clave para estudiantes internacionales y profesionales que llegan con visado de residencia. La ciudad concentra universidades como la UB, la UPC, la Pompeu Fabra y Esade, además del Consulado General, lo que genera una demanda constante de <strong>seguro médico para visado en Barcelona</strong>.",
        "local": [
            ("🎓", "Estudiantes en Barcelona", "Vengas a la UB, UPC, UPF, Esade o UAB, el seguro Sanitas cumple los requisitos del visado de estudios y sirve para el NIE."),
            ("🌍", "Residencia no lucrativa", "Para el visado de residencia en Barcelona, tu seguro debe cubrir toda la estancia sin copagos ni carencias, también para familiares."),
            ("💻", "Nómada digital en Barcelona", "Barcelona es uno de los hubs tecnológicos de Europa. Te gestiono el seguro Sanitas válido para el visado de nómada digital."),
        ],
        "faq": [
            ("¿Qué seguro piden para el visado de estudios en Barcelona?", "Un seguro médico sin copagos ni carencias, válido para todo el curso y con repatriación. El seguro Sanitas que gestiono lo cumple y se puede contratar desde tu país."),
            ("¿Sirve el mismo seguro para residencia y para estudios?", "No exactamente: cambian las condiciones y el producto (Students o Residents). Te oriento según tu trámite en el consulado de Barcelona."),
            ("¿Puedo contratar si todavía no estoy en España?", "Sí. Se contrata a distancia y el pago es por tarjeta o transferencia. Recibes el certificado antes de viajar."),
        ],
    },
    "valencia": {
        "ciudad": "Valencia", "region": "ES-VC", "coord": "39.469907;-0.376288", "icbm": "39.469907, -0.376288",
        "titulo": "Seguro de salud Sanitas para visado en Valencia | CFG Seguros",
        "desc": "Seguro de salud Sanitas para el visado en Valencia: estudiantes, residencia y nómada digital. Sin copagos ni carencias. Agente exclusiva Sanitas. Contratación desde tu país.",
        "h1": "Seguro de salud <span>Sanitas</span> para el visado en Valencia",
        "sub": "Si vas a tramitar tu visado de estudios, residencia o nómada digital en <strong>Valencia</strong>, te gestiono el seguro Sanitas que necesitas, sin copagos ni carencias y con emisión rápida.",
        "intro": "Valencia se ha convertido en una de las ciudades preferidas por estudiantes latinoamericanos y por quienes llegan con visado de residencia, gracias a su calidad de vida y a universidades como la Universitat de València y la UPV. La demanda de <strong>seguro médico para visado en Valencia</strong> crece cada año, tanto para estudios como para residencia y nómada digital.",
        "local": [
            ("🎓", "Estudiantes en Valencia", "Para la Universitat de València, la UPV o la CEU Cardenal Herrera, el seguro Sanitas es válido para el visado de estudios y el NIE."),
            ("🌍", "Residencia y reagrupación", "Muchas familias eligen Valencia para establecerse. Tu seguro para el visado de residencia cubre a todos los miembros sin carencias."),
            ("💻", "Nómada digital en Valencia", "Valencia es un destino emergente para el teletrabajo internacional. Te gestiono el seguro Sanitas para tu visado de nómada digital."),
        ],
        "faq": [
            ("¿Qué seguro de salud piden para el visado en Valencia?", "Un seguro sin copagos ni carencias, con cobertura completa y repatriación, válido para todo el periodo. El seguro Sanitas que gestiono cumple los requisitos."),
            ("¿Cuánto cuesta el seguro Sanitas para un estudiante en Valencia?", "Depende del tramo de edad y del producto. Te preparo un presupuesto personalizado sin compromiso."),
            ("¿Se puede contratar desde Colombia o México antes de venir?", "Sí. Se contrata a distancia, se paga por tarjeta o transferencia y recibes el certificado válido para el visado antes de viajar a Valencia."),
        ],
    },
    "malaga": {
        "ciudad": "Málaga", "region": "ES-AN", "coord": "36.721302;-4.421636", "icbm": "36.721302, -4.421636",
        "titulo": "Seguro de salud Sanitas para visado en Málaga | CFG Seguros",
        "desc": "Seguro de salud Sanitas para el visado en Málaga: estudiantes, residencia y nómada digital. Sin copagos ni carencias. Agente exclusiva Sanitas. Contratación desde tu país.",
        "h1": "Seguro de salud <span>Sanitas</span> para el visado en Málaga",
        "sub": "Málaga es uno de los mayores polos de nómadas digitales y residentes internacionales de España. Te gestiono el seguro Sanitas para tu visado, sin copagos ni carencias.",
        "intro": "Málaga y la Costa del Sol se han consolidado como uno de los principales destinos de nómadas digitales, residentes extranjeros y estudiantes internacionales del sur de España. La ciudad acoge la Universidad de Málaga y un ecosistema tecnológico en auge, lo que dispara la demanda de <strong>seguro médico para visado en Málaga</strong>, sobre todo para residencia y nómada digital.",
        "local": [
            ("💻", "Nómada digital en Málaga", "Málaga lidera el visado de nómada digital en España. Te gestiono el seguro Sanitas que exige la residencia para teletrabajadores."),
            ("🌍", "Residencia en la Costa del Sol", "Muchos residentes internacionales se instalan en Málaga y alrededores. Tu seguro cubre toda la estancia sin copagos ni carencias."),
            ("🎓", "Estudiantes en Málaga", "Para la Universidad de Málaga y otros centros, el seguro Sanitas cumple los requisitos del visado de estudios."),
        ],
        "faq": [
            ("¿Qué seguro necesito para el visado de nómada digital en Málaga?", "Un seguro médico sin copagos ni carencias y con cobertura completa durante la estancia. El seguro Sanitas que gestiono cumple los requisitos de la residencia por teletrabajo."),
            ("¿Sirve Sanitas para el visado de residencia en Málaga?", "Sí. Emito la póliza y el certificado válido para el expediente, listo para presentar en el consulado o en extranjería."),
            ("¿Cuánto tarda todo el proceso?", "Emito el presupuesto el mismo día y el certificado lo antes posible tras confirmar el pago, para no frenar tu expediente."),
        ],
    },
}

def seccion_local(c):
    cards = "\n".join(
        f'''      <div class="card">
        <div class="emoji">{e}</div>
        <h3>{h}</h3>
        <p>{p}</p>
      </div>''' for (e,h,p) in c["local"])
    return f'''<section class="bloque aparte">
  <div class="container">
    <h2>¿Para quién es el seguro Sanitas en {c["ciudad"]}?</h2>
    <p class="lead">Dependiendo de tu trámite, necesitas un producto u otro. Te oriento según tu caso.</p>
    <div class="grid">
{cards}
    </div>
  </div>
</section>'''

def seccion_faq(c):
    items = "\n".join(
        f'''      <div class="card">
        <h3>{q}</h3>
        <p>{a}</p>
      </div>''' for (q,a) in c["faq"])
    return f'''<section class="bloque">
  <div class="container">
    <h2>Preguntas frecuentes · seguro Sanitas en {c["ciudad"]}</h2>
    <div class="grid">
{items}
    </div>
  </div>
</section>'''

def faq_schema(c):
    ent = ",\n".join(
        f'''    {{
      "@type": "Question",
      "name": "{q}",
      "acceptedAnswer": {{ "@type": "Answer", "text": "{a}" }}
    }}''' for (q,a) in c["faq"])
    return f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
{ent}
  ]
}}
</script>'''

def build(slug, c):
    # --- HEAD: cambiar title, description, meta geo y canonical/og ---
    h = head
    h = re.sub(r'<title>.*?</title>', f'<title>{c["titulo"]}</title>', h, count=1)
    h = re.sub(r'<meta name="description" content="[^"]*">',
               f'<meta name="description" content="{c["desc"]}">', h, count=1)
    # geo metas
    h = re.sub(r'<meta name="geo\.region" content="[^"]*">', f'<meta name="geo.region" content="{c["region"]}">', h)
    h = re.sub(r'<meta name="geo\.placename" content="[^"]*">', f'<meta name="geo.placename" content="{c["ciudad"]}">', h)
    h = re.sub(r'<meta name="geo\.position" content="[^"]*">', f'<meta name="geo.position" content="{c["coord"]}">', h)
    h = re.sub(r'<meta name="ICBM" content="[^"]*">', f'<meta name="ICBM" content="{c["icbm"]}">', h)
    # canonical / og url
    url = f'https://cfg-seguros.com/seguros/salud-{slug}'
    h = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', h)
    h = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">', h)
    h = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{c["titulo"].split(" | ")[0]}">', h, count=1)
    h = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{c["desc"]}">', h, count=1)
    # quitar el HealthInsurance+FAQ viejo y meter el FAQ nuevo antes de </head>
    h = re.sub(r'<script type="application/ld\+json">.*?</script>\s*</head>', faq_schema(c) + "\n</head>", h, count=1, flags=re.S)

    # --- HERO con h1/sub de la ciudad ---
    hero = f'''<!-- HERO -->
<header class="hero">
  <div class="container">
    <span class="badge">Agente exclusiva Sanitas</span>
    <h1>{c["h1"]}</h1>
    <p class="sub">{c["sub"]}</p>
    <a href="#contacto" class="cta">Solicitar información →</a>
    <p class="contacto">📱 <a href="tel:+34641754490">+34 641 754 490</a> · ✉️ <a href="mailto:slcaicedo.agenteexclusivo@sanitas.es">slcaicedo.agenteexclusivo@sanitas.es</a></p>
  </div>
</header>'''

    # --- INTRO + LOCAL + FAQ ---
    cuerpo = f'''<section class="bloque">
  <div class="container">
    <h2>Seguro médico para visado en {c["ciudad"]}</h2>
    <p style="max-width:820px;margin:0 auto 1rem;color:#334155;line-height:1.7">{c["intro"]}</p>
    <p style="max-width:820px;margin:0 auto;color:#334155;line-height:1.7">Trabajo con <strong>Sanitas</strong>, la aseguradora líder en sanidad privada en España. Te gestiono la póliza y el <strong>certificado válido para tu visado</strong>, con trato directo y sin intermediarios.</p>
  </div>
</section>
{seccion_local(c)}
{seccion_faq(c)}'''

    # --- CTA final (reutilizo el de salud.html adaptando texto) ---
    cta = f'''<!-- CTA FINAL -->
<section class="ctafinal" id="contacto">
  <div class="container">
    <h2>Solicita tu seguro Sanitas para {c["ciudad"]}</h2>
    <p>Presupuesto sin compromiso · Emisión rápida · Sin copagos ni carencias</p>
    <div class="btns">
      <a class="wa" href="https://api.whatsapp.com/send?phone=34641754490&text=Hola!%20Quiero%20informaci%C3%B3n%20sobre%20el%20seguro%20Sanitas%20para%20{c["ciudad"]}" target="_blank" rel="noopener">💬 WhatsApp</a>
      <a class="mail" href="mailto:slcaicedo.agenteexclusivo@sanitas.es">✉️ Escribir correo</a>
    </div>
  </div>
</section>'''

    out = h + "\n" + hero + "\n" + cuerpo + "\n" + cta + "\n" + tail
    path = os.path.join(BASE, "seguros", f"salud-{slug}.html")
    open(path, "w", encoding="utf-8").write(out)
    return path

for slug, c in CIUDADES.items():
    p = build(slug, c)
    print("creado:", os.path.relpath(p, BASE), os.path.getsize(p), "bytes")
