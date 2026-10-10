# Cómo publicar el sitio en Hostinger

El sitio son archivos estáticos: no necesita PHP, ni base de datos, ni plugins.
Hostinger corre **LiteSpeed**, que lee el `.htaccess` incluido, así que no hay
nada que configurar por fuera.

---

## Lista de verificación del día del cambio

Imprímela o tenla al lado. El orden importa: cada bloque supone que el anterior
quedó hecho. Solo el paso 8 es irreversible.

**Antes de tocar nada**

- [ ] 1. Copia de seguridad del WordPress desde hPanel (**Tablero → Archivos → Copias de seguridad → Restaurar y descargar**), descargada al computador.
- [ ] 2. Export de la base de datos desde **phpMyAdmin → Exportar → Continuar**, guardado junto a la copia anterior.
- [ ] 3. *Backup Now* desde el plugin Backuply, como red extra.
- [ ] 4. Anotar los registros DNS actuales: en hPanel, **Dominios → Zona DNS**, y capturar la pantalla completa. Sirve de prueba si algo se toca por accidente.

**Generar el paquete**

- [ ] 5. `python generar.py` desde `constructor/` → debe escribir 60 páginas.
- [ ] 6. `python revisar.py` → tiene que decir **0 enlaces rotos** y **0/60 páginas con observaciones**. Si sale cualquier otra cosa, no se sube.
- [ ] 7. Rearmar `marinrios-sitio.zip` con el contenido de `sitio/` en la raíz del zip.

**Publicar** *(a partir de aquí el sitio viejo deja de existir)*

- [ ] 8. Vaciar `public_html` por completo, incluido el `.htaccess` del WordPress. **Nada de esto toca el correo:** los buzones de Outlook viven en los registros MX del DNS, no en el hosting.
- [ ] 9. Subir el zip a `public_html` y extraerlo ahí mismo.
- [ ] 10. Borrar el `.zip` del servidor.
- [ ] 11. Confirmar que el `.htaccess` nuevo quedó (**Configuración → Mostrar archivos ocultos**).
- [ ] 12. Purgar la caché del CDN en hPanel (**Rendimiento → Caché** o **CDN → Purgar caché**). El dominio pasa por `cdn.hstgr.net`: sin esto, hay visitantes que van a seguir viendo el WordPress un rato.

**Comprobar en el navegador** *(siempre con Ctrl+Shift+R)*

- [ ] 13. `https://marinriosconsultores.com/` → la portada nueva.
- [ ] 14. `https://marinriosconsultores.com/blog/` → el listado con los 41 artículos.
- [ ] 15. `https://marinriosconsultores.com/niif-para-pymes-colombia/` → un artículo, con la firma «Por Juan David Marín Ríos» arriba y la tarjeta «Sobre el autor» al final.
- [ ] 16. `https://marinriosconsultores.com/precios-outsourcing-contable/` → la página de planes, sin ninguna cifra de precio.
- [ ] 17. `https://marinriosconsultores.com/pagina-que-no-existe/` → la página 404 propia.
- [ ] 18. `http://marinriosconsultores.com` → debe saltar a `https://`.
- [ ] 19. `https://www.marinriosconsultores.com/` → debe quitar el `www`.
- [ ] 20. `https://marinriosconsultores.com/home/` → debe redirigir a la portada.
- [ ] 21. `https://marinriosconsultores.com/sitemap_index.xml` → debe redirigir a `/sitemap.xml`.
- [ ] 22. Abrir la portada **en el celular** y bajar hasta el pie.
- [ ] 23. F12 → pestaña **Red** → recargar: que no haya ningún 404 en imágenes, CSS ni JS.

**Confirmar que el correo sigue vivo**

- [ ] 24. Enviar un correo **desde** `j@marinriosconsultores.com` a un Gmail personal.
- [ ] 25. Responder desde ese Gmail y confirmar que **llega** al buzón de Outlook.
- [ ] 26. En hPanel, **Dominios → Zona DNS**: confirmar que el MX sigue siendo `marinriosconsultores-com.mail.protection.outlook.com`. Si cambió, restaurarlo con la captura del paso 4.

