/**
 * SCRIPT DE LA HOJA "Leads_Consolidado Marin Rios"
 * ------------------------------------------------------------------
 * Cada vez que alguien envía el formulario de la web:
 *   1. Guarda el lead como fila en la pestaña "Leads".
 *   2. Le avisa al equipo por correo, con todos los datos del cliente
 *      (SIEMPRE, califique o no).
 *   3. Si la empresa CALIFICA: le envía al cliente un correo de bienvenida
 *      y avisa a Meta por la API de conversiones.
 *      Si NO califica: no se le envía nada; lo maneja el comercial.
 *
 * DE DÓNDE SALEN LOS CORREOS: de la cuenta de Google que publica este
 * script (la que elige "Ejecutar como: Yo"). El cliente ve esa dirección
 * como remitente. Las respuestas del cliente van a RESPONDER_A.
 *
 * Instalación: Extensiones → Apps Script → pegar este archivo completo →
 * Implementar → Nueva implementación → Aplicación web.
 * (Pasos completos en COMO-CONECTAR-EL-SHEET.md)
 *
 * Ya no hay secuencia de correos de recuperación (día 1, 3 y 7).
 * Si existía el disparador diario, ejecuta una vez `quitarTriggerRecuperacion`.
 */

// ==================================================================
// AJUSTES
// ==================================================================
var PESTANA = 'Leads';
var ZONA = 'America/Bogota';

// Aviso interno: a quién le llega el correo cada vez que entra un lead.
// Varios correos separados por coma. Si se deja vacío, le llega a la cuenta
// de Google dueña de este script.
var AVISAR_A = '';

// Correo de bienvenida al cliente (solo leads calificados)
var CORREO_ACTIVO = true;
// A qué correo llegan las respuestas del cliente a la bienvenida.
// Vacío = a la cuenta de Google dueña de este script.
var RESPONDER_A = '';
var NUMERO_WHATSAPP = '573044176934';
var FIRMA_NOMBRE = 'Maribel';
var FIRMA_CARGO = 'Directora Administrativa';

// Meta (API de conversiones). El token NO va aquí: se guarda en
// Configuración del proyecto (engranaje) → Propiedades de la secuencia de comandos:
//   META_TOKEN      = token de acceso de la API de conversiones
//   META_TEST_CODE  = código de "Probar eventos" (solo mientras se prueba; luego se borra)
var META_PIXEL = '4029344540722147';
var META_API = 'v21.0';

var MESES = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
             'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];


// ==================================================================
// 1. RECIBIR EL FORMULARIO
// ==================================================================
function doPost(e) {
  var p = (e && e.parameter) || {};

  // Filtro mínimo contra bots y envíos vacíos
  if (p.web) return respuesta({ ok: true });
  if (!p.nombre || !p.whatsapp) return respuesta({ ok: false, error: 'faltan datos' });

  var ahora = new Date();
  var bloqueo = LockService.getScriptLock();
  bloqueo.waitLock(20000);
  try {
    guardarLead(p, ahora);
  } finally {
    bloqueo.releaseLock();
  }

  // Lo que sigue no debe impedir que el lead quede guardado: cada paso
  // registra su error (menú Ejecuciones) y deja continuar al siguiente.
  try { avisarAlEquipo(p, ahora); } catch (err) { console.error('Aviso al equipo: ' + err); }
  // Al cliente solo se le escribe si califica. Si no, lo maneja el comercial.
  if (p.calificado === 'Sí') {
    if (CORREO_ACTIVO && correoValido(p.correo)) {
      try { enviarBienvenida(p); } catch (err) { console.error('Correo de bienvenida: ' + err); }
    }
    try { enviarAMeta(p, ahora); } catch (err) { console.error('Meta CAPI: ' + err); }
  }
  return respuesta({ ok: true });
}

// Para comprobar en el navegador que la aplicación web está publicada
function doGet() {
  return respuesta({ ok: true, servicio: 'leads marinriosconsultores.com' });
}

