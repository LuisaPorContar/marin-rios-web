# -*- coding: utf-8 -*-
"""Genera todas las páginas del sitio, el sitemap y el robots.txt."""

import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from base import plantilla, ruta_publica, BASE_URL
import paginas2          # importa paginas.py y añade precios, blog y ciudades
import paginas_home       # la portada
import paginas3           # contáctenos, nosotros y política de privacidad
import paginas_landings   # landings de campaña y páginas de gracias
import paginas_404        # la página de error
import articulos_paginas  # añade una página por cada artículo del blog
import paginas_meta       # landings de pauta en Meta (revisoría fiscal)
import paginas_rf_ciudades  # revisoría fiscal en Medellín y el Eje Cafetero
import paginas_cotizacion   # cotización de outsourcing contable y de revisoría fiscal
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


GUIAS_OUTSOURCING = [
    "que-es-outsourcing-contable", "cuanto-cuesta-contratar-un-servicio-de-outsourcing-contable",
    "como-contratar-un-servicio-de-outsourcing-contable", "cambiar-contador-cuanto-cuesta",
    "calendario-tributario-actualizado", "exogena", "que-es-la-retencion-en-la-fuente",
    "nomina-electronica-colombia",
]
GUIAS_FINANZAS = [
    "flujo-caja-pymes-colombia", "presupuesto-empresarial", "fugas-financieras",
    "aumenta-rentabilidad-negocio-contabilidad", "como-leer-un-balance-general",
    "como-salir-de-deudas-empresariales", "inflacion-tasas-banco-republica-empresas",
    "cuando-escalar-negocio-senales-finacieras",
]


def _articulos_por_fecha():
    import json
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "articulos_cuerpo.json"), encoding="utf-8") as f:
        return sorted(json.load(f), key=lambda a: a.get("publicado", ""), reverse=True)


def recientes_para(p):
    """Carrusel de artículos antes del pie, curado según la sección de la página.
    No va en landings de pauta, páginas noindex ni en el propio /blog/, y tampoco
    en las de revisoría fiscal, que ya traen su carrusel de guías en el cuerpo.
    Devuelve None si no aplica, el slug a excluir (últimas publicaciones) o los
    argumentos de ultimas_publicaciones()."""
    if p.get("landing") is not None or "noindex" in p.get("robots", "") or p["archivo"] == "blog.html":
        return None
    slug = p["archivo"][:-len(".html")]
    if slug == "revisoria-fiscal" or slug.startswith("revisoria-fiscal-"):
        return None
    if slug in ("index", "outsourcing-contable", "precios-outsourcing-contable", "cotizacion-outsourcing-contable") \
            or slug.startswith("outsourcing-contable-"):
        return dict(solo=GUIAS_OUTSOURCING, eyebrow="Guías de outsourcing contable",
                    titulo="Guías para tener su contabilidad al día",
                    intro="Lo que conviene saber antes de tercerizar la contabilidad y las obligaciones que su empresa no puede dejar vencer.")
    if slug == "cotizacion-revisoria-fiscal":
        from paginas import GUIAS_REVISORIA
        return dict(solo=GUIAS_REVISORIA, eyebrow="Guías de revisoría fiscal", titulo="Antes de contratar, lea esto",
                    intro="Quién está obligado, qué hace el revisor fiscal y cómo comparar propuestas.")
    if slug == "consultoria-financiera":
        return dict(solo=GUIAS_FINANZAS, eyebrow="Guías de finanzas", titulo="Finanzas para pymes, sin rodeos",
                    intro="Flujo de caja, presupuesto, rentabilidad y deuda explicados para decidir mejor.")
    cat = p.get("categoria")
    if cat:
        from articulos_paginas import categoria
        mismos = [a["slug"] for a in _articulos_por_fecha() if a["slug"] != slug and categoria(a["slug"]) == cat]
        if len(mismos) < 4:
            mismos += [a["slug"] for a in _articulos_por_fecha() if a["slug"] != slug and a["slug"] not in mismos]
        return dict(solo=mismos[:8], titulo=f"Más guías de {cat[0].lower() + cat[1:]}")
    return slug

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
    # lastmod real: la fecha cambia solo cuando cambia el HTML de la página.
    import hashlib, datetime
    ruta_lm = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lastmod.json")
    try:
        lm = json.load(open(ruta_lm, encoding="utf-8"))
    except (OSError, ValueError):
        lm = {}
    hoy = datetime.date.today().isoformat()
    for a in urls:
        with open(destino(a), encoding="utf-8") as f:
            h = hashlib.sha1(f.read().encode("utf-8")).hexdigest()
        if lm.get(a, {}).get("hash") != h:
            lm[a] = {"hash": h, "fecha": hoy}
    with open(ruta_lm, "w", encoding="utf-8") as f:
        json.dump(lm, f, ensure_ascii=False, indent=1, sort_keys=True)
    vistas, filas = set(), []
    for a in urls:
        if a in vistas:
            continue
        vistas.add(a)
        loc = BASE_URL + ("" if a == "index.html" else a.replace(".html", "/"))
        filas.append(
            f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{lm[a]['fecha']}</lastmod>\n"
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
