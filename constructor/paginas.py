# -*- coding: utf-8 -*-
"""Contenido de las páginas de servicio, precios y blog."""

from base import (ICO, wa, plantilla, heroe, encabezado, servicios_num, fijo,
                  carrusel, acordeon, tarjetas_item, ciudades_grid, directorio,
                  cta_final, proposito, marcas, TEL, TEL_URI, EMAIL,
                  resenas_google)

import json

TRIO = [
    ("01 — Contable", "Gestión contable",
     "Externaliza toda tu operación contable: registros, conciliaciones, impuestos y reportes. Menos carga interna, más control financiero.",
     None, "Quiero este servicio", "outsourcing-contable.html"),
    ("02 — Financiero", "Consultoría financiera",
     "Toma decisiones basadas en datos. Analizamos tus finanzas, rentabilidad, flujo de caja y proyecciones.",
     None, "Quiero este servicio", "consultoria-financiera.html"),
    ("03 — Fiscal", "Revisoría fiscal",
     "Asegura el cumplimiento legal y protege tu empresa frente a riesgos fiscales. Revisión independiente y reportes confiables.",
     None, "Quiero este servicio", "revisoria-fiscal.html"),
]


def schema_servicio(nombre, descripcion, url, faqs=None):
    g = [{
        "@type": "Service",
        "name": nombre,
        "description": descripcion,
        "serviceType": nombre,
        "provider": {"@type": "AccountingService", "name": "Marín Ríos Consultores",
                     "@id": "https://marinriosconsultores.com/#empresa"},
        "areaServed": [{"@type": "City", "name": c} for c in ("Medellín", "Armenia", "Pereira", "Manizales")],
        "url": "https://marinriosconsultores.com/" + url
    }]
    if faqs:
        g.append({
            "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]
        })
    return json.dumps({"@context": "https://schema.org", "@graph": g}, ensure_ascii=False, indent=2)


PAGINAS = []


# ================================================================
# OUTSOURCING CONTABLE
# ================================================================
faq_out = [
    ("¿Qué es un outsourcing contable?",
     "Es delegar la operación contable de tu empresa a una firma externa especializada. En lugar de sostener un área interna, un equipo de contadores asume registros, conciliaciones, impuestos, nómina y reportes, y responde por el cumplimiento mes a mes."),
    ("¿Qué incluye el servicio de outsourcing contable?",
     "Contabilidad general y libros oficiales, conciliaciones bancarias, cuentas por cobrar y pagar, liquidación y presentación de impuestos, nómina electrónica, estados financieros bajo NIIF y acompañamiento en requerimientos de la DIAN."),
    ("¿Cuánto cuesta el outsourcing contable en Colombia?",
     "Depende del volumen de transacciones, el número de empleados en nómina y los servicios incluidos. Revisamos tu operación sin costo y te enviamos una cotización a la medida de tu empresa."),
    ("¿Cuánto tarda la transición desde mi contador actual?",
     "Entre 15 y 30 días. Hacemos un diagnóstico del estado real de la información, migramos saldos y soportes, y asumimos la operación desde el siguiente cierre mensual sin interrumpir tus obligaciones."),
    ("¿Qué pasa si mi contabilidad está atrasada?",
     "Es el escenario más común. Primero cuantificamos el atraso y el riesgo abierto frente a la DIAN, luego ejecutamos un plan de puesta al día con fechas concretas y después entramos en la operación mensual normal."),
]

