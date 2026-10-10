# -*- coding: utf-8 -*-
"""Genera todas las páginas del sitio, el sitemap y el robots.txt."""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from base import plantilla, ruta_publica, BASE_URL
import paginas2          # importa paginas.py y añade precios, blog y ciudades
import paginas_home       # la portada
import paginas3           # contáctenos, nosotros y política de privacidad
import paginas_landings   # landings de campaña y páginas de gracias
import paginas_404        # la página de error
import articulos_paginas  # añade una página por cada artículo del blog
import paginas_meta       # landings de pauta en Meta (revisoría fiscal)
from paginas import PAGINAS

SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sitio")


def destino(archivo):
    """Cada página se publica como `slug/index.html` para que su URL sea
    `/slug/`, exactamente la misma que tenía en el WordPress. La portada
    se queda en la raíz."""
    # El 404 vive en la raíz porque el servidor lo sirve por ruta fija.
    if archivo in ("index.html", "404.html"):
        return os.path.join(SALIDA, archivo)
    carpeta = os.path.join(SALIDA, archivo[:-len(".html")])
    os.makedirs(carpeta, exist_ok=True)
    return os.path.join(carpeta, "index.html")


def limpiar_planos():
    """Borra los .html sueltos de la raíz que dejó el esquema anterior:
    si se quedan, el sitio sirve cada página en dos URLs distintas."""
    borrados = 0
    for nombre in os.listdir(SALIDA):
        if nombre.endswith(".html") and nombre not in ("index.html", "404.html"):
            os.remove(os.path.join(SALIDA, nombre))
            borrados += 1
    return borrados


def recientes_para(p):
    """Carrusel de últimas publicaciones antes del pie: en las páginas de la
    web normal (portada, servicios, ciudades, nosotros, contacto y artículos).
    No va en landings de pauta, páginas noindex ni en el propio /blog/.
    Devuelve el slug a excluir ("" = ninguno) o None si no aplica."""
    if p.get("landing") is not None or "noindex" in p.get("robots", "") or p["archivo"] == "blog.html":
        return None
    return p["archivo"][:-len(".html")]

def main():
    os.makedirs(SALIDA, exist_ok=True)
    sueltos = limpiar_planos()
    if sueltos:
        print(f"  (se retiraron {sueltos} .html sueltos del esquema anterior)\n")
    escritas = []

    for p in PAGINAS:
        html = plantilla(
            archivo=p["archivo"],
            titulo=p["titulo"],
            descripcion=p["descripcion"],
            cuerpo=p["cuerpo"],
            activo=p.get("activo", ""),
            schema=p.get("schema", ""),
            og_img=p.get("og_img", "equipo-ancho.jpg"),
            robots=p.get("robots", "index, follow, max-snippet:-1, max-image-preview:large"),
            css_extra=p.get("css_extra", ()),
            fuentes_extra=p.get("fuentes_extra", ""),
            clase_body=p.get("clase_body", ""),
            landing=p.get("landing"),
            recientes=recientes_para(p),
        )
        with open(destino(p["archivo"]), "w", encoding="utf-8") as f:
            f.write(html)
        if "noindex" not in p.get("robots", ""):
            escritas.append(p["archivo"])
        print(f"  {ruta_publica(p['archivo']):45s} {len(html)//1024:>4d} KB")

    # ---- sitemap ----
    prioridades = {"index.html": "1.0", "outsourcing-contable.html": "0.9",
                   "revisoria-fiscal.html": "0.9", "consultoria-financiera.html": "0.9",
                   "precios-outsourcing-contable.html": "0.8", "blog.html": "0.8"}
    # El sitemap solo lista lo indexable: incluir páginas noindex es una
    # contradicción que Search Console reporta como error.
    urls = ["index.html"] + escritas
    vistas, filas = set(), []
    for a in urls:
        if a in vistas:
            continue
        vistas.add(a)
        loc = BASE_URL + ("" if a == "index.html" else a.replace(".html", "/"))
        filas.append(
            f"  <url>\n    <loc>{loc}</loc>\n"
            f"    <changefreq>monthly</changefreq>\n"
            f"    <priority>{prioridades.get(a, '0.7')}</priority>\n  </url>"
        )
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               + "\n".join(filas) + "\n</urlset>\n")
    with open(os.path.join(SALIDA, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)

    # El sitio es estático: ya no hay panel de WordPress que excluir.
    robots = ("User-agent: *\n"
              "Allow: /\n\n"
              f"Sitemap: {BASE_URL}sitemap.xml\n")
    with open(os.path.join(SALIDA, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots)

    print(f"\n{len(vistas)} URLs en sitemap.xml · robots.txt escrito")


if __name__ == "__main__":
    main()
