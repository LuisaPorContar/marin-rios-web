/* ============================================================
   Landing · Evaluación de revisoría fiscal 2027
   - Envía el lead al Google Sheet (Apps Script, ver integraciones/).
   - Avisa a Google Tag Manager (evento para el píxel de Meta).
   - Abre WhatsApp con el mensaje armado y muestra la pantalla de gracias.
   ============================================================ */
(function () {
  'use strict';

  /* ---------- Video con fachada: YouTube solo carga al hacer clic ---------- */
  document.querySelectorAll('.lp-video[data-video]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var id = btn.getAttribute('data-video');
      var marco = document.createElement('iframe');
      marco.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(id) + '?autoplay=1&rel=0';
      marco.title = 'Video: antes de elegir revisor fiscal';
      marco.allow = 'autoplay; encrypted-media; picture-in-picture';
      marco.allowFullscreen = true;
      btn.replaceWith(marco);
      marco.classList.add('lp-video__marco');
      if (window.dataLayer) window.dataLayer.push({ event: 'lp_revisoria_video_play' });
    });
  });

  /* ---------- Formulario ---------- */
  var form = document.getElementById('lp-form');
  if (!form) return;
  var error = document.getElementById('lp-form-error');
  var boton = form.querySelector('button[type="submit"]');
  var URL_SHEETS = form.getAttribute('data-sheets') || '';
  var WA = form.getAttribute('data-wa');
  var PEQUENA = 'Menos de $1.000 millones';

  // Parámetros de la campaña (Meta los agrega a la URL del anuncio)
  var qs = new URLSearchParams(window.location.search);
  var utm = {};
  ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'fbclid'].forEach(function (k) {
    utm[k] = (qs.get(k) || '').slice(0, 200);
  });

  function valor(nombre) {
    var campo = form.elements[nombre];
    return campo ? String(campo.value || '').trim() : '';
  }

  // 300 123 4567 -> +573001234567 ; deja intactos los números con indicativo
  function normalizarTelefono(t) {
    var d = t.replace(/[^\d+]/g, '');
    if (d.charAt(0) === '+') return d;
    d = d.replace(/^0+/, '');
    if (d.length === 10 && d.charAt(0) === '3') return '+57' + d;
    if (d.indexOf('57') === 0 && d.length === 12) return '+' + d;
    return d;
  }

  function enviarAlSheet(datos) {
    if (!URL_SHEETS) return;
    var cuerpo = new URLSearchParams(datos);
    // no-cors: Apps Script no devuelve encabezados CORS; la respuesta es
    // opaca, pero la fila se escribe igual. keepalive asegura el envío
    // aunque el navegador cambie de pestaña al abrir WhatsApp.
    try {
      fetch(URL_SHEETS, { method: 'POST', mode: 'no-cors', body: cuerpo, keepalive: true });
    } catch (e) {
      if (navigator.sendBeacon) navigator.sendBeacon(URL_SHEETS, cuerpo);
    }
  }

  function mostrar(id) {
    form.hidden = true;
    var panel = document.getElementById(id);
    panel.hidden = false;
    panel.focus({ preventScroll: true });
    panel.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!form.checkValidity()) {
      error.hidden = false;
      form.reportValidity();
      return;
    }
    error.hidden = true;

    // Trampa para bots: si el campo oculto viene lleno, no se envía nada
    if (valor('web')) { mostrar('lp-gracias-ok'); return; }

    boton.disabled = true;

    var d = {
      nombre: valor('nombre'),
      empresa: valor('empresa'),
      cargo: valor('cargo'),
      ciudad: valor('ciudad'),
      ingresos: valor('ingresos'),
      revisor: valor('revisor'),
      whatsapp: normalizarTelefono(valor('whatsapp'))
    };
    var calificado = d.ingresos !== PEQUENA;

    var mensaje = 'Hola, soy ' + d.nombre + ', ' + d.cargo + ' de ' + d.empresa + ' en ' + d.ciudad +
      '. Quiero agendar la evaluación de revisoría fiscal 2027. Ingresos aproximados ' + d.ingresos +
      '. Revisor actual ' + d.revisor + '.';
    var urlWa = 'https://wa.me/' + WA + '?text=' + encodeURIComponent(mensaje);

    var registro = Object.assign({}, d, utm, {
      calificado: calificado ? 'Sí' : 'No',
      formulario: 'Landing Revisoría Fiscal 2027',
      pagina: window.location.origin + window.location.pathname
    });
    enviarAlSheet(registro);

    // Evento para GTM -> píxel de Meta (Lead). Sin datos personales.
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({
      event: 'lead_revisoria_2027',
      lead_calificado: calificado,
      lead_ingresos: d.ingresos,
      lead_ciudad: d.ciudad
    });

    if (calificado) {
      document.getElementById('lp-wa-ok').href = urlWa;
      window.open(urlWa, '_blank', 'noopener');
      mostrar('lp-gracias-ok');
    } else {
      document.getElementById('lp-wa-peq').href = urlWa;
      mostrar('lp-gracias-peq');
    }
  });
})();