cuerpo = f"""
{heroe(
    "Outsourcing contable para empresas en Colombia",
    "Delegamos de tu lado la operación completa: registros, impuestos, nómina y reportes. Tú recibes una contabilidad al día y cifras que sirven para decidir.",
    "reunion-ancho.jpg",
    "Equipo contable de Marín Ríos Consultores revisando estados financieros",
    chip="Servicio · Outsourcing contable",
    migas=[("Inicio", "index.html"), ("Servicios", None), ("Outsourcing contable", None)],
    cta1=("Agenda una asesoría", wa("Hola, quiero cotizar el servicio de outsourcing contable para mi empresa")),
    cta2=("Ver planes", "precios-outsourcing-contable.html"),
    riel=[("+50", "Empresas con su contabilidad tercerizada"),
          ("15 días", "Tiempo promedio de transición"),
          ("100%", "Cumplimiento del calendario DIAN"),
          ("NIIF", "Estados financieros bajo estándar pleno y pymes")]
)}

{marcas()}

<section class="seccion claro">
  <div class="contenedor">
    {encabezado("Qué resolvemos", "Si tu contabilidad no te da respuestas, el problema no es el software", "Cuando la información llega tarde o incompleta, las decisiones se toman a ciegas. Estas son las señales que vemos en el 90% de las empresas que llegan a nosotros.")}
    {tarjetas_item([
        ("reloj", "Cierres que llegan tarde", "Te enteras del resultado de enero en marzo, cuando ya no puedes hacer nada al respecto."),
        ("documento", "Impuestos sobre la hora", "Las declaraciones se preparan el último día, con el riesgo de error y sanción que eso implica."),
        ("lupa", "Cifras que no cuadran", "Los saldos de bancos, cartera y proveedores no coinciden con la realidad del negocio."),
        ("gente", "Dependencia de una sola persona", "Si tu contador se enferma o renuncia, la operación se detiene y el conocimiento se va."),
        ("candado", "Requerimientos sin respuesta", "Llega un oficio de la DIAN y nadie sabe con certeza qué soportes existen."),
        ("grafico", "Contabilidad sin lectura", "Recibes un balance, pero nadie te explica qué significa ni qué deberías hacer."),
    ])}
  </div>
</section>

<section class="seccion">
  {fijo(
    encabezado("Alcance del servicio", "¿Qué incluye nuestro outsourcing contable?",
               "Todo lo que aparece aquí está incluido en el plan mensual. Sin cobros por consulta ni sorpresas al cierre del año.",
               ancho="none", tam="var(--paso-4)"),
    [
        ("Contabilidad general y libros oficiales", "Registro de toda la operación bajo NIIF, con libros al día y trazabilidad completa de cada movimiento."),
        ("Conciliaciones bancarias", "Cruce mensual de extractos contra contabilidad para que los saldos de caja y bancos sean reales."),
        ("Cuentas por cobrar y por pagar", "Control de cartera y proveedores, con reportes de vencimientos para proteger tu flujo de caja."),
        ("Impuestos nacionales y territoriales", "IVA, retención en la fuente, ICA, renta y demás obligaciones preparadas y presentadas dentro del calendario."),
        ("Nómina electrónica y seguridad social", "Liquidación de nómina, prestaciones, aportes y transmisión del documento soporte a la DIAN."),
        ("Estados financieros con lectura", "Balance, resultados y flujo de caja acompañados de una explicación de qué está pasando y por qué."),
        ("Atención de requerimientos DIAN", "Respuesta a oficios, cruces de información y acompañamiento en fiscalizaciones."),
        ("Reunión periódica de seguimiento", "Un espacio fijo con tu contador para revisar cifras, alertas y decisiones del mes."),
    ]
  )}
</section>

{proposito(
    "Un equipo contable completo, sin cargar una nómina",
    "Contratar outsourcing contable te permite tener expertos manejando tus finanzas sin sostener un área interna. Obtienes procesos más eficientes, reportes útiles y cumplimiento garantizado.",
    "Es una forma de ahorrar tiempo, reducir errores y ganar claridad real sobre tu empresa mientras te enfocas en crecer.",
    mensaje="Hola, quiero saber cómo funciona el outsourcing contable para mi empresa"
)}

<section class="seccion oscuro degradado">
  {carrusel(
    "Proceso outsourcing contable",
    "¿Cómo trabajamos contigo?",
    "Cuatro etapas con entregables concretos. Sabes en todo momento en cuál estás y qué sigue.",
    [
        ("Paso 01", "Diagnóstico inicial", "Revisamos el estado real de tu contabilidad, tus obligaciones pendientes y los riesgos abiertos frente a la DIAN. Te entregamos un informe con hallazgos."),
        ("Paso 02", "Organización documental", "Ordenamos soportes, libros y saldos para partir de una base confiable y auditable. Migramos la información de tu contador anterior."),
        ("Paso 03", "Gestión mensual", "Asumimos registros, conciliaciones, impuestos y nómina dentro del calendario tributario, con fechas de entrega comprometidas."),
        ("Paso 04", "Acompañamiento permanente", "Informes, reuniones periódicas y alertas anticipadas para que decides con información al día y sin sorpresas."),
    ],
    etiqueta="Etapas del proceso"
  )}
</section>

<section class="seccion claro">
  <div class="contenedor">
    {encabezado("Otros servicios", "Combina el outsourcing con lo que tu empresa necesite", "Muchas empresas empiezan por la gestión contable y suman revisoría fiscal o consultoría financiera cuando crecen.")}
    {servicios_num(TRIO)}
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    <div class="fijo">
      <div class="fijo__ancla revelar">
        {encabezado("Preguntas frecuentes", "Lo que preguntan antes de contratar", "Si tu duda no está aquí, escríbenos y te respondemos con un caso concreto.", ancho="none", tam="var(--paso-4)")}
      </div>
      {acordeon([(q, f"<p>{a}</p>") for q, a in faq_out], prefijo="oc")}
    </div>
  </div>
</section>

<section class="seccion claro">
  <div class="contenedor">
    {encabezado("Cobertura", "Outsourcing contable por ciudad", ancho="54rem", tam="var(--paso-4)")}
    {ciudades_grid()}
  </div>
</section>

{resenas_google()}

{cta_final(
    "¿Listo para dejar de perseguir tu contabilidad?",
    "Cuéntanos en qué estado está hoy y te decimos con claridad qué necesita tu empresa y cuánto costaría.",
    mensaje="Hola, quiero cotizar el servicio de outsourcing contable"
)}
"""

