# -*- coding: utf-8 -*-
"""
Páginas institucionales: contáctenos, nosotros y política de privacidad.

Las tres existían en el WordPress y estaban enlazadas desde el pie, así que
tienen que seguir viviendo en las mismas URLs (`/contactenos/`, `/nosotros/`
y `/politica-de-privacidad/`) para que la migración no deje huecos.
"""

import json

from base import (ICO, wa, heroe, encabezado, tarjetas_item, servicios_num,
                  cta_final, proposito, marcas, directorio,
                  TEL, TEL_URI, EMAIL, DIR, BASE_URL)
from paginas import PAGINAS, TRIO

MAPA = ("https://maps.google.com/?q=Cl.+49B+%2364b-54,+Laureles+-+Estadio,+Medell%C3%ADn")


# ================================================================
# CONTÁCTENOS
# ================================================================
cuerpo_contacto = f"""
{heroe(
    "Habla con nosotros",
    "Estamos listos para construir contigo una estrategia que te ayude a alcanzar tus objetivos financieros. Cuéntanos en qué estado está tu contabilidad y te decimos con claridad qué necesita tu empresa.",
    "reunion-ancho.jpg",
    "Equipo de Marín Ríos Consultores atendiendo a un cliente",
    chip="Contacto · Respuesta el mismo día",
    migas=[("Inicio", "index.html"), ("Contacto", None)],
    cta1=("Escríbenos por WhatsApp", wa("Hola, quiero hablar con un asesor sobre la contabilidad de mi empresa")),
    cta2=("Ver planes", "/cuanto-cuesta-contratar-un-servicio-de-outsourcing-contable/#planes"),
)}

<section class="seccion--ajustada">
  <div class="contenedor">
    {encabezado("Por dónde empezar", "Tres formas de contactarnos",
                "Elige la que te quede más cómoda. En cualquiera de las tres te responde una persona del equipo, no un formulario automático.")}
    <div class="rejilla-3 rejilla-movil revelar">
      <article class="tarjeta-item">
        <div class="tarjeta-item__icono">{ICO['wa']}</div>
        <h3>WhatsApp</h3>
        <p>La vía más rápida. Escríbenos y coordinamos una llamada el mismo día.</p>
        <p><a class="etiqueta-enlace" href="{wa('Hola, quiero hablar con un asesor sobre la contabilidad de mi empresa')}">{TEL}{ICO['flecha_fina']}</a></p>
      </article>
      <article class="tarjeta-item">
        <div class="tarjeta-item__icono">{ICO['correo']}</div>
        <h3>Correo</h3>
        <p>Si prefieres dejar el caso por escrito y adjuntar documentos.</p>
        <p><a class="etiqueta-enlace" href="mailto:{EMAIL}">{EMAIL}{ICO['flecha_fina']}</a></p>
      </article>
      <article class="tarjeta-item">
        <div class="tarjeta-item__icono">{ICO['pin']}</div>
        <h3>Oficina</h3>
        <p>{DIR}, Medellín. Atendemos con cita previa.</p>
        <p><a class="etiqueta-enlace" href="{MAPA}" target="_blank" rel="noopener">Ver en el mapa{ICO['flecha_fina']}</a></p>
      </article>
    </div>
  </div>
</section>

<section class="seccion claro">
  <div class="contenedor">
    {encabezado("Qué obtienes", "¿Qué obtengo con este servicio?",
                "Un backoffice contable y financiero para tu negocio, con un equipo comprometido con tu crecimiento.")}
    {tarjetas_item([
        ("gente", "Un equipo, no una sola persona",
         "Especialistas que dan soporte a la gestión interna de tu negocio, con quien responda si alguien falta."),
        ("engranaje", "Operación sin interrupciones",
         "Tu contabilidad sigue su ritmo mientras tú trazas la ruta para cumplir los objetivos estratégicos."),
        ("grafico", "Menos costo fijo",
         "No necesitas sostener un departamento contable ni comprar el último software: esa inversión la hacemos nosotros."),
    ])}
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    {encabezado("Cobertura", "Dónde atendemos",
                "Operamos de forma remota en todo el país y presencialmente en Antioquia y el Eje Cafetero.")}
    {directorio()}
  </div>
</section>

{cta_final(
    "Cuéntanos qué necesita tu empresa",
    "Escríbenos con la situación concreta de tu contabilidad y te respondemos con una recomendación, no con un catálogo.",
    boton="Conversemos",
    mensaje="Hola, quiero hablar con un asesor sobre la contabilidad de mi empresa",
)}
"""

