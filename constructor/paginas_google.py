# -*- coding: utf-8 -*-
"""
Landings de pauta en Google Ads (búsqueda): outsourcing contable y revisoría fiscal.

Son el destino de la campaña «MR | Busqueda | Outsourcing y Revisoria | MED-PEI-AXM».
Repiten lo que prometen los anuncios (revisión o evaluación sin costo, +50 empresas,
contador público a cargo, Medellín, Pereira y Armenia) y ponen el formulario en
el primer pantallazo, a la derecha en escritorio y debajo del texto en celular.

Van con `noindex` y sin menú: es tráfico pagado y no debe competir en Google con
/outsourcing-contable/ ni con /revisoria-fiscal/. Usan la piel de la landing de
Meta (lp-revisoria.css) más una capa propia (lp-google.css).

El formulario es el mismo de las cotizaciones (formulario.py): guarda el lead en
el Google Sheet y redirige a una página de gracias propia de cada landing, para
que Google Ads pueda medir la conversión por URL sin mezclarla con Meta.
"""

from base import ICO, WA, acordeon, resenas_google, carrusel_clientes
from paginas import PAGINAS
from formulario import formulario_leads
from paginas_meta import ICONO, TOPE_INGRESOS, TOPE_ACTIVOS, _pagina_gracias

NOINDEX = "noindex, follow"
CSS = ("assets/css/lp-revisoria.css", "assets/css/lp-google.css")
ANCLA = "#cotizar"

GRACIAS_OUT = "gracias-lp-outsourcing"
GRACIAS_RF = "gracias-lp-revisoria"
GRACIAS_PEQ = "gracias-evaluacion-guia"


def _boton(texto):
    return f'<a class="lp-btn" href="{ANCLA}">{texto}{ICO["flecha"]}</a>'


def _chips(items):
    return '<ul class="lp-chips">' + "".join(f"<li>{t}</li>" for t in items) + "</ul>"


def _lista(items, icono="check", clase=""):
    filas = "".join(f"<li>{ICONO[icono]}<span>{t}</span></li>" for t in items)
    return f'<ul class="lp-oferta__lista lp-oferta__lista--sola {clase}">{filas}</ul>'


def _pasos(items, iconos):
    filas = "".join(
        f"""<li>
        <span class="lp-ico lp-ico--grande">{ICONO[ic]}</span>
        <div><h3>{t}</h3><p class="lp-partes__bajada">{b}</p><p>{d}</p></div>
      </li>""" for (t, b, d), ic in zip(items, iconos))
    return f'<ol class="lp-partes revelar">{filas}</ol>'


def _wa(texto):
    from urllib.parse import quote
    return f"https://wa.me/{WA}?text={quote(texto)}"


def _heroe(etiqueta, h1, sub, chips, prueba, formulario, boton):
    return f"""<section class="lp-heroe lp-heroe--cols lp-heroe--form" id="cotizar">
  <div class="lp-contenedor">
    <img class="lp-heroe__logo" src="assets/img/logo-marin-rios.png" alt="Marín Ríos Consultores" width="90" height="80">
    <div class="lp-heroe__rejilla">
      <div class="lp-heroe__texto">
        <p class="lp-etiqueta">{etiqueta}</p>
        <h1>{h1}</h1>
        <p class="lp-heroe__sub">{sub}</p>
        <a class="lp-btn lp-solo-movil" href="#lp-form">{boton}{ICO["flecha"]}</a>
        <p class="lp-heroe__prueba">{prueba}</p>
      </div>
      {formulario}
    </div>
  </div>
</section>"""


def _persona():
    return """<section class="lp-seccion">
  <div class="lp-contenedor lp-centro lp-angosto">
    <h2 class="lp-titulo">Quién responde por tu empresa</h2>
    <div class="lp-heroe__media lp-heroe__media--retrato revelar">
      <img src="assets/img/asesor.png" alt="Juan David Marín Ríos, gerente de Marín Ríos Consultores" width="647" height="900" loading="lazy">
    </div>
    <p class="lp-persona__nombre">Juan David Marín Ríos</p>
    <p class="lp-persona__rol">Gerente · Contador público especialista en finanzas tributarias</p>
  </div>
</section>"""