/**
 * Escribe por NOMBRE de columna, no por posición: si alguien mueve o agrega
 * columnas en la hoja, cada dato sigue cayendo en su lugar.
 */
function guardarLead(p, ahora) {
  var hoja = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(PESTANA);
  var encabezados = hoja.getRange(1, 1, 1, hoja.getLastColumn()).getValues()[0]
    .map(function (h) { return String(h).trim(); });

  var mes = MESES[Number(Utilities.formatDate(ahora, ZONA, 'M')) - 1] + ' ' +
            Utilities.formatDate(ahora, ZONA, 'yyyy');

  var fuente = [p.utm_source, p.utm_medium, p.utm_content].filter(Boolean).join(' / ');
  var notas = [
    'Ciudad: ' + (p.ciudad || ''),
    'Calificado por ingresos: ' + (p.calificado || ''),
    fuente ? 'Fuente: ' + fuente : ''
  ].filter(String).join(' · ');

  var valores = {
    'Mes': mes,
    'Fecha': Utilities.formatDate(ahora, ZONA, 'dd/MM/yyyy'),
    'Nombre': p.nombre,
    'Teléfono': p.whatsapp,
    'Correo': p.correo || '',
    'Empresa': p.empresa || '',
    'Tipo de persona': 'Persona jurídica (empresa)',
    'Rango de ventas': p.ingresos || '',
    'Conjunto de anuncios': p.utm_campaign || p.utm_source || 'Directo / orgánico',
    'Formulario': p.formulario || 'Landing',
    'Estado del lead': '',
    'Notas': notas,
    'ID_Lead': 'RF27-' + Utilities.formatDate(ahora, ZONA, 'yyyyMMdd-HHmmss'),
    'Visible': 1
  };

  hoja.appendRow(encabezados.map(function (h) {
    return h in valores ? limpiar(valores[h]) : '';
  }));
}


