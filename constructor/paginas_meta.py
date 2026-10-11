# -*- coding: utf-8 -*-
"""
Landing de pauta en Meta: evaluación de revisoría fiscal 2027.

Estructura tomada de la landing de 30X (héroe con cifras, logos en carrusel,
video, bloques de dolor, oferta en tres partes, resumen con costo $0, carta
del director, preguntas y formulario), con la piel corporativa de la marca.

Va con `noindex`: es tráfico pagado y no debe competir en Google con
/revisoria-fiscal/. Usa cabecera mínima (sin menú) para no perder leads.

El formulario envía cada lead a la pestaña "Leads" del Google Sheet
"Leads_Consolidado Marin Rios" mediante un Apps Script (ver
integraciones/google-sheets-leads.gs) y además abre WhatsApp con el mensaje.
"""

from base import ICO, WA, acordeon, resenas_google, carrusel_clientes
from paginas import PAGINAS

NOINDEX = "noindex, nofollow"

# ----------------------------------------------------------------- ajustes
# URL del Apps Script publicado como aplicación web (termina en /exec).
# Mientras esté vacía, el formulario igual abre WhatsApp, pero NO guarda en el
# Sheet. Ver integraciones/COMO-CONECTAR-EL-SHEET.md
SHEETS_URL = ""

# ID del video de YouTube con Juan David (lo que va después de v=).
# Vacío = la sección de video no se publica.
VIDEO_YOUTUBE = ""
VIDEO_MINUTOS = 3

# Testimonios autorizados: (nombre, cargo, empresa, frase). Vacío = se
# muestran los logos de clientes en su lugar.
TESTIMONIOS = []

# Topes 2027: 3.000 y 5.000 SMMLV con el salario mínimo de 2026 ($1.750.905).
TOPE_INGRESOS = "$5.252 millones"   # 3.000 × 1.750.905 = 5.252.715.000
TOPE_ACTIVOS = "$8.754 millones"    # 5.000 × 1.750.905 = 8.754.525.000

# Por validar con Juan David antes de pautar.
DURACION_EVALUACION = "45 minutos"
DIAS_PROPUESTA = "3 días hábiles"

# Ley 222 de 1995, art. 86: multas hasta 200 SMMLV (200 × 1.750.905 = 350.181.000).
MULTA_SUPER = "$350 millones"

# Páginas de gracias: una URL por tipo de lead para medir la conversión en Meta.
GRACIAS_OK = "gracias-evaluacion-revisoria"
GRACIAS_PEQ = "gracias-evaluacion-guia"

GUIA_PEQUENAS = "contabilidad-basica-empresas.html"
ANCLA = "#agendar"
CTA_PRINCIPAL = "Quiero saber si mi empresa está obligada"

ICONO = {
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>',
    "alerta": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l10 18H2z"/><path d="M12 10v5M12 18h.01"/></svg>',
    "ingresos": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 20h18"/><path d="M6 16v-5M11 16V8M16 16v-8M21 16V5"/></svg>',
    "activos": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 10l9-6 9 6"/><path d="M5 10v8M9.5 10v8M14.5 10v8M19 10v8"/><path d="M3 20h18"/></svg>',
    "sociedad": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 21V5l8-3 8 3v16"/><path d="M9 21v-5h6v5M9 8h.01M15 8h.01M9 12h.01M15 12h.01"/></svg>',
    "reloj": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    "firma": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 17c3-1 4-6 6-6s1 5 3 5 3-3 5-3 2 2 4 2"/><path d="M3 21h18"/></svg>',
    "socios": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><circle cx="9" cy="8" r="3"/><circle cx="17" cy="9" r="2.5"/><path d="M3 20c0-3.5 2.7-6 6-6s6 2.5 6 6M15 20c0-2.5 1-4.5 4-4.5 1.5 0 2 .5 2 .5"/></svg>',
    "lupa": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.5-4.5"/></svg>',
    "documento": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 2h9l5 5v15H6z"/><path d="M14 2v6h6M9 13h8M9 17h6"/></svg>',
    "persona": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-8 8-8s8 3.6 8 8"/></svg>',
    "campana": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 8a6 6 0 0112 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10 21a2 2 0 004 0"/></svg>',
    "informe": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M7 15l3-3 3 2 4-5"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><path d="M12 21s7-5.5 7-11a7 7 0 10-14 0c0 5.5 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/></svg>',
}

