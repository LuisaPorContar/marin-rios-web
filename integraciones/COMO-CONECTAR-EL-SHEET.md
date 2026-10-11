# Cómo conectar el formulario de la web

> **Montaje actual (oct. 2026):** el script NO va dentro del Consolidado.
> Vive en una hoja nueva creada con la cuenta `marketingmarinrios@gmail.com`
> y desde ahí escribe en el Consolidado. Así los correos salen de la cuenta de
> marketing y la cuenta de la agencia no participa.

## Pasos (todo con la sesión de marketingmarinrios@gmail.com)

1. Comparte "Leads_Consolidado Marin Rios" con `marketingmarinrios@gmail.com`
   como **Editor** (si no lo está ya).
2. Con la sesión de marketing (mejor en ventana de incógnito), crea una hoja
   de cálculo nueva: por ejemplo **"Leads web Marín Ríos"**.
3. En esa hoja: **Extensiones → Apps Script**. Borra lo que haya, pega
   `google-sheets-leads.gs` completo y guarda.
4. Ejecuta **`prepararHoja`**. Autoriza los permisos. En el registro debe
   decir que el Consolidado fue encontrado y tiene todas las columnas.
5. Ejecuta **`verRemitente`**: debe decir "Correcto: los correos salen de
   marketingmarinrios@gmail.com".
6. (Meta) En **Configuración del proyecto → Propiedades de la secuencia de
   comandos** agrega `META_TOKEN`. Para probar agrega también
   `META_TEST_CODE`, ejecuta `probarMeta` y luego **borra `META_TEST_CODE`**.
7. **Implementar → Nueva implementación → Aplicación web** · Ejecutar como:
   **Yo** · Quién tiene acceso: **Cualquier usuario** → Implementar.
8. Copia la URL que termina en `/exec` y pásala para conectarla en la landing
   (`SHEETS_URL` en `constructor/paginas_meta.py`).

Cada lead queda en dos lugares: la pestaña "Leads" de la hoja nueva (respaldo)
y la pestaña "Leads" del Consolidado. Si el Consolidado falla, el lead no se
pierde: queda en el respaldo y el error aparece en **Ejecuciones**.

El script anterior del Consolidado (secuencia de recuperación) ya no se usa:
en el editor del Consolidado, abre **Activadores** (reloj) y borra el de
`procesarRecuperacion`.

---

## Correos que envía el script

| Correo | A quién | Cuándo |
|---|---|---|
| Aviso de lead premium | Juan David (`AVISAR_PREMIUM_A`), con copia a Maribel | Lead de revisoría fiscal que califica |
| Aviso de lead nuevo | Maribel (`AVISAR_A`) | Cualquier otro lead |
| Bienvenida | Al cliente | Siempre, califique o no (texto distinto en cada caso) |

A Meta (CAPI) solo se envían los leads que califican.

**De dónde salen:** de `marketingmarinrios@gmail.com`, porque esa cuenta es la
que crea la hoja y publica el script. Las respuestas del cliente a la
bienvenida llegan a `RESPONDER_A` (Maribel).

Ajustes al inicio del script:

- `AVISAR_A`: correo de quien recibe los avisos (varios separados por coma).
  Vacío = le llegan a la cuenta dueña del script.
- `RESPONDER_A`: a dónde llegan las respuestas del cliente a la bienvenida.
- `CORREO_ACTIVO`: `false` apaga la bienvenida (el aviso al equipo sigue).

Pruebas desde el editor: `probarAviso` y `probarBienvenida`.

Límite de Google: unos 100 correos al día en cuentas Gmail gratuitas.

## Si cambias el script

Después de editarlo: **Implementar → Administrar implementaciones → editar
(lápiz) → Versión: Nueva versión → Implementar**. La URL no cambia.
