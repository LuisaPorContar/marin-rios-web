# -*- coding: utf-8 -*-
"""Formulario de leads reutilizable (cotizaciones, landings).

Envía al mismo Apps Script que la landing de revisoría (ver
integraciones/google-sheets-leads.gs) y lo atiende el mismo
assets/js/lp-revisoria.js. Lo propio de cada página va en atributos data-*.
"""

from base import ICO, WA
from paginas_meta import SHEETS_URL, INGRESOS, _campo_lista

CIUDADES = ["Medellín y Valle de Aburrá", "Pereira", "Dosquebradas", "Armenia", "Manizales", "Otra"]


def formulario_leads(formulario, oferta, servicio, titulo, texto, boton,
                     gracias_ok="gracias-cotizacion", gracias_peq="gracias-evaluacion-guia",
                     califica_todos=False, mensaje_wa="", legal="esta cotización"):
    """Devuelve el bloque <form> completo, listo para meter en una sección."""
    extra = ' data-califica-todos="1"' if califica_todos else ""
    return f"""<div class="lp-form-caja">
      <form class="lp-form" id="lp-form" novalidate
            data-sheets="{SHEETS_URL}" data-wa="{WA}"
            data-gracias-ok="/{gracias_ok}/" data-gracias-peq="/{gracias_peq}/"
            data-formulario="{formulario}" data-oferta="{oferta}" data-servicio="{servicio}"
            data-mensaje="{mensaje_wa or 'recibir una cotización'}"{extra}>
        <h2 class="lp-titulo">{titulo}</h2>
        <p class="lp-texto">{texto}</p>
        <div class="lp-form__campos">
          <div class="lp-campo">
            <label for="lp-nombre">Nombre y apellido</label>
            <input id="lp-nombre" name="nombre" type="text" autocomplete="name" required maxlength="80">
          </div>
          <div class="lp-campo">
            <label for="lp-empresa">Empresa</label>
            <input id="lp-empresa" name="empresa" type="text" autocomplete="organization" required maxlength="120">
          </div>
          <div class="lp-campo">
            <label for="lp-correo">Correo</label>
            <input id="lp-correo" name="correo" type="email" inputmode="email" autocomplete="email" required maxlength="120" placeholder="nombre@empresa.com">
          </div>
          <div class="lp-campo">
            <label for="lp-whatsapp">WhatsApp</label>
            <input id="lp-whatsapp" name="whatsapp" type="tel" inputmode="numeric" autocomplete="tel-national" required
                   pattern="[0-9]{{10,13}}" maxlength="13" placeholder="3001234567"
                   title="Solo números, sin espacios. Ejemplo: 3001234567">
          </div>
          {_campo_lista("ciudad", "Ciudad", CIUDADES)}
          {_campo_lista("ingresos", "Ingresos anuales aproximados", INGRESOS)}
        </div>
        <button class="lp-btn lp-btn--bloque" type="submit">{boton}{ICO['flecha']}</button>
        <p class="lp-form__error" id="lp-form-error" role="alert" hidden>Revisa los campos marcados antes de continuar.</p>
        <p class="lp-form__legal">Tus datos solo se usan para contactarte sobre {legal}. <a href="politica-de-privacidad.html" target="_blank" rel="noopener">Política de privacidad</a>.</p>
      </form>
    </div>"""
