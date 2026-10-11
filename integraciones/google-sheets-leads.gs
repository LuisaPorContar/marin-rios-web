/**
 * SCRIPT COMPLETO DE LA HOJA "Leads_Consolidado Marin Rios"
 * Parte 1: recibe los formularios de la web y avisa a Meta (CAPI).
 * Parte 2: secuencia de correos de recuperación (día 1, 3 y 7).
 *
 * PARTE 1 · Recibe los leads de las landings de marinriosconsultores.com y los agrega
 * como fila en la pestaña "Leads" de "Leads_Consolidado Marin Rios".
 *
 * Se instala desde la propia hoja: Extensiones → Apps Script → pegar este
 * archivo → Implementar → Nueva implementación → Aplicación web.
 * (Pasos completos en COMO-CONECTAR-EL-SHEET.md)
 *
 * Escribe por NOMBRE de columna, no por posición: si alguien mueve o agrega
 * columnas en la hoja, el script sigue llenando cada dato en su lugar.
 */

var PESTANA = 'Leads';
var ZONA = 'America/Bogota';
var MESES = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
             'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];

function doPost(e) {
  var p = (e && e.parameter) || {};

  // Filtro mínimo contra bots y envíos vacíos
  if (p.web) return respuesta({ ok: true });
  if (!p.nombre || !p.whatsapp) return respuesta({ ok: false, error: 'faltan datos' });

  var bloqueo = LockService.getScriptLock();
  bloqueo.waitLock(20000);
  try {
    var hoja = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(PESTANA);
    var encabezados = hoja.getRange(1, 1, 1, hoja.getLastColumn()).getValues()[0]
      .map(function (h) { return String(h).trim(); });

    var ahora = new Date();
    var mes = MESES[Number(Utilities.formatDate(ahora, ZONA, 'M')) - 1] + ' ' +
              Utilities.formatDate(ahora, ZONA, 'yyyy');

    var notas = [
      'Cargo: ' + (p.cargo || ''),
      'Ciudad: ' + (p.ciudad || ''),
      'Revisor actual: ' + (p.revisor || ''),
      'Calificado por ingresos: ' + (p.calificado || ''),
      'Fuente: ' + [p.utm_source, p.utm_medium, p.utm_content].filter(String).join(' / ')
    ].join(' · ');

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

    var fila = encabezados.map(function (h) {
      return h in valores ? limpiar(valores[h]) : '';
    });
    hoja.appendRow(fila);

    // API de conversiones de Meta: solo leads calificados. Si falla, el lead
    // ya quedó guardado en la hoja; el error se registra y no se pierde nada.
    if (p.calificado === 'Sí') {
      try { enviarAMeta(p, ahora); } catch (err) { console.error('Meta CAPI: ' + err); }
    }
    return respuesta({ ok: true });
  } finally {
    bloqueo.releaseLock();
  }
}

// ------------------------------------------------------------------
// API de conversiones de Meta (CAPI)
// El token NO va en este archivo. Se guarda en:
//   Configuración del proyecto (engranaje) → Propiedades de la secuencia
//   de comandos → META_TOKEN = <token de acceso>
// Opcional mientras se prueba: META_TEST_CODE = <código TEST12345>
// ------------------------------------------------------------------
var META_PIXEL = '4029344540722147';
var META_API = 'v21.0';