**Avisar a Google** *(el mismo día, no después)*

- [ ] 27. Search Console → **Sitemaps** → borrar los sitemaps viejos (`sitemap_index.xml`, `post-sitemap.xml`, `page-sitemap.xml`) y enviar `sitemap.xml`.
- [ ] 28. **Inspección de URLs** → pedir indexación de la portada `/`.
- [ ] 29. Ídem para `/outsourcing-contable/`, `/revisoria-fiscal/` y `/consultoria-financiera/`.
- [ ] 30. Ídem para `/blog/`.
- [ ] 31. En **Prueba de resultados enriquecidos** (search.google.com/test/rich-results), pegar la URL de un artículo y confirmar que detecta *BlogPosting* con autor **Juan David Marín Ríos**.

**Las dos semanas siguientes**

- [ ] 32. Revisar **Páginas → No indexadas** en Search Console cada 3 o 4 días: ahí saldría cualquier URL que se hubiera roto.
- [ ] 33. Revisar **Rendimiento** al cabo de 14 días y comparar con las dos semanas previas al cambio.

> **Sobre la caída de impresiones:** es normal ver un bajón de 1 a 2 semanas
> mientras Google vuelve a rastrear el sitio, incluso cuando todo está bien
> hecho. Las 56 URLs que el WordPress tenía indexadas existen las 56 en el sitio
> nuevo, con la misma dirección, así que se recupera solo. Lo que **no** es
> normal es que suban las URLs en «No indexadas» o que aparezcan errores de
> rastreo: eso sí hay que mirarlo.

---

## Ojo: son dos paneles distintos

Casi todo este proceso ocurre en **hPanel**, no en WordPress. Se confunden con
facilidad porque los dos son «el panel de la web»:

| Panel | Qué es | Cómo se entra |
|---|---|---|
| **WordPress** | Donde se escriben páginas y se manejan plugins | `marinriosconsultores.com/wp-admin` |
| **hPanel de Hostinger** | El servidor: archivos, copias, bases de datos | `hpanel.hostinger.com` |

Son cuentas separadas: el usuario de WordPress no sirve para entrar a
Hostinger. Para hPanel se usa el correo con el que se contrató el hosting.

Piénsalo así: WordPress es el inquilino, Hostinger es el edificio. Vamos a
cambiar de inquilino, así que hay que entrar por la portería.

---

## Antes de empezar — la copia de seguridad

**Haz una copia del WordPress actual.** Es lo único irreversible de todo el
proceso.

### En hPanel (la que de verdad respalda)

1. Entra a **hpanel.hostinger.com** con la cuenta de Hostinger.
2. En la lista de sitios, busca la fila de `marinriosconsultores.com` y haz clic
   en **Tablero** (el botón de la derecha, no el de «Herramientas»).
3. Ya dentro, en el **menú izquierdo**: **Archivos → Copias de seguridad**.
4. Pestaña **Restaurar y descargar** → busca el respaldo automático más reciente
   y **descárgalo**.
5. **Bases de datos → phpMyAdmin** → elige la base del sitio → pestaña
   **Exportar** → **Continuar**. Se baja un archivo `.sql`.

> **El plan Premium no permite copias manuales.** El botón «Backups manuales»
> aparece bloqueado y ofrece mejorar el plan: no hace falta pagarlo. Hostinger
> guarda un respaldo **automático semanal**, y ese sirve.
>
> Como ese respaldo puede tener hasta siete días, complétalo con el plugin
> **Backuply** desde WordPress (**Backup Now**), que captura el estado de hoy.
>
> Además, el propio panel avisa de que las copias **excluyen la caché y los
> archivos de exportación de la base de datos**. Por eso el paso 5, el export
> desde phpMyAdmin, no es opcional: es la única garantía de tener la base
> completa.

> Los tres botones de cada fila hacen cosas distintas:
> **Herramientas** son tres atajos sueltos, **Admin WordPress** abre el
> WordPress, y **Tablero** abre el panel completo del sitio. Las copias de
> seguridad solo aparecen entrando por **Tablero**.
>
> El menú de los tres puntos (⋮) es para transferir, renombrar o **borrar el
> sitio entero**. Ese no hace falta tocarlo en ningún paso.

