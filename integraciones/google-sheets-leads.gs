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
    return respuesta({ ok: true });
  } finally {
    bloqueo.releaseLock();
  }
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
