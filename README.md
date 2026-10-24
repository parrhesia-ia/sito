# ParrhesIA — sito

Sito statico di [ParrhesIA](https://parrhesia-ia.com), pubblicato con GitHub Pages.

- `index.html` — home
- `chi-siamo.html` — chi è ParrhesIA, metodo e trasparenza
- `articoli/` — archivio e articoli
- `data/articoli.json` — elenco degli articoli mostrato in home e in archivio
- `assets/` — stile, script, icone

Per aggiungere un articolo: creare la pagina in `articoli/` (vedi `tools/nuovo_articolo.py`), aggiungere una voce in cima a `data/articoli.json` e lanciare `python3 tools/build.py`.

Bozze programmate: `_bozze/<slug>.html` più la scheda `_bozze/<slug>.json`. All'ora di uscita: `python3 tools/pubblica.py <slug> "<data testo>"` sposta la pagina in `articoli/`, aggiunge la scheda all'elenco e rigenera le card. La cartella `_bozze/` non viene pubblicata da GitHub Pages.
