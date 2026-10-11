/**
 * Recibe los leads de las landings de marinriosconsultores.com y los agrega
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
