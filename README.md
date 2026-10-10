# marinriosconsultores.com

Sitio estático de **Marín Ríos Consultores**, generado con un constructor
propio en Python. Reemplaza al WordPress que estaba en el mismo dominio,
conservando exactamente las mismas URLs.

**60 páginas** · 9,2 MB · sin base de datos, sin PHP, sin plugins.

---

## Cómo se trabaja

Nunca se editan los archivos de `sitio/`: los sobrescribe la siguiente
compilación. Todo el contenido vive en `constructor/`.

```bash
cd constructor
python generar.py     # construye el sitio en ../sitio
python revisar.py     # valida enlaces y SEO: debe dar 0 y 0
```

`revisar.py` es la red de seguridad. Si dice algo distinto de **0 enlaces rotos
y 0 páginas con observaciones**, no se publica.

---

## Estructura

```
constructor/          el código que genera el sitio
  base.py               plantilla, cabecera, pie, analítica
  paginas.py            páginas de servicio
  paginas2.py           planes (/precios-outsourcing-contable/), blog y ciudades
  paginas_home.py       portada
  paginas3.py           contacto, nosotros, política de privacidad
  paginas_landings.py   landings de campaña y páginas de gracias
  paginas_404.py        página de error
  articulos_paginas.py  los 41 artículos del blog
  articulos_cuerpo.json el contenido de los artículos, ya migrado
  generar.py            arma todo y escribe sitemap y robots
  revisar.py            valida el resultado

sitio/                el resultado publicable (se sube tal cual al hosting)
COMO-PUBLICAR.md      pasos para desplegar en Hostinger
```

---

## Tres decisiones que conviene no romper

**1. Las páginas se publican en carpetas.** Cada una es `slug/index.html`, para
que su URL sea `/slug/` — idéntica a la que tenía en el WordPress. Por eso la
migración no necesitó redirecciones ni perdió posicionamiento.

Como consecuencia, **todos los enlaces internos son absolutos**. De eso se
encarga `base.enlaces_absolutos()` al final de cada página, así que los módulos
pueden seguir escribiendo `blog.html` con naturalidad.

**2. El sitio no publica precios.** Desde octubre de 2026 todos los servicios
se cotizan a la medida: no hay tarifas en pesos ni en SMMLV en las páginas, en
las meta descripciones ni en los datos estructurados (schema sin `price`).
La página `/precios-outsourcing-contable/` conserva su URL por posicionamiento,
pero ahora explica qué define el valor y aparece en el menú como "Planes".
Las cifras de SMMLV que quedan en el sitio son topes legales o datos de los
artículos, no tarifas de la firma.

**3. Las imágenes se sirven en WebP.** Los módulos las nombran `.jpg` o `.png`
porque se leen mejor; `base.imagenes_webp()` hace la traducción al final. Los
originales están fuera del repositorio, en `originales-img/`.

---

## Dos trampas que ya costaron tiempo

**La clase `revelar` no va en elementos altos.** El observador de `main.js`
exige ver el 14% del área del elemento para mostrarlo. El cuerpo de un artículo
mide unos 8.700 px: en una pantalla normal nunca se alcanza ese umbral, así que
se queda invisible para siempre.

**La rejilla `.entrada` solo lleva dos columnas con índice.** Si la página no
genera tabla de contenidos, hay que omitir la clase `entrada--con-toc`; de lo
contrario el texto cae en la columna estrecha del índice y queda encajonado.

---

## Pendientes

- **La política de privacidad necesita revisión legal.** El WordPress la tenía
  vacía; se redactó siguiendo la Ley 1581 de 2012, pero las finalidades y el
  plazo de conservación los debe confirmar un abogado.
- **El formulario de `/vcl/` no guarda los datos.** Compone un mensaje de
  WhatsApp con las respuestas, así que el lead llega completo, pero no queda
  registrado en ninguna parte. Para eso hace falta un backend.
