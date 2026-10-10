# -*- coding: utf-8 -*-
"""
Landings de campaña y páginas de gracias migradas desde el WordPress.

Son las URLs que las campañas de Ads y los enlaces antiguos ya apuntan, así que
conservan su ruta exacta. Las de campaña van con `noindex`, igual que en el
WordPress, para que no compitan en búsqueda con las páginas de servicio.
"""

import json

from base import (ICO, wa, heroe, encabezado, tarjetas_item, servicios_num,
                  lista_check, acordeon, cta_final, marcas, directorio,
                  TEL, TEL_URI, EMAIL, WA, BASE_URL)
from paginas import PAGINAS, TRIO

NOINDEX = "noindex, follow"


# ================================================================
# /home/  ·  duplicado de la portada
# ================================================================
# En el WordPress esta URL servía la misma portada y estaba indexada, así que
# competía consigo misma. Aquí queda como una página de reenvío: canonical a la
# raíz, noindex y redirección inmediata.
cuerpo_home = f"""
<section class="seccion centrado">
  <div class="contenedor">
    <div class="encabezado-seccion" style="max-width:48rem;margin-inline:auto">
      <p class="eyebrow" style="justify-content:center">Redirigiendo</p>
      <h1 style="font-size:var(--paso-4)">Esta página se movió a la portada</h1>
      <p>Si no se te redirige automáticamente, <a href="index.html">entra aquí</a>.</p>
    </div>
  </div>
</section>
<script>window.location.replace("/");</script>
"""

PAGINAS.append(dict(
    archivo="home.html",
    titulo="Marín Ríos Consultores",
    descripcion="Esta dirección se movió a la portada de Marín Ríos Consultores.",
    activo="",
    og_img="equipo-ancho.jpg",
    robots=NOINDEX,
    schema="",
    cuerpo=cuerpo_home,
))


# ================================================================
# /landing-integral/  ·  elección de servicio
# ================================================================
cuerpo_integral = f"""
{heroe(
    "Empresa de servicios contables para pymes",
    "Encuentra aquí el servicio que necesitas: contabilidad al día, cumplimiento sin sobresaltos y números que sirven para decidir.",
    "detalle-documentos.jpg",
    "Servicios contables para pymes en Colombia",
    chip="Servicios · Contabilidad, revisoría y finanzas",
    cta1=("Pide una cotización", wa("Hola, quiero una cotización de sus servicios contables")),
    cta2=("Ver planes", "precios-outsourcing-contable.html"),
)}

<section class="seccion">
  <div class="contenedor">
    {encabezado("Elige tu servicio", "Tres líneas que puedes contratar por separado o combinadas",
                "Cada una responde a un momento distinto de la empresa.")}
    {servicios_num(TRIO)}
  </div>
</section>

{marcas()}

{cta_final(
    "¿No sabes cuál necesitas?",
    "Cuéntanos en qué estado está tu contabilidad y te decimos con claridad qué le hace falta a tu empresa.",
    boton="Conversemos",
    mensaje="Hola, quiero saber qué servicio contable necesita mi empresa",
)}
"""

PAGINAS.append(dict(
    archivo="landing-integral.html",
    titulo="Servicios contables para pymes | Marín Ríos Consultores",
    descripcion="Contabilidad, revisoría fiscal y consultoría financiera para pymes en Colombia. Encuentra el servicio que necesita tu empresa.",
    activo="",
    og_img="detalle-documentos.jpg",
    schema=json.dumps({
        "@context": "https://schema.org", "@type": "WebPage",
        "name": "Servicios contables para pymes",
        "url": BASE_URL + "landing-integral/",
        "publisher": {"@id": BASE_URL + "#empresa"},
    }, ensure_ascii=False, indent=2),
    cuerpo=cuerpo_integral,
))


