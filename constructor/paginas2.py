# -*- coding: utf-8 -*-
"""Planes, blog y páginas de ciudad."""

import json, os, re
from base import (resenas_google, ICO, wa, heroe, encabezado, servicios_num, fijo, carrusel,
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
    "Planes de outsourcing contable para su empresa",
    "Te explicamos con transparencia qué determina el valor de un servicio contable en Colombia, cuándo conviene externalizar y cómo cotizamos según el tamaño de tu empresa.",
    "detalle-documentos.jpg",
    "Documentos contables y análisis de costos de un servicio de outsourcing contable",
    chip="Planes · Servicios contables",
    migas=[("Inicio", "index.html"), ("Planes", None)],
    cta1=("Pide una cotización", "cotizacion-outsourcing-contable.html"),
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
    titulo="Planes de Outsourcing Contable para Pymes | Marín Ríos",
    descripcion="Planes de outsourcing contable para pymes: qué incluye cada plan, qué servicios puede sumar y cómo se adapta al tamaño de su empresa en Colombia.",
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
    if re.search(r"impuesto|tributar|dian|retencion|exogena|regimen|salario|nomina|niif|calendario|decreto|ley-|4x1000", u): return "Impuestos y normativa"
    if re.search(r"financier|rentab|deuda|credito|factoring|presupuesto|balance|escalar|llaves|volatil|inflacion|tasas", u): return "Finanzas"
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
    tarjetas = "".join(tarjeta_articulo(a, i=j) for j, a in enumerate(arts))
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
# Zona que cubre cada ciudad, para las descripciones de búsqueda.
AREA_CIUDAD = {"medellin": "Medellín y el Valle de Aburrá", "pereira": "Pereira y Dosquebradas",
               "armenia": "Armenia y el Quindío", "manizales": "Manizales y Caldas"}

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


# Lo propio de cada ciudad: así ninguna página es una copia de otra con el nombre cambiado.
LOCAL = {
    "medellin": dict(
        titulo="Outsourcing Contable en Medellín para Empresas | Marín Ríos",
        h1="Outsourcing contable para empresas en Medellín y el Valle de Aburrá",
        atencion=("Nuestra sede está en Laureles - Estadio (Cl. 49B #64b-54). Desde ahí atendemos empresas de Medellín, "
                  "Envigado, Itagüí, Sabaneta, Bello y el Oriente Antioqueño: el trabajo diario se hace en línea y nos "
                  "reunimos en tu empresa o en la oficina cuando hace falta, por ejemplo en cierres, inventarios o "
                  "reuniones con socios y bancos."),
        sectores=[
            ("documento", "Confección y textil", "Inventarios por referencia, costos de producción, maquila y devoluciones. Si el costo está mal calculado, el margen que ves en el estado de resultados no es real."),
            ("grafico", "Comercio y distribución", "Facturación electrónica de alto volumen, cartera, rotación de inventarios y conciliación con bancos y pasarelas de pago."),
            ("escudo", "Construcción e inmobiliario", "Contratos de obra, anticipos, AIU y retenciones especiales que exigen llevar la contabilidad por proyecto."),
            ("lupa", "Tecnología y servicios", "Ingresos recurrentes, pagos al exterior, contratistas y socios inversionistas que piden estados financieros confiables."),
        ],
        faq=[
            ("¿Dónde está su oficina en Medellín?",
             "En Laureles - Estadio, Cl. 49B #64b-54. Allí recibimos a los clientes con cita, y también vamos a tu empresa cuando el trabajo lo requiere: cierres, inventarios o reuniones con socios y bancos."),
            ("¿Atienden empresas de Envigado, Itagüí, Sabaneta o Bello?",
             "Sí, todo el Valle de Aburrá y el Oriente Antioqueño. Ten en cuenta que el ICA se declara en el municipio donde realizas la actividad: si operas en varios municipios, cada uno tiene su propia declaración y su propio calendario, y nosotros los llevamos todos."),
        ],
    ),
    "pereira": dict(
        titulo="Outsourcing Contable en Pereira y Dosquebradas | Marín Ríos",
        h1="Outsourcing contable para empresas en Pereira y Dosquebradas",
        atencion=("Atendemos empresas de Pereira, Dosquebradas, Santa Rosa de Cabal y La Virginia. El trabajo diario se "
                  "hace en línea, con un equipo asignado que conoce tu empresa, y programamos visitas para cierres, "
                  "inventarios y reuniones con socios. La sede principal de la firma está en Medellín."),
        sectores=[
            ("grafico", "Comercio mayorista y minorista", "Pereira es el centro comercial del Eje Cafetero: muchas facturas, inventarios y cartera que hay que conciliar cada mes para saber cuánto se gana de verdad."),
            ("documento", "Industria en Dosquebradas", "Metalmecánica, confección y alimentos, con costos de producción, activos fijos y compras de materia prima que pesan en el IVA y en la renta."),
            ("escudo", "Transporte y logística", "Vinculación de vehículos, anticipos, peajes y retenciones que, mal registrados, inflan la renta o terminan en sanciones."),
            ("gente", "Salud y servicios", "Clínicas, consultorios y empresas de servicios con nómina grande, facturación a EPS o a clientes del exterior."),
        ],
        faq=[
            ("¿Atienden presencialmente en Pereira y Dosquebradas?",
             "Sí. El trabajo diario se hace en línea y programamos visitas en Pereira, Dosquebradas y Santa Rosa de Cabal para cierres, inventarios o reuniones con socios y bancos."),
            ("Mi empresa está en Dosquebradas, ¿cambia algo frente a Pereira?",
             "En los impuestos nacionales no; en los municipales sí. El ICA y la retención de ICA se declaran ante el municipio donde se realiza la actividad, y Dosquebradas tiene su propio estatuto y su propio calendario. Nosotros llevamos los dos."),
        ],
    ),
    "armenia": dict(
        titulo="Outsourcing Contable en Armenia, Quindío | Marín Ríos",
        h1="Outsourcing contable para empresas en Armenia y el Quindío",
        atencion=("Atendemos empresas de Armenia, Calarcá, Montenegro y La Tebaida. El trabajo diario se hace en línea, "
                  "con un equipo asignado que conoce tu empresa, y programamos visitas para cierres, inventarios y "
                  "reuniones con socios. La sede principal de la firma está en Medellín."),
        sectores=[
            ("documento", "Turismo y hotelería", "Temporadas altas y bajas, anticipos de reservas, plataformas de alojamiento e IVA en servicios turísticos."),
            ("grafico", "Café y agroindustria", "Compras a productores, retenciones en la compra de café, inventarios y exportaciones con reglas propias."),
            ("escudo", "Comercio y construcción", "Facturación de alto volumen y contratos de obra que exigen controlar anticipos, inventarios y retenciones."),
            ("gente", "Sector solidario", "Cooperativas y fondos de empleados con reportes a la Supersolidaria y revisoría fiscal obligatoria."),
        ],
        faq=[
            ("¿Atienden presencialmente en Armenia?",
             "Sí. Programamos visitas en Armenia, Calarcá, Montenegro y La Tebaida, y el resto del trabajo se hace en línea."),
            ("¿Llevan la contabilidad de hoteles, alojamientos turísticos o empresas cafeteras?",
             "Sí. Parametrizamos la contabilidad según la actividad: temporadas e IVA en turismo, compras a productores y retenciones en café, y costos de producción en la agroindustria."),
        ],
    ),
    "manizales": dict(
        titulo="Outsourcing y Asesoría Contable en Manizales | Marín Ríos",
        h1="Outsourcing y asesoría contable para empresas en Manizales",
        atencion=("Atendemos empresas de Manizales, Villamaría y Chinchiná. El trabajo diario se hace en línea, con un "
                  "equipo asignado que conoce tu empresa, y programamos visitas para cierres, inventarios y reuniones "
                  "con socios. La sede principal de la firma está en Medellín."),
        sectores=[
            ("documento", "Industria", "Metalmecánica, alimentos y manufactura con costos de producción, inventarios y activos fijos de alto valor."),
            ("gente", "Educación, salud y ESAL", "Instituciones y fundaciones del régimen tributario especial, con reportes a su ente de vigilancia."),
            ("grafico", "Café en Chinchiná y la región", "Compras a caficultores, cooperativas y exportadoras con reglas tributarias propias."),
            ("escudo", "Comercio y servicios", "Empresas en crecimiento que necesitan pasar de una contabilidad para cumplir a una que sirva para decidir."),
        ],
        faq=[
            ("¿Ofrecen asesoría contable en Manizales o solo outsourcing?",
             "Las dos. Puedes delegarnos toda la contabilidad o contratar asesoría puntual: revisión de estados financieros, planeación tributaria, cierre del año o respuesta a requerimientos de la DIAN."),
            ("¿Atienden presencialmente en Manizales?",
             "Sí. Programamos visitas en Manizales, Villamaría y Chinchiná, y el resto del trabajo se hace en línea."),
        ],
    ),
}


def lugar(nombre, depto=None):
    """Nodo schema.org para una zona atendida."""
    if nombre in ("Oriente Antioqueño", "Valle de Aburrá", "Quindío", "Caldas", "Risaralda", "Antioquia"):
        return {"@type": "AdministrativeArea", "name": nombre}
    n = {"@type": "City", "name": nombre}
    if depto:
        n["containedInPlace"] = {"@type": "AdministrativeArea", "name": depto}
    return n


def faq_ciudad(c):
    return LOCAL[c["slug"]]["faq"] + [
        ("¿Qué incluye un servicio de outsourcing contable?",
         "Puede incluir desde la elaboración de estados financieros y libros contables hasta la gestión de nómina, impuestos, auditorías internas y reportes para la toma de decisiones. En general te libera de tareas repetitivas, reduce errores y asegura el cumplimiento tributario."),
        ("¿Cómo se calcula el precio del servicio contable?",
         "Se calcula según el volumen de transacciones mensuales, el número de empleados en nómina, la cantidad de obligaciones tributarias de tu empresa y los servicios adicionales que necesites. Con esa información te enviamos una cotización a la medida."),
        ("¿Qué tipo de empresas pueden tercerizar su contabilidad?",
         f"Cualquier empresa obligada a llevar contabilidad en {c['nombre']}: SAS, LTDA, SA, fundaciones, ESAL y empresas de servicios temporales. Es especialmente útil para pymes que aún no justifican un área contable interna."),
        ("¿Necesito cambiar de software contable?",
         "No necesariamente. Trabajamos sobre el software que ya usa tu empresa. Si tu herramienta actual limita la operación, te lo decimos y te mostramos alternativas, pero la decisión es tuya."),
    ]


for c in CIUDADES:
    slug, nombre, depto = c["slug"], c["nombre"], c["depto"]
    otras = [x for x in CIUDADES if x["slug"] != slug]

    servicios_ciudad = [
        ("01 — Contable", "Outsourcing contable",
         "Nuestro <a href=\"outsourcing-contable.html\">servicio de outsourcing contable</a> se encarga de tu contabilidad de principio a fin. Ideal si no tienes equipo interno o necesitas mayor control.",
         None, "Ver outsourcing contable", "outsourcing-contable.html"),
        ("02 — Financiero", "Consultoría financiera",
         "¿No sabes por qué tu negocio no despega? Analizamos tu situación y te damos soluciones claras para mejorar tu rentabilidad.",
         None, "Ver consultoría financiera", "consultoria-financiera.html"),
        ("03 — Fiscal", "Revisoría fiscal",
         "Cumple con la ley y evita sanciones. Revisamos, auditamos y reportamos todo como exige la norma.",
         None, "Ver revisoría fiscal", "revisoria-fiscal.html"),
    ]

    locales_html = "".join(f'<span class="etiqueta-enlace etiqueta-enlace--inerte">{x}</span>' for x in c["locales"])
    L = LOCAL[slug]

    cuerpo = f"""
{heroe(
    L["h1"],
    c["entrada"],
    f"ciudad-{slug}.jpg",
    f"Servicios de outsourcing contable en {nombre}, {depto}",
    chip=f"{depto} · {nombre}",
    migas=[("Inicio", "index.html"), ("Outsourcing contable", "outsourcing-contable.html"), (nombre, None)],
    cta1=("Conversemos", wa(f"Hola, vengo de la página de {nombre} y quiero cotizar el servicio contable")),
    cta2=("Pide tu cotización", "cotizacion-outsourcing-contable.html"),
    riel=[("+50", "Empresas con su contabilidad tercerizada"),
          ("15 días", "Tiempo promedio de transición"),
          (nombre, f"Atención en {c['zona']}"),
          ("100%", "Cumplimiento del calendario DIAN")]
)}

<section class="seccion claro">
  <div class="contenedor">
    {encabezado(f"Empresas en {nombre}", f"¿Por qué tercerizar tu contabilidad si estás en {nombre}?", c["contexto"])}
    {tarjetas_item(L["sectores"])}
  </div>
</section>

<section class="seccion">
  {fijo(
    encabezado(f"Atención en {nombre}", f"Cómo trabajamos con empresas de {nombre}", L["atencion"],
               ancho="none", tam="var(--paso-4)"),
    [
        ("Un equipo asignado", f"Tu empresa tiene un contador responsable y un equipo que la conoce. No hablas cada mes con alguien distinto ni tienes que volver a explicar tu operación."),
        ("Impuestos nacionales y municipales", f"Llevamos el calendario de la DIAN (IVA, retención en la fuente, renta y exógena) y también el de tu municipio: ICA, retención de ICA y avisos y tableros, cada uno con sus propias fechas."),
        (f"Revisoría fiscal en {nombre}", f'Si tu empresa supera los topes o tus estatutos lo exigen, la <a href="revisoria-fiscal-{slug}.html">revisoría fiscal en {nombre}</a> la hace un equipo distinto del que lleva tu contabilidad, como exige la independencia del cargo.'),
    ]
  )}
</section>

<section class="seccion claro">
  <div class="contenedor">
    {encabezado("Qué incluye", f"Qué hacemos por tu empresa en {nombre}", "Lo que cubre el servicio desde el primer mes:")}
    {tarjetas_item([
        ("libro", "Contabilidad bajo NIIF", "Registro, cierres y estados financieros bajo NIIF, parametrizados según tu actividad económica."),
        ("gente", "Gestión de nómina y liquidaciones", "Nómina electrónica, prestaciones, seguridad social y liquidaciones sin errores ni reprocesos."),
        ("documento", "Obligaciones ante la DIAN", "IVA, retención en la fuente, ICA, renta e información exógena dentro del calendario tributario."),
        ("lupa", "Auditorías internas", "Revisión de procesos y soportes para detectar riesgos antes de que lo haga una entidad de control."),
        ("grafico", "Reducción de costos", "Identificamos sobrecostos y fugas que la contabilidad registra pero nadie está leyendo."),
        ("escudo", "Análisis financiero", "Lectura mensual de márgenes, flujo de caja y cartera para que decidas con cifras y no con intuición."),
    ])}
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    {encabezado("Servicios principales", f"Servicios contables adaptados a los desafíos de las pymes {c['gentilicio']}", "Elige el servicio de gestión contable que mejor responda al momento de tu empresa.")}
    {servicios_num(servicios_ciudad)}
  </div>
</section>

{marcas()}

{resenas_google()}

{proposito(
    f"¿Por qué elegir nuestro outsourcing contable en {nombre}?",
    "Si alguna vez has sentido que tu contabilidad no va a ninguna parte, estás en el lugar indicado. Gestionamos tu nómina, preparamos y presentamos tus declaraciones fiscales, administramos tus cuentas por cobrar y pagar y elaboramos tus estados financieros.",
    "Además realizamos auditorías financieras, evaluamos la salud financiera de la empresa y asesoramos sobre optimización fiscal, deducciones aplicables y cumplimiento de obligaciones tributarias.",
    boton="Cotizar plan",
    mensaje=f"Hola, vengo de la página de {nombre} y quiero cotizar un plan contable",
    flotante_a=("100%", "Cumplimiento DIAN"),
    flotante_b=("Mensual", "Cierre con informe")
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
      <div>
        <h3>Revisoría fiscal en {nombre}</h3>
        <div class="directorio__lista">
          <a class="etiqueta-enlace" href="revisoria-fiscal-{slug}.html">Revisor fiscal en {nombre}</a>
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
                "@type": "Service",
                "name": f"Outsourcing contable en {nombre}",
                "serviceType": "Outsourcing contable",
                "description": f"Contabilidad, nómina, impuestos nacionales y municipales y estados financieros NIIF para empresas de {AREA_CIUDAD.get(slug, nombre)}.",
                "url": f"https://marinriosconsultores.com/outsourcing-contable-{slug}/",
                "provider": {"@id": "https://marinriosconsultores.com/#empresa"},
                "areaServed": [lugar(x, depto) for x in c["locales"]],
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
        titulo=LOCAL[slug]["titulo"],
        descripcion=f"Outsourcing contable en {AREA_CIUDAD.get(slug, nombre)}: contabilidad, nómina, impuestos ante la DIAN y estados financieros NIIF, con un equipo asignado a su empresa.",
        activo="",
        og_img=f"ciudad-{slug}.jpg",
        schema=schema,
        cuerpo=cuerpo,
    ))
