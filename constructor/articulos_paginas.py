# -*- coding: utf-8 -*-
"""
Páginas de artículo del blog.

El contenido vive en `articulos_cuerpo.json`, migrado desde el WordPress:
cada artículo trae sus bloques ya en orden (encabezados, párrafos, listas,
tablas, imágenes y preguntas frecuentes), con las imágenes alojadas en
`assets/img/blog/` y los enlaces internos apuntando al sitio estático.
"""

import json
import os
import re
from html import escape

from base import (ICO, wa, heroe, encabezado, servicios_num, acordeon, cta_final,
                  tarjeta_autor, nodo_autor, recortar, AUTOR_NOMBRE, AUTOR_ID)
from paginas import PAGINAS, TRIO

AQUI = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(AQUI, "articulos_cuerpo.json"), encoding="utf-8") as f:
    ARTICULOS_CUERPO = json.load(f)

# Foto de cabecera según el tema del artículo, para que la portada no se repita siempre.
FOTO_CATEGORIA = {
    "Revisoría fiscal": ("detalle-documentos.jpg", "Documentos contables sobre el escritorio de una revisoría fiscal"),
    "Impuestos y normativa": ("reunion-ancho.jpg", "Equipo de Marín Ríos Consultores revisando obligaciones tributarias"),
    "Finanzas": ("equipo-ancho.jpg", "Equipo de Marín Ríos Consultores analizando indicadores financieros"),
    "Outsourcing contable": ("reunion-duotono.jpg", "Reunión de trabajo del equipo contable de Marín Ríos Consultores"),
}

MENSAJE_WA = "Hola, vengo del artículo «{}» y quiero agendar una asesoría"


def categoria(slug):
    """Misma clasificación que usa el listado del blog."""
    if re.search(r"revisor|revisoria|auditor", slug):
        return "Revisoría fiscal"
    if re.search(r"impuesto|tributar|dian|retencion|exogena|regimen|salario|nomina|niif|calendario|decreto|ley-|4x1000", slug):
        return "Impuestos y normativa"
    if re.search(r"financier|rentab|deuda|credito|factoring|presupuesto|balance|escalar|llaves|volatil|inflacion|tasas", slug):
        return "Finanzas"
    return "Outsourcing contable"


# Página de servicio que encabeza cada categoría: va en las migas y en el botón secundario del cierre.
PILAR_DE = {
    "Revisoría fiscal": ("Revisoría fiscal", "revisoria-fiscal.html"),
    "Outsourcing contable": ("Outsourcing contable", "outsourcing-contable.html"),
    "Finanzas": ("Consultoría financiera", "consultoria-financiera.html"),
}
SECUNDARIO_DE = {
    "Revisoría fiscal": ("Cotiza tu revisoría fiscal", "cotizacion-revisoria-fiscal.html"),
    "Finanzas": ("Conoce la consultoría financiera", "consultoria-financiera.html"),
}


def fecha_larga(iso):
    meses = ("enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
             "agosto", "septiembre", "octubre", "noviembre", "diciembre")
    try:
        a, m, d = iso.split("-")
        return f"{int(d)} de {meses[int(m) - 1]} de {a}"
    except (ValueError, IndexError):
        return iso


# ---------------------------------------------------------------- bloques

def _texto(b):
    """Devuelve el HTML en línea del bloque: el original si traía formato, si no el texto escapado."""
    return b["html"] if b.get("html") else escape(b["texto"])


def _lista(b):
    items = "".join(f"<li>{i['html'] if i.get('html') else escape(i['texto'])}</li>" for i in b["items"])
    return f"<{b['t']}>{items}</{b['t']}>"


def _tabla(b):
    filas = []
    for fila in b["filas"]:
        celdas = "".join(
            f"<{'th' if c['th'] else 'td'}>{escape(c['texto'])}</{'th' if c['th'] else 'td'}>"
            for c in fila
        )
        filas.append(f"<tr>{celdas}</tr>")
    return f'<div class="entrada__tabla"><table>{"".join(filas)}</table></div>'


def _imagen(b, primera=False):
    alt = escape(b.get("alt") or "")
    carga = "" if primera else ' loading="lazy"'
    pie = f'<figcaption>{alt}</figcaption>' if alt else ""
    return (f'<figure class="entrada__figura">'
            f'<img src="{b["src"]}" alt="{alt}" width="1024" height="1024"{carga}>{pie}</figure>')


def cuerpo_bloques(bloques):
    """Convierte la lista de bloques en el HTML del artículo. Las FAQ salen aparte."""
    partes, faqs, primera_img = [], [], True
    for b in bloques:
        t = b["t"]
        if t == "faq":
            faqs.append((escape(b["pregunta"]), b.get("html") or f'<p>{escape(b["respuesta"])}</p>'))
        elif t == "img":
            partes.append(_imagen(b, primera_img))
            primera_img = False
        elif t in ("ul", "ol"):
            partes.append(_lista(b))
        elif t == "table":
            partes.append(_tabla(b))
        elif t == "blockquote":
            partes.append(f"<blockquote>{_texto(b)}</blockquote>")
        elif re.fullmatch(r"h[2-6]", t):
            ancla = f' id="{b["ancla"]}"' if b.get("ancla") else ""
            partes.append(f"<{t}{ancla}>{_texto(b)}</{t}>")
        else:
            partes.append(f"<p>{_texto(b)}</p>")
    return "\n      ".join(partes), faqs