// ==================================================================
// 2. AVISO AL EQUIPO (siempre que entra un lead, califique o no)
// ==================================================================
function avisarAlEquipo(p, ahora) {
  var para = String(AVISAR_A || '').trim() || Session.getEffectiveUser().getEmail();
  if (!para) return;

  var califica = p.calificado === 'Sí';
  var digitos = String(p.whatsapp || '').replace(/\D/g, '');
  var fuente = [p.utm_source, p.utm_medium, p.utm_campaign, p.utm_content].filter(Boolean).join(' / ') || 'Directo / orgánico';
  var primerNombre = String(p.nombre || '').trim().split(/\s+/)[0];
  var enlaceWa = 'https://wa.me/' + digitos + '?text=' + encodeURIComponent(
    'Hola ' + primerNombre + ', te escribe ' + FIRMA_NOMBRE + ' de Marín Ríos Consultores. Recibimos tu solicitud de evaluación de revisoría fiscal.');
  var hoja = SpreadsheetApp.getActiveSpreadsheet();

  var filas = [
    ['Nombre', p.nombre],
    ['Empresa', p.empresa],
    ['WhatsApp', p.whatsapp],
    ['Correo', p.correo],
    ['Ciudad', p.ciudad],
    ['Ingresos anuales', p.ingresos],
    ['¿Califica?', califica ? 'Sí. Ya recibió el correo de bienvenida.' : 'No (empresa pequeña). No se le envió nada: contactar desde comercial.'],
    ['Formulario', p.formulario],
    ['Fuente', fuente],
    ['Fecha', Utilities.formatDate(ahora, ZONA, 'dd/MM/yyyy HH:mm')]
  ].map(function (f) {
    return '<tr><td style="padding: 9px 12px; border-bottom: 1px solid #e6eaf2; color: #5a6b7d; font-size: 13px; white-space: nowrap;">' + f[0] + '</td>' +
           '<td style="padding: 9px 12px; border-bottom: 1px solid #e6eaf2; color: #1a1a1a; font-size: 15px;"><b>' + html(f[1] || '—') + '</b></td></tr>';
  }).join('');

  var cuerpo = '<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">' +
    '<div style="background: ' + (califica ? '#0B0733' : '#5a6b7d') + '; padding: 22px 24px;">' +
    '<div style="color: #8FE3FF; font-size: 12px; letter-spacing: 1px;">NUEVO LEAD · ' + (califica ? 'CALIFICADO' : 'NO CALIFICA') + '</div>' +
    '<div style="color: #ffffff; font-size: 20px; font-weight: bold; margin-top: 4px;">' + html(p.empresa || p.nombre || 'Sin nombre') + '</div>' +
    '</div>' +
    '<div style="padding: 20px 16px; background: #ffffff;">' +
    '<table style="width: 100%; border-collapse: collapse;">' + filas + '</table>' +
    '<div style="text-align: center; margin: 24px 0 8px;">' +
    '<a href="' + enlaceWa + '" style="background: #25D366; color: #ffffff; text-decoration: none; padding: 13px 26px; border-radius: 8px; font-weight: bold; font-size: 15px; display: inline-block; margin: 4px;">Escribirle por WhatsApp</a>' +
    '<a href="tel:+' + digitos + '" style="background: #2BB3EF; color: #0B0733; text-decoration: none; padding: 13px 26px; border-radius: 8px; font-weight: bold; font-size: 15px; display: inline-block; margin: 4px;">Llamar</a>' +
    '</div>' +
    '<p style="text-align: center; font-size: 13px; margin: 14px 0 0;"><a href="' + hoja.getUrl() + '" style="color: #1A6FB8;">Abrir la hoja de leads</a></p>' +
    '</div>' +
    '</div>';

  var opciones = {
    to: para,
    subject: (califica ? 'Nuevo lead CALIFICADO: ' : 'Nuevo lead (no califica): ') + (p.empresa || p.nombre || '') + (p.ciudad ? ' · ' + p.ciudad : ''),
    htmlBody: cuerpo,
    name: 'Leads web Marín Ríos'
  };
  if (correoValido(p.correo)) opciones.replyTo = String(p.correo).trim();   // "Responder" le escribe al cliente
  MailApp.sendEmail(opciones);
}


