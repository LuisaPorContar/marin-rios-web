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

from base import ICO, WA, acordeon
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
    <h2 class="lp-titulo">Antes de elegir revisor, mira esto</h2>
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
        # Sin testimonios autorizados: los clientes hablan por su logo.
        contenido = '<ul class="lp-clientes revelar">' + "".join(_logo(n, i) for n, i in CLIENTES) + "</ul>"
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
    ("¿A quién está dirigida la evaluación?",
     "A gerentes, socios y directores financieros de empresas que facturan más de $1.000 millones al año en Antioquia y el Eje Cafetero, que deben nombrar revisor fiscal o quieren cambiar el que tienen."),
    ("Ya tengo revisor fiscal. ¿Puedo cambiarlo?",
     "Sí. El revisor lo nombra la asamblea, así que la reunión ordinaria es el momento natural para cambiarlo. Te ayudamos a preparar la transición para que no quede ningún informe pendiente."),
    ("¿Una firma mediana tiene el respaldo para hacer revisoría?",
     "La revisoría la firma un contador público inscrito ante la Junta Central de Contadores, con un equipo que trabaja con metodología basada en riesgos. La diferencia con una firma grande es que aquí hablas con el responsable de tu revisoría, no con un profesional distinto cada año."),
    ("¿Pueden llevar mi contabilidad y ser mis revisores fiscales?",
     "No. La revisoría exige independencia, así que no prestamos ambos servicios a la misma empresa."),
    ("¿Cuánto cuesta la revisoría fiscal?",
     "Depende del tamaño de tu empresa, del sector y de las horas que exija. Por eso hacemos la evaluación primero y te entregamos el valor exacto por escrito."),
    ("¿Cuánto dura la evaluación?",
     f"{DURACION_EVALUACION[0].upper() + DURACION_EVALUACION[1:]}, presencial o virtual. La propuesta escrita llega en {DIAS_PROPUESTA}."),
    ("¿Dónde se hace?",
     "En nuestra oficina de Laureles en Medellín, en tu empresa si estás en Pereira, Armenia o Manizales, o por videollamada."),
    ("¿Qué pasa después de la evaluación?",
     "Te quedas con el resultado y la propuesta. Si decides trabajar con nosotros, firmamos antes de la asamblea y arrancamos en cuanto te nombren."),
]

