"""Template caroselli ParrhesIA, 1080x1350 (4:5). Prova: decreto cortei."""
import os, random
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps

D = os.path.dirname(os.path.abspath(__file__)); OUT = f"{D}/out/carosello"; os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1350
BG = (14, 14, 14); BG2 = (24, 24, 24); INK = (240, 238, 234); MUTED = (154, 154, 154); RED = (214, 38, 38); LINE = (46, 46, 46)
def F(n, s): return ImageFont.truetype(n if n.startswith("/") else f"{D}/fonts/{n}.ttf", s)
BLACK, XB, BOLD = "BarlowCondensed-Black", "BarlowCondensed-ExtraBold", "BarlowCondensed-Bold"
IB, ISB, IM, IR = [f"/usr/share/fonts/opentype/inter/Inter-{w}.otf" for w in ("Bold", "SemiBold", "Medium", "Regular")]
N = 8

random.seed(3)
GR = Image.effect_noise((W // 2, H // 2), 40).resize((W, H)).convert("L")
def grain(im):
    return Image.composite(im, Image.new("RGB", (W, H), (0, 0, 0)), ImageOps.invert(GR).point(lambda v: 255 - v // 7))

def wrap(d, t, f, mw):
    out, cur = [], ""
    for w in t.split():
        x = (cur + " " + w).strip()
        if d.textlength(x, font=f) > mw and cur: out.append(cur); cur = w
        else: cur = x
    if cur: out.append(cur)
    return out

def para(d, x, y, t, f, fill, mw, lh=1.32):
    for ln in wrap(d, t, f, mw): d.text((x, y), ln, font=f, fill=fill); y += f.size * lh
    return y

def logo(d, x, y, s):
    f = F(BLACK, s); d.text((x, y), "PARRHES", font=f, fill=INK); d.text((x + d.textlength("PARRHES", font=f), y), "IA", font=f, fill=RED)

def stamp(im, txt, cx, cy, size, rot=-4):
    f = F(BLACK, size); tmp = Image.new("RGBA", (W, int(size * 1.7)), (0, 0, 0, 0)); d = ImageDraw.Draw(tmp)
    tw = d.textlength(txt, font=f); pad = size * .18
    d.rectangle([W/2 - tw/2 - pad, size*.2, W/2 + tw/2 + pad, size*1.45], outline=RED + (255,), width=max(5, size // 14))
    d.text((W/2, size*.82), txt, font=f, fill=RED + (255,), anchor="mm")
    r = random.Random(len(txt))
    for _ in range(int(tw)):
        px, py = r.uniform(W/2 - tw/2 - pad, W/2 + tw/2 + pad), r.uniform(0, size*1.7)
        d.ellipse([px, py, px + r.uniform(2, 6), py + r.uniform(2, 6)], fill=(0, 0, 0, 0))
    tmp = tmp.rotate(rot, resample=Image.BICUBIC)
    im.paste(tmp, (int(cx - W/2), int(cy - tmp.height/2)), tmp)

def frame(i, rubrica=None, fonte=None):
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    logo(d, 64, 52, 46)
    d.text((W - 64, 60), f"{i}/{N}", font=F(BOLD, 36), fill=MUTED, anchor="ra")
    if rubrica:
        f = F(XB, 34); tw = d.textlength(rubrica.upper(), font=f)
        d.rectangle([64, 128, 64 + tw + 36, 176], fill=RED); d.text((82, 152), rubrica.upper(), font=f, fill=INK, anchor="lm")
    d.line([64, H - 110, W - 64, H - 110], fill=LINE, width=2)
    if fonte: d.text((64, H - 80), "Fonti: " + fonte, font=F(IM, 24), fill=MUTED)
    d.text((W - 64, H - 80), "parrhesia-ia.com", font=F(ISB, 24), fill=INK, anchor="ra")
    if i < N: d.text((W - 64, H - 160), "SCORRI  ›", font=F(IB, 28), fill=RED, anchor="ra")
    return im, d

def photo_bg(path, darken=.6):
    p = Image.open(path).convert("RGB"); p = ImageEnhance.Color(p).enhance(.2)
    s = max(W / p.width, H / p.height); p = p.resize((int(p.width*s)+1, int(p.height*s)+1))
    x, y = (p.width - W)//2, (p.height - H)//2; p = p.crop((x, y, x + W, y + H))
    p = Image.blend(p, Image.new("RGB", (W, H), BG), darken)
    g = Image.linear_gradient("L").resize((W, H)).point(lambda v: int(max(0, v - 60) * 1.3))
    return Image.composite(Image.new("RGB", (W, H), BG), p, g)

slides = []

# 1 · copertina
im, d = frame(1, fonte="Consiglio dei ministri, 20/10/2026")
im.paste(photo_bg(f"{D}/img/duomo.jpg", .55)); d = ImageDraw.Draw(im); logo(d, 64, 52, 46)
d.text((W - 64, 60), f"1/{N}", font=F(BOLD, 36), fill=MUTED, anchor="ra")
stamp(im, "IN VIGORE", W/2 - 150, 420, 120, rot=-5)
d = ImageDraw.Draw(im)
y = 600
for ln, c in [("IL DECRETO", INK), ("CORTEI È", INK), ("COSTITUZIONALE?", RED)]:
    d.text((64, y), ln, font=F(BLACK, 150), fill=c); y += 150
d.text((66, y + 30), "Cosa prevede e i 4 punti che dividono i giuristi", font=F(ISB, 38), fill=INK)
d.text((64, H - 80), "Foto: Leonhard Lenz, Wikimedia Commons, CC0", font=F(IM, 22), fill=MUTED)
d.text((W - 64, H - 160), "SCORRI  ›", font=F(IB, 28), fill=RED, anchor="ra")
slides.append(im)

# 2 · la notizia
im, d = frame(2, "La notizia", "ANSA, Askanews, 20-22/10/2026")
d.text((64, 230), "DA IERI È LEGGE", font=F(BLACK, 110), fill=INK)
y = para(d, 64, 380, "Dopo i saccheggi di Milano del 17 e 18 ottobre, il governo ha approvato in 48 ore un nuovo decreto sicurezza. Mattarella lo ha firmato il 22 ottobre ed è in vigore dal 23.", F(IM, 42), INK, W - 128)
d.rounded_rectangle([64, y + 40, W - 64, y + 250], radius=16, fill=BG2, outline=LINE, width=2)
d.rectangle([64, y + 40, 78, y + 250], fill=RED)
para(d, 110, y + 76, "Titolo ufficiale: «Disposizioni urgenti in materia di sicurezza pubblica e contrasto alla criminalità minorile».", F(IR, 34), MUTED, W - 230)
slides.append(im)

# 3 · i numeri
im, d = frame(3, "I numeri", "ANSA, Adnkronos")
for k, (big, small) in enumerate([("48 ORE", "dai saccheggi al decreto"), ("2-5 ANNI", "per la partecipazione violenta ai cortei"),
                                  ("14 ANNI", "da qui si è imputabili fino a prova contraria"), ("2.000 €", "sanzione massima per minori e genitori"),
                                  ("500", "militari in più a Milano fino al 31/12")]):
    y = 240 + k * 178
    d.text((64, y), big, font=F(BLACK, 120), fill=RED if k % 2 == 0 else INK)
    yy = y + (50 if d.textlength(small, font=F(ISB, 34)) <= W - 564 else 30)
    para(d, 500, yy, small, F(ISB, 34), MUTED, W - 564, 1.2)
    d.line([64, y + 160, W - 64, y + 160], fill=LINE, width=2)
slides.append(im)

# 4 · Detto vs Fatto
im, d = frame(4, "Detto vs Fatto", "Adnkronos, testo del decreto")
for col, (lab, colr, txt) in enumerate([("DETTO", MUTED, "Il governo: la presunzione di imputabilità è relativa, si può sempre provare il contrario."),
                                         ("FATTO", RED, "Vero. Ma prima era il giudice a dover dimostrare che un 14enne era capace di intendere e di volere. Ora è la difesa a dover dimostrare che non lo era.")]):
    x0 = 64 + col * 488; x1 = x0 + 464
    d.rounded_rectangle([x0, 240, x1, 1120], radius=18, fill=BG2, outline=colr if col else LINE, width=3)
    d.text((x0 + 36, 270), lab, font=F(BLACK, 96), fill=colr)
    para(d, x0 + 36, 410, txt, F(ISB if col else IM, 38), INK, x1 - x0 - 72)
d.text((64, 1150), "Il governo · la norma", font=F(IM, 26), fill=MUTED)
slides.append(im)

# 5 · i 4 dubbi
im, d = frame(5, "I 4 dubbi", "ItaliaOggi, LaPresse, Il Politico Web")
for k, (art, t) in enumerate([("ART. 13", "Il fermo lo decide la polizia, non il giudice"), ("ARTT. 27 E 31", "Per i minori la capacità ora si presume"),
                              ("ART. 77", "Era già in un ddl fermo in Parlamento: dov'è l'urgenza?"), ("ARTT. 17 E 21", "Il divieto di radunarsi tocca il diritto di riunione")]):
    y = 240 + k * 220
    d.ellipse([64, y, 154, y + 90], fill=RED); d.text((109, y + 45), str(k + 1), font=F(BLACK, 64), fill=INK, anchor="mm")
    d.text((190, y - 6), art, font=F(BOLD, 40), fill=MUTED)
    para(d, 190, y + 44, t, F(ISB, 42), INK, W - 260, 1.2)
slides.append(im)

# 6 · Il conto per l'Italia
im, d = frame(6, "Il conto per l'Italia", "Adnkronos, Sky TG24")
d.text((64, 230), "COSA CAMBIA", font=F(BLACK, 110), fill=INK)
d.text((64, 340), "PER UNA FAMIGLIA", font=F(BLACK, 110), fill=RED)
for k, t in enumerate(["Un figlio di 14 anni, se ritenuto pericoloso, può essere fermato prima di un corteo o ricevere dal questore il divieto di radunarsi.",
                       "Se fa danni durante una manifestazione, la multa può arrivare a 2.000 euro, anche per i genitori.",
                       "Chi partecipa a un corteo pacifico non commette reato: il nuovo reato riguarda gruppi violenti e armati."]):
    y = 520 + k * 210
    d.rectangle([64, y + 8, 76, y + 150], fill=RED if k < 2 else MUTED)
    para(d, 110, y, t, F(IM, 40), INK, W - 180)
slides.append(im)

# 7 · La domanda di ParrhesIA
im, d = frame(7, None, None)
d.rectangle([0, 0, W, H], fill=RED); d = ImageDraw.Draw(im)
d.text((64, 60), "LA DOMANDA DI", font=F(BLACK, 60), fill=BG); d.text((64, 120), "PARRHESIA", font=F(BLACK, 130), fill=INK)
d.text((40, 250), "?", font=F(BLACK, 900), fill=(190, 30, 30))
para(d, 64, 470, "Un quattordicenne che sbaglia in piazza deve rispondere come un adulto?", F(BLACK, 104), INK, W - 128, 1.02)
d.line([64, H - 260, W - 64, H - 260], fill=(240, 160, 150), width=2)
para(d, 64, H - 230, "Scrivilo nei commenti: leggiamo tutto, e le risposte più interessanti finiscono nel prossimo video.", F(IM, 32), (250, 225, 220), W - 128)
d.text((W - 64, H - 80), f"7/{N}", font=F(BOLD, 36), fill=INK, anchor="ra")
slides.append(im)

# 8 · chiusura
im, d = frame(8, None, None)
logo(d, 64, 330, 170)
d.text((66, 540), "E DICO LE COSE COME STANNO.", font=F(XB, 64), fill=INK)
para(d, 66, 660, "Articolo completo, con tutte le fonti:", F(IM, 40), MUTED, W - 128)
d.text((66, 730), "parrhesia-ia.com", font=F(BLACK, 96), fill=RED)
d.rounded_rectangle([64, 920, 600, 990], radius=35, outline=LINE, width=2, fill=BG2)
d.ellipse([90, 946, 108, 964], fill=RED); d.text((124, 955), "Contenuto generato con IA", font=F(ISB, 30), fill=MUTED, anchor="lm")
d.text((66, 1050), "Segui @parrhesia_ia · salva e condividi", font=F(ISB, 36), fill=INK)
slides.append(im)

for k, s in enumerate(slides, 1): grain(s).save(f"{OUT}/slide_{k}.png")
# provino
th = [Image.open(f"{OUT}/slide_{k}.png").resize((324, 405)) for k in range(1, N + 1)]
sh = Image.new("RGB", (4 * 334 + 10, 2 * 415 + 10), "white")
for k, t in enumerate(th): sh.paste(t, (10 + (k % 4) * 334, 10 + (k // 4) * 415))
sh.save(f"{D}/out/carosello_provino.png"); print("ok")