def _whatsapp(texto_wa):
    return f"""<section class="lp-seccion lp-seccion--corta">
  <div class="lp-contenedor">
    <div class="lp-wa revelar">
      <h2 class="lp-titulo">¿Prefieres escribirnos?</h2>
      <p class="lp-texto">Te responde alguien del equipo por WhatsApp, no un robot.</p>
      <a class="lp-btn" href="{_wa(texto_wa)}" target="_blank" rel="noopener">{ICO['wa']}Escribir al +57 314 884 3835</a>
    </div>
  </div>
</section>"""


def _faq(preguntas, prefijo):
    return f"""<section class="lp-seccion">
  <div class="lp-contenedor lp-centro">
    <h2 class="lp-titulo">Preguntas frecuentes</h2>
    <div class="lp-faq">
      {acordeon([(q, f"<p>{a}</p>") for q, a in preguntas], prefijo=prefijo)}
    </div>
  </div>
</section>"""


# ================================================================
# /lp-outsourcing-contable/
# ================================================================
FAQ_OUT = [
    ("¿Cuánto cuesta el outsourcing contable?",
     "Los planes van desde 2 SMMLV al mes. El valor final depende del volumen de facturas y movimientos, del número de empleados en nómina y de los impuestos que declara tu empresa. Por eso revisamos tu operación sin costo y te enviamos el valor por escrito."),
    ("¿La revisión inicial tiene algún costo?",
     "No. Revisar tu caso y enviarte la propuesta no tiene costo ni te compromete a contratar."),
    ("¿Puedo cambiar de contador a mitad de año?",
     "Sí. Organizamos el empalme con el contador saliente para recibir libros, soportes y declaraciones sin que se pierda ningún vencimiento. La transición toma en promedio 15 días."),
    ("¿Qué incluye el servicio?",
     "Contabilidad general y libros oficiales, conciliaciones bancarias, cuentas por cobrar y por pagar, impuestos nacionales y municipales, nómina electrónica y seguridad social, estados financieros NIIF y atención de requerimientos de la DIAN."),
    ("¿Dónde atienden?",
     "Con visitas presenciales en Medellín, Pereira, Armenia y Manizales, y de forma remota para el resto del país."),
    ("¿Qué empresas atienden?",
     "SAS, LTDA y S.A., startups y pymes en crecimiento que todavía no justifican un área contable interna, fundaciones y organizaciones de economía solidaria."),
]

form_out = formulario_leads(
    formulario="Google Ads · Outsourcing contable",
    oferta="Cotización outsourcing contable",
    servicio="outsourcing",
    titulo="Pide tu cotización sin costo",
    texto="Toma menos de un minuto. Te escribimos por WhatsApp en menos de 24 horas hábiles.",
    boton="Quiero mi cotización",
    gracias_ok=GRACIAS_OUT, gracias_peq=GRACIAS_PEQ,
    califica_todos=True,
    mensaje_wa="recibir una cotización de outsourcing contable",
)

