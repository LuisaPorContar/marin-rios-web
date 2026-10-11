/**
 * ESTADOS DE LOS LEADS → META (Conversion Leads)
 * ------------------------------------------------------------------
 * Va en el Apps Script de la hoja "Leads_Consolidado Marin Rios".
 *
 * Cada hora revisa la pestaña "Leads". Cuando alguien cambia el
 * "Estado del lead" de una fila (por ejemplo a "Agendado" o "Cliente"),
 * le avisa a Meta en qué etapa va ese lead. Con eso la campaña aprende a
 * buscar personas parecidas a las que SÍ avanzan, no solo a las que llenan
 * el formulario.
 *
 * - NO modifica la pestaña "Leads": solo la lee.
 * - Lleva su control en una pestaña aparte, "Meta_CRM" (se puede ocultar).
 * - No envía correos a nadie.
 * - Meta usa esta función con leads de formularios de Facebook/Instagram.
 *   Los leads de la web también se envían, pero Meta puede no usarlos para
 *   optimizar.
 *
 * Instalación:
 *   1. Pegar este archivo en el Apps Script del Consolidado y guardar.
 *   2. Configuración del proyecto → Propiedades de la secuencia de comandos:
 *        META_TOKEN = token de la API de conversiones (el mismo del píxel)
 *   3. Ejecutar `probarConexion` (con META_TEST_CODE puesto) y revisar en
 *      Meta → Probar eventos. Luego borrar META_TEST_CODE.
 *   4. Ejecutar `iniciarSeguimiento` UNA vez.
 */

// ==================================================================
// AJUSTES
// ==================================================================
var PESTANA_LEADS = 'Leads';
var PESTANA_CONTROL = 'Meta_CRM';
var ZONA_HORARIA = 'America/Bogota';

var META_PIXEL_ID = '4029344540722147';
var META_VERSION = 'v25.0';   // cada versión dura unos 2 años; revisar cuando Meta avise

// Nombre con el que Meta verá la etapa de un lead que aún no tiene estado
var ETAPA_INICIAL = 'Lead nuevo';

// Estados que NO se envían a Meta (escritos como en la hoja; no importan
// mayúsculas ni tildes). Ejemplo: ['Duplicado', 'Prueba']
var ESTADOS_IGNORADOS = ['Duplicado', 'Prueba'];

// Con qué nombre aparece el origen en Meta
var NOMBRE_CRM = 'Google Sheets';

// Columnas que se leen (por nombre de encabezado)
var COL_ESTADO = 'Estado del lead';
var COL_TELEFONO = 'Teléfono';
var COL_CORREO = 'Correo';
var COL_NOMBRE = 'Nombre';
// Si la hoja tiene el ID del lead de Meta (15 a 17 dígitos), se usa: es el
// dato que mejor identifica al lead. Se busca en cualquiera de estas columnas.
var COLS_ID_META = ['ID_Lead', 'Lead ID', 'ID lead', 'id', 'leadgen_id'];

var LOTE = 50;   // eventos por envío


// ==================================================================
// 1. PUESTA EN MARCHA
// ==================================================================
/**
 * Ejecutar UNA vez.
 * Anota el estado actual de todos los leads SIN enviar nada (para no mandar
 * de golpe todo el historial) y deja programada la revisión cada hora.
 * Desde ese momento se envían los leads nuevos y cada cambio de estado.
 */
function iniciarSeguimiento() {
  var control = hojaControl();
  var datos = leerLeads();
  var enviados = leerControl(control);
  var nuevas = [];
  var ahora = new Date();

  datos.forEach(function (l) {
    if (!l.clave || l.clave in enviados) return;
    enviados[l.clave] = l.estado;
    nuevas.push([l.clave, l.estado, ahora, 'línea base (no enviado)']);
  });
  if (nuevas.length) control.getRange(control.getLastRow() + 1, 1, nuevas.length, 4).setValues(nuevas);

  var existe = ScriptApp.getProjectTriggers().some(function (t) {
    return t.getHandlerFunction() === 'sincronizarEstados';
  });
  if (!existe) ScriptApp.newTrigger('sincronizarEstados').timeBased().everyHours(1).create();

  Logger.log('Listo. Leads anotados como línea base: ' + nuevas.length +
             '. La revisión corre cada hora. Estados que hay hoy en la hoja: ' + resumenEstados(datos));
}