PAGINAS.append(dict(
    archivo="contactenos.html",
    titulo="Contacto | Marín Ríos Consultores",
    descripcion="Habla con un asesor contable de Marín Ríos Consultores. WhatsApp, correo y oficina en Medellín. Te respondemos el mismo día.",
    activo="",
    og_img="reunion-ancho.jpg",
    schema=json.dumps({
        "@context": "https://schema.org",
        "@type": "ContactPage",
        "name": "Contacto — Marín Ríos Consultores",
        "url": BASE_URL + "contactenos/",
        "mainEntity": {
            "@type": "AccountingService",
            "@id": BASE_URL + "#empresa",
            "name": "Marín Ríos Consultores",
            "telephone": TEL,
            "email": EMAIL,
            "address": {"@type": "PostalAddress", "streetAddress": DIR,
                        "addressLocality": "Medellín", "addressRegion": "Antioquia",
                        "addressCountry": "CO"},
        },
    }, ensure_ascii=False, indent=2),
    cuerpo=cuerpo_contacto,
))


# ================================================================
# NOSOTROS
# ================================================================
cuerpo_nosotros = f"""
{heroe(
    "Estamos obsesionados con el crecimiento",
    "Marín Ríos Consultores nace para ayudar a los empresarios a gestionar con eficacia los recursos de su empresa, dándoles las herramientas para decidir con cifras y no con intuición.",
    "equipo-ancho.jpg",
    "Equipo de Marín Ríos Consultores",
    chip="Nosotros · Contadores y consultores",
    migas=[("Inicio", "index.html"), ("Nosotros", None)],
    cta1=("Conversemos", wa("Hola, quiero conocer más sobre Marín Ríos Consultores")),
    riel=[("+50", "Empresas acompañadas"),
          ("4", "Ciudades con atención presencial"),
          ("3", "Líneas de servicio")],
)}

{proposito(
    "Qué hacemos y por qué",
    "Nuestros servicios se centran en identificar, analizar y gestionar los riesgos de las empresas. Trabajamos junto a nuestros clientes para ayudarles a construir una operación financiera que aguante el crecimiento.",
    "Para eso los acompañamos en los riesgos propios de su negocio —el de crédito, el de mercado y el operativo— y en la disciplina contable que permite verlos a tiempo.",
    boton="Hablemos de tu empresa",
    mensaje="Hola, quiero conocer más sobre Marín Ríos Consultores",
)}

<section class="seccion claro">
  <div class="contenedor">
    {encabezado("Cómo trabajamos", "Tres principios que no negociamos")}
    {tarjetas_item([
        ("reloj", "Información a tiempo",
         "Los números sirven cuando llegan cuando se necesitan, no dos semanas después del cierre."),
        ("gente", "Un equipo detrás",
         "La contabilidad de una empresa no puede depender de una sola persona ni de su memoria."),
        ("escudo", "Cumplimiento sin sobresaltos",
         "Las obligaciones se atienden antes de la fecha límite, no sobre el vencimiento."),
    ])}
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    {encabezado("Servicios", "En qué podemos acompañarte",
                "Tres líneas que puedes contratar por separado o combinadas.")}
    {servicios_num(TRIO)}
  </div>
</section>

{marcas()}

{cta_final(
    "¿Conversamos sobre tu empresa?",
    "Cuéntanos en qué estado está tu contabilidad y te decimos con claridad qué necesita y cuánto costaría.",
    boton="Agenda una asesoría",
    mensaje="Hola, quiero agendar una asesoría con Marín Ríos Consultores",
)}
"""

PAGINAS.append(dict(
    archivo="nosotros.html",
    titulo="Nosotros | Marín Ríos Consultores",
    descripcion="Marín Ríos Consultores acompaña a pymes colombianas en contabilidad, revisoría fiscal y consultoría financiera. Conoce cómo trabajamos.",
    activo="",
    og_img="equipo-ancho.jpg",
    schema=json.dumps({
        "@context": "https://schema.org",
        "@type": "AboutPage",
        "name": "Nosotros — Marín Ríos Consultores",
        "url": BASE_URL + "nosotros/",
        "mainEntity": {"@id": BASE_URL + "#empresa"},
    }, ensure_ascii=False, indent=2),
    cuerpo=cuerpo_nosotros,
))


