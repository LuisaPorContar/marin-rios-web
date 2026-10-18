# -*- coding: utf-8 -*-
"""Páginas de cotización: outsourcing contable y revisoría fiscal.

Son el destino de la intención "cotización" (antes repartida entre varias
páginas del blog). Indexables, con formulario que llega a la hoja de leads y
cuenta como Lead en Meta (ver formulario.py).
"""

from base import ICO, wa, heroe, encabezado, tarjetas_item, acordeon, cta_final, resenas_google, carrusel_clientes
from paginas import PAGINAS, schema_servicio
from formulario import formulario_leads


def _ciudades(servicio):
    base = "outsourcing-contable" if servicio == "outsourcing" else "revisoria-fiscal"
    nombre = "Outsourcing contable" if servicio == "outsourcing" else "Revisoría fiscal"
    enlaces = "".join(
        f'<a class="etiqueta-enlace" href="{base}-{slug}.html">{nombre} en {ciudad}</a>'
        for slug, ciudad in (("medellin", "Medellín"), ("pereira", "Pereira"), ("armenia", "Armenia"), ("manizales", "Manizales")))
    return f"""<section class="seccion--ajustada">
  <div class="contenedor">
    {encabezado("Cobertura", "Cotizamos en Medellín y el Eje Cafetero", "Visitas presenciales en Medellín, Pereira, Armenia y Manizales, y trabajo remoto en todo el país.", ancho="54rem", tam="var(--paso-4)")}
    <div class="directorio__lista revelar">{enlaces}</div>
  </div>
</section>"""


def _pasos(items):
    filas = "".join(f"""<li class="cot-paso revelar"><span class="cot-paso__num">{n:02d}</span><div><h3>{t}</h3><p>{d}</p></div></li>"""
                    for n, (t, d) in enumerate(items, 1))
    return f'<ol class="cot-pasos">{filas}</ol>'


# ================================================================
# COTIZACIÓN DE OUTSOURCING CONTABLE
# ================================================================
faq_cot_out = [
    ("¿Cuánto cuesta un outsourcing contable?",
     "Depende del volumen de facturas y movimientos, del número de empleados en nómina, de las obligaciones tributarias de la empresa y del estado en que esté la contabilidad. Por eso cotizamos con los datos de su operación y entregamos el valor por escrito."),
    ("¿La cotización tiene algún costo?",
     "No. Revisar su caso y enviarle la propuesta no tiene costo ni lo compromete a contratar."),
    ("¿Qué información necesitan para cotizar?",
     "Cuántas facturas emite y recibe al mes, cuántas personas tiene en nómina, qué impuestos declara (IVA, retención, ICA, renta), qué software contable usa y si hay meses atrasados por poner al día."),
    ("¿Cuánto tardan en enviar la cotización?",
     "Le escribimos por WhatsApp en menos de 24 horas hábiles para aclarar los datos que falten. Con esa información preparamos la propuesta por escrito."),
    ("¿Puedo cambiar de contador a mitad de año?",
     "Sí. Organizamos el empalme con el contador saliente para recibir libros, soportes y declaraciones sin que se pierda ningún vencimiento."),
    ("¿Atienden empresas fuera de Medellín?",
     "Sí. Tenemos atención presencial en Medellín, Pereira, Armenia y Manizales, y trabajamos de forma remota con empresas de todo el país."),
]