PAGINAS.append(dict(
    archivo="outsourcing-contable.html",
    titulo="Outsourcing Contable en Colombia para Pymes | Marín Ríos",
    descripcion=f"Outsourcing contable para empresas en Colombia: contabilidad, impuestos, nómina y estados financieros NIIF. Cotización a la medida de tu empresa.",
    activo="servicios",
    og_img="reunion-ancho.jpg",
    schema=schema_servicio("Outsourcing contable",
                           "Servicio integral de contabilidad, impuestos, nómina y reportes financieros para pymes en Colombia.",
                           "outsourcing-contable/", faq_out),
    cuerpo=cuerpo,
))


# ================================================================
# REVISORÍA FISCAL
# ================================================================
faq_rev = [
    ("¿Qué es la revisoría fiscal en Colombia?",
     "Es un órgano de fiscalización independiente, regulado por el Código de Comercio y la Ley 43 de 1990, cuya función es dictaminar sobre la razonabilidad de los estados financieros y velar por que la sociedad cumpla la ley, los estatutos y las decisiones de sus órganos de gobierno."),
    ("¿Quiénes pueden ejercer como revisores fiscales en Colombia?",
     "Únicamente contadores públicos con tarjeta profesional vigente expedida por la Junta Central de Contadores, que no estén incursos en las inhabilidades e incompatibilidades del artículo 205 del Código de Comercio. También pueden ejercer las firmas de contadores debidamente inscritas."),
    ("¿Qué empresas están obligadas a tener revisor fiscal?",
     "Las sociedades por acciones y las sucursales de sociedades extranjeras siempre. Las demás sociedades cuando al 31 de diciembre del año anterior sus activos brutos superen 5.000 SMMLV o sus ingresos brutos superen 3.000 SMMLV. También aplica por mandato estatutario o de la asamblea."),
    ("¿Cuáles son las funciones y responsabilidades de un revisor fiscal?",
     "Dictaminar los estados financieros, verificar que las operaciones se ajusten a los estatutos y a las decisiones de la asamblea y la junta directiva, velar por la conservación de los bienes sociales, colaborar con las entidades de vigilancia y control, y dar cuenta oportuna de las irregularidades que encuentre."),
    ("¿Cómo se elige a un revisor fiscal en una empresa?",
     "Lo elige la asamblea general de accionistas o la junta de socios por mayoría absoluta, para el período fijado en los estatutos. La designación se inscribe en el registro mercantil de la Cámara de Comercio para que sea oponible a terceros."),
    ("¿Qué normativas regulan la revisoría fiscal en Colombia?",
     "El Código de Comercio (artículos 203 a 217), la Ley 43 de 1990, la Ley 1314 de 2009 y los decretos que adoptan las Normas de Aseguramiento de la Información (NIA), además de la doctrina del Consejo Técnico de la Contaduría Pública."),
    ("¿Qué es el informe del revisor fiscal y qué debe contener?",
     "Es el dictamen que se presenta a la asamblea. Debe indicar si los estados financieros presentan razonablemente la situación financiera, si la contabilidad se lleva conforme a las normas, si las operaciones se ajustan a los estatutos y a la ley, y si el control interno y la conservación de los bienes son adecuados."),
    ("¿Cuál es la diferencia entre revisoría fiscal y auditoría externa?",
     "La revisoría fiscal es una figura obligatoria y permanente creada por la ley colombiana, con función de fiscalización integral y fe pública. La auditoría externa es voluntaria, contractual, se enfoca en un alcance definido por el cliente y no otorga fe pública."),
]