CLIENTES = [
    ("Etelvina SAS", "cliente-etelvina.png"),
    ("AXL", "cliente-axl.png"),
    ("Rocketfy", "cliente-rocketfy.png"),
    ("María Inmaculada", "cliente-maria-inmaculada.png"),
    ("Labor Diésel", None),
    ("Logística y Abastecimiento", None),
]


def _boton(texto=CTA_PRINCIPAL, extra=""):
    return f'<a class="lp-btn {extra}" href="{ANCLA}">{texto}{ICO["flecha"]}</a>'


def _logo(nombre, img, oculto=False):
    a = ' aria-hidden="true"' if oculto else ""
    marca = (f'<img src="assets/img/{img}" alt="" width="40" height="40" loading="lazy">' if img
             else f'<span class="lp-logo__ini">{"".join(p[0] for p in nombre.split() if len(p) > 2)[:2].upper()}</span>')
    return f'<li class="lp-logo"{a}>{marca}<span>{nombre}</span></li>'


def _carrusel_logos():
    fila = "".join(_logo(n, i) for n, i in CLIENTES)
    eco = "".join(_logo(n, i, True) for n, i in CLIENTES)
    return f"""<div class="lp-marquesina">
      <ul class="lp-marquesina__pista">{fila}{eco}</ul>
    </div>"""


def _video():
    if not VIDEO_YOUTUBE:
        return ""
    # Fachada: se muestra la miniatura y solo se carga YouTube al hacer clic,
    # para que el video no frene la carga de la página.
    return f"""
<section class="lp-seccion">
  <div class="lp-contenedor lp-centro">
    <h2 class="lp-titulo">Lo que dicen quienes ya trabajan con nosotros</h2>
    <button class="lp-video revelar" type="button" data-video="{VIDEO_YOUTUBE}" aria-label="Reproducir video">
      <img src="https://i.ytimg.com/vi/{VIDEO_YOUTUBE}/hqdefault.jpg" alt="" width="480" height="360" loading="lazy">
      <span class="lp-video__play" aria-hidden="true"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg></span>
    </button>
    <p class="lp-texto">{VIDEO_MINUTOS} minutos con Juan David Marín, contador público y director de la firma, sobre lo que cambia para tu empresa en 2027 y lo que nadie te pregunta antes de firmar con un revisor.</p>
  </div>
</section>"""


def _testimonios():
    if TESTIMONIOS:
        tarjetas = "".join(f"""<figure class="lp-testimonio">
        <blockquote>“{frase}”</blockquote>
        <figcaption><strong>{nombre}</strong><span>{cargo} · {empresa}</span></figcaption>
      </figure>""" for nombre, cargo, empresa, frase in TESTIMONIOS)
        contenido = f'<div class="lp-rejilla-3 revelar">{tarjetas}</div>'
    else:
        # Reseñas reales de Google (las mismas del sitio)
        return resenas_google("No confíes solo en lo que decimos",
                              "Opiniones de Marín Ríos en Google", variante="oscuro")
    return f"""
<section class="lp-seccion">
  <div class="lp-contenedor lp-centro">
    <h2 class="lp-titulo">No confíes solo en lo que decimos</h2>
    <p class="lp-texto">Estas son empresas que ya trabajan con nosotros.{' Escúchalas a ellas.' if TESTIMONIOS else ''}</p>
    {contenido}
  </div>
</section>"""


def _campo_lista(clave, etiqueta, opciones):
    ops = "".join(f'<option value="{o}">{o}</option>' for o in opciones)
    return f"""<div class="lp-campo">
          <label for="lp-{clave}">{etiqueta}</label>
          <select id="lp-{clave}" name="{clave}" required>
            <option value="" selected disabled>Elige una opción</option>
            {ops}
          </select>
        </div>"""


INGRESOS = ["Menos de $1.000 millones", "$1.000 a $5.000 millones",
            "$5.000 a $20.000 millones", "Más de $20.000 millones"]

