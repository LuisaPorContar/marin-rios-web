# -*- coding: utf-8 -*-
"""
Página 404.

El servidor la sirve desde la raíz (`/404.html`), así que se genera ahí y no
en una carpeta. Sus enlaces son absolutos, como los del resto del sitio, para
que funcione sin importar desde qué ruta la invoque el visitante.
"""

from base import ICO, wa, heroe, encabezado, cta_final
from paginas import PAGINAS

cuerpo_404 = f"""
{heroe(
    "Esta página ya no existe",
    "Puede que el enlace haya cambiado o que la dirección tenga un error de escritura. Desde aquí puedes seguir a lo que buscabas.",
    "reunion-duotono.jpg",
    "Equipo de Marín Ríos Consultores",
    chip="Error 404",
    cta1=("Ir a la portada", "index.html"),
    cta2=("Ver el blog", "blog.html"),
)}

<section class="seccion--ajustada">
  <div class="contenedor">
    {encabezado("Atajos", "Lo que más buscan quienes llegan aquí")}
    <div class="rejilla-3 rejilla-movil revelar">
      <article class="tarjeta-item">
        <div class="tarjeta-item__icono">{ICO['documento']}</div>
        <h3>Outsourcing contable</h3>
        <p>Toda la operación contable, tributaria y de nómina de tu empresa.</p>
        <p><a class="etiqueta-enlace" href="outsourcing-contable.html">Ver el servicio{ICO['flecha_fina']}</a></p>
      </article>
      <article class="tarjeta-item">
        <div class="tarjeta-item__icono">{ICO['tarjeta']}</div>
        <h3>Planes</h3>
        <p>Qué determina el valor del servicio y cómo lo cotizamos.</p>
        <p><a class="etiqueta-enlace" href="/cuanto-cuesta-contratar-un-servicio-de-outsourcing-contable/#planes">Ver planes{ICO['flecha_fina']}</a></p>
      </article>
      <article class="tarjeta-item">
        <div class="tarjeta-item__icono">{ICO['libro']}</div>
        <h3>Blog</h3>
        <p>Impuestos, revisoría fiscal y finanzas, explicados sin tecnicismos.</p>
        <p><a class="etiqueta-enlace" href="blog.html">Leer el blog{ICO['flecha_fina']}</a></p>
      </article>
    </div>
  </div>
</section>

{cta_final(
    "¿Buscabas algo puntual?",
    "Escríbenos qué necesitabas encontrar y te lo mandamos directo.",
    boton="Escríbenos",
    mensaje="Hola, buscaba algo en su sitio y no lo encontré",
)}
"""

PAGINAS.append(dict(
    archivo="404.html",
    titulo="Página no encontrada | Marín Ríos Consultores",
    descripcion="La página que buscabas no existe o cambió de dirección.",
    activo="",
    og_img="reunion-duotono.jpg",
    robots="noindex, follow",
    schema="",
    cuerpo=cuerpo_404,
))