cuerpo = f"""
{heroe(
    "Empresas de revisoría fiscal en Colombia",
    "Demuestra que tu información contable es fiable y libre de errores, con un dictamen independiente que da confianza a socios, bancos y entidades de control.",
    "reunion-duotono.jpg",
    "Revisores fiscales de Marín Ríos Consultores auditando estados financieros",
    chip="Servicio · Revisoría fiscal",
    migas=[("Inicio", "index.html"), ("Servicios", None), ("Revisoría fiscal", None)],
    cta1=("Quiero una asesoría", wa("Hola, quiero una asesoría sobre el servicio de revisoría fiscal")),
    cta2=("Ver planes", "precios-outsourcing-contable.html"),
    riel=[("Ley 43", "Ejercicio profesional bajo la Ley 43 de 1990"),
          ("Art. 203", "Código de Comercio: obligación de revisor fiscal"),
          ("NIA", "Normas Internacionales de Auditoría aplicadas"),
          ("+50", "Empresas acompañadas")]
)}

<section class="seccion claro">
  <div class="contenedor">
    {encabezado("¿Te está pasando esto?", "¿Buscas asesoría fiscal para tu pyme?", "Si te identificas con alguna de estas situaciones, tu empresa necesita una revisión independiente.")}
    {tarjetas_item([
        ("lupa", "Dudas sobre los estatutos", "Crees que las operaciones de tu negocio no se ajustan a lo que dicen los estatutos de la sociedad."),
        ("escudo", "Necesitas dar confianza", "Quieres brindar mayor seguridad a tus socios, inversionistas o entidades financieras."),
        ("documento", "Superaste los topes", "Cumples con los requisitos de activos o ingresos que te obligan legalmente a tener revisor fiscal."),
    ])}
  </div>
</section>

<section class="seccion">
  {fijo(
    encabezado("Auditoría fiscal", "¿Qué importancia tiene la revisoría fiscal en tu negocio?",
               "El revisor fiscal no es un gasto de cumplimiento: es la figura que protege el patrimonio de los socios y la reputación de la empresa.",
               ancho="none", tam="var(--paso-4)"),
    [
        ("Das fe sobre tus estados financieros", "Un dictamen independiente confirma que las cifras que presentas reflejan razonablemente la realidad de la compañía."),
        ("Facilitas la vigilancia y el control", "Colaboras con las entidades gubernamentales entregando información oportuna y verificada, lo que reduce fricción en cualquier inspección."),
        ("Cumples las leyes y los estatutos", "Verificamos que las decisiones y operaciones se ajusten a lo que exigen la norma y los órganos de gobierno de la sociedad."),
        ("Adviertes irregularidades a tiempo", "Damos cuenta oportuna a la asamblea y a la junta de socios sobre cualquier irregularidad en el funcionamiento de la sociedad."),
        ("Proteges los bienes sociales", "Inspeccionamos los activos de la compañía y procuramos que se conserven y se usen conforme a su destinación."),
        ("Fortaleces tu control interno", "Cada hallazgo viene con una recomendación concreta para cerrar la brecha que lo produjo."),
    ]
  )}
</section>

<section class="seccion oscuro degradado">
  {carrusel(
    "Consultoría contable y fiscal",
    "¿Qué hacemos en tu revisoría fiscal?",
    "Un plan de trabajo anual con pruebas documentadas, no una firma al final del ejercicio.",
    [
        ("01", "Auditamos tus estados financieros", "Verificamos que las operaciones se ajusten a las prescripciones estatutarias y a las decisiones de la junta directiva y la asamblea general."),
        ("02", "Inspeccionamos los bienes de la sociedad", "Revisamos la existencia y el estado de los activos, y procuramos que se adopten las medidas para su conservación y seguridad."),
        ("03", "Velamos por la regularidad", "Autorizamos con nuestra firma los estados financieros en las sociedades donde es obligatorio tener revisor fiscal."),
        ("04", "Reportamos a los órganos de control", "Rendimos los informes que exigen la ley y los estatutos, y damos cuenta oportuna de las irregularidades detectadas."),
    ],
    etiqueta="Funciones de la revisoría fiscal"
  )}
</section>

{proposito(
    "Un revisor fiscal que sí revisa",
    "Prestamos servicios de contabilidad, auditoría y asesoría fiscal para pymes. Nuestro trabajo se documenta bajo Normas Internacionales de Auditoría y se sustenta con papeles de trabajo.",
    "Cada hallazgo llega con su recomendación, y cada informe se explica en una reunión con los socios. Sin lenguaje técnico innecesario.",
    boton="Obtén tu asesoría aquí",
    mensaje="Hola, quiero una asesoría con un experto en revisoría fiscal",
    flotante_a=("NIA", "Normas de auditoría aplicadas"),
    flotante_b=("Anual", "Plan de trabajo documentado")
)}

<section class="seccion">
  <div class="contenedor">
    <div class="fijo">
      <div class="fijo__ancla revelar">
        {encabezado("Preguntas que quizás te estás haciendo", "Revisoría fiscal en Colombia, sin letra pequeña", "Las respuestas se apoyan en el Código de Comercio, la Ley 43 de 1990 y las Normas de Aseguramiento de la Información.", ancho="none", tam="var(--paso-4)")}
      </div>
      {acordeon([(q, f"<p>{a}</p>") for q, a in faq_rev], prefijo="rf")}
    </div>
  </div>
</section>

<section class="seccion claro">
  <div class="contenedor">
    {encabezado("Otros servicios", "Revisoría fiscal, contabilidad y finanzas en un mismo equipo")}
    {servicios_num(TRIO)}
  </div>
</section>

{resenas_google()}

{cta_final(
    "Obtén tu asesoría con un experto especializado",
    "Cuéntanos el tamaño de tu sociedad y te decimos si estás obligado a tener revisor fiscal y qué alcance necesitas.",
    boton="Quiero información",
    mensaje="Hola, quiero información sobre el servicio de revisoría fiscal"
)}
"""

