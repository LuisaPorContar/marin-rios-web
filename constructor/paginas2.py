# -*- coding: utf-8 -*-
"""Planes, blog y páginas de ciudad."""

import json, os, re
from base import (ICO, wa, heroe, encabezado, servicios_num, fijo, carrusel,
                  acordeon, tarjetas_item, ciudades_grid, directorio,
                  cta_final, proposito, marcas)
from paginas import PAGINAS, TRIO, schema_servicio

AQUI = os.path.dirname(os.path.abspath(__file__))


# ================================================================
# PLANES (la URL conserva "precios" por posicionamiento, pero sin cifras)
# ================================================================
faq_pre = [
    ("¿Cuánto cuesta el servicio de outsourcing contable?",
     "El valor depende del tipo de servicio, el tamaño de la empresa, la industria y el nivel de complejidad de las operaciones contables. Por eso no manejamos tarifas de lista: revisamos tu operación sin costo y te enviamos una cotización a la medida."),
    ("¿Qué ofrecen en su servicio de contaduría?",
     "Contabilidad general, asesoría contable y financiera, gestión de impuestos y declaraciones, contabilidad de nómina, estados financieros bajo NIIF y acompañamiento en requerimientos de la DIAN. Puedes sumar revisoría fiscal o consultoría financiera según lo que necesite tu empresa."),
    ("¿Por qué debo contratar una consultora financiera?",
     "Porque la contabilidad te dice qué pasó, pero no qué hacer. Una consultora financiera analiza tu situación, orienta la reducción de costos y apoya el trazado de tu crecimiento con cifras, no con intuición."),
    ("¿Qué es un outsourcing contable?",
     "Es cuando una firma externa asume las funciones contables y financieras de tu empresa. Más que un gasto, es una inversión que asegura precisión, cumplimiento y eficiencia sin sostener un área interna."),
    ("¿Cuánto vale una asesoría contable puntual?",
     "Una asesoría puntual tiene un valor distinto al de la operación mensual. Escríbenos con el caso concreto y te damos el valor exacto: no cobramos por consulta a los clientes con plan mensual activo."),
    ("¿El plan incluye la nómina?",
     "Sí, la liquidación de nómina y la transmisión del documento soporte de nómina electrónica están incluidas. Si tu empresa supera cierto número de empleados, ajustamos el plan y te lo informamos antes de contratar."),
]