/** Apaga la revisión automática. */
function detenerSeguimiento() {
  var n = 0;
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === 'sincronizarEstados') { ScriptApp.deleteTrigger(t); n++; }
  });
  Logger.log('Disparadores eliminados: ' + n);
}

/** Muestra qué estados existen hoy en la hoja y cuántos leads tiene cada uno. */
function verEstados() {
  Logger.log(resumenEstados(leerLeads()));
}


// ==================================================================
// 2. REVISIÓN (corre sola cada hora)
// ==================================================================
function sincronizarEstados() {
  var token = PropertiesService.getScriptProperties().getProperty('META_TOKEN');
  if (!token) { console.error('Falta META_TOKEN en las propiedades del script.'); return; }

  var bloqueo = LockService.getScriptLock();
  if (!bloqueo.tryLock(5000)) return;   // ya hay otra revisión corriendo
  try {
    var control = hojaControl();
    var enviados = leerControl(control);
    var ignorados = ESTADOS_IGNORADOS.map(normal);
    var ahora = new Date();

    // Leads cuyo estado cambió (o que son nuevos) desde la última revisión
    var pendientes = leerLeads().filter(function (l) {
      if (!l.clave || !l.usuario) return false;
      if (ignorados.indexOf(normal(l.estado)) !== -1) return false;
      return enviados[l.clave] !== l.estado;
    });
    // Una persona repetida en varias filas se envía una sola vez por revisión
    var vistos = {};
    pendientes = pendientes.filter(function (l) {
      if (vistos[l.clave]) return false;
      vistos[l.clave] = true;
      return true;
    });
    if (!pendientes.length) return;

    var registro = [];
    for (var i = 0; i < pendientes.length; i += LOTE) {
      var grupo = pendientes.slice(i, i + LOTE);
      var r = enviarAMetaCRM(grupo, ahora, token);
      grupo.forEach(function (l) {
        // Solo se marca como enviado si Meta lo aceptó; si no, se reintenta
        // en la siguiente hora.
        if (r.ok) registro.push([l.clave, l.estado, ahora, 'enviado']);
      });
      if (!r.ok) console.error('Meta rechazó un envío de ' + grupo.length + ' eventos: ' + r.texto);
    }
    if (registro.length) control.getRange(control.getLastRow() + 1, 1, registro.length, 4).setValues(registro);
    console.log('Estados enviados a Meta: ' + registro.length + ' de ' + pendientes.length);
  } finally {
    bloqueo.releaseLock();
  }
}


// ==================================================================
// 3. ENVÍO A META (formato de "Conversion Leads")
// ==================================================================
// Especificación: developers.facebook.com → Conversions API →
// Conversion Leads Integration → Payload Specification
function enviarAMetaCRM(leads, ahora, token) {
  var cuerpo = {
    data: leads.map(function (l) {
      return {
        event_name: l.estado,                        // la etapa, tal como está en la hoja
        event_time: Math.floor(ahora.getTime() / 1000),
        action_source: 'system_generated',           // obligatorio para eventos de CRM
        user_data: l.usuario,
        custom_data: { event_source: 'crm', lead_event_source: NOMBRE_CRM }
      };
    })
  };
  var prueba = PropertiesService.getScriptProperties().getProperty('META_TEST_CODE');
  if (prueba) cuerpo.test_event_code = prueba;

  var r = UrlFetchApp.fetch(
    'https://graph.facebook.com/' + META_VERSION + '/' + META_PIXEL_ID + '/events?access_token=' + encodeURIComponent(token), {
      method: 'post', contentType: 'application/json',
      payload: JSON.stringify(cuerpo), muteHttpExceptions: true
    });
  return { ok: r.getResponseCode() === 200, texto: r.getResponseCode() + ' ' + r.getContentText().slice(0, 300) };
}

/** Envía un evento de prueba. Usar con META_TEST_CODE en las propiedades. */
function probarConexion() {
  var token = PropertiesService.getScriptProperties().getProperty('META_TOKEN');
  if (!token) { Logger.log('Falta META_TOKEN en las propiedades del script.'); return; }
  var r = enviarAMetaCRM([{
    estado: 'Prueba de conexión',
    usuario: { ph: [sha256('573000000000')], em: [sha256('prueba@ejemplo.com')], country: [sha256('co')] }
  }], new Date(), token);
  Logger.log((r.ok ? 'Meta recibió el evento: ' : 'Meta lo rechazó: ') + r.texto);
}