PAGINAS.append(dict(
    archivo="revisoria-fiscal.html",
    titulo="Servicio de Revisoría Fiscal en Colombia | Marín Ríos",
    descripcion=f"Firma de revisoría fiscal en Colombia. Dictamen independiente bajo NIA, cumplimiento del Código de Comercio y reportes confiables. Cotización a la medida.",
    activo="servicios",
    og_img="reunion-duotono.jpg",
    schema=schema_servicio("Revisoría fiscal",
                           "Servicio de revisoría fiscal y auditoría independiente para sociedades en Colombia, conforme al Código de Comercio y las Normas de Aseguramiento de la Información.",
                           "revisoria-fiscal/", faq_rev),
    cuerpo=cuerpo,
))


# ================================================================
# CONSULTORÍA FINANCIERA
# ================================================================
faq_fin = [
    ("¿Qué es la consultoría financiera para empresas?",
     "Es un servicio de análisis y acompañamiento que traduce tu información contable en decisiones: dónde estás perdiendo margen, cuánto efectivo vas a necesitar, qué precio deberías cobrar y si un crecimiento es sostenible o te va a ahogar el flujo de caja."),
    ("¿En qué se diferencia de la contabilidad?",
     "La contabilidad registra lo que ya pasó y cumple con la norma. La consultoría financiera usa esa información para proyectar lo que viene y recomendar qué hacer. Una mira hacia atrás, la otra hacia adelante."),
    ("¿Qué entregables recibo?",
     "Un diagnóstico financiero inicial, un modelo de flujo de caja proyectado, análisis de rentabilidad por línea de negocio o producto, indicadores clave con sus metas, y una reunión mensual para revisar desviaciones y ajustar."),
    ("¿Sirve si mi empresa es pequeña?",
     "Sí. De hecho es donde más impacto tiene, porque las pymes suelen tomar decisiones de precio, endeudamiento y contratación por intuición. Un modelo financiero sencillo y bien construido cambia esas decisiones."),
    ("¿Cuánto cuesta la consultoría financiera?",
     "El valor depende del número de líneas de negocio a analizar y de si se requiere construir el modelo financiero desde cero. Revisamos tu caso y te enviamos una cotización a la medida."),
]

