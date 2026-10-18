# -*- coding: utf-8 -*-
"""Revisoría fiscal por ciudad: Medellín y Eje Cafetero.

Cada página tiene su propio contexto empresarial y sus propias preguntas,
para que no compitan entre sí ni con la página pilar /revisoria-fiscal/.
"""

import json
from base import (ICO, wa, heroe, encabezado, fijo, acordeon, tarjetas_item,
                  cta_final, carrusel_clientes, resenas_google, ultimas_publicaciones)
from paginas import PAGINAS
from paginas2 import CIUDADES, lugar

TOPE_ACTIVOS = "$8.754.525.000"
TOPE_INGRESOS = "$5.252.715.000"

RF = {
    "medellin": dict(
        titulo="Revisoría fiscal en Medellín para empresas que crecen",
        entrada="Revisor fiscal con presencia durante todo el año, no solo al cierre. Para sociedades del Valle de Aburrá que necesitan cifras confiables ante socios, bancos y la DIAN.",
        contexto="Medellín concentra empresas de manufactura, textil y confección, construcción, tecnología y servicios. Muchas crecieron rápido y cruzaron los topes de revisoría fiscal sin darse cuenta, o siguen con un revisor que ya no acompaña el tamaño que tienen hoy.",
        sectores=[
            ("documento", "Manufactura y textil", "Inventarios grandes, costos de producción y operaciones de comercio exterior que exigen pruebas de existencia y valoración."),
            ("escudo", "Construcción e inmobiliario", "Contratos de obra, anticipos, fiducias y reconocimiento de ingresos por avance, con alta exposición tributaria."),
            ("lupa", "Tecnología y servicios", "Empresas con inversionistas o rondas de capital que necesitan estados financieros dictaminados para dar confianza."),
        ],
        faq=[
            ("¿Cuándo debe una empresa de Medellín tener revisor fiscal en 2027?",
             f"Cuando a 31 de diciembre de 2026 sus activos brutos sean iguales o superiores a {TOPE_ACTIVOS} o sus ingresos brutos del año iguales o superiores a {TOPE_INGRESOS}. Las sociedades anónimas lo necesitan siempre, sin importar su tamaño."),
            ("¿Hacen visitas presenciales en el Valle de Aburrá?",
             "Sí. Atendemos presencialmente en Medellín, Envigado, Itagüí, Sabaneta, Bello y el Oriente Antioqueño, y complementamos con revisión remota durante el mes."),
            ("¿Dónde se inscribe el revisor fiscal de una empresa de Medellín?",
             "En la Cámara de Comercio de Medellín para Antioquia, o en la del Aburrá Sur si la empresa está registrada allí. El nombramiento debe inscribirse para que sea oponible a terceros."),
            ("¿Pueden reemplazar a nuestro revisor fiscal actual?",
             "Sí. Le preparamos una propuesta para presentar en la asamblea ordinaria y coordinamos el empalme con el revisor saliente para que no queden informes ni declaraciones pendientes."),
        ],
    ),
    "pereira": dict(
        titulo="Revisoría fiscal en Pereira y Risaralda",
        entrada="Revisor fiscal para sociedades de Pereira y Dosquebradas, con visitas periódicas, informes que se entienden y respaldo frente a la DIAN.",
        contexto="Pereira y Dosquebradas son el centro comercial, logístico e industrial del Eje Cafetero. Distribuidoras, empresas de transporte, confección y metalmecánica han crecido en ventas, y con ellas llegó la obligación de tener revisor fiscal.",
        sectores=[
            ("documento", "Comercio y distribución", "Alto volumen de facturación, cartera con muchos clientes y márgenes estrechos donde un error de inventario pesa."),
            ("escudo", "Transporte y logística", "Flotas, vinculación de vehículos, anticipos y retenciones que exigen un control tributario fino."),
            ("lupa", "Industria en Dosquebradas", "Metalmecánica, confección y alimentos con costos de producción, activos fijos y operaciones de exportación."),
        ],
        faq=[
            ("¿Una empresa de Pereira con ventas de $6.000 millones necesita revisor fiscal?",
             f"Sí. Si sus ingresos brutos de 2026 son iguales o superiores a {TOPE_INGRESOS}, debe tener revisor fiscal en 2027, aunque sus activos sean bajos. Basta con superar uno de los dos topes."),
            ("¿Atienden presencialmente en Pereira y Dosquebradas?",
             "Sí. Hacemos visitas presenciales en Pereira, Dosquebradas y Santa Rosa de Cabal, y el resto del trabajo se apoya en revisión remota de la contabilidad."),
            ("¿Dónde se registra el revisor fiscal en Risaralda?",
             "En la Cámara de Comercio de Pereira, o en la de Dosquebradas si la empresa está matriculada allí, con copia del acta de la asamblea que lo eligió."),
            ("¿Qué pasa si nuestra SAS no nombra revisor estando obligada?",
             "La DIAN puede tener por no presentadas las declaraciones que no lleven su firma, y la Superintendencia de Sociedades puede imponer multas. Conviene nombrarlo antes de la temporada de renta."),
        ],
    ),
    "armenia": dict(
        titulo="Revisoría fiscal en Armenia y el Quindío",
        entrada="Revisor fiscal para empresas, cooperativas y entidades del Quindío, con presencia en Armenia y acompañamiento durante todo el ejercicio.",
        contexto="En el Quindío conviven empresas de turismo y hotelería, comercializadoras de café, agroindustria, construcción y un sector solidario muy activo. Cada una tiene riesgos distintos, y el revisor fiscal debe conocerlos.",
        sectores=[
            ("documento", "Turismo y hotelería", "Ingresos estacionales, anticipos de reservas, plataformas digitales e IVA en servicios turísticos."),
            ("escudo", "Cooperativas y fondos de empleados", "Entidades del sector solidario que por ley deben tener revisor fiscal y reportar a la Supersolidaria."),
            ("lupa", "Café y agroindustria", "Inventarios biológicos, compras a productores, exportaciones y beneficios tributarios del sector agropecuario."),
        ],
        faq=[
            ("¿Las cooperativas del Quindío deben tener revisor fiscal?",
             "Sí. La Ley 79 de 1988 establece la revisoría fiscal como órgano de control de las cooperativas, sin importar su tamaño. Los fondos de empleados también deben tenerlo."),
            ("¿Cuáles son los topes de revisoría fiscal para 2027?",
             f"Activos brutos iguales o superiores a {TOPE_ACTIVOS} o ingresos brutos iguales o superiores a {TOPE_INGRESOS}, medidos con las cifras al 31 de diciembre de 2026."),
            ("¿Atienden presencialmente en Armenia?",
             "Sí. Hacemos visitas en Armenia, Calarcá, Montenegro y La Tebaida, y complementamos con revisión remota de la información contable."),
            ("¿Dónde se inscribe el revisor fiscal en el Quindío?",
             "En la Cámara de Comercio de Armenia y del Quindío para sociedades y ESAL. Las cooperativas además informan a la Superintendencia de la Economía Solidaria según su nivel de supervisión."),
        ],
    ),
    "manizales": dict(
        titulo="Revisoría fiscal en Manizales y Caldas",
        entrada="Revisor fiscal para sociedades y entidades de Caldas, con informes claros para la junta y respaldo ante la DIAN y las superintendencias.",
        contexto="Manizales combina industria metalmecánica y de alimentos, educación, salud y servicios, con un fuerte sector cafetero en Chinchiná y la región. Muchas de estas organizaciones necesitan revisor fiscal por ley, por sus estatutos o por exigencia de bancos y financiadores.",
        sectores=[
            ("documento", "Industria", "Metalmecánica, alimentos y manufactura con costos de producción, inventarios y activos fijos de alto valor."),
            ("escudo", "Educación y salud", "Instituciones y ESAL con exigencias de su ente de vigilancia y del régimen tributario especial."),
            ("lupa", "Sector cafetero", "Cooperativas de caficultores, exportadoras y comercializadoras con operaciones de compra y exportación."),
        ],
        faq=[
            ("¿Las fundaciones e instituciones educativas de Manizales deben tener revisor fiscal?",
             "Depende. La ley no lo impone a todas las fundaciones, pero es obligatorio si sus estatutos lo exigen, si una norma especial lo pide o si lo exige la entidad que las vigila. Las cooperativas sí deben tenerlo siempre."),
            ("¿Cuáles son los topes de revisoría fiscal para 2027?",
             f"Activos brutos iguales o superiores a {TOPE_ACTIVOS} o ingresos brutos iguales o superiores a {TOPE_INGRESOS}, con las cifras al 31 de diciembre de 2026."),
            ("¿Atienden presencialmente en Manizales?",
             "Sí. Hacemos visitas en Manizales, Villamaría y Chinchiná, y complementamos con revisión remota durante el mes."),
            ("¿Dónde se inscribe el revisor fiscal en Caldas?",
             "En la Cámara de Comercio de Manizales por Caldas, con copia del acta de la asamblea o junta que lo eligió y su aceptación del cargo."),
        ],
    ),
}

