# -*- coding: utf-8 -*-
"""
Crawler + verificador de URLs para https://marinriosconsultores.com/
Genera un Excel con todas las URLs encontradas y su estado HTTP.
"""
import re
import time
import queue
import threading
from urllib.parse import urljoin, urldefrag, urlparse

import requests
from lxml import html as lxml_html, etree
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

BASE = "https://marinriosconsultores.com/"
DOMAIN = "marinriosconsultores.com"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
HEADERS = {"User-Agent": UA, "Accept-Language": "es-ES,es;q=0.9,en;q=0.8"}
TIMEOUT = 25
WORKERS = 8

SKIP_SCHEMES = ("mailto:", "tel:", "javascript:", "whatsapp:", "sms:", "#", "data:")
ASSET_EXT = re.compile(r"\.(jpg|jpeg|png|gif|webp|svg|ico|css|js|woff2?|ttf|eot|mp4|webm|avif)(\?|$)", re.I)

session_local = threading.local()


def sess():
    if not hasattr(session_local, "s"):
        s = requests.Session()
        s.headers.update(HEADERS)
        session_local.s = s
    return session_local.s


def norm(u):
    u, _ = urldefrag(u)
    u = u.strip()
    if u.endswith("/index.html"):
        u = u[: -len("index.html")]
    return u


def is_internal(u):
    h = urlparse(u).netloc.lower().replace("www.", "")
    return h == DOMAIN


# ---------------------------------------------------------------- sitemaps
def urls_from_sitemaps():
    found, pending, seen_sm = set(), ["https://marinriosconsultores.com/sitemap_index.xml"], set()
    while pending:
        sm = pending.pop()
        if sm in seen_sm:
            continue
        seen_sm.add(sm)
        try:
            r = sess().get(sm, timeout=TIMEOUT, allow_redirects=True)
            if r.status_code != 200:
                continue
            root = etree.fromstring(r.content)
        except Exception:
            continue
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        for loc in root.xpath("//s:sitemap/s:loc/text()", namespaces=ns):
            pending.append(loc.strip())
        for loc in root.xpath("//s:url/s:loc/text()", namespaces=ns):
            found.add(norm(loc.strip()))
    return found


# ---------------------------------------------------------------- crawl
results = {}          # url -> dict
lock = threading.Lock()
q = queue.Queue()
enqueued = set()


def add(url, origen):
    url = norm(url)
    if not url or url.startswith(SKIP_SCHEMES):
        return
    if not url.startswith(("http://", "https://")):
        return
    with lock:
        if url in enqueued:
            if url in results and origen and results[url].get("origen") == "":
                results[url]["origen"] = origen
            return
        enqueued.add(url)
    q.put((url, origen))


def check(url):
    """Devuelve (status, final_url, content_type, titulo, redirigido)."""
    s = sess()
    try:
        r = s.get(url, timeout=TIMEOUT, allow_redirects=True, stream=True)
    except requests.exceptions.SSLError as e:
        return ("ERROR SSL", "", "", "", "", str(e)[:150], None)
    except requests.exceptions.ConnectTimeout:
        return ("TIMEOUT", "", "", "", "", "Connect timeout", None)
    except requests.exceptions.ReadTimeout:
        return ("TIMEOUT", "", "", "", "", "Read timeout", None)
    except requests.exceptions.ConnectionError as e:
        return ("ERROR CONEXION", "", "", "", "", str(e)[:150], None)
    except Exception as e:
        return ("ERROR", "", "", "", "", str(e)[:150], None)

    ctype = r.headers.get("Content-Type", "").split(";")[0].strip()
    chain = " > ".join(str(h.status_code) for h in r.history)
    titulo, doc = "", None
    body = b""
    if "html" in ctype.lower():
        try:
            body = r.raw.read(600000, decode_content=True) if hasattr(r.raw, "read") else r.content
        except Exception:
            body = r.content or b""
        if not body:
            body = r.content or b""
        try:
            doc = lxml_html.fromstring(body)
            t = doc.xpath("//title/text()")
            titulo = t[0].strip()[:200] if t else ""
        except Exception:
            doc = None
    r.close()
    return (r.status_code, r.url, ctype, titulo, chain, "", doc)