# ================================================================
# POLÍTICA DE PRIVACIDAD
# ================================================================
# El pie de todas las páginas enlaza aquí, así que la página no puede faltar.
# Lo que sigue recoge lo que la Ley 1581 de 2012 y el Decreto 1377 de 2013
# exigen; las finalidades y los plazos concretos los debe confirmar la firma.
POLITICA = [
    ("h2", "Responsable del tratamiento"),
    ("p", f"<strong>Marín Ríos Consultores</strong>, con domicilio en {DIR}, Medellín (Antioquia), Colombia, "
          f"es responsable del tratamiento de los datos personales que se recogen a través de este sitio web. "
          f"Puedes contactarnos en <a href=\"mailto:{EMAIL}\">{EMAIL}</a> o en el teléfono "
          f"<a href=\"tel:{TEL_URI}\">{TEL}</a>."),

    ("h2", "Qué datos recogemos"),
    ("p", "Solo tratamos los datos que nos entregas de forma voluntaria cuando nos escribes por WhatsApp, "
          "por correo electrónico o cuando nos contactas para solicitar una asesoría: nombre, teléfono, "
          "correo electrónico y el nombre de tu empresa."),
    ("p", "El sitio también utiliza herramientas de analítica que registran datos de navegación de forma agregada, "
          "con el fin de entender cómo se usa la página."),

    ("h2", "Para qué usamos tus datos"),
    ("ul", [
        "Responder las solicitudes de contacto y de cotización que nos envías.",
        "Prestar y administrar los servicios contables, de revisoría fiscal y de consultoría financiera que contrates.",
        "Cumplir las obligaciones legales, contables y tributarias derivadas de esa relación.",
        "Enviarte información sobre nuestros servicios, siempre que lo hayas autorizado y hasta que decidas lo contrario.",
    ]),

    ("h2", "Tus derechos como titular"),
    ("p", "De acuerdo con el artículo 8 de la Ley 1581 de 2012, en cualquier momento puedes:"),
    ("ul", [
        "Conocer, actualizar y rectificar tus datos personales.",
        "Solicitar prueba de la autorización que nos otorgaste, salvo en los casos en que la ley no la exige.",
        "Ser informado sobre el uso que le hemos dado a tus datos.",
        "Presentar quejas ante la Superintendencia de Industria y Comercio por infracciones a la ley.",
        "Revocar la autorización o solicitar la supresión de tus datos, cuando no exista un deber legal o contractual que lo impida.",
        "Acceder de forma gratuita a los datos personales que hayan sido objeto de tratamiento.",
    ]),

    ("h2", "Cómo ejercer tus derechos"),
    ("p", f"Escríbenos a <a href=\"mailto:{EMAIL}\">{EMAIL}</a> indicando tu nombre, la forma de contactarte "
          f"y la solicitud concreta. Damos respuesta a las consultas en un plazo máximo de diez (10) días hábiles "
          f"y a los reclamos en un plazo máximo de quince (15) días hábiles, conforme a los artículos 14 y 15 "
          f"de la Ley 1581 de 2012."),

    ("h2", "Seguridad y conservación"),
    ("p", "Aplicamos medidas razonables para proteger la información frente a accesos no autorizados, pérdida o "
          "alteración. Conservamos los datos mientras se mantenga la relación comercial y, después, durante el "
          "tiempo que exijan las obligaciones legales aplicables a la actividad contable."),

    ("h2", "Cambios en esta política"),
    ("p", "Si modificamos esta política, publicaremos la versión actualizada en esta misma página. Te recomendamos "
          "revisarla periódicamente."),
]


def _politica_html():
    partes = []
    for tipo, contenido in POLITICA:
        if tipo == "ul":
            items = "".join(f"<li>{x}</li>" for x in contenido)
            partes.append(f"<ul>{items}</ul>")
        else:
            partes.append(f"<{tipo}>{contenido}</{tipo}>")
    return "\n      ".join(partes)


cuerpo_politica = f"""
{heroe(
    "Política de privacidad",
    "Cómo tratamos los datos personales que nos confías cuando contactas a Marín Ríos Consultores.",
    "detalle-documentos.jpg",
    "Documentos y política de tratamiento de datos personales",
    chip="Legal · Ley 1581 de 2012",
    migas=[("Inicio", "index.html"), ("Política de privacidad", None)],
)}

<section class="seccion--ajustada">
  <div class="contenedor">
    <div class="entrada">
      <article class="entrada__cuerpo">
      {_politica_html()}
      </article>
    </div>
  </div>
</section>
"""

PAGINAS.append(dict(
    archivo="politica-de-privacidad.html",
    titulo="Política de privacidad | Marín Ríos Consultores",
    descripcion="Política de tratamiento de datos personales de Marín Ríos Consultores, conforme a la Ley 1581 de 2012 y el Decreto 1377 de 2013.",
    activo="",
    og_img="detalle-documentos.jpg",
    schema=json.dumps({
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": "Política de privacidad",
        "url": BASE_URL + "politica-de-privacidad/",
        "publisher": {"@id": BASE_URL + "#empresa"},
    }, ensure_ascii=False, indent=2),
    cuerpo=cuerpo_politica,
))