GUIAS = ["empresas-obligadas-revisor-fiscal", "revisor-fiscal-sas", "como-elegir-firma-revisoria-fiscal",
         "cambiar-revisor-fiscal", "dictamen-revisor-fiscal", "cuanto-cobra-un-revisor-fiscal-en-colombia",
         "revisor-fiscal-esal-fundaciones", "funciones-revisor-fiscal-colombia"]

for c in CIUDADES:
    slug, nombre, depto = c["slug"], c["nombre"], c["depto"]
    d = RF[slug]
    otras = [x for x in CIUDADES if x["slug"] != slug]
    locales_html = "".join(f'<span class="etiqueta-enlace etiqueta-enlace--inerte">{x}</span>' for x in c["locales"])

    cuerpo = f"""
{heroe(
    d["titulo"],
    d["entrada"],
    f"ciudad-{slug}.jpg",
    f"Revisoría fiscal para empresas en {nombre}, {depto}",
    chip=f"Revisoría fiscal · {nombre}",
    migas=[("Inicio", "index.html"), ("Revisoría fiscal", "revisoria-fiscal.html"), (nombre, None)],
    cta1=("Evalúa si estás obligado", "evaluacion-revisoria-fiscal.html"),
    cta2=("Conversemos", wa(f"Hola, vengo de la página de revisoría fiscal en {nombre} y quiero una propuesta")),
    riel=[("Topes 2027", "Activos desde $8.754 M o ingresos desde $5.252 M"),
          ("NIA", "Normas de aseguramiento aplicadas"),
          (nombre, "Atención presencial y remota"),
          ("Art. 207", "Funciones del Código de Comercio")]
)}

<section class="seccion claro">
  <div class="contenedor">
    {encabezado(f"Empresas en {nombre}", f"Revisoría fiscal pensada para las empresas {c['gentilicio']}", d["contexto"])}
    {tarjetas_item(d["sectores"])}
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    {encabezado("Topes 2027", f"¿Tu empresa en {nombre} está obligada a tener revisor fiscal?", "Se mide con las cifras al 31 de diciembre de 2026. Basta con superar uno de los dos <a href=\"empresas-obligadas-revisor-fiscal.html\">topes para tener revisor fiscal</a>.")}
    {tarjetas_item([
        ("documento", "Activos desde $8.754 millones", f"Activos brutos iguales o superiores a 5.000 salarios mínimos: {TOPE_ACTIVOS}."),
        ("lupa", "Ingresos desde $5.252 millones", f"Ingresos brutos del año iguales o superiores a 3.000 salarios mínimos: {TOPE_INGRESOS}."),
        ("escudo", "Por tipo o por estatutos", 'Las sociedades anónimas siempre; las <a href="revisor-fiscal-sas.html">SAS</a> por topes; cooperativas y fondos de empleados por ley; fundaciones si sus estatutos lo piden.'),
    ])}
    <p class="centrado revelar" style="margin-top:2rem"><a class="btn btn--primario" href="evaluacion-revisoria-fiscal.html">Evalúa tu empresa gratis{ICO["flecha"]}</a></p>
  </div>
</section>

<section class="seccion claro">
  {fijo(
    encabezado("Cómo trabajamos", f"Un revisor fiscal presente durante todo el año en {nombre}",
               "No una firma en marzo: nuestro <a href=\"revisoria-fiscal.html\">servicio de revisoría fiscal</a> es un plan de trabajo con visitas, alertas e informes.",
               ancho="none", tam="var(--paso-4)"),
    [
        ("Diagnóstico y plan anual", "Revisamos la situación de la empresa, sus riesgos frente a la DIAN y la superintendencia, y fijamos un calendario de visitas y entregables."),
        ("Visitas y revisión permanente", f"Visitas presenciales en {c['zona']} y revisión remota de la contabilidad, el control interno y el cumplimiento tributario."),
        ("Alertas a tiempo", "Si encontramos una irregularidad, la informamos por escrito en el momento, no al cierre."),
        ("Cierre y dictamen", "Acompañamos el cierre contable y entregamos el <a href=\"dictamen-revisor-fiscal.html\">dictamen del revisor fiscal</a> y el <a href=\"informe-revisor-fiscal-asamblea.html\">informe a la asamblea</a> con tiempo para el derecho de inspección."),
        ("Firma de declaraciones", "Revisamos y firmamos las declaraciones tributarias que la ley exige con firma de revisor fiscal."),
    ]
  )}
</section>

{carrusel_clientes()}

{ultimas_publicaciones(solo=GUIAS, eyebrow="Guías de revisoría fiscal",
                       titulo="Antes de contratar, lee esto",
                       intro="Obligación, cambio de revisor, dictamen y honorarios, explicados con la norma en la mano.")}

<section class="seccion">
  <div class="contenedor">
    {encabezado("Cobertura", f"Revisoría fiscal en {c['zona']}", ancho="54rem", tam="var(--paso-4)")}
    <div class="directorio revelar">
      <div>
        <h3>{c['zona']}</h3>
        <div class="directorio__lista">{locales_html}</div>
      </div>
      <div>
        <h3>Revisoría fiscal en otras ciudades</h3>
        <div class="directorio__lista">
          {"".join(f'<a class="etiqueta-enlace" href="revisoria-fiscal-{o["slug"]}.html">{o["nombre"]}</a>' for o in otras)}
        </div>
      </div>
      <div>
        <h3>Contabilidad en {nombre}</h3>
        <div class="directorio__lista">
          <a class="etiqueta-enlace" href="outsourcing-contable-{slug}.html">Outsourcing contable en {nombre}</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="seccion claro">
  <div class="contenedor">
    <div class="fijo">
      <div class="fijo__ancla revelar">
        {encabezado("Preguntas frecuentes", f"Revisoría fiscal en {nombre}", ancho="none", tam="var(--paso-4)")}
      </div>
      {acordeon([(q, f"<p>{a}</p>") for q, a in d["faq"]], prefijo="rf" + slug[:3])}
    </div>
  </div>
</section>

{resenas_google()}

{cta_final(
    f"Tu revisor fiscal en {nombre}",
    "Cuéntanos el tamaño de tu empresa y te decimos si estás obligado, qué alcance necesitas y cuánto costaría.",
    boton="Quiero una propuesta",
    mensaje=f"Hola, vengo de la página de revisoría fiscal en {nombre} y quiero una propuesta",
    secundario=("Cotiza tu revisoría fiscal", f"/cotizacion-revisoria-fiscal/?ciudad={slug}"),
)}
"""

    schema = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Service",
                "name": f"Revisoría fiscal en {nombre}",
                "serviceType": "Revisoría fiscal",
                "description": f"Servicio de revisoría fiscal para sociedades, cooperativas y ESAL en {nombre}, {depto}.",
                "url": f"https://marinriosconsultores.com/revisoria-fiscal-{slug}/",
                "provider": {"@id": "https://marinriosconsultores.com/#empresa"},
                "areaServed": [lugar(x, depto) for x in c["locales"]],
            },
            {
                "@type": "FAQPage",
                "mainEntity": [{"@type": "Question", "name": q,
                                "acceptedAnswer": {"@type": "Answer", "text": a}}
                               for q, a in d["faq"]]
            }
        ]
    }, ensure_ascii=False, indent=2)

    PAGINAS.append(dict(
        archivo=f"revisoria-fiscal-{slug}.html",
        titulo={"pereira": "Revisoría Fiscal en Pereira y Dosquebradas | Marín Ríos",
                "armenia": "Revisoría Fiscal en Armenia, Quindío | Marín Ríos"}.get(
            slug, f"Revisoría Fiscal en {nombre} para Empresas | Marín Ríos"),
        descripcion=f"Revisor fiscal en {nombre}, {depto}: topes 2027, dictamen bajo NIA, visitas presenciales e informes claros para socios, bancos y la DIAN.",
        activo="servicios",
        og_img=f"ciudad-{slug}.jpg",
        schema=schema,
        cuerpo=cuerpo,
    ))
