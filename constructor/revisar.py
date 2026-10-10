# -*- coding: utf-8 -*-
"""Revisión del sitio generado: enlaces internos y metadatos SEO."""

import re, os, glob, sys

SITIO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sitio")
os.chdir(SITIO)

# Las páginas se publican como `slug/index.html` y se sirven en `/slug/`.
paginas = sorted(glob.glob("index.html") + glob.glob("*/index.html"))
paginas = [p for p in paginas if not p.startswith("assets" + os.sep)]


def url_publica(archivo):
    return "/" if archivo == "index.html" else "/" + archivo[: -len("/index.html")] + "/"


def archivo_de(url):
    """'/slug/' -> 'slug/index.html'   ·   '/assets/x.css' -> 'assets/x.css'"""
    ruta = url.lstrip("/")
    if url.endswith("/") or ruta == "":
        return os.path.join(ruta, "index.html")
    return ruta


urls_validas = {url_publica(p) for p in paginas}

rotos, externos, total = [], set(), 0
for p in paginas:
    h = open(p, encoding="utf-8").read()
    for r in re.findall(r'(?:href|src)="([^"#][^"]*)"', h):
        total += 1
        if r.startswith(("http://", "https://", "mailto:", "tel:", "//")):
            externos.add(r.split("?")[0])
            continue
        destino = r.split("?")[0].split("#")[0]
        if not destino:
            continue
        if not destino.startswith("/"):
            rotos.append((p, r, "ruta relativa: no funciona fuera de la raíz"))
            continue
        if destino in urls_validas:
            continue
        if not os.path.exists(archivo_de(destino)):
            rotos.append((p, r, "no existe"))

print(f"Páginas: {len(paginas)} | referencias revisadas: {total}")
print(f"Enlaces internos rotos: {len(rotos)}")
for p, r, motivo in rotos[:25]:
    print("   ", p, "->", r, f"({motivo})")

print(f"\nDestinos externos distintos: {len(externos)}")

print("\n--- SEO por página ---")
problemas = 0
for p in paginas:
    h = open(p, encoding="utf-8").read()
    t = re.search(r"<title>(.*?)</title>", h, re.S)
    d = re.search(r'<meta name="description" content="(.*?)"', h, re.S)
    h1 = re.findall(r"<h1[^>]*>(.*?)</h1>", h, re.S)
    canon = re.search(r'rel="canonical" href="(.*?)"', h)
    schema = h.count("application/ld+json")
    # Una página noindex no necesita datos estructurados: no va a aparecer en
    # resultados, así que exigírselos solo genera ruido en el informe.
    noindex = 'name="robots" content="noindex' in h
    tt = re.sub("<[^>]+>", "", t.group(1)).strip() if t else ""
    dd = d.group(1) if d else ""
    marca = []
    if not tt or len(tt) > 65: marca.append(f"title {len(tt)}")
    if not dd or len(dd) > 165: marca.append(f"desc {len(dd)}")
    if len(h1) != 1: marca.append(f"H1 x{len(h1)}")
    if not canon: marca.append("sin canonical")
    elif not canon.group(1).endswith(url_publica(p)): marca.append("canonical no coincide con la URL")
    if not schema and not noindex: marca.append("sin schema")
    estado = "OK " if not marca else "!! "
    if marca: problemas += 1
    print(f"{estado}{url_publica(p):45s}{' [noindex]' if noindex else '':10s} title:{len(tt):3d} desc:{len(dd):3d} H1:{len(h1)} schema:{schema}"
          + (("  -> " + ", ".join(marca)) if marca else ""))

print(f"\nPáginas con observaciones: {problemas}/{len(paginas)}")
sys.exit(1 if rotos else 0)