# ================================================================
# /outsourcing-contable-ad/  ·  landing de campaña
# ================================================================
cuerpo_ad = f"""
{heroe(
    "¿Tu contabilidad está preparada para el nuevo salario mínimo?",
    "Los errores contables ahora salen más caros. Te ayudamos a liquidar bien, controlar el impacto en tus costos y evitar sanciones.",
    "reunion-ancho.jpg",
    "Equipo contable revisando el impacto del salario mínimo",
    chip="Outsourcing contable · Atención inmediata",
    cta1=("Habla con un asesor", wa("Hola, vengo del anuncio y quiero saber cómo me afecta el nuevo salario mínimo")),
)}

<section class="seccion--ajustada">
  <div class="contenedor">
    {encabezado("Te ayudamos a", "Lo que resolvemos desde el primer mes")}
    <div class="split">
      {lista_check([
          "Liquidar nómina y aportes con los nuevos valores.",
          "Evitar errores en liquidaciones e incapacidades.",
          "Controlar el impacto del salario mínimo en tus costos.",
          "Prevenir sanciones y requerimientos de la DIAN.",
      ])}
    </div>
  </div>
</section>

<section class="seccion claro">
  <div class="contenedor">
    {encabezado("Servicios", "Servicios de contabilidad para tu negocio",
                "Somos una alternativa ágil y flexible para empresas que no tienen equipo contable interno o necesitan apoyo experto.")}
    {tarjetas_item([
        ("documento", "Contabilidad general",
         "Gestión de impuestos y declaraciones, optimización fiscal, acuerdos de pago y nómina."),
        ("escudo", "Revisoría fiscal",
         "Análisis financiero, reducción de costos, plan de crecimiento y asignación de costos y gastos."),
        ("grafico", "Consultoría financiera",
         "Analizamos tu situación financiera, te orientamos a reducir costos y trazamos la ruta de tu crecimiento."),
    ])}
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    {encabezado("Por qué nosotros", "¿Por qué elegirnos como tu outsourcing contable?")}
    <div class="split">
      {lista_check([
          "Nos encargamos de toda tu gestión contable y de nómina.",
          "No interrumpimos tu operación ni tu ritmo de trabajo.",
          "Tendrás un equipo asignado y siempre disponible.",
          "Planes cotizados a la medida de tu empresa, sin cobros por consulta.",
      ])}
    </div>
  </div>
</section>

{marcas()}

{cta_final(
    "Hablemos antes de que llegue el cierre",
    "Cuéntanos cómo está tu contabilidad hoy y te decimos qué necesita tu empresa para el nuevo año.",
    boton="Habla con un asesor",
    mensaje="Hola, vengo del anuncio y quiero hablar con un asesor contable",
)}
"""

PAGINAS.append(dict(
    archivo="outsourcing-contable-ad.html",
    titulo="Consultoría contable para pymes en Colombia",
    descripcion="Despreocúpate por la contabilidad de tu negocio. Liquidación de nómina, impuestos y cumplimiento ante la DIAN, con un equipo asignado.",
    activo="",
    og_img="reunion-ancho.jpg",
    robots=NOINDEX,
    schema="",
    cuerpo=cuerpo_ad,
))


# ================================================================
# /vcl/  ·  captación con cuestionario de calificación
# ================================================================
# El formulario del WordPress enviaba los datos a una variable que nunca se
# configuró (`PEGA_AQUI_LA_URL_DE_TU_APPS_SCRIPT_WEB_APP`), y como el envío iba
# en `mode:"no-cors"` fallaba en silencio: el visitante veía «¡Listo!» y los
# datos se perdían. Aquí el formulario compone un mensaje de WhatsApp con todas
# las respuestas, de modo que el lead llegue de verdad sin depender de backend.
PREGUNTAS_VCL = [
    ("nombre", "¿Cuál es tu nombre completo?", "text", "Ej: Ximena Villalobos", "name"),
    ("whatsapp", "¿Cuál es tu WhatsApp?", "tel", "Ej: +57 300 000 0000", "tel"),
    ("correo", "¿Cuál es tu correo?", "email", "Ej: nombre@empresa.com", "email"),
    ("empresa", "¿Cuál es el nombre de tu empresa?", "text", "Ej: Mi Empresa S.A.S.", "organization"),
]

OPCIONES_VCL = [
    ("constitucion", "¿Cómo está constituido tu negocio?",
     ["Persona natural", "S.A.S.", "Ltda.", "S.A.", "Otra / aún no está constituido"]),
    ("ventas", "¿Cuáles son tus ventas mensuales aproximadas?",
     ["Menos de $20 millones", "Entre $20 y $50 millones",
      "Entre $50 y $150 millones", "Más de $150 millones"]),
    ("inversion", "¿Estás dispuesto a invertir mensualmente en un servicio contable profesional?",
     ["Sí, quiero avanzar", "Todavía no"]),
]


