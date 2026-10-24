#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Recupera el formulario Web3Forms en las 6 paginas de cfg-seguros (home + 5 landings).
En vez de abrir WhatsApp, envia los datos por correo a info@cfg-seguros.com
(Web3Forms: la cuenta que ya tenia la access_key) y muestra boton de exito.
"""
import os, re, subprocess

ROOT = "/home/node/workspace/cfg-seguros"
KEY = "58b165d2-318b-4718-bb6a-9b46dbb4540d"

PAGES = [
    ("estudiantes/index.html", "estudiantes"),
    ("extranjeros/index.html", "extranjeros"),
    ("mayores-65/index.html", "mayores-65"),
    ("autonomos/index.html", "autonomos"),
    ("familias/index.html", "familias"),
    ("index.html", "general"),
]

JS_NEW = """<script>
document.getElementById('contactForm').addEventListener('submit', async function(e){
  e.preventDefault();
  var btn=this.querySelector('.btn-submit'); var orig=btn?btn.textContent:'';
  if(btn){btn.textContent='Enviando...';btn.disabled=true;}
  var fd=new FormData(this); var data={}; fd.forEach(function(v,k){data[k]=v;});
  var ok=false;
  try{
    var r=await fetch('https://api.web3forms.com/submit',{method:'POST',
      headers:{'Content-Type':'application/json','Accept':'application/json'},
      body:JSON.stringify(data)});
    var j=await r.json(); ok=j.success;
  }catch(err){ console.log('W3 error:',err); }
  if(btn){btn.textContent=orig;btn.disabled=false;}
  if(ok){
    this.reset();
    var okd=document.getElementById('formOk');
    okd.style.display='block';
    setTimeout(function(){okd.style.display='none';},8000);
  }else{
    alert('No se pudo enviar. Escríbenos a info@cfg-seguros.com o por WhatsApp.');
  }
});
</script>"""

for rel, nombre in PAGES:
    path = os.path.join(ROOT, rel)
    if not os.path.exists(path):
        print("NO EXISTE:", rel); continue
    html = open(path, encoding="utf-8").read()
    orig = html

    # 1) Boton: "Enviar por WhatsApp" -> "Enviar solicitud"
    html = html.replace("📨 Enviar por WhatsApp", "📨 Enviar solicitud")
    # 2) Mensaje de exito
    html = re.sub(
        r'<div id="formOk"[^>]*>.*?</div>',
        '<div id="formOk" style="display:none;background:#065f46;color:#d1fae5;padding:1rem;border-radius:8px;text-align:center;margin-top:1rem">'
        '✓ ¡Listo! Hemos recibido tus datos. Te contactamos enseguida. '
        'Si prefieres, escríbenos también por WhatsApp.</div>',
        html, count=1, flags=re.S)
    # 3) Reemplazar el <script> del formulario (el que abria WhatsApp)
    html = re.sub(r"<script>\s*\ndocument\.getElementById\('contactForm'\).*?</script>",
                  JS_NEW, html, count=1, flags=re.S)

    if html != orig:
        open(path, "w", encoding="utf-8").write(html)
        print("ACTUALIZADO:", rel)
    else:
        print("SIN CAMBIOS (revisar):", rel)
