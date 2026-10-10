# -*- coding: utf-8 -*-
"""
Marín Ríos Consultores — plantilla y componentes compartidos.
Todas las páginas se arman con estas piezas para que cabecera, pie,
SEO y módulos sean idénticos en todo el sitio.
"""

import re

TEL = "+57 314 884 3835"
TEL_URI = "+573148843835"
WA = "573148843835"
EMAIL = "j@marinriosconsultores.com"
DIR = "Cl. 49B #64b-54, Laureles - Estadio"
BASE_URL = "https://marinriosconsultores.com/"

# ---------------------------------------------------------------- autor
# Todos los artículos del blog los firma el director de la firma. El perfil de
# LinkedIn no es decorativo: es lo que Google usa para ligar a la persona real
# con lo que publica, así que va tanto en el enlace visible como en el `sameAs`
# de los datos estructurados. Si cambia el autor, se cambia aquí y cae en los 41.
AUTOR_NOMBRE = "Juan David Marín Ríos"
AUTOR_CARGO = "Contador público · Director de Marín Ríos Consultores"
AUTOR_LINKEDIN = "https://www.linkedin.com/in/juan-david-marin-55668217b/"
AUTOR_ID = BASE_URL + "#autor"
# Se nombra en .png porque `imagenes_webp` traduce la extensión al final,
# igual que con el resto de las fotos del sitio.
AUTOR_FOTO = "assets/img/autor-juan-david.png"
AUTOR_BIO = ("Acompaña a empresas de Medellín, Pereira, Armenia y Manizales en outsourcing "
             "contable, revisoría fiscal y consultoría financiera. Escribe en este blog sobre "
             "lo que ve todos los días en los cierres y en las auditorías.")

# Contenedor de Google Tag Manager. Es el mismo que carga el WordPress, así que
# al cambiar de sitio la medición y las conversiones de Ads siguen funcionando
# sin tocar nada del lado de Google.
GTM_ID = "GTM-NF8T2Q8"

GTM_HEAD = f"""<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','{GTM_ID}');</script>
<!-- End Google Tag Manager -->"""

GTM_BODY = f"""<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->"""

# El sitio no publica tarifas: todos los servicios se cotizan a la medida.
# No reintroducir precios en pesos ni en SMMLV en ninguna página.


def wa(texto):
    from urllib.parse import quote
    return f"https://wa.me/{WA}?text={quote(texto)}"


# ---------------------------------------------------------------- iconos
ICO = {
    "flecha": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "flecha_fina": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "atras": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>',
    "diagonal": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M7 17L17 7M8 7h9v9"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" aria-hidden="true"><path d="M5 13l4 4L19 7"/></svg>',
    "escudo": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M12 3l8 3v6c0 5-3.4 8.3-8 9-4.6-.7-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/></svg>',
    "libro": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M4 19V5a2 2 0 012-2h12a2 2 0 012 2v14l-4-2-4 2-4-2z"/></svg>',
    "documento": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M14 3H7a2 2 0 00-2 2v14a2 2 0 002 2h10a2 2 0 002-2V8z"/><path d="M14 3v5h5M9 14h6M9 17h4"/></svg>',
    "tarjeta": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M3 7h18v12H3z"/><path d="M3 11h18M7 15h4"/></svg>',
    "lupa": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>',
    "grafico": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M3 17l5-5 4 3 8-8"/><path d="M15 7h5v5"/></svg>',
    "barras": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M3 20h18"/><path d="M6 20V10M11 20V4M16 20v-7M21 20v-3"/></svg>',
    "gente": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="9" cy="8" r="3.4"/><path d="M2.5 20a6.5 6.5 0 0113 0"/><path d="M16 5.2a3.4 3.4 0 010 5.6M18 20a6.6 6.6 0 00-2-4.7"/></svg>',
    "reloj": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.2 2"/></svg>',
    "candado": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M5 11h14v10H5z"/><path d="M8 11V7a4 4 0 018 0v4"/></svg>',
    "engranaje": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="12" cy="12" r="3.2"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M19.1 4.9L17 7M7 17l-2.1 2.1"/></svg>',
    "tel": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M22 16.9v3a2 2 0 01-2.2 2 19.8 19.8 0 01-8.6-3.1 19.5 19.5 0 01-6-6A19.8 19.8 0 012.1 4.2 2 2 0 014.1 2h3a2 2 0 012 1.7c.1 1 .4 1.9.7 2.8a2 2 0 01-.4 2.1L8.1 9.9a16 16 0 006 6l1.3-1.3a2 2 0 012.1-.4c.9.3 1.8.6 2.8.7a2 2 0 011.7 2z"/></svg>',
    "correo": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M4 4h16v16H4z"/><path d="M4 6l8 6 8-6"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M12 21s7-5.5 7-11a7 7 0 10-14 0c0 5.5 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/></svg>',
    "wa": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>',
    "linkedin": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 11-.02 5 2.5 2.5 0 01.02-5zM3 9h4v12H3zM10 9h3.8v1.7h.05c.53-.95 1.83-1.95 3.77-1.95 4.03 0 4.78 2.5 4.78 5.76V21h-4v-5.6c0-1.34-.03-3.06-1.9-3.06-1.9 0-2.2 1.45-2.2 2.96V21h-4z"/></svg>',
}