cuerpo_precios = f"""
{heroe(
    "¿Cuánto cuesta un outsourcing contable? Qué define el valor",
    "Te explicamos con transparencia qué determina el valor de un servicio contable en Colombia, cuándo conviene externalizar y cómo cotizamos según el tamaño de tu empresa.",
    "detalle-documentos.jpg",
    "Documentos contables y análisis de costos de un servicio de outsourcing contable",
    chip="Planes · Servicios contables",
    migas=[("Inicio", "index.html"), ("Planes", None)],
    cta1=("Pide una cotización", wa("Hola, quiero una cotización de sus servicios contables")),
    cta2=("Ver el servicio", "outsourcing-contable.html"),
    riel=[("A la medida", "Cotización según tu operación"),
          ("+50", "Empresas con su contabilidad tercerizada"),
          ("15 días", "Tiempo promedio de transición"),
          ("0", "Cobros por consulta a clientes con plan activo")]
)}

<section class="seccion claro">
  <div class="contenedor">
    {encabezado("El punto de partida", "¿Cómo economizar dinero en tu empresa tercerizando los servicios contables?", "Si has llegado hasta aquí, es probable que tu empresa haya iniciado un camino de crecimiento y con él hayan surgido nuevos desafíos.")}
    {tarjetas_item([
        ("lupa", "Inconsistencias en la gestión contable", "Los registros no reflejan la operación real y cada cierre exige rehacer trabajo."),
        ("documento", "Dificultades con los informes financieros", "La información llega tarde o incompleta para presentarla a socios o bancos."),
        ("candado", "Desafíos en la gestión fiscal", "Las obligaciones tributarias se atienden sobre la fecha límite, con riesgo de error."),
        ("escudo", "Riesgo de incumplimiento normativo", "No hay certeza de que la empresa esté cumpliendo con las regulaciones contables y fiscales vigentes."),
        ("reloj", "Eventualidades de auditorías fiscales", "Un requerimiento de la DIAN encuentra a la empresa sin los soportes organizados."),
        ("grafico", "Presupuesto bajo presión", "El reto es resolver todo lo anterior sin que se dispare el costo del área administrativa."),
    ])}
    <p class="medida" style="margin-top:var(--sp-4);color:var(--texto-suave)">No te alarmes: estos desafíos son más comunes de lo que piensas en las organizaciones colombianas. A continuación te contamos cómo resolverlos sin comprometer la calidad ni la conformidad de tus operaciones contables.</p>
  </div>
</section>

<section class="seccion">
  {fijo(
    encabezado("Cuándo externalizar", "¿Cuándo es pertinente externalizar los servicios contables?",
               "Hay dos aspectos que conviene mirar antes de decidir: el legal y el estratégico.",
               ancho="none", tam="var(--paso-4)"),
    [
        ("Aspecto legal: quién está obligado", "Colombia tiene un marco regulador que obliga a diversas entidades a cumplir requisitos y presentar informes financieros de forma regular: empresas públicas y privadas, contratistas bajo contratos civiles, comerciales o administrativos, organizaciones de economía solidaria, empresas de servicios temporales y trabajadores autónomos."),
        ("Mejora el cumplimiento y la oportunidad", "La presentación de informes financieros deja de depender de la disponibilidad de una sola persona y pasa a un calendario con responsables."),
        ("Reduce el riesgo de sanciones", "Disminuyen las multas por incumplimientos fiscales y contables, que suelen costar más que el servicio mismo."),
        ("Habilita licitaciones y contrataciones", "Permite que la empresa sea competitiva en procesos públicos o privados que exigen estados financieros dictaminados."),
        ("Mejora la percepción de los stakeholders", "Socios, bancos e inversionistas leen la gestión financiera de la empresa como ordenada y verificable."),
        ("Optimiza recursos y productividad", "El área contable deja de consumir tiempo directivo y se mide por entregables, no por horas."),
    ]
  )}
</section>

{proposito(
    "Más que un gasto, una inversión estratégica",
    "La externalización de los servicios contables implica delegar las funciones de contabilidad y finanzas a un proveedor especializado. Permite asegurar la precisión, el cumplimiento y la eficiencia de tu gestión contable y financiera.",
    "Las operaciones financieras de una empresa no solo impactan su salud financiera: también el bienestar y la estabilidad de los empleados y de todos los involucrados.",
    boton="Chateanos",
    mensaje="Hola, quiero una cotización de sus servicios contables",
    flotante_a=("A la medida", "Cotización según tu operación"),
    flotante_b=("Sin", "Cobros por consulta")
)}

<section class="seccion claro">
  <div class="contenedor">
    {encabezado("Tipos de servicio", "Qué encontrarás en una empresa de outsourcing contable", "Tres líneas de servicio que puedes contratar por separado o combinadas.")}
    {servicios_num(TRIO)}
  </div>
</section>

<section class="seccion oscuro degradado">
  <div class="contenedor">
    {encabezado("El ABC del servicio", "¿Qué logras contratando un servicio de outsourcing contable?", ancho="52rem", tam="var(--paso-4)")}
    <div class="rejilla-3 rejilla-movil revelar">
      <article class="tarjeta-servicio"><h3>Finanzas al día</h3><p>Mantienes la contabilidad de tu negocio al día, con cierres entregados en fecha.</p></article>
      <article class="tarjeta-servicio"><h3>Menor costo de contratación</h3><p>Reduces el costo de sostener y reemplazar personal contable interno.</p></article>
      <article class="tarjeta-servicio"><h3>Sin carga operativa</h3><p>Eliminas de tu día a día la persecución de soportes, plazos y trámites.</p></article>
      <article class="tarjeta-servicio"><h3>Estrategias de crecimiento</h3><p>Obtienes lectura financiera para decidir dónde y cómo crecer.</p></article>
      <article class="tarjeta-servicio"><h3>Optimización ante la DIAN</h3><p>Aprovechas correctamente deducciones y beneficios aplicables a tu actividad.</p></article>
      <article class="tarjeta-servicio"><h3>Un equipo, no una persona</h3><p>Cuentas con un equipo completo a tu disposición, sin depender de un solo contador.</p></article>
    </div>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    <div class="fijo">
      <div class="fijo__ancla revelar">
        {encabezado("Cuánto cuesta", "Qué define el valor del servicio de outsourcing contable", "Los costos varían según el tipo de servicio, el tamaño de la empresa, la industria y el nivel de complejidad de las operaciones contables. Por eso cotizamos cada empresa a la medida, con foco en pymes.", ancho="none", tam="var(--paso-4)")}
      </div>
      {acordeon([(q, f"<p>{a}</p>") for q, a in faq_pre], prefijo="pr")}
    </div>
  </div>
</section>

<section class="seccion claro">
  <div class="contenedor">
    {encabezado("Cobertura", "Servicios contables por ciudad", ancho="54rem", tam="var(--paso-4)")}
    {ciudades_grid()}
  </div>
</section>

{cta_final(
    "Pide una asesoría personalizada para tu pyme",
    "Cuéntanos cuántas transacciones y empleados maneja tu empresa y te damos un valor exacto, no un rango. Ten en cuenta que no hacemos declaración de renta ni de ingresos para personas naturales.",
    boton="Hablemos",
    mensaje="Hola, quiero una cotización personalizada de sus servicios contables"
)}
"""

