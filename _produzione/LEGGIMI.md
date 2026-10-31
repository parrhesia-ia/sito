# Produzione ParrhesIA

Cartella non pubblicata (GitHub Pages ignora le cartelle che iniziano con `_`). Qui stanno gli strumenti per video e caroselli.

- `video_decreto_cortei.py` — pipeline video verticale 1080x1920: voce Manuela (ElevenLabs, voice_id oVJbgLwL0s5pk9e2U6QH) con tempi parola per parola, scene animate, sottotitoli evidenziati, etichetta IA. La chiave API **non** va mai salvata qui: si incolla a ogni sessione in un file `.key` locale.
- `carosello_template.py` — template carosello 4:5, 8 slide: copertina, La notizia, I numeri, Detto vs Fatto, punto centrale, Il conto per l'Italia, La domanda di ParrhesIA (slide rossa, domanda aperta, niente verdetti), chiusura.
- `suoni/firma_ParrhesIA.mp3` — firma sonora scelta il 24/10/2026 (versione "pulsazione").
- **Apertura dal 31/10/2026** (decisa dopo l'analisi dei numeri: con 3 s di logo+firma prima della voce il tempo medio di visione su Instagram era sceso da ~12 s a ~3 s):
  - la voce parte a 0,3 s (`m.START = 0.3`), nessuna scena "firma" iniziale; il titolo del tema è sullo schermo dal primo fotogramma;
  - la firma suona sotto la prima frase, volume 0.45, mescolata alla base e abbassata dal sidechain come il tappeto;
  - in chiusura la firma resta come prima (a totale − 4,3 s);
  - modello: `video_apertura_voce_subito.py` (derivato dal video 13 midterm).
- Musica di sottofondo: brano libero da diritti scelto dall'utente (YouTube Audio Library o Pixabay), al posto di `tappeto.mp3`, con `--music percorso.mp3`. In attesa del brano si usa il tappeto.
- `suoni/tappeto.mp3` — tappeto sotto la voce, abbassato con sidechain quando Manuela parla (volume 0.22, ratio 8).
- `fonts/` — Barlow Condensed (OFL).

Colori: fondo #0e0e0e, testo #f0eeea, grigio #9a9a9a, rosso #d62626.

## Pronuncia (testo parlato per ElevenLabs)
Nel testo parlato le sigle vanno scritte come si leggono; nei sottotitoli restano normali (stesso numero di parole).
- CGIL → "Cigièlle" (25/10/2026: letta male nel video 08)
- Numeri e cifre sempre in lettere nel parlato: "ventisette", "due euro e trenta".
