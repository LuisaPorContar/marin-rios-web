# -*- coding: utf-8 -*-
"""PQRS: peticiones, quejas, reclamos y sugerencias.

Sin servidor ni hoja de respaldo: al enviar, se abre el correo de la persona con
el mensaje ya escrito y dirigido a contacto@marinriosconsultores.com. El correo
también queda visible para quien prefiera escribir por su cuenta. No es un lead:
no dispara eventos de Meta ni usa lp-revisoria.js.
"""

import json
from base import ICO, heroe
from paginas import PAGINAS

CORREO_PQRS = "contacto@marinriosconsultores.com"
TIPOS = [("Petición", "Solicitar información, un documento o un trámite"),
         ("Queja", "Inconformidad con la atención de una persona del equipo"),
         ("Reclamo", "Inconformidad con un servicio que contrató"),
         ("Sugerencia", "Una idea para mejorar")]

opciones = "".join(f'<option value="{t}">{t}: {d.lower()}</option>' for t, d in TIPOS)

cuerpo = f"""
{heroe(
    "PQRS: peticiones, quejas, reclamos y sugerencias",
    f"Su mensaje llega directo al equipo de Marín Ríos Consultores, al correo {CORREO_PQRS}. Le respondemos por ese mismo medio.",
    "reunion-cuadro.jpg",
    "Atención de PQRS en Marín Ríos Consultores",
    chip="Atención al cliente · PQRS",
    migas=[("Inicio", "index.html"), ("PQRS", None)],
)}

<section class="seccion form-leads" id="radicar">
  <div class="contenedor">
    <div class="lp-form-caja">
      <form class="lp-form" id="pqrs-form" novalidate>
        <h2 class="lp-titulo">Envíe su PQRS</h2>
        <p class="lp-texto">Al enviar se abre su correo con el mensaje listo, dirigido a {CORREO_PQRS}. Solo tiene que darle enviar.</p>
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
            <label for="pqrs-telefono">Teléfono</label>
            <input id="pqrs-telefono" name="telefono" type="tel" inputmode="numeric" autocomplete="tel-national" maxlength="13" placeholder="3001234567">
          </div>
          <div class="lp-campo lp-campo--ancho">
            <label for="pqrs-empresa">Empresa</label>
            <input id="pqrs-empresa" name="empresa" type="text" autocomplete="organization" maxlength="120">
          </div>
          <div class="lp-campo lp-campo--ancho">
            <label for="pqrs-mensaje">Su mensaje *</label>
            <textarea id="pqrs-mensaje" name="mensaje" rows="6" required maxlength="1500" placeholder="Cuéntenos qué pasó o qué necesita. Si se refiere a un servicio, indique la empresa y el periodo."></textarea>
          </div>
        </div>
        <button class="lp-btn lp-btn--bloque" type="submit">Escribir mi PQRS{ICO['flecha']}</button>
        <p class="lp-form__error" id="pqrs-error" role="alert" hidden>Revise los campos marcados antes de continuar.</p>
        <p class="lp-form__legal">Sus datos solo se usan para atender esta solicitud. <a href="politica-de-privacidad.html" target="_blank" rel="noopener">Política de privacidad</a>.</p>
      </form>
      <div class="pqrs-ok" id="pqrs-ok" role="status" hidden tabindex="-1">
        <h2 class="lp-titulo">Ya casi: revise su correo</h2>
        <p class="lp-texto">Abrimos su programa de correo con la PQRS lista. Si no se abrió, copie el mensaje y envíelo a
          <a href="mailto:{CORREO_PQRS}">{CORREO_PQRS}</a>.</p>
        <p style="margin-top:1rem"><button class="lp-btn" type="button" id="pqrs-copiar">Copiar mensaje</button></p>
      </div>
    </div>
    <p class="centrado revelar" style="margin-top:2rem">¿Prefiere escribirnos directamente? <a href="mailto:{CORREO_PQRS}">{CORREO_PQRS}</a></p>
  </div>
</section>

<script>
(function () {{
  var f = document.getElementById('pqrs-form');
  if (!f) return;
  var ok = document.getElementById('pqrs-ok'), error = document.getElementById('pqrs-error'), texto = '';
  f.addEventListener('submit', function (e) {{
    e.preventDefault();
    error.hidden = true;
    if (!f.checkValidity()) {{ error.hidden = false; f.reportValidity(); return; }}
    var d = new FormData(f), v = function (k) {{ return String(d.get(k) || '').trim(); }};
    var asunto = 'PQRS · ' + v('tipo') + ' · ' + v('nombre') + (v('empresa') ? ' (' + v('empresa') + ')' : '');
    texto = 'Tipo: ' + v('tipo') + '\\nNombre: ' + v('nombre') +
            (v('empresa') ? '\\nEmpresa: ' + v('empresa') : '') +
            (v('telefono') ? '\\nTeléfono: ' + v('telefono') : '') +
            '\\n\\nMensaje:\\n' + v('mensaje');
    location.href = 'mailto:{CORREO_PQRS}?subject=' + encodeURIComponent(asunto) + '&body=' + encodeURIComponent(texto);
    f.hidden = true; ok.hidden = false; ok.focus();
    if (window.dataLayer) window.dataLayer.push({{ event: 'pqrs_correo', pqrs_tipo: v('tipo') }});
  }});
  document.getElementById('pqrs-copiar').addEventListener('click', function () {{
    var b = this;
    navigator.clipboard.writeText('Para: {CORREO_PQRS}\\n\\n' + texto).then(function () {{ b.textContent = 'Mensaje copiado'; }});
  }});
}})();
</script>
"""

PAGINAS.append(dict(
    archivo="pqrs.html",
    titulo="PQRS: Peticiones, Quejas, Reclamos y Sugerencias | Marín Ríos",
    descripcion="Envíe su petición, queja, reclamo o sugerencia a Marín Ríos Consultores. Llega directo a contacto@marinriosconsultores.com y le respondemos por correo.",
    activo="pqrs",
    og_img="reunion-cuadro.jpg",
    schema=json.dumps({
        "@context": "https://schema.org", "@type": "ContactPage",
        "name": "PQRS de Marín Ríos Consultores", "url": "https://marinriosconsultores.com/pqrs/",
        "mainEntity": {"@id": "https://marinriosconsultores.com/#empresa"},
    }, ensure_ascii=False, indent=2),
    cuerpo=cuerpo,
))