# El logo original de la firma, tomado del WordPress (Marin-rios-3.png).
# Tiene las letras en blanco: solo funciona sobre fondo oscuro.
LOGO = """<span class="logo">
      <img class="logo__original" src="assets/img/logo-marin-rios.png" alt="Marín Ríos Consultores" width="90" height="80">
    </span>"""


def cabecera(activo=""):
    def act(clave):
        return ' aria-current="page"' if activo == clave else ""
    return f"""<header class="cabecera">
  <div class="contenedor cabecera__inner">
    <a class="logo" href="index.html" aria-label="Marín Ríos Consultores, inicio">
      <img class="logo__original" src="assets/img/logo-marin-rios.png" alt="" width="90" height="80">
    </a>

    <nav class="nav" data-abierto="false" aria-label="Menú principal">
      <ul class="nav__lista">
        <li class="nav__item" data-abierto="false">
          <a class="nav__enlace nav__toggle" href="outsourcing-contable.html" aria-expanded="false"{act('servicios')}>
            Servicios
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>
          </a>
          <div class="submenu">
            <a href="outsourcing-contable.html">Outsourcing contable<small>Tu operación contable completa</small></a>
            <a href="revisoria-fiscal.html">Revisoría fiscal<small>Cumplimiento y control independiente</small></a>
            <a href="consultoria-financiera.html">Consultoría financiera<small>Decisiones con datos reales</small></a>
          </div>
        </li>
        <li><a class="nav__enlace" href="precios-outsourcing-contable.html"{act('precios')}>Planes</a></li>
        <li><a class="nav__enlace" href="blog.html"{act('blog')}>Blog</a></li>
      </ul>
      <a class="btn btn--primario btn--wa" href="{wa('Hola, vengo de su sitio web y quiero agendar una asesoría contable')}">{ICO['wa']}Agenda Asesoría</a>
    </nav>

    <button class="menu-btn" aria-expanded="false" aria-label="Abrir menú">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
    </button>
  </div>
</header>"""


PIE = f"""<footer class="pie">
  <div class="contenedor">
    <div class="pie__grid">
      <div>
        <div class="pie__logo">{LOGO}</div>
        <p>Firma de outsourcing contable, revisoría fiscal y consultoría financiera para pymes en Antioquia y el Eje Cafetero.</p>
      </div>

      <div>
        <h4>Servicios</h4>
        <ul>
          <li><a href="outsourcing-contable.html">Outsourcing contable</a></li>
          <li><a href="consultoria-financiera.html">Consultoría financiera</a></li>
          <li><a href="revisoria-fiscal.html">Revisoría fiscal</a></li>
          <li><a href="precios-outsourcing-contable.html">Planes</a></li>
        </ul>
      </div>

      <div>
        <h4>Ciudades</h4>
        <ul>
          <li><a href="outsourcing-contable-medellin.html">Medellín</a></li>
          <li><a href="outsourcing-contable-armenia.html">Armenia</a></li>
          <li><a href="outsourcing-contable-pereira.html">Pereira</a></li>
          <li><a href="outsourcing-contable-manizales.html">Manizales</a></li>
          <li><a href="blog.html">Blog</a></li>
          <li><a href="nosotros.html">Nosotros</a></li>
        </ul>
      </div>

      <div>
        <h4>Contacto</h4>
        <ul class="pie__contacto">
          <li>{ICO['pin']}<span>{DIR}<br>Medellín, Colombia</span></li>
          <li>{ICO['tel']}<a href="tel:{TEL_URI}">{TEL}</a></li>
          <li>{ICO['correo']}<a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>{ICO['gente']}<a href="contactenos.html">Contáctanos</a></li>
        </ul>
      </div>
    </div>

    <div class="pie__legal">
      <span>© <span data-anio>2026</span> Marín Ríos Consultores. Todos los derechos reservados.</span>
      <span><a href="politica-de-privacidad.html">Política de privacidad</a></span>
      <span>No hacemos declaración de renta ni de ingresos para personas naturales.</span>
    </div>
  </div>
</footer>

<a class="wa-flotante" href="{wa('Hola, vengo de su sitio web y quiero saber más de sus servicios contables')}" aria-label="Escríbenos por WhatsApp" target="_blank" rel="noopener">
  {ICO['wa']}
</a>

<!-- Barra de acción fija, solo en celular (reemplaza el botón flotante) -->
<nav class="barra-movil" aria-label="Contacto rápido">
  <a class="barra-movil__tel" href="tel:{TEL_URI}">{ICO['tel']}<span>Llamar</span></a>
  <a class="barra-movil__wa" href="{wa('Hola, vengo de su sitio web y quiero agendar una asesoría contable')}" target="_blank" rel="noopener">{ICO['wa']}<span>Agenda tu asesoría</span></a>
</nav>

<script src="assets/js/main.js"></script>"""