cuerpo_out = f"""
{heroe(
    "Cotización de outsourcing contable para su empresa",
    "Cuéntenos cómo opera su empresa y le enviamos una propuesta por escrito: alcance, entregables, responsable y honorarios. Sin costo y sin compromiso.",
    "reunion-cuadro.jpg",
    "Reunión de cotización de outsourcing contable con el equipo de Marín Ríos Consultores",
    chip="Cotización · Outsourcing contable",
    migas=[("Inicio", "index.html"), ("Outsourcing contable", "outsourcing-contable.html"), ("Cotización", None)],
    cta1=("Pedir mi cotización", "#cotizar"),
    cta2=("Escribir por WhatsApp", wa("Hola, quiero una cotización de outsourcing contable para mi empresa")),
    riel=[("$0", "La cotización no tiene costo"),
          ("24 h", "Respuesta en horas hábiles"),
          ("4", "Ciudades con atención presencial"),
          ("2 SMMLV", "Planes desde 2 salarios mínimos al mes")]
)}

<section class="seccion claro">
  <div class="contenedor">
    {encabezado("Qué tenemos en cuenta", "¿De qué depende el valor de un outsourcing contable?", "No cobramos por tarifa fija de catálogo: el valor sale de lo que su empresa realmente necesita cada mes.")}
    {tarjetas_item([
        ("documento", "Volumen de operaciones", "Cuántas facturas emite y recibe, cuántos movimientos bancarios y cuántas cuentas maneja."),
        ("gente", "Nómina", "Número de empleados, nómina electrónica, prestaciones y liquidaciones."),
        ("escudo", "Obligaciones tributarias", "IVA, retención en la fuente, ICA, renta, información exógena y régimen al que pertenece."),
        ("libro", "Estado de la contabilidad", "Si está al día o hay meses atrasados que poner en orden antes de arrancar."),
        ("engranaje", "Software y procesos", "El sistema contable que usa y cómo circulan hoy los soportes."),
        ("grafico", "Reportes que necesita", "Estados financieros mensuales, informes para socios o bancos y análisis de costos."),
    ])}
  </div>
</section>

<section class="seccion form-leads" id="cotizar">
  <div class="contenedor">
    {formulario_leads(
        formulario="Cotización Outsourcing Contable",
        oferta="Cotización outsourcing contable",
        servicio="outsourcing",
        titulo="Pida su cotización de outsourcing contable",
        texto="Toma menos de un minuto. Le escribimos por WhatsApp en menos de 24 horas hábiles para completar los datos y enviarle la propuesta.",
        boton="Pedir mi cotización",
        califica_todos=True,
        mensaje_wa="recibir una cotización de outsourcing contable")}
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    {encabezado("Qué recibe", "Lo que incluye la propuesta", "Un documento que puede comparar con cualquier otra oferta, punto por punto.")}
    {_pasos([
        ("Alcance del servicio", "Qué procesos asumimos: contabilidad, impuestos, nómina, conciliaciones y reportes."),
        ("Entregables y fechas", "Qué recibe cada mes y en qué fecha, incluido el calendario de declaraciones."),
        ("Plan de transición", "Cómo recibimos la información del contador actual y en cuánto tiempo queda al día."),
        ("Responsable y honorarios", "Quién lleva su cuenta y el valor mensual por escrito."),
    ])}
    <p class="centrado revelar" style="margin-top:2rem"><a class="etiqueta-enlace" href="cuanto-cuesta-contratar-un-servicio-de-outsourcing-contable.html">Qué hace subir o bajar el costo de un outsourcing contable{ICO['flecha_fina']}</a></p>
  </div>
</section>

{_ciudades("outsourcing")}

{carrusel_clientes()}

<section class="seccion claro">
  <div class="contenedor">
    <div class="fijo">
      <div class="fijo__ancla revelar">
        {encabezado("Preguntas frecuentes", "Sobre la cotización", ancho="none", tam="var(--paso-4)")}
      </div>
      {acordeon([(q, f"<p>{a}</p>") for q, a in faq_cot_out], prefijo="cot")}
    </div>
  </div>
</section>

{resenas_google()}

{cta_final(
    "¿Prefiere hablarlo directamente?",
    "Escríbanos por WhatsApp y le preparamos la cotización con un asesor.",
    boton="Escribir por WhatsApp",
    mensaje="Hola, quiero una cotización de outsourcing contable para mi empresa",
    secundario=("Conoce el servicio de outsourcing contable", "outsourcing-contable.html"),
)}

<script src="assets/js/lp-revisoria.js" defer></script>
"""

