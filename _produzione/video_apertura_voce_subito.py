"""ParrhesIA · video 13 "Midterm USA: perché il voto ci riguarda"."""
import sys, os, json, math, subprocess
import make as m
from make import W, H, FPS, BG, INK, MUTED, RED, LINE, F, BLACK, XB, BOLD, INTER_B, INTER_SB, INTER_M, ease, lerp, stamp, logo, kenburns, credit
from PIL import Image, ImageDraw

D = m.D
m.START = 0.3  # la voce parte subito; firma sotto la voce
BLUE = (60, 110, 200); REP = (205, 50, 50)

m.SCENES = [
    ("Martedì 3 novembre gli Stati Uniti votano. Non per il presidente, ma per il Congresso. E il risultato si sentirà anche qui.",
     "Martedì tre novembre gli Stati Uniti votano. Non per il presidente, ma per il Congresso. E il risultato si sentirà anche qui.", "apertura"),
    ("Si rinnovano tutti i 435 seggi della Camera, 35 seggi del Senato e 36 governatori. Oggi i repubblicani hanno la maggioranza in entrambe le Camere.",
     "Si rinnovano tutti i quattrocentotrentacinque seggi della Camera, trentacinque seggi del Senato e trentasei governatori. Oggi i repubblicani hanno la maggioranza in entrambe le Camere.", "cosa"),
    ("Secondo la media dei modelli raccolta da YouTrend, i democratici hanno circa nove probabilità su dieci di conquistare la Camera. Al Senato la partita è più aperta: circa sei su dieci.",
     "Secondo la media dei modelli raccolta da YouTrend, i democratici hanno circa nove probabilità su dieci di conquistare la Camera. Al Senato la partita è più aperta: circa sei su dieci.", "sondaggi"),
    ("Perché conta? Il Congresso approva il bilancio, gli aiuti militari e può indagare sul governo. Con una Camera democratica, Trump dovrebbe trattare su ogni legge.",
     "Perché conta? Il Congresso approva il bilancio, gli aiuti militari e può indagare sul governo. Con una Camera democratica, Trump dovrebbe trattare su ogni legge.", "poteri"),
    ("Per l'Italia e l'Europa i fronti sono tre. L'Ucraina, perché gli aiuti passano dal Congresso. La NATO e la spesa per la difesa. E i dazi: ma quelli Trump li ha decisi soprattutto per decreto, e potrebbero cambiare poco.",
     "Per l'Italia e l'Europa i fronti sono tre. L'Ucraina, perché gli aiuti passano dal Congresso. La NATO e la spesa per la difesa. E i dazi: ma quelli Trump li ha decisi soprattutto per decreto, e potrebbero cambiare poco.", "italia"),
    ("E come da noi, il tema numero uno è il carovita: per quasi tre americani su quattro le spese quotidiane vanno nella direzione sbagliata.",
     "E come da noi, il tema numero uno è il carovita: per quasi tre americani su quattro le spese quotidiane vanno nella direzione sbagliata.", "carovita"),
    ("Mercoledì mattina avremo i primi risultati. E ve li raccontiamo.",
     "Mercoledì mattina avremo i primi risultati. E ve li raccontiamo.", "chiusura"),
    ("Io sono ParrhesIA. E dico le cose come stanno.", "Io sono ParrhesIA. E dico le cose come stanno.", "outro"),
]

def fade(c, a): return tuple(int(lerp(BG[i], c[i], ease(a))) for i in range(3))
def wstart(seg, word):
    for w, (s, e) in zip(seg["sub"].split(), seg["words"]):
        if word.lower() in w.lower(): return s - seg["t0"]
    return 0

def sc_apertura(im, d, x, lt, seg):
    im.paste(kenburns("capitol", x, (0.5, 0.45), darken=0.55)); d = ImageDraw.Draw(im)
    d.text((W / 2, 520), "MIDTERM", font=F(BLACK, 210), fill=fade(INK, lt / .6), anchor="mm")
    d.text((W / 2, 690), "3 NOVEMBRE", font=F(BLACK, 120), fill=fade(RED, (lt - .3) / .6), anchor="mm")
    tc = wstart(seg, "Congresso")
    if lt > tc - .3: stamp(im, "SI VOTA PER IL CONGRESSO", W / 2, 940, 92, (lt - tc + .3) / .7, rot=-3)
    credit(ImageDraw.Draw(im), "capitol")