// ==================================================================
// 3. CORREO DE BIENVENIDA AL CLIENTE (uno solo, al recibir el formulario)
// ==================================================================
function enviarBienvenida(p) {
  var primerNombre = String(p.nombre || '').trim().split(/\s+/)[0];
  var saludo = primerNombre ? 'Hola ' + html(primerNombre) + ',' : 'Hola,';
  var enlaceWa = 'https://wa.me/' + NUMERO_WHATSAPP + '?text=' +
    encodeURIComponent('Hola, llené el formulario de revisoría fiscal y quiero agendar mi evaluación');

  var asunto = 'Recibimos tus datos: tu evaluación de revisoría fiscal';
  var parrafos = [
    'Gracias por escribirnos' + (p.empresa ? ' desde <b>' + html(p.empresa) + '</b>' : '') + '. Ya tenemos tus datos.',
    'En menos de 24 horas hábiles te contactamos por WhatsApp para agendar tu evaluación gratuita. En esa reunión revisamos si tu empresa está obligada a tener revisor fiscal en 2027, qué riesgos tiene hoy frente a la DIAN y te entregamos una propuesta escrita para tu asamblea.',
    'Si prefieres adelantarte, escríbenos ahora:'
  ];
  var boton = { texto: 'Agendar por WhatsApp', enlace: enlaceWa };

  var cuerpo = '<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">' +
    '<div style="background: #0B0733; padding: 32px 24px; text-align: center;">' +
    '<div style="color: #ffffff; font-size: 20px; font-weight: bold; letter-spacing: 0.5px;">MARÍN RÍOS CONSULTORES</div>' +
    '<div style="color: #8FE3FF; font-size: 12px; margin-top: 4px; letter-spacing: 1px;">REVISORÍA FISCAL · CONTABILIDAD · FINANZAS</div>' +
    '</div>' +
    '<div style="padding: 32px 28px; background: #ffffff;">' +
    '<p style="font-size: 16px; color: #1a1a1a; margin: 0 0 16px;">' + saludo + '</p>' +
    parrafos.map(function (t) {
      return '<p style="font-size: 15px; line-height: 1.7; color: #1a1a1a; margin: 0 0 16px;">' + t + '</p>';
    }).join('') +
    '<div style="text-align: center; margin: 8px 0 24px;">' +
    '<a href="' + boton.enlace + '" style="background: #2BB3EF; color: #0B0733; text-decoration: none; padding: 14px 32px; border-radius: 8px; font-weight: bold; font-size: 16px; display: inline-block;">' + boton.texto + '</a>' +
    '</div>' +
    '<p style="font-size: 15px; color: #1a1a1a; margin: 24px 0 0;">Con gusto te atendemos,</p>' +
    '<p style="font-size: 15px; color: #1a1a1a; margin: 4px 0 0;"><b>' + FIRMA_NOMBRE + '</b><br>' +
    '<span style="color: #5a6b7d; font-size: 13px;">' + FIRMA_CARGO + ' &middot; Marín Ríos Consultores</span></p>' +
    '</div>' +
    '<div style="background: #EAF2FB; padding: 16px 28px; text-align: center;">' +
    '<span style="font-size: 12px; color: #5a6b7d;">Marín Ríos Consultores S.A.S · Recibes este correo porque llenaste el formulario en marinriosconsultores.com</span>' +
    '</div>' +
    '</div>';

  var opciones = {
    to: String(p.correo).trim(),
    subject: asunto,
    htmlBody: cuerpo,
    name: 'Marín Ríos Consultores'
  };
  if (correoValido(RESPONDER_A)) opciones.replyTo = String(RESPONDER_A).trim();
  MailApp.sendEmail(opciones);
}

function correoValido(c) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(String(c || '').trim());
}


// ==================================================================
// 4. META · API DE CONVERSIONES (CAPI)
// ------------------------------------------------------------------
// Envía el evento "Lead" desde el servidor con el mismo event_id que usa el
// píxel en la página de gracias, para que Meta lo cuente una sola vez.
// Reglas de formato: developers.facebook.com → Conversions API → Parameters
// ==================================================================
function enviarAMeta(p, ahora) {
  var props = PropertiesService.getScriptProperties();
  var token = props.getProperty('META_TOKEN');
  if (!token) return;   // sin token no se envía nada (el lead igual quedó en la hoja)

  // Datos del cliente: normalizados y cifrados con SHA-256, como exige Meta
  var partes = String(p.nombre || '').trim().split(/\s+/);
  var usuario = {
    ph: [hash(String(p.whatsapp || '').replace(/\D/g, ''))],   // solo dígitos, con indicativo: 573001234567
    fn: [hash(nombreMeta(partes[0] || ''))],
    country: [hash('co')],
    client_user_agent: p.agente || ''                          // sin cifrar
  };
  if (partes.length > 1) usuario.ln = [hash(nombreMeta(partes.slice(1).join(' ')))];
  if (correoValido(p.correo)) usuario.em = [hash(String(p.correo).trim().toLowerCase())];
  var ciudad = sinTildes(String(p.ciudad || '').split(' y ')[0]).replace(/[^a-z]/g, '');
  if (ciudad && ciudad !== 'otra') usuario.ct = [hash(ciudad)];
  if (p.fbp) usuario.fbp = p.fbp;                              // cookies del píxel, sin cifrar
  if (p.fbc) usuario.fbc = p.fbc;

  var cuerpo = {
    data: [{
      event_name: 'Lead',
      event_time: Math.floor(ahora.getTime() / 1000),
      event_id: p.event_id || ('rf27-' + ahora.getTime()),
      action_source: 'website',
      event_source_url: p.pagina || 'https://marinriosconsultores.com/evaluacion-revisoria-fiscal/',
      user_data: usuario,
      custom_data: {
        content_name: 'Evaluación revisoría fiscal 2027',
        content_category: 'Servicios profesionales',
        lead_ingresos: p.ingresos || ''
      }
    }]
  };
  var prueba = props.getProperty('META_TEST_CODE');
  if (prueba) cuerpo.test_event_code = prueba;

  var r = UrlFetchApp.fetch(
    'https://graph.facebook.com/' + META_API + '/' + META_PIXEL + '/events?access_token=' + encodeURIComponent(token), {
      method: 'post', contentType: 'application/json',
      payload: JSON.stringify(cuerpo), muteHttpExceptions: true
    });
  if (r.getResponseCode() !== 200) {
    console.error('Meta CAPI ' + r.getResponseCode() + ': ' + r.getContentText().slice(0, 300));
  }
  return r.getResponseCode() + ' ' + r.getContentText().slice(0, 200);
}