cuerpo_out = f"""
{_heroe(
    "Medellín · Pereira · Armenia",
    "Outsourcing contable para empresas en Medellín y el Eje Cafetero",
    'Registros, conciliaciones, impuestos, nómina y reportes con un <span class="lp-acento">contador público a cargo</span>. Tú recibes cifras al día para decidir.',
    ["Revisión inicial sin costo", "Planes desde 2 SMMLV al mes", "Respuesta en 24 h"],
    "Con el equipo que ya lleva la contabilidad de <strong>más de 50 empresas</strong>.",
    form_out, "Pedir mi cotización sin costo")}

<section class="lp-logos">
  <p class="lp-logos__titulo">Empresas que ya tercerizaron su contabilidad con nosotros</p>
  {carrusel_clientes("oscuro")}
</section>

<section class="lp-seccion">
  <div class="lp-contenedor lp-centro lp-angosto">
    <h2 class="lp-titulo">¿Te está pasando esto?</h2>
    <div class="lp-oferta revelar">
      {_lista([
          "Los cierres llegan tarde y decides sin cifras.",
          "Los impuestos se presentan sobre la hora.",
          "Las cuentas no cuadran con el banco.",
          "Toda la contabilidad depende de una sola persona.",
      ], icono="alerta")}
    </div>
    <p class="lp-perspectiva">No entregamos solo un balance: entregamos una lectura de tu empresa que puedes usar para decidir.</p>
  </div>
</section>

<section class="lp-seccion">
  <div class="lp-contenedor lp-centro">
    <h2 class="lp-titulo">Qué incluye tu outsourcing contable</h2>
    <div class="lp-oferta lp-oferta--ancha revelar">
      {_lista([
          "Contabilidad general y libros oficiales",
          "Conciliaciones bancarias",
          "Cuentas por cobrar y por pagar",
          "IVA, retención, ICA, renta y exógena",
          "Nómina electrónica y seguridad social",
          "Estados financieros NIIF con lectura",
          "Atención de requerimientos de la DIAN",
          "Reunión periódica de seguimiento",
      ], clase="lp-oferta__lista--dos")}
    </div>
    {_boton("Pedir mi cotización")}
  </div>
</section>

<section class="lp-seccion">
  <div class="lp-contenedor lp-centro">
    <h2 class="lp-titulo">Así empezamos a trabajar contigo</h2>
    {_pasos([
        ("Revisión inicial", "Sin costo.", "Entendemos cómo opera tu empresa y te enviamos la propuesta por escrito: alcance, entregables, responsable y honorarios."),
        ("Empalme", "15 días en promedio.", "Recibimos libros, soportes y declaraciones del contador anterior sin perder ningún vencimiento."),
        ("Gestión mensual", "Todo al día.", "Registros, impuestos, nómina y cierre mensual con informe."),
        ("Acompañamiento", "Reuniones y alertas.", "Te avisamos antes de cada vencimiento y revisamos contigo las cifras para decidir."),
    ], ["lupa", "documento", "informe", "campana"])}
    <div class="lp-datos">
      <div><strong>+50</strong><span>Empresas con su contabilidad tercerizada</span></div>
      <div><strong>100 %</strong><span>Calendario DIAN cumplido</span></div>
    </div>
  </div>
</section>

{_persona()}

{resenas_google(variante="oscuro")}

{_faq(FAQ_OUT, "gout")}

<section class="lp-seccion lp-seccion--corta">
  <div class="lp-contenedor lp-centro">
    <h2 class="lp-titulo">Recibe tu propuesta por escrito, sin costo</h2>
    <p class="lp-texto">Alcance, entregables, responsable y honorarios en un documento que puedes comparar con cualquier otra oferta.</p>
    {_boton("Pedir mi cotización")}
  </div>
</section>

{_whatsapp("Hola, vengo del anuncio de Google y quiero una cotización de outsourcing contable")}

<script src="assets/js/lp-revisoria.js" defer></script>
"""

PAGINAS.append(dict(
    archivo="lp-outsourcing-contable.html",
    titulo="Outsourcing contable en Medellín y Eje Cafetero | Marín Ríos",
    descripcion="Contabilidad, impuestos, nómina y reportes con un contador público a cargo. Revisión inicial sin costo y cotización por escrito en 24 horas.",
    activo="", og_img="reunion-ancho.jpg", robots=NOINDEX, schema="",
    cuerpo=cuerpo_out, clase_body="lp", css_extra=CSS, landing=(),
))


# ================================================================
# /lp-revisoria-fiscal/
# ================================================================
FAQ_RF = [
    ("¿Mi empresa está obligada a tener revisor fiscal en 2027?",
     f"Si a 31 de diciembre de 2026 tus activos brutos superan {TOPE_ACTIVOS} o tus ingresos brutos del año {TOPE_INGRESOS}, sí. Las sociedades anónimas y las sucursales de sociedades extranjeras siempre lo necesitan, y también aplica cuando lo exigen los estatutos."),
    ("¿La evaluación tiene algún costo?",
     "No. Te confirmamos si estás obligado, revisamos tu contabilidad y te entregamos una propuesta por escrito, sin compromiso."),
    ("¿Cuánto cobra un revisor fiscal?",
     "No hay una tarifa oficial. El valor depende del tamaño de la empresa, del sector, de la complejidad contable y de las horas que exige la revisoría. Por eso te lo entregamos por escrito después de revisar tu caso."),
    ("Ya tengo revisor fiscal. ¿Puedo cambiarlo?",
     "Sí. El revisor lo nombra la asamblea, así que la reunión ordinaria del primer trimestre es el momento natural para cambiarlo. Te ayudamos con el empalme para que no quede ningún informe pendiente."),
    ("¿Dónde atienden?",
     "En nuestra oficina de Laureles en Medellín, en tu empresa si estás en Pereira, Armenia o Manizales, o por videollamada."),
    ("¿Pueden llevar mi contabilidad y ser mis revisores fiscales?",
     "No. La revisoría exige independencia, así que no prestamos ambos servicios a la misma empresa."),
]