# ---------------------------------------------------------------- modo landing
# Las landings de pauta (Meta, Google) van sin menú ni pie con enlaces: cada
# clic que se va a otra página es un lead que no llena el formulario.
def cabecera_landing(boton_texto="", boton_href=""):
    boton = (f'<a class="btn btn--primario" href="{boton_href}">{boton_texto}</a>'
             if boton_texto else "")
    return f"""<header class="cabecera cabecera--landing">
  <div class="contenedor cabecera__inner">
    <span class="logo">
      <img class="logo__original" src="assets/img/logo-marin-rios.png" alt="Marín Ríos Consultores" width="90" height="80">
    </span>
    {boton}
  </div>
</header>"""


PIE_LANDING = f"""<footer class="pie pie--landing">
  <div class="contenedor">
    <div class="pie__legal">
      <span>© <span data-anio>2026</span> Marín Ríos Consultores · {DIR}, Medellín</span>
      <span><a href="politica-de-privacidad.html">Política de privacidad</a></span>
    </div>
  </div>
</footer>

<a class="wa-flotante" href="{wa('Hola, vengo de la página de revisoría fiscal y tengo una pregunta')}" aria-label="Escríbenos por WhatsApp" target="_blank" rel="noopener">
  {ICO['wa']}
</a>

<nav class="barra-movil barra-movil--landing" aria-label="Acción rápida">
  <a class="barra-movil__wa" href="{wa('Hola, vengo de la página de revisoría fiscal y tengo una pregunta')}" target="_blank" rel="noopener" aria-label="Escribir por WhatsApp">{ICO['wa']}</a>
  <a class="barra-movil__cta" href="#agendar"><span>Agendar evaluación gratuita</span></a>
</nav>

<script src="assets/js/main.js"></script>"""


# ---------------------------------------------------------------- reseñas de Google
# Reseñas reales del perfil de Google de la firma, copiadas tal cual.
# estrellas: número de 1 a 5, o None si no se ha confirmado (no se inventan).
RESENAS = [
    dict(nombre="Jorge Mario Rojas", detalle="6 opiniones en Google", estrellas=None,
         texto="Agradezco enormemente sus servicios, me han brindado soluciones a todos los inconvenientes contanbles con los que una empresa se puede encontrar. Nada más agradable que sentir un aliado estratégico de confianza."),
    dict(nombre="Sol Yaneth Castrillon Jimenez", detalle="Local Guide · 8 opiniones", estrellas=None,
         texto="Es una empresa seria y comprometida, sus profesionales son excelentes, aparte de conocimiento tienen calidad humana y gran sentido de pertenencia."),
    dict(nombre="Andres Tette", detalle="3 opiniones en Google", estrellas=None,
         texto="Muy eficiente y claro."),
]
# Resumen del perfil. None = no se muestra hasta confirmarlo en Google.
GOOGLE_NOTA = None        # p. ej. "5.0"
GOOGLE_TOTAL = None       # p. ej. 12
GOOGLE_URL = "https://www.google.com/maps/search/?api=1&query=Mar%C3%ADn%20R%C3%ADos%20Consultores%20Medell%C3%ADn"

G_LOGO = ('<svg class="g-logo" viewBox="0 0 48 48" aria-hidden="true">'
          '<path fill="#FFC107" d="M43.6 20.1H42V20H24v8h11.3c-1.6 4.7-6.1 8-11.3 8-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 8 3l5.7-5.7C34 6.1 29.3 4 24 4 13 4 4 13 4 24s9 20 20 20 20-9 20-20c0-1.3-.1-2.6-.4-3.9z"/>'
          '<path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 8 3l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/>'
          '<path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2A11.9 11.9 0 0124 36c-5.2 0-9.6-3.3-11.3-7.9l-6.5 5C9.5 39.6 16.2 44 24 44z"/>'
          '<path fill="#1976D2" d="M43.6 20.1H42V20H24v8h11.3a12 12 0 01-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.6-.4-3.9z"/></svg>')