function enviarAMeta(p, ahora) {
  var props = PropertiesService.getScriptProperties();
  var token = props.getProperty('META_TOKEN');
  if (!token) return;

  var partes = String(p.nombre || '').trim().split(/\s+/);
  var usuario = {
    ph: [hash(String(p.whatsapp || '').replace(/\D/g, ''))],
    fn: [hash(nombreMeta(partes[0] || ''))],
    country: [hash('co')],
    client_user_agent: p.agente || ''
  };
  if (partes.length > 1) usuario.ln = [hash(nombreMeta(partes.slice(1).join(' ')))];
  var ciudad = normalizar(String(p.ciudad || '').split(' y ')[0]).replace(/[^a-z]/g, '');
  if (ciudad && ciudad !== 'otra') usuario.ct = [hash(ciudad)];
  if (p.fbp) usuario.fbp = p.fbp;
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
        lead_ingresos: p.ingresos || '',
        lead_cargo: p.cargo || ''
      }
    }]
  };
  var prueba = props.getProperty('META_TEST_CODE');
  if (prueba) cuerpo.test_event_code = prueba;

  var r = UrlFetchApp.fetch('https://graph.facebook.com/' + META_API + '/' + META_PIXEL + '/events?access_token=' + encodeURIComponent(token), {
    method: 'post', contentType: 'application/json',
    payload: JSON.stringify(cuerpo), muteHttpExceptions: true
  });
  if (r.getResponseCode() !== 200) console.error('Meta CAPI ' + r.getResponseCode() + ': ' + r.getContentText().slice(0, 300));
}