PREGUNTAS = [
    ("¿Cuánto dura la evaluación?",
     f"{DURACION_EVALUACION[0].upper() + DURACION_EVALUACION[1:]}, presencial o virtual. La propuesta escrita llega en {DIAS_PROPUESTA}."),
    ("¿Hay algún requisito para agendarla?",
     f"Está pensada para empresas que en 2026 facturaron más de {TOPE_INGRESOS}, tienen activos desde {TOPE_ACTIVOS}, o son sociedades anónimas o sucursales extranjeras. Si estás cerca del límite y no sabes si aplica, también te sirve."),
    ("¿Cómo la agendo?",
     "Llenas el formulario de esta página, que toma menos de un minuto, y te escribimos por WhatsApp en menos de 24 horas hábiles para fijar la fecha."),
    ("¿A quién está dirigida?",
     "A gerentes, socios y directores financieros de empresas de Antioquia y el Eje Cafetero que deben nombrar revisor fiscal en 2027 o quieren cambiar el que tienen."),
    ("¿Dónde se hace?",
     "En nuestra oficina de Laureles en Medellín, en tu empresa si estás en Pereira, Armenia o Manizales, o por videollamada."),
    ("¿Cuánto cuesta?",
     "La evaluación no tiene costo. El valor de la revisoría depende del tamaño de tu empresa, del sector y de las horas que exija; por eso te lo entregamos por escrito después de revisarla."),
    ("¿Qué incluye la evaluación?",
     "La confirmación de si estás obligado en 2027, un mapa de los riesgos que hoy tienes frente a la DIAN y la Supersociedades, y una propuesta con alcance, horas y honorarios lista para tu asamblea."),
    ("Ya tengo revisor fiscal. ¿Puedo cambiarlo?",
     "Sí. El revisor lo nombra la asamblea, así que la reunión ordinaria es el momento natural para cambiarlo. Te ayudamos a preparar el empalme para que no quede ningún informe pendiente."),
    ("¿Qué pasa después de la evaluación?",
     "Te quedas con el resultado y la propuesta, sin compromiso. Si decides trabajar con nosotros, firmamos antes de la asamblea y arrancamos en cuanto nos nombren."),
    ("¿Pueden llevar mi contabilidad y ser mis revisores fiscales?",
     "No. La revisoría exige independencia, así que no prestamos ambos servicios a la misma empresa."),
]