_AVATAR = ["#1A73E8", "#0F9D58", "#DB4437", "#7B1FA2", "#F4B400", "#00897B"]


def resenas_google(titulo="Lo que dicen las empresas que acompañamos",
                   kicker="Opiniones de Marín Ríos en Google", variante=""):
    """Carrusel de reseñas de Google, al estilo del de PorContar.
    Usa el carrusel genérico de main.js (.carrusel). variante="oscuro" para
    fondos negros (landing de Meta)."""
    def estrellas(n):
        if not n:
            return ""
        return f'<span class="resena__estrellas" aria-label="{n} de 5 estrellas">{"★" * n}{"☆" * (5 - n)}</span>'
    tarjetas = []
    for i, r in enumerate(RESENAS):
        ini = r["nombre"][0].upper()
        tarjetas.append(f"""<article class="resena">
          <div class="resena__cab">
            <span class="resena__avatar" style="background:{_AVATAR[i % len(_AVATAR)]}" aria-hidden="true">{ini}</span>
            <div class="resena__id"><strong>{r["nombre"]}</strong><small>{r["detalle"]}</small></div>
            {G_LOGO}
          </div>
          {estrellas(r["estrellas"])}
          <p>{r["texto"]}</p>
        </article>""")
    resumen = []
    if GOOGLE_NOTA:
        resumen.append(f'<b>{GOOGLE_NOTA}</b><span class="resenas__estrellas" aria-hidden="true">★★★★★</span>')
    resumen.append(f'<span>{GOOGLE_TOTAL} reseñas en Google</span>' if GOOGLE_TOTAL
                   else '<span>Reseñas verificadas en Google</span>')
    flecha_i = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><path d="M15 6l-6 6 6 6"/></svg>'
    flecha_d = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg>'
    clase = f"resenas resenas--{variante}" if variante else "resenas"
    return f"""<section class="seccion {clase}">
  <div class="contenedor">
    <div class="resenas__cabecera revelar">
      <p class="eyebrow">{kicker}</p>
      <h2>{titulo}</h2>
      <div class="resenas__resumen">{G_LOGO}{"".join(resumen)}<a href="{GOOGLE_URL}" target="_blank" rel="noopener">Ver en Google →</a></div>
    </div>
    <div class="carrusel resenas__carrusel revelar">
      <button class="carrusel__btn resenas__nav resenas__nav--i" data-dir="anterior" aria-label="Reseña anterior">{flecha_i}</button>
      <div class="carrusel__pista resenas__pista" role="group" aria-label="Reseñas de Google">
        {"".join(tarjetas)}
      </div>
      <button class="carrusel__btn resenas__nav resenas__nav--d" data-dir="siguiente" aria-label="Reseña siguiente">{flecha_d}</button>
    </div>
  </div>
</section>"""

def ruta_publica(archivo):
    """'outsourcing-contable.html' -> '/outsourcing-contable/'   ·   'index.html' -> '/'"""
    return "/" if archivo == "index.html" else "/" + archivo[:-len(".html")] + "/"


def enlaces_absolutos(html):
    """Pasa los enlaces del constructor a rutas absolutas del sitio.

    Las páginas se publican como `slug/index.html` para que la URL sea
    `/slug/`, igual que en el WordPress. Con esa estructura un enlace
    relativo como `blog.html` se resolvería contra `/slug/`, así que todos
    los destinos internos tienen que salir de la raíz.
    """
    html = re.sub(r'(href|src)="([a-z0-9][a-z0-9-]*\.html)"',
                  lambda m: f'{m.group(1)}="{ruta_publica(m.group(2))}"', html)
    return re.sub(r'(href|src)="(assets/)', r'\1="/\2', html)


def versionar_recursos(html):
    """Agrega ?v=<huella> a cada CSS y JS propio.

    Hostinger le dice al navegador que guarde CSS y JS por 30 días; sin esto,
    quien ya visitó el sitio sigue viendo los estilos viejos aunque se publique
    una versión nueva. La huella cambia solo cuando cambia el archivo."""
    import hashlib, os
    raiz = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sitio")

    def huella(m):
        ruta = m.group(2)
        try:
            with open(os.path.join(raiz, ruta.lstrip("/")), "rb") as f:
                h = hashlib.md5(f.read()).hexdigest()[:8]
        except OSError:
            return m.group(0)
        return f'{m.group(1)}="{ruta}?v={h}"'
    return re.sub(r'(href|src)="(/assets/(?:css|js)/[^"?]+\.(?:css|js))"', huella, html)


