#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera páginas SEO/GEO por ciudad para Sanitas — LOTE 2 (resto de capitales).
Reutiliza head+style+footer de seguros/salud.html y añade contenido ÚNICO por ciudad."""
import re, os

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "seguros", "salud.html")
src = open(SRC, encoding="utf-8").read()
i_hero = src.index("<!-- HERO -->")
i_cta = src.index("<!-- CTA FINAL -->") if "<!-- CTA FINAL -->" in src else src.index("<footer>")
head = src[:i_hero]
tail = src[src.index("<footer>"):]

CIUDADES = {
    "sevilla": {
        "ciudad": "Sevilla", "region": "ES-AN", "coord": "37.389092;-5.984459", "icbm": "37.389092, -5.984459",
        "titulo": "Seguro de salud Sanitas para visado en Sevilla | CFG Seguros",
        "desc": "Seguro de salud Sanitas para el visado en Sevilla: estudiantes, residencia y nómada digital. Sin copagos ni carencias. Agente exclusiva Sanitas.",
        "h1": "Seguro de salud <span>Sanitas</span> para el visado en Sevilla",
        "sub": "Si tramitas tu visado de estudios, residencia o nómada digital en <strong>Sevilla</strong>, te gestiono el seguro Sanitas que cumple los requisitos, sin copagos ni carencias.",
        "intro": "Sevilla es una de las ciudades andaluzas con mayor presencia de estudiantes internacionales y familias que llegan con visado de residencia. La Universidad de Sevilla y la Pablo de Olavide atraen cada año a miles de alumnos extranjeros, lo que genera una demanda constante de <strong>seguro médico para visado en Sevilla</strong>.",
        "local": [
            ("🎓", "Estudiantes en Sevilla", "Para la Universidad de Sevilla o la Pablo de Olavide, el seguro Sanitas es válido para el visado de estudios y el NIE."),
            ("🌍", "Residencia y reagrupación", "Muchas familias latinoamericanas se establecen en Sevilla. Tu seguro para el visado cubre a todos sin carencias."),
            ("💻", "Nómada digital en Sevilla", "Sevilla gana adeptos entre teletrabajadores internacionales. Te gestiono el seguro Sanitas válido para tu residencia."),
        ],
        "faq": [
            ("¿Qué seguro de salud necesito para el visado en Sevilla?", "Un seguro sin copagos ni carencias, con repatriación y válido para todo el periodo. El seguro Sanitas que gestiono cumple los requisitos del consulado."),
            ("¿Se puede contratar desde América antes de venir a Sevilla?", "Sí. Se contrata a distancia, se paga por tarjeta o transferencia y recibes el certificado válido para el visado antes de viajar."),
            ("¿Cuánto cuesta el seguro Sanitas para un estudiante en Sevilla?", "Depende del tramo de edad y del producto. Te preparo un presupuesto personalizado sin compromiso."),
        ],
    },
    "zaragoza": {
        "ciudad": "Zaragoza", "region": "ES-AR", "coord": "41.648823;-0.889085", "icbm": "41.648823, -0.889085",
        "titulo": "Seguro de salud Sanitas para visado en Zaragoza | CFG Seguros",
        "desc": "Seguro de salud Sanitas para el visado en Zaragoza: estudiantes, residencia y nómada digital. Sin copagos ni carencias. Agente exclusiva Sanitas.",
        "h1": "Seguro de salud <span>Sanitas</span> para el visado en Zaragoza",
        "sub": "Si tramitas tu visado de estudios, residencia o nómada digital en <strong>Zaragoza</strong>, te gestiono el seguro Sanitas que necesitas, sin copagos ni carencias.",
        "intro": "Zaragoza, situada a medio camino entre Madrid y Barcelona, es una ciudad con una comunidad universitaria creciente y un número importante de residentes extranjeros, especialmente latinoamericanos. La demanda de <strong>seguro médico para visado en Zaragoza</strong> ha crecido con la llegada de estudiantes y familias.",
        "local": [
            ("🎓", "Estudiantes en Zaragoza", "Para la Universidad de Zaragoza, el seguro Sanitas cumple los requisitos del visado de estudios."),
            ("🌍", "Residencia y trabajo", "Si llegas a Zaragoza con visado de residencia, tu seguro cubre toda la estancia sin carencias."),
            ("💻", "Nómada digital en Zaragoza", "Te gestiono el seguro Sanitas válido para la residencia de teletrabajadores internacionales."),
        ],
        "faq": [
            ("¿Qué seguro necesito para el visado de estudiante en Zaragoza?", "Un seguro sin copagos ni carencias, válido para todo el curso y con repatriación. El seguro Sanitas que gestiono cumple los requisitos."),
            ("¿Puedo contratarlo si aún no estoy en España?", "Sí. Se contrata a distancia y recibes el certificado antes de viajar a Zaragoza."),
            ("¿Cuánto tarda la emisión del certificado?", "Emito el presupuesto el mismo día y el certificado lo antes posible tras el pago."),
        ],
    },
    "bilbao": {
        "ciudad": "Bilbao", "region": "ES-PV", "coord": "43.263012;-2.934985", "icbm": "43.263012, -2.934985",
        "titulo": "Seguro de salud Sanitas para visado en Bilbao | CFG Seguros",
        "desc": "Seguro de salud Sanitas para el visado en Bilbao: estudiantes, residencia y nómada digital. Sin copagos ni carencias. Agente exclusiva Sanitas.",
        "h1": "Seguro de salud <span>Sanitas</span> para el visado en Bilbao",
        "sub": "Si tramitas tu visado de estudios, residencia o nómada digital en <strong>Bilbao</strong> y el País Vasco, te gestiono el seguro Sanitas que cumple los requisitos.",
        "intro": "Bilbao y el País Vasco atraen a profesionales internacionales, estudiantes de posgrado y familias que llegan con visado de residencia. La Universidad del País Vasco y la Universidad de Deusto concentran buena parte de esa demanda de <strong>seguro médico para visado en Bilbao</strong>.",
        "local": [
            ("🎓", "Estudiantes en Bilbao", "Para la UPV/EHU o Deusto, el seguro Sanitas es válido para el visado de estudios."),
            ("🌍", "Residencia y profesiones", "Bilbao recibe profesionales que llegan con visado de residencia. Tu seguro cubre toda la estancia sin carencias."),
            ("💻", "Nómada digital en Bilbao", "Te gestiono el seguro Sanitas válido para la residencia de teletrabajadores."),
        ],
        "faq": [
            ("¿Qué seguro de salud piden para el visado en Bilbao?", "Un seguro sin copagos ni carencias y con repatriación. El seguro Sanitas que gestiono cumple los requisitos del consulado."),
            ("¿Sirve para residencia y para estudios?", "Cambian las condiciones según el trámite (Students o Residents). Te oriento según tu caso."),
            ("¿Se puede contratar desde el extranjero?", "Sí, a distancia, con pago por tarjeta o transferencia y certificado antes de viajar."),
        ],
    },
    "murcia": {
        "ciudad": "Murcia", "region": "ES-MC", "coord": "37.992240;-1.130654", "icbm": "37.992240, -1.130654",
        "titulo": "Seguro de salud Sanitas para visado en Murcia | CFG Seguros",
        "desc": "Seguro de salud Sanitas para el visado en Murcia: estudiantes, residencia y nómada digital. Sin copagos ni carencias. Agente exclusiva Sanitas.",
        "h1": "Seguro de salud <span>Sanitas</span> para el visado en Murcia",
        "sub": "Si tramitas tu visado en <strong>Murcia</strong> —estudios, residencia o nómada digital—, te gestiono el seguro Sanitas sin copagos ni carencias.",
        "intro": "Murcia es una región con una comunidad latinoamericana muy asentada y una universidad (la Universidad de Murcia y la UPCT) que recibe estudiantes internacionales. La demanda de <strong>seguro médico para visado en Murcia</strong> se mantiene estable todo el año.",
        "local": [
            ("🎓", "Estudiantes en Murcia", "Para la Universidad de Murcia o la UPCT, el seguro Sanitas es válido para el visado de estudios."),
            ("🌍", "Residencia y familia", "Murcia acoge a muchas familias que llegan con visado de residencia o reagrupación. Tu seguro cubre a todos."),
            ("💻", "Nómada digital en Murcia", "Te gestiono el seguro Sanitas válido para la residencia de teletrabajadores internacionales."),
        ],
        "faq": [
            ("¿Qué seguro necesito para el visado en Murcia?", "Un seguro sin copagos ni carencias, con repatriación y válido para todo el periodo. El seguro Sanitas que gestiono lo cumple."),
            ("¿Puedo contratarlo desde mi país?", "Sí. Se contrata a distancia y recibes el certificado válido para el visado antes de viajar."),
            ("¿Cuánto cuesta?", "Depende del tramo de edad y del producto. Te preparo un presupuesto sin compromiso."),
        ],
    },
    "alicante": {
        "ciudad": "Alicante", "region": "ES-VC", "coord": "38.345996;-0.490685", "icbm": "38.345996, -0.490685",
        "titulo": "Seguro de salud Sanitas para visado en Alicante | CFG Seguros",
        "desc": "Seguro de salud Sanitas para el visado en Alicante: estudiantes, residencia y nómada digital. Sin copagos ni carencias. Agente exclusiva Sanitas.",
        "h1": "Seguro de salud <span>Sanitas</span> para el visado en Alicante",
        "sub": "Si tramitas tu visado de estudios, residencia o nómada digital en <strong>Alicante</strong>, te gestiono el seguro Sanitas que cumple los requisitos.",
        "intro": "Alicante y la Costa Blanca concentran un gran número de residentes internacionales y nómadas digitales, además de estudiantes (Universidad de Alicante y Miguel Hernández). Es una de las zonas con más demanda de <strong>seguro médico para visado en Alicante</strong>.",
        "local": [
            ("💻", "Nómada digital en Alicante", "La Costa Blanca es un destino top para teletrabajadores. Te gestiono el seguro Sanitas válido para su residencia."),
            ("🌍", "Residencia en la Costa Blanca", "Muchos extranjeros se instalan en Alicante. Tu seguro cubre toda la estancia sin copagos ni carencias."),
            ("🎓", "Estudiantes en Alicante", "Para la Universidad de Alicante o la UMH, el seguro Sanitas cumple los requisitos del visado de estudios."),
        ],
        "faq": [
            ("¿Qué seguro necesito para el visado de nómada digital en Alicante?", "Un seguro sin copagos ni carencias y con cobertura completa. El seguro Sanitas que gestiono cumple los requisitos."),
            ("¿Sirve Sanitas para residencia en Alicante?", "Sí. Emito la póliza y el certificado válido para el expediente, listo para presentar."),
            ("¿Cuánto tarda el proceso?", "Emito el presupuesto el mismo día y el certificado lo antes posible tras el pago."),
        ],
    },
    "palma": {
        "ciudad": "Palma de Mallorca", "region": "ES-IB", "coord": "39.569600;2.650160", "icbm": "39.569600, 2.650160",
        "titulo": "Seguro de salud Sanitas para visado en Palma de Mallorca | CFG Seguros",
        "desc": "Seguro de salud Sanitas para el visado en Palma de Mallorca: estudiantes, residencia y nómada digital. Sin copagos ni carencias. Agente exclusiva Sanitas.",
        "h1": "Seguro de salud <span>Sanitas</span> para el visado en Palma de Mallorca",
        "sub": "Si tramitas tu visado en <strong>Palma de Mallorca</strong> —estudios, residencia o nómada digital—, te gestiono el seguro Sanitas sin copagos ni carencias.",
        "intro": "Palma de Mallorca y las Islas Baleares atraen a un número creciente de residentes internacionales, nómadas digitales y estudiantes (Universitat de les Illes Balears). La demanda de <strong>seguro médico para visado en Mallorca</strong> va en aumento.",
        "local": [
            ("💻", "Nómada digital en Mallorca", "Baleares es destino preferente de teletrabajadores. Te gestiono el seguro Sanitas válido para su residencia."),
            ("🌍", "Residencia en Baleares", "Muchos extranjeros se instalan en Mallorca. Tu seguro cubre toda la estancia sin carencias."),
            ("🎓", "Estudiantes en Mallorca", "Para la UIB, el seguro Sanitas cumple los requisitos del visado de estudios."),
        ],
        "faq": [
            ("¿Qué seguro necesito para el visado en Mallorca?", "Un seguro sin copagos ni carencias y con repatriación, válido para todo el periodo. El seguro Sanitas que gestiono lo cumple."),
            ("¿Se puede contratar desde el extranjero?", "Sí, a distancia, con pago por tarjeta o transferencia y certificado antes de viajar."),
            ("¿Cuánto cuesta?", "Depende del tramo de edad y del producto. Te preparo un presupuesto sin compromiso."),
        ],
    },
    "las-palmas": {
        "ciudad": "Las Palmas de Gran Canaria", "region": "ES-CN", "coord": "28.123545;-15.436257", "icbm": "28.123545, -15.436257",
        "titulo": "Seguro de salud Sanitas para visado en Las Palmas | CFG Seguros",
        "desc": "Seguro de salud Sanitas para el visado en Las Palmas de Gran Canaria: estudiantes, residencia y nómada digital. Sin copagos ni carencias.",
        "h1": "Seguro de salud <span>Sanitas</span> para el visado en Las Palmas",
        "sub": "Si tramitas tu visado en <strong>Las Palmas de Gran Canaria</strong>, te gestiono el seguro Sanitas que cumple los requisitos, sin copagos ni carencias.",
        "intro": "Las Palmas de Gran Canaria, con la Universidad de Las Palmas y varios centros de investigación, recibe estudiantes y profesionales internacionales. La demanda de <strong>seguro médico para visado en Canarias</strong> se mantiene durante todo el año.",
        "local": [
            ("🎓", "Estudiantes en Las Palmas", "Para la ULPGC, el seguro Sanitas es válido para el visado de estudios."),
            ("🌍", "Residencia en Canarias", "Tu seguro para el visado de residencia cubre toda la estancia sin carencias."),
            ("💻", "Nómada digital en Canarias", "Te gestiono el seguro Sanitas válido para la residencia de teletrabajadores."),
        ],
        "faq": [
            ("¿Qué seguro necesito para el visado en Las Palmas?", "Un seguro sin copagos ni carencias y con repatriación. El seguro Sanitas que gestiono cumple los requisitos."),
            ("¿Puedo contratarlo desde mi país?", "Sí. Se contrata a distancia y recibes el certificado antes de viajar."),
            ("¿Cuánto tarda el proceso?", "Presupuesto el mismo día y certificado lo antes posible tras el pago."),
        ],
    },
    "tenerife": {
        "ciudad": "Santa Cruz de Tenerife", "region": "ES-CN", "coord": "28.463630;-16.251847", "icbm": "28.463630, -16.251847",
        "titulo": "Seguro de salud Sanitas para visado en Tenerife | CFG Seguros",
        "desc": "Seguro de salud Sanitas para el visado en Santa Cruz de Tenerife: estudiantes, residencia y nómada digital. Sin copagos ni carencias.",
        "h1": "Seguro de salud <span>Sanitas</span> para el visado en Tenerife",
        "sub": "Si tramitas tu visado en <strong>Tenerife</strong> —estudios, residencia o nómada digital—, te gestiono el seguro Sanitas sin copagos ni carencias.",
        "intro": "Tenerife, con la Universidad de La Laguna, atrae a estudiantes internacionales y a profesionales que llegan con visado de residencia. La demanda de <strong>seguro médico para visado en Tenerife</strong> es constante.",
        "local": [
            ("🎓", "Estudiantes en Tenerife", "Para la Universidad de La Laguna, el seguro Sanitas es válido para el visado de estudios."),
            ("🌍", "Residencia en Tenerife", "Tu seguro para el visado de residencia cubre toda la estancia sin carencias."),
            ("💻", "Nómada digital en Tenerife", "Te gestiono el seguro Sanitas válido para la residencia de teletrabajadores."),
        ],
        "faq": [
            ("¿Qué seguro necesito para el visado en Tenerife?", "Un seguro sin copagos ni carencias y con repatriación. El seguro Sanitas que gestiono lo cumple."),
            ("¿Se puede contratar a distancia?", "Sí, con pago por tarjeta o transferencia y certificado antes de viajar."),
            ("¿Cuánto cuesta?", "Depende del tramo de edad y del producto. Te preparo un presupuesto sin compromiso."),
        ],
    },
    "valladolid": {
        "ciudad": "Valladolid", "region": "ES-CL", "coord": "41.652251;-4.724532", "icbm": "41.652251, -4.724532",
        "titulo": "Seguro de salud Sanitas para visado en Valladolid | CFG Seguros",
        "desc": "Seguro de salud Sanitas para el visado en Valladolid: estudiantes, residencia y nómada digital. Sin copagos ni carencias. Agente exclusiva Sanitas.",
        "h1": "Seguro de salud <span>Sanitas</span> para el visado en Valladolid",
        "sub": "Si tramitas tu visado en <strong>Valladolid</strong>, te gestiono el seguro Sanitas que necesitas, sin copagos ni carencias.",
        "intro": "Valladolid es una ciudad universitaria (Universidad de Valladolid) con presencia de estudiantes internacionales y residentes extranjeros. La demanda de <strong>seguro médico para visado en Valladolid</strong> se apoya en su comunidad académica.",
        "local": [
            ("🎓", "Estudiantes en Valladolid", "Para la Universidad de Valladolid, el seguro Sanitas es válido para el visado de estudios."),
            ("🌍", "Residencia", "Tu seguro para el visado de residencia cubre toda la estancia sin carencias."),
            ("💻", "Nómada digital", "Te gestiono el seguro Sanitas válido para la residencia de teletrabajadores."),
        ],
        "faq": [
            ("¿Qué seguro piden para el visado en Valladolid?", "Un seguro sin copagos ni carencias y con repatriación. El seguro Sanitas que gestiono cumple los requisitos."),
            ("¿Se contrata a distancia?", "Sí, con pago por tarjeta o transferencia y certificado antes de viajar."),
            ("¿Cuánto cuesta?", "Depende del tramo de edad y del producto. Presupuesto sin compromiso."),
        ],
    },
    "granada": {
        "ciudad": "Granada", "region": "ES-AN", "coord": "37.177336;-3.598557", "icbm": "37.177336, -3.598557",
        "titulo": "Seguro de salud Sanitas para visado en Granada | CFG Seguros",
        "desc": "Seguro de salud Sanitas para el visado en Granada: estudiantes, residencia y nómada digital. Sin copagos ni carencias. Agente exclusiva Sanitas.",
        "h1": "Seguro de salud <span>Sanitas</span> para el visado en Granada",
        "sub": "Si tramitas tu visado en <strong>Granada</strong> —estudios, residencia o nómada digital—, te gestiono el seguro Sanitas sin copagos ni carencias.",
        "intro": "Granada es una de las ciudades universitarias más importantes de España (Universidad de Granada), con un gran volumen de estudiantes internacionales, sobre todo de Erasmus y de América Latina. Es una plaza clave para el <strong>seguro médico para visado en Granada</strong>.",
        "local": [
            ("🎓", "Estudiantes en Granada", "Para la Universidad de Granada, el seguro Sanitas es válido para el visado de estudios y el NIE."),
            ("🌍", "Residencia y familia", "Granada acoge a familias que llegan con visado de residencia o reagrupación. Tu seguro cubre a todos."),
            ("💻", "Nómada digital en Granada", "Te gestiono el seguro Sanitas válido para la residencia de teletrabajadores."),
        ],
        "faq": [
            ("¿Qué seguro necesito para el visado de estudiante en Granada?", "Un seguro sin copagos ni carencias, válido para todo el curso y con repatriación. El seguro Sanitas que gestiono lo cumple."),
            ("¿Puedo contratarlo desde mi país?", "Sí. Se contrata a distancia y recibes el certificado antes de viajar."),
            ("¿Cuánto cuesta?", "Depende del tramo de edad y del producto. Presupuesto sin compromiso."),
        ],
    },
    "cordoba": {
        "ciudad": "Córdoba", "region": "ES-AN", "coord": "37.888175;-4.779383", "icbm": "37.888175, -4.779383",
        "titulo": "Seguro de salud Sanitas para visado en Córdoba | CFG Seguros",
        "desc": "Seguro de salud Sanitas para el visado en Córdoba: estudiantes, residencia y nómada digital. Sin copagos ni carencias. Agente exclusiva Sanitas.",
        "h1": "Seguro de salud <span>Sanitas</span> para el visado en Córdoba",
        "sub": "Si tramitas tu visado en <strong>Córdoba</strong>, te gestiono el seguro Sanitas que cumple los requisitos, sin copagos ni carencias.",
        "intro": "Córdoba, con la Universidad de Córdoba y un creciente interés turístico y residencial, recibe estudiantes y residentes internacionales. La demanda de <strong>seguro médico para visado en Córdoba</strong> se mantiene estable.",
        "local": [
            ("🎓", "Estudiantes en Córdoba", "Para la Universidad de Córdoba, el seguro Sanitas es válido para el visado de estudios."),
            ("🌍", "Residencia", "Tu seguro para el visado de residencia cubre toda la estancia sin carencias."),
            ("💻", "Nómada digital", "Te gestiono el seguro Sanitas válido para la residencia de teletrabajadores."),
        ],
        "faq": [
            ("¿Qué seguro necesito para el visado en Córdoba?", "Un seguro sin copagos ni carencias y con repatriación. El seguro Sanitas que gestiono lo cumple."),
            ("¿Se contrata a distancia?", "Sí, con pago por tarjeta o transferencia y certificado antes de viajar."),
            ("¿Cuánto cuesta?", "Depende del tramo de edad y del producto. Presupuesto sin compromiso."),
        ],
    },
    "a-coruna": {
        "ciudad": "A Coruña", "region": "ES-GA", "coord": "43.362344;-8.411540", "icbm": "43.362344, -8.411540",
        "titulo": "Seguro de salud Sanitas para visado en A Coruña | CFG Seguros",
        "desc": "Seguro de salud Sanitas para el visado en A Coruña: estudiantes, residencia y nómada digital. Sin copagos ni carencias. Agente exclusiva Sanitas.",
        "h1": "Seguro de salud <span>Sanitas</span> para el visado en A Coruña",
        "sub": "Si tramitas tu visado en <strong>A Coruña</strong> o Galicia, te gestiono el seguro Sanitas que necesitas, sin copagos ni carencias.",
        "intro": "A Coruña, con la Universidade da Coruña y un tejido profesional dinámico, recibe estudiantes y trabajadores internacionales. La demanda de <strong>seguro médico para visado en A Coruña</strong> va en aumento en toda Galicia.",
        "local": [
            ("🎓", "Estudiantes en A Coruña", "Para la Universidade da Coruña, el seguro Sanitas es válido para el visado de estudios."),
            ("🌍", "Residencia en Galicia", "Tu seguro para el visado de residencia cubre toda la estancia sin carencias."),
            ("💻", "Nómada digital en Galicia", "Te gestiono el seguro Sanitas válido para la residencia de teletrabajadores."),
        ],
        "faq": [
            ("¿Qué seguro necesito para el visado en A Coruña?", "Un seguro sin copagos ni carencias y con repatriación. El seguro Sanitas que gestiono lo cumple."),
            ("¿Se contrata a distancia?", "Sí, con pago por tarjeta o transferencia y certificado antes de viajar."),
            ("¿Cuánto cuesta?", "Depende del tramo de edad y del producto. Presupuesto sin compromiso."),
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
    h = head
    h = re.sub(r'<title>.*?</title>', f'<title>{c["titulo"]}</title>', h, count=1)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{c["desc"]}">', h, count=1)
    h = re.sub(r'<meta name="geo\.region" content="[^"]*">', f'<meta name="geo.region" content="{c["region"]}">', h)
    h = re.sub(r'<meta name="geo\.placename" content="[^"]*">', f'<meta name="geo.placename" content="{c["ciudad"]}">', h)
    h = re.sub(r'<meta name="geo\.position" content="[^"]*">', f'<meta name="geo.position" content="{c["coord"]}">', h)
    h = re.sub(r'<meta name="ICBM" content="[^"]*">', f'<meta name="ICBM" content="{c["icbm"]}">', h)
    url = f'https://cfg-seguros.com/seguros/salud-{slug}'
    h = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', h)
    h = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">', h)
    h = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{c["titulo"].split(" | ")[0]}">', h, count=1)
    h = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{c["desc"]}">', h, count=1)
    h = re.sub(r'<script type="application/ld\+json">.*?</script>\s*</head>', faq_schema(c) + "\n</head>", h, count=1, flags=re.S)

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

    cuerpo = f'''<section class="bloque">
  <div class="container">
    <h2>Seguro médico para visado en {c["ciudad"]}</h2>
    <p style="max-width:820px;margin:0 auto 1rem;color:#334155;line-height:1.7">{c["intro"]}</p>
    <p style="max-width:820px;margin:0 auto;color:#334155;line-height:1.7">Trabajo con <strong>Sanitas</strong>, la aseguradora líder en sanidad privada en España. Te gestiono la póliza y el <strong>certificado válido para tu visado</strong>, con trato directo y sin intermediarios.</p>
  </div>
</section>
{seccion_local(c)}
{seccion_faq(c)}'''

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
