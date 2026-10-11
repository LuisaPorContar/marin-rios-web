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

## Meta: píxel y API de conversiones (CAPI)

El píxel `4029344540722147` ya está instalado en todo el sitio. Eventos:

| Evento | Cuándo se envía | Por dónde |
|---|---|---|
| PageView | Cada página | Píxel |
| ViewContent | Al abrir la landing | Píxel |
| Contact | Clic en WhatsApp o en llamar (todo el sitio) | Píxel |
| Lead | Formulario enviado por una empresa que califica | Píxel (página de gracias) **y** CAPI (este script) |
| LeadNoCalificado | Formulario de una empresa pequeña | Píxel (evento personalizado) |

El Lead viaja por los dos caminos con el mismo `event_id`, así Meta lo cuenta
una sola vez aunque el navegador bloquee el píxel.

### Activar el CAPI

1. En el Administrador de eventos de Meta: **Configuración → API de
   conversiones → Generar token de acceso**. Copia el token.
2. En el editor de Apps Script: **Configuración del proyecto** (engranaje) →
   **Propiedades de la secuencia de comandos → Agregar propiedad**:
   - Propiedad `META_TOKEN`, valor: el token.
3. Para probar: en Meta abre **Probar eventos**, copia el código (`TEST12345`)
   y agrégalo como propiedad `META_TEST_CODE`. En el editor ejecuta la función
   `probarMeta`. El evento debe aparecer en *Probar eventos* como "Servidor".
4. Cuando funcione, **borra `META_TEST_CODE`** (si se queda, los leads reales
   llegan como prueba y no cuentan).
5. Publica una versión nueva del script (ver abajo).

El token no se escribe en el código ni se sube a GitHub: solo vive en las
propiedades del script.

### En los anuncios

- URL del anuncio con UTM, por ejemplo:
  `?utm_source=meta&utm_medium=paid&utm_campaign={{adset.name}}&utm_content={{ad.name}}`
  Así la columna *Conjunto de anuncios* se llena sola.
- Optimiza la campaña por el evento **Lead** (Cliente potencial).

## Correo de bienvenida

Al recibir un formulario con correo, el script envía **un solo correo** de
bienvenida (texto distinto si la empresa califica o no). Ya no existe la
secuencia de recuperación de día 1, 3 y 7.

- Para ver cómo queda: ejecuta `probarBienvenida` (te llega a tu propia cuenta).
- Para apagarlo: cambia `CORREO_ACTIVO` a `false` al inicio del script.
- Si antes estaba la secuencia de recuperación: ejecuta **una vez**
  `quitarTriggerRecuperacion` para borrar el disparador diario. Si no, Google
  enviará un correo de error cada mañana.
- La primera vez Google pedirá permiso para enviar correos en tu nombre.

## Si cambias el script

Después de editarlo: **Implementar → Administrar implementaciones → editar
(lápiz) → Versión: Nueva versión → Implementar**. La URL no cambia.
