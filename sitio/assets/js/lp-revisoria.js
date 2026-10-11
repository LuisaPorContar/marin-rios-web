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

  /* ---------- Video propio del héroe: el .mp4 solo se pide al hacer clic ---------- */
  document.querySelectorAll('.lp-vvideo[data-mp4]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var v = document.createElement('video');
      v.className = 'lp-vvideo__marco';
      v.src = btn.getAttribute('data-mp4');
      v.poster = btn.querySelector('img').currentSrc || btn.querySelector('img').src;
      v.controls = true; v.autoplay = true; v.playsInline = true;
      v.setAttribute('playsinline', '');
      btn.replaceWith(v);
      v.play().catch(function () {});
      if (window.dataLayer) window.dataLayer.push({ event: 'lp_revisoria_video_play' });
    });
  });

  /* ---------- Páginas de gracias ----------
     El formulario redirige aquí para que Meta mida la conversión por URL.
     El mensaje de WhatsApp armado con los datos viaja en sessionStorage. */
  var panelGracias = document.querySelector('[data-gracias]');
  if (panelGracias) {
    var guardado = '';
    try { guardado = sessionStorage.getItem('lp_wa') || ''; } catch (e) {}
    if (guardado) {
      document.querySelectorAll('[data-wa-lead]').forEach(function (a) { a.href = guardado; });
    }
    // Conversión en Meta: Lead solo para el lead calificado
    if (window.fbq) {
      var idLead = '';
      try { idLead = sessionStorage.getItem('lp_event_id') || ''; sessionStorage.removeItem('lp_event_id'); } catch (e4) {}
      if (panelGracias.getAttribute('data-gracias') === 'calificado') {
        // Solo cuenta si viene del formulario (evita Leads por recargar la página)
        if (idLead) fbq('track', 'Lead', { content_name: 'Evaluación revisoría fiscal 2027', content_category: 'Servicios profesionales' }, { eventID: idLead });
      }
      else fbq('trackCustom', 'LeadNoCalificado');
    }
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({
      event: 'gracias_revisoria_2027',
      lead_calificado: panelGracias.getAttribute('data-gracias') === 'calificado'
    });
  }

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

  function galleta(nombre) {
    var m = document.cookie.match(new RegExp('(?:^|; )' + nombre + '=([^;]*)'));
    return m ? decodeURIComponent(m[1]) : '';
  }

  // Meta: quien llega a la landing vio el contenido del servicio
  if (window.fbq) fbq('track', 'ViewContent', { content_name: 'Evaluación revisoría fiscal 2027', content_category: 'Servicios profesionales' });

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
    // Un solo envío. sendBeacon está hecho para esto: el navegador lo entrega
    // aunque la página cambie enseguida. Solo si no existe o no lo acepta se
    // usa fetch. (Enviar por los dos caminos duplicaba el lead.)
    var entregado = false;
    try { entregado = !!(navigator.sendBeacon && navigator.sendBeacon(URL_SHEETS, cuerpo)); } catch (e) {}
    if (!entregado) {
      try { fetch(URL_SHEETS, { method: 'POST', mode: 'no-cors', body: cuerpo, keepalive: true }).catch(function () {}); } catch (e2) {}
    }
  }

  function mostrar(id) {
    form.hidden = true;
    var panel = document.getElementById(id);
    panel.hidden = false;
    panel.focus({ preventScroll: true });
    panel.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

  // WhatsApp: solo números (borra letras, espacios y símbolos mientras se escribe)
  form.elements.whatsapp.addEventListener('input', function () {
    var limpio = this.value.replace(/\D/g, '');
    if (limpio !== this.value) this.value = limpio;
  });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!form.checkValidity()) {
      error.hidden = false;
      form.reportValidity();
      return;
    }
    error.hidden = true;

    boton.disabled = true;

    var d = {
      nombre: valor('nombre'),
      empresa: valor('empresa'),
      correo: valor('correo').toLowerCase(),
      ciudad: valor('ciudad'),
      ingresos: valor('ingresos'),
      whatsapp: normalizarTelefono(valor('whatsapp'))
    };
    var calificado = d.ingresos !== PEQUENA;

    var mensaje = 'Hola, soy ' + d.nombre + ' de ' + d.empresa + ' en ' + d.ciudad +
      '. Quiero agendar la evaluación de revisoría fiscal 2027. Ingresos aproximados ' + d.ingresos + '.';
    var urlWa = 'https://wa.me/' + WA + '?text=' + encodeURIComponent(mensaje);

    // Identificador único del lead: el píxel (navegador) y la API de
    // conversiones (servidor) lo envían igual para que Meta no lo cuente doble.
    var idEvento = 'rf27-' + Date.now() + '-' + Math.random().toString(36).slice(2, 10);
    try { sessionStorage.setItem('lp_event_id', idEvento); } catch (e3) {}
    var fbc = galleta('_fbc') || (utm.fbclid ? 'fb.1.' + Date.now() + '.' + utm.fbclid : '');

    var registro = Object.assign({}, d, utm, {
      calificado: calificado ? 'Sí' : 'No',
      formulario: 'Landing Revisoría Fiscal 2027',
      pagina: window.location.origin + window.location.pathname,
      event_id: idEvento,
      fbp: galleta('_fbp'),
      fbc: fbc,
      agente: navigator.userAgent
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

    // Redirige a la página de gracias (una URL por tipo de lead, para que
    // Meta cuente solo los calificados). La pausa deja salir el envío al
    // Sheet y el evento de GTM antes de cambiar de página.
    try { sessionStorage.setItem('lp_wa', urlWa); } catch (e2) {}
    var destino = calificado ? form.getAttribute('data-gracias-ok') : form.getAttribute('data-gracias-peq');
    setTimeout(function () { window.location.href = destino; }, 900);
  });
})();