cuerpo = f"""
<!-- ===================== 1. HÉROE =====================
     Dos columnas en escritorio (texto · video); apilado en celular. -->
<section class="lp-heroe lp-heroe--cols">
  <div class="lp-contenedor">
    <img class="lp-heroe__logo" src="assets/img/logo-marin-rios.png" alt="Marín Ríos Consultores" width="90" height="80">
    <div class="lp-heroe__rejilla">
      <div class="lp-heroe__texto">
        <p class="lp-etiqueta">Empresas que facturaron más de {TOPE_INGRESOS} en 2026</p>
        <h1>Sin revisor fiscal en 2027, <em>la DIAN da tus declaraciones por no presentadas</em></h1>
        <p class="lp-heroe__sub">Pagas sanción por extemporaneidad, intereses y una multa de la Supersociedades que llega a {MULTA_SUPER}. Y ante tus socios, el que responde eres tú.</p>
        <p class="lp-heroe__desc">Agenda la evaluación gratuita: en {DURACION_EVALUACION} un contador público te dice si estás obligado, qué riesgos tienes hoy frente a la DIAN y te entrega una propuesta escrita para tu asamblea de marzo.</p>
        {_boton()}
        <p class="lp-heroe__prueba">Con el equipo que ya acompaña a <strong>más de 50 empresas</strong>.</p>
      </div>
      <button class="lp-vvideo" type="button" data-mp4="/assets/video/evaluacion-revisoria.mp4" aria-label="Reproducir video de 44 segundos">
        <img src="assets/img/video-evaluacion.jpg" alt="Video: cómo trabajamos la revisoría fiscal en Marín Ríos Consultores" width="540" height="960" fetchpriority="high">
        <span class="lp-vvideo__play" aria-hidden="true"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg></span>
        <span class="lp-vvideo__dur" aria-hidden="true">0:44</span>
      </button>
    </div>
  </div>
</section>

<!-- ===================== 2. LOGOS ===================== -->
<section class="lp-logos">
  <p class="lp-logos__titulo">Empresas de Antioquia y el Eje Cafetero que ya confían en nosotros</p>
  {carrusel_clientes("oscuro")}
</section>

<!-- ===================== 3. LO QUE DICEN (video) ===================== -->
{_video()}

<!-- ===================== 4. QUIÉNES ===================== -->
<section class="lp-seccion">
  <div class="lp-contenedor lp-centro">
    <h2 class="lp-titulo">Un revisor que solo firma te deja solo cuando llega la DIAN</h2>
    <p class="lp-texto">Aparece en marzo, firma y desaparece. El requerimiento llega en agosto y nadie te avisó. Los que revisan tu empresa con nosotros dan la cara todo el año.</p>
    <div class="lp-rejilla-2 revelar">
      <article class="lp-tarjeta lp-tarjeta--fila"><span class="lp-ico">{ICONO['persona']}</span><div><h3>Un responsable con nombre propio</h3><p>Se acabó perseguir a un revisor que no contesta. Hablas siempre con el mismo contador, que conoce tu empresa.</p></div></article>
      <article class="lp-tarjeta lp-tarjeta--fila"><span class="lp-ico">{ICONO['campana']}</span><div><h3>Alertas antes de la sanción</h3><p>Te enteras del riesgo por nosotros, no por un requerimiento de la DIAN cuando ya no hay nada que corregir.</p></div></article>
      <article class="lp-tarjeta lp-tarjeta--fila"><span class="lp-ico">{ICONO['informe']}</span><div><h3>Informes que tus socios entienden</h3><p>Nada de documentos genéricos que nadie lee. Hallazgos claros para la gerencia, la junta y el banco.</p></div></article>
      <article class="lp-tarjeta lp-tarjeta--fila"><span class="lp-ico">{ICONO['pin']}</span><div><h3>Presencia en tu ciudad</h3><p>No una visita al año: revisión durante todo el ejercicio en Medellín, Pereira, Armenia y Manizales.</p></div></article>
    </div>
  </div>
</section>

<!-- ===================== 5. EL SISTEMA DE 3 PARTES ===================== -->
<section class="lp-seccion">
  <div class="lp-contenedor lp-centro">
    <h2 class="lp-titulo">El sistema de 3 partes para llevarte de la duda a la decisión</h2>
    <p class="lp-texto">Hoy no sabes si estás obligado, qué vería primero la DIAN ni qué decirles a tus socios en marzo. Cada parte resuelve una de esas tres preguntas. Sin teoría y sin discurso comercial.</p>
    <ol class="lp-partes revelar">
      <li>
        <span class="lp-ico lp-ico--grande">{ICONO['lupa']}</span>
        <div><h3>Parte 1: ¿Estoy obligado?</h3><p class="lp-partes__bajada">Deja de suponer. Sal de la duda en la primera conversación.</p><p>Revisamos tus ingresos, tus activos y tu tipo de sociedad frente a los topes de 2027.</p></div>
      </li>
      <li>
        <span class="lp-ico lp-ico--grande">{ICONO['alerta']}</span>
        <div><h3>Parte 2: ¿Qué riesgos tengo?</h3><p class="lp-partes__bajada">Encuentra el problema antes de que lo encuentre la DIAN.</p><p>Leemos tus estados financieros y te mostramos las inconsistencias que la DIAN detecta al cruzar factura, nómina y exógena.</p></div>
      </li>
      <li>
        <span class="lp-ico lp-ico--grande">{ICONO['documento']}</span>
        <div><h3>Parte 3: ¿Qué llevo a la asamblea?</h3><p class="lp-partes__bajada">No improvises frente a tus socios. Llega con la decisión tomada.</p><p>Propuesta escrita con alcance, horas y honorarios, lista para presentar a tus socios.</p></div>
      </li>
    </ol>
    {_boton("Agendar mi evaluación gratuita")}
  </div>
</section>

<!-- ===================== 6. LO QUE OBTIENES ===================== -->
<section class="lp-seccion">
  <div class="lp-contenedor lp-centro">
    <h2 class="lp-titulo">Esto es exactamente lo que obtienes cuando agendas la evaluación</h2>
    <div class="lp-oferta revelar">
      <p class="lp-oferta__nombre">Evaluación de revisoría fiscal 2027</p>
      <p class="lp-oferta__precio">Inversión de <strong>$0</strong></p>
      <p>{DURACION_EVALUACION[0].upper() + DURACION_EVALUACION[1:]} con un contador público de la firma, sobre las cifras reales de tu empresa.</p>
      <p>No es una llamada de ventas: es la misma revisión con la que arrancamos cualquier revisoría, aplicada a tu caso.</p>
      <ul class="lp-oferta__lista">
        <li>{ICONO['check']}<span>Confirmación por escrito de si estás obligado en 2027</span></li>
        <li>{ICONO['check']}<span>Mapa de riesgos frente a la DIAN y la Supersociedades</span></li>
        <li>{ICONO['check']}<span>Propuesta con alcance, horas y honorarios, en {DIAS_PROPUESTA}</span></li>
      </ul>
    </div>
    {_boton("Agendar mi evaluación gratuita")}
  </div>
</section>

<!-- ===================== 7. ¿POR QUÉ HAGO ESTO? ===================== -->
<section class="lp-seccion">
  <div class="lp-contenedor lp-centro lp-angosto">
    <h2 class="lp-titulo">¿Por qué hago esto?</h2>
    <div class="lp-heroe__media lp-heroe__media--retrato revelar">
      <img src="assets/img/asesor.png" alt="Juan David Marín, contador público y director de Marín Ríos Consultores" width="647" height="900" loading="lazy">
    </div>
    <div class="lp-carta__texto">
      <p>Soy Juan David Marín, contador público y director de Marín Ríos Consultores.</p>
      <p>Cada marzo veo lo mismo: empresas que llegan a la asamblea sin saber qué revisor necesitan. Eligen por precio o por una recomendación de última hora.</p>
      <p>Meses después llega el requerimiento de la DIAN, el revisor no contesta y el gerente termina dando explicaciones a sus socios por una decisión que tomó en diez minutos.</p>
      <p>Pero pasa algo: cuando un gerente ve cómo leemos sus números antes de firmar nada, casi siempre se queda. Y nos recomienda a sus socios y a otras empresas.</p>
      <p>Mi incentivo es simple: mientras más claro salgas de la evaluación, más probable es que trabajemos juntos.</p>
      <p class="lp-carta__firma"><strong>Juan David Marín</strong> · Director, Marín Ríos Consultores</p>
    </div>
    <div class="lp-datos">
      <div><strong>+50</strong><span>Empresas acompañadas</span></div>
      <div><strong>4</strong><span>Ciudades con atención presencial</span></div>
    </div>
    {_boton()}
  </div>
</section>

<!-- ===================== 8. EN PERSPECTIVA ===================== -->
<section class="lp-seccion">
  <div class="lp-contenedor lp-centro lp-angosto">
    <h2 class="lp-titulo">Solo para ponerlo en perspectiva</h2>
    <p class="lp-texto">Hoy la DIAN cruza tu facturación electrónica, tu nómina electrónica y la exógena en segundos. Una declaración sin la firma del revisor fiscal se tiene por no presentada: sanción por extemporaneidad más intereses, mes tras mes. La Supersociedades puede sumar multas de hasta <strong class="lp-acento">{MULTA_SUPER}</strong>. Los bancos no reciben estados financieros sin dictamen. Y un revisor elegido a la carrera te cuesta un año entero de informes que no sirven.</p>
    <p class="lp-perspectiva">Tú lo evitas en una reunión de {DURACION_EVALUACION}, sin costo.</p>
  </div>
</section>

<!-- ===================== 9. RESUMEN RÁPIDO ===================== -->
<section class="lp-seccion">
  <div class="lp-contenedor lp-centro">
    <h2 class="lp-titulo">Resumen rápido de todo lo que obtienes con la evaluación</h2>
    <div class="lp-resumen revelar">
      <ul class="lp-valor">
        <li><span>Confirmación de obligación 2027</span><strong>Incluido</strong></li>
        <li><span>Mapa de riesgos DIAN y Supersociedades</span><strong>Incluido</strong></li>
        <li><span>Propuesta escrita para la asamblea</span><strong>Incluido</strong></li>
      </ul>
      <a class="lp-resumen__hoy" href="{ANCLA}">Total: $0</a>
    </div>
    {_boton("Agendar mi evaluación gratuita")}
  </div>
</section>

<!-- ===================== 10. TESTIMONIOS ===================== -->
{_testimonios()}

<!-- ===================== 11. WHATSAPP ===================== -->
<section class="lp-seccion lp-seccion--corta">
  <div class="lp-contenedor">
    <div class="lp-wa revelar">
      <h2 class="lp-titulo">¿Aún tienes preguntas?</h2>
      <p class="lp-texto">Estamos listos para ayudarte por WhatsApp. Te responde alguien del equipo, no un robot.</p>
      <a class="lp-btn" href="https://wa.me/{WA}?text=Hola%2C%20vengo%20de%20la%20p%C3%A1gina%20de%20revisor%C3%ADa%20fiscal%202027%20y%20tengo%20una%20pregunta" target="_blank" rel="noopener">{ICO['wa']}Escribir al +57 314 884 3835</a>
    </div>
  </div>
</section>

<!-- ===================== 12. PREGUNTAS ===================== -->
<section class="lp-seccion">
  <div class="lp-contenedor lp-centro">
    <h2 class="lp-titulo">Preguntas frecuentes</h2>
    <div class="lp-faq">
      {acordeon([(q, f"<p>{a}</p>") for q, a in PREGUNTAS], prefijo="rf")}
    </div>
  </div>
</section>

<!-- ===================== 13. FORMULARIO ===================== -->
<section class="lp-seccion" id="agendar">
  <div class="lp-contenedor lp-centro">
    <div class="lp-form-caja">
      <form class="lp-form" id="lp-form" novalidate
            data-sheets="{SHEETS_URL}" data-wa="{WA}"
            data-gracias-ok="/{GRACIAS_OK}/" data-gracias-peq="/{GRACIAS_PEQ}/">
        <h2 class="lp-titulo">Agenda tu evaluación antes de que la asamblea decida a la carrera</h2>
        <p class="lp-texto">Toma menos de un minuto. Te escribimos por WhatsApp en menos de 24 horas hábiles.</p>
        <div class="lp-form__campos">
          <div class="lp-campo">
            <label for="lp-nombre">Nombre</label>
            <input id="lp-nombre" name="nombre" type="text" autocomplete="name" required maxlength="80">
          </div>
          <div class="lp-campo">
            <label for="lp-empresa">Empresa</label>
            <input id="lp-empresa" name="empresa" type="text" autocomplete="organization" required maxlength="120">
          </div>
          {_campo_lista("cargo", "Cargo", ["Gerente general o representante legal", "Socio o accionista", "Gerente financiero o administrativo", "Contador", "Otro"])}
          {_campo_lista("ciudad", "Ciudad", ["Medellín y Valle de Aburrá", "Pereira", "Armenia", "Manizales", "Otra"])}
          {_campo_lista("ingresos", "Ingresos anuales aproximados", INGRESOS)}
          {_campo_lista("revisor", "¿Tienen revisor fiscal hoy?", ["Sí, persona natural", "Sí, una firma", "No"])}
          <div class="lp-campo lp-campo--ancho">
            <label for="lp-whatsapp">WhatsApp</label>
            <input id="lp-whatsapp" name="whatsapp" type="tel" inputmode="tel" autocomplete="tel" required
                   pattern="[0-9 +()-]{{7,20}}" placeholder="300 123 4567">
          </div>
          <!-- Trampa para bots: los humanos no ven este campo -->
          <div class="lp-trampa" aria-hidden="true">
            <label for="lp-web">No llenar</label>
            <input id="lp-web" name="web" type="text" tabindex="-1" autocomplete="off">
          </div>
        </div>
        <button class="lp-btn lp-btn--bloque" type="submit">Agendar mi evaluación{ICO['flecha']}</button>
        <p class="lp-form__error" id="lp-form-error" role="alert" hidden>Revisa los campos marcados antes de continuar.</p>
        <p class="lp-form__legal">Tus datos solo se usan para contactarte sobre esta evaluación. <a href="politica-de-privacidad.html" target="_blank" rel="noopener">Política de privacidad</a>.</p>
      </form>
    </div>
  </div>
</section>

<script src="assets/js/lp-revisoria.js" defer></script>
"""

