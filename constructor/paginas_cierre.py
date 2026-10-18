# -*- coding: utf-8 -*-
"""Asesoría de cierre contable y fiscal: página de servicio para la temporada octubre-marzo.

Destino de las búsquedas "asesoría de cierre contable", "cierre contable de fin de año
asesoría" y "asesoría de cierre contable y fiscal en Bogotá". Los artículos del blog
sobre cierre (qué es, lista de tareas 2026) enlazan aquí.
"""

from base import ICO, wa, heroe, encabezado, tarjetas_item, acordeon, cta_final, resenas_google, fijo
from paginas import PAGINAS, schema_servicio
from paginas_cotizacion import _pasos
from formulario import formulario_leads


faq_cierre = [
    ("¿Pueden hacer solo el cierre si ya tengo contador?",
     "Sí. Trabajamos con su contador: revisamos las cifras, proponemos los ajustes y dejamos listos los estados financieros y el soporte del cierre fiscal. Su contador sigue con la operación del mes."),
    ("¿Cuándo conviene empezar el cierre contable?",
     "En octubre o noviembre. Así hay tiempo de conciliar, corregir y planear los impuestos antes del 31 de diciembre. En enero solo se puede documentar lo que ya pasó."),
    ("¿Qué diferencia hay entre el cierre contable y el cierre fiscal?",
     "El cierre contable deja los estados financieros bajo NIIF. El cierre fiscal toma esas cifras y las depura con las reglas tributarias para la declaración de renta. Los dos se hacen sobre la misma información, por eso conviene prepararlos juntos."),
    ("¿Cuánto cuesta la asesoría de cierre?",
     "Depende del volumen de operaciones, del estado de la contabilidad y de si el cierre incluye la preparación de la renta. Revisamos su caso sin costo y le enviamos la propuesta por escrito."),
    ("¿Atienden empresas de Bogotá y otras ciudades?",
     "Sí. En Bogotá y el resto del país trabajamos de forma virtual, y en Medellín, Pereira, Armenia y Manizales también con visitas programadas."),
    ("¿Qué pasa si mi contabilidad está atrasada?",
     "Empezamos por ponerla al día. Con un atraso de varios meses el cierre toma más tiempo, así que entre antes empiece, mejor."),
]