def _campos_vcl():
    campos = []
    for clave, etiqueta, tipo, ejemplo, autocompletar in PREGUNTAS_VCL:
        campos.append(f"""<div class="campo">
          <label for="f-{clave}">{etiqueta} <span aria-hidden="true">*</span></label>
          <input id="f-{clave}" name="{clave}" type="{tipo}" placeholder="{ejemplo}"
                 autocomplete="{autocompletar}" required>
        </div>""")
    for clave, etiqueta, opciones in OPCIONES_VCL:
        ops = "".join(f'<option value="{o}">{o}</option>' for o in opciones)
        campos.append(f"""<div class="campo">
          <label for="f-{clave}">{etiqueta} <span aria-hidden="true">*</span></label>
          <select id="f-{clave}" name="{clave}" required>
            <option value="" selected disabled>Elige una opción</option>
            {ops}
          </select>
        </div>""")
    return "\n        ".join(campos)


cuerpo_vcl = f"""
{heroe(
    "El outsourcing contable que evita que vuelvas a perder plata por una mala contabilidad",
    "Muchos gerentes descubren que su contabilidad estaba mal cuando ya les toca pagarle a la DIAN multas e impuestos más altos de lo que debían.",
    "reunion-ancho.jpg",
    "Equipo contable revisando los números de una empresa",
    chip="Para empresas que quieren tercerizar sin perder el control",
    cta1=("Aplicar ahora", "#aplicar"),
)}

<section class="seccion--ajustada">
  <div class="contenedor">
    {encabezado("La diferencia", "Tú diriges tu empresa, nosotros respondemos por tus números",
                "Mientras otras firmas entregan la contabilidad como un trámite mensual, aquí trabajamos con seguimiento directo y un equipo que responde.")}
    {tarjetas_item([
        ("escudo", "No somos una firma de papel",
         "Hay un equipo asignado que conoce tu operación, no una persona que aparece a fin de mes."),
        ("reloj", "Información cuando la necesitas",
         "Los números llegan a tiempo para decidir, no dos semanas después del cierre."),
        ("grafico", "Respondemos por las cifras",
         "Seguimiento directo sobre lo que se reporta, para que no aparezcan sorpresas frente a la DIAN."),
    ])}
  </div>
</section>

<section class="seccion claro" id="aplicar">
  <div class="contenedor">
    {encabezado("Aplicación", "Estás muy cerca de completar tu aplicación",
                "Responde estas preguntas y te escribimos por WhatsApp para agendar la llamada.")}
    <form class="formulario revelar" id="form-vcl" novalidate>
        {_campos_vcl()}
        <p class="formulario__nota">El valor del servicio se cotiza a la medida de tu empresa en la llamada.</p>
        <button class="btn btn--primario" type="submit">Enviar y agendar por WhatsApp {ICO['flecha']}</button>
        <p class="formulario__error" id="form-vcl-error" role="alert" hidden>Revisa los campos marcados antes de continuar.</p>
    </form>
  </div>
</section>

{marcas()}

{cta_final(
    "¿Prefieres escribirnos directamente?",
    "Si no quieres llenar el formulario, cuéntanos tu caso por WhatsApp y seguimos desde ahí.",
    boton="Escríbenos",
    mensaje="Hola, vengo de la página de aplicación y quiero hablar sobre la contabilidad de mi empresa",
)}

<script>
(function () {{
  var form = document.getElementById('form-vcl');
  if (!form) return;
  var error = document.getElementById('form-vcl-error');

  form.addEventListener('submit', function (e) {{
    e.preventDefault();
    if (!form.checkValidity()) {{
      error.hidden = false;
      form.reportValidity();
      return;
    }}
    error.hidden = true;

    // El lead viaja en el propio mensaje de WhatsApp: sin backend no hay
    // forma de guardarlo, pero así al menos llega completo y no se pierde.
    var d = new FormData(form);
    var lineas = ['Hola, vengo de la página de aplicación. Estos son mis datos:'];
    form.querySelectorAll('label').forEach(function (l) {{
      var campo = document.getElementById(l.getAttribute('for'));
      if (!campo) return;
      var etiqueta = l.textContent.replace('*', '').trim();
      lineas.push('- ' + etiqueta + ' ' + (campo.value || '').trim());
    }});
    var url = 'https://wa.me/{WA}?text=' + encodeURIComponent(lineas.join('\\n'));
    if (window.dataLayer) window.dataLayer.push({{ event: 'lead_vcl' }});
    window.location.href = url;
  }});
}})();
</script>
"""