def imagenes_webp(html):
    """Apunta las imágenes a su versión WebP.

    Los archivos del sitio se convirtieron a WebP (la mitad de peso), pero los
    módulos siguen nombrándolas como .jpg o .png porque así se leen mejor. La
    traducción se hace aquí, en un solo sitio, igual que con los enlaces.
    """
    return re.sub(r'(/assets/img/[^"\']+?)\.(?:jpe?g|png)\b', r'\1.webp', html)


def plantilla(archivo, titulo, descripcion, cuerpo, activo="", schema="", og_img="equipo-ancho.jpg",
              robots="index, follow, max-snippet:-1, max-image-preview:large",
              css_extra=(), fuentes_extra="", clase_body="", landing=None):
    """Envuelve el contenido de una página con head, cabecera y pie.

    css_extra / fuentes_extra / clase_body permiten que una página cargue una
    capa visual propia (la portada corporativa) sin afectar al resto."""
    canonical = BASE_URL.rstrip("/") + ruta_publica(archivo)
    bloque_schema = f'\n<script type="application/ld+json">\n{schema}\n</script>' if schema else ""
    bloque_fuentes = f'\n<link href="{fuentes_extra}" rel="stylesheet">' if fuentes_extra else ""
    bloque_css = "".join(f'\n<link rel="stylesheet" href="{h}">' for h in css_extra)
    atr_body = f' class="{clase_body}"' if clase_body else ""
    # landing = (texto_boton, href) activa la cabecera mínima y el pie corto
    # landing = () -> sin barra de cabecera (el logo va dentro del héroe)
    if landing is not None:
        bloque_cabecera = cabecera_landing(*landing) if landing else ""
        bloque_pie = PIE_LANDING
    else:
        bloque_cabecera, bloque_pie = cabecera(activo), PIE
    return versionar_recursos(imagenes_webp(enlaces_absolutos(f"""<!DOCTYPE html>
<html lang="es-CO">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>{titulo}</title>
<meta name="description" content="{descripcion}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="{robots}">

<meta property="og:type" content="website">
<meta property="og:locale" content="es_CO">
<meta property="og:site_name" content="Marín Ríos Consultores">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{descripcion}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE_URL}assets/img/{og_img}">
<meta name="twitter:card" content="summary_large_image">

<script>document.documentElement.className += ' js';</script>
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" href="/favicon-192.png" sizes="192x192">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="theme-color" content="#0B0733">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700;800&family=Instrument+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/estilo.css">
<link rel="stylesheet" href="assets/css/modulos.css">{bloque_fuentes}{bloque_css}
<link rel="stylesheet" href="assets/css/movil.css">{bloque_schema}

{GTM_HEAD}
</head>
<body{atr_body}>
{GTM_BODY}

<a class="salto" href="#contenido">Saltar al contenido</a>

{bloque_cabecera}

<main id="contenido">
{cuerpo}
</main>

{bloque_pie}
</body>
</html>
""")))


# ================================================================
# Componentes
# ================================================================

def heroe(titulo, entrada, foto, alt, chip="", migas=None, cta1=None, cta2=None, riel=None):
    m = ""
    if migas:
        piezas = []
        for i, (txt, href) in enumerate(migas):
            piezas.append(f'<a href="{href}">{txt}</a>' if href else f"<span>{txt}</span>")
            if i < len(migas) - 1:
                piezas.append('<span>/</span>')
        m = f'<nav class="migas" aria-label="Ruta">{" ".join(piezas)}</nav>'

    c = f'<span class="chip"><span class="chip__punto"></span>{chip}</span>' if chip else ""

    acciones = ""
    if cta1 or cta2:
        b = []
        if cta1:
            b.append(f'<a class="btn btn--primario" href="{cta1[1]}">{cta1[0]}{ICO["flecha"]}</a>')
        if cta2:
            b.append(f'<a class="btn btn--fantasma" href="{cta2[1]}">{cta2[0]}</a>')
        acciones = f'<div class="hero__acciones">{"".join(b)}</div>'

    bloque_riel = ""
    if riel:
        datos = "".join(
            f'<div class="riel__dato"><span class="riel__cifra">{c1}</span>'
            f'<span class="riel__etiqueta">{c2}</span></div>' for c1, c2 in riel
        )
        bloque_riel = f'<div class="contenedor"><div class="riel">{datos}</div></div>'

    return f"""<section class="heroe">
  <div class="heroe__fondo">
    <img src="assets/img/{foto}" alt="{alt}" width="1600" height="900" fetchpriority="high">
  </div>
  <div class="contenedor heroe__inner">
    {m}
    {c}
    <h1>{titulo}</h1>
    <p class="heroe__entrada">{entrada}</p>
    {acciones}
  </div>
  {bloque_riel}
</section>"""


