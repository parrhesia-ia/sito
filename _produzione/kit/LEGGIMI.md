# Kit di produzione (dal 22/11/2026)

Lo spazio di lavoro può essere azzerato: qui c'è tutto il necessario per ripartire.

Nuovo video in una cartella /home/claude/<tema>:
- cp kit/make.py kit/tail_main.py kit/carosello_base.py kit/carosello_chiusura.py .
- cp -r fonts .; cp suoni/firma_ParrhesIA.mp3 firma.mp3; cp suoni/tappeto.mp3 .
- mkdir img voce out; img/photos.json = {"nome": {"file": "...", "credit": "..."}}
- .key: chiave ElevenLabs incollata dall'utente a ogni sessione (MAI nel repository).
- head.py con m.SCENES, scene sc_* e m.SC.update; in tail_main.py cambiare OUTNAME.
- Video: cat head.py tail_main.py > make_x.py; python3 make_x.py --dummy --frames 5,20 (prova), poi python3 make_x.py.
- Carosello: cat carosello_base.py slides.py carosello_chiusura.py > carosello_x.py; python3 carosello_x.py.