PAGINAS.append(dict(
    archivo="precios-outsourcing-contable.html",
    titulo="¿Cuánto Cuesta un Outsourcing Contable en Colombia? | Marín Ríos",
    descripcion="¿Cuánto cuesta un outsourcing contable en Colombia? Qué determina el valor del servicio, qué incluye cada plan para pymes y cómo pedir tu cotización.",
    activo="precios",
    og_img="detalle-documentos.jpg",
    schema=schema_servicio("Outsourcing contable",
                           "Planes de outsourcing contable, revisoría fiscal y consultoría financiera para pymes en Colombia, cotizados a la medida.",
                           "precios-outsourcing-contable/", faq_pre),
    cuerpo=cuerpo_precios,
))


# ================================================================
# BLOG
# ================================================================
with open(os.path.join(AQUI, "articulos.json"), encoding="utf-8") as f:
    ARTICULOS = json.load(f)


def categoria(a):
    u = a["url"]
    if re.search(r"revisor|revisoria|auditor", u): return "Revisoría fiscal"
    if re.search(r"impuesto|tributar|dian|retencion|exogena|regimen|salario|nomina|niif|calendario", u): return "Impuestos y normativa"
    if re.search(r"financier|rentab|deuda|credito|factoring|presupuesto|balance|escalar|llaves|volatil", u): return "Finanzas"
    return "Outsourcing contable"


# Artículos que ya tienen página estática propia (ver articulos_paginas.py).
with open(os.path.join(AQUI, "articulos_cuerpo.json"), encoding="utf-8") as f:
    SLUGS_CON_PAGINA = {a["slug"] for a in json.load(f)}


def enlace_articulo(a):
    """Enlaza a la página estática del artículo; si aún no existe, al WordPress."""
    slug = a["url"].replace("https://marinriosconsultores.com/", "").strip("/")
    return f"{slug}.html" if slug in SLUGS_CON_PAGINA else a["url"]


# Set de imágenes del blog: todas en duotono de marca para que la grilla se lea como un sistema
IMAGENES_BLOG = [f"blog-{i}.jpg" for i in range(1, 7)]


def tarjeta_articulo(a, destacado=False, i=0):
    clase = "articulo articulo--destacado" if destacado else "articulo"
    desc = (a["desc"] or "")[:180]
    img = "equipo-ancho.jpg" if destacado else IMAGENES_BLOG[i % len(IMAGENES_BLOG)]
    return f"""<article class="{clase}">
        <div class="articulo__media">
          <img src="assets/img/{img}" alt="" width="900" height="560" loading="lazy">
        </div>
        <div class="articulo__cuerpo">
          <span class="articulo__meta">{categoria(a)} · {a['fecha']}</span>
          <h3><a href="{enlace_articulo(a)}">{a['titulo']}</a></h3>
          <p>{desc}</p>
          <span class="articulo__mas">Leer el artículo {ICO['flecha_fina']}</span>
        </div>
      </article>"""


destacado = ARTICULOS[0]
resto = ARTICULOS[1:]

cats = {}
for a in resto:
    cats.setdefault(categoria(a), []).append(a)