def tabla_contenidos(bloques):
    """Índice con los H2 del artículo."""
    items = [f'<li><a href="#{b["ancla"]}">{escape(b["texto"])}</a></li>'
             for b in bloques if b["t"] == "h2" and b.get("ancla")]
    if len(items) < 3:
        return ""
    return f"""<aside class="entrada__toc revelar">
        <h2>Tabla de contenidos</h2>
        <ol>{"".join(items)}</ol>
      </aside>"""


# ---------------------------------------------------------------- schema

def schema_articulo(a, cat, faqs):
    url = f"https://marinriosconsultores.com/{a['slug']}/"
    grafo = [{
        "@type": "BlogPosting",
        "headline": a["h1"][:110],
        "description": a["desc"],
        "url": url,
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "datePublished": a["publicado"],
        "dateModified": a["modificado"] or a["publicado"],
        "articleSection": cat,
        "inLanguage": "es-CO",
        "wordCount": a["palabras"],
        "publisher": {"@type": "AccountingService", "name": "Marín Ríos Consultores",
                      "@id": "https://marinriosconsultores.com/#empresa"},
        "author": {"@id": AUTOR_ID},
    }, nodo_autor()]
    if a.get("portada"):
        grafo[0]["image"] = "https://marinriosconsultores.com/" + a["portada"]
    grafo.append({
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://marinriosconsultores.com/"},
            {"@type": "ListItem", "position": 2, "name": PILAR_DE.get(cat, ("Blog", "blog.html"))[0],
             "item": "https://marinriosconsultores.com/" + PILAR_DE.get(cat, ("Blog", "blog.html"))[1].replace(".html", "/")},
            {"@type": "ListItem", "position": 3, "name": a["h1"][:110], "item": url},
        ],
    })
    if faqs:
        grafo.append({
            "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": re.sub("<[^>]+>", "", q),
                            "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", " ", r).strip()}}
                           for q, r in faqs],
        })
    return json.dumps({"@context": "https://schema.org", "@graph": grafo}, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------- páginas

def construir():
    for a in ARTICULOS_CUERPO:
        cat = categoria(a["slug"])
        foto, alt_foto = FOTO_CATEGORIA[cat]
        html_cuerpo, faqs = cuerpo_bloques(a["bloques"])
        toc = tabla_contenidos(a["bloques"]) if a.get("toc") else ""

        bloque_faq = ""
        if faqs:
            bloque_faq = f"""
<section class="seccion claro">
  <div class="contenedor">
    {encabezado("Preguntas frecuentes", "Dudas que nos hacen sobre este tema")}
    {acordeon(faqs, prefijo=a["slug"][:14] + "-f")}
  </div>
</section>"""

        cuerpo = f"""
{heroe(
    escape(a["h1"]),
    escape(a["desc"]),
    foto,
    alt_foto,
    chip=f"Blog · {cat}",
    migas=[("Inicio", "index.html"), PILAR_DE.get(cat, ("Blog", "blog.html")), (escape(recortar(a["h1"], 48)), None)],
    cta1=("Agenda una asesoría", wa(MENSAJE_WA.format(a["h1"][:60]))),
    schema_migas=False,
)}

<section class="seccion--ajustada">
  <div class="contenedor">
    <div class="entrada{" entrada--con-toc" if toc else ""}">
      {toc}
      <!-- Sin "revelar": el observador de main.js exige ver el 14% del elemento y
           el cuerpo de un artículo nunca cabe en pantalla, así que no se mostraría. -->
      <article class="entrada__cuerpo">
        <p class="entrada__meta">
          <span><strong>{cat}</strong></span>
          <span>Por <a class="entrada__autor" href="#sobre-el-autor">{AUTOR_NOMBRE}</a></span>
          <span>Publicado el {fecha_larga(a["publicado"])}</span>
          <span>Actualizado el {fecha_larga(a["modificado"] or a["publicado"])}</span>
          <span>{a["palabras"]} palabras</span>
        </p>
      {html_cuerpo}
      {tarjeta_autor()}
      </article>
    </div>
  </div>
</section>
{bloque_faq}
<section class="seccion">
  <div class="contenedor">
    {encabezado("Servicios", "¿Prefieres que lo resolvamos nosotros?",
                "Leer sobre contabilidad ayuda. Tener un equipo que la ejecute, ayuda más.")}
    {servicios_num(TRIO)}
  </div>
</section>

{cta_final(
    "¿Tienes una duda sobre tu caso concreto?",
    "Escríbenos con la situación real de tu empresa y te respondemos con una recomendación, no con un artículo genérico.",
    boton="Escríbenos",
    mensaje=MENSAJE_WA.format(a["h1"][:60]),
    secundario=SECUNDARIO_DE.get(cat, ("Cotiza tu outsourcing contable", "cotizacion-outsourcing-contable.html")),
)}
"""

        PAGINAS.append(dict(
            archivo=f"{a['slug']}.html",
            titulo=a["titulo_seo"][:65],
            descripcion=a["desc"][:165],
            activo="blog",
            og_img=a["portada"].replace("assets/img/", "") if a.get("portada") else "reunion-ancho.jpg",
            schema=schema_articulo(a, cat, faqs),
            cuerpo=cuerpo,
            categoria=cat,
        ))


construir()