PAGINAS.append(dict(
    archivo="evaluacion-revisoria-fiscal.html",
    titulo="Evaluación de revisoría fiscal 2027 | Marín Ríos",
    descripcion="¿Tu empresa debe nombrar revisor fiscal en 2027? Agenda una evaluación gratuita y llega a la asamblea de marzo con la decisión tomada.",
    activo="",
    og_img="oficina-atardecer.jpg",
    robots=NOINDEX,
    schema="",
    cuerpo=cuerpo,
    clase_body="lp",
    css_extra=("assets/css/lp-revisoria.css",),
    landing=(),   # sin barra de cabecera: el logo va dentro del héroe
))


# ================================================================
# PÁGINAS DE GRACIAS (destino del formulario; se miden por URL en Meta)
# ================================================================
def _pagina_gracias(tipo, titulo, texto, acciones):
    return f"""
<section class="lp-heroe lp-gracias-pag" data-gracias="{tipo}">
  <div class="lp-contenedor lp-centro lp-angosto">
    <img class="lp-heroe__logo" src="assets/img/logo-marin-rios.png" alt="Marín Ríos Consultores" width="90" height="80">
    <span class="lp-gracias__ico">{ICONO['check']}</span>
    <h1>{titulo}</h1>
    <p class="lp-heroe__sub">{texto}</p>
    <div class="lp-acciones">{acciones}</div>
  </div>
</section>

<script src="assets/js/lp-revisoria.js" defer></script>
"""