bloques_cat = []
for nombre, arts in cats.items():
    tarjetas = "".join(tarjeta_articulo(a, i=j) for j, a in enumerate(arts[:6]))
    bloques_cat.append(f"""<section class="seccion--ajustada">
  <div class="contenedor carrusel">
    <div class="carrusel__cabecera revelar">
      <div>
        <p class="eyebrow">Categoría</p>
        <h2 style="font-size:var(--paso-3)">{nombre}</h2>
      </div>
      <div class="carrusel__controles">
        <button class="carrusel__btn" data-dir="anterior" aria-label="Anterior">{ICO['atras']}</button>
        <button class="carrusel__btn" data-dir="siguiente" aria-label="Siguiente">{ICO['flecha_fina']}</button>
      </div>
    </div>
    <div class="carrusel__pista revelar" role="group" aria-label="Artículos de {nombre}">{tarjetas}</div>
    <div class="carrusel__progreso"><i></i></div>
  </div>
</section>""")

cuerpo_blog = f"""
{heroe(
    "Blog contable y financiero para empresas",
    "Impuestos, revisoría fiscal, NIIF y finanzas explicados sin lenguaje técnico innecesario, para que tomes mejores decisiones en tu empresa.",
    "reunion-ancho.jpg",
    "Equipo de Marín Ríos Consultores analizando información contable",
    chip="Blog · Actualidad contable",
    migas=[("Inicio", "index.html"), ("Blog", None)],
    cta1=("Agenda una asesoría", wa("Hola, vengo del blog y quiero agendar una asesoría")),
    riel=[(str(len(ARTICULOS)), "Artículos publicados"),
          ("4", "Temas: contable, fiscal, tributario y financiero"),
          ("2026", "Normativa actualizada"),
          ("+50", "Empresas acompañadas")]
)}

<section class="seccion--ajustada">
  <div class="contenedor">
    <div class="encabezado-seccion revelar" style="max-width:54rem">
      <p class="eyebrow">Lo más reciente</p>
      <h2 style="font-size:var(--paso-4)">Último artículo publicado</h2>
    </div>
    <div class="rejilla-blog revelar">{tarjeta_articulo(destacado, destacado=True)}</div>
  </div>
</section>

{"".join(bloques_cat)}

<section class="seccion claro">
  <div class="contenedor">
    {encabezado("Servicios", "¿Prefieres que lo resolvamos nosotros?", "Leer sobre contabilidad ayuda. Tener un equipo que la ejecute, ayuda más.")}
    {servicios_num(TRIO)}
  </div>
</section>

{cta_final(
    "¿Tu caso no está en el blog?",
    "Escríbenos con la situación concreta de tu empresa y te respondemos con una recomendación, no con un artículo genérico.",
    boton="Escríbenos",
    mensaje="Hola, vengo del blog y quiero resolver un caso puntual de mi empresa"
)}
"""

PAGINAS.append(dict(
    archivo="blog.html",
    titulo="Blog Contable y Financiero para Empresas | Marín Ríos",
    descripcion=f"Artículos sobre outsourcing contable, revisoría fiscal, impuestos y NIIF en Colombia. {len(ARTICULOS)} guías prácticas para pymes.",
    activo="blog",
    og_img="reunion-ancho.jpg",
    schema=json.dumps({
        "@context": "https://schema.org",
        "@type": "Blog",
        "name": "Blog de Marín Ríos Consultores",
        "description": "Artículos sobre contabilidad, revisoría fiscal, impuestos y finanzas para empresas en Colombia.",
        "url": "https://marinriosconsultores.com/blog/",
        "publisher": {"@type": "AccountingService", "name": "Marín Ríos Consultores",
                      "@id": "https://marinriosconsultores.com/#empresa"},
        "blogPost": [{"@type": "BlogPosting", "headline": a["titulo"], "url": a["url"],
                      "datePublished": a["fecha"]} for a in ARTICULOS[:12]]
    }, ensure_ascii=False, indent=2),
    cuerpo=cuerpo_blog,
))