PAGINAS.append(dict(
    archivo="cotizacion-outsourcing-contable.html",
    titulo="Cotización de Outsourcing Contable sin Costo | Marín Ríos",
    descripcion="Pida una cotización de outsourcing contable para su empresa en Medellín o el Eje Cafetero: alcance, entregables y honorarios por escrito, sin costo.",
    activo="servicios",
    og_img="reunion-cuadro.jpg",
    schema=schema_servicio("Cotización de outsourcing contable",
                           "Cotización sin costo del servicio de outsourcing contable: contabilidad, impuestos, nómina y estados financieros NIIF.",
                           "cotizacion-outsourcing-contable/", faq_cot_out),
    cuerpo=cuerpo_out,
))


# ================================================================
# COTIZACIÓN DE REVISORÍA FISCAL
# ================================================================
faq_cot_rf = [
    ("¿Cuánto cobra un revisor fiscal?",
     "No hay una tarifa oficial. El valor depende del tamaño de la empresa, del sector, de la complejidad contable y de las horas de trabajo que exige la revisoría. Por eso cotizamos con los datos de su empresa y entregamos el valor por escrito."),
    ("¿La cotización tiene algún costo?",
     "No. Revisar su caso y enviarle la propuesta no tiene costo ni lo compromete a contratar."),
    ("¿Qué datos necesitan para cotizar la revisoría fiscal?",
     "Ingresos y activos del último cierre, tipo de sociedad, sector, número de empleados, si aplica NIIF plenas o para pymes, operaciones con el exterior y si está obligada a SAGRILAFT o PTEE."),
    ("¿Cuándo conviene pedir la cotización?",
     "Antes de la asamblea ordinaria del primer trimestre, que es donde se nombra o se cambia al revisor. Pedirla entre octubre y diciembre deja tiempo para comparar propuestas."),
    ("¿Mi empresa está obligada a tener revisor fiscal en 2027?",
     "Si a 31 de diciembre de 2026 sus activos brutos son iguales o superiores a $8.754.525.000 o sus ingresos brutos del año a $5.252.715.000, sí. Las sociedades anónimas siempre lo necesitan."),
    ("¿Atienden empresas fuera de Medellín?",
     "Sí. Tenemos atención presencial en Medellín, Pereira, Armenia y Manizales, y trabajamos de forma remota con empresas de todo el país."),
]