_WA_GENERICO = f"https://wa.me/{WA}?text=Hola%2C%20acabo%20de%20llenar%20el%20formulario%20de%20la%20evaluaci%C3%B3n%20de%20revisor%C3%ADa%20fiscal%202027"

PAGINAS.append(dict(
    archivo=f"{GRACIAS_OK}.html",
    titulo="Recibimos tus datos | Evaluación de revisoría fiscal 2027",
    descripcion="Recibimos tus datos. Te escribimos por WhatsApp para agendar tu evaluación de revisoría fiscal.",
    activo="", og_img="oficina-atardecer.jpg", robots=NOINDEX, schema="",
    cuerpo=_pagina_gracias(
        "calificado",
        "Listo, <em>ya tenemos tus datos</em>",
        "En menos de 24 horas hábiles te escribimos por WhatsApp para agendar tu evaluación. Si quieres adelantarte, escríbenos ahora: el mensaje ya va con los datos de tu empresa.",
        f'<a class="lp-btn" data-wa-lead href="{_WA_GENERICO}" target="_blank" rel="noopener">{ICO["wa"]}Escribir por WhatsApp ahora</a>'),
    clase_body="lp", css_extra=("assets/css/lp-revisoria.css",), landing=(),
))

PAGINAS.append(dict(
    archivo=f"{GRACIAS_PEQ}.html",
    titulo="Gracias por escribirnos | Marín Ríos Consultores",
    descripcion="Gracias por escribirnos. Te dejamos una guía para mantener tu contabilidad en orden.",
    activo="", og_img="oficina-atardecer.jpg", robots=NOINDEX, schema="",
    cuerpo=_pagina_gracias(
        "no-calificado",
        "Gracias por escribirnos",
        "Por el tamaño de tu empresa, hoy no estás obligada a tener revisor fiscal. Te dejamos una guía para mantener tu contabilidad en orden y cumplir con la DIAN. Si quieres que revisemos tu caso, también podemos hablar.",
        f'<a class="lp-btn" href="{GUIA_PEQUENAS}">Ver la guía{ICO["flecha"]}</a>'
        f'<a class="lp-btn lp-btn--contorno" data-wa-lead href="{_WA_GENERICO}" target="_blank" rel="noopener">Hablar por WhatsApp</a>'),
    clase_body="lp", css_extra=("assets/css/lp-revisoria.css",), landing=(),
))
