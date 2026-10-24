"""ParrhesIA · video "Il decreto cortei è costituzionale?"
Uso: python3 make.py [--dummy]   (--dummy = tempi finti, senza voce, per controllare la grafica)
"""
import os, sys, json, base64, math, random, subprocess, urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps

D = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1080, 1920, 30
BG = (14, 14, 14); INK = (240, 238, 234); MUTED = (154, 154, 154); RED = (214, 38, 38); LINE = (42, 42, 42)
F = lambda name, size: ImageFont.truetype(f"{D}/fonts/{name}.ttf" if not name.startswith("/") else name, size)
BLACK = "BarlowCondensed-Black"; XB = "BarlowCondensed-ExtraBold"; BOLD = "BarlowCondensed-Bold"
INTER_B = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"; INTER_SB = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
INTER_M = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"

# (sottotitolo, testo parlato, scena). Stesso numero di parole tra i due.
SCENES = [
    ("Da ieri in Italia c'è una nuova legge. Si chiama decreto sicurezza, ma tutti lo chiamano decreto cortei.",
     "Da ieri in Italia c'è una nuova legge. Si chiama decreto sicurezza, ma tutti lo chiamano decreto cortei.", "intro"),
    ("È nato in 48 ore, dopo i saccheggi di Milano. E contiene misure mai viste sui minori.",
     "È nato in quarantotto ore, dopo i saccheggi di Milano. E contiene misure mai viste sui minori.", "milano"),
    ("Nasce un nuovo reato, la partecipazione violenta a una manifestazione: da 2 a 5 anni. Il fermo preventivo si estende ai quattordicenni. E dai 14 anni i ragazzi diventano imputabili, fino a prova contraria.",
     "Nasce un nuovo reato, la partecipazione violenta a una manifestazione: da due a cinque anni. Il fermo preventivo si estende ai quattordicenni. E dai quattordici anni i ragazzi diventano imputabili, fino a prova contraria.", "misure"),
    ("Ma è costituzionale? I punti delicati sono quattro.",
     "Ma è costituzionale? I punti delicati sono quattro.", "domanda"),
    ("Il fermo. La Costituzione dice che la libertà si può limitare solo con un atto del giudice. Il fermo preventivo, invece, lo decide la polizia.",
     "Il fermo. La Costituzione dice che la libertà si può limitare solo con un atto del giudice. Il fermo preventivo, invece, lo decide la polizia.", "p1"),
    ("I minori. Finora era il giudice a dover dimostrare che un ragazzo era capace di intendere e di volere. Ora tocca alla difesa provare il contrario.",
     "I minori. Finora era il giudice a dover dimostrare che un ragazzo era capace di intendere e di volere. Ora tocca alla difesa provare il contrario.", "p2"),
    ("L'urgenza. Il decreto legge è per i casi urgenti. Ma questa norma era già in un disegno di legge, fermo da mesi in Parlamento.",
     "L'urgenza. Il decreto legge è per i casi urgenti. Ma questa norma era già in un disegno di legge, fermo da mesi in Parlamento.", "p3"),
    ("La piazza. Il diritto di riunirsi resta, e la linea tra chi devasta e chi manifesta deve restare netta.",
     "La piazza. Il diritto di riunirsi resta, e la linea tra chi devasta e chi manifesta deve restare netta.", "p4"),
    ("Il governo risponde che la violenza è stata reale, e che la presunzione si può superare con la prova contraria. Manifestare è un diritto, devastare no.",
     "Il governo risponde che la violenza è stata reale, e che la presunzione si può superare con la prova contraria. Manifestare è un diritto, devastare no.", "governo"),
    ("Ora il Parlamento ha 60 giorni per cambiarlo. Fino ad allora è legge. Ma su quattro punti cammina su un filo sottile. E su quel filo c'è la libertà di un quattordicenne.",
     "Ora il Parlamento ha sessanta giorni per cambiarlo. Fino ad allora è legge. Ma su quattro punti cammina su un filo sottile. E su quel filo c'è la libertà di un quattordicenne.", "parlamento"),
    ("Io sono ParrhesIA. E dico le cose come stanno.",
     "Io sono ParrhesIA. E dico le cose come stanno.", "outro"),
]