Guarda las dos cosas en tu computador antes de tocar nada.

### Atajo desde WordPress (complemento, no sustituto)

El sitio tiene el plugin **Backuply** instalado: en el escritorio de WordPress
aparece un botón **Backup Now**. Es más rápido y no está de más hacerlo.

Pero no reemplaza la copia de hPanel: Backuply vive *dentro* del WordPress que
vas a borrar. Si algo falla ahí, te quedas sin la herramienta y sin la copia.

Lo ideal es hacer las dos: primero el Backup Now, después la de hPanel.

---

## Paso 1 — Generar el paquete

Desde `constructor/`:

```
python generar.py     # construye el sitio en sitio/
python revisar.py     # debe decir 0 enlaces rotos y 0 observaciones
```

Luego se arma el `.zip`. El archivo ya generado está en la raíz del proyecto:
**`marinrios-sitio.zip`** (7,8 MB, 173 archivos).

Dentro, el contenido va en la raíz del zip: al descomprimirlo, `index.html`
queda directamente en `public_html`.

---

## Paso 2 — Vaciar `public_html`

En **hPanel** (no en WordPress), en la fila de `marinriosconsultores.com`:
**Herramientas → Administrador de archivos**. También llegas desde
**Tablero → Archivos → Administrador de archivos**.

Una vez dentro, entra a la carpeta `public_html`.

Borra todo lo que hay (es el WordPress: `wp-admin`, `wp-content`,
`wp-includes`, `index.php`, `wp-config.php`, el `.htaccess` viejo…).

> **Importante:** el `.htaccess` del WordPress redirige todo a `index.php`.
> Si se queda, el sitio nuevo no funciona.

Si prefieres no borrar de una: renombra `public_html` a `public_html_wp` y crea
uno nuevo vacío. Ocupa el doble de espacio pero permite volver atrás en un clic.

---

## Paso 3 — Subir

En el Administrador de archivos, dentro de `public_html`:

1. Botón **Subir archivos** → elige `marinrios-sitio.zip`.
2. Cuando termine, clic derecho sobre el zip → **Extraer**.
3. Borra el `.zip` del servidor.

Debe quedar así:

```
public_html/
  index.html
  404.html
  .htaccess
  sitemap.xml
  robots.txt
  assets/
  blog/
  outsourcing-contable/
  ... (una carpeta por página)
```

> Si el Administrador de archivos no muestra el `.htaccess`, activa
> **Configuración → Mostrar archivos ocultos**.

---

## Paso 4 — Comprobar

Revisa en el navegador, con el caché desactivado (Ctrl+Shift+R):

- `https://marinriosconsultores.com/` → la portada
- `https://marinriosconsultores.com/blog/` → el listado
- `https://marinriosconsultores.com/niif-para-pymes-colombia/` → un artículo
- `https://marinriosconsultores.com/pagina-que-no-existe/` → la página 404
- `http://marinriosconsultores.com` → debe saltar a `https://`
- `https://www.marinriosconsultores.com/` → debe quitar el `www`

Y con las herramientas de desarrollador (F12 → Red), confirma que no haya
ningún 404 en imágenes ni en CSS.

---

## Paso 5 — Avisar a Google

Corresponde a los puntos 27 a 33 de la lista de arriba.

1. **Search Console** → propiedad de marinriosconsultores.com → **Sitemaps**.
   Elimina los sitemaps de Rank Math (`sitemap_index.xml`, `post-sitemap.xml`,
   `page-sitemap.xml`) y envía `sitemap.xml`.
2. **Inspección de URLs** → pide indexación de `/`, `/blog/`,
   `/outsourcing-contable/`, `/revisoria-fiscal/` y `/consultoria-financiera/`.
   Son las cinco que más tráfico traen; el resto lo encuentra por el sitemap.
3. Durante las dos primeras semanas, vigila **Páginas → No indexadas**: ahí
   aparecería cualquier URL que se hubiera roto.

