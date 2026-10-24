# Produzione ParrhesIA

Cartella non pubblicata (GitHub Pages ignora le cartelle che iniziano con `_`). Qui stanno gli strumenti per video e caroselli.

- `video_decreto_cortei.py` — pipeline video verticale 1080x1920: voce Manuela (ElevenLabs, voice_id oVJbgLwL0s5pk9e2U6QH) con tempi parola per parola, scene animate, sottotitoli evidenziati, etichetta IA. La chiave API **non** va mai salvata qui: si incolla a ogni sessione in un file `.key` locale.
- `carosello_template.py` — template carosello 4:5, 8 slide: copertina, La notizia, I numeri, Detto vs Fatto, punto centrale, Il conto per l'Italia, La domanda di ParrhesIA (slide rossa, domanda aperta, niente verdetti), chiusura.
- `suoni/firma_ParrhesIA.mp3` — firma sonora scelta il 24/10/2026 (versione "pulsazione"): in apertura e chiusura di ogni video.
- `suoni/tappeto.mp3` — tappeto sotto la voce, abbassato con sidechain quando Manuela parla (volume 0.22, ratio 8).
- `fonts/` — Barlow Condensed (OFL).

Colori: fondo #0e0e0e, testo #f0eeea, grigio #9a9a9a, rosso #d62626.
