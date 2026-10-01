#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Anade FAQ + schema GEO (FAQPage + InsuranceAgency) a las landings que ya
   existian: estudiantes, extranjeros, mayores-65. Inserta la seccion FAQ antes
   del bloque <section id="contacto"> y el schema antes de </head>."""
import re, json

BASE = "/home/node/workspace/cfg-seguros"

EXTRA_CSS = """<style>
.faq-sec{background:#fff;border-radius:18px;padding:2rem;margin:1rem 0}
.faq-sec h2{font-size:1.5rem;color:#0a2a4a;margin-bottom:1rem}
.faq-item{border-bottom:1px solid #e2e8f0;padding:1rem 0}
.faq-item:last-child{border-bottom:0}
.faq-item h3{font-size:1.05rem;color:#0a2a4a;margin-bottom:.4rem}
.faq-item p{color:#334155;font-size:.95rem}
</style>
"""

def schema_block(faqs, nombre, slug):
    faqpage = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]
    }
    agency = {
        "@context": "https://schema.org",
        "@type": "InsuranceAgency",
        "name": "CFG Seguros - Agente Exclusiva Sanitas",
        "url": f"https://cfg-seguros.com/{slug}/",
        "telephone": "+34641754490",
        "email": "slcaicedo.agenteexclusivo@sanitas.es",
        "areaServed": {"@type": "Country", "name": "España"},
        "address": {"@type": "PostalAddress", "streetAddress": "Avenida de Jaca, 14",
                    "addressLocality": "Madrid", "postalCode": "28022", "addressCountry": "ES"},
        "brand": {"@type": "Brand", "name": "Sanitas"},
        "description": nombre
    }
    return ('<script type="application/ld+json">\n' + json.dumps(faqpage, ensure_ascii=False, indent=1)
            + '\n</script>\n<script type="application/ld+json">\n'
            + json.dumps(agency, ensure_ascii=False, indent=1) + '\n</script>\n')

def faq_html(faqs):
    return "\n    ".join(f'<div class="faq-item"><h3>{q}</h3><p>{a}</p></div>' for q, a in faqs)

PAGES = {
    "estudiantes/index.html": {
        "slug": "estudiantes",
        "nombre": "Seguro médico Sanitas para estudiantes en España",
        "faqs": [
            ("¿Qué seguro médico necesito para el visado de estudios en España?",
             "Para el visado de estudios en España necesitas un seguro médico con cobertura completa, sin copagos y válido durante toda tu estancia. El seguro Sanitas para estudiantes cumple estos requisitos y es apto para presentar en el consulado."),
            ("¿El seguro Sanitas para estudiantes vale para el visado?",
             "Sí. El seguro médico Sanitas para estudiantes está diseñado para cumplir los requisitos del visado de estudios y residencia en España: cobertura completa, sin copagos y sin carencias."),
            ("¿Cuánto cuesta el seguro de salud para estudiantes en España?",
             "El precio depende de la edad y la duración de la estancia. Te calculamos el precio exacto sin compromiso con tus datos, y puedes contratarlo desde el primer día."),
            ("¿El seguro para estudiantes incluye cobertura dental?",
             "Sí. La póliza de estudiantes de Sanitas incluye cobertura dental además de asistencia médica completa, urgencias y especialistas sin listas de espera."),
            ("¿Puedo contratar el seguro desde mi país antes de llegar a España?",
             "Sí. Puedes contratar tu seguro Sanitas antes de viajar a España, con lo que llegarás con la cobertura activa desde el primer día y podrás usarlo para el trámite del visado."),
        ],
    },
    "extranjeros/index.html": {
        "slug": "extranjeros",
        "nombre": "Seguro médico Sanitas para extranjeros en España",
        "faqs": [
            ("¿Qué seguro médico necesito como extranjero en España?",
             "Como extranjero en España necesitas un seguro médico privado con cobertura completa que te dé acceso a la sanidad sin depender de la Seguridad Social. El seguro Sanitas para extranjeros incluye cobertura desde el primer día y atención en varios idiomas."),
            ("¿El seguro Sanitas sirve para el visado de residencia?",
             "Sí. El seguro médico Sanitas cumple los requisitos de cobertura exigidos para el visado y la residencia en España: cobertura completa, sin copagos y sin periodos de carencia."),
            ("¿Cuánto cuesta el seguro de salud para extranjeros en España?",
             "El precio depende de la edad y de la duración de la estancia. Te preparamos un presupuesto personalizado sin compromiso y te gestionamos toda la póliza."),
            ("¿El seguro incluye atención en mi idioma?",
             "Sí. Sanitas ofrece atención en varios idiomas y una amplia red de hospitales y especialistas en toda España, sin listas de espera."),
            ("¿Puedo contratar el seguro si llego a España por reagrupación familiar o nómada digital?",
             "Sí. Hay pólizas Sanitas adaptadas a cada situación: reagrupación familiar, nómada digital, residencia no lucrativa y otras. Cuéntanos tu caso y te indicamos la mejor opción."),
        ],
    },
    "mayores-65/index.html": {
        "slug": "mayores-65",
        "nombre": "Seguro médico Sanitas para mayores de 65 en España",
        "faqs": [
            ("¿Puedo contratar un seguro de salud Sanitas con más de 65 años?",
             "Sí. Sanitas ofrece seguros de salud para mayores de 65 años, sin edad máxima de permanencia, con cobertura médica completa y acceso a especialistas sin listas de espera."),
            ("¿Cuánto cuesta el seguro de salud para mayores de 65 años?",
             "El precio depende de la edad y del tipo de cobertura. Te calculamos el precio exacto sin compromiso y te gestionamos toda la póliza de principio a fin."),
            ("¿El seguro para mayores de 65 años incluye hospitalización?",
             "Sí. Incluye cobertura completa: consultas, pruebas diagnósticas, hospitalización, cirugía y urgencias en la red de hospitales Sanitas."),
            ("¿Hay copagos en el seguro de salud para mayores de 65 años?",
             "Las pólizas Sanitas para mayores de 65 se pueden contratar sin copagos, pagando solo la prima mensual sin cantidades adicionales por cada visita."),
            ("¿Necesito pasar un reconocimiento médico para contratar el seguro?",
             "No siempre. Te informamos de los requisitos según tu edad y situación al prepararte el presupuesto personalizado."),
        ],
    },
}

for path, data in PAGES.items():
    full = f"{BASE}/{path}"
    with open(full, "r", encoding="utf-8") as f:
        html = f.read()

    if 'class="faq-sec"' in html:
        print(f"SKIP {path} (ya tiene FAQ)")
        continue

    # 1) insertar CSS justo antes de </style> (bloque extra)
    html = html.replace("</style>\n</head>", EXTRA_CSS + "</head>", 1)
    # 2) insertar schema justo antes de </head>
    html = html.replace("</head>", schema_block(data["faqs"], data["nombre"], data["slug"]) + "</head>", 1)
    # 3) insertar seccion FAQ antes de <section id="contacto"
    sec = ('<section class="faq-sec">\n    <h2>Preguntas frecuentes</h2>\n    '
           + faq_html(data["faqs"]) + '\n  </section>\n\n  <section id="contacto"')
    html = html.replace('<section id="contacto"', sec, 1)

    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"OK {path} -> FAQ+schema anadidos")