def sc_cosa(im, d, x, lt, seg):
    d.text((W / 2, 280), "COSA SI VOTA", font=F(BLACK, 140), fill=fade(INK, lt / .5), anchor="mm")
    for i, (k, big, t) in enumerate([("435", "435", "seggi della Camera: tutti"), ("35", "35", "seggi del Senato"), ("36", "36", "governatori")]):
        tk = wstart(seg, k) if i else wstart(seg, "435"); a = (lt - tk + .2) / .5; y = 470 + i * 220
        d.text((90, y), big, font=F(BLACK, 170), fill=fade(INK, a))
        d.text((420, y + 70), t, font=F(INTER_SB, 44), fill=fade(MUTED, a))
    tr = wstart(seg, "repubblicani")
    if lt > tr - .3:
        a = (lt - tr + .3) / .5
        d.rounded_rectangle([80, 1150, W - 80, 1290], radius=16, fill=(24, 24, 24), outline=LINE, width=2)
        d.text((W / 2, 1220), "OGGI: REPUBBLICANI IN MAGGIORANZA", font=F(BLACK, 60), fill=fade(REP, a), anchor="mm")

def prob(d, y, label, p, a):
    d.text((90, y), label, font=F(BLACK, 80), fill=INK)
    bw = W - 180
    d.rectangle([90, y + 110, 90 + bw, y + 200], fill=REP)
    d.rectangle([90, y + 110, 90 + bw * p * ease(a), y + 200], fill=BLUE)
    d.text((110, y + 155), f"DEM {int(round(p * 100 * ease(a)))}%", font=F(BLACK, 60), fill=INK, anchor="lm")
    d.text((W - 110, y + 155), f"REP {100 - int(round(p * 100 * ease(a)))}%", font=F(BLACK, 60), fill=INK, anchor="rm")

def sc_sondaggi(im, d, x, lt, seg):
    d.text((W / 2, 280), "LE PROBABILITÀ", font=F(BLACK, 130), fill=fade(INK, lt / .5), anchor="mm")
    d.text((W / 2, 380), "media dei modelli, YouTrend per Sky TG24", font=F(INTER_SB, 38), fill=fade(MUTED, lt / .5), anchor="mm")
    tc = wstart(seg, "nove")
    if lt > tc - .5: prob(d, 520, "CAMERA", .89, (lt - tc + .5) / 1.2)
    ts = wstart(seg, "Senato")
    if lt > ts - .2: prob(d, 860, "SENATO", .61, (lt - ts + .2) / 1.2)
    d.text((W / 2, 1230), "Probabilità, non certezze", font=F(INTER_M, 34), fill=MUTED, anchor="mm")

def sc_poteri(im, d, x, lt, seg):
    d.text((W / 2, 280), "PERCHÉ CONTA", font=F(BLACK, 140), fill=fade(INK, lt / .5), anchor="mm")
    for i, (k, t) in enumerate([("bilancio", "IL BILANCIO"), ("aiuti", "GLI AIUTI MILITARI"), ("indagare", "LE INDAGINI SUL GOVERNO")]):
        tk = wstart(seg, k); a = ease((lt - tk + .3) / .5); y = 480 + i * 200; x0 = lerp(W, 80, a)
        d.rounded_rectangle([x0, y, x0 + 920, y + 160], radius=16, fill=(24, 24, 24), outline=LINE, width=2)
        d.rectangle([x0, y, x0 + 14, y + 160], fill=BLUE)
        d.text((x0 + 50, y + 80), t, font=F(BLACK, 70), fill=INK, anchor="lm")
    tt = wstart(seg, "trattare")
    if lt > tt - .4: stamp(im, "TRUMP DOVREBBE TRATTARE", W / 2, 1180, 90, (lt - tt + .4) / .6, rot=-2)

def sc_italia(im, d, x, lt, seg):
    d.text((W / 2, 280), "IL CONTO", font=F(BLACK, 140), fill=fade(INK, lt / .5), anchor="mm")
    d.text((W / 2, 410), "PER L'ITALIA", font=F(BLACK, 140), fill=fade(RED, (lt - .2) / .5), anchor="mm")
    for i, (k, t, s) in enumerate([("Ucraina", "UCRAINA", "gli aiuti passano dal Congresso"), ("NATO", "NATO", "la spesa per la difesa"), ("dazi:", "DAZI", "decisi per decreto: cambierebbero poco")]):
        tk = wstart(seg, k); a = (lt - tk + .2) / .5; y = 580 + i * 220
        d.text((90, y), t, font=F(BLACK, 110), fill=fade(INK, a))
        d.text((92, y + 120), s, font=F(INTER_SB, 40), fill=fade(MUTED, a))

def sc_carovita(im, d, x, lt, seg):
    d.text((W / 2, 300), "IL TEMA N. 1", font=F(BLACK, 140), fill=fade(INK, lt / .5), anchor="mm")
    stamp(im, "CAROVITA", W / 2, 520, 160, (lt - .4) / .6, rot=-3)
    d = ImageDraw.Draw(im)
    tq = wstart(seg, "tre")
    if lt > tq - .3:
        a = ease((lt - tq + .3) / 1.0)
        for i in range(4):
            cx = 200 + i * 230; c = RED if i < 3 else (90, 90, 90)
            c = tuple(int(lerp(BG[j], c[j], a)) for j in range(3))
            d.ellipse([cx - 55, 760, cx + 55, 870], fill=c); d.ellipse([cx - 90, 890, cx + 90, 1100], fill=c)
        d.text((W / 2, 1200), "QUASI 3 SU 4: «DIREZIONE SBAGLIATA»", font=F(BLACK, 60), fill=fade(INK, a), anchor="mm")
        d.text((W / 2, 1280), "sondaggio Reuters/Ipsos sulle spese quotidiane", font=F(INTER_M, 32), fill=fade(MUTED, a), anchor="mm")