cuerpo_rf = f"""
{heroe(
    "Cotización de revisoría fiscal para su empresa",
    "Le enviamos una propuesta por escrito con alcance, horas de trabajo, equipo asignado y honorarios, lista para presentar en su asamblea. Sin costo y sin compromiso.",
    "reunion-duotono.jpg",
    "Revisores fiscales de Marín Ríos Consultores preparando una cotización",
    chip="Cotización · Revisoría fiscal",
    migas=[("Inicio", "index.html"), ("Revisoría fiscal", "revisoria-fiscal.html"), ("Cotización", None)],
    cta1=("Pedir mi cotización", "#cotizar"),
    cta2=("Escribir por WhatsApp", wa("Hola, quiero una cotización de revisoría fiscal para mi empresa")),
    riel=[("$0", "La cotización no tiene costo"),
          ("2027", "Topes de obligación actualizados"),
          ("NIA", "Normas de aseguramiento"),
          ("4", "Ciudades con atención presencial")]
)}

<section class="seccion claro">
  <div class="contenedor">
    {encabezado("Qué tenemos en cuenta", "¿De qué depende el valor de una revisoría fiscal?", "La revisoría se cotiza por el trabajo que exige su empresa, no por una tarifa de catálogo.")}
    {tarjetas_item([
        ("grafico", "Tamaño de la empresa", "Ingresos y activos del último cierre, número de sedes y de empleados."),
        ("documento", "Complejidad contable", "NIIF plenas o para pymes, consolidación, inventarios y operaciones con el exterior."),
        ("escudo", "Riesgo y regulación", "Sector vigilado, SAGRILAFT, PTEE y requerimientos abiertos con la DIAN o las superintendencias."),
        ("reloj", "Horas y visitas", "Cuántas horas al mes y cuántas visitas presenciales exige un trabajo serio durante todo el año."),
        ("gente", "Equipo asignado", "Revisor principal, suplente y profesionales de apoyo con nombre propio."),
        ("libro", "Informes que necesita", "Informes periódicos a la gerencia y la junta, dictamen e informe a la asamblea."),
    ])}
    <p class="centrado revelar" style="margin-top:2rem"><a class="etiqueta-enlace" href="cuanto-cobra-un-revisor-fiscal-en-colombia.html">Cómo se fijan los honorarios de un revisor fiscal en Colombia{ICO['flecha_fina']}</a></p>
  </div>
</section>

<section class="seccion form-leads" id="cotizar">
  <div class="contenedor">
    {formulario_leads(
        formulario="Cotización Revisoría Fiscal",
        oferta="Cotización revisoría fiscal",
        servicio="revisoria",
        titulo="Pida su cotización de revisoría fiscal",
        texto="Toma menos de un minuto. Le escribimos por WhatsApp en menos de 24 horas hábiles para completar los datos y enviarle la propuesta.",
        boton="Pedir mi cotización",
        mensaje_wa="recibir una cotización de revisoría fiscal")}
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    {encabezado("Qué recibe", "Lo que incluye la propuesta", "Un documento comparable con cualquier otra oferta, listo para presentar a sus socios.")}
    {_pasos([
        ("Alcance y metodología", "Qué revisamos durante el año y con qué normas de aseguramiento."),
        ("Horas y calendario de visitas", "Cuántas horas dedicamos al mes y cuándo visitamos la empresa."),
        ("Equipo con nombre propio", "Revisor principal, suplente y equipo de apoyo."),
        ("Honorarios por escrito", "El valor, la forma de pago y lo que incluye y no incluye."),
    ])}
    <p class="centrado revelar" style="margin-top:2rem"><a class="etiqueta-enlace" href="como-elegir-firma-revisoria-fiscal.html">8 criterios para comparar propuestas de revisoría fiscal{ICO['flecha_fina']}</a></p>
  </div>
</section>

{_ciudades("revisoria")}

{carrusel_clientes()}

<section class="seccion claro">
  <div class="contenedor">
    <div class="fijo">
      <div class="fijo__ancla revelar">
        {encabezado("Preguntas frecuentes", "Sobre la cotización de revisoría fiscal", ancho="none", tam="var(--paso-4)")}
      </div>
      {acordeon([(q, f"<p>{a}</p>") for q, a in faq_cot_rf], prefijo="cotrf")}
    </div>
  </div>
</section>

{resenas_google()}

{cta_final(
    "¿Prefiere hablarlo directamente?",
    "Escríbanos por WhatsApp y un revisor le prepara la cotización.",
    boton="Escribir por WhatsApp",
    mensaje="Hola, quiero una cotización de revisoría fiscal para mi empresa",
    secundario=("Conoce el servicio de revisoría fiscal", "revisoria-fiscal.html"),
)}

<script src="assets/js/lp-revisoria.js" defer></script>
"""

PAGINAS.append(dict(
    archivo="cotizacion-revisoria-fiscal.html",
    titulo="Cotización de Revisoría Fiscal sin Costo | Marín Ríos",
    descripcion="Pida una cotización de revisoría fiscal en Medellín o el Eje Cafetero: alcance, horas, equipo y honorarios por escrito para su asamblea. Sin costo.",
    activo="servicios",
    og_img="reunion-duotono.jpg",
    schema=schema_servicio("Cotización de revisoría fiscal",
                           "Cotización sin costo del servicio de revisoría fiscal bajo normas de aseguramiento, para empresas obligadas o que quieren cambiar de revisor.",
                           "cotizacion-revisoria-fiscal/", faq_cot_rf),
    cuerpo=cuerpo_rf,
))
