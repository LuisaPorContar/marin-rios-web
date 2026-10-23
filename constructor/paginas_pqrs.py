# -*- coding: utf-8 -*-
"""PQRS: peticiones, quejas, reclamos y sugerencias.

El formulario envía al mismo Apps Script de los leads con tipo_envio=pqrs
(ver integraciones/google-sheets-leads.gs, recibirPQRS): llega de inmediato a
contacto@marinriosconsultores.com, se guarda en la pestaña "PQRS" del
Consolidado y el cliente recibe su número de radicado. No es un lead: no
dispara eventos de Meta ni usa lp-revisoria.js.
"""

import json
from base import ICO, heroe, encabezado
from paginas import PAGINAS
from paginas_meta import SHEETS_URL

CORREO_PQRS = "contacto@marinriosconsultores.com"
TIPOS = [("Petición", "Solicitar información, un documento o un trámite"),
         ("Queja", "Inconformidad con la atención de una persona del equipo"),
         ("Reclamo", "Inconformidad con un servicio que contrató"),
         ("Sugerencia", "Una idea para mejorar")]

opciones = "".join(f'<option value="{t}">{t}: {d.lower()}</option>' for t, d in TIPOS)

cuerpo = f"""
{heroe(
    "PQRS: peticiones, quejas, reclamos y sugerencias",
    "Escríbanos y su mensaje llega de inmediato al equipo de Marín Ríos Consultores. Le enviamos un número de radicado a su correo y le respondemos por ese mismo medio.",
    "reunion-cuadro.jpg",
    "Atención de PQRS en Marín Ríos Consultores",
    chip="Atención al cliente · PQRS",
    migas=[("Inicio", "index.html"), ("PQRS", None)],
)}

<section class="seccion form-leads" id="radicar">
  <div class="contenedor">
    <div class="lp-form-caja">
      <form class="lp-form" id="pqrs-form" novalidate data-sheets="{SHEETS_URL}">
        <h2 class="lp-titulo">Radique su PQRS</h2>
        <p class="lp-texto">Los campos marcados con * son obligatorios.</p>
        <div class="lp-form__campos">
          <div class="lp-campo lp-campo--ancho">
            <label for="pqrs-tipo">Tipo de solicitud *</label>
            <select id="pqrs-tipo" name="tipo" required>
              <option value="" selected disabled>Elija una opción</option>
              {opciones}
            </select>
          </div>
          <div class="lp-campo">
            <label for="pqrs-nombre">Nombre y apellido *</label>
            <input id="pqrs-nombre" name="nombre" type="text" autocomplete="name" required maxlength="80">
          </div>
          <div class="lp-campo">
            <label for="pqrs-correo">Correo *</label>
            <input id="pqrs-correo" name="correo" type="email" inputmode="email" autocomplete="email" required maxlength="120" placeholder="nombre@empresa.com">
          </div>
          <div class="lp-campo">
            <label for="pqrs-telefono">Teléfono</label>
            <input id="pqrs-telefono" name="telefono" type="tel" inputmode="numeric" autocomplete="tel-national" maxlength="13" placeholder="3001234567">
          </div>
          <div class="lp-campo">
            <label for="pqrs-empresa">Empresa</label>
            <input id="pqrs-empresa" name="empresa" type="text" autocomplete="organization" maxlength="120">
          </div>
          <div class="lp-campo lp-campo--ancho">
            <label for="pqrs-mensaje">Su mensaje *</label>
            <textarea id="pqrs-mensaje" name="mensaje" rows="6" required maxlength="3000" placeholder="Cuéntenos qué pasó o qué necesita. Si se refiere a un servicio, indique la empresa y el periodo."></textarea>
          </div>
          <label class="lp-check lp-campo--ancho">
            <input type="checkbox" name="autoriza" value="Sí" required>
            <span>Autorizo el tratamiento de mis datos para atender esta solicitud, según la <a href="politica-de-privacidad.html" target="_blank" rel="noopener">política de privacidad</a>.</span>
          </label>
        </div>
        <button class="lp-btn lp-btn--bloque" type="submit">Enviar PQRS{ICO['flecha']}</button>
        <p class="lp-form__error" id="pqrs-error" role="alert" hidden>Revise los campos marcados antes de enviar.</p>
        <p class="lp-form__error" id="pqrs-fallo" role="alert" hidden>
          No pudimos enviar su PQRS en este momento. Escríbanos directamente a
          <a id="pqrs-mailto" href="mailto:{CORREO_PQRS}">{CORREO_PQRS}</a> y la atendemos igual.
        </p>
      </form>
      <div class="pqrs-ok" id="pqrs-ok" role="status" hidden tabindex="-1">
        <h2 class="lp-titulo">Recibimos su PQRS</h2>
        <p class="lp-texto">Su número de radicado es <b data-radicado></b>. Le enviamos una copia a su correo y le responderemos por ese medio.</p>
      </div>
    </div>
    <p class="centrado revelar" style="margin-top:2rem">¿Prefiere escribirnos directamente? <a href="mailto:{CORREO_PQRS}">{CORREO_PQRS}</a></p>
  </div>
</section>

<script>
(function () {{
  var f = document.getElementById('pqrs-form');
  if (!f) return;
  var ok = document.getElementById('pqrs-ok'), error = document.getElementById('pqrs-error'),
      fallo = document.getElementById('pqrs-fallo'), boton = f.querySelector('button[type=submit]'),
      textoBoton = boton.innerHTML;
  f.addEventListener('submit', function (e) {{
    e.preventDefault();
    error.hidden = true; fallo.hidden = true;
    if (!f.checkValidity()) {{ error.hidden = false; f.reportValidity(); return; }}
    boton.disabled = true; boton.textContent = 'Enviando…';
    var datos = new URLSearchParams(new FormData(f));
    datos.set('tipo_envio', 'pqrs');
    datos.set('pagina', location.href);
    datos.set('event_id', 'pqrs-' + Date.now() + '-' + Math.random().toString(36).slice(2, 8));
    // Si el envío falla, el enlace de correo ya lleva el mensaje escrito
    document.getElementById('pqrs-mailto').href = 'mailto:{CORREO_PQRS}?subject=' +
      encodeURIComponent('PQRS · ' + (datos.get('tipo') || '') + ' · ' + (datos.get('nombre') || '')) +
      '&body=' + encodeURIComponent(datos.get('mensaje') || '');
    fetch(f.getAttribute('data-sheets'), {{ method: 'POST', body: datos }})
      .then(function (r) {{ return r.json(); }})
      .then(function (j) {{
        if (!j || !j.ok) throw new Error('no ok');
        ok.querySelector('[data-radicado]').textContent = j.radicado || '';
        f.hidden = true; ok.hidden = false; ok.focus();
        if (window.dataLayer) window.dataLayer.push({{ event: 'pqrs_enviada', pqrs_tipo: datos.get('tipo') }});
      }})
      .catch(function () {{
        fallo.hidden = false; boton.disabled = false; boton.innerHTML = textoBoton;
      }});
  }});
}})();
</script>
"""

PAGINAS.append(dict(
    archivo="pqrs.html",
    titulo="PQRS: Peticiones, Quejas, Reclamos y Sugerencias | Marín Ríos",
    descripcion="Radique su petición, queja, reclamo o sugerencia ante Marín Ríos Consultores. Llega de inmediato a nuestro equipo y recibe un número de radicado por correo.",
    activo="pqrs",
    og_img="reunion-cuadro.jpg",
    schema=json.dumps({
        "@context": "https://schema.org", "@type": "ContactPage",
        "name": "PQRS de Marín Ríos Consultores", "url": "https://marinriosconsultores.com/pqrs/",
        "mainEntity": {"@id": "https://marinriosconsultores.com/#empresa"},
    }, ensure_ascii=False, indent=2),
    cuerpo=cuerpo,
))
