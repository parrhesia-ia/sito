"""Scrive le card degli articoli direttamente nell'HTML (visibili anche senza JavaScript e ai motori di ricerca)."""
import json, html, re, os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
items = json.load(open(os.path.join(R, "data/articoli.json"), encoding="utf-8"))
def cards(base, limit=None):
    out = []
    for a in items[:limit] if limit else items:
        if not a.get("url"): continue
        thumb = f'<div class="thumb"><img src="{base}{a["img"]}" alt="" loading="lazy"></div>' if a.get("img") else ""
        out.append(f'<a class="card" href="{base}{a["url"]}">{thumb}<span class="fmt">{html.escape(a["formato"])}</span>'
                   f'<h3>{html.escape(a["titolo"])}</h3><p>{html.escape(a["sommario"])}</p><span class="meta">{html.escape(a["data_testo"])}</span></a>')
    return "\n        ".join(out)
for path, base, limit in [("index.html", "", 5), ("articoli/index.html", "../", None)]:
    p = os.path.join(R, path); s = open(p, encoding="utf-8").read()
    s = re.sub(r'(<div class="grid" data-articoli[^>]*>)(.*?)(</div>)', lambda m: m.group(1) + "\n        " + cards(base, limit) + "\n      " + m.group(3), s, count=1, flags=re.S)
    open(p, "w", encoding="utf-8").write(s)
print("ok", len(items))