cuerpo = f"""
{heroe(
    "Asesoría de cierre contable y fiscal para empresas",
    "Cerramos el año con su empresa: conciliaciones, ajustes NIIF, estados financieros y el cierre fiscal para la renta. Para que llegue a la asamblea con cifras que se pueden sustentar.",
    "detalle-documentos.jpg",
    "Asesoría de cierre contable y fiscal de Marín Ríos Consultores",
    chip="Servicio · Cierre contable 2026",
    migas=[("Inicio", "index.html"), ("Outsourcing contable", "outsourcing-contable.html"), ("Cierre contable", None)],
    cta1=("Pedir mi propuesta", "#cotizar"),
    cta2=("Escribir por WhatsApp", wa("Hola, necesito asesoría para el cierre contable de mi empresa")),
    riel=[("Oct – Mar", "Del precierre a la asamblea"),
          ("NIIF", "Estados financieros bajo norma"),
          ("$0", "El diagnóstico no tiene costo"),
          ("Virtual", "Bogotá y todo el país")]
)}

<section class="seccion claro">
  <div class="contenedor">
    {encabezado("Para quién es", "¿Cuándo necesita una asesoría de cierre contable?", "El cierre es el momento en que se ve si la contabilidad del año aguanta una revisión. Estas son las situaciones en las que más ayudamos:")}
    {tarjetas_item([
        ("gente", "No tiene contador interno", "Una persona externa le lleva los libros, pero nadie revisa el cierre a fondo ni planea los impuestos del año."),
        ("lupa", "Su contador necesita apoyo", "La operación del mes está bien, pero el cierre exige ajustes NIIF, impuesto diferido y conciliación fiscal."),
        ("documento", "Cambió de contador", "Recibe la contabilidad a mitad de año y necesita saber en qué estado está antes de firmar el cierre."),
        ("escudo", "Tiene revisor fiscal o socios exigentes", "Necesita cifras soportadas para el dictamen, la asamblea, el banco o un inversionista."),
    ])}
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    {encabezado("Qué incluye", "Lo que hacemos en el cierre", "Cada etapa termina con un entregable concreto:")}
    {_pasos([
        ("Precierre (octubre – noviembre)", "Revisamos saldos, cartera, inventarios y soportes, y le decimos qué hay que corregir y qué decisiones tributarias quedan por tomar antes del 31 de diciembre."),
        ("Conciliaciones y ajustes", "Bancos, cartera, proveedores, inventario físico, depreciaciones, deterioro y provisiones, con cada ajuste documentado."),
        ("Cierre fiscal", "Depuración de la renta a partir de las cifras contables, diferencias entre lo contable y lo fiscal e impuesto diferido."),
        ("Estados financieros para la asamblea", "Balance, resultados, flujo de efectivo, cambios en el patrimonio y notas, listos para la reunión ordinaria."),
        ("Lo que sigue en enero", "Certificados para empleados y proveedores, nómina del cierre e información para la exógena, sin cabos sueltos."),
    ])}
  </div>
</section>

<section class="seccion form-leads" id="cotizar">
  <div class="contenedor">
    {formulario_leads(
        formulario="Asesoría Cierre Contable",
        oferta="Asesoría de cierre contable 2026",
        servicio="outsourcing",
        titulo="Pida su propuesta para el cierre 2026",
        texto="Toma menos de un minuto. Le escribimos por WhatsApp en menos de 24 horas hábiles para conocer el estado de su contabilidad y enviarle la propuesta.",
        boton="Pedir mi propuesta",
        califica_todos=True,
        mensaje_wa="recibir una propuesta de asesoría para el cierre contable 2026",
        legal="esta propuesta")}
  </div>
</section>

<section class="seccion claro">
  {fijo(
    encabezado("Guías del cierre", "Antes de empezar, lea esto",
               "Explicamos el cierre paso a paso en el blog. Si prefiere que lo hagamos con usted, pida la propuesta arriba.",
               ancho="none", tam="var(--paso-4)"),
    [
        ("Qué es el cierre contable y cómo se hace", '<a href="cierre-contable-empresas.html">Guía del cierre contable y fiscal</a>: pasos, diferencias entre lo contable y lo fiscal y errores frecuentes.'),
        ("Lista de tareas del cierre 2026", '<a href="preparar-cierre-contable-2026.html">Cómo preparar el cierre contable 2026</a>: qué hacer en cada mes, de octubre a marzo.'),
        ("El revisor fiscal en el cierre", '<a href="revisor-fiscal-cierre-contable.html">Qué revisa el revisor fiscal en el cierre</a> y qué conviene tener listo para el dictamen.'),
        ("Lo que se viene en 2027", '<a href="calendario-tributario-2027.html">Calendario tributario 2027</a>: qué se sabe y qué preparar desde ya.'),
    ]
  )}
</section>

<section class="seccion">
  <div class="contenedor">
    <div class="fijo">
      <div class="fijo__ancla revelar">
        {encabezado("Preguntas frecuentes", "Sobre la asesoría de cierre", ancho="none", tam="var(--paso-4)")}
      </div>
      {acordeon([(q, f"<p>{a}</p>") for q, a in faq_cierre], prefijo="cie")}
    </div>
  </div>
</section>

{resenas_google()}

{cta_final(
    "¿Quiere cerrar el año sin sorpresas?",
    "Escríbanos por WhatsApp y revisamos cómo va la contabilidad de su empresa antes del 31 de diciembre.",
    boton="Escribir por WhatsApp",
    mensaje="Hola, necesito asesoría para el cierre contable de mi empresa",
    secundario=("Conoce el servicio de outsourcing contable", "outsourcing-contable.html"),
)}

<script src="assets/js/lp-revisoria.js" defer></script>
"""

PAGINAS.append(dict(
    archivo="asesoria-cierre-contable.html",
    titulo="Asesoría de Cierre Contable y Fiscal 2026 | Marín Ríos",
    descripcion="Asesoría de cierre contable y fiscal 2026 para empresas: conciliaciones, ajustes NIIF, estados financieros y cierre fiscal. Medellín, Eje Cafetero y Bogotá.",
    activo="servicios",
    og_img="detalle-documentos.jpg",
    schema=schema_servicio("Asesoría de cierre contable y fiscal",
                           "Cierre contable y fiscal de fin de año para empresas en Colombia: precierre, conciliaciones, ajustes NIIF, cierre fiscal y estados financieros.",
                           "asesoria-cierre-contable/", faq_cierre),
    cuerpo=cuerpo,
))