// Nombre y apellido: minúsculas, sin puntuación (las tildes se conservan)
function nombreMeta(t) {
  return String(t).toLowerCase().trim().replace(/[.,;:'"()\-]/g, '');
}

// Ciudad: minúsculas y sin tildes
function sinTildes(t) {
  return String(t).toLowerCase().trim().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
}

function hash(t) {
  if (!t) return '';
  return Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, t, Utilities.Charset.UTF_8)
    .map(function (b) { return ('0' + (b & 0xff).toString(16)).slice(-2); }).join('');
}


// ==================================================================
// 5. PRUEBAS Y MANTENIMIENTO (se ejecutan a mano desde el editor)
// ==================================================================
var LEAD_DE_PRUEBA = {
  nombre: 'Prueba Marin Rios', empresa: 'Empresa de Prueba SAS', whatsapp: '+573000000000',
  ciudad: 'Medellín y Valle de Aburrá', ingresos: '$5.000 a $20.000 millones',
  correo: 'prueba@ejemplo.com', agente: 'Mozilla/5.0 (prueba)', calificado: 'Sí', formulario: 'PRUEBA'
};

// Envía el aviso interno de prueba (a AVISAR_A, o a tu cuenta si está vacío).
function probarAviso() {
  avisarAlEquipo(LEAD_DE_PRUEBA, new Date());
  Logger.log('Aviso de prueba enviado a ' + (String(AVISAR_A || '').trim() || Session.getEffectiveUser().getEmail()));
}

// Envía un Lead de prueba a Meta. Debe verse en "Probar eventos" como Servidor.
function probarMeta() {
  Logger.log(enviarAMeta(LEAD_DE_PRUEBA, new Date()) || 'No hay META_TOKEN en las propiedades del script');
}

// Envía el correo de bienvenida a tu propia cuenta para ver cómo queda.
function probarBienvenida() {
  var lead = JSON.parse(JSON.stringify(LEAD_DE_PRUEBA));
  lead.correo = Session.getActiveUser().getEmail();
  enviarBienvenida(lead);
  Logger.log('Correo de prueba enviado a ' + lead.correo);
}

// Ejecutar UNA VEZ: borra el disparador diario de la secuencia de
// recuperación anterior (día 1, 3 y 7), que ya no existe en este script.
function quitarTriggerRecuperacion() {
  var borrados = 0;
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === 'procesarRecuperacion') { ScriptApp.deleteTrigger(t); borrados++; }
  });
  Logger.log('Disparadores eliminados: ' + borrados);
}


// ==================================================================
// UTILIDADES
// ==================================================================
// Evita que un texto que empiece por = + - @ se interprete como fórmula
// (así el teléfono +57... queda como texto, igual que los leads existentes).
function limpiar(v) {
  if (typeof v !== 'string') return v;
  v = v.slice(0, 500);
  return /^[=+\-@]/.test(v) ? "'" + v : v;
}

// Para usar en el correo lo que escribió la persona sin que rompa el HTML
function html(t) {
  return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function respuesta(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