// Reglas de Meta antes de cifrar (SHA-256):
//  - teléfono: solo dígitos, con indicativo de país (573001234567)
//  - nombre y apellido: minúsculas, sin puntuación (las tildes se conservan)
//  - ciudad: minúsculas, sin espacios, tildes ni puntuación (medellin)
//  - país: código ISO de 2 letras en minúscula (co)
function nombreMeta(t) {
  return String(t).toLowerCase().trim().replace(/[.,;:'"()\-]/g, '');
}

function normalizar(t) {
  return String(t).toLowerCase().trim().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
}

function hash(t) {
  if (!t) return '';
  return Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, t, Utilities.Charset.UTF_8)
    .map(function (b) { return ('0' + (b & 0xff).toString(16)).slice(-2); }).join('');
}

// Ejecutar a mano desde el editor para probar la conexión con Meta
function probarMeta() {
  enviarAMeta({ nombre: 'Prueba Marin Rios', whatsapp: '+573000000000', ciudad: 'Medellín y Valle de Aburrá',
                ingresos: '$5.000 a $20.000 millones', cargo: 'Gerente general o representante legal',
                agente: 'Mozilla/5.0 (prueba)', calificado: 'Sí' }, new Date());
}

// Para comprobar en el navegador que la aplicación web está publicada
function doGet() {
  return respuesta({ ok: true, servicio: 'leads marinriosconsultores.com' });
}

// Evita que un texto que empiece por = + - @ se interprete como fórmula
// (así el teléfono +57... queda como texto, igual que los leads existentes).
function limpiar(v) {
  if (typeof v !== 'string') return v;
  v = v.slice(0, 500);
  return /^[=+\-@]/.test(v) ? "'" + v : v;
}

function respuesta(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}


// ==================================================================
// PARTE 2 · SECUENCIA DE RECUPERACIÓN DE LEADS POR CORREO
// ------------------------------------------------------------------
// Cada día hábil a las 9 a. m. revisa la pestaña "Leads". A los leads con
// Estado = "Recuperación" y con correo les envía tres correos: día 1, día 3
// y día 7. Si el estado cambia, limpia el control (columnas N a Q).
//
// Corregido frente a la versión anterior:
//  - El correo nunca salía: decía `content.asunto` en vez de `contenido.asunto`.
//  - Si el día 1 fallaba, ese lead se quedaba sin el primer correo para siempre.
// ==================================================================

var LIMITE_CORREOS_POR_CORRIDA = 30;
var NUMERO_WHATSAPP = '573044176934';
var MENSAJE_WHATSAPP = 'Tengo una empresa y quiero agendar una asesoria';

// Posición de cada columna (A = 0). Si se mueven columnas en la hoja, hay
// que actualizar estos números.
var COL = {
  MES: 0, FECHA: 1, NOMBRE: 2, TELEFONO: 3, CORREO: 4, EMPRESA: 5,
  TIPO_PERSONA: 6, RANGO_VENTAS: 7, CONJUNTO_ANUNCIOS: 8, FORMULARIO: 9,
  ESTADO: 10, NOTAS: 11,
  ID_LEAD: 12,                    // columna M
  FECHA_INICIO_RECUPERACION: 13,  // columna N
  DIA1_ENVIADO: 14,               // columna O
  DIA3_ENVIADO: 15,               // columna P
  DIA7_ENVIADO: 16                // columna Q
};

var ENCABEZADOS_CONTROL = ['Fecha inicio recuperacion', 'Dia 1 enviado', 'Dia 3 enviado', 'Dia 7 enviado'];

/** Ejecutar UNA VEZ: crea el disparador diario de las 9 a. m. */
function configurarTriggerRecuperacion() {
  asegurarEncabezadosControl();
  var yaExiste = ScriptApp.getProjectTriggers().some(function (t) {
    return t.getHandlerFunction() === 'procesarRecuperacion';
  });
  if (!yaExiste) {
    ScriptApp.newTrigger('procesarRecuperacion').timeBased().everyDays(1).atHour(9).create();
  }
  procesarRecuperacion();
}

function asegurarEncabezadosControl() {
  var hoja = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(PESTANA);
  var rango = hoja.getRange(1, COL.FECHA_INICIO_RECUPERACION + 1, 1, 4);
  var faltan = rango.getValues()[0].some(function (v) { return !v; });
  if (faltan) rango.setValues([ENCABEZADOS_CONTROL]);
}

function procesarRecuperacion() {
  var hoy = new Date();
  var diaSemana = Number(Utilities.formatDate(hoy, ZONA, 'u'));  // 1 = lunes … 7 = domingo
  if (diaSemana >= 6) return;                                    // no corre fines de semana

  var hoja = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(PESTANA);
  var datos = hoja.getDataRange().getValues();
  var enviados = 0;

  for (var fila = 1; fila < datos.length; fila++) {
    if (enviados >= LIMITE_CORREOS_POR_CORRIDA) break;

    var registro = datos[fila];
    var estado = String(registro[COL.ESTADO] || '').trim();
    var correo = String(registro[COL.CORREO] || '').trim();
    var nombre = String(registro[COL.NOMBRE] || '').trim();
    var filaSheet = fila + 1;

    var fechaInicioRaw = registro[COL.FECHA_INICIO_RECUPERACION];
    var dia1Enviado = registro[COL.DIA1_ENVIADO] === true;
    var dia3Enviado = registro[COL.DIA3_ENVIADO] === true;
    var dia7Enviado = registro[COL.DIA7_ENVIADO] === true;

    // Si ya no está en recuperación, limpia N a Q (la M, ID_Lead, no se toca)
    if (quitarTildes(estado) !== 'recuperacion') {
      if (fechaInicioRaw || dia1Enviado || dia3Enviado || dia7Enviado) {
        hoja.getRange(filaSheet, COL.FECHA_INICIO_RECUPERACION + 1, 1, 4).setValues([['', false, false, false]]);
      }
      continue;
    }
    if (!correo) continue;

    var dia = 0;
    if (!dia1Enviado) {
      dia = 1;
    } else {
      var transcurridos = Math.floor((hoy - new Date(fechaInicioRaw)) / (1000 * 60 * 60 * 24));
      if (!dia3Enviado && transcurridos >= 3) dia = 3;
      else if (dia3Enviado && !dia7Enviado && transcurridos >= 7) dia = 7;
    }
    if (!dia) continue;

    try {
      enviarCorreoRecuperacion(correo, nombre, dia);
      // La fecha de inicio se marca cuando el día 1 sí salió
      if (dia === 1) hoja.getRange(filaSheet, COL.FECHA_INICIO_RECUPERACION + 1).setValue(hoy);
      var columna = dia === 1 ? COL.DIA1_ENVIADO : (dia === 3 ? COL.DIA3_ENVIADO : COL.DIA7_ENVIADO);
      hoja.getRange(filaSheet, columna + 1).setValue(true);
      enviados++;
    } catch (error) {
      // Un correo mal escrito no detiene a los demás
      console.error('No se pudo enviar el dia ' + dia + ' a ' + correo + ': ' + error);
      if (String(error).indexOf('Service invoked too many times') !== -1) break;  // cupo diario de Gmail agotado
    }
  }
}

function quitarTildes(texto) {
  return String(texto).toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
}

function enviarCorreoRecuperacion(correo, nombre, dia) {
  var enlaceWhatsapp = 'https://wa.me/' + NUMERO_WHATSAPP + '?text=' + encodeURIComponent(MENSAJE_WHATSAPP);
  var primerNombre = nombre ? nombre.split(' ')[0] : '';
  var saludo = primerNombre ? ('Hola ' + primerNombre + ',') : 'Hola,';

  var contenidos = {
    1: {
      asunto: '¿Sigues pensando en poner al día tu contabilidad?',
      cuerpo: 'Notamos que dejaste tus datos con nosotros hace poco, pero no hemos logrado concretar un espacio contigo. ' +
        'Sabemos que el día a día de una empresa no da tregua, así que te dejamos la puerta abierta: agenda una asesoría ' +
        'con nuestro equipo cuando te quede más cómodo.'
    },
    3: {
      asunto: 'No queremos perder el contacto contigo',
      cuerpo: 'Hace unos días te escribimos y todavía no hemos podido coordinar tu asesoría. Entendemos que la agenda se ' +
        'complica, por eso te dejamos abierta la posibilidad de escribirnos directo por WhatsApp y cuadrar el espacio ' +
        'en el horario que mejor te funcione.'
    },
    7: {
      asunto: 'Última invitación: hablemos de tu contabilidad',
      cuerpo: 'Esta es la última vez que te escribimos por este medio. Si en algún momento quieres retomar la conversación ' +
        'sobre cómo ayudarte con tu contabilidad y tus obligaciones tributarias, con gusto te atendemos. Solo escríbenos ' +
        'por WhatsApp cuando quieras.'
    }
  };
  var contenido = contenidos[dia];

  var cuerpoHtml = '<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">' +
    '<div style="background: #0B0733; padding: 32px 24px; text-align: center;">' +
    '<div style="color: #ffffff; font-size: 20px; font-weight: bold; letter-spacing: 0.5px;">MARÍN RÍOS CONSULTORES</div>' +
    '<div style="color: #8FE3FF; font-size: 12px; margin-top: 4px; letter-spacing: 1px;">ASESORÍA CONTABLE Y TRIBUTARIA</div>' +
    '</div>' +
    '<div style="padding: 32px 28px; background: #ffffff;">' +
    '<p style="font-size: 16px; color: #1a1a1a; margin: 0 0 16px;">' + saludo + '</p>' +
    '<p style="font-size: 15px; line-height: 1.7; color: #1a1a1a; margin: 0 0 24px;">' + contenido.cuerpo + '</p>' +
    '<div style="text-align: center; margin: 0 0 24px;">' +
    '<a href="' + enlaceWhatsapp + '" style="background: #25D366; color: #ffffff; text-decoration: none; padding: 14px 32px; border-radius: 8px; font-weight: bold; font-size: 16px; display: inline-block;">Escribir por WhatsApp</a>' +
    '</div>' +
    '<p style="font-size: 13px; color: #5a6b7d; text-align: center; margin: 0 0 24px;">O escríbenos directo al +' + NUMERO_WHATSAPP + '</p>' +
    '<p style="font-size: 15px; color: #1a1a1a; margin: 24px 0 0;">Con gusto te atendemos,</p>' +
    '<p style="font-size: 15px; color: #1a1a1a; margin: 4px 0 0;"><b>Maribel</b><br><span style="color: #5a6b7d; font-size: 13px;">Directora Administrativa &middot; Marín Ríos Consultores</span></p>' +
    '</div>' +
    '<div style="background: #EAF2FB; padding: 16px 28px; text-align: center;">' +
    '<span style="font-size: 12px; color: #5a6b7d;">Marín Ríos Consultores S.A.S</span>' +
    '</div>' +
    '</div>';

  MailApp.sendEmail({
    to: correo,
    subject: contenido.asunto,
    htmlBody: cuerpoHtml,
    name: 'Marín Ríos Consultores'
  });
}