# Foto (file, credito in sovrimpressione)
PHOTOS = json.load(open(f"{D}/img/photos.json"))

# ------------------------------------------------------------------ voce
VOICE = "oVJbgLwL0s5pk9e2U6QH"  # Manuela
def tts():
    out_dir = f"{D}/voce"; os.makedirs(out_dir, exist_ok=True)
    ap = f"{out_dir}/align.json"
    if os.path.exists(ap):
        old = json.load(open(ap))
        if [o["spoken"] for o in old] == [s[1] for s in SCENES]: return old
    key = open(f"{D}/.key").read().strip()
    out, prev = [], []
    for i, (sub, spk, _) in enumerate(SCENES):
        assert len(sub.split()) == len(spk.split()), (i, sub, spk)
        body = {"text": spk, "model_id": "eleven_multilingual_v2", "language_code": "it",
                "voice_settings": {"stability": 0.5, "similarity_boost": 0.8, "style": 0.25, "use_speaker_boost": True}}
        if prev: body["previous_request_ids"] = prev[-3:]
        req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_128",
                                     data=json.dumps(body).encode(), headers={"xi-api-key": key, "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=180) as r:
            rid = r.headers.get("request-id"); j = json.loads(r.read())
        if rid: prev.append(rid)
        open(f"{out_dir}/s{i}.mp3", "wb").write(base64.b64decode(j["audio_base64"]))
        a = j["alignment"]
        out.append({"sub": sub, "spoken": spk, "chars": a["characters"], "start": a["character_start_times_seconds"],
                    "end": a["character_end_times_seconds"]})
        print("voce", i, "ok", flush=True)
    json.dump(out, open(ap, "w"), ensure_ascii=False)
    return out

def word_times(al):
    """Inizio/fine di ogni parola del parlato, dai tempi dei caratteri."""
    chars, st, en = al["chars"], al["start"], al["end"]
    words, cur, cs = [], None, None
    for c, s, e in zip(chars, st, en):
        if c.isspace():
            if cur is not None: words.append((cs, ce)); cur = None
        else:
            if cur is None: cur, cs = "", s
            cur += c; ce = e
    if cur is not None: words.append((cs, ce))
    return words

def dur(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]).decode())

# ------------------------------------------------------------------ tempi
GAP = 0.35
def timeline(dummy):
    T, t = [], 0.6
    if dummy:
        for sub, spk, sc in SCENES:
            n = len(spk.split()); d = n * 0.36
            ws = [(t + i * 0.36, t + i * 0.36 + 0.3) for i in range(n)]
            T.append(dict(scene=sc, sub=sub, t0=t, t1=t + d, words=ws, audio=None)); t += d + GAP
    else:
        al = tts()
        for i, ((sub, spk, sc), a) in enumerate(zip(SCENES, al)):
            p = f"{D}/voce/s{i}.mp3"; d = dur(p)
            ws = [(t + s, t + e) for s, e in word_times(a)]
            assert len(ws) == len(sub.split()), (i, len(ws), len(sub.split()))
            T.append(dict(scene=sc, sub=sub, t0=t, t1=t + d, words=ws, audio=p)); t += d + GAP
    return T, t + 1.2

# ------------------------------------------------------------------ disegno
def ease(x): x = max(0, min(1, x)); return 1 - (1 - x) ** 3
def lerp(a, b, x): return a + (b - a) * x