def worker():
    while True:
        try:
            url, origen = q.get(timeout=3)
        except queue.Empty:
            return
        try:
            interno = is_internal(url)
            status, final, ctype, titulo, chain, err, doc = check(url)
            with lock:
                results[url] = {
                    "url": url,
                    "estado": status,
                    "ok": (isinstance(status, int) and 200 <= status < 300),
                    "tipo": "Interna" if interno else "Externa",
                    "url_final": final if final and norm(final) != url else "",
                    "redirecciones": chain,
                    "content_type": ctype,
                    "titulo": titulo,
                    "error": err,
                    "origen": origen,
                }
            # solo seguimos enlaces dentro de páginas HTML internas
            if doc is not None and interno and isinstance(status, int) and status < 400:
                base_url = final or url
                for href in set(doc.xpath("//a/@href") + doc.xpath("//area/@href")):
                    href = href.strip()
                    if not href or href.startswith(SKIP_SCHEMES):
                        continue
                    absu = norm(urljoin(base_url, href))
                    if ASSET_EXT.search(absu):
                        continue
                    add(absu, base_url)
        except Exception as e:
            with lock:
                results[url] = {"url": url, "estado": "ERROR", "ok": False,
                                "tipo": "Interna" if is_internal(url) else "Externa",
                                "url_final": "", "redirecciones": "", "content_type": "",
                                "titulo": "", "error": str(e)[:150], "origen": origen}
        finally:
            q.task_done()


def main():
    print("Leyendo sitemaps...")
    sm = urls_from_sitemaps()
    print(f"  {len(sm)} URLs en sitemap")

    add(BASE, "semilla")
    for u in sm:
        add(u, "sitemap.xml")

    hilos = [threading.Thread(target=worker, daemon=True) for _ in range(WORKERS)]
    for h in hilos:
        h.start()
    while any(h.is_alive() for h in hilos):
        time.sleep(2)
        with lock:
            print(f"  procesadas: {len(results)} | en cola: {q.qsize()}", end="\r")
    for h in hilos:
        h.join()
    print(f"\nTotal URLs verificadas: {len(results)}")
    return sm