def encabezado(eyebrow, titulo, texto="", ancho="56rem", tam="var(--paso-5)"):
    p = f"<p>{texto}</p>" if texto else ""
    return f"""<div class="encabezado-seccion revelar" style="max-width:{ancho}">
      <p class="eyebrow">{eyebrow}</p>
      <h2 style="font-size:{tam}">{titulo}</h2>
      {p}
    </div>"""


def servicios_num(items):
    """items: [(num_etiqueta, titulo, texto, _, cta_texto, href)]
    El cuarto campo era el precio; el sitio ya no publica tarifas."""
    cartas = []
    for i, (num, tit, txt, _, cta, href) in enumerate(items, 1):
        cartas.append(f"""<article class="servicio-num servicio-num--{i}">
        <span class="servicio-num__num">{num}</span>
        <h3>{tit}</h3>
        <p>{txt}</p>
        <a class="servicio-num__cta" href="{href}">{cta}{ICO['flecha_fina']}</a>
      </article>""")
    return f'<div class="servicios-num revelar">{"".join(cartas)}</div>'


def fijo(ancla_html, filas):
    """filas: [(titulo, texto)] — se numeran porque son un inventario ordenado."""
    f = "".join(
        f"""<div class="fijo__fila">
        <span class="fijo__indice">{i:02d}</span>
        <div><h3>{t}</h3><p>{x}</p></div>
      </div>""" for i, (t, x) in enumerate(filas, 1)
    )
    return f"""<div class="contenedor fijo">
    <div class="fijo__ancla revelar">{ancla_html}</div>
    <div class="fijo__lista revelar">{f}</div>
  </div>"""


def carrusel(eyebrow, titulo, texto, tarjetas, oscuro=True, etiqueta="Elementos"):
    color = ' style="color:var(--cian-300)"' if oscuro else ""
    cartas = []
    for et, tit, txt in tarjetas:
        cartas.append(f"""<article class="tarjeta-servicio">
        <span class="fijo__indice"{color}>{et}</span>
        <h3 style="margin-top:var(--sp-3)">{tit}</h3>
        <p>{txt}</p>
      </article>""")
    return f"""<div class="contenedor carrusel">
    <div class="carrusel__cabecera revelar">
      <div style="max-width:44rem">
        <p class="eyebrow">{eyebrow}</p>
        <h2 style="font-size:var(--paso-4)">{titulo}</h2>
        <p style="margin-top:var(--sp-2)">{texto}</p>
      </div>
      <div class="carrusel__controles">
        <button class="carrusel__btn" data-dir="anterior" aria-label="Anterior">{ICO['atras']}</button>
        <button class="carrusel__btn" data-dir="siguiente" aria-label="Siguiente">{ICO['flecha_fina']}</button>
      </div>
    </div>
    <div class="carrusel__pista revelar" role="group" aria-label="{etiqueta}">{"".join(cartas)}</div>
    <div class="carrusel__progreso"><i></i></div>
  </div>"""


def acordeon(preguntas, prefijo="p"):
    """preguntas: [(pregunta, respuesta_html)]"""
    items = []
    for i, (q, a) in enumerate(preguntas, 1):
        pid = f"{prefijo}{i}"
        items.append(f"""<div class="acordeon__item">
          <button class="acordeon__btn" aria-expanded="false" aria-controls="{pid}" id="{pid}-btn">
            <span class="acordeon__idx">{i:02d}</span>
            <span class="acordeon__titulo">{q}</span>
            <span class="acordeon__signo" aria-hidden="true"></span>
          </button>
          <div class="acordeon__panel" id="{pid}" role="region" aria-labelledby="{pid}-btn" data-abierto="false"><div><div class="interior">
            {a}
          </div></div></div>
        </div>""")
    return f'<div class="acordeon revelar">{"".join(items)}</div>'


def tarjetas_item(items):
    """items: [(icono, titulo, texto)]"""
    t = "".join(f"""<article class="tarjeta-item revelar">
        <div class="tarjeta-item__icono">{ICO[ic]}</div>
        <h3>{tit}</h3>
        <p>{txt}</p>
      </article>""" for ic, tit, txt in items)
    return f'<div class="rejilla-3 rejilla-movil">{t}</div>'


def lista_check(items, oscuro=False):
    li = "".join(
        f'<li><span class="check">{ICO["check"]}</span> {x}</li>' for x in items
    )
    return f'<ul class="split__lista">{li}</ul>'