# ================================================================
# CIUDADES
# ================================================================
CIUDADES = [
    dict(slug="medellin", nombre="Medellín", depto="Antioquia", gentilicio="antioqueñas",
         zona="Valle de Aburrá", locales=["Medellín", "Envigado", "Bello", "Oriente Antioqueño"],
         entrada="Libérate de la carga contable y enfócate en hacer crecer tu negocio. Nosotros nos encargamos de los números, tú del crecimiento.",
         contexto="Si operas en Medellín o el Valle de Aburrá, sabes que la contabilidad mal llevada cuesta tiempo, dinero y tranquilidad. Nuestro servicio está diseñado para que delegues esta tarea con confianza y resultados.",
         sede=True),
    dict(slug="armenia", nombre="Armenia", depto="Quindío", gentilicio="quindianas",
         zona="Quindío", locales=["Armenia", "Calarcá", "Montenegro", "La Tebaida"],
         entrada="Contabilidad, impuestos y revisoría fiscal para empresas del Quindío, con acompañamiento remoto y presencial cuando se necesita.",
         contexto="El tejido empresarial del Quindío se mueve entre comercio, turismo, café y servicios. Cada uno tiene un tratamiento contable y tributario distinto, y ahí es donde se cometen los errores más costosos.",
         sede=False),
    dict(slug="pereira", nombre="Pereira", depto="Risaralda", gentilicio="risaraldenses",
         zona="Área Metropolitana Centro Occidente", locales=["Pereira", "Dosquebradas", "La Virginia", "Santa Rosa de Cabal"],
         entrada="Gestión contable y tributaria para negocios en Risaralda, con reportes claros y cumplimiento garantizado ante la DIAN.",
         contexto="Pereira concentra buena parte de la actividad comercial e industrial del Eje Cafetero. Las empresas que crecen rápido suelen quedarse con una contabilidad que ya no les alcanza para decidir.",
         sede=False),
    dict(slug="manizales", nombre="Manizales", depto="Caldas", gentilicio="caldenses",
         zona="Caldas", locales=["Manizales", "Villamaría", "Chinchiná", "La Dorada"],
         entrada="Outsourcing contable para empresas caldenses que necesitan orden, cumplimiento y cifras confiables para crecer.",
         contexto="Manizales combina un fuerte sector educativo y de servicios con industria y agroindustria cafetera. Son operaciones con estructuras de costos muy distintas, que exigen una contabilidad bien parametrizada.",
         sede=False),
]


def faq_ciudad(c):
    return [
        ("¿Qué incluye un servicio de outsourcing contable?",
         "Puede incluir desde la elaboración de estados financieros y libros contables hasta la gestión de nómina, impuestos, auditorías internas y reportes para la toma de decisiones. En general te libera de tareas repetitivas, reduce errores y asegura el cumplimiento tributario."),
        ("¿Cómo se calcula el precio del servicio contable?",
         "Se calcula según el volumen de transacciones mensuales, el número de empleados en nómina, la cantidad de obligaciones tributarias de tu empresa y los servicios adicionales que necesites. Con esa información te enviamos una cotización a la medida."),
        ("¿Qué tipo de empresas pueden tercerizar su contabilidad?",
         f"Cualquier empresa obligada a llevar contabilidad en {c['nombre']}: SAS, LTDA, SA, fundaciones, ESAL y empresas de servicios temporales. Es especialmente útil para pymes y startups que aún no justifican un área contable interna."),
        (f"¿Atienden empresas fuera de {c['nombre']}?",
         "Sí. Trabajamos con herramientas digitales que permiten operar de forma remota en todo el país, y atendemos presencialmente en " + ", ".join(c["locales"][:3]) + " y municipios cercanos."),
        ("¿Necesito cambiar de software contable?",
         "No necesariamente. Trabajamos sobre el software que ya usa tu empresa. Si tu herramienta actual limita la operación, te lo decimos y te mostramos alternativas, pero la decisión es tuya."),
    ]