// ==================================================================
// 4. LECTURA DE LA HOJA
// ==================================================================
function leerLeads() {
  var hoja = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(PESTANA_LEADS);
  if (!hoja) throw new Error('No existe la pestaña "' + PESTANA_LEADS + '"');
  var valores = hoja.getDataRange().getValues();
  if (valores.length < 2) return [];
  var enc = valores[0].map(function (h) { return String(h).trim(); });
  var iEstado = enc.indexOf(COL_ESTADO), iTel = enc.indexOf(COL_TELEFONO),
      iCorreo = enc.indexOf(COL_CORREO), iNombre = enc.indexOf(COL_NOMBRE);
  if (iEstado === -1) throw new Error('No existe la columna "' + COL_ESTADO + '"');
  var iId = -1;
  COLS_ID_META.forEach(function (c) { if (iId === -1) iId = enc.indexOf(c); });

  return valores.slice(1).map(function (f) {
    var tel = iTel === -1 ? '' : telefono(f[iTel]);
    var correo = iCorreo === -1 ? '' : String(f[iCorreo] || '').trim().toLowerCase();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(correo)) correo = '';
    var idMeta = iId === -1 ? '' : String(f[iId] || '').replace(/^l:/i, '').trim();
    if (!/^\d{15,17}$/.test(idMeta)) idMeta = '';

    var usuario = null;
    if (tel || correo || idMeta) {
      usuario = { country: [sha256('co')] };
      if (idMeta) usuario.lead_id = idMeta;          // el ID de Meta va sin cifrar
      if (correo) usuario.em = [sha256(correo)];
      if (tel) usuario.ph = [sha256(tel)];
      var partes = iNombre === -1 ? [] : String(f[iNombre] || '').trim().toLowerCase().replace(/[.,;:'"()\-]/g, '').split(/\s+/).filter(String);
      if (partes.length) usuario.fn = [sha256(partes[0])];
      if (partes.length > 1) usuario.ln = [sha256(partes.slice(1).join(' '))];
    }
    return {
      clave: idMeta || tel || correo,                // identifica a la persona
      estado: String(f[iEstado] || '').trim() || ETAPA_INICIAL,
      usuario: usuario
    };
  });
}

// Teléfono como lo pide Meta: solo dígitos y con indicativo (573001234567)
function telefono(v) {
  var d = String(v || '').replace(/\D/g, '').replace(/^0+/, '');
  if (d.length === 10 && d.charAt(0) === '3') d = '57' + d;
  return d.length >= 10 ? d : '';
}

function resumenEstados(datos) {
  var cuenta = {};
  datos.forEach(function (l) { if (l.clave) cuenta[l.estado] = (cuenta[l.estado] || 0) + 1; });
  return Object.keys(cuenta).sort(function (a, b) { return cuenta[b] - cuenta[a]; })
    .map(function (k) { return k + ' (' + cuenta[k] + ')'; }).join(' · ') || 'ninguno';
}


// ==================================================================
// 5. CONTROL (pestaña "Meta_CRM": qué estado se le envió de cada lead)
// ==================================================================
function hojaControl() {
  var libro = SpreadsheetApp.getActiveSpreadsheet();
  var hoja = libro.getSheetByName(PESTANA_CONTROL);
  if (!hoja) {
    hoja = libro.insertSheet(PESTANA_CONTROL);
    hoja.getRange(1, 1, 1, 4).setValues([['Lead (teléfono, correo o ID)', 'Estado enviado', 'Fecha', 'Resultado']]).setFontWeight('bold');
    hoja.setFrozenRows(1);
    hoja.getRange('A:A').setNumberFormat('@');   // texto, para no perder dígitos
  }
  return hoja;
}

// Devuelve el último estado registrado de cada lead
function leerControl(hoja) {
  var mapa = {};
  var n = hoja.getLastRow();
  if (n < 2) return mapa;
  hoja.getRange(2, 1, n - 1, 2).getValues().forEach(function (f) {
    if (f[0] !== '') mapa[String(f[0])] = String(f[1]);
  });
  return mapa;
}


// ==================================================================
// UTILIDADES
// ==================================================================
function normal(t) {
  return String(t).toLowerCase().trim().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
}

function sha256(t) {
  return Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, String(t), Utilities.Charset.UTF_8)
    .map(function (b) { return ('0' + (b & 0xff).toString(16)).slice(-2); }).join('');
}