def ciudades_grid():
    datos = [
        ("medellin", "Medellín", "Antioquia", "Outsourcing contable para pymes y startups del Valle de Aburrá."),
        ("armenia", "Armenia", "Quindío", "Contabilidad y revisoría fiscal para empresas del Quindío."),
        ("pereira", "Pereira", "Risaralda", "Gestión contable y tributaria para negocios en Risaralda."),
        ("manizales", "Manizales", "Caldas", "Outsourcing contable para empresas caldenses en crecimiento."),
    ]
    c = "".join(f"""<a class="caso" href="outsourcing-contable-{slug}.html">
        <img src="assets/img/ciudad-{slug}.jpg" alt="{nombre}" width="900" height="1120" loading="lazy">
        <span class="caso__redondo">{ICO['diagonal']}</span>
        <div class="caso__cuerpo">
          <span class="caso__etiqueta">{depto}</span>
          <h3>{nombre}</h3>
          <p>{txt}</p>
        </div>
      </a>""" for slug, nombre, depto, txt in datos)
    return f'<div class="rejilla-4 rejilla-movil revelar">{c}</div>'


def directorio(ciudad_actual=None):
    ciudades = [("Medellín", "medellin"), ("Armenia", "armenia"),
                ("Pereira", "pereira"), ("Manizales", "manizales")]
    enlaces = []
    for nombre, slug in ciudades:
        if ciudad_actual == slug:
            enlaces.append(f'<span class="etiqueta-enlace etiqueta-enlace--inerte">{nombre}</span>')
        else:
            enlaces.append(f'<a class="etiqueta-enlace" href="outsourcing-contable-{slug}.html">{nombre}</a>')
    return f"""<div class="directorio revelar">
      <div>
        <h3>Industria</h3>
        <div class="directorio__lista">
          <span class="etiqueta-enlace etiqueta-enlace--inerte">Servicios profesionales</span>
          <span class="etiqueta-enlace etiqueta-enlace--inerte">Financiero</span>
          <span class="etiqueta-enlace etiqueta-enlace--inerte">Empresas de tecnología</span>
          <span class="etiqueta-enlace etiqueta-enlace--inerte">Retail</span>
        </div>
      </div>
      <div>
        <h3>Ciudad</h3>
        <div class="directorio__lista">{"".join(enlaces)}</div>
      </div>
    </div>"""


def cta_final(titulo, texto, boton="Agenda tu asesoría", mensaje="Hola, quiero agendar una asesoría contable para mi empresa"):
    return f"""<section class="seccion cta-final oscuro degradado centrado">
  <div class="contenedor">
    <p class="eyebrow" style="justify-content:center">Siguiente paso</p>
    <h2>{titulo}</h2>
    <p>{texto}</p>
    <div class="cta-final__acciones">
      <a class="btn btn--primario" href="{wa(mensaje)}">{boton}{ICO['flecha']}</a>
      <a class="btn btn--fantasma" href="precios-outsourcing-contable.html">Conoce nuestros planes</a>
    </div>
    <div class="cta-contacto">
      <a href="tel:{TEL_URI}">{ICO['tel']}{TEL}</a>
      <a href="mailto:{EMAIL}">{ICO['correo']}{EMAIL}</a>
      <a href="https://maps.google.com/?q=Cl.+49B+%2364b-54,+Laureles+-+Estadio,+Medellín" target="_blank" rel="noopener">{ICO['pin']}Cl. 49B #64b-54, Laureles</a>
    </div>
  </div>
</section>"""


def tarjeta_autor():
    """Bloque «Sobre el autor» que cierra cada artículo del blog."""
    return f"""<aside class="autor" id="sobre-el-autor">
      <img class="autor__foto" src="{AUTOR_FOTO}"
           alt="{AUTOR_NOMBRE}, contador público y director de Marín Ríos Consultores"
           width="320" height="320" loading="lazy">
      <div>
        <p class="autor__etiqueta">Sobre el autor</p>
        <p class="autor__nombre">{AUTOR_NOMBRE}</p>
        <p class="autor__cargo">{AUTOR_CARGO}</p>
        <p class="autor__bio">{AUTOR_BIO}</p>
        <a class="btn btn--contorno autor__enlace" href="{AUTOR_LINKEDIN}"
           target="_blank" rel="noopener">{ICO['linkedin']}Ver perfil en LinkedIn{ICO['diagonal']}</a>
      </div>
    </aside>"""