for c in CIUDADES:
    slug, nombre, depto = c["slug"], c["nombre"], c["depto"]
    otras = [x for x in CIUDADES if x["slug"] != slug]

    servicios_ciudad = [
        ("01 — Contable", "Outsourcing contable",
         "Nos encargamos de tu contabilidad de principio a fin. Ideal si no tienes equipo interno o necesitas mayor control.",
         None, "Quiero este servicio", "outsourcing-contable.html"),
        ("02 — Financiero", "Consultoría financiera",
         "¿No sabes por qué tu negocio no despega? Analizamos tu situación y te damos soluciones claras para mejorar tu rentabilidad.",
         None, "Quiero este servicio", "consultoria-financiera.html"),
        ("03 — Fiscal", "Revisoría fiscal",
         "Cumple con la ley y evita sanciones. Revisamos, auditamos y reportamos todo como exige la norma.",
         None, "Quiero este servicio", "revisoria-fiscal.html"),
    ]

    locales_html = "".join(f'<span class="etiqueta-enlace etiqueta-enlace--inerte">{x}</span>' for x in c["locales"])

    cuerpo = f"""
{heroe(
    f"Outsourcing contable en {nombre} para pymes y startups",
    c["entrada"],
    f"ciudad-{slug}.jpg",
    f"Servicios de outsourcing contable en {nombre}, {depto}",
    chip=f"{depto} · {nombre}",
    migas=[("Inicio", "index.html"), ("Ciudades", None), (nombre, None)],
    cta1=("Conversemos", wa(f"Hola, vengo de la página de {nombre} y quiero cotizar el servicio contable")),
    cta2=("Ver planes", "precios-outsourcing-contable.html"),
    riel=[("+50", "Empresas con su contabilidad tercerizada"),
          ("15 días", "Tiempo promedio de transición"),
          (nombre, f"Atención en {c['zona']}"),
          ("100%", "Cumplimiento del calendario DIAN")]
)}

<section class="seccion claro">
  <div class="contenedor">
    {encabezado(f"Por qué tercerizar en {nombre}", f"¿Por qué tercerizar tu contabilidad si estás en {nombre}?", c["contexto"] + " Te ayudamos con:")}
    {tarjetas_item([
        ("libro", "Contabilidad para pymes y startups", "Registro, cierres y estados financieros bajo NIIF, parametrizados según tu actividad económica."),
        ("gente", "Gestión de nómina y liquidaciones", "Nómina electrónica, prestaciones, seguridad social y liquidaciones sin errores ni reprocesos."),
        ("documento", "Obligaciones ante la DIAN", "IVA, retención en la fuente, ICA, renta e información exógena dentro del calendario tributario."),
        ("lupa", "Auditorías internas", "Revisión de procesos y soportes para detectar riesgos antes de que lo haga una entidad de control."),
        ("grafico", "Reducción de costos", "Identificamos sobrecostos y fugas que la contabilidad registra pero nadie está leyendo."),
        ("escudo", "Revisoría fiscal y análisis financiero", "Dictamen independiente y lectura financiera cuando tu empresa alcanza el tamaño que lo exige."),
    ])}
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    {encabezado("Servicios principales", f"Servicios contables adaptados a los desafíos de las pymes {c['gentilicio']}", "Elige el servicio de gestión contable que mejor responda al momento de tu empresa.")}
    {servicios_num(servicios_ciudad)}
  </div>
</section>

<section class="seccion claro">
  {fijo(
    encabezado("Gestión contable", f"Servicios de contabilidad para negocios en {nombre}",
               "Cinco frentes de trabajo que cubrimos desde el primer mes.",
               ancho="none", tam="var(--paso-4)"),
    [
        ("Revisión financiera estratégica", "Examinamos tus finanzas a fondo para identificar fugas de dinero, oportunidades de mejora y puntos ciegos. Todo enfocado en el ritmo y los retos de las startups."),
        ("Optimización de procesos contables", "Corregimos errores frecuentes y rediseñamos tu contabilidad para que sea clara, eficiente y útil. Nos adaptamos a la realidad de las pymes y al entorno emprendedor."),
        ("Planeación fiscal inteligente", "Creamos un plan tributario que se ajusta a la normativa y a las necesidades de tu empresa. Menos riesgos, más ahorro y cero improvisación."),
        ("Capacitación en herramientas digitales", "Entrenamos a tu equipo en el uso de software contable y herramientas digitales que automatizan tareas y reducen errores."),
        ("Acompañamiento contable constante", "No te dejamos solo. Agendamos reuniones periódicas para revisar tu contabilidad, hacer ajustes y tomar decisiones con información real."),
    ]
  )}
</section>

{marcas()}

{proposito(
    f"¿Por qué elegir nuestro outsourcing contable en {nombre}?",
    "Si alguna vez has sentido que tu contabilidad no va a ninguna parte, estás en el lugar indicado. Gestionamos tu nómina, preparamos y presentamos tus declaraciones fiscales, administramos tus cuentas por cobrar y pagar y elaboramos tus estados financieros.",
    "Además realizamos auditorías financieras, evaluamos la salud financiera de la empresa y asesoramos sobre optimización fiscal, deducciones aplicables y cumplimiento de obligaciones tributarias.",
    boton="Cotizar plan",
    mensaje=f"Hola, vengo de la página de {nombre} y quiero cotizar un plan contable",
    flotante_a=("100%", "Cumplimiento DIAN"),
    flotante_b=("Día 10", "Cierre mensual entregado")
)}

<section class="seccion oscuro degradado">
  {carrusel(
    f"Contadores en {nombre}",
    "Así trabajamos contigo",
    "Cuatro etapas con entregables concretos, desde el diagnóstico hasta el acompañamiento permanente.",
    [
        ("Paso 01", "Diagnóstico inicial", "Evaluamos tu situación actual: estado de la contabilidad, obligaciones pendientes y riesgos abiertos."),
        ("Paso 02", "Plan de trabajo", "Te mostramos qué vamos a resolver, cómo y en qué fechas, con responsables definidos."),
        ("Paso 03", "Implementación", "Nos encargamos de todo el proceso contable: registros, impuestos, nómina y conciliaciones."),
        ("Paso 04", "Acompañamiento constante", "Informes, reuniones, alertas y soporte continuo para que decidas con información al día."),
    ],
    etiqueta="Etapas del proceso"
  )}
</section>

<section class="seccion">
  <div class="contenedor">
    {encabezado("Cobertura local", f"Atendemos empresas en {c['zona']}", ancho="54rem", tam="var(--paso-4)")}
    <div class="directorio revelar">
      <div>
        <h3>{c['zona']}</h3>
        <div class="directorio__lista">{locales_html}</div>
      </div>
      <div>
        <h3>Otras ciudades</h3>
        <div class="directorio__lista">
          {"".join(f'<a class="etiqueta-enlace" href="outsourcing-contable-{o["slug"]}.html">{o["nombre"]}</a>' for o in otras)}
        </div>
      </div>
    </div>
  </div>
</section>

<section class="seccion claro">
  <div class="contenedor">
    <div class="fijo">
      <div class="fijo__ancla revelar">
        {encabezado("Preguntas frecuentes", f"Dudas sobre contabilidad en {nombre}", ancho="none", tam="var(--paso-4)")}
      </div>
      {acordeon([(q, f"<p>{a}</p>") for q, a in faq_ciudad(c)], prefijo=slug[:3])}
    </div>
  </div>
</section>

{cta_final(
    f"Comunícate con nuestro equipo en {nombre}",
    "Cuéntanos en qué estado está tu contabilidad y te decimos con claridad qué necesita tu empresa y cuánto costaría.",
    boton="Conversemos",
    mensaje=f"Hola, vengo de la página de {nombre} y quiero agendar una asesoría"
)}
"""

    schema = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "AccountingService",
                "name": f"Marín Ríos Consultores — Outsourcing contable en {nombre}",
                "description": f"Servicio de outsourcing contable, revisoría fiscal y consultoría financiera para empresas en {nombre}, {depto}.",
                "url": f"https://marinriosconsultores.com/outsourcing-contable-{slug}/",
                "telephone": "+57 314 884 3835",
                "email": "j@marinriosconsultores.com",
                "priceRange": "$$",
                "parentOrganization": {"@id": "https://marinriosconsultores.com/#empresa"},
                "address": {"@type": "PostalAddress", "addressLocality": nombre,
                            "addressRegion": depto, "addressCountry": "CO"},
                "areaServed": [{"@type": "City", "name": x} for x in c["locales"]],
            },
            {
                "@type": "FAQPage",
                "mainEntity": [{"@type": "Question", "name": q,
                                "acceptedAnswer": {"@type": "Answer", "text": a}}
                               for q, a in faq_ciudad(c)]
            }
        ]
    }, ensure_ascii=False, indent=2)

    PAGINAS.append(dict(
        archivo=f"outsourcing-contable-{slug}.html",
        titulo=f"Outsourcing Contable en {nombre} para Pymes | Marín Ríos",
        descripcion=f"Outsourcing contable en {nombre}: contabilidad, nómina, impuestos DIAN y revisoría fiscal para pymes y startups. Cotización a la medida.",
        activo="",
        og_img=f"ciudad-{slug}.jpg",
        schema=schema,
        cuerpo=cuerpo,
    ))
