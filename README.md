# CFG Seguros — cfg-seguros.com

## Información general
- **Dominio:** cfg-seguros.com
- **Propósito:** Web corporativa para el ramo de seguros
- **Colaborador de:** Grupo Galilea
- **Fecha de creación:** Julio 2026

---

## Hosting
- **Plataforma:** Cloudflare Pages
- **Proyecto:** cfg-seguros-web
- **URL producción:** https://cfg-seguros.com
- **URL pages.dev:** https://cfg-seguros-web.pages.dev
- **Account ID:** 72305fb85467e89da2940e359f9e09cc
- **Zone ID:** 9986e3c1cb4dd72f25ba56ec9afdb727

## DNS (Cloudflare)
- **Nameservers:** chase.ns.cloudflare.com / sima.ns.cloudflare.com
- **CNAME @:** cfg-seguros-web.pages.dev (Proxied)
- **CNAME www:** cfg-seguros-web.pages.dev (Proxied)
- **MX 10:** aspmx1.migadu.com
- **MX 20:** aspmx2.migadu.com
- **TXT @:** hosted-email-verify=cpnvofqk
- **TXT @:** v=spf1 include:spf.migadu.com -all
- **TXT _dmarc:** v=DMARC1; p=quarantine;
- **CNAME key1._domainkey:** key1.cfg-seguros.com._domainkey.migadu.com.
- **CNAME key2._domainkey:** key2.cfg-seguros.com._domainkey.migadu.com.
- **CNAME key3._domainkey:** key3.cfg-seguros.com._domainkey.migadu.com.

## SSL/TLS
- **Estado:** Activo (automático por Cloudflare)
- **Tipo:** Full (strict) — Cloudflare gestiona el certificado
- **Emisor:** Cloudflare SSL

## Correo electrónico
- **Proveedor:** Migadu
- **Cuenta:** sandluc22@gmail.com
- **Contraseña cuenta:** AlfaySandra!
- **API key AlfaDefinitiva:** bAdZUBg6MPIM-ABYBOBZI7IcB61i0UFqMdK_Mlm7ps_y9hLCb0t0aca6HyD4Je7EYzjwLL5dVaxFaaVOVoggzg
- **Buzones creados:**
  - admin@cfg-seguros.com (Postmaster — automático)
  - info@cfg-seguros.com (CFG Seguros)
  - ventas@cfg-seguros.com (CFG Seguros - Ventas)

## Web3Forms
- **Access Key:** 58b165d2-318b-4718-bb6a-9b46dbb4540d
- **Correo destino leads:** info@cfg-seguros.com
- **Formulario campos:** nombre, email, teléfono, fecha nacimiento, seguro, aseguradora, mensaje

## Telegram
- **Token:** 766728…PFzA
- **Chat ID:** 7890204626
- **Notificaciones:** Llegan leads del formulario

## Estructura de la web
```
cfg-seguros.com/
├── index.html                    — Home completo
├── seguros/
│   ├── index.html                — Listado de seguros
│   ├── vida.html                 — Seguro de Vida
│   ├── salud.html                — Seguro de Salud
│   ├── hogar.html                — Seguro de Hogar
│   ├── coche.html                — Seguro de Coche
│   ├── empresas.html             — Seguro de Empresas
│   └── ahorro-inversion.html     — Ahorro e Inversión
└── blog/
    ├── index.html                — Índice del blog
    ├── seguro-vida-mitos-realidades.html
    ├── seguro-salud-guia-completa.html
    ├── proteccion-empresas-autonomos.html
    └── ahorro-inversion-primeros-pasos.html
```

## Deploy (Cloudflare Pages)
- **Método:** npx wrangler pages deploy . --project-name=cfg-seguros-web
- **Último deploy:** https://bf71da9f.cfg-seguros-web.pages.dev
- **Dominio asignado manualmente:** API Cloudflare (add domain) o dashboard

## Notas
- Antes del deploy: quitar dominio con API, deployar, re-asignar dominio
- Token Cloudflare guardado en: /tmp/cf_token.txt
- Token NO tiene permisos de Email Routing
- Para cambiar contenido: editar archivos en /home/node/workspace/cfg-seguros/