def excel(sm_urls):
    filas = sorted(results.values(), key=lambda d: (d["tipo"] != "Interna", str(d["url"])))
    wb = Workbook()

    # ---- Hoja 1: todas las URLs
    ws = wb.active
    ws.title = "URLs"
    cols = ["#", "URL", "Estado", "Resultado", "Observación", "Tipo", "En sitemap",
            "Redirige a", "Cadena redirecciones", "Content-Type", "Título de la página",
            "Error", "Encontrada en"]
    ws.append(cols)

    # dominios que bloquean peticiones automatizadas -> el código no indica enlace roto
    BLOQUEAN_BOTS = ("web.whatsapp.com", "api.whatsapp.com", "wa.me", "linkedin.com",
                     "facebook.com", "instagram.com", "x.com", "twitter.com")

    def bloqueado(d):
        h = urlparse(d["url"]).netloc.lower()
        return any(h.endswith(b) or h == b for b in BLOQUEAN_BOTS)

    def observacion(d):
        if d["ok"]:
            return ""
        if bloqueado(d):
            return "Falso positivo: la plataforma bloquea peticiones automáticas. Verificar manualmente."
        if str(d["estado"]).startswith("ERROR SSL"):
            return "Certificado SSL del sitio externo no válido para Python. Suele abrir bien en navegador."
        if isinstance(d["estado"], int) and d["estado"] == 404:
            return "ENLACE ROTO: la página no existe." if d["tipo"] == "Interna" else "Enlace externo roto."
        if isinstance(d["estado"], int) and 300 <= d["estado"] < 400:
            return "Redirección."
        return "Revisar: el servidor no devolvió una respuesta válida."

    def etiqueta(d):
        s = d["estado"]
        if isinstance(s, int):
            if 200 <= s < 300:
                return "OK"
            if 300 <= s < 400:
                return "Redirección"
            if s == 404:
                return "No encontrada (404)"
            if 400 <= s < 500:
                return f"Error cliente ({s})"
            return f"Error servidor ({s})"
        return str(s)

    for i, d in enumerate(filas, 1):
        ws.append([i, d["url"], d["estado"], etiqueta(d), observacion(d), d["tipo"],
                   "Sí" if d["url"] in sm_urls else "No",
                   d["url_final"], d["redirecciones"], d["content_type"],
                   d["titulo"], d["error"], d["origen"]])

    verde = PatternFill("solid", fgColor="C6EFCE")
    amar = PatternFill("solid", fgColor="FFEB9C")
    rojo = PatternFill("solid", fgColor="FFC7CE")
    gris = PatternFill("solid", fgColor="E7E6E6")
    for row, d in zip(ws.iter_rows(min_row=2, max_row=ws.max_row), filas):
        s = row[2].value
        if isinstance(s, int) and 200 <= s < 300:
            f = verde
        elif bloqueado(d) or str(s).startswith("ERROR SSL"):
            f = gris
        elif isinstance(s, int) and 300 <= s < 400:
            f = amar
        else:
            f = rojo
        for c in row:
            c.fill = f
        row[1].hyperlink = row[1].value
        row[1].font = Font(color="0563C1", underline="single")

    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="1F4E79")
        c.alignment = Alignment(horizontal="center", vertical="center")
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    anchos = [5, 70, 9, 20, 60, 10, 12, 55, 18, 22, 55, 40, 55]
    for i, w in enumerate(anchos, 1):
        ws.column_dimensions[get_column_letter(i)].width = w

    # ---- Hoja 2: resumen
    ws2 = wb.create_sheet("Resumen")
    internas = [d for d in filas if d["tipo"] == "Interna"]
    externas = [d for d in filas if d["tipo"] == "Externa"]
    rotas = [d for d in filas if not d["ok"] and not (isinstance(d["estado"], int) and 300 <= d["estado"] < 400)]
    redir = [d for d in filas if isinstance(d["estado"], int) and 300 <= d["estado"] < 400]
    reales = [d for d in rotas if not bloqueado(d) and not str(d["estado"]).startswith("ERROR SSL")]
    falsos = [d for d in rotas if d not in reales]
    resumen = [
        ("Sitio analizado", BASE),
        ("Total de URLs encontradas", len(filas)),
        ("URLs internas", len(internas)),
        ("URLs externas", len(externas)),
        ("URLs en el sitemap", len(sm_urls)),
        ("", ""),
        ("URLs OK (2xx)", sum(1 for d in filas if d["ok"])),
        ("Redirecciones (3xx)", len(redir)),
        ("URLs con problema", len(rotas)),
        ("   - Errores reales a corregir", len(reales)),
        ("   - Falsos positivos (bloqueo anti-bot / SSL)", len(falsos)),
        ("Enlaces internos rotos (404)", sum(1 for d in reales if d["tipo"] == "Interna")),
    ]
    ws2.append(["Métrica", "Valor"])
    for k, v in resumen:
        ws2.append([k, v])
    for c in ws2[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="1F4E79")
    ws2.column_dimensions["A"].width = 40
    ws2.column_dimensions["B"].width = 50

    # desglose por código
    ws2.append(["", ""])
    ws2.append(["Desglose por código", "Cantidad"])
    ws2.cell(ws2.max_row, 1).font = Font(bold=True)
    ws2.cell(ws2.max_row, 2).font = Font(bold=True)
    conteo = {}
    for d in filas:
        conteo[str(d["estado"])] = conteo.get(str(d["estado"]), 0) + 1
    for k in sorted(conteo, key=lambda x: (not x.isdigit(), x)):
        ws2.append([k, conteo[k]])

    # ---- Hoja 3: solo problemas
    ws3 = wb.create_sheet("Problemas")
    ws3.append(["URL", "Estado", "Tipo", "Diagnóstico", "Observación", "Error", "Encontrada en"])
    for d in reales + falsos:
        ws3.append([d["url"], d["estado"], d["tipo"],
                    "ERROR REAL" if d in reales else "Falso positivo",
                    observacion(d), d["error"], d["origen"]])
    for row in ws3.iter_rows(min_row=2, max_row=ws3.max_row):
        f = rojo if row[3].value == "ERROR REAL" else gris
        for c in row:
            c.fill = f
    for c in ws3[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="C00000")
    for i, w in enumerate([70, 12, 10, 16, 60, 45, 55], 1):
        ws3.column_dimensions[get_column_letter(i)].width = w
    ws3.freeze_panes = "A2"

    out = r"C:\Users\XIMEN\OneDrive\Escritorio\Marin rios\URLs_marinriosconsultores.xlsx"
    wb.save(out)
    print("Excel guardado en:", out)
    print(f"OK: {sum(1 for d in filas if d['ok'])} | Redirecciones: {len(redir)} | Problemas: {len(rotas)}")


if __name__ == "__main__":
    sm = main()
    excel(sm)