def sc_chiusura(im, d, x, lt, seg):
    d.text((W / 2, 640), "MERCOLEDÌ MATTINA", font=F(BLACK, 120), fill=fade(INK, lt / .5), anchor="mm")
    d.text((W / 2, 800), "I PRIMI RISULTATI", font=F(BLACK, 120), fill=fade(RED, (lt - .3) / .5), anchor="mm")

def sc_outro(im, d, x, lt, seg): m.sc_outro(im, d, x, lt, seg)
def sc_firma(im, d, x, lt, seg): logo(d, W / 2, 820, 170, ease(lt / 1.2))

m.SC.update({"apertura": sc_apertura, "cosa": sc_cosa, "sondaggi": sc_sondaggi, "poteri": sc_poteri, "italia": sc_italia,
             "carovita": sc_carovita, "chiusura": sc_chiusura, "outro": sc_outro, "firma": sc_firma})

_kb = kenburns
def kenburns(name, x, *a, **k): return _kb(name, max(x, 0.002), *a, **k)  # evita arrotondamenti negativi al fotogramma 0
OUTNAME = "ParrhesIA_13_midterm_PROVA_apertura"
MUSIC = sys.argv[sys.argv.index("--music") + 1] if "--music" in sys.argv else None
def main():
    dummy = "--dummy" in sys.argv
    T, total = m.timeline(dummy)
    total += 2.0
    T[0]["at"] = T[0]["t0"]; T[0]["t0"] = 0.0  # la prima scena si vede dal primo fotogramma
    out = f"{D}/out"; os.makedirs(out, exist_ok=True)
    orig_sub = m.subtitles
    m.subtitles = lambda d, seg, t: orig_sub(d, seg, t) if seg["words"] else None
    if "--frames" in sys.argv:
        for tt in [float(v) for v in sys.argv[sys.argv.index("--frames") + 1].split(",")]:
            m.frame(T, total, tt, 0).save(f"{out}/f_{tt:05.1f}.png")
        print("scene:", [(s["scene"], round(s["t0"], 1)) for s in T], "totale", round(total, 1)); return
    segs = [s for s in T if s["audio"]]
    parts, filt = [], []
    for i, s in enumerate(segs):
        parts += ["-i", s["audio"]]; ms = int(s.get("at", s["t0"]) * 1000); filt.append(f"[{i}:a]adelay={ms}|{ms},aformat=channel_layouts=stereo[a{i}]")
    n = len(segs)
    parts += ["-i", f"{D}/firma.mp3", "-i", f"{D}/firma.mp3", "-stream_loop", "-1", "-i", MUSIC or f"{D}/tappeto.mp3"]
    end_ms = int((total - 4.3) * 1000)
    filt.append(f"[{n}:a]volume=0.45,aformat=channel_layouts=stereo[f1]")
    filt.append(f"[{n+1}:a]adelay={end_ms}|{end_ms},volume=0.8,aformat=channel_layouts=stereo[f2]")
    mix = "".join(f"[a{i}]" for i in range(n))
    filt.append(f"{mix}amix=inputs={n}:normalize=0,apad,atrim=0:{total},loudnorm=I=-15:TP=-1.5,asplit=2[v][sc]")
    filt.append(f"[{n+2}:a]atrim=0:{total},afade=t=in:d=0.3,afade=t=out:st={total-3}:d=3,volume=0.22,aformat=channel_layouts=stereo[bed0]")
    filt.append("[bed0][f1]amix=inputs=2:normalize=0[bed]")
    filt.append("[bed][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[duck]")
    filt.append("[v][duck][f2]amix=inputs=3:normalize=0,alimiter=limit=0.95[out]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *parts, "-filter_complex", ";".join(filt), "-map", "[out]", "-ar", "44100", "-t", str(total), f"{out}/audio.wav"], check=True)
    nf = int(total * FPS)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", f"{out}/audio.wav", "-c:a", "aac", "-b:a", "192k", "-shortest", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
           "-preset", "medium", "-movflags", "+faststart", f"{out}/{OUTNAME}.mp4"]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for fi in range(nf):
        p.stdin.write(m.frame(T, total, fi / FPS, fi).tobytes())
        if fi % 600 == 0: print("frame", fi, "/", nf, flush=True)
    p.stdin.close(); p.wait(); print("fatto", round(total, 1))

if __name__ == "__main__":
    main()