def nodo_autor():
    """Nodo `Person` del autor para los datos estructurados de los artículos.

    Va aparte del nodo de la empresa: Google necesita saber que detrás de los
    artículos hay una persona identificable, y el `sameAs` al LinkedIn es la
    prueba de que esa persona existe fuera del sitio.
    """
    return {
        "@type": "Person",
        "@id": AUTOR_ID,
        "name": AUTOR_NOMBRE,
        "jobTitle": "Contador público",
        "description": AUTOR_BIO,
        "image": BASE_URL + AUTOR_FOTO,
        "url": BASE_URL + "nosotros/",
        "sameAs": [AUTOR_LINKEDIN],
        "worksFor": {"@id": BASE_URL + "#empresa"},
    }


def recortar(texto, limite):
    """Acorta por palabra completa y cierra con puntos suspensivos.

    Recortar a lo bruto deja migas de pan como «…para no sufrir co», que es lo
    que se veía antes en los artículos de título largo.
    """
    if len(texto) <= limite:
        return texto
    corte = texto[:limite].rsplit(" ", 1)[0].rstrip(" ,;:.—-")
    return (corte or texto[:limite]) + "…"


def proposito(titulo, p1, p2, boton="Haz clic para conversar", mensaje="Hola, quiero conversar sobre outsourcing contable",
              flotante_a=("100%", "Cumplimiento DIAN"), flotante_b=("Día 10", "Cierre mensual entregado")):
    return f"""<section class="proposito">
  <div class="contenedor proposito__grid">
    <div class="proposito__texto">
      <p class="eyebrow" style="color:var(--cian-300)">Sobre nosotros</p>
      <h2>{titulo}</h2>
      <p>{p1}</p>
      <p>{p2}</p>
      <a class="btn btn--primario" style="margin-top:var(--sp-4)" href="{wa(mensaje)}">{boton}{ICO['flecha']}</a>
    </div>
    <div class="proposito__media">
      <div class="proposito__forma" aria-hidden="true"></div>
      <div class="flotante flotante--a">
        <span class="flotante__icono">{ICO['escudo']}</span>
        <span><span class="flotante__valor">{flotante_a[0]}</span><span class="flotante__nota">{flotante_a[1]}</span></span>
      </div>
      <div class="flotante flotante--b">
        <span class="barras" aria-hidden="true"><span></span><span></span><span></span><span></span><span></span></span>
        <span><span class="flotante__valor">{flotante_b[0]}</span><span class="flotante__nota">{flotante_b[1]}</span></span>
      </div>
      <img class="proposito__foto" src="assets/img/asesor.png" alt="Juan David Marín, contador público y director de Marín Ríos Consultores" width="647" height="900" loading="lazy">
    </div>
  </div>
</section>"""


# Clientes: logo recortado y sin fondo (originales-img/logo-cliente-*.png).
# Las empresas sin logo disponible se muestran como nombre tipográfico.
CLIENTES = [
    ("Etelvina SAS", "logo-cliente-etelvina.png", 128, 144),
    ("Axcel", "logo-cliente-axl.png", 126, 72),
    ("Rocketfy", "logo-cliente-rocketfy.png", 226, 62),
    ("Corporación María Inmaculada", "logo-cliente-maria-inmaculada.png", 114, 172),
    ("Labor Diésel", None, 0, 0),
    ("Logística y Abastecimiento", None, 0, 0),
]


def carrusel_clientes(variante=""):
    """Logos grandes, sin recuadro, en carrusel continuo.
    La lista va dos veces para que el desplazamiento no tenga corte; la
    segunda copia se oculta a lectores de pantalla."""
    def item(nombre, img, w, h, eco):
        oculto = ' aria-hidden="true"' if eco else ""
        if img:
            alt = "" if eco else nombre
            marca = f'<img src="assets/img/{img}" alt="{alt}" width="{w}" height="{h}" loading="lazy">'
        else:
            marca = f'<span class="clientes-logos__texto">{nombre}</span>'
        return f'<li class="clientes-logos__item"{oculto}>{marca}</li>'
    fila = "".join(item(*c, False) for c in CLIENTES)
    eco = "".join(item(*c, True) for c in CLIENTES)
    clase = f"clientes-logos clientes-logos--{variante}" if variante else "clientes-logos"
    return f"""<div class="{clase}">
      <ul class="clientes-logos__pista" aria-label="Empresas que confían en nosotros">{fila}{eco}</ul>
    </div>"""


def marcas():
    return f"""<section class="seccion--ajustada clientes">
  <div class="contenedor revelar">
    <div class="clientes__cabecera">
      <p class="eyebrow">Confían en nosotros</p>
      <h2 style="font-size:var(--paso-3)">Ellos han tercerizado sus procesos con nosotros</h2>
      <p style="color:var(--texto-suave);margin-top:.7rem">Más de 50 empresas se orientaron por sus objetivos más estratégicos.</p>
    </div>
  </div>
  {carrusel_clientes()}
</section>"""