form_rf = formulario_leads(
    formulario="Google Ads · Revisoría fiscal",
    oferta="Evaluación revisoría fiscal",
    servicio="revisoria",
    titulo="Pide tu evaluación sin costo",
    texto="Toma menos de un minuto. Te escribimos por WhatsApp en menos de 24 horas hábiles.",
    boton="Quiero mi evaluación",
    gracias_ok=GRACIAS_RF, gracias_peq=GRACIAS_PEQ,
    mensaje_wa="una evaluación de revisoría fiscal",
    legal="esta evaluación",
)

cuerpo_rf = f"""
{_heroe(
    "Medellín · Pereira · Armenia",
    "Servicio de revisoría fiscal para empresas en Medellín y el Eje Cafetero",
    'Un revisor fiscal presente todo el año, no solo al cierre. <span class="lp-acento">Evaluación inicial sin costo</span> y propuesta por escrito, lista para tu asamblea.',
    ["Evaluación sin costo", "Contador público a cargo", "SAS, LTDA y S.A."],
    "Con el equipo que ya acompaña a <strong>más de 50 empresas</strong>.",
    form_rf, "Pedir mi evaluación sin costo")}

<section class="lp-logos">
  <p class="lp-logos__titulo">Empresas que confían sus estados financieros en nosotros</p>
  {carrusel_clientes("oscuro")}
</section>

<section class="lp-seccion">
  <div class="lp-contenedor lp-centro">
    <h2 class="lp-titulo">¿Tu empresa está obligada a tener revisor fiscal en 2027?</h2>
    <p class="lp-texto">Basta con cumplir una de estas condiciones al 31 de diciembre de 2026.</p>
    <ul class="lp-topes revelar">
      <li><strong>Activos desde {TOPE_ACTIVOS}</strong><span>Activos brutos al cierre del año.</span></li>
      <li><strong>Ingresos desde {TOPE_INGRESOS}</strong><span>Ingresos brutos del año.</span></li>
      <li><strong>Sociedad anónima</strong><span>Las S.A. y las sucursales extranjeras siempre, y cualquier sociedad si lo piden sus estatutos.</span></li>
    </ul>
    {_boton("Saber si estoy obligado")}
  </div>
</section>

<section class="lp-seccion">
  <div class="lp-contenedor lp-centro">
    <h2 class="lp-titulo">Un revisor fiscal que sí revisa</h2>
    {_pasos([
        ("Diagnóstico y plan anual", "Al empezar.", "Conocemos tu operación y fijamos qué revisamos, cuándo y con qué normas de aseguramiento."),
        ("Visitas y revisión permanente", "Durante todo el año.", "Revisamos la contabilidad, los impuestos y el control interno, no solo al cierre."),
        ("Alertas a tiempo", "Antes de cada vencimiento.", "Te avisamos de inconsistencias en retenciones, IVA o facturación para corregirlas antes de que sean sanción."),
        ("Cierre y dictamen", "Para tu asamblea.", "Dictamen de estados financieros, informe a la asamblea y firma de las declaraciones obligatorias."),
    ], ["lupa", "activos", "campana", "firma"])}
    {_boton("Pedir mi evaluación")}
  </div>
</section>

<section class="lp-seccion">
  <div class="lp-contenedor lp-centro">
    <h2 class="lp-titulo">Lo que recibe tu empresa</h2>
    <div class="lp-oferta revelar">
      {_lista([
          "Dictamen de estados financieros con validez ante bancos y entes de control.",
          "Informes de control interno para la gerencia y la junta.",
          "Revisión de las declaraciones tributarias antes de presentarlas.",
          "Informe a la asamblea y acompañamiento si hay requerimientos de la DIAN.",
      ])}
    </div>
  </div>
</section>

{_persona()}

<section class="lp-seccion">
  <div class="lp-contenedor lp-centro lp-angosto">
    <h2 class="lp-titulo">El costo de prevenir frente al costo de un error</h2>
    <p class="lp-texto">Una sanción de la DIAN por inexactitud, o por presentar declaraciones sin la firma obligatoria del revisor fiscal, puede superar fácilmente los <strong class="lp-acento">$20 millones</strong>, sin contar los intereses de mora.</p>
    <p class="lp-perspectiva">Nombrar a tiempo un revisor fiscal cuesta una fracción de eso.</p>
  </div>
</section>

{resenas_google(variante="oscuro")}

{_faq(FAQ_RF, "grf")}

<section class="lp-seccion lp-seccion--corta">
  <div class="lp-contenedor lp-centro">
    <h2 class="lp-titulo">Llega a la asamblea con la decisión tomada</h2>
    <p class="lp-texto">Te confirmamos si estás obligado y te entregamos la propuesta por escrito, sin costo.</p>
    {_boton("Pedir mi evaluación")}
  </div>
</section>

{_whatsapp("Hola, vengo del anuncio de Google y quiero una evaluación de revisoría fiscal")}

<script src="assets/js/lp-revisoria.js" defer></script>
"""

