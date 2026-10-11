# Estados de los leads → Meta (Conversion Leads)

Script: `consolidado-estados-meta.gs`. Va en el Apps Script del **Consolidado**
(no en la hoja de marketing).

## Qué hace

Cada hora lee la pestaña "Leads". Cuando cambia el **Estado del lead** de una
fila, o aparece un lead nuevo, le envía a Meta la etapa en la que va ese lead.
El nombre de la etapa es el texto que está en la hoja, tal cual. Un lead sin
estado se envía como "Lead nuevo".

- No modifica la pestaña "Leads".
- Crea una pestaña "Meta_CRM" con lo que ya envió (se puede ocultar; no borrar).
- No envía correos.
- Identifica a cada persona por su teléfono y su correo cifrados. Si la hoja
  tuviera el ID del lead de Meta (15 a 17 dígitos), lo usa.

## Límite que pone Meta

Meta indica que esta optimización funciona con leads de **formularios nativos
de Facebook e Instagram**. Sirve para los leads de pauta del Consolidado. Los
de la web y los orgánicos también se envían, pero Meta puede no usarlos.

## Instalación

1. En el Consolidado: Extensiones → Apps Script → pegar el archivo → Guardar.
2. Configuración del proyecto → Propiedades de la secuencia de comandos →
   `META_TOKEN` (el mismo token del píxel).
3. Agregar `META_TEST_CODE` con el código de *Probar eventos*, ejecutar
   `probarConexion` y confirmar en Meta que llegó. **Borrar `META_TEST_CODE`.**
4. Ejecutar `verEstados` para ver qué estados hay hoy en la hoja.
5. Ajustar `ESTADOS_IGNORADOS` si hay estados que no deben ir a Meta.
6. Ejecutar `iniciarSeguimiento` **una vez**. Anota el estado actual de todos
   los leads sin enviar nada y programa la revisión cada hora.

Quien ejecute `iniciarSeguimiento` es la cuenta con la que corre la revisión.
Este script no envía correos, así que no aparece ningún remitente.

## Después, en Meta

1. Administrador de eventos → el conjunto de datos → verificar que llegan
   eventos con origen "CRM".
2. Cuando Meta valide los datos, **configurar el embudo**: ordenar las etapas
   (por ejemplo Lead nuevo → Contactado → Agendado → Cliente) y marcar cuáles
   son positivas.
3. En la campaña de formularios, elegir como objetivo de rendimiento
   **"Maximizar el número de clientes potenciales de conversión"** y la etapa
   a optimizar (la más temprana que indique un lead bueno).

Para que sirva, el equipo debe mantener el "Estado del lead" al día y escribir
los estados siempre igual.

## Apagarlo

Ejecutar `detenerSeguimiento`.