Las 56 URLs que el WordPress tenía indexadas existen todas en el sitio nuevo,
con exactamente la misma dirección. Las redirecciones que sí hicieron falta ya
están en el `.htaccess` (ver la tabla de abajo), así que no debería haber caída
de posiciones más allá del bajón normal de rastreo.

### Comprobar el autor en los datos estructurados

Los 41 artículos declaran a Juan David Marín Ríos como `Person` autor, con
`sameAs` a su LinkedIn. Para confirmarlo, pega la URL de cualquier artículo en
**search.google.com/test/rich-results**: debe detectar `BlogPosting` y mostrar
el autor con nombre propio, no la empresa.

---

## El correo de Outlook no se ve afectado

Vale la pena tenerlo claro antes de borrar nada, porque es la duda que más
angustia da el día del cambio.

Los buzones `@marinriosconsultores.com` están en **Microsoft 365**, y lo que los
hace funcionar son registros del **DNS**, no archivos del hosting:

| Registro | Valor | Qué hace |
|---|---|---|
| `MX` | `marinriosconsultores-com.mail.protection.outlook.com` | Dice a dónde entregar el correo entrante |
| `TXT` (SPF) | `v=spf1 include:spf.protection.outlook.com include:_spf.google.com ~all` | Autoriza a quién puede enviar en nombre del dominio |
| `CNAME` autodiscover | `autodiscover.outlook.com` | Configura Outlook solo, sin poner servidores a mano |

Vaciar `public_html` y subir el sitio nuevo **no toca ninguno de los tres**. El
WordPress nunca manejó ese correo.

Lo único que sí lo tumbaría, y por eso no se hace: cambiar los *nameservers*, o
usar el asistente de **«conectar dominio» / «restablecer zona DNS»** de hPanel,
que reescribe la zona entera y se lleva los MX por delante. Por eso el punto 4
de la lista es capturar la zona DNS antes de empezar: si alguien la toca por
error, se restaura en dos minutos.

> **Aparte, para otro día:** el dominio no tiene **DMARC** ni **DKIM** de
> Microsoft configurados. No afecta al cambio de sitio, pero hace que los
> correos que salen tengan más probabilidad de caer en spam. Se arregla en el
> panel de Microsoft 365 más tres registros en Hostinger.

---

## Qué hace el `.htaccess`

| Regla | Para qué |
|---|---|
| `DirectoryIndex index.html` | Que `/slug/` sirva `slug/index.html` |
| `ErrorDocument 404 /404.html` | Página de error propia, no la genérica del servidor |
| Redirección a `https://` sin `www` | Una sola dirección canónica |
| `/contacto` → `/contactenos/` | Enlace que estaba roto en el WordPress |
| `/costos-de-outsourcing-contable/` → `/precios-outsourcing-contable/` | Ídem |
| `/home/` → `/` | Era un duplicado de la portada, indexado. El 301 traslada su autoridad en vez de tirarla |
| `sitemap_index.xml` y `post/page-sitemap.xml` → `/sitemap.xml` | Los sitemaps de Rank Math están registrados en Search Console: sin esto darían 404 |
| `/slug` → `/slug/` | Que la página no exista en dos direcciones |
| `/slug/index.html` → `/slug/` | Ídem |
| Caché de un año para imágenes y tipografías | Velocidad en visitas repetidas |
| HTML sin caché | Que un cambio de contenido se vea enseguida |

---

## Para actualizar el sitio más adelante

1. Edita lo que corresponda en `constructor/`.
2. `python generar.py` y `python revisar.py`.
3. Vuelve a armar el zip y repite los pasos 2 y 3 — o sube solo las carpetas
   que cambiaron, si es un ajuste puntual.

**No edites los archivos de `sitio/` directamente:** la siguiente compilación
los sobrescribe.

---

## Dos cosas que quedan pendientes

- **La política de privacidad necesita revisión legal.** El WordPress la tenía
  vacía; se redactó con la estructura de la Ley 1581 de 2012, pero las
  finalidades y el plazo de conservación los debe confirmar un abogado.
- **El formulario de `/vcl/` no guarda los datos en ninguna parte.** Compone un
  mensaje de WhatsApp con las respuestas, así que el lead llega completo, pero
  no queda registrado. Para eso hace falta un backend.