PAGINAS.append(dict(
    archivo="vcl.html",
    titulo="Aplica para nuestro outsourcing contable | Marín Ríos",
    descripcion="Cuéntanos cómo está tu empresa y agenda una llamada con nuestro equipo de outsourcing contable.",
    activo="",
    og_img="reunion-ancho.jpg",
    robots=NOINDEX,
    schema="",
    cuerpo=cuerpo_vcl,
))


# ================================================================
# Páginas de gracias
# ================================================================
def _gracias(archivo, titulo_h1, entrada, extra=""):
    return f"""
{heroe(
    titulo_h1,
    entrada,
    "equipo-ancho.jpg",
    "Equipo de Marín Ríos Consultores",
    chip="Gracias por escribirnos",
    cta1=("Escríbenos por WhatsApp", wa("Hola, acabo de dejar mis datos en su sitio")),
)}
{extra}
<section class="seccion--ajustada">
  <div class="contenedor">
    {encabezado("Mientras tanto", "Puedes ir mirando esto",
                "Tres lecturas que suelen resolver las dudas más frecuentes antes de la primera llamada.")}
    <div class="rejilla-3 rejilla-movil revelar">
      <article class="tarjeta-item">
        <div class="tarjeta-item__icono">{ICO['tarjeta']}</div>
        <h3>Cuánto cuesta</h3>
        <p>Qué determina el valor de un outsourcing contable y cómo lo cotizamos.</p>
        <p><a class="etiqueta-enlace" href="precios-outsourcing-contable.html">Ver planes{ICO['flecha_fina']}</a></p>
      </article>
      <article class="tarjeta-item">
        <div class="tarjeta-item__icono">{ICO['escudo']}</div>
        <h3>¿Necesitas revisor fiscal?</h3>
        <p>Los topes de activos e ingresos que obligan a tener uno este año.</p>
        <p><a class="etiqueta-enlace" href="empresas-obligadas-revisor-fiscal.html">Revisar topes{ICO['flecha_fina']}</a></p>
      </article>
      <article class="tarjeta-item">
        <div class="tarjeta-item__icono">{ICO['libro']}</div>
        <h3>Blog</h3>
        <p>Impuestos, revisoría fiscal y finanzas explicados sin lenguaje técnico.</p>
        <p><a class="etiqueta-enlace" href="blog.html">Leer el blog{ICO['flecha_fina']}</a></p>
      </article>
    </div>
  </div>
</section>
"""


PAGINAS.append(dict(
    archivo="gracias-1.html",
    titulo="Gracias por contactarnos | Marín Ríos Consultores",
    descripcion="Gracias por dejarnos tus datos. Nos comunicamos contigo en unos minutos.",
    activo="",
    og_img="equipo-ancho.jpg",
    robots=NOINDEX,
    schema="",
    cuerpo=_gracias(
        "gracias-1.html",
        "Gracias por contactarnos, ¡ya te hablamos!",
        "En unos minutos conversamos contigo. Si prefieres adelantar, escríbenos por WhatsApp.",
    ),
))

PAGINAS.append(dict(
    archivo="thank-you-organico.html",
    titulo="Gracias por dejarnos tus datos | Marín Ríos Consultores",
    descripcion="Gracias por dejarnos tus datos. Estamos a un paso de conocernos.",
    activo="",
    og_img="equipo-ancho.jpg",
    robots=NOINDEX,
    schema="",
    cuerpo=_gracias(
        "thank-you-organico.html",
        "Estamos a un paso de conocernos",
        "Gracias por dejarnos tus datos. En unos minutos nos comunicamos contigo.",
        extra=f"""
<section class="seccion claro">
  <div class="contenedor">
    {encabezado("Hacia dónde vamos", "Lo que buscamos lograr contigo")}
    <div class="split">
      {lista_check([
          "Orientar tus esfuerzos hacia objetivos más estratégicos.",
          "Abaratar los costos de contratación de tu área contable.",
          "Conectarte con profesionales confiables, de forma personalizada.",
      ])}
    </div>
  </div>
</section>""",
    ),
))
