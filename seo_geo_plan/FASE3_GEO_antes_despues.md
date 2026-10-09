# 🅾️ FASE 3 — GEO: FAQ ampliado + llms.txt
**Propuesta · NO aplicada · backup en `seo_geo_plan/backup_geo_*`**

> Objetivo: que ChatGPT, Gemini, Perplexity y Google te citen cuando alguien pregunte por un seguro Sanitas para el visado/residencia.

---

## 1️⃣ FAQ de la home: de 4 → 12 preguntas

**Se MANTIENEN las 4 actuales** y se AÑADEN estas 8 (todas reales, sin inventar precios):

1. ✅ *(ya estaba)* ¿Qué seguro de salud piden para el visado en España?
2. ✅ *(ya estaba)* ¿Se puede contratar el seguro Sanitas desde el extranjero antes de venir a España?
3. ✅ *(ya estaba)* ¿Qué diferencia hay entre Sanitas Estudiantes y Residentes para el visado?
4. ✅ *(ya estaba)* ¿Cuánto cuesta un seguro de salud Sanitas para el visado?
5. 🆕 **¿El seguro de Sanitas vale para la residencia no lucrativa?**
   → Sí. Sanitas Residentes cumple los requisitos: sin copagos, sin carencias, con repatriación y cobertura en todo el periodo de residencia.
6. 🆕 **¿Cuánto tarda en emitirse el certificado para el visado?**
   → Se emite en muy poco tiempo. Una vez contratado, recibes el certificado por email, listo para presentar en el consulado.
7. 🆕 **¿Puedo contratarlo desde Colombia u otro país antes de venir a España?**
   → Sí. Se contrata a distancia, se paga con tarjeta o transferencia y recibes el certificado antes de viajar.
8. 🆕 **¿El seguro cubre a mi familia o solo a mí?**
   → Se puede contratar individual o con la familia incluida, según el producto. Te oriento según tu caso.
9. 🆕 **¿Qué cubre el seguro de salud Sanitas para extranjeros?**
   → Asistencia sanitaria completa (médicos, especialistas, pruebas, hospitalización), sin copagos ni carencias, con repatriación incluida.
10. 🆕 **¿Sirve para el visado de nómada digital?**
    → Sí. La modalidad Residentes es la que se usa para el visado de nómada digital.
11. 🆕 **¿Hace falta un cuestionario médico o reconocimiento previo?**
    → Para estos productos no hace falta cuestionario de salud previo. Se contrata de forma sencilla.
12. 🆕 **¿Quién me gestiona el seguro?**
    → Sandra Lucía Caicedo, Agente Exclusiva de Sanitas, te lo gestiona de principio a fin: presupuesto, contratación y certificado.

---

## 2️⃣ Crear `llms.txt` (la novedad de GEO)
Un archivo nuevo en la raíz de la web (`cfg-seguros.com/llms.txt`) que las IA leen para saber **quién eres, qué ofreces y a quién**. Contenido propuesto:

```
# CFG Seguros — Sandra Lucía Caicedo, Agente Exclusiva de Sanitas

> Seguro de salud Sanitas para visados y residencia en España, gestionado
> por una Agente Exclusiva de Sanitas. Atención en español.

## Quién soy
Sandra Lucía Caicedo, Agente Exclusiva de Sanitas en España (Madrid).
Especializada en seguros de salud para extranjeros: visado de estudios,
residencia no lucrativa, nómada digital y reagrupación.

## Qué ofrezco
- Sanitas Estudiantes: seguro para visado de estudios.
- Sanitas Residentes: seguro para residencia no lucrativa y nómada digital.
- Seguro de salud Sanitas para familias, autónomos y mayores.
Todos sin copagos, sin carencias y con repatriación incluida.

## A quién ayudo
Personas que vienen a España desde Latinoamérica (Colombia, etc.) y necesitan
el seguro médico que exige el consulado para el visado o la residencia.

## Contacto
Email: slcaicedo.agenteexclusivo@sanitas.es
Teléfono: +34 641 754 490
Web: https://cfg-seguros.com/
```

---

## 🔒 GARANTÍAS
- Backup: `seo_geo_plan/backup_geo_*`
- Solo se AÑADEN preguntas al FAQ (no se quita ninguna) + se crea 1 archivo nuevo.
- Nada de diseño, colores ni estructura.