cuerpo = f"""
<!-- ===================== 1. HÉROE ===================== -->
<section class="lp-heroe">
  <div class="lp-contenedor lp-centro">
    <img class="lp-heroe__logo" src="assets/img/logo-marin-rios.png" alt="Marín Ríos Consultores" width="90" height="80">
    <p class="lp-etiqueta">Evaluación de revisoría fiscal 2027</p>
    <h1>¿Tu empresa facturó más de {TOPE_INGRESOS} en 2026? En marzo tu asamblea tiene que nombrar revisor fiscal.</h1>
    <p class="lp-heroe__sub">Si llegas a la asamblea sin propuestas, eliges a la carrera, con los socios preguntando y el riesgo de contratar a alguien que solo firma. <span class="lp-acento">Agenda una evaluación gratuita y llega a marzo con la decisión tomada.</span></p>
    <div class="lp-heroe__media">
      <img src="assets/img/equipo-ancho.jpg" alt="Equipo de Marín Ríos Consultores en su oficina de Medellín" width="1600" height="900" fetchpriority="high">
    </div>
    {_boton()}
    <ul class="lp-cifras">
      <li><strong>+50</strong><span>empresas acompañadas</span></li>
      <li><strong>4</strong><span>ciudades con atención presencial</span></li>
      <li><strong>100 %</strong><span>del calendario DIAN cumplido</span></li>
    </ul>
  </div>
</section>

<!-- ===================== 2. LOGOS ===================== -->
<section class="lp-logos">
  <p class="lp-logos__titulo">Empresas que ya confían en nosotros</p>
  {_carrusel_logos()}
</section>

<!-- ===================== 3. VIDEO ===================== -->
{_video()}

<!-- ===================== 4. ¿ESTÁS OBLIGADO? ===================== -->
<section class="lp-seccion">
  <div class="lp-contenedor lp-centro">
    <h2 class="lp-titulo">Si cumples una de estas tres, en 2027 necesitas revisor fiscal</h2>
    <div class="lp-rejilla-3 revelar">
      <article class="lp-tarjeta">
        <span class="lp-ico">{ICONO['ingresos']}</span>
        <p>Ingresos brutos de 2026 iguales o superiores a <strong class="lp-acento">{TOPE_INGRESOS}</strong>.</p>
      </article>
      <article class="lp-tarjeta">
        <span class="lp-ico">{ICONO['activos']}</span>
        <p>Activos brutos iguales o superiores a <strong class="lp-acento">{TOPE_ACTIVOS}</strong>.</p>
      </article>
      <article class="lp-tarjeta">
        <span class="lp-ico">{ICONO['sociedad']}</span>
        <p>Sociedad anónima, sucursal extranjera o empresa con una norma especial que lo exija.</p>
      </article>
    </div>
    <p class="lp-texto lp-texto--cierre">¿Estás cerca del límite y no sabes si aplica? <strong>Eso es lo primero que resolvemos en la evaluación.</strong></p>
    {_boton()}
  </div>
</section>

<!-- ===================== 5. AGITACIÓN ===================== -->
<section class="lp-seccion">
  <div class="lp-contenedor lp-centro">
    <h2 class="lp-titulo">Lo que pasa cuando llegas a marzo sin revisor</h2>
    <div class="lp-fotos revelar">
      <article class="lp-foto">
        <img src="assets/img/oficina-atardecer.jpg" alt="" width="1920" height="707" loading="lazy">
        <div class="lp-foto__cuerpo"><span class="lp-foto__eti">01</span><h3>Eliges con prisa</h3><p>Dos semanas antes de la asamblea aceptas la primera propuesta que llega, sin comparar alcance ni horas.</p></div>
      </article>
      <article class="lp-foto">
        <img src="assets/img/detalle-documentos.jpg" alt="" width="1100" height="640" loading="lazy">
        <div class="lp-foto__cuerpo"><span class="lp-foto__eti">02</span><h3>Contratas a quien solo firma</h3><p>Aparece una vez al año, firma los estados financieros y nunca te avisa de un riesgo antes de que lo encuentre la DIAN.</p></div>
      </article>
      <article class="lp-foto">
        <img src="assets/img/domino-riesgo.jpg" alt="" width="1671" height="941" loading="lazy">
        <div class="lp-foto__cuerpo"><span class="lp-foto__eti">03</span><h3>Quedas mal con tus socios</h3><p>Te preguntan por qué no se previó y por qué los informes no sirven para decidir. La respuesta te toca darla a ti.</p></div>
      </article>
    </div>
    {_boton()}
  </div>
</section>

<!-- ===================== 6. LA EVALUACIÓN ===================== -->
<section class="lp-seccion">
  <div class="lp-contenedor lp-centro">
    <h2 class="lp-titulo">La evaluación que te lleva de la duda a la decisión</h2>
    <p class="lp-texto">Cada parte resuelve una pregunta concreta. Al final tienes una respuesta, un mapa de riesgos y una propuesta por escrito.</p>
    <ol class="lp-partes revelar">
      <li>
        <span class="lp-ico lp-ico--grande">{ICONO['lupa']}</span>
        <div><h3>Parte 1 · ¿Estoy obligado?</h3><p class="lp-partes__bajada">Sal de la duda en la primera conversación.</p><p>Revisamos tus ingresos, tus activos y tu tipo de sociedad, y te decimos si en 2027 necesitas revisor fiscal.</p></div>
      </li>
      <li>
        <span class="lp-ico lp-ico--grande">{ICONO['alerta']}</span>
        <div><h3>Parte 2 · ¿Qué riesgos tengo?</h3><p class="lp-partes__bajada">Encuentra lo que la DIAN vería primero.</p><p>Leemos tus estados financieros de 2025 y lo que va de 2026, y te mostramos los puntos que hoy te exponen ante la DIAN y la Supersociedades.</p></div>
      </li>
      <li>
        <span class="lp-ico lp-ico--grande">{ICONO['documento']}</span>
        <div><h3>Parte 3 · ¿Qué propongo en la asamblea?</h3><p class="lp-partes__bajada">Llega a marzo con la decisión tomada.</p><p>Recibes una propuesta escrita con alcance, horas y honorarios, lista para presentar a tus socios.</p></div>
      </li>
    </ol>
    {_boton("Agendar mi evaluación gratuita")}
  </div>
</section>

<!-- ===================== 7. RESUMEN ===================== -->
<section class="lp-seccion">
  <div class="lp-contenedor lp-centro">
    <h2 class="lp-titulo">Esto es exactamente lo que recibes en la evaluación</h2>
    <div class="lp-resumen revelar">
      <div class="lp-resumen__cab">
        <img src="assets/img/logo-marin-rios.png" alt="" width="90" height="80">
        <span>Evaluación de<br>revisoría fiscal 2027</span>
      </div>
      <ul class="lp-resumen__lista">
        <li>{ICONO['check']}<div><strong>Confirmación de si estás obligado en 2027</strong><span>Saber qué tienes que presentar en la asamblea</span></div></li>
        <li>{ICONO['check']}<div><strong>Revisión de riesgos frente a la DIAN y la Supersociedades</strong><span>Corregir antes de que alguien más lo encuentre</span></div></li>
        <li>{ICONO['check']}<div><strong>Plan de alcance y horas de revisoría para tu empresa</strong><span>Comparar propuestas con el mismo criterio</span></div></li>
        <li>{ICONO['check']}<div><strong>Propuesta escrita lista para la asamblea</strong><span>Presentarla a tus socios sin trabajo extra</span></div></li>
      </ul>
      <p class="lp-resumen__total">Costo de la evaluación</p>
      <a class="lp-resumen__hoy" href="{ANCLA}">HOY: $0</a>
    </div>
    {_boton("Agendar mi evaluación gratuita")}
  </div>
</section>

<!-- ===================== 8. CARTA ===================== -->
<section class="lp-seccion">
  <div class="lp-contenedor lp-centro lp-angosto">
    <h2 class="lp-titulo">¿Por qué la evaluación es gratis?</h2>
    <div class="lp-carta__foto revelar">
      <img src="assets/img/asesor.png" alt="Juan David Marín, contador público y director de Marín Ríos Consultores" width="647" height="900" loading="lazy">
    </div>
    <div class="lp-carta__texto">
      <p>Soy Juan David Marín, contador público y director de Marín Ríos Consultores.</p>
      <p>En mis años de trabajo he visto a decenas de empresas llegar a la asamblea sin saber qué revisor necesitan. Eligen por precio o por recomendación de última hora, y al año siguiente están buscando otra vez.</p>
      <p>Prefiero que conozcas cómo trabajamos antes de firmar cualquier cosa. En la evaluación ves cómo leemos tus números, qué preguntas hacemos y qué tan claro te explicamos lo que encontramos.</p>
      <p>Si después decides trabajar con otra firma, te llevas igual un mapa de riesgos que te sirve. Si decides trabajar con nosotros, ya empezamos sabiendo dónde está cada cosa.</p>
      <p class="lp-carta__firma"><strong>Juan David Marín</strong> · Director, Marín Ríos Consultores</p>
    </div>
    <div class="lp-datos">
      <div><strong>+50</strong><span>Empresas acompañadas</span></div>
      <div><strong>100 %</strong><span>Calendario DIAN cumplido</span></div>
    </div>
    {_boton()}
  </div>
</section>

<!-- ===================== 9. QUIÉN RESPONDE ===================== -->
<section class="lp-seccion">
  <div class="lp-contenedor lp-centro">
    <h2 class="lp-titulo">Tu revisoría tiene un responsable con nombre propio</h2>
    <div class="lp-rejilla-2 revelar">
      <article class="lp-tarjeta lp-tarjeta--fila"><span class="lp-ico">{ICONO['persona']}</span><div><h3>Un socio que conoces</h3><p>Hablas siempre con la misma persona, que conoce tu empresa y contesta cuando lo necesitas.</p></div></article>
      <article class="lp-tarjeta lp-tarjeta--fila"><span class="lp-ico">{ICONO['campana']}</span><div><h3>Alertas antes de cada vencimiento</h3><p>Te avisamos de riesgos y fechas tributarias antes de que se conviertan en sanción.</p></div></article>
      <article class="lp-tarjeta lp-tarjeta--fila"><span class="lp-ico">{ICONO['informe']}</span><div><h3>Informes que entiendes</h3><p>Reportes claros para la gerencia, los socios y el banco, entregados a tiempo.</p></div></article>
      <article class="lp-tarjeta lp-tarjeta--fila"><span class="lp-ico">{ICONO['pin']}</span><div><h3>Cerca de tu empresa</h3><p>Atención presencial en Medellín, Pereira, Armenia y Manizales.</p></div></article>
    </div>
  </div>
</section>

<!-- ===================== 10. TESTIMONIOS ===================== -->
{_testimonios()}

<!-- ===================== 11. WHATSAPP ===================== -->
<section class="lp-seccion lp-seccion--corta">
  <div class="lp-contenedor">
    <div class="lp-wa revelar">
      <h2 class="lp-titulo">¿Aún tienes preguntas?</h2>
      <p class="lp-texto">Escríbenos por WhatsApp y te responde alguien del equipo, no un robot.</p>
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
            data-sheets="{SHEETS_URL}" data-wa="{WA}">
        <h2 class="lp-titulo">Agenda tu evaluación de revisoría fiscal 2027</h2>
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

      <!-- 14. Pantallas de gracias -->
      <div class="lp-gracias" id="lp-gracias-ok" hidden tabindex="-1">
        <span class="lp-gracias__ico">{ICONO['check']}</span>
        <h2 class="lp-titulo">Listo, ya tenemos tus datos</h2>
        <p class="lp-texto">En menos de 24 horas hábiles te escribimos por WhatsApp para agendar tu evaluación. Si quieres adelantarte, escríbenos ahora.</p>
        <a class="lp-btn" id="lp-wa-ok" href="https://wa.me/{WA}" target="_blank" rel="noopener">{ICO['wa']}Escribir por WhatsApp</a>
      </div>
      <div class="lp-gracias" id="lp-gracias-peq" hidden tabindex="-1">
        <span class="lp-gracias__ico">{ICONO['check']}</span>
        <h2 class="lp-titulo">Gracias por escribirnos</h2>
        <p class="lp-texto">Por el tamaño de tu empresa, hoy no estás obligada a tener revisor fiscal. Te dejamos una guía para mantener tu contabilidad en orden y cumplir con la DIAN. Si quieres que revisemos tu caso, también podemos hablar.</p>
        <div class="lp-acciones">
          <a class="lp-btn" href="{GUIA_PEQUENAS}">Ver la guía{ICO['flecha']}</a>
          <a class="lp-btn lp-btn--contorno" id="lp-wa-peq" href="https://wa.me/{WA}" target="_blank" rel="noopener">Hablar por WhatsApp</a>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ===================== 15. CIERRE ===================== -->
<section class="lp-seccion lp-final">
  <div class="lp-contenedor lp-centro">
    <h2 class="lp-titulo lp-titulo--acento">Las asambleas son en marzo. Las buenas decisiones se toman antes.</h2>
    <p class="lp-texto">Agenda tu evaluación hoy y llega a la reunión con la propuesta en la mano.</p>
    {_boton()}
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