random.seed(7)
GRAIN = [Image.effect_noise((W // 2, H // 2), 40).resize((W, H)).convert("L") for _ in range(4)]
def grain(im, k):
    g = GRAIN[k % 4]
    return Image.composite(im, Image.new("RGB", (W, H), (0, 0, 0)), ImageOps.invert(g).point(lambda v: 255 - v // 7))

_ph = {}
def photo(name):
    if name not in _ph:
        im = Image.open(f"{D}/img/{PHOTOS[name]['file']}").convert("RGB")
        im = ImageEnhance.Color(im).enhance(0.25); im = ImageEnhance.Contrast(im).enhance(1.15)
        _ph[name] = im
    return _ph[name]

def kenburns(name, x, focus=(0.5, 0.5), z0=1.0, z1=1.12, darken=0.55):
    im = photo(name); iw, ih = im.size
    s = max(W / iw, H / ih) * lerp(z0, z1, x)
    cw, ch = W / s, H / s
    cx = min(max(focus[0] * iw, cw / 2), iw - cw / 2); cy = min(max(focus[1] * ih, ch / 2), ih - ch / 2)
    box = (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)
    fr = im.resize((W, H), Image.BILINEAR, box=box)
    fr = Image.blend(fr, Image.new("RGB", (W, H), BG), darken)
    # gradiente in basso per i sottotitoli
    g = Image.linear_gradient("L").resize((W, H)).point(lambda v: int(max(0, v - 90) * 1.6))
    return Image.composite(Image.new("RGB", (W, H), BG), fr, g)

def ctext(d, cx, y, txt, f, fill, anchor="ma"):
    d.text((cx, y), txt, font=f, fill=fill, anchor=anchor)

def wrap(d, txt, f, maxw):
    out, cur = [], ""
    for w in txt.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) > maxw and cur: out.append(cur); cur = w
        else: cur = t
    if cur: out.append(cur)
    return out

def stamp(im, txt, cx, cy, size, x, rot=-4, color=RED):
    """Scritta a timbro con bordo, che entra scalando."""
    f = F(BLACK, size)
    tmp = Image.new("RGBA", (W, int(size * 1.6)), (0, 0, 0, 0)); d = ImageDraw.Draw(tmp)
    tw = d.textlength(txt, font=f)
    pad = size * 0.18
    d.rectangle([W / 2 - tw / 2 - pad, size * 0.18, W / 2 + tw / 2 + pad, size * 1.42], outline=color + (255,), width=max(6, size // 14))
    d.text((W / 2, size * 0.8), txt, font=f, fill=color + (255,), anchor="mm")
    # effetto consumato
    rnd = random.Random(len(txt))
    for _ in range(int(tw * 0.9)):
        px, py = rnd.uniform(W / 2 - tw / 2 - pad, W / 2 + tw / 2 + pad), rnd.uniform(0, size * 1.6)
        d.ellipse([px, py, px + rnd.uniform(2, 7), py + rnd.uniform(2, 7)], fill=(0, 0, 0, 0))
    sc = lerp(1.6, 1.0, ease(x * 2.2)); a = int(255 * ease(x * 3))
    tmp = tmp.rotate(rot, resample=Image.BICUBIC, expand=False)
    tmp = tmp.resize((int(W * sc), int(tmp.height * sc)), Image.BICUBIC)
    if a < 255: tmp.putalpha(tmp.getchannel("A").point(lambda v: v * a // 255))
    im.paste(tmp, (int(cx - tmp.width / 2), int(cy - tmp.height / 2)), tmp)

def logo(d, cx, y, size, a=1.0):
    f = F(BLACK, size)
    A, B = "PARRHES", "IA"
    wa, wb = d.textlength(A, font=f), d.textlength(B, font=f)
    x = cx - (wa + wb) / 2
    col = lambda c: tuple(int(lerp(BG[i], c[i], a)) for i in range(3))
    d.text((x, y), A, font=f, fill=col(INK)); d.text((x + wa, y), B, font=f, fill=col(RED))

def credit(d, name):
    c = PHOTOS[name]["credit"]; f = F(INTER_M, 22)
    d.text((W - 40, 150), c, font=f, fill=(200, 200, 200), anchor="ra")

def ai_label(d):
    f = F(INTER_SB, 24)
    d.rounded_rectangle([40, 60, 40 + d.textlength("Contenuto generato con IA", font=f) + 64, 108], radius=24, fill=(22, 22, 22), outline=LINE, width=2)
    d.ellipse([60, 77, 74, 91], fill=RED)
    d.text((88, 84), "Contenuto generato con IA", font=f, fill=MUTED, anchor="lm")
    logo(d, W - 40 - ImageDraw.Draw(Image.new("RGB", (1, 1))).textlength("PARRHESIA", font=F(BLACK, 44)) / 2 - 2, 62, 44)

def subtitles(d, seg, t):
    """Sottotitolo a righe, con la parola pronunciata evidenziata in rosso."""
    words = seg["sub"].split(); ws = seg["words"]
    f = F(INTER_B, 50); maxw = W - 140
    # dividi in blocchi da max 2 righe
    lines = wrap(d, seg["sub"], f, maxw)
    blocks, cur = [], []
    for ln in lines:
        cur.append(ln)
        if len(cur) == 2 or ln.endswith((".", "?", ":")): blocks.append(cur); cur = []
    if cur: blocks.append(cur)
    idx, bi = 0, []
    for b in blocks:
        n = sum(len(l.split()) for l in b); bi.append((idx, idx + n)); idx += n
    k = None
    for j, (a, b) in enumerate(bi):
        if ws[a][0] - 0.05 <= t: k = j
    if k is None: return
    a, b = bi[k]
    if t > ws[b - 1][1] + 0.6 and k == len(bi) - 1 and t > seg["t1"] + 0.1: return
    y0 = 1500; wi = a
    for li, ln in enumerate(blocks[k]):
        lw = d.textlength(ln, font=f); x = W / 2 - lw / 2; y = y0 + li * 68
        for w in ln.split():
            s, e = ws[wi]
            col = RED if s - 0.04 <= t <= e + 0.12 else (INK if t >= s else (170, 170, 170))
            d.text((x + 3, y + 3), w, font=f, fill=(0, 0, 0)); d.text((x, y), w, font=f, fill=col)
            x += d.textlength(w + " ", font=f); wi += 1

# ---- scene: ogni funzione riceve (im, d, x, lt, seg) con x = avanzamento 0..1 e lt = tempo locale
def sc_intro(im, d, x, lt, seg):
    d.text((W / 2, 520), "DA IERI", font=F(XB, 90), fill=MUTED, anchor="mm")
    stamp(im, "IN VIGORE", W / 2, 700, 210, lt / 1.2)
    if lt > 2.6:
        a = ease((lt - 2.6) / 0.6)
        f = F(BLACK, 130)
        d.text((W / 2, 980), "DECRETO", font=f, fill=tuple(int(lerp(BG[i], INK[i], a)) for i in range(3)), anchor="mm")
        d.text((W / 2, 1110), "CORTEI", font=f, fill=tuple(int(lerp(BG[i], RED[i], a)) for i in range(3)), anchor="mm")
        f2 = F(INTER_M, 34)
        d.text((W / 2, 1220), "dl \"Sicurezza pubblica e criminalità minorile\"", font=f2, fill=tuple(int(lerp(BG[i], MUTED[i], a)) for i in range(3)), anchor="mm")

def cracks(d, x, seed=3):
    rnd = random.Random(seed); cx, cy = 560, 760
    n = int(14 * ease(x * 1.5))
    for i in range(n):
        ang = rnd.uniform(0, 2 * math.pi); L = rnd.uniform(220, 520); px, py = cx, cy
        for s in range(6):
            ang += rnd.uniform(-0.5, 0.5); nx, ny = px + math.cos(ang) * L / 6, py + math.sin(ang) * L / 6
            d.line([px, py, nx, ny], fill=(235, 235, 235), width=3); px, py = nx, ny

def sc_milano(im, d, x, lt, seg):
    im.paste(kenburns("duomo", x, (0.5, 0.45), darken=0.5)); d = ImageDraw.Draw(im)
    cracks(d, lt / 2.0)
    stamp(im, "48 ORE", W / 2, 520, 230, lt / 1.0, rot=3)
    if lt > 2.0:
        a = ease((lt - 2.0) / 0.5)
        f = F(BLACK, 92); col = tuple(int(lerp(40, 240, a)) for _ in range(3))
        d.text((W / 2, 1100), "MISURE MAI VISTE", font=f, fill=col, anchor="mm")
        d.text((W / 2, 1200), "SUI MINORI", font=f, fill=tuple(int(lerp(BG[i], RED[i], a)) for i in range(3)), anchor="mm")
    credit(d, "duomo")
    return d

def card(d, y, a, big, small, num):
    x0 = lerp(-900, 70, ease(a)); w = 940
    d.rounded_rectangle([x0, y, x0 + w, y + 250], radius=18, fill=(24, 24, 24), outline=LINE, width=2)
    d.rectangle([x0, y, x0 + 14, y + 250], fill=RED)
    d.text((x0 + 60, y + 30), num, font=F(BOLD, 40), fill=RED)
    d.text((x0 + 60, y + 72), big, font=F(BLACK, 92), fill=INK)
    d.text((x0 + 62, y + 182), small, font=F(INTER_SB, 38), fill=MUTED)

def sc_misure(im, d, x, lt, seg):
    d.text((W / 2, 300), "COSA CAMBIA", font=F(XB, 80), fill=MUTED, anchor="mm")
    ws = seg["words"]; t0 = seg["t0"]
    def at(i): return ws[i][0] - t0
    # 0 Nasce · 15 Il (fermo) · 22 E (dai 14)
    card(d, 420, (lt - at(0) + 0.2) / 0.6, "NUOVO REATO", "da 2 a 5 anni", "01")
    card(d, 710, (lt - at(15) + 0.2) / 0.6, "FERMO PREVENTIVO", "anche a 14 anni", "02")
    card(d, 1000, (lt - at(22) + 0.2) / 0.6, "IMPUTABILI A 14 ANNI", "fino a prova contraria", "03")

def sc_domanda(im, d, x, lt, seg):
    # la Costituzione che si apre: due pagine che ruotano
    a = ease(lt / 1.4)
    cx, cy, bw, bh = W / 2, 720, 330, 460
    open_w = bw * a
    d.rectangle([cx - open_w - 8, cy - bh / 2, cx - 4, cy + bh / 2], fill=(232, 226, 210))
    d.rectangle([cx + 4, cy - bh / 2, cx + 4 + max(open_w, 30), cy + bh / 2], fill=(240, 235, 220) if a > 0.5 else (120, 20, 20))
    if a < 0.5:
        d.rectangle([cx + 4, cy - bh / 2, cx + 4 + bw * (1 - a * 2), cy + bh / 2], fill=(150, 24, 24))
        d.text((cx + 4 + bw * (1 - a * 2) / 2, cy), "COSTITUZIONE", font=F(BOLD, 34), fill=(240, 220, 200), anchor="mm")
    else:
        for i in range(9):
            yy = cy - bh / 2 + 60 + i * 42
            d.line([cx - open_w + 30, yy, cx - 30, yy], fill=(160, 150, 130), width=5)
            d.line([cx + 30, yy, cx + open_w - 30, yy], fill=(160, 150, 130), width=5)
        d.text((cx - open_w / 2, cy - bh / 2 + 22), "Art.", font=F(BOLD, 30), fill=(120, 20, 20), anchor="ma")
    if lt > 1.0:
        aa = ease((lt - 1.0) / 0.5)
        d.text((W / 2, 1110), "È COSTITUZIONALE?", font=F(BLACK, 120), fill=tuple(int(lerp(BG[i], INK[i], aa)) for i in range(3)), anchor="mm")
    ws = seg["words"]
    if lt > ws[3][0] - seg["t0"] - 0.1:
        stamp(im, "4 PUNTI DELICATI", W / 2, 1290, 110, (lt - (ws[3][0] - seg["t0"])) / 0.8, rot=-2)

PUNTI = {"p1": ("1", "IL FERMO", "Art. 13", "la libertà si limita solo\ncon un atto del giudice", "DECIDE LA POLIZIA,\nNON IL GIUDICE"),
         "p2": ("2", "I MINORI", "Artt. 27 e 31", "la capacità del minore\nora si presume", "PROVA A CARICO\nDELLA DIFESA"),
         "p3": ("3", "L'URGENZA", "Art. 77", "il decreto legge serve\nper i casi urgenti", "GIÀ IN UN DDL\nFERMO DA MESI"),
         "p4": ("4", "LA PIAZZA", "Artt. 17 e 21", "il diritto di riunirsi\npacificamente resta", "CHI DEVASTA NON È\nCHI MANIFESTA")}

def sc_punto(im, d, x, lt, seg, k):
    n, tit, art, txt, verdict = PUNTI[k]
    a = ease(lt / 0.5)
    d.text((140, 330), n, font=F(BLACK, int(lerp(200, 360, a))), fill=RED, anchor="lm")
    d.text((380, 290), tit, font=F(BLACK, 110), fill=INK)
    d.text((384, 410), art.upper(), font=F(BOLD, 52), fill=MUTED)
    d.line([80, 520, lerp(80, W - 80, ease(lt / 1.0)), 520], fill=LINE, width=4)
    if lt > 0.9:
        aa = ease((lt - 0.9) / 0.6)
        for i, ln in enumerate(txt.split("\n")):
            d.text((90, 590 + i * 74), ln, font=F(INTER_SB, 58), fill=tuple(int(lerp(BG[j], INK[j], aa)) for j in range(3)))
    ws = seg["words"]; mid = ws[len(ws) * 3 // 5][0] - seg["t0"]
    if lt > mid:
        vl = verdict.split("\n")
        for i, ln in enumerate(vl):
            stamp(im, ln, W / 2, 1000 + i * 150, 96, (lt - mid) / 0.8, rot=-3 + i * 2)

def sc_governo(im, d, x, lt, seg):
    im.paste(kenburns("meloni", x, PHOTOS["meloni"].get("focus", (0.5, 0.4)), z0=1.02, z1=1.1, darken=0.35)); d = ImageDraw.Draw(im)
    d.rectangle([0, 220, W, 300], fill=(14, 14, 14))
    d.text((70, 260), "LA RISPOSTA DEL GOVERNO", font=F(XB, 62), fill=INK, anchor="lm")
    d.rectangle([0, 220, 18, 300], fill=RED)
    ws = seg["words"]; q = ws[len(ws) - 6][0] - seg["t0"]
    if lt > q - 0.2:
        aa = ease((lt - q + 0.2) / 0.5)
        y = 1080
        d.rectangle([70, y - 20, W - 70, y + 260], fill=(14, 14, 14))
        d.text((110, y), "«MANIFESTARE È UN DIRITTO,", font=F(BLACK, 70), fill=tuple(int(lerp(14, INK[i], aa)) for i in range(3)))
        d.text((110, y + 86), "DEVASTARE LE NOSTRE CITTÀ NO»", font=F(BLACK, 70), fill=tuple(int(lerp(14, RED[i], aa)) for i in range(3)))
        d.text((112, y + 190), "Giorgia Meloni, presidente del Consiglio", font=F(INTER_M, 32), fill=MUTED)
    credit(d, "meloni")
    return d

def sc_parlamento(im, d, x, lt, seg):
    im.paste(kenburns("montecitorio", x, (0.5, 0.5), darken=0.55)); d = ImageDraw.Draw(im)
    ws = seg["words"]; t0 = seg["t0"]
    # contatore 60 giorni
    a = ease(lt / 1.6); n = int(round(lerp(0, 60, a)))
    d.text((W / 2, 520), f"{n}", font=F(BLACK, 330), fill=INK, anchor="mm")
    d.text((W / 2, 720), "GIORNI PER CONVERTIRLO", font=F(XB, 68), fill=RED, anchor="mm")
    # filo sottile (dalla parola "Ma")
    fi = next(i for i, w in enumerate(seg["sub"].split()) if w == "Ma")
    tf = ws[fi][0] - t0
    if lt > tf:
        aa = ease((lt - tf) / 1.2); y = 1000
        xs = lerp(80, W - 80, aa)
        pts = [(xx, y + math.sin(xx / 60 + lt * 3) * 6) for xx in range(80, int(xs), 8)]
        if len(pts) > 1: d.line(pts, fill=RED, width=4)
        for i, pos in enumerate([0.2, 0.4, 0.6, 0.8]):
            if aa > pos:
                px = lerp(80, W - 80, pos); d.ellipse([px - 16, y - 16, px + 16, y + 16], fill=INK)
                d.text((px, y - 60), str(i + 1), font=F(BLACK, 52), fill=INK, anchor="mm")
        d.text((W / 2, 1120), "UN FILO SOTTILE", font=F(BLACK, 96), fill=tuple(int(lerp(BG[i], INK[i], aa)) for i in range(3)), anchor="mm")
    credit(d, "montecitorio")
    return d

def sc_outro(im, d, x, lt, seg):
    a = ease(lt / 0.8)
    logo(d, W / 2, 700, 190, a)
    if lt > 1.2:
        aa = ease((lt - 1.2) / 0.6)
        d.text((W / 2, 980), "E DICO LE COSE COME STANNO.", font=F(XB, 64), fill=tuple(int(lerp(BG[i], INK[i], aa)) for i in range(3)), anchor="mm")
        d.text((W / 2, 1080), "Articolo completo con le fonti su parrhesia-ia.com", font=F(INTER_M, 36), fill=tuple(int(lerp(BG[i], MUTED[i], aa)) for i in range(3)), anchor="mm")

SC = {"intro": sc_intro, "milano": sc_milano, "misure": sc_misure, "domanda": sc_domanda, "governo": sc_governo,
      "parlamento": sc_parlamento, "outro": sc_outro}
for k in PUNTI: SC[k] = (lambda kk: (lambda im, d, x, lt, seg: sc_punto(im, d, x, lt, seg, kk)))(k)

def frame(T, total, t, fi):
    k = 0
    for i, s in enumerate(T):
        if t >= s["t0"] - GAP / 2: k = i
    seg = T[k]
    nxt = T[k + 1]["t0"] - GAP / 2 if k + 1 < len(T) else total
    st = seg["t0"] - GAP / 2 if k else 0
    x = (t - st) / max(0.01, nxt - st); lt = t - st
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    r = SC[seg["scene"]](im, d, x, lt, seg)
    d = ImageDraw.Draw(im)
    # dissolvenza d'ingresso di ogni scena
    if lt < 0.18 and k: im = Image.blend(Image.new("RGB", (W, H), BG), im, lt / 0.18); d = ImageDraw.Draw(im)
    ai_label(d)
    subtitles(d, seg, t)
    return grain(im, fi // 2)

def main():
    dummy = "--dummy" in sys.argv
    T, total = timeline(dummy)
    out = f"{D}/out"; os.makedirs(out, exist_ok=True)
    if "--frames" in sys.argv:
        for tt in [float(v) for v in sys.argv[sys.argv.index("--frames") + 1].split(",")]:
            frame(T, total, tt, 0).save(f"{out}/f_{tt:05.1f}.png")
        print("scene:", [(s["scene"], round(s["t0"], 1)) for s in T], "totale", round(total, 1)); return
    # audio: voce con pause
    if not dummy:
        parts, filt = [], []
        for i, s in enumerate(T):
            parts += ["-i", s["audio"]]; filt.append(f"[{i}:a]adelay={int(s['t0'] * 1000)}|{int(s['t0'] * 1000)},aformat=channel_layouts=stereo[a{i}]")
        mix = "".join(f"[a{i}]" for i in range(len(T)))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *parts, "-filter_complex",
                        ";".join(filt) + f";{mix}amix=inputs={len(T)}:normalize=0,apad,atrim=0:{total},loudnorm=I=-15:TP=-1.5[out]",
                        "-map", "[out]", "-ar", "44100", f"{out}/voce.wav"], check=True)
    n = int(total * FPS)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-"]
    if not dummy: cmd += ["-i", f"{out}/voce.wav", "-c:a", "aac", "-b:a", "192k", "-shortest"]
    cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium", "-movflags", "+faststart",
            f"{out}/ParrhesIA_07_decreto_cortei{'_bozza' if dummy else ''}.mp4"]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for fi in range(n):
        p.stdin.write(frame(T, total, fi / FPS, fi).tobytes())
        if fi % 300 == 0: print("frame", fi, "/", n, flush=True)
    p.stdin.close(); p.wait()
    print("fatto", round(total, 1), "s")

if __name__ == "__main__":
    main()