cuerpo = f"""
{heroe(
    "Consultoría financiera para empresas que quieren decidir con datos",
    "Analizamos tu rentabilidad, tu flujo de caja y tus proyecciones para que dejes de decidir por intuición y empieces a decidir por cifras.",
    "detalle-documentos.jpg",
    "Análisis financiero y proyecciones sobre documentos contables",
    chip="Servicio · Consultoría financiera",
    migas=[("Inicio", "index.html"), ("Servicios", None), ("Consultoría financiera", None)],
    cta1=("Quiero este servicio", wa("Hola, quiero cotizar el servicio de consultoría financiera")),
    cta2=("Ver planes", "precios-outsourcing-contable.html"),
    riel=[("Diagnóstico", "Lectura financiera inicial de tu empresa"),
          ("12 meses", "Horizonte de proyección del flujo de caja"),
          ("Mensual", "Reunión de seguimiento con indicadores"),
          ("+50", "Empresas acompañadas")]
)}

<section class="seccion claro">
  <div class="contenedor">
    {encabezado("El problema", "Tu empresa factura, pero no sabes si gana", "Facturar no es ganar, y tener caja no es ser rentable. Estas son las preguntas que resolvemos.")}
    {tarjetas_item([
        ("barras", "¿Cuál producto deja margen?", "Analizamos la rentabilidad real por línea, producto o cliente, con costos indirectos asignados de forma correcta."),
        ("reloj", "¿Me va a alcanzar la caja?", "Construimos un flujo de caja proyectado a 12 meses para anticipar los meses apretados antes de que lleguen."),
        ("grafico", "¿A qué precio debo vender?", "Modelamos estructura de costos y punto de equilibrio para fijar precios que sostengan la operación."),
        ("engranaje", "¿Puedo asumir este crecimiento?", "Evaluamos si una nueva contratación, sede o línea es viable con tu capacidad financiera actual."),
        ("candado", "¿Me conviene endeudarme?", "Comparamos el costo de la deuda contra el retorno esperado antes de que firmes con el banco."),
        ("escudo", "¿Cómo mejoro mi margen?", "Identificamos fugas de dinero y sobrecostos que la contabilidad registra pero nadie está leyendo."),
    ])}
  </div>
</section>

<section class="seccion">
  {fijo(
    encabezado("Alcance", "¿Qué incluye la consultoría financiera?",
               "Un modelo financiero propio de tu empresa, no una plantilla genérica.",
               ancho="none", tam="var(--paso-4)"),
    [
        ("Diagnóstico financiero inicial", "Radiografía de rentabilidad, liquidez, endeudamiento y capital de trabajo, con los hallazgos priorizados por impacto."),
        ("Análisis de rentabilidad", "Margen real por línea de negocio, producto o cliente, con asignación correcta de costos indirectos."),
        ("Flujo de caja proyectado", "Modelo a 12 meses con escenarios base, optimista y de estrés, para anticipar necesidades de efectivo."),
        ("Estructura de costos y precios", "Punto de equilibrio, costos fijos y variables, y recomendación de política de precios."),
        ("Indicadores y tablero de control", "Un set corto de indicadores con metas, para que midas lo que de verdad mueve el negocio."),
        ("Evaluación de decisiones de inversión", "Análisis de viabilidad para nuevas líneas, sedes, contrataciones o compra de activos."),
        ("Acompañamiento en banca y crédito", "Preparación de la información financiera que exigen los bancos y lectura de las condiciones ofrecidas."),
        ("Reunión mensual de revisión", "Seguimiento de desviaciones frente a lo proyectado y ajuste del plan."),
    ]
  )}
</section>

{proposito(
    "Números que se convierten en decisiones",
    "No entregamos solo un balance: entregamos una lectura de tu empresa que puedes usar para decidir qué vender, a qué precio y con cuánta gente.",
    "Trabajamos con la información que ya produce tu contabilidad, así que no tienes que montar un área nueva para empezar.",
    boton="Hablemos de tu caso",
    mensaje="Hola, quiero hablar sobre consultoría financiera para mi empresa",
    flotante_a=("12 meses", "Flujo de caja proyectado"),
    flotante_b=("Mensual", "Revisión de indicadores")
)}

<section class="seccion oscuro degradado">
  {carrusel(
    "Cómo trabajamos",
    "De la información contable a la decisión",
    "Cuatro etapas para pasar de cifras dispersas a un tablero que puedes usar cada mes.",
    [
        ("Paso 01", "Levantamiento", "Recogemos tu información contable, comercial y operativa, y validamos que los datos sean confiables antes de analizarlos."),
        ("Paso 02", "Diagnóstico", "Construimos la radiografía financiera y priorizamos los hallazgos según cuánto dinero está en juego en cada uno."),
        ("Paso 03", "Modelo y proyección", "Armamos el modelo financiero de tu empresa con escenarios, para ver el efecto de cada decisión antes de tomarla."),
        ("Paso 04", "Seguimiento", "Revisión mensual de indicadores, desviaciones y ajustes del plan con los responsables de cada área."),
    ],
    etiqueta="Etapas de la consultoría"
  )}
</section>

<section class="seccion">
  <div class="contenedor">
    <div class="fijo">
      <div class="fijo__ancla revelar">
        {encabezado("Preguntas frecuentes", "Sobre la consultoría financiera", ancho="none", tam="var(--paso-4)")}
      </div>
      {acordeon([(q, f"<p>{a}</p>") for q, a in faq_fin], prefijo="cf")}
    </div>
  </div>
</section>

<section class="seccion claro">
  <div class="contenedor">
    {encabezado("Otros servicios", "Súmale la operación contable y el control fiscal")}
    {servicios_num(TRIO)}
  </div>
</section>

{resenas_google()}

{cta_final(
    "Pide una lectura financiera de tu empresa",
    "Con tus estados financieros del último año podemos mostrarte dónde está el margen y dónde se está yendo.",
    boton="Quiero este servicio",
    mensaje="Hola, quiero una consultoría financiera para mi empresa"
)}
"""

PAGINAS.append(dict(
    archivo="consultoria-financiera.html",
    titulo="Consultoría Financiera para Empresas y Pymes | Marín Ríos",
    descripcion=f"Consultoría financiera para pymes: análisis de rentabilidad, flujo de caja a 12 meses, costos e indicadores. Cotización a la medida de tu empresa.",
    activo="servicios",
    og_img="detalle-documentos.jpg",
    schema=schema_servicio("Consultoría financiera",
                           "Análisis de rentabilidad, flujo de caja, estructura de costos y proyecciones financieras para pymes en Colombia.",
                           "consultoria-financiera/", faq_fin),
    cuerpo=cuerpo,
))