PAGINAS.append(dict(
    archivo="lp-revisoria-fiscal.html",
    titulo="Revisoría fiscal en Medellín y Eje Cafetero | Marín Ríos",
    descripcion="Revisor fiscal presente todo el año para SAS, LTDA y S.A. Evaluación inicial sin costo y propuesta por escrito, lista para tu asamblea.",
    activo="", og_img="reunion-duotono.jpg", robots=NOINDEX, schema="",
    cuerpo=cuerpo_rf, clase_body="lp", css_extra=CSS, landing=(),
))


# ================================================================
# Páginas de gracias (Google Ads mide la conversión por estas URL)
# ================================================================
PAGINAS.append(dict(
    archivo=f"{GRACIAS_OUT}.html",
    titulo="Recibimos tu solicitud | Outsourcing contable | Marín Ríos",
    descripcion="Recibimos tu solicitud de cotización de outsourcing contable. Te escribimos por WhatsApp en menos de 24 horas hábiles.",
    activo="", og_img="oficina-atardecer.jpg", robots=NOINDEX, schema="",
    cuerpo=_pagina_gracias(
        "calificado",
        "Listo, <em>recibimos tu solicitud</em>",
        "En menos de 24 horas hábiles te escribimos por WhatsApp para entender tu operación y enviarte la cotización por escrito. Si quieres adelantarte, escríbenos ahora.",
        f'<a class="lp-btn" data-wa-lead href="{_wa("Hola, acabo de pedir una cotización de outsourcing contable en su página")}" target="_blank" rel="noopener">{ICO["wa"]}Escribir por WhatsApp ahora</a>'),
    clase_body="lp", css_extra=CSS, landing=(),
))

PAGINAS.append(dict(
    archivo=f"{GRACIAS_RF}.html",
    titulo="Recibimos tu solicitud | Revisoría fiscal | Marín Ríos",
    descripcion="Recibimos tu solicitud de evaluación de revisoría fiscal. Te escribimos por WhatsApp en menos de 24 horas hábiles.",
    activo="", og_img="oficina-atardecer.jpg", robots=NOINDEX, schema="",
    cuerpo=_pagina_gracias(
        "calificado",
        "Listo, <em>recibimos tu solicitud</em>",
        "En menos de 24 horas hábiles te escribimos por WhatsApp para agendar tu evaluación de revisoría fiscal. Si quieres adelantarte, escríbenos ahora.",
        f'<a class="lp-btn" data-wa-lead href="{_wa("Hola, acabo de pedir una evaluación de revisoría fiscal en su página")}" target="_blank" rel="noopener">{ICO["wa"]}Escribir por WhatsApp ahora</a>'),
    clase_body="lp", css_extra=CSS, landing=(),
))
