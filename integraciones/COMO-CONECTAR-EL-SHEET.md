# Cómo conectar el formulario de la landing con el Google Sheet

La landing `/evaluacion-revisoria-fiscal/` envía cada lead a la pestaña
**Leads** de la hoja **Leads_Consolidado Marin Rios**. El puente es un Apps
Script que vive dentro de la hoja. Se configura una sola vez (unos 5 minutos).

## 1. Pegar el script en la hoja

1. Abre la hoja *Leads_Consolidado Marin Rios* con la cuenta dueña.
2. Menú **Extensiones → Apps Script**.
3. Borra lo que haya en `Código.gs` y pega todo el contenido de
   `google-sheets-leads.gs` (está en esta misma carpeta).
4. Guarda (ícono de disquete).

## 2. Publicarlo como aplicación web

1. Botón azul **Implementar → Nueva implementación**.
2. En *Tipo*, el engranaje → **Aplicación web**.
3. Configura:
   - **Ejecutar como:** Yo (tu cuenta)
   - **Quién tiene acceso:** Cualquier persona
4. **Implementar**. Google pide autorizar: acepta con tu cuenta
   (aparece "Google no verificó esta app" → *Configuración avanzada* →
   *Ir a … (no seguro)* → *Permitir*. Es normal: el script es tuyo).
5. Copia la **URL de la aplicación web** (termina en `/exec`).

Para comprobarla, ábrela en el navegador: debe mostrar
`{"ok":true,"servicio":"leads marinriosconsultores.com"}`.

## 3. Ponerla en la landing

1. Abre `constructor/paginas_meta.py`.
2. Pega la URL en `SHEETS_URL = ""`, entre las comillas.
3. Regenera: `python generar.py` y `python revisar.py` desde `constructor/`.
4. Sube a Hostinger la carpeta `evaluacion-revisoria-fiscal/` y el archivo
   `assets/js/lp-revisoria.js` (y `assets/css/lp-revisoria.css` la primera vez).

## Qué llega a la hoja

Cada envío agrega una fila en **Leads** con:

| Columna | Valor |
|---|---|
| Mes / Fecha | Mes y fecha del envío (hora de Bogotá) |
| Nombre, Teléfono, Empresa | Lo que escribió el lead (teléfono con +57) |
| Tipo de persona | Persona jurídica (empresa) |
| Rango de ventas | Ingresos anuales que eligió |
| Conjunto de anuncios | `utm_campaign` del anuncio de Meta |
| Formulario | Landing Revisoría Fiscal 2027 |
| Notas | Cargo, ciudad, revisor actual, si califica y la fuente |
| ID_Lead | RF27-fecha-hora |
| Visible | 1 (para que cuente en el Dashboard) |

**Estado del lead** queda vacío para que el equipo lo califique.

## Importante para Meta

- En los anuncios, usa parámetros UTM en la URL, por ejemplo:
  `?utm_source=meta&utm_medium=paid&utm_campaign={{adset.name}}&utm_content={{ad.name}}`
  Así la columna *Conjunto de anuncios* se llena sola.
- Al enviar el formulario, la página manda a Google Tag Manager el evento
  `lead_revisoria_2027` (con `lead_calificado` = true/false). En GTM, crea un
  activador de *Evento personalizado* con ese nombre y conéctalo a la etiqueta
  del píxel de Meta (`Lead`). Si quieres optimizar solo por leads que califican,
  agrega la condición `lead_calificado` igual a `true`.

## Si cambias el script

Después de editarlo: **Implementar → Administrar implementaciones → editar
(lápiz) → Versión: Nueva versión → Implementar**. La URL no cambia.
