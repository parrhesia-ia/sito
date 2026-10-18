"""Genera una pagina articolo di ParrhesIA a partire da un dizionario.

Uso: importare e chiamare scrivi(art) con chiavi:
slug, titolo, kicker, sommario, data_testo, descrizione, corpo_html, fonti=[(testo, url)]
"""
import html, os

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "articoli")

TPL = """<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{titolo} · ParrhesIA</title>
<meta name="description" content="{descrizione}">
<meta property="og:title" content="{titolo}">
<meta property="og:description" content="{descrizione}">
<meta property="og:image" content="https://parrhesia-ia.com/assets/og.jpg">
<meta property="og:type" content="article">
<meta name="theme-color" content="#0e0e0e">
<link rel="icon" href="../assets/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800;900&family=Inter:wght@400;500;600;700&family=Source+Serif+4:wght@700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/style.css">
</head>
<body>
<a class="skip" href="#contenuto">Vai al contenuto</a>
<header class="top">
  <div class="wrap">
    <a class="logo" href="../">PARRHES<span class="ia">IA</span></a>
    <button class="burger" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav class="nav" id="nav">
      <a href="./">Articoli</a>
      <a href="../#video">Video</a>
      <a href="../chi-siamo.html">Chi è ParrhesIA</a>
      <a href="../#newsletter">Newsletter</a>
    </nav>
  </div>
</header>

<main id="contenuto" class="article">
  <p class="kicker">{kicker}</p>
  <h1>{titolo}</h1>
  <p class="sum">{sommario}</p>
  <div class="byline"><span class="pill"><i></i> Testo generato con IA, verificato sulle fonti</span><span>{data_testo}</span></div>

{corpo_html}

  <h2>Fonti</h2>
  <ul class="sources">
{fonti_html}
  </ul>

  <p class="disclaimer">Questo articolo è stato scritto con l'intelligenza artificiale e verificato sulle fonti indicate. Hai trovato un errore? Segnalalo sui nostri social: le correzioni vengono pubblicate qui con la data della modifica.</p>
</main>

<footer>
  <div class="wrap">
    <div><a class="logo" href="../">PARRHES<span class="ia">IA</span></a>
      <p style="margin:8px 0 0;max-width:420px">ParrhesIA è un'intelligenza artificiale. Testi, voce e video sono generati con l'IA e verificati sulle fonti prima della pubblicazione.</p></div>
    <div><p style="margin:0"><a href="./">Tutti gli articoli</a> · <a href="../chi-siamo.html">Chi è ParrhesIA</a></p><p style="margin:8px 0 0">© 2026 ParrhesIA</p></div>
  </div>
</footer>
<script src="../assets/main.js"></script>
</body>
</html>
"""

def scrivi(art):
    fonti_html = "\n".join(
        f'    <li><a href="{html.escape(u)}" target="_blank" rel="noopener">{html.escape(t)}</a></li>' for t, u in art["fonti"])
    out = TPL.format(titolo=html.escape(art["titolo"]), kicker=html.escape(art["kicker"]), sommario=html.escape(art["sommario"]),
                     data_testo=html.escape(art["data_testo"]), descrizione=html.escape(art["descrizione"]),
                     corpo_html=art["corpo_html"], fonti_html=fonti_html)
    path = os.path.join(BASE, art["slug"] + ".html")
    with open(path, "w", encoding="utf-8") as f: f.write(out)
    return path
